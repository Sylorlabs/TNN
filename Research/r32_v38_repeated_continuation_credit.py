from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

import joblib
import numpy as np

ROOT = Path('/mnt/data/r32_epistemic')
SEED = 38038
REPLICATES = 128
HORIZONS = [1, 2, 3, 5, 8, 12]
TRIALS = 12
MODES = ['balanced_no_unique','biased_no_unique','stable_weak','unstable_then_stable','replacement','reversal','costly_stable']
RESOURCE_COUNT = 5
EPISODES_PER_MODE_RESOURCE = 70

import sys
sys.path[:0] = ['/mnt/data/r31_part2', str(ROOT)]
import r31_sequential_evidence_abstention_REFERENCE_ONLY as r31
import r32_epistemic_r31_matched_v17_cached_REFERENCE_ONLY as v
import r32_v26_candidate_selected_conditional_advantage as world
import r32_v32_predictive_dynamics_population as v32
import r32_v37_regret_weighted_candidate_support as v37


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reconstruct_episode(eid: int, env):
    mi = eid // (RESOURCE_COUNT * EPISODES_PER_MODE_RESOURCE)
    rem = eid % (RESOURCE_COUNT * EPISODES_PER_MODE_RESOURCE)
    ri = rem // EPISODES_PER_MODE_RESOURCE
    j = rem % EPISODES_PER_MODE_RESOURCE
    epseed = 9714 * 4_000_000 + mi * 300_000 + ri * 50_000 + j
    ep = v.make_ep(epseed, 'genuine_ambiguity', env)
    params = world.world_params(epseed, MODES[mi])
    return mi, ri, j, epseed, ep, params


def rollout_matrix(ep, mode: str, params, env, reps: int) -> np.ndarray:
    idx = env[6]
    target = int(idx[ep.target]); twin = int(idx[ep.twin_target])
    if mode in ('balanced_no_unique', 'biased_no_unique'):
        # Independent ordinary continuations of the same observable world state.
        # The hidden generator mode is never a learner input; it only produces outcomes.
        rng = np.random.default_rng(ep.seed * 30011 + 3803801)
        u = rng.random((reps, TRIALS))
        return np.where(u < float(params.stochastic_p), target, twin).astype(np.int8)
    seq = np.array([int(idx[world.world_outcome(ep, mode, params, t)]) for t in range(TRIALS)], dtype=np.int8)
    return np.repeat(seq[None, :], reps, axis=0)


def repeated_pair_targets(z32, z33):
    episode = z32['episode_id'].astype(int)
    trial = z32['trial_index'].astype(int)
    current = np.argmax(z33['learned_ensemble_next_prediction'], axis=1).astype(int)
    n = len(episode)
    mean = np.zeros((n, 2 * len(HORIZONS)), np.float32)
    var = np.zeros_like(mean)
    env = r31.setup(9714)
    stats = {m: {'rows': 0, 'mean_target_variance': 0.0} for m in MODES}
    for eid in np.unique(episode):
        rows = np.where(episode == eid)[0]
        rows = rows[np.argsort(trial[rows])]
        mi, ri, j, epseed, ep, params = reconstruct_episode(int(eid), env)
        roll = rollout_matrix(ep, MODES[mi], params, env, REPLICATES)
        vals = []
        for row in rows:
            t = int(trial[row]); top = int(current[row]); blocks = []
            for h in HORIZONS:
                q = roll[:, t:min(TRIALS, t + h)]
                same = np.mean(q == top, axis=1)
                # Generic dominant future mass; K is small and only observed outcomes contribute.
                counts = np.stack([np.sum(q == k, axis=1) for k in range(5)], axis=1)
                dom = np.max(counts, axis=1) / q.shape[1]
                blocks.extend([dom, same])
            b = np.asarray(blocks, float).T  # [replicate, scalar]
            mean[row] = b.mean(axis=0)
            var[row] = b.var(axis=0)
            vals.append(float(b.var(axis=0).mean()))
        stats[MODES[mi]]['rows'] += len(rows)
        stats[MODES[mi]]['mean_target_variance'] += float(np.sum(vals))
    for m in MODES:
        stats[m]['mean_target_variance'] /= max(1, stats[m]['rows'])
    return mean, var, stats


