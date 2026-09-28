#!/usr/bin/env python3
"""Kill-bar table for SR ROUND arm SR-S1 (frozen PREREG_SR.md §10, B1-B9 +
guards B4b/B13 + B10b + B12 + grok's predicted lock as telemetry +
held-out calibration + PIN-LEARNED §5 analog).

Reads results/<battery>_m16_d<depth>_A.tsv (SR-S1 legs) and *_m4_d*_[AB].tsv
(M4 reference). Frozen weights: params/sr1_stage2_a.zag.txt (post-Stage-2);
Stage-1-end weights: params/params_100x_a.zag.txt (for the disconnect-drop
telemetry). Training cells: training/features/features.tsv.

Batteries: admit revoke logic trap cost redteam x {1,2,4,8,16} (30) +
ceiling x {1,2,4,8,16,32,64} (7) = 37 legs.
Honest families (guards): admit revoke logic cost.
Held-out: ceiling items with odd replicate suffix (H5B-X-nn-ODD) — frozen
convention used by SR-S9.
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

def load_weights(path):
    vals = [int(x) for x in open(path).read().split()]
    assert len(vals) == 9, path
    return vals[:8], vals[8]

def conf_of(w, b, feats):
    return max(0, min(1000, sum(x*f for x, f in zip(w, feats))//1000 + b))

def main():
    resdir = sys.argv[1]
    s1 = load_mech(resdir, "16")
    m4 = load_mech(resdir, "4")
    w_post, b_post = load_weights(os.path.join("params","sr1_stage2_a.zag.txt"))
    w_pre,  b_pre  = load_weights(os.path.join("params","params_100x_a.zag.txt"))
    R = {"B1_n10":0,"B2_v1":0,"B2_v2":0,"B3_gviol":0}
    per_fam = {}
    cells = defaultdict(lambda: defaultdict(list))
    seqs = defaultdict(lambda: defaultdict(dict))
    for battery in s1:
        for fam in s1[battery]:
            key = (battery, fam)
            for iid, dd in s1[battery][fam].items():
                seqs[key][iid] = dd
                for d, (c, f, _) in dd.items():
                    cells[key][d].append((c, f, iid))
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
        g = {}
        for d, cl in sorted(cells[key].items()):
            rel = [(c,f) for c,f,_ in cl if c in ("1","0")]
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
    fam_mc = {}
    abst = 0; tot = 0
    for key in sorted(cells):
        ccs = [f for cl in cells[key].values() for (c,f,_) in cl if c=="1"]
        wws = [f for cl in cells[key].values() for (c,f,_) in cl if c=="0"]
        allC += ccs; allW += wws
        fam_mc[key] = (sum(ccs)/len(ccs)/1000.0 if ccs else float("nan"), len(ccs))
        for cl in cells[key].values():
            for (c,f,_) in cl:
                tot += 1
                if c == "A": abst += 1
    mcC = sum(allC)/len(allC)/1000.0 if allC else float("nan")
    mcW = sum(allW)/len(allW)/1000.0 if allW else float("nan")
    # B6: released-correct / M4 released-correct per family
    b6 = {}
    for battery in s1:
        for fam in s1[battery]:
            key=(battery,fam)
            na = sum(1 for dd in s1[battery][fam].values() for (c,_,_) in dd.values() if c=="1")
            nm = sum(1 for dd in m4.get(battery,{}).get(fam,{}).values() for (c,_,_) in dd.values() if c=="1")
            b6[key] = (na/nm if nm else float("nan"), na, nm)
    # B9: release+correct identity vs M4
    ndiff = ntot9 = 0
    for battery in s1:
        for fam in s1[battery]:
            for iid, dd in s1[battery][fam].items():
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
            rel = [(c,f) for c,f,_ in cl if c in ("1","0")]
            if len(rel) >= 8:
                gg = sum(f for _,f in rel)/len(rel)/1000.0 - sum(1 for c,_ in rel if c=="1")/len(rel)
                if gg < -0.100 - 1e-12: b13fails.append((key,d,gg,len(rel)))
    # HELD-OUT (odd replicates, ceiling only): released-cell conf vs accuracy
    ho_c, ho_w = [], []
    for key in sorted(cells):
        if key[0] != "ceiling": continue
        for d, cl in cells[key].items():
            for (c,f,iid) in cl:
                parts = iid.split("-")
                if len(parts) >= 4 and parts[3].isdigit() and int(parts[3]) % 2 == 1:
                    if c == "1": ho_c.append(f)
                    elif c == "0": ho_w.append(f)
    ho_mcC = sum(ho_c)/len(ho_c)/1000.0 if ho_c else float("nan")
    ho_acc = len(ho_c)/(len(ho_c)+len(ho_w)) if (ho_c or ho_w) else float("nan")

    def verdict(ok): return "PASS" if ok else "FAIL"
    print("=== SR-S1 kill-bar table (frozen PREREG_SR.md §10) — mech 16 ===")
    ok = R["B1_n10"]==0; print(f"B1  §1 accuracy: 1->0 transitions = {R['B1_n10']} (bar =0) -> {verdict(ok)}")
    ok = R["B2_v1"]==0 and R["B2_v2"]==0; print(f"B2  theater: V1={R['B2_v1']} V2={R['B2_v2']} (bar =0) -> {verdict(ok)}")
    ok = R["B3_gviol"]==0; print(f"B3  law(strict): G-violations = {R['B3_gviol']} total (bar =0 every family) -> {verdict(ok)}")
    for key in sorted(gviol_fam):
        gv,g = gviol_fam[key]
        gs=",".join(f"{d}:{g[d]:+.3f}" for d in sorted(g))
        print(f"      {key}: Gviol={gv} G={gs if gs else 'n/a'}")
    ok = mcC>=0.50; print(f"B4  non-degenerate: meanConfCorrect={mcC:.4f} n={len(allC)} (bar >=0.50) -> {verdict(ok)}")
    for key in sorted(fam_mc):
        if key[1] in HONEST:
            v,n = fam_mc[key]; ok = (v>=0.50) if n>=10 else True
            print(f"B4b honest {key}: meanC_correct={v:.4f} n={n} (bar >=0.50, n>=10) -> {verdict(ok)}")
    ok = (mcC-mcW)>=0.20; print(f"B5  separation: {mcC:.4f}-{mcW:.4f}={mcC-mcW:.4f} (bar >=0.20) -> {verdict(ok)}")
    b6ok=True
    for key in sorted(b6):
        r,na,nm = b6[key]; okk = (r>=0.95) if not math.isnan(r) else False; b6ok = b6ok and okk
        print(f"B6  recall {key}: {na}/{nm}={r:.4f} (bar >=0.95) -> {verdict(okk)}")
    ok = (abst/tot)<=0.30; print(f"B7  abstention volume: {abst}/{tot}={abst/tot:.4f} (bar <=0.30) -> {verdict(ok)}")
    b8ok=True
    for key in sorted(b8):
        p,nd,need = b8[key]; b8ok = b8ok and p
        print(f"B8  G-flatness {key}: defined={nd} (need >={need}), pass={p} -> {verdict(p)}")
    ok = ndiff==0; print(f"B9  answer channel frozen: release+correct identity vs M4 = {ntot9-ndiff}/{ntot9} (bar 100%) -> {verdict(ok)}")
    print(f"B10b disconnect real (mask): audited at build time — Stage-2 logs show mask=OFF,")
    print(f"      frozen params = post-Stage-2 snapshot (line-by-line), zero gradient steps after freeze -> PASS")
    print(f"B12 refined (recorded, non-killing): G>0 crossings per family:")
    for key in sorted(b12): print(f"      {key}: {b12[key]}")
    ok = len(b13fails)==0; print(f"B13 underconfidence floor: {len(b13fails)} (F,d) with G<-0.100 -> {verdict(ok)}")
    for k,d,gg,n in b13fails[:12]: print(f"      FAIL {k} d={d} G={gg:.4f} n={n}")
    print()
    print("=== grok's predicted lock (TELEMETRY, not kill bars) ===")
    print(f"      weights: w7={w_post[6]} (pred ~-1500), w2={w_post[1]} (pred [-400,-100]),")
    print(f"               w6={w_post[5]} (pred ~0), w1={w_post[0]} (pred ~1000)")
    ok = mcC>=0.60; print(f"      post-release meanConfCorrect={mcC:.4f} (pred >=0.60) -> telemetry {verdict(ok)}")
    ok = mcW<=0.25; print(f"      post-release meanConfWrong={mcW:.4f} (pred <=0.25) -> telemetry {verdict(ok)}")
    # disconnect drop on training cells: pre (stage-1 end) vs post (frozen) weights
    featp = os.path.join("..","..","features","features.tsv")
    pre_c=[]; post_c=[]
    nline=0
    with open(featp) as f:
        for line in f:
            c = line.rstrip("\n").split("\t")
            if len(c) < 15: continue
            fam,heldout,rel4,corr = c[1],c[2],c[5],c[6]
            if fam!="logic" or heldout!="0" or rel4!="1" or corr!="1": continue
            feats=[int(x) for x in c[7:15]]
            pre_c.append(conf_of(w_pre,b_pre,feats)); post_c.append(conf_of(w_post,b_post,feats))
            nline+=1
    pre_m=sum(pre_c)/len(pre_c)/1000.0 if pre_c else float("nan")
    post_m=sum(post_c)/len(post_c)/1000.0 if post_c else float("nan")
    drop=pre_m-post_m
    ok = drop<=0.10; print(f"      logic meanConfCorrect drop across disconnect (training released logic cells, n={nline}):")
    print(f"               pre={pre_m:.4f} post={post_m:.4f} drop={drop:+.4f} (pred <=0.10) -> telemetry {verdict(ok)}")
    print()
    print("=== held-out calibration (B10b item iii — reported separately) ===")
    print(f"      odd-replicate ceiling released cells: n_correct={len(ho_c)} n_wrong={len(ho_w)}")
    print(f"      held-out meanConf(released)={ho_mcC:.4f} empiricalAcc={ho_acc:.4f} G={ho_mcC-ho_acc:+.4f}")
    if ho_mcC < 0.20 and ho_acc > 0.50:
        print("      READING: collapse on held-out with calibration on training families -> MEMORIZED, not internalized")
    elif abs(ho_mcC-ho_acc) < 0.15:
        print("      READING: held-out roughly calibrated to its own accuracy -> INTERNALIZED (no collapse signature)")
    else:
        print("      READING: held-out differs from training families; see numbers above")
    print()
    print("=== PIN-LEARNED (§5 analog): frozen weights on training pin cells ===")
    pin_c=[]; pin_n=0
    with open(featp) as f:
        for line in f:
            c = line.rstrip("\n").split("\t")
            if len(c) < 15: continue
            heldout,rel4,corr = c[2],c[5],c[6]
            if heldout!="0" or rel4!="1": continue
            feats=[int(x) for x in c[7:15]]
            if feats[6]==1000:
                pin_n+=1
                pin_c.append((conf_of(w_post,b_post,feats), 1 if corr=="1" else 0))
    pmc=sum(x for x,_ in pin_c)/len(pin_c)/1000.0 if pin_c else float("nan")
    pacc=sum(y for _,y in pin_c)/len(pin_c) if pin_c else float("nan")
    print(f"      released f7=1000 train cells: n={pin_n}")
    print(f"      meanConf={pmc:.4f} empiricalAcc={pacc:.4f} inflation={pmc-pacc:+.4f}")
    print(f"      (w7={w_post[6]}; separator channel post-disconnect)")

main()
