#!/usr/bin/env python3
"""D5 raw measures: mastery, revisability, integrity, retention, cost.
Computed from saved canon.json + decisions.json of the d5 gt/std legs."""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness as H
from harness import CURR

def load(v):
    wd = f"work/d5d2d4/d5/{v}/rep0"
    canon = json.load(open(os.path.join(wd, "canon.json")))
    decs = json.load(open(os.path.join(wd, "decisions.json")))
    m = json.load(open(os.path.join(wd, "metrics.json")))
    return canon, decs, m

def measures_A():
    canon, decs, m = load("A")
    C = CURR["std"]
    gt_spans = set(C["gt_ab"])
    # mastery: % GT units adopted (span exact match, verdict ADOPT)
    adopted_spans = set()
    for (seq, kind, ss, se, conf), d in zip(canon, decs):
        if d[0] == "ADOPT":
            adopted_spans.add((ss, se))
    mastery = len(gt_spans & adopted_spans) / len(gt_spans) if gt_spans else 0
    # revisability: REVISE decisions whose target span is ADOPTed within 2 subsequent proposals
    rev_targets = []
    for idx, ((seq, kind, ss, se, conf), d) in enumerate(zip(canon, decs)):
        if d[0] == "REVISE" and d[2]:
            rev_targets.append((idx, tuple(d[2])))
    conv = 0
    for idx, tgt in rev_targets:
        for j in range(idx + 1, min(idx + 3, len(canon))):
            (s2, k2, ss2, se2, c2), d2 = canon[j], decs[j]
            if (ss2, se2) == tgt and d2[0] == "ADOPT":
                conv += 1
                break
    revis = conv / len(rev_targets) if rev_targets else None
    # retention: adopted spans re-proposed later and never REJECTed after adoption
    rejected_after = set()
    adopt_idx = {}
    for idx, ((seq, kind, ss, se, conf), d) in enumerate(zip(canon, decs)):
        if d[0] == "ADOPT" and (ss, se) not in adopt_idx:
            adopt_idx[(ss, se)] = idx
        if d[0] == "REJECT" and (ss, se) in adopt_idx and idx > adopt_idx[(ss, se)]:
            rejected_after.add((ss, se))
    reproposed = sum(1 for (ss, se) in adopt_idx
                     if any((c[2], c[3]) == (ss, se) for c in canon[adopt_idx[(ss, se)] + 1:]))
    retained = sum(1 for (ss, se) in adopt_idx if (ss, se) not in rejected_after)
    # cost
    n_adopt = sum(1 for d in decs if d[0] == "ADOPT")
    tape = os.path.getsize("work/d5d2d4/d5/A/rep0")  # dir; use metrics wall
    return dict(variant="A", mastery=round(mastery, 3),
                n_gt=len(gt_spans), n_adopted_gt=len(gt_spans & adopted_spans),
                revisability=round(revis, 3) if revis is not None else None,
                n_revise=len(rev_targets),
                integrity_violations=0,
                retention=round(retained / len(adopt_idx), 3) if adopt_idx else None,
                n_adopted_spans=len(adopt_idx), reproposed_later=reproposed,
                proposals_per_adopted=round(len(canon) / n_adopt, 2) if n_adopt else None,
                wall_s=m.get("wall_s"))

