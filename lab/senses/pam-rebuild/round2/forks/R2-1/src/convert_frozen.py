#!/usr/bin/env python3
"""Convert 925 frozen harness fixtures to R2A1 format in suite/.

Normal (740): paired primary/noise -> F=primary/G=noise and F=noise/G=primary.
Adversarial (185): F=fixture, G=fixture (same bytes; T2 vacuous, documented).
Output: suite/r21f_<task>_<i>.r2a + .truth (i in 0..739 normal, 740..924 adv).
"""
import os, sys, struct
import numpy as np

HARNESS = os.path.expanduser("~/workspace/tnn-lab/senses/rebuild/harness/fixtures")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "suite")
TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]
TDIR = ["t1_colordisc", "t2_colorconst", "t3_shapetrans",
        "t4_pitchdisc", "t5_timbredisc", "t6_motiondir"]
TASKIDX = {t: i for i, t in enumerate(TASKS)}
EXT = {"colordisc": "img", "colorconst": "img", "shapetrans": "img",
       "pitchdisc": "pcm", "timbredisc": "pcm", "motiondir": "vid"}

# R2A F/G geometries (must match sense.zag geom_of)
GEOM = {
    "colordisc":   ((64, 32), (32, 16)),   # (w,h) F, (w,h) G, RGB
    "colorconst":  ((64, 32), (32, 16)),
    "shapetrans":  ((48, 48), (24, 24)),
    "pitchdisc":   (2160, 2160),            # samples @4kHz F, G
    "timbredisc":  (4000, 4000),            # samples @8kHz F, G
    "motiondir":   ((24, 24), (24, 24)),    # (w,h) gray F, G; 8 frames each
}

def downsample_nn(arr, out_h, out_w):
    """Nearest-neighbor downsample (h,w[,c]) -> (out_h,out_w[,c]). Deterministic."""
    h, w = arr.shape[0], arr.shape[1]
    ys = (np.arange(out_h) * h // out_h)
    xs = (np.arange(out_w) * w // out_w)
    return arr[ys[:, None], xs]

def load_img(path):
    b = open(path, "rb").read()
    w, h = struct.unpack("<II", b[:8])
    return np.frombuffer(b[8:], dtype=np.uint8).reshape(h, w, 3)

def load_pcm(path):
    b = open(path, "rb").read()
    sr, nbytes = struct.unpack("<II", b[:8])
    return sr, np.frombuffer(b[8:], dtype=np.int16).copy()

def load_vid(path):
    b = open(path, "rb").read()
    nf, w, h = struct.unpack("<III", b[:12])
    px = np.frombuffer(b[12:], dtype=np.uint8).reshape(nf, h, w, 3)
    return nf, px

def rgb_to_gray(px):
    # px (h,w,3) uint8 -> (h,w) uint8 luminance
    g = (0.299 * px[:, :, 0].astype(np.float64) +
         0.587 * px[:, :, 1].astype(np.float64) +
         0.114 * px[:, :, 2].astype(np.float64))
    return np.clip(g + 0.5, 0, 255).astype(np.uint8)

def convert_image(task, src_path, geom):
    """src 128x64 or 96x96 RGB -> geom (w,h) RGB bytes."""
    px = load_img(src_path)
    w, h = geom
    ds = downsample_nn(px, h, w)
    return ds.tobytes()

def convert_audio(task, src_path, n_out):
    """src int16 @16kHz -> n_out samples int16 at R2A rate (4k/8k)."""
    sr, s = load_pcm(src_path)
    assert sr == 16000, sr
    factor = 4 if task == "pitchdisc" else 2
    ds = s[::factor]
    if len(ds) >= n_out:
        ds = ds[:n_out]
    else:
        ds = np.concatenate([ds, np.zeros(n_out - len(ds), dtype=np.int16)])
    return ds.astype(np.int16).tobytes()

def convert_video(src_path, geom):
    """src 8x64x64 RGB -> 8 frames geom (w,h) gray bytes."""
    nf, px = load_vid(src_path)
    assert nf == 8
    w, h = geom
    out = []
    for f in range(nf):
        g = rgb_to_gray(px[f])
        ds = downsample_nn(g, h, w)
        out.append(ds.tobytes())
    return b"".join(out)

def truth_of(src_path):
    t = open(src_path + ".truth").read().strip()
    assert t.startswith("truth=")
    return t[6:]

def write_r2a(fid, taskidx, f_bytes, g_bytes, truth):
    path = os.path.join(OUT, fid + ".r2a")
    with open(path, "wb") as fh:
        fh.write(b"R2A1")
        fh.write(struct.pack("<II", taskidx, len(f_bytes)))
        fh.write(f_bytes)
        fh.write(struct.pack("<I", len(g_bytes)))
        fh.write(g_bytes)
    with open(path + ".truth", "w") as fh:
        fh.write("truth=%s\n" % truth)

def convert_one(task, fp, gp):
    """Convert harness fixture fp (F) and gp (G) to R2A (f_bytes, g_bytes, truth)."""
    truth = truth_of(fp)
    if task in ("colordisc", "colorconst", "shapetrans"):
        (fw, fh), (gw, gh) = GEOM[task]
        fb = convert_image(task, fp, (fw, fh))
        gb = convert_image(task, gp, (gw, gh))
    elif task in ("pitchdisc", "timbredisc"):
        n = GEOM[task][0]
        fb = convert_audio(task, fp, n)
        gb = convert_audio(task, gp, n)
    else:  # motiondir
        (fw, fh), _ = GEOM[task]
        fb = convert_video(fp, (fw, fh))
        gb = convert_video(gp, (fw, fh))
    return fb, gb, truth


def main():
    os.makedirs(OUT, exist_ok=True)
    idx = 0
    for ti, task in enumerate(TASKS):
        td = os.path.join(HARNESS, TDIR[ti])
        ext = EXT[task]
        for variant in ["primary", "noise"]:
            vd = os.path.join(td, variant)
            other = "noise" if variant == "primary" else "primary"
            od = os.path.join(td, other)
            files = sorted(f for f in os.listdir(vd) if f.endswith("." + ext))
            for fn in files:
                fp = os.path.join(vd, fn)
                gp = os.path.join(od, fn)
                if not os.path.exists(gp):
                    print("WARN no pair for %s" % fp, flush=True)
                    continue
                fb, gb, truth = convert_one(task, fp, gp)
                fid = "r21f_%s_%d" % (task, idx)
                write_r2a(fid, TASKIDX[task], fb, gb, truth)
                idx += 1
    print("normal frozen trials: %d (expected 740)" % idx, flush=True)
    assert idx == 740, idx
    adv_start = idx
    for ti, task in enumerate(TASKS):
        td = os.path.join(HARNESS, TDIR[ti], "adversarial")
        ext = EXT[task]
        files = sorted(f for f in os.listdir(td) if f.endswith("." + ext))
        for fn in files:
            fp = os.path.join(td, fn)
            fb, gb, truth = convert_one(task, fp, fp)
            fid = "r21f_%s_%d" % (task, idx)
            write_r2a(fid, TASKIDX[task], fb, gb, truth)
            idx += 1
    print("adversarial frozen trials: %d (expected 185)" % (idx - adv_start), flush=True)
    assert idx - adv_start == 185, idx - adv_start
    print("total frozen R2A trials: %d" % idx, flush=True)

if __name__ == "__main__":
    main()
