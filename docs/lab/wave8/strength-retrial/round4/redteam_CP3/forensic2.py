#!/usr/bin/env python3
"""Abandon counts per episode for C vs C-P3 (VUP v0), anchored on ADD aux."""
def load(fn):
    ev=[]
    with open(fn) as f:
        for line in f:
            if line.startswith('AUD '):
                ev.append([int(x) for x in line.split()[2:]])
    return ev

def per_episode(ev):
    cur_ep=-1; counts={}
    for e in ev:
        op,sl,aux=e[0],e[1],e[2]
        if op==1 and aux>=0:  # ADD: aux = candidate episode
            cur_ep=aux
        if op==18:  # ABANDON
            counts[cur_ep]=counts.get(cur_ep,0)+1
    return counts

c=per_episode(load('dump_C_VUP_0_S1.txt'))
p=per_episode(load('dump_C-P3_VUP_0_S1.txt'))
alleps=sorted(set(c)|set(p))
print("ep: C_abandons P3_abandons (pressure eps marked *)")
tot=0
for ep in alleps:
    ac=c.get(ep,0); ap=p.get(ep,0)
    mark=' *' if ep>0 and ep%100==0 else ''
    flag='  <-- DIFF' if ac!=ap else ''
    tot+=ap-ac
    if ac!=ap or (ep>0 and ep%100==0):
        print(f"  ep {ep}: {ac} {ap}{mark}{flag}")
print("net delta:",tot)
