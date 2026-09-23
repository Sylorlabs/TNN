#!/usr/bin/env python3
"""F2 appeal battery scorer (glue only). PREREG_FROZEN_F2APPEAL.md §5.

At score time ONLY: builds truth_rows.txt from truth.json. For each member
verdict file: 2-run byte-identity check (verdict lines + generation SHA256s),
pure-Zag contingency counts (score_tcp binary), independent Python recompute
(0 mismatches required), MI/bits + rates, RECOVERY bar evaluation.

Members: R1 levels L0..L6; R2 configs L3/L5; R3 transforms vflip/signflip/fshift
(per valid (sense,transform) cell); R4 variants V1/V2.

Outputs: scores_f2.json, brief_r1.txt, brief_r2.txt, brief_r3.txt, brief_r4.txt.
truth.json is opened ONLY here, at score time.
"""
import json, math, os, subprocess, sys

CHAN = os.path.dirname(os.path.abspath(__file__))
TN = os.path.expanduser("~/workspace/tnn-lab")
CORPUS = os.path.join(TN, "prose-learning", "epistemic_wave", "kb4_rerun")
SCORER = os.path.join(CHAN, "build", "score_tcp")
TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]

def mi_2x2(c):
    N = sum(sum(row) for row in c)
    if N == 0:
        return 0.0
    mi = 0.0
    for v in (0, 1):
        for y in (0, 1):
            if c[v][y] > 0:
                mi += (c[v][y] / N) * math.log2((c[v][y] / N) / ((sum(c[v]) / N) * ((c[0][y] + c[1][y]) / N)))
    return mi

def entropy_prior(trows):
    n = len(trows)
    if n == 0:
        return 0.0
    p1 = sum(1 for r in trows if r["Y"] == 1) / n
    if p1 in (0.0, 1.0):
        return 0.0
    return -(p1 * math.log2(p1) + (1 - p1) * math.log2(1 - p1))

def base_of(r):
    b = r["relpath"].rsplit("/", 1)[-1]
    if b.endswith(".img"):
        b = b[:-4]
    return b

def prep_truth_rows(man):
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
    path = os.path.join(CHAN, "truth_rows_f2.txt")
    with open(path, "w") as f:
        for r in rows:
            f.write("%s\t%s\t%s\t%s\t%d\t%d\n" % (
                r["sense"], r["task"], r["variant"], r["logical"], r["Y"], r["kb4idx"]))
    return path, rows

def parse_verdicts(vpath):
    cal, test = [], []
    for line in open(vpath):
        p = line.rstrip("\n").split("\t")
        if p[0] == "CAL" and len(p) >= 6:
            cal.append({"sense": p[1], "task": p[2], "logical": p[4], "C": int(p[5])})
        elif p[0] == "TEST" and len(p) >= 7:
            test.append({"sense": p[1], "task": p[2], "logical": p[4], "C": int(p[5]), "V": int(p[6])})
    return cal, test

def run_zag_scorer(verdicts, truth_rows):
    q = subprocess.run([SCORER, verdicts, truth_rows], capture_output=True, text=True)
    if q.returncode != 0:
        raise RuntimeError("score_tcp failed: %s" % q.stdout.strip())
    out = {"sense": {}, "cell": {}, "pooled": {}, "done": None}
    for line in q.stdout.splitlines():
        p = line.split("\t")
        if p[0] == "SENSE":
            out["sense"][p[1]] = dict(zip(p[2::2], map(int, p[3::2])))
        elif p[0] == "CELL":
            out["cell"][(p[1], p[2])] = dict(zip(p[3::2], map(int, p[4::2])))
        elif p[0] == "POOLED":
            out["pooled"] = dict(zip(p[1::2], map(int, p[2::2])))
        elif p[0] == "DONE":
            out["done"] = int(p[1])
    return out

def recompute(cal, test, trows):
    tmap = {(r["sense"], r["task"], r["logical"]): r["Y"] for r in trows}
    for r in test:
        k = (r["sense"], r["task"], r["logical"])
        assert k in tmap, "truth join failed: %s" % (k,)
        r["Y"] = tmap[k]
    def zero():
        return {"n": 0, "c": 0, "v1y1": 0, "v1y0": 0, "v0y1": 0, "v0y0": 0, "caln": 0, "calc": 0}
    def zero_cell():
        return {"n": 0, "c": 0, "ny1": 0, "cy1": 0, "ny0": 0, "cy0": 0, "caln": 0, "calc": 0}
    z = {"sense": {"A": zero(), "B": zero()}, "cell": {}, "pooled": {}, "done": len(test)}
    for s in ("A", "B"):
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

def metrics_from_counts(d):
    n = d["n"]
    c2x2 = [[d["v0y0"], d["v0y1"]], [d["v1y0"], d["v1y1"]]]
    bits = mi_2x2(c2x2)
    acc = (d["v1y1"] + d["v0y0"]) / n if n else 0.0
    fi_denom = d["v1y1"] + d["v1y0"]
    fi = d["v1y0"] / fi_denom if fi_denom else 0.0
    # P(agree|Y) filled by the caller from cell sums (sense level) or from
    # the pooled ny/cy counts (pooled level)
    p_agree_y1 = (d["cy1"] / d["ny1"]) if d.get("ny1") else None
    p_agree_y0 = (d["cy0"] / d["ny0"]) if d.get("ny0") else None
    return {"n": n, "bits": bits, "resolution_accuracy": acc,
            "false_install": fi, "P_agree_Y1": p_agree_y1,
            "P_agree_Y0": p_agree_y0}

