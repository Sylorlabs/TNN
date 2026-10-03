#!/usr/bin/env python3
"""F21 kill-bar table from frozen TSVs. Mech 21 A-legs in results_full."""
import os, glob
from collections import defaultdict

RD='/home/hatch/workspace/tnn-lab/deliberation_depth/monotonicity/training/results_full'
BATT={'admit':[1,2,4,8,16],'revoke':[1,2,4,8,16],'logic':[1,2,4,8,16],
      'trap':[1,2,4,8,16],'cost':[1,2,4,8,16],'redteam':[1,2,4,8,16],
      'ceiling':[1,2,4,8,16,32,64]}
def fam_of(b,iid):
    if b=='ceiling':
        p=iid.split('-')
        if len(p)>=2 and p[0]=='H5B': return p[1]
        return 'ceiling?'
    return b
# data[fam][iid][d] = (correct, conf, released_bool)
data=defaultdict(lambda: defaultdict(dict))
for b,ds in BATT.items():
    for d in ds:
        for fn in glob.glob(os.path.join(RD,f'{b}_m21_d{d}_A.tsv')):
            for line in open(fn):
                line=line.rstrip('\n')
                if not line: continue
                c=line.split('\t')
                iid,d2,rel,corr,conf=c[0],int(c[1]),c[6],c[7],int(c[8])
                fam=fam_of(b,iid)
                data[fam][iid][d2]=(corr,conf,not rel.startswith('ABSTAIN'))
# M4 release counts per (fam,depth) for B8 denominator
m4rel=defaultdict(lambda: defaultdict(int))
for b,ds in BATT.items():
    for d in ds:
        for fn in glob.glob(os.path.join(RD,f'{b}_m4_d{d}_A.tsv')):
            for line in open(fn):
                line=line.rstrip('\n')
                if not line: continue
                c=line.split('\t')
                if not c[6].startswith('ABSTAIN'):
                    m4rel[fam_of(b,c[0])][int(c[1])]+=1

def G_of(cells):
    rel=[(co,cf) for co,cf in cells if co in ('1','0')]
    if not rel: return None,0
    mc=sum(cf for _,cf in rel)/len(rel)/1000.0
    acc=sum(1 for co,_ in rel if co=='1')/len(rel)
    return mc-acc,len(rel)

print('=== per-family G curves (mech 21) ===')
gviol_fam={}; b13_bad=[]; b12_cross=0
for fam in sorted(data):
    ds=sorted({d for iid in data[fam] for d in data[fam][iid]})
    gs={}; ns={}
    for d in ds:
        cells=[(data[fam][iid][d][0],data[fam][iid][d][1]) for iid in data[fam] if d in data[fam][iid]]
        g,n=G_of(cells); gs[d]=g; ns[d]=n
    gv=sum(1 for i in range(len(ds)-1)
           if gs[ds[i]] is not None and gs[ds[i+1]] is not None
           and gs[ds[i+1]]>gs[ds[i]]+1e-12)
    gviol_fam[fam]=gv
    for d in ds:
        if ns[d]>=8 and gs[d] is not None and gs[d]<-0.100:
            b13_bad.append((fam,d,round(gs[d],4),ns[d]))
        if gs[d] is not None and gs[d]>0: b12_cross+=1
    print(f'{fam}: '+' '.join(f'{d}:{gs[d]:+.3f}/{ns[d]}' if gs[d] is not None else f'{d}:n/a/{ns[d]}' for d in ds)+f'  Gviol={gv}')

# B1/B2 totals, B3pi, B4/B5, B7
n10=V1=V2=0; b3pi=0; b3pi_n=0
sc=scc=sw=swc=0; abst=tot=0
for fam in data:
    for iid,dd in data[fam].items():
        sq=sorted(dd.items())
        for i in range(len(sq)-1):
            d0,(c0,f0,r0)=sq[i]; d1,(c1,f1,r1)=sq[i+1]
            if c0=='1' and c1=='0': n10+=1
            if c0=='1' and c1=='0' and f1>=f0: V1+=1
            if c0=='0' and c1=='0' and f1>f0: V2+=1
            if r0 and r1 and c0 in ('1','0') and c1 in ('1','0'):
                g0=f0/1000.0-(1 if c0=='1' else 0)
                g1=f1/1000.0-(1 if c1=='1' else 0)
                b3pi_n+=1
                if g1>g0+1e-12: b3pi+=1
        for d,(c,f,r) in dd.items():
            tot+=1
            if not r: abst+=1
            else:
                if c=='1': sc+=f; scc+=1
                elif c=='0': sw+=f; swc+=1
