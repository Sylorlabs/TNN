#!/usr/bin/env python3
"""HARNESS-CREW runner: executes approach binaries over all fixtures.

Wait protocol: blocks until ../a_raw/DONE and ../b_percept/DONE exist.
Then for each (approach, task, variant, fixture): run `sense <task> <fixture>`,
capture stdout, validate required keys, record (judgment, confidence, ops).
Determinism (KB5): 10-fixture primary sample per task, 3 runs each, require
byte-identical stdout for BOTH approaches.

Output: results/raw_results.json
"""
import json, os, subprocess, sys, time, hashlib

ROOT = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(ROOT, "fixtures")
RES = os.path.join(ROOT, "results")
A_BIN = os.environ.get("SENSE_A", os.path.normpath(os.path.join(ROOT, "..", "a_raw", "sense")))
B_BIN = os.environ.get("SENSE_B", os.path.normpath(os.path.join(ROOT, "..", "b_percept", "sense")))

TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]
TDIRS = {"colordisc": "t1_colordisc", "colorconst": "t2_colorconst",
         "shapetrans": "t3_shapetrans", "pitchdisc": "t4_pitchdisc",
         "timbredisc": "t5_timbredisc", "motiondir": "t6_motiondir"}
VARIANTS = ["primary", "noise", "adversarial"]
VOCAB = {
    "colordisc": {"SAME", "DIFFERENT"},
    "colorconst": {"SAME_SURFACE", "DIFFERENT"},
    "shapetrans": {"CIRCLE", "TRIANGLE", "SQUARE"},
    "pitchdisc": {"SAME", "HIGHER", "LOWER"},
    "timbredisc": {"PURE", "BRIGHT", "DARK", "RICH"},
    "motiondir": {"STILL", "N", "NE", "E", "SE", "S", "SW", "W", "NW"},
}

def wait_for_crews(timeout_s=12 * 3600):
    t0 = time.time()
    need = [os.path.normpath(os.path.join(ROOT, "..", "a_raw", "DONE")),
            os.path.normpath(os.path.join(ROOT, "..", "b_percept", "DONE"))]
    while True:
        if all(os.path.exists(p) for p in need):
            return True
        if time.time() - t0 > timeout_s:
            return False
        time.sleep(30)

def parse_kv(stdout):
    kv = {}
    for line in stdout.splitlines():
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            kv[k.strip()] = v.strip()
    return kv

def run_once(binary, task, fixture):
    try:
        p = subprocess.run([binary, task, fixture], capture_output=True,
                           text=True, timeout=120)
    except subprocess.TimeoutExpired:
        return None, "timeout"
    kv = parse_kv(p.stdout)
    if p.returncode != 0:
        return None, "exit=%d stdout=%r" % (p.returncode, p.stdout[:200])
    return kv, None

def validate(approach_tag, task, kv):
    errs = []
    for k in ("approach", "task", "judgment", "confidence", "ops"):
        if k not in kv:
            errs.append("missing key %s" % k)
    if errs:
        return errs
    if kv["approach"] != approach_tag:
        errs.append("approach tag %r != %r" % (kv["approach"], approach_tag))
    if kv["task"] != task:
        errs.append("task tag %r != %r" % (kv["task"], task))
    if kv["judgment"] not in VOCAB[task]:
        errs.append("judgment %r not in vocab" % kv["judgment"])
    try:
        c = int(kv["confidence"])
        if not (0 <= c <= 1000):
            errs.append("confidence out of range")
    except ValueError:
        errs.append("confidence not int")
    try:
        o = int(kv["ops"])
        if o < 0:
            errs.append("ops negative")
    except ValueError:
        errs.append("ops not int")
    return errs

def main():
    skip_wait = "--no-wait" in sys.argv
    if not skip_wait:
        print("waiting for A/B crews...", flush=True)
        if not wait_for_crews():
            print("TIMEOUT waiting for DONE files", flush=True); sys.exit(2)
    os.makedirs(RES, exist_ok=True)
    bins = {"A": A_BIN, "B": B_BIN}
    for tag, b in bins.items():
        if not (os.path.exists(b) and os.access(b, os.X_OK)):
            print("FATAL: binary missing/not executable: %s" % b, flush=True)
            sys.exit(2)
    results = {"runs": [], "errors": [], "determinism": {}}
    det_fail = False
    for tag, binary in bins.items():
        det = {"samples": 0, "identical": 0, "failures": []}
        for task in TASKS:
            tdir = TDIRS[task]
            # determinism sample: first 10 primary fixtures, 3 runs each
            pdir = os.path.join(FIX, tdir, "primary")
            fps = sorted(f for f in os.listdir(pdir) if f.endswith((".img", ".pcm", ".vid")))[:10]
            for fn in fps:
                fx = os.path.join(pdir, fn)
                outs = []
                for r in range(3):
                    p = subprocess.run([binary, task, fx], capture_output=True,
                                       text=True, timeout=120)
                    outs.append(p.stdout)
                det["samples"] += 1
                if outs[0] == outs[1] == outs[2]:
                    det["identical"] += 1
                else:
                    det["failures"].append("%s/%s" % (task, fn))
                    det_fail = True
            # full sweep
            for variant in VARIANTS:
                vdir = os.path.join(FIX, tdir, variant)
                for fn in sorted(os.listdir(vdir)):
                    if not fn.endswith((".img", ".pcm", ".vid")):
                        continue
                    fx = os.path.join(vdir, fn)
                    kv, err = run_once(binary, task, fx)
                    rec = {"approach": tag, "task": task, "variant": variant,
                           "fixture": os.path.relpath(fx, FIX)}
                    if err:
                        rec["error"] = err
                        results["errors"].append(rec)
                        continue
                    rec["stdout_sha256"] = hashlib.sha256(kv and "".join(
                        "%s=%s\n" % (k, v) for k, v in sorted(kv.items())
                    ).encode() or b"").hexdigest()
                    verrs = validate(tag, task, kv)
                    if verrs:
                        rec["error"] = "; ".join(verrs)
                        rec["kv"] = kv
                        results["errors"].append(rec)
                        continue
                    rec["judgment"] = kv["judgment"]
                    rec["confidence"] = int(kv["confidence"])
                    rec["ops"] = int(kv["ops"])
                    if "percept" in kv:
                        rec["percept"] = kv["percept"]
                    if "percept2" in kv:
                        rec["percept2"] = kv["percept2"]
                    # ground truth
                    with open(fx + ".truth") as f:
                        rec["truth"] = f.read().strip().split("=", 1)[1]
                    rec["correct"] = rec["judgment"] == rec["truth"]
                    results["runs"].append(rec)
        results["determinism"][tag] = det
    with open(os.path.join(RES, "raw_results.json"), "w") as f:
        json.dump(results, f, indent=1)
    n_ok = len(results["runs"]); n_err = len(results["errors"])
    print("runs recorded: %d, errors: %d" % (n_ok, n_err), flush=True)
    print("determinism: %s" % json.dumps(results["determinism"], indent=1), flush=True)
    if det_fail:
        print("KB5 FAIL: nondeterministic outputs detected", flush=True)
    sys.exit(0)

if __name__ == "__main__":
    main()
