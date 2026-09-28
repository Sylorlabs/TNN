#!/usr/bin/env python3
# score corpus against tsv oracle; usage: score.py corpus.tsv out.txt
import sys
corpus, out = sys.argv[1], sys.argv[2]
rows = {}
for ln in open(corpus):
    f = ln.rstrip("\n").split("\t")
    rows[f[0]] = f[4]
tagmap = {"NEUTRAL": "0", "AFFIRM": "1", "DENY": "2"}
miss = []
for ln in open(out):
    p = ln.split()
    iid, tag = p[0], p[1]
    oracle = rows.get(iid, "?")
    if oracle == "?" or tagmap[oracle] == tag:
        continue
    miss.append((iid, tag, oracle, " ".join(p[2:])))
print(f"misses: {len(miss)}")
for m in miss:
    print(" ", m[0], "got", m[1], "oracle", m[2], "|", m[3])
