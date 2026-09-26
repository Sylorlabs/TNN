#!/usr/bin/env python3
"""Run the Crew P battery: organ on all questions, 3x, byte-identity check.

Usage: run_battery.py <organ_bin> <test_wavs_dir> <out_dir> <run_tag>
Logs every argv. Writes answers_<tag>.json + runlog_<tag>.txt.
"""
import json, os, subprocess, sys, hashlib

ORGAN, WAVDIR, OUTDIR, TAG = sys.argv[1:5]
os.makedirs(OUTDIR, exist_ok=True)

man = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  'manifest_p.json')))
VOID = set(json.load(open(os.path.join(OUTDIR, 'void_qids.json')))
           if os.path.exists(os.path.join(OUTDIR, 'void_qids.json')) else [])

def run_organ(qtype, qid, *wavs):
    argv = [ORGAN, '%s:%s' % (qtype, qid)] + list(wavs)
    p = subprocess.run(argv, capture_output=True, text=True, timeout=300)
    return p.stdout.strip(), ' '.join(argv)

results = {}
log = []
n = 0
for name, qs in man['batteries'].items():
    for q in qs:
        qid = q['qid'].split(':')[1]
        if q['qid'] in VOID:
            continue
        if name in ('pitchrel', 'rhy', 'hf'):
            a = os.path.join(WAVDIR, q['qid'] + '_A.wav')
            b = os.path.join(WAVDIR, q['qid'] + '_B.wav')
            ans, argv = run_organ(name, qid, a, b)
        else:
            a = os.path.join(WAVDIR, q['qid'] + '.wav')
            ans, argv = run_organ(name, qid, a)
        results[q['qid']] = dict(answer=ans, label=str(q['label']),
                                 hit=1 if ans == str(q['label']) else 0)
        log.append(argv + ' -> ' + ans)
        n += 1
        if n % 50 == 0:
            print('%d/%d' % (n, sum(len(v) for v in man['batteries'].values())), flush=True)

# P-R5 (diagnostic, pitch pairs)
for q in man['pr5']:
    qid = q['qid'].split(':')[1]
    a = os.path.join(WAVDIR, q['qid'] + '_A.wav')
    b = os.path.join(WAVDIR, q['qid'] + '_B.wav')
    ans, argv = run_organ('pr5', qid, a, b)
    results[q['qid']] = dict(answer=ans, label=str(q['label']),
                             hit=1 if ans == str(q['label']) else 0)
    log.append(argv + ' -> ' + ans)

# P-R4 (diagnostic, 3-bit)
for q in man['pr4']:
    qid = q['qid'].split(':')[1]
    a = os.path.join(WAVDIR, q['qid'] + '.wav')
    ans, argv = run_organ('pr4', qid, a)
    lab = q['label']
    agree = sum(1 for x, y in zip(ans, lab) if x == y) / 3.0 if len(ans) == 3 else 0.0
    results[q['qid']] = dict(answer=ans, label=lab, agree=agree)
    log.append(argv + ' -> ' + ans)

json.dump(results, open(os.path.join(OUTDIR, 'answers_%s.json' % TAG), 'w'), indent=1)
open(os.path.join(OUTDIR, 'runlog_%s.txt' % TAG), 'w').write('\n'.join(log) + '\n')
# hash answers
h = hashlib.sha256(open(os.path.join(OUTDIR, 'answers_%s.json' % TAG), 'rb').read()).hexdigest()
print('TAG', TAG, 'n=', len(results), 'sha256=', h)
# summary per battery
for name, qs in man['batteries'].items():
    hits = sum(results[q['qid']]['hit'] for q in qs if q['qid'] in results)
    tot = sum(1 for q in qs if q['qid'] in results)
    print('%s: %d/%d' % (name, hits, tot))
