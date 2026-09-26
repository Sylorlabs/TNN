#!/usr/bin/env python3
"""Human-inspection instruments for the binding confirmatory run.

Independent of the TNN analyzer. Reads raw WAV/PPM bytes and reports
waveform statistics, spectra, envelope, transient regularity (audio);
pixel stats, edges, texture, regions (image); frame diffs and coarse
motion (video). Output guides the human-written descriptions.
"""
import struct, math, os
import numpy as np

IN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inputs")
SR = 16000

def read_wav(p):
    with open(p, "rb") as f:
        b = f.read()
    assert b[:4] == b"RIFF"
    # find data chunk
    i = 12
    doff = dlen = None
    while i + 8 <= len(b):
        tag, sz = b[i:i+4], struct.unpack("<I", b[i+4:i+8])[0]
        if tag == b"data":
            doff, dlen = i + 8, sz
            break
        i += 8 + sz + (sz & 1)
    x = np.frombuffer(b[doff:doff+dlen], dtype=np.int16).astype(np.float64) / 32768.0
    return x

def env_rms(x, win):
    n = len(x) // win
    return np.sqrt((x[:n*win].reshape(n, win) ** 2).mean(axis=1))

def analyze_audio(name):
    x = read_wav(os.path.join(IN, name + ".wav"))
    dur = len(x) / SR
    peak = float(np.abs(x).max())
    rms = float(np.sqrt((x ** 2).mean()))
    dc = float(x.mean())
    e50 = env_rms(x, 800)  # 50 ms
    emax, emin = float(e50.max()), float(e50[e50 > 1e-9].min()) if (e50 > 1e-9).any() else 0.0
    dyn_db = 20 * math.log10(emax / emin) if emin > 0 else float("inf")
    # spectrum: band energies via FFT
    n = len(x)
    X = np.abs(np.fft.rfft(x * np.hanning(n)))
    freqs = np.fft.rfftfreq(n, 1 / SR)
    tot = (X ** 2).sum()
    def band(lo, hi):
        m = (freqs >= lo) & (freqs < hi)
        return float((X[m] ** 2).sum() / tot)
    # tonal peaks: top local maxima in 50-4000 Hz
    m = (freqs >= 50) & (freqs <= 4000)
    f2, X2 = freqs[m], X[m]
    peaks = []
    for i in range(1, len(X2) - 1):
        if X2[i] > X2[i-1] and X2[i] >= X2[i+1] and X2[i] > 0.05 * X2.max():
            peaks.append((f2[i], float(X2[i] / X2.max())))
    peaks.sort(key=lambda t: -t[1])
    # pitch via autocorrelation (50..4000 Hz lags), FFT-based O(n log n)
    xc = x - x.mean()
    nn = 1
    while nn < 2 * n:
        nn *= 2
    F = np.fft.rfft(xc, nn)
    ac = np.fft.irfft(F * np.conj(F), nn)[:n]
    ac /= ac[0]
    lo_lag, hi_lag = int(SR / 4000), int(SR / 50)
    seg = ac[lo_lag:hi_lag]
    # best local maximum (not just global argmax)
    cand = [(lag, float(seg[lag])) for lag in range(1, len(seg) - 1)
            if seg[lag] > seg[lag-1] and seg[lag] >= seg[lag+1]]
    cand.sort(key=lambda t: -t[1])
    bl = (cand[0][0] + lo_lag) if cand else (int(np.argmax(seg)) + lo_lag)
    f0 = SR / bl
    # HNR-ish: harmonic energy ratio at f0 (sum of first 6 harmonic bins)
    harm_e = sum(float((X[(freqs >= k*f0*0.97) & (freqs <= k*f0*1.03)] ** 2).sum()) for k in range(1, 7))
    hnr_db = 10 * math.log10(harm_e / max(tot - harm_e, 1e-12))
    # envelope autocorr rhythm (1 s windows), FFT-based
    e1s = env_rms(x, SR)  # 1 s windows
    e1s = e1s - e1s.mean()
    if len(e1s) > 4 and float((e1s ** 2).mean()) > 1e-18:
        m2 = 1
        while m2 < 2 * len(e1s):
            m2 *= 2
        FE = np.fft.rfft(e1s, m2)
        ae = np.fft.irfft(FE * np.conj(FE), m2)[:len(e1s)]
        ae /= ae[0]
        rpeaks = []
        for lag in range(1, len(ae) - 1):
            if ae[lag] > ae[lag-1] and ae[lag] >= ae[lag+1] and ae[lag] > 0.25:
                rpeaks.append((lag, round(float(ae[lag]), 3)))
        rpeaks.sort(key=lambda t: -t[1])
    else:
        rpeaks = []
    # onset detection: envelope derivative crossings
    e20 = env_rms(x, 320)  # 20 ms
    d = np.diff(e20)
    thr = 3.0 * np.median(np.abs(d)) + 1e-6
    onsets = [i for i in range(1, len(d) - 1) if d[i] > thr and d[i] >= d[i-1] and d[i] > d[i+1]]
    # merge within 200 ms
    merged = []
    for o in onsets:
        if merged and o - merged[-1] < 10:
            continue
        merged.append(o)
    onset_times = [round(o * 0.02, 2) for o in merged]
    print("== %s ==" % name)
    print("dur %.2f s  n=%d  peak %.3f  rms %.4f  dc %.5f" % (dur, len(x), peak, rms, dc))
    print("env50: max %.4f min>0 %.5f  dynamic_range ~%.1f dB" % (emax, emin, dyn_db))
    print("bands 0-400Hz %.3f  400-2000 %.3f  2-4k %.3f  4-8k %.3f" % (band(0,400), band(400,2000), band(2000,4000), band(4000,8000)))
    print("tonal peaks (Hz, rel):", [(round(f), r) for f, r in peaks[:8]])
    print("autocorr f0 ~%.1f Hz (lag str %.3f)  harmonic-ratio ~%.1f dB" % (f0, float(ac[bl]), hnr_db))
    print("env-rhythm peaks (lag s, str):", rpeaks[:6])
    print("onset candidates (%d):" % len(onset_times), onset_times[:40])
    print()

