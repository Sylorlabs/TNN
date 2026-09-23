#!/usr/bin/env python3
"""STEP 2 — tcp_transform self-checks (glue only; transforms are pure-Zag).
(a) T(T(x)) SHA256 == SHA256(x) for all 185 fixtures (involution).
(b) Transformed header re-parses with identical W,H / rate,count / F,W,H.
Exits nonzero on any failure."""
import hashlib, json, os, struct, subprocess, sys

CHAN = os.path.dirname(os.path.abspath(__file__))
FIXROOT = os.path.normpath(os.path.join(CHAN, "..", "..", "..", "senses", "rebuild", "harness", "fixtures"))
BIN = os.path.join(CHAN, "src", "tcp_transform")
TMP = "/home/hatch/workspace/tmp_tcp"

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def parse_hdr(p, ext):
    b = open(p, "rb").read()
    if ext == "img":
        w, h = struct.unpack("<II", b[:8]); return ("img", w, h), len(b)
    if ext == "pcm":
        r, c = struct.unpack("<II", b[:8]); return ("pcm", r, c), len(b)
    if ext == "vid":
        f, w, h = struct.unpack("<III", b[:12]); return ("vid", f, w, h), len(b)
    raise ValueError(ext)

def main():
    man = json.load(open(os.path.join(CHAN, "inputs_tcp", "blob_manifest.json")))
    fails = []
    for i, r in enumerate(man):
        src = os.path.join(FIXROOT, r["relpath"])
        t1 = os.path.join(TMP, "t1_%d.bin" % i)
        t2 = os.path.join(TMP, "t2_%d.bin" % i)
        for outp, inp in ((t1, src), (t2, t1)):
            q = subprocess.run([BIN, r["task"], inp, outp], capture_output=True, text=True)
            if q.returncode != 0:
                fails.append((r["relpath"], "transform rc=%d: %s" % (q.returncode, q.stdout.strip())))
                break
        else:
            if sha(t2) != sha(src):
                fails.append((r["relpath"], "involution mismatch"))
            ext = r["relpath"].rsplit(".", 1)[-1]
            hx, _ = parse_hdr(src, ext)
            ht, _ = parse_hdr(t1, ext)
            if hx != ht:
                fails.append((r["relpath"], "header %s != %s" % (ht, hx)))
            # byte-size preserved
            if os.path.getsize(t1) != os.path.getsize(src):
                fails.append((r["relpath"], "size changed"))
    for rp, why in fails:
        print("FAIL", rp, why)
    print("checked %d fixtures, %d failures" % (len(man), len(fails)))
    return 1 if fails else 0

sys.exit(main())
