#!/usr/bin/env python3
"""Rematch fixture driver: TRAIN budgets (seed 20260922) and TEST-FRESH
(seed 20260923), primary-style only, reusing the frozen 170-photo cache.
Never downloads. Fixtures are NOT committed; only MANIFEST.sha256 + counts.
Usage: gen_driver.py <name> <seed> <mult>   (mult=1 -> 370 fixtures)
"""
import os, sys, hashlib, json, time

sys.path.insert(0, "/home/hatch/workspace/senses-rebuild/harness")
import gen

CACHE = "/home/hatch/workspace/senses-rebuild/harness/fixtures/_photos"
WORK = "/home/hatch/workspace/senses-rematch/data"
BASE = [60, 40, 90, 60, 60, 60]
GEXT = {0: ".img", 1: ".img", 2: ".img", 3: ".pcm", 4: ".pcm", 5: ".vid"}
PHOTO_TASKS = {1, 2, 5}

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()

def main():
    name, seed, mult = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    assert len(os.listdir(CACHE)) >= 170, "photo cache incomplete"
    gen.MASTER_SEED = seed
    gen.PHOTOS = CACHE
    outdir = os.path.join(WORK, name)
    gen.FIX = outdir
    os.makedirs(outdir, exist_ok=True)
    t_all = time.time()
    manifest = []
    counts = {}
    for ti, tdir in enumerate(gen.DIRS_T):
        n = BASE[ti] * mult
        g = [gen.gen_t1, gen.gen_t2, gen.gen_t3, gen.gen_t4, gen.gen_t5, gen.gen_t6][ti]
        truths = {}
        t0 = time.time()
        for idx in range(n):
            if ti in PHOTO_TASKS:
                t = g(ti, "primary", idx, 170)
            else:
                t = g(ti, "primary", idx)
            truths[t] = truths.get(t, 0) + 1
        dt = time.time() - t0
        d = os.path.join(outdir, tdir, "primary")
        for f in sorted(os.listdir(d)):
            if f.endswith(".truth"):
                continue
            manifest.append((os.path.join(tdir, "primary", f),
                             sha256_file(os.path.join(d, f))))
        counts[tdir] = {"n": n, "truths": truths, "gen_s": round(dt, 1)}
        print("%s: %d fixtures, %s, %.1fs" % (tdir, n, truths, dt), flush=True)
    with open(os.path.join(outdir, "MANIFEST.sha256"), "w") as f:
        for rel, h in manifest:
            f.write("%s  %s\n" % (h, rel))
    with open(os.path.join(outdir, "counts.json"), "w") as f:
        json.dump({"name": name, "seed": seed, "mult": mult,
                   "tasks": counts,
                   "total_s": round(time.time() - t_all, 1)}, f, indent=1)
    print("TOTAL: %d fixtures in %.1fs -> %s" %
          (len(manifest), time.time() - t_all, outdir), flush=True)

main()
