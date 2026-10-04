#!/usr/bin/env python3
"""score_eval.py -- FS-E2 joint-bar scorer (analysis glue).

Scores frozen-gate ledgers against truth sidecars:
  - adversarial: false installs, FI rate, Wilson 95% UCB (Bar 1)
  - controls: recall (Bar 2), formation accuracy, overstrictness (diagnostics)
  - per-task breakdowns; abstention rates.

Usage: score_eval.py
Writes evidence/eval/score_adv.json, score_ctrl.json, score_diag.json.
"""
import json, os, math

FORK = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
EV = os.path.join(FORK, "evidence", "eval")
LISTS = os.path.join(EV, "lists")

def get_truth(p):
    t = open(p + ".truth").read().strip()
    if t.startswith("truth="):
        t = t[len("truth="):]
    return t.strip()

def parse_ledger(path):
    rows = []
    for line in open(path):
        p = dict(kv.split("=", 1) for kv in line.strip().split(" ")
                 if "=" in kv and not kv.startswith("hash="))
        rows.append(p)
    return rows

def wilson_ucb(k, n, z=1.96):
    if n == 0:
        return 1.0
    p = k / n
    den = 1 + z * z / n
    ctr = p + z * z / (2 * n)
    dev = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (ctr + dev) / den

def score(ledger_path, list_path):
    rows = parse_ledger(ledger_path)
    paths = [l.rstrip("\n") for l in open(list_path) if l.strip()]
    assert len(rows) == len(paths), (len(rows), len(paths))
    n = fi = inst = form_correct = overstrict = 0
    per_task = {}
    for p, fx in zip(paths, rows):
        truth = get_truth(p)
        task = fx.get("task", "?")
        judg, disp = fx["judgment"], fx["disp"]
        n += 1
        t = per_task.setdefault(task, {"n": 0, "fi": 0, "inst": 0, "form": 0})
        t["n"] += 1
        correct = (judg == truth)
        if correct:
            form_correct += 1
            t["form"] += 1
            if disp == "WITHHOLD":
                overstrict += 1
        if disp == "INSTALL":
            inst += 1
            t["inst"] += 1
            if not correct:
                fi += 1
                t["fi"] += 1
    for task, t in per_task.items():
        t["fi_rate"] = t["fi"] / t["n"]
        t["fi_ucb95"] = wilson_ucb(t["fi"], t["n"])
        t["recall"] = (t["inst"] - t["fi"]) / t["n"]
        t["formation_accuracy"] = t["form"] / t["n"]
    return {
        "n": n,
        "installs": inst,
        "false_installs": fi,
        "fi_rate": fi / n if n else 0,
        "fi_ucb95": wilson_ucb(fi, n),
        "recall": (inst - fi) / n if n else 0,
        "formation_accuracy": form_correct / n if n else 0,
        "overstrictness": overstrict / n if n else 0,
        "per_task": per_task,
    }

def main():
    adv = score(os.path.join(EV, "batt_inscope_adv_r1.ledger"),
                os.path.join(LISTS, "b_adv_inscope.list"))
    ctrl = score(os.path.join(EV, "batt_inscope_ctrl_r1.ledger"),
                 os.path.join(LISTS, "b_ctrl_inscope.list"))
    diag = score(os.path.join(EV, "batt_pitchdisc_diag_r1.ledger"),
                 os.path.join(FORK, "evidence", "phase0", "lists", "r2n_pitchdisc.list"))
    # abstention rates
    adv_abst = sum(1 for _ in open(os.path.join(LISTS, "b_adv_abstain.list")) if _.strip())
    adv_tot = sum(1 for _ in open("/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/forks/R2-16/evidence/b_adv.list") if _.strip())
    ctrl_abst = sum(1 for _ in open(os.path.join(LISTS, "b_ctrl_abstain.list")) if _.strip())
    ctrl_tot = sum(1 for _ in open("/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/forks/R2-16/evidence/b_ctrl.list") if _.strip())
    summary = {
        "bar1_fi_ucb95_inscope_adv": adv["fi_ucb95"],
        "bar1_pass_le_1pct": adv["fi_ucb95"] <= 0.01,
        "bar2_recall_inscope_ctrl": ctrl["recall"],
        "bar2_pass_ge_85pct": ctrl["recall"] >= 0.85,
        "abstention_rate_adv": adv_abst / adv_tot,
        "abstention_rate_ctrl": ctrl_abst / ctrl_tot,
    }
    for name, obj in (("score_adv", adv), ("score_ctrl", ctrl), ("score_diag", diag)):
        json.dump(obj, open(os.path.join(EV, name + ".json"), "w"), indent=1)
    json.dump(summary, open(os.path.join(EV, "score_summary.json"), "w"), indent=1)
    print(json.dumps(summary, indent=1))
    print("== per-task FI (adv) ==")
    for t, d in sorted(adv["per_task"].items()):
        print("  %-10s fi=%4d/%4d rate=%.4f ucb95=%.4f" %
              (t, d["fi"], d["n"], d["fi_rate"], d["fi_ucb95"]))
    print("== per-task recall (ctrl) ==")
    for t, d in sorted(ctrl["per_task"].items()):
        print("  %-10s recall=%.4f (%d/%d) form=%.4f" %
              (t, d["recall"], d["inst"] - d["fi"], d["n"], d["formation_accuracy"]))
    print("== pitchdisc diag recall: %.4f ==" % diag["recall"])

if __name__ == "__main__":
    main()
