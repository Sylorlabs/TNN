from __future__ import annotations

import hashlib
import json
import math
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

import joblib
import numpy as np

ROOT = Path('/mnt/data/r32_epistemic')
ENV_SEED = 9714
EVAL_SEED = 41041
SOURCE = 7
TRIALS_TRAINED = 12
SAFETY_MAX = 40  # evaluator safety only; not exposed as a learner feature
N_PER_CELL = 40
MODES = ['balanced_no_unique','biased_no_unique','stable_weak','unstable_then_stable','replacement','reversal','costly_stable']
RESOURCE_REGIMES = ['generous','balanced','scarce','low_value','volatile']
HORIZONS = np.array([1,2,3,5,8,12], float)

import sys
sys.path[:0] = ['/mnt/data/r31_part2', str(ROOT)]
import r31_sequential_evidence_abstention_REFERENCE_ONLY as r31
import r32_epistemic_r31_matched_v17_cached_REFERENCE_ONLY as v
import r32_v26_candidate_selected_conditional_advantage as world
import r32_v28_learned_resource_shadow_price as resource
import r32_v28_complete_from_checkpoint as resource_fast
import r32_v29_resource_grounded_inspect_advantage as v29
import r32_v30_candidate_ordered_history as v30
import r32_v32_predictive_dynamics_population as v32
import r32_v33_learned_predictive_gating as v33
import r32_v39_candidate_recurrent_temporal_pam as v39
import r32_v40_horizon_hazard_population as v40


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_logit(p: np.ndarray) -> np.ndarray:
    q = np.clip(np.asarray(p, float), 1e-6, 1 - 1e-6)
    return np.log(q / (1 - q)).reshape(-1, 1)


def load_two_stage(prefix: str) -> dict[str, Any]:
    return {
        'classifier': joblib.load(ROOT / f'{prefix}_CLASSIFIER_SEED_9714.joblib'),
        'calibrator': joblib.load(ROOT / f'{prefix}_CALIBRATOR_SEED_9714.joblib'),
        'positive': joblib.load(ROOT / f'{prefix}_POSITIVE_SEED_9714.joblib'),
        'nonpositive': joblib.load(ROOT / f'{prefix}_NONPOSITIVE_SEED_9714.joblib'),
    }


def expected_advantage(models: dict[str, Any], x: np.ndarray) -> float:
    xx = np.asarray(x, float).reshape(1, -1)
    raw = models['classifier'].predict_proba(xx)[:, 1]
    p = float(models['calibrator'].predict_proba(safe_logit(raw))[0, 1])
    qp = float(models['positive'].predict(xx)[0])
    qn = float(models['nonpositive'].predict(xx)[0])
    return p * qp + (1 - p) * qn


class LiveModels:
    def __init__(self):
        self.shadow = joblib.load(ROOT / 'R32_V28_RESOURCE_SHADOW_MODEL_SEED_9714.joblib')
        self.gater = joblib.load(ROOT / 'R32_V33_NEXT_LOSS_GATER_SEED_9714.joblib')
        self.gate_temperature = float(json.loads((ROOT / 'R32_V33_LEARNED_PREDICTIVE_GATING_REFERENCE_ONLY.json').read_text())['dataset']['temperature'])
        self.rep_mean = joblib.load(ROOT / 'R32_V38_REPEATED_MEAN_MODEL_SEED_9714.joblib')
        self.rep_var = joblib.load(ROOT / 'R32_V38_REPEATED_VARIANCE_MODEL_SEED_9714.joblib')
        self.horizon_support = joblib.load(ROOT / 'R32_V40_HORIZON_SUPPORT_MODEL_SEED_9714.joblib')
        self.horizon_dominant = joblib.load(ROOT / 'R32_V40_HORIZON_DOMINANT_MODEL_SEED_9714.joblib')
        self.v38_action = load_two_stage('R32_V38_PREDICTED_MEAN_VARIANCE')
        self.v40_action = load_two_stage('R32_V40_HORIZON_HAZARD_VARIANCE')
        self.keep = joblib.load(ROOT / 'R32_V19_BASE_KEEP_SEED_9714.joblib')
        self.commit = joblib.load(ROOT / 'R32_V19_BASE_COMMIT_SEED_9714.joblib')
        self.epoch = joblib.load(ROOT / 'R32_V19_BASE_EPOCH_SEED_9714.joblib')
        self.unknown = joblib.load(ROOT / 'R32_V19_BASE_UNKNOWN_SEED_9714.joblib')
        self.nonstationary = joblib.load(ROOT / 'R32_V18_NONSTATIONARY_HYPOTHESIS_SEED_9714.joblib')


