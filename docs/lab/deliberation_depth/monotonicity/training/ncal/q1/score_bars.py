#!/usr/bin/env python3
"""Full-bar scorer for NEC Q1 / B9X2 leg TSVs.

Reads 11-col leg files {battery}_m{mech}_d{depth}_{A,B,C}.tsv from a results dir
and computes the frozen bar set:
  B1  accuracy: 1->0 transitions == 0
  B2  theater: V1 == 0 and V2 == 0 (non-negotiable)
  B3  law (strict): G-violations per family == 0 (rise > 1e-12)
  B4  non-degenerate: meanConfCorrect (aggregate) >= 0.50
  B5  separation: meanConfCorrect - meanConfWrong >= 0.20
  B6  recall: released-correct / M4 released-correct per family >= 0.95
  B7  abstention volume: abstained / total cells (aggregate) <= 0.30
  B8  G-flatness (defective as frozen; computed, reported, NOT gated):
      G defined (>=10 released) on >=4/5 slots (5-depth) / >=5/7 (ceiling);
      not all slot G values equal within 1e-3. Matrix-limited fams excluded.
  B13 underconfidence floor: per (family,depth) with n_rel >= 8: G >= -0.100
Also reports: redteam Gviol, ceiling/O Gviol, TOTAL Gviol.

Usage: score_bars.py <results_dir> <mech_id> [ref_mech_id] [run]
  ref_mech_id defaults to 11 (m11 = frozen M4 release baseline for B6).
  run defaults to A.

Exit 0. Prints a one-row table plus per-family detail.
"""
import sys, os, glob
from collections import defaultdict

BATTERY_DEPTHS = {
    "admit": [1,2,4,8,16], "revoke": [1,2,4,8,16], "logic": [1,2,4,8,16],
    "trap": [1,2,4,8,16], "cost": [1,2,4,8,16], "redteam": [1,2,4,8,16],
    "ceiling": [1,2,4,8,16,32,64],
}

def family_of(battery, item_id):
    if battery == "ceiling":
        parts = item_id.split("-")
        if len(parts) >= 2 and parts[0] == "H5B":
            return parts[1]
        return "ceiling?"
    return battery

def load(results_dir, mech, run):
    # data[battery][family][item][depth] = (correct, conf) ; correct in 1/0/A
    data = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
    for battery, depths in BATTERY_DEPTHS.items():
        for d in depths:
            pat = os.path.join(results_dir, f"{battery}_m{mech}_d{d}_{run}.tsv")
            for fn in glob.glob(pat):
                with open(fn) as f:
                    for line in f:
                        line = line.rstrip("\n")
                        if not line:
                            continue
                        cols = line.split("\t")
                        iid, depth = cols[0], int(cols[1])
                        correct, conf = cols[7], int(cols[8])
                        fam = family_of(battery, iid)
                        data[battery][fam][iid][depth] = (correct, conf)
    return data

