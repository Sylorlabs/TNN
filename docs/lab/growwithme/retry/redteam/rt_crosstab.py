#!/usr/bin/env python3
"""Crew 3: cross-tab unhittable items vs M3's actual verdicts.
For each unhittable miss: did M3 retrieve the right fact (pure scorer gap)
or fail retrieval too (retrieval failure on an unhittable item)?"""
import re, pathlib
from itertools import combinations

BASE = pathlib.Path.home() / "workspace/growwithme_retry"
RT = BASE / "redteam"
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

# full-pair ceiling (rigorous)
def ceiling(key, facts):
    fn = {fid: normalize(t) for fid, t in facts.items()}
    best, how = 0.0, None
    for fid, t in facts.items():
        sc = score_answer(t, key)
        if sc > best: best, how = sc, fid
    ids = list(facts)
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            sc = score_answer(facts[ids[i]] + " " + facts[ids[j]], key)
            if sc > best: best, how = sc, ids[i] + "+" + ids[j]
    return best, how

def traces(s):
    text = (RT / "repro" / f"D_rt1/snapshot_S{s}.txt").read_text()
    out = {}
    pat = re.compile(r"TRACE \d+ \|\| kind=m3-deliberation \|\| ref=(.*?) \|\| considered=(.*?) \|\| evidence=(.*?) \|\| verdict=(.*?) \|\| reason=")
    for m in pat.finditer(text):
        out[m.group(1)] = (m.group(2), m.group(3), m.group(4))
    return out

print("qid | key-ceiling | M3 verdict | right-fact? | class")
print("-" * 100)
pure_gap, ret_fail = 0, 0
for s in (5, 6):
    facts = store_at(s)
    md = (BASE / "probes_resealed" / f"immediate_S{s}.md").read_text()
    tr = traces(s)
    probes = [(m.group(1), m.group(2).strip(), m.group(3).split("\n")[0].strip())
              for m in re.finditer(r"### (\S+)\nQ: (.*?)\nKey: (.*?)\n", md, re.DOTALL)]
    for qid, q, key in probes:
        ceil, how = ceiling(key, facts)
        if ceil >= 0.7: continue
        right = qid[:-2]
        t = tr.get(q[:40])
        ver = t[2] if t else "depb-withhold"
        if "tie-withhold" in ver: vcls, got_right = "tie-withhold", False
        elif ver.startswith("union"):
            w = ver.replace("union ", "").split("+")[0]; vcls, got_right = "union", (w == right)
        elif ver.startswith("single"):
            w = ver.replace("single ", ""); vcls, got_right = "single", (w == right)
        else: vcls, got_right = "depb-withhold", False
        cls = "PURE SCORER GAP (right fact, unhittable)" if got_right else "retrieval failure on unhittable item"
        if got_right: pure_gap += 1
        else: ret_fail += 1
        print(f"S{s} {qid}: ceil={ceil:.2f} best={how} | {vcls} winner-right={got_right} | {cls}")
print(f"\n pure scorer-gap misses: {pure_gap} | retrieval failures on unhittable items: {ret_fail}")