def terminal_values(st, ep, safe, a0, env, models: LiveModels):
    q = v.q_feat(st, ep, safe, a0, env)
    full = int(env[5][int(np.argmax(st.p(True)))])
    epoch_cand = int(env[5][int(np.argmax(st.epoch_p()))])
    q_keep = float(models.keep.predict(q[None, :])[0])
    q_full = float(models.commit.predict(q[None, :])[0])
    q_epoch = float(models.epoch.predict(q[None, :])[0])
    q_unknown_base = float(models.unknown.predict(q[None, :])[0])
    uq = np.delete(np.asarray(q), [len(q) - 6, len(q) - 5])
    unresolved_mass = float(models.nonstationary.predict_proba(uq[None, :])[0, 1])
    q_unresolved = unresolved_mass * 1.0 + (1 - unresolved_mass) * (-1.2)
    q_unknown = max(q_unknown_base, q_unresolved)
    if q_epoch > q_full:
        candidate, q_commit = epoch_cand, q_epoch
    else:
        candidate, q_commit = full, q_full
    vals = {'keep': q_keep, 'commit': q_commit, 'unknown': q_unknown}
    choice = max(vals, key=vals.get)
    decision = a0 if choice == 'keep' else (candidate if choice == 'commit' else -1)
    return decision, choice, vals, unresolved_mass


