#!/usr/bin/env python3
"""G5 battery Leg 2: mint on the sealed 288. Glue only: runs the pure-Zag
g5sense binary on each sealed trial where triggered and records output."""
import os, re, subprocess

LAB = os.path.expanduser("~/workspace/tnn-lab")
G5 = os.path.join(LAB, "senses/pam-rebuild/v2/g5_sense/src/g5sense")
VSENSE = os.path.join(LAB, "senses/pam-rebuild/v2/g5_sense/work/vsense_test_bin")
RT4 = os.path.join(LAB, "senses/pam-rebuild/v2/g5_sense/rtbuild/rt4")
REC = os.path.join(LAB, "senses/pam-rebuild/v2/redteam/evidence/rec_clean.records")
OUTDIR = os.path.join(LAB, "senses/pam-rebuild/v2/g5_sense/evidence")

TASKS = ['colordisc','colorconst','shapetrans','pitchdisc','timbredisc','motiondir']
JCODE = {
    'colordisc': {'SAME':0,'DIFFERENT':1},
    'colorconst': {'SAME_SURFACE':0,'DIFFERENT':1},
    'shapetrans': {'SQUARE':0,'TRIANGLE':1,'CIRCLE':2},
    'pitchdisc': {'SAME':0,'HIGHER':1,'LOWER':2},
    'timbredisc': {'PURE':0,'DARK':1,'RICH':2,'BRIGHT':3},
    'motiondir': {'STILL':0,'N':1,'NE':2,'E':3,'SE':4,'S':5,'SW':6,'W':7,'NW':8},
}

def vsense_params(task, fixture):
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
    rows = [l.strip().split('|') for l in open(REC)]
    print(f"sealed records: {len(rows)}", flush=True)
    results = []
    for r in rows:
        seq, tcode, fixture, prog, jcode, judgment, conf = r[0], int(r[1]), r[2], r[3], int(r[4]), r[5], int(r[6])
        truth = r[10]
        task = TASKS[tcode]
        fpath = os.path.join(RT4, fixture)
        # trigger: conf>=700 && prog != PASS (prog: 0=PASS)
        if not (conf>=700 and prog!='0'):
            results.append((seq, task, 'NOTRIGGER', -1, -1, truth, judgment))
            continue
        fA, fB = vsense_params(task, fpath)
        p = subprocess.run([G5, task, fpath, str(jcode), str(conf), str(fA), str(fB)],
                           capture_output=True, text=True, timeout=120)
        out = p.stdout.strip()
        m = re.match(r'result=(PASS|ABSTAIN)\|label=(-?\d+)\|mval=(-?\d+)', out)
        if m:
            res, lab, mval = m.group(1), int(m.group(2)), int(m.group(3))
        else:
            m2 = re.match(r'result=ABSTAIN\|mval=(-?\d+)', out)
            res, lab, mval = 'ABSTAIN', -1, int(m2.group(1)) if m2 else -1
        # g5 false-PASS: emitted PASS with label != truth
        truth_jc = JCODE[task][truth]
        results.append((seq, task, res, lab, mval, truth, judgment, truth_jc))
    with open(os.path.join(OUTDIR, 'leg2_results.txt'), 'w') as f:
        for row in results:
            f.write('|'.join(str(x) for x in row) + '\n')
    # count G5's new false-PASSes
    g_new = sum(1 for r in results if r[2]=='PASS' and r[3]!=r[7])
    print(f"G5 new false-PASSes: {g_new}/288", flush=True)
    print(f"system rate: {(67+g_new)}/288 = {(67+g_new)/288:.4f}", flush=True)

if __name__=='__main__':
    main()
