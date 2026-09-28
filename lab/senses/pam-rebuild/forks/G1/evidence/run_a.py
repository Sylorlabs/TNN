#!/usr/bin/env python3
"""Run Approach A on the identical fixture set as G1 (for B2 head-to-head).

Writes evidence/results/runA/raw_a.json with judgments per fixture.
Usage: run_a.py
"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from run_g1 import TASKS, ADV_PREFIX, VOCAB, truth_of, list_fixtures, parse_stdout  # noqa: E402

BASE = os.path.expanduser("~/workspace/tnn-lab/senses")
SENSE_A = os.path.expanduser("~/workspace/tmp_g1build/sense_a")
RES = os.path.join(BASE, "pam-rebuild", "forks", "G1", "evidence", "results")


def main():
    outdir = os.path.join(RES, "runA")
    os.makedirs(outdir, exist_ok=True)
    records = []
    n_err = 0
    for task, tdir, ext in TASKS:
        for path, pop in list_fixtures(task, tdir, ext):
            try:
                r = subprocess.run([SENSE_A, task, path],
                                   capture_output=True, timeout=900)
            except subprocess.TimeoutExpired:
                records.append({"task": task, "fixture": path, "pop": pop,
                                "error": "timeout"})
                n_err += 1
                continue
            if r.returncode != 0:
                records.append({"task": task, "fixture": path, "pop": pop,
                                "error": (r.stdout or b"").decode()[:120]})
                n_err += 1
                continue
            kv = parse_stdout(r.stdout)
            rec = {"task": task, "fixture": path, "pop": pop,
                   "truth": truth_of(path)}
            try:
                assert kv.get("approach") == "A", kv
                j = kv["judgment"]
                assert j in VOCAB[task], kv
                rec["judgment"] = j
                rec["confidence"] = int(kv["confidence"])
                rec["ops"] = int(kv["ops"])
                rec["correct"] = (j == rec["truth"])
            except Exception as e:  # noqa: BLE001
                rec["error"] = "bad_output: %s" % e
                n_err += 1
            records.append(rec)
        print("A: task %s done" % task, flush=True)
    with open(os.path.join(outdir, "raw_a.json"), "w") as f:
        json.dump({"approach": "A", "errors": n_err, "records": records}, f)
    print("A run: %d fixtures, %d errors" % (len(records), n_err))


if __name__ == "__main__":
    main()
