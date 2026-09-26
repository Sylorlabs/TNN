#!/usr/bin/env python3
"""Independent white-box verification of the Zag stage traces.

Recomputes FNV-1a/64 over the actual stage bytes and checks them against the
hashes the Zag binary wrote into the trace files. Any mismatch = the trace
is dishonest or a stage mutated bytes unexpectedly.

Stages:
  H_I: frame bytes as INGESTED (read from source PPM by the Zag ingestor)
  H_S: bytes as STORED in the deliberate-memory payload region
  H_R: bytes as RECALLED (returned by mem_recall)
  H_E: bytes as EMITTED (the exact bytes handed to the OS for the output PPM)

Checks:
  verbatim: H_I == fnv(src px); H_S == fnv(store payloads); stored == src px
            H_R == fnv(out px); out px == src px  (end-to-end lossless)
  encoded:  H_S == fnv(python 2x2-downsample(src px))  (loss ONLY the downsample)
            H_R == fnv(out-downsampled==stored); out == python-upsample(stored)
Usage: verify_traces.py <srcdir> <runsdir>
"""
import os, re, sys

SRC, RUNS = sys.argv[1], sys.argv[2]

def fnv(data: bytes) -> int:
    h = 14695981039346656037
    for b in data:
        h ^= b
        h = (h * 1099511628211) & 0xFFFFFFFFFFFFFFFF
    return h

def read_ppm_px(path):
    with open(path, "rb") as f:
        data = f.read()
    assert data[:3] == b"P6\n", path
    # parse 3 header tokens
    p = 3
    toks = []
    while len(toks) < 3:
        while data[p:p+1] in b" \t\n\r":
            p += 1
        q = p
        while data[q:q+1] not in b" \t\n\r":
            q += 1
        toks.append(data[p:q]); p = q
    w, h, mv = int(toks[0]), int(toks[1]), int(toks[2])
    p += 1  # exactly one whitespace byte follows maxval per the P6 spec
    px = data[p:p + w*h*3]
    assert len(px) == w*h*3, (path, len(px))
    return w, h, px

def parse_trace(path):
    rows = {}
    with open(path) as f:
        for line in f:
            m = re.match(r"(INGEST|RECALL) f=(\d+) H([ISR E])=([0-9a-f]{16}) H([S E])=([0-9a-f]{16})".replace(" ", ""), line.strip())
            # simpler: split
            parts = line.strip().split()
            tag, ff = parts[0], int(parts[1].split("=")[1])
            h1 = int(parts[2].split("=")[1], 16)
            h2 = int(parts[3].split("=")[1], 16)
            rows[ff] = (tag, h1, h2)
    return rows

def downsample(px, w=320, h=240):
    import numpy as np
    a = np.frombuffer(px, dtype=np.uint8).reshape(h, w, 3).astype(np.uint16)
    ds = (a[0::2, 0::2] + a[0::2, 1::2] + a[1::2, 0::2] + a[1::2, 1::2]) // 4
    return ds.astype(np.uint8).tobytes()

def upsample(ds_bytes, w=160, h=120):
    import numpy as np
    a = np.frombuffer(ds_bytes, dtype=np.uint8).reshape(h, w, 3)
    return np.repeat(np.repeat(a, 2, axis=0), 2, axis=1).tobytes()

def store_payloads(store_path, frame, rows, plen, nframes=24):
    ns = nframes * rows
    with open(store_path, "rb") as f:
        data = f.read()
    base = 32 + ns * 32 + (frame * rows) * plen
    return data[base:base + rows * plen]

fails = 0
def check(name, cond, detail=""):
    global fails
    if cond:
        print(f"  ok   {name}")
    else:
        print(f"  FAIL {name} {detail}")
        fails += 1

for enc, rows, plen in (("verbatim", 240, 960), ("encoded", 120, 480)):
    print(f"== {enc} ==")
    store = os.path.join(RUNS, f"work_{enc}", f"store_{enc}.bin")
    ti = parse_trace(os.path.join(RUNS, f"work_{enc}", f"trace_ingest_{enc}.txt"))
    tr = parse_trace(os.path.join(RUNS, f"work_{enc}", f"trace_recall_{enc}.txt"))
    outd = os.path.join(RUNS, f"out_{enc}")
    for f in range(24):
        w, h, srcpx = read_ppm_px(os.path.join(SRC, f"frame_{f:02d}.ppm"))
        w2, h2, outpx = read_ppm_px(os.path.join(outd, f"frame_{f:02d}.ppm"))
        tag_i, HI, HS = ti[f]
        tag_r, HR, HE = tr[f]
        stored = store_payloads(store, f, rows, plen)
        check(f"f{f:02d} ingest read src faithfully", HI == fnv(srcpx), f"{HI:016x}")
        if enc == "verbatim":
            check(f"f{f:02d} stored == ingested (machinery lossless in)", HS == fnv(stored) and stored == srcpx)
            check(f"f{f:02d} recalled == stored (machinery lossless out)", HR == fnv(outpx) and outpx == srcpx)
        else:
            ds = downsample(srcpx)
            check(f"f{f:02d} stored == downsample(src) ONLY (knowledge loss = the 2x2)", HS == fnv(stored) and stored == ds)
            check(f"f{f:02d} recalled == stored; emitted == upsample(stored)", HR == fnv(stored) and outpx == upsample(stored))
    # H_E is over header+px; verify one frame's emitted bytes equal the file on disk
    w, h, px0 = read_ppm_px(os.path.join(outd, "frame_00.ppm"))
    raw = open(os.path.join(outd, "frame_00.ppm"), "rb").read()
    tag_r, HR0, HE0 = tr[0]
    check("f00 emitted-bytes hash == file on disk", HE0 == fnv(raw))

print("FAILURES:", fails)
sys.exit(1 if fails else 0)
