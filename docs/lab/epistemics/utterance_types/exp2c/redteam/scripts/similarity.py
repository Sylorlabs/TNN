#!/usr/bin/env python3
"""Quantify corpus<->probe template similarity for the red-team near-paraphrase attack."""
import os, re
from itertools import product

WT = os.path.expanduser("~/workspace/tnn-native-lab-redteam")
RT = os.path.expanduser("~/workspace/redteam_exp2c")

def items(fp):
    out = []
    with open(fp) as f:
        for line in f:
            line = line.rstrip()
            if not line or line.startswith("#"):
                continue
            p = line.split("|")
            if len(p) > 4:
                out.append((p[0], p[3]))
    return out

corpus = items(WT + "/docs/lab/epistemics/utterance_types/exp2c/cal_ab.txt")
probes = []
with open(RT + "/root/sinc3.txt") as f:
    for line in f:
        line = line.rstrip()
        if line:
            p = line.split("|")
            probes.append((p[0], p[3]))
probe_lk = probes[10:20]

def toks(s):
    return re.findall(r"[a-z']+", s.lower())

def jacc(a, b):
    A, B = set(toks(a)), set(toks(b))
    return len(A & B) / len(A | B) if A | B else 0.0

def template(s):
    # reduce to skeleton: first 3 words + frame verb class
    t = toks(s)
    return " ".join(t[:4])

print("=== max Jaccard(corpus item, any SINC-LK probe) ===")
rows = []
for cid, c in corpus:
    best = max((jacc(c, p), pid, p) for pid, p in probe_lk)
    rows.append((best[0], cid, c, best[1], best[2]))
rows.sort(reverse=True)
for j, cid, c, pid, p in rows[:20]:
    print(f"{j:.2f} {cid:6s} ~ {pid:7s} | {c[:52]}")
print("...")
n_high = sum(1 for r in rows if r[0] >= 0.40)
print(f"items with max-Jaccard >= 0.40: {n_high}/{len(rows)}")

print()
print("=== template-skeleton matches (first-4-words identical to a probe) ===")
pm = {template(p): pid for pid, p in probe_lk}
n = 0
for cid, c in corpus:
    t = template(c)
    if t in pm:
        n += 1
        print(f"  {cid} [{c}]  ==skeleton==  {pm[t]}")
print(f"skeleton-identical pairs: {n}")

print()
print("=== shared 3-grams between corpus and probes (excluding stopword-only) ===")
def trigrams(s):
    t = toks(s)
    return {" ".join(t[i:i+3]) for i in range(len(t)-2)}
c3 = set()
for _, c in corpus:
    c3 |= trigrams(c)
hits = {}
for pid, p in probe_lk:
    for tg in trigrams(p):
        if tg in c3 and not all(w in {"the","a","an","is","it","if","of","to"} for w in tg.split()):
            hits.setdefault(tg, []).append(pid)
for tg, pids in sorted(hits.items(), key=lambda x: -len(x[1]))[:15]:
    print(f"  '{tg}' in probes {pids}")