def live_state_features(st, ep, safe, a0, env, params, ctx, cache, budget, seq_hist, models: LiveModels):
    resf = resource_fast.fast_feature(ctx, cache, budget, params.cost)
    raw = v29.action_feature_base(st, ep, safe, a0, env, params.cost, resf)
    shadow_cost = float(max(0.0, models.shadow.predict(np.asarray(resf).reshape(1, -1))[0]))
    x_base = np.r_[raw, shadow_cost, v30.candidate_history_features(st, SOURCE)].astype(np.float32)

    dyn, _, model_pred, raw_weights, avg_loss = v32.predictive_features(st, SOURCE)
    xg = np.r_[x_base, avg_loss, raw_weights, model_pred.reshape(-1)].astype(np.float32)
    pred_loss = np.asarray(models.gater.predict(xg.reshape(1, -1))[0], np.float32)
    learned_weights = v33.softmax_neg_loss(pred_loss.reshape(1, -1), models.gate_temperature)[0].astype(np.float32)
    learned_ens = v33.mixture(learned_weights.reshape(1, -1), model_pred.reshape(1, *model_pred.shape))[0].astype(np.float32)
    gf = v33.gate_features(pred_loss.reshape(1, -1), learned_weights.reshape(1, -1), learned_ens.reshape(1, -1), model_pred.reshape(1, *model_pred.shape))[0]
    x_action = np.r_[x_base, dyn, gf].astype(np.float32)

    pmean = np.clip(models.rep_mean.predict(x_action.reshape(1, -1))[0], 0, 1).astype(np.float32)
    pvar = np.clip(models.rep_var.predict(np.r_[x_action, pmean].reshape(1, -1))[0], 0, 0.25).astype(np.float32)
    x_v38 = np.r_[x_action, pmean, pvar].astype(np.float32)

    action_count = int(env[8].shape[1])
    seq = np.zeros((TRIALS_TRAINED, st.K + action_count), np.float32)
    recent = seq_hist[-TRIALS_TRAINED:]
    if recent:
        seq[:len(recent)] = np.asarray(recent, np.float32)
    length = min(len(seq_hist), TRIALS_TRAINED)
    top = int(np.argmax(learned_ens))
    onehot = np.eye(st.K, dtype=np.float32)[top]
    base_h = np.r_[seq.reshape(-1), gf, pred_loss, learned_weights, learned_ens, onehot, length / TRIALS_TRAINED, (TRIALS_TRAINED - length) / TRIALS_TRAINED].astype(np.float32)
    remain = max(1, TRIALS_TRAINED - min(length, TRIALS_TRAINED - 1))
    hh = HORIZONS
    hf = np.c_[hh / 12, np.log1p(hh) / np.log(13), np.minimum(hh, remain) / remain, np.full(len(hh), remain / 12)]
    xh = np.c_[np.repeat(base_h.reshape(1, -1), len(hh), axis=0), hf].astype(np.float32)
    ps = np.clip(models.horizon_support.predict(xh), 0, 1).reshape(1, -1).astype(np.float32)
    pd = np.clip(models.horizon_dominant.predict(xh), 0, 1).reshape(1, -1).astype(np.float32)
    pair = v40.interleave(pd, ps)[0]
    hz = v40.hazard_features(pd, ps)[0]
    x_v40 = np.r_[x_action, pair, pvar, hz].astype(np.float32)
    return {
        'x_base': x_base,
        'dyn': np.asarray(dyn, np.float32),
        'pred_loss': pred_loss,
        'weights': learned_weights,
        'ensemble': learned_ens,
        'gate_features': gf.astype(np.float32),
        'x_action': x_action,
        'pmean': pmean,
        'pvar': pvar,
        'pair': pair,
        'hazard': hz,
        'x_v38': x_v38,
        'x_v40': x_v40,
        'shadow_cost': shadow_cost,
        'resource_features': np.asarray(resf, np.float32),
    }


def exact_feature_replay(env, safe, models: LiveModels):
    z32 = np.load(ROOT / 'R32_V32_PREDICTIVE_DYNAMICS_DATA_SEED_9714.npz')
    z33 = np.load(ROOT / 'R32_V33_LEARNED_GATING_DATA_SEED_9714.npz')
    z38 = np.load(ROOT / 'R32_V38_REPEATED_CONTINUATION_DATA_SEED_9714.npz')
    z40 = np.load(ROOT / 'R32_V40_HORIZON_HAZARD_DATA_SEED_9714.npz')
    eligible = np.where((z32['split_code'] >= 8) & (z32['trial_index'] == 5))[0]
    row = int(eligible[17])
    eid = int(z32['episode_id'][row]); mi, ri, j, epseed, ep, params = v39.reconstruct_episode(eid, env)
    ep.avail[:] = False; ep.avail[0] = ep.avail[1] = ep.avail[SOURCE] = True; ep.cost[SOURCE] = params.cost
    ctx = resource.draw_context(v29.SEED * 50_000_000 + mi * 4_000_000 + ri * 500_000 + j * 53 + 23, ri)
    cache = resource_fast.context_cache(ctx); budget = ctx.budget
    st = v.initial_state(ep, env, 'D'); a0 = int(env[5][int(np.argmax(st.p(True)))]); used=[]; seq_hist=[]
    target_trial = int(z32['trial_index'][row])
    for t in range(target_trial + 1):
        if t == target_trial:
            f = live_state_features(st, ep, safe, a0, env, params, ctx, cache, budget, seq_hist, models)
            break
        vec, action = v39.evidence_and_action(ep, MODES[mi], params, st, env, used, t)
        aa = np.zeros(int(env[8].shape[1]), np.float32); aa[action] = 1.0
        seq_hist.append(np.r_[v.softmax(vec).astype(np.float32), aa])
        st.add(SOURCE, vec, params.cost); budget = max(0.0, budget - params.cost)
    checks = {
        'row': row, 'episode_id': eid, 'split_code': int(z32['split_code'][row]), 'trial': target_trial,
        'x_base_max_abs_delta': float(np.max(np.abs(f['x_base'] - z32['X_base'][row]))),
        'x_action_max_abs_delta': float(np.max(np.abs(f['x_action'] - np.r_[z32['X_dynamics'][row], z33['gate_features'][row]]))),
        'gate_features_max_abs_delta': float(np.max(np.abs(f['gate_features'] - z33['gate_features'][row]))),
        'pmean_max_abs_delta': float(np.max(np.abs(f['pmean'] - z38['predicted_repeated_mean'][row]))),
        'pvar_max_abs_delta': float(np.max(np.abs(f['pvar'] - z38['predicted_repeated_variance'][row]))),
        'pair_max_abs_delta': float(np.max(np.abs(f['pair'] - z40['predicted_pair'][row]))),
        'hazard_max_abs_delta': float(np.max(np.abs(f['hazard'] - z40['hazard_features'][row]))),
    }
    checks['pass'] = bool(max(vv for kk, vv in checks.items() if kk.endswith('_delta')) < 2e-5)
    return checks


