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
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

ROOT = Path('/mnt/data/r32_epistemic')
sys.path[:0] = ['/mnt/data/r31_part2', str(ROOT)]

import r31_sequential_evidence_abstention_REFERENCE_ONLY as r31
import r32_epistemic_r31_matched_v17_cached_REFERENCE_ONLY as v
import r32_v26_candidate_selected_conditional_advantage as g

SEED = 9714
N_RESOURCE_EPISODES = 26000
UNIT = 0.10
RESOURCE_REGIMES = ['generous', 'balanced', 'scarce', 'low_value', 'volatile']
EPISTEMIC_MODES = g.MODES
TRIALS = 12


@dataclass(frozen=True)
class ResourceContext:
    regime: int
    budget: float
    history_cost: np.ndarray
    history_reward: np.ndarray
    future_cost: np.ndarray
    future_reward: np.ndarray


def regime_parameters(regime: int, rng: np.random.Generator) -> tuple[float, tuple[float, float], tuple[float, float], int]:
    if regime == 0:  # generous reserve, moderate value density
        return float(rng.uniform(6.0, 9.0)), (0.80, 1.60), (0.20, 0.80), 12
    if regime == 1:  # balanced
        return float(rng.uniform(4.0, 7.0)), (0.60, 1.40), (0.30, 1.00), 14
    if regime == 2:  # scarce reserve, valuable pending opportunities
        return float(rng.uniform(2.0, 4.0)), (0.40, 1.00), (0.50, 1.20), 16
    if regime == 3:  # low-value future demand
        return float(rng.uniform(3.0, 6.0)), (0.50, 1.30), (0.05, 0.40), 14
    return float(rng.uniform(2.5, 5.0)), (0.30, 1.60), (0.20, 1.20), 16


def draw_context(seed: int, regime: int | None = None) -> ResourceContext:
    rng = np.random.default_rng(seed)
    r = int(rng.integers(len(RESOURCE_REGIMES))) if regime is None else int(regime)
    budget, cost_range, reward_range, n = regime_parameters(r, rng)
    history_cost = rng.uniform(*cost_range, n)
    history_reward = rng.uniform(*reward_range, n)
    # Future opportunities are independent draws from the same locally observed
    # resource process. The regime identity itself is never a learner feature.
    future_cost = rng.uniform(*cost_range, n)
    future_reward = rng.uniform(*reward_range, n)
    return ResourceContext(r, budget, history_cost, history_reward, future_cost, future_reward)


def knapsack_value(cost: np.ndarray, reward: np.ndarray, budget: float) -> float:
    capacity = max(0, int(round(float(budget) / UNIT)))
    dp = np.zeros(capacity + 1, dtype=float)
    for c, u in zip(cost, reward):
        weight = max(1, int(round(float(c) / UNIT)))
        if weight <= capacity:
            dp[weight:] = np.maximum(dp[weight:], dp[:-weight] + float(u))
    return float(dp.max())


def opportunity_loss(context: ResourceContext, budget: float, action_cost: float) -> float:
    before = knapsack_value(context.future_cost, context.future_reward, budget)
    after = knapsack_value(context.future_cost, context.future_reward, max(0.0, budget - action_cost))
    return max(0.0, before - after)


def resource_features(context: ResourceContext, budget: float, action_cost: float) -> np.ndarray:
    c = context.history_cost
    r = context.history_reward
    density = r / np.maximum(c, 1e-6)
    qcost = np.quantile(c, [0.25, 0.50, 0.75])
    qreward = np.quantile(r, [0.25, 0.50, 0.75])
    history_value = knapsack_value(c, r, budget)
    history_after = knapsack_value(c, r, max(0.0, budget - action_cost))
    history_loss = max(0.0, history_value - history_after)
    recent_n = min(5, len(c))
    return np.asarray([
        action_cost,
        budget,
        action_cost / max(budget, 1e-6),
        len(c) / 20.0,
        float(np.mean(c)),
        float(np.std(c)),
        float(np.min(c)),
        float(np.max(c)),
        *map(float, qcost),
        float(np.mean(r)),
        float(np.std(r)),
        float(np.min(r)),
        float(np.max(r)),
        *map(float, qreward),
        float(np.mean(density)),
        float(np.std(density)),
        float(np.max(density)),
        float(np.sum(c) / max(budget, 1e-6)),
        float(np.sum(r)),
        float(np.mean(c <= budget)),
        float(np.mean(c[-recent_n:])),
        float(np.mean(r[-recent_n:])),
        history_value,
        history_loss,
        history_loss / max(action_cost, 1e-6),
    ], dtype=float)


