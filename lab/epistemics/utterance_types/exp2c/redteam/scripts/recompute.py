#!/usr/bin/env python3
"""Independent recomputation of exp2c bar table from raw run outputs.
Reads runs/*.txt (committed rep1), parses 2C_CURVE + H7_CHECK lines,
recomputes per-type TR/PA/NO/DP/LK, n_2c_fail, frozen_fail, and all
auxiliary checks (leakage, suppression, NEST, FHYP, nofilter_guards).
Then diffs against the claimed bartable.md."""
import re, sys, os, hashlib

RUNS = os.path.expanduser("~/workspace/redteam_exp2c/evidence/runs")
LEG_FILES = {
    "base": "base_rep1.txt",
    "ab-a": "ab_a_rep1.txt",
    "ab-b": "ab_b_rep1.txt",
    "ab-a-rev": "ab_a_rev_rep1.txt",
    "abc-a": "abc_a_rep1.txt",
    "abc-b": "abc_b_rep1.txt",
    "vol-a": "vol_a_rep1.txt",
    "vol-b": "vol_b_rep1.txt",
    "vol2-a": "vol2_a_rep1.txt",
    "vol2-b": "vol2_b_rep1.txt",
    "de-a": "de_a_rep1.txt",
    "de-b": "de_b_rep1.txt",
}

def parse_run(path):
    curves = {}   # type -> dict(TR,PA,NO,DP,LK)
    checks = {}   # checkname -> (num, den)
    meta = {}
    with open(path) as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith("2C_CURVE|"):
                p = line.split("|")
                t = int(p[1])
                d = {}
                i = 2
                while i < len(p) - 1:
                    d[p[i]] = int(p[i+1]); i += 2
                curves[t] = d
            elif line.startswith("H7_CHECK,"):
                p = line.split(",")
                if len(p) >= 4:
                    checks[p[1]] = (int(p[2]), int(p[3]))
            elif line.startswith("2CMODE|"):
                meta["mode"] = line.split("|")[1]
            elif line.startswith("2CITEMS|"):
                meta["items"] = line
    return curves, checks, meta

rows = []
for leg, fn in LEG_FILES.items():
    path = os.path.join(RUNS, fn)
    curves, checks, meta = parse_run(path)
    assert len(curves) == 5, f"{leg}: {len(curves)} curves"
    # 2c failures: 2c_sinc_dp_N / 2c_sinc_lk_N with num==0
    fails = []
    for t in range(1, 6):
        for k in ("dp", "lk"):
            name = f"2c_sinc_{k}_{t}"
            num, den = checks[name]
            assert den == 1, f"{leg} {name} den={den}"
            if num == 0:
                fails.append(name)
    # frozen failure: pre-2c sinc_lk checks with num==0
    ffails = []
    for t in range(1, 6):
        for k in ("dp", "lk"):
            name = f"sinc_{k}_{t}"
            if name in checks and checks[name][0] == 0:
                ffails.append(name)
    row = [leg]
    for t in range(1, 6):
        c = curves[t]
        row += [c["TR"], c["PA"], c["NO"], c["DP"], c["LK"]]
    # cross-check: 2c check nums must equal (score >= 9)
    for t in range(1, 6):
        dp = curves[t]["DP"]; lk = curves[t]["LK"]
        ndp, ddp = checks[f"2c_sinc_dp_{t}"]
        nlk, dlk = checks[f"2c_sinc_lk_{t}"]
        if (ndp == 1) != (dp >= 9):
            print(f"SCORE-CHECK INCONSISTENCY {leg}: 2c_sinc_dp_{t}={ndp} but DP={dp}")
        if (nlk == 1) != (lk >= 9):
            print(f"SCORE-CHECK INCONSISTENCY {leg}: 2c_sinc_lk_{t}={nlk} but LK={lk}")
    # auxiliary bars
    aux = {"leak_substring": (0,0), "leak_paraphrase": (0,0),
           "supp_bogus": (5,5), "supp_count": (5,5),
           "nest_verdict": (20,20), "fhyp_verdict": (20,20),
           "phase3_fact_recall": (20,20), "phase3_fact_predict": (20,20)}
    for name, (en, ed) in aux.items():
        num, den = checks.get(name, (-1,-1))
        if (num, den) != (en, ed):
            print(f"AUX MISMATCH {leg}: {name}={num},{den} expected {en},{ed}")
    for t in range(1, 6):
        num, den = checks.get(f"xinterf_no_{t}", (-1,-1))
        if (num, den) != (1, 1):
            print(f"AUX MISMATCH {leg}: xinterf_no_{t}={num},{den}")
    row += [len(fails), ",".join(ffails) if ffails else "-"]
    rows.append((leg, row, fails))

# print recomputed table
hdr = ["leg","t1_TR","t1_PA","t1_NO","t1_DP","t1_LK","t2_TR","t2_PA","t2_NO","t2_DP","t2_LK",
       "t3_TR","t3_PA","t3_NO","t3_DP","t3_LK","t4_TR","t4_PA","t4_NO","t4_DP","t4_LK",
       "t5_TR","t5_PA","t5_NO","t5_DP","t5_LK","n_2c_fail","frozen_fail"]
print(",".join(hdr))
for leg, row, fails in rows:
    print(",".join(str(x) for x in row))

# diff vs claimed bartable.md
claimed = {}
with open(os.path.expanduser("~/workspace/redteam_exp2c/evidence/bartable.md")) as f:
    indata = False
    for line in f:
        if line.startswith("leg,design,"):
            indata = True; continue
        if indata and line.strip():
            p = line.rstrip("\n").split(",")
            if len(p) != 31:
                continue
            leg = p[0]
            # claimed cols: leg,design,corpus,order, then 25 nums, n_2c_fail, frozen_fail
            claimed[leg] = (p[4:29], p[29], p[30])
print("\n=== DIFF vs claimed bartable.md ===")
diffs = 0
for leg, row, fails in rows:
    mine_nums = [str(x) for x in row[1:26]]
    mine_nfail = str(row[26]); mine_ff = row[27]
    cnums, cnfail, cff = claimed[leg]
    if mine_nums != cnums or mine_nfail != cnfail or mine_ff.replace("-","sinc_lk_3") != cff:
        diffs += 1
        print(f"MISMATCH {leg}:")
        print(f"  mine : {','.join(mine_nums)} nfail={mine_nfail} ff={mine_ff}")
        print(f"  claim: {','.join(cnums)} nfail={cnfail} ff={cff}")
print("diffs:", diffs)