def desired(ep, mode):
    if mode in ('balanced_no_unique','biased_no_unique','costly_stable'):
        return -1
    if mode == 'replacement':
        return ep.twin_target
    return ep.target


def run_episode(epseed, mode, resource_index, arm, reuse, env, safe, models: LiveModels):
    ep = v.make_ep(epseed, 'genuine_ambiguity', env)
    ep.avail[:] = False; ep.avail[0] = ep.avail[1] = ep.avail[SOURCE] = True
    params = world.world_params(epseed, mode); ep.cost[SOURCE] = params.cost
    ctxseed = EVAL_SEED * 70_000_000 + MODES.index(mode) * 5_000_000 + resource_index * 700_000 + (epseed % 100000) * 71 + 41
    ctx = resource.draw_context(ctxseed, resource_index); cache = resource_fast.context_cache(ctx); budget = ctx.budget
    st = v.initial_state(ep, env, 'D'); a0 = int(env[5][int(np.argmax(st.p(True)))]); used=[]; seq_hist=[]
    raw_cost = 0.0; opportunity_loss = 0.0; advantage_trace=[]; terminal_trace=[]
    runaway = False; stop_reason = ''
    for trial in range(SAFETY_MAX):
        dec, terminal_choice, terminal_q, unresolved_mass = terminal_values(st, ep, safe, a0, env, models)
        terminal_trace.append({'trial': trial, 'choice': terminal_choice, 'q': terminal_q, 'unresolved_mass': unresolved_mass})
        if arm == 'terminal_only':
            stop_reason = 'terminal_only'; break
        f = live_state_features(st, ep, safe, a0, env, params, ctx, cache, budget, seq_hist, models)
        ex = expected_advantage(models.v38_action if arm == 'v38' else models.v40_action, f['x_v38'] if arm == 'v38' else f['x_v40'])
        advantage_trace.append(float(ex))
        can = bool(ep.avail[SOURCE] and (reuse or not st.seen[SOURCE]))
        if not can or ex <= 0:
            stop_reason = 'no_available_evidence' if not can else 'nonpositive_expected_advantage'; break
        actual_loss = float(resource_fast.fast_actual_loss(cache, budget, params.cost))
        vec, action = v39.evidence_and_action(ep, mode, params, st, env, used, trial)
        aa = np.zeros(int(env[8].shape[1]), np.float32); aa[action] = 1.0
        seq_hist.append(np.r_[v.softmax(vec).astype(np.float32), aa])
        st.add(SOURCE, vec, params.cost); budget = max(0.0, budget - params.cost)
        raw_cost += params.cost; opportunity_loss += actual_loss
    else:
        runaway = True; stop_reason = 'evaluator_safety_loop'
    decision, terminal_choice, terminal_q, unresolved_mass = terminal_values(st, ep, safe, a0, env, models)
    want = desired(ep, mode)
    cons = world.delayed_consensus_from_outcomes(ep, mode, params)
    return {
        'decision': int(decision), 'desired': int(want), 'correct': bool(decision == want),
        'unknown': bool(decision == -1), 'wrong_commit': bool(decision not in (-1, want)),
        'trials': len(seq_hist), 'raw_cost': raw_cost, 'opportunity_loss': opportunity_loss,
        'runaway': runaway, 'stop_reason': stop_reason, 'final_unresolved_mass': unresolved_mass,
        'final_terminal_choice': terminal_choice, 'final_expected_inspect_advantage': advantage_trace[-1] if advantage_trace else None,
        'mean_expected_inspect_advantage': float(np.mean(advantage_trace)) if advantage_trace else None,
        'consensus_evaluator_only': cons,
    }


