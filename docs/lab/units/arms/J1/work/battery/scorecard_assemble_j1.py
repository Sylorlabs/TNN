#!/usr/bin/env python3
"""
J1 scorecard assembler — deterministic postprocessing for J1 fragments.

Reads METRIC_JSON fragments from work/battery/r1_1x/<mode>/fragment.json
and assembles the scorecard per ARM_INTERFACE.md.

J1-specific:
- m1_id_probe: top-level key with the A15 probe result
  (PROVISIONAL-PENDING-FREEZE). B-64 sets "N/A (no ID layer)"; J1 has an ID
  layer, so we report the probe outcome.
- m7: J1 provides hit_rate/reuse/dedup (not na_reason).
- All other keys follow the frozen interface literally.
"""
import json
import os
import sys

def load_frag(work, mode):
    p = os.path.join(work, mode, "fragment.json")
    if not os.path.exists(p):
        return None
    try:
        with open(p) as f:
            content = f.read().strip()
            if not content:
                return None
            return json.loads(content)
    except:
        return None

def t(x):
    # tenths to 0.1 precision
    return round(float(x), 1) if isinstance(x, (int, float)) else x

def main(work, out):
    F = lambda m: load_frag(work, m)
    row = {"schema": "metrics-v1", "arm": "j1", "round": "r1", "scale": "1x"}

    # M1
    m1 = {}
    id_probe = None
    for mode, key in (("m1-1x-prose", "prose"), ("m1-1x-code", "code")):
        f = F(mode)
        if f:
            fd = f["fields"]
            m1[key] = {"recall": t(fd["m1_recall_tenths"]),
                       "boundary": t(fd["m1_boundary_tenths"]),
                       "units": fd["m1_units"]}
            # J1 ID probe (A15, PROVISIONAL-PENDING-FREEZE)
            if id_probe is None and "m1_id_probe" in fd:
                id_probe = fd["m1_id_probe"]
    row["m1"] = m1
    row["m1_id_probe"] = id_probe if id_probe else "NOT-RUN (PROVISIONAL-PENDING-FREEZE)"

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

    # M3
    f = F("m3-1x")
    if f:
        fd = f["fields"]
        row["m3"] = {"survival": t(fd["m3_survival_tenths"]),
                     "fresh_recall": t(fd["m3_fresh_recall_tenths"]),
                     "mgmt_entries": fd["m3_mgmt_entries"],
                     "weaken_handled": fd["m3_weaken_handled"],
                     "freeze": fd["m3_freeze"], "valuable": fd["m3_valuable"]}

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
        # RSS delta: read from stdout.log if available, else None
        rss_delta = None
        # Try to get RSS from the run logs (if the harness captured it)
        # For now, use the fragment fields directly
        src = fd["m5_source_bytes_learned"]
        mem = {"units_learned": fd["m5_units_learned"],
               "source_bytes": src,
               "slot_table_bytes": fd["m5_slot_table_bytes"],
               "ledger_bytes": fd["m5_ledger_bytes"],
               "ledger_entries": fd["m5_ledger_entries"],
               "corpus_buffer_bytes": fd["m5_corpus_buffer_bytes"],
               "rss_delta_bytes": rss_delta}
        # Memory bar requires RSS; without it, mark as UNKNOWN
        mem["memory_per_source_byte"] = None
        mem["memory_bar_1_5x"] = "UNKNOWN (no RSS)"
        kb = src / 1024 if src else 0
        if kb > 0:
            mem["audit_entries_per_kb"] = round(fd["m5_ledger_entries"] / kb, 3)
            mem["audit_bar_10_per_kb"] = ("PASS" if fd["m5_ledger_entries"] / kb <= 10
                                          else "FAIL")
        row["m5"] = mem

    # M6 + memorizer gate
    m6 = {}
    for mode, key in (("m6-p2c-1x", "p2c"), ("m6-c2p-1x", "c2p")):
        f = F(mode)
        if f:
            fd = f["fields"]
            m6[key] = {"recall": t(fd["rec_tenths"]), "boundary": t(fd["bnd_tenths"]),
                       "revision": t(fd["rev_tenths"]), "tax": t(fd["tax_tenths"])}
    mem = {}
    for mode, key in (("memctrl-p2c-1x", "p2c"), ("memctrl-c2p-1x", "c2p")):
        f = F(mode)
        if f:
            fd = f["fields"]
            mem[key] = {"indomain": t(fd["memctrl_indomain_recall_tenths"]),
                        "transfer": t(fd["memctrl_transfer_recall_tenths"]),
                        "drop": t(fd["memctrl_drop_tenths"])}
    gate = any(v["drop"] >= 15 for v in mem.values()) if mem else False
    m6["memorizer"] = mem
    m6["validity_gate_15pt"] = "PASS" if gate else "FAIL"
    row["m6"] = m6

    # M7 (J1 provides metrics, not na_reason)
    f = F("m7-1x")
    if f:
        fd = f["fields"]
        if "m7_na_reason" in fd:
            row["m7"] = {"hit_rate": None, "reuse": None, "dedup": None,
                         "na_reason": fd["m7_na_reason"],
                         "reread_bytes": fd["m7_reread_bytes"]}
        else:
            row["m7"] = {"hit_rate": t(fd["m7_hit_rate_tenths"]),
                         "reuse": t(fd["m7_reuse_rate_tenths"]),
                         "dedup": fd["m7_dedup_savings_bytes"],
                         "na_reason": None,
                         "reread_bytes": fd["m7_reread_bytes"]}

    # M8 verdict
    gp = os.path.join(work, "m8", "GATE.txt")
    if os.path.exists(gp):
        with open(gp) as f:
            lines = [l for l in f.read().strip().split("\n") if l.strip()]
        row["m8"] = {"verdict": lines[-1] if lines else "EMPTY-LOG"}
    else:
        row["m8"] = {"verdict": "NOT-RUN"}

    # J1 kill criteria evidence (not in frozen schema, but required for verdict)
    j1k = {}
    for mode in ["m1-1x-prose", "m1-1x-code", "m2-t1-prose", "m2-t1-code",
                 "m2-t2-prose", "m2-t2-code", "m2-t3-1x", "m3-1x"]:
        f = F(mode)
        # Kill evidence is in stdout.log, not fragment; skip for now
    row["j1_kill"] = "see VERDICT.md for kill-criteria evaluation"

    with open(out, "w") as f:
        json.dump(row, f, indent=2)
    print(f"wrote {out}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
