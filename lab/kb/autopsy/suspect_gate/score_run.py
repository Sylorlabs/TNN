"""Score the SUSPECT-gate run against TEST truth only (scorer oracle)."""
import json
from collections import defaultdict

RERUN = '/home/hatch/workspace/tnn-lab/prose-learning/epistemic_wave/kb4_rerun'
AUTO = '/home/hatch/workspace/tnn-lab/kb/autopsy'
BUILD = '/home/hatch/workspace/scratch_suspect1/build'
TASKS = ['colordisc', 'colorconst', 'shapetrans', 'pitchdisc', 'timbredisc', 'motiondir']

truth = json.load(open(RERUN + '/truth.json'))
manifest = json.load(open(AUTO + '/SPLIT_MANIFEST.json'))
test = {t: set(manifest['test'][t]) for t in TASKS}

# (sense, stim) -> {adv_correct, adv_judg}
adv = {}
for k, v in truth.items():
    if v['variant'] == 'adversarial':
        adv[(k.split('/')[0], v['stim_idx'])] = {
            'correct': bool(v['correct']), 'task': v['task'], 'judg': v['judgment']}

def score(rep):
    rows = []  # test fixtures: dict(sense, stim, task, dec, match, pc, adv_correct)
    per_sense = defaultdict(lambda: defaultdict(int))
    for tag in ('A', 'B'):
        seen = set()
        for ln in open('%s/out_%s_rep%d.txt' % (BUILD, tag, rep)):
            if not ln.startswith('LEDGER'):
                continue
            f = ln.rstrip('\n').split('\t')
            stim, cl, ja, jpv, match, pc, dec = \
                int(f[2]), int(f[3]), int(f[4]), int(f[5]), int(f[6]), int(f[7]), f[8]
            assert (tag, stim) not in seen, ('dup ledger', tag, stim)
            seen.add((tag, stim))
            assert jpv >= 0, ('fail-safe triggered', tag, stim)
            task = TASKS[cl]
            if stim not in test[task]:
                continue  # calibration fixture: gate ran, scorer ignores
            a = adv[(tag, stim)]
            assert a['task'] == task
            rows.append({'sense': tag, 'stim': stim, 'task': task, 'dec': dec,
                         'match': bool(match), 'pc': pc, 'adv_correct': a['correct']})
            per_sense[tag]['n'] += 1
            per_sense[tag][dec] += 1
    # every test adversarial fixture scored exactly once
    expect = sum(len(test[t]) for t in TASKS) * 2
    # A missing shapetrans stim 142 is calibration, so both senses have all 92
    assert len(rows) == expect, (len(rows), expect)

    n = len(rows)
    inst = [r for r in rows if r['dec'] == 'INSTALL']
    withh = [r for r in rows if r['dec'] == 'WITHHOLD']
    susp = [r for r in rows if r['dec'] == 'SUSPECT']
    false_inst = [r for r in inst if not r['adv_correct']]
    true_inst = [r for r in inst if r['adv_correct']]
    unverified = [r for r in inst if not (r['match'] and r['pc'] >= 900)]

    b1 = len(false_inst) / len(inst) if inst else None
    # B2: Bayes-optimal judgment-only action = INSTALL on match else WITHHOLD
    bayes_wrong = [r for r in susp
                   if (r['match'] and not r['adv_correct']) or (not r['match'] and r['adv_correct'])]
    b2 = len(bayes_wrong) / len(susp) if susp else None
    d_strict = len([r for r in susp if not r['match'] and r['adv_correct']]) / len(susp) if susp else None
    d_differ = len([r for r in susp if not r['match']]) / len(susp) if susp else None
    b3 = len(unverified)
    b4 = len(true_inst)

    adv_correct_n = sum(1 for r in rows if r['adv_correct'])
    withheld_true = len([r for r in withh if r['adv_correct']]) / adv_correct_n if adv_correct_n else None
    suspect_rate = len(susp) / n

    by_class = {}
    for t in TASKS:
        cr = [r for r in rows if r['task'] == t]
        ci = [r for r in cr if r['dec'] == 'INSTALL']
        cw = [r for r in cr if r['dec'] == 'WITHHOLD']
        cs = [r for r in cr if r['dec'] == 'SUSPECT']
        cc = sum(1 for r in cr if r['adv_correct'])
        by_class[t] = {
            'n': len(cr), 'INSTALL': len(ci), 'WITHHOLD': len(cw), 'SUSPECT': len(cs),
            'false_installs': sum(1 for r in ci if not r['adv_correct']),
            'true_installs': sum(1 for r in ci if r['adv_correct']),
            'adv_correct': cc,
            'withheld_true': sum(1 for r in cw if r['adv_correct']),
            'suspect_correct_abstain': sum(1 for r in cs if (r['match'] and not r['adv_correct']) or (not r['match'] and r['adv_correct'])),
        }
    by_sense = {}
    for tag in ('A', 'B'):
        sr = [r for r in rows if r['sense'] == tag]
        si = [r for r in sr if r['dec'] == 'INSTALL']
        ss = [r for r in sr if r['dec'] == 'SUSPECT']
        bw = [r for r in ss if (r['match'] and not r['adv_correct']) or (not r['match'] and r['adv_correct'])]
        by_sense[tag] = {
            'n': len(sr),
            'B1': (sum(1 for r in si if not r['adv_correct']) / len(si)) if si else None,
            'B2': (len(bw) / len(ss)) if ss else None,
            'B4': sum(1 for r in si if r['adv_correct']),
            'suspect_rate': len(ss) / len(sr),
        }
    verdict = ('PASS' if (b1 is not None and b1 <= 0.10 and b2 is not None and b2 >= 0.80
                          and b3 == 0 and b4 >= 40)
               else ('FAIL' if b3 > 0 else 'MARGINAL'))
    return {
        'rep': rep, 'n_test_adv': n,
        'B1_false_install_rate': b1, 'B1_n_install': len(inst), 'B1_n_false': len(false_inst),
        'B2_correct_abstention': b2, 'B2_n_suspect': len(susp),
        'B2_D_strict_parenthetical': d_strict, 'B2_D_differ_fraction': d_differ,
        'B3_unverified_installs': b3,
        'B4_true_installs': b4,
        'withheld_true_rate': withheld_true, 'n_withhold': len(withh),
        'n_adv_correct': adv_correct_n, 'suspect_rate': suspect_rate,
        'by_class': by_class, 'by_sense': by_sense, 'verdict': verdict,
    }

results = [score(r) for r in (1, 2, 3)]
# reps must agree exactly on all scored quantities (excluding the rep label)
norm = [json.dumps({k: v for k, v in r.items() if k != 'rep'}, sort_keys=True) for r in results]
assert norm[0] == norm[1] == norm[2], 'rep disagreement'
json.dump(results[0], open(BUILD + '/scores.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in results[0].items() if k not in ('by_class', 'by_sense')}, indent=1))
print('verdict:', results[0]['verdict'])
