#!/usr/bin/env python3
"""m3_numpy.py — vectorized replica of frozen motion3.zag (M3), for RM2 mining.

Identical arithmetic to motion3.zag (verified against the verdict binary):
block grid 8x8/stride 8, SAD over 25 offsets ox,oy in -2..2 with
edge-clamping, best-SAD tie-break (smallest |ox|+|oy|, then ox, then oy),
e = SAD(0,0)-SAD(best), vote iff e>0, eb[octant_bin] += e, isqrt of
ox^2+oy^2 for g_num. Zero RNG.
"""
import math
import numpy as np

NB = 8  # 8x8 blocks


def lum_plane(frame_rgb):
    a = np.frombuffer(frame_rgb, dtype=np.uint8).astype(np.int64)
    return (a[0::3] + a[1::3] + a[2::3]).reshape(64, 64)


def octant_bin(ox, oy):
    if ox == 0 and oy == 0:
        return 0
    ax, ay = abs(ox), abs(oy)
    if ax >= 2 * ay:
        return 3 if ox > 0 else 7
    if ay >= 2 * ax:
        return 5 if oy > 0 else 1
    if ox > 0 and oy > 0:
        return 4
    if ox < 0 and oy > 0:
        return 6
    if ox > 0 and oy < 0:
        return 2
    return 8


def pair_result(lum0, lum1):
    """lum arrays int64 (64,64). Returns (eb[9], n_vote, e_total, g_num,
    win_bin, per_block_best list[(ox,oy,e)])."""
    # clamp-shifted L1 for each offset (replicates the zag edge clamp)
    yy, xx = np.mgrid[0:64, 0:64]
    sad_per_off = np.empty((5, 5, NB, NB), dtype=np.int64)
    for oy_i, oy in enumerate((-2, -1, 0, 1, 2)):
        y1 = np.clip(yy + oy, 0, 63)
        for ox_i, ox in enumerate((-2, -1, 0, 1, 2)):
            x1 = np.clip(xx + ox, 0, 63)
            diff = np.abs(lum1[y1, x1] - lum0)
            # block sums: reshape (8,8,8,8) -> sum over inner axes
            sad_per_off[oy_i, ox_i] = diff.reshape(NB, 8, NB, 8).sum(axis=(1, 3))
    sad0 = sad_per_off[2, 2]
    # argmin with zag tie-break: iterate offsets in same order, take
    # strictly-less, then ties resolved by smaller |ox|+|oy|, ox, oy
    best_ox = np.zeros((NB, NB), dtype=np.int64)
    best_oy = np.zeros((NB, NB), dtype=np.int64)
    best_sad = np.full((NB, NB), 10 ** 18)
    cab_order = []
    for oy in (-2, -1, 0, 1, 2):
        for ox in (-2, -1, 0, 1, 2):
            cab_order.append((abs(ox) + abs(oy), ox, oy))
    for cab, ox, oy in sorted(cab_order):
        s = sad_per_off[oy + 2, ox + 2]
        # zag takes first (in loop order) on first encounter, then strictly
        # smaller sad, then tie by smaller cab, ox, oy. Iterating in the
        # sorted cab/ox/oy order gives exactly the tie rule: take when
        # sad < best_sad (loop order already respects the preference).
        take = s < best_sad
        best_sad = np.where(take, s, best_sad)
        best_ox = np.where(take, ox, best_ox)
        best_oy = np.where(take, oy, best_oy)
    e = sad0 - best_sad
    vote = e > 0
    n_vote = int(vote.sum())
    e_total = int(e[vote].sum())
    g_num = 0
    eb = [0] * 9
    win_bin = 0
    if n_vote:
        best_ox_v = best_ox[vote]
        best_oy_v = best_oy[vote]
        g_num = int(np.sum([math.isqrt(a * a + b * b)
                            for a, b in zip(best_ox_v, best_oy_v)]))
        for ox, oy, ev in zip(best_ox_v, best_oy_v, e[vote]):
            eb[octant_bin(int(ox), int(oy))] += int(ev)
        win_bin = max(range(9), key=lambda b: eb[b])
    return (eb, n_vote, e_total, g_num, win_bin,
            best_ox, best_oy, e, vote)


def clip_result(lums):
    """lums: list of 8 int64 (64,64) luminance planes."""
    eb = [0] * 9
    n_vote = 0
    e_total = 0
    g_num = 0
    pair_wins = []
    pair_nvotes = []
    for t in range(len(lums) - 1):
        peb, pn, pe, pg, pw, *_ = pair_result(lums[t], lums[t + 1])
        for b in range(9):
            eb[b] += peb[b]
        n_vote += pn
        e_total += pe
        g_num += pg
        pair_wins.append(pw)
        pair_nvotes.append(pn)
    n_tot = NB * NB * (len(lums) - 1)
    win = max(range(9), key=lambda b: eb[b])
    return {
        "eb": eb, "win": win,
        "coh_pm": 1000 * eb[win] // e_total if e_total else 0,
        "g_pm": 1000 * g_num // n_vote if n_vote else 0,
        "ebar": e_total // n_vote if n_vote else 0,
        "n_vote": n_vote, "n_tot": n_tot, "e_total": e_total,
        "pair_wins": pair_wins, "pair_nvotes": pair_nvotes,
    }
