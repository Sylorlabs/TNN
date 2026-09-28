"""validate_vid.py — prove vidio.write_vid matches the harness .vid layout.

Checks:
 1. Byte-identical output to harness gen.py's write_vid() on synthetic frames
    (same frame bytes, incl. RGB-tuple pixel sources like gen.py emits).
 2. A real harness .vid fixture (t6_motiondir p000) has header (8,64,64) and
    total size 12 + 8*64*64*3, i.e. the layout we emit is what sense.zag reads.
"""
import os, struct, sys, hashlib

WORK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, WORK)
from vidio import write_vid, read_vid_header  # noqa: E402

HARNESS_GEN = os.path.expanduser(
    "~/workspace/tnn-lab/senses/rebuild/harness/gen.py")
REAL_VID = os.path.expanduser(
    "~/workspace/tnn-lab/senses/rebuild/harness/fixtures/t6_motiondir/primary/p000.vid")

# --- reference implementation copied verbatim from harness gen.py (lines 155-182)
def _flat(px):
    out = bytearray()
    for p in px:
        if isinstance(p, (tuple, list)):
            out.extend(p)
        else:
            out.append(p)
    return bytes(out)

def ref_write_vid(path, w, h, frames):
    with open(path, "wb") as f:
        f.write(struct.pack("<III", len(frames), w, h))
        for fr in frames:
            f.write(_flat(fr))
# --- end verbatim copy

def synth_frames():
    # 8 frames of 64x64; pixel tuples like gen.py's motiondir writer emits.
    # Deterministic pattern: diagonal bar shifting 2px/frame (no RNG).
    frames = []
    for t in range(8):
        px = []
        for y in range(64):
            for x in range(64):
                if abs((x - y) - 2 * t) < 3:
                    px.append((255, 255, 255))
                else:
                    px.append(((x * 3) % 256, (y * 5) % 256, 128))
        frames.append(px)
    return frames

def main():
    outdir = os.path.join(WORK, "validation")
    os.makedirs(outdir, exist_ok=True)
    frames = synth_frames()

    p_mine = os.path.join(outdir, "synth_mine.vid")
    p_ref = os.path.join(outdir, "synth_ref.vid")
    write_vid(p_mine, 64, 64, [_flat(fr) for fr in frames])
    ref_write_vid(p_ref, 64, 64, frames)

    a = open(p_mine, "rb").read()
    b = open(p_ref, "rb").read()
    print("mine size:", len(a), "ref size:", len(b))
    print("sha mine:", hashlib.sha256(a).hexdigest())
    print("sha ref :", hashlib.sha256(b).hexdigest())
    ok1 = a == b
    print("CHECK1 byte-identical to harness write_vid:", "PASS" if ok1 else "FAIL")

    nf, w, h = read_vid_header(REAL_VID)
    sz = os.path.getsize(REAL_VID)
    exp = 12 + nf * w * h * 3
    print("real fixture header:", (nf, w, h), "size:", sz, "expected:", exp)
    ok2 = (nf, w, h) == (8, 64, 64) and sz == exp
    print("CHECK2 real fixture matches emitted layout:", "PASS" if ok2 else "FAIL")

    # payload framing: 8 equal frames of 64*64*3 in the real fixture
    ok3 = sz == 12 + 8 * 64 * 64 * 3
    print("CHECK3 real fixture payload framing 8x64x64x3:", "PASS" if ok3 else "FAIL")

    ok = ok1 and ok2 and ok3
    print("VALIDATION:", "PASS" if ok else "FAIL")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
