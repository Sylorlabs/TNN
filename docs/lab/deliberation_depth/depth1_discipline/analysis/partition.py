#!/usr/bin/env python3
"""SINGLE/MULTI knowledge partition (prereg §3, analysis-only, mechanism-blind).
For each item: apply each single evidence e alone from zero scores;
leader = argmax, ties -> lowest index (matches dlb_leader).
SINGLE: >=1 single evidence makes GT the leader. MULTI: none does.
"""
import json

D = "/home/hatch/workspace/tnn-lab/deliberation_depth/depth1_discipline"
BATS = ["trap", "admit", "revoke", "logic", "rt_d1"]

def part(item):
    hyps = [h["id"] for h in item["input"]["hypotheses"]]
    gt = item["ground_truth"]
    for e in item["input"]["evidence"]:
        scores = [0] * len(hyps)
        for h, w in e["supports"].items():
            scores[hyps.index(h)] += w
        for h, w in e["attacks"].items():
            scores[hyps.index(h)] -= w
        best = 0
        for i in range(1, len(hyps)):
            if scores[i] > scores[best]:
                best = i
        if hyps[best] == gt:
            return "SINGLE"
    return "MULTI"

out = {}
with open(f"{D}/analysis/partition.jsonl", "w") as f:
    for b in BATS:
        path = f"{D}/batteries/rt_d1.jsonl" if b == "rt_d1" else f"{D}/../items_v2/{b}.jsonl"
        for l in open(path):
            it = json.loads(l)
            p = part(it)
            out[it["id"]] = p
            f.write(json.dumps({"id": it["id"], "battery": b, "partition": p,
                                "gt": it["ground_truth"]}) + "\n")

from collections import Counter
c = Counter(out.values())
print("partition counts:", dict(c))
cb = Counter()
for l in open(f"{D}/analysis/partition.jsonl"):
    d = json.loads(l)
    cb[(d["battery"], d["partition"])] += 1
for b in BATS:
    print(b, "SINGLE:", cb[(b, "SINGLE")], "MULTI:", cb[(b, "MULTI")])
