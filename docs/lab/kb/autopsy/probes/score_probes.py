#!/usr/bin/env python3
"""KB4 autopsy probe scorer — joins probe-gate outputs with frozen truth.

Metric (frozen KB4): adversarial false installs / adversarial installs.
Bars: <=15% PASS; 15-30% MARGINAL; >30% FAIL. Anti-degeneracy: >=50 true
adversarial installs else DEGENERATE.

Probes:
  pl1 / pl2 : per-approach (A/B), kb4_gate output format, truth keys TAG/ln
             in the frozen per-approach batch order.
  pa2       : per-approach (A/B), same format; pbatch preserves frozen order.
  pa1       : combined A+B batch; pa1_truth.json keyed by line number.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
RERUN = "/home/hatch/workspace/tnn-lab/prose-learning/epistemic_wave/kb4_rerun"

def verdict(adv_installs, adv_false, adv_true):
    if adv_true < 50:
        return "DEGENERATE"
    if not adv_installs:
        return "DEGENERATE"
    rate = adv_false / adv_installs
    if rate <= 0.15:
        return "PASS"
    if rate <= 0.30:
        return "MARGINAL"
    return "FAIL"

def score_per_approach(probe, tag, rep):
    truth = json.load(open(os.path.join(RERUN, "truth.json")))
    out = [l.rstrip("\n") for l in
           open(os.path.join(HERE, "out_%s_%s_rep%d.txt" % (probe, tag, rep)))
           if l.strip()]
    assert out[-1].startswith("SUMMARY"), out[-1]
    ai = af = at = 0
    for ln, ol in enumerate(out[:-1]):
        if ol.split("\t")[2] != "INSTALL":
            continue
        t = truth["%s/%d" % (tag, ln)]
        if t["variant"] == "adversarial":
            ai += 1
            if t["correct"]:
                at += 1
            else:
                af += 1
    return ai, af, at

def score_pa1(rep):
    pt = json.load(open(os.path.join(HERE, "pa1_truth.json")))
    out = [l.rstrip("\n") for l in
           open(os.path.join(HERE, "out_pa1_rep%d.txt" % rep)) if l.strip()]
    assert out[-1].startswith("SUMMARY"), out[-1]
    ai = af = at = 0
    for ln, ol in enumerate(out[:-1]):
        if ol.split("\t")[1] != "INSTALL":
            continue
        e = pt[str(ln)]
        if e["variant"] == "adversarial":
            ai += 1
            if e["adv_correct"]:
                at += 1
            else:
                af += 1
    return ai, af, at

def main():
    results = {}
    for probe, tag in [("pl1", "A"), ("pl1", "B"), ("pl2", "A"),
                       ("pl2", "B"), ("pa2", "A"), ("pa2", "B")]:
        for rep in (1, 2, 3):
            ai, af, at = score_per_approach(probe, tag, rep)
            v = verdict(ai, af, at)
            results["%s_%s_rep%d" % (probe, tag, rep)] = {
                "adv_installs": ai, "adv_false": af, "adv_true": at,
                "false_install_rate": af / ai if ai else None, "verdict": v}
            print("%s %s rep%d: adv_installs=%d adv_false=%d adv_true=%d "
                  "rate=%.1f%% -> %s" % (
                      probe, tag, rep, ai, af, at,
                      100 * af / ai if ai else float("nan"), v))
    for rep in (1, 2, 3):
        ai, af, at = score_pa1(rep)
        v = verdict(ai, af, at)
        results["pa1_rep%d" % rep] = {
            "adv_installs": ai, "adv_false": af, "adv_true": at,
            "false_install_rate": af / ai if ai else None, "verdict": v}
        print("pa1 rep%d: adv_installs=%d adv_false=%d adv_true=%d "
              "rate=%.1f%% -> %s" % (
                  rep, ai, af, at, 100 * af / ai if ai else float("nan"), v))
    json.dump(results, open(os.path.join(HERE, "probe_scores.json"), "w"),
              indent=1)
    print("probe_scores.json written")

if __name__ == "__main__":
    main()
