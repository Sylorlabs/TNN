#!/usr/bin/env python3
"""Reconstruct the IDR frame (NAL 3) from the h264fix parse and compare
pixel-exactness against ffmpeg's no-deblock decode.

Implements H.264 spec:
  - 4x4 dequant+inverse transform (8-336/8-337, 8-338..8-354)
  - luma DC Hadamard + scaling (8.5.10, 8-321/8-322)
  - chroma DC 2x2 Hadamard + scaling (8.5.11, 8-326)
  - Intra_4x4 (8.3.1.2), Intra_16x16 (8.3.3), Intra chroma (8.3.4)
"""
import sys, hashlib
sys.path.insert(0, '/home/hatch/workspace/decoder_land/h264b')
import h264fix as H

W, Hh = 320, 240
Wc, Hc = W // 2, Hh // 2

YL = [[0] * W for _ in range(Hh)]
Cb = [[0] * Wc for _ in range(Hc)]
Cr = [[0] * Wc for _ in range(Hc)]

# 4x4 zigzag: scan index -> raster (y*4+x)
SCAN2RASTER = [0, 1, 4, 8, 5, 2, 3, 6, 9, 12, 13, 10, 7, 11, 14, 15]

def clip(v):
    return 0 if v < 0 else (255 if v > 255 else v)

