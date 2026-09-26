#!/usr/bin/env python3
# circles_gen.py — deterministic synthetic circle test image (512x187, 24-bit BMP).
# White ring r=60 @(140,93); filled red disc r=40 @(360,93);
# green concentric rings r=25/38 @(260,40); blue disc r=28 @(420,150) with a
# subpixel-blended edge; flat gray background.
import struct, math
w, h = 512, 187
px = bytearray(w * h * 3)
def setp(x, y, r, g, b):
    if 0 <= x < w and 0 <= y < h:
        o = (y * w + x) * 3
        px[o] = r; px[o + 1] = g; px[o + 2] = b
for i in range(w * h):
    px[i * 3] = px[i * 3 + 1] = px[i * 3 + 2] = 128
for yy in range(h):
    for xx in range(w):
        d = math.hypot(xx - 140, yy - 93)
        if abs(d - 60) < 0.75:
            setp(xx, yy, 255, 255, 255)
for yy in range(h):
    for xx in range(w):
        if math.hypot(xx - 360, yy - 93) <= 40:
            setp(xx, yy, 220, 30, 30)
for yy in range(h):
    for xx in range(w):
        d = math.hypot(xx - 260, yy - 40)
        if abs(d - 25) < 0.75 or abs(d - 38) < 0.75:
            setp(xx, yy, 30, 200, 30)
for yy in range(h):
    for xx in range(w):
        d = math.hypot(xx - 420, yy - 150)
        if d < 27:
            setp(xx, yy, 60, 60, 200)
        elif d < 28:
            t = int(128 + (60 - 128) * (28 - d))
            setp(xx, yy, t, t, 200)
stride = (w * 3 + 3) // 4 * 4
body = bytearray()
for sy in range(h - 1, -1, -1):
    for x in range(w):
        o = (sy * w + x) * 3
        body += bytes([px[o + 2], px[o + 1], px[o]])
    body += b'\x00' * (stride - w * 3)
hdr = (struct.pack('<2sIHHI', b'BM', 54 + len(body), 0, 0, 54)
       + struct.pack('<IiiHHIIIIII', 40, w, h, 1, 24, 0, len(body), 3780, 3780, 0, 0))
open('circles.bmp', 'wb').write(hdr + body)
print('wrote circles.bmp', len(hdr + body))
