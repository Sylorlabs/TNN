#!/usr/bin/env python3
"""Resume interrupted evaluation shards. For each shard, reads the existing
ledger, finds the last prevchain, and continues from the next fixture.
Appends to the existing ledger files.

Usage: resume_eval.py <sense2-bin> <senseA-bin> <rundir>
"""
import os, sys, subprocess, json

SENSE2 = sys.argv[1]
SENSEA = sys.argv[2]
RUNDIR = sys.argv[3]
ONLY_SHARD = int(sys.argv[4]) if len(sys.argv) > 4 else None

HARNESS = "/home/hatch/workspace/tnn-lab/senses/rebuild/harness/fixtures"
R22 = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/forks/R2-2"
GENDIR = os.path.join(R22, "work", "fixtures", "r2a")
HARNESS_TASKS = [("t1_colordisc","colordisc","img"),("t2_colorconst","colorconst","img"),("t3_shapetrans","shapetrans","img"),("t4_pitchdisc","pitchdisc","pcm"),("t5_timbredisc","timbredisc","pcm"),("t6_motiondir","motiondir","vid")]
TASKS = [("colordisc","colordisc","img"),("colorconst","colorconst","img"),("shapetrans","shapetrans","img"),("pitchdisc","pitchdisc","pcm"),("timbredisc","timbredisc","pcm"),("motiondir","motiondir","vid")]
NSHARDS = 8
LAB = "/home/hatch/workspace/tnn-lab"

def collect():
    fixtures = []
    for dirname, taskname, ext in HARNESS_TASKS:
        d = os.path.join(HARNESS, dirname, "primary")
        for fn in sorted(os.listdir(d)):
            if fn.endswith("." + ext):
                fx = os.path.join(d, fn)
                fixtures.append((fx, taskname, fx + ".truth", "primary", "frozen-primary"))
    for dirname, taskname, ext in TASKS:
        d = os.path.join(GENDIR, dirname)
        if not os.path.isdir(d): continue
        nd = os.path.join(d, "normal")
        if os.path.isdir(nd):
            for fn in sorted(os.listdir(nd)):
                if fn.endswith("." + ext):
                    fx = os.path.join(nd, fn)
                    fixtures.append((fx, taskname, fx + ".truth", "normal", "gen-normal"))
        for fam in sorted(os.listdir(d)):
            if not fam.startswith("R2A-"): continue
            fd = os.path.join(d, fam)
            if not os.path.isdir(fd): continue
            for fn in sorted(os.listdir(fd)):
                if fn.endswith("." + ext):
                    fx = os.path.join(fd, fn)
                    fixtures.append((fx, taskname, fx + ".truth", "adversarial", fam))
    # sort to match run_eval.py order
    # run_eval sorts by (taskname, variant, fam, fn)
    fixtures.sort(key=lambda x: (x[1], x[3], x[4], os.path.basename(x[0])))
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
    print("total fixtures: %d" % len(fixtures))
    shards = range(NSHARDS) if ONLY_SHARD is None else [ONLY_SHARD]
    for s in shards:
        outp = os.path.join(RUNDIR, "ledger_shard%d.jsonl" % s)
        # read existing
        done_fixtures = set()
        prev = "GENESIS:shard%d" % s
        if os.path.exists(outp):
            with open(outp) as f:
                for line in f:
                    e = json.loads(line)
                    done_fixtures.add(e["fixture"])
                    prev = e["r22"]["chain"]
        # find missing for this shard
        missing = []
        for i, (fx, taskname, truthfile, variant, family) in enumerate(fixtures):
            if i % NSHARDS != s: continue
            rel = os.path.relpath(fx, LAB)
            if rel not in done_fixtures:
                missing.append((fx, taskname, truthfile, variant, family, rel))
        print("shard %d: %d done, %d missing" % (s, len(done_fixtures), len(missing)))
        if not missing: continue
        with open(outp, "a") as f:
            for (fx, taskname, truthfile, variant, family, rel) in missing:
                r = subprocess.run([SENSE2, fx, taskname, truthfile, prev],
                                   capture_output=True, text=True, timeout=300)
                if r.returncode != 0:
                    raise RuntimeError("sense2 rc=%d on %s" % (r.returncode, fx))
                rec2 = parse_kv(r.stdout)
                ra = subprocess.run([SENSEA, taskname, fx],
                                    capture_output=True, text=True, timeout=300)
                recA = parse_kv(ra.stdout or "")
                entry = {"fixture": rel, "task": taskname, "variant": variant,
                         "family": family, "prevchain": prev, "r22": rec2,
                         "approachA": {"judgment": recA.get("judgment"),
                                       "confidence": recA.get("confidence"),
                                       "ops": recA.get("ops")}}
                f.write(json.dumps(entry, sort_keys=True) + "\n")
                prev = rec2["chain"]
        print("shard %d: resumed %d" % (s, len(missing)))

main()
