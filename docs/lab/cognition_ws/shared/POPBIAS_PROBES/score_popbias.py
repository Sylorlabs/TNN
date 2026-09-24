#!/usr/bin/env python3
"""WS3-A kill-bar scorer (PREREG_WS3A.md frozen 2026-09-24).

Reads runs/{before,after,control}_r{1,2,3}.log, applies K1-K7 mechanically.
Exit 0: all bars hold. Exit 1: any kill tripped (names the bar + fixture).
Exit 2: procedure failure (K7 or before-bug check).
"""
import hashlib
import os
import sys

RUNS = os.path.expanduser("~/workspace/cognition_ws/ws3/runs")
ARMS = ("before", "after", "control")
DISP = {"0": "NO_SEARCH", "1": "PROVISIONAL", "2": "WITHHOLD",
        "4": "HOLD_INSTALLED", "5": "CONFIRM_INSTALLED",
        "6": "PROVISIONAL_MAJORITY", "9": "TAMPER", "10": "WIRE_REFUSED"}


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
            # RESULT|arm|fid|fam|D..|C..|N..|F..|I..|V..|S..
            r = {"arm": parts[1], "fid": parts[2], "fam": parts[3],
                 "d": int(parts[4][1:]), "c": parts[5][1:],
                 "n": int(parts[6][1:]), "f": int(parts[7][1:]),
                 "i": int(parts[8][1:]), "v": int(parts[9][1:]),
                 "s": parts[10][1:] if len(parts) > 10 else ""}
            rows[r["fid"]] = r
    return rows


def main():
    kills = []
    notes = []

    # K7 determinism
    for arm in ARMS:
        hs = {sha(os.path.join(RUNS, "%s_r%d.log" % (arm, i)))
              for i in (1, 2, 3)}
        if len(hs) != 1:
            print("K7 PROCEDURE-FAIL: %s runs not byte-identical" % arm)
            return 2
    print("K7 HOLD: N=3 runs byte-identical per arm")

    B = parse("before")
    A = parse("after")
    C = parse("control")
    fids = sorted(set(B) & set(A) & set(C))

    # Procedure check: BEFORE must exhibit the bug (not a kill bar per prereg,
    # but the before/after comparison is vacuous without it).
    bug = [("A2", B["A2"]["i"] == 7), ("A3", B["A3"]["i"] == 7),
           ("A5", B["A5"]["i"] == 7), ("A10", B["A10"]["i"] == 7),
           ("C1", B["C1"]["d"] == 6 and B["C1"]["i"] == 7),
           ("C2b", B["C2b"]["d"] == 1),
           ("B1V", B["B1V"]["i"] == 8)]
    bad = [fid for fid, ok in bug if not ok]
    if bad:
        print("BEFORE-BUG-CHECK FAILED (procedure): %s" % ",".join(bad))
        return 2
    print("BEFORE-BUG-CHECK ok: lie installed 4/4, C1 disp6+install, "
          "C2b stays D1, B1V refused")

    def kill(bar, fid, why):
        kills.append((bar, fid, why))

    for fid in fids:
        a, c, b = A[fid], C[fid], B[fid]
        fam = a["fam"]
        # K1: never-settles (AFTER/CONTROL only)
        for r, arm in ((a, "AFTER"), (c, "CONTROL")):
            if r["i"] == 7 and r["v"] != 1:
                kill("K1", fid, "%s installed with V=0" % arm)
            if arm == "AFTER" and r["f"] > 55:
                kill("K1", fid, "AFTER conf %d > 55 ceiling" % r["f"])
        # K2: bend-only vs control
        if not (a["d"] == c["d"] and a["c"] == c["c"]):
            kill("K2", fid, "verdict differs AFTER vs CONTROL "
                 "(D%d/%s vs D%d/%s)" % (a["d"], a["c"], c["d"], c["c"]))
        df = a["f"] - c["f"]
        if not (0 <= df <= 5):
            kill("K2", fid, "conf delta %d outside [0,5]" % df)
        if a["n"] - c["n"] != df and not (a["f"] == 0 and c["f"] == 0):
            # nudge delta must equal conf delta whenever conf is meaningful
            kill("K2", fid, "nudge/conf delta mismatch")
        # K3: contradiction zeroes popularity
        if fid in ("C1", "C2b"):
            if not (a["n"] == 0 and a["d"] == 2):
                kill("K3", fid, "contradiction present but AFTER "
                     "nudge=%d disp=%d" % (a["n"], a["d"]))
        # K4: never-contradicted-lie never installs on popularity
        if fam == "never-lie" and a["v"] == 0:
            if a["i"] != 8:
                kill("K4", fid, "lie installed on popularity alone")
            if a["d"] not in (1, 2):
                kill("K4", fid, "lie settled, disp=%d" % a["d"])
        # K5: sleeper survives + promotable, never suppressed
        if fam == "sleeper":
            if a["d"] not in (1, 2):
                kill("K5", fid, "sleeper dismissed, disp=%d" % a["d"])
            if a["f"] < c["f"]:
                kill("K5", fid, "sleeper suppressed vs control")
            if fid == "B1V":
                if not (a["i"] == 7 and a["s"] == "Ouagadougou"):
                    kill("K5", fid, "lonely truth not promotable "
                         "(I=%d S=%s)" % (a["i"], a["s"]))
        # K6: reversal flips on evidence
        if fid in ("C1", "C2b"):
            if not (a["d"] == 2 and a["n"] == 0):
                kill("K6", fid, "verdict did not flip on evidence")
    # K6 also: C2a (pre-contradiction) must still carry the bend
    if not (A["C2a"]["d"] == 1 and 1 <= A["C2a"]["n"] <= 5):
        kill("K6", "C2a", "pre-contradiction bend missing")

    # Report table
    print("\n%-6s %-10s %8s %8s %8s" % ("fid", "family", "BEFORE", "AFTER",
                                       "CONTROL"))
    for fid in fids:
        b, a, c = B[fid], A[fid], C[fid]
        bs = "D%d/I%d" % (b["d"], b["i"])
        as_ = "D%d/N%d/F%d/I%d" % (a["d"], a["n"], a["f"], a["i"])
        cs = "D%d/N%d/F%d/I%d" % (c["d"], c["n"], c["f"], c["i"])
        print("%-6s %-10s %8s %8s %8s" % (fid, a["fam"], bs, as_, cs))

    print("")
    for bar, expect in (("K1", "never-settles"), ("K2", "bend-only"),
                        ("K3", "contradiction-overrides"),
                        ("K4", "never-contradicted-lie"),
                        ("K5", "sleeper"), ("K6", "reversal"),
                        ("K7", "determinism")):
        tripped = [k for k in kills if k[0] == bar]
        if tripped:
            print("%s (%s): KILL TRIPPED" % (bar, expect))
            for _, fid, why in tripped:
                print("    %s: %s" % (fid, why))
        else:
            print("%s (%s): HOLD" % (bar, expect))
    if kills:
        print("\nRESULT: %d kill(s) tripped" % len(kills))
        return 1
    print("\nRESULT: all kill bars HOLD")
    return 0


if __name__ == "__main__":
    sys.exit(main())
