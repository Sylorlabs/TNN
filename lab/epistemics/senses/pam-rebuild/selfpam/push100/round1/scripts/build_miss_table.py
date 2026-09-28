#!/usr/bin/env python3
"""Round-1 autopsy step 3: build the final miss_table.tsv using the
AUTHORITATIVE committed truth files (repo fixtures), plus per-pair
byte-relationship classification and the miss/correct-admit verdict.
"""
import struct, os, csv, subprocess

SCRATCH = os.path.dirname(os.path.abspath(__file__))
PAIRS = "/home/hatch/workspace/selfpam_consumer/pairs_full"
TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]
REPO = "/home/hatch/workspace/tnn-native-lab-work"
FIX = "docs/lab/senses/pam-rebuild/round2/fixtures/r2p"

def git_show(path):
    return subprocess.run(["git", "-C", REPO, "show", "origin/tnn-native-lab:" + path],
                          capture_output=True).stdout

def parse_pair(path):
    data = open(path, "rb").read()
    assert data[:4] == b"R2P1", path
    task, idx, scene, flen, glen, fkind = struct.unpack("<iiQiii", data[4:32])
    assert len(data) == 64 + flen + glen
    return task, idx, scene, fkind, data[64:64 + flen], data[64 + flen:]

def span_judgment(blob):
    return (sum(blob) % 2147483648) // 8

def truth_of(task, pidx):
    raw = git_show("%s/r2p_%s_%03d.pair.truth" % (FIX, TASKS[task], pidx)).decode()
    d = {}
    for line in raw.splitlines():
        k, _, v = line.partition("=")
        d[k] = v
    return d

def main():
    rows = list(csv.DictReader(open(os.path.join(SCRATCH, "admitted_raw.tsv")), delimiter="\t"))
    out_rows = []
    for r in rows:
        idx = int(r["ledger_idx"]); task = r["task"]; pidx = int(r["pair_idx"])
        t2, i2, scene, fkind, F, G = parse_pair(os.path.join(PAIRS, "r2p_%s_%03d.pair" % (task, pidx)))
        assert t2 == TASKS.index(task) and i2 == pidx
        truth = truth_of(TASKS.index(task), pidx)
        assert int(truth["scene"]) == scene, "scene mismatch %s %d" % (task, pidx)
        assert int(truth["family"]) == fkind
        jf, jg = span_judgment(F), span_judgment(G)
        assert jf == int(r["jf"]) and jg == int(r["jg"]) and jf == jg
        # byte relationship class
        if F == G:
            rel = "identical"
        elif len(F) == len(G) and sorted(F) == sorted(G):
            rel = "byte-permutation"
        else:
            rel = "distinct-content"
        # mechanism + verdict
        note = truth["note"]
        if task == "motiondir" and note == "reversed":
            # proven: F frames == reverse(G frames), exact (prove_mechanisms.py)
            mech = "A: permutation-blindness (F = exact frame-reversal of G)"
            verdict = "MISS"
            why = ("generator asserts F fooled (naive dir != truth) and G clean; "
                   "reference gate withholds 1200/1200 incl. this pair; "
                   "byte-sum measurement cannot see order")
        elif task == "colordisc" and note == "illuminant-drift":
            mech = "B: exact byte-sum collision (warm illuminant preserves per-pixel channel sum)"
            verdict = "MISS"
            why = ("generator asserts F fooled (naive DIFFERENT, truth SAME) and G clean; "
                   "reference gate withholds it; sums exactly equal so /8 tolerance is not the cause; "
                   "no prereg carve-out for truth=SAME pairs")
        else:
            mech = "UNEXPECTED"
            verdict = "REVIEW"
            why = "does not match known classes"
        out_rows.append({
            "ledger_idx": idx, "task": task, "pair_idx": pidx, "mode": pidx % 2,
            "truth": truth["truth"], "note": note,
            "jf": jf, "jg": jg,
            "sumF": sum(F) % 2147483648, "sumG": sum(G) % 2147483648,
            "sums_exactly_equal": sum(F) == sum(G),
            "lenF": len(F), "lenG": len(G),
            "byte_relationship": rel,
            "mechanism_class": mech, "verdict": verdict, "verdict_basis": why,
        })
    assert all(r["verdict"] == "MISS" for r in out_rows), "non-miss verdicts present"
    outp = os.path.join(SCRATCH, "miss_table.tsv")
    with open(outp, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()), delimiter="\t")
        w.writeheader(); w.writerows(out_rows)
    print("wrote", outp, len(out_rows), "rows;",
          sum(1 for r in out_rows if r["mechanism_class"].startswith("A:")), "class A,",
          sum(1 for r in out_rows if r["mechanism_class"].startswith("B:")), "class B")

if __name__ == "__main__":
    main()
