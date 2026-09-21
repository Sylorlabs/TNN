#!/usr/bin/env python3
# z1_scorecard_assemble.py — Z1-specific scorecard assembler.
# Reads METRIC_JSON lines from battery .out logs and M3 rerun, emits metrics-v1.
# Unlike the shared b64 assembler: arm="z1", includes real m1_id_probe and m7
# ID metrics, plus Z1 kill-criterion fields (regretted-cut rate, challenge
# revision probe). Does NOT modify shared harness infrastructure.
import sys, os, json, re

def load_json(logdir, mode):
    # battery logs: <logdir>/<mode>.out ; M3 rerun override via env
    p = os.path.join(logdir, mode + ".out")
    if not os.path.exists(p):
        return None
    for line in open(p):
        if line.startswith("METRIC_JSON "):
            return json.loads(line[len("METRIC_JSON "):])
    return None

def t(x):
    return round(float(x), 1) if isinstance(x, (int, float)) else x

def main(logdir, m3_json_path, out):
    F = lambda m: load_json(logdir, m)
    row = {"schema": "metrics-v1", "arm": "z1", "round": "r1", "scale": "1x"}

    # M1 + real ID probe (Z1 is an ID arm; probe is live, not N/A)
    m1 = {}
    for mode, key in (("m1-1x-prose", "prose"), ("m1-1x-code", "code")):
        f = F(mode)
        if f:
            fd = f["fields"]
            m1[key] = {"recall": t(fd["m1_recall_tenths"]),
                       "boundary": t(fd["m1_boundary_tenths"]),
                       "units": fd["m1_units"],
                       "id_probe": fd.get("m1_id_probe"),
                       "id_probe_note": fd.get("m1_id_probe_note")}
    row["m1"] = m1

    # M2 + M9
    m2, m9 = {}, {}
    tiers = (("m2-t1-prose", "t1", "prose"), ("m2-t1-code", "t1", "code"),
             ("m2-t2-prose", "t2", "prose"), ("m2-t2-code", "t2", "code"),
             ("m2-t3-1x", "t3", "synthetic"))
    for mode, tier, ck in tiers:
        f = F(mode)
        if not f:
            continue
        fd = f["fields"]
        m2.setdefault(tier, {})[ck] = {
            "etc": fd["m2_episodes"] if not fd["m2_censored"] else "50+",
            "censored": fd["m2_censored"],
            "rel_etc_vs_taught": None,
            "ep0_recall": t(fd["m2_ep0_recall_tenths"]),
            "final_recall": t(fd["m2_final_recall_tenths"]),
            "final_boundary": t(fd["m2_final_boundary_tenths"])}
        if "m9_shape" in fd:
            m9.setdefault(tier, {})[ck] = {
                "shape": fd["m9_shape"], "takeoff_ep": fd["m9_takeoff_ep"],
                "steepness": t(fd["m9_steepness_tenths"]),
                "late_gain": t(fd["m9_late_gain_tenths"])}
    row["m2"] = m2
    row["m9"] = m9

    # M3 (from rerun with freelist fix)
    if m3_json_path and os.path.exists(m3_json_path):
        fd = json.loads(open(m3_json_path).read())["fields"]
        row["m3"] = {"survival": t(fd["m3_survival_tenths"]),
                     "fresh_recall": t(fd["m3_fresh_recall_tenths"]),
                     "mgmt_entries": fd["m3_mgmt_entries"],
                     "weaken_handled": fd["m3_weaken_handled"],
                     "freeze": fd["m3_freeze"], "valuable": fd["m3_valuable"],
                     "note": "rerun with freelist ID-reuse fix; original run hit ID exhaustion (0% fresh recall)"}

    # M4
    m4 = {}
    for mode, key in (("m4-1x-prose", "prose"), ("m4-1x-code", "code")):
        f = F(mode)
        if f:
            fd = f["fields"]
            m4[key] = {"rev_boundary": t(fd["m4_rev_boundary_tenths"]),
                       "rev_content": t(fd["m4_rev_content_tenths"]),
                       "kill_rate": t(fd["m4_kill_rate_tenths"]),
                       "killsub": fd["m4_killsub"], "episodes": fd["m4_episodes"]}
    row["m4"] = m4

    # M5
    f = F("m5-1x")
    if f:
        fd = f["fields"]
        src = fd["m5_source_bytes_learned"]
        mem = {"units_learned": fd["m5_units_learned"],
               "source_bytes": src,
               "slot_table_bytes": fd["m5_slot_table_bytes"],
               "ledger_bytes": fd["m5_ledger_bytes"],
               "ledger_entries": fd["m5_ledger_entries"],
               "corpus_buffer_bytes": fd["m5_corpus_buffer_bytes"],
               "rss_delta_bytes": None,
               "note": "RSS delta not measured (harness STATUS not wired for Z1 battery); slot+ledger bytes reported"}
        row["m5"] = mem

    # M6
    m6 = {}
    for mode, key in (("m6-p2c-1x", "p2c"), ("m6-c2p-1x", "c2p")):
        f = F(mode)
        if f:
            fd = f["fields"]
            m6[key] = {"recall": t(fd["rec_tenths"]), "boundary": t(fd["bnd_tenths"]),
                       "revision": t(fd["rev_tenths"]), "tax": t(fd["tax_tenths"])}
    row["m6"] = m6

    # M7 with real ID metrics (not N/A)
    f = F("m7-1x")
    if f:
        fd = f["fields"]
        row["m7"] = {"hit_rate": t(fd["m7_hit_rate_tenths"]),
                     "reuse_rate_pct": fd["m7_reuse_rate_hundredths"],
                     "dedup_savings_bytes": fd["m7_dedup_savings_bytes"],
                     "dedup_ratio": t(fd["m7_dedup_ratio_tenths"]),
                     "reread_bytes": fd["m7_reread_bytes"],
                     "units": fd["m7_units"]}

    # Z1 kill-criterion fields (from M1/M4 JSON if present)
    kc = {}
    for mode in ("m1-1x-prose", "m4-1x-prose"):
        f = F(mode)
        if f:
            for k in ("z1_proposed_cuts", "z1_challenged_failed", "z1_regretted",
                      "z1_survived", "z1_live_witnesses", "z1_regret_rate_tenths",
                      "z1_challenge_rev_invalidated_tenths", "z1_arm_d_status"):
                if k in f["fields"]:
                    kc.setdefault(mode, {})[k] = f["fields"][k]
    if kc:
        row["z1_kill_metrics"] = kc
    else:
        row["z1_kill_metrics"] = {
            "note": "kill-metric counters not yet wired into arm output; "
                    "regretted-cut rate vs arm D and challenge-revision >10% "
                    "cells are BLOCKED pending implementation + arm-D baseline"}

    # M8 verdict placeholder (filled after gate)
    row["m8"] = {"verdict": "PENDING (10 runs in progress)"}

    json.dump(row, open(out, "w"), indent=2)
    print(f"wrote {out}")

if __name__ == "__main__":
    # args: <battery-logdir> <m3-json-path-or-NONE> <out.json>
    m3p = sys.argv[2] if sys.argv[2] != "NONE" else None
    main(sys.argv[1], m3p, sys.argv[3])
