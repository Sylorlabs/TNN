#!/usr/bin/env python3
"""gen_fresh.py -- FS-F2T fresh gating draw (glue only).

Per PREREG_FS-F2T §5 (frozen): uses the FROZEN R2-7 generator
(gen_r2a.gen_timbredisc) at stream indices NEVER used in exploratory work.
  rng = Rng(stream_seed(MASTER=20260923, STREAM_NORMAL+TIDX=404, i))
  gen_timbredisc(rng, family=0, idx=i) for i in 720..1719 (1000 fixtures)
Truth comes from the frozen generator itself (_tmb_template_class).
No AI decisions here; no RNG beyond the frozen deterministic streams.

Writes: fixtures_fresh/f2t_timbredisc_<i>.r2fx + .truth sidecars,
        fixtures_fresh/manifest.tsv  (sha256, filename, truth)
Prints: manifest sha256, truth class counts.
"""
import sys
import os
import hashlib
from collections import Counter

sys.path.insert(0, "/home/hatch/workspace/tnn-lab/senses/rebuild/harness")  # frozen gen.py
sys.path.insert(0, "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/forks/R2-7/src")
import gen_r2a as R

FORKDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTDIR = os.path.join(FORKDIR, "fixtures_fresh")
MASTER = 20260923
STREAM = 400 + 4  # STREAM_NORMAL + tidx(timbredisc)
LO, HI = 720, 1719


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    manifest = []
    counts = Counter()
    for i in range(LO, HI + 1):
        rng = R.Rng(R.stream_seed(MASTER, STREAM, i))
        f, g, truth = R.gen_timbredisc(rng, 0, i)
        fid = "f2t_timbredisc_%d" % i
        path = os.path.join(OUTDIR, fid + ".r2fx")
        R.write_r2fx(path, 4, i, 0, f, g)
        R.write_truth(path + ".truth", truth)
        h = hashlib.sha256(open(path, "rb").read()).hexdigest()
        manifest.append("%s  %s  %s\n" % (h, fid + ".r2fx", truth))
        counts[truth] += 1
    man_path = os.path.join(OUTDIR, "manifest.tsv")
    with open(man_path, "w") as fh:
        fh.writelines(manifest)
    man_hash = hashlib.sha256(open(man_path, "rb").read()).hexdigest()
    print("fixtures: %d" % len(manifest))
    print("truth counts:", dict(counts))
    print("manifest sha256: %s" % man_hash)


if __name__ == "__main__":
    main()
