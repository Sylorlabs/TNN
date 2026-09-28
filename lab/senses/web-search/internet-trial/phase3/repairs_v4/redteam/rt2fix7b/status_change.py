#!/usr/bin/env python3
# usage: status_change.py <corpus> <style> <out_t5> <out_t6>
# prints per-item oracle-status change: WR (wrong->right), RW (right->wrong), ch (verdict changed, status same)
import sys
corpus, style, o5, o6 = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
W2N = {"NEUTRAL": "0", "AFFIRM": "1", "DENY": "2"}
rows = {}
for ln in open(corpus):
    ln = ln.rstrip("\n")
    if not ln.strip():
        continue
    f = ln.split("\t")
    if style == "rt2":
        rows[f[0]] = f[3]
    elif style in ("rt2b", "rt2c", "rt2d"):
        rows[f[0]] = W2N[f[4]]
def load(p):
    d = {}
    for ln in open(p):
        ln = ln.strip()
        if not ln:
            continue
        q = ln.split()
        d[q[0]] = (q[1], " ".join(q[2:]))
    return d
t5, t6 = load(o5), load(o6)
print(f"== {corpus.split('/')[-1]} ==")
for iid in sorted(rows):
    oracle = rows[iid]
    v5, r5 = t5[iid]
    v6, r6 = t6[iid]
    ok5, ok6 = (v5 == oracle), (v6 == oracle)
    if ok5 != ok6 or v5 != v6:
        arrow = "WR" if (not ok5 and ok6) else ("RW" if (ok5 and not ok6) else "ch")
        print(f"  {arrow} {iid}: t5={v5}({r5}) t6={v6}({r6}) oracle={oracle}")
