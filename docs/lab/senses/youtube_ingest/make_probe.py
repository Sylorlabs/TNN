#!/usr/bin/env python3
"""make_probe.py — build the YT1 held-out adversarial probe set.

Synthetic .vid fixtures with known truth, DISJOINT from the KB4-VIDEO
readiness fixtures (those come from rebuild/harness; these are generated
here with a different seed/structure, never shared with the readiness trial).

Recipes (mirror the adversarial motion profile, KB4-VIDEO prereg §2):
  - ADV: 8 frames 64x64, textured panel translating 1px/frame at 0.25
    contrast on mid-gray background, known 8-way truth. The fitted sense
    must often get these right; the GATE decides install/withhold.
  - STILL: identical textured panel, zero translation (truth STILL).
  - PRIMARY-like: 2px/frame full-contrast translation, truth known.
    Sanity that true percepts are not false installs.

Zero RNG: panel texture = deterministic hash of (x,y,seed_id) — not random,
fully reproducible. Truth written to probe_manifest.tsv.
"""
import os, struct, sys

WORK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, WORK)
from vidio import write_vid  # noqa: E402

OUT = os.path.join(WORK, "probe_heldout")
W = H = 64
NF = 8
BG = (128, 128, 128)

def texel(x, y, sid):
    # deterministic texture: splitmix-ish hash of coordinates
    z = (x * 0x9E3779B97F4A7C15 + y * 0xBF58476D1CE4E5B9 + sid * 0x94D049BB133111EB) & 0xFFFFFFFFFFFFFFFF
    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & 0xFFFFFFFFFFFFFFFF
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & 0xFFFFFFFFFFFFFFFF
    return (z >> 56) & 0xFF

DIRS = {"N": (0, -1), "NE": (1, -1), "E": (1, 0), "SE": (1, 1),
        "S": (0, 1), "SW": (-1, 1), "W": (-1, 0), "NW": (-1, -1)}

def make(name, direction, step_px, contrast, sid):
    """direction=None -> static. contrast in (0,1]: blend of texture toward BG."""
    frames = []
    dx, dy = DIRS[direction] if direction else (0, 0)
    for t in range(NF):
        ox = int(round(dx * step_px * t))
        oy = int(round(dy * step_px * t))
        px = bytearray(W * H * 3)
        for y in range(H):
            for x in range(W):
                sx, sy = x - ox, y - oy
                v = texel(sx % W, sy % H, sid) if (0 <= sx < W and 0 <= sy < H) else 128
                c = int(round(BG[0] + (v - BG[0]) * contrast))
                o = (y * W + x) * 3
                px[o] = px[o + 1] = px[o + 2] = c
        frames.append(bytes(px))
    path = os.path.join(OUT, name + ".vid")
    write_vid(path, W, H, frames)
    return path

def main():
    os.makedirs(OUT, exist_ok=True)
    man = []
    sid = 0
    # adversarial: 1px/frame, 0.25 contrast, all 8 directions + STILL
    for d in sorted(DIRS):
        sid += 1
        make("adv_%s" % d, d, 1.0, 0.25, sid)
        man.append(("adv_%s" % d, d, "adversarial"))
    sid += 1
    make("adv_STILL", None, 0, 0.25, sid)
    man.append(("adv_STILL", "STILL", "adversarial"))
    # primary-like: 2px/frame, full contrast, 4 directions
    for d in ["N", "E", "S", "W"]:
        sid += 1
        make("pri_%s" % d, d, 2.0, 1.0, sid)
        man.append(("pri_%s" % d, d, "primary-like"))
    with open(os.path.join(OUT, "probe_manifest.tsv"), "w") as f:
        f.write("# name\ttruth\tclass\n")
        for name, truth, cls in man:
            f.write("%s\t%s\t%s\n" % (name, truth, cls))
    print("probe fixtures: %d -> %s" % (len(man), OUT))

if __name__ == "__main__":
    sys.exit(main())
