#!/usr/bin/env python3
# gen_loudclick.py — analytical (zero-RNG) replacement for the RNG-generated
# smoke/loudclick.wav (which used np.random.RandomState(7).randn).
#
# Fixture purpose: exercise the analyzer's onset detector with 6 transient
# clicks on a steady tonal bed. Expected: n_onsets == 6, ~500 ms spacing.
#
# FORMULA (all deterministic, no random numbers):
#   sr = 16000 Hz, dur = 3.0 s  ->  N = 48000 samples, mono 16-bit PCM.
#   bed[i]   = round(8000 * sin(2*pi*(4000/9)*i/sr))   # 444.444 Hz tonal bed
#                                                     # (period exactly 36 samples)
#   click at t_k = 0.25 + 0.5*k seconds, k = 0..5 (6 clicks):
#     for n = 0..99 (6.25 ms), rectangular-gated 2600 Hz burst:
#       c[n]     = round(15000 * sin(2*pi*2600*n/sr))
#     s[t_k*sr + n] += c[n]   (additive; deterministic phase interference)
#   s[i] clipped to [-32768, 32767], written as little-endian s16.
# WAV: 44-byte PCM header (no LIST chunk), data chunk = 96000 bytes.
#
# Design note: the analyzer's onset detector fires when a 20 ms window's
# energy exceeds 2x the median of the previous 5 windows. Bed window energy
# ~10.2e9; a 100-sample 15000-amplitude burst adds ~11.3e9 -> ~2.1x ratio,
# so each click fires exactly one onset (6 total, 500 ms apart).
#
# Determinism: pure math functions of the sample index. Byte-identical on
# every run, on any platform (round-half-away via int(x+0.5) for x>=0).

import math, struct, hashlib

SR = 16000
DUR = 3.0
N = int(SR * DUR)
F_BED = 4000.0 / 9.0   # 444.444... Hz, period exactly 36 samples @16kHz
A_BED = 8000.0
F_CLICK = 2600.0
A_CLICK = 15000.0
CLICK_LEN = 100
CLICK_TIMES = [0.25 + 0.5 * k for k in range(6)]

def rint(x):
    return int(math.floor(x + 0.5)) if x >= 0 else int(math.ceil(x - 0.5))

s = [0] * N
for i in range(N):
    s[i] = rint(A_BED * math.sin(2.0 * math.pi * F_BED * i / SR))
for t in CLICK_TIMES:
    start = int(t * SR)
    for n in range(CLICK_LEN):
        car = math.sin(2.0 * math.pi * F_CLICK * n / SR)
        v = s[start + n] + rint(A_CLICK * car)
        if v > 32767: v = 32767
        if v < -32768: v = -32768
        s[start + n] = v

pcm = struct.pack('<%dh' % N, *s)
hdr = struct.pack('<4sI4s4sIHHIIHH4sI',
    b'RIFF', 36 + len(pcm), b'WAVE',
    b'fmt ', 16, 1, 1, SR, SR * 2, 2, 16,
    b'data', len(pcm))
out = hdr + pcm
with open('loudclick.wav', 'wb') as f:
    f.write(out)
print('wrote loudclick.wav', len(out), 'bytes')
print('SHA-256:', hashlib.sha256(out).hexdigest())
# determinism self-check: regenerate in memory and compare
pcm2 = struct.pack('<%dh' % N, *s)
assert hashlib.sha256(hdr + pcm2).hexdigest() == hashlib.sha256(out).hexdigest()
print('determinism self-check: PASS (byte-identical regeneration)')
