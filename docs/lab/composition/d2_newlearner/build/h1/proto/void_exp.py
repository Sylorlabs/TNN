#!/usr/bin/env python3
"""Void-inference convergence experiment: run d2bin tui with all-WAIT policy,
capture OBS lines, run occupancy-gap void inference offline, report tick at
which inferred void == true void_a (from scenario file)."""
import subprocess, os, re, sys

D2BIN = os.path.expanduser("~/workspace/composition_d2_rerun/d2build/d2bin")
SDIR = os.path.expanduser("~/workspace/composition_d2_rerun/src/docs/lab/composition/d2/scenarios")

def true_void(path):
    txt = open(path).read()
    m = re.search(r"# void_a=(\d+)", txt)
    return int(m.group(1))

def parse_motes(obs):
    # motes=3:a,4:d12,...
    m = re.search(r"motes=([^\s]+)", obs)
    poss = []
    for tok in m.group(1).split(","):
        p, _ = tok.split(":")
        poss.append(int(p))
    return poss

def run_scen(path):
    proc = subprocess.Popen([D2BIN, "tui", path], stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, text=True, bufsize=1)
    seen = [0]*24
    conv_tick = None
    va = true_void(path)
    tick = 0
    while True:
        line = proc.stdout.readline()
        if not line: break
        line = line.strip()
        if line.startswith("OBS "):
            for p in parse_motes(line):
                seen[p] = 1
            # inference: adjacent unseen pair with seen on both sides
            cands = []
            for c in range(23):
                if seen[c]==0 and seen[c+1]==0:
                    if any(seen[:c]) and any(seen[c+2:]):
                        cands.append(c)
            if len(cands)==1 and cands[0]==va and conv_tick is None:
                conv_tick = tick
            tick += 1
            proc.stdin.write("6\n"); proc.stdin.flush()
        elif line.startswith("RESULT"):
            break
    proc.stdin.close(); proc.wait()
    return conv_tick, tick

files = sorted(f for f in os.listdir(SDIR) if re.match(r"^(F|W|T|FW|WF|FWF|N)-\d+\.txt$", f))
worst = 0
for f in files:
    ct, nt = run_scen(os.path.join(SDIR, f))
    flag = "" if ct is not None else "  <-- NEVER CONVERGED"
    if ct is not None: worst = max(worst, ct)
    print(f"{f}: converged@{ct} nticks={nt}{flag}")
print("worst convergence tick:", worst)
