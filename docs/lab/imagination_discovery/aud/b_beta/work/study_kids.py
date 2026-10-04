#!/usr/bin/env python3
"""B-beta study: kids sources -> event catalog. Deterministic, no randomness.
Emits catalog_kids.bin (20-byte LE records) + prints STUDY LOG section.
Record: start_u32 end_u32 src_u16 voice_u16 peak_u16 cent_u16 durms_u16 flags_u16
flags: bit0 group, bit1 shout, bit2 laugh, bit3 ok_reverse, bit4 bed, bit5 footstep
src ids: 0 kids_park, 1 kids_playground, 2 kid_laugh, 3 kids_berlin
"""
import wave, struct, math, os, sys
import numpy as np

W = os.path.expanduser('~/workspace/tnn-lab/imagination_discovery/aud/b_beta/work/wav')
SR = 44100

def load(name):
    w = wave.open(os.path.join(W, name), 'rb')
    n = w.getnframes(); ch = w.getnchannels()
    raw = w.readframes(n); w.close()
    xs = np.array(struct.unpack('<' + 'h' * (n * ch), raw), dtype=np.float64)
    if ch == 2:
        xs = (xs[0::2] + xs[1::2]) / 2.0
    return xs

def envelope(xs, win=441):
    a = np.abs(xs)
    k = np.ones(win) / win
    return np.convolve(a, k, mode='same')

def detect(xs, thr_hi, thr_lo, min_gap_ms=100, min_dur_ms=80, max_dur_ms=5000):
    env = envelope(xs)
    evs = []
    i, n = 0, len(xs)
    mg = int(min_gap_ms * SR / 1000)
    while i < n:
        if env[i] > thr_hi:
            s = i
            last_hi = i
            while i < n:
                if env[i] > thr_hi:
                    last_hi = i
                if env[i] < thr_lo and (i - last_hi) > mg:
                    break
                i += 1
            e = min(i, n)
            dur_ms = (e - s) * 1000.0 / SR
            if min_dur_ms <= dur_ms <= max_dur_ms:
                evs.append((s, e))
        else:
            i += 1
    return evs

def features(xs, s, e):
    seg = xs[s:e]
    peak = float(np.max(np.abs(seg)))
    rms = float(np.sqrt(np.mean(seg ** 2)))
    dur_ms = (e - s) * 1000.0 / SR
    n = len(seg)
    if n >= 256:
        sp = np.abs(np.fft.rfft(seg * np.hanning(n)))
        fr = np.fft.rfftfreq(n, 1.0 / SR)
        cent = float(np.sum(fr * sp) / (np.sum(sp) + 1e-9))
    else:
        cent = 0.0
    zc = float(np.sum((seg[:-1] < 0) != (seg[1:] < 0))) / max(n - 1, 1)
    # subpeaks: envelope local maxima above 45% of event peak, >=60ms apart
    env = envelope(seg, 441)
    pk = np.max(env)
    sub = 0
    last = -10**9
    for j in range(1, len(env) - 1):
        if env[j] > 0.45 * pk and env[j] >= env[j-1] and env[j] >= env[j+1]:
            if j - last > int(0.06 * SR):
                sub += 1
                last = j
    return dict(peak=peak, rms=rms, dur_ms=dur_ms, cent=cent, zcr=zc, sub=sub)

def kmeans1d(vals, k=2, iters=30):
    # deterministic: init at min and max
    vs = sorted(vals)
    cs = [vs[0], vs[-1]][:k]
    assign = [0] * len(vs)
    for _ in range(iters):
        for i, v in enumerate(vs):
            assign[i] = min(range(k), key=lambda c: abs(v - cs[c]))
        for c in range(k):
            m = [vs[i] for i in range(len(vs)) if assign[i] == c]
            if m:
                cs[c] = sum(m) / len(m)
    return assign, cs

