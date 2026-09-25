#!/usr/bin/env python3
"""H5 SR-ROUND, arm CTL: yardstick table B1-B13 for frozen v2-100x params.

Inputs: frozen v2 eval TSVs (training/v2/work/results/*_m14_*_A.tsv),
        M4 reference (same dir, *_m4_*_A.tsv), frozen analyzer
        (training/analyze.py) — loaded via exec of its def-block so TSV
        parsing and metric definitions (n10/V1/V2/G/Gviol) are the frozen
        ones, not a reimplementation. No new binaries, no new runs.

Outputs (under sr_round/ctl/):
  analysis/ctl_curves.tsv   per-(family,depth) G, acc, n_rel, conf means
  analysis/ctl_bars.tsv     B1-B13 verdict table for mech 14 (v2-100x)
  analysis/ctl_buildlog.txt input SHAs + reproduction cross-checks
  VERDICT_CTL.md            yardstick verdict (written by hand from ctl_bars.tsv)

Usage: python3 analyze_ctl.py
"""
import sys, os, hashlib, glob
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
TRAINING = os.path.normpath(os.path.join(HERE, "..", ".."))
RESULTS = os.path.join(TRAINING, "v2", "work", "results")
ANALYSIS_M4 = os.path.join(TRAINING, "v2", "analysis")  # m0-m8 baselines (symlinks)
ANALYZER = os.path.join(TRAINING, "analyze.py")
PREREG = os.path.join(HERE, "..", "PREREG_SR.md")
PREREG_SHA = hashlib.sha256(open(PREREG, "rb").read()).hexdigest()
FROZEN_PREREG_SHA = "f55d1dbbe1a609f69301ce8f537282a0372880b51fdec6b51d0f588b9fd96d30"
if PREREG_SHA != FROZEN_PREREG_SHA:
    print(f"*** PREREG SHA MISMATCH: {PREREG_SHA} != frozen {FROZEN_PREREG_SHA} ***")
    sys.exit(1)

# --- frozen analyzer defs (identical parsing/metrics; never retyped) ---
_frozen_src = open(ANALYZER).read()
_frozen_defs = _frozen_src.rsplit("main()", 1)[0]
_ns = {}
exec(compile(_frozen_defs, ANALYZER, "exec"), _ns)
load = _ns["load"]
metrics_for_cells = _ns["metrics_for_cells"]
g_curve = _ns["g_curve"]
BATTERY_DEPTHS = _ns["BATTERY_DEPTHS"]

MECH = 14   # v2-100x (MT2-CONF-100x)
REF = 4     # M4 baseline
TOL = 1e-12

FAMILIES = [("admit", "admit"), ("revoke", "revoke"), ("logic", "logic"),
            ("cost", "cost"), ("trap", "trap"),
            ("ceiling", "D"), ("ceiling", "O"), ("ceiling", "P"),
            ("redteam", "redteam")]
HONEST = {"admit", "revoke", "logic", "cost"}

def fam_name(battery, fam):
    return f"{battery}/{fam}" if battery == "ceiling" else battery

def per_depth(mech_data, battery, fam):
    """depth -> list of (correct, conf) over all items."""
    out = defaultdict(list)
    for iid, dd in mech_data[battery][fam].items():
        for d, (c, f, _rel) in dd.items():
            out[d].append((c, f))
    return out

def g_vals(cells_by_depth):
    return g_curve(cells_by_depth)

