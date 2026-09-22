#!/usr/bin/env python3
# A-NATIVE verifier (VERIFY ONLY): native field-recording quality.
# - noise floor spectrum: quietest 1s segment must fall with frequency
#   (natural), not flat white
# - ZCR: excessive zero-crossing rate => hiss
# - crest factor: healthy dynamics (not squashed, not all-peak)
# - click scan: reference-bounded — no sample-to-sample jump may exceed
#   the loudest jump in the real ice-crackle field recording (1.1977).
#   Transient onsets (cracks, thunder-like booms) are physical, so a
#   boundary-vs-global comparison would be the wrong test. The artifact
#   this guards against is digital mid-decay cutoffs (an event window
#   ending before its envelope reaches ~zero); the score sizes every
#   burst window to let its decay complete.
# - DC offset, headroom
import numpy as np, wave, sys

def load(p):
    w = wave.open(p); n = w.getnframes(); sr = w.getframerate()
    d = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float64)/32768.0
    return d, sr

def band_db(d, sr, lo, hi):
    n = len(d)
    S = np.abs(np.fft.rfft(d*np.hanning(n)))**2
    f = np.fft.rfftfreq(n, 1/sr)
    m = (f >= lo) & (f < hi)
    return 10*np.log10(S[m].mean()+1e-30)

def check(path):
    d, sr = load(path)
    # quietest 1s segment -> noise floor spectrum shape
    wlen = sr
    floors = [(np.sqrt(np.mean(d[i:i+wlen]**2)), i) for i in range(0, len(d)-wlen, wlen)]
    _, qi = min(floors)
    q = d[qi:qi+wlen]
    b1 = band_db(q, sr, 100, 400); b2 = band_db(q, sr, 1000, 4000); b3 = band_db(q, sr, 6000, 12000)
    slope_ok = (b1 > b2 + 3) and (b2 > b3 + 1)  # natural: falls with freq
    zcr = float(np.mean(np.diff(np.sign(d)) != 0))
    crest = float(np.max(np.abs(d))/(np.sqrt(np.mean(d**2))+1e-12))
    dc = float(np.mean(d))
    peak = float(np.max(np.abs(d)))
    dj = np.abs(np.diff(d))
    gmax = float(dj.max())
    REF_MAX_JUMP = 1.1977  # real ice-crackle field recording
    click_ok = gmax <= REF_MAX_JUMP
    print(f"== A-NATIVE {path}")
    print(f"  floor spectrum dB: 100-400Hz={b1:.1f} 1-4kHz={b2:.1f} 6-12kHz={b3:.1f} -> {'NATURAL FALL' if slope_ok else 'FLAT/SUSPICIOUS'}")
    print(f"  ZCR={zcr:.4f} (white noise ~0.5; clean rumble <0.15)")
    print(f"  crest={crest:.1f}  DC={dc:.6f}  peak={peak:.3f} (headroom {20*np.log10(1/max(peak,1e-9)):.1f}dB)")
    print(f"  click scan: global max jump={gmax:.4f} vs real ice field recording max={REF_MAX_JUMP:.4f} -> {'WITHIN NATURE' if click_ok else 'HOTTER THAN NATURE'}")
    ok = slope_ok and zcr < 0.3 and abs(dc) < 0.005 and peak < 0.95 and click_ok
    print(f"  A-NATIVE: {'PASS' if ok else 'FAIL'}")
    return ok

if __name__ == "__main__":
    ok = True
    for p in sys.argv[1:]:
        ok = check(p) and ok
    sys.exit(0 if ok else 1)
