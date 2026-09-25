#!/usr/bin/env python3
"""run_boundary.py — run the 27 MG6 boundary cells + decoy through v4, 3x each.

Per cell: 3 runs (metrics + trace), sha256-compare (KB-V4-4 per stream),
then score trial-D disposition, which veto conjunct fired (first-firing),
revised_installs, rk1. Compares against the preregistered expectation
(allow iff mrgF>=400 AND |dseq|>=20 AND spans disjoint).
The decoy (V9 x100) is reported, not expectation-checked.
Zero RNG.
"""
import hashlib, os, subprocess

W = os.path.expanduser("~/workspace/pam_gov_lh/crew6_held")
BIN = os.path.join(W, "src/v4_bin")
BO = os.path.join(W, "gen/boundary")
EV = os.path.join(W, "evidence/boundary")
os.makedirs(EV, exist_ok=True)

def sha(b): return hashlib.sha256(b).hexdigest()

def parse_metrics(path):
    d = {}
    for ln in open(path):
        ln = ln.strip()
        if "=" in ln:
            k, v = ln.split("=", 1)
            d[k] = int(v)
    return d

def run3(case, tag):
    mhs, ths = [], []
    for r in (1, 2, 3):
        mf = os.path.join(EV, "%s_run%d.metrics" % (tag, r))
        tf = os.path.join(EV, "%s_run%d.trace" % (tag, r))
        with open(tf, "wb") as tout:
            pr = subprocess.run([BIN, case, "2", mf, "1"],
                                stdout=tout, stderr=subprocess.PIPE)
        assert pr.returncode == 0, (tag, r, pr.stderr[:200])
        mhs.append(sha(open(mf, 'rb').read()))
        ths.append(sha(open(tf, 'rb').read()))
    det = (mhs[0] == mhs[1] == mhs[2]) and (ths[0] == ths[1] == ths[2])
    return det, mhs[0], ths[0]

def trialD_disp(tracefile):
    for ln in open(tracefile):
        p = ln.strip().split("|")
        if p[1] == "3":
            return int(p[2])
    raise AssertionError("no trial 3 in trace")

rows = []
ndev = 0
for V in (399, 400, 401):
    for D in (19, 20, 21):
        for sname in ("overlap", "touching", "disjoint"):
            tag = "b_mrg%d_dseq%d_%s" % (V, D, sname)
            case = os.path.join(BO, tag + ".txt")
            det, mh, th = run3(case, tag)
            m = parse_metrics(os.path.join(EV, "%s_run1.metrics" % tag))
            ddisp = trialD_disp(os.path.join(EV, "%s_run1.trace" % tag))
            exp_allow = (V >= 400) and (D >= 20) and (sname != "overlap")
            got_allow = (ddisp == 9)
            dev = (got_allow != exp_allow)
            ndev += dev
            veto = "-"
            if not got_allow:
                if m["f5_vetoes"]: veto = "f5"
                elif m["mg6_veto_floor"]: veto = "floor"
                elif m["mg6_veto_span"]: veto = "span"
                elif m["mg6_veto_seqgap"]: veto = "seqgap"
            rows.append((tag, det, ddisp, "ALLOW" if got_allow else "veto",
                         veto, "ALLOW" if exp_allow else "veto",
                         "DEVIATION" if dev else "ok",
                         m["revised_installs"], m["rk1_falseperm"], mh[:12]))
            print("%-28s det=%s trialD=%d -> %-5s veto=%-6s exp=%-5s %s rev=%d rk1=%d" %
                  (tag, det, ddisp, "ALLOW" if got_allow else "veto", veto,
                   "ALLOW" if exp_allow else "veto", "DEVIATION" if dev else "ok",
                   m["revised_installs"], m["rk1_falseperm"]))

print("boundary deviations from preregistered expectation:", ndev)

with open(os.path.join(EV, "boundary_scores.tsv"), "w") as o:
    o.write("cell\tdet3x\ttrialD_disp\toutcome\tveto_conjunct\texpected\tmatch\trevised_installs\trk1\tmsha12\n")
    for r in rows:
        o.write("\t".join(map(str, r)) + "\n")

# decoy: verbatim V9 x100, 3x
dcase = os.path.join(BO, "decoy_v9_x100.txt")
det, mh, th = run3(dcase, "decoy_v9_x100")
m = parse_metrics(os.path.join(EV, "decoy_v9_x100_run1.metrics"))
print("decoy det=%s trials=%d revised_installs=%d rk1=%d rk2=%d/%d f5=%d floor=%d span=%d seqgap=%d allows=%d d8=%d d9=%d msha=%s" % (
    det, m["trials"], m["revised_installs"], m["rk1_falseperm"],
    m["rk2_num"], m["rk2_den"], m["f5_vetoes"], m["mg6_veto_floor"],
    m["mg6_veto_span"], m["mg6_veto_seqgap"], m["mg6_allows"],
    m["d8"], m["d9"], mh))
with open(os.path.join(EV, "decoy_summary.tsv"), "w") as o:
    o.write("det3x\ttrials\trevised_installs\trk1\trk2n\trk2d\tf5\tfloor\tspan\tseqgap\tallows\td8\td9\tmsha\n")
    o.write("\t".join(map(str, [int(det), m["trials"], m["revised_installs"],
          m["rk1_falseperm"], m["rk2_num"], m["rk2_den"], m["f5_vetoes"],
          m["mg6_veto_floor"], m["mg6_veto_span"], m["mg6_veto_seqgap"],
          m["mg6_allows"], m["d8"], m["d9"], mh])) + "\n")
