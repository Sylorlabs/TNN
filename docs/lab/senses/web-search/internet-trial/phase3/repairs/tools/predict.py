#!/usr/bin/env python3
"""Predict ladder dispositions using the validated prototype classifier.
Mirrors ws_decide/ht2_end semantics (unweighted for rungs 1-4, weighted for rung 5)."""
import sys
sys.path.insert(0, '/home/hatch/workspace/tnn-lab/senses/web-search/internet-trial/phase3/repairs/tools')
from proto_r12 import classify

EV = '/home/hatch/workspace/tnn-lab/senses/web-search/internet-trial/phase3/repairs/evidence'
CAND_IDS = ["C1","C2","C3","C4","C14","C5","C6","C7","C8","C9","C10","C11","C12","C13","C15","C16","A1","A2","A3"]
GATED = {"C5","C6","C8","C11","C12","C13"}

cands = {}
for l in open(EV+'/candidates.tsv'):
    p = l.rstrip('\n').split('\t')
    cands[int(p[0])] = dict(id=p[1], claim=p[2], known=int(p[3]), contra=p[6], oracle=p[7])
tiers = {}
for l in open(EV+'/tier_map.tsv'):
    p = l.rstrip('\n').split('\t'); tiers[p[0]] = int(p[1])
W = {3:32, 2:16, 1:8, 0:4, -1:1}

def decide(entries, known, contra, weighted):
    """entries: list of (domain, answer, weight). Returns trial disposition 2/3/4/5."""
    # dedup (domain, answer) keep first; cap 6
    seen = set(); ded = []
    for d, a, w in entries:
        if (d, a) not in seen:
            seen.add((d, a)); ded.append((d, a, w))
    ded = ded[:6]
    if known:
        if weighted:
            bad = sum(w for _, a, w in ded if a != 'AFFIRM')
            if bad == 0: return 2
            cw = sum(w for _, a, w in ded if a == contra)
            return 5 if (contra and cw >= 8) else 4
        else:
            bad = sum(1 for _, a, _ in ded if a != 'AFFIRM')
            if bad == 0: return 2
            ncontra = sum(1 for d, a, _ in ded if a == contra)
            doms = set(d for d, a, _ in ded if a == contra)
            if contra and ncontra >= 2 and len(doms) >= 2: return 5
            return 4
    # unweighted count
    cnt = {}
    for _, a, _ in ded: cnt[a] = cnt.get(a, 0) + 1
    wcnt = {}
    for _, a, w in ded: wcnt[a] = wcnt.get(a, 0) + w
    if weighted:
        # winner = max weight, strict >, first appearance wins ties
        best = None; bestw = -1
        for _, a, w in ded:
            if wcnt[a] > bestw: bestw = wcnt[a]; best = a
        if bestw >= 8:
            return 2 if best == 'AFFIRM' else (3 if best == 'DENY' else 4)
        return 4
    else:
        top = None; topc = 0
        for _, a, _ in ded:
            if cnt[a] > topc: topc = cnt[a]; top = a
        if topc >= 2:
            return 2 if top == 'AFFIRM' else (3 if top == 'DENY' else 4)
        return 4

ANS = {0:'IRRELEVANT', 1:'AFFIRM', 2:'DENY'}
for arm in ('solo', 'helper'):
    rows = [l.rstrip('\n').split('\t') for l in open(f'{EV}/course_input_{arm}.tsv')]
    print(f'=== {arm} ===')
    for c in range(19):
        md = cands[c]
        # group rows by env_seq
        seqs = {}
        for r in rows:
            if int(r[0]) != c: continue
            s = int(r[1]); seqs.setdefault(s, []).append(r)
        # final disposition = last cycle's decide (ht2_end per cycle; SENSE_DECIDED per cycle, last wins)
        last_disp = None
        for s in sorted(seqs):
            entries = []
            for r in seqs[s]:
                i = int(r[2]); dom = r[3]
                if i == 96:
                    hs = int(r[7]); a = ANS.get(hs, 'IRRELEVANT')
                    entries.append(('helper', a, W[0]))
                else:
                    st, _ = classify(md['claim'], r[4], r[5])
                    entries.append((dom, ANS[st], W.get(tiers.get(dom.lower(), 1), 8)))
            last_disp = (decide(entries, md['known'], md['contra'], False),
                         decide(entries, md['known'], md['contra'], True))
        d_u, d_w = last_disp
        flag = '' if str(d_u) == str({'INSTALL':2,'REJECT':3,'WITHHOLD':4,'REVISE':5}[md['oracle']]) else '   <-- vs oracle '+md['oracle']
        print(f"{md['id']:4s} unweighted={d_u} weighted={d_w}{flag}")
