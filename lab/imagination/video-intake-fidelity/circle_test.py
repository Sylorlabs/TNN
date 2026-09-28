#!/usr/bin/env python3
"""circle_test.py — the circle-faceting stage-localization test.

Draws smooth anti-aliased circles on gray (white outline r=48, red filled r=28,
blue filled r=18, green outline r=36; 512x187), then:

  (a) stillingest/stillrecall x2 through composer.zag  -> byte-compare (video line intake)
  (b) ingest_bin (zoom fork, docs/lab/image_zoom_fork) on the BMP conversion
      -> byte-compare renderA.bmp (the held frame) to the input BMP
      -> the understanding render is inspected for faceting (motif stage)

Pass criterion: (a) and (b) held frames byte-identical to inputs. Faceting in
the understanding render then localizes to motif fitting, not intake.
"""
import hashlib, os, shutil, subprocess, sys

HOME = os.path.expanduser("~")
LAB = os.path.join(HOME, "workspace/tnn-lab")
ZNC = os.path.join(LAB, "toolchain/bin/znc_linux_x86_64_abed8aa1")
CSRC = os.path.join(LAB, "imagination/video-composer-step2/src/composer.zag")
ZB = os.path.join(HOME, "workspace/image_zoom_fork/ingest_bin")
WORK = os.path.join(HOME, "workspace/intake_verdict")

def sh(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        raise RuntimeError("FAILED: %s\n%s" % (cmd, r.stderr[-2000:]))
    return r.stdout

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def main():
    from PIL import Image, ImageDraw
    W, H = 512, 187
    im = Image.new("RGB", (W, H), (128, 128, 128))
    d = ImageDraw.Draw(im)
    d.ellipse([100-48, 95-48, 100+48, 95+48], outline=(255, 255, 255), width=2)
    d.ellipse([200-28, 120-28, 200+28, 120+28], fill=(255, 0, 0))
    d.ellipse([300-18, 60-18, 300+18, 60+18], fill=(0, 0, 255))
    d.ellipse([400-36, 110-36, 400+36, 110+36], outline=(0, 255, 0), width=3)
    ppm = os.path.join(WORK, "circ_test.ppm")
    bmp = os.path.join(WORK, "circ_test.bmp")
    im.save(ppm); im.save(bmp)

    # (a) composer still path
    bdir = os.path.join(WORK, "repro_vc/src")
    os.makedirs(bdir, exist_ok=True)
    shutil.copy(CSRC, os.path.join(bdir, "composer.zag"))
    link = os.path.join(WORK, "tnn-lab")
    if not os.path.islink(link):
        os.symlink(LAB, link)
    sh([ZNC, "composer.zag", "-o", "composer_bin"], cwd=bdir)
    BIN = os.path.join(bdir, "composer_bin")
    outs = []
    for tag in ("A", "B"):
        wd = os.path.join(WORK, "circ_still" + tag)
        os.makedirs(wd, exist_ok=True)
        sh([BIN, "stillingest", "circ", ppm, os.path.join(wd, "ing")])
        o = os.path.join(wd, "out.ppm")
        sh([BIN, "stillrecall", os.path.join(wd, "ing"), o])
        outs.append(o)
    a_ok = sha(ppm) == sha(outs[0]) == sha(outs[1])

    # (b) zoom fork ingest (held frame = renderA)
    assert os.path.isfile(ZB), "zoom fork ingest_bin missing: " + ZB
    ind = os.path.join(WORK, "circ_zindir"); out = os.path.join(WORK, "circ_zout")
    os.makedirs(ind, exist_ok=True); os.makedirs(out, exist_ok=True)
    shutil.copy(bmp, os.path.join(ind, "original_512.bmp"))
    sh([ZB, ind, out, "circ_kmap.bin", "circ_renderA.bmp"])
    b_ok = sha(bmp) == sha(os.path.join(out, "circ_renderA.bmp"))

    print("still path byte-identical x2:", a_ok, sha(ppm)[:16])
    print("zoom-fork held frame byte-identical:", b_ok, sha(bmp)[:16])
    print("CIRCLE VERDICT:", "INTAKE EXONERATED" if (a_ok and b_ok) else "INTAKE LOSS")
    print("(faceting, if present, lives in render_understanding.bmp = motif fitting)")
    return 0 if (a_ok and b_ok) else 1

if __name__ == "__main__":
    sys.exit(main())
