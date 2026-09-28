#!/usr/bin/env python3
"""ATTACK 3a — operator neutering: render every P2plane take as MEAN-FILL
instead of PLANE-FIT (same take geometry, same labels, red-team-only binary).
If neutering PLANE barely moves the sealed-battery score, the 'measured
construction' claim is hollow. Also asserts the neutered binary reproduces
P2plane's take geometry exactly (same GEN_TRACE take counts) to prove the
edit touched only the render branch.
"""
import os, re, shutil, sys

RT = "/home/hatch/workspace/upscale_r4/redteam_r4"
sys.path.insert(0, RT)
from rt_common import BIN_P2, VOC3, prep, run_bin, psnr

NEUT = os.path.join(RT, "build", "bin_p2_NEUTMEAN_redteam_only")
SEALED = [f"sealed_{i:02d}" for i in range(1, 11)]
TAKES_RE = re.compile(r"(SHAPES|LINES): G=\d+ N=\d+ takes=(\d+)")

def takecounts(trace_path):
    return TAKES_RE.findall(open(trace_path).read())

def main():
    os.chdir(os.path.join(RT, "work", "attack3"))
    print(f"{'image':10s} {'p2plane':>8s} {'neutmean':>8s} {'delta':>7s}  geom_same", flush=True)
    deltas = []
    for name in SEALED:
        ps = {}
        geoms = {}
        for cfg, binary in (("p2plane", BIN_P2), ("neutmean", NEUT)):
            indir, outd = f"ind_{name}_{cfg}", f"out_{name}_{cfg}"
            shutil.rmtree(indir, ignore_errors=True); shutil.rmtree(outd, ignore_errors=True)
            prep("sealed", name, VOC3, indir)
            p = run_bin(binary, indir, outd, "plane")
            assert p.returncode == 0, (name, cfg, p.stderr[-1000:])
            ps[cfg] = psnr(os.path.join(indir, "gt.bmp"), os.path.join(outd, "upscale_gen.bmp"))
            geoms[cfg] = takecounts(os.path.join(outd, "GEN_TRACE.txt"))
            shutil.rmtree(indir); shutil.rmtree(outd)
        d = ps["neutmean"] - ps["p2plane"]
        deltas.append(d)
        print(f"{name:10s} {ps['p2plane']:8.2f} {ps['neutmean']:8.2f} {d:+7.2f}  {geoms['p2plane']==geoms['neutmean']}", flush=True)
    print(f"mean delta (neutmean - p2plane): {sum(deltas)/len(deltas):+.3f} dB", flush=True)

if __name__ == "__main__":
    main()
