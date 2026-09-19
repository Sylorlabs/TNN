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
SEED = 33033
MODEL_NAMES = [
    'uniform','global','recent2','recent3','recent5','exp50','exp75','exp90',
    'last','changepoint','transition1','transition2','parity2','phase3','return2'
]
MODES = ['balanced_no_unique','biased_no_unique','stable_weak','unstable_then_stable','replacement','reversal','costly_stable']
TRIALS = 12


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def softmax_neg_loss(loss: np.ndarray, temperature: float) -> np.ndarray:
    z = -np.asarray(loss, dtype=np.float64) / max(float(temperature), 1e-6)
    z -= np.max(z, axis=1, keepdims=True)
    e = np.exp(np.clip(z, -60.0, 0.0))
    return e / np.maximum(e.sum(axis=1, keepdims=True), 1e-12)


def entropy_rows(p: np.ndarray) -> np.ndarray:
    q = np.clip(p, 1e-12, 1.0)
    return -(q * np.log(q)).sum(axis=1) / math.log(q.shape[1])


def margin_rows(p: np.ndarray) -> np.ndarray:
    q = np.sort(p, axis=1)
    return q[:, -1] - q[:, -2]


def mixture(weights: np.ndarray, model_predictions: np.ndarray) -> np.ndarray:
    q = np.einsum('nm,nmk->nk', weights, model_predictions, optimize=True)
    q = np.maximum(q, 1e-12)
    return q / q.sum(axis=1, keepdims=True)


def nll_rows(p: np.ndarray, y: np.ndarray) -> np.ndarray:
    return -np.log(np.clip(p[np.arange(len(y)), y], 1e-12, 1.0))


def prediction_metrics(p: np.ndarray, y: np.ndarray) -> dict:
    one = np.eye(p.shape[1], dtype=np.float64)[y]
    return {
        'top1': float(np.mean(np.argmax(p, axis=1) == y)),
        'nll': float(np.mean(nll_rows(p, y))),
        'brier': float(np.mean(np.sum((p - one) ** 2, axis=1))),
    }


def gater_inputs(z) -> np.ndarray:
    # Every column is learner-visible at decision time: persistent V30 state,
    # each generic dynamics hypothesis's current prediction, and its accumulated
    # prequential evidence. Evaluator mode/trial/resource IDs and the next outcome
    # are excluded.
    return np.c_[
        z['X_base'].astype(np.float32),
        z['model_prequential_avg_loss'].astype(np.float32),
        z['model_weights'].astype(np.float32),
        z['model_next_predictions'].reshape(len(z['X_base']), -1).astype(np.float32),
    ].astype(np.float32)


def targets(z) -> np.ndarray:
    pred = z['model_next_predictions'].astype(np.float64)
    y = z['true_next_outcome_evaluator_only'].astype(int)
    prob = np.take_along_axis(pred, y[:, None, None], axis=2).squeeze(2)
    return -np.log(np.clip(prob, 1e-9, 1.0)).astype(np.float32)


def make_model(seed: int) -> ExtraTreesRegressor:
    return ExtraTreesRegressor(
        n_estimators=140,
        max_depth=18,
        min_samples_leaf=18,
        max_features=0.55,
        bootstrap=False,
        n_jobs=6,
        random_state=seed,
    )


def crossfit(X: np.ndarray, Y: np.ndarray, split: np.ndarray):
    train = split <= 5
    calibration = (split == 6) | (split == 7)
    test = split >= 8
    pred = np.empty_like(Y, dtype=np.float32)
    folds = [np.isin(split, [0, 3]), np.isin(split, [1, 4]), np.isin(split, [2, 5])]
    fold_meta = []
    for fi, hold in enumerate(folds):
        fit_mask = train & ~hold
        hold_mask = train & hold
        print('V33_GATER_FOLD', fi, 'fit', int(fit_mask.sum()), 'hold', int(hold_mask.sum()), flush=True)
        m = make_model(SEED + fi)
        t0 = time.time(); m.fit(X[fit_mask], Y[fit_mask]); seconds = time.time() - t0
        pred[hold_mask] = m.predict(X[hold_mask]).astype(np.float32)
        fold_meta.append({'fold': fi, 'fit_rows': int(fit_mask.sum()), 'hold_rows': int(hold_mask.sum()), 'seconds': seconds})
    print('V33_GATER_FINAL fit', int(train.sum()), flush=True)
    final = make_model(SEED + 20)
    t0 = time.time(); final.fit(X[train], Y[train]); final_seconds = time.time() - t0
    pred[calibration | test] = final.predict(X[calibration | test]).astype(np.float32)
    return pred, final, {'folds': fold_meta, 'final_seconds': final_seconds, 'train_rows': int(train.sum()), 'calibration_rows': int(calibration.sum()), 'test_rows': int(test.sum())}


