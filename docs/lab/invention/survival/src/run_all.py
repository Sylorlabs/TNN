#!/usr/bin/env python3
"""Final runner for TNN Experiment 1: Invent-to-Survive.
Runs all 5 arms x 12 variants = 60 runs. Outputs results.tsv + traces.
Deterministic: agents are pure Zag, zero RNG in decision paths.
"""
import subprocess, hashlib, os, sys

BUILD = os.path.dirname(os.path.abspath(__file__))
OUTDIR = sys.argv[1] if len(sys.argv) > 1 else BUILD

ARMS = [
    ("p",  ["./agent_p"], {}),
    ("z",  ["./agent_z"], {}),
    ("r",  ["./agent_r"], {}),
    ("is", ["./agent_i"], {"goal": "survive"}),
    ("ii", ["./agent_i"], {"goal": "invent"}),
]

def run_one(arm, bin_args, extra, v):
    cmd = bin_args + [f"worlds/v{v:02d}.txt", str(v), "0"]
    if extra.get("goal"):
        cmd.append(extra["goal"])
    r = subprocess.run(cmd, cwd=BUILD, capture_output=True, text=True, timeout=120)
    result = disc = trace = None
    for line in r.stdout.splitlines():
        if line.startswith("RESULT"): result = line
        elif line.startswith("DISC"): disc = line
        elif line.startswith("TRACE"): trace = line
    return result, disc, trace

def main():
    rows = []
    traces = {}
    for arm, bin_args, extra in ARMS:
        for v in range(12):
            result, disc, trace = run_one(arm, bin_args, extra, v)
            # RESULT <arm> <variant> <rerun> <ticks> <cause> <e_death> <c122> <n_take> <n_combine> <n_drop> <c126>
            parts = result.split()
            # parts[0]=RESULT, [1]=arm, [2]=variant, [3]=rerun, [4]=ticks, [5]=cause,
            # [6]=e_death, [7]=c122, [8]=n_take, [9]=n_combine, [10]=n_drop, [11]=c126
            ticks = int(parts[4]); cause = int(parts[5])
            rows.append((arm, v, ticks, cause,
                         int(parts[6]), int(parts[7]), int(parts[8]), int(parts[9]), int(parts[10]),
                         disc if disc else ""))
            traces[(arm, v)] = trace if trace else ""
            print(f"{arm} v{v:02d}: ticks={ticks} cause={cause}", flush=True)
    # results.tsv
    tsv_path = os.path.join(OUTDIR, "results.tsv")
    with open(tsv_path, "w") as f:
        f.write("arm\tvariant\tticks\tcause\te_death\tn_take\tn_combine\tn_drop\tdisc\n")
        for r in rows:
            # r = (arm, v, ticks, cause, e_death, c122, n_take, n_combine, n_drop, disc)
            f.write(f"{r[0]}\t{r[1]}\t{r[2]}\t{r[3]}\t{r[4]}\t{r[6]}\t{r[7]}\t{r[8]}\t{r[9]}\n")
    # traces
    tr_path = os.path.join(OUTDIR, "traces.tsv")
    with open(tr_path, "w") as f:
        f.write("arm\tvariant\ttrace\n")
        for (arm, v), tr in traces.items():
            f.write(f"{arm}\t{v}\t{tr}\n")
    # sha256
    h = hashlib.sha256(open(tsv_path, "rb").read()).hexdigest()
    print(f"results.tsv SHA-256: {h}")
    with open(os.path.join(OUTDIR, "results.sha256"), "w") as f:
        f.write(f"{h}  results.tsv\n")

if __name__ == "__main__":
    main()