def read_ppm(p):
    with open(p, "rb") as f:
        b = f.read()
    assert b[:2] == b"P6"
    i = 2
    toks = []
    while len(toks) < 3:
        while b[i:i+1].isspace():
            i += 1
        j = i
        while not b[j:j+1].isspace():
            j += 1
        toks.append(b[i:j])
        i = j
    while b[i:i+1].isspace():
        i += 1
    w, h, mv = int(toks[0]), int(toks[1]), int(toks[2])
    assert mv == 255
    px = np.frombuffer(b[i:i+w*h*3], dtype=np.uint8).reshape(h, w, 3)
    return px

def analyze_image(name):
    px = read_ppm(os.path.join(IN, name + ".ppm")).astype(np.float64)
    h, w, _ = px.shape
    gray = px.mean(axis=2)
    r, g, b = px[:, :, 0], px[:, :, 1], px[:, :, 2]
    mx, mn = px.max(axis=2), px.min(axis=2)
    sat = np.where(mx > 1e-9, (mx - mn) / mx, 0.0)
    print("== %s ==" % name)
    print("size %dx%d  mean brightness %.1f  mean sat %.3f  sat>0.3 frac %.3f" % (w, h, gray.mean(), sat.mean(), (sat > 0.3).mean()))
    # tone thirds
    print("brightness thirds: top %.1f mid %.1f bot %.1f | left %.1f right %.1f" % (
        gray[:h//3].mean(), gray[h//3:2*h//3].mean(), gray[2*h//3:].mean(),
        gray[:, :w//2].mean(), gray[:, w//2:].mean()))
    # Sobel orientation histogram (strong edges only)
    gx = np.abs(np.diff(gray, axis=1))
    gy = np.abs(np.diff(gray, axis=0))
    mag = np.sqrt(gx[:-1]**2 + gy[:, :-1]**2)
    ang = np.degrees(np.arctan2(gy[:, :-1], gx[:-1])) % 180
    strong = mag > np.percentile(mag, 90)
    horiz = float(((ang < 22.5) | (ang >= 157.5))[strong].mean()) if strong.any() else 0
    vert = float((((ang >= 67.5) & (ang < 112.5)))[strong].mean()) if strong.any() else 0
    diag = 1.0 - horiz - vert
    print("strong-edge orientation: horiz %.2f vert %.2f diag/other %.2f" % (horiz, vert, diag))
    # texture: 8x8 cell variance fraction (var>100 like the analyzer)
    ch, cw = h // 8, w // 8
    tv = gray[:ch*8, :cw*8].reshape(ch, 8, cw, 8).var(axis=(1, 3))
    frac = float((tv > 100).mean())
    print("native 8x8 texture frac (var>100): %.3f" % frac)
    # regions: quantize to 32-level, flood fill
    q = (gray / 32).astype(np.int32)
    seen = np.zeros_like(q, dtype=bool)
    regs = []
    for yy in range(h):
        for xx in range(w):
            if seen[yy, xx]:
                continue
            v = q[yy, xx]
            stack = [(yy, xx)]
            seen[yy, xx] = True
            cnt = 0
            while stack:
                cy, cx = stack.pop()
                cnt += 1
                for ny, nx in ((cy-1,cx),(cy+1,cx),(cy,cx-1),(cy,cx+1)):
                    if 0 <= ny < h and 0 <= nx < w and not seen[ny, nx] and abs(int(q[ny,nx]) - int(v)) <= 1:
                        seen[ny, nx] = True
                        stack.append((ny, nx))
            regs.append(cnt)
    regs.sort(reverse=True)
    print("regions: %d total; largest fracs: %s" % (len(regs), [round(r/(h*w), 3) for r in regs[:6]]))
    print()

def analyze_video(prefix, n):
    fr = [read_ppm(os.path.join(IN, "%s_f_%03d.ppm" % (prefix, f))).astype(np.float64).mean(axis=2) for f in range(1, n+1)]
    h, w = fr[0].shape
    print("== %s (%d frames %dx%d) ==" % (prefix, n, w, h))
    print("frame means:", [round(float(f.mean()), 2) for f in fr])
    # frame diffs
    for f in range(1, n):
        d = np.abs(fr[f] - fr[f-1])
        print("  %d->%d: mean|diff| %.2f  max %.1f  frac>20: %.3f" % (f, f+1, d.mean(), d.max(), (d > 20).mean()))
    # motion: centroid of the dark region per frame (independent check)
    cents = []
    for f in fr:
        dark = f < 100
        ys, xs = np.nonzero(dark)
        cents.append((float(xs.mean()), float(ys.mean())))
    print("dark-region centroid per frame:", [(round(cx,1), round(cy,1)) for cx, cy in cents])
    dxs = [cents[i+1][0]-cents[i][0] for i in range(len(cents)-1)]
    dys = [cents[i+1][1]-cents[i][1] for i in range(len(cents)-1)]
    print("centroid motion px/frame: dx", [round(v,1) for v in dxs], "dy", [round(v,1) for v in dys])
    print()

if __name__ == "__main__":
    for a in ("C1_dyad_swells", "C2_soft_phrases", "C3_rumble_hum"):
        analyze_audio(a)
    for im in ("C4_pickets", "C5_diag_wedge"):
        analyze_image(im)
    analyze_video("C6_drift", 8)
