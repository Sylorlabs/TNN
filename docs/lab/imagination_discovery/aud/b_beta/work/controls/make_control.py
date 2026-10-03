#!/usr/bin/env python3
"""BLIND-TEST CONTROL (not a B-beta deliverable): a genuine same-brief
attempt at 'kids playing and laughter' (30 s) using the BANNED paradigm —
oscillators + filtered noise. Deterministic (hash noise, fixed seed).
This is what the blind bake-off compares the B-beta piece against."""
import wave, struct, numpy as np

SR = 44100
DUR = 30.0
N = int(SR * DUR)
SEED = 20260922

def hnoise(i, salt):
    z = (i * 2654435761 + salt * 40503 + SEED) & 0xFFFFFFFF
    z = (z ^ (z >> 16)) & 0xFFFFFFFF
    z = (z * 2246822519) & 0xFFFFFFFF
    z = (z ^ (z >> 13)) & 0xFFFFFFFF
    return (z / 2**32) * 2 - 1

def laugh(out, t0, f0, dur, amp):
    n = int(dur * SR); s0 = int(t0 * SR)
    if s0 + n > N: n = N - s0
    t = np.arange(n) / SR
    vib = 1 + 0.08 * np.sin(2 * np.pi * 6 * t)
    f = f0 * vib * (1 - 0.15 * t / max(dur, 1e-6))
    ph = np.cumsum(2 * np.pi * f / SR)
    am = 0.5 + 0.5 * np.sin(2 * np.pi * 8 * t)   # ha-ha-ha syllables
    am = np.clip(am, 0.15, 1.0)
    sig = (np.sin(ph) + 0.4 * np.sin(2 * ph) + 0.15 * np.sin(3 * ph)) * am
    edge = int(0.01 * SR)
    sig[:edge] *= np.linspace(0, 1, edge); sig[-edge:] *= np.linspace(1, 0, edge)
    out[s0:s0 + n] += sig * amp

def shout(out, t0, f0a, f0b, dur, amp):
    n = int(dur * SR); s0 = int(t0 * SR)
    if s0 + n > N: n = N - s0
    t = np.arange(n) / SR
    f = f0a + (f0b - f0a) * (t / dur)
    ph = np.cumsum(2 * np.pi * f / SR)
    sig = np.sin(ph) + 0.3 * np.sin(2 * ph)
    edge = int(0.008 * SR)
    sig[:edge] *= np.linspace(0, 1, edge); sig[-edge:] *= np.linspace(1, 0, edge)
    out[s0:s0 + n] += sig * amp

def step(out, t0, amp, salt):
    n = int(0.09 * SR); s0 = int(t0 * SR)
    if s0 + n > N: n = N - s0
    nz = np.array([hnoise(s0 + i, salt) for i in range(n)])
    y = np.zeros(n); a = 0.25
    for i in range(n):
        y[i] = a * nz[i] + (1 - a) * (y[i-1] if i else 0)  # one-pole lowpass
    env = np.exp(-np.arange(n) / (0.02 * SR))
    out[s0:s0 + n] += y * env * amp

def main():
    out = np.zeros(N)
    rng = np.random.default_rng(SEED)
    f0s = [320.0, 410.0, 520.0]
    # P0 sparse calls 0-5s
    for t0 in [0.4, 1.6, 2.9, 4.2]:
        shout(out, t0, 500, 800, 0.25, 0.35)
    # P1 chase 5-13s: steps + shouts
    t = 5.0; salt = 1
    while t < 13.0:
        step(out, t, 0.5, salt); salt += 1
        t += 0.28 + rng.random() * 0.10
    for t0 in [7.0, 9.5, 12.0]:
        shout(out, t0, 550, 850, 0.22, 0.4)
    # P2 tag 13-15s
    shout(out, 13.1, 600, 950, 0.3, 0.55)
    # P3 laugh pile 15-26s: 3 voices overlapping
    t = 15.0
    vi = 0
    while t < 26.0:
        dur = 0.3 + rng.random() * 0.6
        laugh(out, t, f0s[vi % 3] * (0.95 + rng.random() * 0.1), dur, 0.42)
        t += dur * (0.55 + rng.random() * 0.3)  # heavy overlap
        vi += 1
    # P4 settle 26-30s
    for t0 in [26.3, 27.5, 28.8]:
        laugh(out, t0, f0s[int(rng.integers(0, 3))], 0.3, 0.3)
    # room tone: a synth practitioner would never leave digital silence —
    # lowpassed hash-noise bed, the paradigm's own honest tool
    nz = np.array([hnoise(i, 777) for i in range(N)])
    y = np.zeros(N); a = 0.06
    for i in range(1, N):
        y[i] = a * nz[i] + (1 - a) * y[i - 1]
    out += y * 0.02
    out /= max(np.max(np.abs(out)), 1e-9)
    out *= 10 ** (-3 / 20)
    pcm = (np.clip(out, -1, 1) * 32767).astype('<i2')
    w = wave.open('control_synth_kids.wav', 'wb')
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(pcm.tobytes()); w.close()
    print("wrote control_synth_kids.wav", N / SR, "s")

if __name__ == '__main__':
    main()
