#!/usr/bin/env python3
"""gen_fresh.py -- FS-F2C: generate the FRESH colorconst control draw.

Frozen procedure (see PREREG_FS-F2C.md section 4):
- Imports the FROZEN R2-7 generator pieces (gen_colorconst, Rng, stream_seed,
  write_r2fx, write_truth) — the same code that built the frozen suite.
- MASTER_F2C = 20260924 (disjoint from the frozen suite's 20260923);
  stream = 401 (= STREAM_NORMAL + taskidx(colorconst=1)); family = 0;
  indices 0..1199 (n = 1200).
- Writes forks/FS-F2C/fixtures_fresh/f2c_colorconst_<i>.r2fx + .truth sidecars
  + MANIFEST.sha256 + gen_ledger.jsonl.

Deterministic: every draw comes from the per-fixture splitmix64 stream.
Run AFTER PREREG_FS-F2C.md is committed; the prereg names the seed.
Usage: python3 src/gen_fresh.py
"""
import sys, os, json, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
FORK = os.path.dirname(HERE)
R27SRC = os.path.normpath(os.path.join(
    FORK, "..", "..", "..", "..", "..",
    "tnn-lab", "senses", "pam-rebuild", "round2", "forks", "R2-7", "src"))
# robust: resolve relative to this file's real location
R27SRC = os.path.join(os.path.expanduser("~"), "workspace", "tnn-lab",
                      "senses", "pam-rebuild", "round2", "forks", "R2-7", "src")
sys.path.insert(0, R27SRC)
os.environ.setdefault("R2A_OUT", "/tmp/f2c_unused")

import gen_r2a as G  # noqa: E402  (frozen R2-7 generator)

MASTER_F2C = 20260924
STREAM = 401          # STREAM_NORMAL(400) + taskidx(colorconst=1)
N = 1200
TASKIDX = 1           # colorconst

def main():
    outdir = os.path.join(FORK, "fixtures_fresh")
    os.makedirs(outdir, exist_ok=True)
    manifest = []
    ledger_path = os.path.join(outdir, "gen_ledger.jsonl")
    with open(ledger_path, "w") as ledger:
        for i in range(N):
            rng = G.Rng(G.stream_seed(MASTER_F2C, STREAM, i))
            f, g, truth = G.gen_colorconst(rng, 0, i)
            fid = "f2c_colorconst_%d" % i
            path = os.path.join(outdir, fid + ".r2fx")
            G.write_r2fx(path, TASKIDX, i, 0, f, g)
            G.write_truth(path + ".truth", truth)
            h = hashlib.sha256(open(path, "rb").read()).hexdigest()
            manifest.append("%s  ./%s.r2fx\n" % (h, fid))
            ledger.write(json.dumps({"id": fid, "task": "colorconst",
                                     "split": "f2c_fresh", "family": 0,
                                     "truth": truth, "sha256": h,
                                     "master": MASTER_F2C, "stream": STREAM,
                                     "index": i}) + "\n")
            if (i + 1) % 300 == 0:
                print("  %d/%d" % (i + 1, N), flush=True)
    with open(os.path.join(outdir, "MANIFEST.sha256"), "w") as mf:
        mf.writelines(sorted(manifest))
    n_same = sum(1 for l in open(ledger_path)
                 if json.loads(l)["truth"] == "SAME_SURFACE")
    print("wrote %d fixtures -> %s (SAME_SURFACE=%d DIFFERENT=%d)" %
          (N, outdir, n_same, N - n_same))

if __name__ == "__main__":
    main()