def main():
    man = json.load(open(os.path.join(CHAN, "..", "inputs_tcp", "blob_manifest.json")))
    members = []
    for lv in ["0", "1", "2", "3", "4", "5", "6"]:
        members.append(("R1", "L%s" % lv, "out_r1", "verdicts_L%s.txt" % lv, "noise_sha256_L%s.txt" % lv))
    for cfg in ["L3", "L5"]:
        members.append(("R2", cfg, "out_r2", "verdicts_%s.txt" % cfg, "noise_sha256_%s.txt" % cfg))
    for tr in ["vflip", "signflip", "fshift"]:
        members.append(("R3", tr, "out_r3", "verdicts_%s.txt" % tr, "transform_sha256_%s.txt" % tr))
    for va in ["1", "2"]:
        members.append(("R4", "V%s" % va, "out_r4", "verdicts_V%s.txt" % va, "noise_sha256_V%s.txt" % va))
    result = {"members": {}, "two_run_check": {}, "cross_check_errors": 0, "recovery_fires": []}
    truth_rows, trows = prep_truth_rows(man)
    result["H_Y_prior"] = entropy_prior([r for r in trows])
    for test, cfg, outdir, vfile, sfile in members:
        key = "%s-%s" % (test, cfg)
        r1v = os.path.join(CHAN, outdir, "run1", vfile)
        r2v = os.path.join(CHAN, outdir, "run2", vfile)
        r1s = os.path.join(CHAN, outdir, "run1", sfile)
        r2s = os.path.join(CHAN, outdir, "run2", sfile)
        entry = {"config": cfg}
        vb1 = open(r1v, "rb").read(); vb2 = open(r2v, "rb").read()
        sb1 = open(r1s, "rb").read(); sb2 = open(r2s, "rb").read()
        entry["verdict_lines_identical"] = (vb1 == vb2)
        entry["gen_sha256_identical"] = (sb1 == sb2)
        result["two_run_check"][key] = {"verdict": vb1 == vb2, "gen": sb1 == sb2}
        if vb1 != vb2 or sb1 != sb2:
            entry["void"] = "run1/run2 mismatch"
            result["members"][key] = entry
            continue
        cal, tst = parse_verdicts(r1v)
        zag = run_zag_scorer(r1v, truth_rows)
        ind = recompute(cal, tst, trows)
        errs = cross_check(zag, ind)
        entry["cross_check_errors"] = len(errs)
        result["cross_check_errors"] += len(errs)
        if errs:
            entry["void"] = "cross-check errors: %s" % (errs[:3],)
            result["members"][key] = entry
            continue
        # per-sense metrics on TEST (P(agree|Y) summed from cells; sense-level
        # keys must stay identical to the Zag scorer's for cross_check)
        for s in ("A", "B"):
            d = dict(ind["sense"][s])
            ny1 = sum(ind["cell"][(s, t)]["ny1"] for t in TASKS)
            cy1 = sum(ind["cell"][(s, t)]["cy1"] for t in TASKS)
            ny0 = sum(ind["cell"][(s, t)]["ny0"] for t in TASKS)
            cy0 = sum(ind["cell"][(s, t)]["cy0"] for t in TASKS)
            m = metrics_from_counts(d)
            m["P_agree_Y1"] = (cy1 / ny1) if ny1 else None
            m["P_agree_Y0"] = (cy0 / ny0) if ny0 else None
            entry["sense_%s" % s] = m
        # pooled = sum over senses of the TEST contingency (per-sense reported; either sense counts)
        p = dict(ind["pooled"])
        entry["pooled"] = metrics_from_counts(p)
        # calibration summary (R3 gate uses CAL rows)
        entry["cal_rate_A"] = (ind["sense"]["A"]["calc"] / ind["sense"]["A"]["caln"]) if ind["sense"]["A"]["caln"] else None
        entry["cal_rate_B"] = (ind["sense"]["B"]["calc"] / ind["sense"]["B"]["caln"]) if ind["sense"]["B"]["caln"] else None
        # RECOVERY bar: bits > 0.15 AND false-install < 0.15, pooled or either sense
        fires = []
        for scope in ("pooled", "sense_A", "sense_B"):
            m = entry[scope]
            if m["bits"] > 0.15 and m["false_install"] < 0.15 and m["n"] > 0:
                fires.append(scope)
        entry["recovery_bar"] = "FIRES" if fires else "null"
        entry["recovery_scopes"] = fires
        if fires:
            result["recovery_fires"].append(key)
        result["members"][key] = entry
    result["verdict_rule"] = ("NOT WRAPS" if result["recovery_fires"] else "WRAPS")
    json.dump(result, open(os.path.join(CHAN, "scores_f2.json"), "w"), indent=1)
    # briefs
    for test in ("R1", "R2", "R3", "R4"):
        lines = ["%s member summary (pooled TEST unless noted):" % test]
        for key in sorted(result["members"]):
            if key.startswith(test + "-"):
                e = result["members"][key]
                if "void" in e:
                    lines.append("  %s VOID: %s" % (key, e["void"]))
                    continue
                p, a, b = e["pooled"], e["sense_A"], e["sense_B"]
                lines.append("  %s pooled bits=%.4f fi=%.3f n=%d | A bits=%.4f fi=%.3f | B bits=%.4f fi=%.3f | RECOVERY=%s" % (
                    key, p["bits"], p["false_install"], p["n"],
                    a["bits"], a["false_install"], b["bits"], b["false_install"], e["recovery_bar"]))
        open(os.path.join(CHAN, "brief_%s.txt" % test.lower()), "w").write("\n".join(lines) + "\n")
    print(json.dumps({"verdict_rule": result["verdict_rule"],
                      "recovery_fires": result["recovery_fires"],
                      "cross_check_errors": result["cross_check_errors"]}, indent=1))

if __name__ == "__main__":
    main()
