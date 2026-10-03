#!/usr/bin/env python3
"""Crew 3: exact-replica hittability audit.
Replicates Crew 2's score_answer EXACTLY (keyword LIST with duplicates,
substring `in` on the normalized answer string), then computes per-key
ceilings over the session-appropriate store state (single fact, and pairs).
"""
import re, pathlib
from itertools import combinations

BASE = pathlib.Path.home() / "workspace/growwithme_retry"
STOP = {"the", "and", "for", "with", "from", "that", "this", "are", "was", "were", "has", "have",
        "had", "will", "would", "can", "could", "should", "must", "may", "might", "shall", "not", "no",
        "yes", "its", "his", "her", "their", "our", "your", "than", "then", "when", "where", "what",
        "which", "who", "whom", "whose", "why", "how", "all", "any", "both", "each", "few", "more",
        "most", "other", "some", "such", "only", "own", "same", "too", "very", "just", "also"}

def normalize(s):
    s = s.lower()
    s = re.sub(r"[`'\"]", "", s)
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def score_answer(answer, key):
    """Exact replica of tools/score_c1c2.py::score_answer."""
    na = normalize(answer)
    nk = normalize(key)
    if nk in na or na in nk:
        return 1.0
    kw = [w for w in nk.split() if len(w) > 3 and w not in STOP]
    if not kw:
        return 1.0 if nk in na else 0.0
    hit = sum(1 for w in kw if w in na)
    return 1.0 if hit / len(kw) >= 0.7 else 0.0

def store_at(sess):
    facts = {}
    for s in range(1, sess + 1):
        for line in (BASE / f"inputs/S{s}.in").read_text().splitlines():
            m = re.match(r"FACT (\S+) \|\| (.*)", line)
            if m: facts[m.group(1)] = m.group(2)
            m = re.match(r"CORR \S+ (\S+) \|\| (.*)", line)
            if m: facts[m.group(1)] = m.group(2)
    return facts

unhittable = []
for s in range(1, 7):
    facts = store_at(s)
    md = (BASE / "probes_resealed" / f"immediate_S{s}.md").read_text()
    for m in re.finditer(r"### (\S+)\nQ: .*?\nKey: (.*?)\n", md, re.DOTALL):
        qid, key = m.group(1), m.group(2).split("\n")[0].strip()
        best1, bf = 0.0, None
        scored = []
        for fid, t in facts.items():
            sc = score_answer(t, key)
            scored.append((sc, fid))
            if sc > best1: best1, bf = sc, fid
        top = sorted(scored, reverse=True)[:10]
        best2 = best1
        for (s1, f1), (s2, f2) in combinations(top, 2):
            sc = score_answer(facts[f1] + " " + facts[f2], key)
            if sc > best2: best2 = sc
        if best2 < 1.0:
            unhittable.append((s, qid, key, best1, bf, best2))
            print(f"S{s} {qid}: single-best={best1:.2f}({bf}) pair-ceil={best2:.2f}")
print(f"\n{len(unhittable)} items with ceiling < 1.0 (cannot score full marks from taught facts)")
