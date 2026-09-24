#!/usr/bin/env python3
"""FAIR FIGHT legs S1..S4 vs a_raw/sense (autopilot control).

Chunked: --tasks colordisc,colorconst  --run2 1  --slice 0:60
S1 throughput: episodes/sec (bulk clear stimuli)
S2 latency floor: per-episode wall p50/p95 per task
S3 no-uncertainty: confidence distribution, frac conf>=950 & correct
S4 compute/episode: ops distribution (deterministic)
Byte-identity: run1 vs run2 sha of full stdout (when --run2 1).

Appends per-episode rows to evidence/autopilot_legs/rows.jsonl.
Aggregate with aggregate.py when all chunks done.
"""
import json, os, subprocess, sys, time, hashlib

ROOT = os.path.dirname(os.path.abspath(__file__))
SENSE = os.path.normpath(os.path.join(ROOT, "..", "tnn-lab", "senses", "rebuild", "a_raw", "sense"))
FXP = os.path.normpath(os.path.join(ROOT, "..", "tnn-lab", "senses", "rebuild", "harness", "fixtures"))
FXN = os.path.join(ROOT, "fixtures", "test")
OUT = os.path.join(ROOT, "evidence", "autopilot_legs")
os.makedirs(OUT, exist_ok=True)

TASKS = {"colordisc": ("t1_colordisc", "img"),
         "colorconst": ("t2_colorconst", "img"),
         "shapetrans": ("t3_shapetrans", "img"),
         "pitchdisc": ("t4_pitchdisc", "pcm"),
         "timbredisc": ("t5_timbredisc", "pcm"),
         "motiondir": ("t6_motiondir", "vid")}
# new fairfight fixtures: explicit (task, legdir, filename) — each fixture is
# scored ONLY under its intended task (cross-task runs are meaningless)
NEW_FIXTURES = [
    ("pitchdisc", "omission", "om_p1.pcm"),
    ("pitchdisc", "omission", "om_p2.pcm"),
    ("pitchdisc", "omission", "om_p3.pcm"),
    ("pitchdisc", "omission", "om_p4.pcm"),
    ("timbredisc", "omission", "om_t1.pcm"),
    ("timbredisc", "omission", "om_t2.pcm"),
    ("motiondir", "inattentional", "ib_m1.vid"),
    ("motiondir", "inattentional", "ib_m2.vid"),
    ("pitchdisc", "ambiguity", "am_p1.pcm"),
    ("colordisc", "ambiguity", "am_c1.img"),
    ("colorconst", "illusion", "il_c1.img"),
    ("colorconst", "illusion", "il_c2.img"),
    ("pitchdisc", "redteam", "rt_p1.pcm"),
    ("colordisc", "redteam", "rt_c1.img"),
]

def parse_kv(stdout):
    kv = {}
    for line in stdout.splitlines():
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            kv[k.strip()] = v.strip()
    return kv

def read_truth(fx):
    try:
        with open(fx + ".truth") as f:
            for line in f:
                line = line.strip()
                if line.startswith("truth="):
                    return line.split("=", 1)[1]
    except FileNotFoundError:
        return None
    return None

def run_once(task, fx):
    t0 = time.perf_counter()
    p = subprocess.run([SENSE, task, fx], capture_output=True, text=True, timeout=600)
    dt = time.perf_counter() - t0
    return p.stdout, p.returncode, dt

def main():
    args = dict(a.split("=", 1) for a in sys.argv[1:] if "=" in a)
    tasks = args.get("tasks", "colordisc").split(",")
    run2 = args.get("run2", "1") == "1"
    newonly = args.get("newonly", "0") == "1"
    slo = args.get("slice", "0:1000000")
    lo, hi = (int(x) for x in slo.split(":"))
    rows_path = os.path.join(OUT, "rows.jsonl")
    for task in tasks:
        tdir, ext = TASKS[task]
        d = os.path.join(FXP, tdir, "primary")
        fixtures = sorted(f for f in os.listdir(d) if f.endswith("." + ext))
        # append new fairfight fixtures intended for this task
        newfx = [os.path.join(FXN, legdir, fn) for (t, legdir, fn) in NEW_FIXTURES if t == task]
        allfx = [os.path.join(d, f) for f in fixtures] + newfx
        if newonly:
            allfx = newfx
        chunk = allfx[lo:hi]
        print(f"{task}: {len(chunk)} fixtures (slice {lo}:{hi})", flush=True)
        with open(rows_path, "a") as out:
            for path in chunk:
                o1, rc1, dt1 = run_once(task, path)
                h1 = hashlib.sha256(o1.encode()).hexdigest()
                bi = None
                dt2 = 0.0
                if run2:
                    o2, rc2, dt2 = run_once(task, path)
                    h2 = hashlib.sha256(o2.encode()).hexdigest()
                    bi = (h1 == h2) and rc1 == 0 and rc2 == 0
                if rc1 != 0:
                    print(f"  ERROR rc={rc1} {path} :: {o1[:120]}", flush=True)
                    continue
                kv = parse_kv(o1)
                truth = read_truth(path)
                row = {
                    "task": task,
                    "fixture": os.path.relpath(path, ROOT),
                    "judgment": kv.get("judgment"),
                    "confidence": int(kv.get("confidence", -1)),
                    "ops": int(kv.get("ops", -1)),
                    "truth": truth,
                    "correct": (kv.get("judgment") == truth),
                    "wall_s": dt1, "wall_s2": dt2,
                    "run2_checked": run2,
                    "byte_identical": bi,
                }
                out.write(json.dumps(row) + "\n")
                out.flush()
    print("done", flush=True)

if __name__ == "__main__":
    main()
