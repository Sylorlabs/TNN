#!/usr/bin/env python3
# pr4_noregress.py — OFFLINE scorer for the P-R4 no-regression re-run.
# Runs the wiring-built frozen organ binary on the 40 P-R4 held-out real
# clips (crew_p manifest), 3 consecutive passes; checks byte-identical
# answers across passes and agreement vs the frozen analyzer labels.
# Baseline (frozen, principles): 0.783. Prereg §4 FIXED bar: within ±0.01.
import json, subprocess, sys, os

ORGAN = os.path.expanduser('~/workspace/audio_longhorizon/wiring/build/organ_frozen')
WAVDIR = os.path.expanduser('~/workspace/audio_principles/crew_p/test_wavs')
MAN = json.load(open(os.path.expanduser('~/workspace/audio_principles/crew_p/manifest_p.json')))
PR4 = MAN['pr4']

def run_once():
    ans = {}
    for q in PR4:
        qid = q['qid']                      # 'pr4:NNNN'
        short = qid.split(':')[1]
        wav = os.path.join(WAVDIR, qid + '.wav')
        p = subprocess.run([ORGAN, 'pr4:' + short, wav], capture_output=True, text=True, timeout=300)
        ans[qid] = p.stdout.strip()
    return ans

passes = []
for i in range(3):
    passes.append(run_once())
    print('pass %d done' % (i + 1), flush=True)

a0, a1, a2 = passes
det = a0 == a1 == a2
agree_sum = 0.0
for q in PR4:
    qid = q['qid']
    lab = q['label']
    a = a0[qid]
    agree_sum += sum(1 for x, y in zip(a, lab) if x == y) / 3.0 if len(a) == 3 else 0.0
agree = agree_sum / len(PR4)
print('byte-identical across 3 passes:', det)
print('P-R4 agreement: %.4f (n=%d)' % (agree, len(PR4)))
print('within +-0.01 of frozen baseline 0.783:', abs(agree - 0.783) <= 0.01)
json.dump({'pass1': a0, 'byte_identical': det, 'agreement': agree}, open('pr4_noregress.json', 'w'), indent=1)
