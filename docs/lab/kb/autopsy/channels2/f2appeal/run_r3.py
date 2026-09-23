#!/usr/bin/env python3
"""R3 alternative-transforms runner (glue only). PREREG_FROZEN_F2APPEAL.md §4-R3.

For pass in {1,2}, transform in {vflip, signflip, fshift}:
  (a) involution self-check: T(T(x)) byte-identical to x on all 185 fixtures
      (any failure -> that transform VOID for the affected task);
  (b) F3-style calibration gate per (sense, transform): P(C)>=95% on the 93
      calibration primaries, C:=[Jt==J] (J from the G0 cache). Fail -> that
      sense VOID for that transform;
  (c) TEST: 92 adversarials x valid senses; verdict INSTALL iff Jt==J via the
      pure-Zag channel_c3 binary.
Records transform-byte SHA256s + verdict lines (CAL rows for the gate,
TEST rows for scoring). 2 passes must be byte-identical.

Outputs: out_r3/run{N}/transform_sha256_{tr}.txt,
         out_r3/run{N}/verdicts_{tr}.txt, out_r3/run{N}/gate_{tr}.txt
"""
import hashlib, json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

CHAN = os.path.dirname(os.path.abspath(__file__))
TN = os.path.expanduser("~/workspace/tnn-lab")
FIXROOT = os.path.join(TN, "senses", "rebuild", "harness", "fixtures")
SENSE_A = os.path.join(TN, "senses", "rebuild", "a_raw", "sense")
SENSE_B = os.path.expanduser("~/workspace/kb4-f2/build_b/sense_b_rebuilt")
SENSES = {"A": SENSE_A, "B": SENSE_B}
BUILD = os.path.join(CHAN, "build")
ALT = os.path.join(BUILD, "alt_transform")
CHANNEL = os.path.join(BUILD, "channel_c3")
TMP = os.path.expanduser("~/workspace/tmp_f2appeal")
OUT = os.path.join(CHAN, "out_r3")
WORKERS = 12
TRANSFORMS = ["vflip", "signflip", "fshift"]
TR_TASKS = {"vflip": ["colordisc", "colorconst", "shapetrans"],
            "signflip": ["pitchdisc", "timbredisc"],
            "fshift": ["motiondir"]}

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def logical(task, relpath):
    base = relpath.rsplit("/", 1)[-1]
    if base.endswith(".img"):
        base = base[:-4]
    return "%s/%s" % (task, base)

def run_sense(spath, task, fx):
    q = subprocess.run([spath, task, fx], capture_output=True, text=True, timeout=120)
    if q.returncode != 0:
        raise RuntimeError("sense rc=%d: %s" % (q.returncode, q.stdout.strip()[:200]))
    for line in q.stdout.splitlines():
        if line.startswith("judgment="):
            return line[len("judgment="):]
    raise RuntimeError("no judgment: %r" % q.stdout[:200])

def run_channel(j, jt):
    q = subprocess.run([CHANNEL, j, jt], capture_output=True, text=True, timeout=60)
    if q.returncode != 0:
        raise RuntimeError("channel rc=%d: %s" % (q.returncode, q.stdout.strip()))
    c = v = None
    for line in q.stdout.splitlines():
        if line.startswith("C="):
            c = int(line[2:])
        elif line.startswith("verdict="):
            v = line[8:]
    assert c in (0, 1) and v in ("INSTALL", "WITHHOLD"), q.stdout
    return c, 1 if v == "INSTALL" else 0

def one(args):
    tag, spath, task, split, log, j, tf = args
    jt = run_sense(spath, task, tf)
    c, vi = run_channel(j, jt)
    return (tag, task, split, log, c, vi)

