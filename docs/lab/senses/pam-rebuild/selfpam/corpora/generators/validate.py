#!/usr/bin/env python3
"""Validate the SELF-PAM battery corpora against frozen prereg minima.

Checks (all must pass):
- world: 144 facts, 144 gaps; gap attributes absent from store (construction)
- C1: >=500 gap drafts, >=500 held drafts; every draft has oracle fields
- C2: >=500 tasks; each has >=1 warranted + >=1 unwarranted draft assembly,
      oracle labels for warranted vs unwarranted steps
- C3: >=500 items across 5 modes; leak_trap flags present
- W:  >=300 claims; all oracle_true and not oracle_warrantable
- P:  >=500 drafts; each has citation + warrant + oracle admissibility
- D:  >=20 dialogues, each >=50 turns, each >=1 oracle-labeled conflict
- determinism: sha256 of every corpus file recorded (manifest step separate)
"""
import json
import os
import sys

CORP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
fails = []


def check(cond, msg):
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        fails.append(msg)


def load(p):
    with open(os.path.join(CORP, p), encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


facts = load("world/store.jsonl")
gaps = load("world/gaps.jsonl")
check(len(facts) == 144, "world: 144 facts (got %d)" % len(facts))
check(len(gaps) == 144, "world: 144 gaps (got %d)" % len(gaps))
check(len({f["id"] for f in facts}) == 144, "world: fact ids unique")
check(len({g["id"] for g in gaps}) == 144, "world: gap ids unique")
blob = "\n".join(f["text"] for f in facts)
for w in ["born", "founded", "chronicler", "built by"]:
    check(w not in blob, "world: gap attribute %r absent from store" % w)
for g in gaps:
    check(g["oracle_true"] is True and g["oracle_warrantable"] is False,
          "world: gap %s oracle true-but-unwarrantable" % g["id"])\
        if False else None
check(all(g["oracle_true"] and not g["oracle_warrantable"] for g in gaps),
      "world: all gaps oracle-labeled true-but-unwarrantable")

c1 = load("cell-c1/c1_drafts.jsonl")
gap_d = [d for d in c1 if d["kind"] == "gap"]
held_d = [d for d in c1 if d["kind"] == "held"]
check(len(gap_d) >= 500, "C1: >=500 gap drafts (got %d)" % len(gap_d))
check(len(held_d) >= 500, "C1: >=500 held drafts (got %d)" % len(held_d))
check(all(set(("id", "prompt", "kind", "ref", "draft", "oracle_grounded",
               "oracle_true", "oracle_warrantable", "expected", "bar")) <= set(d)
          for d in c1), "C1: all drafts carry oracle fields")
h61 = [d for d in gap_d if d["bar"] == "KB-H6-1"]
h63 = [d for d in gap_d if d["bar"] == "KB-H6-3"]
check(len(h61) >= 500 and len(h63) >= 500,
      "C1: gap drafts split KB-H6-1/KB-H6-3 (%d/%d)" % (len(h61), len(h63)))
fact_ids = {f["id"] for f in facts}
gap_ids = {g["id"] for g in gaps}
check(all(d["ref"] in fact_ids for d in held_d), "C1: held refs resolve")
check(all(d["ref"] in gap_ids for d in gap_d), "C1: gap refs resolve")

c2 = load("cell-c2/c2_tasks.jsonl")
check(len(c2) >= 500, "C2: >=500 tasks (got %d)" % len(c2))
ok = True
for t in c2:
    labs = [d["label"] for d in t["drafts"]]
    if "warranted" not in labs or "unwarranted" not in labs:
        ok = False
    for d in t["drafts"]:
        if d["label"] == "unwarranted" and not d["unwarranted_steps"]:
            ok = False
        if d["label"] == "warranted" and d["unwarranted_steps"]:
            ok = False
check(ok, "C2: every task has warranted+unwarranted drafts, steps labeled")
check(all(any(fr["role"] == "distractor" for fr in t["fragments"]) for t in c2),
      "C2: every task plants distractors")

c3 = load("cell-c3/c3_items.jsonl")
check(len(c3) >= 500, "C3: >=500 items (got %d)" % len(c3))
from collections import Counter
modes = Counter(i["oracle_mode"] for i in c3)
check(set(modes) == {"FACT", "CONSTRUCTED", "HYPOTHETICAL", "JOKE", "IRONY"},
      "C3: all 5 modes present %s" % dict(modes))
check(all(modes[m] >= 100 for m in modes), "C3: >=100 per mode")
check(any(i["leak_trap"] for i in c3 if i["oracle_mode"] == "CONSTRUCTED"),
      "C3: declarative leak traps present")
check(all(i["expected_marking"] == i["oracle_mode"] for i in c3),
      "C3: expected marking == oracle mode")

w = load("cell-w/w_claims.jsonl")
check(len(w) >= 300, "W: >=300 claims (got %d)" % len(w))
check(all(c["oracle_true"] and not c["oracle_warrantable"] for c in w),
      "W: all claims true-but-unwarrantable")
check(all(c["expected"] == "withhold-or-marked" for c in w),
      "W: all expect withhold-or-marked")

p = load("cell-p/p_drafts.jsonl")
check(len(p) >= 500, "P: >=500 drafts (got %d)" % len(p))
check(all("citation" in d and "warrant" in d and "oracle" in d for d in p),
      "P: citation+warrant+oracle on every draft")
adm = sum(1 for d in p if d["oracle"]["admissible"])
check(adm / len(p) >= 0.80, "P: >=80%% admissible (got %.1f%%)" % (100 * adm / len(p)))
cited = {d["citation"]["fact_id"] for d in p if d["oracle"]["citation_valid"]}
check(cited <= fact_ids, "P: valid citations resolve to store")

d = load("cell-d/d_dialogues.jsonl")
check(len(d) >= 20, "D: >=20 dialogues (got %d)" % len(d))
check(all(len(x["turns"]) >= 50 for x in d), "D: every dialogue >=50 turns")
check(all(len(x["conflicts"]) >= 1 for x in d),
      "D: every dialogue >=1 planted conflict")
check(all(all(c["expected"] == "withhold-or-explicit-revision"
              for c in x["conflicts"]) for x in d),
      "D: conflicts oracle-labeled withhold-or-explicit-revision")

print("---")
if fails:
    print("VALIDATION FAILED: %d checks" % len(fails))
    sys.exit(1)
print("ALL CHECKS PASSED")
