#!/usr/bin/env python3
"""Aggregate autopilot leg measurements into evidence/autopilot_legs/SUMMARY.md + .json"""
import json, os, statistics

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "evidence", "autopilot_legs")

def pct(v):
    return round(100 * v, 1)

def main():
    rows = []
    for l in open(os.path.join(OUT, "rows.jsonl")):
        rows.append(json.loads(l))
    # dedupe: prefer non-identity rows for wall/ops; identity rows only for the BI fraction
    base = [r for r in rows if not r.get("identity_check")]
    ident = [r for r in rows if r.get("identity_check")]
    # BI fraction: ONLY rows with a real second run (wall_s2>0 on base rows,
    # or explicit identity_check rows). Single-run rows must not be counted:
    # they were initialized byte_identical=True with no comparison (bug,
    # fixed in measure_autopilot_legs.py — run2_checked field added).
    checked = {}
    for r in base:
        if r.get("wall_s2", 0) > 0:
            checked[(r["task"], r["fixture"])] = bool(r.get("byte_identical"))
    for r in ident:
        checked[(r["task"], r["fixture"])] = bool(r.get("byte_identical"))
    bi_n = len(checked)
    bi_all = sum(1 for v in checked.values() if v)

    tasks = sorted(set(r["task"] for r in base))
    per_task = {}
    for t in tasks:
        es = [r for r in base if r["task"] == t]
        walls = sorted(r["wall_s"] for r in es)
        ops = [r["ops"] for r in es]
        acc = sum(1 for r in es if r["correct"]) / len(es)
        hi = [r for r in es if r["confidence"] >= 950]
        hi_c = sum(1 for r in hi if r["correct"]) / len(es)
        conf_hist = {}
        for r in es:
            b = (r["confidence"] // 100) * 100
            conf_hist[b] = conf_hist.get(b, 0) + 1
        per_task[t] = {
            "n": len(es),
            "accuracy": round(acc, 4),
            "wall_p50": round(walls[len(walls) // 2], 3),
            "wall_p95": round(walls[int(0.95 * len(walls)) - 1], 3),
            "wall_max": round(walls[-1], 3),
            "eps_per_s": round(len(es) / sum(walls), 3),
            "ops_median": int(statistics.median(ops)),
            "ops_min": min(ops), "ops_max": max(ops),
            "conf_ge950_frac": round(len(hi) / len(es), 4),
            "conf_ge950_correct_frac": round(hi_c, 4),
            "conf_hist_100bins": {str(k): v for k, v in sorted(conf_hist.items())},
            "byte_identical": all(r["byte_identical"] for r in es if "byte_identical" in r),
        }

    # new-fixture baseline (autopilot on the frozen conscious-leg fixtures)
    newf = [r for r in base if "/test/" in r["fixture"]]
    newf_sorted = sorted(newf, key=lambda r: r["fixture"])
    newbase = [{"fixture": r["fixture"], "task": r["task"], "judgment": r["judgment"],
                "confidence": r["confidence"], "truth": r["truth"],
                "correct": r["correct"], "ops": r["ops"]} for r in newf_sorted]

    total_wall = sum(r["wall_s"] for r in base)
    summary = {
        "binary": "tnn-lab/senses/rebuild/a_raw/sense (Approach A, current pipeline = autopilot control)",
        "n_episodes": len(base),
        "byte_identical": {"checked": bi_n, "passed": bi_all},
        "overall_eps_per_s": round(len(base) / total_wall, 3),
        "per_task": per_task,
        "new_fixture_baseline": newbase,
    }
    with open(os.path.join(OUT, "autopilot_legs.json"), "w") as f:
        json.dump(summary, f, indent=1)

    L = []
    L.append("# Autopilot legs S1-S4 — measured 2026-09-23")
    L.append("")
    L.append("Binary: `tnn-lab/senses/rebuild/a_raw/sense` (Approach A, the current pipeline).")
    L.append(f"Episodes: {len(base)} (370 primary + 14 new fair-fight fixtures). "
             f"Byte-identical reruns: {bi_all}/{bi_n} PASS.")
    L.append("")
    L.append("## S1 raw throughput (episodes/sec, bulk clear stimuli)")
    L.append("")
    L.append("| task | n | eps/sec |")
    L.append("|---|---|---|")
    for t in tasks:
        L.append(f"| {t} | {per_task[t]['n']} | {per_task[t]['eps_per_s']} |")
    L.append(f"| **overall** | {len(base)} | **{summary['overall_eps_per_s']}** |")
    L.append("")
    L.append("## S2 latency floor (per-episode wall time)")
    L.append("")
    L.append("| task | p50 (s) | p95 (s) | max (s) |")
    L.append("|---|---|---|---|")
    for t in tasks:
        p = per_task[t]
        L.append(f"| {t} | {p['wall_p50']} | {p['wall_p95']} | {p['wall_max']} |")
    L.append("")
    L.append("## S3 no-uncertainty cases (deliberation adds nothing but latency)")
    L.append("")
    L.append("Fraction of episodes with autopilot confidence >= 950 AND correct:")
    L.append("")
    L.append("| task | conf>=950 frac | conf>=950 & correct frac | accuracy |")
    L.append("|---|---|---|---|")
    for t in tasks:
        p = per_task[t]
        L.append(f"| {t} | {pct(p['conf_ge950_frac'])}% | {pct(p['conf_ge950_correct_frac'])}% | {pct(p['accuracy'])}% |")
    L.append("")
    L.append("## S4 compute per episode (ops, deterministic instrumented counter)")
    L.append("")
    L.append("| task | ops median | ops min | ops max |")
    L.append("|---|---|---|---|")
    for t in tasks:
        p = per_task[t]
        L.append(f"| {t} | {p['ops_median']:,} | {p['ops_min']:,} | {p['ops_max']:,} |")
    L.append("")
    L.append("## New-fixture baseline (autopilot on the frozen conscious-leg battery)")
    L.append("")
    L.append("| fixture | task | judgment | conf | truth | correct | ops |")
    L.append("|---|---|---|---|---|---|---|")
    for r in newbase:
        L.append(f"| {r['fixture'].split('/')[-1]} | {r['task']} | {r['judgment']} | "
                 f"{r['confidence']} | {r['truth']} | {r['correct']} | {r['ops']:,} |")
    L.append("")
    txt = "\n".join(L)
    with open(os.path.join(OUT, "SUMMARY.md"), "w") as f:
        f.write(txt + "\n")
    print(txt)

if __name__ == "__main__":
    main()
