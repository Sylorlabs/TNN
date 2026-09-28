#!/usr/bin/env python3
"""PACKAGE 2 glue: score the channel shootout (TEST split only).

Reads kb/autopsy/channels/out/runN/out_{A,B}.txt (pure-Zag output) and the
frozen truth.json (scorer-only). Verifies every Zag-emitted feature against
truth.json's non-truth fields, then computes the frozen metrics.

Writes scores.json and prints the shootout table.
"""
import json, math, os, sys

CHAN = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.normpath(os.path.join(CHAN, "..", "..", "..", "prose-learning",
                                        "epistemic_wave", "kb4_rerun"))
CLASSES = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]
CIX = {c: i for i, c in enumerate(CLASSES)}
COST = {"a": "immediate table lookup", "b": "delayed re-observation (proxy)",
        "c": "immediate (second sense, same time)",
        "d1": "immediate table lookup", "d2": "immediate table lookup",
        "a+c": "immediate (second sense)", "a+b": "delayed re-observation (proxy)"}
# tie-break rank: lower = cheaper/faster
COSTRANK = {"a": 0, "d1": 0, "d2": 0, "c": 1, "a+c": 1, "b": 2, "a+b": 2}
CHKEYS = ["a", "b", "c", "d1", "d2", "a+c", "a+b"]

def parse_out(path):
    cal, thr, feats = [], {}, []
    nF = 0
    for line in open(path):
        p = line.rstrip("\n").split("\t")
        if p[0] == "CAL":
            cal.append(tuple(map(int, p[1:])))
        elif p[0] == "THR":
            thr[p[1]] = (int(p[2]), int(p[3]))
        elif p[0] == "F":
            feats.append(tuple(map(int, p[1:])))
            nF += 1
        elif p[0] == "SKIP":
            raise SystemExit("SKIP line present in %s: %s" % (path, line))
        elif p[0] == "DONE":
            assert int(p[1]) == nF, "DONE/F mismatch in %s" % path
    return cal, thr, feats

def main():
    rundir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(CHAN, "out", "run1")
    truth = json.load(open(os.path.join(CORPUS, "truth.json")))
    man = json.load(open(os.path.join(CHAN, "..", "SPLIT_MANIFEST.json")))
    testset = set()
    for task in CLASSES:
        testset.update(man["test"][task])

    # index truth: (sense, stim, variant) -> rec ; primary rec per (sense, stim)
    per = {}
    for k, v in truth.items():
        se, _ = k.split("/")
        per[(se, v["stim_idx"], v["variant"])] = v

    rows = []  # (sense, stim, class, agree_pa, conf_a, conf_p, agree_n, agree_ab, verdicts[7], correct)
    for sense in ("A", "B"):
        cal, thr, feats = parse_out(os.path.join(rundir, "out_%s.txt" % sense))
        other = "B" if sense == "A" else "A"
        for f in feats:
            (stim, cl, agr_pa, ca, cp, agr_n, agr_ab,
             va, vb, vc, vd1, vd2, vac, vab) = f
            a = per[(sense, stim, "adversarial")]
            p = per[(sense, stim, "primary")]
            n = per[(sense, stim, "noise")]
            o = per[(other, stim, "adversarial")]
            # ---- anti-gaming cross-check: Zag features vs truth.json ----
            assert a["task"] == CLASSES[cl], (sense, stim, "class")
            assert stim in testset, (sense, stim, "not in TEST")
            assert (1 if a["judg_idx"] == p["judg_idx"] else 0) == agr_pa, (sense, stim, "agree_pa")
            assert a["confidence"] == ca, (sense, stim, "conf_a")
            assert p["confidence"] == cp, (sense, stim, "conf_p")
            assert (1 if n["judg_idx"] == a["judg_idx"] else 0) == agr_n, (sense, stim, "agree_n")
            assert (1 if o["judg_idx"] == a["judg_idx"] else 0) == agr_ab, (sense, stim, "agree_ab")
            rows.append((sense, stim, cl, agr_pa, ca, cp, agr_n, agr_ab,
                         [va, vb, vc, vd1, vd2, vac, vab],
                         1 if a["correct"] else 0))
    print("verified %d fixtures (A+B pooled test adversarial)" % len(rows))

    # prior entropy of the target
    n1 = sum(r[-1] for r in rows)
    n0 = len(rows) - n1
    p1 = n1 / len(rows)
    H = -(p1 * math.log2(p1) + (1 - p1) * math.log2(1 - p1))
    print("prior: n=%d correct=%d H(adv_correct)=%.4f bits" % (len(rows), n1, H))

    out = {"H_adv_correct": H, "n": len(rows), "n_correct": n1, "channels": {}}
    table = []
    for ci, key in enumerate(CHKEYS):
        # contingency verdict(0,1,2) x correct(0,1)
        cnt = [[0, 0], [0, 0], [0, 0]]
        for r in rows:
            v = r[8][ci]
            cnt[v][r[9]] += 1
        N = len(rows)
        mi = 0.0
        for v in range(3):
            for y in range(2):
                if cnt[v][y]:
                    pv = sum(cnt[v]) / N
                    py = (sum(cnt[vv][y] for vv in range(3))) / N
                    pvy = cnt[v][y] / N
                    mi += pvy * math.log2(pvy / (pv * py))
        # resolution accuracy over non-SUSPECT
        nn = sum(cnt[v][y] for v in (0, 1) for y in (0, 1))
        match = cnt[1][1] + cnt[0][0]
        racc = match / nn if nn else float("nan")
        # false-install rate
        ni = cnt[1][0] + cnt[1][1]
        fir = cnt[1][0] / ni if ni else float("nan")
        # SUSPECT stats
        ns = cnt[2][0] + cnt[2][1]
        srate = ns / N
        sprec = (sum(1 for r in rows if r[8][ci] == 2 and r[3] == 0) / ns) if ns else float("nan")
        out["channels"][key] = {
            "bits": mi, "resolution_accuracy": racc,
            "false_install_rate": fir, "cost": COST[key],
            "suspect_rate": srate, "suspect_precision": sprec,
            "n_install": ni, "n_withhold": cnt[0][0] + cnt[0][1], "n_suspect": ns,
            "contingency": cnt,
        }
        table.append((key, mi, racc, fir, srate, sprec, COST[key]))
    for key, mi, racc, fir, srate, sprec, cost in table:
        print("%-4s bits=%7.4f  res_acc=%.3f  false_install=%.3f  "
              "suspect_rate=%.3f suspect_prec=%.3f  [%s]"
              % (key, mi, racc, fir, srate, sprec, cost))

    # champion: most bits; tie-break lower cost rank; deployability vs 10% bar
    ranked = sorted(table, key=lambda t: (-t[1], COSTRANK[t[0]]))
    lead = ranked[0]
    deployable = [t for t in ranked if t[3] <= 0.10]
    out["champion_on_bits"] = lead[0]
    if lead[3] > 0.10:
        out["champion_status"] = "NOT DEPLOYABLE"
        out["best_deployable"] = deployable[0][0] if deployable else None
    else:
        out["champion_status"] = "DEPLOYABLE"
        out["best_deployable"] = lead[0]
    print("champion-on-bits:", lead[0], "->", out["champion_status"],
          "| best deployable:", out["best_deployable"])

    with open(os.path.join(rundir, "scores.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("wrote", os.path.join(rundir, "scores.json"))

if __name__ == "__main__":
    main()
