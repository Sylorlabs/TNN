#!/usr/bin/env python3
"""Red-team common helpers (R4, P2plane). Replicates battery indir prep byte-exactly."""
import hashlib, os, re, shutil, subprocess, sys

BUILD = "/home/hatch/workspace/upscale_r4/battery_build"
HARNESS_DIR = "/home/hatch/workspace/selfpam_run/tnn-lab/docs/lab/image_upscale/diverse_set"
METRICS = "/home/hatch/workspace/selfpam_run/tnn-lab/docs/lab/image_upscale/generation/src/metrics.py"
VOC2 = "/home/hatch/workspace/upscale_gen/teach_out/vocab.bin"
VOC3 = "/home/hatch/workspace/upscale_r4/impl_p2/vocab_v3.bin"
RT = "/home/hatch/workspace/upscale_r4/redteam_r4"
BIN_BASE = os.path.join(RT, "build", "bin_base")
BIN_P2 = os.path.join(RT, "build", "bin_p2")

sys.path.insert(0, HARNESS_DIR)
from eval_all import write_bmp, downscale_2x2  # noqa
sys.path.insert(0, BUILD)
import run_matrix as M  # noqa: prep_indir, score_psnr, bmp_gt, jpg_gt

PSNR_RE = re.compile(r"PSNR (\S+) dB")

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def prep(kind, name, vocab_src, indir):
    """Replicate battery indir prep exactly; return (gt_w, gt_h)."""
    return M.prep_indir(kind, name, vocab_src, indir)

def run_bin(binary, indir, outdir, argv3=None):
    os.makedirs(outdir, exist_ok=True)
    args = [binary, indir, outdir] + ([argv3] if argv3 else [])
    p = subprocess.run(args, capture_output=True, text=True, timeout=3600)
    return p

def psnr(gt_path, gen_path):
    p = subprocess.run([sys.executable, METRICS, gt_path, gen_path],
                       capture_output=True, text=True, timeout=600)
    assert p.returncode == 0, p.stderr[-500:]
    m = PSNR_RE.search(p.stdout)
    assert m, p.stdout
    return float(m.group(1))
