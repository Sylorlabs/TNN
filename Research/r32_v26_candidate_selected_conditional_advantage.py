from __future__ import annotations

import hashlib
import json
import math
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    mean_absolute_error,
    mean_squared_error,
    roc_auc_score,
)

ROOT = Path('/mnt/data/r32_epistemic')
sys.path[:0] = ['/mnt/data/r31_part2', str(ROOT)]

import r31_sequential_evidence_abstention_REFERENCE_ONLY as r31
import r32_epistemic_r31_matched_v17_cached_REFERENCE_ONLY as v

MODES = [
    'balanced_no_unique',
    'biased_no_unique',
    'stable_weak',
    'unstable_then_stable',
    'replacement',
    'reversal',
    'costly_stable',
]
TRIALS = 12
EPISODES_PER_MODE = 220
SOURCE = 7
SEED = 9714


@dataclass(frozen=True)
class WorldParams:
    stochastic_p: float | None
    phase1: int
    sigma: float
    cost: float


def world_params(episode_seed: int, mode: str) -> WorldParams:
    rng = np.random.default_rng(episode_seed * 31 + 123)
    if mode == 'balanced_no_unique':
        p = float(rng.uniform(0.45, 0.55))
    elif mode == 'biased_no_unique':
        p = float(rng.uniform(0.62, 0.76))
    else:
        p = None
    phase1 = int(rng.integers(2, 7))
    if mode == 'stable_weak':
        sigma = float(rng.uniform(0.95, 1.18))
    elif mode == 'costly_stable':
        sigma = float(rng.uniform(0.72, 0.96))
    else:
        sigma = float(rng.uniform(0.62, 0.90))
    cost = float(rng.uniform(1.80, 2.80)) if mode == 'costly_stable' else float(rng.uniform(0.28, 0.52))
    return WorldParams(p, phase1, sigma, cost)


def world_outcome(ep: Any, mode: str, params: WorldParams, trial: int) -> int:
    # The regime name is used only by the external world generator. It is never
    # included in learner features or model inputs.
    rng = np.random.default_rng(ep.seed * 9176 + trial * 17011 + 37)
    if mode in ('balanced_no_unique', 'biased_no_unique'):
        assert params.stochastic_p is not None
        return ep.target if rng.random() < params.stochastic_p else ep.twin_target
    if mode in ('stable_weak', 'costly_stable'):
        return ep.target
    if mode == 'unstable_then_stable':
        return (ep.target if trial % 2 == 0 else ep.twin_target) if trial < params.phase1 else ep.target
    if mode == 'replacement':
        return ep.target if trial < params.phase1 else ep.twin_target
    if mode == 'reversal':
        return ep.twin_target if trial < params.phase1 else ep.target
    raise ValueError(mode)


def delayed_consensus_from_outcomes(ep: Any, mode: str, params: WorldParams) -> int | None:
    # Two later, disjoint grounded windows determine whether development
    # eventually supports a unique state. No ambiguity/mode label is consulted.
    def window(start: int, n: int = 32) -> tuple[int, float]:
        values = [world_outcome(ep, mode, params, start + i) for i in range(n)]
        ids, counts = np.unique(values, return_counts=True)
        at = int(np.argmax(counts))
        return int(ids[at]), float(counts[at] / n)

    a, fa = window(48)
    b, fb = window(112)
    return a if a == b and min(fa, fb) >= 0.80 else None


def source7_observation(
    ep: Any,
    mode: str,
    params: WorldParams,
    st: Any,
    env: Any,
    used_actions: list[int],
    trial: int,
) -> np.ndarray:
    *_, classes, idx, sig, learned = env
    outcome = world_outcome(ep, mode, params, trial)
    action = r31.select_action(st.score, learned, used_actions)
    used_actions.append(action)
    rng = np.random.default_rng(ep.seed * 2029 + trial * 12347 + action * 31 + 97)
    observation = sig[idx[outcome], action] + float(rng.normal(0, params.sigma))
    variance = 0.95 if mode in ('balanced_no_unique', 'biased_no_unique', 'unstable_then_stable') else 0.88
    return np.array(
        [-((observation - learned[ci, action]) ** 2) / (2 * variance**2) for ci in range(len(classes))],
        dtype=float,
    )


def terminal_utility(st: Any, a0: int, consensus: int | None, env: Any) -> float:
    classes = env[5]
    full = int(classes[int(np.argmax(st.p(True)))])
    epoch = int(classes[int(np.argmax(st.epoch_p()))])
    unresolved = 1.0 if consensus is None else -1.2
    return float(
        max(
            v.delayed_action_utility(a0, consensus),
            v.delayed_action_utility(full, consensus),
            v.delayed_action_utility(epoch, consensus),
            0.0,  # explicit UNKNOWN is neutral
            unresolved,
        )
    )


