#!/usr/bin/env python3
"""analyze.py — Phase B2b analysis driver (PREREG_LH §2b/§2c).

Runs the frozen scorer over finished run dirs and emits:
  - control hit rates per axis (r1/r2/r3), byte-identity check across reruns
  - RC0 permutation tests, RC1 deranged scores
  - closed-loop battery stats (loop + loopfresh)
  - depth curve (bands + paired early-vs-deep repeats)
Outputs JSON to stdout; writes markdown tables to the given outdir.
"""
import hashlib, json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from scorer_ctrl import (score_axis, perm_p, score_loop, HITFN, measure,
                         DERANGE_SHIFT)


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()


def wav_manifest(d):
    m = {}
    for fn in sorted(os.listdir(d)):
        if fn.endswith('.wav'):
            m[fn] = sha256_file(os.path.join(d, fn))
    return m


def main():
    base = sys.argv[1]          # trials_control dir
    outdir = sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    R = lambda *a: os.path.join(base, 'runs', *a)

    res = {'scorer_derange': DERANGE_SHIFT}

    # ---- control: r1/r2/r3 ----
    for run in ['r1', 'r2', 'r3']:
        j, d = R(run, 'journal.txt'), R(run)
        res[run] = {ax: score_axis(j, d, ax,
                                  lo=lo, hi=hi)
                    for ax, lo, hi in [('pitch', 1, 41), ('env', 41, 81),
                                       ('pros', 81, 121)]}
        res[run]['journal_sha'] = sha256_file(j)
        res[run]['wav_manifest'] = wav_manifest(d)

    # byte-identity across reruns
    man1 = res['r1']['wav_manifest']
    res['rerun_identity'] = {
        'journal_identical_r1r2': res['r1']['journal_sha'] == res['r2']['journal_sha'],
        'journal_identical_r1r3': res['r1']['journal_sha'] == res['r3']['journal_sha'],
        'wav_identical_r1r2': man1 == res['r2']['wav_manifest'],
        'wav_identical_r1r3': man1 == res['r3']['wav_manifest'],
        'n_wavs': len(man1),
    }

    # ---- RC0 ----
    rc0 = {}
    for ax, lo, hi in [('pitch', 1, 41), ('env', 41, 81), ('pros', 81, 121)]:
        rw = score_axis(R('r1', 'journal.txt'), R('r1'), ax, lo=lo, hi=hi)
        rs = score_axis(R('rc0', 'journal.txt'), R('rc0'), ax, lo=lo, hi=hi)
        hw = [1 if i in rw['hit_idx'] else 0 for i in range(rw['n'])]
        hs = [1 if i in rs['hit_idx'] else 0 for i in range(rs['n'])]
        p, obs = perm_p(hw, hs)
        rc0[ax] = {'wired_hits': rw['hits'], 'severed_hits': rs['hits'],
                   'n': rw['n'], 'perm_p': p, 'obs_diff': obs}
    res['rc0'] = rc0

    # ---- RC1 (deranged, on r1) ----
    res['rc1'] = {ax: score_axis(R('r1', 'journal.txt'), R('r1'), ax,
                                derange=True, lo=lo, hi=hi)
                  for ax, lo, hi in [('pitch', 1, 41), ('env', 41, 81),
                                      ('pros', 81, 121)]}

    # ---- closed loop ----
    res['loop_deep'] = score_loop(R('r1', 'journal.txt'), R('r1'))
    res['loop_fresh'] = score_loop(R('loopfresh', 'journal.txt'), R('loopfresh'))

    # ---- depth curve: control hit rate by depth band (r1) ----
    depth_curve = {}
    for ax, lo, hi in [('pitch', 1, 41), ('env', 41, 81), ('pros', 81, 121)]:
        s = score_axis(R('r1', 'journal.txt'), R('r1'), ax, lo=lo, hi=hi)
        hits = set(s['hit_idx'])
        bands = {}
        for b0 in range(0, 40, 10):
            idxs = list(range(b0, b0 + 10))
            h = sum(1 for i in idxs if i in hits)
            bands[f'{lo + b0}-{lo + b0 + 9}'] = {'hits': h, 'n': 10}
        depth_curve[ax] = bands
    res['depth_curve'] = depth_curve

    # ---- paired early-vs-deep pitch repeats (idx 0-19 vs 140-159) ----
    j, d = R('r1', 'journal.txt'), R('r1')
    early = score_axis(j, d, 'pitch', lo=0, hi=20)
    ds = score_axis(j, d, 'pitch', lo=140, hi=160)
    eh = set(early['hit_idx'])
    dh = set(ds['hit_idx'])
    res['paired_repeat'] = {
        'early_hits': early['hits'], 'deep_hits': ds['hits'], 'n': 20,
        'both_hit': len(eh & dh), 'early_only': len(eh - dh),
        'deep_only': len(dh - eh), 'neither': 20 - len(eh | dh),
    }

    with open(os.path.join(outdir, 'analysis.json'), 'w') as f:
        json.dump(res, f, indent=1)
    print(json.dumps({k: v for k, v in res.items()
                      if k not in ('r1', 'r2', 'r3')}, indent=1)[:4000])


if __name__ == '__main__':
    main()