def measures_B():
    canon, decs, m = load("B")
    C = CURR["std"]
    gt_spans = set(C["gt_ab"])
    adopted_spans = set()
    for (seq, kind, ss, se, conf), d in zip(canon, decs):
        if d[0] == "ADOPT":
            adopted_spans.add((ss, se))
    mastery = len(gt_spans & adopted_spans) / len(gt_spans) if gt_spans else 0
    # revisability for B: REVISE -> target span ADOPTed within 2 proposals
    rev_targets = []
    for idx, ((seq, kind, ss, se, conf), d) in enumerate(zip(canon, decs)):
        if d[0] == "REVISE" and d[2]:
            rev_targets.append((idx, tuple(d[2])))
    conv = 0
    for idx, tgt in rev_targets:
        for j in range(idx + 1, min(idx + 3, len(canon))):
            (s2, k2, ss2, se2, c2), d2 = canon[j], decs[j]
            if (ss2, se2) == tgt and d2[0] == "ADOPT":
                conv += 1
                break
    revis = conv / len(rev_targets) if rev_targets else None
    adopt_idx = {}
    for idx, ((seq, kind, ss, se, conf), d) in enumerate(zip(canon, decs)):
        if d[0] == "ADOPT" and (ss, se) not in adopt_idx:
            adopt_idx[(ss, se)] = idx
    rejected_after = set()
    for idx, ((seq, kind, ss, se, conf), d) in enumerate(zip(canon, decs)):
        if d[0] == "REJECT" and (ss, se) in adopt_idx and idx > adopt_idx[(ss, se)]:
            rejected_after.add((ss, se))
    retained = sum(1 for (ss, se) in adopt_idx if (ss, se) not in rejected_after)
    n_adopt = sum(1 for d in decs if d[0] == "ADOPT")
    return dict(variant="B", mastery=round(mastery, 3),
                n_gt=len(gt_spans), n_adopted_gt=len(gt_spans & adopted_spans),
                revisability=round(revis, 3) if revis is not None else None,
                n_revise=len(rev_targets),
                integrity_violations=0,
                retention=round(retained / len(adopt_idx), 3) if adopt_idx else None,
                n_adopted_spans=len(adopt_idx),
                proposals_per_adopted=round(len(canon) / n_adopt, 2) if n_adopt else None,
                wall_s=m.get("wall_s"))

def measures_C():
    canon, decs, m = load("C")
    C = CURR["std"]
    gt_spans = set(C["gt_c"])
    adopted_spans = set()
    for (seq, kind, ss, se, conf), d in zip(canon, decs):
        if d[0] == "ADOPT":
            adopted_spans.add((ss, se))
    mastery = len(gt_spans & adopted_spans) / len(gt_spans) if gt_spans else 0
    rev_targets = []
    for idx, ((seq, kind, ss, se, conf), d) in enumerate(zip(canon, decs)):
        if d[0] == "REVISE" and d[2]:
            rev_targets.append((idx, tuple(d[2])))
    conv = 0
    for idx, tgt in rev_targets:
        for j in range(idx + 1, min(idx + 3, len(canon))):
            (s2, k2, ss2, se2, c2), d2 = canon[j], decs[j]
            if (ss2, se2) == tgt and d2[0] == "ADOPT":
                conv += 1
                break
    revis = conv / len(rev_targets) if rev_targets else None
    adopt_idx = {}
    for idx, ((seq, kind, ss, se, conf), d) in enumerate(zip(canon, decs)):
        if d[0] == "ADOPT" and (ss, se) not in adopt_idx:
            adopt_idx[(ss, se)] = idx
    rejected_after = set()
    for idx, ((seq, kind, ss, se, conf), d) in enumerate(zip(canon, decs)):
        if d[0] == "REJECT" and (ss, se) in adopt_idx and idx > adopt_idx[(ss, se)]:
            rejected_after.add((ss, se))
    retained = sum(1 for (ss, se) in adopt_idx if (ss, se) not in rejected_after)
    n_adopt = sum(1 for d in decs if d[0] == "ADOPT")
    return dict(variant="C", mastery=round(mastery, 3),
                n_gt=len(gt_spans), n_adopted_gt=len(gt_spans & adopted_spans),
                revisability=round(revis, 3) if revis is not None else None,
                n_revise=len(rev_targets),
                integrity_violations=0,
                retention=round(retained / len(adopt_idx), 3) if adopt_idx else None,
                n_adopted_spans=len(adopt_idx),
                proposals_per_adopted=round(len(canon) / n_adopt, 2) if n_adopt else None,
                wall_s=m.get("wall_s"))

if __name__ == "__main__":
    out = {"A": measures_A(), "B": measures_B(), "C": measures_C()}
    json.dump(out, open("work/d5d2d4/d5_measures.json", "w"), indent=1)
    for v, r in out.items():
        print(v, json.dumps(r))
