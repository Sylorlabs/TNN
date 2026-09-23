#!/usr/bin/env python3
"""rerun_yt3.py — YT3 determinism check: converter + sense on ONE full video,
twice, byte-compared.

Usage: rerun_yt3.py <video_id>
Re-converts raw/<video_id>.mp4 into rerun_yt3/windows (fresh), sha256-compares
each .vid against windows/<same>, then re-perceives and compares the JSON
records field-by-field against percepts_full.jsonl (same video). Prints
PASS/FAIL. Zero RNG; the only inputs are the downloaded bytes.
"""
import hashlib, json, os, subprocess, sys

WORK = os.path.dirname(os.path.abspath(__file__))
VENV_PY = os.path.join(WORK, "venv", "bin", "python")

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()

def main():
    vid = sys.argv[1]
    rdir = os.path.join(WORK, "rerun_yt3")
    wdir = os.path.join(rdir, "windows")
    os.makedirs(wdir, exist_ok=True)
    # 1. re-convert: same ffmpeg recipe as convert.py, stride 30
    src = os.path.join(WORK, "raw", vid + ".mp4")
    rawf = os.path.join(rdir, vid + "_frames.raw")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src,
                    "-vf", r"crop=min(iw\,ih):min(iw\,ih),scale=64:64",
                    "-pix_fmt", "rgb24", "-f", "rawvideo", rawf], check=True)
    data = open(rawf, "rb").read()
    fsz = 64 * 64 * 3
    total = len(data) // fsz
    k = 0
    names = []
    while k * 30 + 8 <= total:
        name = "%s_w%03d.vid" % (vid, k)
        with open(os.path.join(wdir, name), "wb") as f:
            import struct
            f.write(struct.pack("<III", 8, 64, 64))
            for j in range(8):
                o = (k * 30 + j) * fsz
                f.write(data[o:o + fsz])
        names.append(name)
        k += 1
    os.remove(rawf)
    # 2. byte-compare .vid files
    ok1 = True
    for name in names:
        a, b = sha(os.path.join(wdir, name)), sha(os.path.join(WORK, "windows", name))
        if a != b:
            ok1 = False
            print("VID MISMATCH", name)
    print("converter byte-compare: %d windows, %s" % (len(names), "PASS" if ok1 else "FAIL"))
    # 3. re-perceive and compare records
    out = os.path.join(rdir, "percepts_rerun.jsonl")
    subprocess.run([VENV_PY, os.path.join(WORK, "perceive.py"), wdir, out,
                    os.path.join(rdir, "sub")], check=True,
                   capture_output=True)
    new = [json.loads(l) for l in open(out)]
    old = [json.loads(l) for l in open(os.path.join(WORK, "percepts_full.jsonl"))
           if json.loads(l)["video_id"] == vid]
    ok2 = (len(new) == len(old) and
           all(json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)
               for a, b in zip(sorted(new, key=lambda r: r["window_idx"]),
                               sorted(old, key=lambda r: r["window_idx"]))))
    print("sense record compare: %d vs %d records, %s" % (len(new), len(old), "PASS" if ok2 else "FAIL"))
    print("YT3:", "PASS" if (ok1 and ok2) else "FAIL")
    return 0 if (ok1 and ok2) else 1

if __name__ == "__main__":
    sys.exit(main())
