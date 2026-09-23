#!/usr/bin/env python3
"""verify_pd.py — independent oracle for the principle-detection trial.

Reads expected.json (from gen_pd.py) and one run log per arch; scores
detection / false-alarm / refinement vs the frozen PREREG; checks A-vs-B
agreement and the preregistered probe divergence. No shared code with the
Zag binary beyond the frozen tables.
"""
import json, sys, os

D = os.path.dirname(os.path.abspath(__file__))
exp = json.load(open(os.path.join(D, "expected.json")))["facts"]


def parse(path):
    verdicts = {}
    summary = {}
    for line in open(path):
        line = line.strip()
        if line.startswith("F") and " " in line:
            fid, v = line[1:].split()
            verdicts[fid] = int(v)
        if line.startswith("PD_SUMMARY"):
            for kv in line.split(",")[1:]:
                k, val = kv.split("=")
                summary[k] = val
    return verdicts, summary


def score(verdicts):
    viol = [f for f, e in exp.items() if e["probe"] == 0 and e["expect"] == 1]
    exc = [f for f, e in exp.items() if e["probe"] == 0 and e["expect"] == 2]
    nonv = [f for f, e in exp.items()
            if e["probe"] == 0 and e["expect"] in (0, 3)]
    det_hit = sum(1 for f in viol if verdicts[f] == 1)
    fa = [f for f in nonv
          if verdicts[f] == 1 or (f in exc and False)]
    # false alarm: consistent/noscope item flagged(1); true exception rejected(1)
    fa = [f for f in nonv if verdicts[f] == 1]
    fa += [f for f in exc if verdicts[f] == 1]
    ref_hit = sum(1 for f in exc if verdicts[f] == 2)
    exact = sum(1 for f, e in exp.items()
                if e["probe"] == 0 and verdicts.get(f) == e["expect"])
    return {
        "n_scored": len(viol) + len(exc) + len(nonv),
        "detection": det_hit / len(viol),
        "det_hit": det_hit, "det_n": len(viol),
        "false_alarm": len(fa) / len(nonv),
        "fa_n": len(fa), "fa_denom": len(nonv), "fa_items": fa,
        "refinement": ref_hit / len(exc),
        "ref_hit": ref_hit, "ref_n": len(exc),
        "exact": exact,
    }


va, sa = parse(os.path.join(D, "runs", "pd_a_r1.log"))
vb, sb = parse(os.path.join(D, "runs", "pd_b_r1.log"))
ra, rb = score(va), score(vb)

print("== arch A (derive-check) ==")
print("scored items: %d  exact: %d" % (ra["n_scored"], ra["exact"]))
print("detection: %d/%d = %.4f  (bar >= 0.90)" %
      (ra["det_hit"], ra["det_n"], ra["detection"]))
print("false-alarm: %d/%d = %.4f  (bar <= 0.05)" %
      (ra["fa_n"], ra["fa_denom"], ra["false_alarm"]), ra["fa_items"])
print("refinement: %d/%d = %.4f" % (ra["ref_hit"], ra["ref_n"], ra["refinement"]))
print("probes: F44=%d F45=%d" % (va["44"], va["45"]))
print("summary:", sa)
print()
print("== arch B (materialize + arbitrate) ==")
print("scored items: %d  exact: %d" % (rb["n_scored"], rb["exact"]))
print("detection: %d/%d = %.4f  (bar >= 0.90)" %
      (rb["det_hit"], rb["det_n"], rb["detection"]))
print("false-alarm: %d/%d = %.4f  (bar <= 0.05)" %
      (rb["fa_n"], rb["fa_denom"], rb["false_alarm"]), rb["fa_items"])
print("refinement: %d/%d = %.4f" % (rb["ref_hit"], rb["ref_n"], rb["refinement"]))
print("probes: F44=%d F45=%d" % (vb["44"], vb["45"]))
print("summary:", sb)
print()
agree = sum(1 for f, e in exp.items()
            if e["probe"] == 0 and va[f] == vb[f])
print("A-vs-B agreement on scored: %d/%d" % (agree, ra["n_scored"]))
print("A-vs-B divergence items:",
      [f for f in exp if va.get(f) != vb.get(f)])

ok = True
for name, r in (("A", ra), ("B", rb)):
    if r["detection"] < 0.90:
        print("KB-PD-DET TRIPPED on", name); ok = False
    if r["false_alarm"] > 0.05:
        print("KB-PD-FA TRIPPED on", name); ok = False
print("KILL BARS:", "ALL HOLD" if ok else "TRIPPED — see above")
