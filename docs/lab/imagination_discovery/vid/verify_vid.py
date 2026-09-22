#!/usr/bin/env python3
"""D-VID-1 mechanical bar verification (VERIFY ONLY — never generates).
Bars: V-RES, V-SHARP (frames 0/23/47), V-TEMP, V-DET (via sha256 manifest),
V-COMP (grep audit is done separately in shell).
"""
import hashlib, os, struct, sys
import numpy as np
from PIL import Image

FRAMES_DIR = sys.argv[1] if len(sys.argv) > 1 else "frames"
N = 48

def load_gray(i):
    p = os.path.join(FRAMES_DIR, "dvid1_f%02d.bmp" % i)
    im = Image.open(p)
    return np.asarray(im.convert("L"), dtype=np.float64), im

def grad_mean(g):
    gx = np.abs(np.diff(g, axis=1))
    gy = np.abs(np.diff(g, axis=0))
    return (gx.mean() + gy.mean()) / 2.0

def main():
    ok = True
    # ---- V-RES ----
    nfiles = 0
    for i in range(N):
        p = os.path.join(FRAMES_DIR, "dvid1_f%02d.bmp" % i)
        sz = os.path.getsize(p)
        with open(p, "rb") as fh:
            hdr = fh.read(54)
        assert hdr[0:2] == b"BM", p
        w, h = struct.unpack("<ii", hdr[18:26])
        bpp = struct.unpack("<H", hdr[28:30])[0]
        stat = "OK" if (w == 1024 and h == 1024 and bpp == 24 and sz == 3145782) else "FAIL"
        if stat == "FAIL":
            ok = False
            print("V-RES FAIL frame %d: %dx%d bpp=%d size=%d" % (i, w, h, bpp, sz))
        nfiles += 1
    print("V-RES: %d/48 files, all 1024x1024 24-bit: %s" % (nfiles, "PASS" if ok and nfiles == 48 else "FAIL"))

    # ---- V-SHARP (frames 0, 23, 47) ----
    for i in (0, 23, 47):
        g, im = load_gray(i)
        small = im.convert("L").resize((512, 512), Image.BOX)
        back = small.resize((1024, 1024), Image.BOX)
        gb = np.asarray(back, dtype=np.float64)
        go, gg = grad_mean(g), grad_mean(gb)
        ratio = go / gg if gg > 0 else float("inf")
        stat = "PASS" if ratio >= 1.20 else "FAIL"
        if stat == "FAIL":
            ok = False
        print("V-SHARP frame %2d: grad(O)=%.3f grad(B)=%.3f ratio=%.3f -> %s" % (i, go, gg, ratio, stat))

    # ---- V-TEMP ----
    prev, _ = load_gray(0)
    diffs = []
    per = []
    for i in range(1, N):
        g, _ = load_gray(i)
        d = np.abs(g - prev).mean() / 255.0
        per.append(d)
        diffs.append(d)
        prev = g
    mn, mx, mean = min(per), max(per), sum(per) / len(per)
    stat = "PASS" if (0.005 <= mn and mx <= 0.15) else "FAIL"
    if stat == "FAIL":
        ok = False
    print("V-TEMP: mean|dF|/255 per pair: min=%.4f max=%.4f mean=%.4f in [0.5%%,15%%] -> %s"
          % (mn, mx, mean, stat))
    # frozen-frame / flicker detail
    print("   per-pair: " + " ".join("%.2f%%" % (d * 100) for d in per[:8]) + " ...")

    # ---- manifest sha256 (for V-DET comparison across runs) ----
    man = []
    for i in range(N):
        p = os.path.join(FRAMES_DIR, "dvid1_f%02d.bmp" % i)
        h = hashlib.sha256(open(p, "rb").read()).hexdigest()
        man.append("dvid1_f%02d.bmp %s" % (i, h))
    with open(os.path.join(FRAMES_DIR, "SHA256SUMS"), "w") as fh:
        fh.write("\n".join(man) + "\n")
    whole = hashlib.sha256("\n".join(man).encode()).hexdigest()
    print("V-DET manifest sha256: %s (written to SHA256SUMS)" % whole)

    print("OVERALL: " + ("ALL MECHANICAL BARS PASS" if ok else "FAIL — see above"))
    return 0 if ok else 1

sys.exit(main())
