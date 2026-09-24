#!/usr/bin/env python3
"""T-05 kill-bar + guard analysis (PREREG_T05.md §3/§6, pure-form v2).
TSV cols: id depth t rounds consumed ne release correct conf leader_idx cert
Usage: analyze_t05.py <results_dir> <v2_analysis_dir> <features.tsv>
"""
import sys, os, glob
from collections import defaultdict

RES, V2A, FEAT = sys.argv[1], sys.argv[2], sys.argv[3]
DEPTHS = {"admit": [1,2,4,8,16], "logic": [1,2,4,8,16], "trap": [1,2,4,8,16],
          "ceiling": [1,2,4,8,16,32,64]}

def family_of(battery, iid):
    if battery == "ceiling":
        parts = iid.split("-")
        if len(parts) >= 2 and parts[0] == "H5B":
            return parts[1]
    return battery

def load_t05():
    # data[arm][scale][battery][fam][iid][depth] = (correct, conf, release)
    data = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))))
    for arm in ("W", "L"):
        for scale in ("100x", "10x"):
            for battery, depths in DEPTHS.items():
                for d in depths:
                    pat = os.path.join(RES, f"{battery}_t05{arm}_{scale}_d{d}_A.tsv")
                    for fn in glob.glob(pat):
                        for line in open(fn):
                            line = line.rstrip("\n")
                            if not line: continue
                            c = line.split("\t")
                            fam = family_of(battery, c[0])
                            data[arm][scale][battery][fam][c[0]][int(c[1])] = (c[7], int(c[8]), c[6])
    return data

def load_v2_ref():
    # ref[mech][battery][fam][iid][depth] = (correct, conf)  (A-legs only)
    ref = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(dict))))
    for mech in (4, 14):
        for battery, depths in DEPTHS.items():
            for d in depths:
                pat = os.path.join(V2A, f"{battery}_m{mech}_d{d}_A.tsv")
                for fn in glob.glob(pat):
                    for line in open(fn):
                        line = line.rstrip("\n")
                        if not line: continue
                        c = line.split("\t")
                        fam = family_of(battery, c[0])
                        ref[mech][battery][fam][c[0]][int(c[1])] = (c[7], int(c[8]))
    return ref

def g_curve(items):
    # items: {iid: {depth: (correct, conf, release)}} -> {depth: (G, n)}
    by_d = defaultdict(list)
    for iid, dd in items.items():
        for d, (corr, conf, rel) in dd.items():
            if corr in ("1", "0"):
                by_d[d].append((corr, conf))
    out = {}
    for d in sorted(by_d):
        cells = by_d[d]
        mc = sum(f for _, f in cells)/len(cells)/1000.0
        acc = sum(1 for c, _ in cells if c == "1")/len(cells)
        out[d] = (mc - acc, len(cells))
    return out

def v_counts(items):
    v1 = v1o = v2 = v2o = n10 = 0
    for iid, dd in items.items():
        ds = sorted(dd)
        for i in range(len(ds)-1):
            c0, f0, _ = dd[ds[i]]; c1, f1, _ = dd[ds[i+1]]
            if c0 == "1" and c1 == "0":
                n10 += 1
                v1o += 1
                if f1 >= f0: v1 += 1
            if c0 == "0" and c1 == "0":
                v2o += 1
                if f1 > f0: v2 += 1
    return v1, v1o, v2, v2o, n10

def mean_conf(items, corr_want):
    fs = [f for dd in items.values() for (c, f, _) in dd.values() if c == corr_want]
    return (sum(fs)/len(fs), len(fs)) if fs else (None, 0)

data = load_t05(); ref = load_v2_ref()

print("="*70); print("T-05 KILL-BAR EVALUATION (100x, strict primary)")
print("="*70)
for arm in ("W", "L"):
    cel = data[arm]["100x"]["ceiling"]
    for fam in ("O", "P"):
        items = cel.get(fam, {})
        g = g_curve(items); v1, v1o, v2, v2o, n10 = v_counts(items)
        g64, n64 = g.get(64, (None, 0))
        v2pct = 100.0*v2/v2o if v2o else 0
        # refined: zero-crossings
        zc = 0; prev = None
        for d in sorted(g):
            if g[d][0] is None: continue
            if prev is not None and ((prev <= 0) != (g[d][0] <= 0)) and prev != g[d][0]: zc += 1
            prev = g[d][0]
        print(f"arm {arm} family {fam}: n={len(items)}")
        print(f"  G curve: " + " ".join(f"d{d}:{g[d][0]:+.3f}" for d in sorted(g)))
        g64s = f"{g64:+.3f}" if g64 is not None else "UNDEF(n=0)"
        print(f"  G(64)={g64s} (n={n64}) | V1={v1}/{v1o} V2={v2}/{v2o} ({v2pct:.1f}%) | zero-crossings={zc}")
