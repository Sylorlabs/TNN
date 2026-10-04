#!/usr/bin/env python3
"""gen_battery_e2b.py -- FS-E2b fresh battery draw (glue only).

Per PREREG_FS-E2b.md (frozen): fresh deterministic draw from the FROZEN
R2-7 generator (forks/R2-7/src/gen_r2a.py, unchanged).
  MASTER = 20260926 (fresh, unused anywhere in the program)
  adv : stream = STREAM_ADV + tidx = 500 + tidx, family mix mirrors R2-16 b_adv
  ctrl: stream = STREAM_NORMAL + tidx = 400 + tidx, family 0
  rng = Rng(stream_seed(MASTER, STREAM, i)); gen_<task>(rng, family, i)
Indices from 30000 upward, disjoint ranges per (task, family) / per task.
No RNG in any decision path beyond the frozen deterministic streams.

Writes: fixtures_e2b/e2b_<split>_<task>_<i>.r2fx + .truth sidecars,
        evidence/eval/b_adv_e2b.list, b_ctrl_e2b.list,
        evidence/eval/b_adv_e2b.manifest, b_ctrl_e2b.manifest,
        evidence/eval/DRAW_RECORD.md
"""
import sys
import os
import hashlib
from collections import Counter

sys.path.insert(0, "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/forks/R2-7/src")
import gen_r2a as R

FORKDIR = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/forks/FS-E2b"
OUTDIR = os.path.join(FORKDIR, "fixtures_e2b")
EVDIR = os.path.join(FORKDIR, "evidence", "eval")
MASTER = 20260926
BASE = 30000

TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]
TIDX = {t: i for i, t in enumerate(TASKS)}
GEN = {
    "colordisc": R.gen_colordisc, "colorconst": R.gen_colorconst,
    "shapetrans": R.gen_shapetrans, "pitchdisc": R.gen_pitchdisc,
    "timbredisc": R.gen_timbredisc, "motiondir": R.gen_motiondir,
}

# (task, family) -> count for the adversarial battery (mirrors R2-16 b_adv)
ADV_MIX = [
    ("colorconst", 1, 690), ("colorconst", 2, 690),
    ("colordisc", 1, 810), ("colordisc", 2, 710), ("colordisc", 3, 810),
    ("motiondir", 1, 504), ("motiondir", 2, 116), ("motiondir", 3, 10),
    ("pitchdisc", 1, 710), ("pitchdisc", 2, 810), ("pitchdisc", 3, 810),
    ("shapetrans", 1, 815), ("shapetrans", 2, 915), ("shapetrans", 3, 615),
    ("timbredisc", 1, 500), ("timbredisc", 2, 295), ("timbredisc", 3, 190),
]
# task -> count for the control battery (family 0)
CTRL_MIX = [
    ("colordisc", 600), ("colorconst", 500), ("shapetrans", 300),
    ("pitchdisc", 200), ("timbredisc", 200), ("motiondir", 200),
]


def draw(task, family, stream, idx):
    rng = R.Rng(R.stream_seed(MASTER, stream, idx))
    return GEN[task](rng, family, idx)


