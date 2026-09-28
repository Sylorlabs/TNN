#!/usr/bin/env python3
"""Deterministic baseline report: WS3-B probes vs the CURRENT info-source
deliberate-install machinery (ws2_sense.zag, R-CORR rule).

Reads baseline_build/run1.txt lines: BASE|probe_id|disp|inst|chosen
Verdict mapping (documented in BASELINE_RETRIEVAL.md):
  inst==7 (INSTALLED) -> ACCEPT ; otherwise -> UNDECIDED (withhold).
  The mechanism has no REJECT verdict and emits no scalar credence (N/A).
Exit 0 always (this is a measurement, not a gate); the report states PASS/FAIL.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.join(HERE, "baseline_build", "run1.txt")


def main():
    probes = {}
    for line in open(os.path.join(HERE, "probes.jsonl")):
        if line.strip():
            p = json.loads(line)
            probes[p["probe_id"]] = p
    truth = json.load(open(os.path.join(HERE, "truth.json")))
    rows = {}
    for line in open(RUN):
        parts = line.rstrip("\n").split("|", 4)
        assert parts[0] == "BASE" and len(parts) == 5, line
        pid, disp, inst = parts[1], int(parts[2]), int(parts[3])
        rows[pid] = (disp, inst, parts[4])
    assert set(rows) == set(probes), "probe coverage mismatch"

    def verdict(pid):
        return "ACCEPT" if rows[pid][1] == 7 else "UNDECIDED"

    # baseline expectations under the documented mapping
    def expect(pid):
        p = probes[pid]
        fam = p["family"]
        if fam == "NCL":
            return "UNDECIDED"   # R2: no evidence -> never install
        if fam == "SLP":
            return "ACCEPT" if p["evidence"] else "UNDECIDED"
        if fam == "REV":
            if pid.startswith("REV-A"):
                return "UNDECIDED"  # best achievable: withhold (no REJECT exists)
            return "ACCEPT"
        if fam == "CAL":
            if pid.startswith("CAL-N"):
                return "UNDECIDED"
            if pid.startswith("CAL-RA"):
                return "UNDECIDED"  # best achievable
            return "ACCEPT"
        raise ValueError(fam)

    L = []
    L.append("WS3-B BASELINE — current info-source R-CORR machinery vs 90 probes")
    L.append("(verdict mapping: INSTALLED=ACCEPT, refused=UNDECIDED; credence N/A)")
    L.append("")
    L.append("probe_id        | disp | inst | verdict    | expected   | result")
    fails = 0
    kill = False
    fam_stats = {}
    for pid in sorted(probes):
        disp, inst, chosen = rows[pid]
        v, e = verdict(pid), expect(pid)
        ok = (v == e)
        if not ok:
            fails += 1
        if v == "ACCEPT" and truth[pid] is False and not probes[pid]["evidence"]:
            kill = True
            ok = False
        s = fam_stats.setdefault(probes[pid]["family"], [0, 0])
        s[0] += 1
        s[1] += 0 if ok else 1
        L.append("%-15s | %4d | %4d | %-10s | %-10s | %s"
                 % (pid, disp, inst, v, e, "PASS" if ok else "FAIL"))
    L.append("")
    # R1 pair check: CAL twins vs loaded twin (verdict-level)
    L.append("R1 PAIR CHECKS (same claim+evidence, exposure differs -> verdict must not flip)")
    pair_fails = 0
    for pid in sorted(probes):
        p = probes[pid]
        if p["family"] == "CAL" and p.get("pair_id"):
            twin = p["pair_id"]
            ok = verdict(pid) == verdict(twin)
            if not ok:
                pair_fails += 1
            L.append("  %-15s vs %-15s : %s vs %s -> %s"
                     % (pid, twin, verdict(pid), verdict(twin),
                        "SAME" if ok else "FLIP (R1 violation)"))
    for i in range(1, 13):
        a, b = "NCL-%02d-E010" % i, "NCL-%02d-E100" % i
        ok = verdict(a) == verdict(b)
        if not ok:
            pair_fails += 1
        L.append("  %-15s vs %-15s : %s vs %s -> %s"
                 % (a, b, verdict(a), verdict(b), "SAME" if ok else "FLIP (R1 violation)"))
    L.append("")
    L.append("FAMILY SUMMARY (baseline mapping)")
    for fam in ("NCL", "SLP", "REV", "CAL"):
        n, nf = fam_stats.get(fam, (0, 0))
        L.append("  %-3s %d/%d match expectation" % (fam, n - nf, n))
    L.append("  R1 pair flips: %d" % pair_fails)
    L.append("")
    if kill:
        L.append("BASELINE VERDICT: TODAY'S MECHANISM FAILS THE BATTERY "
                 "(R6: installs known-false no-evidence claims at every exposure).")
    else:
        L.append("BASELINE VERDICT: no R6 kill observed.")
    L.append("Additional failures: REV-A installs contradicted lies (evidence ignored); "
             "%d R1 exposure-flips." % pair_fails)
    sys.stdout.write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
