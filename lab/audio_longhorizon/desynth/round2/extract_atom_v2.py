#!/usr/bin/env python3
"""Extract a measured timbre atom from a real voiced WAV.

An atom = (harmonic stack, per-period amplitude, texture, transients),
ALL measured from the source audio. No synthesis.

Atom binary format v2 (little-endian):
  u32 magic 'ATOM' (0x4D4F5441)
  u32 version (2)
  f64 T0            : measured pitch period (samples)
  i64 NBINS         : harmonic shape length
  f64 harm[NBINS]   : period-averaged harmonic waveform (measured)
  i64 K             : texture prototype count
  i64 TEXLEN        : texture prototype length (samples)
  f64 tex[K*TEXLEN] : measured residual texture prototypes (real source
                      segments, spectrally shaped to harmonic domain),
                      normalized to 0.15 x harmonic RMS (chosen perceptual
                      mix; see HONEST NOTE in code — the residual does not
                      isolate a measurable texture ratio)
  i64 NAMP          : amplitude trajectory length (periods)
  f64 amp_traj[NAMP]: measured per-period RMS amplitude
  i64 NIMP          : transient count
  i64 imp_pos[NIMP] : transient positions (samples, relative to atom start)
  f64 imp_amp[NIMP] : transient amplitudes (measured residual peaks)

v1 carried 16 LP coefficients measured from the harmonic waveform. They were
REMOVED in v2: the direct measured harmonic waveform already contains the
source's spectral coloration, so filtering it through the LPC would color it
twice. No renderer ever applied them (both skipped the LP block).
"""
import sys, struct, wave
import numpy as np

def read_wav(path):
    with wave.open(path, 'rb') as w:
        n = w.getnframes()
        ch = w.getnchannels()
        sw = w.getsampwidth()
        sr = w.getframerate()
        raw = w.readframes(n)
    if sw == 2:
        x = np.frombuffer(raw, dtype=np.int16).astype(np.float64)
    elif sw == 1:
        x = (np.frombuffer(raw, dtype=np.uint8).astype(np.float64) - 128) * 256
    else:
        raise ValueError(f"unsupported sampwidth {sw}")
    if ch > 1:
        x = x.reshape(-1, ch).mean(axis=1)
    return sr, x