def main():
    # A/B byte-identity check on m14 legs (frozen evidence asserts it; verify)
    import subprocess
    for a in sorted(glob.glob(os.path.join(RESULTS, "*_m14_*_A.tsv"))):
        b = a.replace("_A.tsv", "_B.tsv")
        if not os.path.exists(b) or subprocess.run(
                ["cmp", "-s", a, b]).returncode != 0:
            print(f"*** A/B BYTE-IDENTITY FAILURE: {a} ***")
            sys.exit(1)

    d14_src = load(RESULTS, [MECH])       # m14 legs live in work/results
    d4_src = load(ANALYSIS_M4, [REF])     # m4 legs live in v2/analysis (symlinks)
    data = {MECH: d14_src[MECH], REF: d4_src[REF]}
    if not data[REF]:
        print("*** M4 data failed to load from v2/analysis ***")
        sys.exit(1)
    d14, d4 = data[MECH], data[REF]

    # ---------- reproduction cross-checks vs v2 VERDICT.md ----------
    rep = []
    for mech, expect in ((14, (0, 0, 44, 7)), (4, (0, 0, 160, 14))):
        tot = defaultdict(int)
        per_fam = {}
        for battery, fam in FAMILIES:
            items = data[mech][battery][fam]
            m = defaultdict(int)
            for iid, dd in items.items():
                seq = sorted(dd.items())
                sm = metrics_for_cells([(d, c, f) for d, (c, f, _r) in seq])
                for k, v in sm.items():
                    m[k] += v; tot[k] += v
            cells_by_depth = per_depth(data[mech], battery, fam)
            g = g_vals(cells_by_depth)
            ds = sorted(g.keys())
            gviol = sum(1 for i in range(len(ds) - 1)
                        if g[ds[i]] is not None and g[ds[i + 1]] is not None
                        and g[ds[i + 1]] > g[ds[i]] + TOL)
            tot["gviol"] += gviol
            per_fam[fam_name(battery, fam)] = (m["n10"], m["v1"], m["v2"], gviol)
        got = (tot["n10"], tot["v1"], tot["v2"], tot["gviol"])
        ok = got == expect
        rep.append((mech, got, expect, ok, per_fam))
        print(f"mech {mech}: n10={got[0]} V1={got[1]} V2={got[2]} Gviol={got[3]} "
              f"expected={expect} -> {'MATCH' if ok else '*** MISMATCH ***'}")
    # per-family expectations from v2 VERDICT.md §4 table
    fam_expect = {"revoke": (0, 0), "logic": (0, 0), "cost": (0, 0),
                  "trap": (0, 0), "ceiling/D": (0, 0), "admit": (0, 1),
                  "ceiling/O": (0, 2), "ceiling/P": (44, 2),
                  "redteam": (0, 2)}
    ok_all = True
    for mech, got, expect, ok, per_fam in rep:
        if mech != 14:
            continue
        for fn, (v2e, gve) in fam_expect.items():
            v2g, gvg = per_fam[fn][2], per_fam[fn][3]
            if (v2g, gvg) != (v2e, gve):
                ok_all = False
                print(f"  *** family {fn}: V2/Gviol {v2g}/{gvg} != expected {v2e}/{gve}")
    print("per-family vs v2 VERDICT.md:", "MATCH" if ok_all else "*** MISMATCH ***")
    if not all(ok for _, _, _, ok, _ in rep) or not ok_all:
        print("STOP: re-analysis disagrees with frozen evidence. Implementation bug until proven otherwise.")
        sys.exit(1)

    # ---------- guard metrics on mech 14 ----------
    # accumulate per (family, depth) and matrix aggregates
    curves = {}   # fname -> {d: dict(g, acc, n_rel, n_tot, n_rel_correct, mean_conf_correct, n_wrong, mean_conf_wrong)}
    agg_cc = []   # (conf/1000) of released correct cells, matrix-wide
    agg_ww = []   # (conf/1000) of released wrong cells, matrix-wide
    n_abs = 0; n_tot_all = 0
    fam_relcorrect = {}   # fname -> (n_m14, n_m4) released-correct counts
    for battery, fam in FAMILIES:
        fname = fam_name(battery, fam)
        cd = per_depth(d14, battery, fam)
        cd4 = per_depth(d4, battery, fam)
        cur = {}
        nc14 = 0; nc4 = 0
        for d in sorted(cd.keys()):
            cells = cd[d]
            rel = [(c, f) for (c, f) in cells if c in ("1", "0")]
            cc = [f / 1000.0 for (c, f) in rel if c == "1"]
            ww = [f / 1000.0 for (c, f) in rel if c == "0"]
            agg_cc.extend(cc); agg_ww.extend(ww)
            nc14 += len(cc)
            nc4 += sum(1 for (c, f) in cd4.get(d, []) if c == "1")
            n_abs += sum(1 for (c, f) in cells if c == "A")
            n_tot_all += len(cells)
            mean_conf = (sum(f for _, f in rel) / len(rel) / 1000.0) if rel else None
            acc = (sum(1 for c, _ in rel if c == "1") / len(rel)) if rel else None
            cur[d] = dict(g=(mean_conf - acc) if (mean_conf is not None) else None,
                          acc=acc, n_rel=len(rel), n_tot=len(cells),
                          n_cc=len(cc), n_ww=len(ww),
                          mcc=(sum(cc) / len(cc)) if cc else None,
                          mcw=(sum(ww) / len(ww)) if ww else None)
        curves[fname] = cur
        fam_relcorrect[fname] = (nc14, nc4)

    B = {}  # bar -> (status, value-string)

    # B1: 1->0 transitions = 0
    b1 = rep[0][4]
    B["B1"] = ("PASS" if sum(v[0] for v in b1.values()) == 0 else "FAIL",
               f"n10 total = {sum(v[0] for v in b1.values())} (threshold 0)")

    # B2: V1=0 and V2=0
    v1t = sum(v[1] for v in b1.values()); v2t = sum(v[2] for v in b1.values())
    B["B2"] = ("PASS" if (v1t == 0 and v2t == 0) else "FAIL",
               f"V1={v1t} V2={v2t} (thresholds 0)")

    # B3: strict G-violations per family = 0 every family
    fam_gviol = {}
    for battery, fam in FAMILIES:
        fname = fam_name(battery, fam)
        cur = curves[fname]
        ds = sorted(d for d in cur if cur[d]["g"] is not None)
        fam_gviol[fname] = sum(1 for i in range(len(ds) - 1)
                               if cur[ds[i + 1]]["g"] > cur[ds[i]]["g"] + TOL)
    bad3 = [f for f, v in fam_gviol.items() if v > 0]
    B["B3"] = ("PASS" if not bad3 else "FAIL",
               "Gviol per family: " + ", ".join(f"{f}={v}" for f, v in fam_gviol.items())
               + ("; FAILING: " + ", ".join(bad3) if bad3 else ""))

    # B4: aggregate meanConfCorrect >= 0.50
    mcc_agg = sum(agg_cc) / len(agg_cc)
    B["B4"] = ("PASS" if mcc_agg >= 0.50 else "FAIL",
               f"meanConfCorrect = {mcc_agg:.6f} (n={len(agg_cc)}, threshold >=0.50)")

    # B4b: per honest family mean C on released correct >= 0.50 (n_rel_correct>=10)
    b4b_rows = []
    for battery, fam in FAMILIES:
        if fam_name(battery, fam) not in HONEST:
            continue
        fname = fam_name(battery, fam)
        cells = []
        for iid, dd in d14[battery][fam].items():
            for d, (co, f, _r) in dd.items():
                if co == "1":
                    cells.append(f / 1000.0)
        n = len(cells)
        m = (sum(cells) / n) if n else float("nan")
        status = "PASS" if (n >= 10 and m >= 0.50) else ("FAIL" if n >= 10 else "n/a<10")
        b4b_rows.append((fname, n, m, status))
    bad4b = [r for r in b4b_rows if r[3] == "FAIL"]
    B["B4b"] = ("PASS" if not bad4b else "FAIL",
                "; ".join(f"{f}: meanC={m:.6f} (n={n}) {s}" for f, n, m, s in b4b_rows))

    # B5: separation >= 0.20
    mcw_agg = sum(agg_ww) / len(agg_ww)
    sep = mcc_agg - mcw_agg
    B["B5"] = ("PASS" if sep >= 0.20 else "FAIL",
               f"meanConfCorrect-meanConfWrong = {sep:.6f} (n_c={len(agg_cc)}, n_w={len(agg_ww)}, threshold >=0.20)")

    # B6: released-correct / M4 released-correct >= 0.95 per family.
    # 0/0 (no released-correct in reference AND arm) is vacuous, not drift:
    # with B9's 5240/5240 release+correct identity there is nothing to lose.
    b6_rows = []
    for fname, (n14, n4) in fam_relcorrect.items():
        if n4 == 0:
            r = float("nan")
            status = "vacuous" if n14 == 0 else "FAIL"
        else:
            r = n14 / n4
            status = "PASS" if r >= 0.95 else "FAIL"
        b6_rows.append((fname, n14, n4, r, status))
    bad6 = [r for r in b6_rows if r[4] == "FAIL"]
    B["B6"] = ("PASS" if not bad6 else "FAIL",
               "; ".join(f"{f}: {a}/{b}=" + (f"{r:.4f}" if r == r else "vacuous(0/0)") + f" {s}"
                         for f, a, b, r, s in b6_rows))

    # B7: abstained/total <= 0.30
    abst_rate = n_abs / n_tot_all
    B["B7"] = ("PASS" if abst_rate <= 0.30 else "FAIL",
               f"abstained {n_abs}/{n_tot_all} = {abst_rate:.6f} (threshold <=0.30)")

    # B8: G defined (>=10 rel cells) on >=4/5 slots (5-depth fams), >=5/7 (ceiling);
    #     defined values not all equal within 1e-3
    b8_rows = []
    for battery, fam in FAMILIES:
        fname = fam_name(battery, fam)
        cur = curves[fname]
        defined = [d for d in cur if cur[d]["n_rel"] >= 10 and cur[d]["g"] is not None]
        need = 5 if battery == "ceiling" else 4
        gvals = [cur[d]["g"] for d in defined]
        flat = (max(gvals) - min(gvals) <= 1e-3) if gvals else True
        ok_def = len(defined) >= need
        status = "PASS" if (ok_def and not flat) else "FAIL"
        b8_rows.append((fname, len(defined), need, "flat" if flat else f"range={max(gvals)-min(gvals):.6f}", status))
    bad8 = [r for r in b8_rows if r[4] == "FAIL"]
    B["B8"] = ("PASS" if not bad8 else "FAIL",
               "; ".join(f"{f}: {n}/{need} defined, {fl} {s}" for f, n, need, fl, s in b8_rows))

    # B9: answer channel frozen — applies to SR-S9,SR-S1,WC,ARCH,LOSS only; CTL informational
    # release+correct identity vs M4 over all 5240 cells
    diff = 0; n = 0
    for battery in d14:
        for fam in d14[battery]:
            for iid, dd in d14[battery][fam].items():
                rdd = d4[battery][fam].get(iid, {})
                for d, (c, f, rel) in dd.items():
                    if d in rdd:
                        n += 1
                        if rel != rdd[d][2] or c != rdd[d][0]:
                            diff += 1
    B["B9"] = ("n/a-CTL" if diff == 0 else "*** IDENTITY DRIFT ***",
               f"release+correct identity vs M4: {n-diff}/{n} (applies to trained arms; CTL carries v2's frozen assertion)")

    # B10/B10b/B11: SR-specific — not applicable to CTL
    B["B10"] = ("n/a-CTL", "disconnect-real (source audit): applies to SR-S9 only")
    B["B10b"] = ("n/a-CTL", "disconnect-real (mask audit): applies to SR-S1 only")
    B["B11"] = ("n/a-CTL", "post-release-only evidence: applies to SR-S9/SR-S1 only")

    # B12: refined reading — G>0 crossings recorded (does not kill).
    # Crossing rule consistent with v2 VERDICT.md refined table
    # (O x1, P x1, redteam x2): an adjacent pair counts iff it touches or
    # crosses 0 with a strict change: (s0,s1) in {(-1,0),(-1,+1),(0,+1)}
    # with tol=1e-12 sign bands.
    def sgn(x):
        return 0 if abs(x) <= TOL else (1 if x > 0 else -1)
    b12_rows = []
    for battery, fam in FAMILIES:
        fname = fam_name(battery, fam)
        cur = curves[fname]
        ds = sorted(d for d in cur if cur[d]["g"] is not None)
        xs = 0
        detail = []
        for i in range(len(ds) - 1):
            a, b = cur[ds[i]]["g"], cur[ds[i + 1]]["g"]
            if (sgn(a), sgn(b)) in ((-1, 0), (-1, 1), (0, 1)):
                xs += 1
                detail.append(f"d{ds[i]}->{ds[i+1]}({a:+.3f}->{b:+.3f})")
        b12_rows.append((fname, xs, detail))
    tot_x = sum(r[1] for r in b12_rows)
    B["B12"] = ("RECORDED",
                f"total G>0 crossings = {tot_x}; " + "; ".join(
                    f"{f}={x}" + (f" [{', '.join(d)}]" if d else "")
                    for f, x, d in b12_rows))

    # B13: per (F,d) with n_rel >= 8: G(F,d) >= -0.100
    b13_off = []
    worst = 1e9
    for battery, fam in FAMILIES:
        fname = fam_name(battery, fam)
        for d, c in curves[fname].items():
            if c["n_rel"] >= 8 and c["g"] is not None:
                worst = min(worst, c["g"])
                if c["g"] < -0.100:
                    b13_off.append((fname, d, c["g"], c["n_rel"]))
    B["B13"] = ("PASS" if not b13_off else "FAIL",
                f"min G over qualifying (F,d) = {worst:+.6f} (threshold >= -0.100)"
                + ("; OFFENDERS: " + ", ".join(f"{f}/d{d}: G={g:+.3f} (n={nn})"
                   for f, d, g, nn in b13_off) if b13_off else ""))

    # ---------- write outputs ----------
    adir = os.path.join(HERE, "analysis")
    os.makedirs(adir, exist_ok=True)
    sha_line = f"# prereg SHA256: {PREREG_SHA} (PREREG_SR.md FROZEN v1, {FROZEN_PREREG_SHA[:12]}...)\n"
    with open(os.path.join(adir, "ctl_curves.tsv"), "w") as f:
        f.write(sha_line)
        f.write("family\tdepth\tG\tacc\tn_rel\tn_tot\tn_correct\tn_wrong\tmean_conf_correct\tmean_conf_wrong\n")
        for battery, fam in FAMILIES:
            fname = fam_name(battery, fam)
            for d in sorted(curves[fname]):
                c = curves[fname][d]
                fmt = lambda x: "n/a" if x is None else f"{x:.6f}"
                f.write(f"{fname}\t{d}\t{fmt(c['g'])}\t{fmt(c['acc'])}\t"
                        f"{c['n_rel']}\t{c['n_tot']}\t{c['n_cc']}\t{c['n_ww']}\t"
                        f"{fmt(c['mcc'])}\t{fmt(c['mcw'])}\n")

    order = ["B1", "B2", "B3", "B4", "B4b", "B5", "B6", "B7", "B8",
             "B9", "B10", "B10b", "B11", "B12", "B13"]
    with open(os.path.join(adir, "ctl_bars.tsv"), "w") as f:
        f.write(sha_line)
        f.write("bar\tstatus\tevidence\n")
        for b in order:
            f.write(f"{b}\t{B[b][0]}\t{B[b][1]}\n")

    # build log with input SHAs
    def sha(p):
        return hashlib.sha256(open(p, "rb").read()).hexdigest()
    m14_files = sorted(glob.glob(os.path.join(RESULTS, "*_m14_*_A.tsv")) +
                      glob.glob(os.path.join(RESULTS, "*_m14_*_B.tsv")))
    m4_files = sorted(glob.glob(os.path.join(ANALYSIS_M4, "*_m4_*_A.tsv")))
    with open(os.path.join(adir, "ctl_buildlog.txt"), "w") as f:
        f.write(f"prereg SHA256: {PREREG_SHA} (PREREG_SR.md FROZEN v1)\n")
        f.write("CTL build log — re-analysis of frozen v2-100x evidence (no new runs)\n")
        f.write(f"analyzer: {ANALYZER} sha256={sha(ANALYZER)}\n")
        f.write(f"params: training/v2/params/mt2_params_100x.zag sha256="
                f"{sha(os.path.join(TRAINING, 'v2', 'params', 'mt2_params_100x.zag'))}\n")
        f.write(f"prereg: sr_round/PREREG_SR.md (frozen v1)\n")
        f.write(f"script: sr_round/ctl/analyze_ctl.py sha256={sha(os.path.abspath(__file__))}\n")
        f.write(f"m14 legs: {len(m14_files)} files ({len(m14_files)//2} A + {len(m14_files)//2} B), "
                f"A/B byte-identical all (verified by cmp at runtime)\n")
        f.write(f"m4 legs: {len(m4_files)} files (A only, recall reference, from v2/analysis/ symlinks)\n")
        f.write("--- m14 A-leg SHAs (B-legs byte-identical, verified by cmp) ---\n")
        for p in sorted(glob.glob(os.path.join(RESULTS, "*_m14_*_A.tsv"))):
            f.write(f"{sha(p)}  {os.path.basename(p)}\n")

    print("\n=== CTL B1-B13 ===")
    for b in order:
        print(f"{b:6s} {B[b][0]:10s} {B[b][1]}")
    print("\nwrote:", adir + "/ctl_bars.tsv, ctl_curves.tsv, ctl_buildlog.txt")

main()
