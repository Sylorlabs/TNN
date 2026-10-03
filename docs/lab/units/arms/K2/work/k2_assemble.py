#!/usr/bin/env python3
# k2_assemble.py — K2-local metrics-v1 scorecard assembler.
# Reads K2 METRIC_JSON lines from per-mode output files and merges into one
# metrics-v1 scorecard row. Does NOT modify the frozen shared harness files.
# Usage: k2_assemble.py <smoke-dir> <out.json>
import sys, os, json, glob

def load_metrics(smoke_dir):
    frags = {}
    for fp in glob.glob(os.path.join(smoke_dir, "*.txt")):
        mode = os.path.basename(fp).replace(".txt", "")
        with open(fp, "rb") as f:
            for line in f:
                try:
                    s = line.decode("utf-8", "replace")
                except Exception:
                    continue
                if "METRIC_JSON " in s:
                    try:
                        d = json.loads(s.split("METRIC_JSON ", 1)[1].strip())
                        frags[d.get("metric", mode)] = d
                    except Exception:
                        pass
    return frags

def t(x):
    return round(float(x), 1) if isinstance(x, (int, float)) else x

def main(smoke_dir, out):
    F = load_metrics(smoke_dir)
    row = {"schema": "metrics-v1", "arm": "k2", "round": "r1", "scale": "1x"}

    # M1 (scan files directly; two fragments share metric="m1")
    m1 = {}
    m1_probe = None
    for fp in glob.glob(os.path.join(smoke_dir, "*.txt")):
        stem = os.path.basename(fp).replace(".txt", "")
        if stem not in ("m1p", "m1c"):
            continue
        with open(fp, "rb") as f:
            for line in f:
                s = line.decode("utf-8", "replace")
                if "METRIC_JSON " in s:
                    try:
                        d = json.loads(s.split("METRIC_JSON ", 1)[1].strip())
                    except Exception:
                        continue
                    if d.get("metric") != "m1":
                        continue
                    ck = "prose" if stem == "m1p" else "code"
                    m1[ck] = {"recall": t(d["m1_recall_tenths"]),
                              "boundary": t(d["m1_boundary_tenths"]),
                              "units": d["m1_nunits"],
                              "dedup_savings_tenths": d.get("m1_dedup_savings_tenths"),
                              "nlive": d.get("m1_nlive"),
                              "max_chain": d.get("m1_max_chain"),
                              "collisions": d.get("m1_collisions")}
                    if ck == "prose":
                        # A15 swap probe is PROVISIONAL-PENDING-FREEZE
                        m1_probe = {
                            "status": "PROVISIONAL-PENDING-FREEZE",
                            "detected": d.get("m1_probe_detected"),
                            "total": d.get("m1_probe_total"),
                            "pass": d.get("m1_probe_pass")}
    row["m1"] = m1
    if m1_probe:
        row["m1_id_probe"] = m1_probe

    # M2 + M9 (fragments keyed by metric; use file stems via re-scan)
    m2, m9 = {}, {}
    tier_map = {"m2-t1-prose": ("t1", "prose"), "m2-t1-code": ("t1", "code"),
                "m2-t2-prose": ("t2", "prose"), "m2-t2-code": ("t2", "code"),
                "m2t3": ("t3", "synthetic"), "m2-t3-1x": ("t3", "synthetic")}
    for fp in glob.glob(os.path.join(smoke_dir, "*.txt")):
        stem = os.path.basename(fp).replace(".txt", "")
        if stem not in tier_map:
            continue
        tier, ck = tier_map[stem]
        with open(fp, "rb") as f:
            for line in f:
                s = line.decode("utf-8", "replace")
                if "METRIC_JSON " in s:
                    try:
                        d = json.loads(s.split("METRIC_JSON ", 1)[1].strip())
                    except Exception:
                        continue
                    if d.get("metric") != "m2":
                        continue
                    m2.setdefault(tier, {})[ck] = {
                        "etc": d["m2_episodes"] if not d["m2_censored"] else "50+",
                        "censored": d["m2_censored"],
                        "ep0_recall": t(d["m2_ep0_recall_tenths"]),
                        "final_recall": t(d["m2_final_recall_tenths"]),
                        "final_boundary": t(d["m2_final_boundary_tenths"]),
                        "max_chain": d.get("m2_max_chain"),
                        "collisions": d.get("m2_collisions"),
                        "ledger_bound": d.get("m2_ledger_bound", 0)}
                    if "m9_shape" in d:
                        m9[ck] = {"shape": d["m9_shape"],
                                  "takeoff_ep": d.get("m9_takeoff_ep"),
                                  "steepness_tenths": d.get("m9_steepness_tenths"),
                                  "late_gain_tenths": d.get("m9_late_gain_tenths")}
    row["m2"] = m2
    row["m9"] = m9

    # M3
    d = F.get("m3", {})
    row["m3"] = {"survival_tenths": d.get("m3_survival_tenths"),
                 "fresh_recall_tenths": d.get("m3_fresh_recall_tenths"),
                 "liveness_windows": d.get("m3_liveness_windows"),
                 "weaken_handled": d.get("m3_weaken_handled"),
                 "freeze": "CLEAR" if not d.get("m3_frozen_flag") else "FROZEN",
                 "max_chain": d.get("m3_max_chain"),
                 "collisions": d.get("m3_collisions")}

    # M4 (scan files directly; two fragments share metric="m4")
    m4 = {}
    for fp in glob.glob(os.path.join(smoke_dir, "*.txt")):
        stem = os.path.basename(fp).replace(".txt", "")
        if not stem.startswith("m4"):
            continue
        with open(fp, "rb") as f:
            for line in f:
                s = line.decode("utf-8", "replace")
                if "METRIC_JSON " in s:
                    try:
                        d = json.loads(s.split("METRIC_JSON ", 1)[1].strip())
                    except Exception:
                        continue
                    if d.get("metric") != "m4":
                        continue
                    ck = "prose" if "p" in stem and "c" not in stem.replace("m4p", "") else \
                         "code" if "c" in stem else stem
                    # stems are m4p/m4c
                    ck = "prose" if stem == "m4p" else "code" if stem == "m4c" else stem
                    m4[ck] = {"rev_boundary_tenths": d.get("m4_rev_boundary_tenths"),
                              "rev_content_tenths": d.get("m4_rev_content_tenths"),
                              "kill_rate_tenths": d.get("m4_kill_rate_tenths"),
                              "kill_substitution": bool(d.get("m4_killsub")),
                              "max_chain": d.get("m4_max_chain"),
                              "collisions": d.get("m4_collisions")}
    row["m4"] = m4

    # M5
    d = F.get("m5", {})
    adds = d.get("m5_adds", 0) or 1
    src = d.get("m5_source_bytes_learned", 0) or 1
    mem = (d.get("m5_slot_table_bytes", 0) or 0) + (d.get("m5_arena_used_bytes", 0) or 0)
    led = d.get("m5_ledger_entries", 0) or 0
    row["m5"] = {"adds": d.get("m5_adds"),
                 "units_learned": d.get("m5_units_learned"),
                 "source_bytes": src,
                 "slot_table_bytes": d.get("m5_slot_table_bytes"),
                 "arena_used_bytes": d.get("m5_arena_used"),
                 "per_byte_memory_ratio": round(mem / src, 3),
                 "per_byte_memory_bar": 1.5,
                 "per_byte_memory_pass": (mem / src) <= 1.5,
                 "ledger_entries": led,
                 "audit_per_kb": round(led / (src / 1024), 2),
                 "audit_per_kb_bar": 10,
                 "audit_per_kb_pass": (led / (src / 1024)) <= 10,
                 "max_chain": d.get("m5_max_chain"),
                 "collisions": d.get("m5_collisions")}

    # M6 (scan files directly; two fragments share metric="m6")
    m6 = {}
    for fp in glob.glob(os.path.join(smoke_dir, "*.txt")):
        stem = os.path.basename(fp).replace(".txt", "")
        if stem not in ("m6p2c", "m6c2p_b", "m6c2p"):
            continue
        with open(fp, "rb") as f:
            for line in f:
                s = line.decode("utf-8", "replace")
                if "METRIC_JSON " in s:
                    try:
                        d = json.loads(s.split("METRIC_JSON ", 1)[1].strip())
                    except Exception:
                        continue
                    if d.get("metric") != "m6":
                        continue
                    dk = d.get("m6_dir", stem)
                    # prefer the fixed-sizing run (m6c2p_b) over the stale one
                    if dk in m6 and stem == "m6c2p":
                        continue
                    m6[dk] = {"transfer_rec_tenths": d.get("m6_transfer_rec_tenths"),
                              "transfer_bnd_tenths": d.get("m6_transfer_bnd_tenths"),
                              "transfer_rev_tenths": d.get("m6_transfer_rev_tenths"),
                              "transfer_tax_tenths": d.get("m6_transfer_tax_tenths"),
                              "max_chain": d.get("m6_max_chain"),
                              "collisions": d.get("m6_collisions")}
    row["m6"] = m6

    # M7
    d = F.get("m7", {})
    row["m7"] = {"hit_tenths": d.get("m7_hit_tenths"),
                 "reuse_hundredths": d.get("m7_reuse_hundredths"),
                 "dedup_tenths": d.get("m7_dedup_tenths"),
                 "dedup_round3_tenths": d.get("m7_dedup_round3_tenths"),
                 "max_chain": d.get("m7_max_chain"),
                 "collisions": d.get("m7_collisions")}

    # M8 (from m8_compare.py result; filled by caller)
    row["m8"] = {"gate": "PENDING"}

    # chain kill-bar summary
    chains = []
    for mk, d in F.items():
        if isinstance(d, dict):
            for k in ("m1_max_chain", "m2_max_chain", "m3_max_chain",
                      "m4_max_chain", "m5_max_chain", "m6_max_chain",
                      "m7_max_chain"):
                if k in d and d[k] is not None:
                    chains.append(d[k])
    row["k2_chain_max_all_runs"] = max(chains) if chains else None
    row["k2_chain_kill_bar"] = 4
    row["k2_chain_kill_fired"] = (max(chains) > 4) if chains else None

    with open(out, "w") as f:
        json.dump(row, f, indent=1)
    print(f"wrote {out}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
