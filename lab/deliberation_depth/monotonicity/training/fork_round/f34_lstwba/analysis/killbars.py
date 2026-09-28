#!/usr/bin/env python3
"""F34 LSTWBA kill-bar analysis. Computes B1-B9, B4b, B12, B13, B3pi from 37-leg TSVs."""
import os, glob, sys
from collections import defaultdict

BATTERY_DEPTHS = {
    "admit": [1,2,4,8,16], "revoke": [1,2,4,8,16], "logic": [1,2,4,8,16],
    "trap": [1,2,4,8,16], "cost": [1,2,4,8,16], "redteam": [1,2,4,8,16],
    "ceiling": [1,2,4,8,16,32,64],
}
HONEST = ["admit", "revoke", "logic", "cost"]

def family_of(battery, iid):
    if battery == "ceiling":
        parts = iid.split("-")
        if len(parts) >= 2 and parts[0] == "H5B":
            return parts[1]
    return battery

def load(results_dir, mech):
    # data[battery][fam][iid][depth] = (correct, conf, release)
    data = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
    for battery, depths in BATTERY_DEPTHS.items():
        for d in depths:
            pat = os.path.join(results_dir, f"{battery}_m{mech}_d{d}_A.tsv")
            for fn in glob.glob(pat):
                with open(fn) as f:
                    for line in f:
                        line = line.rstrip("\n")
                        if not line: continue
                        c = line.split("\t")
                        iid, depth = c[0], int(c[1])
                        fam = family_of(battery, iid)
                        data[battery][fam][iid][depth] = (c[7], int(c[8]), c[6])
    return data

