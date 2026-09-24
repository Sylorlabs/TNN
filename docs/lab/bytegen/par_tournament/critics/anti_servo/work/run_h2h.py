#!/usr/bin/env python3
"""CRITIC 4: 5-build x 15-scenario head-to-head. Builds: stock off gated x xy.
Parses traces -> work/h2h.json. Pure determinism: reruns must cmp-clean."""
import os, subprocess, json, sys

W = os.path.expanduser("~/workspace/par_critics/anti_servo")
BUILD = W + "/build"
OUT = W + "/work/h2h"
os.makedirs(OUT, exist_ok=True)
P = W + "/plans/plan_v1.txt"
T = W + "/tests/"
C = os.path.expanduser("~/workspace/par_critics/anti_servo/tests/")  # local copies

SCEN = [
    ("a_nominal",  P, "seqmix"),
    ("b_rtlong",   W + "/tests/plan_rtlong_octlie.txt", "seqmix"),
    ("c_nearmiss", C + "plan_long_460.txt", "seqmix"),
    ("d_suboct",   C + "plan_long_suboct.txt", "seqmix"),
    ("e_2oct",     C + "plan_long_2oct.txt", "seqmix"),
    ("f_vibtort",  C + "plan_long_vibtort.txt", "seqmix"),
    ("f_glide",    C + "plan_long_glide.txt", "seqmix"),
    ("g_chord16",  W + "/tests/plan_chord16.txt", "seqmix"),
    ("h_sus1292",  P, "sus1292mix"),
    ("i_rail1",    C + "plan_rail1.txt", "seqmix"),
    ("i_rail2",    C + "plan_rail2.txt", "seqmix"),
    ("drift",      W + "/tests/plan_drift.txt", "seqmix"),
    ("flap",       W + "/tests/plan_flap.txt", "seqmix"),
    ("sawbomb",    P, "sawbombmix"),
    ("edge14",     P, "edge14mix"),
]
BUILDS = ["stock", "off", "gated", "x", "xy"]

def run(build, key, plan, mode):
    wav = f"{OUT}/{build}_{key}.wav"
    log = f"{OUT}/{build}_{key}.log"
    r = subprocess.run([f"{BUILD}/render_c_{build}", plan, wav, mode],
                       capture_output=True, text=True, timeout=300)
    open(log, "w").write(r.stdout + r.stderr)
    return r.returncode, wav, log

def main():
    only = sys.argv[1:] or []
    results = {}
    if os.path.exists(OUT + "/h2h.json"):
        try:
            results.update(json.load(open(OUT + "/h2h.json")))
        except Exception:
            pass
    for b in BUILDS:
        for key, plan, mode in SCEN:
            tag = f"{b}/{key}"
            if only and not any(tag.startswith(o) for o in only):
                continue
            rc, wav, log = run(b, key, plan, mode)
            # parse summary
            adapts = vetoes = -1
            latches = []
            for line in open(log, errors="replace"):
                if line.startswith("C blocks="):
                    # C blocks=1295 vetoes=0 adapts=137 latched=0 kept=0
                    parts = dict(p.split("=") for p in line.split()[1:])
                    adapts, vetoes = int(parts["adapts"]), int(parts["vetoes"])
                if "LATCHED" in line or "ABSTAIN" in line:
                    latches.append(line.strip()[:80])
            # dsum/engage via parse_trace (trace st=1/st=2 = crew_servo convention)
            sys.path.insert(0, W + "/work")
            from parse_trace import parse
            pr = parse(log)
            adapts, vetoes = pr["adapts"], pr["vetoes"]
            engage = (adapts + vetoes) / pr["n"] if pr["n"] else 0.0
            results[tag] = dict(rc=rc, adapts=adapts, vetoes=vetoes,
                                dsum=round(pr["dsum"], 2), engage=round(engage, 3),
                                holds=pr["holds"], latch=latches[:4])
            print(f"{tag}: rc={rc} a={adapts} v={vetoes} dsum={pr['dsum']:.2f} eng={engage:.3f}",
                  flush=True)
    json.dump(results, open(OUT + "/h2h.json", "w"), indent=1)
    print("wrote", OUT + "/h2h.json")

if __name__ == "__main__":
    main()