def select_temperature(pred_loss: np.ndarray, model_pred: np.ndarray, y: np.ndarray, mask: np.ndarray):
    grid = np.geomspace(0.06, 5.0, 96)
    rows = []
    for temp in grid:
        w = softmax_neg_loss(pred_loss[mask], float(temp))
        p = mixture(w, model_pred[mask])
        rows.append((float(np.mean(nll_rows(p, y[mask]))), float(temp)))
    rows.sort()
    return rows[0], rows[:12]


def gate_features(pred_loss: np.ndarray, weights: np.ndarray, ens: np.ndarray, model_pred: np.ndarray) -> np.ndarray:
    n, m = pred_loss.shape
    order = np.argsort(pred_loss, axis=1)
    selected = order[:, 0]
    onehot = np.eye(m, dtype=np.float32)[selected]
    sorted_loss = np.take_along_axis(pred_loss, order, axis=1)
    model_top = np.argmax(model_pred, axis=2)
    ens_top = np.argmax(ens, axis=1)
    top_agreement = np.mean(model_top == ens_top[:, None], axis=1)
    weighted_top_agreement = np.sum(weights * (model_top == ens_top[:, None]), axis=1)
    # Weighted predictive disagreement from squared distance to the learned mixture.
    disagree = np.sum(weights[:, :, None] * (model_pred - ens[:, None, :]) ** 2, axis=(1, 2))
    summaries = np.c_[
        sorted_loss[:, 0], sorted_loss[:, 1], sorted_loss[:, 1] - sorted_loss[:, 0],
        pred_loss.mean(axis=1), pred_loss.std(axis=1),
        weights.max(axis=1), entropy_rows(weights),
        ens.max(axis=1), margin_rows(ens), entropy_rows(ens),
        top_agreement, weighted_top_agreement, disagree,
    ].astype(np.float32)
    return np.c_[pred_loss.astype(np.float32), weights.astype(np.float32), ens.astype(np.float32), onehot, summaries].astype(np.float32)


def save_action_models(prefix: str, models: dict) -> dict:
    out = {}
    for name, model in models.items():
        p = ROOT / f'R32_V33_{prefix}_{name.upper()}_SEED_9714.joblib'
        joblib.dump(model, p, compress=3)
        out[name] = {'file': p.name, 'sha256': sha(p)}
    return out


