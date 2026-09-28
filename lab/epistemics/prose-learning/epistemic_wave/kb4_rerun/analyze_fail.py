#!/usr/bin/env python3
"""Analyze WHY the §4(a) gate failed: break down installs/withholds by
(primary correct?, adversarial correct?, match?)."""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))

def analyze(tag):
    with open(os.path.join(ROOT, "truth.json")) as f:
        truth = json.load(f)
    with open(os.path.join(ROOT, "out_%s_rep1.txt" % tag)) as f:
        lines = [l.rstrip("\n") for l in f if l.strip()]
    out_lines = [l for l in lines if not l.startswith("SUMMARY")]

    # group by stimulus
    from collections import defaultdict
    by_stim = defaultdict(dict)
    for ln, ol in enumerate(out_lines):
        t = truth["%s/%d" % (tag, ln)]
        decision = ol.split("\t")[2]
        by_stim[t["stim"]][t["variant"]] = {
            "decision": decision, "correct": t["correct"],
            "judgment": t["judgment"],
        }

    # categories for adversarial
    cats = defaultdict(int)
    for stim, vs in by_stim.items():
        if "adversarial" not in vs or "primary" not in vs:
            continue
        a = vs["adversarial"]
        p = vs["primary"]
        match = (a["judgment"] == p["judgment"])
        key = (
            "adv_correct" if a["correct"] else "adv_wrong",
            "pri_correct" if p["correct"] else "pri_wrong",
            "match" if match else "differ",
            a["decision"],
        )
        cats[key] += 1

    print("=== %s ===" % tag)
    for k in sorted(cats):
        print("%-60s %d" % (str(k), cats[k]))
    print()

for tag in ("A", "B"):
    analyze(tag)
