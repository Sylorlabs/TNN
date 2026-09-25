#!/usr/bin/env python3
"""Hunt stable vowel cores v2: spectral-correlation stability (robust),
median-spectrum formants per run. Cuts fossils in VF meta format.
"""
import wave, struct, math, hashlib, sys
import numpy as np

SRC = '/home/hatch/workspace/tnn-lab/imagination_discovery/aud/b_alpha/consistency_gate/calibration/aporee_kids_play_area.wav'
OUT = '/home/hatch/workspace/audio_round2/grain_unit'

def load(p):
    w = wave.open(p); sr = w.getframerate(); n = w.getnframes()
    d = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float64); w.close()
    return d, sr

def liftered_logspec(xf):
    """liftered log magnitude spectra, one per frame row."""
    n = xf.shape[1]
    w = xf * np.hanning(n)
    S = np.abs(np.fft.rfft(w, 2048))
    ceps = np.fft.irfft(np.log(S + 1e-9))
    lif = np.zeros_like(ceps); lif[:40] = 1
    return np.fft.rfft(ceps * lif, 2048).real

def run_formants(x, sr, i0, i1, hop=441, n=1102):
    fr = np.arange(i0, i1)
    xf = x[fr[:, None] * hop + np.arange(n)[None, :]]
    L = liftered_logspec(xf)
    med = np.median(L, axis=0)
    freqs = np.fft.rfftfreq(2048, 1 / sr)
    m_ = (freqs >= 200) & (freqs <= 4200)
    e, f = med[m_], freqs[m_]
    pks = [(e[j], f[j]) for j in range(1, len(e) - 1) if e[j] > e[j-1] and e[j] >= e[j+1]]
    pks.sort(reverse=True)
    got = []
    for mag, ff in pks:
        if all(abs(ff - g) > 250 for g in got): got.append(ff)
        if len(got) == 3: break
    got += [0.0] * (3 - len(got)); got.sort()
    return got

def ac_f0_frames(x, sr, hop=441, n=1102):
    idx = np.arange(n)[None, :] + hop * np.arange((len(x) - n) // hop + 1)[:, None]
    xf = x[idx]
    xw = (xf - xf.mean(1, keepdims=True)) * np.hanning(n)
    N = 2048
    S = np.abs(np.fft.rfft(xw, N)) ** 2
    r = np.fft.irfft(S, N)[:, :n]; r /= r[:, :1] + 1e-12
    lo, hi = int(sr / 1400), int(sr / 200)
    pk = lo + np.argmax(r[:, lo:hi], axis=1)
    return sr / pk.astype(float), r[np.arange(len(r)), pk]

def cut_fossil(x, sr, c0, c1, tag, pf):
    a, b = int(c0 * sr), int(c1 * sr)
    L = 2 * pf
    def grain(fpos):
        idx = np.clip(np.arange(fpos - pf, fpos + pf), 0, len(x) - 1)
        return x[idx] * (0.5 - 0.5 * np.cos(2 * np.pi * np.arange(L) / (L - 1)))
    g0 = grain(a); best = 1e18; bnf = 4
    for nf in range(4, (b - a) // pf):
        g = grain(a + nf * pf); e = ((g - g0) ** 2).sum()
        if e < best: best = e; bnf = nf
    span = bnf * pf
    seg = x[a - pf:a + span + pf]
    dc = int(round(seg.mean()))
    pre = f'{OUT}/fossil_{tag}'
    seg_i = np.clip(seg, -32768, 32767).astype(np.int16)
    open(pre + '.bin', 'wb').write(seg_i.tobytes())
    meta = struct.pack('<7Q', sr, len(seg_i), pf, pf, span, int(3.0 * 65536),
                       dc if dc >= 0 else dc + 2**64)
    open(pre + '.meta', 'wb').write(meta)
    print(f'{tag}: core {c0:.2f}-{c1:.2f}s PF={pf} span={span} seam_rms={math.sqrt(best/L):.1f} dc={dc}',
          file=sys.stderr)

def main():
    x, sr = load(SRC)
    print('source sha256:', hashlib.sha256(open(SRC, 'rb').read()).hexdigest())
    f0, rr = ac_f0_frames(x, sr)
    voiced = (rr > 0.6) & (f0 > 250) & (f0 < 1400)
    n = 1102; hop = 441
    corr = np.zeros(len(f0) - 1)
    CH = 2000
    for c0 in range(0, len(f0), CH):
        c1 = min(len(f0), c0 + CH)
        idx = np.arange(n)[None, :] + hop * np.arange(c0, c1)[:, None]
        L = liftered_logspec(x[np.clip(idx, 0, len(x) - 1)].astype(np.float64))
        Ln = L / (np.linalg.norm(L, axis=1, keepdims=True) + 1e-12)
        corr[c0:c1 - 1] = (Ln[:-1] * Ln[1:]).sum(axis=1)
        if c1 < len(f0):
            # stitch: last frame of this chunk vs first of next
            i2 = np.arange(n) + hop * c1
            L2 = liftered_logspec(x[np.clip(i2, 0, len(x) - 1)][None, :].astype(np.float64))
            a = Ln[-1] / (np.linalg.norm(Ln[-1]) + 1e-12)
            b = L2[0] / (np.linalg.norm(L2[0]) + 1e-12)
            corr[c1 - 1] = float((a * b).sum())
        del L, Ln, idx
    stable = np.zeros(len(f0), bool); stable[1:] = corr > 0.98
    ok = voiced & stable
    runs = []; cur = []
    for i in range(len(ok)):
        if ok[i]: cur.append(i)
        else:
            if len(cur) >= 12: runs.append(cur)
            cur = []
    if len(cur) >= 12: runs.append(cur)
    print(f'{len(runs)} stable runs', file=sys.stderr)
    cands = []
    for r in runs:
        t0, t1 = r[0] * hop / sr, (r[-1] * hop + n) / sr
        if 129.0 < t0 < 130.5: continue  # VF-3 region
        if 25.0 < t0 < 26.0: continue    # VF-1 region (30s file offset differs; keep anyway)
        F = run_formants(x, sr, r[0], r[-1] + 1)
        F0m = float(np.median(f0[r]))
        cands.append((F[0], F[1], F[2], F0m, t0, t1))
    for c in sorted(cands, key=lambda c: c[1]):
        print(f'  F1={c[0]:.0f} F2={c[1]:.0f} F3={c[2]:.0f} F0={c[3]:.0f} t={c[4]:.2f}-{c[5]:.2f}s')
    back = [c for c in cands if c[1] < 2000 and c[0] > 250]
    cent = [c for c in cands if 2000 <= c[1] < 3200]
    picks = {}
    if back: picks['back'] = max(back, key=lambda c: c[5] - c[4])
    if cent: picks['cent'] = max(cent, key=lambda c: c[5] - c[4])
    print('PICKS:', {k: tuple(round(v, 1) for v in (p[0], p[1], p[4], p[5])) for k, p in picks.items()})
    for tag, (F1, F2, F3, F0m, t0, t1) in picks.items():
        cut_fossil(x, sr, t0 + 0.02, t1 - 0.02, tag, int(round(sr / F0m)))

if __name__ == '__main__':
    main()
