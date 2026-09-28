#!/usr/bin/env python3
"""ATTACK 2 — close-call amplification (R3 showed 8/12 close decisions
flipping, 50-95x output amplification on C3).

Method: for each of 3 sealed images (sealed_03: P2plane's largest sealed
win +1.73; sealed_04: edge-dense, the repaired panic image; sealed_07:
P2plane ties baseline, C3/P1 regressed -0.99), perturb the prepared LR
input.bmp by deterministic +/-1 and +/-2 LSB (clip at 0/255, all three
channels), rerun P2plane, and measure:
  - take-decision change: SHAPES takes / LINES takes / G / N from GEN_TRACE
    (the trace records summary counts only; no per-take records exist, so
    decision flips are proxied by take-count changes + output pixel diffs,
    stated explicitly in the report)
  - output amplification: max |delta| and mean |delta| over changed pixels
    of upscale_gen.bmp, divided by the input perturbation magnitude.
"""
import numpy as np, os, re, shutil, sys

RT = "/home/hatch/workspace/upscale_r4/redteam_r4"
sys.path.insert(0, RT)
from rt_common import BIN_P2, VOC3, prep, run_bin, sha256_file
sys.path.insert(0, "/home/hatch/workspace/selfpam_run/tnn-lab/docs/lab/image_upscale/diverse_set")
from eval_all import write_bmp  # noqa
sys.path.insert(0, "/home/hatch/workspace/upscale_r4/battery_build")
import run_matrix as M  # noqa

IMAGES = ["sealed_03", "sealed_04", "sealed_07"]
PERTURBS = {"p1": 1, "m1": -1, "p2": 2, "m2": -2}

TRACE_RE = {
    "shapes_takes": re.compile(r"SHAPES: G=(\d+) N=(\d+) takes=(\d+)"),
    "lines_takes": re.compile(r"LINES: G=(\d+) N=(\d+) takes=(\d+)"),
    "lineage": re.compile(r"lineage: top=(\d+) restricted=(\d+) empty_fallback=(\d+) parent_nofit=(\d+)"),
}

def read_bmp(path):
    return M.bmp_gt(path)

def parse_trace(path):
    d = open(path).read()
    out = {}
    for k, r in TRACE_RE.items():
        m = r.search(d)
        out[k] = tuple(map(int, m.groups())) if m else None
    return out

def main():
    os.chdir(os.path.join(RT, "work", "attack2"))
    for name in IMAGES:
        base_indir = f"base_{name}"
        shutil.rmtree(base_indir, ignore_errors=True)
        prep("sealed", name, VOC3, base_indir)
        base_out = f"out_{name}_orig"
        shutil.rmtree(base_out, ignore_errors=True)
        p = run_bin(BIN_P2, base_indir, base_out, "plane")
        assert p.returncode == 0, (name, p.stderr[-1000:])
        base_gen = read_bmp(f"{base_out}/upscale_gen.bmp")
        base_tr = parse_trace(f"{base_out}/GEN_TRACE.txt")
        base_sha = sha256_file(f"{base_out}/upscale_gen.bmp")
        print(f"== {name}: shapes_takes={base_tr['shapes_takes'][2]} "
              f"lines_takes={base_tr['lines_takes'][2]} lineage={base_tr['lineage']}", flush=True)
        base_input = read_bmp(f"{base_indir}/input.bmp").astype(np.int32)
        for ptag, d in PERTURBS.items():
            indir = f"ind_{name}_{ptag}"
            shutil.rmtree(indir, ignore_errors=True)
            shutil.copytree(base_indir, indir)
            pert = np.clip(base_input + d, 0, 255).astype(np.uint8)
            write_bmp(os.path.join(indir, "input.bmp"), pert)
            outd = f"out_{name}_{ptag}"
            shutil.rmtree(outd, ignore_errors=True)
            q = run_bin(BIN_P2, indir, outd, "plane")
            assert q.returncode == 0, (name, ptag, q.stderr[-1000:])
            gen = read_bmp(f"{outd}/upscale_gen.bmp").astype(np.int32)
            diff = np.abs(gen - base_gen.astype(np.int32))
            changed = diff > 0
            nchanged = int(changed.sum())
            maxd = int(diff.max())
            meand = float(diff[changed].mean()) if nchanged else 0.0
            amp = maxd / abs(d)
            tr = parse_trace(f"{outd}/GEN_TRACE.txt")
            dtakes = tr["shapes_takes"][2] - base_tr["shapes_takes"][2]
            dltakes = tr["lines_takes"][2] - base_tr["lines_takes"][2]
            dG = tr["shapes_takes"][0] - base_tr["shapes_takes"][0]
            same_sha = sha256_file(f"{outd}/upscale_gen.bmp") == base_sha
            print(f"  {ptag} (d={d:+d} LSB): shapes_takes {base_tr['shapes_takes'][2]}->{tr['shapes_takes'][2]} "
                  f"(d={dtakes:+d}), lines_takes d={dltakes:+d}, G d={dG:+d}, "
                  f"pix_changed={nchanged}/{gen.size} ({100.0*nchanged/gen.size:.2f}%), "
                  f"max|d|={maxd}, mean|d|={meand:.1f}, amp={amp:.0f}x, same_sha={same_sha}", flush=True)
            shutil.rmtree(outd); shutil.rmtree(indir)
        shutil.rmtree(base_out); shutil.rmtree(base_indir)

if __name__ == "__main__":
    main()