def prediction_metrics(Y, P, split, advantage):
    return v37.metrics(Y, P, split, advantage)


def save_action(prefix: str, models: dict) -> dict:
    out = {}
    for name, model in models.items():
        p = ROOT / f'R32_V38_{prefix}_{name.upper()}_SEED_9714.joblib'
        joblib.dump(model, p, compress=3)
        out[name] = {'file': p.name, 'sha256': sha(p)}
    return out


def main():
    t0 = time.time()
    z32 = np.load(ROOT / 'R32_V32_PREDICTIVE_DYNAMICS_DATA_SEED_9714.npz')
    z33 = np.load(ROOT / 'R32_V33_LEARNED_GATING_DATA_SEED_9714.npz')
    z34 = np.load(ROOT / 'R32_V34_MULTISTEP_STATE_DATA_SEED_9714.npz')
    assert np.array_equal(z32['episode_id'], z33['episode_id'])
    assert np.array_equal(z32['split_code'], z33['split_code'])
    split = z32['split_code'].astype(int)
    advantage = z32['advantage'].astype(float)
    X = np.c_[z32['X_dynamics'].astype(np.float32), z33['gate_features'].astype(np.float32)]
    cols = v37.pair_cols()
    single = z34['target_future_state_evaluator_only'][:, cols].astype(np.float32)

    print('V38_REPEATED_TARGETS', flush=True)
    Ymean, Yvar, mode_variance = repeated_pair_targets(z32, z33)
    print('V38_MEAN_MODEL', flush=True)
    Pmean, mean_model, mean_meta = v37.crossfit(X, Ymean, split, advantage, 'unweighted', SEED)
    print('V38_VARIANCE_MODEL', flush=True)
    Pvar, var_model, var_meta = v37.crossfit(np.c_[X, Pmean], Yvar, split, advantage, 'unweighted', SEED + 100)

    arms = {}
    action_files = {}
    for i, (name, feat) in enumerate([
        ('predicted_mean', np.c_[X, Pmean]),
        ('predicted_mean_variance', np.c_[X, Pmean, Pvar]),
        ('exact_repeated_mean_variance_evaluator_only', np.c_[X, Ymean, Yvar]),
    ]):
        print('V38_ACTION', name, flush=True)
        models, val = v32.fit(feat, advantage, split, SEED + 500 + i * 100)
        arms[name] = val
        if 'evaluator_only' not in name:
            action_files[name] = save_action(name.upper(), models)

    v37_result = json.loads((ROOT / 'R32_V37_REGRET_WEIGHTED_CANDIDATE_SUPPORT_REFERENCE_ONLY.json').read_text())
    v37_ref = v37_result['action_value']['arms']['specialized_unweighted']
    exact_single = v37_result['action_value']['exact_pair_ceiling_evaluator_only']
    te = split >= 8
    target_shift = {
        'overall_single_to_repeated_mean_mae': float(np.mean(np.abs(single[te] - Ymean[te]))),
        'overall_repeated_target_variance': float(np.mean(Yvar[te])),
        'by_mode_evaluator_only': {},
    }
    mode = z32['mode_evaluator_only'].astype(int)
    for i, name in enumerate(MODES):
        q = te & (mode == i)
        target_shift['by_mode_evaluator_only'][name] = {
            'n': int(q.sum()),
            'single_to_repeated_mean_mae': float(np.mean(np.abs(single[q] - Ymean[q]))),
            'repeated_target_variance': float(np.mean(Yvar[q])),
        }

    pred = {
        'single_continuation_specialized_unweighted': v37_result['prediction_metrics']['specialized_unweighted'],
        'repeated_mean_prediction': prediction_metrics(Ymean, Pmean, split, advantage),
        'repeated_variance_prediction': prediction_metrics(Yvar, Pvar, split, advantage),
    }
    model_files = {}
    for name, model in [('mean', mean_model), ('variance', var_model)]:
        p = ROOT / f'R32_V38_REPEATED_{name.upper()}_MODEL_SEED_9714.joblib'
        joblib.dump(model, p, compress=3)
        model_files[name] = {'file': p.name, 'sha256': sha(p)}

    data_path = ROOT / 'R32_V38_REPEATED_CONTINUATION_DATA_SEED_9714.npz'
    np.savez_compressed(
        data_path,
        repeated_mean_target=Ymean,
        repeated_variance_target=Yvar,
        predicted_repeated_mean=Pmean,
        predicted_repeated_variance=Pvar,
        single_continuation_target=single,
        split_code=split.astype(np.int8),
        episode_id=z32['episode_id'],
    )
    deltas = {}
    for name, val in arms.items():
        deltas[name] = {
            'expected_auc_vs_v37_unweighted': val['expected_advantage']['roc_auc'] - v37_ref['expected_advantage']['roc_auc'],
            'beneficial_cross_vs_v37_unweighted': val['expected_advantage']['true_positive_cross_zero'] - v37_ref['expected_advantage']['true_positive_cross_zero'],
            'false_cross_vs_v37_unweighted': val['expected_advantage']['false_positive_cross_zero'] - v37_ref['expected_advantage']['false_positive_cross_zero'],
            'selected_advantage_vs_v37_unweighted': val['expected_advantage']['actual_mean_selected'] - v37_ref['expected_advantage']['actual_mean_selected'],
        }

    out = {
        'experiment': 'R32 V38 repeated-continuation expectation credit over matched observable epistemic states',
        'replicates_per_state': REPLICATES,
        'horizons': HORIZONS,
        'target_shift': target_shift,
        'external_world_variance_by_mode_evaluator_only': mode_variance,
        'prediction_metrics': pred,
        'training_meta': {'mean': mean_meta, 'variance': var_meta},
        'action_value': {
            'v37_single_continuation_reference': v37_ref,
            'exact_single_continuation_pair_ceiling_evaluator_only': exact_single,
            'arms': arms,
            'delta_vs_v37_unweighted': deltas,
            'models': action_files,
        },
        'models': model_files,
        'data': {'file': data_path.name, 'sha256': sha(data_path)},
        'seconds': time.time() - t0,
        'training_boundary': 'Repeated targets are consolidated from independent delayed grounded continuations of the same observable state. Hidden world mode generates experience but is never a learner feature or runtime input.',
        'claim_boundary': 'REFERENCE_ONLY. No ambiguity label, mode identity, resource-regime identity, final answer, graph, transformer, tokenizer, supplied boundary, or fixed runtime probe count enters cognition.',
    }
    result_path = ROOT / 'R32_V38_REPEATED_CONTINUATION_CREDIT_REFERENCE_ONLY.json'
    result_path.write_text(json.dumps(out, indent=2))
    config = {
        'status': 'REFERENCE_ONLY_MATCHED_REPEATED_CONTINUATION_CREDIT',
        'seed': SEED,
        'replicates_per_state': REPLICATES,
        'episode_disjoint_splits': True,
        'runtime_fixed_probe_count': False,
        'native_promotion_allowed': False,
        'source_sha256': sha(Path(__file__)),
    }
    (ROOT / 'R32_V38_CONFIG.json').write_text(json.dumps(config, indent=2))
    summary = {
        'target_shift': target_shift,
        'prediction_metrics': pred,
        'action_delta': deltas,
        'seconds': out['seconds'],
    }
    (ROOT / 'R32_V38_TRAINING.log').write_text(json.dumps(summary, indent=2) + '\n')
    (ROOT / 'R32_V38_DONE.flag').write_text('')
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == '__main__':
    main()