def main():
    assert sum(c for _, _, c in ADV_MIX) == 10000
    assert sum(c for _, c in CTRL_MIX) == 2000
    os.makedirs(OUTDIR, exist_ok=True)
    os.makedirs(EVDIR, exist_ok=True)
    manifest_adv, manifest_ctrl = [], []
    counts = Counter()
    ranges = []
    idx = BASE
    # adversarial
    for task, family, n in ADV_MIX:
        stream = 500 + TIDX[task]
        lo = idx
        for k in range(n):
            i = idx
            f, g, truth = draw(task, family, stream, i)
            fid = "e2b_adv_%s_%d" % (task, i)
            path = os.path.join(OUTDIR, fid + ".r2fx")
            R.write_r2fx(path, TIDX[task], i, family, f, g)
            R.write_truth(path + ".truth", truth)
            h = hashlib.sha256(open(path, "rb").read()).hexdigest()
            manifest_adv.append((h, path, fid, truth))
            counts[("adv", task, family)] += 1
            idx += 1
        ranges.append(("adv", task, family, n, stream, lo, idx - 1))
        print("adv %-10s f%d: %d fixtures (idx %d..%d)" % (task, family, n, lo, idx - 1), flush=True)
    # controls
    for task, n in CTRL_MIX:
        stream = 400 + TIDX[task]
        lo = idx
        for k in range(n):
            i = idx
            f, g, truth = draw(task, 0, stream, i)
            fid = "e2b_ctrl_%s_%d" % (task, i)
            path = os.path.join(OUTDIR, fid + ".r2fx")
            R.write_r2fx(path, TIDX[task], i, 0, f, g)
            R.write_truth(path + ".truth", truth)
            h = hashlib.sha256(open(path, "rb").read()).hexdigest()
            manifest_ctrl.append((h, path, fid, truth))
            counts[("ctrl", task)] += 1
            idx += 1
        ranges.append(("ctrl", task, 0, n, stream, lo, idx - 1))
        print("ctrl %-10s: %d fixtures (idx %d..%d)" % (task, n, lo, idx - 1), flush=True)

    def write_list(name, manifest):
        lp = os.path.join(EVDIR, name + ".list")
        mp = os.path.join(EVDIR, name + ".manifest")
        with open(lp, "w") as fh:
            fh.write("\n".join(m[1] for m in manifest) + "\n")
        with open(mp, "w") as fh:
            for h, p, fid, truth in manifest:
                fh.write("%s  %s  %s\n" % (h, fid + ".r2fx", truth))

    write_list("b_adv_e2b", manifest_adv)
    write_list("b_ctrl_e2b", manifest_ctrl)

    with open(os.path.join(EVDIR, "DRAW_RECORD.md"), "w") as fh:
        fh.write("# FS-E2b battery draw record\n\n")
        fh.write("Drawn after the PREREG_FS-E2b.md commit; the prereg named the\n")
        fh.write("seed (MASTER=20260926), so no re-rolling was possible.\n\n")
        fh.write("Generator: frozen `forks/R2-7/src/gen_r2a.py` (unchanged).\n")
        fh.write("MASTER=20260926, adv stream=500+tidx, ctrl stream=400+tidx,\n")
        fh.write("`rng=Rng(stream_seed(MASTER, stream, i))`, `gen_<task>(rng, family, i)`.\n\n")
        fh.write("| split | task | family | n | stream | idx_lo | idx_hi |\n")
        fh.write("|---|---|---|---|---|---|---|\n")
        for split, task, fam, n, stream, lo, hi in ranges:
            fh.write("| %s | %s | %d | %d | %d | %d | %d |\n" % (split, task, fam, n, stream, lo, hi))
        fh.write("\nManifest SHA-256:\n")
        for name in ("b_adv_e2b", "b_ctrl_e2b"):
            mp = os.path.join(EVDIR, name + ".manifest")
            fh.write("- %s.manifest: %s\n" % (name, hashlib.sha256(open(mp, "rb").read()).hexdigest()))
        fh.write("\nTruth-class counts (adv):\n")
        tc = Counter((m[3], m[2].split("_")[2]) for m in manifest_adv)
        for k in sorted(tc):
            fh.write("- %s %s: %d\n" % (k[1], k[0], tc[k]))
        fh.write("\nTruth-class counts (ctrl):\n")
        tc2 = Counter((m[3], m[2].split("_")[2]) for m in manifest_ctrl)
        for k in sorted(tc2):
            fh.write("- %s %s: %d\n" % (k[1], k[0], tc2[k]))
    print("DRAW COMPLETE: %d adv + %d ctrl" % (len(manifest_adv), len(manifest_ctrl)))


if __name__ == "__main__":
    main()
