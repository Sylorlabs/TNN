#!/usr/bin/env python3
# scorecard_assemble_l2.py — evidence-side scorecard assembler for arm L2.
# Mirrors the frozen harness scorecard_assemble.py but with arm="l2", the real
# M1 ID-swap probe result, real M7 ID-arm metrics, and L2 epoch/translation
# accounting folded in. Does NOT modify the frozen harness assembler.
# Usage: scorecard_assemble_l2.py <battery-workdir> <out.json>
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

def epoch_acct(fd):
    return {"epoch_bumps": fd.get("l2_epoch_bumps"),
            "xepoch_recalls": fd.get("l2_xepoch_recalls"),
            "xepoch_misses": fd.get("l2_xepoch_misses")}

def main(work, out):
    F = lambda m: load_frag(work, m)
    row = {"schema": "metrics-v1", "arm": "l2", "round": "r1", "scale": "1x"}

    # M1 (with the real provisional A15 swap-probe result)
    m1 = {}
    for mode, key in (("m1-1x-prose", "prose"), ("m1-1x-code", "code")):
        f = F(mode)
        if f:
            fd = f["fields"]
            m1[key] = {"recall": t(fd["m1_recall_tenths"]),
                       "boundary": t(fd["m1_boundary_tenths"]),
                       "units": fd["m1_units"],
                       "id_probe": fd.get("m1_id_probe"),
                       "id_changes": fd.get("l2_id_changes"),
                       "epoch": epoch_acct(fd)}
    row["m1"] = m1
    row["m1_id_probe"] = {k: v.get("id_probe") for k, v in m1.items()}

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
            "final_boundary": t(fd["m2_final_boundary_tenths"]),
            "epoch": epoch_acct(fd)}
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
                     "freeze": fd["m3_freeze"], "valuable": fd["m3_valuable"],
                     "epoch": epoch_acct(fd)}

    # M4 (with L2 within-epoch ID-change audit + cross-epoch translation audit)
    m4 = {}
    for mode, key in (("m4-1x-prose", "prose"), ("m4-1x-code", "code")):
        f = F(mode)
        if f:
            fd = f["fields"]
            m4[key] = {"rev_boundary": t(fd["m4_rev_boundary_tenths"]),
                       "rev_content": t(fd["m4_rev_content_tenths"]),
                       "kill_rate": t(fd["m4_kill_rate_tenths"]),
                       "killsub": fd["m4_killsub"], "episodes": fd["m4_episodes"],
                       "id_changes": fd.get("l2_id_changes"),
                       "audit_xepoch_recalls": fd.get("l2_audit_xepoch_recalls"),
                       "audit_xepoch_misses": fd.get("l2_audit_xepoch_misses"),
                       "epoch": epoch_acct(fd)}
    row["m4"] = m4

    # M5 (literal: memory = RSS delta + slot table; audit = entries/KB)
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
        mem["epoch"] = epoch_acct(fd)
        row["m5"] = mem

    # M6 + memorizer gate
    m6 = {}
    for mode, key in (("m6-p2c-1x", "p2c"), ("m6-c2p-1x", "c2p")):
        f = F(mode)
        if f:
            fd = f["fields"]
            m6[key] = {"recall": t(fd["rec_tenths"]), "boundary": t(fd["bnd_tenths"]),
                       "revision": t(fd["rev_tenths"]), "tax": t(fd["tax_tenths"]),
                       "epoch": epoch_acct(fd)}
    mem = {}
    for mode, key in (("memctrl-p2c-1x", "p2c"), (("memctrl-c2p-1x"), "c2p")):
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

    # M7 (ID arm: real metrics; provisional C'/schedule flagged)
    f = F("m7-1x")
    if f:
        fd = f["fields"]
        row["m7"] = {"hit_rate": t(fd["m7_hit_rate_tenths"]),
                     "reuse": t(fd["m7_reuse_rate_tenths"]),
                     "dedup": t(fd["m7_dedup_tenths"]),
                     "cell": fd["m7_cell"],
                     "round2_revised": fd.get("m7_round2_revised"),
                     "provisional": "PROVISIONAL-PENDING-FREEZE: C' edit + lookup schedule",
                     "epoch": epoch_acct(fd)}

    # M8 verdict: last line of the gate log is "M8GATE PASS|FAIL"
    gp = os.path.join(work, "m8", "GATE.txt")
    if os.path.exists(gp):
        lines = [l for l in open(gp).read().strip().split("\n") if l.strip()]
        row["m8"] = {"verdict": lines[-1] if lines else "EMPTY-LOG"}
    else:
        row["m8"] = {"verdict": "NOT-RUN"}

    # L2 binding kill-bar evaluation from the evidence.
    # (i) within-epoch ID changes: l2_id_changes is a snapshot audit (RIDs
    # snapshotted at mode start, re-derived at mode end; any mismatch counts).
    # It is emitted by the m1 (dedup probe) and m4 (revision audit) modes —
    # the modes that mutate the store. No other mode emits it.
    id_modes = ("m1-1x-prose", "m1-1x-code", "m4-1x-prose", "m4-1x-code")
    id_changes = sum(
        (F(m) or {"fields": {}})["fields"].get("l2_id_changes", 0)
        for m in id_modes)
    # (ii) cross-epoch translation misses: l2_xepoch_recalls/_misses are the
    # UNIQUE instrumented cross-epoch recall counters per mode instance.
    # The M4 dedicated translation audit's recalls are already included in
    # l2_xepoch_recalls (same instance counter) — they must NOT be added
    # again. l2_audit_xepoch_* are reported below as detail only.
    x_modes = ("m1-1x-prose", "m1-1x-code",
               "m2-t1-prose", "m2-t1-code", "m2-t2-prose", "m2-t2-code",
               "m2-t3-1x", "m3-1x", "m4-1x-prose", "m4-1x-code",
               "m5-1x", "m6-p2c-1x", "m6-c2p-1x", "m7-1x")
    xrec = sum(
        (F(m) or {"fields": {}})["fields"].get("l2_xepoch_recalls", 0)
        for m in x_modes)
    xmiss = sum(
        (F(m) or {"fields": {}})["fields"].get("l2_xepoch_misses", 0)
        for m in x_modes)
    xbreak = {m: {"recalls": (F(m) or {"fields": {}})["fields"].get("l2_xepoch_recalls", 0),
                  "misses": (F(m) or {"fields": {}})["fields"].get("l2_xepoch_misses", 0)}
              for m in x_modes}
    audit_rec = sum(
        (F(m) or {"fields": {}})["fields"].get("l2_audit_xepoch_recalls", 0)
        for m in ("m4-1x-prose", "m4-1x-code"))
    audit_miss = sum(
        (F(m) or {"fields": {}})["fields"].get("l2_audit_xepoch_misses", 0)
        for m in ("m4-1x-prose", "m4-1x-code"))
    bumps = sum(
        (F(m) or {"fields": {}})["fields"].get("l2_epoch_bumps", 0)
        for m in x_modes)
    kill_i = "KILLED" if id_changes > 0 else "CLEAR"
    miss_rate = xmiss / xrec if xrec else 0.0
    kill_ii = "KILLED" if miss_rate > 0.01 else "CLEAR"
    row["l2_kill_bars"] = {
        "i_within_epoch_id_changes": id_changes, "i_verdict": kill_i,
        "i_modes_audited": list(id_modes),
        "ii_xepoch_recalls": xrec, "ii_xepoch_misses": xmiss,
        "ii_per_mode": xbreak,
        "ii_audit_xepoch_recalls_detail": audit_rec,
        "ii_audit_xepoch_misses_detail": audit_miss,
        "ii_audit_note": "audit recalls are a subset of ii_xepoch_recalls "
                         "(same instance counter); shown for detail, not "
                         "added to the denominator",
        "ii_epoch_bumps_total": bumps,
        "ii_miss_rate": round(miss_rate, 4), "ii_verdict": kill_ii,
        "note": "denominator = unique instrumented cross-epoch recalls "
                "across all metric modes. Kill bar (ii) fires only if "
                "miss rate > 1%."}
    row["l2_provisional_flags"] = [
        "A15 trainer swap probe: PROVISIONAL-PENDING-FREEZE (harness schedule)",
        "M7 C' edit + lookup schedule: PROVISIONAL-PENDING-FREEZE",
        "D-EPOCH-SEG: epoch-segment = 64 KiB (arm design decision, disclosed). "
        "Bump rule touch_n*20 > seg_next*16 is the >5%-of-segments rule with "
        "the 16x sub-segment scaling folded in.",
        "D-EPOCH-DENOM: denominator = allocated 1 MiB storage segments "
        "(seg_next), not 'live non-sealed' segments; sealed old-epoch "
        "segments inflate it, making bumps rarer (conservative direction).",
        "D-TOUCH-SRC: epoch-segment touches are counted for boundary/content "
        "defect repair and revisions, not for ingestion or plain recall.",
        "D-IDCHG: l2_id_changes is a snapshot audit (RIDs snapshotted at "
        "mode start, re-derived at mode end) in the store-mutating modes "
        "m1/m4; it is not a runtime counter in the shared recall path.",
        "D-M6: 'train on prose' = prose.bin corpus with the M2 episode loop",
        "FIX-2026-09-21: main() gated _zag_arg(3)/(4) on argc, but this znc "
        "build passes argc=0 to main (ZNC-2026-09-21-007); the m8 outdir and "
        "perturbation selector were silently empty, so no M8 artifacts were "
        "written. Fixed to read _zag_arg unconditionally; binary rebuilt; "
        "full battery rerun. No arm mechanism semantics changed.",
    ]

    json.dump(row, open(out, "w"), indent=2)
    print(f"wrote {out}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
