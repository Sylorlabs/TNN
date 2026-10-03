#!/usr/bin/env python3
"""Did the P3 baseline discount (need=1) ever decide a kill in the S1 trial?
For each successful KILL_EVIDENCED / OVERWRITE in C-P3 cells, reconstruct
whether the slot carried a live PROTECTION_EXPIRED marker (ck_pexp=1) at
kill time. Also report per-kill citation counts to see if any kill succeeded
with fewer cites than st_n(strength) (the full price)."""
import glob

def load(fn):
    ev=[]
    for line in open(fn):
        if line.startswith('AUD '):
            ev.append([int(x) for x in line.split()[2:]])
    return ev

def st_n(s):
    return 0 if s<=0 else (s+24)//25

for fn in sorted(glob.glob('dump_C-P3_*_S1.txt')):
    ev=load(fn)
    pexp={}      # slot -> bool: live PROTECTION_EXPIRED marker
    cites={}     # slot -> list of cite eps since last strength write (approx via EVIDENCE/STR/WEA aux)
    adm={}; stren={}
    baseline_kills=[]; total_kills=0
    for i,e in enumerate(ev):
        op,sl,aux,aux2,rc=e[0],e[1],e[2],e[3],e[4]
        if rc!=0: continue
        if op==1: pexp[sl]=False; cites[sl]=[]; adm[sl]=aux
        elif op==10: pexp[sl]=False; cites.setdefault(sl,[]).append(aux)
        elif op in (12,13) and aux>=0: pexp[sl]=False; cites.setdefault(sl,[]).append(aux)
        elif op==19: pexp[sl]=True
        elif op in (2,9,15):
            if op in (9,15):
                total_kills+=1
                # strength before = b4&255 ; cites counted
                str_b=e[8]&255
                ncite=len(cites.get(sl,[]))
                if pexp.get(sl,False):
                    baseline_kills.append((i,sl,op,ncite,st_n(str_b),str_b))
            pexp[sl]=False; cites[sl]=[]
    print(f"{fn}: KILL_EVIDENCED/OVERWRITE ok={total_kills}, with live PEXPIRED marker={len(baseline_kills)}")
    for b in baseline_kills:
        print("   baseline kill at idx",b)
