#!/usr/bin/env python3
"""F1 autopilot reference implementation (bit-exact integer algorithms).

This is the oracle the Zag port (src/f1.zag) must match bit-for-bit on every
fixture. All arithmetic is integer; division truncates toward zero (tdiv);
right-shift on negatives is arithmetic (floor), matching the znc codegen
(probed 2026-09-23: (-7)/2=-3, (-7)>>1=-4).

DECLARED F1 SAMPLING POLICY (frozen; also embedded in the ledger header):
  PITCH (.pcm, n=16384): split halves A=[0:8192), B=[8192:16384).
      First-pass window = first 2048 samples of each half. Dominant frequency
      per window via interpolated zero-crossing count. rel_ppm =
      |fB-fA|*1e6/fA; SAME iff rel_ppm < 20000 else HIGHER/LOWER.
      LOSS: any pitch event confined to samples [2048:8192) of either half is
      invisible; frequency resolution ~ rate/(2*2048).
  TIMBRE (.pcm, n=8192): first 2048 samples. hp1000 =
      1000*sum|x[i]-x[i-1]|/sum|x|. Class by fixed thresholds.
      LOSS: timbre changes after sample 2048 are invisible.
  COLORDISC (.img 64x64, flat halves): mean RGB of left/right 32x64 halves;
      euclidean distance of the means; SAME iff dist < 40 else DIFFERENT.
      LOSS: sub-threshold color differences destroyed by the 40-unit gate.
  COLORCONST (.img 64x64, textured halves): white-patch illuminant = per-half
      max RGB; discounted mean = 255*mean/max per channel; SAME_SURFACE iff
      max channel difference of discounted means < 8 else DIFFERENT.
      LOSS: single-pixel illuminant corruption propagates to the whole panel;
      discount-identical surfaces under different absolute levels collide.
  MOTION (.vid 8x64x64): brightness-weighted centroid of frame 0 vs frame 7
      only (6 of 8 frames discarded). Displacement -> 8-way/STILL, still iff
      max(|dx|,|dy|) < 2 (in 1/64-pixel units: < 128).
      LOSS: small-target motion is invisible to the global centroid; 75% of
      frames never examined.
  ROUTER: .pcm n=16384 -> PITCH, n=8192 -> TIMBRE; .img variance test ->
      COLORDISC vs COLORCONST; .vid -> MOTION.
"""
import struct, sys, math

def tdiv(a, b):
    q = abs(a) // abs(b)
    return q if (a >= 0) == (b > 0) else -q

