#!/usr/bin/env python3
"""F33 falsifiers (a) non-stationarity and (b) cross-family pooling.

(a) Recompute delta_d per (key, d_idx) from EVAL stay/drop moments with the
    EXACT integer rules of train_f33.zag, compare to the applied (training)
    delta. Adjudicated only at depths with >=200 pooled released transitions.
    Mismatch iff |applied - recomp_uncapped| > 42 (truncation slack 2 + cap 40).
    KILL iff mismatches on >1/4 of adjudicated key-depth cells.
(b) Per family F and (key, d_idx) with nstay>=8, nall>=8 in both the
    family-restricted and pooled eval moments: flip iff sign(E_F) strictly
    opposes sign(E_pooled) (zeros neutral). A depth counts for F if >=1 key
    flips. KILL iff any family flips on >=3 depths.

Inputs: results dir (eval _A TSVs), state file (id -> m,s,cstar,f8_1),
        params (applied delta table).
"""
import csv, glob, os, sys
from collections import defaultdict

BATTERY_DEPTHS = {"admit":[1,2,4,8,16],"revoke":[1,2,4,8,16],"logic":[1,2,4,8,16],
                  "trap":[1,2,4,8,16],"cost":[1,2,4,8,16],"redteam":[1,2,4,8,16],
                  "ceiling":[1,2,4,8,16,32,64]}
def dslot(d): return {1:0,2:1,4:2,8:3,16:4,32:5,64:6}[d]
def tdiv(a,b):
    assert b>0
    return a//b if a>=0 else -((-a)//b)
def newdelta(nstay,sstay,nall,sall,kstay,kall):
    if nstay==0 or nall==0: return None
    e=tdiv(sstay,nstay)-tdiv(sall,nall)
    da=tdiv(kstay*1000,nstay)-tdiv(kall*1000,nall)
    return da-e-3
def family_of(battery,iid):
    if battery=="ceiling":
        p=iid.split("-")
        if len(p)>=2 and p[0]=="H5B": return p[1]
        return "ceiling?"
    return battery

def load_state(path):
    st={}
    with open(path) as f:
        for row in csv.reader(f,delimiter='\t'):
            if len(row)>=5: st[row[0]]=(int(row[1]),int(row[2]),int(row[3]),int(row[4]))
    return st  # id -> (m,s,cstar,f8_1)

def load_params(path):
    # parse generated mt_f33_params.zag: f33_delta key/di table
    import re
    txt=open(path).read()
    delta={}
    for m in re.finditer(r"if\(key==(\d+)\)\{\s*((?:if\(di==\d+\)\{return -?\d+;\}\s*)+)\}",txt):
        key=int(m.group(1))
        for d,v in re.findall(r"if\(di==(\d+)\)\{return (-?\d+);\}",m.group(2)):
            delta[(key,int(d))]=int(v)
    cstar={}
    for k,v in re.findall(r"if\(key==(\d+)\)\{return (\d+);\}",txt.split("fn f33_delta")[0]):
        cstar[int(k)]=int(v)
    return delta,cstar

def eval_moments(resdir,mech,state):
    """moments[(key,ds)] = [nstay,sstay,nall,sall,kstay,kall];
       fammoments[fam][(key,ds)] = same. Only items with a known key."""
    moments=defaultdict(lambda:[0]*6)
    famm=defaultdict(lambda:defaultdict(lambda:[0]*6))
    ntrans=defaultdict(int)  # ds -> pooled released transitions
    missing=0
    for battery,depths in BATTERY_DEPTHS.items():
        cells=defaultdict(dict)
        for d in depths:
            for fn in glob.glob(os.path.join(resdir,f"{battery}_m{mech}_d{d}_A.tsv")):
                with open(fn) as f:
                    for line in f:
                        c=line.rstrip("\n").split("\t")
                        if len(c)<9: continue
                        iid,dep,corr,conf=c[0],int(c[1]),c[7],int(c[8])
                        cells[iid][dep]=(corr,conf)
        for iid,dd in cells.items():
            if iid not in state: missing+=1; continue
            m,s,_,_=state[iid]; key=m*4+s
            fam=family_of(battery,iid)
            for d in depths:
                ds=dslot(d); dp=d//2
                if ds==0 or dp not in dd or d not in dd: continue
                corr_p,conf_p=dd[dp]
                corr_d,_=dd[d]
                rel_p=corr_p in ("1","0"); rel_d=corr_d in ("1","0")
                if not rel_p: continue
                y_p=1 if corr_p=="1" else 0
                M=moments[(key,ds)]; F=famm[fam][(key,ds)]
                for T in (M,F):
                    T[2]+=1; T[3]+=conf_p; T[5]+=y_p
                    if rel_d: T[0]+=1; T[1]+=conf_p; T[4]+=y_p
                ntrans[ds]+=1
    return moments,famm,ntrans,missing

