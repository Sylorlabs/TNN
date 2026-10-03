#!/usr/bin/env python3
"""WC kill-bar evaluator (SR round, PREREG_SR §10).

Imports the FROZEN analyzer (training/analyze.py) as a module — its
load()/g_curve()/metrics_for_cells() are the only measurement code.
WC TSVs are exposed to it via _m9_ symlinks (mech id 9); M4 reference
TSVs are the frozen _m4_ copies.

Kill bars evaluated: B1,B2,B3,B4,B4b,B5,B6,B7,B8,B9,B12(record),B13.
Thresholds exact per PREREG_SR §10 (FROZEN v1).
"""

import os
import sys
from collections import defaultdict

ANALYZER = os.path.expanduser(
    "~/workspace/tnn-lab/deliberation_depth/monotonicity/training/analyze.py")
WCDIR = os.path.expanduser(
    "~/workspace/tnn-lab/deliberation_depth/monotonicity/training/sr_round/wc")
MECH = 9

srctext = open(ANALYZER).read()
# the frozen analyzer calls main() at module bottom; strip it so import is safe
srctext = srctext.replace("\nmain()\n", "\n")
import types
fa = types.ModuleType("frozen_analyzer")
exec(compile(srctext, ANALYZER, "exec"), fa.__dict__)

LINKDIR = os.path.join(WCDIR, "analysis", "eval_m9")
os.makedirs(LINKDIR, exist_ok=True)
RES = os.path.join(WCDIR, "results")
for fn in os.listdir(RES):
    if "_wc_" in fn:
        os.symlink(os.path.join(RES, fn),
                   os.path.join(LINKDIR, fn.replace("_wc_", "_m9_")))
    elif "_m4_" in fn:
        dst = os.path.join(LINKDIR, fn)
        if not os.path.exists(dst):
            os.symlink(os.path.join(RES, fn), dst)

data = fa.load(LINKDIR, [MECH, 4])
wc = data[MECH]
m4 = data[4]

HONEST = {"admit", "revoke", "logic", "cost"}

def iter_cells():
    for battery in wc:
        for fam in wc[battery]:
            for iid, dd in wc[battery][fam].items():
                for d, (c, f, rel) in dd.items():
                    yield battery, fam, iid, d, c, f, rel

# --- aggregates ---
rel_corr_conf = []   # (fam, conf) released correct
rel_wrong_conf = []  # (fam, conf) released wrong
n_abst = 0; n_tot = 0
fam_relcorr = defaultdict(list)
for battery, fam, iid, d, c, f, rel in iter_cells():
    n_tot += 1
    if c == "A":
        n_abst += 1
        continue
    if c == "1":
        rel_corr_conf.append((fam, f)); fam_relcorr[fam].append(f)
    elif c == "0":
        rel_wrong_conf.append((fam, f))

mcC = sum(f for _, f in rel_corr_conf) / len(rel_corr_conf) / 1000.0
mcW = sum(f for _, f in rel_wrong_conf) / len(rel_wrong_conf) / 1000.0

# --- per-family metrics: n10, V1, V2, G curve ---
bars = {}
famstat = {}
tot_n10 = tot_v1 = tot_v2 = tot_gviol = 0
for battery in sorted(wc):
    for fam in sorted(wc[battery]):
        items = wc[battery][fam]
        m = defaultdict(int)
        cells_by_depth = defaultdict(list)
        for iid, dd in items.items():
            seq = sorted(dd.items())
            sm = fa.metrics_for_cells([(d, c, f) for d, (c, f, _) in seq])
            for k, v in sm.items():
                m[k] += v
            for d, (c, f, _) in seq:
                cells_by_depth[d].append((c, f))
        g = fa.g_curve(cells_by_depth)
        gviol = sum(1 for i in range(len(sorted(g)) - 1)
                    if g[sorted(g)[i]] is not None and g[sorted(g)[i+1]] is not None
                    and g[sorted(g)[i+1]] > g[sorted(g)[i]] + 1e-12)
        tot_n10 += m["n10"]; tot_v1 += m["v1"]; tot_v2 += m["v2"]; tot_gviol += gviol
        defined = {d: gv for d, gv in g.items() if gv is not None}
        famstat[(battery, fam)] = dict(m=m, g=g, gviol=gviol, defined=defined)

# --- B9: release+correct identity vs M4 ---
diff = 0; n = 0
for battery in wc:
    for fam in wc[battery]:
        for iid, dd in wc[battery][fam].items():
            rdd = m4[battery][fam].get(iid, {})
            for d, (c, f, rel) in dd.items():
                if d in rdd:
                    n += 1
                    if rel != rdd[d][2] or c != rdd[d][0]:
                        diff += 1

# --- B6: released-correct ratio vs M4 per family ---
def relcorr_count(dset):
    out = defaultdict(int)
    for battery in dset:
        for fam in dset[battery]:
            for iid, dd in dset[battery][fam].items():
                for d, (c, f, rel) in dd.items():
                    if c == "1":
                        out[fam] += 1
    return out
