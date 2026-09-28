#!/usr/bin/env python3
"""perceive.py — per-window G-ALL percept production (READINESS.md gate spec).

Usage: perceive.py [windows_dir] [out_jsonl] [subclip_cache_dir]
Per 8-frame 64x64 .vid window (stream order: sorted filename):
  1. Byte-exact slicing (mirrors sibling windowize.py):
       w1 = frames 0-3, w2 = frames 4-7, cl = x[0,32), cr = x[32,64)
  2. P1 = centroid-track on whole/w1/w2/cl/cr  (yt_sense/sense_t1,
     rematch-T4 fitted: STILL iff mag < 1)
  3. P2 = block-match on whole (code/src/method2, STILL iff mag < 1)
  4. gate.zag ALL over the six pairs in the exact sibling order
     (w1, w2, cl, cr, whole, m2) -> CANDIDATE | WITHHOLD + reason
Emits one JSON record per window with all six sub-judgments and the gate
verdict. Deterministic: pure-Zag senses, sorted order, no RNG, no clock.
The INSTALL/memory-rule layer lives in gate.py; nothing here touches memory.
"""
import json, os, re, struct, subprocess, sys

WORK = os.path.dirname(os.path.abspath(__file__))
SENSE = os.environ.get("SENSE_BIN", os.path.join(WORK, "yt_sense", "sense_t1"))
METHOD2 = os.environ.get("METHOD2_BIN", os.path.join(WORK, "code", "src", "method2"))
GATE = os.environ.get("GATE_BIN", os.path.join(WORK, "code", "src", "gate"))

def kv_parse(stdout):
    rec = {}
    for line in stdout.splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            rec[k.strip()] = v.strip()
    return rec

def sense_judgment(path):
    r = subprocess.run([SENSE, "motiondir", path], capture_output=True,
                       text=True, timeout=120)
    if r.returncode != 0:
        raise RuntimeError("sense failed on %s: %s" % (path, r.stdout.strip()[:200]))
    kv = kv_parse(r.stdout)
    dbg = kv.get("debug_vec", "")
    def dn(k):
        m = re.search(k + r"=(-?\d+)", dbg)
        return int(m.group(1)) if m else None
    return {"judgment": kv.get("judgment"), "confidence": int(kv.get("confidence", -1)),
            "dx": dn("dx"), "dy": dn("dy"), "mag": dn("mag")}

def m2_judgment(path):
    r = subprocess.run([METHOD2, path], capture_output=True,
                       text=True, timeout=300)
    if r.returncode != 0:
        raise RuntimeError("method2 failed on %s: %s" % (path, r.stdout.strip()[:200]))
    kv = kv_parse(r.stdout)
    dbg = kv.get("debug_vec", "")
    def dn(k):
        m = re.search(k + r"=(-?\d+)", dbg)
        return int(m.group(1)) if m else None
    return {"judgment": kv.get("judgment"), "confidence": int(kv.get("confidence", -1)),
            "sx": dn("sx"), "sy": dn("sy"), "mag": dn("mag")}

def gate_all(clip, pairs):
    args = [GATE, "ALL", clip]
    for (j, c) in pairs:
        args += [j, str(c)]
    r = subprocess.run(args, capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        raise RuntimeError("gate failed: %s" % r.stdout.strip()[:200])
    kv = kv_parse(r.stdout)
    return {"corroborated": kv.get("corroborated") == "1",
            "judgment": kv.get("judgment"),
            "confidence": int(kv.get("confidence", -1)),
            "decision": kv.get("decision"),
            "reason": kv.get("reason")}

def read_vid(path):
    with open(path, "rb") as f:
        raw = f.read()
    nf, w, h = struct.unpack("<III", raw[:12])
    fsz = w * h * 3
    assert len(raw) == 12 + nf * fsz, path
    return nf, w, h, [raw[12 + i * fsz:12 + (i + 1) * fsz] for i in range(nf)]

def write_vid(path, w, h, frames):
    with open(path, "wb") as f:
        f.write(struct.pack("<III", len(frames), w, h))
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

def main():
    windows = sys.argv[1] if len(sys.argv) > 1 else os.path.join(WORK, "windows")
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(WORK, "percepts.jsonl")
    sub = sys.argv[3] if len(sys.argv) > 3 else os.path.join(WORK, "subclips_yt")
    os.makedirs(sub, exist_ok=True)
    files = sorted(f for f in os.listdir(windows) if f.endswith(".vid"))
    n = 0
    with open(out, "w") as fo:
        for fn in files:
            m = re.match(r"^(.+)_w(\d+)\.vid$", fn)
            if m:
                vid, idx = m.group(1), int(m.group(2))
                clipid = "%s_w%03d" % (vid, idx)
            else:
                vid, idx, clipid = fn[:-4], 0, fn[:-4]
            path = os.path.join(windows, fn)
            nf, w, h, frames = read_vid(path)
            assert nf == 8 and w == 64 and h == 64, (fn, nf, w, h)
            stem = fn[:-4]
            p_w1 = os.path.join(sub, stem + "_w1.vid"); write_vid(p_w1, w, h, frames[0:4])
            p_w2 = os.path.join(sub, stem + "_w2.vid"); write_vid(p_w2, w, h, frames[4:8])
            p_cl = os.path.join(sub, stem + "_cl.vid"); write_vid(p_cl, 32, h, crop(frames, w, h, 0, 32))
            p_cr = os.path.join(sub, stem + "_cr.vid"); write_vid(p_cr, 32, h, crop(frames, w, h, 32, 64))
            whole = sense_judgment(path)
            w1 = sense_judgment(p_w1)
            w2 = sense_judgment(p_w2)
            cl = sense_judgment(p_cl)
            cr = sense_judgment(p_cr)
            m2 = m2_judgment(path)
            pairs = [(w1["judgment"], w1["confidence"]),
                     (w2["judgment"], w2["confidence"]),
                     (cl["judgment"], cl["confidence"]),
                     (cr["judgment"], cr["confidence"]),
                     (whole["judgment"], whole["confidence"]),
                     (m2["judgment"], m2["confidence"])]
            g = gate_all(clipid, pairs)
            rec = {"video_id": vid, "window_idx": idx, "window_path": fn,
                   "whole": whole, "w1": w1, "w2": w2, "cl": cl, "cr": cr,
                   "m2": m2, "gate": g}
            fo.write(json.dumps(rec, sort_keys=True) + "\n")
            n += 1
    print("percepts written: %d -> %s" % (n, out))

if __name__ == "__main__":
    sys.exit(main())
