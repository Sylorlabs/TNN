#!/usr/bin/env python3
"""Aggregate three-arm results: decision battery + speed legs. Prints tables."""
import json, os, statistics

ROOT = os.path.dirname(os.path.abspath(__file__))
rows = [json.loads(l) for l in open(os.path.join(ROOT, "runs", "main", "rows.jsonl"))]
spd = [json.loads(l) for l in open(os.path.join(ROOT, "runs", "speed", "speed_rows.jsonl"))]

def mean(xs): return sum(xs) / len(xs)
def pctl(xs, q):
    s = sorted(xs); return s[min(len(s) - 1, int(q * len(s)))]

print("=" * 100)
print("DECISION BATTERY — per arm x fixture class")
print("=" * 100)
print("%-8s %-14s %5s %8s %12s %8s %10s %9s" % (
    "arm", "class", "acc", "n", "mean_wall_ms", "mean_ops", "resense%", "rss_kb"))
for arm in ("F1", "F2", "F3"):
    for leg in ("omission", "inattentional", "ambiguity", "illusion", "redteam"):
        rs = [r for r in rows if r["arm"] == arm and r["leg"] == leg]
        acc = mean([1 if r["correct"] else 0 for r in rs])
        print("%-8s %-14s %5.1f%% %8d %12.1f %8d %10.1f %9d" % (
            arm, leg, 100 * acc, len(rs),
            1000 * mean([w for r in rs for w in r["wall_s"]]),
            int(mean([r["ops"] for r in rs])),
            100 * mean([r["resense"] for r in rs]),
            int(mean([k for r in rs for k in r["peak_rss_kb"]]))))
    rs = [r for r in rows if r["arm"] == arm]
    print("%-8s %-14s %5.1f%% %8d %12.1f %8d %10.1f %9d  <-- all 14" % (
        arm, "ALL", 100 * mean([1 if r["correct"] else 0 for r in rs]), len(rs),
        1000 * mean([w for r in rs for w in r["wall_s"]]),
        int(mean([r["ops"] for r in rs])), 100 * mean([r["resense"] for r in rs]),
        int(mean([k for r in rs for k in r["peak_rss_kb"]]))))
    print("-" * 100)

print()
print("CATCHES (deliberative correct ^ F1 wrong, 12 scored fixtures):")
f1 = {r["fixture"]: r for r in rows if r["arm"] == "F1"}
for arm in ("F2", "F3"):
    catches = [r["fixture"] for r in rows if r["arm"] == arm and r["leg"] != "redteam"
               and r["correct"] and not f1[r["fixture"]]["correct"]]
    fi = [r["fixture"] for r in rows if r["arm"] == arm and r["leg"] != "redteam"
          and not r["correct"] and f1[r["fixture"]]["correct"]]
    print("  %s: %d/12 catches %s | false-install delta %d %s" % (
        arm, len(catches), catches, len(fi), fi))

print()
print("OPS RATIOS per fixture (delib_ops / F1_ops) and marginal (ops_total / p1ops):")
for r in [x for x in rows if x["arm"] in ("F2", "F3")]:
    a = f1[r["fixture"]]
    print("  %s %-22s ops=%7d F1ops=%9d ratio=%8.4f marginal=%5.2f rs=%d" % (
        r["arm"], r["leg"] + "/" + r["fixture"], r["ops"], a["ops"],
        r["ops"] / a["ops"], r["ops"] / r["p1ops"], r["resense"]))

