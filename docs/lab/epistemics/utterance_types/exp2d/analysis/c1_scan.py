#!/usr/bin/env python3
"""C1 near-duplicate scan: corpus items vs all curriculum (probe) utterances.

For each corpus item, reports the most similar curriculum utterance under:
  - 16-byte case-insensitive substring overlap (inherited minimum bar)
  - shared word-4-gram (template-copy signal)
  - word-unigram Jaccard
  - word-trigram Jaccard (diagnostic)

Pre-registered replacement rule (EXP2D amendment):
  REPLACE the item iff it shares a 16-byte substring, a word-4-gram, or has
  word-unigram Jaccard >= 0.60 with any curriculum utterance.
"""
import os, sys, itertools

BASE = "/home/hatch/workspace/tnn-native-lab-work/docs/lab/epistemics/utterance_types"
CUR = BASE + "/crew2/curriculum"
WORK = "/home/hatch/workspace/sinc_exp/exp2c/work"

def utts_of(path):
    out = []
    for line in open(path, encoding="utf-8", errors="replace"):
        line = line.rstrip("\n")
        if not line or line.startswith("#"):
            continue
        p = line.split("|")
        if len(p) >= 4:
            out.append((p[0], p[3].lower()))
    return out

def words(t):
    return [w for w in "".join(c if c.isalnum() else " " for c in t).split()]

def ngrams(ws, n):
    return set(tuple(ws[i:i+n]) for i in range(len(ws)-n+1))

def jacc(a, b):
    if not a and not b: return 1.0
    if not a or not b: return 0.0
    return len(a & b) / len(a | b)

def substr16(a, b):
    a = a.lower(); b = b.lower()
    for i in range(len(a)-15):
        if a[i:i+16] in b: return a[i:i+16]
    return None

# curriculum utterances: every .txt in crew2/curriculum
cur = []
for fn in sorted(os.listdir(CUR)):
    if fn.endswith(".txt"):
        for pid, u in utts_of(os.path.join(CUR, fn)):
            cur.append((f"{fn}:{pid}", u))
print(f"curriculum utterances: {len(cur)}", file=sys.stderr)

# corpus items: (tag, id, utterance)
corpus = []
for tag, path in (("orig48", WORK+"/cal_abc.txt"),
                  ("volnew48", WORK+"/cal_vol2.txt"),
                  ("de32", WORK+"/cal_de.txt")):
    seen_ids = set()
    for pid, u in utts_of(path):
        if tag == "volnew48" and pid in seen_ids:
            continue
        # volnew48 file = orig48 + 48 new; keep only the new block (ids starting with vn)
        if tag == "volnew48" and not pid.startswith("vn"):
            seen_ids.add(pid); continue
        seen_ids.add(pid)
        corpus.append((tag, pid, u))
print(f"corpus items: {len(corpus)}", file=sys.stderr)

print("tag\titem_id\tbest_probe\tJ1\tJ3\tshared4\t\tsub16\tutterance")
n_replace = 0
for tag, pid, u in corpus:
    wu, t3u, w4u = set(words(u)), ngrams(words(u),3), ngrams(words(u),4)
    best = None
    for ctag, cu in cur:
        # skip self-comparison is unnecessary: corpus items are not curriculum items
        j1 = jacc(wu, set(words(cu)))
        s16 = substr16(u, cu) is not None
        sh4 = len(w4u & ngrams(words(cu),4)) > 0
        score = (s16, sh4, j1)
        if best is None or score > best[0]:
            best = (score, ctag, cu, j1, jacc(t3u, ngrams(words(cu),3)), sh4, s16)
    (s16, sh4, j1), ctag, cu, j1, j3, sh4, s16 = best
    flag = "REPLACE" if (s16 or sh4 or j1 >= 0.60) else "ok"
    if flag == "REPLACE": n_replace += 1
    print(f"{tag}\t{pid}\t{ctag}\t{j1:.2f}\t{j3:.2f}\t{int(sh4)}\t{int(s16)}\t{flag}\t{u[:60]}")
print(f"\nflagged for replacement: {n_replace}", file=sys.stderr)
