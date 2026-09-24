#!/usr/bin/env python3
"""Speed legs S1-S4 analogues for F1/F2/F3 on the 370 primary fixtures.

F1: a_raw/sense <task> <fx> (task from CLI, as in the frozen S-legs).
F2/F3: router auto-detects task from the fixture; shapetrans primaries are
  EXCLUDED (the F2 router only handles pitch/timbre/colordisc/colorconst/
  motion — a documented mechanism limitation, not a run failure).

One full pass per arm + byte-identity recheck on every 10th fixture.
Peak RSS per episode via os.wait4. No fixture writes by the forks.
"""
import json, os, sys, time, hashlib, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.normpath(os.path.join(ROOT, "..", "..", "..", ".."))
FF = os.path.join(LAB, "senses", "conscious-perception")
FXP = os.path.join(LAB, "senses", "rebuild", "harness", "fixtures")
SENSE = os.path.join(LAB, "senses", "rebuild", "a_raw", "sense")
F2BIN = os.path.join(FF, "forks", "deliberative", "f2_bin")
F3BIN = os.path.join(ROOT, "f3", "f3_bin")
sys.path.insert(0, ROOT)
from run_three_arm import parse_kv, parse_verdict, rs_kind_for, TASKMAP  # noqa

TASKS = {"colordisc": ("t1_colordisc", "img"), "colorconst": ("t2_colorconst", "img"),
         "shapetrans": ("t3_shapetrans", "img"), "pitchdisc": ("t4_pitchdisc", "pcm"),
         "timbredisc": ("t5_timbredisc", "pcm"), "motiondir": ("t6_motiondir", "vid")}

def run_child(argv):
    t0 = time.perf_counter()
    p = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pid, status, ru = os.wait4(p.pid, 0)
    dt = time.perf_counter() - t0
    out = p.stdout.read().decode("utf-8", "replace")
    return out, os.waitstatus_to_exitcode(status), dt, int(ru.ru_maxrss)

def f1_row(task, fx):
    out, rc, dt, rss = run_child([SENSE, task, fx])
    kv = parse_kv(out)
    return {"judgment": kv.get("judgment"), "confidence": int(kv.get("confidence", -1)),
            "ops": int(kv.get("ops", -1)), "resense": 0, "rs_ops": 0,
            "rc": rc, "wall_s": dt, "rss_kb": rss,
            "out_sha": hashlib.sha256(out.encode()).hexdigest()}

def fxf_row(task, fx, binary, tag, outdir, i):
    pre = os.path.join(outdir, "spd_%s_%04d" % (tag, i))
    out, rc, dt, rss = run_child([binary, fx, pre, "100000"])
    vp = pre + ".verdict"
    kv = parse_verdict(vp) if os.path.exists(vp) else {}
    vtask = TASKMAP.get(kv.get("task", ""), "?")
    rounds = int(kv.get("rounds", 0))
    sels = [int(x) for x in kv.get("selectors", "").split(",") if x.strip().isdigit()]
    return {"judgment": kv.get("final"), "confidence": int(kv.get("finalconf", -1)),
            "ops": int(kv.get("ops_total", -1)), "resense": 1 if rounds > 0 else 0,
            "rs_ops": int(kv.get("ops_p2", 0)), "rs_kind": rs_kind_for(vtask, sels),
            "detected_task": vtask, "rounds": rounds,
            "p1": kv.get("p1"), "p1ops": int(kv.get("p1ops", -1)),
            "rc": rc, "wall_s": dt, "rss_kb": rss,
            "out_sha": hashlib.sha256(open(vp, "rb").read()).hexdigest() if os.path.exists(vp) else None}

def main():
    outdir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "runs", "speed")
    os.makedirs(outdir, exist_ok=True)
    arms = sys.argv[2].split(",") if len(sys.argv) > 2 else ["F1", "F2", "F3"]
    fixtures = []
    for task, (tdir, ext) in TASKS.items():
        d = os.path.join(FXP, tdir, "primary")
        for f in sorted(os.listdir(d)):
            if f.endswith("." + ext):
                fixtures.append((task, os.path.join(d, f)))
    print("fixtures:", len(fixtures), flush=True)
    w = open(os.path.join(outdir, "speed_rows.jsonl"), "w")
    n = 0
    for (task, fx) in fixtures:
        for arm in arms:
            if arm in ("F2", "F3") and task == "shapetrans":
                continue  # router limitation, documented
            if arm == "F1":
                r = f1_row(task, fx)
            else:
                r = fxf_row(task, fx, F2BIN if arm == "F2" else F3BIN, arm, outdir, n)
            r.update({"arm": arm, "task": task, "fixture": os.path.basename(fx)})
            if n % 10 == 0:  # byte-identity recheck on every 10th (arm, fixture)
                if arm == "F1":
                    r2 = f1_row(task, fx)
                else:
                    r2 = fxf_row(task, fx, F2BIN if arm == "F2" else F3BIN, arm + "x", outdir, n)
                r["byte_identical"] = (r["out_sha"] == r2["out_sha"])
            w.write(json.dumps(r) + "\n"); w.flush()
        n += 1
        if n % 20 == 0:
            print("  %d/%d" % (n, len(fixtures)), flush=True)
    w.close()
    print("done", flush=True)

if __name__ == "__main__":
    main()
