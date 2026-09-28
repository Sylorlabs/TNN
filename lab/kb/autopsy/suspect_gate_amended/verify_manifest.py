"""Independently re-verify SPLIT_MANIFEST.json for the SUSPECT-gate trial.

truth.json holds more stimuli than this trial uses; the manifest's job is
to split the IN-TRIAL stimuli. Checks: (1) per task, calibration and test
are disjoint and both subsets of truth.json stimuli; (2) counts match the
frozen record (calibration 93, test 92 stimuli); (3) every adversarial
stimulus in the frozen batch files is covered by cal|test (per sense batch
uses the same task-level split); (4) SHA256 of the manifest file.
The byte-identical recomputation of the manifest was recorded 2026-09-22.

Writes manifest_verification.json.
"""
import hashlib
import json

AUTO = '/home/hatch/workspace/tnn-lab/kb/autopsy'
RERUN = '/home/hatch/workspace/tnn-lab/prose-learning/epistemic_wave/kb4_rerun'
OUT = '/home/hatch/workspace/scratch_suspect1/build_v2'
TASKS = ['colordisc', 'colorconst', 'shapetrans', 'pitchdisc', 'timbredisc', 'motiondir']

raw = open(AUTO + '/SPLIT_MANIFEST.json', 'rb').read()
manifest = json.loads(raw)
truth = json.load(open(RERUN + '/truth.json'))

in_truth = {}
for k, v in truth.items():
    in_truth.setdefault(v['task'], set()).add(v['stim_idx'])

cmap = {}
for ln in open(OUT + '/classmap.txt'):
    s, c = ln.split()
    cmap[int(s)] = int(c)

# adversarial stimuli per batch file (3rd block per segment)
def adv_stims(tag):
    batch = [[int(x) for x in ln.split('\t')]
             for ln in open(OUT + '/batch_%s.txt' % tag).read().splitlines()]
    seg = [[int(x) for x in ln.split()] for ln in open(OUT + '/segments_%s.txt' % tag)]
    spans = []
    for i, (t, start, np, nn) in enumerate(seg):
        end = seg[i + 1][1] if i + 1 < len(seg) else len(batch)
        spans.append((start, np, nn, end))
    out = set()
    for L, (stim, judg, conf, src) in enumerate(batch):
        start, np, nn, end = next(x for x in spans if x[0] <= L < x[3])
        if L - start >= np + nn:
            out.add(stim)
    return out

batch_adv = {tag: adv_stims(tag) for tag in ('A', 'B')}

res = {'sha256': hashlib.sha256(raw).hexdigest(), 'tasks': {}}
ok = True
for t in TASKS:
    cal = set(manifest['calibration'][t])
    tst = set(manifest['test'][t])
    task_ok = cal.isdisjoint(tst) and cal <= in_truth[t] and tst <= in_truth[t]
    ok = ok and task_ok
    res['tasks'][t] = {
        'n_calibration': len(cal), 'n_test': len(tst),
        'disjoint_and_subsets_of_truth': task_ok,
    }
n_cal = sum(v['n_calibration'] for v in res['tasks'].values())
n_test = sum(v['n_test'] for v in res['tasks'].values())
res['n_calibration_stimuli'] = n_cal
res['n_test_stimuli'] = n_test
res['frozen_record_match_93_92'] = (n_cal == 93 and n_test == 92)

# batch coverage: every adversarial stimulus in the frozen batches is in cal|test
cov_ok = True
for tag in ('A', 'B'):
    uncovered = [s for s in batch_adv[tag]
                 if s not in set(manifest['calibration'][TASKS[cmap[s]]]) | set(manifest['test'][TASKS[cmap[s]]])]
    cov_ok = cov_ok and not uncovered
    res['batch_%s_adv_stimuli' % tag] = len(batch_adv[tag])
    res['batch_%s_uncovered' % tag] = uncovered
res['batch_coverage'] = 'PASS' if cov_ok else 'FAIL'
res['byte_compare_note'] = ('independent recomputation of SPLIT_MANIFEST.json from '
                            'truth.json was byte-identical TRUE on 2026-09-22')
res['overall'] = 'PASS' if (ok and res['frozen_record_match_93_92'] and cov_ok) else 'FAIL'
json.dump(res, open(OUT + '/manifest_verification.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != 'tasks'}, indent=1))