print()
print("KILL-BAR VERDICTS (literal; O-battery vacuity documented below):")
oW = data["W"]["100x"]["ceiling"].get("O", {}); oL = data["L"]["100x"]["ceiling"].get("O", {})
gW = g_curve(oW); gL = g_curve(oL)
_, _, v2W, v2oW, _ = v_counts(oW)
g64W = gW.get(64, (None, 0))[0]; v2pctW = 100.0*v2W/v2oW if v2oW else 0.0
g64L = gL.get(64, (None, 0))[0]
def f3(x): return f"{x:+.3f}" if x is not None else "UNDEF"
print(f"  worst-case arm: O G(64)={f3(g64W)} (kill if >0.1) -> {'KILLED' if (g64W is not None and g64W>0.1) else 'NOT TRIGGERED'}")
print(f"  worst-case arm: O V2={v2pctW:.1f}% (kill if >5%) -> {'KILLED' if v2pctW>5 else 'NOT TRIGGERED'}")
print(f"  'only worst-case' clause: control O G(64)={f3(g64L)} (kill clause if <=0)")
print(f"    -> literal reading: {'CLAUSE KILLED' if (g64L is not None and g64L<=0) else 'not triggered'}; substantive reading in verdict")
print()
print("SUBSTANCE CHECK on P (wrong released cells live here):")
for arm in ("W", "L"):
    p = data[arm]["100x"]["ceiling"].get("P", {})
    gp = g_curve(p); v1, v1o, v2, v2o, n10 = v_counts(p)
    print(f"  arm {arm} P: " + " ".join(f"d{d}:{gp[d][0]:+.3f}" for d in sorted(gp)))
    print(f"    V1={v1}/{v1o} V2={v2}/{v2o} 1->0 transitions={n10}")
print()
print("="*70); print("PREDICTED OBSERVABLES (§5)")
print("="*70)
for arm in ("W", "L"):
    cel = data[arm]["100x"]["ceiling"]
    o = cel.get("O", {})
    for d in (32, 64):
        fs = [f for dd in o.values() if d in dd for (c, f, _) in [dd[d]]]
        print(f"  arm {arm} O d{d}: mean c = {sum(fs)/len(fs):.0f} (n={len(fs)})")
print()
print("="*70); print("NON-DEGENERACY GUARDS D1-D3 (100x)")
print("="*70)
for arm in ("W", "L"):
    lg = data[arm]["100x"]["logic"].get("logic", {})
    ad = data[arm]["100x"]["admit"].get("admit", {})
    mcC, nC = mean_conf(lg, "1"); mcW, nW = mean_conf(lg, "0")
    sep = (mcC - mcW) if (mcC is not None and mcW is not None) else None
    seps = f"{sep:.0f}" if sep is not None else "n/a(no wrong logic cells)"
    # D2 collapse vs v2-100x (mech 14)
    lg14 = ref[14]["logic"].get("logic", {}); ad14 = ref[14]["admit"].get("admit", {})
    def mc_ref(items, cw):
        fs = [f for dd in items.values() for (c, f) in dd.values() if c == cw]
        return (sum(fs)/len(fs), len(fs)) if fs else (None, 0)
    mcC14, _ = mc_ref(lg14, "1")
    adC, _ = mean_conf(ad, "1"); adC14, _ = mc_ref(ad14, "1")
    coll_lg = (mcC14 - mcC)/mcC14 if mcC14 else 0
    coll_ad = (adC14 - adC)/adC14 if adC14 else 0
    # D3 answer-channel: disagreement vs M4 (mech 4) on all legs
    disag = 0; total = 0
    for battery in DEPTHS:
        for fam, items in data[arm]["100x"][battery].items():
            ritems = ref[4][battery].get(fam, {})
            for iid, dd in items.items():
                if iid in ritems:
                    for d, (c, f, _) in dd.items():
                        if d in ritems[iid]:
                            total += 1
                            if c != ritems[iid][d][0]: disag += 1
    print(f"arm {arm}: D1 logic correct mean c = {mcC:.0f} (bar >=500) -> {'PASS' if mcC>=500 else 'FAIL'}")
    print(f"        D2 logic C-W separation = {seps} (bar >=200) -> {'PASS' if (sep is not None and sep>=200) else 'FAIL'}")
    print(f"        D2 collapse vs v2-100x: logic {coll_lg*100:.0f}% (bar <50%), admit {coll_ad*100:.0f}% (bar <50%) -> {'PASS' if coll_lg<0.5 and coll_ad<0.5 else 'FAIL'}")
    print(f"        D3 answer-channel disagreements vs M4: {disag}/{total} -> {'PASS' if disag==0 else 'FAIL'}")
