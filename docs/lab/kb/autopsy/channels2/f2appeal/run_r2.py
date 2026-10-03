#!/usr/bin/env python3
"""R2 multi-draw consensus runner (glue only). PREREG_FROZEN_F2APPEAL.md §4-R2.

For pass in {1,2}, config in {L3, L5}: for each TEST adversarial fixture,
generate 5 noise fields with the pure-Zag r1_noise binary (modes r2d0..r2d4),
run frozen senses A/B on each, apply the pure-Zag r2_maj rule (INSTALL iff
>=3/5 agree with the G0-cached J). Records 5 noise-byte SHA256s per fixture +
verdict lines. 2 passes must be byte-identical.

Outputs: out_r2/run{N}/noise_sha256_{cfg}.txt, out_r2/run{N}/verdicts_{cfg}.txt
(TEST lines: TEST\\tsense\\ttask\\tadversarial\\tlogical\\tC\\tV, C=1 iff majority agrees).
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
R1NOISE = os.path.join(BUILD, "r1_noise")
MAJ = os.path.join(BUILD, "r2_maj")
TMP = os.path.expanduser("~/workspace/tmp_f2appeal")
OUT = os.path.join(CHAN, "out_r2")
WORKERS = 12
CFGS = [("L3", "3"), ("L5", "5")]
DRAWS = ["r2d0", "r2d1", "r2d2", "r2d3", "r2d4"]

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

def run_maj(j, jns):
    q = subprocess.run([MAJ, j] + jns, capture_output=True, text=True, timeout=60)
    if q.returncode != 0:
        raise RuntimeError("r2_maj rc=%d: %s" % (q.returncode, q.stdout.strip()))
    c = v = None
    for line in q.stdout.splitlines():
        if line.startswith("C="):
            c = int(line[2:])
        elif line.startswith("verdict="):
            v = line[8:]
    assert c in (0, 1) and v in ("INSTALL", "WITHHOLD"), q.stdout
    return c, 1 if v == "INSTALL" else 0

def one(args):
    tag, spath, task, log, j, nfs = args
    jns = [run_sense(spath, task, nf) for nf in nfs]
    c, vi = run_maj(j, jns)
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
        tdir = os.path.join(TMP, "r2", "run%d" % run)
        os.makedirs(tdir, exist_ok=True)
        for cfg, lv in CFGS:
            vpath = os.path.join(rundir, "verdicts_%s.txt" % cfg)
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
                nfs = []
                for dk, dm in enumerate(DRAWS):
                    nf = os.path.join(tdir, "n_%s_d%d_%d.bin" % (cfg, dk, i))
                    q = subprocess.run([R1NOISE, r["task"], lv, dm, src, nf],
                                       capture_output=True, text=True)
                    if q.returncode != 0:
                        raise RuntimeError("r1_noise %s %s %s rc=%d: %s" % (log, cfg, dm, q.returncode, q.stdout.strip()))
                    sha_lines.append("%s  %s/%s/d%d" % (sha(nf), log, cfg, dk))
                    nfs.append(nf)
                for tag, spath in SENSES.items():
                    if (tag, log) not in done:
                        jobs.append((tag, spath, r["task"], log, jcache[(tag, log)], nfs))
            open(os.path.join(rundir, "noise_sha256_%s.txt" % cfg), "w").write("\n".join(sha_lines) + "\n")
            with ThreadPoolExecutor(max_workers=WORKERS) as ex:
                for (tag, task, log, c, vi) in ex.map(one, jobs):
                    rows[(tag, log)] = ["TEST", tag, task, "adversarial", log, str(c), str(vi)]
            with open(vpath, "w") as f:
                for (tag, log) in sorted(rows):
                    f.write("\t".join(rows[(tag, log)]) + "\n")
            print("run %d config %s: %d verdict rows" % (run, cfg, len(rows)), flush=True)
    print("R2 done")

if __name__ == "__main__":
    main()
