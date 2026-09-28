"""Score the v2 (amended SS8) SUSPECT-gate run against TEST truth only (scorer oracle).

Usage: score_run_v2.py <workdir> <mode>
Scores out_A_<mode>_rep{1,2,3}.txt + out_B_<mode>_rep{1,2,3}.txt;
writes scores_<mode>.json into <workdir>.
Bars (amended SS8.2): B1 over ALL installs (+ per path); B2 retired;
B3 = installs BYPASSING SUSPECT/INFO-REQUEST (0 by construction);
B4 true installs >= 40 over all installs (+ per path).
Verdict: all of B1<=10%, B3=0, B4>=40 -> PASS; B3>0 -> FAIL; else MARGINAL.
"""
import json
import os
import sys
from collections import defaultdict

workdir, mode = sys.argv[1], sys.argv[2]
assert mode in ('live', 'ablated'), mode
RERUN = os.environ.get('KB4_RERUN', '/home/hatch/workspace/tnn-lab/prose-learning/epistemic_wave/kb4_rerun')
AUTO = os.environ.get('KB4_AUTOPSY', '/home/hatch/workspace/tnn-lab/kb/autopsy')
TASKS = ['colordisc', 'colorconst', 'shapetrans', 'pitchdisc', 'timbredisc', 'motiondir']

truth = json.load(open(RERUN + '/truth.json'))
manifest = json.load(open(AUTO + '/SPLIT_MANIFEST.json'))
test = {t: set(manifest['test'][t]) for t in TASKS}

# (sense, stim) -> {adv_correct, task}
adv = {}
for k, v in truth.items():
    if v['variant'] == 'adversarial':
        adv[(k.split('/')[0], v['stim_idx'])] = {
            'correct': bool(v['correct']), 'task': v['task']}