B4=sc/scc/1000 if scc else 0
B5=(sc/scc-sw/swc)/1000 if scc and swc else 0
B7=abst/tot
print(f'\nB1 n10={n10} | B2 V1={V1} V2={V2} | B3pi={b3pi}/{b3pi_n} ({100*b3pi/max(b3pi_n,1):.1f}%)')
print(f'B4 meanConfCorrect={B4:.4f} (n={scc}) | B5 separation={B5:.4f} | B7 abstention={B7:.4f} ({abst}/{tot})')
print(f'B12 G>0 crossings (family-depth cells): {b12_cross}')
# B4b per honest family
print('\nB4b per family (released correct, n>=10):')
for fam in sorted(data):
    cs=[f for iid in data[fam] for d,(c,f,r) in data[fam][iid].items() if r and c=='1']
    if len(cs)>=10:
        print(f'  {fam}: {sum(cs)/len(cs)/1000:.4f} (n={len(cs)})')
    else:
        print(f'  {fam}: n={len(cs)} <10 (exempt)')
# B6: released-correct vs M4 per family
m4corr=defaultdict(int); m21corr=defaultdict(int)
for b,ds in BATT.items():
    for d in ds:
        for fn in glob.glob(os.path.join(RD,f'{b}_m4_d{d}_A.tsv')):
            for line in open(fn):
                c=line.rstrip('\n').split('\t')
                if not c[6].startswith('ABSTAIN') and c[7]=='1':
                    m4corr[fam_of(b,c[0])]+=1
for fam in data:
    for iid in data[fam]:
        for d,(c,f,r) in data[fam][iid].items():
            if r and c=='1': m21corr[fam]+=1
print('\nB6 released-correct vs M4 per family:')
for fam in sorted(set(list(m4corr)+list(m21corr))):
    a=m4corr.get(fam,0); v=m21corr.get(fam,0)
    print(f'  {fam}: {v}/{a} = {v/max(a,1):.4f}')
# B8 amended
print('\nB8 amended per family:')
for fam in sorted(data):
    ds=sorted({d for iid in data[fam] for d in data[fam][iid]})
    feas=[d for d in ds if m4rel[fam].get(d,0)>=10]
    gvals=[]
    for d in feas:
        cells=[(data[fam][iid][d][0],data[fam][iid][d][1]) for iid in data[fam] if d in data[fam][iid]]
        g,n=G_of(cells)
        if g is not None: gvals.append(g)
    five=len(ds)<=5
    need=4 if five else 5
    if len(feas)<need:
        print(f'  {fam}: VOID (M4-feasible slots {len(feas)} < {need})')
        continue
    defined=len(gvals)>=need
    alleq=max(gvals)-min(gvals)<=1e-3 if gvals else True
    perfect=alleq and all(abs(g)<=1e-6 for g in gvals)
    nonvac=(not alleq) or perfect
    print(f'  {fam}: M4-feasible={len(feas)} defined-G={len(gvals)} allEqual1e-3={alleq} perfect={perfect} -> {"PASS" if defined and nonvac else "FAIL"}')
print(f'\nB13 offenders (G<-0.100, n_rel>=8): {len(b13_bad)}')
for fam,d,g,n in b13_bad: print(f'  {fam} d={d}: G={g} n_rel={n}')
# falsification (a): legs with n_rel>=16 at every rung + their Gviol
print('\nFalsification (a) check — legs with n_rel>=16 at EVERY rung:')
for fam in sorted(data):
    ds=sorted({d for iid in data[fam] for d in data[fam][iid]})
    ns={}
    ok=True
    for d in ds:
        cells=[(data[fam][iid][d][0],data[fam][iid][d][1]) for iid in data[fam] if d in data[fam][iid]]
        _,n=G_of(cells); ns[d]=n
        if n<16: ok=False
    print(f'  {fam}: all-rungs>=16: {ok}  rungs={[(d,ns[d]) for d in ds]}  Gviol={gviol_fam[fam]}')