def action_feature(st: Any, ep: Any, safe: Any, a0: int, env: Any, cost: float) -> np.ndarray:
    q = v.q_feat(st, ep, safe, a0, env)
    return np.r_[q, np.eye(v.S)[SOURCE], cost, st.group_n[v.GROUP[SOURCE]] / 3]


def split_code(mode_index: int, episode_index: int) -> int:
    # Episode-level split: every state from one trajectory stays in one split.
    return int((episode_index * 7 + mode_index * 3) % 10)


def generate_dataset() -> tuple[dict[str, np.ndarray], dict[str, Any]]:
    t0 = time.time()
    env = r31.setup(SEED)
    safe = v.train_A(SEED, env)

    x_rows: list[np.ndarray] = []
    advantages: list[float] = []
    episode_ids: list[int] = []
    splits: list[int] = []
    modes: list[int] = []
    trials: list[int] = []
    costs: list[float] = []
    consensus_flags: list[int] = []

    episode_id = 0
    mode_counts: dict[str, dict[str, float]] = {}
    for mode_index, mode in enumerate(MODES):
        print('GENERATE_MODE', mode, flush=True)
        mode_adv: list[float] = []
        mode_consensus = 0
        for episode_index in range(EPISODES_PER_MODE):
            episode_seed = SEED * 1_000_000 + mode_index * 100_000 + episode_index
            ep = v.make_ep(episode_seed, 'genuine_ambiguity', env)
            ep.avail[:] = False
            ep.avail[0] = True
            ep.avail[1] = True
            ep.avail[SOURCE] = True
            params = world_params(episode_seed, mode)
            ep.cost[SOURCE] = params.cost
            consensus = delayed_consensus_from_outcomes(ep, mode, params)
            mode_consensus += int(consensus is not None)

            st = v.initial_state(ep, env, 'D')
            a0 = int(env[5][int(np.argmax(st.p(True)))])
            used_actions: list[int] = []
            path: list[tuple[np.ndarray, float, float, int, float]] = []

            for trial in range(TRIALS):
                current_terminal = terminal_utility(st, a0, consensus, env)
                feat = action_feature(st, ep, safe, a0, env, params.cost)
                evidence = source7_observation(ep, mode, params, st, env, used_actions, trial)
                nxt = st.clone()
                nxt.add(SOURCE, evidence, params.cost)
                next_terminal = terminal_utility(nxt, a0, consensus, env)
                path.append((feat, current_terminal, next_terminal, trial, params.cost))
                st = nxt

            continuation = -1e9
            local: list[tuple[np.ndarray, float, int, float]] = []
            for feat, current_terminal, next_terminal, trial, cost in reversed(path):
                inspect_return = max(next_terminal, continuation) - cost
                advantage = float(inspect_return - current_terminal)
                local.append((feat, advantage, trial, cost))
                continuation = inspect_return
            local.reverse()

            sc = split_code(mode_index, episode_index)
            for feat, advantage, trial, cost in local:
                x_rows.append(feat)
                advantages.append(advantage)
                episode_ids.append(episode_id)
                splits.append(sc)
                modes.append(mode_index)
                trials.append(trial)
                costs.append(cost)
                consensus_flags.append(int(consensus is not None))
                mode_adv.append(advantage)
            episode_id += 1

        z = np.asarray(mode_adv)
        mode_counts[mode] = {
            'rows': int(len(z)),
            'positive_rate': float(np.mean(z > 0)),
            'mean_advantage': float(np.mean(z)),
            'delayed_consensus_episode_rate': float(mode_consensus / EPISODES_PER_MODE),
        }

    data = {
        'X': np.asarray(x_rows, dtype=np.float32),
        'advantage': np.asarray(advantages, dtype=np.float32),
        'episode_id': np.asarray(episode_ids, dtype=np.int32),
        'split_code': np.asarray(splits, dtype=np.int8),
        'mode_evaluator_only': np.asarray(modes, dtype=np.int8),
        'trial_index': np.asarray(trials, dtype=np.int8),
        'cost': np.asarray(costs, dtype=np.float32),
        'delayed_consensus_evaluator_only': np.asarray(consensus_flags, dtype=np.int8),
    }
    meta = {
        'seed': SEED,
        'episodes_per_mode': EPISODES_PER_MODE,
        'trials_per_episode': TRIALS,
        'episodes': episode_id,
        'rows': len(advantages),
        'feature_dim': int(data['X'].shape[1]),
        'overall_positive_rate': float(np.mean(data['advantage'] > 0)),
        'mode_evaluator_only': mode_counts,
        'generation_seconds': time.time() - t0,
        'selection': 'source 7 is the sole optional reusable evidence action in high-uncertainty apparatus states; all reached pre-action states are retained',
        'target': 'episodic backward grounded INSPECT return minus best delayed terminal utility (KEEP/current/global/current-epoch/UNKNOWN/UNRESOLVED)',
        'learner_inputs': '60-dimensional persistent epistemic state + source one-hot/provenance + experienced cost + lineage repetition count',
        'forbidden_inputs': 'mode, ambiguity label, final evaluator state, fixed runtime probe count',
    }
    return data, meta


