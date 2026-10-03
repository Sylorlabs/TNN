#!/usr/bin/env python3
"""scorer_ctrl.py — FROZEN scorer for Phase B2b (PREREG_LH §2b/§2c).

Offline Python: reads committed render WAVs + the ctrl journal, never touches
the per-trial path. Measurement definitions are frozen here BEFORE scored runs.

Definitions (frozen):
  - F0: scorer_p.med_f0 (median of scorer-voiced frame F0), Hz.
  - ENV: scorer_p.ans_env (rise/flat/decay, ±4 dB thirds).
  - PROSODY CV: robust coefficient of variation of scorer-voiced frame F0:
    median-3 filtered (kills isolated octave-jump frames), f0>0 only
    (f0=0 is the estimator's "no estimate" flag, not a measurement), then
    std/mean. Rationale: raw frame CV on real speech is dominated by
    estimator octave-jumps (measured: neutral speech reads cv~1.0 raw vs
    ~true prosody); the median-3 robust CV measures pitch variation.
    FROZEN choice, documented in RUNLOG as prereg-noted deviation
    (scorer_p.py defines no prosody CV; the prereg's "scorer prosody CV"
    is underdetermined).

Hit criteria (§2b):
  - pitch:   |f0_ren - f0_ref| / f0_ref <= 0.05  (f0_ref > 0)
  - env:     env_ren == env_ref
  - prosody: |cv_ren - cv_ref| / cv_ref <= 0.25  (cv_ref > 0)

ERR (§2c, per loop iteration k):
  ERR(k) = |f0_ren_k - f0_ref|/f0_ref            [only if f0_ref >= 125]
         + 0.5 * [env_ren_k != env_ref]
         + 0.5 * [|cv_ren_k - cv_ref|/cv_ref > 0.25]

Guards:
  - RC0: severed renders (440 Hz / flat / no vibrato) vs same refs.
    One-sided EXACT test (Fisher hypergeometric, zero RNG) for
    wired hits > severed hits, per axis. Bar: p < 0.01.
  - RC1: frozen derangement = cyclic shift by n/2 of each axis target list
    (pitch/prosody: spread-ordered, so shift pairs low<->high;
     envelope: list interleaved R/F/D, shift by 20 pairs cross-class).
    Scorer compares render_i against ref_{der(i)}. Bar: <= 25% hits per
    axis, else the SCORER is void (not the trial).

Usage:
  scorer_ctrl.py score <journal> <outdir> <axis>   # axis: pitch|env|pros|loop
  scorer_ctrl.py rc0  <journal_w> <dir_w> <journal_s> <dir_s> <axis>
  scorer_ctrl.py rc1  <journal> <outdir> <axis>
  scorer_ctrl.py loop <journal> <outdir>           # full §2c battery
Prints JSON to stdout.
"""
import json, math, os, sys

sys.path.insert(0, '/home/hatch/workspace/audio_principles/crew_p')
import scorer_p as SP  # noqa: E402  (frozen measurement definitions)
import numpy as np  # noqa: E402


def cv_robust(fe):
    v = fe['f0'][fe['voiced'] & (fe['f0'] > 0)]
    if len(v) < 7:
        return 0.0
    m = float(v.mean())
    if m <= 0:
        return 0.0
    w = np.array([sorted((v[max(0, i - 1)], v[i], v[min(len(v) - 1, i + 1)]))[1]
                  for i in range(len(v))])
    return float(w.std() / w.mean())


def measure(path):
    fe = SP.features(path)
    return {'f0': float(SP.med_f0(fe)), 'env': SP.ans_env(fe),
            'cv': cv_robust(fe), 'nfr': int(fe['nfr'])}


def pitch_hit(m_ref, m_ren):
    fr, fn = m_ref['f0'], m_ren['f0']
    if fr <= 0 or fn <= 0:
        return False
    return abs(fn - fr) / fr <= 0.05


def env_hit(m_ref, m_ren):
    return m_ren['env'] == m_ref['env']


def pros_hit(m_ref, m_ren):
    cr, cn = m_ref['cv'], m_ren['cv']
    if cr <= 0:
        return cn <= 0.005
    return abs(cn - cr) / cr <= 0.25


HITFN = {'pitch': pitch_hit, 'env': env_hit, 'pros': pros_hit}


# Frozen RC1 derangements (documented, fixed before scored runs):
#   pitch40, pros40 (spread-ordered): cyclic shift by 20  -> min rel dist 0.41 / 0.26
#   env40 (interleaved R/F/D order in env40_order.json): shift by 1 -> 0 same-class pairs
DERANGE_SHIFT = {'pitch': 20, 'env': 1, 'pros': 20}


