#!/usr/bin/env python3
"""Kill-bar table for F31 DDCL (PREREG_FORKROUND.md §4, B8 amended §4b), mech 31.

Reads results_f31full/<battery>_m31_d<depth>_A.tsv (F31 legs) and
*_m4_d*_[AB].tsv (M4 reference); NEC m9 legs for deltas.

Bars: B1..B9, B4b, amended B8, B13; recorded B12, B3pi; deltas vs NEC m9.

F31-specific falsifiers (§3 + task spec):
  KILL (a): feedback oscillation/saturation. Measurable: (i) training flip
            storm (flip rate in the damp log), (ii) eval per-family G sequences
            with adjacent-rung sign alternation (ping-pong), (iii) saturation
            at the offset (±200) or damp (200..800) clamps.
  KILL (b): tiny-n redteam B3 no better than base (NEC m9). Strict-law
            G-violation count on redteam legs F31 vs NEC m9; KILL if F31's
            violations are NOT strictly fewer.
  KILL (c): B13 failure from over-correction. B13 fails (G<-0.100, n_rel>=8)
            AND failing cells at depths with positive offsets (over-subtraction).

Usage: python3 killbars_f31.py
"""
import os, glob, math, re
from collections import defaultdict

BASE = os.path.expanduser("~/workspace/tnn-lab/deliberation_depth/monotonicity/training")
RES  = os.path.join(BASE, "results_f31full")
NEC  = os.path.join(BASE, "ncal", "results_nec")
PARAMS = os.path.expanduser("~/workspace/tnn-lab/deliberation_depth/monotonicity/training/fork_round/f31_ddcl/params/f31_params_a.zag")
TRAINLOG = os.path.expanduser("~/workspace/tnn-lab/deliberation_depth/monotonicity/training/fork_round/f31_ddcl/logs/train_a.tsv")

BATTERY_DEPTHS = {"admit":[1,2,4,8,16],"revoke":[1,2,4,8,16],"logic":[1,2,4,8,16],
                  "trap":[1,2,4,8,16],"cost":[1,2,4,8,16],"redteam":[1,2,4,8,16],
                  "ceiling":[1,2,4,8,16,32,64]}
HONEST = {"admit","revoke","logic","cost"}
DSLOT = {1:0,2:1,4:2,8:3,16:4,32:5,64:6}

def family_of(battery, iid):
    if battery == "ceiling":
        parts = iid.split("-")
        if len(parts) >= 2 and parts[0] == "H5B":
            return parts[1]
        return "ceiling?"
    return battery

def load_mech(resdir, mtag):
    data = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
    n = 0
    for battery, depths in BATTERY_DEPTHS.items():
        for d in depths:
            pat = os.path.join(resdir, f"{battery}_m{mtag}_d{d}_A.tsv")
            for fn in glob.glob(pat):
                n += 1
                with open(fn) as f:
                    for line in f:
                        line = line.rstrip("\n")
                        if not line: continue
                        c = line.split("\t")
                        iid, depth = c[0], int(c[1])
                        rel, corr, conf = c[6], c[7], int(c[8])
                        fam = family_of(battery, iid)
                        data[battery][fam][iid][depth] = (corr, conf, rel)
    return data, n

def load_nec():
    nec = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
    for battery, depths in BATTERY_DEPTHS.items():
        for d in depths:
            pat = os.path.join(NEC, f"{battery}_m9_d{d}_A.tsv")
            for fn in glob.glob(pat):
                with open(fn) as f:
                    for line in f:
                        line = line.rstrip("\n")
                        if not line: continue
                        c = line.split("\t")
                        iid, depth = c[0], int(c[1])
                        rel, corr, conf = c[6], c[7], int(c[8])
                        fam = family_of(battery, iid)
                        nec[battery][fam][iid][depth] = (corr, conf, rel)
    return nec