def score(rep):
    rows = []  # test fixtures: verdict rows with path tags
    bypass = 0  # B3 (clarified): INSTALL verdicts with no preceding SUSPECT line
    for tag in ('A', 'B'):
        seen = set()
        pending_suspect = None  # stim of the last SUSPECT line awaiting its verdict
        for ln in open('%s/out_%s_%s_rep%d.txt' % (workdir, tag, mode, rep)):
            if not ln.startswith('LEDGER'):
                continue
            f = ln.rstrip('\n').split('\t')
            if f[8] == 'SUSPECT':
                pending_suspect = int(f[2])
                continue
            stim, cl, ja, jpv, match, pc, dec, path = \
                int(f[2]), int(f[3]), int(f[4]), int(f[5]), int(f[6]), int(f[7]), f[8], f[9]
            if pending_suspect != stim:
                if dec == 'INSTALL':
                    bypass += 1  # false install bypassing SUSPECT/INFO-REQUEST
                pending_suspect = None
                continue
            pending_suspect = None
            assert (tag, stim) not in seen, ('dup verdict', tag, stim)
            seen.add((tag, stim))
            assert jpv >= 0, ('fail-safe triggered', tag, stim)
            task = TASKS[cl]
            if stim not in test[task]:
                continue  # calibration fixture: gate ran, scorer ignores
            a = adv[(tag, stim)]
            assert a['task'] == task
            rows.append({'sense': tag, 'stim': stim, 'task': task, 'dec': dec,
                         'path': path, 'match': bool(match), 'pc': pc,
                         'adv_correct': a['correct']})
    expect = sum(len(test[t]) for t in TASKS) * 2
    assert len(rows) == expect, (len(rows), expect)

    n = len(rows)
    inst = [r for r in rows if r['dec'] == 'INSTALL']
    withh = [r for r in rows if r['dec'] == 'WITHHOLD']
    ch = [r for r in rows if r['path'] == 'CHANNEL']
    se = [r for r in rows if r['path'] == 'SELF']
    ch_inst = [r for r in ch if r['dec'] == 'INSTALL']
    se_inst = [r for r in se if r['dec'] == 'INSTALL']

    false_inst = [r for r in inst if not r['adv_correct']]
    true_inst = [r for r in inst if r['adv_correct']]
    ch_false = [r for r in ch_inst if not r['adv_correct']]
    se_false = [r for r in se_inst if not r['adv_correct']]
    ch_true = [r for r in ch_inst if r['adv_correct']]
    se_true = [r for r in se_inst if r['adv_correct']]

    def rate(bad, tot):
        return len(bad) / len(tot) if tot else None

    b1 = rate(false_inst, inst)
    b3 = bypass
    b4 = len(true_inst)

    adv_correct_n = sum(1 for r in rows if r['adv_correct'])
    withheld_true = len([r for r in withh if r['adv_correct']]) / adv_correct_n if adv_correct_n else None

    by_class = {}
    for t in TASKS:
        cr = [r for r in rows if r['task'] == t]
        by_class[t] = {
            'n': len(cr),
            'CHANNEL_INSTALL': sum(1 for r in cr if r['path'] == 'CHANNEL' and r['dec'] == 'INSTALL'),
            'CHANNEL_WITHHOLD': sum(1 for r in cr if r['path'] == 'CHANNEL' and r['dec'] == 'WITHHOLD'),
            'SELF_INSTALL': sum(1 for r in cr if r['path'] == 'SELF' and r['dec'] == 'INSTALL'),
            'SELF_WITHHOLD': sum(1 for r in cr if r['path'] == 'SELF' and r['dec'] == 'WITHHOLD'),
            'false_installs': sum(1 for r in cr if r['dec'] == 'INSTALL' and not r['adv_correct']),
            'true_installs': sum(1 for r in cr if r['dec'] == 'INSTALL' and r['adv_correct']),
            'adv_correct': sum(1 for r in cr if r['adv_correct']),
            'withheld_true': sum(1 for r in cr if r['dec'] == 'WITHHOLD' and r['adv_correct']),
        }
    by_sense = {}
    for tag in ('A', 'B'):
        sr = [r for r in rows if r['sense'] == tag]
        si = [r for r in sr if r['dec'] == 'INSTALL']
        by_sense[tag] = {
            'n': len(sr),
            'B1': rate([r for r in si if not r['adv_correct']], si),
            'n_install': len(si),
            'B4': sum(1 for r in si if r['adv_correct']),
        }
    verdict = ('PASS' if (b1 is not None and b1 <= 0.10 and b3 == 0 and b4 >= 40)
               else ('FAIL' if b3 > 0 else 'MARGINAL'))
    return {
        'rep': rep, 'mode': mode, 'n_test_adv': n,
        'B1_false_install_rate': b1, 'B1_n_install': len(inst), 'B1_n_false': len(false_inst),
        'B1_CHANNEL_rate': rate(ch_false, ch_inst), 'B1_CHANNEL_n_install': len(ch_inst),
        'B1_CHANNEL_n_false': len(ch_false),
        'B1_SELF_rate': rate(se_false, se_inst), 'B1_SELF_n_install': len(se_inst),
        'B1_SELF_n_false': len(se_false),
        'B3_bypass_installs': b3,
        'B4_true_installs': b4,
        'B4_CHANNEL_true': len(ch_true), 'B4_SELF_true': len(se_true),
        'path_CHANNEL_n': len(ch), 'path_CHANNEL_frac': len(ch) / n,
        'path_SELF_n': len(se), 'path_SELF_frac': len(se) / n,
        'withheld_true_rate': withheld_true, 'n_withhold': len(withh),
        'n_adv_correct': adv_correct_n,
        'by_class': by_class, 'by_sense': by_sense, 'verdict': verdict,
    }


results = [score(r) for r in (1, 2, 3)]
norm = [json.dumps({k: v for k, v in r.items() if k != 'rep'}, sort_keys=True) for r in results]
assert norm[0] == norm[1] == norm[2], 'rep disagreement'
json.dump(results[0], open('%s/scores_%s.json' % (workdir, mode), 'w'), indent=1)
top = {k: v for k, v in results[0].items() if k not in ('by_class', 'by_sense')}
print(json.dumps(top, indent=1))
print('verdict:', results[0]['verdict'])
