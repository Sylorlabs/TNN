#!/usr/bin/env python3
"""Score Sol-vs-Grok duel verdicts. Usage:
score_sg.py <battery_dir> <sol_verdicts> <grok_verdicts> [--hybrid-out <path>]
Prints Markdown table + JSON summary to stdout."""
import json, sys
from collections import defaultdict

bdir, solf, grokf = sys.argv[1], sys.argv[2], sys.argv[3]
expected = json.load(open(f"{bdir}/expected_sg.json"))

def load(p):
    d = {}
    with open(p) as f:
        for ln in f:
            ln = ln.rstrip("\n")
            if not ln:
                continue
            i, v = ln.split("\t", 1)
            d[i] = v
    return d

sol, grok = load(solf), load(grokf)
# mechanical hybrid: sol unless sol UNKNOWN -> grok
hyb = {i: (sol[i] if sol.get(i) != "UNKNOWN" else grok.get(i)) for i in expected}

def correct(exp, got):
    if exp.startswith("VALUE:"):
        return got == exp
    if exp.startswith("NOT-VALUE:"):
        return got != exp.split(":", 1)[1] and got != "VALUE:" + exp.split(":", 1)[1]
    return got == exp

def wrong_value(exp, got):
    return got.startswith("VALUE:") and got != exp

SLICES = {
    "canon": ["canon"],
    "heldout": ["heldout"],
    "extra": ["extra"],
    "typo": ["typo"],
    "neg": ["neg"],
    "hedge": ["hedge"],
    "contr": ["contr"],
    "distr": ["distr"],
    "multi": ["multi"],
}
PARA = ["heldout", "extra", "typo"]
SAFE = ["neg", "hedge", "contr"]

def metrics(verdicts):
    per = {}
    for name, clses in SLICES.items():
        ids = [i for i, e in expected.items() if e["class"] in clses]
        ok = sum(1 for i in ids if correct(expected[i]["verdict"], verdicts.get(i, "")))
        per[name] = (ok, len(ids))
    def acc(names):
        ids = [i for i, e in expected.items() if e["class"] in names]
        ok = sum(1 for i in ids if correct(expected[i]["verdict"], verdicts.get(i, "")))
        return ok / len(ids)
    wrong = sum(1 for i in expected if wrong_value(expected[i]["verdict"], verdicts.get(i, "")))
    return {
        "per_slice": {k: {"ok": v[0], "n": v[1], "acc": v[0] / v[1]} for k, v in per.items()},
        "SG_PARA": acc(PARA),
        "SG_CANON": acc(["canon"]),
        "SG_SAFE": acc(SAFE),
        "SG_PREC": acc(["distr"]),
        "SG_COMP": acc(["multi"]),
        "SG_WRONG": wrong / len(expected),
        "n_wrong": wrong,
        "n": len(expected),
    }

res = {"sol": metrics(sol), "grok": metrics(grok), "hybrid": metrics(hyb)}
names = ["sol", "grok", "hybrid"]
print("| metric | sol | grok | hybrid |")
print("|---|---|---|---|")
for m in ["SG_PARA", "SG_CANON", "SG_SAFE", "SG_PREC", "SG_COMP", "SG_WRONG"]:
    print(f"| {m} | " + " | ".join(f"{res[n][m]:.4f}" for n in names) + " |")
print()
print("| slice | sol | grok | hybrid |")
print("|---|---|---|---|")
for s in SLICES:
    row = []
    for n in names:
        d = res[n]["per_slice"][s]
        row.append(f"{d['ok']}/{d['n']}={d['acc']:.4f}")
    print(f"| {s} | " + " | ".join(row) + " |")
print()
print("JSON:" + json.dumps(res))
