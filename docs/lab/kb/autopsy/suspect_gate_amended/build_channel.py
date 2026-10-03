"""Build the perturbation-truth channel table from CALIBRATION truth only.

Estimand (frozen): truth_preserved(s) = 1 iff ground-truth judgment for the
adversarial variant == ground-truth judgment for the primary variant of s.
p_c = mean over CALIBRATION adversarial fixtures of class c, pooling senses.
Table stores per-mille integers; build-time check: no exact rational
disagrees with its per-mille rounding on the tau_hi=0.9 / tau_lo=0.1
threshold comparisons.
"""
import json

RERUN = '/home/hatch/workspace/tnn-lab/prose-learning/epistemic_wave/kb4_rerun'
AUTO = '/home/hatch/workspace/tnn-lab/kb/autopsy'
OUT = '/home/hatch/workspace/scratch_suspect1/build'
TASKS = ['colordisc', 'colorconst', 'shapetrans', 'pitchdisc', 'timbredisc', 'motiondir']

truth = json.load(open(RERUN + '/truth.json'))
manifest = json.load(open(AUTO + '/SPLIT_MANIFEST.json'))
cal = {t: set(manifest['calibration'][t]) for t in TASKS}

# primary truth per (sense, stim)
prim_truth = {}
for k, v in truth.items():
    if v['variant'] == 'primary':
        tag = k.split('/')[0]
        prim_truth[(tag, v['stim_idx'])] = v['truth']

per_class = {t: [0, 0] for t in TASKS}  # [preserved, total]
used = []
for k, v in truth.items():
    if v['variant'] != 'adversarial':
        continue
    tag = k.split('/')[0]
    s, task = v['stim_idx'], v['task']
    if s not in cal[task]:
        continue
    pt = prim_truth[(tag, s)]
    pres = 1 if v['truth'] == pt else 0
    per_class[task][0] += pres
    per_class[task][1] += 1
    used.append({'sense': tag, 'stim': s, 'task': task,
                 'truth_adv': v['truth'], 'truth_primary': pt,
                 'preserved': pres})

table = {}
disagree = []
for i, t in enumerate(TASKS):
    pres, tot = per_class[t]
    assert tot > 0, t
    permille = int(round(1000.0 * pres / tot))
    # exact-rational vs per-mille agreement on threshold comparisons
    exact_hi = (pres * 10 >= tot * 9)
    exact_lo = (pres * 10 <= tot * 1)
    q_hi = permille >= 900
    q_lo = permille <= 100
    if exact_hi != q_hi or exact_lo != q_lo:
        disagree.append(t)
    table[t] = {'class': i, 'preserved': pres, 'total': tot,
                'exact': '%d/%d' % (pres, tot), 'permille': permille,
                'exact_ge_0.9': exact_hi, 'exact_le_0.1': exact_lo}

assert not disagree, ('quantization disagreement on %s -> freeze amendment required' % disagree)

with open(OUT + '/channel.txt', 'w') as f:
    for t in TASKS:
        f.write('%d %d\n' % (table[t]['class'], table[t]['permille']))

doc = {
    'frozen_prereg': 'kb/autopsy/PREREG_FROZEN_SUSPECT_GATE.md',
    'estimand': 'truth_preserved(s) = [truth_adv == truth_primary]; p_c = mean over calibration adversarial fixtures, senses pooled',
    'calibration_source': 'SPLIT_MANIFEST.json calibration split (human-verification stand-in); test truth never touched',
    'n_calibration_fixtures': len(used),
    'quantization_check': 'no exact-rational vs per-mille disagreement on tau comparisons',
    'classes': table,
}
with open(OUT + '/channel_table.json', 'w') as f:
    json.dump(doc, f, indent=1)

print('per-class P(truth preserved | class) [calibration only]:')
for t in TASKS:
    d = table[t]
    print('  %-10s class=%d  %s = %.4f  permille=%d' % (t, d['class'], d['exact'], d['preserved'] / d['total'], d['permille']))
print('quantization check: CLEAN (no threshold disagreement)')
