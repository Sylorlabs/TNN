#!/usr/bin/env python3
"""Crew 3: were the 15 unhittable items hittable under the FROZEN keys?
If yes, the re-seal's key changes manufactured those misses."""
import re, pathlib
from itertools import combinations

BASE = pathlib.Path.home() / "workspace/growwithme_retry"
STOP = {"the", "and", "for", "with", "from", "that", "this", "are", "was", "were", "has", "have",
        "had", "will", "would", "can", "could", "should", "must", "may", "might", "shall", "not", "no",
        "yes", "its", "his", "her", "their", "our", "your", "than", "then", "when", "where", "what",
        "which", "who", "whom", "whose", "why", "how", "all", "any", "both", "each", "few", "more",
        "most", "other", "some", "such", "only", "own", "same", "too", "very", "just", "also"}

def normalize(s):
    s = s.lower(); s = re.sub(r"[`'\"]", "", s)
    s = re.sub(r"[^a-z0-9 ]", " ", s); return re.sub(r"\s+", " ", s).strip()

def score_answer(answer, key):
    na, nk = normalize(answer), normalize(key)
    if nk in na or na in nk: return 1.0
    kw = [w for w in nk.split() if len(w) > 3 and w not in STOP]
    if not kw: return 1.0 if nk in na else 0.0
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

def parse_md(path):
    md = pathlib.Path(path).read_text(); items = []
    for m in re.finditer(r"^### (\S+).*?\n(?:\w[^:\n]*: .*?\n)?Q: (.*?)\n(?:S7 key|Key): ([^\n]*)", md, re.M):
        qid = m.group(1)
        if qid.endswith("-Q"): qid = qid[:-2]
        items.append((qid, m.group(2).strip(), m.group(3).strip()))
    return items

# frozen keys, SUITE-SCOPED (file-stem, probe-id). v1 keyed by bare probe
# id, so S7_recall's corrected keys overwrote the immediate keys for the
# 6 corrected facts (F1-01, F1-09, F1-14, F2-02, F2-07, F2-08). Fixed 2026-09-28.
frozen_keys = {}
for p in (BASE / "_src/docs/lab/growwithme/frozen/probes").glob("*.md"):
    for qid, q, k in parse_md(p):
        frozen_keys[(p.stem, qid)] = k

UNHITTABLE = ["F5-03", "F5-05", "F5-06", "F5-08", "F5-09", "F5-11", "F5-16", "F5-17",
              "F6-02", "F6-03", "F6-06", "F6-07", "F6-12", "F6-17", "F6-18"]
print("qid | frozen-key ceiling (single best) | verdict")
for qid in UNHITTABLE:
    s = int(qid[1])
    facts = store_at(s)
    fk = frozen_keys.get((f"immediate_S{s}", qid), None)
    if fk is None:
        print(f"{qid}: NO FROZEN KEY"); continue
    best, bf = 0.0, None
    for fid, t in facts.items():
        sc = score_answer(t, fk)
        if sc > best: best, bf = sc, fid
    # full pairs for the ones that are 0
    if best < 1.0:
        ids = list(facts)
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                sc = score_answer(facts[ids[i]] + " " + facts[ids[j]], fk)
                if sc > best: best, bf = sc, ids[i] + "+" + ids[j]
                if best >= 1.0: break
            if best >= 1.0: break
    tag = "HITTABLE under frozen" if best >= 1.0 else "unhittable under frozen too"
    print(f"{qid}: best={best:.2f}({bf}) -> {tag}")