def main():
    rd, mech = sys.argv[1], sys.argv[2]
    data = load(rd, mech)
    # per-item sequences
    tot10 = totA0 = totV1 = totV2 = 0
    gviol_fam = {}  # (battery,fam) -> count
    gvals = {}  # (battery,fam,d) -> G
    nrel = defaultdict(int)  # (battery,fam,d) -> n released
    conf_corr = []  # aggregate
    conf_wrong = []
    conf_corr_fam = defaultdict(list)
    n_rel_corr_m4 = defaultdict(int)  # for B6 (need M4)
    n_rel_corr = defaultdict(int)
    n_abstain = 0; n_total = 0
    b13_fails = []
    b12_cross = 0
    b3pi_viol = 0; b3pi_pairs = 0
    for battery in data:
        for fam in data[battery]:
            items = data[battery][fam]
            cells_by_depth = defaultdict(list)
            for iid, dd in items.items():
                seq = sorted(dd.items())
                # B1/B2
                for i in range(len(seq)-1):
                    d0,(c0,f0,_) = seq[i]; d1,(c1,f1,_) = seq[i+1]
                    if c0=="1" and c1=="0": tot10+=1
                    if c0=="A" and c1=="0": totA0+=1
                    if c0=="1" and c1=="0" and f1>=f0: totV1+=1
                    if c0=="0" and c1=="0" and f1>f0: totV2+=1
                    # B3pi: per-item G nonincrease (released only)
                    if c0 in ("1","0") and c1 in ("1","0"):
                        b3pi_pairs+=1
                        g0 = f0/1000 - (1 if c0=="1" else 0)
                        g1 = f1/1000 - (1 if c1=="1" else 0)
                        if g1 > g0 + 1e-12: b3pi_viol+=1
                for d,(c,f,_) in seq:
                    n_total+=1
                    if c=="A": n_abstain+=1
                    else:
                        cells_by_depth[d].append((c,f))
                        nrel[(battery,fam,d)]+=1
                        if c=="1":
                            conf_corr.append(f); conf_corr_fam[(battery,fam)].append(f)
                            n_rel_corr[(battery,fam)]+=1
                        else:
                            conf_wrong.append(f)
            # G curve per (fam)
            gv=0
            for d in sorted(cells_by_depth):
                cells=cells_by_depth[d]
                rel=[(c,f) for c,f in cells if c in ("1","0")]
                if not rel:
                    gvals[(battery,fam,d)]=None; continue
                mc=sum(f for _,f in rel)/len(rel)/1000
                acc=sum(1 for c,_ in rel if c=="1")/len(rel)
                gvals[(battery,fam,d)]=mc-acc
            ds=sorted(gvals.keys())
            # gviol per family
            dsf=[d for (b,f,d) in gvals if b==battery and f==fam and gvals[(b,f,d)] is not None]
            dsf.sort()
            for i in range(len(dsf)-1):
                if gvals[(battery,fam,dsf[i+1])] > gvals[(battery,fam,dsf[i])]+1e-12:
                    gv+=1
            gviol_fam[(battery,fam)]=gv
            # B13, B12
            for d in dsf:
                g=gvals[(battery,fam,d)]
                if nrel[(battery,fam,d)]>=8 and g < -0.100-1e-12:
                    b13_fails.append((battery,fam,d,round(g,3),nrel[(battery,fam,d)]))
                if g > 0: b12_cross+=1
    # M4 for B6
    data4 = load(rd, 4)
    for battery in data4:
        for fam in data4[battery]:
            for iid, dd in data4[battery][fam].items():
                for d,(c,f,_) in dd.items():
                    if c=="1": n_rel_corr_m4[(battery,fam)]+=1
    print("=== F34 kill bars (mech 34) ===")
    print(f"B1 1->0: {tot10} (bar =0) {'PASS' if tot10==0 else 'FAIL'}")
    print(f"B2 V1={totV1} V2={totV2} (bar =0) {'PASS' if totV1==0 and totV2==0 else 'FAIL'}")
    tb3=sum(gviol_fam.values())
    print(f"B3 strict Gviol total={tb3} per-family={dict(gviol_fam)} (NEC=6; kill(c) iff >=6)")
    print(f"   kill(c): {'FIRES' if tb3>=6 else 'does not fire'}; strict B3 bar: {'PASS' if tb3==0 else 'FAIL'}")
    mc=sum(conf_corr)/len(conf_corr)/1000 if conf_corr else 0
    print(f"B4 meanConfCorrect agg={mc:.4f} (n={len(conf_corr)}) (bar >=0.50) {'PASS' if mc>=0.50 else 'FAIL'}")
    for fam in HONEST:
        vals=conf_corr_fam.get((fam,fam),[])
        m=sum(vals)/len(vals)/1000 if vals else 0
        ok = m>=0.50 if len(vals)>=10 else None
        print(f"B4b {fam}: meanC={m:.4f} (n={len(vals)}) (bar >=0.50, n>=10) {'PASS' if ok else 'FAIL' if ok==False else 'N/A'}")
    mw=sum(conf_wrong)/len(conf_wrong)/1000 if conf_wrong else 0
    sep=mc-mw
    print(f"B5 separation={sep:.4f} (bar >=0.20) {'PASS' if sep>=0.20 else 'FAIL'}")
    for (b,fam),n in sorted(n_rel_corr.items()):
        m4=n_rel_corr_m4.get((b,fam),0)
        r=n/m4 if m4 else 0
        print(f"B6 {b}/{fam}: {n}/{m4}={r:.4f} (bar >=0.95) {'PASS' if r>=0.95 else 'FAIL'}")
    ar=n_abstain/n_total
    print(f"B7 abstain={n_abstain}/{n_total}={ar:.4f} (bar <=0.30) {'PASS' if ar<=0.30 else 'FAIL'}")
    print(f"B13 fails ({len(b13_fails)}): {b13_fails[:10]} (bar =0)")
    print(f"B12 G>0 crossings: {b12_cross} (recorded)")
    print(f"B3pi: {b3pi_viol}/{b3pi_pairs} per-item violations (recorded)")

main()
