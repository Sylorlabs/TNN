#!/usr/bin/env python3
"""Independent hash-chain verifier for R2-2 ledgers.

For each shard ledger: checks prevchain linkage and recomputes
SHA256(prev|task|truth|class|install|dt|df|feats), comparing to the
record's chain field. Pure Python; independent of the Zag binary.

Usage: verify_chain.py <rundir>   (expects ledger_shard0..7.jsonl)
Exit 0 iff every record in every shard verifies.
"""
import os, sys, json, hashlib

def main():
    rundir = sys.argv[1]
    total, bad = 0, 0
    for s in range(8):
        p = os.path.join(rundir, "ledger_shard%d.jsonl" % s)
        prev_expect = "GENESIS:shard%d" % s
        with open(p) as f:
            for ln, line in enumerate(f):
                e = json.loads(line)
                r = e["r22"]
                total += 1
                if e["prevchain"] != prev_expect:
                    print("LINK FAIL shard %d line %d" % (s, ln)); bad += 1
                msg = "|".join([e["prevchain"], r["task"], r["truth"], r["class"],
                                r["install"], r["d_true"], r["d_false"], r["feat"]])
                h = hashlib.sha256(msg.encode()).hexdigest()
                if h != r["chain"]:
                    print("HASH FAIL shard %d line %d:\n  want %s\n  got  %s" % (s, ln, h, r["chain"]))
                    bad += 1
                prev_expect = r["chain"]
    print("verified %d records, %d failures" % (total, bad))
    sys.exit(1 if bad else 0)

main()
