#!/usr/bin/env python3
"""G5 battery Leg 1: conversion on the 278. Glue only: runs the pure-Zag
g5sense binary on each trial and records its output. Scoring is done by
the pure-Zag g5score.zag."""
import json, os, re, subprocess, sys

LAB = os.path.expanduser("~/workspace/tnn-lab")
G5 = os.path.join(LAB, "senses/pam-rebuild/v2/g5_sense/src/g5sense")
VSENSE = os.path.join(LAB, "senses/pam-rebuild/v2/g5_sense/work/vsense_test_bin")
FIX = os.path.join(LAB, "senses/pam-rebuild/round2/forks/R2-4/fixtures")
SWEEP = os.path.join(LAB, "senses/pam-rebuild/round2/forks/R2-4/evidence/clean/sweep.jsonl")
CASE = os.path.join(LAB, "senses/pam-rebuild/v2/diagnostics/case_r24_rk3.txt")
OUTDIR = os.path.join(LAB, "senses/pam-rebuild/v2/g5_sense/evidence")

JCODE = {
    'colordisc': {'SAME':0,'DIFFERENT':1},
    'colorconst': {'SAME_SURFACE':0,'DIFFERENT':1},
    'shapetrans': {'SQUARE':0,'TRIANGLE':1,'CIRCLE':2},
    'pitchdisc': {'SAME':0,'HIGHER':1,'LOWER':2},
    'timbredisc': {'PURE':0,'DARK':1,'RICH':2,'BRIGHT':3},
    'motiondir': {'STILL':0,'N':1,'NE':2,'E':3,'SE':4,'S':5,'SW':6,'W':7,'NW':8},
}

def load():
    sweep = {}
    for l in open(SWEEP):
        r = json.loads(l); sweep[r['seq']] = r
    seqs = []
    for l in open(CASE):
        r = l.strip().split('|')
        if r[4]=='1' and int(r[5])>=700 and r[2]!='0':
            seqs.append(int(r[0]))
    return sweep, seqs

def vsense_params(task, fixture):
    """Run frozen vsense to get fA/fB (pitchdisc) or f0 (timbredisc)."""
    if task not in ('pitchdisc','timbredisc'):
        return 0, 0
    p = subprocess.run([VSENSE, task, fixture], capture_output=True, text=True, timeout=120)
    out = p.stdout
    if task=='pitchdisc':
        m = re.search(r'fA=(\d+),fB=(\d+)', out)
        return (int(m.group(1)), int(m.group(2))) if m else (0,0)
    else:
        m = re.search(r'f0=(\d+)', out)
        return (int(m.group(1)), 0) if m else (0,0)

def main():
    os.makedirs(OUTDIR, exist_ok=True)
    sweep, seqs = load()
    print(f"278 count: {len(seqs)}", flush=True)
    results = []
    for i, s in enumerate(seqs):
        sw = sweep[s]
        task, fid = sw['task'], sw['fid']
        fixture = os.path.join(FIX, fid)
        if not os.path.exists(fixture):
            results.append((s, task, -1, 'MISSING', -1, -1))
            continue
        jcode = JCODE[task][sw['judgment']]
        conf = sw['conf']
        # trigger: conf>=700 && sweep_prog != PASS
        if not (conf>=700 and sw['prog']!='PASS'):
            results.append((s, task, JCODE[task][sw['truth']], 'NOTRIGGER', -1, -1))
            continue
        fA, fB = vsense_params(task, fixture)
        p = subprocess.run([G5, task, fixture, str(jcode), str(conf), str(fA), str(fB)],
                           capture_output=True, text=True, timeout=120)
        out = p.stdout.strip()
        m = re.match(r'result=(PASS|ABSTAIN)\|label=(-?\d+)\|mval=(-?\d+)', out)
        if m:
            res, lab, mval = m.group(1), int(m.group(2)), int(m.group(3))
        else:
            m2 = re.match(r'result=ABSTAIN\|mval=(-?\d+)', out)
            res, lab, mval = 'ABSTAIN', -1, int(m2.group(1)) if m2 else -1
        truth_jc = JCODE[task][sw['truth']]
        results.append((s, task, truth_jc, res, lab, mval))
        if (i+1)%50==0:
            print(f"  {i+1}/{len(seqs)}", flush=True)
    # write results: seq|task|truth_jc|g5res|g5label|mval
    with open(os.path.join(OUTDIR, 'leg1_results.txt'), 'w') as f:
        for s, task, tjc, res, lab, mval in results:
            f.write(f"{s}|{task}|{tjc}|{res}|{lab}|{mval}\n")
    print(f"wrote {len(results)} results", flush=True)

if __name__=='__main__':
    main()
