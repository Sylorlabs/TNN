#!/usr/bin/env python3
"""Build run/bad.bin: the frozen 1,200-fact negative control lesson.
Reads the LAST key of run/facts.bin (sorted stream), then emits:
  200 wellformed dupes of that key        -> expect G2
  250 empty-text facts                    -> expect G1
  250 NUL-in-key facts                    -> expect G1
  250 circular dict definitions            -> expect G3
  250 sentences without terminal punct     -> expect G3
Expected histogram: g1=500, g2=200, g3=500, installed=0.
Record: [1B kind][2B key_len BE][4B text_len BE][key][text]
"""
import struct, os, sys

RUN = os.path.expanduser("~/workspace/tnn-lab/knowledge/ingest_1gb/run")

def rec(kind, key: bytes, text: bytes) -> bytes:
    return bytes([kind]) + struct.pack(">H", len(key)) + struct.pack(">I", len(text)) + key + text

def last_key(path):
    # stream once, keep only the last record's key (simple, O(n), low memory)
    with open(path, "rb") as f:
        last = None
        while True:
            hdr = f.read(7)
            if len(hdr) < 7:
                break
            klen = struct.unpack(">H", hdr[1:3])[0]
            tlen = struct.unpack(">I", hdr[3:7])[0]
            key = f.read(klen)
            f.seek(tlen, 1)
            last = key
    if last is None:
        raise SystemExit("facts.bin is empty")
    return last

def main():
    facts = os.path.join(RUN, "facts.bin")
    lk = last_key(facts)
    print(f"last key: {lk!r}")
    bad = []
    for _ in range(200):
        bad.append(rec(1, lk, b"dupe of the last real key probe"))
    for i in range(250):
        bad.append(rec(1, f"zzbad:e1:{i:04d}".encode(), b""))
    for i in range(250):
        bad.append(rec(1, b"zzbad\x00:e2:%04d" % i, b"nul key probe text"))
    for i in range(250):
        w = f"zzcirc{i:04d}".encode()
        bad.append(rec(1, b"wikt:en:" + w + b":noun:1", w))
    for i in range(250):
        bad.append(rec(3, f"zzbad:w:{i:04d}".encode(), b"this sentence has no terminal punctuation"))
    assert len(bad) == 1200
    with open(os.path.join(RUN, "bad.bin"), "wb") as f:
        for b in bad:
            f.write(b)
    print(f"bad.bin: {len(bad)} records")

if __name__ == "__main__":
    main()
