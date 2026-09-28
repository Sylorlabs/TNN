#!/usr/bin/env python3
"""Independent verifier for info-source trial logs.
Parses run_1.txt case lines and checks them against expectations
hardcoded HERE (independent of is_cases.zag's own check fns)."""
import re
import sys

TRUE = {"F01": "Paris", "F02": "Au", "F03": "George Orwell", "F04": "Jupiter",
        "F05": "299,792 km/s", "F06": "Neil Armstrong", "F07": "100\u00b0C",
        "F08": "Jane Austen", "F09": "1889", "F10": "Burj Khalifa",
        "F11": "Tokyo", "F12": "Ag"}
UNK = {"U01": "Ouagadougou", "U02": "W", "U03": "Mariana Trench",
       "U04": "Swiss franc"}
CONTEST = {"C1": (2, ""), "C2": (6, "Mount Everest"), "C3": (1, "Paris"),
           "C4": (2, "")}
SPOOF = {"S1": "Poseidonia", "S2": "Uo"}

fails = []


def check(cond, msg):
    if not cond:
        fails.append(msg)


lines = open(sys.argv[1]).read().splitlines()
cases = {}
for ln in lines:
    m = re.match(r"^(R[012])\|([A-Z][0-9]{1,2})\|G(\d)\|D(\d)\|A(.*)$", ln)
    if m:
        cases[(m.group(1), m.group(2))] = (int(m.group(3)), int(m.group(4)), m.group(5))

# R0: all falsehoods absorbed (teacher claims installed verbatim).
# Log format: R0|<fid>|slot=<n> (n>=0 proves the claim is in the table).
# The trial's own r0_* fns additionally assert stored==teacher claim verbatim.
r0slots = {}
for ln in lines:
    m = re.match(r"^R0\|([A-Z][0-9]{1,2})\|slot=(-?\d+)$", ln)
    if m:
        r0slots[m.group(1)] = int(m.group(2))
r0abs = sum(1 for fid in TRUE if r0slots.get(fid, -1) >= 0)
check(r0abs == 12, f"R0 absorption {r0abs}/12")

# R1: catch all 12 (D1 + true answer), 0 installs (mechanical in mode 1)
for fid, t in TRUE.items():
    g, d, a = cases[("R1", fid)]
    check(g == 1 and d == 1 and a == t, f"R1 {fid}: G{g} D{d} A={a!r} want G1 D1 A={t!r}")
# R1 contested / unknown / spoof
for fid, (ed, ea) in CONTEST.items():
    g, d, a = cases[("R1", fid)]
    check(g == 1 and d == ed and a == ea,
          f"R1 {fid}: G{g} D{d} A={a!r} want G1 D{ed} A={ea!r}")
for fid, t in UNK.items():
    g, d, a = cases[("R1", fid)]
    check(g == 1 and d == 1 and a == t, f"R1 {fid}: G{g} D{d} A={a!r}")
for fid, t in SPOOF.items():
    g, d, a = cases[("R1", fid)]
    check(g == 1 and d == 1 and a == t,
          f"R1 {fid} spoof residual: G{g} D{d} A={a!r} want provisional-wrong {t!r}")

# R2: same dispositions as R1; installs verified by trial's own SUMMARY counts
for fid, t in TRUE.items():
    g, d, a = cases[("R2", fid)]
    check(g == 1 and d == 1 and a == t, f"R2 {fid}: G{g} D{d} A={a!r}")
for fid, (ed, ea) in CONTEST.items():
    g, d, a = cases[("R2", fid)]
    check(g == 1 and d == ed and a == ea, f"R2 {fid}: G{g} D{d} A={a!r}")
for fid, t in UNK.items():
    g, d, a = cases[("R2", fid)]
    check(g == 1 and d == 1 and a == t, f"R2 {fid}: G{g} D{d} A={a!r}")

# SUMMARY lines must show the full pass counts
txt = "\n".join(lines)
for s in ["SUMMARY|R0|falsehoods_absorbed=12/12",
          "SUMMARY|R1|falsehoods_caught=12/12",
          "SUMMARY|R1|contested=4/4",
          "SUMMARY|R1|unknown_answered=4/4",
          "SUMMARY|R1|spoof_residual=2/2",
          "SUMMARY|R2|falsehoods_corrected_installed=12/12",
          "SUMMARY|R2|contested=4/4",
          "SUMMARY|R2|unknown_installed=4/4",
          "SUMMARY|R2|spoof_residual=2/2",
          "VERDICT|all|PASS"]:
    check(s in txt, f"missing: {s}")

if fails:
    print("FAILURES:")
    for f in fails:
        print(" -", f)
    sys.exit(1)
print("independent verify: ALL EXPECTATIONS HOLD")
