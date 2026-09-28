#!/usr/bin/env python3
"""G1 sweep runner (frozen by PREREG_G1.md section 7).

Runs every fixture through sense: all 6 tasks x harness primary fixtures
(sorted) + the 75 G1 adversarial fixtures, on a FRESH ledger per run.
Validates every output field. Writes evidence/results/run<N>/raw_g1.json.

Usage: run_g1.py <run_id>   (run_id = 1,2,3 for the determinism triple)
"""
import hashlib
import json
import os
import re
import subprocess
import sys

BASE = os.path.expanduser("~/workspace/tnn-lab/senses")
SENSE = os.path.expanduser("~/workspace/tmp_g1build/sense")
FIX = os.path.join(BASE, "rebuild", "harness", "fixtures")
ADV = os.path.join(BASE, "pam-rebuild", "forks", "G1", "evidence", "adv")
RES = os.path.join(BASE, "pam-rebuild", "forks", "G1", "evidence", "results")

TASKS = [
    ("colordisc", "t1_colordisc", "img"),
    ("colorconst", "t2_colorconst", "img"),
    ("shapetrans", "t3_shapetrans", "img"),
    ("pitchdisc", "t4_pitchdisc", "pcm"),
    ("timbredisc", "t5_timbredisc", "pcm"),
    ("motiondir", "t6_motiondir", "vid"),
]
ADV_PREFIX = {
    "colordisc": (),
    "colorconst": ("g1_t2_m3_",),
    "shapetrans": ("g1_t3_m1_", "g1_t3_m2_"),
    "pitchdisc": ("g1_t4_m4_",),
    "timbredisc": ("g1_t5_m5_",),
    "motiondir": ("g1_t6_m6_",),
}
VOCAB = {
    "colordisc": {"SAME", "DIFFERENT"},
    "colorconst": {"SAME_SURFACE", "DIFFERENT"},
    "shapetrans": {"CIRCLE", "SQUARE", "TRIANGLE"},
    "pitchdisc": {"SAME", "HIGHER", "LOWER"},
    "timbredisc": {"PURE", "DARK", "RICH", "BRIGHT"},
    "motiondir": {"STILL", "N", "NE", "E", "SE", "S", "SW", "W", "NW"},
}

HEX128 = re.compile(r"^[0-9a-f]{128}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def truth_of(path):
    with open(path + ".truth") as f:
        return f.read().strip().split("=", 1)[1]


def list_fixtures(task, tdir, ext):
    out = []
    d = os.path.join(FIX, tdir, "primary")
    for name in sorted(os.listdir(d)):
        if name.endswith("." + ext):
            p = os.path.join(d, name)
            out.append((p, "primary"))
    for pref in ADV_PREFIX[task]:
        for name in sorted(os.listdir(ADV)):
            if name.startswith(pref) and name.endswith("." + ext):
                p = os.path.join(ADV, name)
                out.append((p, "g1adv"))
    return out


def parse_stdout(raw):
    kv = {}
    for line in raw.decode("utf-8", "replace").splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            kv[k] = v
    return kv


def main():
    run_id = int(sys.argv[1])
    outdir = os.path.join(RES, "run%d" % run_id)
    leddir = os.path.join(outdir, "ledgers")
    os.makedirs(leddir, exist_ok=True)
    records = []
    n_err = 0
    for task, tdir, ext in TASKS:
        ledger = os.path.join(leddir, "sgp_%s.txt" % task)
        if os.path.exists(ledger):
            os.unlink(ledger)
        for path, pop in list_fixtures(task, tdir, ext):
            try:
                r = subprocess.run(
                    [SENSE, task, path, ledger],
                    capture_output=True, timeout=600)
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
                assert kv.get("approach") == "G1", kv
                assert kv.get("task") == task, kv
                j = kv["judgment"]
                assert j in VOCAB[task], kv
                rec["judgment"] = j
                rec["confidence"] = int(kv["confidence"])
                assert 0 <= rec["confidence"] <= 1000
                rec["ops"] = int(kv["ops"])
                assert rec["ops"] >= 0
                p = kv["percept"]
                assert HEX128.match(p), kv
                rec["percept"] = p
                d = kv["disposition"]
                assert d in ("INSTALL", "WITHHOLD"), kv
                rec["disposition"] = d
                rec["variance"] = int(kv["variance"])
                rec["anchor"] = int(kv["anchor"])
                lh = kv["ledger_hash"]
                assert HEX64.match(lh), kv
                rec["ledger_hash"] = lh
                rec["correct"] = (j == rec["truth"])
            except Exception as e:  # noqa: BLE001
                rec["error"] = "bad_output: %s :: %s" % (e, str(kv)[:200])
                n_err += 1
            records.append(rec)
    out = {"approach": "G1", "run": run_id, "errors": n_err,
           "records": records}
    op = os.path.join(outdir, "raw_g1.json")
    with open(op, "w") as f:
        json.dump(out, f)
    print("run %d: %d fixtures, %d errors -> %s" % (run_id, len(records),
                                                   n_err, op))


if __name__ == "__main__":
    main()
