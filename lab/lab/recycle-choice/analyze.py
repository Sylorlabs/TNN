#!/usr/bin/env python3
"""Experiment A analysis: parse battery logs, compute effect sizes C vs D.
Metrics: slot utilization, memory health, task performance, cite economy,
ledger growth, misuse leg.
"""
import os, re, glob, json
from collections import defaultdict

LOGDIR_S1 = os.path.expanduser("~/workspace/recycle-choice/logs/s1")
LOGDIR_S10 = os.path.expanduser("~/workspace/recycle-choice/logs/s10")

def parse_log(path):
    """Parse one r1 log (r2 is byte-identical by battery)."""
    d = {
        "ts": [],  # list of dicts
        "summary": None, "ledger": None, "metrics": {},
        "drops": None, "abandons": None, "invalid": None,
        "delib": [],  # (t, slot, trig, choice, reason)
    }
    with open(path) as f:
        for line in f:
            p = line.strip().split()
            if not p: continue
            if p[0] == "ST_TS" and len(p) >= 18:
                # t live audit_n cites_spent cites_saved deletes recycles dodges
                # imp_held imp_offered p3_exp drops abandons wrong_offered
                # rev_done rev_lat_sum rev_lat_n
                d["ts"].append({
                    "t": int(p[1]), "live": int(p[2]), "audit_n": int(p[3]),
                    "cites_spent": int(p[4]), "cites_saved": int(p[5]),
                    "deletes": int(p[6]), "recycles": int(p[7]),
                    "dodges": int(p[8]), "imp_held": int(p[9]),
                    "imp_offered": int(p[10]), "p3_exp": int(p[11]),
                    "drops": int(p[12]), "abandons": int(p[13]),
                    "wrong_offered": int(p[14]), "rev_done": int(p[15]),
                    "rev_lat_sum": int(p[16]), "rev_lat_n": int(p[17]),
                })
            elif p[0] == "ST_A_SUMMARY" and len(p) >= 6:
                d["summary"] = {
                    "deletes": int(p[1]), "recycles": int(p[2]),
                    "dodges": int(p[3]), "cites_spent": int(p[4]),
                    "cites_saved": int(p[5]),
                }
            elif p[0] == "ST_LEDGER" and len(p) >= 3:
                d["ledger"] = {"entries": int(p[1]), "bytes": int(p[2])}
            elif p[0] == "ST_METRIC" and len(p) >= 4:
                d["metrics"][int(p[1])] = (int(p[2]), int(p[3]))
            elif p[0] == "ST_DROPS" and len(p) >= 2:
                d["drops"] = int(p[1])
            elif p[0] == "ST_ABANDONS" and len(p) >= 2:
                d["abandons"] = int(p[1])
            elif p[0] == "ST_INVALID" and len(p) >= 2:
                d["invalid"] = int(p[1])
            elif p[0] == "ST_DELIB" and len(p) >= 9:
                # t slot trig choice reason strength price contra revimp
                d["delib"].append({
                    "t": int(p[1]), "slot": int(p[2]), "trig": int(p[3]),
                    "choice": int(p[4]), "reason": int(p[5]),
                })
    return d

def cell_key(fname):
    """cell_C_VUP_0_s1_r1.log -> (C, VUP, 0, s1)"""
    m = re.match(r"cell_([CMD])_([A-Z]+)_(\d+)_(s\d+)_r1\.log", os.path.basename(fname))
    if not m: return None
    return (m.group(1), m.group(2), int(m.group(3)), m.group(4))

def load_all(logdir):
    cells = {}
    for fp in glob.glob(os.path.join(logdir, "cell_*_r1.log")):
        k = cell_key(fp)
        if k: cells[k] = parse_log(fp)
    return cells

def summarize(cells):
    """Aggregate by (arm, scale, cur). Returns dict."""
    agg = defaultdict(list)
    for (arm, cur, v, scale), d in cells.items():
        if d["invalid"] != 0:
            print(f"WARNING: invalid cell {arm}/{cur}/{v}/{scale}")
            continue
        agg[(arm, scale, cur)].append(d)
    out = {}
    for k, ds in agg.items():
        # Endpoint metrics (mean across variants)
        n = len(ds)
        def mean(f):
            return sum(f(d) for d in ds) / n
        s = ds[0]["summary"] or {}
        final_ts = ds[0]["ts"][-1] if ds[0]["ts"] else {}
        out[k] = {
            "n_variants": n,
            "deletes": mean(lambda d: d["summary"]["deletes"]),
            "recycles": mean(lambda d: d["summary"]["recycles"]),
            "dodges": mean(lambda d: d["summary"]["dodges"]),
            "cites_spent": mean(lambda d: d["summary"]["cites_spent"]),
            "cites_saved": mean(lambda d: d["summary"]["cites_saved"]),
            "ledger_entries": mean(lambda d: d["ledger"]["entries"]),
            "ledger_bytes": mean(lambda d: d["ledger"]["bytes"]),
            "drops": mean(lambda d: d["drops"]),
            "abandons": mean(lambda d: d["abandons"]),
            # Time-series derived: per-episode rates from final TS
            "live_final": mean(lambda d: d["ts"][-1]["live"]),
            "imp_held_final": mean(lambda d: d["ts"][-1]["imp_held"]),
            "imp_offered_final": mean(lambda d: d["ts"][-1]["imp_offered"]),
            "wrong_offered": mean(lambda d: d["ts"][-1]["wrong_offered"]),
            "rev_done": mean(lambda d: d["ts"][-1]["rev_done"]),
            "rev_lat_mean": mean(lambda d: d["ts"][-1]["rev_lat_sum"] / max(1, d["ts"][-1]["rev_lat_n"])),
            # Deliberation counts
            "delib_total": mean(lambda d: len(d["delib"])),
        }
        # WBS revision rate (metric 2: honest revisions)
        rev_rates = []
        for d in ds:
            if 2 in d["metrics"]:
                done, total = d["metrics"][2]
                rev_rates.append(done / total if total else 0)
        if rev_rates:
            out[k]["honest_rev_rate"] = sum(rev_rates) / len(rev_rates)
    return out

if __name__ == "__main__":
    for name, logdir in [("S1", LOGDIR_S1), ("S10", LOGDIR_S10)]:
        print(f"\n===== {name} =====")
        cells = load_all(logdir)
        print(f"cells loaded: {len(cells)}")
        if not cells: continue
        agg = summarize(cells)
        for k in sorted(agg):
            print(f"{k}: {json.dumps(agg[k], indent=1)}")