def aggregate_rows(rows):
    out = {}
    for arm in ['terminal_only','v38','v40']:
        rr = [x for x in rows if x['arm'] == arm and x['reuse']]
        no_unique = [x for x in rr if x['mode'] in ('balanced_no_unique','biased_no_unique')]
        resolv = [x for x in rr if x['mode'] in ('stable_weak','unstable_then_stable','replacement','reversal')]
        costly = [x for x in rr if x['mode'] == 'costly_stable']
        out[arm] = {
            'n': len(rr),
            'no_unique_unknown': float(np.mean([x['unknown'] for x in no_unique])),
            'resolvable_success': float(np.mean([x['correct'] for x in resolv])),
            'costly_unknown': float(np.mean([x['unknown'] for x in costly])),
            'wrong_commit': float(np.mean([x['wrong_commit'] for x in rr])),
            'mean_trials': float(np.mean([x['trials'] for x in rr])),
            'mean_raw_cost': float(np.mean([x['raw_cost'] for x in rr])),
            'mean_opportunity_loss': float(np.mean([x['opportunity_loss'] for x in rr])),
            'runaway': float(np.mean([x['runaway'] for x in rr])),
            'replacement_success': float(np.mean([x['correct'] for x in rr if x['mode'] == 'replacement'])),
            'reversal_success': float(np.mean([x['correct'] for x in rr if x['mode'] == 'reversal'])),
            'unstable_then_stable_success': float(np.mean([x['correct'] for x in rr if x['mode'] == 'unstable_then_stable'])),
        }
    out['one_shot'] = {}
    for arm in ['v38','v40']:
        rr = [x for x in rows if x['arm'] == arm and not x['reuse']]
        no_unique = [x for x in rr if x['mode'] in ('balanced_no_unique','biased_no_unique')]
        resolv = [x for x in rr if x['mode'] in ('stable_weak','unstable_then_stable','replacement','reversal')]
        costly = [x for x in rr if x['mode'] == 'costly_stable']
        out['one_shot'][arm] = {
            'no_unique_unknown': float(np.mean([x['unknown'] for x in no_unique])),
            'resolvable_success': float(np.mean([x['correct'] for x in resolv])),
            'costly_unknown': float(np.mean([x['unknown'] for x in costly])),
            'wrong_commit': float(np.mean([x['wrong_commit'] for x in rr])),
            'mean_trials': float(np.mean([x['trials'] for x in rr])),
            'runaway': float(np.mean([x['runaway'] for x in rr])),
        }
    out['by_mode_resource'] = {}
    for arm in ['terminal_only','v38','v40']:
        out['by_mode_resource'][arm] = {}
        for mode in MODES:
            out['by_mode_resource'][arm][mode] = {}
            for ri, rname in enumerate(RESOURCE_REGIMES):
                q = [x for x in rows if x['arm'] == arm and x['reuse'] and x['mode'] == mode and x['resource_index'] == ri]
                out['by_mode_resource'][arm][mode][rname] = {
                    'n': len(q), 'correct': float(np.mean([x['correct'] for x in q])),
                    'unknown': float(np.mean([x['unknown'] for x in q])), 'wrong_commit': float(np.mean([x['wrong_commit'] for x in q])),
                    'mean_trials': float(np.mean([x['trials'] for x in q])), 'mean_opportunity_loss': float(np.mean([x['opportunity_loss'] for x in q])),
                    'runaway': float(np.mean([x['runaway'] for x in q])),
                }
    return out