def parse_journal(path):
    """-> list of dicts: idx, depth, kind, ref, planned dict, render paths."""
    tgts = []
    cur = None
    iters = None
    with open(path) as f:
        for line in f:
            line = line.rstrip('\n')
            if line.startswith('TARGET '):
                p = line.split()
                cur = {'idx': int(p[1]), 'depth': int(p[2].split('=')[1]),
                       'kind': p[3].split('=')[1], 'ref': p[4].split('=', 1)[1],
                       'planned': {}, 'iters': [], 'render': None,
                       'dev': {}}
                tgts.append(cur)
                iters = cur['iters']
            elif line.startswith('PLANNED ') and cur is not None and not iters:
                kv = dict(kv.split('=', 1) for kv in line.split()[1:])
                cur['planned'] = kv
            elif line.startswith('RENDERED ') and cur is not None and not iters:
                cur['render'] = line.split(' ', 1)[1]
            elif line.startswith('ITER ') and cur is not None:
                p = line.split()
                itn = int(p[1])
                while len(iters) <= itn:
                    iters.append({})
                if p[2] == 'PLANNED':
                    kv = dict(kv.split('=', 1) for kv in p[3:])
                    iters[itn]['planned'] = kv
                elif p[2] == 'RENDERED':
                    iters[itn]['render'] = line.split('RENDERED ', 1)[1]
                elif p[2] == 'DEVIATION':
                    kv = dict(kv.split('=', 1) for kv in p[3:])
                    iters[itn]['dev'] = kv
    return tgts


def err_of(m_ref, m_ren):
    e = 0.0
    if m_ref['f0'] >= 125:
        fr, fn = m_ref['f0'], m_ren['f0']
        e += abs(fn - fr) / fr if fr > 0 else 1.0
    if m_ren['env'] != m_ref['env']:
        e += 0.5
    cr, cn = m_ref['cv'], m_ren['cv']
    if cr > 0 and abs(cn - cr) / cr > 0.25:
        e += 0.5
    elif cr <= 0 and cn > 0.005:
        e += 0.5
    return e


def score_axis(journal, outdir, axis, derange=False, lo=None, hi=None):
    tgts = parse_journal(journal)
    ms = [t for t in tgts if t['kind'] == 'M']
    if lo is not None:
        ms = [t for t in ms if lo <= t['idx'] < hi]
    n = len(ms)
    refs = [measure(t['ref']) for t in ms]
    rens = [measure(os.path.join(outdir, os.path.basename(t['render'])))
            for t in ms]
    if derange:
        sh = DERANGE_SHIFT[axis]
        refs = [refs[(i + sh) % n] for i in range(n)]
    hits = [HITFN[axis](rf, rn) for rf, rn in zip(refs, rens)]
    return {'axis': axis, 'n': n, 'hits': sum(hits),
            'hit_rate': sum(hits) / n if n else 0.0,
            'hit_idx': [i for i, h in enumerate(hits) if h],
            'miss_idx': [i for i, h in enumerate(hits) if not h],
            'deranged': derange}


def perm_p(hits_w, hits_s):
    """One-sided exact test for wired hits > severed hits.

    Fisher's exact (hypergeometric): given total hits H across N=nw+ns trials,
    wired hits X ~ Hypergeometric(N, H, nw) under the null. p = P(X >= x_obs).
    Zero RNG; deterministic exact calculation.
    """
    nw, ns = len(hits_w), len(hits_s)
    x_obs = sum(hits_w)
    H = x_obs + sum(hits_s)
    N = nw + ns
    obs = x_obs - sum(hits_s)
    # P(X >= x_obs) = sum_{x=x_obs}^{min(nw,H)} C(H,x)*C(N-H,nw-x) / C(N,nw)
    denom = math.comb(N, nw)
    p = 0.0
    for x in range(x_obs, min(nw, H) + 1):
        if x < 0 or (nw - x) < 0 or (nw - x) > (N - H):
            continue
        p += math.comb(H, x) * math.comb(N - H, nw - x) / denom
    return p, obs


def wilcoxon_onesided(diffs):
    """signed-rank, H1: median < 0 (improvement). Exact via 2^n enumeration."""
    pairs = [(abs(d), 1 if d < 0 else -1) for d in diffs if d != 0]
    nn = len(pairs)
    if nn == 0:
        return 1.0, 0, 0
    order = sorted(range(nn), key=lambda i: pairs[i][0])
    ranks = [0.0] * nn
    i = 0
    while i < nn:
        j = i
        while j + 1 < nn and pairs[order[j + 1]][0] == pairs[order[i]][0]:
            j += 1
        avg = (i + 1 + j + 1) / 2.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    w_obs = sum(ranks[i] for i in range(nn) if pairs[i][1] > 0)
    ge = 0
    total = 1 << nn
    for mask in range(total):
        w = 0.0
        for i in range(nn):
            if (mask >> i) & 1:
                w += ranks[i]
        if w >= w_obs:
            ge += 1
    return ge / total, w_obs, nn


