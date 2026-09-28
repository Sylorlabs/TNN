#!/usr/bin/env python3
"""Generate waveform-comparison PNGs with PIL (fast, no matplotlib)."""
import struct
import numpy as np
from PIL import Image, ImageDraw, ImageFont

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
        sz = struct.unpack('<I', d[off+4:off+8])[0]
        off += 8 + sz
    raise ValueError('no data')

W, H = 1200, 800
PANEL_H = 220
TOP = 60

def draw_wave(draw, x, y0, h, color, peak):
    # min/max per pixel column
    n = len(x)
    step = max(1, n // W)
    for px in range(W):
        s = x[px*step:(px+1)*step]
        if len(s) == 0: continue
        mn, mx = s.min(), s.max()
        y1 = y0 + h//2 - int(mx/peak * (h//2 - 4))
        y2 = y0 + h//2 - int(mn/peak * (h//2 - 4))
        draw.line([(px, y1), (px, y2)], fill=color)

clips = ['strike', 'vowel', 'cry', 'clang']
R = '/home/hatch/workspace/exact_audio_replication/phase2/run'
F = '/home/hatch/workspace/rawbyte_longmem'

for c in clips:
    src, sr = read_wav(f'{F}/fixture_{c}.wav')
    ex, _ = read_wav(f'{R}/t_{c}/{c}_exact.wav')
    se, _ = read_wav(f'{R}/t_{c}/{c}_sem.wav')
    n = len(src)
    derr = ex[:n] - src
    serr = se[:n] - src
    rms = float(np.sqrt((serr**2).mean()))
    maxd = float(np.abs(derr).max())

    img = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.load_default()
    except:
        font = None

    # panel 1: source
    d.text((10, 8), f'{c}: source waveform (full duration {n/sr:.2f}s)', fill='black', font=font)
    draw_wave(d, src, TOP, PANEL_H, (31, 119, 180), 32768)
    # panel 2: exact error
    y0 = TOP + PANEL_H + 40
    d.text((10, y0 - 28), f'{c}: exact(mode10) - source  [max|d| = {maxd:.1f} LSB -> BYTE-IDENTICAL]', fill='black', font=font)
    d.line([(0, y0 + PANEL_H//2), (W, y0 + PANEL_H//2)], fill=(200, 200, 200))
    peak2 = max(1.0, maxd * 1.2)
    draw_wave(d, derr, y0, PANEL_H, (44, 160, 44), peak2)
    # panel 3: semantic error
    y0 = TOP + 2*(PANEL_H + 40)
    d.text((10, y0 - 28), f'{c}: semantic(mode11) - source  [RMS {rms:.1f} LSB -- the knowledge gap]', fill='black', font=font)
    d.line([(0, y0 + PANEL_H//2), (W, y0 + PANEL_H//2)], fill=(200, 200, 200))
    peak3 = max(1.0, np.abs(serr).max() * 1.1)
    draw_wave(d, serr, y0, PANEL_H, (214, 39, 40), peak3)

    img.save(f'{R}/wave_{c}.png')
    print(f'wrote wave_{c}.png')
print('done')
