#!/usr/bin/env python3
"""Parallel binary runner: runs A and B binaries over a dataset dir once,
parses stdout (scores, judgments, confidence, ops, instrument lines),
reads truths, writes one JSON line per (fixture, approach).

Output records are sorted by (fixture, approach) -> deterministic.
Usage: run_all.py <dataset_root> <out_jsonl> <variants_csv>
  dataset_root: contains t1_colordisc/ ... t6_motiondir/ subdirs
  variants_csv: e.g. "primary" or "adversarial"
"""
import json, os, subprocess, sys
from multiprocessing import Pool

A_BIN = "/home/hatch/workspace/senses-rebuild/a_raw/sense"
B_BIN = "/home/hatch/workspace/senses-rematch/b_inst/sense"
TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]
TDIRS = {"colordisc": "t1_colordisc", "colorconst": "t2_colorconst",
         "shapetrans": "t3_shapetrans", "pitchdisc": "t4_pitchdisc",
         "timbredisc": "t5_timbredisc", "motiondir": "t6_motiondir"}

def parse_stdout(stdout):
    kv = {}
    for line in stdout.splitlines():
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            kv[k.strip()] = v.strip()
    return kv

def parse_debug_vec(kv):
    d = {}
    dv = kv.get("debug_vec", "")
    for part in dv.split(";"):
        part = part.strip()
        if "=" in part:
            k, v = part.split("=", 1)
            try:
                d[k.strip()] = int(v.strip())
            except ValueError:
                d[k.strip()] = v.strip()
    return d

def work(args):
    approach, task, fixture = args
    binary = A_BIN if approach == "A" else B_BIN
    try:
        p = subprocess.run([binary, task, fixture], capture_output=True,
                           text=True, timeout=300)
    except subprocess.TimeoutExpired:
        return {"approach": approach, "task": task, "fixture": fixture,
                "error": "timeout"}
    if p.returncode != 0:
        return {"approach": approach, "task": task, "fixture": fixture,
                "error": "exit=%d out=%r" % (p.returncode, p.stdout[:150])}
    kv = parse_stdout(p.stdout)
    rec = {"approach": approach, "task": task, "fixture": fixture,
           "judgment": kv.get("judgment"), "confidence": int(kv.get("confidence", -1)),
           "ops": int(kv.get("ops", -1))}
    if approach == "A":
        rec["scores"] = parse_debug_vec(kv)
    else:
        b = {}
        for k in ("percept", "percept2", "shape_curv", "shape_sym",
                  "timbre_ev", "timbre_crest", "timbre_bright", "timbre_form",
                  "motion_mcount", "motion_dx", "motion_dy", "motion_spd"):
            if k in kv:
                try:
                    b[k] = int(kv[k])
                except ValueError:
                    b[k] = kv[k]
        rec["scores"] = b
    return rec

def main():
    root, out, variants = sys.argv[1], sys.argv[2], sys.argv[3].split(",")
    jobs = []
    for task in TASKS:
        td = os.path.join(root, TDIRS[task])
        for variant in variants:
            vd = os.path.join(td, variant)
            if not os.path.isdir(vd):
                continue
            for f in sorted(os.listdir(vd)):
                if f.endswith(".truth"):
                    continue
                fp = os.path.join(vd, f)
                rel = os.path.relpath(fp, root)
                for approach in ("A", "B"):
                    jobs.append((approach, task, fp))
    print("jobs: %d" % len(jobs), flush=True)
    with Pool(2) as pool:
        recs = pool.map(work, jobs, chunksize=8)
    # attach truths
    for r in recs:
        tf = r["fixture"] + ".truth"
        try:
            with open(tf) as fh:
                r["truth"] = fh.read().strip().split("=", 1)[1].strip()
        except Exception:
            r["truth"] = None
        r["rel"] = os.path.relpath(r["fixture"], root)
    recs.sort(key=lambda r: (r["rel"], r["approach"]))
    errs = sum(1 for r in recs if "error" in r)
    with open(out, "w") as f:
        for r in recs:
            f.write(json.dumps(r) + "\n")
    print("wrote %d records, errors %d -> %s" % (len(recs), errs, out), flush=True)
    if errs:
        for r in recs:
            if "error" in r:
                print("ERR", r["rel"], r["approach"], r["error"], flush=True)

main()
