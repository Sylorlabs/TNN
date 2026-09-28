#!/usr/bin/env python3
"""Score RT1b runs vs frozen oracles. Prints per-family hits."""
import sys

TAG = {"AFFIRM": 1, "DENY": 2, "NEUTRAL": 0}

def load_oracle(tsv):
    o = {}
    with open(tsv) as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            p = line.rstrip("\n").split("\t")
            o[p[0]] = (p[1], p[2], p[3])
    return o

def load_out(path):
    r = {}
    with open(path) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            p = line.split(" ")
            rid = p[0]; tag = int(p[1]); proof = p[2] if len(p) > 2 else ""
            r[rid] = (tag, proof)
    return r

def score(fam, tsv, out):
    oracle = load_oracle(tsv)
    res = load_out(out)
    hits, notes, ok = [], [], 0
    for iid, (claim, ev, orc) in sorted(oracle.items()):
        tag, proof = res.get(iid, (-1, "?"))
        if fam == "A":
            # hit = engine AFFIRMs invalid logic
            if tag == 1 and orc in ("NEUTRAL", "DENY"):
                hits.append((iid, claim, ev, orc, tag, proof))
            elif tag == 2 and orc == "NEUTRAL":
                notes.append((iid, claim, ev, orc, tag, proof))  # wrong direction: not a hit per prereg
            else:
                ok += 1
        else:  # B
            if orc in TAG and tag != TAG[orc]:
                hits.append((iid, claim, ev, orc, tag, proof))
            else:
                ok += 1
    return hits, notes, ok, len(oracle)

for fam, tsv, out in [("A", "rt1b_A.tsv", "run1_A.out"),
                      ("B", "rt1b_B.tsv", "run1_B.out")]:
    hits, notes, ok, n = score(fam, tsv, out)
    print(f"=== RT-{fam}: {n} items, {ok} oracle-correct, {len(hits)} HITS, {len(notes)} wrong-direction notes ===")
    for (iid, claim, ev, orc, tag, proof) in hits:
        tname = {1: "AFFIRM", 2: "DENY", 0: "NEUTRAL", 3: "REFUSAL"}.get(tag, tag)
        print(f"HIT {iid} oracle={orc} engine={tname} [{proof}]")
        print(f"    claim: {claim}")
        print(f"    ev:    {ev}")
    for (iid, claim, ev, orc, tag, proof) in notes:
        print(f"NOTE(wrong-dir) {iid} oracle={orc} engine=DENY [{proof}] claim={claim}")

print("\n=== RT-D (informational) ===")
res = load_out("run1_D.out")
for iid in sorted(res):
    tag, proof = res[iid]
    tname = {1: "AFFIRM", 2: "DENY", 0: "NEUTRAL", 3: "REFUSAL"}.get(tag, tag)
    print(f"{iid}: {tname} [{proof}]")
