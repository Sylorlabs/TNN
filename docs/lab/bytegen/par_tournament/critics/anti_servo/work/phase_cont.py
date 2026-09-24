#!/usr/bin/env python3
"""Phase continuity (fable Q2): per 1024-sample block, estimate phase at block
end and next block start via Goertzel at the block's dominant f0 (ZCR-based),
flag |dphi - expected_advance| > 0.2 rad unexplained by f0 change.
Plan-content flags (note onsets) are expected on ALL builds; build-attributable
= flags present in one build but not the others."""
import sys, wave
import numpy as np

def load(path):
    w = wave.open(path)
    n = w.getnframes(); sr = w.getframerate()
    s = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float64) / 32768.0
    return s, sr

def zcr_f0(block, sr):
    z = np.where(np.diff(np.signbit(block)))[0]
    if len(z) < 4: return 0.0
    # median zero-crossing interval -> f0
    iv = np.median(np.diff(z))
    if iv <= 0: return 0.0
    return sr / (2.0 * iv)

def goertzel_phase(block, sr, f0):
    n = len(block)
    k = f0 * n / sr
    # DFT bin at exact f0 via correlation
    t = np.arange(n) / sr
    c = np.sum(block * np.cos(2*np.pi*f0*t))
    s_ = np.sum(block * np.sin(2*np.pi*f0*t))
    return np.arctan2(s_, c)

def flags_for(path):
    s, sr = load(path)
    BS = 1024
    nb = len(s) // BS
    flags = []
    for b in range(nb - 1):
        b0 = s[b*BS:(b+1)*BS]; b1 = s[(b+1)*BS:(b+2)*BS]
        f0 = zcr_f0(b0, sr); f1 = zcr_f0(b1, sr)
        if f0 < 50 or f1 < 50: continue
        if abs(f1 - f0) / max(f0, f1) > 0.25: continue  # f0 change explains it
        p_end = goertzel_phase(b0, sr, f0)
        p_start = goertzel_phase(b1, sr, f0)
        expected = 2*np.pi*f0*BS/sr
        dphi = (p_start - p_end - expected) % (2*np.pi)
        if dphi > np.pi: dphi -= 2*np.pi
        if abs(dphi) > 0.2:
            flags.append((b, round(float(dphi),3), round(float(f0),1), round(float(f1),1)))
    return flags

if __name__ == "__main__":
    import hashlib
    allf = {}
    for p in sys.argv[1:]:
        fl = flags_for(p)
        allf[p] = fl
        h = hashlib.md5(str([f[0] for f in fl]).encode()).hexdigest()[:12]
        print(f"{p}: {len(fl)} flags md5={h}")
        for f in fl[:25]:
            print(f"   block {f[0]} t={f[0]*1024/44100:.3f}s err={f[1]} rad f0={f[2]}/{f[3]}")
    # build-attributable = flag blocks not shared by all
    if len(allf) > 1:
        sets = [set(f[0] for f in fl) for fl in allf.values()]
        common = set.intersection(*sets)
        for p, fl in allf.items():
            extra = sorted(set(f[0] for f in fl) - common)
            print(f"{p}: build-attributable flags: {len(extra)} {extra[:10]}")
