#!/usr/bin/env python3
"""analyze_plan.py — score the unified planner/vocabulary closed-loop runs
with the FROZEN scorer (trials_control/src/scorer_ctrl.py). Produces the
B-F1 §2c battery table per run + rerun byte-identity check + VOCAB.md.
Usage: analyze_plan.py <runs_root>   (runs_root holds fresh/deep/fresh2/deep2)
"""
import json, os, sys, hashlib, re

sys.path.insert(0, '/home/hatch/workspace/audio_longhorizon/trials_control/src')
import scorer_ctrl as SC

ROOT = sys.argv[1]
RUNS = ['fresh', 'deep', 'fresh2', 'deep2']

def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()

def canonical_journal(p, rundir):
    # journals record the outdir in RENDERED lines; canonicalize to compare
    # deliberation content, not the run's own directory name.
    with open(p, 'rb') as f:
        data = f.read()
    tag = os.path.basename(rundir).encode()
    return data.replace(b'runs/' + tag + b'/', b'runs/RUN/')

results = {}
for r in RUNS:
    d = os.path.join(ROOT, r)
    j = os.path.join(d, 'journal.txt')
    if not os.path.exists(j):
        results[r] = {'missing': True}
        continue
    out = SC.score_loop(j, d)
    results[r] = {
        'n': out['n'],
        'err_ratio': out['mean_err_ratio'],
        'wilcoxon_p': out['wilcoxon_p'],
        'strictly_improved': out['strictly_improved'],
        'unstable': out['unstable_cases'],
        'sawtooth': out['sawtooth_cases'],
        'sign_agree_n': out['sign_agree_n'],
        'sign_agree_rate': out['sign_agree_rate'],
        'cases': out['cases'],
    }

# byte-identity: fresh vs fresh2, deep vs deep2 (journals + WAV SHAs)
identity = {}
for a, b in (('fresh', 'fresh2'), ('deep', 'deep2')):
    da, db = os.path.join(ROOT, a), os.path.join(ROOT, b)
    ja, jb = os.path.join(da, 'journal.txt'), os.path.join(db, 'journal.txt')
    if not (os.path.exists(ja) and os.path.exists(jb)):
        identity['%s_vs_%s' % (a, b)] = 'missing'
        continue
    jid = canonical_journal(ja, da) == canonical_journal(jb, db)
    wavs_a = sorted(f for f in os.listdir(da) if f.endswith('.wav'))
    wavs_b = sorted(f for f in os.listdir(db) if f.endswith('.wav'))
    wav_id = (wavs_a == wavs_b and
              all(sha(os.path.join(da, f)) == sha(os.path.join(db, f)) for f in wavs_a))
    identity['%s_vs_%s' % (a, b)] = {
        'journal_identical': jid,
        'n_wavs': len(wavs_a),
        'wavs_identical': wav_id,
    }

print(json.dumps({'runs': results, 'identity': identity}, indent=1))
evdir = os.path.join(ROOT, '..', 'evidence')
os.makedirs(evdir, exist_ok=True)
with open(os.path.join(evdir, 'analysis.json'), 'w') as f:
    json.dump({'runs': results, 'identity': identity}, f, indent=1)

# ---- verdict table ----
print()
print('| Run | ERR(3)/ERR(0) ≤0.80 | Wilcoxon p<0.01 | ≥16/20 improve | sign≥80% | unstable | sawtooth |')
for r in RUNS:
    x = results[r]
    if 'missing' in x:
        print('| %s | MISSING |' % r); continue
    print('| %s | %.3f %s | %.4g %s | %d/20 %s | %.1f%% %s | %d | %d |' % (
        r, x['err_ratio'], 'PASS' if x['err_ratio'] <= 0.80 else 'FAIL',
        x['wilcoxon_p'], 'PASS' if x['wilcoxon_p'] < 0.01 else 'FAIL',
        x['strictly_improved'], 'PASS' if x['strictly_improved'] >= 16 else 'FAIL',
        100 * x['sign_agree_rate'], 'PASS' if x['sign_agree_rate'] >= 0.80 else 'FAIL',
        x['unstable'], x['sawtooth']))