wc_rc = relcorr_count(wc); m4_rc = relcorr_count(m4)
b6 = {fam: (wc_rc[fam] / m4_rc[fam] if m4_rc[fam] else float("nan"))
      for fam in set(wc_rc) | set(m4_rc)}

# --- B8: G-flatness ---
def b8_pass():
    for (battery, fam), st in famstat.items():
        ds = sorted(st["g"].keys())
        ndef = sum(1 for d in ds if st["g"][d] is not None)
        need = 5 if len(ds) == 7 else 4
        if ndef < need:
            return False, f"{battery}/{fam}: defined {ndef} < {need}"
        vals = [st["g"][d] for d in ds if st["g"][d] is not None]
        if max(vals) - min(vals) < 1e-3:
            return False, f"{battery}/{fam}: G flat within 1e-3"
    return True, "all families defined+varying"

# --- B13: underconfidence floor ---
def b13_worst():
    worst = 0.0; where = None
    for (battery, fam), st in famstat.items():
        for d, gv in st["g"].items():
            # n_rel >= 8 check via raw cells
            nrel = sum(1 for iid, dd in wc[battery][fam].items()
                       for ddpt, (c, f, rel) in dd.items()
                       if ddpt == d and c in ("1", "0"))
            if nrel >= 8 and gv < worst:
                worst = gv; where = f"{battery}/{fam} d{d} nrel={nrel}"
    return worst, where

worst_g13, where_g13 = b13_worst()

# --- B12 refined: G>0 crossings ---
gpos = []
for (battery, fam), st in famstat.items():
    for d, gv in sorted(st["defined"].items()):
        if gv > 0:
            gpos.append((battery, fam, d, gv))

print("=== WC kill-bar evaluation (PREREG_SR §10, FROZEN v1) ===")
print(f"B1  §1 accuracy (1->0 transitions = 0):            {tot_n10}  "
      + ("PASS" if tot_n10 == 0 else "FAIL"))
print(f"B2  theater (V1=0 and V2=0):                       V1={tot_v1} V2={tot_v2}  "
      + ("PASS" if tot_v1 == 0 and tot_v2 == 0 else "FAIL"))
print(f"B3  law strict (G-violations per family = 0):       {tot_gviol}  "
      + ("PASS" if tot_gviol == 0 else "FAIL"))
print(f"B4  non-degenerate (meanConfCorrect >= 0.50):       {mcC:.4f}  "
      + ("PASS" if mcC >= 0.50 else "FAIL"))
b4b_ok = True
for fam in sorted(HONEST):
    vals = fam_relcorr.get(fam, [])
    if len(vals) >= 10:
        mv = sum(vals) / len(vals) / 1000.0
        ok = mv >= 0.50
        b4b_ok = b4b_ok and ok
        print(f"B4b honest-family floor {fam}: n={len(vals)} meanC={mv:.4f}  "
              + ("PASS" if ok else "FAIL"))
    else:
        print(f"B4b honest-family floor {fam}: n={len(vals)} < 10 (no floor)")
print(f"B4b overall: " + ("PASS" if b4b_ok else "FAIL"))
print(f"B5  separation (mcC-mcW >= 0.20):                  {mcC-mcW:.4f}  "
      + ("PASS" if mcC - mcW >= 0.20 else "FAIL"))
b6_ok = all(v >= 0.95 for v in b6.values())
for fam in sorted(b6):
    print(f"B6  recall {fam}: wc={wc_rc[fam]} m4={m4_rc[fam]} ratio={b6[fam]:.4f}  "
          + ("PASS" if b6[fam] >= 0.95 else "FAIL"))
print(f"B6 overall: " + ("PASS" if b6_ok else "FAIL"))
abst = n_abst / n_tot
print(f"B7  abstention volume (<= 0.30):                   {abst:.4f} (n={n_abst}/{n_tot})  "
      + ("PASS" if abst <= 0.30 else "FAIL"))
ok8, msg8 = b8_pass()
print(f"B8  G-flatness:                                    {msg8}  "
      + ("PASS" if ok8 else "FAIL"))
print(f"B9  answer channel frozen (identity vs M4 = 100%): {n-diff}/{n}  "
      + ("PASS" if diff == 0 else "FAIL"))
print(f"B12 refined (G>0 crossings, recorded):             {len(gpos)} crossings")
for bp, fp, d, gv in gpos[:20]:
    print(f"      {bp}/{fp} d{d}: G={gv:+.4f}")
print(f"B13 underconfidence floor (G >= -0.100):           worst {worst_g13:+.4f} at {where_g13}  "
      + ("PASS" if worst_g13 >= -0.100 else "FAIL"))
print()
print("per-family detail (n10 V1 V2 Gviol):")
for (battery, fam) in sorted(famstat):
    st = famstat[(battery, fam)]
    gstr = ",".join(f"{d}:{st['g'][d]:+.3f}" if st['g'][d] is not None else f"{d}:n/a"
                    for d in sorted(st["g"]))
    print(f"  {battery}/{fam}: 1->0={st['m']['n10']} V1={st['m']['v1']} V2={st['m']['v2']} "
          f"Gviol={st['gviol']} G=[{gstr}]")
