#!/usr/bin/env python3
"""gen_fresh_shapetrans.py -- FS-F2S fresh-draw fixture generation (glue only).
Generates the frozen Bar-(a) fresh draw per PREREG_FS-F2S_AMENDMENT.md:
  rng = Rng(stream_seed(MASTER, STREAM_NORMAL + 2, i)), MASTER=20260923
  (f, g, truth) = gen_shapetrans(rng, family=0, idx=i), i in 5000..6295
packaged with the frozen write_r2fx / write_truth from forks/R2-7/src/gen_r2a.py.
Deterministic: same indices -> byte-identical fixtures.
Usage: gen_fresh_shapetrans.py <outdir>
"""
import os
import sys

LAB = os.path.expanduser("~/workspace/tnn-lab/senses/pam-rebuild/round2")
sys.path.insert(0, os.path.join(LAB, "forks/R2-7/src"))
import gen_r2a as R27  # noqa: E402  (frozen R2A battery generator)

def main():
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    n = 0
    for i in range(5000, 6296):
        rng = R27.Rng(R27.stream_seed(R27.MASTER, R27.STREAM_NORMAL + 2, i))
        f, g, truth = R27.gen_shapetrans(rng, 0, i)
        path = os.path.join(outdir, "r2n_shapetrans_%d.r2fx" % i)
        R27.write_r2fx(path, 2, i, 0, f, g)
        R27.write_truth(path + ".truth", truth)
        n += 1
        if n % 200 == 0:
            print("progress %d/%d" % (n, 1296), flush=True)
    print("generated %d fixtures -> %s" % (n, outdir))

if __name__ == "__main__":
    main()
