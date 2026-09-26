#!/usr/bin/env python3
"""H2d: faithful independent recomputation of frame-12 neckcut.
Replicates v4_snout + v4_neckcut integer math (trunc division) from the
dumped dark mask (frame_91.ppm). Compares against the Zag probe's numbers.
"""
import math, sys

def read_ppm(path):
    with open(path, 'rb') as f:
        data = f.read()
    assert data[:2] == b'P6'
    i = 2
    parts = []
    while len(parts) < 3:
        while data[i:i+1] in (b' ', b'\n', b'\t', b'\r'): i += 1
        j = i
        while data[j:j+1] not in (b' ', b'\n', b'\t', b'\r'): j += 1
        parts.append(data[i:j].decode()); i = j
    W, H = int(parts[0]), int(parts[1])
    px = data[i+1:]
    assert len(px) == W*H*3, (len(px), W*H*3)
    return W, H, px

def tdiv(a, b):
    # truncating integer division like Zag i64 /
    q = abs(a)//abs(b)
    return -q if (a < 0) != (b < 0) else q

def main():
    d = sys.argv[1] if len(sys.argv) > 1 else '/tmp/dumpanat_test'
    W, H, dark = read_ppm(f'{d}/frame_91.ppm')
    N = W*H
    dm = bytearray(N)
    for p in range(N):
        dm[p] = 1 if dark[p*3] > 127 else 0
    # moments
    n = sx = sy = 0
    for p in range(N):
        if dm[p]: n += 1; sx += p % W; sy += p // W
    cx1024 = tdiv(sx*1024, n); cy1024 = tdiv(sy*1024, n)
    sxx = syy = sxy = 0
    for p in range(N):
        if dm[p]:
            dx = (p % W)*1024 - cx1024; dy = (p // W)*1024 - cy1024
            sxx += tdiv(dx*dx, 1024); syy += tdiv(dy*dy, 1024); sxy += tdiv(dx*dy, 1024)
    cxx = tdiv(sxx, n*1024); cyy = tdiv(syy, n*1024); cxy = tdiv(sxy, n*1024)
    # eigenvec (float is fine for the direction; snap to x1024 at the end)
    tr = cxx + cyy; det = tdiv(cxx*cyy - cxy*cxy, 1024)
    disc = max(0, tdiv(tr*tr, 1024) - 4*det)
    sq = int(math.isqrt(disc*1024))
    lam1 = tdiv(tr + sq, 2); lam2 = tdiv(tr - sq, 2)
    vx, vy = cxy, lam1 - cxx
    if vx == 0 and vy == 0:
        vx, vy = (1024, 0) if cxx >= cyy else (0, 1024)
    else:
        if vx < 0 or (vx == 0 and vy < 0): vx, vy = -vx, -vy
    ln = int(math.isqrt(vx*vx + vy*vy))
    ux, uy = (tdiv(vx*1024, ln), tdiv(vy*1024, ln)) if ln else (1024, 0)

    def snout(fx, fy):
        best = -(1 << 62); bx = by = 0
        for p in range(N):
            if dm[p]:
                pr = (p % W)*fx + (p // W)*fy
                if pr > best: best = pr; bx, by = p % W, p // W
        return bx, by

    def neckcut(sx_, sy_, fx, fy):
        px, py = -fy, fx
        cnt = [0]*128; tmn = [0]*128; tmx = [0]*128; wid = [-1]*128
        dmax = 0
        for p in range(N):
            if dm[p]:
                x = p % W; y = p // W
                dx = x - sx_; dy = y - sy_
                bd = -tdiv(dx*fx + dy*fy, 1024)
                if bd < 0: bd = 0
                t = tdiv(dx*px + dy*py, 1024)
                b = bd//4
                if b > 127: b = 127
                if bd > dmax: dmax = bd
                if cnt[b] == 0: tmn[b] = tmx[b] = t
                else:
                    if t < tmn[b]: tmn[b] = t
                    if t > tmx[b]: tmx[b] = t
                cnt[b] += 1
        for b in range(128):
            if cnt[b] >= 8: wid[b] = tmx[b] - tmn[b]
        sk, skw = -1, 0
        for b in range(128):
            if wid[b] > skw: skw = wid[b]; sk = b
        if sk < 0: return dict(rc=1)
        out = dict(rc=1, d_neck=-1, d_skull=sk*4+2, skull_w=skw, neck_w=0, prom=0)
        b = sk + 1
        while b < 127:
            w0 = wid[b]
            if w0 > 0 and cnt[b] >= 5:
                wl = wid[b-1]; wr = wid[b+1]
                ismin = 1
                if wl >= 0 and w0 > wl: ismin = 0
                if wr >= 0 and w0 > wr: ismin = 0
                if ismin == 1 and tdiv(skw*1024, w0) >= 1331:
                    out = dict(rc=0, d_neck=b*4+2, d_skull=sk*4+2,
                               skull_w=skw, neck_w=w0, prom=tdiv(skw*1024, w0))
                    break
            b += 1
        return out

    cands = []
    for (fx, fy) in ((ux, uy), (-ux, -uy)):
        sx_, sy_ = snout(fx, fy)
        nk = neckcut(sx_, sy_, fx, fy)
        cands.append((nk.get('prom', -1), fx, fy, sx_, sy_, nk))
    cands.sort(key=lambda c: -c[0])
    for prom, fx, fy, sx_, sy_, nk in cands:
        print("dir fx=%d fy=%d snout=(%d,%d) rc=%s d_neck=%s d_skull=%s skull_w=%s neck_w=%s prom=%s" % (
            fx, fy, sx_, sy_, nk['rc'], nk.get('d_neck'), nk.get('d_skull'),
            nk.get('skull_w'), nk.get('neck_w'), nk.get('prom')))
    print("zag_ref: snout=(63,220) rc=0 d_neck=154 d_skull=126 skull_w=83 neck_w=15 prom=5666")

main()
