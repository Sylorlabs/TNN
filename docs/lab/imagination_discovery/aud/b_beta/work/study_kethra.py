#!/usr/bin/env python3
"""Mine gesture catalogs from the Kethra/ocean sources.
Record format (20 bytes, same as catalog_kids.bin):
  start_u32, end_u32 (samples), src_u16, voice_u16, peak_u16, centroid_u16,
  durms_u16, flags_u16.
Deterministic: no RNG anywhere.
Sources: 6=ocean_tropical 7=sea_waves 8=loon_yodels 9=throat_singing 10=whale_song
"""
import wave, struct, numpy as np, os

SR = 44100
SRC = {'ocean_tropical': 6, 'sea_waves': 7, 'loon_yodels': 8,
       'throat_singing': 9, 'whale_song': 10}

def load(nm):
    w = wave.open('wav/' + nm + '.wav', 'rb')
    n = w.getnframes(); ch = w.getnchannels()
    raw = w.readframes(n); w.close()
    xs = np.array(struct.unpack('<' + 'h' * (n * ch), raw), dtype=np.float64)
    if ch == 2: xs = (xs[0::2] + xs[1::2]) / 2.0
    return xs

def spec_centroid(seg):
    if len(seg) < 256: return 0
    sp = np.abs(np.fft.rfft(seg * np.hanning(len(seg))))
    fr = np.fft.rfftfreq(len(seg), 1 / SR)
    e = np.sum(sp)
    return int(np.sum(fr * sp) / e) if e > 0 else 0

def env(xs, ms):
    # O(n) moving average via cumsum (np.convolve is O(n*k), unusable here)
    k = max(1, int(SR * ms / 1000))
    a = np.abs(xs).astype(np.float64)
    c = np.cumsum(a)
    out = np.empty_like(a)
    out[k:] = (c[k:] - c[:-k]) / k
    out[:k] = c[:k] / np.arange(1, k + 1)
    return out

def onsets(xs, thr_mult, min_gap_ms, min_dur_ms):
    e = env(xs, 20)
    thr = np.median(e) * thr_mult + 600
    evs = []
    i = 0
    while i < len(e):
        if e[i] > thr:
            s = i
            while i < len(e) and e[i] > thr * 0.25: i += 1
            if (i - s) > min_dur_ms * SR / 1000: evs.append((s, i))
            i += int(min_gap_ms * SR / 1000)
        else:
            i += 1
    return evs

recs = []

def add(s, e, src, voice, xs, flags=0):
    seg = xs[s:e]
    peak = int(min(np.max(np.abs(seg)), 32767))
    cent = min(spec_centroid(seg[::4] if len(seg) > 4096 else seg), 20000)
    recs.append((s, e, src, voice, peak, cent,
                 int((e - s) * 1000 / SR), flags))

# --- loon yodels: 4+ discrete rising gestures (voice 11, flags bit1=vocal) ---
xs = load('loon_yodels')
for (s, e) in onsets(xs, 2.0, 400, 250):
    pad = int(0.15 * SR)
    add(max(0, s - pad), min(len(xs), e + pad), 8, 11, xs, 2)
print('loon events:', len([r for r in recs if r[2] == 8]))

# --- whale song: phrases (voice 12, flags bit1=vocal) ---
xs = load('whale_song')
for (s, e) in onsets(xs, 2.2, 600, 400):
    pad = int(0.25 * SR)
    add(max(0, s - pad), min(len(xs), e + pad), 10, 12, xs, 2)
print('whale events:', len([r for r in recs if r[2] == 10]))

# --- throat singing: sustained low drones, 2-4 s windows with lowest
# spectral variance (voice 13). Take 6 non-overlapping windows. ---
xs = load('throat_singing')
W = int(3 * SR); step = int(1 * SR)
cands = []
for s in range(0, len(xs) - W, step):
    seg = xs[s:s + W]
    sp = np.abs(np.fft.rfft(seg[::8] * np.hanning(len(seg[::8]))))
    sp = sp / (np.sum(sp) + 1e-9)
    var = np.sum((sp - np.mean(sp)) ** 2)  # low var = steady drone
    e = np.mean(np.abs(seg))
    cands.append((var, -e, s))
cands.sort()
taken = []
for _, _, s in cands:
    if all(abs(s - t) > W for t in taken):
        taken.append(s)
        add(s, s + W, 9, 13, xs, 2)
        if len(taken) == 6: break
print('throat drones:', len(taken))

# --- ocean_tropical: slow swells (voice 14) + crashes (voice 15) ---
xs = load('ocean_tropical')
e = env(xs, 3000)  # 3 s smoothing -> swell structure
# swell segments: 12-20 s windows around the 8 largest envelope maxima
idx = np.argsort(e)[::-1]
taken = []
for i in idx:
    if all(abs(i - t) > 15 * SR for t in taken):
        s = max(0, i - int(8 * SR)); en = min(len(xs), i + int(8 * SR))
        taken.append(i); add(s, en, 6, 14, xs, 4)
        if len(taken) == 8: break
print('ocean swells:', len(taken))
# crashes: fast wave-crash attacks via 0.5 s rise of the 100 ms envelope
e2 = env(xs, 100)
rise = e2[22050:] - e2[:-22050]
thr = np.percentile(rise, 99.5)
i = 0; nc = 0
while i < len(rise) and nc < 12:
    if rise[i] > thr:
        s = max(0, i - int(0.5 * SR))
        en = min(len(xs), i + int(3.5 * SR))
        add(s, en, 6, 15, xs, 8); nc += 1
        i += int(4 * SR)
    else:
        i += 1
print('ocean crashes:', nc)

# --- sea_waves: full span as swell/crash vocabulary (voices 14/15) ---
xs = load('sea_waves')
for (s, e) in onsets(xs, 2.0, 1500, 800):
    pad = int(0.3 * SR)
    v = 15 if (e - s) < 3 * SR else 14
    fl = 8 if v == 15 else 4
    add(max(0, s - pad), min(len(xs), e + pad), 7, v, xs, fl)
print('sea_waves events:', len([r for r in recs if r[2] == 7]))

# --- quiet air segments from ocean_tropical (voice 16): lowest-energy
# 2 s windows, for beds ---
e3 = env(xs, 2000)
idx = np.argsort(e3)
taken = []
for i in idx:
    if all(abs(i - t) > 4 * SR for t in taken):
        s = max(0, i - SR); en = min(len(xs), i + SR)
        taken.append(i); add(s, en, 6, 16, xs, 16)
        if len(taken) == 6: break
print('ocean air:', len(taken))

_cat_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                       '..', 'catalog_kethra.bin'))
with open(_cat_path, 'wb') as f:
    for (s, e, src, v, pk, ce, dm, fl) in recs:
        f.write(struct.pack('<IIHHHHHH', s, e, src, v, pk, ce, dm, fl))
print('total records:', len(recs), '->', _cat_path)
