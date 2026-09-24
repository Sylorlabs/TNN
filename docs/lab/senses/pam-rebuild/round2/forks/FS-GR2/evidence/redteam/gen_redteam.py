#!/usr/bin/env python3
"""FS-GR2 red-team hostile motiondir corpora (RT-A .. RT-D).

Deterministic: every draw comes from frozen splitmix64 streams in
gen_r2a.py (Rng / _sm_integers) or fixed seeds documented below.
No RNG in any decision path; generation seeds are frozen constants.

Corpora (task=5 motiondir, family=9, frozen r2fx layout):
  RT-A periodic   : region = 128 + 100*sin(2*pi*(x*cos t + y*sin t)/L),
                    t in 6 orientations (k*pi/6), L in {4,8,16}px
                    8 dirs x 3 freq x 6 orient = 144 fixtures
  RT-B flat+noise : region = 128 + splitmix noise in [-40,40]
                    8 dirs x 5 seeds = 40 fixtures
  RT-C ramps      : region = 128 + 100*((x*cos t + y*sin t)/48),
                    t in 8 orientations (k*pi/8)
                    8 dirs x 8 orient = 64 fixtures
  RT-D flicker    : photo-crop region; F = _mot_frames(direction, 50,
                    flicker=(0.5, mdir), blob=mdir), mdir != direction;
                    G = clean high-contrast truth frames
                    8 dirs x 5 seeds = 40 fixtures

Seed plan (fixture index n within corpus, corpus-local):
  RT-A frames rng seed = 9000 + n ; G rng seed = 9005 + n
  RT-B region noise    = _sm_integers(Rng(9100 + n), -40, 41, (48,48))
       frames rng seed = 9200 + n ; G rng seed = 9300 + n
  RT-C frames rng seed = 9400 + n ; G rng seed = 9500 + n
  RT-D region rng seed = 9600 + n (photo crop via _mot_region)
       mdir  via Rng(9650 + n).pick(others)
       frames rng seed = 9700 + n ; G rng seed = 9800 + n

Output: REDTEAM/corpora/<corpus>/rt<C>_<n:04d>.r2fx + .truth sidecar
        ("truth=<DIRNAME>" like the frozen battery), plus corpora/<corpus>.list
        and a MANIFEST.txt recording every seed.
"""
import sys, os
import numpy as np

sys.path.insert(0, "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/forks/R2-7/src")
import gen_r2a as R

OUT = os.path.dirname(os.path.abspath(__file__)) + "/corpora"
DIRS = R.MOT_DIRS  # ["N","NE","E","SE","S","SW","W","NW"]
JMAP = {"STILL": 0, "N": 1, "NE": 2, "E": 3, "SE": 4, "S": 5, "SW": 6, "W": 7, "NW": 8}

yy, xx = np.mgrid[0:48, 0:48].astype(np.float64)

manifest = []

def emit(corpus, n, fname, frames_F, frames_G, truth):
    fb = b"".join(fr.tobytes() for fr in frames_F)
    gb = b"".join(fr.tobytes() for fr in frames_G)
    assert len(fb) == 51200 and len(gb) == 51200
    d = os.path.join(OUT, corpus)
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, fname)
    R.write_r2fx(p, 5, n, 9, fb, gb)
    R.write_truth(p + ".truth", truth)
    manifest.append((corpus, fname, truth))
    return p

def rtA():
    for di, d in enumerate(DIRS):
        for li, L in enumerate((4, 8, 16)):
            for oi in range(6):
                t = oi * np.pi / 6
                region = 128.0 + 100.0 * np.sin(2 * np.pi * (xx * np.cos(t) + yy * np.sin(t)) / L)
                n = (di * 3 + li) * 6 + oi
                F = R._mot_frames(region, d, 50, rng=R.Rng(9000 + n))
                G = R._mot_high_contrast(R._mot_frames(region, d, 50, rng=R.Rng(9005 + n)))
                emit("rtA", n, "rtA_%04d.r2fx" % n, F, G, d)
    assert n == 143

def rtB():
    for di, d in enumerate(DIRS):
        for s in range(5):
            n = di * 5 + s
            noise = R._sm_integers(R.Rng(9100 + n), -40, 41, (48, 48)).astype(np.float64)
            region = 128.0 + noise
            F = R._mot_frames(region, d, 50, rng=R.Rng(9200 + n))
            G = R._mot_high_contrast(R._mot_frames(region, d, 50, rng=R.Rng(9300 + n)))
            emit("rtB", n, "rtB_%04d.r2fx" % n, F, G, d)
    assert n == 39

def rtC():
    for di, d in enumerate(DIRS):
        for oi in range(8):
            t = oi * np.pi / 8
            region = 128.0 + 100.0 * ((xx * np.cos(t) + yy * np.sin(t)) / 48.0)
            n = di * 8 + oi
            F = R._mot_frames(region, d, 50, rng=R.Rng(9400 + n))
            G = R._mot_high_contrast(R._mot_frames(region, d, 50, rng=R.Rng(9500 + n)))
            emit("rtC", n, "rtC_%04d.r2fx" % n, F, G, d)
    assert n == 63

def rtD():
    for di, d in enumerate(DIRS):
        for s in range(5):
            n = di * 5 + s
            region = R._mot_region(R.Rng(9600 + n))
            mdir = R.Rng(9650 + n).pick([x for x in DIRS if x != d])
            F = R._mot_frames(region, d, 50, rng=R.Rng(9700 + n),
                              flicker=(0.5, mdir), blob=mdir)
            G = R._mot_high_contrast(R._mot_frames(region, d, 50, rng=R.Rng(9800 + n)))
            emit("rtD", n, "rtD_%04d.r2fx" % n, F, G, d)
            manifest.append(("rtD-mdir", "rtD_%04d.r2fx" % n, "mdir=" + mdir))
    assert n == 39

if __name__ == "__main__":
    rtA(); rtB(); rtC(); rtD()
    with open(os.path.join(OUT, "MANIFEST.txt"), "w") as f:
        f.write("# corpus fixture truth  (seeds per file header comment)\n")
        for c, fn, t in manifest:
            if c.startswith("rtD-mdir"):
                f.write("%s %s %s\n" % (c, fn, t))
            else:
                f.write("%s %s truth=%s\n" % (c, fn, t))
    for c in ("rtA", "rtB", "rtC", "rtD"):
        d = os.path.join(OUT, c)
        files = sorted(x for x in os.listdir(d) if x.endswith(".r2fx"))
        with open(os.path.join(OUT, c + ".list"), "w") as f:
            for x in files:
                f.write(os.path.join(d, x) + "\n")
        print(c, len(files))
