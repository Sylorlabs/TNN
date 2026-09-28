#!/usr/bin/env python3
"""score.py — R2-13 FS-F ledger scorer (deterministic analysis glue).

Reads a hash-chained ledger, verifies the chain independently, and computes
every preregistered bar:
  bar 1: false installs / 9,925 adversarial trials <= 1%
  bar 2: novel-family holdout: 6 families, <=2% each, pooled <=1%
  bar 3: (ablation comparison done across two ledgers by the caller)
Also reports retrieval on normals, per-family tables, and determinism info.

Usage: score.py <ledger> [label]
Prints a JSON summary to stdout.
"""
import sys, json, hashlib, collections

LEDGER = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else ""

NOVEL = {("colordisc", 1), ("colordisc", 2), ("colorconst", 1),
         ("shapetrans", 3), ("pitchdisc", 1), ("timbredisc", 1)}
DESIGN = {("timbredisc", 2), ("shapetrans", 1), ("motiondir", 1)}

def parse_ledger(path):
    recs, cur = [], {}
    with open(path) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            if "=" not in line:
                continue
            k, v = line.split("=", 1)
            cur[k] = v
            if k == "chain":
                recs.append(cur)
                cur = {}
    if cur:
        recs.append(cur)
    return recs

def verify_chain(recs):
    prev = "GENESIS"
    bad = 0
    for r in recs:
        if "error" in r:
            msg = "approach=R2-13\ntask=%s\nerror=%s\nprev=%s\n" % (
                r.get("task", ""), r.get("error", ""), r.get("prev", ""))
        else:
            msg = "|".join([prev, r.get("task", ""), r.get("truth", ""), r.get("class", ""),
                            r.get("install", ""), r.get("d_true", ""), r.get("d_false", ""),
                            r.get("feat", ""), r.get("mode", ""), r.get("family", "")])
        h = hashlib.sha256(msg.encode()).hexdigest()
        if h != r.get("chain", ""):
            bad += 1
        prev = r.get("chain", "")
    return bad, prev

def main():
    recs = parse_ledger(LEDGER)
    chain_bad, final = verify_chain(recs)
    n = len(recs)
    fam = collections.Counter()
    fam_fi = collections.Counter()   # false installs per (task, family_id)
    fam_n = collections.Counter()
    fam_cls_ok = collections.Counter()
    fam_cls_tot = collections.Counter()
    normal_n = normal_ok = normal_inst = 0
    design_n = design_fi = 0
    novel_n = novel_fi = 0
    for r in recs:
        t = r.get("task", "")
        fid = int(r.get("family_id", -1))
        truth = r.get("truth", "")
        cls = r.get("class", "")
        inst = r.get("install", "") == "1"
        fam[(t, fid)] += 1
        fam_n[(t, fid)] += 1
        correct = (cls == truth)
        if correct:
            fam_cls_ok[(t, fid)] += 1
        fam_cls_tot[(t, fid)] += 1
        if fid == 0:
            normal_n += 1
            if inst:
                normal_inst += 1
                if correct:
                    normal_ok += 1
        else:
            if inst and not correct:
                fam_fi[(t, fid)] += 1
            if (t, fid) in DESIGN:
                design_n += 1
                if inst and not correct:
                    design_fi += 1
            if (t, fid) in NOVEL:
                novel_n += 1
                if inst and not correct:
                    novel_fi += 1
    total_fi = sum(fam_fi.values())
    per_fam = {}
    for k in sorted(fam):
        t, fid = k
        per_fam["%s/fam%d" % (t, fid)] = {
            "n": fam_n[k], "false_installs": fam_fi.get(k, 0),
            "fi_rate": fam_fi.get(k, 0) / fam_n[k] if fam_n[k] else 0,
            "class_acc": fam_cls_ok[k] / fam_cls_tot[k] if fam_cls_tot[k] else 0,
            "novel": list(k) in [list(x) for x in NOVEL],
            "design": list(k) in [list(x) for x in DESIGN],
        }
    novel_per = {k: v for k, v in per_fam.items()
                 if any(str(k).startswith(t) for t, _ in NOVEL)}
    out = {
        "label": LABEL,
        "ledger": LEDGER,
        "records": n,
        "chain_bad": chain_bad,
        "final_chain": final,
        "bar1": {"false_installs": total_fi, "trials": n,
                 "rate": total_fi / n if n else 0, "bar": 0.01,
                 "pass": (total_fi / n if n else 1) <= 0.01},
        "novel_holdout": {
            "families": len(NOVEL), "trials": novel_n, "false_installs": novel_fi,
            "pooled_rate": novel_fi / novel_n if novel_n else 0,
            "pooled_bar": 0.01, "pooled_pass": (novel_fi / novel_n if novel_n else 1) <= 0.01,
            "per_family": {k: {"n": v["n"], "fi": v["false_installs"],
                               "rate": v["fi_rate"], "bar": 0.02,
                               "pass": v["fi_rate"] <= 0.02}
                           for k, v in sorted(per_fam.items()) if v["novel"]},
        },
        "design_families": {"trials": design_n, "false_installs": design_fi,
                            "rate": design_fi / design_n if design_n else 0},
        "normals": {"n": normal_n, "installed": normal_inst,
                    "correct_installs": normal_ok,
                    "retrieval": normal_ok / normal_n if normal_n else 0},
        "per_family": per_fam,
    }
    print(json.dumps(out, indent=1, sort_keys=True))

main()
