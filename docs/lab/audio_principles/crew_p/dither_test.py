#!/usr/bin/env python3
"""Dither stability: x1.001 gain on 20 qids/subtest; require >=19/20 same answer.

Compares organ answer on original vs x1.001-dithered clip.
"""
import json, os, subprocess, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ORGAN = os.path.join(HERE, 'organ')
WAVDIR = os.path.join(HERE, 'test_wavs')
OUTDIR = os.path.join(HERE, 'evidence')

man = json.load(open(os.path.join(HERE, 'manifest_p.json')))
G = 1.001

def run_organ(qtype, qid, *wavs):
    argv = [ORGAN, '%s:%s' % (qtype, qid)] + list(wavs)
    p = subprocess.run(argv, capture_output=True, text=True, timeout=300)
    return p.stdout.strip()

def dithered(src, dst):
    w = wave.open(src, 'rb')
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64)
    params = w.getparams(); w.close()
    y = np.clip(np.round(x * G), -32768, 32767).astype(np.int16)
    ww = wave.open(dst, 'wb'); ww.setparams(params)
    ww.writeframes(y.tobytes()); ww.close()

os.makedirs('/tmp/dither_p', exist_ok=True)
res = {}
for name in ['pitchrel', 'pitchabs', 'env', 'rhy']:
    qids = man['dither'][name]
    stable = 0
    for qid in qids:
        qn = qid.split(':')[1]
        if name in ('pitchrel', 'rhy'):
            awavs = [os.path.join(WAVDIR, qid + '_A.wav'), os.path.join(WAVDIR, qid + '_B.wav')]
        else:
            awavs = [os.path.join(WAVDIR, qid + '.wav')]
        a0 = run_organ(name, qn, *awavs)
        dwavs = []
        for a in awavs:
            d = '/tmp/dither_p/' + os.path.basename(a)
            dithered(a, d)
            dwavs.append(d)
        a1 = run_organ(name, qn, *dwavs)
        if a0 == a1:
            stable += 1
        else:
            print('UNSTABLE', qid, a0, '->', a1)
    res[name] = dict(stable=stable, total=len(qids),
                     pass_=stable >= 19)
    print('%s: %d/%d stable %s' % (name, stable, len(qids),
                                   'PASS' if stable >= 19 else 'FAIL'))
json.dump(res, open(os.path.join(OUTDIR, 'dither_report.json'), 'w'), indent=1)
