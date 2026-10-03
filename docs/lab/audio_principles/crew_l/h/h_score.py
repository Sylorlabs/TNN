#!/usr/bin/env python3
"""Score the Crew L battery (frozen scorer) and compute all prereg 2.3 statistics:
(a) mean ERR(3)/ERR(0); (b) Wilcoxon signed-rank exact one-sided ERR(3)<ERR(0);
(c) non-degeneracy: #strictly improved, SHA(iter3)!=SHA(iter0), sign agreement;
L-R1 per-iteration error curve. Deterministic, zero RNG."""
import json, os, subprocess, sys
from itertools import product

HERE = os.path.dirname(os.path.abspath(__file__))
CREW = os.path.dirname(HERE)
MAN = json.load(open(os.path.join(CREW, "manifests", "intent_manifest.json")))
SCORER = os.path.join(CREW, "frozen", "scorer_l.py")
EV = os.path.join(CREW, "evidence")

def score_wav(path, thz, tenv):
    p = subprocess.run(["python3", SCORER, path, str(thz), str(tenv)],
                       capture_output=True, text=True)
    return json.loads(p.stdout)

def wilcoxon_exact(diffs):
    """One-sided exact p for H1: median(diffs) > 0. diffs = ERR0-ERR3."""
    d = [x for x in diffs if x != 0.0]
    m = len(d)
    ad = sorted(abs(x) for x in d)
    # average ranks for ties (no ties expected; handled generally)
    ranks = []
    i = 0
    while i < m:
        j = i
        while j < m and ad[j] == ad[i]:
            j += 1
        avg = (i + 1 + j) / 2.0
        ranks.extend([avg] * (j - i))
        i = j
    # map back: rank of each diff by its |d|
    w_obs = 0.0
    for x in d:
        # find rank of |x| (first matching)
        r = ranks[ad.index(abs(x))]
        if x > 0:
            w_obs += r
    # exact null distribution over 2^m sign assignments
    count = 0
    total = 1 << m
    # iterate bitmasks; use rank list (order by sorted |d| is fine for the sum dist)
    for mask in range(total):
        w = 0.0
        for i in range(m):
            if mask >> i & 1:
                w += ranks[i]
        if w >= w_obs - 1e-12:
            count += 1
    return count / total, w_obs, m

def parse_loop_log(path):
    """-> dict iter -> {meas_mhz, env_meas, dev_mhz, corr_mhz, render_mhz}"""
    out = {}
    for line in open(path):
        p = line.split()
        if not p or not p[0].startswith("iter="):
            continue
        it = int(p[0].split("=")[1])
        d = {}
        for tok in p[1:]:
            k, v = tok.split("=")
            d[k] = int(v)
        out[it] = d
    return out

def main():
    runs = [int(a) for a in sys.argv[1:]] or [1, 2, 3]
    allres = {}
    for r in runs:
        rd = os.path.join(EV, "run%d" % r)
        sha_table = json.load(open(os.path.join(rd, "sha_table.json")))
        rows = []
        for c in MAN:
            cid = c["case_id"]
            cd = os.path.join(rd, cid)
            errs, f0s, envs = [], [], []
            for k in range(4):
                s = score_wav(os.path.join(cd, "%s_iter%d.wav" % (cid, k)),
                              c["target_hz"], c["target_env_int"])
                errs.append(s["err"]); f0s.append(s["f0"]); envs.append(s["env"])
            log = parse_loop_log(os.path.join(cd, "loop.log"))
            d1 = log[1]
            dev_rel = abs(d1["dev_mhz"]) / (c["target_hz"] * 1000.0)
            rows.append({
                "case": cid, "target_hz": c["target_hz"], "target_env": c["target_env"],
                "err": errs, "f0": f0s, "env_meas": envs,
                "sha0": sha_table[cid]["iter0"], "sha3": sha_table[cid]["iter3"],
                "dev1_mhz": d1["dev_mhz"], "corr1_mhz": d1["corr_mhz"],
                "dev1_rel": dev_rel,
            })
        # (a)
        ratios = [row["err"][3] / row["err"][0] for row in rows]
        mean_ratio = sum(ratios) / len(ratios)
        # (b)
        diffs = [row["err"][0] - row["err"][3] for row in rows]
        pval, w_obs, m = wilcoxon_exact(diffs)
        # (c)
        n_improved = sum(1 for d in diffs if d > 0)
        sha_diff = all(row["sha3"] != row["sha0"] for row in rows)
        sig_cases = [row for row in rows if row["dev1_rel"] > 0.01]
        agree = sum(1 for row in sig_cases
                    if (row["dev1_mhz"] > 0) == (row["corr1_mhz"] > 0)
                    or (row["dev1_mhz"] == 0 and row["corr1_mhz"] == 0))
        # L-R1 curve
        curve = [sum(row["err"][k] for row in rows) / len(rows) for k in range(4)]
        res = {
            "run": r, "n": len(rows),
            "mean_err3_over_err0": mean_ratio,
            "criterion_a_pass": mean_ratio <= 0.80,
            "wilcoxon_p": pval, "wilcoxon_Wplus": w_obs, "wilcoxon_m": m,
            "criterion_b_pass": pval < 0.01,
            "n_strictly_improved": n_improved,
            "all_sha3_differ_sha0": sha_diff,
            "sign_agree": "%d/%d" % (agree, len(sig_cases)),
            "sign_agree_frac": (agree / len(sig_cases)) if sig_cases else 1.0,
            "criterion_c_pass": (n_improved >= 16 and sha_diff
                                 and (agree / len(sig_cases) >= 0.80 if sig_cases else True)),
            "mean_err_curve": curve,
            "rows": rows,
        }
        json.dump(res, open(os.path.join(rd, "score.json"), "w"), indent=2)
        allres[r] = {k: v for k, v in res.items() if k != "rows"}
        print("run%d: mean ERR3/ERR0=%.4f (a:%s)  wilcoxon p=%.2e (b:%s)  improved %d/20  sha-diff:%s  sign %d/%d (c:%s)  curve=%s"
              % (r, mean_ratio, res["criterion_a_pass"], pval, res["criterion_b_pass"],
                 n_improved, sha_diff, agree, len(sig_cases), res["criterion_c_pass"],
                 ["%.4f" % v for v in curve]))
    json.dump(allres, open(os.path.join(EV, "scores_summary.json"), "w"), indent=2)

if __name__ == "__main__":
    main()
