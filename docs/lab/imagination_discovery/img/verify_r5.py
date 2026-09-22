#!/usr/bin/env python3
"""Round-5 killer-death + light-consistency self-check (VERIFY ONLY).
Reads the Zag-emitted BMP and the layout lines the binary printed.
Checks:
  K1 pasted-disc planet: limb softness, limb irregularity, extinction,
      terminator-vs-sun agreement
  K2 repeating mountains: ridgeline autocorrelation (reimplemented Zag
      noise in Python), peak variety
  K3 floating rocks: contact AO, burial, non-circularity, shadow presence
  K4 one sun: implied light azimuth sampled from planet, moon, hero rock
      lit centroids + hero-rock shadow azimuth vs the SUN vector
"""
import struct, sys, math, os
import numpy as np
from PIL import Image

MASK = 0xFFFFFFFF
def tdiv(a, b):
    q = abs(a) // abs(b)
    return q if (a >= 0) == (b > 0) else -q

def r5_hash(x, y, seed):
    h = (x * 374761393 + y * 668265263 + seed * 2246822519) & MASK
    h = (h ^ (h >> 16)) & MASK
    h = (h * 3266489917) & MASK
    h = (h ^ (h >> 13)) & MASK
    h = (h * 1103515245 + 12345) & MASK
    h = (h ^ (h >> 16)) & MASK
    return h
def r5_h01(x, y, seed):
    return r5_hash(x, y, seed) >> 22
def r5_sstep(t):
    t2 = t * t
    t3 = t2 * t
    return (3 * t2 * 255 - 2 * t3) // 65025
def r5_vnoise(x, y, seed):
    xb = x + 268435456
    yb = y + 268435456
    xi = xb >> 8; yi = yb >> 8
    xf = xb & 255; yf = yb & 255
    u = r5_sstep(xf); v = r5_sstep(yf)
    a = r5_h01(xi, yi, seed); b = r5_h01(xi + 1, yi, seed)
    c = r5_h01(xi, yi + 1, seed); d = r5_h01(xi + 1, yi + 1, seed)
    ab = a + tdiv((b - a) * u, 256)
    cd = c + tdiv((d - c) * u, 256)
    return ab + tdiv((cd - ab) * v, 256)
def r5_fbm(x, y, seed, oct):
    s = 0; amp = 512; norm = 0
    xx, yy = x, y
    for o in range(oct):
        s += r5_vnoise(xx, yy, seed + o * 131) * amp // 512
        norm += amp
        xx += xx; yy += yy; amp //= 2
    return s * 512 // norm if norm else 512
def r5_ridge(x, y, seed, oct):
    s = 0; amp = 512; norm = 0
    xx, yy = x, y
    for o in range(oct):
        n = r5_vnoise(xx, yy, seed + o * 131)
        r = 1023 - abs(n + n - 1023)
        r = r * r // 1023
        s += r * amp // 512
        norm += amp
        xx += xx; yy += yy; amp //= 2
    return s * 512 // norm if norm else 0

