#!/usr/bin/env python3
"""Extract G spans for V2-D replay. Writes gspan_<seq>.bin for dual-span
trials with F conf>=700."""
import json, os, struct

LAB = os.path.expanduser("~/workspace/tnn-lab")
FIX = os.path.join(LAB, "senses/pam-rebuild/round2/forks/R2-4/fixtures")
SWEEP = os.path.join(LAB, "senses/pam-rebuild/round2/forks/R2-4/evidence/clean/sweep.jsonl")
OUT = os.path.join(LAB, "senses/pam-rebuild/v2/g5_sense/work/gspans")
os.makedirs(OUT, exist_ok=True)

def r24_flen(d, tcode):
    if tcode in (0,1,2):
        w,h = struct.unpack('<II', d[8:16])
        return 8 + w*h*3
    elif tcode in (3,4):
        cnt = struct.unpack('<I', d[12:16])[0]
        return 8 + cnt*2
    elif tcode==5:
        nf,w,h = struct.unpack('<III', d[8:20])
        return 12 + nf*w*h*3
    return -1

TCODES = {'colordisc':0,'colorconst':1,'shapetrans':2,'pitchdisc':3,'timbredisc':4,'motiondir':5}

sweep = {}
for l in open(SWEEP):
    r = json.loads(l); sweep[r['seq']] = r

n=0
for s,r in sweep.items():
    if not (r['conf']>=700 and r['t1']==1):
        continue
    p = os.path.join(FIX, r['fid'])
    d = open(p,'rb').read()
    magic, tc = struct.unpack('<II', d[:8])
    assert magic==1093939794 and tc==TCODES[r['task']], (s, r['fid'])
    flen = r24_flen(d, tc)
    g = d[8+flen:]
    open(os.path.join(OUT, f'gspan_{s}.bin'),'wb').write(g)
    # write task for the runner
    open(os.path.join(OUT, f'gspan_{s}.task'),'w').write(r['task'])
    n+=1
print(f"extracted {n} G spans")
