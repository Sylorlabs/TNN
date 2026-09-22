#!/usr/bin/env python3
"""Analyze throughput battery logs. Prints median + range per measurement."""
import glob, os, statistics, re

RUNS = os.path.expanduser("~/workspace/tnn-lab/ops/throughput/runs")

def parse_kv(line):
    d = {}
    for part in line.split(",")[1:]:
        if "=" in part:
            k, v = part.split("=", 1)
            d[k.strip()] = v.strip()
    return d

def collect(prefix, key):
    vals = []
    for f in sorted(glob.glob(os.path.join(RUNS, prefix + "*.log"))):
        with open(f) as fh:
            for line in fh:
                line = line.strip()
                if line.startswith(key + ","):
                    vals.append((f, parse_kv(line)))
    return vals

def stats(xs):
    xs = sorted(xs)
    return f"median={statistics.median(xs):.1f} range=[{xs[0]:.1f},{xs[-1]:.1f}] n={len(xs)}"

print("## INSTALL (teach path, per pass)")
for N in (240, 2400, 24000, 240000):
    rows = collect(f"learner_N{N}_rep", "THRU_INSTALL")
    us = [float(r["ns_teach_total"]) / float(r["facts"]) / 1000.0 for _, r in rows]
    truth_us = [float(r["ns_truth_total"]) / float(r["facts"]) / 1000.0 for _, r in rows]
    fps = [1e9 / (float(r["ns_teach_total"]) / float(r["facts"])) for _, r in rows]
    print(f"N={N}: teach µs/fact: {stats(us)} | truth-derive µs/fact: {stats(truth_us)} | facts/sec: {stats(fps)}")

print("\n## RECALL microbenchmark (read-only sc_recall sweeps)")
for N in (240, 2400, 24000, 240000):
    rows = collect(f"learner_N{N}_rep", "THRU_RECALL")
    ns = [float(r["ns_total"]) / float(r["recalls"]) for _, r in rows]
    pps = [float(r["recalls"]) / (float(r["ns_total"]) / 1e9) for _, r in rows]
    print(f"N={N}: ns/probe: {stats(ns)} | probes/sec: {stats(pps)}")

print("\n## EVAL SWEEP (one full recall sweep w/ truth derivation)")
for N in (240, 2400, 24000, 240000):
    rows = collect(f"learner_N{N}_rep", "THRU_EVALSWEEP")
    ns = [float(r["ns_total"]) / float(r["probes"]) for _, r in rows]
    print(f"N={N}: ns/probe: {stats(ns)}")

print("## INSTALL CPU ANCHOR (process CPU clock, contention-robust)")
for N in (240, 2400, 24000, 240000):
    vals = []
    for f in sorted(glob.glob(os.path.join(RUNS, f"learner_N{N}_rep*.log"))):
        with open(f) as fh:
            for line in fh:
                line = line.strip()
                if line.startswith("THRU_INSTALL,"):
                    r = parse_kv(line)
                    if "ns_teach_cpu_total" in r:
                        vals.append(float(r["ns_teach_cpu_total"]) / float(r["facts"]) / 1000.0)
    if vals:
        fps = [1000.0 / v * 1000.0 for v in vals]
        print(f"N={N}: teach CPU µs/fact: {stats(vals)} | facts/sec (CPU): {stats(fps)}")

print("\n## OPS/fact sanity (driver's own accounting)")
for N in (240, 2400, 24000, 240000):
    vals = []
    for f in sorted(glob.glob(os.path.join(RUNS, f"learner_N{N}_rep*.log"))):
        with open(f) as fh:
            for line in fh:
                m = re.match(r"SCALE_OPS,add=(\d+),verify=(\d+),audit=(\d+),find=(\d+),total=(\d+),ops_per_fact_x1000=(\d+)", line.strip())
                if m:
                    vals.append(int(m.group(6)) / 1000.0)
    print(f"N={N}: ops/fact: {stats(vals)}")

print("\n## DIALOGUE (deliberation + emission, 370-turn battery)")
rows = collect("dialogue_rep", "THRU_TURNS")
ms = [float(r["ns_total"]) / float(r["turns"]) / 1e6 for _, r in rows]
eps = [float(r["turns"]) / (float(r["ns_total"]) / 1e9) for _, r in rows]
ee_cps = [float(r["chars_total"]) / (float(r["ns_total"]) / 1e9) for _, r in rows]
print(f"turn ms/turn: {stats(ms)} | episodes/sec: {stats(eps)} | end-to-end chars/sec: {stats(ee_cps)}")
rows = collect("dialogue_rep", "THRU_EMIT")
us = [float(r["ns_total"]) / float(r["emits"]) / 1000.0 for _, r in rows]
cps = [float(rt["chars_total"]) / (float(r["ns_total"]) / 1e9) for (f, r), (f2, rt) in zip(rows, collect("dialogue_rep", "THRU_TURNS"))]
print(f"emit µs/utterance: {stats(us)} | emission chars/sec: {stats(cps)}")

print("\n## PASS/FAIL sanity")
for f in sorted(glob.glob(os.path.join(RUNS, "dialogue_rep*.log"))):
    with open(f) as fh:
        t = fh.read()
    print(os.path.basename(f), "PASS=", t.count(" PASS"), "FAIL=", t.count(" FAIL"))
