#!/usr/bin/env python3
"""score_e2b.py -- FS-GR1 scorer (analysis only).

Reads evidence/eval/{adv,ctrl}_gate_r1.ledger + formation TSVs, truth from
<fixture>.truth sidecars.

Definitions (frozen):
  FI     = disposition INSTALL with formation claim != truth
  Recall = correct INSTALLs / n (controls)
  Formation accuracy = claim == truth (all fixtures)
  Overstrictness = WITHHOLD rate on controls where claim == truth
Bars (PREREG_FS-GR1.md):
  1. FI Wilson 95% UCB <= 1% pooled (adv, n=10000)
  2. Recall >= 85% pooled (ctrl, n=2000)
  3. FI Wilson 95% UCB <= 1% per-task (adv)
  4. Recall >= 85% per-task (ctrl)
  5. Scoping audit: all six formation figures >= 85%
  6. Determinism: handled by run_eval_e2b.py (byte-identity + chain verify)

Writes: score_adv.json, score_ctrl.json, score_summary.json (FINAL numbers).
"""
import json
import math
import os
from collections import Counter

FORK = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/forks/FS-GR1"
EV = os.path.join(FORK, "evidence", "eval")
TN = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]

FORM_MIN = {"colordisc": 0.9296, "pitchdisc": 0.9792, "motiondir": 0.9663,
            "shapetrans": 1.0000, "colorconst": 0.9858, "timbredisc": 1.0000}


def wilson_ucb(x, n, z=1.96):
    if n == 0:
        return None
    p = x / n
    d = 1.0 + z * z / n
    c = p + z * z / (2 * n)
    dev = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (c + dev) / d


def kv(line):
    return dict(x.split("=", 1) for x in line.strip().split(" ") if "=" in x)


def load(tag):
    # Formation TSV rows and ledger rows are in the same list order
    # (run_eval_e2b.py asserts this); zip positionally. The ledger's
    # fixture= id is built from the file header's (task,index,family),
    # so the formation TSV's absolute path is the reliable path source.
    form_rows = []
    for line in open(os.path.join(EV, "%s_formation_r1.tsv" % tag)):
        p, t, j = line.rstrip("\n").split("\t")
        form_rows.append((p, t.split("=", 1)[1], j.split("=", 1)[1]))
    rows = []
    led = [l for l in open(os.path.join(EV, "%s_gate_r1.ledger" % tag))
           if l.strip()]
    assert len(led) == len(form_rows), (len(led), len(form_rows))
    for (p, tname, jname), line in zip(form_rows, led):
        line = line.rstrip("\n")
        i = line.rfind(" hash=")
        d = kv(line[:i])
        assert d["task"] == tname and d["judgment"] == jname, \
            (d["task"], tname, d["judgment"], jname)
        tline = open(p + ".truth").read().strip()
        truth = tline.split("=", 1)[1] if "=" in tline else tline
        rows.append({"path": p, "task": tname, "judgment": jname,
                     "disp": d["disp"], "challenge": d["challenge"],
                     "outcome": d["outcome"], "admit": d["admit"],
                     "truth": truth})
    return rows


def score_adv(rows):
    FI = [r for r in rows if r["disp"] == "INSTALL" and r["judgment"] != r["truth"]]
    per = {}
    for t in TN:
        rt = [r for r in rows if r["task"] == t]
        xt = [r for r in FI if r["task"] == t]
        per[t] = {"n": len(rt), "fi": len(xt),
                  "fi_rate": len(xt) / len(rt) if rt else None,
                  "ucb": wilson_ucb(len(xt), len(rt)),
                  "bar": wilson_ucb(len(xt), len(rt)) is not None
                  and wilson_ucb(len(xt), len(rt)) <= 0.01}
    pooled = {"n": len(rows), "fi": len(FI),
              "fi_rate": len(FI) / len(rows),
              "ucb": wilson_ucb(len(FI), len(rows)),
              "bar": wilson_ucb(len(FI), len(rows)) <= 0.01}
    fam = Counter()
    for r in FI:
        fam[(r["task"], r["challenge"])] += 1
    return {"pooled": pooled, "per_task": per,
            "fi_list": [(r["path"], r["task"], r["judgment"], r["truth"],
                         r["challenge"], r["outcome"]) for r in FI],
            "per_family_fi": {"%s/%s" % k: v for k, v in sorted(fam.items())}}


def score_ctrl(rows):
    per = {}
    for t in TN:
        rt = [r for r in rows if r["task"] == t]
        ok = [r for r in rt if r["disp"] == "INSTALL" and r["judgment"] == r["truth"]]
        right = [r for r in rt if r["judgment"] == r["truth"]]
        wh = [r for r in right if r["disp"] != "INSTALL"]
        per[t] = {"n": len(rt), "recall_ok": len(ok),
                  "recall": len(ok) / len(rt) if rt else None,
                  "bar": len(rt) > 0 and len(ok) / len(rt) >= 0.85,
                  "formation": len(right) / len(rt) if rt else None,
                  "overstrictness": len(wh) / len(right) if right else None}
    ok = [r for r in rows if r["disp"] == "INSTALL" and r["judgment"] == r["truth"]]
    right = [r for r in rows if r["judgment"] == r["truth"]]
    pooled = {"n": len(rows), "recall_ok": len(ok),
              "recall": len(ok) / len(rows),
              "bar": len(ok) / len(rows) >= 0.85,
              "formation": len(right) / len(rows),
              "overstrictness": len([r for r in right if r["disp"] != "INSTALL"]) / len(right)}
    audit = {t: {"reproduced": per[t]["formation"], "min": FORM_MIN[t],
                 "pass": per[t]["formation"] is not None and per[t]["formation"] >= 0.85}
             for t in TN}
    return {"pooled": pooled, "per_task": per, "scoping_audit": audit}


def main():
    adv = load("adv")
    ctrl = load("ctrl")
    sa = score_adv(adv)
    sc = score_ctrl(ctrl)
    bars = {
        "bar1_pooled_fi_ucb_le_1pct": sa["pooled"]["bar"],
        "bar2_pooled_recall_ge_85pct": sc["pooled"]["bar"],
        "bar3_per_task_fi_ucb_le_1pct": all(v["bar"] for v in sa["per_task"].values()),
        "bar4_per_task_recall_ge_85pct": all(v["bar"] for v in sc["per_task"].values()),
        "bar5_scoping_audit": all(v["pass"] for v in sc["scoping_audit"].values()),
        "bar6_determinism": "checked by run_eval_e2b.py",
    }
    json.dump(sa, open(os.path.join(EV, "score_adv.json"), "w"), indent=1)
    json.dump(sc, open(os.path.join(EV, "score_ctrl.json"), "w"), indent=1)
    json.dump({"bars": bars, "verdict_hint": "ALIVE" if all(
        v for k, v in bars.items() if k != "bar6_determinism") else "DEAD"},
              open(os.path.join(EV, "score_summary.json"), "w"), indent=1)
    print(json.dumps(bars, indent=1))


if __name__ == "__main__":
    main()
