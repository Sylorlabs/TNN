#!/usr/bin/env python3
"""Dev-render synthesis for organ validation (NOT test material).
Deterministic, no RNG. Recipes:
  pool0: harmonics [1.0, 0.30, 0.10], zero phase
  pool1: harmonics [1.0, 0.15, 0.05, 0.02], zero phase
"""
import wave, math, struct, os, sys

SR = 44100
DEV = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dev')

def write_wav(path, x):
    pk = max(abs(v) for v in x) or 1.0
    g = 20000.0 / pk
    xi = [int(max(-32768, min(32767, round(v * g)))) for v in x]
    w = wave.open(path, 'wb')
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(struct.pack('<%dh' % len(xi), *xi)); w.close()

def tone(f0, dur, harms, env=None):
    n = int(SR * dur)
    x = [0.0] * n
    for i in range(n):
        t = i / SR
        v = 0.0
        for h, a in enumerate(harms, start=1):
            v += a * math.sin(2 * math.pi * f0 * h * t)
        if env:
            v *= env(i / n)
        x[i] = v
    return x

def main():
    os.makedirs(DEV, exist_ok=True)
    pools = {'p0': [1.0, 0.30, 0.10], 'p1': [1.0, 0.15, 0.05, 0.02]}
    # 24 pitch classes, 110*2^(k/12)
    for pname, harms in pools.items():
        for k in range(24):
            f0 = 110.0 * 2 ** (k / 12.0)
            write_wav(f'{DEV}/dev_pitch_{pname}_k{k:02d}.wav', tone(f0, 2.0, harms))
    # env classes at 220 Hz
    for pname, harms in pools.items():
        write_wav(f'{DEV}/dev_env_{pname}_flat.wav', tone(220.0, 2.0, harms))
        write_wav(f'{DEV}/dev_env_{pname}_rise.wav',
                  tone(220.0, 2.0, harms, env=lambda u: 10 ** ((-12.0 + 12.0 * u) / 20.0)))
        write_wav(f'{DEV}/dev_env_{pname}_decay.wav',
                  tone(220.0, 2.0, harms, env=lambda u: 10 ** ((0.0 - 12.0 * u) / 20.0)))
    print('dev renders done')

if __name__ == '__main__':
    main()
