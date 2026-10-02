#!/usr/bin/env python3
"""Scorer sanity floor: frozen scorer must agree >=95% with manifest labels.

Run AFTER test WAVs exist, BEFORE the organ battery.
Writes void_qids.json (questions to void) and sanity_report.json.
A question is void if the scorer disagrees with the manifest label.
Per-question rule: void if scorer != label. (The >=95% is per-question-type
in the prereg; we void individual disagreements and report the rate.)
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scorer_p import features, DISPATCH

HERE = os.path.dirname(os.path.abspath(__file__))
WAVDIR = os.path.join(HERE, 'test_wavs')
OUTDIR = os.path.join(HERE, 'evidence')

man = json.load(open(os.path.join(HERE, 'manifest_p.json')))
os.makedirs(OUTDIR, exist_ok=True)

void = []
report = {}
for name, qs in man['batteries'].items():
    agree = 0
    total = 0
    for q in qs:
        qid = q['qid']
        if name in ('pitchrel', 'rhy', 'hf'):
            fa = features(os.path.join(WAVDIR, qid + '_A.wav'))
            fb = features(os.path.join(WAVDIR, qid + '_B.wav'))
            ans = DISPATCH[name](fa, fb)
        else:
            fa = features(os.path.join(WAVDIR, qid + '.wav'))
            ans = DISPATCH[name](fa)
        ok = (str(ans) == str(q['label']))
        agree += ok
        total += 1
        if not ok:
            void.append(qid)
    report[name] = dict(agree=agree, total=total, rate=agree / total)
    print('%s: scorer agreement %d/%d = %.3f' % (name, agree, total, agree / total))

json.dump(void, open(os.path.join(OUTDIR, 'void_qids.json'), 'w'))
json.dump(report, open(os.path.join(OUTDIR, 'sanity_report.json'), 'w'), indent=1)
print('void:', len(void))