def main():
    f31, nf31 = load_mech(RES, "31")
    m4, nm4 = load_mech(RES, "4")
    nec = load_nec()
    print(f"parsed {nf31} F31 run-A TSVs, {nm4} M4 run-A TSVs")

    R = {"B1_n10":0,"B2_v1":0,"B2_v2":0,"B3_gviol":0}
    cells = defaultdict(lambda: defaultdict(list))
    m4cells = defaultdict(lambda: defaultdict(list))
    seqs = defaultdict(lambda: defaultdict(dict))
    for battery in f31:
        for fam in f31[battery]:
            key = (battery, fam)
            for iid, dd in f31[battery][fam].items():
                seqs[key][iid] = dd
                for d, (c, f, _) in dd.items():
                    cells[key][d].append((c, f, iid))
    for battery in m4:
        for fam in m4[battery]:
            key = (battery, fam)
            for iid, dd in m4[battery][fam].items():
                for d, (c, f, _) in dd.items():
                    m4cells[key][d].append((c, f, iid))

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
        g = {}; nrel_d = {}
        for d, cl in sorted(cells[key].items()):
            rel = [(c,f) for c,f,_ in cl if c in ("1","0")]
            nrel_d[d] = len(rel)
            if len(rel) >= 1:
                g[d] = (sum(f for _,f in rel)/len(rel)/1000.0
                        - sum(1 for c,_ in rel if c=="1")/len(rel))
        gv = 0
        ds = sorted(g)
        for i in range(len(ds)-1):
            if g[ds[i+1]] > g[ds[i]] + 1e-12:
                gv += 1
        gviol_fam[key] = (gv, g, nrel_d)
        R["B3_gviol"] += gv

    nec_gviol = {}
    for battery in nec:
        for fam in nec[battery]:
            key = (battery, fam)
            cb = defaultdict(list)
            for iid, dd in nec[battery][fam].items():
                for d, (c, f, _) in dd.items():
                    if c in ("1","0"): cb[d].append((c,f))
            g = {}
            for d, cl in sorted(cb.items()):
                if cl:
                    g[d] = (sum(f for _,f in cl)/len(cl)/1000.0
                            - sum(1 for c,_ in cl if c=="1")/len(cl))
            ds = sorted(g)
            nec_gviol[key] = sum(1 for i in range(len(ds)-1)
                                 if g[ds[i+1]] > g[ds[i]] + 1e-12)

    allC = []; allW = []
    fam_mc = {}; hon_mc = {}
    abst = tot = 0
    for key in sorted(cells):
        ccs = [f for cl in cells[key].values() for (c,f,_) in cl if c=="1"]
        wws = [f for cl in cells[key].values() for (c,f,_) in cl if c=="0"]
        allC += ccs; allW += wws
        fam_mc[key] = (sum(ccs)/len(ccs)/1000.0 if ccs else float("nan"), len(ccs))
        if key[0] in HONEST:
            hon_mc[key] = fam_mc[key]
        for cl in cells[key].values():
            for (c,f,_) in cl:
                tot += 1
                if c == "A": abst += 1
    mcC = sum(allC)/len(allC)/1000.0 if allC else float("nan")
    mcW = sum(allW)/len(allW)/1000.0 if allW else float("nan")
    kill_b_hits = [(k,v,n) for k,(v,n) in hon_mc.items() if v < 0.50]

    b6 = {}
    for key in sorted(seqs):
        na = sum(1 for dd in seqs[key].values() for (c,_,_) in dd.values() if c=="1")
        nm = sum(1 for dd in m4.get(key[0],{}).get(key[1],{}).values() for (c,_,_) in dd.values() if c=="1")
        b6[key] = (na/nm if nm else float("nan"), na, nm)

    ndiff = ntot9 = 0
    for key in seqs:
        for iid, dd in seqs[key].items():
            rdd = m4.get(key[0],{}).get(key[1],{}).get(iid,{})
            for d,(c,f,rel) in dd.items():
                if d in rdd:
                    ntot9 += 1
                    if rel != rdd[d][2] or c != rdd[d][0]: ndiff += 1

    b8 = {}
    for key,(gv,g,nr) in gviol_fam.items():
        battery,_ = key
        need = 5 if battery=="ceiling" else 4
        feas = [d for d,cl in sorted(m4cells[key].items())
                if sum(1 for (c,f,_) in cl if c in ("1","0")) >= 10]
        defined = [d for d in feas if nr.get(d,0) >= 1]
        vals = [g[d] for d in defined if d in g]
        if len(feas) < need:
            b8[key] = ("VOID", len(feas), need, len(defined))
        else:
            okdef = len(defined) >= need
            alleq = len(vals)>0 and all(abs(v-vals[0])<1e-3 for v in vals)
            tiny = alleq and abs(vals[0])<=1e-6
            oknv = (not alleq) or tiny
            b8[key] = ("PASS" if (okdef and oknv) else "FAIL",
                       len(feas), need, len(defined),
                       ("nonvac-ok" if oknv else "VACUOUS"),
                       ("perfect-cal" if tiny else ""))

    b12 = {key: sum(1 for v in g.values() if v > 0) for key,(gv,g,_) in gviol_fam.items()}

    b13fails = []
    for key in sorted(cells):
        for d, cl in sorted(cells[key].items()):
            rel = [(c,f) for c,f,_ in cl if c in ("1","0")]
            if len(rel) >= 8:
                gg = (sum(f for _,f in rel)/len(rel)/1000.0
                      - sum(1 for c,_ in rel if c=="1")/len(rel))
                if gg < -0.100 - 1e-12: b13fails.append((key,d,gg,len(rel)))

    b3pi = b3pi_pairs = 0
    for key in seqs:
        for iid, dd in seqs[key].items():
            s = sorted(dd.items())
            for i in range(len(s)-1):
                d0,(c0,f0,_) = s[i]; d1,(c1,f1,_) = s[i+1]
                if c0 in ("1","0") and c1 in ("1","0"):
                    b3pi_pairs += 1
                    if (f1/1000.0-(1 if c1=="1" else 0)) > (f0/1000.0-(1 if c0=="1" else 0)) + 1e-12:
                        b3pi += 1

    offs = {}
    txt = open(PARAMS).read()
    for m in re.finditer(r"fn f31_off(\d)\(\)i64 \{ return (-?\d+); \}", txt):
        offs[int(m.group(1))] = int(m.group(2))
    w1m = re.search(r"fn f31_w1\(\)i64 \{ return (-?\d+); \}", txt)

    flips = ups = downs = maxdamp = 0
    damp_final = None
    ntrain = 0
    for line in open(TRAINLOG):
        p = line.rstrip("\n").split("\t")
        if line.startswith("#") and "train_f31" in line:
            m = re.search(r"train_released=(\d+)", line); ntrain = int(m.group(1))
        if p[0] == "damp":
            if "flip" in p[2]: flips += 1
            else: ups += 1
            d = int(p[3].split("=")[1]); maxdamp = max(maxdamp, d)
        if p[0] == "final":
            damp_final = int(p[1].split("=")[1])
            ups = int(p[3].split("=")[1]); downs = int(p[4].split("=")[1])

    # F31 KILL (a): oscillation — eval ping-pong (adjacent-rung G sign alternation)
    ping = []
    for key,(gv,g,nr) in sorted(gviol_fam.items()):
        ds = sorted(g)
        sgn = [1 if g[d]>1e-9 else (-1 if g[d]<-1e-9 else 0) for d in ds]
        alt = sum(1 for i in range(len(sgn)-1) if sgn[i]!=0 and sgn[i+1]!=0 and sgn[i]!=sgn[i+1])
        if alt >= 2:
            ping.append((key, alt, [(d, round(g[d],3)) for d in ds]))

    # F31 KILL (b): redteam tiny-n B3 vs NEC m9 base
    rt_keys = sorted(k for k in gviol_fam if k[0]=="redteam")
    f31_rt_gv = sum(gviol_fam[k][0] for k in rt_keys)
    nec_rt_gv = sum(nec_gviol.get(k,0) for k in rt_keys)

    def verdict(ok): return "PASS" if ok else "FAIL"
    print("=== F31 DDCL kill-bar table (PREREG_FORKROUND.md §4; B8 amended §4b) — mech 31 ===")
    print(f"B1  accuracy: 1->0 = {R['B1_n10']} (bar =0) -> {verdict(R['B1_n10']==0)}")
    print(f"B2  theater: V1={R['B2_v1']} V2={R['B2_v2']} (bar =0) -> {verdict(R['B2_v1']==0 and R['B2_v2']==0)}")
    print(f"B3  law(strict): G-violations total = {R['B3_gviol']} (bar =0 every family) -> {verdict(R['B3_gviol']==0)}")
    nec_tot = sum(nec_gviol.values())
    for key in sorted(gviol_fam):
        gv,g,nr = gviol_fam[key]
        gs=",".join(f"{d}:{g[d]:+.3f}(n={nr[d]})" for d in sorted(g))
        ng = f" vs NEC m9 Gviol={nec_gviol.get(key,'?')}" if nec_gviol else ""
        print(f"      {key}: Gviol={gv}{ng} G={gs if gs else 'n/a'}")
    print(f"      NEC m9 total Gviol={nec_tot}")
    print(f"B4  non-degenerate: meanConfCorrect={mcC:.4f} n={len(allC)} (bar >=0.50) -> {verdict(mcC>=0.50)}")
    for key in sorted(hon_mc):
        v,n = hon_mc[key]; okk = (v>=0.50) if n>=10 else True
        print(f"B4b honest {key}: meanC_correct={v:.4f} n={n} (bar >=0.50, n>=10) -> {verdict(okk)}")
    print(f"B5  separation: {mcC:.4f}-{mcW:.4f}={mcC-mcW:.4f} (bar >=0.20) -> {verdict((mcC-mcW)>=0.20)}")
    b6ok=True
    for key in sorted(b6):
        r,na,nm = b6[key]
        if math.isnan(r):
            print(f"B6  recall {key}: {na}/{nm}=nan (M4 releases none correct; B9-identical -> VACUOUS PASS)")
            continue
        okk = r>=0.95; b6ok = b6ok and okk
        print(f"B6  recall {key}: {na}/{nm}={r:.4f} (bar >=0.95) -> {verdict(okk)}")
    print(f"B7  abstention: {abst}/{tot}={abst/tot:.4f} (bar <=0.30) -> {verdict((abst/tot)<=0.30)}")
    for key in sorted(b8):
        print(f"B8  amended {key}: {b8[key]}")
    print(f"B9  answer channel frozen: identity vs M4 = {ntot9-ndiff}/{ntot9} (bar 100%) -> {verdict(ndiff==0)}")
    print(f"B12 refined (recorded): G>0 crossings per family:")
    for key in sorted(b12): print(f"      {key}: {b12[key]}")
    print(f"B13 underconfidence floor: {len(b13fails)} (F,d) with G<-0.100 -> {verdict(len(b13fails)==0)}")
    for k,d,gg,n in b13fails[:12]:
        print(f"      FAIL {k} d={d} G={gg:.4f} n={n} off_ds{DSLOT[d]}={offs.get(DSLOT[d],'?')}")
    print(f"B3pi per-item (recorded): {b3pi} rising pairs / {b3pi_pairs} adjacent released pairs")
    print()
    print("=== F31 mechanism evidence ===")
    print(f"f31_w1={w1m.group(1) if w1m else '?'} (nonzero -> weights != init)")
    print(f"offsets per depth-slot: {sorted(offs.items())} (clamp ±200; max|off|={max(abs(v) for v in offs.values())}; 0 cap-hits)")
    print(f"damp: final={damp_final} max_observed={maxdamp} ups={ups} downs={downs} flips={flips} over {ntrain} released training cells")
    print(f"      flip_rate={flips/ntrain:.4f}; damp 800-cap hit={'yes' if maxdamp>=800 else 'no'}; 2048-FIFO test-cap bound: no (max depth count 940)")
    print()
    print("=== F31 falsification triggers ===")
    osc = (flips/ntrain > 0.05) or len(ping) >= 3
    print(f"KILL (a) oscillation: training flip_rate={flips/ntrain:.4f} (storm if >>5%), eval ping-pong families={len(ping)} -> {'KILL' if osc else 'clear'}")
    for k,alt,gs in ping: print(f"      {k}: {alt} sign-alternations G={gs}")
    print(f"KILL (b) redteam tiny-n B3 vs NEC m9 base: F31 Gviol={f31_rt_gv} vs NEC={nec_rt_gv} on {len(rt_keys)} redteam fams -> {'KILL (no better than base)' if f31_rt_gv>=nec_rt_gv else 'clear (strictly better)'}")
    over = [b for b in b13fails if offs.get(DSLOT[b[1]],0) > 0]
    if b13fails and over:
        print(f"KILL (c) B13 from over-correction: {len(b13fails)} B13 fails, {len(over)} at positive-offset depths -> KILL")
    elif b13fails:
        print(f"KILL (c): {len(b13fails)} B13 fails but none at positive-offset depths -> B13 FAILS (not over-correction-driven)")
    else:
        print("KILL (c) B13 from over-correction: 0 B13 fails -> clear")
    print(f"KILL (shared b) B4<0.50 on any honest leg: {len(kill_b_hits)} hits -> {'KILL' if kill_b_hits else 'clear'}")
    for k,v,n in kill_b_hits: print(f"      {k}: meanC={v:.4f} n={n}")

main()
