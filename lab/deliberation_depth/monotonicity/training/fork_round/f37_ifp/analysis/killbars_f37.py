#!/usr/bin/env python3
"""Kill-bar table for F37 IFP (PREREG_FORKROUND.md §4, B8 amended §4b).

Reads results/<battery>_m37_d<depth>_A.tsv (F37 legs) and *_m4_d*_[AB].tsv
(M4 reference). NEC m9 legs (optional 2nd arg) for delta-vs-NEC reporting.

Bars:
  B1  1->0 transitions = 0
  B2  V1 = 0 and V2 = 0
  B3  strict: G-violations per family = 0 every family
  B4  meanConfCorrect (aggregate) >= 0.50
  B4b honest-family floor: mean C on released correct, per honest family
      (n_rel_correct >= 10) >= 0.50
  B5  separation: meanConfCorrect - meanConfWrong >= 0.20
  B6  recall: released-correct / M4 released-correct, per family >= 0.95
  B7  abstention volume: abstained / total cells (aggregate) <= 0.30
  B8  AMENDED §4b: definedness (denominator = depth slots where M4 releases
      >=10; pass iff G defined on >=4 such slots (5-depth fams) / >=5
      (ceiling); fewer feasible slots -> VOID) + nonvacuity (defined G not
      all equal within 1e-3, except all-equal with |G|<=1e-6 passes)
  B9  release+correct identity vs M4 = 100%
  B12 recorded: G>0 crossings per family
  B13 per (F,d), n_rel >= 8: G(F,d) >= -0.100
  B3pi recorded: per-item (conf/1000 - acc) rises across adjacent depths
      (released cells only)

F37 fixed-point checks (from training log, 4th arg):
  FP1 contraction: max|w| after t=10000 bounded (not growing linearly)
  FP2 edge mass at fixed point (t>10000): 0% in [1,20]U[980,999]
"""
import sys, os, glob, math
from collections import defaultdict

BATTERY_DEPTHS = {"admit":[1,2,4,8,16],"revoke":[1,2,4,8,16],"logic":[1,2,4,8,16],
                  "trap":[1,2,4,8,16],"cost":[1,2,4,8,16],"redteam":[1,2,4,8,16],
                  "ceiling":[1,2,4,8,16,32,64]}
HONEST = {"admit","revoke","logic","cost"}

def family_of(battery, iid):
    if battery == "ceiling":
        parts = iid.split("-")
        if len(parts) >= 2 and parts[0] == "H5B":
            return parts[1]
        return "ceiling?"
    return battery

def load_mech(resdir, mtag):
    data = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
    for battery, depths in BATTERY_DEPTHS.items():
        for d in depths:
            pat = os.path.join(resdir, f"{battery}_m{mtag}_d{d}_A.tsv")
            for fn in glob.glob(pat):
                with open(fn) as f:
                    for line in f:
                        line = line.rstrip("\n")
                        if not line: continue
                        c = line.split("\t")
                        iid, depth = c[0], int(c[1])
                        rel, corr, conf = c[6], c[7], int(c[8])
                        fam = family_of(battery, iid)
                        data[battery][fam][iid][depth] = (corr, conf, rel)
    return data

