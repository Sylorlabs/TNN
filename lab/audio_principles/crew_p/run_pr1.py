#!/usr/bin/env python3
"""P-R1: run organ on +1dB perturbed clips. If a PASSED subtest drops below
chance on perturbed, its pass is void."""
import json, os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ORGAN = os.path.join(HERE, 'organ')
WAVDIR = os.path.join(HERE, 'test_wavs_pert')
OUTDIR = os.path.join(HERE, 'evidence')

man = json.load(open(os.path.join(HERE, 'manifest_p.json')))
chance = {'pitchrel': 0.5, 'pitchabs': 1/24, 'env': 1/3, 'rhy': 0.5}

def run_organ(qtype, qid, *wavs):
    argv = [ORGAN, '%s:%s' % (qtype, qid)] + list(wavs)
    p = subprocess.run(argv, capture_output=True, text=True, timeout=300)
    return p.stdout.strip()

res = {}
for name, qids in man['pr1']['qids'].items():
    hits = 0
    for qid in qids:
        qn = qid.split(':')[1]
        # find label
        lab = None
        for q in man['batteries'][name]:
            if q['qid'] == qid:
                lab = str(q['label'])
                break
        if name in ('pitchrel', 'rhy'):
            wavs = [os.path.join(WAVDIR, qid + '_A.wav'), os.path.join(WAVDIR, qid + '_B.wav')]
        else:
            wavs = [os.path.join(WAVDIR, qid + '.wav')]
        ans = run_organ(name, qn, *wavs)
        if ans == lab:
            hits += 1
    n = len(qids)
    ch = chance[name]
    below = hits < ch * n
    res[name] = dict(hits=hits, total=n, chance=ch, below_chance=below)
    print('%s +1dB: %d/%d (chance %.3f) %s' % (name, hits, n, ch,
          'BELOW CHANCE - VOID' if below else 'ok'))
json.dump(res, open(os.path.join(OUTDIR, 'pr1_report.json'), 'w'), indent=1)
