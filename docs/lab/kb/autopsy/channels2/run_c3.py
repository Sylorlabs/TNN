#!/usr/bin/env python3
"""C3 run glue (PREREG_FROZEN_TCP.md §9). Glue only — reasoning/noise/counts
are in pure Zag (src/c3_noise, src/channel_c3, src/score_tcp).
For run in {1,2}:
  - HALTs if either frozen sense binary's SHA256 differs from the frozen value
  - noises the 92 TEST adversarial fixtures with the frozen pure-Zag
    instrument (records noised-fixture SHA256s)
  - runs frozen sense A and B on the original and on the noised fixture
  - applies the frozen §9 rule via the pure-Zag channel_c3 binary
    (INSTALL iff J_noisy == J(stim))
  - writes out_c3/runN/verdicts.txt (TEST rows, both senses)
    and out_c3/runN/noised_sha256.txt
No truth anywhere in this script."""
import hashlib, json, os, subprocess, sys

CHAN = os.path.dirname(os.path.abspath(__file__))
TN = os.path.expanduser("~/workspace/tnn-lab")
FIXROOT = os.path.join(TN, "senses", "rebuild", "harness", "fixtures")
SENSE_A = os.path.join(TN, "senses", "rebuild", "a_raw", "sense")
SENSE_B = os.path.expanduser("~/workspace/senses-rebuild/b_percept/sense")
NOISE = os.path.join(CHAN, "src", "c3_noise")
CHANNEL = os.path.join(CHAN, "src", "channel_c3")
TMP = "/home/hatch/workspace/tmp_c3"
OUT = os.path.join(CHAN, "out_c3")
SENSES = {"A": SENSE_A, "B": SENSE_B}
FROZEN_SHA = {
    "A": "68db15216d9dc75a10839212ac5349195248f5ae113a7e37dc336795db8e35a1",
    "B": "3921dc65cc7ccdc0f7c36ff291e55973322c11d43a648c162c2bf54abb6a0bda",
}

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
    return c, v

def main():
    for tag, spath in SENSES.items():
        h = sha(spath)
        if h != FROZEN_SHA[tag]:
            print("HALT: sense %s SHA mismatch:\n  got %s\n  want %s" % (tag, h, FROZEN_SHA[tag]))
            sys.exit(10)
    print("sense binary SHAs verified (A, B match frozen)", flush=True)
    man = [r for r in json.load(open(os.path.join(CHAN, "inputs_tcp", "blob_manifest.json")))
           if r["split"] == "test"]
    assert len(man) == 92, len(man)
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
                if len(p) >= 7:
                    done.add((p[1], p[4]))  # (sense, logical)
        sha_lines = []
        ntest = 0
        pf = open(partial, "a")
        for i, r in enumerate(man):
            log = logical(r["task"], r["relpath"])
            src = os.path.join(FIXROOT, r["relpath"])
            nf = os.path.join(tdir, "n_%d.bin" % i)
            if not (os.path.exists(nf) and os.path.getsize(nf) == os.path.getsize(src)):
                # noise provably preserves byte length, so size equality is a
                # valid resume-integrity guard
                q = subprocess.run([NOISE, r["task"], src, nf], capture_output=True, text=True)
                if q.returncode != 0:
                    raise RuntimeError("noise %s rc=%d: %s" % (r["relpath"], q.returncode, q.stdout.strip()))
            sha_lines.append("%s  %s" % (sha(nf), r["relpath"]))
            for tag, spath in SENSES.items():
                if (tag, log) in done:
                    ntest += 1
                    continue
                j = run_sense(spath, r["task"], src)
                jn = run_sense(spath, r["task"], nf)
                c, v = run_channel(j, jn)
                vi = 1 if v == "INSTALL" else 0
                row = "TEST\t%s\t%s\t%s\t%s\t%d\t%d" % (tag, r["task"], r["variant"], log, c, vi)
                pf.write(row + "\n")
                pf.flush()
                done.add((tag, log))
                ntest += 1
            if (i + 1) % 25 == 0:
                print("run%d: %d/%d fixtures" % (run, i + 1, len(man)), flush=True)
        pf.close()
        vlines = [l.rstrip("\n") for l in open(partial)]
        vlines.append("DONE\t0\t%d" % ntest)
        with open(os.path.join(rundir, "verdicts.txt"), "w") as f:
            f.write("\n".join(vlines) + "\n")
        with open(os.path.join(rundir, "noised_sha256.txt"), "w") as f:
            f.write("\n".join(sha_lines) + "\n")
        print("run%d done: %d TEST rows" % (run, ntest), flush=True)

main()
