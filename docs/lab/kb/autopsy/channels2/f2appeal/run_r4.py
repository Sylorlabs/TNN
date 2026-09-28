#!/usr/bin/env python3
"""R4 structured-noise runner (glue only). PREREG_FROZEN_F2APPEAL.md §4-R4.

For pass in {1,2}, variant in {1,2}: noise each TEST adversarial fixture
with the pure-Zag r4_noise binary, run frozen senses A/B on the noised
bytes, apply the pure-Zag channel_c3 rule (INSTALL iff Jn==J, J from the G0
cache). Records noise-byte SHA256s + verdict lines. 2 passes must be
byte-identical.

Outputs: out_r4/run{N}/noise_sha256_V{V}.txt, out_r4/run{N}/verdicts_V{V}.txt
(TEST lines: TEST\\tsense\\ttask\\tadversarial\\tlogical\\tC\\tV).
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
R4NOISE = os.path.join(BUILD, "r4_noise")
CHANNEL = os.path.join(BUILD, "channel_c3")
TMP = os.path.expanduser("~/workspace/tmp_f2appeal")
OUT = os.path.join(CHAN, "out_r4")
WORKERS = 12
VARIANTS = ["1", "2"]

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

def run_channel(j, jn):
    q = subprocess.run([CHANNEL, j, jn], capture_output=True, text=True, timeout=60)
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
    tag, spath, task, log, j, nf = args
    jn = run_sense(spath, task, nf)
    c, vi = run_channel(j, jn)
    return (tag, task, log, c, vi)

def main():
    man = json.load(open(os.path.join(CHAN, "..", "inputs_tcp", "blob_manifest.json")))
    test_rows = [r for r in man if r["split"] == "test"]
    jcache = {}
    for line in open(os.path.join(CHAN, "out_g0", "jwave_run1.tsv")):
        p = line.rstrip("\n").split("\t")
        jcache[(p[0], p[3])] = p[4]
    runs = [int(x) for x in sys.argv[1:]] or [1, 2]
    for run in runs:
        rundir = os.path.join(OUT, "run%d" % run)
        os.makedirs(rundir, exist_ok=True)
        tdir = os.path.join(TMP, "r4", "run%d" % run)
        os.makedirs(tdir, exist_ok=True)
        for va in VARIANTS:
            vpath = os.path.join(rundir, "verdicts_V%s.txt" % va)
            done = set()
            if os.path.exists(vpath):
                for line in open(vpath):
                    p = line.rstrip("\n").split("\t")
                    if len(p) >= 5:
                        done.add((p[1], p[4]))
            rows = {}
            for line in open(vpath) if os.path.exists(vpath) else []:
                p = line.rstrip("\n").split("\t")
                rows[(p[1], p[4])] = p
            sha_lines = []
            jobs = []
            for i, r in enumerate(test_rows):
                log = logical(r["task"], r["relpath"])
                src = os.path.join(FIXROOT, r["relpath"])
                nf = os.path.join(tdir, "n_V%s_%d.bin" % (va, i))
                q = subprocess.run([R4NOISE, r["task"], va, src, nf],
                                   capture_output=True, text=True)
                if q.returncode != 0:
                    raise RuntimeError("r4_noise %s V%s rc=%d: %s" % (log, va, q.returncode, q.stdout.strip()))
                sha_lines.append("%s  %s/V%s" % (sha(nf), log, va))
                for tag, spath in SENSES.items():
                    if (tag, log) not in done:
                        jobs.append((tag, spath, r["task"], log, jcache[(tag, log)], nf))
            open(os.path.join(rundir, "noise_sha256_V%s.txt" % va), "w").write("\n".join(sha_lines) + "\n")
            with ThreadPoolExecutor(max_workers=WORKERS) as ex:
                for (tag, task, log, c, vi) in ex.map(one, jobs):
                    rows[(tag, log)] = ["TEST", tag, task, "adversarial", log, str(c), str(vi)]
            with open(vpath, "w") as f:
                for (tag, log) in sorted(rows):
                    f.write("\t".join(rows[(tag, log)]) + "\n")
            print("run %d variant %s: %d verdict rows" % (run, va, len(rows)), flush=True)
    print("R4 done")

if __name__ == "__main__":
    main()
