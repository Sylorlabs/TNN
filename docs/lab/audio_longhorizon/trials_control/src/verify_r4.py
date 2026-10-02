#!/usr/bin/env python3
"""verify_r4.py — 3x byte-identity verification for the r4 rerun.

Checks:
  1. r4 complete: done.txt present, 160 TARGETs in journal, 220 WAVs.
  2. Canonical journal SHA == r1 canonical (5f8c19f9fb8de908...).
  3. WAV manifest (basename->sha256) == r1 manifest, zero mismatches.
  4. Control axes score identically to r1 (pitch 28/39? no: 28/40, env 39/40, pros 29/40).
Writes evidence/rerun_identity_r1r3r4.json. Prints PASS/FAIL lines.
"""
import hashlib, json, os, re, sys

BASE = '/home/hatch/workspace/audio_longhorizon/trials_control'
os.chdir(BASE)
sys.path.insert(0, 'src')


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()


def canon(path):
    out = []
    for ln in open(path):
        out.append(re.sub(r'RENDERED runs/[^/]+/', 'RENDERED runs/RUN/', ln))
    return hashlib.sha256(''.join(out).encode()).hexdigest()


def wavman(d):
    return {fn: sha(os.path.join(d, fn))
            for fn in sorted(os.listdir(d)) if fn.endswith('.wav')}


def main():
    ok = True
    # 1. completeness
    done = os.path.exists('runs/r4/done.txt')
    tgts = sum(1 for ln in open('runs/r4/journal.txt') if ln.startswith('TARGET '))
    wavs = wavman('runs/r4')
    print('done.txt:', done, '| targets:', tgts, '| wavs:', len(wavs))
    if not (done and tgts == 160 and len(wavs) == 220):
        print('FAIL: r4 incomplete'); return 1
    # 2. canonical journal identity
    c1 = canon('runs/r1/journal.txt'); c4 = canon('runs/r4/journal.txt')
    print('canonical r1:', c1[:16], 'r4:', c4[:16], 'identical:', c1 == c4)
    ok &= (c1 == c4)
    # 3. WAV manifest identity
    m1 = wavman('runs/r1'); m4 = wavs
    only1 = sorted(set(m1) - set(m4)); only4 = sorted(set(m4) - set(m1))
    mm = sorted(f for f in set(m1) & set(m4) if m1[f] != m4[f])
    print('wav identical:', not only1 and not only4 and not mm,
          '| only_r1:', len(only1), '| only_r4:', len(only4),
          '| sha_mismatch:', len(mm))
    ok &= not (only1 or only4 or mm)
    # 4. control axes score identically
    from scorer_ctrl import score_axis
    exp = {'pitch': (1, 41, 28), 'env': (41, 81, 39), 'pros': (81, 121, 29)}
    for ax, (lo, hi, eh) in exp.items():
        s = score_axis('runs/r4/journal.txt', 'runs/r4', ax, lo=lo, hi=hi)
        match = (s['hits'] == eh and s['n'] == 40)
        print(f'{ax}: {s["hits"]}/40 (expect {eh})', 'MATCH' if match else 'MISMATCH')
        ok &= match
    res = {'r4_complete': True, 'n_targets': tgts, 'n_wavs': len(wavs),
           'journal_canonical_sha': c4,
           'canonical_identical_r1r4': c1 == c4,
           'wav_identical_r1r4': not (only1 or only4 or mm),
           'wav_sha_mismatches': mm,
           'wav_manifest': m4}
    with open('evidence/rerun_identity_r1r3r4.json', 'w') as f:
        json.dump(res, f, indent=1)
    print('3x IDENTITY:', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
