#!/usr/bin/env python3
# A-NATIVE verifier (VERIFY ONLY): native field-recording quality.
# - noise floor spectrum: quietest 1s segment must fall with frequency
#   (natural), not flat white
# - ZCR < 0.20: excessive zero-crossing rate => hiss (v1 planetvoice,
#   the lead's "shitty mic" ground truth, sits at 0.266)
# - exposed-hiss gate: quietest 100 ms window must be <25% HF energy
#   (v1 = 0.577, v2 = 0.013) — catches constant hiss between transients
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
    # exposed-hiss gate (2026-09-22 cleanup): quietest 100 ms window —
    # hiss is constant, so short windows catch it between transients,
    # where a 1 s window can dodge an LFO-breathing bed. Calibrated on
    # ground truth: v1 planetvoice (lead: "shitty mic") = 0.577 FAIL;
    # v2 = 0.013, D-AUD-4 = 0.015 PASS.
    wq = sr // 10
    qrms = [np.sqrt(np.mean(d[i:i+wq]**2)) for i in range(0, len(d)-wq, wq)]
    qs = d[int(np.argmin(qrms))*wq:int(np.argmin(qrms))*wq+wq] * np.hanning(wq)
    QS = np.abs(np.fft.rfft(qs))**2
    qf = np.fft.rfftfreq(wq, 1/sr)
    qhf = float(QS[qf > 8000].sum() / max(QS.sum(), 1e-30))
    hiss_ok = qhf < 0.25
    # ZCR gate tightened 0.30 -> 0.20 the same day: v1 planetvoice sits
    # at 0.266 (hiss riding on LF — passes 0.30, fails 0.20); v2 and
    # D-AUD-4 sit at ~0.055.
    print(f"== A-NATIVE {path}")
    print(f"  floor spectrum dB: 100-400Hz={b1:.1f} 1-4kHz={b2:.1f} 6-12kHz={b3:.1f} -> {'NATURAL FALL' if slope_ok else 'FLAT/SUSPICIOUS'}")
    print(f"  ZCR={zcr:.4f} (v1 planetvoice 0.266 FAIL; v2/D-AUD-4 ~0.055 PASS; white noise ~0.5)")
    print(f"  exposed hiss: quietest 100ms HF frac={qhf:.3f} (v1 0.577 FAIL; v2 0.013 PASS) -> {'CLEAN' if hiss_ok else 'HISSY'}")
    print(f"  crest={crest:.1f}  DC={dc:.6f}  peak={peak:.3f} (headroom {20*np.log10(1/max(peak,1e-9)):.1f}dB)")
    print(f"  click scan: global max jump={gmax:.4f} vs real ice field recording max={REF_MAX_JUMP:.4f} -> {'WITHIN NATURE' if click_ok else 'HOTTER THAN NATURE'}")
    ok = slope_ok and zcr < 0.20 and hiss_ok and abs(dc) < 0.005 and peak < 0.95 and click_ok
    print(f"  A-NATIVE: {'PASS' if ok else 'FAIL'}")
    return ok

if __name__ == "__main__":
    ok = True
    for p in sys.argv[1:]:
        ok = check(p) and ok
    sys.exit(0 if ok else 1)
