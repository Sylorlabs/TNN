#!/usr/bin/env python3
"""H5 monotonicity + L-OVERCONF metrics from mechanism TSVs.
TSV cols: id depth t rounds consumed ne release correct conf leader_idx cert
Computes per (mech, battery, family): transitions 1->0, A->0, V1, V2,
G(d) curve, accuracy(d), abstention rate, release-identity vs a reference mech.
Usage: analyze.py <results_dir> [mech_ids...]
"""
import sys, os, glob, math
from collections import defaultdict

BATTERY_DEPTHS = {
    "admit": [1,2,4,8,16], "revoke": [1,2,4,8,16], "logic": [1,2,4,8,16],
    "trap": [1,2,4,8,16], "cost": [1,2,4,8,16], "redteam": [1,2,4,8,16],
    "ceiling": [1,2,4,8,16,32,64],
}

def family_of(battery, item_id):
    if battery == "ceiling":
        # H5B-P-06-00 -> P ; H5B-O-.. -> O ; H5B-D-.. -> D
        parts = item_id.split("-")
        if len(parts) >= 2 and parts[0] == "H5B":
            return parts[1]
        return "ceiling?"
    return battery

def load(results_dir, mechs):
    # data[mech][battery][family][item] = {depth: (correct, conf, release)}
    data = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(dict))))
    for mech in mechs:
        for battery, depths in BATTERY_DEPTHS.items():
            for d in depths:
                pat = os.path.join(results_dir, f"{battery}_m{mech}_d{d}_A.tsv")
                for fn in glob.glob(pat):
                    with open(fn) as f:
                        for line in f:
                            line = line.rstrip("\n")
                            if not line:
                                continue
                            cols = line.split("\t")
                            iid, depth = cols[0], int(cols[1])
                            release, correct, conf = cols[6], cols[7], int(cols[8])
                            fam = family_of(battery, iid)
                            data[mech][battery][fam][iid][depth] = (correct, conf, release)
    return data

def metrics_for_cells(seq):
    """seq: list of (depth, correct, conf) sorted by depth. Returns dict of metrics."""
    m = {"n10": 0, "a0": 0, "v1": 0, "v2": 0}
    for i in range(len(seq) - 1):
        d0, c0, f0 = seq[i]
        d1, c1, f1 = seq[i + 1]
        if c0 == "1" and c1 == "0":
            m["n10"] += 1
        if c0 == "A" and c1 == "0":
            m["a0"] += 1
        if c0 == "1" and c1 == "0" and f1 >= f0:
            m["v1"] += 1
        if c0 == "0" and c1 == "0" and f1 > f0:
            m["v2"] += 1
    return m

def g_curve(cells_by_depth):
    """cells_by_depth: {depth: [(correct, conf), ...]} -> {depth: G or None}"""
    out = {}
    for d, cells in sorted(cells_by_depth.items()):
        rel = [(c, f) for (c, f) in cells if c in ("1", "0")]
        if not rel:
            out[d] = None
            continue
        mean_conf = sum(f for _, f in rel) / len(rel) / 1000.0
        acc = sum(1 for c, _ in rel if c == "1") / len(rel)
        out[d] = mean_conf - acc
    return out

def main():
    results_dir = sys.argv[1]
    mechs = [int(x) for x in sys.argv[2:]] or [0,1,2,3,4,5,6,7,8]
    data = load(results_dir, mechs)
    ref_mech = 4  # release-identity reference for trained policy
    for mech in mechs:
        print(f"=== mech {mech} ===")
        tot = defaultdict(int)
        for battery in sorted(data[mech].keys()):
            for fam in sorted(data[mech][battery].keys()):
                items = data[mech][battery][fam]
                m = defaultdict(int)
                cells_by_depth = defaultdict(list)
                nrel = defaultdict(int); ntot = defaultdict(int)
                nacc = defaultdict(int); nrelacc = defaultdict(int)
                for iid, dd in items.items():
                    seq = sorted(dd.items())  # (depth, (correct, conf, release))
                    sm = metrics_for_cells([(d, c, f) for d, (c, f, _) in seq])
                    for k, v in sm.items():
                        m[k] += v; tot[k] += v
                    for d, (c, f, _) in seq:
                        cells_by_depth[d].append((c, f))
                        ntot[d] += 1
                        if c in ("1", "0"):
                            nrel[d] += 1
                            if c == "1":
                                nrelacc[d] += 1
                        if c == "1":
                            nacc[d] += 1
                g = g_curve(cells_by_depth)
                gviol = 0
                ds = sorted(g.keys())
                for i in range(len(ds) - 1):
                    if g[ds[i]] is not None and g[ds[i+1]] is not None:
                        if g[ds[i+1]] > g[ds[i]] + 1e-12:
                            gviol += 1
                tot["gviol"] += gviol
                acc_d = {d: (nacc[d]/ntot[d] if ntot[d] else 0.0) for d in ntot}
                rel_rate = {d: (nrel[d]/ntot[d] if ntot[d] else 0.0) for d in ntot}
                gstr = ",".join(f"{d}:{g[d]:+.3f}" if g[d] is not None else f"{d}:n/a" for d in ds)
                accstr = ",".join(f"{d}:{acc_d[d]:.3f}" for d in sorted(acc_d))
                relstr = ",".join(f"{d}:{rel_rate[d]:.2f}" for d in sorted(rel_rate))
                print(f"  {battery}/{fam}: n={len(items)} 1->0={m['n10']} A->0={m['a0']} "
                      f"V1={m['v1']} V2={m['v2']} Gviol={gviol}")
                print(f"    G: {gstr}")
                print(f"    acc: {accstr}")
                print(f"    relrate: {relstr}")
                racc_d = {d: (nrelacc[d]/nrel[d] if nrel[d] else float("nan")) for d in ntot}
                raccstr = ",".join(f"{d}:{racc_d[d]:.3f}" for d in sorted(racc_d))
                print(f"    racc(released-only): {raccstr}")
        print(f"  TOTAL: 1->0={tot['n10']} A->0={tot['a0']} V1={tot['v1']} V2={tot['v2']} Gviol={tot['gviol']}")
        # release-identity vs M4
        if mech != ref_mech and ref_mech in data:
            diff = 0; n = 0
            for battery in data[mech]:
                for fam in data[mech][battery]:
                    for iid, dd in data[mech][battery][fam].items():
                        rdd = data[ref_mech][battery][fam].get(iid, {})
                        for d, (c, f, rel) in dd.items():
                            if d in rdd:
                                n += 1
                                if rel != rdd[d][2] or c != rdd[d][0]:
                                    diff += 1
            print(f"  release-identity vs M4: {n-diff}/{n} identical cells")
        print()

main()
