#!/usr/bin/env python3
"""Goal-A video fix crew: metrics + template-persistence self-attack v2.
Measurement only. Uses exact background-only renders (field_bg_bin) as the
per-frame background reference. Reports:
 1. per-frame mean abs diff profile (min/mean/max, opening, active phase)
 2. subject presence per frame vs exact bg (bbox fraction + full-frame silhouette fraction)
 3. beat boundaries from the position functions
 4. template-persistence attack: translation-register subject crops across
    6+ frames; interior residuals must NOT be near-zero (articulation required)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vidtool import parse_avi, frame_to_rows, mean_abs_diff

W = H = 480
NF = 36

def ease_v1(u):
    if u <= 300: return 250 * u * u // 90000
    if u <= 700: return 250 + 550 * (u - 300) // 400
    t = 1000 - u
    return 1000 - 200 * t * t // 90000

def ease_v2(u):
    if u <= 400: return 300 * u * u // 160000
    if u <= 800: return 300 + 550 * (u - 400) // 400
    t = 1000 - u
    return 1000 - 150 * t * t // 40000

def subj_s(v, fr):
    if fr <= 5: return 0
    if fr >= NF - 4: return 1000
    u = (fr - 6) * 1000 // (NF - 11)
    return ease_v1(u) if v == 1 else ease_v2(u)

def bird_state(fr):
    s = subj_s(1, fr)
    sx = 140 + s * 720 // 1000
    sy = 310
    fold = (s - 900) * 1000 // 100 if s > 900 else 0
    if fold <= 500:
        sy += -22 if fr % 4 < 2 else 18
    if 430 < sx < 670:
        d = abs(550 - sx)
        sy += 70 * (120 - d) // 120
    if s > 900:
        sy += (s - 900) * 55 // 100
    return s, sx, sy, fold

def bird_bbox(fr):
    s, sx, sy, fold = bird_state(fr)
    return (sx - 380, sy - 210, sx + 380, sy + 165)

def boat_bx(fr):
    s = subj_s(2, fr)
    bx = 120 + s * 760 // 1000
    hx = abs(bx - 535)
    if hx < 130:
        bx -= 70 * (130 - hx) // 130
    return bx

def boat_state(fr):
    bx = boat_bx(fr)
    px = boat_bx(fr - 1) if fr > 0 else bx
    vel = bx - px
    m2 = fr % 12
    if m2 > 6: m2 = 12 - m2
    by = 760 + 8 * (m2 - 3) // 3
    return bx, by, vel

def boat_bbox(fr):
    bx, by, vel = boat_state(fr)
    wl = 95 + vel * 8
    return (bx - 145 - wl - 20, by - 280, bx + 215, by + 260)

def to_px(bb):
    x0, y0, x1, y1 = bb
    f = lambda c: max(0, min(W - 1, int(c * W / 1000)))
    return (f(x0), f(y0), f(x1), f(y1))

def luma(r, g, b):
    return (r * 77 + g * 150 + b * 29) >> 8

def luma_frame(rows):
    lr = bytearray(W * H)
    for y in range(H):
        row = rows[y]; base = y * W
        for x in range(W):
            lr[base + x] = luma(row[3*x], row[3*x+1], row[3*x+2])
    return lr

def crop_luma(lr, bb):
    x0, y0, x1, y1 = bb
    return [[lr[y*W+x] for x in range(x0, x1+1)] for y in range(y0, y1+1)]

def mask_of(sub_lr, bg_lr, bb, thr=25):
    # backgrounds are bit-identical between builds (deterministic grain cancels),
    # so a low threshold is safe and honest
    x0, y0, x1, y1 = bb
    return [[1 if abs(sub_lr[y*W+x] - bg_lr[y*W+x]) > thr else 0
             for x in range(x0, x1+1)] for y in range(y0, y1+1)]

def centroid(m):
    sx = sy = n = 0
    for y in range(len(m)):
        for x in range(len(m[0])):
            if m[y][x]: sx += x; sy += y; n += 1
    return (sx/max(1,n), sy/max(1,n), n)

def main():
    subj_path, bg_path, v = sys.argv[1], sys.argv[2], int(sys.argv[3])
    sframes, _ = parse_avi(subj_path)
    bframes, _ = parse_avi(bg_path)
    assert len(sframes) == len(bframes) == NF
    srows = [frame_to_rows(f, W, H) for f in sframes]
    brows = [frame_to_rows(f, W, H) for f in bframes]
    sflats = [b''.join(r) for r in srows]
    slum = [luma_frame(r) for r in srows]
    blum = [luma_frame(r) for r in brows]

    diffs = [mean_abs_diff(sflats[i], sflats[i+1]) for i in range(NF-1)]
    print(f'== v{v} per-frame mean abs diff ==')
    print(' '.join(f'{d:.1f}' for d in diffs))
    print(f'min={min(diffs):.2f} mean={sum(diffs)/len(diffs):.2f} max={max(diffs):.2f}')
    print(f'opening 0->1..4->5: {[f"{d:.2f}" for d in diffs[:5]]} (bar: no near-frozen opening; active motion must exceed 2.0)')
    act = diffs[6:31]
    print(f'active 6..31: min={min(act):.2f} mean={sum(act)/len(act):.2f}')

    bbox_fn = bird_bbox if v == 1 else boat_bbox
    print('== subject presence vs exact bg ==')
    pres = []; sil = []
    for fr in range(NF):
        bb = to_px(bbox_fn(fr))
        m = mask_of(slum[fr], blum[fr], bb)
        n = sum(sum(row) for row in m)
        tot = (bb[2]-bb[0]+1) * (bb[3]-bb[1]+1)
        p = n / tot
        pres.append(p)
        # full-frame silhouette fraction
        sn = 0
        for i in range(W*H):
            d = slum[fr][i] - blum[fr][i]
            if d < 0: d = -d
            if d > 25: sn += 1
        sil.append(sn / (W*H))
        bbf = tot / (W*H) * 100
        print(f'  fr {fr:02d}: bbox_presence={p:.3f} bbox={bb[2]-bb[0]+1}x{bb[3]-bb[1]+1} ({bbf:.1f}% frame) silhouette={sil[fr]*100:.2f}%')
    print(f'frames with bbox_presence>0.02: {sum(1 for p in pres if p>0.02)}/36')
    print(f'silhouette: min={min(sil)*100:.2f}% mean={sum(sil)/NF*100:.2f}% max={max(sil)*100:.2f}%')

    print('== beat boundaries (from position functions) ==')
    if v == 1:
        occ = [fr for fr in range(NF) if 490 <= bird_state(fr)[1] <= 610]
        land = [fr for fr in range(NF) if bird_state(fr)[0] > 900]
        print(f'establish 0-5 | move 6-31 | ridge occlusion {occ[0]}..{occ[-1]} | landing descent {land[0]}..{land[-1]} | settle 32-35')
    else:
        occ = [fr for fr in range(NF) if 488 <= boat_state(fr)[0] <= 582]
        hes = [fr for fr in range(NF) if abs((120 + subj_s(2, fr)*760//1000) - 535) < 130]
        print(f'establish 0-5 | move 6-31 | hesitation {hes[0]}..{hes[-1]} | piling occlusion {occ[0]}..{occ[-1]} | settle 32-35')

    print('== template-persistence self-attack (translation registration) ==')
    print('per-frame analytic subject boxes (from the deterministic position fns);')
    print('translation search +-40/12/6 inside; masks from exact bg.')
    print('sanity: frame vs itself shifted by (-10,-5) must score ~0 (validates the metric chain)')
    test_frames = [2, 9, 14, 24, 27, 31] if v == 1 else [2, 9, 15, 21, 26, 31]
    ref = test_frames[0]

    def register(fa_lum, fb_lum, fa_mask, fb_mask, fa_bb, fb_bb):
        """translate fb-box onto fa-box; returns (mad, dx, dy, n) or None"""
        acrop = crop_luma(fa_lum, fa_bb); amask = fa_mask
        bcrop = crop_luma(fb_lum, fb_bb); bmask = fb_mask
        best = None
        for step, rng in ((4, 40), (2, 12), (1, 6)):
            cx = best[1] if best else 0
            cy = best[2] if best else 0
            for dy in range(cy - rng, cy + rng + 1, step):
                for dx in range(cx - rng, cx + rng + 1, step):
                    tot = n = 0
                    for y in range(len(acrop)):
                        ty = y - dy
                        if ty < 0 or ty >= len(bcrop): continue
                        am = amask[y]; bc = bcrop[ty]; bm = bmask[ty]
                        for x in range(len(acrop[0])):
                            tx = x - dx
                            if tx < 0 or tx >= len(bc): continue
                            if am[x] or bm[tx]:
                                d = acrop[y][x] - bc[tx]
                                if d < 0: d = -d
                                tot += d; n += 1
                    if n > 2000:
                        mad = tot / n
                        if best is None or mad < best[0]:
                            best = (mad, dx, dy, n)
        return best

    def shift_luma(lr, dx, dy):
        out = bytearray(W * H)
        for y in range(H):
            sy = y - dy
            if 0 <= sy < H:
                for x in range(W):
                    sx = x - dx
                    if 0 <= sx < W:
                        out[y*W+x] = lr[sy*W+sx]
        return out

    ref_bb = to_px(bbox_fn(ref))
    refmask_full = mask_of(slum[ref], blum[ref], ref_bb)
    # sanity on the ref box: rigid content must score ~0. The (-10,-5) shift
    # pushes a few mask pixels off the box edge; restrict to the non-clipped
    # domain so the check is exact.
    Hm, Wm = len(refmask_full), len(refmask_full[0])
    sh = shift_luma(slum[ref], -10, -5)
    shm2 = [[0]*Wm for _ in range(Hm)]
    valid = [[0]*Wm for _ in range(Hm)]
    for y in range(Hm):
        for x in range(Wm):
            sx = x + 10; sy = y + 5
            if 0 <= sx < Wm and 0 <= sy < Hm:
                shm2[y][x] = refmask_full[sy][sx]
                valid[y][x] = 1
    refmask_v = [[refmask_full[y][x] & valid[y][x] for x in range(Wm)] for y in range(Hm)]
    sane = register(slum[ref], sh, refmask_v, shm2, ref_bb, ref_bb)
    _, _, rn = centroid(refmask_full)
    print(f'ref frame {ref}: box={ref_bb} subject mask px={rn}')
    print(f'sanity self-shift (-10,-5): MAD={sane[0]:.2f} at dx={sane[1]} dy={sane[2]} (expect ~0)')
    results = []
    for t in test_frames[1:]:
        t_bb = to_px(bbox_fn(t))
        tmask = mask_of(slum[t], blum[t], t_bb)
        rmask = mask_of(slum[ref], blum[ref], ref_bb)
        r = register(slum[ref], slum[t], rmask, tmask, ref_bb, t_bb)
        if r is None:
            print(f'  frame {t:02d} vs {ref}: NO VALID REGISTRATION')
            results.append(None); continue
        print(f'  frame {t:02d} vs {ref}: best interior MAD={r[0]:.2f} at dx={r[1]} dy={r[2]} (n={r[3]})')
        results.append(r[0])
    ok = [r for r in results if r is not None]
    if ok:
        print(f'mean interior MAD={sum(ok)/len(ok):.2f}')
        print('verdict rule: MADs far above the ~0 self-shift floor = ARTICULATED (PASS); near-zero = rigid template (FAIL)')

if __name__ == '__main__':
    main()
