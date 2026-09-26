#!/usr/bin/env python3
# odd_gen.py — odd-geometry intake test (511x199 -> stride padding path).
# Deterministic per-pixel pattern + one white ring r=70 @(255,99).
import struct, math
w, h = 511, 199
px = bytearray(w * h * 3)
for i in range(w * h):
    px[i * 3] = px[i * 3 + 1] = px[i * 3 + 2] = (i * 7) % 256
for yy in range(h):
    for xx in range(w):
        if abs(math.hypot(xx - 255, yy - 99) - 70) < 0.75:
            o = (yy * w + xx) * 3
            px[o] = px[o + 1] = px[o + 2] = 255
stride = (w * 3 + 3) // 4 * 4
body = bytearray()
for sy in range(h - 1, -1, -1):
    for x in range(w):
        o = (sy * w + x) * 3
        body += bytes([px[o + 2], px[o + 1], px[o]])
    body += b'\x00' * (stride - w * 3)
hdr = (struct.pack('<2sIHHI', b'BM', 54 + len(body), 0, 0, 54)
       + struct.pack('<IiiHHIIIIII', 40, w, h, 1, 24, 0, len(body), 3780, 3780, 0, 0))
open('odd.bmp', 'wb').write(hdr + body)
print('wrote odd.bmp', len(hdr + body), 'stride', stride)
