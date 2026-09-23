#!/usr/bin/env python3
"""STEP 6 — KB4 C2 scoring glue (PREREG_FROZEN_TCP.md §5, §6, §8).
Zag does all counting (src/score_tcp); this script only:
  1. prepares truth_rows.txt from truth.json AT SCORE TIME (channel code never
     opened truth.json),
  2. runs the Zag scorer, parses its counts,
  3. independently recomputes every Zag-emitted count from verdict lines +
     truth_rows and VOIDS on any mismatch,
  4. derives ratios / MIs from the counts, scores A1 (champion stacking),
  5. writes scores_tcp.json.
Also enforces the 2x byte-identical rerun requirement (run1 vs run2).
"""
import json, math, os, subprocess, sys

CHAN = os.path.dirname(os.path.abspath(__file__))
TN = os.path.expanduser("~/workspace/tnn-lab")
CORPUS = os.path.join(TN, "prose-learning", "epistemic_wave", "kb4_rerun")
CHAMP = os.path.join(TN, "kb", "autopsy", "channels", "out", "run1")
SCORER = os.path.join(CHAN, "src", "score_tcp")
TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]
CHAMP_BITS = 0.1483  # frozen (a)+(c) champion bits, prereg §6 F1

def mi_2x2(c):
    # c = [[v0y0, v0y1], [v1y0, v1y1]] -> I(V;Y)
    N = sum(sum(r) for r in c)
    mi = 0.0
    for v in range(2):
        for y in range(2):
            if c[v][y]:
                mi += (c[v][y] / N) * math.log2((c[v][y] / N) / ((sum(c[v]) / N) * ((c[0][y] + c[1][y]) / N)))
    return mi

def entropy(p1):
    if p1 <= 0 or p1 >= 1:
        return 0.0
    return -(p1 * math.log2(p1) + (1 - p1) * math.log2(1 - p1))

def parse_verdicts(path):
    cal, test = [], []
    for line in open(path):
        line = line.rstrip("\n")
        if not line:
            continue
        p = line.split("\t")
        if p[0] == "CAL":
            cal.append({"sense": p[1], "task": p[2], "variant": p[3], "logical": p[4], "C": int(p[5])})
        elif p[0] == "TEST":
            test.append({"sense": p[1], "task": p[2], "variant": p[3], "logical": p[4], "C": int(p[5]), "V": int(p[6])})
    return cal, test

def prep_truth_rows(man):
    """truth.json touched ONLY here, at score time. Returns (path, rows)."""
    truth = json.load(open(os.path.join(CORPUS, "truth.json")))
    keys = set()
    for r in man:
        if r["split"] == "test":
            for se in ("A", "B"):
                keys.add((se, r["task"], r["variant"], r["task"] + "/" + base_of(r)))
    rows = []
    for k, v in truth.items():
        se, _ = k.split("/", 1)
        kk = (se, v["task"], v["variant"], v["stim"])
        if kk in keys:
            rows.append({"sense": se, "task": v["task"], "variant": v["variant"],
                         "logical": v["stim"], "Y": 1 if v["correct"] else 0,
                         "kb4idx": v["stim_idx"]})
    rows.sort(key=lambda r: (r["sense"], r["task"], r["logical"]))
    path = os.path.join(CHAN, "out_tcp", "truth_rows.txt")
    with open(path, "w") as f:
        for r in rows:
            f.write("%s\t%s\t%s\t%s\t%d\t%d\n" % (
                r["sense"], r["task"], r["variant"], r["logical"], r["Y"], r["kb4idx"]))
    return path, rows

def base_of(r):
    b = r["relpath"].rsplit("/", 1)[-1]
    if b.endswith(".img"):
        b = b[:-4]
    return b

def run_zag_scorer(verdicts, truth_rows):
    q = subprocess.run([SCORER, verdicts, truth_rows], capture_output=True, text=True)
    if q.returncode != 0:
        raise RuntimeError("score_tcp failed: %s" % q.stdout.strip())
    out = {"sense": {}, "cell": {}, "pooled": {}, "done": None}
    for line in q.stdout.splitlines():
        p = line.split("\t")
        if p[0] == "SENSE":
            d = dict(zip(p[2::2], map(int, p[3::2])))
            out["sense"][p[1]] = d
        elif p[0] == "CELL":
            d = dict(zip(p[3::2], map(int, p[4::2])))
            out["cell"][(p[1], p[2])] = d
        elif p[0] == "POOLED":
            out["pooled"] = dict(zip(p[1::2], map(int, p[2::2])))
        elif p[0] == "DONE":
            out["done"] = int(p[1])
    return out

