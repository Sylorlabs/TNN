#!/usr/bin/env python3
"""Round-1 autopsy step 1: independently recompute admitted indices from the
committed self-PAM ledger, verify the ledger's judgments against a fresh
byte-level recomputation of span_sum/8 over the actual F/G blobs, and dump
the admit list with truth metadata.
"""
import struct, hashlib, os, csv

SCRATCH = os.path.dirname(os.path.abspath(__file__))
PAIRS = "/home/hatch/workspace/selfpam_consumer/pairs_full"
TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]

def parse_pair(path):
    data = open(path, "rb").read()
    assert data[:4] == b"R2P1", path
    task, idx, scene, flen, glen, fkind = struct.unpack("<iiQiii", data[4:32])
    assert len(data) == 64 + flen + glen, (path, len(data), flen, glen)
    return task, idx, scene, fkind, data[64:64 + flen], data[64 + flen:]

def span_judgment(blob):
    return (sum(blob) % 2147483648) // 8

def parse_ledger(path):
    entries = []
    for line in open(path):
        line = line.strip()
        if not line.startswith("e "):
            continue
        f = line.split()
        # e idx a b decision hash
        entries.append((int(f[1]), int(f[2]), int(f[3]), int(f[4]), f[5]))
    return entries

def read_truth(task, pidx):
    p = os.path.join(PAIRS, "r2p_%s_%03d.pair.truth" % (TASKS[task], pidx))
    if not os.path.exists(p):
        return None
    d = {}
    for line in open(p):
        k, _, v = line.strip().partition("=")
        d[k] = v
    return d

def main():
    ledgers = [parse_ledger(os.path.join(SCRATCH, "ledger_r%d.txt" % r)) for r in (1, 2, 3)]
    assert len(ledgers[0]) == 1200
    # byte-identical runs: same (idx,a,b,decision) across r1..r3
    for r in (1, 2):
        assert [(e[0], e[1], e[2], e[3]) for e in ledgers[r]] == \
               [(e[0], e[1], e[2], e[3]) for e in ledgers[0]], "run %d differs" % (r + 1)
    print("runs r1/r2/r3: byte-identical entry sequences (1200 each)")

    ent = ledgers[0]
    withheld = sum(1 for e in ent if e[3] == 1)
    admitted = [e for e in ent if e[3] == 0]
    print("withheld=%d admitted=%d" % (withheld, len(admitted)))

    # independent byte-level re-verification of every ledger judgment
    mism = 0
    for (idx, a, b, dec, h) in ent:
        task, pidx = idx // 200, idx % 200
        t2, i2, scene, fkind, F, G = parse_pair(
            os.path.join(PAIRS, "r2p_%s_%03d.pair" % (TASKS[task], pidx)))
        assert t2 == task and i2 == pidx
        ja, jb = span_judgment(F), span_judgment(G)
        if ja != a or jb != b or (1 if ja != jb else 0) != dec:
            mism += 1
            print("MISMATCH idx=%d ledger=(%d,%d,%d) recomputed=(%d,%d)" % (idx, a, b, dec, ja, jb))
    print("ledger judgment re-verification: %d mismatches / 1200" % mism)

    rows = []
    for (idx, a, b, dec, h) in admitted:
        task, pidx = idx // 200, idx % 200
        t2, i2, scene, fkind, F, G = parse_pair(
            os.path.join(PAIRS, "r2p_%s_%03d.pair" % (TASKS[task], pidx)))
        truth = read_truth(task, pidx) or {}
        perm = (len(F) == len(G) and sorted(F) == sorted(G))
        ident = (F == G)
        rows.append({
            "ledger_idx": idx, "task": TASKS[task], "pair_idx": pidx,
            "jf": a, "jg": b, "sumF": sum(F) % 2147483648, "sumG": sum(G) % 2147483648,
            "lenF": len(F), "lenG": len(G),
            "byte_perm": perm, "byte_identical": ident,
            "truth": truth.get("truth", "?"), "family": truth.get("family", "?"),
            "note": truth.get("note", "?"), "mode": pidx % 2,
        })
    out = os.path.join(SCRATCH, "admitted_raw.tsv")
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter="\t")
        w.writeheader(); w.writerows(rows)
    print("wrote", out, "(%d rows)" % len(rows))
    # quick breakdown
    from collections import Counter
    print(Counter((r["task"], r["note"]) for r in rows))

if __name__ == "__main__":
    main()