def sample_action_cost(rng: np.random.Generator) -> float:
    u = rng.random()
    if u < 0.70:
        return float(rng.uniform(0.28, 0.52))
    if u < 0.90:
        return float(rng.uniform(0.60, 1.20))
    return float(rng.uniform(1.80, 2.80))


def generate_resource_dataset() -> dict[str, np.ndarray]:
    X = []
    y = []
    raw_cost = []
    budget = []
    regime = []
    split = []
    for i in range(N_RESOURCE_EPISODES):
        context = draw_context(SEED * 10_000_000 + i * 17 + 3)
        rng = np.random.default_rng(SEED * 20_000_000 + i * 31 + 11)
        cost = sample_action_cost(rng)
        X.append(resource_features(context, context.budget, cost))
        y.append(opportunity_loss(context, context.budget, cost))
        raw_cost.append(cost)
        budget.append(context.budget)
        regime.append(context.regime)
        split.append(i % 10)
    return {
        'X': np.asarray(X, dtype=np.float32),
        'opportunity_loss': np.asarray(y, dtype=np.float32),
        'raw_cost': np.asarray(raw_cost, dtype=np.float32),
        'budget': np.asarray(budget, dtype=np.float32),
        'regime_evaluator_only': np.asarray(regime, dtype=np.int8),
        'split_code': np.asarray(split, dtype=np.int8),
    }


def fit_shadow_model(data: dict[str, np.ndarray]) -> tuple[Any, dict[str, Any]]:
    X = data['X']
    y = data['opportunity_loss'].astype(float)
    c = data['raw_cost'].astype(float)
    split = data['split_code']
    train = split <= 7
    test = split >= 8

    model = HistGradientBoostingRegressor(
        random_state=28028,
        max_iter=220,
        max_leaf_nodes=27,
        min_samples_leaf=30,
        l2_regularization=1.0,
        learning_rate=0.05,
    ).fit(X[train], y[train])
    pred = np.maximum(0.0, model.predict(X[test]))
    yt = y[test]
    ct = c[test]
    alpha = float(np.dot(c[train], y[train]) / max(1e-12, np.dot(c[train], c[train])))
    fixed_raw = ct
    fixed_audit = 0.55 * ct
    fixed_global = alpha * ct

    metrics: dict[str, Any] = {
        'rows': {'train': int(np.sum(train)), 'test': int(np.sum(test))},
        'feature_dim': int(X.shape[1]),
        'adaptive_model': {
            'mse': float(mean_squared_error(yt, pred)),
            'mae': float(mean_absolute_error(yt, pred)),
            'r2': float(r2_score(yt, pred)),
            'mean_predicted_loss': float(np.mean(pred)),
            'mean_actual_loss': float(np.mean(yt)),
        },
        'baselines': {
            'raw_scale_1_0': {'mse': float(mean_squared_error(yt, fixed_raw)), 'mae': float(mean_absolute_error(yt, fixed_raw))},
            'audit_scale_0_55': {'mse': float(mean_squared_error(yt, fixed_audit)), 'mae': float(mean_absolute_error(yt, fixed_audit))},
            'learned_global_scalar': {'alpha': alpha, 'mse': float(mean_squared_error(yt, fixed_global)), 'mae': float(mean_absolute_error(yt, fixed_global))},
        },
        'by_regime_evaluator_only': {},
        'by_budget_pressure_quintile': [],
    }
    rr = data['regime_evaluator_only'][test]
    for i, name in enumerate(RESOURCE_REGIMES):
        mask = rr == i
        metrics['by_regime_evaluator_only'][name] = {
            'n': int(np.sum(mask)),
            'mean_actual_loss': float(np.mean(yt[mask])),
            'mean_predicted_loss': float(np.mean(pred[mask])),
            'mean_actual_multiplier': float(np.mean(yt[mask] / np.maximum(ct[mask], 1e-6))),
            'mean_predicted_multiplier': float(np.mean(pred[mask] / np.maximum(ct[mask], 1e-6))),
            'mae': float(mean_absolute_error(yt[mask], pred[mask])),
        }
    pressure = X[test, 2]
    order = np.argsort(pressure)
    for q, ids in enumerate(np.array_split(order, 5)):
        metrics['by_budget_pressure_quintile'].append({
            'quintile': q,
            'n': int(len(ids)),
            'mean_cost_over_budget': float(np.mean(pressure[ids])),
            'mean_actual_multiplier': float(np.mean(yt[ids] / np.maximum(ct[ids], 1e-6))),
            'mean_predicted_multiplier': float(np.mean(pred[ids] / np.maximum(ct[ids], 1e-6))),
            'mae': float(mean_absolute_error(yt[ids], pred[ids])),
        })
    return model, metrics


