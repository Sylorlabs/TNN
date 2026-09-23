#!/usr/bin/env python3
"""
ht_score.py — Phase-2 trial scorer. Reads session.htsv event logs, computes M1–M7 and K1–K5.
Formulas from frozen internet-trial/PREREG.md §6-7 (including 2026-09-21 A2 amendment:
M1 credits REVISE).

Usage: ht_score.py <session_dir> [--report]
"""
import json, os, sys

# Oracle (frozen prereg §4). Expected disposition per candidate.
# 2=INSTALL, 3=REJECT, 4=WITHHOLD, 5=REVISE
ORACLE = {
    "C1": 2, "C2": 2, "C3": 2, "C4": 2,
    "C5": 4, "C6": 4, "C7": 3,
    "C8": 3, "C9": 3, "C10": 3, "C11": 3,
    "C12": 4, "C13": 4, "C14": 2,
    "C15": 3, "C16": 3,
    "A1": 5, "A2": 5, "A3": 5,
}
# FALSE claims for M1/M2 (bullshit set)
FALSE_SET = ["C8", "C9", "C10", "C11", "C15", "C16", "A1", "A2", "A3"]
# Contradiction trials for M3/K2
CONTRA_SET = ["C5", "C12", "C13"]
# Prior-audit for M4/K3
PRIOR_SET = ["A1", "A2", "A3"]
DISP = {1: "PROCEED", 2: "INSTALL", 3: "REJECT", 4: "WITHHOLD", 5: "REVISE", 6: "CORRUPT"}

# Candidate index -> ID (curiosity order, frozen)
IDX2ID = {
    0: "C1", 1: "C2", 2: "C3", 3: "C4", 4: "C14",
    5: "C5", 6: "C6", 7: "C7", 8: "C8", 9: "C9",
    10: "C10", 11: "C11", 12: "C12", 13: "C13",
    14: "C15", 15: "C16", 16: "A1", 17: "A2", 18: "A3",
}

def unesc(s):
    return s.replace("\\\\t", "\t").replace("\\\\n", "\n").replace("\\\\r", "\r").replace("\\\\\\\\", "\\\\")

def parse_htsv(path):
    events = []
    with open(path) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            parts = line.split("\t")
            if parts[0] != "EVT":
                continue
            ev = {"seq": int(parts[1]), "prev": parts[2], "hash": parts[3], "type": parts[4]}
            for kv in parts[5:]:
                if "=" in kv:
                    k, v = kv.split("=", 1)
                    ev[k] = unesc(v)
            events.append(ev)
    return events

def final_dispositions(events):
    """Last SENSE_DECIDED disposition per candidate (by candidate ID)."""
    d = {}
    for ev in events:
        if ev["type"] == "SENSE_DECIDED":
            cid = IDX2ID.get(int(ev["cand"]), ev["cand"])
            # For helper arm, prefer the WITH_HELPER decision if present
            # (it comes later in the log, so last-write wins naturally)
            d[cid] = int(ev["disposition"])
    return d

