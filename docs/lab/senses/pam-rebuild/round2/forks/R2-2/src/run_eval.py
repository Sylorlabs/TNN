#!/usr/bin/env python3
"""R2-2 evaluation runner: sharded, deterministic, hash-chained.

Runs the frozen sense2 binary over the full battery in a fixed order.
8 shards; within a shard fixtures run sequentially with prevchain chaining
from GENESIS:shard<N>. Also runs Approach A on identical fixtures.

Shard assignment: index of the fixture in the global sorted list, mod 8.
Zero RNG; fixed order; byte-identical across runs.

Usage: R2_SHARD=<0..7> run_eval.py <sense2-bin> <senseA-bin> <outdir>
Writes <outdir>/ledger_shard<N>.jsonl
"""
import os, sys, subprocess, json

SENSE2 = sys.argv[1]
SENSEA = sys.argv[2]
OUTDIR = sys.argv[3]
SHARD = int(os.environ["R2_SHARD"])

HARNESS = "/home/hatch/workspace/tnn-lab/senses/rebuild/harness/fixtures"
R22 = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/forks/R2-2"
GENDIR = os.path.join(R22, "work", "fixtures", "r2a")

TASKS = [
    ("colordisc", "colordisc", "img"),
    ("colorconst", "colorconst", "img"),
    ("shapetrans", "shapetrans", "img"),
    ("pitchdisc", "pitchdisc", "pcm"),
    ("timbredisc", "timbredisc", "pcm"),
    ("motiondir", "motiondir", "vid"),
]
# Harness uses tN_ prefixes; generated uses bare task names.
HARNESS_TASKS = [
    ("t1_colordisc", "colordisc", "img"),
    ("t2_colorconst", "colorconst", "img"),
    ("t3_shapetrans", "shapetrans", "img"),
    ("t4_pitchdisc", "pitchdisc", "pcm"),
    ("t5_timbredisc", "timbredisc", "pcm"),
    ("t6_motiondir", "motiondir", "vid"),
]
NSHARDS = 8
LAB = "/home/hatch/workspace/tnn-lab"

def collect():
    fixtures = []  # (sortkey, fixture, taskname, truthfile, variant, family)
    for dirname, taskname, ext in HARNESS_TASKS:
        d = os.path.join(HARNESS, dirname, "primary")
        for fn in sorted(os.listdir(d)):
            if fn.endswith("." + ext):
                fx = os.path.join(d, fn)
                fixtures.append(((taskname, "primary", "", fn), fx, taskname,
                                 fx + ".truth", "primary", "frozen-primary"))
    for dirname, taskname, ext in TASKS:
        d = os.path.join(GENDIR, dirname)
        if not os.path.isdir(d):
            continue
        # normal/
        nd = os.path.join(d, "normal")
        if os.path.isdir(nd):
            for fn in sorted(os.listdir(nd)):
                if fn.endswith("." + ext):
                    fx = os.path.join(nd, fn)
                    fixtures.append(((taskname, "normal", "", fn), fx, taskname,
                                     fx + ".truth", "normal", "gen-normal"))
        # R2A-*/ adversarial families directly under task dir
        for fam in sorted(os.listdir(d)):
            if not fam.startswith("R2A-"):
                continue
            fd = os.path.join(d, fam)
            if not os.path.isdir(fd):
                continue
            for fn in sorted(os.listdir(fd)):
                if fn.endswith("." + ext):
                    fx = os.path.join(fd, fn)
                    fixtures.append(((taskname, "adversarial", fam, fn), fx, taskname,
                                     fx + ".truth", "adversarial", fam))
    fixtures.sort(key=lambda x: x[0])
    return fixtures

def parse_kv(out):
    rec = {}
    for line in out.splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            rec[k.strip()] = v.strip()
    return rec

def main():
    fixtures = collect()
    mine = [fx for i, fx in enumerate(fixtures) if i % NSHARDS == SHARD]
    print("shard %d: %d fixtures (total %d)" % (SHARD, len(mine), len(fixtures)), flush=True)
    os.makedirs(OUTDIR, exist_ok=True)
    outp = os.path.join(OUTDIR, "ledger_shard%d.jsonl" % SHARD)
    prev = "GENESIS:shard%d" % SHARD
    n = 0
    with open(outp, "w") as f:
        for (sortkey, fixture, taskname, truthfile, variant, family) in mine:
            r = subprocess.run([SENSE2, fixture, taskname, truthfile, prev],
                               capture_output=True, text=True, timeout=300)
            if r.returncode != 0:
                raise RuntimeError("sense2 rc=%d on %s" % (r.returncode, fixture))
            rec2 = parse_kv(r.stdout)
            ra = subprocess.run([SENSEA, taskname, fixture],
                                capture_output=True, text=True, timeout=300)
            recA = parse_kv(ra.stdout or "")
            entry = {
                "fixture": os.path.relpath(fixture, LAB),
                "task": taskname,
                "variant": variant,
                "family": family,
                "prevchain": prev,
                "r22": rec2,
                "approachA": {"judgment": recA.get("judgment"),
                              "confidence": recA.get("confidence"),
                              "ops": recA.get("ops")},
            }
            f.write(json.dumps(entry, sort_keys=True) + "\n")
            prev = rec2["chain"]
            n += 1
            if n % 200 == 0:
                print("shard %d: %d/%d" % (SHARD, n, len(mine)), flush=True)
    print("shard %d done: %d records" % (SHARD, n), flush=True)

main()
