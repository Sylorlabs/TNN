#!/usr/bin/env python3
"""Forensics: where does the C vs C-P3 abandon delta come from (VUP)?
Compares per-slot event timelines and locates the first divergence."""
import sys

OP={1:'ADD',2:'KILL',8:'SETSTAGE',9:'KEV',10:'EV',11:'JUS',12:'STR',13:'WEA',
    14:'TDEC',15:'OW',16:'FPIN',17:'FUNPIN',18:'ABAN',19:'PEXP'}

def load(fn):
    ev=[]
    with open(fn) as f:
        for line in f:
            if line.startswith('AUD '):
                p=[int(x) for x in line.split()[2:]]
                ev.append(p)
    return ev

def timelines(ev):
    t={}
    for i,e in enumerate(ev):
        t.setdefault(e[1],[]).append((i,e[0],e[2],e[4]))
    return t

c=load('dump_C_VUP_0_S1.txt')
p=load('dump_C-P3_VUP_0_S1.txt')
tc=timelines(c); tp=timelines(p)

print("slots:",sorted(set(tc)|set(tp)))
print()
# abandon counts per slot
print("slot: C_abandons C-P3_abandons")
tot_c=tot_p=0
for sl in sorted(set(tc)|set(tp)):
    ac=sum(1 for _,op,_,_ in tc.get(sl,[]) if op==18)
    ap=sum(1 for _,op,_,_ in tp.get(sl,[]) if op==18)
    tot_c+=ac; tot_p+=ap
    flag='' if ac==ap else '   <-- DIFF'
    print(f"  slot {sl}: {ac} {ap}{flag}")
print(f"total: {tot_c} {tot_p}  delta={tot_p-tot_c}")
print()
# for slots with diff, show first divergence in event sequence
for sl in sorted(set(tc)|set(tp)):
    sc=[(op,aux) for _,op,aux,_ in tc.get(sl,[])]
    sp=[(op,aux) for _,op,aux,_ in tp.get(sl,[])]
    if sc==sp: continue
    print(f"=== slot {sl}: first divergence ===")
    n=min(len(sc),len(sp))
    j=0
    while j<n and sc[j]==sp[j]: j+=1
    print(f"  common prefix len {j} of C:{len(sc)} P3:{len(sp)}")
    print(f"  C  next 5: {[(OP.get(o,o),a) for o,a in sc[j:j+5]]}")
    print(f"  P3 next 5: {[(OP.get(o,o),a) for o,a in sp[j:j+5]]}")
    # show pexpired/str events in P3 timeline
    special=[(OP.get(o,o),a) for _,o,a,_ in tp.get(sl,[]) if o in (12,19)]
    print(f"  P3 STR/PEXP events: {special[:12]}")
    print()