def main():
    man = json.load(open(os.path.join(CHAN, "..", "inputs_tcp", "blob_manifest.json")))
    jcache = {}
    for line in open(os.path.join(CHAN, "out_g0", "jwave_run1.tsv")):
        p = line.rstrip("\n").split("\t")
        jcache[(p[0], p[3])] = p[4]
    runs = [int(x) for x in sys.argv[1:]] or [1, 2]
    for run in runs:
        rundir = os.path.join(OUT, "run%d" % run)
        os.makedirs(rundir, exist_ok=True)
        tdir = os.path.join(TMP, "r3", "run%d" % run)
        os.makedirs(tdir, exist_ok=True)
        for tr in TRANSFORMS:
            vpath = os.path.join(rundir, "verdicts_%s.txt" % tr)
            done = set()
            if os.path.exists(vpath):
                for line in open(vpath):
                    p = line.rstrip("\n").split("\t")
                    if len(p) >= 6:
                        done.add((p[0], p[1], p[4]))
            rows = {}
            for line in open(vpath) if os.path.exists(vpath) else []:
                p = line.rstrip("\n").split("\t")
                rows[(p[0], p[1], p[4])] = p
            sha_lines = []
            inv_fail = []
            jobs = []
            for i, r in enumerate(man):
                if r["task"] not in TR_TASKS[tr]:
                    continue
                log = logical(r["task"], r["relpath"])
                src = os.path.join(FIXROOT, r["relpath"])
                tf = os.path.join(tdir, "t_%s_%d.bin" % (tr, i))
                tf2 = os.path.join(tdir, "t2_%s_%d.bin" % (tr, i))
                q = subprocess.run([ALT, tr, r["task"], src, tf], capture_output=True, text=True)
                if q.returncode != 0:
                    raise RuntimeError("alt_transform %s %s rc=%d: %s" % (tr, log, q.returncode, q.stdout.strip()))
                sha_lines.append("%s  %s/%s" % (sha(tf), log, tr))
                # involution self-check T(T(x))==x (validity per §4-R3)
                q2 = subprocess.run([ALT, tr, r["task"], tf, tf2], capture_output=True, text=True)
                if q2.returncode != 0:
                    inv_fail.append("RCFAIL " + log)
                elif sha(tf2) != sha(src):
                    inv_fail.append(log)
                for tag, spath in SENSES.items():
                    if (tag, r["split"], log) not in done:
                        jobs.append((tag, spath, r["task"], r["split"], log, jcache[(tag, log)], tf))
            open(os.path.join(rundir, "transform_sha256_%s.txt" % tr), "w").write("\n".join(sha_lines) + "\n")
            with ThreadPoolExecutor(max_workers=WORKERS) as ex:
                for (tag, task, split, log, c, vi) in ex.map(one, jobs):
                    if split == "calibration":
                        rows[(tag, split, log)] = ["CAL", tag, task, "primary", log, str(c)]
                    else:
                        rows[(tag, split, log)] = ["TEST", tag, task, "adversarial", log, str(c), str(vi)]
            with open(vpath, "w") as f:
                for k in sorted(rows):
                    f.write("\t".join(rows[k]) + "\n")
            # F3-style calibration gate per (sense, transform)
            gate = []
            for tag in SENSES:
                cal = [k for k in rows if k[0] == tag and k[1] == "calibration"]
                n = len(cal)
                cn = sum(int(rows[k][5]) for k in cal)
                rate = cn / n if n else 0.0
                verdict = "PASS" if rate >= 0.95 else "VOID"
                gate.append("%s %s cal=%d/%d rate=%.4f %s" % (tag, tr, cn, n, rate, verdict))
            gate.append("involution_failures=%d" % len(inv_fail))
            for f_ in inv_fail[:10]:
                gate.append("  INVFAIL " + f_)
            open(os.path.join(rundir, "gate_%s.txt" % tr), "w").write("\n".join(gate) + "\n")
            print("run %d transform %s: %d verdict rows; %s" % (run, tr, len(rows), "; ".join(gate[:2])), flush=True)
    print("R3 done")

if __name__ == "__main__":
    main()
