#!/usr/bin/env python3
"""NO-COPY AUDIT: no 2s output window within min-variation bar of any source.
Bar: max normalized cross-correlation (2s windows, 1s hop, zero-mean) < 0.75.
Deterministic. Usage: nocopy.py <output.wav> <src1.wav> [src2.wav ...]
Exit 0 = PASS, 1 = FAIL."""
import wave, struct, numpy as np, sys

def load(p):
    w = wave.open(p, 'rb')
    n = w.getnframes(); ch = w.getnchannels()
    raw = w.readframes(n); w.close()
    xs = np.array(struct.unpack('<' + 'h' * (n * ch), raw), dtype=np.float32)
    if ch == 2:
        xs = (xs[0::2] + xs[1::2]) / 2.0
    return xs - np.mean(xs)

def main():
    out = load(sys.argv[1])
    worst = (0.0, None, None)
    for sp in sys.argv[2:]:
        src = load(sp)
        W = min(2 * 44100, len(src))  # short sources compare at their own length
        if W < 2205:
            continue
        hop = max(W // 2, 2205)
        owins = [out[i:i + W] for i in range(0, len(out) - W + 1, hop)]
        onorm = np.array([np.sqrt(np.sum(w * w)) + 1e-9 for w in owins])
        swins = [src[i:i + W] for i in range(0, len(src) - W + 1, hop)]
        snorm = np.array([np.sum(w * w) for w in swins])
        for oi, ow in enumerate(owins):
            if onorm[oi] < 1e-6:
                continue
            dots = np.array([float(np.dot(ow, sw)) for sw in swins])
            ncc = dots / (onorm[oi] * np.sqrt(snorm + 1e-9))
            j = int(np.argmax(ncc))
            if ncc[j] > worst[0]:
                worst = (float(ncc[j]), sp, (oi, j))
    print(f"worst 2s-window NCC = {worst[0]:.3f}  (out_win {worst[2][0]}, src {worst[1].split('/')[-1]} win {worst[2][1]})")
    bar = 0.75
    if worst[0] < bar:
        print(f"NO-COPY AUDIT: PASS (< {bar})")
        return 0
    print(f"NO-COPY AUDIT: FAIL (>= {bar})")
    return 1

if __name__ == '__main__':
    sys.exit(main())
