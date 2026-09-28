#!/usr/bin/env python3
"""C3 scoring glue (PREREG_FROZEN_TCP.md §5, §9). Glue only:
  1. prepares truth_rows.txt from truth.json AT SCORE TIME (channel code never
     opened truth.json),
  2. runs the frozen Zag scorer (src/score_tcp — pure-Zag counting),
  3. independently recomputes every Zag-emitted count from verdict lines +
     truth_rows and VOIDS on any mismatch (0 tolerance),
  4. derives ratios / MIs from the counts,
  5. writes scores_c3.json.
Also enforces the 2x byte-identical rerun requirement (run1 vs run2)."""
import json, math, os, subprocess, sys

CHAN = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CHAN)
import score_tcp as C2  # noqa: E402  (reuse: mi_2x2, entropy, parse_verdicts,
                        # run_zag_scorer, recompute, cross_check)

TN = os.path.expanduser("~/workspace/tnn-lab")
CORPUS = os.path.join(TN, "prose-learning", "epistemic_wave", "kb4_rerun")
OUT = os.path.join(CHAN, "out_c3")
TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]

def prep_truth_rows(man):
    """truth.json touched ONLY here, at score time. Returns (path, rows)."""
    truth = json.load(open(os.path.join(CORPUS, "truth.json")))
    keys = set()
    for r in man:
        if r["split"] == "test":
            for se in ("A", "B"):
                base = r["relpath"].rsplit("/", 1)[-1]
                if base.endswith(".img"):
                    base = base[:-4]
                keys.add((se, r["task"], r["variant"], r["task"] + "/" + base))
    rows = []
    for k, v in truth.items():
        se, _ = k.split("/", 1)
        kk = (se, v["task"], v["variant"], v["stim"])
        if kk in keys:
            rows.append({"sense": se, "task": v["task"], "variant": v["variant"],
                         "logical": v["stim"], "Y": 1 if v["correct"] else 0,
                         "kb4idx": v["stim_idx"]})
    rows.sort(key=lambda r: (r["sense"], r["task"], r["logical"]))
    path = os.path.join(OUT, "truth_rows.txt")
    with open(path, "w") as f:
        for r in rows:
            f.write("%s\t%s\t%s\t%s\t%d\t%d\n" % (
                r["sense"], r["task"], r["variant"], r["logical"], r["Y"], r["kb4idx"]))
    return path, rows

def main():
    os.makedirs(OUT, exist_ok=True)
    man = json.load(open(os.path.join(CHAN, "inputs_tcp", "blob_manifest.json")))
    r1v = os.path.join(OUT, "run1", "verdicts.txt")
    r2v = os.path.join(OUT, "run2", "verdicts.txt")
    r1s = os.path.join(OUT, "run1", "noised_sha256.txt")
    r2s = os.path.join(OUT, "run2", "noised_sha256.txt")
    result = {"two_run_check": {}}
    r1b = open(r1v, "rb").read(); r2b = open(r2v, "rb").read()
    s1b = open(r1s, "rb").read(); s2b = open(r2s, "rb").read()
    result["two_run_check"]["verdict_lines_identical"] = (r1b == r2b)
    result["two_run_check"]["noised_sha256_identical"] = (s1b == s2b)
    if r1b != r2b or s1b != s2b:
        result["void"] = "run1/run2 mismatch"
        json.dump(result, open(os.path.join(CHAN, "scores_c3.json"), "w"), indent=1)
        print("VOID: run1/run2 mismatch")
        return 2

    truth_rows, trows = prep_truth_rows(man)
    cal_all, test_all = C2.parse_verdicts(r1v)
    assert len(cal_all) == 0, "C3 runs TEST rows only"
    assert len(test_all) == 184, len(test_all)  # 92 fixtures x 2 senses
    zag = C2.run_zag_scorer(r1v, truth_rows)
    ind = C2.recompute(cal_all, test_all, trows)
    errs = C2.cross_check(zag, ind)
    result["cross_check"] = {"n_errors": len(errs), "errors": errs[:20]}
    if errs:
        result["void"] = "Zag/Python count mismatch"
        json.dump(result, open(os.path.join(CHAN, "scores_c3.json"), "w"), indent=1)
        print("VOID: count cross-check failed: %s" % (errs[:5],))
        return 3

    def ratio(a, b):
        return (a / b) if b else None

    met = {}
    p = zag["pooled"]
    bits = C2.mi_2x2([[p["v0y0"], p["v0y1"]], [p["v1y0"], p["v1y1"]]]) if p["n"] else None
    met["pooled"] = {
        "n_test": p["n"],
        "P_Jnoisy_eq_J": ratio(p["c"], p["n"]),
        "P_C_given_Y1": ratio(p["cy1"], p["ny1"]),
        "P_C_given_Y0": ratio(p["cy0"], p["ny0"]),
        "bits": bits,
        "resolution_accuracy": ratio(p["v1y1"] + p["v0y0"], p["n"]),
        "false_install_rate": ratio(p["v1y0"], p["v1y1"] + p["v1y0"]),
        "H_adv_correct": C2.entropy(ratio(p["ny1"], p["n"])),
        "n_correct": p["ny1"],
    }
    met["sense"] = {}
    for s in ("A", "B"):
        q = zag["sense"][s]
        sny1 = scy1 = sny0 = scy0 = 0
        for t in TASKS:
            cell = zag["cell"][(s, t)]
            sny1 += cell["ny1"]; scy1 += cell["cy1"]
            sny0 += cell["ny0"]; scy0 += cell["cy0"]
        b = C2.mi_2x2([[q["v0y0"], q["v0y1"]], [q["v1y0"], q["v1y1"]]]) if q["n"] else None
        met["sense"][s] = {
            "n_test": q["n"],
            "P_Jnoisy_eq_J": ratio(q["c"], q["n"]),
            "P_C_given_Y1": ratio(scy1, sny1),
            "P_C_given_Y0": ratio(scy0, sny0),
            "bits": b,
            "resolution_accuracy": ratio(q["v1y1"] + q["v0y0"], q["n"]),
            "false_install_rate": ratio(q["v1y0"], q["v1y1"] + q["v1y0"]),
        }
    met["cells"] = {}
    for s in ("A", "B"):
        for t in TASKS:
            cell = zag["cell"][(s, t)]
            met["cells"]["%s/%s" % (s, t)] = {
                "P_Jnoisy_eq_J": ratio(cell["c"], cell["n"]),
                "P_C_given_Y1": ratio(cell["cy1"], cell["ny1"]),
                "P_C_given_Y0": ratio(cell["cy0"], cell["ny0"]),
                "n": cell["n"],
            }
    result["metrics"] = met
    result["counts"] = {"pooled": zag["pooled"], "sense": zag["sense"]}
    json.dump(result, open(os.path.join(CHAN, "scores_c3.json"), "w"), indent=1)
    print(json.dumps(met, indent=1))
    return 0

if __name__ == "__main__":
    sys.exit(main())
