#!/usr/bin/env python3
"""Measure semantic-ceiling (mode 11) vs fixture: RMS err (LSB), corr, max|d|."""
import sys, struct
import numpy as np

def read_wav(path):
    d = open(path, 'rb').read()
    off = 12
    while off + 8 < len(d):
        if d[off:off+4] == b'data':
            sz = struct.unpack('<I', d[off+4:off+8])[0]
            n = sz // 2
            x = np.frombuffer(d[off+8:off+8+2*n], dtype='<i2').astype(np.float64)
            return x
        sz = struct.unpack('<I', d[off+4:off+8])[0]
        off += 8 + sz
    raise ValueError('no data chunk')

for fix, sem in [(sys.argv[1], sys.argv[2])]:
    x = read_wav(fix)
    y = read_wav(sem)
    n = min(len(x), len(y))
    x, y = x[:n], y[:n]
    d = y - x
    rms = float(np.sqrt((d**2).mean()))
    mx = float(np.abs(d).max())
    mx_i = int(np.abs(d).argmax())
    # correlation
    xm, ym = x - x.mean(), y - y.mean()
    corr = float((xm*ym).sum() / (np.sqrt((xm**2).sum() * (ym**2).sum()) + 1e-12))
    print(f"n={n} rms_err_LSB={rms:.3f} max_abs_d={mx:.1f} at_i={mx_i} corr={corr:.6f}")
