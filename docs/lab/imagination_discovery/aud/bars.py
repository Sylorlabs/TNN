#!/usr/bin/env python3
# A-BAR analyzer (VERIFY ONLY): A-DUR, A-EVOLVE, A-SPEC, A-NOHARM
import numpy as np, wave, sys

def analyze(path):
    w = wave.open(path)
    n, sr, ch, sw = w.getnframes(), w.getframerate(), w.getnchannels(), w.getsampwidth()
    d = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float64)
    if ch > 1: d = d.reshape(-1, ch).mean(axis=1)
    dur = n / sr
    fr = sr
    nf = n // fr
    cents, flats = [], []
    hi_e = tot_e = 0.0
    for i in range(nf):
        seg = d[i*fr:(i+1)*fr] * np.hanning(fr)
        S = np.abs(np.fft.rfft(seg))**2
        f = np.fft.rfftfreq(fr, 1/sr)
        se = S.sum(); tot_e += se; hi_e += S[f > 8000].sum()
        cents.append((f*S).sum()/max(se, 1e-30))
        am = np.mean(S); gm = np.exp(np.mean(np.log(S+1e-30)))
        flats.append(gm/max(am, 1e-30))
    cents = np.array(cents); flats = np.array(flats)
    res = {
        "dur_s": dur, "sr": sr, "ch": ch, "bits": sw*8,
        "centroid_std": float(np.std(cents)),
        "hi_frac_pct": float(hi_e/max(tot_e,1e-30)*100),
        "flat_gt03_pct": float(np.mean(flats > 0.30)*100),
        "centroid_mean": float(np.mean(cents)),
        "peak": float(np.max(np.abs(d))/32768.0),
        "rms": float(np.sqrt(np.mean(d**2))/32768.0),
    }
    bars = {
        "A-DUR": res["dur_s"] >= 20 and sr == 44100 and ch == 1 and sw == 2,
        "A-EVOLVE": res["centroid_std"] >= 400,
        "A-SPEC": res["hi_frac_pct"] >= 2.0,
        "A-NOHARM": res["flat_gt03_pct"] >= 30.0,
    }
    return res, bars

if __name__ == "__main__":
    for p in sys.argv[1:]:
        res, bars = analyze(p)
        print(f"== {p}")
        for k, v in res.items(): print(f"  {k}={v:.3f}" if isinstance(v, float) else f"  {k}={v}")
        for k, v in bars.items(): print(f"  {k}: {'PASS' if v else 'FAIL'}")
        print(f"  ALL: {'PASS' if all(bars.values()) else 'FAIL'}")
