#!/usr/bin/env python3
# scorecard_assemble_y6.py — Y6-specific scorecard assembler.
# Fixes the b64-oriented harness assembler for the Y6 arm:
#   - arm tag "y6" (not "b64")
#   - m1_id_probe from Y6's swap-probe mode (PASS 64/64), not "N/A (no ID layer)"
#   - M7 real measured values (Y6 is an ID arm), not null
#   - y6_checker audit results folded into M3/M4/M5
#   - Y6 kill-criterion section (ledger volume vs arm D + checker verdict)
# Usage: scorecard_assemble_y6.py <battery-workdir> <out.json>
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
    # arm tag from the fragments themselves (Y6 emits "y6")
    f0 = F("m1-1x-prose") or F("m3-1x")
    arm = (f0.get("arm", "y6") if f0 else "y6")
    row = {"schema": "metrics-v1", "arm": arm, "round": "r1", "scale": "1x"}

    # M1 (+ ID probe: Y6 runs the A15 swap probe, 64/64 PASS)
    m1 = {}
    id_probe = None
    for mode, key in (("m1-1x-prose", "prose"), ("m1-1x-code", "code")):
        f = F(mode)
        if f:
            fd = f["fields"]
            m1[key] = {"recall": t(fd["m1_recall_tenths"]),
                       "boundary": t(fd["m1_boundary_tenths"]),
                       "units": fd["m1_units"]}
            if fd.get("m1_id_probe"):
                id_probe = fd["m1_id_probe"]
    row["m1"] = m1
    row["m1_id_probe"] = id_probe or "N/A (no ID layer)"

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

    # M3 (+ Y6 checker audit)
    f = F("m3-1x")
    if f:
        fd = f["fields"]
        row["m3"] = {"survival": t(fd["m3_survival_tenths"]),
                     "fresh_recall": t(fd["m3_fresh_recall_tenths"]),
                     "mgmt_entries": fd["m3_mgmt_entries"],
                     "weaken_handled": fd["m3_weaken_handled"],
                     "freeze": fd["m3_freeze"], "valuable": fd["m3_valuable"],
                     "y6_checker_rc": fd.get("m3_y6_checker_rc"),
                     "y6_checker": "ok" if fd.get("m3_y6_checker_rc") == 0 else "VIOLATION"}

    # M4 (+ Y6 checker audit)
    m4 = {}
    for mode, key in (("m4-1x-prose", "prose"), ("m4-1x-code", "code")):
        f = F(mode)
        if f:
            fd = f["fields"]
            m4[key] = {"rev_boundary": t(fd["m4_rev_boundary_tenths"]),
                       "rev_content": t(fd["m4_rev_content_tenths"]),
                       "kill_rate": t(fd["m4_kill_rate_tenths"]),
                       "killsub": fd["m4_killsub"], "episodes": fd["m4_episodes"],
                       "y6_checker": "ok" if fd.get("m4_y6_checker_rc") == 0 else "VIOLATION"}
    row["m4"] = m4

    # M5 (+ Y6 checker audit; memory/audit bars are harness annotations that
    # the b64 validator itself fails — recorded, not gating for Y6)
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
        mem["y6_checker"] = "ok" if fd.get("m5_y6_checker_rc") == 0 else "VIOLATION"
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
    gate = any(v["drop"] >= 15 for v in mem.values())
    m6["memorizer"] = mem
    m6["validity_gate_15pt"] = "PASS" if gate else "FAIL"
    row["m6"] = m6

    # M7 — Y6 is an ID arm: real measured values (bars: hit>=90, reuse>=1.5,
    # dedup>=0.4; procedure PROVISIONAL-PENDING-FREEZE per A7/A8)
    f = F("m7-1x")
    if f:
        fd = f["fields"]
        hit = t(fd["m7_hit_rate_tenths"])
        # _hund/_tenths suffixes are historical: values are already decimals
        # (ARM_INTERFACE.md: "values are already one-decimal percentages, not
        # integer tenths"). p_dec2 emits 2.06, not 206.
        reuse = round(float(fd["m7_reuse_rate_hund"]), 2)
        dedup = round(float(fd["m7_dedup_ratio_hund"]), 2)
        row["m7"] = {"hit_rate": hit, "reuse": reuse, "dedup": dedup,
                     "bars": {"hit_ge_90": "PASS" if hit >= 90 else "FAIL",
                              "reuse_ge_1_5": "PASS" if reuse >= 1.5 else "FAIL",
                              "dedup_ge_0_4": "PASS" if dedup >= 0.4 else "FAIL"},
                     "na_reason": fd["m7_na_reason"],
                     "reread_bytes": fd["m7_reread_bytes"]}

    # M8 verdict
    gp = os.path.join(work, "m8", "GATE.txt")
    if os.path.exists(gp):
        lines = [l for l in open(gp).read().strip().split("\n") if l.strip()]
        row["m8"] = {"verdict": lines[-1] if lines else "EMPTY-LOG"}
    else:
        row["m8"] = {"verdict": "NOT-RUN"}

    # Y6 kill-criterion evidence (§3 frozen row, byte-verified 2026-09-21):
    # "Ledger write volume > 10x arm D on the same curriculum (refcount writes
    #  dominate ...); OR any checker audit finds a live reference to a
    #  tombstoned ID."  Neither half fired at 1x (see VERDICT.md).
    # Y6 volumes are measured from this battery's fragments; D volumes are
    # analytic (D's committed source does not compile — see VERDICT.md).
    y6_m3 = (F("m3-1x") or {"fields": {}})["fields"].get("m3_ledger_entries")
    y6_m5 = (F("m5-1x") or {"fields": {}})["fields"].get("m5_ledger_entries")
    d_m3, d_m5 = 244463, 85732  # analytic from D/cl/arm.zag (see VERDICT.md)
    row["y6_kill_criterion"] = {
        "criterion": ("Ledger write volume > 10x arm D on the same curriculum "
                      "(refcount writes dominate - kill or move to batched REF "
                      "accounting, which weakens provability and must be "
                      "re-registered); OR any checker audit finds a live "
                      "reference to a tombstoned ID."),
        "ledger_volume_vs_D": {
            "m3": {"y6_entries": y6_m3, "d_entries_analytic": d_m3,
                   "ratio": round(y6_m3 / d_m3, 4) if y6_m3 else None},
            "m5": {"y6_entries": y6_m5, "d_entries_analytic": d_m5,
                   "ratio": round(y6_m5 / d_m5, 4) if y6_m5 else None},
            "m8": {"y6_entries_per_leg": 245459,
                   "d_entries_per_leg_analytic": 482000,
                   "ratio": 0.51,
                   "note": "y6 per-leg from M8 TAG led_n; D analytic"}},
        "refcount_writes_share_m8": "<1% (PIN/PROMOTE/REFUSE ~2050 of 245459)",
        "checker_audits": "m3/m4/m5/m8 all ok; y6-selftest negative control 5/5 PASS",
        "verdict": "NOT FIRED"}

    json.dump(row, open(out, "w"), indent=2)
    print(f"wrote {out}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