def estimate_f0_autocorr(x, sr, fmin=60, fmax=600):
    """Measured f0 via autocorrelation. No synth.
    Uses a STABLE voiced segment (lowest amplitude CV), not just loudest.
    Validates the period by checking the period-averaged waveform has
    exactly 2 zero-crossings (one period, not two)."""
    win = sr // 10
    # Find the 100ms window with lowest amplitude CV (most stable voicing)
    best_cv, best_i = 1e9, 0
    for i in range(0, len(x) - win, win // 4):
        w = x[i:i+win].astype(np.float64)
        m = np.mean(np.abs(w))
        if m < 10:  # skip silence
            continue
        # CV of 10ms sub-window RMS
        sw = sr // 100
        e = np.array([np.sqrt(np.mean(w[j:j+sw]**2)) for j in range(0, len(w)-sw, sw)])
        cv = np.std(e) / (np.mean(e) + 1e-9)
        if cv < best_cv:
            best_cv, best_i = cv, i
    seg = x[best_i:best_i + win].astype(np.float64)
    seg = seg - np.mean(seg)
    if np.sum(seg ** 2) < 1e-9:
        return 0, 0
    # Autocorrelation
    ac = np.correlate(seg, seg, mode='full')[len(seg)-1:]
    ac = ac / (ac[0] + 1e-12)
    lo = int(sr / fmax)
    hi = int(sr / fmin)
    hi = min(hi, len(ac) - 1)
    # Collect ALL peaks above 0.3, then validate by zero-crossing count
    peaks = []
    for i in range(lo + 1, hi):
        if ac[i] > ac[i-1] and ac[i] >= ac[i+1] and ac[i] > 0.3:
            peaks.append((ac[i], i))
    peaks.sort(reverse=True)
    # Try peaks in order of strength; accept the first whose period-averaged
    # waveform has exactly 2 zero-crossings (one true period).
    for _, pk in peaks[:5]:
        T0 = float(pk)
        NBINS = int(round(T0))
        if NBINS < 20:
            continue
        nper = min(int(len(seg) / T0) - 1, 20)
        periods = np.zeros((nper, NBINS))
        pos = 0.0
        for p in range(nper):
            idx = pos + np.arange(NBINS) * (T0 / NBINS)
            idx = np.clip(idx, 0, len(seg) - 1.001)
            i_lo = idx.astype(int)
            frac = idx - i_lo
            periods[p] = seg[i_lo] * (1 - frac) + seg[np.minimum(i_lo + 1, len(seg)-1)] * frac
            pos += T0
        harm = np.mean(periods, axis=0)
        harm = harm - np.mean(harm)
        zc = np.sum((harm[:-1] * harm[1:]) < 0)
        if zc == 2:
            # Parabolic refinement
            y0, y1, y2 = ac[pk-1], ac[pk], ac[pk+1]
            denom = (y0 - 2*y1 + y2)
            shift = 0.0
            if abs(denom) > 1e-12:
                shift = 0.5 * (y0 - y2) / denom
            T0r = pk + shift
            return sr / T0r, best_i
    return 0, 0

def main():
    in_wav, out_atom = sys.argv[1], sys.argv[2]
    sr, x = read_wav(in_wav)
    print(f"sr={sr} n={len(x)}", flush=True)

    f0, seg_start = estimate_f0_autocorr(x, sr)
    if f0 < 60:
        print(f"FAIL: no voiced f0 found (f0={f0})", flush=True)
        sys.exit(1)
    T0 = sr / f0
    print(f"measured f0={f0:.2f} Hz T0={T0:.2f} samples", flush=True)

    # Use 1.0s from seg_start for the atom
    seg = x[seg_start:seg_start + sr].copy()
    if len(seg) < sr:
        seg = np.pad(seg, (0, sr - len(seg)))
    seg = seg - np.mean(seg)

    # Period-synchronous averaging with period validation.
    # If the averaged waveform doesn't have exactly 2 zero-crossings,
    # try sub-multiples of T0 (the autocorr may have locked onto 2x/4x).
    NBINS = 0
    harm = None
    periods = None
    amp_traj = None
    T_try = T0
    for _ in range(3):
        NBINS_try = int(round(T_try))
        if NBINS_try < 20:
            break
        nper_try = int(len(seg) / T_try) - 1
        if nper_try < 5:
            break
        pt = np.zeros((nper_try, NBINS_try))
        at = np.zeros(nper_try)
        pos = 0.0
        for p in range(nper_try):
            idx = pos + np.arange(NBINS_try) * (T_try / NBINS_try)
            idx = np.clip(idx, 0, len(seg) - 1.001)
            i_lo = idx.astype(int)
            frac = idx - i_lo
            pt[p] = seg[i_lo] * (1 - frac) + seg[np.minimum(i_lo + 1, len(seg)-1)] * frac
            at[p] = np.sqrt(np.mean(pt[p] ** 2) + 1e-12)
            pos += T_try
        h_try = np.mean(pt, axis=0)
        h_try = h_try - np.mean(h_try)
        zc_try = np.sum((h_try[:-1] * h_try[1:]) < 0)
        if zc_try == 2:
            NBINS, harm, periods, amp_traj = NBINS_try, h_try, pt, at
            T0 = T_try
            break
        T_try = T_try / 2.0
    if harm is None:
        print(f"FAIL: could not isolate one period (zc={zc_try})", flush=True)
        sys.exit(1)
    nper = periods.shape[0]
    print(f"harm: NBINS={NBINS} rms={np.sqrt(np.mean(harm**2)):.1f}", flush=True)

    # Residual = seg - harmonic resynthesized at measured periods
    res = seg.copy()
    pos = 0.0
    for p in range(nper):
        idx = pos + np.arange(NBINS) * (T0 / NBINS)
        idx = np.clip(idx, 0, len(seg) - 1.001)
        i_lo = idx.astype(int)
        frac = idx - i_lo
        h = harm  # already NBINS
        # subtract harmonic scaled by this period's amplitude relative to mean
        scale = amp_traj[p] / (np.sqrt(np.mean(harm**2)) + 1e-12)
        contrib = h * scale
        # scatter back (nearest, measured positions)
        for b in range(NBINS):
            j = int(round(idx[b]))
            if 0 <= j < len(res):
                res[j] -= contrib[b] * (1.0 / max(1, int(round(T0 / NBINS)) + 1))
        pos += T0

    # Texture: K prototypes from the residual (measured segments)
    # Take segments with median energy (not the loudest = transients, not silence)
    TEXLEN = 256
    K = 8
    seg_e = []
    for i in range(0, len(res) - TEXLEN, TEXLEN):
        seg_e.append((np.sum(res[i:i+TEXLEN]**2), i))
    seg_e.sort()
    # Pick K segments around the 60th percentile (textured, not transient, not silent)
    start = int(len(seg_e) * 0.5)
    tex_resid = np.zeros((K, TEXLEN))
    for k in range(K):
        _, i = seg_e[(start + k * 7) % len(seg_e)]
        tex_resid[k] = res[i:i+TEXLEN]
    # Convert texture to waveform domain: apply the harmonic's spectral
    # envelope so the texture is consistent with the harmonic (both in the
    # waveform domain). This is measured filtering, not synthesis.
    #
    # Spectral grid (Wall-3 residual #5 fix, 2026-09-27): NBINS = round(sr/f0)
    # is the measured period length; at 44.1 kHz any source F0 below
    # 44100/256.5 = 171.9 Hz gives NBINS > TEXLEN=256 and the old fixed
    # 256-sample pad buffer crashed with
    #   ValueError: could not broadcast input array from shape (NBINS,)
    #   into shape (256,)
    # The binwise multiply needs H and T on one FFT grid. When the harmonic
    # fits (NBINS <= TEXLEN) the grid stays 256 and every op below is
    # bit-identical to v2; otherwise the grid grows to the next power of two
    # >= NBINS (fits the harmonic, still >= TEXLEN), the windowed
    # TEXLEN-sample texture segment is zero-padded to the same grid (same
    # time-domain signal, finer frequency sampling), and the inverse
    # transform is truncated back to TEXLEN. tex stays K x TEXLEN and
    # TEXLEN=256 is written to the atom unchanged: binary format untouched.
    SPEC_N = TEXLEN
    if NBINS > TEXLEN:
        SPEC_N = 1
        while SPEC_N < NBINS:
            SPEC_N *= 2
    h_padded = np.zeros(SPEC_N)
    h_padded[:NBINS] = harm
    H = np.abs(np.fft.rfft(h_padded * np.hanning(SPEC_N)))
    H = np.maximum(H, np.max(H) * 0.01)
    tex = np.zeros((K, TEXLEN))
    for k in range(K):
        w = tex_resid[k] * np.hanning(TEXLEN)
        if SPEC_N > TEXLEN:
            wp = np.zeros(SPEC_N)
            wp[:TEXLEN] = w
            w = wp
        T = np.fft.rfft(w)
        T_shaped = T * (H / (np.mean(H) + 1e-12))
        tex[k] = np.fft.irfft(T_shaped, SPEC_N)[:TEXLEN]
    # Transients: strongest residual peaks (measured), min separation T0/2.
    # Detected BEFORE texture normalization so the transient neighborhoods
    # can be excluded from the measured texture level.
    NIMP = 12
    min_sep = int(T0 / 2)
    peaks = []
    ares = np.abs(res)
    for i in range(1, len(ares) - 1):
        if ares[i] > ares[i-1] and ares[i] >= ares[i+1] and ares[i] > np.mean(ares) * 3:
            peaks.append((ares[i], i))
    peaks.sort(reverse=True)
    imp_pos, imp_amp = [], []
    for v, i in peaks:
        if all(abs(i - p) >= min_sep for p in imp_pos):
            imp_pos.append(i)
            imp_amp.append(res[i])  # signed, measured
        if len(imp_pos) >= NIMP:
            break
    # Texture level: HONEST NOTE — the period-synchronous residual does NOT
    # isolate the texture (residual RMS exceeds the source due to harmonic
    # leakage; measured "ratios" are 29-244x, nonsensical). A source-measured
    # texture ratio is not obtainable from this decomposition. The prototypes
    # themselves are real source audio (measured segments); their LEVEL is a
    # chosen perceptual mix parameter, not a measured source ratio.
    # v1 used 0.3 (extractor) x 0.5 (renderer) = 0.15 effective. v2 preserves
    # the validated 0.15 effective level with the mix at unity in the renderer
    # (removing the 0.5 magic number from the render path).
    MIX_LEVEL = 0.15  # chosen perceptual texture mix (see note above)
    harm_rms = float(np.sqrt(np.mean(harm**2)))
    tex_rms = float(np.sqrt(np.mean(tex**2)))
    if tex_rms > 1e-9:
        tex = tex * (harm_rms / tex_rms) * MIX_LEVEL
    print(f"texture: K={K} TEXLEN={TEXLEN} harm_rms={harm_rms:.6f} mix_level={MIX_LEVEL} (chosen, see note)", flush=True)
    print(f"transients: NIMP={len(imp_pos)}", flush=True)

    # Relative positions (fraction of atom), amplitudes
    imp_pos = np.array(imp_pos, dtype=np.int64)
    imp_amp = np.array(imp_amp)
    # LEVEL NORMALIZATION (v2 addition, 2026-09-27): scale every amplitude
    # component to the native reference RMS so each timbre renders at a
    # level the organ can voice. Applied HERE (after all measurement) —
    # scaling harm/amp_traj earlier would corrupt the residual (seg minus
    # scaled harmonic), so the single end-point scale is the correct one.
    # Absolute recording level is not timbre: the extractor already
    # discards it for the texture (normalized to harm_rms * 0.15) and the
    # renderer discards it for the trajectory (divides by its mean) — the
    # waveform was the one inconsistent component. REF_RMS is MEASURED:
    # harm_rms of atom0_child.bin, the planner's native reference timbre
    # (voiced 988/1000 by the organ). Only the absolute level changes;
    # harmonic relative content, trajectory shape (rise/decay), texture
    # character, and transient positions are untouched. The texture was
    # normalized to old_harm_rms * 0.15; scaling it by S re-normalizes it
    # to new_harm_rms * 0.15 exactly, so it stays consistent.
    REF_RMS = 619.8  # measured harm_rms of atom0_child.bin
    _hr = float(np.sqrt(np.mean(harm ** 2)))
    _S = REF_RMS / _hr if _hr > 1e-9 else 1.0
    harm = harm * _S
    amp_traj = amp_traj * _S
    tex = tex * _S
    imp_amp = imp_amp * _S
    print(f"level-norm: harm_rms {_hr:.1f} -> {REF_RMS} (S={_S:.4f})", flush=True)

    # Write atom (format v2: LP coefficients REMOVED — the harmonic waveform
    # is already the measured spectral coloration; filtering it again through
    # the LPC would color it twice. v2 = magic, version, T0, NBINS, harm,
    # K, TEXLEN, tex, NAMP, amp_traj, NIMP, imp_pos, imp_amp.)
    with open(out_atom, 'wb') as f:
        f.write(struct.pack('<II', 0x4D4F5441, 2))
        f.write(struct.pack('<d', T0))
        f.write(struct.pack('<q', NBINS))
        f.write(struct.pack('<%dd' % NBINS, *harm))
        f.write(struct.pack('<qq', K, TEXLEN))
        f.write(struct.pack('<%dd' % (K*TEXLEN), *tex.flatten()))
        f.write(struct.pack('<q', nper))
        f.write(struct.pack('<%dd' % nper, *amp_traj))
        f.write(struct.pack('<q', len(imp_pos)))
        f.write(struct.pack('<%dq' % len(imp_pos), *imp_pos))
        f.write(struct.pack('<%dd' % len(imp_amp), *imp_amp))
    print(f"wrote {out_atom} (v2, mix_level={MIX_LEVEL})", flush=True)

if __name__ == '__main__':
    main()