def main():
    import sys
    sys.path[:0] = ['/mnt/data/r31_part2', str(ROOT)]
    import r32_v32_predictive_dynamics_population as v32

    t0 = time.time()
    z = np.load(ROOT / 'R32_V32_PREDICTIVE_DYNAMICS_DATA_SEED_9714.npz')
    split = z['split_code'].astype(int)
    y = z['true_next_outcome_evaluator_only'].astype(int)
    model_pred = z['model_next_predictions'].astype(np.float64)
    current_ens = z['ensemble_next_prediction'].astype(np.float64)
    Xg = gater_inputs(z)
    Yloss = targets(z)
    pred_loss, final_gater, gater_meta = crossfit(Xg, Yloss, split)

    train = split <= 5
    calibration = (split == 6) | (split == 7)
    test = split >= 8

    (best_nll, temperature), temp_frontier = select_temperature(pred_loss, model_pred, y, calibration)
    weights = softmax_neg_loss(pred_loss, temperature)
    learned_soft = mixture(weights, model_pred)
    hard_idx = np.argmin(pred_loss, axis=1)
    learned_hard = model_pred[np.arange(len(model_pred)), hard_idx]

    # Select the fixed control only on calibration outcomes, then evaluate once on test.
    cal_model_nll = np.asarray([np.mean(nll_rows(model_pred[calibration, j], y[calibration])) for j in range(model_pred.shape[1])])
    fixed_idx = int(np.argmin(cal_model_nll))
    fixed_pred = model_pred[:, fixed_idx]

    # Per-row oracle is evaluator-only and provides the ceiling of the existing inventory.
    actual_loss = Yloss.astype(np.float64)
    oracle_idx = np.argmin(actual_loss, axis=1)
    oracle_pred = model_pred[np.arange(len(model_pred)), oracle_idx]

    methods = {
        'current_prequential_mixture': current_ens,
        'calibration_selected_fixed': fixed_pred,
        'learned_hard_selector': learned_hard,
        'learned_soft_mixture': learned_soft,
        'per_row_oracle_evaluator_only': oracle_pred,
    }
    prediction = {name: prediction_metrics(p[test], y[test]) for name, p in methods.items()}

    # Gater's ability to predict the 15 next-loss surfaces.
    gate_loss_metrics = {
        'mse': float(mean_squared_error(Yloss[test], pred_loss[test])),
        'mae': float(mean_absolute_error(Yloss[test], pred_loss[test])),
        'r2_variance_weighted': float(r2_score(Yloss[test], pred_loss[test], multioutput='variance_weighted')),
        'hard_selector_matches_oracle': float(np.mean(hard_idx[test] == oracle_idx[test])),
        'hard_selector_excess_nll_over_oracle': float(np.mean(actual_loss[test, hard_idx[test]] - actual_loss[test, oracle_idx[test]])),
        'soft_mixture_excess_nll_over_oracle': float(prediction['learned_soft_mixture']['nll'] - prediction['per_row_oracle_evaluator_only']['nll']),
        'current_mixture_excess_nll_over_oracle': float(prediction['current_prequential_mixture']['nll'] - prediction['per_row_oracle_evaluator_only']['nll']),
    }

    mode = z['mode_evaluator_only'].astype(int)
    trial = z['trial_index'].astype(int)
    by_mode = {}
    for i, name in enumerate(MODES):
        q = test & (mode == i)
        by_mode[name] = {method: prediction_metrics(p[q], y[q]) for method, p in methods.items() if method != 'per_row_oracle_evaluator_only'}
        by_mode[name]['mean_learned_weight'] = {MODEL_NAMES[j]: float(weights[q, j].mean()) for j in range(len(MODEL_NAMES))}
    by_trial = {}
    for i in range(TRIALS):
        q = test & (trial == i)
        by_trial[str(i)] = {method: prediction_metrics(p[q], y[q]) for method, p in methods.items() if method != 'per_row_oracle_evaluator_only'}

    # Add learned gate state to the exact corrected V32 representation. Cross-fitted
    # features are used for action-value training rows; final-gater features are used
    # for calibration/test rows. This prevents target leakage into the train features.
    gf = gate_features(pred_loss, weights, learned_soft, model_pred)
    X_plus = np.c_[z['X_dynamics'].astype(np.float32), gf]
    X_replace = np.c_[z['X_base'].astype(np.float32), model_pred.reshape(len(model_pred), -1).astype(np.float32), gf]
    advantage = z['advantage'].astype(float)

    print('V33_ACTION_VALUE_PLUS', X_plus.shape, flush=True)
    plus_models, plus_val = v32.fit(X_plus, advantage, split, SEED + 100)
    print('V33_ACTION_VALUE_REPLACE', X_replace.shape, flush=True)
    replace_models, replace_val = v32.fit(X_replace, advantage, split, SEED + 200)

    gater_path = ROOT / 'R32_V33_NEXT_LOSS_GATER_SEED_9714.joblib'
    joblib.dump(final_gater, gater_path, compress=3)
    plus_files = save_action_models('PLUS_GATE', plus_models)
    replace_files = save_action_models('REPLACE_GATE', replace_models)

    dataset_path = ROOT / 'R32_V33_LEARNED_GATING_DATA_SEED_9714.npz'
    np.savez_compressed(
        dataset_path,
        predicted_model_next_loss=pred_loss.astype(np.float32),
        learned_model_weights=weights.astype(np.float32),
        learned_ensemble_next_prediction=learned_soft.astype(np.float32),
        learned_hard_model=hard_idx.astype(np.int8),
        gate_features=gf.astype(np.float32),
        split_code=split.astype(np.int8),
        episode_id=z['episode_id'],
    )

    old = json.loads((ROOT / 'R32_V32_PREDICTIVE_DYNAMICS_VALIDATION.json').read_text())
    result = {
        'experiment': 'R32 V33 learned predictive-dynamics gating from delayed next-observation loss',
        'dataset': {
            'rows': int(len(split)),
            'gater_feature_dim': int(Xg.shape[1]),
            'gate_output_feature_dim': int(gf.shape[1]),
            'v32_plus_gate_dim': int(X_plus.shape[1]),
            'replacement_gate_dim': int(X_replace.shape[1]),
            'temperature': float(temperature),
            'calibration_nll_at_temperature': float(best_nll),
            'fixed_model_selected_on_calibration': MODEL_NAMES[fixed_idx],
            'fixed_model_calibration_nll': float(cal_model_nll[fixed_idx]),
            'temperature_frontier': [{'nll': n, 'temperature': t} for n, t in temp_frontier],
            'crossfit': gater_meta,
            'learner_inputs': 'persistent V30 state, generic model predictions, and accumulated prequential losses only',
            'delayed_training_target': 'experienced next grounded observation log loss for each generic dynamics hypothesis',
            'forbidden_inputs': 'world mode, ambiguity label, resource-regime identity, trial index, future opportunity list, final answer, fixed probe count',
        },
        'next_outcome_prediction': prediction,
        'gater_loss_prediction': gate_loss_metrics,
        'by_mode_evaluator_only': by_mode,
        'by_trial_evaluator_only': by_trial,
        'action_value': {
            'v32_reference': {
                'classifier': old['classifier'],
                'expected_advantage': old['expected_advantage'],
                'direct': old['direct'],
            },
            'v32_plus_learned_gate': plus_val,
            'learned_gate_replacement': replace_val,
            'models': {'plus': plus_files, 'replacement': replace_files},
        },
        'artifacts': {
            'gater': {'file': gater_path.name, 'sha256': sha(gater_path)},
            'dataset': {'file': dataset_path.name, 'sha256': sha(dataset_path)},
        },
        'seconds': time.time() - t0,
        'claim_boundary': 'REFERENCE_ONLY. Learned dynamics weights use only episode-disjoint delayed next-observation loss. Evaluator identities are metrics only. No graph, transformer, tokenizer, VAD, supplied boundary, or fixed runtime probe count.',
    }
    out_path = ROOT / 'R32_V33_LEARNED_PREDICTIVE_GATING_REFERENCE_ONLY.json'
    out_path.write_text(json.dumps(result, indent=2))
    config = {
        'status': 'REFERENCE_ONLY_MATCHED_LEARNED_DYNAMICS_CREDIT',
        'seed': SEED,
        'source_sha256': sha(Path(__file__)),
        'base_v32_data_sha256': sha(ROOT / 'R32_V32_PREDICTIVE_DYNAMICS_DATA_SEED_9714.npz'),
        'episode_disjoint_crossfit': True,
        'runtime_fixed_probe_count': False,
        'native_promotion_allowed': False,
    }
    (ROOT / 'R32_V33_CONFIG.json').write_text(json.dumps(config, indent=2))
    summary = {
        'fixed_model': MODEL_NAMES[fixed_idx],
        'temperature': temperature,
        'prediction': prediction,
        'gater_loss_prediction': gate_loss_metrics,
        'plus_action_value': plus_val,
        'replacement_action_value': replace_val,
        'seconds': result['seconds'],
    }
    (ROOT / 'R32_V33_TRAINING.log').write_text(json.dumps(summary, indent=2) + '\n')
    (ROOT / 'R32_V33_DONE.flag').write_text('')
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == '__main__':
    main()
