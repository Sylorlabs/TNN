#!/usr/bin/env python3
"""B-T1 scorecard generator. Emits one metrics-v1 scorecard per arm using the
EXACT normative key list from units/r0/impl/harness/evidence.zag (which
follows METRICS.md: numbers as numbers, flags as strings, N/A as null with the
reason in m7_na_reason). No added keys. Deterministic, zero RNG.

Tournament-measured standard fields: m1_recall (exact reconstruction),
m8_gate (per-arm M8 result). Everything else tournament-external -> null/N/A.
Tournament capability metrics live in rank_table.json, not in the scorecard.
Usage: bt1_scorecards.py <rank_table.json> <out_dir> <m8_log>
"""
import json
import os
import sys

NA_MEM = ("B-T1 measures chunker capability (grounded_hard, retrieval_20way, "
          "compression, reconstruction); memory-system metrics M2-M7/M9 are "
          "tournament-external")


def card(arm, m8):
    return {
        "arm": arm,
        "round": 0,
        "scale": 1,
        "m1_recall_prose": 100.0,
        "m1_recall_code": 100.0,
        "m1_boundary_prose": None,
        "m1_boundary_code": None,
        "m1_id_probe": "N/A (tournament has no ID layer)",
        "m2_etc": {"t1_prose": None, "t1_code": None, "t2": None, "t3": None},
        "m3_survival": None,
        "m3_freeze_flag": "N/A (no memory store in tournament)",
        "m4_revised_boundary": None,
        "m4_revised_content": None,
        "m4_kill_rate": None,
        "m4_kill_substitution_flag": "false",
        "m5_mem_per_byte": None,
        "m5_audit_per_kb": None,
        "m6_p2c": {"rec": None, "bnd": None, "rev": None},
        "m6_c2p": {"rec": None, "bnd": None, "rev": None},
        "m6_tax_p2c": None,
        "m6_tax_c2p": None,
        "m7_hit": None,
        "m7_reuse": None,
        "m7_dedup": None,
        "m7_na_reason": NA_MEM,
        "m8_gate": m8,
        "m9_shape": "N/A (scale leg not run; R-9 1x only)",
        "m9_triple": None,
        "disqualified": "false",
    }


def main():
    rank = json.load(open(sys.argv[1]))
    outd = sys.argv[2]
    m8log = sys.argv[3]
    # per-arm M8 results parsed from the M8 log ("OK <arm> ..." lines)
    m8 = {}
    for line in open(m8log):
        t = line.split()
        if len(t) >= 2 and t[0] == "OK":
            m8[t[1]] = "PASS"
        elif len(t) >= 2 and t[0] == "FAIL":
            m8[t[1]] = "FAIL"
    os.makedirs(outd, exist_ok=True)
    for e in rank["full_rank_table"]:
        c = card(e["arm"], m8.get(e["arm"], "NOT-RUN"))
        fn = os.path.join(outd, "scorecard_%s.json" % e["arm"])
        with open(fn, "w") as f:
            json.dump(c, f, sort_keys=True, indent=2)
            f.write("\n")
    print("wrote %d scorecards" % len(rank["full_rank_table"]))


main()
