from __future__ import annotations

import hashlib
import json
import math
import time
from pathlib import Path

import joblib
import numpy as np
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

ROOT = Path('/mnt/data/r32_epistemic')
SEED = 34034
HORIZONS = [1, 2, 3, 5, 8, 12]
K = 5
MODES = ['balanced_no_unique','biased_no_unique','stable_weak','unstable_then_stable','replacement','reversal','costly_stable']


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def entropy_dist(p: np.ndarray) -> float:
    q = np.clip(np.asarray(p, float), 1e-12, 1.0)
    return float(-(q * np.log(q)).sum() / math.log(len(q)))


def longest_run_fraction(seq: np.ndarray) -> float:
    if len(seq) == 0:
        return 0.0
    best = cur = 1
    for i in range(1, len(seq)):
        if seq[i] == seq[i - 1]:
            cur += 1
            best = max(best, cur)
        else:
            cur = 1
    return best / len(seq)


def window_target(seq: np.ndarray, current_top: int) -> np.ndarray:
    n = len(seq)
    hist = np.bincount(seq, minlength=K).astype(float)
    hist /= max(1, n)
    transition = float(np.mean(seq[1:] != seq[:-1])) if n > 1 else 0.0
    return2 = float(np.mean(seq[2:] == seq[:-2])) if n > 2 else 0.0
    same_current = float(np.mean(seq == current_top)) if n else 0.0
    return np.r_[
        hist,
        entropy_dist(hist),
        float(hist.max()),
        transition,
        longest_run_fraction(seq),
        same_current,
        return2,
    ]


def build_targets(z32, z33) -> tuple[np.ndarray, dict]:
    episode = z32['episode_id'].astype(int)
    trial = z32['trial_index'].astype(int)
    outcome = z32['true_next_outcome_evaluator_only'].astype(int)
    current = np.argmax(z33['learned_ensemble_next_prediction'], axis=1)
    n = len(episode)
    per_h = K + 6
    Y = np.zeros((n, len(HORIZONS) * per_h + K), dtype=np.float32)
    for eid in np.unique(episode):
        idx = np.where(episode == eid)[0]
        idx = idx[np.argsort(trial[idx])]
        seq_all = outcome[idx]
        for pos, row in enumerate(idx):
            rem = seq_all[pos:]
            blocks = []
            for h in HORIZONS:
                blocks.append(window_target(rem[:min(h, len(rem))], int(current[row])))
            final = np.eye(K, dtype=float)[rem[-1]]
            Y[row] = np.r_[*blocks, final]
    layout = {
        'horizons': HORIZONS,
        'per_horizon': ['outcome_distribution_0..4','normalized_entropy','dominant_mass','transition_rate','longest_run_fraction','fraction_equal_current_top','return_lag2_rate'],
        'per_horizon_dim': per_h,
        'final_outcome_distribution_dim': K,
        'target_dim': int(Y.shape[1]),
    }
    return Y, layout


def postprocess(pred: np.ndarray) -> np.ndarray:
    q = np.asarray(pred, float).copy()
    per_h = K + 6
    for hi in range(len(HORIZONS)):
        st = hi * per_h
        dist = np.clip(q[:, st:st+K], 1e-7, None)
        dist /= dist.sum(axis=1, keepdims=True)
        q[:, st:st+K] = dist
        q[:, st+K:st+per_h] = np.clip(q[:, st+K:st+per_h], 0.0, 1.0)
    st = len(HORIZONS) * per_h
    dist = np.clip(q[:, st:st+K], 1e-7, None)
    q[:, st:st+K] = dist / dist.sum(axis=1, keepdims=True)
    return q.astype(np.float32)


def make_model(seed: int) -> ExtraTreesRegressor:
    return ExtraTreesRegressor(
        n_estimators=150,
        max_depth=19,
        min_samples_leaf=16,
        max_features=0.55,
        n_jobs=6,
        random_state=seed,
    )


def crossfit(X: np.ndarray, Y: np.ndarray, split: np.ndarray):
    train = split <= 5
    caltest = split >= 6
    pred = np.empty_like(Y, dtype=np.float32)
    folds = [np.isin(split, [0, 3]), np.isin(split, [1, 4]), np.isin(split, [2, 5])]
    meta = []
    for fi, hold in enumerate(folds):
        fit = train & ~hold
        h = train & hold
        print('V34_FUTURE_FOLD', fi, 'fit', int(fit.sum()), 'hold', int(h.sum()), flush=True)
        m = make_model(SEED + fi)
        t0 = time.time(); m.fit(X[fit], Y[fit]); sec = time.time() - t0
        pred[h] = postprocess(m.predict(X[h]))
        meta.append({'fold': fi, 'fit_rows': int(fit.sum()), 'hold_rows': int(h.sum()), 'seconds': sec})
    print('V34_FUTURE_FINAL', int(train.sum()), flush=True)
    final = make_model(SEED + 20)
    t0 = time.time(); final.fit(X[train], Y[train]); sec = time.time() - t0
    pred[caltest] = postprocess(final.predict(X[caltest]))
    return pred, final, {'folds': meta, 'final_seconds': sec}


