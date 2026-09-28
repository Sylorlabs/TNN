#!/usr/bin/env python3
"""Hunt stable vowel cores in the 134 s field recording for fork 2 (grain_unit).
Finds >=15-frame stable voiced runs (v1+v2 < 15000), clusters by (F1,F2),
cuts fossils in the VF meta format: SR,N,PF,CORE_A,SPAN,GAIN_Q16,DC (56 B).
Target: one back vowel (F2<2000), one central (F2 2000-3200), front already
covered by VF-1/VF-3.
"""
import wave, struct, math, hashlib, sys
import numpy as np

SRC = '/home/hatch/workspace/tnn-lab/imagination_discovery/aud/b_alpha/consistency_gate/calibration/aporee_kids_play_area.wav'
OUT = '/home/hatch/workspace/audio_round2/grain_unit'

def load(p):
    w = wave.open(p); sr = w.getframerate(); n = w.getnframes()
    d = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float64); w.close()
    return d, sr

def frame_feats(x, sr, hop=441, n=1102):
    idx = np.arange(n)[None, :] + hop * np.arange((len(x) - n) // hop + 1)[:, None]
    xf = x[idx]
    # autocorr F0
    xw = (xf - xf.mean(1, keepdims=True)) * np.hanning(n)
    N = 2048
    S = np.abs(np.fft.rfft(xw, N)) ** 2
    r = np.fft.irfft(S, N)[:, :n]; r /= r[:, :1] + 1e-12
    lo, hi = int(sr / 1000), int(sr / 200)
    pk = lo + np.argmax(r[:, lo:hi], axis=1)
    f0 = sr / pk.astype(float); rr = r[np.arange(len(r)), pk]
    # band-peak formants on liftered spectrum
    f1 = np.zeros(len(xf)); f2 = np.zeros(len(xf))
    for i in range(len(xf)):
        w_ = xf[i] * np.hanning(n)
        S_ = np.abs(np.fft.rfft(w_, 4096))
        ceps = np.fft.irfft(np.log(S_ + 1e-9))
        lif = np.zeros_like(ceps); lif[:40] = 1
        env = np.exp(np.fft.rfft(ceps * lif, 4096).real)
        fr = np.fft.rfftfreq(4096, 1 / sr)
        m_ = (fr >= 200) & (fr <= 4200)
        e, f = env[m_], fr[m_]
        pks = [(e[j], f[j]) for j in range(1, len(e) - 1) if e[j] > e[j-1] and e[j] >= e[j+1]]
        pks.sort(reverse=True)
        got = []
        for mag, ff in pks:
            if all(abs(ff - g) > 250 for g in got): got.append(ff)
            if len(got) == 2: break
        got += [0.0] * (2 - len(got)); got.sort()
        f1[i], f2[i] = got
    return f0, rr, f1, f2

def cut_fossil(x, sr, c0, c1, tag, pf):
    a, b = int(c0 * sr), int(c1 * sr)
    L = 2 * pf
    def grain(fpos):
        idx = np.clip(np.arange(fpos - pf, fpos + pf), 0, len(x) - 1)
        g = x[idx] * (0.5 - 0.5 * np.cos(2 * np.pi * np.arange(L) / (L - 1)))
        return g
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
    print(f'{tag}: core {c0:.2f}-{c1:.2f}s PF={pf} span={span} seam_rms={math.sqrt(best/L):.1f} dc={dc}')

def main():
    x, sr = load(SRC)
    print('source sha256:', hashlib.sha256(open(SRC, 'rb').read()).hexdigest(), file=sys.stderr)
    f0, rr, f1, f2 = frame_feats(x, sr)
    voiced = (rr > 0.6) & (f0 > 250) & (f0 < 950) & (f1 > 250) & (f2 > 800)
    # static: frame-to-frame formant movement small
    df = np.abs(np.diff(f1, prepend=f1[0])) + np.abs(np.diff(f2, prepend=f2[0]))
    static = voiced & (df < 120)
    # runs >= 15 frames
    runs = []; cur = []
    for i in range(len(static)):
        if static[i]: cur.append(i)
        else:
            if len(cur) >= 15: runs.append(cur)
            cur = []
    if len(cur) >= 15: runs.append(cur)
    print(f'{len(runs)} stable runs', file=sys.stderr)
    cands = []
    for r in runs:
        t0, t1 = r[0] * 441 / sr, r[-1] * 441 / sr
        cands.append((float(np.median(f1[r])), float(np.median(f2[r])),
                      float(np.median(f0[r])), t0, t1))
    # exclude regions already used (VF-3 at 129.55-129.78)
    cands = [c for c in cands if not (129.0 < c[3] < 130.5)]
    for c in sorted(cands, key=lambda c: c[1]):
        print(f'  F1={c[0]:.0f} F2={c[1]:.0f} F0={c[2]:.0f} t={c[3]:.2f}-{c[4]:.2f}s')
    # pick: back (F2<2000), central (2000<F2<3200), and best front spare
    back = [c for c in cands if c[1] < 2000]
    cent = [c for c in cands if 2000 <= c[1] < 3200]
    front = [c for c in cands if c[1] >= 3200]
    picks = {}
    if back: picks['back'] = max(back, key=lambda c: c[4] - c[3])
    if cent: picks['cent'] = max(cent, key=lambda c: c[4] - c[3])
    if front: picks['front'] = max(front, key=lambda c: c[4] - c[3])
    print('PICKS:', {k: (round(v[0]), round(v[1]), round(v[3], 2), round(v[4], 2)) for k, v in picks.items()})
    for tag, (F1, F2, F0, t0, t1) in picks.items():
        pf = int(round(sr / F0))
        cut_fossil(x, sr, t0 + 0.02, t1 - 0.02, tag, pf)

if __name__ == '__main__':
    main()
