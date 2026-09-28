#!/usr/bin/env python3
"""B4 contract ablation: same T0 through contract-less gate (always INSTALL).
Suite = 305 adversarial. PASS requires (a) disposition differs on >=10%
(>=31), AND (b) false installs strictly fewer WITH the contract.
"""
import json, re, sys

def main():
    rows = [json.loads(l) for l in open(sys.argv[1])]
    adv = [r for r in rows if r["split"] in ("adversarial", "h3adv")]
    print("adversarial n=%d" % len(adv))
    diff = 0
    fi_with, fi_without = 0, 0
    for r in rows:
        if r["split"] not in ("adversarial", "h3adv"):
            continue
        tr = r["h3_transition"] or ""
        m = re.search(r"\|t0=([^|]*)\|", tr)
        t0 = m.group(1) if m else None
        # with contract
        disp_w, judge_w = r["h3_disp"], r["h3_judge"]
        # without contract (always INSTALL T0)
        disp_wo, judge_wo = "INSTALLED", t0
        if disp_w != disp_wo or judge_w != judge_wo:
            diff += 1
        if disp_w == "INSTALLED" and judge_w != r["truth"]:
            fi_with += 1
        if judge_wo != r["truth"]:
            fi_without += 1
    print("disposition differs: %d/305 (need >=31): %s" % (
        diff, "PASS" if diff >= 31 else "FAIL"))
    print("false installs WITH contract: %d, WITHOUT: %d: %s" % (
        fi_with, fi_without, "PASS" if fi_with < fi_without else "FAIL"))
    b4 = (diff >= 31) and (fi_with < fi_without)
    print("B4:", "PASS" if b4 else "FAIL")

if __name__ == "__main__":
    main()
