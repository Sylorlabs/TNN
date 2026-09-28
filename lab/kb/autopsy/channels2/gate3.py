#!/usr/bin/env python3
"""STEP 3 — pre-run validity gate (glue only).
Runs frozen sense binaries A and B on all 185 TCP fixtures (370 runs) with
CLI "task in-path", parses judgment=/confidence= lines, and confirms
byte-identical reproduction of kb4_rerun/truth.json (== batch_A/B.txt content)
for these stimuli. Any mismatch -> HALT."""
import hashlib, json, os, subprocess, sys

CHAN = os.path.dirname(os.path.abspath(__file__))
TN = os.path.expanduser("~/workspace/tnn-lab")
FIXROOT = os.path.join(TN, "senses", "rebuild", "harness", "fixtures")
SENSE_A = os.path.join(TN, "senses", "rebuild", "a_raw", "sense")
SENSE_B = os.path.expanduser("~/workspace/senses-rebuild/b_percept/sense")
CORPUS = os.path.join(TN, "prose-learning", "epistemic_wave", "kb4_rerun")

FROZEN = {
    "A": ("68db15216d9dc75a10839212ac5349195248f5ae113a7e37dc336795db8e35a1", SENSE_A),
    "B": ("3921dc65cc7ccdc0f7c36ff291e55973322c11d43a648c162c2bf54abb6a0bda", SENSE_B),
}

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def logical(task, relpath):
    base = relpath.rsplit("/", 1)[-1]
    if base.endswith(".img"):  # matches gen_batch.py: only .img is stripped
        base = base[:-4]
    return "%s/%s" % (task, base)

def run_sense(path, task, fx):
    q = subprocess.run([path, task, fx], capture_output=True, text=True, timeout=1200)
    if q.returncode != 0:
        return None, "rc=%d out=%s" % (q.returncode, q.stdout.strip()[:200])
    j = c = None
    for line in q.stdout.splitlines():
        if line.startswith("judgment="):
            j = line[len("judgment="):]
        elif line.startswith("confidence="):
            c = int(line[len("confidence="):])
    if j is None or c is None:
        return None, "missing keys: %r" % q.stdout[:200]
    return (j, c), None

def main():
    fails = []
    # 0. frozen binary SHAs
    for tag, (want, path) in FROZEN.items():
        got = sha(path)
        if got != want:
            fails.append(("BINARY", "sense %s sha %s != frozen %s" % (tag, got, want)))
        else:
            print("binary %s sha OK: %s" % (tag, got[:16]))
    if fails:
        for f in fails: print("FAIL", f[0], f[1])
        return 1
    # 1. index truth.json
    truth = json.load(open(os.path.join(CORPUS, "truth.json")))
    per = {}
    for k, v in truth.items():
        se, _ = k.split("/", 1)
        per[(se, v["task"], v["variant"], v["stim"])] = v
    man = json.load(open(os.path.join(CHAN, "inputs_tcp", "blob_manifest.json")))
    n = 0
    for r in man:
        fx = os.path.join(FIXROOT, r["relpath"])
        log = logical(r["task"], r["relpath"])
        for tag, (_, path) in FROZEN.items():
            rec = per.get((tag, r["task"], r["variant"], log))
            if rec is None:
                fails.append((r["relpath"], "%s: no truth rec for %s" % (tag, log)))
                continue
            got, err = run_sense(path, r["task"], fx)
            if got is None:
                fails.append((r["relpath"], "%s: %s" % (tag, err)))
                continue
            if got[0] != rec["judgment"] or got[1] != rec["confidence"]:
                fails.append((r["relpath"], "%s: got %s/%d want %s/%d" % (
                    tag, got[0], got[1], rec["judgment"], rec["confidence"])))
            n += 1
        if len(man) and (man.index(r) + 1) % 25 == 0:
            print("progress %d/%d fixtures, fails=%d" % (man.index(r) + 1, len(man), len(fails)), flush=True)
    for rp, why in fails:
        print("FAIL", rp, why)
    print("ran %d/370 runs, %d mismatches" % (n, len(fails)))
    return 1 if fails else 0

sys.exit(main())