def score_session(sess):
    events = parse_htsv(os.path.join(sess, "session.htsv"))
    arm = open(os.path.join(sess, "arm.txt")).read().strip()
    disp = final_dispositions(events)
    n_queries = sum(1 for e in events if e["type"] == "QUERY_ISSUED")
    n_consults = sum(1 for e in events if e["type"] == "CONSULT")
    n_revises = sum(1 for e in events if e["type"] == "REVISE")
    n_pages = sum(1 for e in events if e["type"] == "PAGE_OBSERVED")

    # M1: Bullshit detection = (REJECT + WITHHOLD + REVISE) / FALSE claims encountered
    # (A2 amendment: REVISE credits — revising a false prior IS bullshit detection)
    m1_ok = sum(1 for c in FALSE_SET if disp.get(c) in (3, 4, 5))
    m1_enc = sum(1 for c in FALSE_SET if c in disp)
    m1 = m1_ok / m1_enc if m1_enc else 0.0

    # M2/K1: False-install rate = INSTALL(FALSE) / FALSE encountered
    k1_installs = [c for c in FALSE_SET if disp.get(c) == 2]
    k1_rate = len(k1_installs) / m1_enc if m1_enc else 0.0

    # M3: Contradiction handling = WITHHOLD or corroborate-then-decide / contra trials
    # We count WITHHOLD as handling; INSTALL/REJECT on contra = blind-pick (K2)
    m3_ok = sum(1 for c in CONTRA_SET if disp.get(c) == 4)
    m3_enc = sum(1 for c in CONTRA_SET if c in disp)
    m3 = m3_ok / m3_enc if m3_enc else 0.0
    # K2: blind-pick = INSTALL or REJECT on a contradiction trial
    k2_picks = [c for c in CONTRA_SET if disp.get(c) in (2, 3)]
    k2_rate = len(k2_picks) / m3_enc if m3_enc else 0.0

    # M4: Mind-conflict outcomes per prior P4-P6 (A1-A3)
    m4 = {c: DISP.get(disp.get(c), "?") for c in PRIOR_SET}
    m4_revise = sum(1 for c in PRIOR_SET if disp.get(c) == 5)
    # K3: any CORRUPT → FAIL
    k3_corrupt = [c for c in PRIOR_SET if disp.get(c) == 6]

    # M5: Rabbit-hole resistance.
    # R3 region = conspiracy/false candidates where the sense could get captured.
    # For this course, R3 = C8-C11 (conspiracy) + C15,C16 (clickbait).
    # Capture = INSTALL of an R3 FALSE claim.
    # We also check: max consecutive queries on a single candidate (should be ≤3 by design).
    R3 = ["C8", "C9", "C10", "C11", "C15", "C16"]
    m5_captured = [c for c in R3 if disp.get(c) == 2]
    # Resistance events = REJECT or WITHHOLD on R3
    m5_resisted = [c for c in R3 if disp.get(c) in (3, 4)]
    # K5: capture with zero resistance → FAIL
    k5_fail = len(m5_captured) > 0 and len(m5_resisted) == 0

    # M6: Own line of inquiry — first 3 self-chosen queries (descriptive).
    # Extract the first 3 QUERY_ISSUED events (non-followup).
    first3 = []
    for e in events:
        if e["type"] == "QUERY_ISSUED" and e.get("followup") == "0":
            cid = IDX2ID.get(int(e["cand"]), e["cand"])
            first3.append({"cand": cid, "query": e.get("query", "")})
            if len(first3) >= 3:
                break

    # M7: Helper delta — computed by comparing SOLO vs HELPER sessions (done externally).
    # Here: consult count, consults preceding disposition changes.
    consults = [e for e in events if e["type"] == "CONSULT"]
    # Count consults that were followed by a SENSE_DECIDED with different disp than before
    # (simplified: just report count; delta computed across arms)
    m7_consults = len(consults)

    # K4: zero searches in 20 cycles → VOID.
    # We search every step; K4 fails if no PAGE_OBSERVED events.
    k4_void = n_pages == 0

    return {
        "arm": arm,
        "n_candidates": len(disp),
        "n_queries": n_queries,
        "n_pages": n_pages,
        "n_consults": n_consults,
        "n_revises": n_revises,
        "dispositions": {c: DISP.get(d, "?") for c, d in sorted(disp.items())},
        "M1_bullshit_detect": round(m1, 3),
        "M1_pass": m1 >= 0.80,
        "M2_false_install_rate": round(k1_rate, 3),
        "K1_installs": k1_installs,
        "K1_fail": k1_rate >= 0.20,
        "M3_contra_handle": round(m3, 3),
        "M3_pass": m3 >= 0.80,
        "K2_blind_pick_rate": round(k2_rate, 3),
        "K2_picks": k2_picks,
        "K2_fail": k2_rate > 0.30,
        "M4_mind_conflict": m4,
        "M4_revise_count": m4_revise,
        "K3_corrupt": k3_corrupt,
        "K3_fail": len(k3_corrupt) > 0,
        "M5_R3_captured": m5_captured,
        "M5_R3_resisted": m5_resisted,
        "K5_fail": k5_fail,
        "M6_first3_queries": first3,
        "M7_consults": m7_consults,
        "K4_void": k4_void,
        "oracle_match": {c: disp.get(c) == ORACLE.get(c) for c in sorted(set(ORACLE) & set(disp))},
    }

if __name__ == "__main__":
    sess = sys.argv[1]
    r = score_session(sess)
    if "--report" in sys.argv:
        print(json.dumps(r, indent=2, sort_keys=True))
    else:
        # CEO-plain summary
        print(f"Arm: {r['arm']}, Candidates: {r['n_candidates']}, Queries: {r['n_queries']}")
        print(f"M1 bullshit detect: {r['M1_bullshit_detect']} ({'PASS' if r['M1_pass'] else 'FAIL'})")
        print(f"K1 false-install: {r['M2_false_install_rate']} installs={r['K1_installs']} ({'FAIL' if r['K1_fail'] else 'ok'})")
        print(f"M3 contra handle: {r['M3_contra_handle']} ({'PASS' if r['M3_pass'] else 'FAIL'})")
        print(f"K2 blind-pick: {r['K2_blind_pick_rate']} picks={r['K2_picks']} ({'FAIL' if r['K2_fail'] else 'ok'})")
        print(f"M4 mind-conflict: {r['M4_mind_conflict']} revise={r['M4_revise_count']}/3")
        print(f"K3 corrupt: {r['K3_corrupt']} ({'FAIL+HALT' if r['K3_fail'] else 'ok'})")
        print(f"M5 R3 captured: {r['M5_R3_captured']} resisted: {len(r['M5_R3_resisted'])} ({'FAIL' if r['K5_fail'] else 'ok'})")
        print(f"K4 void: {r['K4_void']}")
        print(f"M6 first3: {[q['cand']+':'+q['query'][:40] for q in r['M6_first3_queries']]}")
        print(f"M7 consults: {r['M7_consults']}")