def score(results_dir, mech, ref_mech, run, ref_dir=None):
    data = load(results_dir, mech, run)
    ref = load(ref_dir or results_dir, ref_mech, run) if ref_mech != mech else data
    per_fam = {}
    tot = defaultdict(int)
    # aggregates for B4/B5/B7
    cc_sum = cc_n = 0      # correct cells conf sum/count
    cw_sum = cw_n = 0      # wrong cells conf sum/count
    n_abst = n_tot = 0
    b13_viol = []          # list of (battery, family, depth, G)
    for battery in sorted(data.keys()):
        nslots_need = 5 if battery == "ceiling" else 4
        for fam in sorted(data[battery].keys()):
            items = data[battery][fam]
            m = defaultdict(int)
            cells_by_depth = defaultdict(list)
            nrel = defaultdict(int)
            g = {}
            for iid, dd in items.items():
                seq = sorted(dd.items())
                for i in range(len(seq) - 1):
                    (d0, (c0, f0)), (d1, (c1, f1)) = seq[i], seq[i+1]
                    if c0 == "1" and c1 == "0":
                        m["n10"] += 1
                    if c0 == "A" and c1 == "0":
                        m["a0"] += 1
                    if c0 == "1" and c1 == "0" and f1 >= f0:
                        m["v1"] += 1
                    if c0 == "0" and c1 == "0" and f1 > f0:
                        m["v2"] += 1
                for d, (c, f) in seq:
                    n_tot += 1
                    if c == "A":
                        n_abst += 1
                    else:
                        cells_by_depth[d].append((c, f))
                        nrel[d] += 1
                        if c == "1":
                            cc_sum += f; cc_n += 1
                        else:
                            cw_sum += f; cw_n += 1
            for d in sorted(cells_by_depth):
                cells = cells_by_depth[d]
                if not cells:
                    g[d] = None
                    continue
                mean_conf = sum(f for _, f in cells) / len(cells) / 1000.0
                acc = sum(1 for c, _ in cells if c == "1") / len(cells)
                g[d] = mean_conf - acc
            gviol = 0
            ds = sorted(g.keys())
            for i in range(len(ds) - 1):
                if g[ds[i]] is not None and g[ds[i+1]] is not None:
                    if g[ds[i+1]] > g[ds[i]] + 1e-12:
                        gviol += 1
            for d in ds:
                if nrel[d] >= 8 and g[d] is not None and g[d] < -0.100:
                    b13_viol.append((battery, fam, d, g[d]))
            # B6: released-correct / M4 released-correct (summed over depths)
            relcorr = sum(1 for iid, dd in items.items()
                          for d, (c, f) in dd.items() if c == "1")
            ritems = ref.get(battery, {}).get(fam, {})
            refcorr = sum(1 for iid, dd in ritems.items()
                          for d, (c, f) in dd.items() if c == "1")
            b6 = (relcorr / refcorr) if refcorr else float("nan")
            # B8 inputs
            slots_def = sum(1 for d in ds if nrel[d] >= 10)
            gvals = [g[d] for d in ds if g[d] is not None and nrel[d] >= 10]
            tot["gviol"] += gviol
            tot["n10"] += m["n10"]; tot["a0"] += m["a0"]
            tot["v1"] += m["v1"]; tot["v2"] += m["v2"]
            per_fam[(battery, fam)] = dict(gviol=gviol, n10=m["n10"], a0=m["a0"],
                                           v1=m["v1"], v2=m["v2"], b6=b6,
                                           slots_def=slots_def,
                                           slots_need=nslots_need, gvals=gvals,
                                           n_items=len(items))
    mean_cc = cc_sum / cc_n / 1000.0 if cc_n else float("nan")
    mean_cw = cw_sum / cw_n / 1000.0 if cw_n else float("nan")
    b4 = mean_cc
    b5 = (mean_cc - mean_cw) if (cc_n and cw_n) else float("nan")
    b7 = n_abst / n_tot if n_tot else float("nan")
    # B8 per family (report only)
    b8_fails = []
    for (battery, fam), pf in per_fam.items():
        if battery == "trap":
            continue  # matrix-limited, excluded per frozen note
        if pf["slots_def"] < pf["slots_need"]:
            b8_fails.append((battery, fam, "slots"))
        elif pf["gvals"] and (max(pf["gvals"]) - min(pf["gvals"]) <= 1e-3):
            b8_fails.append((battery, fam, "flat"))
    redteam_gviol = per_fam.get(("redteam", "redteam"), {}).get("gviol", 0)
    o_gviol = per_fam.get(("ceiling", "O"), {}).get("gviol", 0)
    return {
        "mech": mech, "run": run,
        "B1_n10": tot["n10"], "B2_v1": tot["v1"], "B2_v2": tot["v2"],
        "B3_total_gviol": tot["gviol"],
        "redteam_gviol": redteam_gviol, "O_gviol": o_gviol,
        "B4_meanConfCorrect": round(b4, 4), "B5_sep": round(b5, 4),
        "B6_min": round(min(pf["b6"] for pf in per_fam.values()
                            if pf["b6"] == pf["b6"]), 4),
        "B6_by_fam": {k: round(v["b6"], 4) for k, v in per_fam.items()
                      if v["b6"] != v["b6"] or True},
        "B7_abst": round(b7, 4),
        "B8_fails": b8_fails,
        "B13_viol": len(b13_viol), "B13_cells": sorted(b13_viol),
        "per_fam_gviol": {k: v["gviol"] for k, v in per_fam.items()},
    }

def main():
    results_dir = sys.argv[1]
    mech = sys.argv[2]
    ref_mech = sys.argv[3] if len(sys.argv) > 3 else "11"
    run = sys.argv[4] if len(sys.argv) > 4 else "A"
    ref_dir = sys.argv[5] if len(sys.argv) > 5 else None
    r = score(results_dir, mech, ref_mech, run, ref_dir)
    print(f"mech={r['mech']} run={r['run']}")
    print(f"B1 n10={r['B1_n10']} | B2 V1={r['B2_v1']} V2={r['B2_v2']} | "
          f"B3 TOTAL Gviol={r['B3_total_gviol']} (redteam={r['redteam_gviol']}, O={r['O_gviol']})")
    print(f"B4 meanConfCorrect={r['B4_meanConfCorrect']} (>=0.50) | "
          f"B5 sep={r['B5_sep']} (>=0.20) | B7 abst={r['B7_abst']} (<=0.30)")
    print(f"B6 min={r['B6_min']} (>=0.95); by fam: {r['B6_by_fam']}")
    print(f"B8 fails (report-only): {r['B8_fails']}")
    print(f"B13 violations={r['B13_viol']}")
    for cell in r["B13_cells"]:
        print(f"   B13 {cell[0]}/{cell[1]} d{cell[2]} G={cell[3]:+.3f}")

if __name__ == "__main__":
    main()
