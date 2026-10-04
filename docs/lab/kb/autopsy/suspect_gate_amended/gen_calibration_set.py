"""Generate calibration_set.json: the exact calibration examples + provenance
that trained the perturbation-truth channel (frozen SS1.4).

For every calibration adversarial fixture: (sense, stim, task),
truth_preserved = [truth_adv == truth_primary]. p_c per class is the
mean of truth_preserved over these fixtures (senses pooled); see
channel_table.json for the aggregated table and build_channel.py for
the aggregation code. No test truth is touched.
"""
import json

RERUN = '/home/hatch/workspace/tnn-lab/prose-learning/epistemic_wave/kb4_rerun'
AUTO = '/home/hatch/workspace/tnn-lab/kb/autopsy'
TASKS = ['colordisc', 'colorconst', 'shapetrans', 'pitchdisc', 'timbredisc', 'motiondir']

truth = json.load(open(RERUN + '/truth.json'))
manifest = json.load(open(AUTO + '/SPLIT_MANIFEST.json'))
cal = {t: set(manifest['calibration'][t]) for t in TASKS}

prim_truth = {}
for k, v in truth.items():
    if v['variant'] == 'primary':
        prim_truth[(k.split('/')[0], v['stim_idx'])] = v['truth']

fixtures = []
for k, v in sorted(truth.items()):
    if v['variant'] != 'adversarial':
        continue
    tag, s, task = k.split('/')[0], v['stim_idx'], v['task']
    if s not in cal[task]:
        continue
    fixtures.append({
        'sense': tag, 'stim': s, 'task': task,
        'truth_primary': prim_truth[(tag, s)],
        'truth_adversarial': v['truth'],
        'truth_preserved': v['truth'] == prim_truth[(tag, s)],
    })

per_class = {}
for t in TASKS:
    cf = [f for f in fixtures if f['task'] == t]
    per_class[t] = {
        'n': len(cf),
        'preserved': sum(1 for f in cf if f['truth_preserved']),
    }

out = {
    'frozen_prereg': 'kb/autopsy/PREREG_FROZEN_SUSPECT_GATE.md',
    'source': 'truth.json (calibration split per SPLIT_MANIFEST.json); test truth never touched',
    'n_calibration_fixtures': len(fixtures),
    'per_class': per_class,
    'fixtures': fixtures,
}
json.dump(out, open('/home/hatch/workspace/scratch_suspect1/build_v2/calibration_set.json', 'w'), indent=1)
print('fixtures:', len(fixtures))
print('per_class:', json.dumps(per_class))