def score_loop(journal, outdir):
    tgts = [t for t in parse_journal(journal) if t['kind'] == 'L']
    cases = []
    for t in tgts:
        m_ref = measure(t['ref'])
        errs = []
        for it in t['iters']:
            rp = os.path.join(outdir, os.path.basename(it['render']))
            errs.append(err_of(m_ref, measure(rp)))
        cases.append({'depth': t['depth'], 'ref': t['ref'],
                      'f0_ref': m_ref['f0'], 'errs': errs,
                      'dev0_df0': int(t['iters'][1]['dev'].get('df0_mhz', 0))
                      if len(t['iters']) > 1 else 0,
                      'render0': t['iters'][0]['render'] if t['iters'] else None,
                      'render3': t['iters'][3]['render'] if len(t['iters']) > 3 else None})
    n = len(cases)
    e0 = [c['errs'][0] for c in cases]
    e3 = [c['errs'][3] for c in cases]
    # Aggregate ERR ratio: sum(ERR3)/sum(ERR0) (prereg "ERR(3)/ERR(0)").
    s0, s3 = sum(e0), sum(e3)
    mean_ratio = (s3 / s0) if s0 > 0 else float('nan')
    diffs = [b - a for a, b in zip(e0, e3)]
    p_w, w_obs, nn = wilcoxon_onesided(diffs)
    improved = sum(1 for d in diffs if d < 0)
    # instability flags
    for c in cases:
        es = c['errs']
        c['unstable'] = any(es[k + 1] > es[k] + 0.01 for k in range(3))
        dirs = [1 if es[k + 1] < es[k] else (-1 if es[k + 1] > es[k] else 0)
                for k in range(3)]
        revs = sum(1 for k in range(2)
                   if dirs[k] != 0 and dirs[k + 1] != 0 and dirs[k] != dirs[k + 1])
        c['sawtooth'] = revs >= 2
    nunstable = sum(1 for c in cases if c['unstable'])
    nsaw = sum(1 for c in cases if c['sawtooth'])
    # sign agreement: cases with |relative pitch deviation| > 1%
    sa_n = sa_ok = 0
    for c, t in zip(cases, tgts):
        m_ref = measure(t['ref'])
        m_r0 = measure(os.path.join(outdir, os.path.basename(t['iters'][0]['render'])))
        fr, fn = m_ref['f0'], m_r0['f0']
        if fr >= 125 and fn > 0:
            need = (fr - fn) / fr
            if abs(need) > 0.01:
                sa_n += 1
                planned = c['dev0_df0'] / 1000.0  # mHz -> Hz
                if (planned > 0) == (need > 0) and planned != 0:
                    sa_ok += 1
    out = {'n': n, 'mean_err_ratio': mean_ratio,
           'wilcoxon_p': p_w, 'wilcoxon_Wplus': w_obs, 'wilcoxon_n': nn,
           'strictly_improved': improved,
           'unstable_cases': nunstable, 'sawtooth_cases': nsaw,
           'sign_agree_n': sa_n,
           'sign_agree_rate': sa_ok / sa_n if sa_n else 0.0,
           'cases': [{'depth': c['depth'], 'f0_ref': round(c['f0_ref'], 1),
                      'errs': [round(e, 4) for e in c['errs']],
                      'unstable': c['unstable'], 'sawtooth': c['sawtooth']}
                     for c in cases]}
    return out


def main():
    cmd = sys.argv[1]
    if cmd == 'score':
        journal, outdir, axis = sys.argv[2], sys.argv[3], sys.argv[4]
        lo, hi = {'pitch': (1, 41), 'env': (41, 81), 'pros': (81, 121)}[axis]
        print(json.dumps(score_axis(journal, outdir, axis, lo=lo, hi=hi), indent=1))
    elif cmd == 'rc1':
        journal, outdir, axis = sys.argv[2], sys.argv[3], sys.argv[4]
        lo, hi = {'pitch': (1, 41), 'env': (41, 81), 'pros': (81, 121)}[axis]
        print(json.dumps(score_axis(journal, outdir, axis, derange=True, lo=lo, hi=hi), indent=1))
    elif cmd == 'rc0':
        jw, dw, js, ds, axis = sys.argv[2:7]
        lo, hi = {'pitch': (1, 41), 'env': (41, 81), 'pros': (81, 121)}[axis]
        rw = score_axis(jw, dw, axis, lo=lo, hi=hi)
        rs = score_axis(js, ds, axis, lo=lo, hi=hi)
        hw = [1 if i in rw['hit_idx'] else 0 for i in range(rw['n'])]
        hs = [1 if i in rs['hit_idx'] else 0 for i in range(rs['n'])]
        p, obs = perm_p(hw, hs)
        print(json.dumps({'axis': axis, 'wired': rw, 'severed': rs,
                          'perm_p': p, 'obs_diff': obs}, indent=1))
    elif cmd == 'loop':
        journal, outdir = sys.argv[2], sys.argv[3]
        print(json.dumps(score_loop(journal, outdir), indent=1))


if __name__ == '__main__':
    main()
