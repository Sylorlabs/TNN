#!/usr/bin/env python3
"""KB4 §4(a) scorer — joins gate output with frozen truth, applies frozen bars.

Metric: adversarial false installs / adversarial installs.
Bars: <=15% PASS; 15-30% MARGINAL (repair+rerun); >30% FAIL.
Anti-degeneracy: >=50 true adversarial installs, else DEGENERATE.
(Integration-clearance bar remains <=10%; a <=15% EPI-KB4 pass alone does
not clear integration — prereg §4(a).)
"""
import json, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))

def score(tag, rep):
    with open(os.path.join(ROOT, "truth.json")) as f:
        truth = json.load(f)
    with open(os.path.join(ROOT, "out_%s_rep%d.txt" % (tag, rep))) as f:
        lines = [l.rstrip("\n") for l in f if l.strip()]
    # last line is SUMMARY
    assert lines[-1].startswith("SUMMARY"), lines[-1]
    out_lines = lines[:-1]

    # truth keys are "A/<line_no>" in batch order
    n_adv_installs = 0
    n_adv_false = 0
    n_adv_true = 0
    n_total_installs = 0
    for ln, ol in enumerate(out_lines):
        parts = ol.split("\t")
        decision = parts[2]
        t = truth["%s/%d" % (tag, ln)]
        if decision == "INSTALL":
            n_total_installs += 1
            if t["variant"] == "adversarial":
                n_adv_installs += 1
                if t["correct"]:
                    n_adv_true += 1
                else:
                    n_adv_false += 1
    rate = (n_adv_false / n_adv_installs) if n_adv_installs else None
    return {
        "tag": tag, "rep": rep,
        "total_installs": n_total_installs,
        "adv_installs": n_adv_installs,
        "adv_false": n_adv_false,
        "adv_true": n_adv_true,
        "false_install_rate": rate,
    }

def verdict(r):
    if r["adv_true"] < 50:
        return "DEGENERATE"
    rate = r["false_install_rate"]
    if rate is None:
        return "DEGENERATE"
    if rate <= 0.15:
        return "PASS"
    if rate <= 0.30:
        return "MARGINAL"
    return "FAIL"

def main():
    results = {}
    for tag in ("A", "B"):
        for rep in (1, 2, 3):
            r = score(tag, rep)
            r["verdict"] = verdict(r)
            results["%s_rep%d" % (tag, rep)] = r
            fr = "n/a" if r["false_install_rate"] is None else "%.1f%%" % (r["false_install_rate"]*100)
            print("%s rep%d: installs=%d adv_installs=%d adv_false=%d adv_true=%d rate=%s -> %s" % (
                tag, rep, r["total_installs"], r["adv_installs"],
                r["adv_false"], r["adv_true"], fr, r["verdict"]))
    with open(os.path.join(ROOT, "epi_kb4_scores.json"), "w") as f:
        json.dump(results, f, indent=1)
    print("scores written")

if __name__ == "__main__":
    main()
