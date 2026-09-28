#!/usr/bin/env python3
"""Deterministic probe of B-beta source WAVs. No randomness. Prints stats."""
import wave, struct, math, sys, os

def load(p):
    w = wave.open(p, 'rb')
    n = w.getnframes(); ch = w.getnchannels(); sr = w.getframerate()
    raw = w.readframes(n); w.close()
    fmt = '<' + 'h' * (n * ch)
    xs = struct.unpack(fmt, raw)
    if ch == 2:
        xs = [(xs[i] + xs[i+1]) // 2 for i in range(0, len(xs), 2)]
    return sr, list(xs)

def stats(name, xs, sr):
    n = len(xs)
    peak = max(abs(x) for x in xs)
    rms = math.sqrt(sum(x*x for x in xs) / n)
    # 1-second block RMS profile (first 12 blocks) + loudest block index
    bs = sr
    blocks = [xs[i:i+bs] for i in range(0, n, bs)]
    brms = [math.sqrt(sum(x*x for x in b)/len(b)) if b else 0 for b in blocks]
    loud = max(range(len(brms)), key=lambda i: brms[i])
    # spectral centroid approx via zero-crossing rate + block energy
    zc = sum(1 for i in range(1, n) if (xs[i-1] < 0) != (xs[i] < 0)) / n
    # crest: top-10 peak positions (seconds)
    order = sorted(range(n), key=lambda i: abs(xs[i]), reverse=True)
    tops = []
    for i in order:
        t = i / sr
        if all(abs(t - u) > 0.25 for u in tops):
            tops.append(t)
        if len(tops) == 8:
            break
    tops.sort()
    print(f"== {name}: {n/sr:.1f}s peak={peak} rms={rms:.0f} zcr={zc:.3f} loudest_1s_block={loud}")
    print(f"   block_rms[:12]={[int(v) for v in brms[:12]]}")
    print(f"   loudest_moments_s={[round(t,2) for t in tops]}")

if __name__ == '__main__':
    d = os.path.expanduser('~/workspace/tnn-lab/imagination_discovery/aud/b_beta/work/wav')
    for f in sys.argv[1:] or sorted(os.listdir(d)):
        if f.endswith('.wav'):
            sr, xs = load(os.path.join(d, f))
            stats(f, xs, sr)
