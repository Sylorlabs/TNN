#!/usr/bin/env python3
"""Analyze a B-beta render: block structure, gaps, DC, ZCR, peak. Deterministic."""
import wave, struct, numpy as np, sys

def load(p):
    w = wave.open(p, 'rb')
    n = w.getnframes(); ch = w.getnchannels()
    raw = w.readframes(n); w.close()
    xs = np.array(struct.unpack('<' + 'h' * (n * ch), raw), dtype=np.float64)
    if ch == 2:
        xs = (xs[0::2] + xs[1::2]) / 2.0
    return xs

def envelope(xs, win=441):
    a = np.abs(xs)
    k = np.ones(win) / win
    return np.convolve(a, k, mode='same')

def main(p):
    xs = load(p)
    sr = 44100
    n = len(xs)
    print(f"file={p} dur={n/sr:.2f}s peak={int(np.max(np.abs(xs)))} mean={np.mean(xs):.2f}")
    zc = np.sum((xs[:-1] < 0) != (xs[1:] < 0)) / (n - 1)
    print(f"zcr={zc:.4f}")
    env = envelope(xs)
    thr = np.median(env) * 2 + 600
    for b in range(6):
        s0 = b * 5 * sr
        seg = env[s0:s0 + 5 * sr]
        ne = 0; i = 0
        while i < len(seg):
            if seg[i] > thr:
                ne += 1
                while i < len(seg) and seg[i] > thr * 0.35:
                    i += 1
            i += 1
        xseg = xs[s0:s0 + 5 * sr]
        print(f"  block {b*5:2d}-{(b+1)*5:2d}s: events~{ne:2d} maxenv={int(np.max(seg)):5d} rms={int(np.sqrt(np.mean(xseg**2))):5d}")
    quiet = env < 300
    gaps = []; i = 0
    while i < len(quiet):
        if quiet[i]:
            s = i
            while i < len(quiet) and quiet[i]:
                i += 1
            if (i - s) > 22050:
                gaps.append((s / sr, (i - s) / sr))
        else:
            i += 1
    print("gaps>500ms:", [(round(a, 1), round(d, 2)) for a, d in gaps[:12]] or "none")

if __name__ == '__main__':
    main(sys.argv[1])