def main():
    files = ['kids_park.wav', 'kids_playground.wav', 'kid_laugh.wav', 'kids_berlin.wav']
    data = {f: load(f) for f in files}
    catalog = []  # (src_id, s, e, voice, flags, feat)

    for sid, f in enumerate(files):
        xs = data[f]
        env = envelope(xs)
        med = float(np.median(env))
        thr_hi = med * 2.0 + 600
        thr_lo = thr_hi * 0.35
        evs = detect(xs, thr_hi, thr_lo, min_gap_ms=180)
        print(f"--- {f}: {len(xs)/SR:.1f}s med_env={med:.0f} thr_hi={thr_hi:.0f} events={len(evs)}")
        feats = []
        for (s, e) in evs:
            ft = features(xs, s, e)
            if ft['peak'] < 2500:
                continue
            feats.append((s, e, ft))
        print(f"    kept {len(feats)} (peak>=2500)")
        for (s, e, ft) in feats:
            fl = 0
            if ft['sub'] >= 3 and ft['dur_ms'] <= 3000:
                fl |= 4  # laugh
            elif ft['sub'] <= 2 and 150 <= ft['dur_ms'] <= 1500 and ft['peak'] > 8000:
                fl |= 2  # shout
            fl |= 8  # ok_reverse default
            catalog.append([sid, s, e, -1, fl, ft])

    # group flag: event starting within 250ms of another event's start (any src)
    starts = sorted((c[1], idx) for idx, c in enumerate(catalog))
    for k in range(len(starts) - 1):
        if starts[k+1][0] - starts[k][0] < int(0.25 * SR):
            catalog[starts[k][1]][4] |= 1
            catalog[starts[k+1][1]][4] |= 1

    # voice assignment
    # voice 0 = kid_laugh.wav (known single 4yo boy)
    for c in catalog:
        if c[0] == 2:
            c[3] = 0
    # kids_park (src 0): 2-means on centroid -> voices 1,2 (order by centroid)
    for sid, vbase in ((0, 1), (1, 3)):
        idxs = [i for i, c in enumerate(catalog) if c[0] == sid]
        cents = [catalog[i][5]['cent'] for i in idxs]
        if len(cents) >= 4:
            assign, cs = kmeans1d(cents, 2)
            order = sorted(range(2), key=lambda c: cs[c])
            vmap = {order[0]: vbase, order[1]: vbase + 1}
            for i, a in zip(idxs, assign):
                catalog[i][3] = vmap[a]
            print(f"    src {sid}: centroid clusters {[round(x) for x in cs]} -> voices {vbase},{vbase+1}")
        elif idxs:
            for i in idxs:
                catalog[i][3] = vbase
    # kids_berlin footsteps: transient detector -> voice 9
    # (kids_berlin is distant ambience: no usable transients; steps are mined
    #  from kids_park / kids_playground / footstep_gravel instead)
    def mine_steps(xs, sid, cap, rise=1400, envthr=1800, peakthr=1800):
        env5 = envelope(xs, 220)
        d = env5[220:] - env5[:-220]
        steps = []
        i, n = 0, len(xs)
        while i < n - 300 and len(steps) < cap:
            if d[i] > rise and env5[i + 220] > envthr:
                s = max(0, i - 130)
                e = min(n, s + int(0.20 * SR))
                seg = xs[s:e]
                if float(np.max(np.abs(seg))) > peakthr:
                    # reject long tonal events: require fast decay (second half < 60% of first)
                    h = len(seg) // 2
                    r1 = float(np.sqrt(np.mean(seg[:h] ** 2)) + 1)
                    r2 = float(np.sqrt(np.mean(seg[h:] ** 2)))
                    if r2 < 0.6 * r1:
                        steps.append((s, e))
                i = e
            else:
                i += 1
        return steps
    n_steps = 0
    # steps are mined ONLY from forest_track4 (real footstep sequence, PD)
    # and the single gravel step; vocal-attack mining from src0/1 was rejected
    # (those transients are laugh onsets, not feet - using them as feet would
    # be dishonest labeling, caught in review 2026-09-22)
    g = load('footstep_gravel.wav')
    data['footstep_gravel.wav'] = g
    ft = features(g, 0, len(g))
    catalog.append([4, 0, len(g), 9, 8 | 32, ft])
    n_steps += 1
    fx = load('forest_track4.wav')
    data['forest_track4.wav'] = fx
    for (s, e) in mine_steps(fx, 5, 30, rise=600, envthr=800, peakthr=1500):
        ft = features(fx, s, e)
        catalog.append([5, s, e, 9, 8 | 32, ft])
        n_steps += 1
    print(f"    step transients: {n_steps} (gravel src 4 + forest src 5)")
    # kids_berlin (src 3) distant events -> voice 5 (background calls)
    for c in catalog:
        if c[0] == 3 and c[3] == -1:
            c[3] = 5
    # bed segments: 3 lowest-rms 4s windows in kids_berlin without events
    ev_ranges = [(c[1], c[2]) for c in catalog if c[0] == 3 and not (c[4] & 32)]
    win = 4 * SR
    cands = []
    for st in range(0, len(xs) - win, SR):
        if any(s < st + win and e > st for (s, e) in ev_ranges):
            continue
        seg = xs[st:st+win]
        cands.append((float(np.sqrt(np.mean(seg**2))), st))
    cands.sort()
    for rms, st in cands[:3]:
        ft = features(xs, st, st + win)
        catalog.append([3, st, st + win, 8, 8 | 16, ft])  # ok_reverse + bed
        print(f"    bed seg at {st/SR:.1f}s rms={rms:.0f}")

    # drop unvoiced
    catalog = [c for c in catalog if c[3] >= 0]
    catalog.sort(key=lambda c: (c[0], c[1]))

    # report
    print("\n=== CATALOG ===")
    for c in catalog:
        sid, s, e, v, fl, ft = c
        typ = 'laugh' if fl & 4 else ('shout' if fl & 2 else ('step' if fl & 32 else ('bed' if fl & 16 else 'vocal')))
        grp = 'G' if fl & 1 else '.'
        print(f"src{sid} v{v} {s/SR:7.2f}-{e/SR:7.2f}s {typ:6s}{grp} peak={ft['peak']:6.0f} cent={ft['cent']:5.0f}Hz sub={ft['sub']} dur={ft['dur_ms']:5.0f}ms")

    out = os.path.expanduser('~/workspace/tnn-lab/imagination_discovery/aud/b_beta/catalog_kids.bin')
    with open(out, 'wb') as f:
        for (sid, s, e, v, fl, ft) in catalog:
            f.write(struct.pack('<IIHHHHHH', s, e, sid, v, int(min(ft['peak'], 65535)),
                               int(min(ft['cent'], 65535)), int(min(ft['dur_ms'], 65535)), fl))
    print(f"\nwrote {out} ({len(catalog)} records)")

if __name__ == '__main__':
    main()
