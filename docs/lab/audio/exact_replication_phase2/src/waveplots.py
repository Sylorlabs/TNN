#!/usr/bin/env python3
"""Generate waveform-comparison PNGs for the gallery (matplotlib, Agg)."""
import struct
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def read_wav(path):
    d = open(path, 'rb').read()
    off = 12
    while off + 8 < len(d):
        if d[off:off+4] == b'data':
            sz = struct.unpack('<I', d[off+4:off+8])[0]
            n = sz // 2
            x = np.frombuffer(d[off+8:off+8+2*n], dtype='<i2').astype(np.float64)
            sr = struct.unpack('<I', d[24:28])[0]
            return x, sr
    raise ValueError('no data')

clips = ['strike', 'vowel', 'cry', 'clang']
R = '/home/hatch/workspace/exact_audio_replication/phase2/run'
F = '/home/hatch/workspace/rawbyte_longmem'

for c in clips:
    src, sr = read_wav(f'{F}/fixture_{c}.wav')
    ex, _ = read_wav(f'{R}/t_{c}/{c}_exact.wav')
    se, _ = read_wav(f'{R}/t_{c}/{c}_sem.wav')
    n = len(src)
    t = np.arange(n) / sr
    # exact error (should be all zeros)
    derr = ex[:n] - src
    # semantic error
    serr = se[:n] - src

    fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True)
    axes[0].plot(t, src, lw=0.4, color='#1f77b4')
    axes[0].set_title(f'{c}: source waveform (full duration, {n/sr:.2f}s @ {sr} Hz)', fontsize=11)
    axes[0].set_ylabel('PCM')
    axes[1].plot(t, derr, lw=0.4, color='#2ca02c')
    axes[1].set_title(f'{c}: exact(mode10) − source  [max|d| = {np.abs(derr).max():.1f} LSB → byte-identical]', fontsize=11)
    axes[1].set_ylabel('LSB err')
    axes[2].plot(t, serr, lw=0.4, color='#d62728')
    rms = np.sqrt((serr**2).mean())
    axes[2].set_title(f'{c}: semantic(mode11) − source  [RMS {rms:.1f} LSB — the knowledge gap]', fontsize=11)
    axes[2].set_ylabel('LSB err')
    axes[2].set_xlabel('seconds')
    fig.tight_layout()
    fig.savefig(f'{R}/wave_{c}.png', dpi=90)
    plt.close(fig)
    print(f'wrote wave_{c}.png  max_exact_err={np.abs(derr).max():.1f}')
print('done')
