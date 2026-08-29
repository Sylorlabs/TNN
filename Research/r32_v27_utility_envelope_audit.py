from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path('/mnt/data/r32_epistemic')
sys.path[:0] = ['/mnt/data/r31_part2', str(ROOT)]

import r31_sequential_evidence_abstention_REFERENCE_ONLY as r31
import r32_epistemic_r31_matched_v17_cached_REFERENCE_ONLY as v
import r32_v26_candidate_selected_conditional_advantage as g

SEED = 9714
EPISODES_PER_MODE = 220
TRIALS = 12
MULTIPLIERS = [round(x, 2) for x in np.arange(0.0, 1.5001, 0.05)]
RESOLVABLE = ['stable_weak', 'unstable_then_stable', 'replacement', 'reversal']
NO_UNIQUE = ['balanced_no_unique', 'biased_no_unique']


def build_paths() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    t0 = time.time()
    env = r31.setup(SEED)
    safe = v.train_A(SEED, env)
    paths: list[dict[str, Any]] = []

    for mode_index, mode in enumerate(g.MODES):
        print('AUDIT_GENERATE', mode, flush=True)
        for episode_index in range(EPISODES_PER_MODE):
            episode_seed = SEED * 1_000_000 + mode_index * 100_000 + episode_index
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
            paths.append({
                'mode': mode,
                'episode_index': episode_index,
                'consensus': None if consensus is None else int(consensus),
                'need_observation': bool(path[0][0] < 0.999999),
                'path': path,
            })

    meta = {
        'seed': SEED,
        'episodes_per_mode': EPISODES_PER_MODE,
        'episodes': len(paths),
        'trials_per_episode': TRIALS,
        'generation_seconds': time.time() - t0,
        'held_constant': 'identical world trajectories, evidence representation, terminal regret values, and source costs',
        'varied_only': 'scalar conversion from experienced observation cost to terminal-regret utility',
        'learner_visibility': 'This is an evaluator/utility audit only; mode and future consensus are never proposed as runtime features.',
    }
    return paths, meta


def evaluate_path(path: list[tuple[float, float, float]], multiplier: float) -> tuple[float, int]:
    continuation = -1e9
    continuation_steps = 0
    initial_advantage = 0.0
    initial_steps = 0
    for index in range(len(path) - 1, -1, -1):
        current_terminal, next_terminal, raw_cost = path[index]
        if continuation > next_terminal:
            best_after = continuation
            steps = 1 + continuation_steps
        else:
            best_after = next_terminal
            steps = 1
        value = best_after - multiplier * raw_cost
        advantage = value - current_terminal
        if index == 0:
            initial_advantage = float(advantage)
            initial_steps = int(steps if advantage > 0 else 0)
        continuation = value
        continuation_steps = steps
    return initial_advantage, initial_steps


