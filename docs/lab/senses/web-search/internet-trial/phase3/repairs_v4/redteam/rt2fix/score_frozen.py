#!/usr/bin/env python3
# Frozen-battery scorer: corpus (id\tclaim\ttitle\tsnippet\toracle) + run log (idx tag reason)
# Prints score + misses. Usage: score_frozen.py corpus.tsv run.log [label]
import sys

TAG = {"0": "NEUTRAL", "1": "AFFIRM", "2": "DENY"}
TAGW = {"0": "NEUTRAL", "1": "AFFIRM", "2": "DENY"}


def main():
    corpus, run = sys.argv[1], sys.argv[2]
    label = sys.argv[3] if len(sys.argv) > 3 else corpus
    oracle = {}
    order = []
    for line in open(corpus, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) >= 5:
            oracle[parts[0]] = parts[4].strip()
            order.append(parts[0])
    got = {}
    for line in open(run, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line:
            continue
        parts = line.split(" ")
        got[parts[0]] = (parts[1], parts[2] if len(parts) > 2 else "")
    n = len(order)
    ok = 0
    misses = []
    for idx in order:
        w = oracle[idx]
        g = got.get(idx)
        if g is None:
            misses.append((idx, w, "MISSING", ""))
            continue
        if TAGW.get(w) == TAG.get(g[0]):
            ok += 1
        else:
            misses.append((idx, w, g[0], g[1]))
    print(f"{label}: {ok}/{n}")
    for idx, w, gtag, reason in misses:
        print(f"  MISS {idx}: oracle={TAGW.get(w,w)} got={TAG.get(gtag,gtag)} ({reason})")


if __name__ == "__main__":
    main()