def recompute(cal, test, trows):
    """Independent recompute of every Zag-emitted count. Same layout."""
    tmap = {(r["sense"], r["task"], r["logical"]): r["Y"] for r in trows}
    for r in test:
        k = (r["sense"], r["task"], r["logical"])
        assert k in tmap, "truth join failed in recompute: %s" % (k,)
        r["Y"] = tmap[k]
    z = {"sense": {"A": {}, "B": {}}, "cell": {}, "pooled": {}, "done": len(test)}
    def zero():
        return {"n": 0, "c": 0, "v1y1": 0, "v1y0": 0, "v0y1": 0, "v0y0": 0, "caln": 0, "calc": 0}
    def zero_cell():
        return {"n": 0, "c": 0, "ny1": 0, "cy1": 0, "ny0": 0, "cy0": 0, "caln": 0, "calc": 0}
    for s in ("A", "B"):
        z["sense"][s] = zero()
        for t in TASKS:
            z["cell"][(s, t)] = zero_cell()
    zp = {"n": 0, "c": 0, "ny1": 0, "cy1": 0, "ny0": 0, "cy0": 0,
          "v1y1": 0, "v1y0": 0, "v0y1": 0, "v0y0": 0, "caln": 0, "calc": 0}
    for r in cal:
        s, t, c = r["sense"], r["task"], r["C"]
        z["cell"][(s, t)]["caln"] += 1
        z["cell"][(s, t)]["calc"] += c
        z["sense"][s]["caln"] += 1
        z["sense"][s]["calc"] += c
        zp["caln"] += 1
        zp["calc"] += c
    for r in test:
        s, t, c, v, y = r["sense"], r["task"], r["C"], r["V"], r["Y"]
        cell = z["cell"][(s, t)]
        se = z["sense"][s]
        cell["n"] += 1; cell["c"] += c
        se["n"] += 1; se["c"] += c
        zp["n"] += 1; zp["c"] += c
        if y == 1:
            cell["ny1"] += 1; cell["cy1"] += c
            zp["ny1"] += 1; zp["cy1"] += c
        else:
            cell["ny0"] += 1; cell["cy0"] += c
            zp["ny0"] += 1; zp["cy0"] += c
        if v == 1 and y == 1:
            se["v1y1"] += 1; zp["v1y1"] += 1
        elif v == 1 and y == 0:
            se["v1y0"] += 1; zp["v1y0"] += 1
        elif v == 0 and y == 1:
            se["v0y1"] += 1; zp["v0y1"] += 1
        else:
            se["v0y0"] += 1; zp["v0y0"] += 1
    z["pooled"] = zp
    return z

def cross_check(zag, ind):
    errs = []
    for s in ("A", "B"):
        for k, v in ind["sense"][s].items():
            if zag["sense"][s].get(k) != v:
                errs.append(("SENSE", s, k, zag["sense"][s].get(k), v))
    for k, cell in ind["cell"].items():
        for kk, v in cell.items():
            if zag["cell"][k].get(kk) != v:
                errs.append(("CELL", k, kk, zag["cell"][k].get(kk), v))
    for k, v in ind["pooled"].items():
        if zag["pooled"].get(k) != v:
            errs.append(("POOLED", k, zag["pooled"].get(k), v))
    if zag["done"] != ind["done"]:
        errs.append(("DONE", zag["done"], ind["done"]))
    return errs

def parse_champion():
    """(a)+(c) champion TEST verdicts: (sense, kb4idx) -> vac in {0,1,2}."""
    champ = {}
    for se in ("A", "B"):
        for line in open(os.path.join(CHAMP, "out_%s.txt" % se)):
            p = line.rstrip("\n").split("\t")
            if p[0] == "F":
                stim = int(p[1])
                vac = int(p[12])
                champ[(se, stim)] = vac
    return champ