def r5_hf_ghost(x, h, w):
    base = h * 395 // 1000
    g = r5_fbm(x * 256 // 420, 31, 5401, 3)
    g2 = r5_fbm(x * 256 // 900, 33, 5410, 2)
    return base - tdiv((g - 512) * 64, 1024) - tdiv((g2 - 512) * 26, 1024)
def r5_hf_near(x, h, w):
    base = h * 685 // 1000
    g = r5_fbm(x * 256 // 260, 47, 5405, 3)
    g2 = r5_fbm(x * 256 // 90, 49, 5406, 2)
    return base + tdiv((g - 512) * 34, 1024) + tdiv((g2 - 512) * 14, 1024)
def r5_hf_far(x, h, w):
    base = h * 470 // 1000
    m = r5_ridge(x * 256 // 170, 37, 5402, 2)
    dd = x - w * 62 // 100
    pk = 0
    if dd < 0: pk = 130 - dd * dd // 70
    else: pk = 130 - dd * dd // 120
    if pk < 0: pk = 0
    rough = r5_fbm(x * 256 // 90, 77, 5409, 2)
    pk = pk * (600 + rough * 800 // 1024) // 1024
    dd2 = x - w * 30 // 100
    pk2 = 70 - dd2 * dd2 // 51
    if pk2 < 0: pk2 = 0
    rough2 = r5_fbm(x * 256 // 110, 79, 5419, 2)
    pk2 = pk2 * (600 + rough2 * 800 // 1024) // 1024
    return base - pk - pk2 - tdiv((m - 512) * 100, 1024)
def r5_hf_mid(x, h, w):
    base = h * 585 // 1000
    m = r5_ridge(x * 256 // 75, 41, 5403, 3)
    g = r5_fbm(x * 256 // 200, 43, 5404, 2)
    hf = base + tdiv((m - 512) * 95, 1024) + tdiv((g - 512) * 40, 1024)
    nd = x - w * 30 // 100
    if -30 < nd < 30:
        hf = hf + 62 * (1 - nd * nd // 900)
    return hf
def r5_hf_plain(x, h):
    g2 = r5_fbm(x * 256 // 380, 53, 5407, 2)
    g3 = r5_fbm(x * 256 // 150, 55, 5408, 2)
    return h * 705 // 1000 + tdiv((g2 - 512) * 80, 1024) + tdiv((g3 - 512) * 30, 1024)

def read_bmp_24(path):
    with open(path, 'rb') as f:
        data = f.read()
    assert data[0:2] == b'BM'
    off = struct.unpack('<I', data[10:14])[0]
    w = struct.unpack('<i', data[18:22])[0]
    h = struct.unpack('<i', data[22:26])[0]
    assert struct.unpack('<H', data[28:30])[0] == 24
    stride = (w * 3 + 3) // 4 * 4
    img = np.zeros((h, w, 3), dtype=np.uint8)
    for row in range(h):
        src = off + (h - 1 - row) * stride
        px = np.frombuffer(data[src:src + w * 3], dtype=np.uint8).reshape(w, 3)
        img[row, :, 0] = px[:, 2]; img[row, :, 1] = px[:, 1]; img[row, :, 2] = px[:, 0]
    return img, w, h

def luma(img):
    return 0.299 * img[:, :, 0] + 0.587 * img[:, :, 1] + 0.114 * img[:, :, 2]

def parse_layout(path):
    lay = {}
    rocks = {}
    with open(path) as f:
        for line in f:
            p = line.split()
            if not p: continue
            if p[0] == 'SUN': lay['sun'] = tuple(map(int, p[1:4]))
            elif p[0] == 'SIZE': lay['size'] = tuple(map(int, p[1:3]))
            elif p[0] == 'PLANET': lay['planet'] = tuple(map(int, p[1:4]))
            elif p[0] == 'MOON': lay['moon'] = tuple(map(int, p[1:4]))
            elif p[0] == 'ROCK': rocks[int(p[1])] = tuple(map(int, p[2:5]))
    lay['rocks'] = rocks
    return lay

def azim(dx, dy):
    return math.degrees(math.atan2(dy, dx)) % 360.0

def ang_diff(a, b):
    d = abs(a - b) % 360.0
    return min(d, 360.0 - d)

def lit_centroid_az(img, cx, cy, r, frac=0.85):
    yy, xx = np.mgrid[0:img.shape[0], 0:img.shape[1]]
    d2 = (xx - cx) ** 2 + (yy - cy) ** 2
    m = d2 < (r * frac) ** 2
    lum = luma(img)
    vals = lum[m]
    lit = lum > np.median(vals)
    sel = m & lit
    if sel.sum() < 10: return None
    vx = xx[sel].mean() - cx
    vy = yy[sel].mean() - cy
    return azim(vx, vy), sel.sum()

def ac_local_maxima(ys, lo=150, hi=500, floor=0.0):
    y = np.array(ys, dtype=float)
    y -= y.mean()
    n = len(y)
    denom = (y * y).sum()
    cs = [abs((y[:n - l] * y[l:]).sum() / denom) for l in range(lo, hi)]
    mx = [(lo + i, cs[i]) for i in range(1, len(cs) - 1)
          if cs[i] >= cs[i - 1] and cs[i] >= cs[i + 1] and cs[i] > floor]
    mx.sort(key=lambda t: -t[1])
    return mx

def xcorr(a, b):
    a = np.array(a, dtype=float); b = np.array(b, dtype=float)
    a -= a.mean(); b -= b.mean()
    return abs((a * b).sum() / math.sqrt((a * a).sum() * (b * b).sum()))

def main():
    bmp_path, layout_path = sys.argv[1], sys.argv[2]
    img, w, h = read_bmp_24(bmp_path)
    lay = parse_layout(layout_path)
    sx, sy, sz = lay['sun']
    sun_az = azim(sx, sy)
    print(f'SUN vector {lay["sun"]} -> sun azimuth {sun_az:.1f} deg (screen x-right/y-down)')
    ok = True

    print('\n=== K4: one sun — implied azimuth from 4 elements ===')
    checks = []
    for name, key, fr in [('planet', 'planet', 0.85), ('moon', 'moon', 0.8), ('hero rock', 'rock0', 0.8)]:
        if key == 'rock0':
            cx, cy, rr = lay['rocks'][0]
        else:
            cx, cy, rr = lay[key]
        r = lit_centroid_az(img, cx, cy, rr, fr)
        if r is None:
            print(f'  {name}: NO LIT REGION (FAIL)'); ok = False; continue
        a, n = r
        d = ang_diff(a, sun_az)
        passed = d <= 30.0
        ok = ok and passed
        checks.append((name, a, d, passed))
        print(f'  {name}: implied az {a:.1f} deg, |dAz vs SUN| = {d:.1f} deg -> {"PASS" if passed else "FAIL"} (n={n})')
    # shadow azimuth of hero rock
    cx, cy, rr = lay['rocks'][0]
    lum = luma(img)
    yy, xx = np.mgrid[0:h, 0:w]
    # local plain reference: annulus to the left of the rock (away from shadow)
    ref = (xx > cx - 4 * rr) & (xx < cx - 2 * rr) & (np.abs(yy - cy) < rr)
    plain_lum = np.median(lum[ref])
    wedge = (xx > cx) & (xx < cx + 4 * rr) & (yy > cy - rr) & (yy < cy + 2 * rr)
    dark = wedge & (lum < 0.78 * plain_lum)
    if dark.sum() > 50:
        saz = azim(xx[dark].mean() - cx, yy[dark].mean() - cy)
        expect = (sun_az + 180.0) % 360.0
        d = ang_diff(saz, expect)
        passed = d <= 45.0
        ok = ok and passed
        print(f'  hero shadow: az {saz:.1f} deg vs expected {expect:.1f} (sun+180), d={d:.1f} -> {"PASS" if passed else "FAIL"}')
    else:
        print('  hero shadow: NO SHADOW FOUND (FAIL)'); ok = False

    print('\n=== K1: pasted-disc planet ===')
    pcx, pcy, pr = lay['planet']
    # sky color sampled outside the disc along each spoke
    widths, radii = [], []
    for k in range(16):
        th = k * math.pi / 8
        dx, dy = math.cos(th), math.sin(th)
        sxo = int(pcx + dx * (pr + 30)); syo = int(pcy + dy * (pr + 30))
        sky = img[syo, sxo].astype(float)
        center = img[pcy, pcx].astype(float)
        prof = []
        for r in range(pr - 14, pr + 14):
            x = int(pcx + dx * r); y = int(pcy + dy * r)
            if 0 <= x < w and 0 <= y < h:
                c = img[y, x].astype(float)
                denom = np.linalg.norm(center - sky)
                f = np.linalg.norm(c - sky) / denom if denom > 1 else 0
                prof.append((r, min(1.0, max(0.0, f))))
        r85 = r15 = r50 = None
        for r, f in prof:
            if r50 is None and f <= 0.5: r50 = r
            if f <= 0.85 and r85 is None: r85 = r
            if f <= 0.15: r15 = r
        if r85 is not None and r15 is not None:
            widths.append(r15 - r85)
        if r50 is not None:
            radii.append(r50)
    mw = float(np.mean(widths)) if widths else 0
    sr = float(np.std(radii)) if radii else 0
    p1 = mw >= 2.5
    p2 = sr >= 1.2
    ok = ok and p1 and p2
    print(f'  limb 15-85% width: {mw:.2f}px over {len(widths)} spokes (need >=2.5) -> {"PASS" if p1 else "FAIL"}')
    print(f'  limb radius std: {sr:.2f}px (need >=1.2, kills perfect circle) -> {"PASS" if p2 else "FAIL"}')
    # extinction: edge-half color close to sky
    edge_c = img[pcy, min(w - 1, pcx + int(np.mean(radii)) - 2)].astype(float) if radii else img[pcy, pcx].astype(float)
    sky_c = img[max(0, pcy - pr - 25), pcx].astype(float)
    cen_c = img[pcy, pcx].astype(float)
    er = np.linalg.norm(edge_c - sky_c) / max(1, np.linalg.norm(cen_c - sky_c))
    p3 = er < 0.55
    ok = ok and p3
    print(f'  extinction: |edge-sky|/|center-sky| = {er:.2f} (need <0.55) -> {"PASS" if p3 else "FAIL"}')

    print('\n=== K2: repeating mountain templates ===')
    T = 64  # trim to avoid convolution boundary artifacts
    xs = list(range(T, w - T))
    profs = {
        'ghost': np.array([r5_hf_ghost(x, h, w) for x in xs], dtype=float),
        'far': np.array([r5_hf_far(x, h, w) for x in xs], dtype=float),
        'mid': np.array([r5_hf_mid(x, h, w) for x in xs], dtype=float),
        'near': np.array([r5_hf_near(x, h, w) for x in xs], dtype=float),
    }
    # (a) no stamped repetition: a stamped peak train would imprint a
    # NARROW autocorrelation spike at its period; broad feature-scale
    # humps are natural and allowed
    p4 = True
    for name, pr in profs.items():
        mx = ac_local_maxima(pr, lo=150, hi=500, floor=0.35)
        narrow = []
        if mx:
            y = pr - pr.mean(); n = len(y); den = (y * y).sum()
            cs = np.array([abs((y[:n - l] * y[l:]).sum() / den) for l in range(150, 500)])
            for lag, val in mx[:3]:
                region = cs[max(0, lag - 150 - 80):lag - 150 + 80]
                wd = int(np.sum(region > 0.85 * val))
                narrow.append((lag, round(val, 3), wd))
        bad = [t for t in narrow if t[2] < 30]
        passed = len(bad) == 0
        p4 = p4 and passed
        print(f'  {name}: ac spikes>0.35 {narrow} -> {"PASS" if passed else "FAIL"}')
    ok = ok and p4
    # (b) the far row's two summits are different mountains, not stamps
    base_f = h * 470 // 1000
    full = np.array([r5_hf_far(x, h, w) for x in range(w)], dtype=float)
    def summit_params(x0, x1):
        seg = full[x0:x1]
        i = int(np.argmin(seg)); ht = base_f - seg[i]
        half = base_f - ht / 2
        l = i
        while l > 0 and seg[l] < half: l -= 1
        r = i
        while r < len(seg) - 1 and seg[r] < half: r += 1
        return ht, r - l
    h1, w1 = summit_params(560, 710)
    h2, w2 = summit_params(250, 365)
    hr = h1 / max(1, h2); wr = w1 / max(1, w2)
    p5 = (hr < 0.85 or hr > 1.18) or (wr < 0.80 or wr > 1.25)
    ok = ok and p5
    print(f'  far summits: heights {h1:.0f}/{h2:.0f}px widths {w1}/{w2}px -> {"PASS" if p5 else "FAIL"}')
    # (c) no row is a copy of another (detrended, boundary-trimmed)
    def detrend(p):
        k = np.ones(61) / 61
        return p[30:-30] - np.convolve(p, k, mode='valid')
    d = {n: detrend(pr) for n, pr in profs.items()}
    names = ['ghost', 'far', 'mid', 'near']
    p6 = True
    for ii in range(4):
        for jj in range(ii + 1, 4):
            c = xcorr(d[names[ii]], d[names[jj]])
            passed = c < 0.35
            p6 = p6 and passed
            print(f'  xcorr({names[ii]},{names[jj]}) = {c:.3f} (need <0.35) -> {"PASS" if passed else "FAIL"}')
    ok = ok and p6

    print('\n=== K3: floating rocks ===')
    lum = luma(img)
    dirt = np.array([138.0, 104.0, 78.0])
    for i in sorted(lay['rocks']):
        cx, cy, rr = lay['rocks'][i]
        ry = int(rr * 0.72)
        # contact AO: shader's exact AO band, darkest quartile vs a
        # local annulus (same ground ring, outside AO+shadow+rock)
        dnx = (xx - cx) * 1024 // (rr * 12 // 10)
        dny = (yy - (cy + ry * 30 // 100)) * 1024 // ry
        d2n = (dnx * dnx + dny * dny) // 1024
        band = (d2n > 655) & (d2n < 1600) & (yy > cy + ry * 10 // 100)
        inrock = ((xx - cx) ** 2 / (1.35 * rr) ** 2 + (yy - cy) ** 2 / (1.35 * ry) ** 2) < 1
        ann = (d2n >= 2200) & (d2n < 5200) & (yy > cy) & (~inrock)
        ratio = np.percentile(lum[band], 25) / max(1, np.median(lum[ann])) \
            if band.sum() > 20 and ann.sum() > 20 else 1.0
        p_ao = ratio < 0.92
        # burial: the stone's foot is dirt-tinted by the burial blend,
        # the crown is not
        c_foot = img[min(h - 1, cy + int(0.55 * ry)), cx].astype(float)
        c_mid = img[max(0, cy - int(0.2 * ry)), cx].astype(float)
        p_bu = np.linalg.norm(c_foot - dirt) < np.linalg.norm(c_mid - dirt)
        # non-circular: squat dome => top height / radius ~= 0.7,
        # never 1.0 (sphere). Top edge via strongest vertical gradient.
        col = lum[max(0, cy - 2 * rr):cy + 1, cx]
        gcol = np.abs(np.diff(col))
        lo = max(0, len(col) - int(1.6 * ry) - 1)
        uph = (len(col) - 1) - (lo + int(np.argmax(gcol[lo:])))
        squash = uph / max(1, rr)
        p_sq = 0.55 < squash < 0.90
        # cast shadow: near-field wedge core vs flanking ground at the
        # same distance (controls for radial ground-tint gradients)
        ox = cx + rr * 30 // 100; oy = cy + ry * 55 // 100
        rxx = xx - ox; ryy = yy - oy; sl = rr * 36 // 10
        t = (rxx * 94 + ryy * 34) // 100
        lat = np.abs(rxx * 34 - ryy * 94) // 100
        wdt = rr * 70 // 100 + t * 25 // 100
        core = (t > rr // 2) & (t < int(1.8 * rr)) & (lat < (wdt * 0.7)) & (~inrock)
        flank = (t > rr // 2) & (t < int(1.8 * rr)) & (lat > (wdt * 1.5)) & (lat < (wdt * 2.8)) & (~inrock)
        shr = np.median(lum[core]) / max(1, np.median(lum[flank])) \
            if core.sum() > 10 and flank.sum() > 10 else 1.0
        p_sh = shr < 0.95
        pall = p_ao and p_bu and p_sq and p_sh
        ok = ok and pall
        print(f'  rock{i}: AO {ratio:.2f}({"P" if p_ao else "F"}) burial({"P" if p_bu else "F"}) '
              f'dome {squash:.2f}({"P" if p_sq else "F"}) shadow {shr:.2f}({"P" if p_sh else "F"}) -> {"PASS" if pall else "FAIL"}')

    print('\nOVERALL:', 'ALL KILLERS DEAD' if ok else 'FAIL — see above')
    return 0 if ok else 1

if __name__ == '__main__':
    sys.exit(main())
