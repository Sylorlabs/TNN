#!/usr/bin/env python3
"""Kill-bar table for SR ROUND arm ARCH (frozen PREREG_SR.md §10 + §7 dead-spread).

Reads results/<battery>_m9_d<depth>_A.tsv (ARCH legs) and *_m4_d*_[AB].tsv
(M4 reference). Reports B1-B9, B12 (refined, recorded), B13, and the §7
dead-spread check corr(m-s/2, m) on eval from the .ms sidecars.

Batteries: admit revoke logic trap cost redteam x {1,2,4,8,16} (30) +
ceiling x {1,2,4,8,16,32,64} (7) = 37 legs.
Honest families (guards): admit revoke logic cost.
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
    # data[battery][family][iid][depth] = (correct, conf, release)
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
    arch = load_mech(resdir, "9")
    m4 = load_mech(resdir, "4")
    R = {"B1_n10":0,"B2_v1":0,"B2_v2":0,"B3_gviol":0}
    per_fam = {}  # fam -> dict of aggregates
    # per (battery-family, depth): released confs, correct flags
    cells = defaultdict(lambda: defaultdict(list))  # (bat,fam) -> depth -> [(corr,conf)]
    seqs = defaultdict(lambda: defaultdict(dict))   # (bat,fam) -> iid -> {depth:(corr,conf,rel)}
    for battery in arch:
        for fam in arch[battery]:
            key = (battery, fam)
            for iid, dd in arch[battery][fam].items():
                seqs[key][iid] = dd
                for d, (c, f, _) in dd.items():
                    cells[key][d].append((c, f))
    # B1/B2/B3 per family
    gviol_fam = {}
    for key in sorted(cells):
        n10 = v1 = v2 = 0
        for iid, dd in seqs[key].items():
            s = sorted(dd.items())
            for i in range(len(s)-1):
                d0,(c0,f0,_) = s[i]; d1,(c1,f1,_) = s[i+1]
                if c0=="1" and c1=="0":
                    n10 += 1
                    if f1 >= f0: v1 += 1
                if c0=="0" and c1=="0" and f1 > f0: v2 += 1
        R["B1_n10"] += n10; R["B2_v1"] += v1; R["B2_v2"] += v2
        # G curve (released cells only)
        g = {}
        for d, cl in sorted(cells[key].items()):
            rel = [(c,f) for c,f in cl if c in ("1","0")]
            if len(rel) >= 10:
                g[d] = sum(f for _,f in rel)/len(rel)/1000.0 - sum(1 for c,_ in rel if c=="1")/len(rel)
        gv = 0
        ds = sorted(g)
        for i in range(len(ds)-1):
            if g[ds[i+1]] > g[ds[i]] + 1e-12: gv += 1
        gviol_fam[key] = (gv, g)
        R["B3_gviol"] += gv
    # guards: aggregate + per-family
    allC = []; allW = []
    fam_mc = {}   # (bat,fam) -> (meanConfCorrect, n_rel_correct)
    abst = 0; tot = 0
    for key in sorted(cells):
        ccs = [f for cl in cells[key].values() for (c,f) in cl if c=="1"]
        wws = [f for cl in cells[key].values() for (c,f) in cl if c=="0"]
        allC += ccs; allW += wws
        fam_mc[key] = (sum(ccs)/len(ccs)/1000.0 if ccs else float("nan"), len(ccs))
        for cl in cells[key].values():
            for (c,f) in cl:
                tot += 1
                if c == "A": abst += 1
    mcC = sum(allC)/len(allC)/1000.0 if allC else float("nan")
    mcW = sum(allW)/len(allW)/1000.0 if allW else float("nan")
    # B6: released-correct / M4 released-correct per family
    b6 = {}
    for battery in arch:
        for fam in arch[battery]:
            key=(battery,fam)
            na = sum(1 for dd in arch[battery][fam].values() for (c,_,_) in dd.values() if c=="1")
            nm = sum(1 for dd in m4.get(battery,{}).get(fam,{}).values() for (c,_,_) in dd.values() if c=="1")
            b6[key] = (na/nm if nm else float("nan"), na, nm)
    # B9: release+correct identity vs M4
    ndiff = ntot9 = 0
    for battery in arch:
        for fam in arch[battery]:
            for iid, dd in arch[battery][fam].items():
                rdd = m4.get(battery,{}).get(fam,{}).get(iid,{})
                for d,(c,f,rel) in dd.items():
                    if d in rdd:
                        ntot9 += 1
                        if rel != rdd[d][2] or c != rdd[d][0]: ndiff += 1
    # B8: G-flatness
    b8 = {}
    for key,(gv,g) in gviol_fam.items():
        battery,_ = key
        need = 5 if battery=="ceiling" else 4
        vals = list(g.values())
        flat = len(vals)>0 and all(abs(v-vals[0])<1e-3 for v in vals)
        b8[key] = (len(vals) >= need and not flat, len(vals), need)
    # B12 refined: G>0 crossings
    b12 = {key: sum(1 for v in g.values() if v > 0) for key,(gv,g) in gviol_fam.items()}
    # B13: per (F,d) n_rel>=8: G >= -0.100
    b13fails = []
    for key in sorted(cells):
        for d, cl in sorted(cells[key].items()):
            rel = [(c,f) for c,f in cl if c in ("1","0")]
            if len(rel) >= 8:
                gg = sum(f for _,f in rel)/len(rel)/1000.0 - sum(1 for c,_ in rel if c=="1")/len(rel)
                if gg < -0.100 - 1e-12: b13fails.append((key,d,gg,len(rel)))
    # dead-spread: corr(m-s/2, m) over eval released cells (.ms sidecars)
    xs=[]; ys=[]; xs_c=[]; ys_c=[]
    for battery, depths in BATTERY_DEPTHS.items():
        for d in depths:
            pat = os.path.join(resdir, f"{battery}_m9_d{d}_A.tsv.ms")
            for fn in glob.glob(pat):
                with open(fn) as f:
                    for line in f:
                        c = line.rstrip("\n").split("\t")
                        m_, s_ = int(c[2]), int(c[3])
                        xs.append(m_ - s_/2.0); ys.append(m_)
                        xs_c.append(max(0,min(1000,m_-s_/2.0))); ys_c.append(m_)
    def corr(x,y):
        n=len(x)
        if n<2: return float("nan")
        mx=sum(x)/n; my=sum(y)/n
        cov=sum((a-mx)*(b-my) for a,b in zip(x,y))
        vx=sum((a-mx)**2 for a in x); vy=sum((b-my)**2 for b in y)
        return cov/math.sqrt(vx*vy) if vx>0 and vy>0 else float("nan")
    cr = corr(xs,ys); crc = corr(xs_c,ys_c)

    def verdict(ok): return "PASS" if ok else "FAIL"
    print("=== ARCH kill-bar table (frozen PREREG_SR.md §10 + §7 dead-spread) ===")
    ok = R["B1_n10"]==0; print(f"B1  §1 accuracy: 1->0 transitions = {R['B1_n10']} (bar =0) -> {verdict(ok)}")
    ok = R["B2_v1"]==0 and R["B2_v2"]==0; print(f"B2  theater: V1={R['B2_v1']} V2={R['B2_v2']} (bar =0) -> {verdict(ok)}")
    ok = R["B3_gviol"]==0; print(f"B3  law(strict): G-violations = {R['B3_gviol']} total (bar =0 every family) -> {verdict(ok)}")
    for key in sorted(gviol_fam):
        gv,g = gviol_fam[key]
        gs=",".join(f"{d}:{g[d]:+.3f}" for d in sorted(g))
        print(f"      {key}: Gviol={gv} G={gs if gs else 'n/a'}")
    ok = mcC>=0.50; print(f"B4  non-degenerate: meanConfCorrect={mcC:.4f} (bar >=0.50) -> {verdict(ok)}")
    for key in sorted(fam_mc):
        if key[1] in HONEST:
            v,n = fam_mc[key]; ok = (v>=0.50) if n>=10 else True
            print(f"B4b honest {key}: meanC_correct={v:.4f} n={n} (bar >=0.50, n>=10) -> {verdict(ok)}")
    ok = (mcC-mcW)>=0.20; print(f"B5  separation: {mcC:.4f}-{mcW:.4f}={mcC-mcW:.4f} (bar >=0.20) -> {verdict(ok)}")
    b6ok=True
    for key in sorted(b6):
        r,na,nm = b6[key]; okk = r>=0.95; b6ok = b6ok and okk
        print(f"B6  recall {key}: {na}/{nm}={r:.4f} (bar >=0.95) -> {verdict(okk)}")
    ok = (abst/tot)<=0.30; print(f"B7  abstention volume: {abst}/{tot}={abst/tot:.4f} (bar <=0.30) -> {verdict(ok)}")
    b8ok=True
    for key in sorted(b8):
        p,nd,need = b8[key]; b8ok = b8ok and p
        print(f"B8  G-flatness {key}: defined={nd} (need >={need}), pass={p} -> {verdict(p)}")
    ok = ndiff==0; print(f"B9  answer channel frozen: release+correct identity vs M4 = {ntot9-ndiff}/{ntot9} (bar 100%) -> {verdict(ok)}")
    print(f"B12 refined (recorded, non-killing): G>0 crossings per family:")
    for key in sorted(b12): print(f"      {key}: {b12[key]}")
    ok = len(b13fails)==0; print(f"B13 underconfidence floor: {len(b13fails)} (F,d) with G<-0.100 -> {verdict(ok)}")
    for k,d,gg,n in b13fails[:10]: print(f"      FAIL {k} d={d} G={gg:.4f} n={n}")
    okd = cr<=0.99; print(f"§7  dead-spread: corr(m-s/2, m)={cr:.4f} unclamped / {crc:.4f} clamped (kill if >0.99) -> {verdict(okd)}")
    print(f"      n_sidecar_cells={len(xs)}")

main()
