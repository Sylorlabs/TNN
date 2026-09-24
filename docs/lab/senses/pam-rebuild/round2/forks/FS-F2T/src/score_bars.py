#!/usr/bin/env python3
"""score_bars.py -- FS-F2T bar scoring (analysis only; judgments come from Zag).
Usage: score_bars.py <run#>   reads evidence/eval/run<#>_*.tsv
Prints per-battery accuracy, confusion for timbredisc, and bar PASS/FAIL.
"""
import csv
import sys
from collections import Counter

EV = "evidence/eval"
RUN = sys.argv[1]

BARS = {
    "fresh_timbredisc": ("timbredisc fresh draw", 1000, 85.00),
    "reg_colordisc": ("colordisc (no-reg)", 1080, 91.96),
    "reg_pitchdisc": ("pitchdisc (no-reg)", 720, 96.92),
    "reg_motiondir": ("motiondir (no-reg)", 564, 95.63),
}


def load(name):
    rows = list(csv.reader(open("%s/run%s_%s.tsv" % (EV, RUN, name)),
                           delimiter="\t"))
    return rows


def main():
    allpass = True
    for name, (label, expect_n, floor) in BARS.items():
        rows = load(name)
        n = len(rows)
        ok = sum(1 for r in rows if r[4] == "1")
        pct = 100.0 * ok / n if n else 0.0
        passed = (pct >= floor)
        allpass = allpass and passed and (n == expect_n)
        print("%-24s %4d/%-4d = %6.2f%%  floor %5.2f%%  n=%d  %s" %
              (label, ok, n, pct, floor, expect_n,
               "PASS" if (passed and n == expect_n) else "FAIL"))
        if name == "fresh_timbredisc":
            cm = Counter((r[2], r[3]) for r in rows)
            print("  confusion (judgment x truth):")
            for j in ["PURE", "BRIGHT", "DARK", "RICH"]:
                print("   %-6s %s" % (j, {t: cm[(j, t)]
                      for t in ["PURE", "BRIGHT", "DARK", "RICH"]}))
            miss = [(r[0].split("/")[-1], r[2], r[3]) for r in rows
                    if r[4] != "1"]
            for m in miss[:20]:
                print("   miss:", m)
            if len(miss) > 20:
                print("   ... and %d more" % (len(miss) - 20))
    print("ALL GATING BARS:", "PASS" if allpass else "FAIL")


if __name__ == "__main__":
    main()
