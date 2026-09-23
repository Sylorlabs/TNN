#!/usr/bin/env python3
"""Byte-exact .vid sub-clip slicer (glue, not a sense).

Reads an 8-frame 64x64 .vid and writes:
  <out>/<stem>_w1.vid : frames 0-3 (temporal window 1)
  <out>/<stem>_w2.vid : frames 4-7 (temporal window 2)
  <out>/<stem>_cl.vid : frames 0-7, x in [0,32)  (left crop)
  <out>/<stem>_cr.vid : frames 0-7, x in [32,64) (right crop)
Deterministic byte slicing only. Copies the .truth alongside the
whole-clip name (sub-clips share the clip's truth).
"""
import os, struct, sys

def read_vid(path):
    with open(path, "rb") as f:
        raw = f.read()
    nf, w, h = struct.unpack("<iii", raw[:12])
    fsz = w * h * 3
    assert len(raw) == 12 + nf * fsz, (path, len(raw), nf, w, h)
    frames = [raw[12 + i * fsz:12 + (i + 1) * fsz] for i in range(nf)]
    return nf, w, h, frames

def write_vid(path, w, h, frames):
    with open(path, "wb") as f:
        f.write(struct.pack("<iii", len(frames), w, h))
        for fr in frames:
            f.write(fr)

def crop(frames, w, h, x0, x1):
    out = []
    for fr in frames:
        buf = bytearray((x1 - x0) * h * 3)
        for y in range(h):
            src = (y * w + x0) * 3
            dst = y * (x1 - x0) * 3
            buf[dst:dst + (x1 - x0) * 3] = fr[src:src + (x1 - x0) * 3]
        out.append(bytes(buf))
    return out

def windowize(src, outdir):
    nf, w, h, frames = read_vid(src)
    assert nf == 8 and w == 64 and h == 64, (src, nf, w, h)
    stem = os.path.basename(src)[:-4]
    os.makedirs(outdir, exist_ok=True)
    write_vid(os.path.join(outdir, stem + "_w1.vid"), w, h, frames[0:4])
    write_vid(os.path.join(outdir, stem + "_w2.vid"), w, h, frames[4:8])
    write_vid(os.path.join(outdir, stem + "_cl.vid"), 32, h, crop(frames, w, h, 0, 32))
    write_vid(os.path.join(outdir, stem + "_cr.vid"), 32, h, crop(frames, w, h, 32, 64))

def main():
    srcs = sys.argv[1:-1]
    outdir = sys.argv[-1]
    for s in sorted(srcs):
        windowize(s, outdir)
    print("windowized %d clips -> %s" % (len(srcs), outdir))

main()