def isqrt(n):
    # integer sqrt, floor; matches Zag isqrt loop
    if n <= 0: return 0
    x = 1 << ((n.bit_length() + 1) // 2)
    while True:
        y = (x + n // x) // 2
        if y >= x: return x
        x = y

OPS = [0]

def rd_pcm(p):
    d = open(p, 'rb').read()
    rate, n = struct.unpack('<II', d[:8])
    s = struct.unpack('<%dh' % n, d[8:8 + 2 * n])
    return rate, n, list(s)

def rd_img(p):
    d = open(p, 'rb').read()
    w, h = struct.unpack('<II', d[:8])
    return w, h, d[8:]

def rd_vid(p):
    d = open(p, 'rb').read()
    nf, w, h = struct.unpack('<III', d[:12])
    fr = []
    o = 12
    for _ in range(nf):
        fr.append(d[o:o + w * h * 3]); o += w * h * 3
    return nf, w, h, fr

def zc_freq_q16(win, rate):
    """Interpolated zero-crossing frequency. Returns Hz as integer,
    computed with Q16 fractional crossing positions (all integer ops)."""
    # find crossings; position in Q16 samples
    prev = win[0]
    first = -1; last = -1; count = 0
    OPS[0] += 1
    for i in range(1, len(win)):
        cur = win[i]
        OPS[0] += 1
        if (prev < 0 and cur >= 0) or (prev > 0 and cur <= 0):
            num = abs(prev); den = num + abs(cur)
            pos = ((i - 1) << 16) + tdiv(num << 16, den)
            if first < 0: first = pos
            last = pos; count += 1
        prev = cur
    if count < 2 or last <= first:
        return 0
    # f = (count-1)/2 cycles over (last-first)/65536 samples
    # f = (count-1)*rate*65536 / (2*(last-first))
    num = (count - 1) * rate * 65536
    den = 2 * (last - first)
    return tdiv(num, den)

def pitch_perceive(s, rate):
    assert len(s) == 16384
    fA = zc_freq_q16(s[0:2048], rate)
    fB = zc_freq_q16(s[8192:10240], rate)
    if fA <= 0:
        return "SAME", 0, fA, fB, 0
    rel = tdiv(abs(fB - fA) * 1000000, fA)
    if rel < 20000:
        p = "SAME"
    elif fB > fA:
        p = "HIGHER"
    else:
        p = "LOWER"
    conf = min(1000, abs(rel - 20000) * 1000 // 20000)
    return p, conf, fA, fB, rel

# timbre thresholds (hp1000): calibrated on harness t5 TIMBRES @440Hz, first 2048 samples
# measured: PURE=62, DARK=72, RICH=93, BRIGHT=166 -> midpoints 67/82/110
TIMBRE_T = {"PURE_MAX": 67, "DARK_MAX": 82, "RICH_MAX": 110}

def timbre_perceive(s):
    assert len(s) == 8192
    w = s[0:2048]
    et = sum(abs(v) for v in w); OPS[0] += len(w)
    eh = 0
    prev = w[0]
    for v in w[1:]:
        eh += abs(v - prev); prev = v; OPS[0] += 1
    hp = tdiv(eh * 1000, max(et, 1))
    if hp <= TIMBRE_T["PURE_MAX"]:
        p = "PURE"
    elif hp <= TIMBRE_T["DARK_MAX"]:
        p = "DARK"
    elif hp <= TIMBRE_T["RICH_MAX"]:
        p = "RICH"
    else:
        p = "BRIGHT"
    # confidence: distance to nearest boundary
    bounds = sorted([TIMBRE_T["PURE_MAX"], TIMBRE_T["DARK_MAX"], TIMBRE_T["RICH_MAX"]])
    m = min(abs(hp - b) for b in bounds)
    conf = min(1000, m * 1000 // 60)
    return p, conf, hp

def img_halves(w, h, px):
    # returns (mean1, var1, max1, mean2, var2, max2) for x<w/2, x>=w/2
    n = (w // 2) * h
    s1 = [0, 0, 0]; s1q = [0, 0, 0]; m1 = [0, 0, 0]
    s2 = [0, 0, 0]; s2q = [0, 0, 0]; m2 = [0, 0, 0]
    for y in range(h):
        for x in range(w):
            o = (y * w + x) * 3
            r, g, b = px[o], px[o + 1], px[o + 2]
            OPS[0] += 1
            if x < w // 2:
                s1[0] += r; s1[1] += g; s1[2] += b
                s1q[0] += r * r; s1q[1] += g * g; s1q[2] += b * b
                m1[0] = max(m1[0], r); m1[1] = max(m1[1], g); m1[2] = max(m1[2], b)
            else:
                s2[0] += r; s2[1] += g; s2[2] += b
                s2q[0] += r * r; s2q[1] += g * g; s2q[2] += b * b
                m2[0] = max(m2[0], r); m2[1] = max(m2[1], g); m2[2] = max(m2[2], b)
    mean1 = [tdiv(v, n) for v in s1]; mean2 = [tdiv(v, n) for v in s2]
    var1 = max(tdiv(s1q[i], n) - mean1[i] * mean1[i] for i in range(3))
    var2 = max(tdiv(s2q[i], n) - mean2[i] * mean2[i] for i in range(3))
    return mean1, var1, m1, mean2, var2, m2

def colordisc_perceive(w, h, px):
    mean1, _, _, mean2, _, _ = img_halves(w, h, px)
    d2 = sum((a - b) ** 2 for a, b in zip(mean1, mean2))
    dist = isqrt(d2)
    p = "SAME" if dist < 40 else "DIFFERENT"
    conf = min(1000, abs(dist - 40) * 1000 // 40)
    return p, conf, dist

def colorconst_perceive(w, h, px):
    mean1, _, mx1, mean2, _, mx2 = img_halves(w, h, px)
    # discounted means in 0..255
    disc = []
    for c in range(3):
        d1 = tdiv(mean1[c] * 255, max(mx1[c], 1))
        d2 = tdiv(mean2[c] * 255, max(mx2[c], 1))
        disc.append(abs(d1 - d2))
    md = max(disc)
    p = "SAME_SURFACE" if md < 8 else "DIFFERENT"
    conf = min(1000, abs(md - 8) * 1000 // 8)
    return p, conf, md

def motion_perceive(nf, w, h, frames):
    # frames 0 and 7 only; brightness-weighted centroid, Q6 subpixel
    def cent(fr):
        sx = sy = sw = 0
        for y in range(h):
            for x in range(w):
                o = (y * w + x) * 3
                b = (fr[o] + fr[o + 1] + fr[o + 2]) // 3
                OPS[0] += 1
                if b > 16:
                    sx += x * b; sy += y * b; sw += b
        if sw == 0: return 0, 0
        return tdiv(sx * 64, sw), tdiv(sy * 64, sw)
    x0, y0 = cent(frames[0]); x1, y1 = cent(frames[7])
    dx = x1 - x0; dy = y1 - y0
    ax, ay = abs(dx), abs(dy)
    if max(ax, ay) < 128:
        p = "STILL"
    else:
        # 8-way by dominant axis; diagonal if within factor 2
        if ax >= 2 * ay: p = "E" if dx > 0 else "W"
        elif ay >= 2 * ax: p = "S" if dy > 0 else "N"
        else:
            p = ("S" if dy > 0 else "N") + ("E" if dx > 0 else "W")
            p = {"NE": "NE", "NW": "NW", "SE": "SE", "SW": "SW"}[p]
    conf = min(1000, max(ax, ay) * 1000 // 512)
    return p, conf, dx, dy

def route(ext, n=None, w=None, h=None, px=None):
    if ext == '.pcm':
        return 'PITCH' if n == 16384 else ('TIMBRE' if n == 8192 else 'UNKNOWN')
    if ext == '.img':
        _, var1, _, _, var2, _ = img_halves(w, h, px)
        return 'COLORDISC' if max(var1, var2) < 1 else 'COLORCONST'
    if ext == '.vid':
        return 'MOTION'
    return 'UNKNOWN'

def perceive(path):
    OPS[0] = 0
    ext = '.' + path.rsplit('.', 1)[-1]
    if ext == '.pcm':
        rate, n, s = rd_pcm(path)
        task = route(ext, n=n)
        if task == 'PITCH':
            p, conf, fA, fB, rel = pitch_perceive(s, rate)
            det = 'fA=%d fB=%d rel_ppm=%d' % (fA, fB, rel)
        elif task == 'TIMBRE':
            p, conf, hp = timbre_perceive(s)
            det = 'hp1000=%d' % hp
        else:
            p, conf, det = 'NONE', 0, 'unsupported'
    elif ext == '.img':
        w, h, px = rd_img(path)
        task = route(ext, w=w, h=h, px=px)
        if task == 'COLORDISC':
            p, conf, dist = colordisc_perceive(w, h, px)
            det = 'dist=%d' % dist
        else:
            p, conf, md = colorconst_perceive(w, h, px)
            det = 'maxdisc=%d' % md
    elif ext == '.vid':
        nf, w, h, fr = rd_vid(path)
        task = 'MOTION'
        p, conf, dx, dy = motion_perceive(nf, w, h, fr)
        det = 'dx_q6=%d dy_q6=%d' % (dx, dy)
    else:
        task, p, conf, det = 'UNKNOWN', 'NONE', 0, 'unsupported'
    return task, p, conf, det, OPS[0]

if __name__ == '__main__':
    for p in sys.argv[1:]:
        task, perc, conf, det, ops = perceive(p)
        print('RESULT fixture=%s task=%s percept=%s conf=%d ops=%d %s' % (p, task, perc, conf, ops, det))
