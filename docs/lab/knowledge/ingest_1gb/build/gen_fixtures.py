#!/usr/bin/env python3
"""Generate small synthetic fixtures for the ingest binary smoke test."""
import struct, sys

def rec(kind, key: bytes, text: bytes) -> bytes:
    return (bytes([kind]) + struct.pack(">H", len(key)) + struct.pack(">I", len(text)) + key + text)

recs = []
# 400 wiki (sort first)
for i in range(400):
    k = f"wiki:simple:article{i:04d}:sent001".encode()
    t = f"This is sentence number {i} about the world and its many wonders.".encode()
    recs.append((k, rec(3, k, t)))
# 800 dict
for i in range(800):
    w = f"word{i:04d}"
    k = f"wikt:en:{w}:noun:1".encode()
    t = f"a definition of {w} describing the thing in plain terms".encode()
    recs.append((k, rec(1, k, t)))
# 600 infl
for i in range(600):
    w = f"word{i:04d}"
    k = f"wikt:en:{w}:verb:3s".encode()
    t = f"third person singular present of {w}".encode()
    recs.append((k, rec(2, k, t)))
# 200 wn
for i in range(200):
    k = f"wn:3.1:synset{i:06d}".encode()
    t = f"gloss for synset number {i} with a short description".encode()
    recs.append((k, rec(4, k, t)))

recs.sort(key=lambda r: r[0])
with open(sys.argv[1], "wb") as f:
    for _, b in recs:
        f.write(b)
last_key = recs[-1][0]
print(f"facts: {len(recs)} last_key={last_key!r}")

# bad.bin: 200 dupes of last key, 250 empty-text, 250 NUL-key, 250 circular, 250 no-terminal
bad = []
for i in range(200):
    bad.append(rec(1, last_key, b"dupe of the last real key probe"))
for i in range(250):
    bad.append(rec(1, f"zzbad:e1:{i:04d}".encode(), b""))
for i in range(250):
    bad.append(rec(1, b"zzbad\x00:e2:%04d" % i, b"nul key probe text"))
for i in range(250):
    w = f"zzcirc{i:04d}".encode()
    bad.append(rec(1, b"wikt:en:" + w + b":noun:1", w))
for i in range(250):
    bad.append(rec(3, f"zzbad:w:{i:04d}".encode(), b"this sentence has no terminal punctuation"))
with open(sys.argv[2], "wb") as f:
    for b in bad:
        f.write(b)
print(f"bad: {len(bad)}")