def safe_logit(p: np.ndarray) -> np.ndarray:
    q = np.clip(p, 1e-6, 1 - 1e-6)
    return np.log(q / (1 - q)).reshape(-1, 1)


def calibration_deciles(p: np.ndarray, y: np.ndarray, expected: np.ndarray, actual: np.ndarray) -> list[dict[str, float]]:
    order = np.argsort(p)
    groups = np.array_split(order, 10)
    out = []
    for i, g in enumerate(groups):
        if not len(g):
            continue
        out.append({
            'decile': i,
            'n': int(len(g)),
            'mean_probability': float(np.mean(p[g])),
            'actual_positive_rate': float(np.mean(y[g])),
            'mean_expected_advantage': float(np.mean(expected[g])),
            'mean_actual_advantage': float(np.mean(actual[g])),
        })
    return out


def fit_and_validate(data: dict[str, np.ndarray], meta: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    X = data['X']
    adv = data['advantage'].astype(float)
    y = (adv > 0).astype(int)
    code = data['split_code']
    train = code <= 5
    calibrate = (code == 6) | (code == 7)
    test = code >= 8

    classifier = HistGradientBoostingClassifier(
        random_state=26026,
        max_iter=180,
        max_leaf_nodes=23,
        min_samples_leaf=28,
        l2_regularization=1.1,
        learning_rate=0.05,
    ).fit(X[train], y[train])

    raw_cal = classifier.predict_proba(X[calibrate])[:, 1]
    platt = LogisticRegression(max_iter=1000, C=1.0).fit(safe_logit(raw_cal), y[calibrate])

    pos_reg = HistGradientBoostingRegressor(
        random_state=26027,
        max_iter=170,
        max_leaf_nodes=21,
        min_samples_leaf=22,
        l2_regularization=0.8,
        learning_rate=0.05,
    ).fit(X[train & (y == 1)], adv[train & (y == 1)])
    neg_reg = HistGradientBoostingRegressor(
        random_state=26028,
        max_iter=170,
        max_leaf_nodes=21,
        min_samples_leaf=30,
        l2_regularization=1.0,
        learning_rate=0.05,
    ).fit(X[train & (y == 0)], adv[train & (y == 0)])

    raw_p = classifier.predict_proba(X[test])[:, 1]
    p = platt.predict_proba(safe_logit(raw_p))[:, 1]
    q_pos = pos_reg.predict(X[test])
    q_neg = neg_reg.predict(X[test])
    expected = p * q_pos + (1 - p) * q_neg
    yt = y[test]
    at = adv[test]

    validation: dict[str, Any] = {
        'rows': {
            'train': int(np.sum(train)),
            'calibration': int(np.sum(calibrate)),
            'test': int(np.sum(test)),
        },
        'episode_split': 'episode-level deterministic 60/20/20; no trajectory crosses a split',
        'positive_rate': {
            'train': float(np.mean(y[train])),
            'calibration': float(np.mean(y[calibrate])),
            'test': float(np.mean(yt)),
        },
        'classifier': {
            'raw_roc_auc': float(roc_auc_score(yt, raw_p)),
            'calibrated_roc_auc': float(roc_auc_score(yt, p)),
            'average_precision': float(average_precision_score(yt, p)),
            'raw_brier': float(brier_score_loss(yt, raw_p)),
            'calibrated_brier': float(brier_score_loss(yt, p)),
        },
        'conditional_regressors': {
            'positive_mse': float(mean_squared_error(at[yt == 1], q_pos[yt == 1])),
            'positive_mae': float(mean_absolute_error(at[yt == 1], q_pos[yt == 1])),
            'nonpositive_mse': float(mean_squared_error(at[yt == 0], q_neg[yt == 0])),
            'nonpositive_mae': float(mean_absolute_error(at[yt == 0], q_neg[yt == 0])),
            'mean_predicted_positive_component_on_positive': float(np.mean(q_pos[yt == 1])),
            'mean_predicted_nonpositive_component_on_nonpositive': float(np.mean(q_neg[yt == 0])),
        },
        'expected_advantage': {
            'mse': float(mean_squared_error(at, expected)),
            'mae': float(mean_absolute_error(at, expected)),
            'roc_auc_for_positive_advantage': float(roc_auc_score(yt, expected)),
            'mean_on_actual_positive': float(np.mean(expected[yt == 1])),
            'mean_on_actual_nonpositive': float(np.mean(expected[yt == 0])),
            'positive_rate_on_actual_positive': float(np.mean(expected[yt == 1] > 0)),
            'positive_rate_on_actual_nonpositive': float(np.mean(expected[yt == 0] > 0)),
            'overall_predicted_positive_rate': float(np.mean(expected > 0)),
        },
        'calibration_deciles': calibration_deciles(p, yt, expected, at),
        'by_mode_evaluator_only': {},
        'by_trial': {},
        'v25_reference': {
            'validation_positive_rate': 0.017036275517697166,
            'roc_auc': 0.8988664495072051,
            'true_positive_expected_advantage_above_zero_rate': 0.004310344827586207,
            'false_positive_expected_advantage_above_zero_rate': 0.00007470491558344539,
            'mean_expected_advantage_actual_positive': -0.890899349117942,
        },
    }

    mode_arr = data['mode_evaluator_only'][test]
    for i, mode in enumerate(MODES):
        m = mode_arr == i
        validation['by_mode_evaluator_only'][mode] = {
            'n': int(np.sum(m)),
            'actual_positive_rate': float(np.mean(yt[m])),
            'expected_advantage_mean': float(np.mean(expected[m])),
            'actual_advantage_mean': float(np.mean(at[m])),
            'actual_positive_predicted_above_zero': float(np.mean(expected[m & (yt == 1)] > 0)) if np.any(m & (yt == 1)) else None,
            'actual_nonpositive_predicted_above_zero': float(np.mean(expected[m & (yt == 0)] > 0)) if np.any(m & (yt == 0)) else None,
        }

    trial_arr = data['trial_index'][test]
    for trial in range(TRIALS):
        m = trial_arr == trial
        validation['by_trial'][str(trial)] = {
            'n': int(np.sum(m)),
            'actual_positive_rate': float(np.mean(yt[m])),
            'predicted_positive_rate': float(np.mean(expected[m] > 0)),
            'mean_expected_advantage': float(np.mean(expected[m])),
            'mean_actual_advantage': float(np.mean(at[m])),
        }

    models = {
        'classifier': classifier,
        'probability_calibrator': platt,
        'positive_advantage_regressor': pos_reg,
        'nonpositive_advantage_regressor': neg_reg,
    }
    return models, validation


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    data, meta = generate_dataset()
    dataset_path = ROOT / 'R32_V26_CANDIDATE_SOURCE7_DATA_SEED_9714.npz'
    np.savez_compressed(dataset_path, **data)
    meta['dataset_sha256'] = sha256(dataset_path)

    models, validation = fit_and_validate(data, meta)
    model_files = {}
    for name, model in models.items():
        p = ROOT / f'R32_V26_{name.upper()}_SEED_9714.joblib'
        joblib.dump(model, p, compress=3)
        model_files[name] = {'file': p.name, 'sha256': sha256(p)}

    validation['models'] = model_files
    validation['dataset'] = meta
    validation['scientific_boundary'] = (
        'REFERENCE_ONLY. Candidate selection uses only action availability and experienced state; '
        'model features exclude generator mode, ambiguity status, delayed answer, and fixed probe count. '
        'Targets use delayed grounded outcomes and experienced observation cost.'
    )
    validation_path = ROOT / 'R32_V26_CONDITIONAL_ADVANTAGE_VALIDATION.json'
    validation_path.write_text(json.dumps(validation, indent=2))

    config = {
        'status': 'REFERENCE_ONLY_VALIDATION_PENDING_RUNTIME_GATE',
        'base': 'V25 pairwise INSPECT advantage target',
        'change_only': 'candidate-selected reusable source-7 development distribution plus two-part conditional utility calibration',
        'seed': SEED,
        'modes_evaluator_only': MODES,
        'episodes_per_mode': EPISODES_PER_MODE,
        'trials_per_episode': TRIALS,
        'runtime_rule_if_validated': 'select INSPECT only when learned expected advantage over best terminal utility is positive',
        'runtime_fixed_probe_count': False,
        'native_promotion_allowed': False,
        'source_sha256': sha256(Path(__file__)),
    }
    (ROOT / 'R32_V26_CONFIG.json').write_text(json.dumps(config, indent=2))

    summary = {
        'candidate_positive_rate': meta['overall_positive_rate'],
        'test_positive_rate': validation['positive_rate']['test'],
        'auc': validation['classifier']['calibrated_roc_auc'],
        'average_precision': validation['classifier']['average_precision'],
        'brier': validation['classifier']['calibrated_brier'],
        **validation['expected_advantage'],
    }
    (ROOT / 'R32_V26_TRAINING.log').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == '__main__':
    main()
