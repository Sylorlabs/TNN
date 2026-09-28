#!/usr/bin/env python3
"""Zero-lag normalized cross-correlation between the two MOTIF-A windows
of a rendered WAV (44-byte header, i16 mono 44.1kHz).
Window 1: t=2.0..5.15 s ; Window 2: t=24.0..27.15 s (identical plan params).
"""
import struct, sys, math

def read_wav(path):
    with open(path, "rb") as f:
        data = f.read()
    assert data[0:4] == b"RIFF" and data[8:12] == b"WAVE", "not a wav"
    raw = data[44:]
    n = len(raw) // 2
    return struct.unpack("<%dh" % n, raw[: n * 2])

def xcorr(a, b):
    n = min(len(a), len(b))
    ma = sum(a[:n]) / n
    mb = sum(b[:n]) / n
    num = sum((a[i] - ma) * (b[i] - mb) for i in range(n))
    da = math.sqrt(sum((a[i] - ma) ** 2 for i in range(n)))
    db = math.sqrt(sum((b[i] - mb) ** 2 for i in range(n)))
    return num / (da * db) if da and db else 0.0

SR = 44100
for path in sys.argv[1:]:
    s = read_wav(path)
    w1 = s[int(2.0 * SR) : int(5.15 * SR)]
    w2 = s[int(24.0 * SR) : int(27.15 * SR)]
    print("%s motif xcorr = %.6f" % (path, xcorr(w1, w2)))
