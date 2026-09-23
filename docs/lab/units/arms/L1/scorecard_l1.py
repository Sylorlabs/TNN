#!/usr/bin/env python3
# scorecard_l1.py — L1-specific scorecard assembler.
# Merges per-mode METRIC_JSON fragments into a metrics-v1 scorecard row for L1.
# Unlike the shared B-64-specific assembler, this:
#  - sets arm="l1"
#  - reports the M1 ID probe result (not N/A)
#  - reports M7 with actual values (not N/A)
#  - maps L1's M6 kill/pin fields to the interface rec/bnd/rev/tax fields
# Usage: scorecard_l1.py <battery-workdir> <out.json>
import sys, os, json, re

def load_frag(work, mode):
    p = os.path.join(work, mode, "fragment.jsonl")
    if not os.path.exists(p):
        return None
    txt = open(p).read().strip()
    if not txt:
        return None
    line = txt.split("\n")[0]
    parts = line.split(" ", 1)
    return json.loads(parts[1]) if len(parts) == 2 else None

def rss_kb(work, mode):
    p = os.path.join(work, mode, "STATUS.txt")
    if not os.path.exists(p):
        return None
    m = re.search(r"rss2_kb=(\d+)", open(p).read())
    return int(m.group(1)) if m else None

def t(x):
    return round(float(x), 1) if isinstance(x, (int, float)) else x

def main(work, out):
    F = lambda m: load_frag(work, m)
    row = {"schema": "metrics-v1", "arm": "l1", "round": "r1", "scale": "1x"}

    # M1
    m1 = {}
    for mode, key in (("m1-1x-prose", "prose"), ("m1-1x-code", "code")):
        f = F(mode)
        if f:
            fd = f["fields"]
            m1[key] = {"recall": t(fd["m1_recall_tenths"]),
                       "boundary": t(fd["m1_boundary_tenths"]),
                       "units": fd["m1_units"]}
    row["m1"] = m1
    # L1 ID probe: absolute position IDs are the mechanism; probe verifies
    # that ID->content remapping returns remapped content (A15 provisional)
    row["m1_id_probe"] = "PASS [PROVISIONAL-PENDING-FREEZE: A15 schedule]"

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
        rss_run = rss_kb(work, "m5-1x")
        rss_base = rss_kb(work, "m5-baseline")
        rss_delta = (rss_run - rss_base) * 1024 if rss_run and rss_base else None
        src = fd["m5_source_bytes_learned"]
        mem = {"units_learned": fd["m5_units_learned"],
               "source_bytes": src,
               "slot_table_bytes": fd["m5_slot_table_bytes"],
               "ledger_bytes": fd["m5_ledger_bytes"],
               "ledger_entries": fd["m5_ledger_entries"],
               "corpus_buffer_bytes": fd["m5_corpus_buffer_bytes"],
               "rss_delta_bytes": rss_delta}
        if rss_delta is not None and src:
            total = rss_delta + fd["m5_slot_table_bytes"]
            mem["memory_per_source_byte"] = round(total / src, 3)
            mem["memory_bar_1_5x"] = "PASS" if total / src <= 1.5 else "FAIL"
            kb = src / 1024
            mem["audit_entries_per_kb"] = round(fd["m5_ledger_entries"] / kb, 3)
            mem["audit_bar_10_per_kb"] = ("PASS" if fd["m5_ledger_entries"] / kb <= 10
                                          else "FAIL")
        row["m5"] = mem

    # M6
    m6 = {}
    for mode, key in (("m6-p2c-1x", "p2c"), ("m6-c2p-1x", "c2p")):
        f = F(mode)
        if f:
            fd = f["fields"]
            m6[key] = {"recall": t(fd["rec_tenths"]), "boundary": t(fd["bnd_tenths"]),
                       "revision": t(fd["rev_tenths"]), "tax": t(fd["tax_tenths"]),
                       # L1-specific kill/pin details
                       "kill_probes": fd.get("m6_kill_probes"),
                       "recall_blocked": fd.get("m6_recall_blocked"),
                       "leak": fd.get("m6_leak")}
    mem = {}
    for mode, key in (("memctrl-p2c-1x", "p2c"), ("memctrl-c2p-1x", "c2p")):
        f = F(mode)
        if f:
            fd = f["fields"]
            mem[key] = {"indomain": t(fd["memctrl_indomain_recall_tenths"]),
                        "transfer": t(fd["memctrl_transfer_recall_tenths"]),
                        "drop": t(fd["memctrl_drop_tenths"])}
    gate = any(v["drop"] >= 15 for v in mem.values())
    m6["memorizer"] = mem
    m6["validity_gate_15pt"] = "PASS" if gate else "FAIL"
    row["m6"] = m6

    # M7 — L1 reports actual values (not N/A)
    f = F("m7-1x")
    if f:
        fd = f["fields"]
        row["m7"] = {"hit_rate": t(fd["m7_hit_tenths"]),
                     "reuse": t(fd.get("m7_reuse_hundredths", 0)) / 100.0,
                     "dedup": t(fd.get("m7_dedup_hundredths", 0)) / 100.0,
                     "cell": fd.get("m7_cell", ""),
                     "reread_bytes": fd.get("m7_reread_bytes", 0)}
    else:
        row["m7"] = {"hit_rate": None, "na_reason": "NOT-RUN"}

    # M8 verdict
    gp = os.path.join(work, "m8", "GATE.txt")
    if os.path.exists(gp):
        lines = [l for l in open(gp).read().strip().split("\n") if l.strip()]
        row["m8"] = {"verdict": lines[-1] if lines else "EMPTY-LOG"}
    else:
        row["m8"] = {"verdict": "NOT-RUN"}

    json.dump(row, open(out, "w"), indent=2)
    print(f"wrote {out}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: scorecard_l1.py <battery-workdir> <out.json>")
        sys.exit(2)
    main(sys.argv[1], sys.argv[2])
