#!/usr/bin/env python3
# Deterministic scorer: corpus TSV (id\tclaim\tevidence\toracle) + run log (idx tag reason)
# Prints hits only. Usage: score.py corpus.tsv run.log
import sys

TAG = {"0": "NEUTRAL", "1": "AFFIRM", "2": "DENY"}
TAGW = {"0": "NEUTRAL", "1": "AFFIRM", "2": "DENY"}


def main():
    corpus, run = sys.argv[1], sys.argv[2]
    oracle = {}
    for line in open(corpus, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line:
            continue
        parts = line.split("\t")
        oracle[parts[0]] = parts[3]
    hits = []
    n = 0
    for line in open(run, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line:
            continue
        parts = line.split(" ")
        idx, tag, reason = parts[0], parts[1], parts[2] if len(parts) > 2 else ""
        n += 1
        want = oracle.get(idx)
        got = TAG.get(tag, "?")
        if want is None:
            continue
        # direction per PREREG_V4_RT: RT-A hit = accepts invalid (AFFIRM on non-AFFIRM oracle)
        # RT-B hit = rejects valid (any mismatch, corpus oracles are all AFFIRM or DENY)
        is_rtA = idx.startswith("A")
        hit = (got == "AFFIRM" and want != "1") if is_rtA else (got != TAGW.get(want, "?"))
        if hit:
            hits.append((idx, want, got, reason))
    print(f"{corpus} vs {run}: {n} items, {len(hits)} hits")
    for idx, want, got, reason in hits:
        print(f"  HIT {idx}: oracle={want} got={got} ({reason})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
