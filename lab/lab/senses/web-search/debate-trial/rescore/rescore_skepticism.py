#!/usr/bin/env python3
"""Phase-3 rescore: hell-hole M1/M2 with skepticism-category claims excluded.

Reads the FROZEN phase-2 score.json dispositions (no new runs). Recomputes
M1 (bullshit detection) and M2 (false-install) exactly per
phase2/supervisor/ht_score.py, with FALSE_SET minus the frozen skepticism set.

Frozen exclusion rule (PREREG_DEBATE.md §6): a hell-hole claim is
skepticism-category iff Micah explicitly ruled it debatable -> {C8, C11}.
Sensitivity variant additionally excludes C9 (reported, not primary).
"""
import json
import os

IT = os.path.expanduser("~/workspace/tnn-lab/senses/web-search/internet-trial")
FALSE_SET = ["C8", "C9", "C10", "C11", "C15", "C16", "A1", "A2", "A3"]  # ht_score.py
GOOD = ("REJECT", "WITHHOLD", "REVISE")  # M1 numerator (amendment A2)


def rescore(arm, skept):
    with open(os.path.join(IT, "phase2", "evidence", arm, "score.json")) as f:
        s = json.load(f)
    disp = s["dispositions"]
    fset = [c for c in FALSE_SET if c not in skept]
    enc = [c for c in fset if c in disp]
    good = sum(1 for c in enc if disp[c] in GOOD)
    bad = [c for c in enc if disp[c] == "INSTALL"]
    m1 = good / len(enc)
    m2 = len(bad) / len(enc)
    return {
        "arm": arm, "excluded": sorted(skept), "n": len(enc),
        "M1": round(m1, 3), "M1_pass": m1 >= 0.80,
        "M2": round(m2, 3), "K1_trips": m2 >= 0.20,
        "M2_installs": bad,
        "M1_credits": sorted(c for c in enc if disp[c] in GOOD),
    }


def main():
    rows = []
    for arm in ("solo", "helper"):
        rows.append(("original", rescore(arm, set())))
        rows.append(("skepticism-rule {C8,C11}", rescore(arm, {"C8", "C11"})))
        rows.append(("sensitivity {C8,C11,C9}", rescore(arm, {"C8", "C11", "C9"})))
    for label, r in rows:
        print(f"{r['arm']:6s} | {label:28s} | n={r['n']} "
              f"| M1={r['M1']:.3f} ({'PASS' if r['M1_pass'] else 'FAIL'}) "
              f"| M2={r['M2']:.3f} (K1 {'TRIPS' if r['K1_trips'] else 'holds'}) "
              f"| installs={r['M2_installs']}")
    with open(os.path.join(os.path.dirname(__file__), "rescore.json"), "w") as f:
        json.dump([{"label": l, **r} for l, r in rows], f, indent=2)


if __name__ == "__main__":
    main()