def falsifier_a(moments,ntrans,applied):
    rows=[]; mism=0; adj=0
    for ds in range(1,7):
        if ntrans[ds]<200: continue
        for key in range(20):
            M=moments[(key,ds)]
            r=newdelta(*M)
            if r is None: continue
            a=applied.get((key,ds),0)
            bad=abs(a-r)>42
            adj+=1; mism+=1 if bad else 0
            rows.append((ds,key,a,r,bad,M[0],M[2]))
    frac=mism/adj if adj else 0.0
    return dict(rows=rows,mism=mism,adj=adj,frac=frac,kill=frac>0.25)

def falsifier_b(moments,famm):
    # per family: depths with >=1 flipping key
    fam_depths=defaultdict(set); table=[]
    for fam,F in famm.items():
        for (key,ds),FM in F.items():
            M=moments[(key,ds)]
            if min(FM[0],FM[2],M[0],M[2])<8: continue
            e_f=tdiv(FM[1],FM[0])-tdiv(FM[3],FM[2])
            e_p=tdiv(M[1],M[0])-tdiv(M[3],M[2])
            flip=(e_f>0 and e_p<0) or (e_f<0 and e_p>0)
            if flip:
                fam_depths[fam].add(ds)
                table.append((fam,ds,key,e_f,e_p,FM[0],FM[2],M[0],M[2]))
    worst=max([len(v) for v in fam_depths.values()]+[0])
    killfams={f:sorted(v) for f,v in fam_depths.items() if len(v)>=3}
    return dict(table=table,fam_depths={f:sorted(v) for f,v in fam_depths.items()},
                worst=worst,kill=bool(killfams),killfams=killfams)

def main():
    resdir,mech,state_path,params_path=sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]
    state=load_state(state_path); applied,_=load_params(params_path)
    moments,famm,ntrans,missing=eval_moments(resdir,mech,state)
    print(f"state rows={len(state)} missing-key items={missing}")
    print("pooled released transitions per d_idx:",dict(sorted(ntrans.items())))
    A=falsifier_a(moments,ntrans,applied)
    print(f"FALSIFIER (a): adjudicated cells={A['adj']} mismatches={A['mism']} frac={A['frac']:.3f} -> {'KILL' if A['kill'] else 'clear'}")
    for ds,key,a,r,bad,ns,na in A['rows']:
        if bad: print(f"  MISMATCH d_idx={ds} key={key}: applied={a} recomp={r} nstay={ns} nall={na}")
    B=falsifier_b(moments,famm)
    print(f"FALSIFIER (b): worst family flips on {B['worst']} depths -> {'KILL '+str(B['killfams']) if B['kill'] else 'clear'}")
    for fam,ds,key,ef,ep,ns_f,na_f,ns_p,na_p in B['table']:
        print(f"  flip fam={fam} d_idx={ds} key={key}: E_fam={ef:+d} E_pool={ep:+d} (n {ns_f}/{na_f} vs {ns_p}/{na_p})")
    print("per-family flip depths:",B['fam_depths'])

if __name__=='__main__': main()
