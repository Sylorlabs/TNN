#!/usr/bin/env python3
"""run_cc1.py — run the 10 CC1-family mode-2 cells through v4, 3x each.

For each cell: 3 runs (metrics + trace), sha256-compare all outputs
(KB-V4-4 per stream), then score from the trace:
  final_perm_j, false_installs (disp 1/9 with jcode != truth),
  installs (disp in {0,1,2,8,9}), veto breakdown from metrics.
Compares against EXPECT_GUARD_CELL.tsv MG6 expectations:
  all 9 scored cells -> final 3, false 0, installs 4. V9 reported only.
Writes per-cell evidence files. Zero RNG.
"""
import hashlib, os, subprocess, sys

W = os.path.expanduser("~/workspace/pam_gov_lh/crew6_held")
BIN = os.path.join(W, "src/v4_bin")
M2 = os.path.join(W, "gen/cc1_cells/mode2")
EV = os.path.join(W, "evidence/cc1")
os.makedirs(EV, exist_ok=True)

CELLS = ["cc1", "cc1_v1", "cc1_v2", "cc1_v3", "cc1_v4",
         "cc1_v5", "cc1_v6", "cc1_v7", "cc1_v8", "cc1_v9"]
SCORED = set(CELLS[:9])

def sha(b): return hashlib.sha256(b).hexdigest()

def parse_metrics(path):
    d = {}
    for ln in open(path):
        ln = ln.strip()
        if "=" in ln:
            k, v = ln.split("=", 1)
            d[k] = int(v)
    return d

results = []
for cell in CELLS:
    case = os.path.join(M2, "cc1_%s_m2.txt" % cell)
    trials = [ln.split("|") for ln in open(case).read().strip().split("\n")]
    mfiles, tfiles = [], []
    for r in (1, 2, 3):
        mf = os.path.join(EV, "%s_run%d.metrics" % (cell, r))
        tf = os.path.join(EV, "%s_run%d.trace" % (cell, r))
        with open(tf, "wb") as tout:
            pr = subprocess.run([BIN, case, "2", mf, "1"],
                                stdout=tout, stderr=subprocess.PIPE)
        assert pr.returncode == 0, (cell, r, pr.stderr[:200])
        mfiles.append(mf); tfiles.append(tf)
    mh = [sha(open(f, 'rb').read()) for f in mfiles]
    th = [sha(open(f, 'rb').read()) for f in tfiles]
    det = (mh[0] == mh[1] == mh[2]) and (th[0] == th[1] == th[2])
    m = parse_metrics(mfiles[0])
    # score from trace run 1
    disps = []
    for ln in open(tfiles[0]):
        p = ln.strip().split("|")
        assert p[0] == "V4" and len(p) == 3
        disps.append(int(p[2]))
    assert len(disps) == len(trials), (cell, len(disps), len(trials))
    perm_j = -1
    false_inst = 0
    installs = 0
    for (flds, d) in zip(trials, disps):
        jc, truth = int(flds[8]), int(flds[12])
        if d in (0, 1, 2, 8, 9):
            installs += 1
        if d in (1, 9):
            perm_j = jc
            if jc != truth:
                false_inst += 1
    rev = m["revised_installs"]
    row = {
        "cell": cell, "scored": cell in SCORED, "det3x": det,
        "msha": mh[0], "tsha": th[0],
        "final_perm_j": perm_j, "false_installs": false_inst,
        "installs": installs, "revised_installs": rev,
        "rk1": m["rk1_falseperm"], "rk2n": m["rk2_num"], "rk2d": m["rk2_den"],
        "f5": m["f5_vetoes"], "floor": m["mg6_veto_floor"],
        "span": m["mg6_veto_span"], "seqgap": m["mg6_veto_seqgap"],
        "allows": m["mg6_allows"], "disps": disps,
    }
    results.append(row)
    exp = "EXP(3,0,4)" if cell in SCORED else "V9-probe"
    ok = (perm_j == 3 and false_inst == 0 and installs == 4 and rev == 0) if cell in SCORED else True
    print("%-8s det=%s perm=%d false=%d installs=%d rev=%d f5=%d fl=%d sp=%d sg=%d al=%d disps=%s %s %s"
          % (cell, det, perm_j, false_inst, installs, rev, m["f5_vetoes"],
             m["mg6_veto_floor"], m["mg6_veto_span"], m["mg6_veto_seqgap"],
             m["mg6_allows"], disps, exp, "OK" if ok else "MISMATCH"))

with open(os.path.join(EV, "cc1_scores.tsv"), "w") as o:
    o.write("cell\tscored\tdet3x\tfinal_perm_j\tfalse_installs\tinstalls\trevised_installs\trk1\trk2n\trk2d\tf5\tfloor\tspan\tseqgap\tallows\tmsha\ttsha\n")
    for r in results:
        o.write("\t".join(map(str, [r["cell"], int(r["scored"]), int(r["det3x"]),
              r["final_perm_j"], r["false_installs"], r["installs"],
              r["revised_installs"], r["rk1"], r["rk2n"], r["rk2d"],
              r["f5"], r["floor"], r["span"], r["seqgap"], r["allows"],
              r["msha"], r["tsha"]])) + "\n")
print("wrote", os.path.join(EV, "cc1_scores.tsv"))
nbad = sum(1 for r in results if r["scored"] and not
           (r["final_perm_j"] == 3 and r["false_installs"] == 0 and
            r["installs"] == 4 and r["revised_installs"] == 0 and r["det3x"]))
print("scored cells failing expectation:", nbad)