def main():
    t0 = time.time(); env = r31.setup(ENV_SEED); safe = v.train_A(ENV_SEED, env); models = LiveModels()
    replay = exact_feature_replay(env, safe, models)
    if not replay['pass']:
        raise RuntimeError(f'live feature replay failed: {replay}')
    rows = []
    for mi, mode in enumerate(MODES):
        print('V41_MODE', mode, flush=True)
        for ri, rname in enumerate(RESOURCE_REGIMES):
            for j in range(N_PER_CELL):
                epseed = EVAL_SEED * 10_000_000 + mi * 500_000 + ri * 50_000 + j
                # terminal-only and reusable V38/V40 share the exact external world episode.
                for arm, reuse in [('terminal_only', True), ('v38', True), ('v40', True), ('v38', False), ('v40', False)]:
                    q = run_episode(epseed, mode, ri, arm, reuse, env, safe, models)
                    q.update({'arm': arm, 'reuse': reuse, 'mode': mode, 'resource_index': ri, 'resource_regime_evaluator_only': rname, 'episode_seed': epseed})
                    rows.append(q)
    summary = aggregate_rows(rows)
    result = {
        'experiment': 'R32 V41 live fresh-stream qualification of V40 horizon-hazard evidence acquisition',
        'feature_replay': replay,
        'config': {'environment_seed': ENV_SEED, 'fresh_evaluation_seed': EVAL_SEED, 'n_per_mode_resource': N_PER_CELL, 'episodes_per_reusable_arm': len(MODES)*len(RESOURCE_REGIMES)*N_PER_CELL, 'evaluator_safety_max': SAFETY_MAX, 'runtime_fixed_probe_count': False},
        'arms': {'terminal_only': 'retained V19 terminal COMMIT/UNKNOWN controller without extra evidence', 'v38': 'V38 repeated mean+variance INSPECT advantage plus retained terminal controller', 'v40': 'V40 horizon hazard+variance INSPECT advantage plus retained terminal controller'},
        'summary': summary,
        'rows': rows,
        'seconds': time.time() - t0,
        'training_boundary': 'All acquisition and terminal inputs are learner-visible evidence, provenance, learned resource shadow price, and delayed-trained models. Mode/resource names, delayed consensus, desired answer, and evaluator safety loop are excluded from runtime decisions.',
        'claim_boundary': 'REFERENCE_ONLY. Native Zag reproduction is required before promotion.',
    }
    outp = ROOT / 'R32_V41_LIVE_HORIZON_HAZARD_QUALIFICATION_REFERENCE_ONLY.json'; outp.write_text(json.dumps(result, indent=2))
    cfg = {'status': 'REFERENCE_ONLY_LIVE_FRESH_STREAM_QUALIFICATION', 'environment_seed': ENV_SEED, 'fresh_evaluation_seed': EVAL_SEED, 'n_per_mode_resource': N_PER_CELL, 'runtime_fixed_probe_count': False, 'native_promotion_allowed': False, 'source_sha256': sha(Path(__file__))}
    (ROOT / 'R32_V41_CONFIG.json').write_text(json.dumps(cfg, indent=2))
    (ROOT / 'R32_V41_TRAINING.log').write_text(json.dumps({'feature_replay': replay, 'summary': summary, 'seconds': result['seconds']}, indent=2) + '\n')
    (ROOT / 'R32_V41_DONE.flag').write_text('')
    print(json.dumps({'feature_replay': replay, 'summary': summary, 'seconds': result['seconds']}, indent=2), flush=True)


if __name__ == '__main__':
    main()
