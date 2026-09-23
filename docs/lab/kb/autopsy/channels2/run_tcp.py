#!/usr/bin/env python3
"""STEP 4 (calibration) + STEP 5 (test) runner for KB4 C2 (glue only).
For run in {1,2}:
  - transforms all 185 fixtures with the frozen pure-Zag instrument
    (records transform SHA256s)
  - runs frozen sense A and B on original and transformed fixtures
  - applies the frozen §2 law via the pure-Zag channel_c2 binary
  - writes out_tcp/runN/verdicts.txt (CAL + TEST rows, both senses)
    and out_tcp/runN/transform_sha256.txt
Verdict rule: INSTALL iff Jt == L(J). No truth anywhere in this script.
F3 is evaluated downstream from Zag-emitted counts (score_tcp.py)."""
import hashlib, json, os, subprocess, sys

CHAN = os.path.dirname(os.path.abspath(__file__))
TN = os.path.expanduser("~/workspace/tnn-lab")
FIXROOT = os.path.join(TN, "senses", "rebuild", "harness", "fixtures")
SENSE_A = os.path.join(TN, "senses", "rebuild", "a_raw", "sense")
SENSE_B = os.path.expanduser("~/workspace/senses-rebuild/b_percept/sense")
TRANSFORM = os.path.join(CHAN, "src", "tcp_transform")
CHANNEL = os.path.join(CHAN, "src", "channel_c2")
TMP = "/home/hatch/workspace/tmp_tcp"
OUT = os.path.join(CHAN, "out_tcp")
SENSES = {"A": SENSE_A, "B": SENSE_B}

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def logical(task, relpath):
    base = relpath.rsplit("/", 1)[-1]
    if base.endswith(".img"):
        base = base[:-4]
    return "%s/%s" % (task, base)

def run_sense(path, task, fx):
    q = subprocess.run([path, task, fx], capture_output=True, text=True, timeout=1800)
    if q.returncode != 0:
        raise RuntimeError("sense %s %s rc=%d: %s" % (task, fx, q.returncode, q.stdout.strip()[:200]))
    j = None
    for line in q.stdout.splitlines():
        if line.startswith("judgment="):
            j = line[len("judgment="):]
    if j is None:
        raise RuntimeError("no judgment line: %r" % q.stdout[:200])
    return j

def run_channel(task, j, jt):
    q = subprocess.run([CHANNEL, task, j, jt], capture_output=True, text=True, timeout=60)
    if q.returncode != 0:
        raise RuntimeError("channel rc=%d: %s" % (q.returncode, q.stdout.strip()))
    c = v = None
    for line in q.stdout.splitlines():
        if line.startswith("C="):
            c = int(line[2:])
        elif line.startswith("verdict="):
            v = line[8:]
    assert c in (0, 1) and v in ("INSTALL", "WITHHOLD"), q.stdout
    return c, v

def main():
    man = json.load(open(os.path.join(CHAN, "inputs_tcp", "blob_manifest.json")))
    runs = [int(x) for x in sys.argv[1:]] or [1, 2]
    for run in runs:
        rundir = os.path.join(OUT, "run%d" % run)
        os.makedirs(rundir, exist_ok=True)
        tdir = os.path.join(TMP, "run%d" % run)
        os.makedirs(tdir, exist_ok=True)
        partial = os.path.join(rundir, "verdicts_partial.tsv")
        done = set()
        if os.path.exists(partial):
            for line in open(partial):
                p = line.rstrip("\n").split("\t")
                if len(p) >= 6:
                    done.add((p[1], p[4]))  # (sense, logical)
        sha_lines = []
        ncal = ntest = 0
        pf = open(partial, "a")
        for i, r in enumerate(man):
            log = logical(r["task"], r["relpath"])
            src = os.path.join(FIXROOT, r["relpath"])
            tf = os.path.join(tdir, "t_%d.bin" % i)
            if not (os.path.exists(tf) and os.path.getsize(tf) == os.path.getsize(src)):
                # transform provably preserves byte length (selfcheck: 185/185),
                # so size equality is a valid resume-integrity guard
                q = subprocess.run([TRANSFORM, r["task"], src, tf], capture_output=True, text=True)
                if q.returncode != 0:
                    raise RuntimeError("transform %s rc=%d: %s" % (r["relpath"], q.returncode, q.stdout.strip()))
            th = sha(tf)
            sha_lines.append("%s  %s" % (th, r["relpath"]))
            for tag, spath in SENSES.items():
                if (tag, log) in done:
                    if r["split"] == "calibration":
                        ncal += 1
                    else:
                        ntest += 1
                    continue
                j = run_sense(spath, r["task"], src)
                jt = run_sense(spath, r["task"], tf)
                c, v = run_channel(r["task"], j, jt)
                vi = 1 if v == "INSTALL" else 0
                if r["split"] == "calibration":
                    row = "CAL\t%s\t%s\t%s\t%s\t%d" % (tag, r["task"], r["variant"], log, c)
                    ncal += 1
                else:
                    row = "TEST\t%s\t%s\t%s\t%s\t%d\t%d" % (tag, r["task"], r["variant"], log, c, vi)
                    ntest += 1
                pf.write(row + "\n")
                pf.flush()
                done.add((tag, log))
            if (i + 1) % 25 == 0:
                print("run%d: %d/%d fixtures" % (run, i + 1, len(man)), flush=True)
        pf.close()
        vlines = [l.rstrip("\n") for l in open(partial)]
        vlines.append("DONE\t%d\t%d" % (ncal, ntest))
        with open(os.path.join(rundir, "verdicts.txt"), "w") as f:
            f.write("\n".join(vlines) + "\n")
        with open(os.path.join(rundir, "transform_sha256.txt"), "w") as f:
            f.write("\n".join(sha_lines) + "\n")
        print("run%d done: %d CAL rows, %d TEST rows" % (run, ncal, ntest), flush=True)

main()