def distribution_ce(actual: np.ndarray, pred: np.ndarray) -> float:
    return float(np.mean(-np.sum(actual * np.log(np.clip(pred, 1e-9, 1.0)), axis=1)))


def evaluate_future(Y: np.ndarray, P: np.ndarray, z32, z33, test: np.ndarray) -> dict:
    per_h = K + 6
    one_step = z33['learned_ensemble_next_prediction'].astype(float)
    out = {
        'overall': {
            'mse': float(mean_squared_error(Y[test], P[test])),
            'mae': float(mean_absolute_error(Y[test], P[test])),
            'r2_variance_weighted': float(r2_score(Y[test], P[test], multioutput='variance_weighted')),
        },
        'horizons': {},
        'final_outcome': {},
        'by_mode_evaluator_only': {},
    }
    for hi, h in enumerate(HORIZONS):
        st = hi * per_h
        a = Y[test, st:st+per_h]
        p = P[test, st:st+per_h]
        out['horizons'][str(h)] = {
            'distribution_cross_entropy': distribution_ce(a[:, :K], p[:, :K]),
            'one_step_distribution_baseline_cross_entropy': distribution_ce(a[:, :K], one_step[test]),
            'distribution_mse': float(np.mean((a[:, :K] - p[:, :K]) ** 2)),
            'entropy_mae': float(np.mean(np.abs(a[:, K] - p[:, K]))),
            'dominant_mass_mae': float(np.mean(np.abs(a[:, K+1] - p[:, K+1]))),
            'transition_rate_mae': float(np.mean(np.abs(a[:, K+2] - p[:, K+2]))),
            'longest_run_mae': float(np.mean(np.abs(a[:, K+3] - p[:, K+3]))),
            'same_current_top_mae': float(np.mean(np.abs(a[:, K+4] - p[:, K+4]))),
            'return_lag2_mae': float(np.mean(np.abs(a[:, K+5] - p[:, K+5]))),
        }
    st = len(HORIZONS) * per_h
    final_a = Y[test, st:st+K]
    final_p = P[test, st:st+K]
    final_y = np.argmax(final_a, axis=1)
    out['final_outcome'] = {
        'top1': float(np.mean(np.argmax(final_p, axis=1) == final_y)),
        'nll': float(np.mean(-np.log(np.clip(final_p[np.arange(len(final_y)), final_y], 1e-9, 1.0)))),
        'one_step_baseline_top1': float(np.mean(np.argmax(one_step[test], axis=1) == final_y)),
        'one_step_baseline_nll': float(np.mean(-np.log(np.clip(one_step[test][np.arange(len(final_y)), final_y], 1e-9, 1.0)))),
    }
    mode = z32['mode_evaluator_only'].astype(int)
    hidx = HORIZONS.index(12); st12 = hidx * per_h
    for mi, name in enumerate(MODES):
        q = test & (mode == mi)
        a = Y[q, st12:st12+per_h]
        p = P[q, st12:st12+per_h]
        out['by_mode_evaluator_only'][name] = {
            'n': int(q.sum()),
            'h12_distribution_cross_entropy': distribution_ce(a[:, :K], p[:, :K]),
            'h12_one_step_baseline_cross_entropy': distribution_ce(a[:, :K], one_step[q]),
            'h12_transition_rate_mae': float(np.mean(np.abs(a[:, K+2] - p[:, K+2]))),
            'h12_entropy_mae': float(np.mean(np.abs(a[:, K] - p[:, K]))),
        }
    return out


def save_models(models: dict) -> dict:
    out = {}
    for name, model in models.items():
        p = ROOT / f'R32_V34_ACTION_{name.upper()}_SEED_9714.joblib'
        joblib.dump(model, p, compress=3)
        out[name] = {'file': p.name, 'sha256': sha(p)}
    return out