def build_epistemic_paths() -> tuple[Any, Any, list[dict[str, Any]]]:
    env = r31.setup(SEED)
    safe = v.train_A(SEED, env)
    rows = []
    # Fresh episode indices, distinct from V26/V27 development rows.
    for mode_index, mode in enumerate(EPISTEMIC_MODES):
        print('SHADOW_APPLY', mode, flush=True)
        for episode_index in range(120):
            episode_seed = SEED * 2_000_000 + mode_index * 100_000 + episode_index + 50_000
            ep = v.make_ep(episode_seed, 'genuine_ambiguity', env)
            ep.avail[:] = False
            ep.avail[0] = True
            ep.avail[1] = True
            ep.avail[g.SOURCE] = True
            params = g.world_params(episode_seed, mode)
            ep.cost[g.SOURCE] = params.cost
            consensus = g.delayed_consensus_from_outcomes(ep, mode, params)
            st = v.initial_state(ep, env, 'D')
            a0 = int(env[5][int(np.argmax(st.p(True)))])
            used: list[int] = []
            path = []
            for trial in range(TRIALS):
                current_terminal = g.terminal_utility(st, a0, consensus, env)
                evidence = g.source7_observation(ep, mode, params, st, env, used, trial)
                nxt = st.clone()
                nxt.add(g.SOURCE, evidence, params.cost)
                next_terminal = g.terminal_utility(nxt, a0, consensus, env)
                path.append((float(current_terminal), float(next_terminal), float(params.cost)))
                st = nxt
            rows.append({'mode': mode, 'episode_seed': episode_seed, 'path': path, 'need': path[0][0] < 0.999999})
    return env, safe, rows


def backward_advantage(path: list[tuple[float, float, float]], costs: list[float]) -> tuple[float, int]:
    continuation = -1e9
    continuation_steps = 0
    initial_adv = 0.0
    initial_steps = 0
    for i in range(len(path) - 1, -1, -1):
        current_terminal, next_terminal, _ = path[i]
        if continuation > next_terminal:
            best = continuation
            steps = 1 + continuation_steps
        else:
            best = next_terminal
            steps = 1
        value = best - costs[i]
        advantage = value - current_terminal
        if i == 0:
            initial_adv = float(advantage)
            initial_steps = int(steps if advantage > 0 else 0)
        continuation = value
        continuation_steps = steps
    return initial_adv, initial_steps


def apply_shadow_price(model: Any, rows: list[dict[str, Any]]) -> dict[str, Any]:
    arms = ['raw_1_0', 'fixed_0_55', 'learned_shadow']
    resource_results: dict[str, Any] = {}
    all_records = []
    for resource_regime, resource_name in enumerate(RESOURCE_REGIMES):
        records = []
        for j, row in enumerate(rows):
            context = draw_context(SEED * 30_000_000 + resource_regime * 1_000_000 + j * 43 + 19, resource_regime)
            predicted_costs = []
            actual_costs = []
            raw_costs = []
            budget = context.budget
            for _, _, raw_cost in row['path']:
                feat = resource_features(context, budget, raw_cost)
                predicted_costs.append(max(0.0, float(model.predict(feat[None, :])[0])))
                actual_costs.append(opportunity_loss(context, budget, raw_cost))
                raw_costs.append(raw_cost)
                budget = max(0.0, budget - raw_cost)
            actual_adv, _ = backward_advantage(row['path'], actual_costs)
            predictions = {
                'raw_1_0': backward_advantage(row['path'], raw_costs)[0],
                'fixed_0_55': backward_advantage(row['path'], [0.55 * x for x in raw_costs])[0],
                'learned_shadow': backward_advantage(row['path'], predicted_costs)[0],
            }
            records.append({
                'mode': row['mode'],
                'need': row['need'],
                'actual_advantage': actual_adv,
                'predicted_advantage': predictions,
            })
        resource_results[resource_name] = summarize_decisions(records, arms)
        all_records.extend(records)
    return {'by_resource_regime_evaluator_only': resource_results, 'pooled': summarize_decisions(all_records, arms)}


