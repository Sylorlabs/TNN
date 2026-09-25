#!/usr/bin/env python3
"""Cut fork-2 third fossil (122.42-122.57s, distinct high vowel) + fork-6 laugh
source segment (17.7-19.3s). Lightweight: no full-file scans.
Fossil meta: SR,N,PF,CORE_A,SPAN,GAIN_Q16,DC (56 B, matches VF format).
Laugh: raw i16 bin + pitch-mark file (marks: u64 LE count + i64 LE positions).
"""
import wave, struct, math, hashlib
import numpy as np

SRC = '/home/hatch/workspace/tnn-lab/imagination_discovery/aud/b_alpha/consistency_gate/calibration/aporee_kids_play_area.wav'
OUT2 = '/home/hatch/workspace/audio_round2/grain_unit'
OUT6 = '/home/hatch/workspace/audio_round2/psola_voice'

w = wave.open(SRC); sr = w.getframerate(); n = w.getnframes()
x = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float64); w.close()
print('source sha256:', hashlib.sha256(open(SRC, 'rb').read()).hexdigest())

# ---- fork 2: third fossil @ 122.42-122.57 (F1~2371 F2~4725 F0~788)
C0, C1, F0 = 122.42, 122.57, 788
pf = int(round(sr / F0)); L = 2 * pf
a, b = int(C0 * sr), int(C1 * sr)
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
seg_i = np.clip(seg, -32768, 32767).astype(np.int16)
open(f'{OUT2}/fossil_hi.bin', 'wb').write(seg_i.tobytes())
meta = struct.pack('<7Q', sr, len(seg_i), pf, pf, span, int(3.0 * 65536),
                   dc if dc >= 0 else dc + 2**64)
open(f'{OUT2}/fossil_hi.meta', 'wb').write(meta)
print(f'fossil_hi: core {C0}-{C1}s PF={pf} span={span} seam_rms={math.sqrt(best/L):.1f} dc={dc}')

# ---- fork 6: laugh source 17.70-19.30 s
L0, L1 = 17.70, 19.30
seg = x[int(L0 * sr):int(L1 * sr)]
seg_i = np.clip(seg, -32768, 32767).astype(np.int16)
open(f'{OUT6}/laugh_src.bin', 'wb').write(seg_i.tobytes())
print(f'laugh_src: {L0}-{L1}s {len(seg_i)} samples')
# pitch marks: autocorr F0 per 5 ms, then peak-pick glottal pulses via
# waveform peak nearest each period grid point (deterministic)
hop = 220
marks = []
pos = 0
def ac_period(s):
    s = s - s.mean(); n_ = len(s)
    r = np.correlate(s, s, 'full')[n_ - 1:]
    r /= r[0] + 1e-12
    lo, hi = int(sr / 1800), int(sr / 200)
    return lo + int(np.argmax(r[lo:hi]))
while pos < len(seg) - hop:
    f = seg[pos:pos + 2205]
    P = ac_period(f)
    # nearest waveform peak to pos+P (glottal pulse marker)
    c = pos + P
    lo_, hi_ = max(0, c - P // 3), min(len(seg), c + P // 3)
    pk = lo_ + int(np.argmax(seg[lo_:hi_]))
    marks.append(pk)
    pos = pk + int(P * 0.9)
marks = sorted(set(marks))
print(f'pitch marks: {len(marks)}')
with open(f'{OUT6}/laugh_src.marks', 'wb') as f:
    f.write(struct.pack('<Q', len(marks)))
    for m in marks:
        f.write(struct.pack('<q', m))
for p in [f'{OUT2}/fossil_hi.bin', f'{OUT2}/fossil_hi.meta',
          f'{OUT6}/laugh_src.bin', f'{OUT6}/laugh_src.marks']:
    print(p, hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16])
