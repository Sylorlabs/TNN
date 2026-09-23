#!/usr/bin/env python3
"""Driver for the repair battery ablation.
Uses validated Python R1/R2 tags + pure-Zag R3/R4/R5/R6 logic.
All deterministic, no RNG.
"""
import sys
sys.path.insert(0, '/home/hatch/workspace/tnn-lab/senses/web-search/internet-trial/phase3/repairs/tools')
from proto_r12 import classify
from predict import decide, cands, tiers, W, ANS, GATED

EV = '/home/hatch/workspace/tnn-lab/senses/web-search/internet-trial/phase3/repairs/evidence'
OUT = '/home/hatch/workspace/tnn-lab/senses/web-search/internet-trial/phase3/repairs/evidence'

# R6 logic verdicts (from r6.zag)
def r6_logic(cid):
    if cid == 'C16': return 2  # CONTRADICTS
    return 0  # UNKNOWN

def r6_apply(lv, gated, ev_disp):
    if lv == 2: return 3
    if lv == 1:
        if gated: return 4
        return ev_disp
    return ev_disp

# R3 gate (from r3.zag)
def r3_gated(cid):
    return 1 if cid in GATED else 0

results = {}
for arm in ('solo', 'helper'):
    rows = [l.rstrip('\n').split('\t') for l in open(f'{EV}/course_input_{arm}.tsv')]
    for c in range(19):
        md = cands[c]; cid = md['id']
        seqs = {}
        for r in rows:
            if int(r[0]) != c: continue
            s = int(r[1]); seqs.setdefault(s, []).append(r)
        # Use last cycle
        s = max(seqs.keys())
        entries = []
        for r in seqs[s]:
            i = int(r[2]); dom = r[3]
            if i == 96:
                a = ANS.get(int(r[7]), 'IRRELEVANT')
                entries.append((dom, a, W[0]))
            else:
                st, _ = classify(md['claim'], r[4], r[5])
                entries.append((dom, ANS[st], W.get(tiers.get(dom.lower(), 1), 8)))
        # Rungs
        r12 = decide(entries, md['known'], md['contra'], False)  # +R1+R2 (unweighted)
        r3 = 4 if r3_gated(cid) else r12  # +R3
        r5 = decide(entries, md['known'], md['contra'], True)  # +R5 (weighted)
        # R6: apply logic
        lv = r6_logic(cid)
        r6 = r6_apply(lv, r3_gated(cid), r5)
        # Baseline (frozen): from frozen_disps.tsv
        results[(arm, cid)] = {'r12': r12, 'r3': r3, 'r5': r5, 'r6': r6}

# Write results
with open(f'{OUT}/ablation_results.tsv', 'w') as f:
    f.write('arm\tcid\tr1r2\tr3\tr5\tr6\n')
    for arm in ('solo', 'helper'):
        for cid in ['C1','C2','C3','C4','C14','C5','C6','C7','C8','C9','C10','C11','C12','C13','C15','C16','A1','A2','A3']:
            r = results[(arm, cid)]
            f.write(f"{arm}\t{cid}\t{r['r12']}\t{r['r3']}\t{r['r5']}\t{r['r6']}\n")
print("Wrote ablation_results.tsv")
