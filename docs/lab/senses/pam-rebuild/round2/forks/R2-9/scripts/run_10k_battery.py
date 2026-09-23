#!/usr/bin/env python3
"""Run the R2-9 10,000-trial mechanical battery (B5, B6, KB-E1/E2/E5).
3 emit runs + 1 noemit run, then verify_battery.py, then score_10k.py.
Usage: run_10k_battery.py <trials.tsv> <sense_binary> <outbase>
cwd must be ~/workspace/tnn-lab (fixture paths are lab-relative).
Pure glue.
"""
import os, subprocess, sys

def main():
    trials, sense, outbase = sys.argv[1], sys.argv[2], sys.argv[3]
    log = os.path.join(outbase, "battery.log")
    os.makedirs(outbase, exist_ok=True)
    with open(log, "a") as lf:
        for name, mode in (("run1_emit", "emit"), ("run2_emit", "emit"),
                           ("run3_emit", "emit"), ("run1_noemit", "noemit")):
            outd = os.path.join(outbase, name)
            print(f"== {name} ==", flush=True)
            lf.write(f"== {name} ==\n"); lf.flush()
            r = subprocess.run([sense, "batch", trials, outd, mode],
                               capture_output=True, text=True, timeout=14400)
            out = (r.stdout or "") + (r.stderr or "")
            last = out.strip().splitlines()[-1] if out.strip() else "(no output)"
            print(last, flush=True)
            lf.write(last + f"\nrc={r.returncode}\n"); lf.flush()
            if r.returncode != 0:
                print(f"FAILED {name}", flush=True)
                return 1
    print("ALL RUNS DONE", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())
