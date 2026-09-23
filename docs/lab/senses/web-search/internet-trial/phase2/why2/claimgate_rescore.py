#!/usr/bin/env python3
"""claimgate_rescore.py — deterministic rescoring of frozen Phase-2 dispositions
under Micah's 2026-09-22 SKEPTICISM rule.

Reads ONLY frozen dispositions from phase2/evidence/{solo,helper}/score.json.
No RNG, no timestamps, sorted iteration. Formulas mirror
phase2/supervisor/ht_score.py:
  M1 = (REJECT + WITHHOLD + REVISE) / FALSE claims encountered, bar >= 0.80
  M2/K1 = INSTALL(FALSE) / FALSE encountered, K1 trips if >= 0.20
  M3 = WITHHOLD / CONTRA encountered, bar >= 0.80
  K2 = (INSTALL|REJECT on CONTRA) / CONTRA encountered, trips if > 0.30
Scorings:
  (a) ORIGINAL            FALSE_SET as frozen in ht_score.py
  (b) SKEPTICISM-EXCLUDED remove C8, C11 (Micah's explicit ruling)
  (c) SENSITIVITY         also remove C9, C10
"""
import json
import os
import sys

BASE = os.path.expanduser(
    "~/workspace/tnn-lab/senses/web-search/internet-trial/phase2/evidence"
)

FALSE_ORIG = ["C8", "C9", "C10", "C11", "C15", "C16", "A1", "A2", "A3"]
CONTRA_SET = ["C5", "C12", "C13"]

SCORINGS = [
    ("a", "ORIGINAL", FALSE_ORIG),
    ("b", "SKEPTICISM-EXCLUDED", [c for c in FALSE_ORIG if c not in ("C8", "C11")]),
    ("c", "SENSITIVITY", [c for c in FALSE_ORIG if c not in ("C8", "C11", "C9", "C10")]),
]


def score_arm(arm, false_set):
    with open(os.path.join(BASE, arm, "score.json")) as f:
        data = json.load(f)
    disp = data["dispositions"]
    enc = sorted(c for c in false_set if c in disp)
    m1_ok = sum(1 for c in enc if disp[c] in ("REJECT", "WITHHOLD", "REVISE"))
    k1_installs = [c for c in false_set if disp.get(c) == "INSTALL"]
    # frozen scorer lists installs in FALSE_SET order; keep a sorted copy for display
    k1_installs_sorted = sorted(k1_installs)
    m1 = m1_ok / len(enc)
    k1 = len(k1_installs) / len(enc)
    # M3/K2 unchanged under the rule (C5/C12/C13 are CONTESTED/AMBIGUOUS, never SKEPTICISM)
    cenc = sorted(c for c in CONTRA_SET if c in disp)
    m3 = sum(1 for c in cenc if disp[c] == "WITHHOLD") / len(cenc)
    k2 = sum(1 for c in cenc if disp[c] in ("INSTALL", "REJECT")) / len(cenc)
    return {
        "arm": arm,
        "false_set": sorted(false_set),
        "n_enc": len(enc),
        "M1_ok": m1_ok,
        "M1": round(m1, 3),
        "M1_pass": m1 >= 0.80,
        "K1_installs": k1_installs,
        "K1_installs_sorted": k1_installs_sorted,
        "K1_rate": round(k1, 3),
        "K1_trip": k1 >= 0.20,
        "M3": round(m3, 3),
        "M3_pass": m3 >= 0.80,
        "K2_rate": round(k2, 3),
        "K2_trip": k2 > 0.30,
        # cross-check fields vs frozen scorer output
        "frozen_M1": data["M1_bullshit_detect"],
        "frozen_M1_pass": data["M1_pass"],
        "frozen_K1_rate": data["M2_false_install_rate"],
        "frozen_K1_trip": data["K1_fail"],
        "frozen_K1_installs": data["K1_installs"],
    }


def main():
    arms = ["solo", "helper"]  # fixed order, no timestamps, no randomness
    results = {}
    for code, name, fset in SCORINGS:
        rows = [score_arm(a, fset) for a in arms]
        results[code] = {"name": name, "rows": rows}
    # Cross-check: scoring (a) must reproduce frozen values exactly
    xcheck = []
    for r in results["a"]["rows"]:
        ok = (
            r["M1"] == r["frozen_M1"]
            and r["M1_pass"] == r["frozen_M1_pass"]
            and r["K1_rate"] == r["frozen_K1_rate"]
            and r["K1_trip"] == r["frozen_K1_trip"]
            and r["K1_installs"] == r["frozen_K1_installs"]
        )
        xcheck.append((r["arm"], "MATCH" if ok else "MISMATCH"))
        if not ok:
            sys.exit("CROSS-CHECK FAILED for arm %s" % r["arm"])
    out_lines = []
    for code, name, _fset in SCORINGS:
        blk = results[code]
        out_lines.append("== scoring (%s) %s ==" % (code, name))
        out_lines.append("false_set = %s" % json.dumps(blk["rows"][0]["false_set"]))
        for r in blk["rows"]:
            out_lines.append(
                "arm=%-6s M1=%d/%d=%.3f pass=%s | K1_rate=%.3f installs=%s trip=%s | "
                "M3=%.3f pass=%s | K2=%.3f trip=%s"
                % (
                    r["arm"],
                    r["M1_ok"],
                    r["n_enc"],
                    r["M1"],
                    r["M1_pass"],
                    r["K1_rate"],
                    json.dumps(r["K1_installs_sorted"]),
                    r["K1_trip"],
                    r["M3"],
                    r["M3_pass"],
                    r["K2_rate"],
                    r["K2_trip"],
                )
            )
    out_lines.append("== cross-check (a) vs frozen scorer ==")
    for arm, status in xcheck:
        out_lines.append("arm=%s frozen-repro=%s" % (arm, status))
    print("\n".join(out_lines) + "\n")


if __name__ == "__main__":
    main()
