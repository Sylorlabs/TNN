#!/usr/bin/env python3
"""Independent oracle for RSI-2 kill bars (KB1-KB6). Reads only artifacts."""
import json, re, sys, hashlib, os

LAB = os.path.expanduser("~/workspace/tnn-lab/rsi/rsi2")
RUNS = os.path.join(LAB, "runs")

def read(n):
    with open(os.path.join(RUNS, n)) as f: return f.read()

def batt_metric(txt, bid):
    m = re.search(r"RSI2_BATT,id=%s,metric=(-?\d+)" % bid, txt)
    return int(m.group(1)) if m else None

def main():
    res = {}
    diag = [read("diag_r%d.log" % r) for r in range(5)]
    d0 = diag[0]
    # determinism first (needed to trust d0 parses)
    det_d = len(set(hashlib.md5(d.encode()).hexdigest() for d in diag)) == 1
    vb = [read("verify_vbase_r%d.log" % r) for r in range(5)]
    vg = [read("verify_vgen_r%d.log" % r) for r in range(5)]
    vw = [read("verify_vwrong_r%d.log" % r) for r in range(5)]
    det_v = all(len(set(hashlib.md5(x.encode()).hexdigest() for x in g)) == 1 for g in (vb, vg, vw))
    res["KB5-DET"] = ("PASS" if (det_d and det_v) else "FAIL",
                      "diag 5/5 identical=%s verify 5/5 each=%s" % (det_d, det_v))

    # KB4: manifests + held-out integrity
    has_d = all(all(("RSI2_BATT,id=%s,metric=" % b) in d for b in ("D1","RECALL","COST")) and "RSI2_DONE" in d for d in diag)
    no_d2 = all("RSI2_BATT,id=D2,metric=" not in d for d in diag)
    has_v = all(all(("RSI2_BATT,id=%s,metric=" % b) in x for b in ("D1","D2","RECALL","COST")) and "RSI2_VERIFY_DONE" in x for x in vb[0:1]+vg[0:1]+vw[0:1])
    res["KB4-NOSKIP"] = ("PASS" if (has_d and no_d2 and has_v) else "FAIL",
                         "diag manifest=%s no-D2-in-diag=%s verify manifest=%s" % (has_d, no_d2, has_v))

    # predictions from diag
    preds = {}
    for m in re.finditer(r"RSI2_PRED,id=(P\d),target=([A-Z0-9-]+),lo=(-?\d+),hi=(-?\d+)", d0):
        preds[m.group(1)] = (m.group(2), int(m.group(3)), int(m.group(4)))
    fixm = re.search(r"RSI2_FIX,ops=([0-9+]+),targets=([A-Z+]+),analogy=A(\d),discount=(\d+),gap=(\d+),lo=(\d+),hi=(\d+)", d0)
    fixtext = re.search(r"RSI2_FIXTEXT,(.*)", d0).group(1) if "RSI2_FIXTEXT" in d0 else ""
    gap = int(fixm.group(5)) if fixm else None

    with open(os.path.join(LAB, "rsi2.zag")) as f: src = f.read()
    catalog_names = ["T-DENSE","T-PRIN-PRIORITY","T-DOMAIN3","T-QUIET-SKIP","T-AUDIT-TRIM","T-BAR-LOWER","T-GATE-SKIP"]
    not_catalog = not any(n in fixtext for n in catalog_names)
    pair_hits = len(re.findall(r"qi==\d&&qj==\d", src))
    res["KB1-INVENT"] = ("PASS" if (fixm and "+" in fixm.group(1) and not_catalog and pair_hits >= 6) else "FAIL",
                        "composition=%s not-catalog=%s qcompat-pairs=%d" % (fixm.group(1) if fixm else None, not_catalog, pair_hits))

    # actuals
    d2b, d2g, d2w = batt_metric(vb[0],"D2"), batt_metric(vg[0],"D2"), batt_metric(vw[0],"D2")
    rb, rg, rw = batt_metric(vb[0],"RECALL"), batt_metric(vg[0],"RECALL"), batt_metric(vw[0],"RECALL")
    cb, cg = batt_metric(vb[0],"COST"), batt_metric(vg[0],"COST")
    ag, aw = d2g-d2b, d2w-d2b
    p1 = preds.get("P1"); p2 = preds.get("P2")
    taut = (p1[1], p1[2]) == (gap, gap)
    width_ok = 0 < (p1[2]-p1[1]) < 8000
    in_range = p1[1] <= ag <= p1[2]
    res["KB2-CALIBRATE"] = ("PASS" if (in_range and width_ok and not taut and fixm) else "FAIL",
        "P1=[%d,%d] actual=%d in_range=%s width_ok=%s tautology=%s analogy=A%s" % (p1[1],p1[2],ag,in_range,width_ok,taut,fixm.group(3) if fixm else "?"))

    disc = (p1[1] > 500 and ag > 500 and p2[2] <= 500 and aw <= 500 and aw < ag)
    res["KB3-DISCRIMINATE"] = ("PASS" if disc else "FAIL",
        "genuine lo=%d>500 actual=%d>500; wrong hi=%d<=500 actual=%d<=500; wrong<genuine=%s" % (p1[1],ag,p2[2],aw,aw<ag))

    pj = os.path.join(LAB, "PREDICTIONS.json")
    pj_ok = os.path.exists(pj) and set(json.load(open(pj)).keys()) >= {"P1","P2","P3","P4","P5"}
    vd = os.path.join(LAB, "VERDICT2.md")
    vd_ok = os.path.exists(vd) and all(("P%d" % i) in open(vd).read() for i in range(1,6))
    res["KB6-HONEST"] = ("PASS" if (pj_ok and vd_ok) else "FAIL", "predictions.json=%s verdict-covers-P1..P5=%s" % (pj_ok, vd_ok))

    # per-prediction HIT/MISS table
    calls = {
        "P1": (p1, ag, p1[1] <= ag <= p1[2]),
        "P2": (p2, aw, p2[1] <= aw <= p2[2]),
        "P3": (preds.get("P3"), rg-rb, preds["P3"][1] <= rg-rb <= preds["P3"][2]),
        "P4": (preds.get("P4"), cg-cb, preds["P4"][1] <= cg-cb <= preds["P4"][2]),
        "P5": (preds.get("P5"), rw-rb, preds["P5"][1] <= rw-rb <= preds["P5"][2]),
    }
    print("RSI-2 ORACLE ADJUDICATION")
    for k, v in res.items(): print("%s: %s — %s" % (k, v[0], v[1]))
    print("\nPREDICTION HIT/MISS (all published):")
    allpass = all(v[0]=="PASS" for v in res.values())
    for pid, (pr, actual, hit) in calls.items():
        print("  %s target=%s predicted=[%d,%d] actual=%d -> %s" % (pid, pr[0], pr[1], pr[2], actual, "HIT" if hit else "MISS"))
    print("\nOVERALL:", "ALL KILL BARS PASS" if allpass else "FAIL — see bars")
    return 0 if allpass else 1

sys.exit(main())