def main():
    resdir = sys.argv[1]
    necdir = sys.argv[2] if len(sys.argv) > 2 else None
    trainlog = sys.argv[3] if len(sys.argv) > 3 else None
    f37 = load_mech(resdir, "37")
    m4 = load_mech(resdir, "4")
    nec = load_mech(necdir, "9") if necdir else None

    # per (battery,fam) -> iid -> {d:(corr,conf,rel)}
    seqs = defaultdict(dict)
    for battery in f37:
        for fam in f37[battery]:
            key = (battery, fam)
            for iid, dd in f37[battery][fam].items():
                seqs[key][iid] = dd

    print("=== F37 IFP kill-bar table ===")
    # B1/B2
    n10=v1=v2=0
    for key in seqs:
        for iid, dd in seqs[key].items():
            s = sorted(dd.items())
            for i in range(len(s)-1):
                d0,(c0,f0,_) = s[i]; d1,(c1,f1,_) = s[i+1]
                if c0=="1" and c1=="0":
                    n10+=1
                    if f1>=f0: v1+=1
                if c0=="0" and c1=="0" and f1>f0: v2+=1
    print(f"B1 1->0: {n10} -> {'PASS' if n10==0 else 'FAIL'}")
    print(f"B2 V1={v1} V2={v2} -> {'PASS' if v1==0 and v2==0 else 'FAIL'}")

    # B3 strict G-violations per family
    gviol_fam={}
    for key in sorted(seqs):
        cells=defaultdict(list)
        for iid, dd in seqs[key].items():
            for d,(c,f,_) in dd.items():
                if c in ("1","0"): cells[d].append((c,f))
        g={}
        for d,cl in sorted(cells.items()):
            if len(cl)>=1:
                g[d]=(sum(f for _,f in cl)/len(cl)/1000.0
                      - sum(1 for c,_ in cl if c=="1")/len(cl))
        ds=sorted(g); gv=sum(1 for i in range(len(ds)-1) if g[ds[i+1]]>g[ds[i]]+1e-12)
        gviol_fam[key]=(gv,g)
    totgv=sum(gv for gv,g in gviol_fam.values())
    print(f"B3 strict G-violations: total {totgv} -> {'PASS' if totgv==0 else 'FAIL'}")
    for key in sorted(gviol_fam):
        gv,g=gviol_fam[key]
        if gv>0:
            print(f"  {key[0]}/{key[1]}: Gviol={gv} G={ {d:round(v,3) for d,v in sorted(g.items())} }")

    # B4/B5 aggregate
    cc=[]; cw=[]
    for key in seqs:
        for iid, dd in seqs[key].items():
            for d,(c,f,_) in dd.items():
                if c=="1": cc.append(f/1000.0)
                elif c=="0": cw.append(f/1000.0)
    mcc=sum(cc)/len(cc) if cc else float('nan')
    mcw=sum(cw)/len(cw) if cw else float('nan')
    print(f"B4 meanConfCorrect={mcc:.3f} (n={len(cc)}) -> {'PASS' if mcc>=0.50 else 'FAIL'}")
    print(f"B5 separation={mcc-mcw:.3f} (wrong={mcw:.3f},n={len(cw)}) -> {'PASS' if (mcc-mcw)>=0.20 else 'FAIL'}")

    # B4b honest-family floor
    print("B4b honest-family floor:")
    for key in sorted(seqs):
        if key[1] not in HONEST: continue
        cf=[]
        for iid, dd in seqs[key].items():
            for d,(c,f,_) in dd.items():
                if c=="1": cf.append(f/1000.0)
        if len(cf)>=10:
            m=sum(cf)/len(cf)
            print(f"  {key[0]}/{key[1]}: meanC_correct={m:.3f} (n={len(cf)}) -> {'PASS' if m>=0.50 else 'FAIL'}")

    # B6 recall per family vs M4
    print("B6 recall (released-correct / M4 released-correct):")
    for key in sorted(seqs):
        f37rc=0; m4rc=0
        for iid, dd in seqs[key].items():
            for d,(c,f,_) in dd.items():
                if c=="1": f37rc+=1
        b,f=key
        if b in m4 and f in m4[b]:
            for iid, dd in m4[b][f].items():
                for d,(c,ff,_) in dd.items():
                    if c=="1": m4rc+=1
        r=f37rc/max(m4rc,1)
        print(f"  {b}/{f}: {f37rc}/{m4rc}={r:.3f} -> {'PASS' if r>=0.95 else 'FAIL'}")

    # B7 abstention
    tot=0; abst=0
    for key in seqs:
        for iid, dd in seqs[key].items():
            for d,(c,f,rel) in dd.items():
                tot+=1
                if c=="A": abst+=1
    print(f"B7 abstention={abst}/{tot}={abst/max(tot,1):.3f} -> {'PASS' if abst/max(tot,1)<=0.30 else 'FAIL'}")

    # B9 identity
    mm=0; tt=0
    for key in sorted(seqs):
        b,f=key
        for iid, dd in seqs[key].items():
            if b in m4 and f in m4[b] and iid in m4[b][f]:
                for d,(c,ff,rel) in dd.items():
                    if d in m4[b][f][iid]:
                        tt+=1
                        mc,mf,mr=m4[b][f][iid][d]
                        if (c,rel)!=(mc,mr): mm+=1
    print(f"B9 release+correct identity vs M4: {tt-mm}/{tt} -> {'PASS' if mm==0 else 'FAIL'}")

    # B12: G>0 crossings per family
    print("B12 G>0 crossings per family (recorded):")
    for key in sorted(gviol_fam):
        gv,g=gviol_fam[key]
        cross=sum(1 for d in g if g[d]>0)
        print(f"  {key[0]}/{key[1]}: {cross} depth slots with G>0")

    # B13: G(F,d)>=-0.100 where n_rel>=8
    print("B13 G(F,d)>=-0.100 (n_rel>=8; recorded):")
    b13bad=[]
    for key in sorted(seqs):
        cells=defaultdict(list)
        for iid, dd in seqs[key].items():
            for d,(c,f,_) in dd.items():
                if c in ("1","0"): cells[d].append((c,f))
        for d,cl in sorted(cells.items()):
            if len(cl)>=8:
                g=sum(f for _,f in cl)/len(cl)/1000.0 - sum(1 for c,_ in cl if c=="1")/len(cl)
                if g<-0.100: b13bad.append((key,d,round(g,3),len(cl)))
    if b13bad:
        for k,d,g,n in b13bad: print(f"  {k[0]}/{k[1]} d={d}: G={g} (n={n}) BELOW -0.100")
    else:
        print("  all (F,d) with n_rel>=8 satisfy G>=-0.100")

    # B3pi: per-item (conf/1000-acc) rises across adjacent depths
    pi=0; pit=0
    for key in seqs:
        for iid, dd in seqs[key].items():
            s=sorted(dd.items())
            for i in range(len(s)-1):
                d0,(c0,f0,_)=s[i]; d1,(c1,f1,_)=s[i+1]
                if c0 in ("1","0") and c1 in ("1","0"):
                    pit+=1
                    a0=1.0 if c0=="1" else 0.0; a1=1.0 if c1=="1" else 0.0
                    if (f1/1000.0-a1)>(f0/1000.0-a0)+1e-12: pi+=1
    print(f"B3pi per-item pi-rises: {pi}/{pit}={pi/max(pit,1):.3f} (recorded)")

    # NEC deltas
    if nec:
        print("=== deltas vs NEC m9 ===")
        for key in sorted(gviol_fam):
            b,f=key
            gv37,_=gviol_fam[key]
            gv9=0
            if b in nec and f in nec[b]:
                cb=defaultdict(list)
                for iid,dd in nec[b][f].items():
                    for d,(c,ff,_) in dd.items():
                        if c in ("1","0"): cb[d].append((c,ff))
                g={}
                for d,cl in sorted(cb.items()):
                    if len(cl)>=1:
                        g[d]=(sum(x for _,x in cl)/len(cl)/1000.0
                              - sum(1 for c,_ in cl if c=="1")/len(cl))
                ds=sorted(g); gv9=sum(1 for i in range(len(ds)-1) if g[ds[i+1]]>g[ds[i]]+1e-12)
            print(f"  {b}/{f}: Gviol F37={gv37} NEC={gv9} delta={gv37-gv9:+d}")

    # F37 fixed-point checks from training log
    if trainlog:
        print("=== F37 fixed-point checks (training log) ===")
        rows=[]
        with open(trainlog) as fh:
            for line in fh:
                if line.startswith("#"): continue
                p=line.rstrip().split("\t")
                if len(p)==5: rows.append(tuple(int(x) for x in p))
        # FP1: max|w| trend after t=10000
        post=[r for r in rows if r[0]>=10000]
        mws=[r[1] for r in post]
        print(f"FP1 contraction: max|w| over t>=10000: min={min(mws)} max={max(mws)} "
              f"(n={len(post)} checkpoints) -> {'PASS (bounded, not growing)' if max(mws)<=1 else 'CHECK'}")
        # FP2: edge mass at fixed point (t>10000)
        # edge counts are cumulative; take diff between last and t=10000 rows
        r10=[r for r in rows if r[0]==10000][0]
        rl=rows[-1]
        d_edge=rl[2]-r10[2]; d_emit=rl[3]-r10[3]
        print(f"FP2 edge mass t>10000: {d_edge}/{d_emit}={d_edge/max(d_emit,1):.4f} "
              f"-> {'PASS' if d_edge/max(d_emit,1)<=0.05 else 'FAIL'}")
        # also report literal all-emits edge mass
        print(f"  (literal all-training-emits edge mass: {rl[2]}/{rl[3]}={rl[2]/rl[3]:.3f})")

if __name__=="__main__":
    main()