def zigzag_to_mat(coeff):
    m = [[0] * 4 for _ in range(4)]
    for s, c in enumerate(coeff):
        r = SCAN2RASTER[s]
        m[r // 4][r % 4] = c
    return m

def scale_4x4(coeff_scan, qp, dc_already_scaled):
    """coeff_scan: 16 values in zigzag scan order. Returns scaled d[4][4].
    If dc_already_scaled, coeff_scan[0] is used as-is (d00=c00 per 8-335).
    LevelScale4x4 = weightScale(16, default flat) * normAdjust."""
    WS = 16  # default weightScale4x4 (no scaling lists in this stream)
    d = [[0] * 4 for _ in range(4)]
    for s in range(16):
        r = SCAN2RASTER[s]
        i, j = r // 4, r % 4
        c = coeff_scan[s]
        if s == 0 and dc_already_scaled:
            d[i][j] = c
        else:
            ls = H.level_scale_4x4(qp % 6, i, j) * WS
            if qp >= 24:
                d[i][j] = (c * ls) << (qp // 6 - 4)
            else:
                d[i][j] = (c * ls + (1 << (3 - qp // 6))) >> (4 - qp // 6)
    return d

def itrans_4x4(d):
    e = [[0] * 4 for _ in range(4)]
    f = [[0] * 4 for _ in range(4)]
    g = [[0] * 4 for _ in range(4)]
    h = [[0] * 4 for _ in range(4)]
    for i in range(4):
        e[i][0] = d[i][0] + d[i][2]
        e[i][1] = d[i][0] - d[i][2]
        e[i][2] = (d[i][1] >> 1) - d[i][3]
        e[i][3] = d[i][1] + (d[i][3] >> 1)
        f[i][0] = e[i][0] + e[i][3]
        f[i][1] = e[i][1] + e[i][2]
        f[i][2] = e[i][1] - e[i][2]
        f[i][3] = e[i][0] - e[i][3]
    for j in range(4):
        g[0][j] = f[0][j] + f[2][j]
        g[1][j] = f[0][j] - f[2][j]
        g[2][j] = (f[1][j] >> 1) - f[3][j]
        g[3][j] = f[1][j] + (f[3][j] >> 1)
        h[0][j] = g[0][j] + g[3][j]
        h[1][j] = g[1][j] + g[2][j]
        h[2][j] = g[1][j] - g[2][j]
        h[3][j] = g[0][j] - g[3][j]
    return [[(h[i][j] + 32) >> 6 for j in range(4)] for i in range(4)]

def luma_dc_scale(dc_coeff_scan, qp):
    """dc_coeff_scan: 16 DC values in zigzag order. Returns dcY[4][4]
    (dcY[i][j] = scaled DC for 4x4 block at block-col j, block-row i)."""
    c = zigzag_to_mat(dc_coeff_scan)
    t = [[0] * 4 for _ in range(4)]
    f = [[0] * 4 for _ in range(4)]
    for i in range(4):
        t[i][0] = c[i][0] + c[i][1] + c[i][2] + c[i][3]
        t[i][1] = c[i][0] + c[i][1] - c[i][2] - c[i][3]
        t[i][2] = c[i][0] - c[i][1] - c[i][2] + c[i][3]
        t[i][3] = c[i][0] - c[i][1] + c[i][2] - c[i][3]
    for j in range(4):
        f[0][j] = t[0][j] + t[1][j] + t[2][j] + t[3][j]
        f[1][j] = t[0][j] + t[1][j] - t[2][j] - t[3][j]
        f[2][j] = t[0][j] - t[1][j] - t[2][j] + t[3][j]
        f[3][j] = t[0][j] - t[1][j] + t[2][j] - t[3][j]
    ls = H.level_scale_4x4(qp % 6, 0, 0) * 16  # weightScale=16 default
    dcY = [[0] * 4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            if qp >= 36:
                dcY[i][j] = (f[i][j] * ls) << (qp // 6 - 6)
            else:
                dcY[i][j] = (f[i][j] * ls + (1 << (5 - qp // 6))) >> (6 - qp // 6)
    return dcY

def chroma_dc_scale(dc4, qp):
    """dc4: 4 DC coeffs in 2x2 scan order [c00,c10,c01,c11].
    Returns dcC[2][2] (dcC[i][j] for chroma block at block-col j,row i)."""
    c00, c10, c01, c11 = dc4
    f00 = c00 + c10 + c01 + c11
    f01 = c00 - c10 + c01 - c11
    f10 = c00 + c10 - c01 - c11
    f11 = c00 - c10 - c01 + c11
    ls = H.level_scale_4x4(qp % 6, 0, 0) * 16  # weightScale=16 default
    sh = qp // 6
    return [[((f * ls) << sh) >> 5 for f in row] for row in ((f00, f01), (f10, f11))]

# ---------------- reference sample availability ----------------
def ref_luma_4x4(fx, fy, mbX, mbY, curb):
    if fx < 0 or fy < 0 or fx >= W or fy >= Hh:
        return False, 0
    nx, ny = fx // 16, fy // 16
    if ny < mbY or (ny == mbY and nx < mbX):
        return True, YL[fy][fx]
    if ny == mbY and nx == mbX:
        bx, by = (fx % 16) // 4, (fy % 16) // 4
        if H._l4_idx(bx, by) < curb:
            return True, YL[fy][fx]
    return False, 0

def ref_luma_mb(fx, fy, mbX, mbY):
    if fx < 0 or fy < 0 or fx >= W or fy >= Hh:
        return False, 0
    nx, ny = fx // 16, fy // 16
    if ny < mbY or (ny == mbY and nx < mbX):
        return True, YL[fy][fx]
    return False, 0

def ref_chroma(fx, fy, mbX, mbY, plane):
    if fx < 0 or fy < 0 or fx >= Wc or fy >= Hc:
        return False, 0
    nx, ny = fx // 8, fy // 8
    if ny < mbY or (ny == mbY and nx < mbX):
        return True, plane[fy][fx]
    return False, 0

# ---------------- Intra_4x4 ----------------
def pred_intra4x4(xO, yO, mbX, mbY, b, mode):
    P = {}
    for x in range(8):
        P[(x, -1)] = ref_luma_4x4(xO + x, yO - 1, mbX, mbY, b)
    for y in range(-1, 4):
        P[(-1, y)] = ref_luma_4x4(xO - 1, yO + y, mbX, mbY, b)
    # group substitution: p[4..7][-1] all unavailable & p[3][-1] available
    if all(not P[(x, -1)][0] for x in range(4, 8)) and P[(3, -1)][0]:
        for x in range(4, 8):
            P[(x, -1)] = (True, P[(3, -1)][1])
    v = lambda k: P[k][1]
    av = lambda k: P[k][0]
    out = [[0] * 4 for _ in range(4)]
    if mode == 0:
        for x in range(4):
            for y in range(4):
                out[y][x] = v((x, -1))
    elif mode == 1:
        for x in range(4):
            for y in range(4):
                out[y][x] = v((-1, y))
    elif mode == 2:
        top = all(av((x, -1)) for x in range(4))
        left = all(av((-1, y)) for y in range(4))
        if top and left:
            s = sum(v((x, -1)) for x in range(4)) + sum(v((-1, y)) for y in range(4))
            d = (s + 4) >> 3
        elif left:
            d = (sum(v((-1, y)) for y in range(4)) + 2) >> 2
        elif top:
            d = (sum(v((x, -1)) for x in range(4)) + 2) >> 2
        else:
            d = 128
        out = [[d] * 4 for _ in range(4)]
    elif mode == 3:
        for x in range(4):
            for y in range(4):
                if x == 3 and y == 3:
                    out[y][x] = (v((6, -1)) + 3 * v((7, -1)) + 2) >> 2
                else:
                    out[y][x] = (v((x + y, -1)) + 2 * v((x + y + 1, -1)) + v((x + y + 2, -1)) + 2) >> 2
    elif mode == 4:
        for x in range(4):
            for y in range(4):
                if x > y:
                    out[y][x] = (v((x - y - 2, -1)) + 2 * v((x - y - 1, -1)) + v((x - y, -1)) + 2) >> 2
                elif x < y:
                    out[y][x] = (v((-1, y - x - 2)) + 2 * v((-1, y - x - 1)) + v((-1, y - x)) + 2) >> 2
                else:
                    out[y][x] = (v((0, -1)) + 2 * v((-1, -1)) + v((-1, 0)) + 2) >> 2
    elif mode == 5:
        for x in range(4):
            for y in range(4):
                z = 2 * x - y
                if z in (0, 2, 4, 6):
                    out[y][x] = (v((x - (y >> 1) - 1, -1)) + v((x - (y >> 1), -1)) + 1) >> 1
                elif z in (1, 3, 5):
                    out[y][x] = (v((x - (y >> 1) - 2, -1)) + 2 * v((x - (y >> 1) - 1, -1)) + v((x - (y >> 1), -1)) + 2) >> 2
                elif z == -1:
                    out[y][x] = (v((-1, 0)) + 2 * v((-1, -1)) + v((0, -1)) + 2) >> 2
                else:
                    out[y][x] = (v((-1, y - 1)) + 2 * v((-1, y - 2)) + v((-1, y - 3)) + 2) >> 2
    elif mode == 6:
        for x in range(4):
            for y in range(4):
                z = 2 * y - x
                if z in (0, 2, 4, 6):
                    out[y][x] = (v((-1, y - (x >> 1) - 1)) + v((-1, y - (x >> 1))) + 1) >> 1
                elif z in (1, 3, 5):
                    out[y][x] = (v((-1, y - (x >> 1) - 2)) + 2 * v((-1, y - (x >> 1) - 1)) + v((-1, y - (x >> 1))) + 2) >> 2
                elif z == -1:
                    out[y][x] = (v((-1, 0)) + 2 * v((-1, -1)) + v((0, -1)) + 2) >> 2
                else:
                    out[y][x] = (v((x - 1, -1)) + 2 * v((x - 2, -1)) + v((x - 3, -1)) + 2) >> 2
    elif mode == 7:
        for x in range(4):
            for y in range(4):
                if y in (0, 2):
                    out[y][x] = (v((x + (y >> 1), -1)) + v((x + (y >> 1) + 1, -1)) + 1) >> 1
                else:
                    out[y][x] = (v((x + (y >> 1), -1)) + 2 * v((x + (y >> 1) + 1, -1)) + v((x + (y >> 1) + 2, -1)) + 2) >> 2
    elif mode == 8:
        for x in range(4):
            for y in range(4):
                z = x + 2 * y
                if z in (0, 2, 4):
                    out[y][x] = (v((-1, y + (x >> 1))) + v((-1, y + (x >> 1) + 1)) + 1) >> 1
                elif z in (1, 3):
                    out[y][x] = (v((-1, y + (x >> 1))) + 2 * v((-1, y + (x >> 1) + 1)) + v((-1, y + (x >> 1) + 2)) + 2) >> 2
                elif z == 5:
                    out[y][x] = (v((-1, 2)) + 3 * v((-1, 3)) + 2) >> 2
                else:  # z > 5
                    out[y][x] = v((-1, 3))
    return out

# ---------------- Intra_16x16 ----------------
def pred_intra16x16(xO, yO, mbX, mbY, mode):
    P = {}
    for x in range(-1, 16):
        P[(x, -1)] = ref_luma_mb(xO + x, yO - 1, mbX, mbY)
    for y in range(16):
        P[(-1, y)] = ref_luma_mb(xO - 1, yO + y, mbX, mbY)
    v = lambda k: P[k][1]
    av = lambda k: P[k][0]
    out = [[0] * 16 for _ in range(16)]
    if mode == 0:
        for x in range(16):
            for y in range(16):
                out[y][x] = v((x, -1))
    elif mode == 1:
        for x in range(16):
            for y in range(16):
                out[y][x] = v((-1, y))
    elif mode == 2:
        top = all(av((x, -1)) for x in range(16))
        left = all(av((-1, y)) for y in range(16))
        if top and left:
            s = sum(v((x, -1)) for x in range(16)) + sum(v((-1, y)) for y in range(16))
            d = (s + 16) >> 5
        elif left:
            d = (sum(v((-1, y)) for y in range(16)) + 8) >> 4
        elif top:
            d = (sum(v((x, -1)) for x in range(16)) + 8) >> 4
        else:
            d = 128
        out = [[d] * 16 for _ in range(16)]
    elif mode == 3:
        Hh_ = sum((xp + 1) * (v((8 + xp, -1)) - v((6 - xp, -1))) for xp in range(8))
        Vv = sum((yp + 1) * (v((-1, 8 + yp)) - v((-1, 6 - yp))) for yp in range(8))
        b = (5 * Hh_ + 32) >> 6
        c = (5 * Vv + 32) >> 6
        a = 16 * (v((-1, 15)) + v((15, -1)))
        for x in range(16):
            for y in range(16):
                out[y][x] = clip((a + b * (x - 7) + c * (y - 7) + 16) >> 5)
    return out

# ---------------- Intra chroma ----------------
def pred_intra_chroma(xO, yO, mbX, mbY, mode, plane):
    P = {}
    for x in range(-1, 8):
        P[(x, -1)] = ref_chroma(xO + x, yO - 1, mbX, mbY, plane)
    for y in range(8):
        P[(-1, y)] = ref_chroma(xO - 1, yO + y, mbX, mbY, plane)
    v = lambda k: P[k][1]
    av = lambda k: P[k][0]
    out = [[0] * 8 for _ in range(8)]
    if mode == 2:
        for x in range(8):
            for y in range(8):
                out[y][x] = v((x, -1))
    elif mode == 1:
        for x in range(8):
            for y in range(8):
                out[y][x] = v((-1, y))
    elif mode == 0:
        for (bxo, byo) in ((0, 0), (4, 0), (0, 4), (4, 4)):
            top = all(av((bxo + x, -1)) for x in range(4))
            left = all(av((-1, byo + y)) for y in range(4))
            st = sum(v((bxo + x, -1)) for x in range(4))
            sl = sum(v((-1, byo + y)) for y in range(4))
            if (bxo, byo) == (0, 0) or (bxo > 0 and byo > 0):
                if top and left:
                    d = (st + sl + 4) >> 3
                elif left:
                    d = (sl + 2) >> 2
                elif top:
                    d = (st + 2) >> 2
                else:
                    d = 128
            elif byo == 0:
                if top:
                    d = (st + 2) >> 2
                elif left:
                    d = (sl + 2) >> 2
                else:
                    d = 128
            else:
                if left:
                    d = (sl + 2) >> 2
                elif top:
                    d = (st + 2) >> 2
                else:
                    d = 128
            for x in range(4):
                for y in range(4):
                    out[byo + y][bxo + x] = d
    elif mode == 3:
        Hh_ = sum((xp + 1) * (v((4 + xp, -1)) - v((2 - xp, -1))) for xp in range(4))
        Vv = sum((yp + 1) * (v((-1, 4 + yp)) - v((-1, 2 - yp))) for yp in range(4))
        b = (34 * Hh_ + 32) >> 6
        c = (34 * Vv + 32) >> 6
        a = 16 * (v((-1, 7)) + v((7, -1)))
        for x in range(8):
            for y in range(8):
                out[y][x] = clip((a + b * (x - 3) + c * (y - 3) + 16) >> 5)
    return out

# ---------------- main reconstruction ----------------
def main():
    nals = H.load_stream('stream.in')
    sps = pps = None
    mbW = mbH = 0
    for nal in nals:
        t = nal[0] & 31
        if t == 7:
            sps = H.parse_sps(nal)
        elif t == 8:
            pps = H.parse_pps(nal)
        elif t == 5:
            mbW = sps.pic_width_in_mbs_minus1 + 1
            mbH = sps.pic_height_in_map_units_minus1 + 1
            br = H.BitReader(H.rbsp_unescape(nal[1:]))
            h = H.parse_slice_header(br, t, sps, pps)
            mbs = H.parse_slice(br, h, sps, pps, None)
            break
    qp_off = pps.chroma_qp_index_offset
    for mbAddr, mb in enumerate(mbs):
        if mb is None:
            continue
        mbX, mbY = mbAddr % mbW, mbAddr // mbW
        xO, yO = mbX * 16, mbY * 16
        qpY = mb.qp
        qpC = H.QPC_T[max(0, min(51, qpY + qp_off))]
        resd = {('y', r['b']): r['coeff'] for r in mb.res if r['comp'] == 'y'}
        resCb = {r['b']: r['coeff'] for r in mb.res if r['comp'] == 'cb'}
        resCr = {r['b']: r['coeff'] for r in mb.res if r['comp'] == 'cr'}
        if mb.name == 'I_4x4':
            for b in range(16):
                bx, by = H._l4_xy(b)
                px, py = xO + bx * 4, yO + by * 4
                pred = pred_intra4x4(px, py, mbX, mbY, b, mb.i4modes[b])
                coeff = resd.get(('y', b), [0] * 16)
                r = itrans_4x4(scale_4x4(coeff, qpY, False))
                for yy in range(4):
                    for xx in range(4):
                        YL[py + yy][px + xx] = clip(pred[yy][xx] + r[yy][xx])
        elif mb.name == 'I_16x16':
            pred = pred_intra16x16(xO, yO, mbX, mbY, mb.i16mode)
            dcY = luma_dc_scale(resd[('y', 16)], qpY)
            for b in range(16):
                bx, by = H._l4_xy(b)
                px, py = xO + bx * 4, yO + by * 4
               
                coeff_ac = resd.get(('y', b), [0] * 15)
                full = [dcY[by][bx]] + coeff_ac  # zigzag order: [DC, AC...]
                r = itrans_4x4(scale_4x4(full, qpY, True))
                for yy in range(4):
                    for xx in range(4):
                        YL[py + yy][px + xx] = clip(pred[by * 4 + yy][bx * 4 + xx] + r[yy][xx])
        # chroma (4:2:0, 8x8 per MB)
        cxO, cyO = mbX * 8, mbY * 8
        for plane, resC in ((Cb, resCb), (Cr, resCr)):
            pred = pred_intra_chroma(cxO, cyO, mbX, mbY, mb.chroma_mode, plane)
            dcC = chroma_dc_scale(resC.get(4, [0] * 4), qpC)
            for b in range(4):
                bx, by = (b % 2), (b // 2)
                px, py = cxO + bx * 4, cyO + by * 4
                coeff_ac = resC.get(b, [0] * 15)
                full = [dcC[by][bx]] + coeff_ac
                r = itrans_4x4(scale_4x4(full, qpC, True))
                for yy in range(4):
                    for xx in range(4):
                        plane[py + yy][px + xx] = clip(pred[by * 4 + yy][bx * 4 + xx] + r[yy][xx])
    out = bytearray()
    for row in YL:
        out += bytes(row)
    for row in Cb:
        out += bytes(row)
    for row in Cr:
        out += bytes(row)
    open('/tmp/recon_idr0.yuv', 'wb').write(bytes(out))
    mine = hashlib.sha256(bytes(out)).hexdigest()
    ref = hashlib.sha256(open('/tmp/idr0_nodeblock.yuv', 'rb').read()).hexdigest()
    print('mine:', mine)
    print('ff  :', ref)
    print('MATCH' if mine == ref else 'DIFFER')

if __name__ == '__main__':
    main()