def summarize_decisions(records: list[dict[str, Any]], arms: list[str]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    actual = np.asarray([r['actual_advantage'] for r in records])
    need = np.asarray([r['need'] for r in records], dtype=bool)
    oracle = actual > 0
    for arm in arms:
        predicted = np.asarray([r['predicted_advantage'][arm] for r in records])
        choose = predicted > 0
        chosen_utility = np.where(choose, actual, 0.0)
        oracle_utility = np.maximum(actual, 0.0)
        out[arm] = {
            'inspect_rate': float(np.mean(choose)),
            'oracle_beneficial_rate': float(np.mean(oracle)),
            'precision_actual_benefit': float(np.mean(oracle[choose])) if np.any(choose) else None,
            'recall_actual_benefit': float(np.mean(choose[oracle])) if np.any(oracle) else None,
            'false_positive_rate': float(np.mean(choose[~oracle])) if np.any(~oracle) else None,
            'mean_realized_incremental_utility': float(np.mean(chosen_utility)),
            'mean_oracle_incremental_utility': float(np.mean(oracle_utility)),
            'mean_policy_regret': float(np.mean(oracle_utility - chosen_utility)),
            'needed_resolvable_selection_rate': float(np.mean(choose[need])) if np.any(need) else None,
        }
    return out


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    t0 = time.time()
    data = generate_resource_dataset()
    dataset_path = ROOT / 'R32_V28_RESOURCE_SHADOW_DATA_SEED_9714.npz'
    np.savez_compressed(dataset_path, **data)
    model, validation = fit_shadow_model(data)
    model_path = ROOT / 'R32_V28_RESOURCE_SHADOW_MODEL_SEED_9714.joblib'
    joblib.dump(model, model_path, compress=3)

    _, _, epistemic_rows = build_epistemic_paths()
    application = apply_shadow_price(model, epistemic_rows)
    result = {
        'experiment': 'R32 V28 learned resource shadow price from delayed opportunity loss',
        'validation': validation,
        'epistemic_cost_application_audit': application,
        'meta': {
            'resource_episodes': N_RESOURCE_EPISODES,
            'resource_regimes_evaluator_only': RESOURCE_REGIMES,
            'epistemic_modes_evaluator_only': EPISTEMIC_MODES,
            'epistemic_episodes_per_mode': 120,
            'runtime_fixed_cost_multiplier': False,
            'learner_features_exclude_resource_regime': True,
            'target': 'delayed optimal future opportunity value before spending minus after spending',
            'seconds': time.time() - t0,
            'dataset_sha256': sha256(dataset_path),
            'model_sha256': sha256(model_path),
        },
        'claim_boundary': (
            'REFERENCE_ONLY component qualification. The cost model receives current budget, experienced action cost, '
            'and summaries of recent resource opportunities; hidden resource regime and future opportunity list are excluded. '
            'Epistemic application is an evaluator audit using fixed evidence trajectories, not a promoted runtime policy.'
        ),
    }
    out_path = ROOT / 'R32_V28_RESOURCE_SHADOW_PRICE_REFERENCE_ONLY.json'
    out_path.write_text(json.dumps(result, indent=2))
    config = {
        'status': 'REFERENCE_ONLY_RESOURCE_SHADOW_COMPONENT',
        'seed': SEED,
        'resource_episodes': N_RESOURCE_EPISODES,
        'runtime_fixed_multiplier': False,
        'native_promotion_allowed': False,
        'source_sha256': sha256(Path(__file__)),
    }
    (ROOT / 'R32_V28_CONFIG.json').write_text(json.dumps(config, indent=2))
    summary = {
        'adaptive_validation': validation['adaptive_model'],
        'baselines': validation['baselines'],
        'pooled_epistemic_application': application['pooled'],
    }
    (ROOT / 'R32_V28_TRAINING.log').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == '__main__':
    main()
