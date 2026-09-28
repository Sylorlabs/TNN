#!/usr/bin/env python3
"""intake_measure.py — reproduce the video intake fidelity verdict.

Builds composer.zag with the pinned znc toolchain (mirror layout so the
../../tnn-lab/toolchain import resolves; the committed source is copied, not
modified), runs ingest x2 + recall x2 on the sealed Big Buck Bunny reference
frames, byte-compares all 24 held frames against sources, and verifies the
pipeline's own FNV-1a-64 hash chain (H_I == H_R == fnv(source raster)).

Expects: ~/workspace/video-repro/source/frames/frame_00.ppm .. frame_23.ppm
Zero RNG anywhere; all comparisons are SHA-256 / byte equality.
"""
import hashlib, os, re, shutil, subprocess, sys

HOME = os.path.expanduser("~")
LAB = os.path.join(HOME, "workspace/tnn-lab")
ZNC = os.path.join(LAB, "toolchain/bin/znc_linux_x86_64_abed8aa1")
SRC = os.path.join(LAB, "imagination/video-composer-step2/src/composer.zag")
FRAMES = os.path.join(HOME, "workspace/video-repro/source/frames")
WORK = os.path.join(HOME, "workspace/intake_verdict")

def sh(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        raise RuntimeError("FAILED: %s\n%s" % (cmd, r.stderr[-2000:]))
    return r.stdout

def fnv1a(b):
    h = 0xCBF29CE484222325
    for x in b:
        h = ((h ^ x) * 0x100000001B3) & 0xFFFFFFFFFFFFFFFF
    return h

def main():
    for p in (ZNC, SRC):
        assert os.path.exists(p), "missing " + p
    assert os.path.isdir(FRAMES), "missing BBB frames: " + FRAMES
    bdir = os.path.join(WORK, "repro_vc/src")
    os.makedirs(bdir, exist_ok=True)
    shutil.copy(SRC, os.path.join(bdir, "composer.zag"))
    link = os.path.join(WORK, "tnn-lab")
    if not os.path.islink(link):
        os.symlink(LAB, link)
    sh([ZNC, "composer.zag", "-o", "composer_bin"], cwd=bdir)
    BIN = os.path.join(bdir, "composer_bin")
    assert os.path.isfile(BIN)

    runs = []
    for tag in ("A", "B"):
        wd = os.path.join(WORK, "repro_run" + tag)
        os.makedirs(wd, exist_ok=True)
        out = sh([BIN, "ingest", "bunny", FRAMES, os.path.join(wd, "ing")])
        assert "ingest_rc=0" in out, out
        out = sh([BIN, "recall", os.path.join(wd, "ing"), os.path.join(wd, "rec")])
        assert "recall_rc=0" in out, out
        runs.append(wd)

    # 1) per-frame byte identity
    nf, bad = 24, []
    for f in range(nf):
        a = open(os.path.join(FRAMES, "frame_%02d.ppm" % f), "rb").read()
        b = open(os.path.join(runs[0], "rec/frame_%02d.ppm" % f), "rb").read()
        if a != b:
            bad.append((f, sum(1 for x, y in zip(a, b) if x != y),
                        max(abs(x - y) for x, y in zip(a, b))))
    # 2) determinism x2 (stores + one recalled frame)
    det = open(os.path.join(runs[0], "ing/store.bin"), "rb").read() == \
          open(os.path.join(runs[1], "ing/store.bin"), "rb").read()
    # 3) hash chain: H_I (trace) == fnv(source raster) == H_R (recall stdout)
    tr = open(os.path.join(runs[0], "ing/trace_ingest.txt")).read()
    m = re.search(r"INGEST f=0 H_I=([0-9a-f]+)", tr)
    hi = m.group(1)
    raw = open(os.path.join(FRAMES, "frame_00.ppm"), "rb").read()
    mh = re.match(rb"P6\n(\d+) (\d+)\n255\n", raw)
    rast = raw[mh.end():]
    fnv = "%x" % fnv1a(rast)
    h_all = lambda d: hashlib.sha256(
        b"".join(open(os.path.join(d, "frame_%02d.ppm" % f), "rb").read()
                 for f in range(nf))).hexdigest()
    print("frames byte-identical: %d/%d  mismatches=%s" % (nf - len(bad), nf, bad))
    print("determinism x2 (stores):", det)
    print("H_I trace:", hi, "| fnv(source raster):", fnv, "| match:", hi == fnv)
    print("all-frames sha256 source:", h_all(FRAMES))
    print("all-frames sha256 held  :", h_all(os.path.join(runs[0], "rec")))
    ok = (not bad) and det and (hi == fnv) and \
         (h_all(FRAMES) == h_all(os.path.join(runs[0], "rec")))
    print("INTAKE VERDICT:", "BIT-EXACT" if ok else "LOSS DETECTED")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
