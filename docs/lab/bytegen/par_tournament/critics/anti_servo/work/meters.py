#!/usr/bin/env python3
"""RT-LONG pitch meter: spectral peak (parabolic interpolation) on the RESPOND
window, report Hz and cents vs expected. Also coherence: zero-lag normalized
xcorr of two windows + byte-identity check."""
import sys, wave
import numpy as np

def load(path):
    w = wave.open(path)
    n = w.getnframes(); sr = w.getframerate()
    s = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float64) / 32768.0
    return s, sr

def pitch_hz(seg, sr, lo_hz=100.0, hi_hz=2000.0):
    n = len(seg)
    win = seg * np.hanning(n)
    S = np.abs(np.fft.rfft(win))
    lo = int(lo_hz * n / sr); hi = int(hi_hz * n / sr)
    k = lo + int(np.argmax(S[lo:hi]))
    # parabolic interpolation
    if 0 < k < len(S)-1:
        a, b, c = S[k-1], S[k], S[k+1]
        d = 0.5*(a-c)/(a-2*b+c+1e-18)
        k = k + d
    return k * sr / n

def cents(f, ref):
    return 1200*np.log2(f/ref)

def coherence(a_path, b_path, w0, w1):
    sa, sra = load(a_path); sb, srb = load(b_path)
    assert sra == srb
    A0 = sa[int(w0[0]*sra):int(w0[1]*sra)]; A1 = sa[int(w1[0]*sra):int(w1[1]*sra)]
    B0 = sb[int(w0[0]*srb):int(w0[1]*srb)]; B1 = sb[int(w1[0]*srb):int(w1[1]*srb)]
    def xc(x, y):
        x = x - x.mean(); y = y - y.mean()
        return float(np.dot(x, y) / np.sqrt(np.dot(x,x)*np.dot(y,y)+1e-18))
    return xc(A0, A1), xc(B0, B1)

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "pitch":
        # pitch <wav> <t0> <t1> <expected_hz> [lo_hz hi_hz]
        s, sr = load(sys.argv[2])
        t0, t1, exp = float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
        seg = s[int(t0*sr):int(t1*sr)]
        if len(sys.argv) > 7:
            f = pitch_hz(seg, sr, float(sys.argv[6]), float(sys.argv[7]))
        else:
            f = pitch_hz(seg, sr)
        print(f"{sys.argv[2]}: {f:.2f} Hz  {cents(f,exp):+.1f}c vs {exp}")
    elif cmd == "coh":
        # coh <wavA> <wavB>  (motif windows 2.0-5.4 vs 24.0-27.4 within each)
        a, b = sys.argv[2], sys.argv[3]
        ca, cb = coherence(a, b, (2.0,5.4), (24.0,27.4))
        sa, sra = load(a)
        w0 = sa[int(2.0*sra):int(5.4*sra)]; w1 = sa[int(24.0*sra):int(27.4*sra)]
        # byte-identity of windows only meaningful int16; report max abs diff
        d = np.max(np.abs(w0[:min(len(w0),len(w1))] - w1[:min(len(w0),len(w1))]))
        print(f"coh A-self={ca:.10f} B-self={cb:.10f} max|w0-w1|_A={d:.6f}")
