#!/usr/bin/env python3
"""Crew 3: rescore M3's actual answers against the FROZEN keys.
This gives M3's uncontaminated score (removing the re-seal key-change artifacts)."""
import re, pathlib

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

def strip_note(a): return re.sub(r"\s*\[m3:.*?\]\s*$", "", a).strip()

def score_answer(answer, key):
    na, nk = normalize(strip_note(answer)), normalize(key)
    if nk in na or na in nk: return 1.0
    kw = [w for w in nk.split() if len(w) > 3 and w not in STOP]
    if not kw: return 1.0 if nk in na else 0.0
    hit = sum(1 for w in kw if w in na)
    return 1.0 if hit / len(kw) >= 0.7 else 0.0

def parse_md(path):
    md = pathlib.Path(path).read_text(); items = []
    for m in re.finditer(r"^### (\S+).*?\n(?:\w[^:\n]*: .*?\n)?Q: (.*?)\n(?:S7 key|Key): ([^\n]*)", md, re.M):
        qid = m.group(1)
        if qid.endswith("-Q"): qid = qid[:-2]
        items.append((qid, m.group(2).strip(), m.group(3).strip()))
    return items

# Suite-scoped frozen keys: (file-stem, probe-id) -> key. v1 keyed by bare
# probe id; immediate_S1..S6 share F-IDs with S7_recall, so S7's corrected
# keys overwrote the immediate keys (S5/S6 "frozen" scores were really S7
# scores). Fixed 2026-09-28.
frozen_keys = {}
for p in (BASE / "_src/docs/lab/growwithme/frozen/probes").glob("*.md"):
    for qid, q, k in parse_md(p): frozen_keys[(p.stem, qid)] = k
resealed_keys = {}
for p in (BASE / "probes_resealed").glob("*.md"):
    if p.name == "MANIFEST.md": continue
    for qid, q, k in parse_md(p): resealed_keys[(p.stem, qid)] = k

print("arm session | resealed-key score (as reported) | frozen-key score (uncontaminated)")
for arm, d in [("D", "D_rt1"), ("N", "N_rt1")]:
    for s in range(1, 7):
        items = parse_md(BASE / f"probes_resealed/immediate_S{s}.md")
        anss = [l[5:].strip() for l in (RT / "repro" / d / f"probe_immediate_S{s}.txt").read_text().splitlines()
                if l.startswith("A || ")]
        rs = sum(score_answer(a, resealed_keys[(f"immediate_S{s}", q)]) for (q, _, _), a in zip(items, anss))
        fs = sum(score_answer(a, frozen_keys[(f"immediate_S{s}", q)]) for (q, _, _), a in zip(items, anss))
        print(f"{arm} S{s}: {rs:.0f}/18 ({rs/18:.3f}) | {fs:.0f}/18 ({fs/18:.3f})")
