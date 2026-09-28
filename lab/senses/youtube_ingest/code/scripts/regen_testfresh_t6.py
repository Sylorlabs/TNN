#!/usr/bin/env python3
"""Regenerate TEST_FRESH t6_motiondir primary fixtures (seed 20260923)
using the frozen round-1 generator, then verify every sha256 against
rematch/data/TEST_FRESH/MANIFEST.sha256. Deterministic; no RNG of ours."""
import os, sys, hashlib

LAB = "/home/hatch/workspace/tnn-lab/senses"
sys.path.insert(0, os.path.join(LAB, "rebuild/harness"))
import gen

OUT = "/home/hatch/workspace/tnn-lab/senses/youtube_ingest/fixtures_testfresh"
MAN = os.path.join(LAB, "rematch/data/TEST_FRESH/MANIFEST.sha256")
CACHE = os.path.join(LAB, "rebuild/harness/fixtures/_photos")

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()

def main():
    assert len(os.listdir(CACHE)) >= 170, "photo cache incomplete"
    gen.MASTER_SEED = 20260923
    gen.PHOTOS = CACHE
    gen.FIX = OUT
    os.makedirs(OUT, exist_ok=True)
    n = 60  # round-1 primary count for t6
    truths = {}
    for idx in range(n):
        t = gen.gen_t6(5, "primary", idx, 170)
        truths[t] = truths.get(t, 0) + 1
    print("generated %d, truths=%s" % (n, truths), flush=True)
    want = {}
    with open(MAN) as f:
        for line in f:
            h, rel = line.strip().split("  ", 1)
            if rel.startswith("t6_motiondir/"):
                want[rel] = h
    d = os.path.join(OUT, "t6_motiondir", "primary")
    bad = 0
    for f in sorted(os.listdir(d)):
        if f.endswith(".truth"):
            continue
        rel = "t6_motiondir/primary/" + f
        got = sha256_file(os.path.join(d, f))
        if want.get(rel) != got:
            print("MISMATCH", rel, file=sys.stderr)
            bad += 1
    print("verified %d/%d t6 fixtures against frozen manifest, bad=%d"
          % (len(want), len([f for f in os.listdir(d) if not f.endswith('.truth')]), bad))
    return 1 if bad else 0

sys.exit(main())