def summarize(paths: list[dict[str, Any]], multiplier: float) -> dict[str, Any]:
    by_mode: dict[str, Any] = {}
    all_rows = []
    for mode in g.MODES:
        rows = [x for x in paths if x['mode'] == mode]
        values = []
        steps = []
        need = []
        for row in rows:
            advantage, nsteps = evaluate_path(row['path'], multiplier)
            values.append(advantage)
            steps.append(nsteps)
            need.append(row['need_observation'])
            all_rows.append((mode, advantage, nsteps, row['need_observation']))
        a = np.asarray(values)
        s = np.asarray(steps)
        n = np.asarray(need, dtype=bool)
        by_mode[mode] = {
            'episodes': len(rows),
            'need_observation_rate': float(np.mean(n)),
            'inspect_beneficial_rate_all': float(np.mean(a > 0)),
            'inspect_beneficial_rate_given_need': float(np.mean(a[n] > 0)) if np.any(n) else None,
            'mean_initial_advantage_all': float(np.mean(a)),
            'mean_initial_advantage_given_need': float(np.mean(a[n])) if np.any(n) else None,
            'mean_optimal_trials_when_beneficial': float(np.mean(s[a > 0])) if np.any(a > 0) else 0.0,
        }

    def pooled(modes: list[str]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        z = [(a, st, need) for mode, a, st, need in all_rows if mode in modes]
        return (
            np.asarray([x[0] for x in z]),
            np.asarray([x[1] for x in z]),
            np.asarray([x[2] for x in z], dtype=bool),
        )

    ra, rs, rn = pooled(RESOLVABLE)
    na, ns, nn = pooled(NO_UNIQUE)
    ca, cs, cn = pooled(['costly_stable'])
    dynamic_need_rates = [by_mode[m]['inspect_beneficial_rate_given_need'] for m in RESOLVABLE]
    return {
        'cost_multiplier': multiplier,
        'by_mode': by_mode,
        'aggregate': {
            'resolvable_need_rate': float(np.mean(rn)),
            'resolvable_inspect_beneficial_all': float(np.mean(ra > 0)),
            'resolvable_inspect_beneficial_given_need': float(np.mean(ra[rn] > 0)) if np.any(rn) else None,
            'resolvable_min_mode_beneficial_given_need': float(min(x for x in dynamic_need_rates if x is not None)),
            'resolvable_mean_optimal_trials_when_beneficial': float(np.mean(rs[ra > 0])) if np.any(ra > 0) else 0.0,
            'no_unique_inspect_beneficial_all': float(np.mean(na > 0)),
            'costly_need_rate': float(np.mean(cn)),
            'costly_inspect_beneficial_all': float(np.mean(ca > 0)),
            'costly_inspect_beneficial_given_need': float(np.mean(ca[cn] > 0)) if np.any(cn) else None,
            'separation_resolvable_need_minus_costly_need': float(
                (np.mean(ra[rn] > 0) if np.any(rn) else 0.0) - (np.mean(ca[cn] > 0) if np.any(cn) else 0.0)
            ),
        },
    }


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    paths, meta = build_paths()
    rows = [summarize(paths, multiplier) for multiplier in MULTIPLIERS]
    best = max(rows, key=lambda x: x['aggregate']['separation_resolvable_need_minus_costly_need'])

    # Diagnostic envelope, not a runtime threshold: asks whether one scalar can
    # make most needed ordinary observations useful while leaving clearly costly
    # observations mostly non-beneficial and no-unique observations non-beneficial.
    feasible = [
        x for x in rows
        if x['aggregate']['resolvable_inspect_beneficial_given_need'] >= 0.70
        and x['aggregate']['costly_inspect_beneficial_given_need'] <= 0.10
        and x['aggregate']['no_unique_inspect_beneficial_all'] <= 0.01
    ]
    actual = next(x for x in rows if x['cost_multiplier'] == 1.0)
    half = next(x for x in rows if x['cost_multiplier'] == 0.5)
    zero = next(x for x in rows if x['cost_multiplier'] == 0.0)

    result = {
        'experiment': 'R32 V27 matched utility-envelope audit',
        'meta': meta,
        'multipliers': rows,
        'key_points': {
            'zero_cost_upper_bound': zero['aggregate'],
            'current_scale_1_0': actual['aggregate'],
            'scale_0_5': half['aggregate'],
            'best_separation': best,
            'diagnostic_feasible_multipliers': [x['cost_multiplier'] for x in feasible],
            'diagnostic_feasible_interval': [feasible[0]['cost_multiplier'], feasible[-1]['cost_multiplier']] if feasible else None,
        },
        'claim_boundary': (
            'REFERENCE_ONLY evaluator/utility audit. No policy was trained or promoted. '
            'All trajectories, hypotheses, evidence, and terminal regret values are fixed; only the scalar utility conversion of experienced observation cost changes.'
        ),
    }
    out = ROOT / 'R32_V27_UTILITY_ENVELOPE_REFERENCE_ONLY.json'
    out.write_text(json.dumps(result, indent=2))

    config = {
        'status': 'REFERENCE_ONLY_UTILITY_SCALE_CAUSAL_AUDIT',
        'seed': SEED,
        'episodes_per_mode': EPISODES_PER_MODE,
        'trials_per_episode': TRIALS,
        'multipliers': MULTIPLIERS,
        'terminal_regret_fixed': {'correct': 1.0, 'unknown': 0.0, 'wrong': -2.0, 'commit_nonconvergent': -1.2, 'unresolved_correct': 1.0, 'unresolved_wrong': -1.2},
        'runtime_policy_changed': False,
        'native_promotion_allowed': False,
        'source_sha256': sha256(Path(__file__)),
    }
    (ROOT / 'R32_V27_CONFIG.json').write_text(json.dumps(config, indent=2))

    summary = {
        'current_scale': actual['aggregate'],
        'half_scale': half['aggregate'],
        'best_multiplier': best['cost_multiplier'],
        'best_separation': best['aggregate']['separation_resolvable_need_minus_costly_need'],
        'feasible_interval': result['key_points']['diagnostic_feasible_interval'],
    }
    (ROOT / 'R32_V27_UTILITY_ENVELOPE.log').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == '__main__':
    main()
