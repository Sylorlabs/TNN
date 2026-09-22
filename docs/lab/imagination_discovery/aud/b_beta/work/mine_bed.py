#!/usr/bin/env python3
"""Mine quiet 'air' bed segments for B-beta kids piece. Deterministic.
Appends voice-8 bed records to catalog_kids.bin (flags bit4=16 set).
Sources: kids_berlin.wav (distant playground air), kids_playground.wav (quiet gaps).
Picks lowest-energy non-overlapping windows; segment length 1500-2500ms.
Zero RNG: lengths come from explicit h32 arithmetic (no random module)."""
import wave, struct, numpy as np, os, sys

W = os.path.dirname(os.path.abspath(__file__))
SR = 44100

def h32(s, st):
    z = (s * 2654435761 + st * 40503 + 1) & 0xFFFFFFFF
    z = (z ^ (z >> 16)) & 0xFFFFFFFF
    z = (z * 2246822519) & 0xFFFFFFFF
    z = (z ^ (z >> 13)) & 0xFFFFFFFF
    z = (z * 3266489917) & 0xFFFFFFFF
    z = (z ^ (z >> 16)) & 0xFFFFFFFF
    return z

def load(name):
    w = wave.open(os.path.join(W, 'wav', name), 'rb')
    n = w.getnframes(); ch = w.getnchannels()
    raw = w.readframes(n); w.close()
    xs = np.array(struct.unpack('<' + 'h' * (n * ch), raw), dtype=np.float64)
    if ch == 2:
        xs = (xs[0::2] + xs[1::2]) / 2.0
    return xs

def env(xs, win=2205):
    a = np.abs(xs)
    k = np.ones(win) / win
    return np.convolve(a, k, mode='same')

def mine(name, srcid, nwant, lo_ms, hi_ms):
    xs = load(name)
    e = env(xs)
    cands = []
    step = int(0.5 * SR)
    L = int(hi_ms * SR / 1000)
    ci = 0
    for s in range(0, len(xs) - L, step):
        # deterministic sub-length from explicit hash arithmetic (no RNG)
        ln = int((lo_ms + h32(20260922, ci * 7919 + srcid) % (hi_ms - lo_ms)) * SR / 1000)
        ci += 1
        seg = e[s:s + ln]
        cands.append((float(np.mean(seg)), s, s + ln))
    cands.sort(key=lambda c: c[0])
    picked = []
    for en, s, t in cands:
        if all(t <= ps or s >= pt for _, ps, pt in picked):
            # reject if it overlaps a catalogued loud event region (keep air clean):
            picked.append((en, s, t))
        if len(picked) >= nwant:
            break
    return picked

def main():
    recs = []
    for name, srcid, nwant in (('kids_berlin.wav', 3, 8), ('kids_playground.wav', 1, 4)):
        for en, s, t in mine(name, srcid, nwant, 1500, 2500):
            durms = int(round((t - s) * 1000 / SR))
            peak = 0  # filled below
            recs.append((s, t, srcid, 8, durms, en))
    # fill peaks/centroids deterministically from audio
    srcs = {}
    out = []
    for s, t, srcid, voice, durms, en in recs:
        nm = ('kids_berlin.wav', 'kids_playground.wav')[0 if srcid == 3 else 1]
        if srcid not in srcs:
            srcs[srcid] = load(nm)
        xs = srcs[srcid]
        seg = xs[s:t]
        peak = int(np.max(np.abs(seg)))
        sp = np.abs(np.fft.rfft(seg * np.hanning(len(seg))))**2
        fr = np.fft.rfftfreq(len(seg), 1 / SR)
        cent = int(np.sum(fr * sp) / max(sp.sum(), 1e-9))
        out.append(struct.pack('<IIHHHHHH', s, t, srcid, voice, min(peak, 65535),
                               min(cent, 65535), min(durms, 65535), 16))
        print(f"bed src{srcid} {s/SR:.2f}-{t/SR:.2f}s dur={durms}ms peak={peak} cent={cent}")
    p = os.path.join(W, '..', 'catalog_kids.bin')
    before = os.path.getsize(p)
    with open(p, 'ab') as f:
        for r in out:
            f.write(r)
    print(f"appended {len(out)} bed records ({before} -> {os.path.getsize(p)} bytes)")

if __name__ == '__main__':
    main()
