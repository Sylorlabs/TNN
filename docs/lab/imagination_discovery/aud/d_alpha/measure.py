#!/usr/bin/env python3
"""D-ALPHA measurement gates (analysis only, never generates audio):
1. basic signal stats (DC, peak, ZCR)
2. laugh-pulse segmentation + per-pulse f0/centroid/duration vs study
3. GESTURE UNIQUENESS: pairwise normalized xcorr of laugh pulses
   (pre-listening gate: no two pulses identical)
4. synth-smell forensics: formant movement (centroid variance),
   period jitter, no repeated 2s windows
"""
import os, sys
import numpy as np
from scipy.io import wavfile

SR = 44100

def load(p):
    sr, x = wavfile.read(p)
    assert sr == SR
    return x.astype(np.float64) / 32768.0

def envelope(x, win_ms=8):
    w = int(SR * win_ms / 1000)
    e = np.abs(x)
    return np.convolve(e, np.ones(w) / w, mode="same")

def segment(x, thr_frac=0.30, min_gap_ms=60, min_dur_ms=40):
    env = envelope(x)
    thr = thr_frac * env.max()
    above = env > thr
    out, i, n = [], 0, len(x)
    mg = int(SR * min_gap_ms / 1000)
    md = int(SR * min_dur_ms / 1000)
    while i < n:
        if above[i]:
            j = i
            while j < n and above[j]:
                j += 1
            k = j
            while k < min(n, j + mg) and not above[k]:
                k += 1
            if k < n and above[k]:
                j = k
                while j < n and above[j]:
                    j += 1
            if j - i >= md:
                out.append((i, j))
            i = j
        else:
            i += 1
    return out

def f0_ac(seg, fmin=150, fmax=1400):
    seg = seg - seg.mean()
    if len(seg) < int(SR / fmin) + 10:
        return None
    ac = np.correlate(seg, seg, mode="full")[len(seg)-1:]
    lo, hi = int(SR / fmax), min(int(SR / fmin), len(ac) - 1)
    if lo >= hi:
        return None
    return SR / (lo + np.argmax(ac[lo:hi]))

def centroid(seg):
    w = seg * np.hanning(len(seg))
    sp = np.abs(np.fft.rfft(w))
    fr = np.fft.rfftfreq(len(seg), 1 / SR)
    return float(np.sum(fr * sp) / (np.sum(sp) + 1e-12))

def basic(x, name):
    print(f"--- {name}: {len(x)/SR:.2f}s ---")
    print(f"  peak {np.abs(x).max():.3f}  DC {x.mean():+.6f}  "
          f"RMS {np.sqrt((x**2).mean()):.4f}")
    zc = np.mean(np.abs(np.diff(np.sign(x))) > 0)
    print(f"  ZCR {zc:.3f}")

def uniqueness(x, name):
    pulses = [p for p in segment(x) if (p[1]-p[0]) < SR*0.5]
    print(f"--- uniqueness {name}: {len(pulses)} pulses ---")
    if len(pulses) < 4:
        print("  too few pulses"); return
    # resample each pulse to 2048 pts, normalize
    vecs = []
    for a, b in pulses:
        seg = x[a:b]
        idx = (np.linspace(0, len(seg) - 1, 2048)).astype(int)
        v = seg[idx].astype(float)
        v = v - v.mean()
        n = np.linalg.norm(v)
        if n > 1e-9:
            vecs.append(v / n)
    mx, pair = -1, None
    for i in range(len(vecs)):
        for j in range(i + 1, len(vecs)):
            c = abs(float(np.dot(vecs[i], vecs[j])))
            if c > mx:
                mx, pair = c, (i, j)
    print(f"  max pairwise |xcorr| = {mx:.3f} (pulses {pair[0]},{pair[1]})")
    print(f"  GATE (no two alike, bar < 0.90): {'PASS' if mx < 0.90 else 'FAIL'}")
    # per-pulse params table
    print("  pulse: dur_ms  f0_Hz  centroid_Hz")
    for k, (a, b) in enumerate(pulses[:24]):
        seg = x[a:b]
        f = f0_ac(seg)
        fs = f"{f:.0f}" if f else "?"
        print(f"  p{k:02d}: {(b-a)/SR*1000:6.0f}  {fs:>6}  {centroid(seg):7.0f}")

def forensics(x, name):
    print(f"--- synth-smell forensics {name} ---")
    pulses = [p for p in segment(x) if (p[1]-p[0]) < SR*0.5]
    cents = [centroid(x[a:b]) for a, b in pulses]
    print(f"  centroid across pulses: mean {np.mean(cents):.0f} sd {np.std(cents):.0f} "
          f"(sd>250 => resonances MOVE, not static)")
    # no repeated 2s windows: self-similarity of 2s envelope chunks
    env = envelope(x, 20)
    L = 2 * SR
    chunks = [env[i:i+L] for i in range(0, len(env) - L, L // 2)]
    cn = [c / (np.linalg.norm(c) + 1e-12) for c in chunks]
    mx = 0
    for i in range(len(cn)):
        for j in range(i + 2, len(cn)):
            c = float(np.dot(cn[i], cn[j]))
            mx = max(mx, c)
    print(f"  max 2s-window self-similarity (non-adjacent): {mx:.3f} (bar < 0.90)")

if __name__ == "__main__":
    for p in sys.argv[1:]:
        x = load(p)
        basic(x, os.path.basename(p))
        uniqueness(x, os.path.basename(p))
        forensics(x, os.path.basename(p))
        print()
