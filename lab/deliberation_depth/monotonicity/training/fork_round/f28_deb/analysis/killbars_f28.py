#!/usr/bin/env python3
"""Kill-bar table for F28 DEB (PREREG_FORKROUND.md §4; B8 amended §4b).

Reads results/<battery>_m28_d<depth>_A.tsv (F28 legs) and *_m4_d*_[AB].tsv
(M4 reference). NEC m9 legs (2nd arg) for delta-vs-NEC reporting.
Probe TSVs (3rd arg, from probe_f28: id depth t nh budget margin_t rounds)
for kill-bar (b) budget-pinning measurement.

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

F28 falsification triggers (task brief; prereg §3 "Kill: B3 no better than
NEC (structurally blind to FM6)"):
  (a) strict B3 no better than NEC m9 -> KILL, failure mode (6)
  (b) clamp attractor: budget pins at 0/1000 on >50% of cells in ANY leg
      -> KILL, failure mode (1)
  (c) B4 < 0.50 on honest families -> KILL
"""
import sys, os, glob, math
from collections import defaultdict

BATTERY_DEPTHS = {"admit":[1,2,4,8,16],"revoke":[1,2,4,8,16],"logic":[1,2,4,8,16],
                  "trap":[1,2,4,8,16],"cost":[1,2,4,8,16],"redteam":[1,2,4,8,16],
                  "ceiling":[1,2,4,8,16,32,64]}
HONEST = {"admit","revoke","logic","cost"}
MECH = "28"

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

def gviol_of(data):
    """per (battery,fam): (gviol, {d:G}, {d:n_rel}) — frozen analyzer semantics."""
    out = {}
    for battery in data:
        for fam in data[battery]:
            key = (battery, fam)
            cb = defaultdict(list)
            for iid, dd in data[battery][fam].items():
                for d, (c, f, _) in dd.items():
                    if c in ("1","0"): cb[d].append((c,f))
            g = {}; nrel = {}
            for d, cl in sorted(cb.items()):
                nrel[d] = len(cl)
                if len(cl) >= 1:
                    g[d] = (sum(f for _,f in cl)/len(cl)/1000.0
                            - sum(1 for c,_ in cl if c=="1")/len(cl))
            gv = sum(1 for i in range(len(sorted(g))-1)
                     if g[sorted(g)[i+1]] > g[sorted(g)[i]] + 1e-12)
            out[key] = (gv, g, nrel)
    return out

def load_probe(probedir):
    """probe TSVs: id depth t nh budget margin_t rounds -> per (battery,depth): pin fractions."""
    pin = {}
    for battery, depths in BATTERY_DEPTHS.items():
        for d in depths:
            pat = os.path.join(probedir, f"{battery}_d{d}.tsv")
            for fn in glob.glob(pat):
                n = n0 = n1000 = 0
                with open(fn) as f:
                    for line in f:
                        line = line.rstrip("\n")
                        if not line: continue
                        c = line.split("\t")
                        b = int(c[4])
                        n += 1
                        if b == 0: n0 += 1
                        if b == 1000: n1000 += 1
                pin[(battery, d)] = (n, n0, n1000)
    return pin

