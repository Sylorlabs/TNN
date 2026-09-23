#!/usr/bin/env python3
"""verify_chain.py — independent hash-chain verifier for R2-13 ledgers.

Recomputes every link from the record fields (not from any stored chain value
except as the prev for the next link) and reports mismatches.

Usage: verify_chain.py <ledger>
Exit 0 iff every link verifies.
"""
import sys, hashlib

def main():
    path = sys.argv[1]
    recs, cur = [], {}
    with open(path) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip() or "=" not in line:
                continue
            k, v = line.split("=", 1)
            cur[k] = v
            if k == "chain":
                recs.append(cur)
                cur = {}
    if cur:
        recs.append(cur)
    prev = "GENESIS"
    bad = 0
    for i, r in enumerate(recs):
        if "error" in r:
            # error record: sha256 of "approach=R2-13\ntask=...\nerror=...\nprev=...\n"
            msg = "approach=R2-13\ntask=%s\nerror=%s\nprev=%s\n" % (
                r.get("task", ""), r.get("error", ""), r.get("prev", ""))
        else:
            msg = "|".join([prev, r.get("task", ""), r.get("truth", ""), r.get("class", ""),
                            r.get("install", ""), r.get("d_true", ""), r.get("d_false", ""),
                            r.get("feat", ""), r.get("mode", ""), r.get("family", "")])
        h = hashlib.sha256(msg.encode()).hexdigest()
        if h != r.get("chain", ""):
            bad += 1
            if bad <= 5:
                print("MISMATCH record %d: stored %s computed %s" % (i, r.get("chain", ""), h))
        prev = r.get("chain", "")
    print("records=%d mismatches=%d final=%s" % (len(recs), bad, prev))
    sys.exit(1 if bad else 0)

main()