print()
print("KILL BARS:")
for arm in ("F2", "F3"):
    catches = [r for r in rows if r["arm"] == arm and r["leg"] != "redteam"
               and r["correct"] and not f1[r["fixture"]]["correct"]]
    ratios = [r["ops"] / f1[r["fixture"]]["ops"] for r in rows if r["arm"] == arm and r["leg"] != "redteam"]
    mrt = [r["ops"] / f1[r["fixture"]]["ops"] for r in rows if r["arm"] == arm and r["leg"] == "redteam"]
    wrt = [(r["wall_s"][0]) / (f1[r["fixture"]]["wall_s"][0]) for r in rows if r["arm"] == arm and r["leg"] == "redteam"]
    print("  %s KB-D1 catches=%d -> %s" % (arm, len(catches), "KILLED" if len(catches) == 0 else "alive"))
    print("  %s KB-D2 mean_ops_ratio=%.4f catches=%d -> %s" % (
        arm, mean(ratios), len(catches),
        "KILLED" if (mean(ratios) > 2.0 and len(catches) < 3) else "alive"))
    print("  %s KB-D3 max_rt_ops_ratio=%.3f max_rt_wall_ratio=%.3f -> %s" % (
        arm, max(mrt), max(wrt),
        "KILLED" if (max(mrt) > 10 or max(wrt) > 10) else "alive"))

print()
print("=" * 100)
print("SPEED LEGS — per arm x task (370 primary fixtures; F2/F3 exclude shapetrans)")
print("=" * 100)
print("%-4s %-12s %4s %6s %9s %10s %10s %10s %9s %9s %9s %8s" % (
    "arm", "task", "n", "acc%", "eps/sec", "wall_p50", "wall_p95", "ops_med", "ops_min", "ops_max", "rs%", "bi_ok"))
for arm in ("F1", "F2", "F3"):
    for task in ("colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"):
        rs = [r for r in spd if r["arm"] == arm and r["task"] == task]
        if not rs:
            print("%-4s %-12s %4s %6s %9s" % (arm, task, 0, "-", "(router N/A)")); continue
        walls = [r["wall_s"] for r in rs]
        ops = [r["ops"] for r in rs]
        bi = [r for r in rs if "byte_identical" in r]
        acc = 100 * sum(1 for r in rs if r.get("correct")) / len(rs)
        ops_s = "      N/A" if all(o < 0 for o in ops) else "%10d" % int(statistics.median([o for o in ops if o >= 0]))
        print("%-4s %-12s %4d %6.1f %9.3f %10.3f %10.3f %s %9s %9s %8.1f %s" % (
            arm, task, len(rs), acc, len(rs) / sum(walls), pctl(walls, .5), pctl(walls, .95),
            ops_s,
            min(ops) if min(ops) >= 0 else "N/A", max(ops) if max(ops) >= 0 else "N/A",
            100 * mean([r["resense"] for r in rs]),
            "%d/%d" % (sum(1 for r in bi if r["byte_identical"]), len(bi))))
    rs = [r for r in spd if r["arm"] == arm]
    print("%-4s %-12s %4d %9.3f" % (arm, "ALL", len(rs), len(rs) / sum(r["wall_s"] for r in rs)))
    print("-" * 100)

print()
print("F1 S1-S4 VERIFICATION vs frozen (FAIR_FIGHT.md S8 / SUMMARY.md):")
frozen_acc = {"shapetrans": 100.0, "motiondir": 41.7, "colorconst": 87.5,
              "colordisc": 48.3, "timbredisc": 75.0, "pitchdisc": 83.3}
frozen_eps = {"shapetrans": 3.666, "motiondir": 2.453, "colorconst": 1.266,
              "colordisc": 1.268, "timbredisc": 0.384, "pitchdisc": 0.355}
frozen_ops = {"shapetrans": 27651, "motiondir": 28674, "colorconst": 8193,
              "colordisc": 8193, "timbredisc": 2293308, "pitchdisc": 4521065}
print("%-12s %4s %9s %9s %10s %10s" % ("task", "n", "eps/s", "frozen", "ops_med", "frozen"))
for task in frozen_acc:
    rs = [r for r in spd if r["arm"] == "F1" and r["task"] == task]
    walls = [r["wall_s"] for r in rs]; ops = [r["ops"] for r in rs]
    print("%-12s %4d %9.3f %9.3f %10d %10d" % (
        task, len(rs), len(rs) / sum(walls), frozen_eps[task],
        int(statistics.median(ops)), frozen_ops[task]))
