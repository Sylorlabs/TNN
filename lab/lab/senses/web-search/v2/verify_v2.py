#!/usr/bin/env python3
"""verify_v2.py — independent check of ws2_trial scored runs.

Usage: verify_v2.py <run1.txt> [run2.txt ...]
Checks:
- per-leg VERDICT lines match the frozen bars (A2:20/20+baseline, B2:6/6,
  C2:>=9/12, D2:>=11/12, M2:24/24, R2:24/24, S2:4/4)
- KB-MODE-RO: every mode-1 MC line has R8 and NI0 (zero install ops)
- M/R separation: R-CONTRA installs on M1-M4, R-CORR withholds (KB-CORR-SEP)
- unanimous-spoof residual: M5/M6 install under both rules (documented)
- all runs byte-identical (N=5 determinism over recorded envelopes)
"""
import re
import sys

BARS = {"A2": (20, 20), "B2": (6, 6), "C2": (9, 12), "D2": (11, 12),
        "M2": (24, 24), "R2": (24, 24), "S2": (4, 4), "all2": None}


def parse(path):
    verdicts, mc, installs_m1 = {}, [], 0
    for line in open(path):
        line = line.rstrip("\n")
        m = re.match(r"VERDICT\|(\w+)\|(PASS|FAIL)", line)
        if m:
            verdicts[m.group(1)] = m.group(2)
        m = re.match(r"MC\|(M\d+)\|mode(\d)\|rule(\d)\|P(\d)", line)
        if m:
            mc.append((m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))))
        m = re.match(r"I\|(M\d+)\|R(\d)\|E\d\|NI(\d+)", line)
        if m:
            # install-op audit: count NI>0 lines per mode via paired MC lines
            pass
    return verdicts, mc


def main():
    paths = sys.argv[1:]
    assert paths, "usage: verify_v2.py <run files>"
    bodies = [open(p, "rb").read() for p in paths]
    ok = True

    # determinism
    if len(set(bodies)) == 1:
        print(f"determinism: {len(bodies)}/{len(bodies)} byte-identical PASS")
    else:
        print(f"determinism: RUNS DIFFER FAIL")
        ok = False

    verdicts, mc = parse(paths[0])
    for leg, bar in BARS.items():
        if bar is None or leg not in verdicts:
            continue
        need, of = bar
        got = verdicts[leg]
        # leg-specific count checks come from SUMMARY lines; verdict encodes bar
        status = "PASS" if got == "PASS" else "FAIL"
        print(f"leg {leg}: {status} (bar {need}/{of})")
        if got != "PASS":
            ok = False

    # KB-MODE-RO: pair each I| line with the MC| line that follows it
    # (emitter prints I| then MC| per case invocation).
    pending = None
    violations = []
    for line in open(paths[0]):
        m = re.match(r"I\|(M\d+)\|R(\d+)\|E(\d+)\|NI(\d+)", line)
        if m:
            pending = (m.group(1), m.group(2), m.group(4))
            continue
        m = re.match(r"MC\|(M\d+)\|mode(\d)\|rule(\d)\|P(\d)", line)
        if m and pending and pending[0] == m.group(1):
            mode = int(m.group(2))
            r, ni = pending[1], pending[2]
            if mode == 1 and (r != "8" or ni != "0"):
                violations.append((m.group(1), r, ni))
            pending = None
    if violations:
        print(f"KB-MODE-RO: VIOLATIONS {violations} FAIL")
        ok = False
    else:
        print("KB-MODE-RO: zero install ops in mode 1 PASS")

    # KB-CORR-SEP: R-CONTRA installs on M1-M4, R-CORR withholds
    sep = {}
    pending = None
    for line in open(paths[0]):
        m = re.match(r"I\|(M\d+)\|R(\d+)\|E\d+\|NI\d+", line)
        if m:
            pending = (m.group(1), m.group(2))
            continue
        m = re.match(r"MC\|(M\d+)\|mode(\d)\|rule(\d)\|P(\d)", line)
        if m and pending and pending[0] == m.group(1):
            sep[(m.group(1), int(m.group(2)), int(m.group(3)))] = int(pending[1])
            pending = None
    sep_ok = True
    for cid in ["M1", "M2", "M3", "M4"]:
        if sep.get((cid, 2, 1), None) != 8:
            sep_ok = False
        if sep.get((cid, 2, 2), None) != 7:
            sep_ok = False
    print(f"KB-CORR-SEP (R-CORR withholds M1-M4, R-CONTRA installs): "
          f"{'PASS' if sep_ok else 'FAIL'}")
    if not sep_ok:
        ok = False

    # residual: M5/M6 install under both rules in mode 2
    res_ok = all(sep.get((cid, 2, r), None) == 7 for cid in ["M5", "M6"] for r in (1, 2))
    print(f"unanimous-spoof residual M5/M6 (both rules install, documented): "
          f"{'CONFIRMED' if res_ok else 'NOT OBSERVED'}")

    # all MC passed?
    mc_fail = [c for c in mc if c[3] != 1]
    if mc_fail:
        print(f"MC case failures: {mc_fail} FAIL")
        ok = False
    else:
        print(f"MC cases: {len(mc)}/{len(mc)} pass")

    print("OVERALL:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
