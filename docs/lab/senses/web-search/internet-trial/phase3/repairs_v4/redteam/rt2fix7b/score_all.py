#!/usr/bin/env python3
# Universal oracle scorer.
# usage: score_all.py <corpus> <out> <style>
# style: rt2 (col4=num 0/1/2), rt2b (col5=WORD), rt2c (col4=WORD), rt2d (col5=WORD)
import sys
corpus, outpath, style = sys.argv[1], sys.argv[2], sys.argv[3]
W2N = {"NEUTRAL": "0", "AFFIRM": "1", "DENY": "2"}
rows = {}
for ln in open(corpus):
    ln = ln.rstrip("\n")
    if not ln.strip():
        continue
    f = ln.split("\t")
    if style == "rt2":
        rows[f[0]] = (f[3], f[1], f[2])
    elif style == "rt2b":
        rows[f[0]] = (W2N[f[4]], f[1], f[3])
    elif style == "rt2c":
        rows[f[0]] = (W2N[f[4]], f[1], f[3])
    elif style == "rt2d":
        rows[f[0]] = (W2N[f[4]], f[1], f[3])
tags = {}
for ln in open(outpath):
    ln = ln.strip()
    if not ln:
        continue
    p = ln.split()
    tags[p[0]] = (p[1], " ".join(p[2:]))
ok, miss = 0, []
for iid, (oracle, claim, ev) in rows.items():
    tag, reason = tags.get(iid, ("?", ""))
    if tag == oracle:
        ok += 1
    else:
        miss.append((iid, oracle, tag, reason))
n = len(rows)
print(f"{corpus.split('/')[-1]} vs {outpath.split('/')[-1]}: {ok}/{n}")
for m in miss:
    print(f"  MISS {m[0]} oracle={m[1]} got={m[2]} ({m[3]})")