def main():
    outdir = os.path.join(CHAN, "out_tcp")
    man = json.load(open(os.path.join(CHAN, "inputs_tcp", "blob_manifest.json")))
    r1v = os.path.join(outdir, "run1", "verdicts.txt")
    r2v = os.path.join(outdir, "run2", "verdicts.txt")
    r1s = open(os.path.join(outdir, "run1", "transform_sha256.txt"), "rb").read()
    r2s = open(os.path.join(outdir, "run2", "transform_sha256.txt"), "rb").read()
    r1b = open(r1v, "rb").read()
    r2b = open(r2v, "rb").read()
    result = {"two_run_check": {}}
    result["two_run_check"]["verdict_lines_identical"] = (r1b == r2b)
    result["two_run_check"]["transform_sha256_identical"] = (r1s == r2s)
    if r1b != r2b or r1s != r2s:
        result["void"] = "run1/run2 mismatch"
        json.dump(result, open(os.path.join(CHAN, "scores_tcp.json"), "w"), indent=1)
        print("VOID: run1/run2 mismatch")
        return 2

    # ---- F3 gate: voided senses contribute nothing downstream ----
    truth_rows, trows = prep_truth_rows(man)
    cal_all, test_all = parse_verdicts(r1v)
    zag_full = run_zag_scorer(r1v, truth_rows)
    ind_full = recompute(cal_all, test_all, trows)
    errs = cross_check(zag_full, ind_full)
    result["cross_check"] = {"n_errors": len(errs), "errors": errs[:20]}
    if errs:
        result["void"] = "Zag/Python count mismatch"
        json.dump(result, open(os.path.join(CHAN, "scores_tcp.json"), "w"), indent=1)
        print("VOID: count cross-check failed: %s" % (errs[:5],))
        return 3

    def f3_pass(q):
        return (q["calc"] / q["caln"]) >= 0.95 and q["calc"] >= 89
    f3 = {"A": f3_pass(zag_full["sense"]["A"]), "B": f3_pass(zag_full["sense"]["B"])}
    voided = [s for s in ("A", "B") if not f3[s]]
    result["F3"] = {"A": f3["A"], "B": f3["B"], "voided_senses": voided}
    if len(voided) == 2:
        result["void"] = "F3: both senses failed the calibration gate"
        json.dump(result, open(os.path.join(CHAN, "scores_tcp.json"), "w"), indent=1)
        print("VOID: both senses failed F3")
        return 4
    if voided:
        # filtered verdicts, still counted by Zag (per prereg: pure Zag counting)
        fv = os.path.join(CHAN, "out_tcp", "verdicts_filtered.tsv")
        with open(fv, "w") as f:
            for r in cal_all:
                if f3[r["sense"]]:
                    f.write("CAL\t%s\t%s\t%s\t%s\t%d\n" % (
                        r["sense"], r["task"], r["variant"], r["logical"], r["C"]))
            for r in test_all:
                if f3[r["sense"]]:
                    f.write("TEST\t%s\t%s\t%s\t%s\t%d\t%d\n" % (
                        r["sense"], r["task"], r["variant"], r["logical"], r["C"], r["V"]))
        zag = run_zag_scorer(fv, truth_rows)
        cal = [r for r in cal_all if f3[r["sense"]]]
        test = [r for r in test_all if f3[r["sense"]]]
    else:
        zag = zag_full
        cal, test = cal_all, test_all

    # ---- metrics from the (verified) counts ----
    def ratio(a, b):
        return (a / b) if b else None
    met = {}
    p = zag["pooled"]
    bits = mi_2x2([[p["v0y0"], p["v0y1"]], [p["v1y0"], p["v1y1"]]]) if p["n"] else None
    met["pooled"] = {
        "n_test": p["n"],
        "P_C": ratio(p["c"], p["n"]),
        "P_C_given_Y1": ratio(p["cy1"], p["ny1"]),
        "P_C_given_Y0": ratio(p["cy0"], p["ny0"]),   # F2-primary
        "bits": bits,
        "resolution_accuracy": ratio(p["v1y1"] + p["v0y0"], p["n"]),
        "false_install_rate": ratio(p["v1y0"], p["v1y1"] + p["v1y0"]),
        "H_adv_correct": entropy(ratio(p["ny1"], p["n"])),
        "n_correct": p["ny1"],
    }
    met["sense"] = {}
    for s in ("A", "B"):
        q = zag["sense"][s]
        # per-sense Y-conditional counts from Zag CELL counts
        sny1 = scy1 = sny0 = scy0 = 0
        for t in TASKS:
            cell = zag["cell"][(s, t)]
            sny1 += cell["ny1"]; scy1 += cell["cy1"]
            sny0 += cell["ny0"]; scy0 += cell["cy0"]
        cal_pc = ratio(q["calc"], q["caln"])
        bits = mi_2x2([[q["v0y0"], q["v0y1"]], [q["v1y0"], q["v1y1"]]]) if q["n"] else None
        met["sense"][s] = {
            "n_test": q["n"],
            "F3_cal_consistency": cal_pc,
            "F3_pass": cal_pc is not None and cal_pc >= 0.95 and q["calc"] >= 89,
            "P_C": ratio(q["c"], q["n"]),
            "P_C_given_Y1": ratio(scy1, sny1),
            "P_C_given_Y0": ratio(scy0, sny0),
            "bits": bits,
            "resolution_accuracy": ratio(q["v1y1"] + q["v0y0"], q["n"]),
            "false_install_rate": ratio(q["v1y0"], q["v1y1"] + q["v1y0"]),
        }
    # per-(sense,task) consistency table + vacuity (A2)
    met["cells"] = {}
    vacuous = []
    for s in ("A", "B"):
        for t in TASKS:
            cell = zag["cell"][(s, t)]
            cal_pc = ratio(cell["calc"], cell["caln"])
            test_pc = ratio(cell["c"], cell["n"])
            vac = (cal_pc == 1.0) and (test_pc is not None) and (test_pc >= 0.95)
            if vac:
                vacuous.append([s, t])
            met["cells"]["%s/%s" % (s, t)] = {
                "cal_P_C": cal_pc, "test_P_C": test_pc,
                "P_C_given_Y1": ratio(cell["cy1"], cell["ny1"]),
                "P_C_given_Y0": ratio(cell["cy0"], cell["ny0"]),
                "n": cell["n"], "vacuous": vac,
            }
    met["vacuous_cells"] = vacuous
    # F2-A2: P(C|Y=0) over non-vacuous cells
    nv_cy0 = nv_ny0 = 0
    for s in ("A", "B"):
        for t in TASKS:
            if [s, t] in vacuous:
                continue
            cell = zag["cell"][(s, t)]
            nv_cy0 += cell["cy0"]; nv_ny0 += cell["ny0"]
    met["F2_primary"] = met["pooled"]["P_C_given_Y0"]
    met["F2_A2"] = ratio(nv_cy0, nv_ny0)
    met["F2_A2_n"] = nv_ny0

    # ---- A1: stacking vs frozen (a)+(c) champion ----
    champ = parse_champion()
    tmap = {(r["sense"], r["kb4idx"]): r["Y"] for r in trows}
    rows = []
    for r in test:
        kb = next(x["kb4idx"] for x in trows
                  if x["sense"] == r["sense"] and x["task"] == r["task"] and x["logical"] == r["logical"])
        cv = champ.get((r["sense"], kb))
        assert cv is not None, (r["sense"], kb)
        rows.append((cv, r["V"], tmap[(r["sense"], kb)]))
    # joint MI over product alphabet (champ 0/1/2 x C2 0/1)
    N = len(rows)
    joint = {}
    for cv, v, y in rows:
        joint[(cv, v, y)] = joint.get((cv, v, y), 0) + 1
    jmi = 0.0
    marg_x = {}
    marg_y = {0: 0, 1: 0}
    for (cv, v, y), n_ in joint.items():
        marg_x[(cv, v)] = marg_x.get((cv, v), 0) + n_
        marg_y[y] += n_
    for (cv, v, y), n_ in joint.items():
        jmi += (n_ / N) * math.log2((n_ / N) / ((marg_x[(cv, v)] / N) * (marg_y[y] / N)))
    # reference: champion-alone bits on the same (filtered) rows
    marg_c = {}
    for (cv, v, y), n_ in joint.items():
        marg_c[cv] = marg_c.get(cv, 0) + n_
    cmi = 0.0
    for (cv, v, y), n_ in joint.items():
        cmi += (n_ / N) * math.log2((n_ / N) / ((marg_c[cv] / N) * (marg_y[y] / N)))
    met["A1"] = {
        "joint_bits": jmi,
        "champion_bits_frozen": CHAMP_BITS,
        "champion_bits_same_rows": cmi,
        "incremental_bits": jmi - CHAMP_BITS,
        "incremental_bits_same_rows": jmi - cmi,
        "n": N,
    }
    result["metrics"] = met
    result["counts"] = {"pooled": zag["pooled"], "sense": zag["sense"]}
    result["counts_full"] = {"pooled": zag_full["pooled"], "sense": zag_full["sense"]}
    json.dump(result, open(os.path.join(CHAN, "scores_tcp.json"), "w"), indent=1)
    print(json.dumps(met, indent=1))
    return 0

if __name__ == "__main__":
    sys.exit(main())