def main():
    resdir = sys.argv[1]
    necdir = sys.argv[2] if len(sys.argv) > 2 else None
    probedir = sys.argv[3] if len(sys.argv) > 3 else None
    f28 = load_mech(resdir, MECH)
    m4 = load_mech(resdir, "4")
    nec = load_mech(necdir, "9") if necdir else None

    R = {"B1_n10":0,"B2_v1":0,"B2_v2":0}
    cells = defaultdict(lambda: defaultdict(list))
    m4cells = defaultdict(lambda: defaultdict(list))
    seqs = defaultdict(lambda: defaultdict(dict))
    for battery in f28:
        for fam in f28[battery]:
            key = (battery, fam)
            for iid, dd in f28[battery][fam].items():
                seqs[key][iid] = dd
                for d, (c, f, _) in dd.items():
                    cells[key][d].append((c, f, iid))
    for battery in m4:
        for fam in m4[battery]:
            key = (battery, fam)
            for iid, dd in m4[battery][fam].items():
                for d, (c, f, _) in dd.items():
                    m4cells[key][d].append((c, f, iid))

    # B1/B2 per family (frozen analyzer semantics)
    for key in sorted(seqs):
        for iid, dd in seqs[key].items():
            s = sorted(dd.items())
            for i in range(len(s)-1):
                d0,(c0,f0,_) = s[i]; d1,(c1,f1,_) = s[i+1]
                if c0=="1" and c1=="0":
                    R["B1_n10"] += 1
                    if f1 >= f0: R["B2_v1"] += 1
                if c0=="0" and c1=="0" and f1 > f0: R["B2_v2"] += 1

    gviol_fam = gviol_of(f28)
    nec_gviol = gviol_of(nec) if nec else {}
    R["B3_gviol"] = sum(gv for gv,_,_ in gviol_fam.values())
    nec_tot = sum(gv for gv,_,_ in nec_gviol.values()) if nec else None

    # aggregate conf stats
    allC = []; allW = []
    fam_mc = {}; hon_mc = {}
    abst = 0; tot = 0
    for key in sorted(cells):
        ccs = [f for cl in cells[key].values() for (c,f,_) in cl if c=="1"]
        wws = [f for cl in cells[key].values() for (c,f,_) in cl if c=="0"]
        allC += ccs; allW += wws
        fam_mc[key] = (sum(ccs)/len(ccs)/1000.0 if ccs else float("nan"), len(ccs))
        if key[1] in HONEST and len(ccs) >= 10:
            hon_mc[key] = fam_mc[key]
        for cl in cells[key].values():
            for (c,f,_) in cl:
                tot += 1
                if c == "A": abst += 1
    mcC = sum(allC)/len(allC)/1000.0 if allC else float("nan")
    mcW = sum(allW)/len(allW)/1000.0 if allW else float("nan")
    kill_c_hits = [(k, v, n) for k,(v,n) in hon_mc.items() if v < 0.50]
    # B6
    b6 = {}
    for battery in f28:
        for fam in f28[battery]:
            key=(battery,fam)
            na = sum(1 for dd in f28[battery][fam].values() for (c,_,_) in dd.values() if c=="1")
            nm = sum(1 for dd in m4.get(battery,{}).get(fam,{}).values() for (c,_,_) in dd.values() if c=="1")
            b6[key] = (na/nm if nm else float("nan"), na, nm)
    # B9
    ndiff = ntot9 = 0
    for battery in f28:
        for fam in f28[battery]:
            for iid, dd in f28[battery][fam].items():
                rdd = m4.get(battery,{}).get(fam,{}).get(iid,{})
                for d,(c,f,rel) in dd.items():
                    if d in rdd:
                        ntot9 += 1
                        if rel != rdd[d][2] or c != rdd[d][0]: ndiff += 1
    # B8 amended §4b
    b8 = {}
    for key,(gv,g,nrel_d) in gviol_fam.items():
        battery,_ = key
        need = 5 if battery=="ceiling" else 4
        feas = [d for d,cl in sorted(m4cells[key].items())
                if sum(1 for (c,f,_) in cl if c in ("1","0")) >= 10]
        defined = [d for d in feas if nrel_d.get(d,0) >= 1]
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
    # B12
    b12 = {key: sum(1 for v in g.values() if v > 0) for key,(gv,g,_) in gviol_fam.items()}
    # B13
    b13fails = []
    for key in sorted(cells):
        for d, cl in sorted(cells[key].items()):
            rel = [(c,f) for c,f,_ in cl if c in ("1","0")]
            if len(rel) >= 8:
                gg = (sum(f for _,f in rel)/len(rel)/1000.0
                      - sum(1 for c,_ in rel if c=="1")/len(rel))
                if gg < -0.100 - 1e-12: b13fails.append((key,d,gg,len(rel)))
    # B3pi (recorded)
    b3pi = 0; b3pi_pairs = 0
    for key in seqs:
        for iid, dd in seqs[key].items():
            s = sorted(dd.items())
            for i in range(len(s)-1):
                d0,(c0,f0,_) = s[i]; d1,(c1,f1,_) = s[i+1]
                if c0 in ("1","0") and c1 in ("1","0"):
                    b3pi_pairs += 1
                    if (f1/1000.0-(1 if c1=="1" else 0)) > (f0/1000.0-(1 if c0=="1" else 0)) + 1e-12:
                        b3pi += 1
    # Kill (b): budget pinning from probe
    pin = load_probe(probedir) if probedir else {}
    kill_b_hits = [(k, n, n0, n1000) for k,(n,n0,n1000) in pin.items()
                   if n > 0 and (n0+n1000)/n > 0.50]

    def verdict(ok): return "PASS" if ok else "FAIL"
    print("=== F28 DEB kill-bar table (PREREG_FORKROUND.md §4; B8 amended §4b) — mech 28 ===")
    ok = R["B1_n10"]==0; print(f"B1  accuracy: 1->0 = {R['B1_n10']} (bar =0) -> {verdict(ok)}")
    ok = R["B2_v1"]==0 and R["B2_v2"]==0; print(f"B2  theater: V1={R['B2_v1']} V2={R['B2_v2']} (bar =0) -> {verdict(ok)}")
    ok = R["B3_gviol"]==0; print(f"B3  law(strict): G-violations total = {R['B3_gviol']} (bar =0 every family) -> {verdict(ok)}")
    for key in sorted(gviol_fam):
        gv,g,nr = gviol_fam[key]
        gs=",".join(f"{d}:{g[d]:+.3f}(n={nr[d]})" for d in sorted(g))
        ng = f" vs NEC m9 Gviol={nec_gviol.get(key,('?'))[0]}" if nec else ""
        print(f"      {key}: Gviol={gv}{ng} G={gs if gs else 'n/a'}")
    ok = mcC>=0.50; print(f"B4  non-degenerate: meanConfCorrect={mcC:.4f} n={len(allC)} (bar >=0.50) -> {verdict(ok)}")
    for key in sorted(fam_mc):
        if key[1] in HONEST:
            v,n = fam_mc[key]; okk = (v>=0.50) if n>=10 else True
            tag = "n<10:exempt" if n<10 else ""
            print(f"B4b honest {key}: meanC_correct={v:.4f} n={n} (bar >=0.50, n>=10) -> {verdict(ok)} {tag}")
    ok = (mcC-mcW)>=0.20; print(f"B5  separation: {mcC:.4f}-{mcW:.4f}={mcC-mcW:.4f} (bar >=0.20) -> {verdict(ok)}")
    b6ok=True
    for key in sorted(b6):
        r,na,nm = b6[key]
        if math.isnan(r):
            print(f"B6  recall {key}: {na}/{nm}=nan (M4 releases none correct; B9-identical -> VACUOUS PASS)")
            continue
        okk = r>=0.95; b6ok = b6ok and okk
        print(f"B6  recall {key}: {na}/{nm}={r:.4f} (bar >=0.95) -> {verdict(okk)}")
    ok = (abst/tot)<=0.30; print(f"B7  abstention: {abst}/{tot}={abst/tot:.4f} (bar <=0.30) -> {verdict(ok)}")
    for key in sorted(b8):
        print(f"B8  amended {key}: {b8[key]}")
    ok = ndiff==0; print(f"B9  answer channel frozen: identity vs M4 = {ntot9-ndiff}/{ntot9} (bar 100%) -> {verdict(ok)}")
    print(f"B12 refined (recorded): G>0 crossings per family:")
    for key in sorted(b12): print(f"      {key}: {b12[key]}")
    ok = len(b13fails)==0; print(f"B13 underconfidence floor: {len(b13fails)} (F,d) with G<-0.100 -> {verdict(ok)}")
    for k,d,gg,n in b13fails[:12]: print(f"      FAIL {k} d={d} G={gg:.4f} n={n}")
    print(f"B3pi per-item (recorded): {b3pi} rising pairs / {b3pi_pairs} adjacent released pairs")
    print()
    print("=== F28 falsification triggers ===")
    nb = (R["B3_gviol"] >= nec_tot) if nec_tot is not None else None
    print(f"KILL (a) strict B3 no better than NEC m9: F28 Gviol={R['B3_gviol']} vs NEC m9 Gviol={nec_tot} -> {'KILL' if nb else 'clear'}")
    print(f"KILL (b) clamp attractor: budget pinned at 0/1000 on >50% cells in any leg: {len(kill_b_hits)} legs -> {'KILL' if kill_b_hits else 'clear'}")
    for k,n,n0,n1000 in sorted(kill_b_hits)[:40]:
        print(f"      {k}: pinned {(n0+n1000)}/{n}={((n0+n1000)/n):.3f} (0:{n0} 1000:{n1000})")
    if len(kill_b_hits) > 40: print(f"      ... and {len(kill_b_hits)-40} more")
    print(f"KILL (c) B4<0.50 on honest families (n>=10): {len(kill_c_hits)} hits -> {'KILL' if kill_c_hits else 'clear'}")
    for k,v,n in kill_c_hits: print(f"      {k}: meanC={v:.4f} n={n}")

main()
