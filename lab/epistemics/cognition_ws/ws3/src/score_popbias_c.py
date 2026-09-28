#!/usr/bin/env python3
"""WS3-C kill-bar scorer (PREREG_WS3C.md frozen 2026-09-24).

Reads runs_c/{before,after,control}_r{1,2,3}.log (C battery) and
runs_c/mw_{frozen,port}_r{1,2,3}.log (MW sibling port, report only).
Applies CK1-CK8 mechanically. Exit 0: all bars hold. Exit 1: any kill
tripped (names the bar + fixture). Exit 2: procedure failure (CK7/CK8 or
before-bug check).
"""
import hashlib
import os
import re
import sys

WS3 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(WS3, "runs_c")
SRC = os.path.join(WS3, "src")
BUILD = os.path.join(WS3, "build_c")
ARMS = ("before", "after", "control")
MW_ARMS = ("mw_frozen", "mw_port")

GATE_FIDS = ("P2", "P3b", "S1b", "S2a", "S2b", "S3b", "S4b", "S5a",
             "L1", "L2", "L3", "L3b", "L5", "L6", "SP2", "SP3", "SP4")


def sha(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def parse(arm):
    rows = {}
    with open(os.path.join(RUNS, "%s_r1.log" % arm)) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.startswith("RESULT|"):
                continue
            parts = line.split("|")
            r = {"arm": parts[1], "fid": parts[2], "fam": parts[3],
                 "d": int(parts[4][1:]), "c": parts[5][1:],
                 "n": int(parts[6][1:]), "f": int(parts[7][1:]),
                 "i": int(parts[8][1:]), "v": int(parts[9][1:]),
                 "s": parts[10][1:] if len(parts) > 10 else ""}
            rows[r["fid"]] = r
    return rows


def parse_mw(arm):
    rows = {}
    with open(os.path.join(RUNS, "%s_r1.log" % arm)) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.startswith("MW|"):
                continue
            parts = line.split("|")
            rows[parts[1]] = {"v": parts[2], "c": parts[3], "rule": parts[4]}
    return rows


def rng_gate():
    """CK8: no RNG call-shape identifiers in src/*.zag or generated drivers."""
    pat = re.compile(
        r"(?<![A-Za-z_])(rand|srand|drand48|nrand|lcg|random_bytes)"
        r"(?![A-Za-z_])\s*\(|(?<![A-Za-z_.])Math\.random|"
        r"(?<![A-Za-z_])_rng\b|(?<![A-Za-z_])rng_state\b")
    hits = []
    files = []
    for d in (SRC, BUILD):
        for fn in sorted(os.listdir(d)):
            if fn.endswith(".zag"):
                files.append(os.path.join(d, fn))
    for p in files:
        with open(p) as f:
            for ln, line in enumerate(f, 1):
                if "no rng" in line.lower():
                    continue
                m = pat.search(line)
                if m:
                    hits.append("%s:%d: %s" % (p, ln, line.strip()[:80]))
    return hits


def main():
    kills = []

    # CK7 determinism
    for arm in ARMS + MW_ARMS:
        hs = {sha(os.path.join(RUNS, "%s_r%d.log" % (arm, i)))
              for i in (1, 2, 3)}
        if len(hs) != 1:
            print("CK7 PROCEDURE-FAIL: %s runs not byte-identical" % arm)
            return 2
    print("CK7 HOLD: N=3 runs byte-identical per arm (C battery + MW battery)")

    # CK8 zero-RNG
    hits = rng_gate()
    if hits:
        print("CK8 PROCEDURE-FAIL: RNG identifiers found:")
        for h in hits:
            print("    " + h)
        return 2
    print("CK8 HOLD: zero RNG identifiers in src/*.zag + generated drivers")

    B = parse("before")
    A = parse("after")
    C = parse("control")
    fids = sorted(set(B) & set(A) & set(C))

    # Procedure check: BEFORE must exhibit the bug.
    bug = [("P1", B["P1"]["d"] == 1 and B["P1"]["i"] == 7),
           ("P2", B["P2"]["d"] == 6 and B["P2"]["i"] == 7),
           ("S2b", B["S2b"]["d"] == 6 and B["S2b"]["i"] == 7),
           ("S3b", B["S3b"]["d"] == 6 and B["S3b"]["i"] == 7
            and B["S3b"]["s"] == "Yarrow"),
           ("S4b", B["S4b"]["d"] == 1 and B["S4b"]["i"] == 8),
           ("L2", B["L2"]["d"] == 6 and B["L2"]["i"] == 7),
           ("L3b", B["L3b"]["d"] == 6 and B["L3b"]["i"] == 7),
           ("SP4", B["SP4"]["d"] == 6 and B["SP4"]["i"] == 7)]
    bad = [fid for fid, ok in bug if not ok]
    if bad:
        print("BEFORE-BUG-CHECK FAILED (procedure): %s" % ",".join(bad))
        return 2
    print("BEFORE-BUG-CHECK ok: poison/majority/sockpuppet installs land in "
          "BEFORE (P1,P2,S2b,S3b,L2,L3b,SP4); S4b D1/I8")

    def kill(bar, fid, why):
        kills.append((bar, fid, why))

    for fid in fids:
        a, c, b = A[fid], C[fid], B[fid]
        fam = a["fam"]
        # CK1: never-settles-on-popularity (AFTER/CONTROL only)
        for r, arm in ((a, "AFTER"), (c, "CONTROL")):
            if r["i"] == 7 and r["v"] != 1:
                kill("CK1", fid, "%s installed with V=%d" % (arm, r["v"]))
            if arm == "AFTER" and r["f"] > 55:
                kill("CK1", fid, "AFTER conf %d > 55 ceiling" % r["f"])
        # CK2: bend-only vs control
        if not (a["d"] == c["d"] and a["c"] == c["c"]):
            kill("CK2", fid, "verdict differs AFTER vs CONTROL "
                 "(D%d/%s vs D%d/%s)" % (a["d"], a["c"], c["d"], c["c"]))
        df = a["f"] - c["f"]
        if not (0 <= df <= 5):
            kill("CK2", fid, "conf delta %d outside [0,5]" % df)
        if a["n"] - c["n"] != df and not (a["f"] == 0 and c["f"] == 0):
            kill("CK2", fid, "nudge/conf delta mismatch")
        # CK3: evidence gate
        if fid in GATE_FIDS:
            if not (a["n"] == 0 and a["d"] == 2):
                kill("CK3", fid, "contradiction present but AFTER "
                     "nudge=%d disp=%d" % (a["n"], a["d"]))
        # CK4: poison never installs on popularity (V==0 members)
        if fam == "poison" and a["v"] == 0:
            if a["i"] != 8:
                kill("CK4", fid, "poison installed on popularity alone")
        # CK6: ladder thresholds
        if fid == "L4":
            if not (a["d"] == 1 and a["n"] == 4 and a["f"] == 54
                    and a["i"] == 8):
                kill("CK6", fid, "below-bar bend wrong "
                     "(D%d N%d F%d I%d)" % (a["d"], a["n"], a["f"], a["i"]))
        if fid in ("L1", "L2", "L3", "L3b"):
            if not (a["d"] == 2 and a["n"] == 0):
                kill("CK6", fid, "live gate not ratio-insensitive "
                     "(D%d N%d)" % (a["d"], a["n"]))
        if fid == "L7":
            if a["n"] > 5:
                kill("CK6", fid, "nudge cap exceeded: N=%d" % a["n"])
            if a["d"] != 1:
                kill("CK6", fid, "cap-boundary disp wrong: D=%d" % a["d"])
    # CK5: reversal completeness
    if not (A["S1b"]["n"] == 0):
        kill("CK5", "S1b", "popularity residue after reversal: N=%d"
             % A["S1b"]["n"])
    if A["S3b"]["s"] != "Quince":
        kill("CK5", "S3b", "installed truth dislodged by popular reversal "
             "(S=%s)" % A["S3b"]["s"])
    if A["S4b"]["d"] != 2:
        kill("CK5", "S4b", "gate asymmetric on installed lie: D=%d"
             % A["S4b"]["d"])
    # CK4/P5 trust-boundary expectation (preregistered: I==7, V==1)
    if not (A["P5"]["i"] == 7 and A["P5"]["v"] == 1
            and A["P5"]["s"] == "Xylyl"):
        kill("CK4", "P5", "trust-boundary case off-spec "
             "(I%d V%d S%s)" % (A["P5"]["i"], A["P5"]["v"], A["P5"]["s"]))

    # Report tables, per family
    print("\n%-5s %-11s %10s %14s %14s" % ("fid", "family", "BEFORE",
                                          "AFTER", "CONTROL"))
    for fam in ("poison", "sleeper-rev", "ladder", "sockpuppet"):
        for fid in fids:
            if A[fid]["fam"] != fam:
                continue
            b, a, c = B[fid], A[fid], C[fid]
            bs = "D%d/I%d" % (b["d"], b["i"])
            as_ = "D%d/N%d/F%d/I%d/V%d" % (a["d"], a["n"], a["f"], a["i"],
                                          a["v"])
            cs = "D%d/N%d/F%d/I%d" % (c["d"], c["n"], c["f"], c["i"])
            print("%-5s %-11s %10s %14s %14s" % (fid, fam, bs, as_, cs))
        print("")

    for bar, expect in (("CK1", "never-settles-on-popularity"),
                        ("CK2", "bend-only-vs-control"),
                        ("CK3", "evidence-gate"),
                        ("CK4", "poison-never-installs"),
                        ("CK5", "reversal-completeness"),
                        ("CK6", "ladder-thresholds"),
                        ("CK7", "determinism"),
                        ("CK8", "zero-RNG")):
        tripped = [k for k in kills if k[0] == bar]
        if tripped:
            print("%s (%s): KILL TRIPPED" % (bar, expect))
            for _, fid, why in tripped:
                print("    %s: %s" % (fid, why))
        else:
            print("%s (%s): HOLD" % (bar, expect))

    # MW sibling port: report only, no kill bars
    print("\n--- MW sibling port (report only) ---")
    print("%-6s %28s %28s" % ("case", "FROZEN", "PORT"))
    MF = parse_mw("mw_frozen")
    MP = parse_mw("mw_port")
    for cid in sorted(set(MF) & set(MP)):
        f, p = MF[cid], MP[cid]
        fs = "%s/%s/%s" % ("CONVERGE" if f["v"] == "1" else "WITHHOLD",
                           f["c"] or "-", f["rule"])
        ps = "%s/%s/%s" % ("CONVERGE" if p["v"] == "1" else "WITHHOLD",
                           p["c"] or "-", p["rule"])
        mark = "  <-- CHANGED" if fs != ps else ""
        print("%-6s %28s %28s%s" % (cid, fs, ps, mark))

    if kills:
        print("\nRESULT: %d kill(s) tripped" % len(kills))
        return 1
    print("\nRESULT: all WS3-C kill bars HOLD")
    return 0


if __name__ == "__main__":
    sys.exit(main())