def main():
    import sys
    sys.path[:0] = ['/mnt/data/r31_part2', str(ROOT)]
    import r32_v32_predictive_dynamics_population as v32

    t0 = time.time()
    z32 = np.load(ROOT / 'R32_V32_PREDICTIVE_DYNAMICS_DATA_SEED_9714.npz')
    z33 = np.load(ROOT / 'R32_V33_LEARNED_GATING_DATA_SEED_9714.npz')
    assert np.array_equal(z32['split_code'], z33['split_code'])
    assert np.array_equal(z32['episode_id'], z33['episode_id'])
    split = z32['split_code'].astype(int)
    Xv33 = np.c_[z32['X_dynamics'].astype(np.float32), z33['gate_features'].astype(np.float32)]
    Y, layout = build_targets(z32, z33)
    future_pred, future_model, cross_meta = crossfit(Xv33, Y, split)
    test = split >= 8
    future_metrics = evaluate_future(Y, future_pred, z32, z33, test)

    Xv34 = np.c_[Xv33, future_pred]
    print('V34_ACTION_VALUE', Xv34.shape, flush=True)
    action_models, action_val = v32.fit(Xv34, z32['advantage'].astype(float), split, SEED + 100)

    future_model_path = ROOT / 'R32_V34_MULTISTEP_STATE_MODEL_SEED_9714.joblib'
    joblib.dump(future_model, future_model_path, compress=3)
    action_files = save_models(action_models)
    data_path = ROOT / 'R32_V34_MULTISTEP_STATE_DATA_SEED_9714.npz'
    np.savez_compressed(
        data_path,
        predicted_future_state=future_pred.astype(np.float32),
        target_future_state_evaluator_only=Y.astype(np.float32),
        split_code=split.astype(np.int8),
        episode_id=z32['episode_id'],
    )

    v33_result = json.loads((ROOT / 'R32_V33_LEARNED_PREDICTIVE_GATING_REFERENCE_ONLY.json').read_text())
    v33_plus = v33_result['action_value']['v32_plus_learned_gate']
    result = {
        'experiment': 'R32 V34 multi-step convergence and duration state from delayed observed outcome sequences',
        'dataset': {
            'rows': int(len(split)),
            'input_feature_dim': int(Xv33.shape[1]),
            'future_state_target_dim': int(Y.shape[1]),
            'augmented_action_feature_dim': int(Xv34.shape[1]),
            'target_layout': layout,
            'crossfit': cross_meta,
            'learner_inputs': 'V33 persistent state and learned one-step model gate only',
            'delayed_targets': 'future observed outcome distributions, entropy, transition, duration, return, and final outcome summaries',
            'forbidden_inputs': 'world mode, ambiguity label, resource regime, trial identity, future target values at runtime, final answer, fixed probe count',
        },
        'future_state_prediction': future_metrics,
        'action_value': {
            'v33_reference': v33_plus,
            'v34_multistep_state': action_val,
            'delta': {
                'classifier_auc': action_val['classifier']['roc_auc'] - v33_plus['classifier']['roc_auc'],
                'classifier_ap': action_val['classifier']['average_precision'] - v33_plus['classifier']['average_precision'],
                'expected_auc': action_val['expected_advantage']['roc_auc'] - v33_plus['expected_advantage']['roc_auc'],
                'beneficial_cross_zero': action_val['expected_advantage']['true_positive_cross_zero'] - v33_plus['expected_advantage']['true_positive_cross_zero'],
                'nonbeneficial_cross_zero': action_val['expected_advantage']['false_positive_cross_zero'] - v33_plus['expected_advantage']['false_positive_cross_zero'],
                'selected_realized_advantage': action_val['expected_advantage']['actual_mean_selected'] - v33_plus['expected_advantage']['actual_mean_selected'],
            },
            'models': action_files,
        },
        'artifacts': {
            'future_model': {'file': future_model_path.name, 'sha256': sha(future_model_path)},
            'data': {'file': data_path.name, 'sha256': sha(data_path)},
        },
        'seconds': time.time() - t0,
        'claim_boundary': 'REFERENCE_ONLY. Multi-step state is predicted from episode-disjoint delayed experienced outcome sequences; evaluator identities are metrics only. No ambiguity label, graph, transformer, tokenizer, supplied boundary, or fixed runtime probe count.',
    }
    out = ROOT / 'R32_V34_MULTISTEP_CONVERGENCE_STATE_REFERENCE_ONLY.json'
    out.write_text(json.dumps(result, indent=2))
    config = {
        'status': 'REFERENCE_ONLY_MATCHED_MULTISTEP_OPTION_STATE',
        'seed': SEED,
        'horizons': HORIZONS,
        'episode_disjoint_crossfit': True,
        'runtime_fixed_probe_count': False,
        'native_promotion_allowed': False,
        'source_sha256': sha(Path(__file__)),
        'base_v33_data_sha256': sha(ROOT / 'R32_V33_LEARNED_GATING_DATA_SEED_9714.npz'),
    }
    (ROOT / 'R32_V34_CONFIG.json').write_text(json.dumps(config, indent=2))
    summary = {
        'future_state_prediction': future_metrics,
        'action_value': result['action_value'],
        'seconds': result['seconds'],
    }
    (ROOT / 'R32_V34_TRAINING.log').write_text(json.dumps(summary, indent=2) + '\n')
    (ROOT / 'R32_V34_DONE.flag').write_text('')
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == '__main__':
    main()
