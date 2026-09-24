#!/usr/bin/env python3
"""build_rm2_clips.py — build RM2 .vid clips + labeling montages from the
mined shortlist. Zero RNG. Clips: frames t+j*b from decoded 64x64 raws.
Montages: frame0 vs frame7 side-by-side, 2x upscale (B3 convention)."""
import os
import struct
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

MINE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.expanduser("~/workspace/tnn-lab/senses/youtube_ingest")
FDIR = os.path.join(LAB, "motion4", "rm2", "fixtures")
MOND = os.path.join(MINE, "montages")
FSZ = 64 * 64 * 3

_cache = {}


def raw_frames(vid):
    if vid not in _cache:
        with open(os.path.join(MINE, vid + ".raw"), "rb") as f:
            data = f.read()
        n = len(data) // FSZ
        _cache[vid] = [data[i * FSZ:(i + 1) * FSZ] for i in range(n)]
    return _cache[vid]


def write_vid(path, frames):
    with open(path, "wb") as f:
        f.write(struct.pack("<iii", 8, 64, 64))
        for fr in frames:
            f.write(fr)


def montage(name, vid, b, t, kind, dir_lab, pair_wins, e_total):
    frames = raw_frames(vid)
    clip = [frames[t + j * b] for j in range(8)]
    f0 = Image.frombytes("RGB", (64, 64), clip[0]).resize((128, 128), Image.NEAREST)
    f7 = Image.frombytes("RGB", (64, 64), clip[7]).resize((128, 128), Image.NEAREST)
    im = Image.new("RGB", (256 + 8, 128), (0, 0, 0))
    im.paste(f0, (0, 0))
    im.paste(f7, (136, 0))
    im.save(os.path.join(MOND, name + ".png"))


def main():
    os.makedirs(FDIR, exist_ok=True)
    os.makedirs(MOND, exist_ok=True)
    n = 0
    for line in open(os.path.join(MINE, "rm2_mine_top.tsv")):
        if line.startswith("#"):
            continue
        kind, vid, b, t, dir_lab, pair_wins, e_total = line.rstrip("\n").split("\t")
        b, t = int(b), int(t)
        frames = raw_frames(vid)
        clip = [frames[t + j * b] for j in range(8)]
        name = "rm2_%s_b%d_t%04d" % (vid, b, t)
        vpath = os.path.join(FDIR, name + ".vid")
        write_vid(vpath, clip)
        montage(name, vid, b, t, kind, dir_lab, pair_wins, e_total)
        n += 1
    print("clips+montages built: %d" % n)


if __name__ == "__main__":
    sys.exit(main())
