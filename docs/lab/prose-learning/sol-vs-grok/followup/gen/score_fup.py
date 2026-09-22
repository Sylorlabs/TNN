#!/usr/bin/env python3
"""Score followup verdict files against a battery's expected_sg.json.
Usage: score_fup.py <battery_dir> <name=verdicts> [name=verdicts ...]
Prints a Markdown table of SG-PARA/SAFE/PREC/COMP/WRONG per build plus
per-slice correct/total, and a JSON summary."""
import json, sys

bdir = sys.argv[1]
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

def correct(exp, got):
    if exp.startswith("VALUE:"):
        return got == exp
    if exp.startswith("NOT-VALUE:"):
        return got != exp.split(":", 1)[1] and got != "VALUE:" + exp.split(":", 1)[1]
    return got == exp

def wrong_value(exp, got):
    return got.startswith("VALUE:") and got != exp

PARA = ["heldout", "extra", "typo"]
SAFE = ["neg", "hedge", "contr"]
SLICES = ["canon", "heldout", "extra", "typo", "neg", "hedge",
          "contr", "distr", "multi"]

def metrics(verdicts):
    per = {}
    for s in SLICES:
        ids = [i for i, e in expected.items() if e["class"] == s]
        ok = sum(1 for i in ids if correct(expected[i]["verdict"], verdicts.get(i, "")))
        per[s] = (ok, len(ids))
    def acc(names):
        ids = [i for i, e in expected.items() if e["class"] in names]
        ok = sum(1 for i in ids if correct(expected[i]["verdict"], verdicts.get(i, "")))
        return ok / len(ids)
    # SG-PREC: precision on VALUE answers
    tp = sum(1 for i in expected if verdicts.get(i, "").startswith("VALUE:")
             and correct(expected[i]["verdict"], verdicts[i]))
    vp = sum(1 for i in expected if verdicts.get(i, "").startswith("VALUE:"))
    prec = tp / vp if vp else 1.0
    wrong = sum(1 for i in expected if wrong_value(expected[i]["verdict"], verdicts.get(i, "")))
    return {"SG-PARA": acc(PARA), "SG-SAFE": acc(SAFE), "SG-PREC": prec,
            "SG-COMP": per["multi"][0] / per["multi"][1],
            "SG-WRONG": wrong / len(expected), "per": per,
            "wrong_n": wrong, "n_value": vp}

rows = []
for arg in sys.argv[2:]:
    name, path = arg.split("=", 1)
    rows.append((name, metrics(load(path))))

hdr = ["build", "SG-PARA", "SG-SAFE", "SG-PREC", "SG-COMP", "SG-WRONG"]
print("| " + " | ".join(hdr) + " |")
print("|" + "|".join(["---"] * len(hdr)) + "|")
for name, m in rows:
    print("| %s | %.4f | %.4f | %.4f | %.4f | %.4f |"
          % (name, m["SG-PARA"], m["SG-SAFE"], m["SG-PREC"],
             m["SG-COMP"], m["SG-WRONG"]))
print()
print("per-slice correct/total:")
for name, m in rows:
    print(" ", name, {s: "%d/%d" % m["per"][s] for s in SLICES},
          "wrong_n=%d" % m["wrong_n"])
print()
print(json.dumps({n: {k: (round(v, 4) if isinstance(v, float) else v)
                      for k, v in m.items() if k != "per"}}
                 for n, m in rows), flush=True)
