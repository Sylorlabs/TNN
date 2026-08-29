from __future__ import annotations

import json, math, hashlib, sys, traceback
from pathlib import Path
from typing import Any

import joblib
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor, GradientBoostingRegressor
from sklearn.metrics import average_precision_score, mean_absolute_error, mean_squared_error, r2_score, roc_auc_score
from sklearn.model_selection import KFold, GroupKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

ROOT = Path('/mnt/data/r32_epistemic')
SEED = 9714
PREFIX = 'R32_V39'


def atomic_text(path: Path, text: str) -> None:
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(text)
    tmp.replace(path)


def atomic_json(path: Path, obj: Any) -> None:
    atomic_text(path, json.dumps(obj, indent=2, sort_keys=False))


def finite_1d(a: np.ndarray) -> bool:
    return a.ndim == 1 and np.issubdtype(a.dtype, np.number) and np.isfinite(a).all()


def locate_v38_npz() -> Path:
    candidates = sorted(ROOT.glob('*V38*.npz'), key=lambda p: p.stat().st_mtime, reverse=True)
    if not candidates:
        candidates = sorted(ROOT.glob('*v38*.npz'), key=lambda p: p.stat().st_mtime, reverse=True)
    if not candidates:
        raise FileNotFoundError('No V38 NPZ dataset found')
    return candidates[0]


def select_arrays(z: np.lib.npyio.NpzFile):
    names = list(z.files)
    arrays = {k: z[k] for k in names}
    # Feature matrix: prefer explicit X/features/state_features and largest plausible 2-D numeric array.
    x_rank = []
    for k, a in arrays.items():
        if a.ndim != 2 or not np.issubdtype(a.dtype, np.number) or a.shape[0] < 200 or a.shape[1] < 2:
            continue
        score = a.shape[0] * math.log2(a.shape[1] + 1)
        lk = k.lower()
        if lk in {'x', 'features', 'state_features', 'x_state'}: score *= 100
        elif 'feature' in lk or lk.startswith('x'): score *= 20
        x_rank.append((score, k, a))
    if not x_rank:
        raise ValueError(f'No plausible 2-D feature matrix among {names}')
    _, x_name, X = max(x_rank, key=lambda q: q[0])
    n = X.shape[0]

    # Repeated-continuation mean target.
    target_rank = []
    for k, a in arrays.items():
        if a.shape != (n,) or not finite_1d(a):
            continue
        lk = k.lower(); score = 0
        if any(w in lk for w in ('mean', 'avg', 'expected')): score += 8
        if any(w in lk for w in ('continu', 'adv', 'value', 'utility', 'target')): score += 8
        if any(w in lk for w in ('repeat', 'multi', 'rollout')): score += 7
        if any(w in lk for w in ('var', 'std', 'count', 'group', 'seed', 'split', 'mode', 'kind', 'label')): score -= 12
        # Advantage/utility should normally straddle zero.
        if np.min(a) < 0 < np.max(a): score += 5
        score += min(3, float(np.std(a)))
        target_rank.append((score, k, a.astype(float)))
    if not target_rank:
        raise ValueError('No 1-D numeric target aligned to feature matrix')
    target_rank.sort(reverse=True, key=lambda q: q[0])
    score, y_name, y = target_rank[0]
    if score < 5:
        raise ValueError(f'Target selection ambiguous: top candidates {[(s,k) for s,k,_ in target_rank[:8]]}')

    # Variance / standard-error target if present.
    var_name = None; yvar = None
    vrank = []
    for k, a in arrays.items():
        if a.shape != (n,) or not finite_1d(a) or k == y_name: continue
        lk = k.lower(); score = 0
        if 'var' in lk: score += 12
        if 'std' in lk or 'sigma' in lk: score += 8
        if any(w in lk for w in ('continu', 'repeat', 'rollout', 'adv', 'utility', 'value')): score += 5
        if np.min(a) >= 0: score += 2
        vrank.append((score, k, a.astype(float)))
    if vrank and max(vrank)[0] >= 8:
        _, var_name, yvar = max(vrank, key=lambda q: q[0])
        if 'std' in var_name.lower() or 'sigma' in var_name.lower(): yvar = yvar ** 2

    # Group identifier for leakage-resistant cross-fitting.
    group_name = None; groups = None
    grank = []
    for k, a in arrays.items():
        if a.shape != (n,) or k in {y_name, var_name}: continue
        lk = k.lower()
        if any(w in lk for w in ('group', 'episode', 'state_id', 'trace_id', 'history_id', 'base_id')):
            uniq = len(np.unique(a))
            if 5 <= uniq < n:
                grank.append((uniq, k, a))
    if grank:
        _, group_name, groups = max(grank, key=lambda q: q[0])

    # Optional single-continuation target for explicit noise comparison.
    single_name = None; ysingle = None
    srank = []
    for k, a in arrays.items():
        if a.shape != (n,) or not finite_1d(a) or k in {y_name, var_name}: continue
        lk = k.lower(); score = 0
        if any(w in lk for w in ('single', 'one_', 'realized')): score += 8
        if any(w in lk for w in ('adv', 'value', 'utility', 'target')): score += 6
        if np.min(a) < 0 < np.max(a): score += 3
        srank.append((score, k, a.astype(float)))
    if srank and max(srank)[0] >= 8:
        _, single_name, ysingle = max(srank, key=lambda q: q[0])

    return {
        'X_name': x_name, 'X': X.astype(np.float32), 'y_name': y_name, 'y': y,
        'var_name': var_name, 'yvar': yvar, 'group_name': group_name, 'groups': groups,
        'single_name': single_name, 'ysingle': ysingle,
        'schema': {k: {'shape': list(a.shape), 'dtype': str(a.dtype)} for k,a in arrays.items()},
        'target_candidates': [(float(s), k) for s,k,_ in target_rank[:12]],
    }


def folds(n: int, groups: np.ndarray | None):
    if groups is not None and len(np.unique(groups)) >= 5:
        return list(GroupKFold(n_splits=5).split(np.arange(n), groups=groups))
    return list(KFold(n_splits=5, shuffle=True, random_state=SEED).split(np.arange(n)))


def metric_block(y: np.ndarray, pred: np.ndarray, name: str):
    truth = y > 0
    select = pred > 0
    tp = np.sum(select & truth); fp = np.sum(select & ~truth)
    fn = np.sum(~select & truth); tn = np.sum(~select & ~truth)
    oracle = np.maximum(y, 0)
    realized = np.where(select, y, 0)
    regret = oracle - realized
    out = {
        'name': name,
        'mse': float(mean_squared_error(y, pred)),
        'mae': float(mean_absolute_error(y, pred)),
        'r2': float(r2_score(y, pred)),
        'positive_prevalence': float(np.mean(truth)),
        'selection_rate': float(np.mean(select)),
        'true_positive_crossing': float(tp / max(1, tp + fn)),
        'false_positive_crossing': float(fp / max(1, fp + tn)),
        'precision_positive': float(tp / max(1, tp + fp)),
        'selected_realized_value': float(np.mean(y[select])) if np.any(select) else 0.0,
        'mean_policy_incremental_utility': float(np.mean(realized)),
        'mean_oracle_incremental_utility': float(np.mean(oracle)),
        'mean_policy_regret': float(np.mean(regret)),
        'p95_regret': float(np.quantile(regret, .95)),
    }
    if len(np.unique(truth)) == 2:
        out['roc_auc_as_score'] = float(roc_auc_score(truth, pred))
        out['average_precision_as_score'] = float(average_precision_score(truth, pred))
    return out


def main():
    npz = locate_v38_npz(); z = np.load(npz, allow_pickle=True); s = select_arrays(z)
    X, y, groups = s['X'], s['y'], s['groups']; n = len(y)
    cv = folds(n, groups)
    oof_mean = np.zeros(n); oof_cls = np.zeros(n); oof_pos = np.zeros(n); oof_non = np.zeros(n)
    oof_q10 = np.zeros(n); oof_q50 = np.zeros(n); oof_q90 = np.zeros(n)
    fold_meta=[]
    for fi,(tr,te) in enumerate(cv):
        # Direct repeated-mean regression.
        mean = HistGradientBoostingRegressor(max_iter=180, max_leaf_nodes=31, min_samples_leaf=35,
                                             l2_regularization=1.0, learning_rate=.045,
                                             random_state=SEED+fi).fit(X[tr], y[tr])
        oof_mean[te] = mean.predict(X[te])
        cls = HistGradientBoostingClassifier(max_iter=160, max_leaf_nodes=23, min_samples_leaf=35,
                                             l2_regularization=1.0, learning_rate=.045,
                                             random_state=SEED+100+fi).fit(X[tr], y[tr] > 0)
        p = cls.predict_proba(X[te])[:,1]; oof_cls[te]=p
        posmask = y[tr] > 0
        nonmask = ~posmask
        pos = HistGradientBoostingRegressor(max_iter=160, max_leaf_nodes=23, min_samples_leaf=25,
                                            l2_regularization=1.2, learning_rate=.045,
                                            random_state=SEED+200+fi).fit(X[tr][posmask], y[tr][posmask])
        non = HistGradientBoostingRegressor(max_iter=160, max_leaf_nodes=23, min_samples_leaf=30,
                                            l2_regularization=1.2, learning_rate=.045,
                                            random_state=SEED+300+fi).fit(X[tr][nonmask], y[tr][nonmask])
        oof_pos[te]=pos.predict(X[te]);oof_non[te]=non.predict(X[te])
        # Quantile family estimates continuation distribution rather than a point label.
        for alpha,store in [(.10,oof_q10),(.50,oof_q50),(.90,oof_q90)]:
            q = make_pipeline(StandardScaler(), GradientBoostingRegressor(loss='quantile', alpha=alpha,
                n_estimators=160, max_depth=3, min_samples_leaf=25, learning_rate=.035,
                random_state=SEED+400+fi+int(alpha*100))).fit(X[tr],y[tr])
            store[te]=q.predict(X[te])
        fold_meta.append({'fold':fi,'train':len(tr),'test':len(te),'train_positive':float(np.mean(y[tr]>0))})

    mixture = oof_cls*oof_pos + (1-oof_cls)*oof_non
    spread = np.maximum(0., oof_q90-oof_q10)
    # Distributional conservative expected value: shrink only in proportion to learned continuation spread.
    # This is an action value, not a confidence threshold or probe count.
    dist_value = mixture - 0.18*spread
    # Mean plus variance feature candidate: variance is learned from repeated outcomes, not evaluator mode.
    if s['yvar'] is not None:
        # Fit variance cross-fitted and use expected downside magnitude from learned variance.
        oof_var=np.zeros(n)
        for fi,(tr,te) in enumerate(cv):
            vm=HistGradientBoostingRegressor(max_iter=140,max_leaf_nodes=23,min_samples_leaf=35,
                l2_regularization=1.2,learning_rate=.045,random_state=SEED+700+fi).fit(X[tr],np.log1p(np.maximum(0,s['yvar'][tr])))
            oof_var[te]=np.expm1(vm.predict(X[te])).clip(0)
        mean_var_value=oof_mean-0.18*np.sqrt(oof_var)
    else:
        oof_var=None;mean_var_value=oof_mean-0.18*spread/2.563 # 10-90 Gaussian width

    methods = {
        'direct_repeated_mean': oof_mean,
        'probability_magnitude_mixture': mixture,
        'distributional_spread_value': dist_value,
        'mean_variance_value': mean_var_value,
        'quantile_median': oof_q50,
        'quantile_lower_10': oof_q10,
        'exact_repeated_experience_ceiling': y.copy(),
    }
    metrics={k:metric_block(y,v,k) for k,v in methods.items()}
    # Explicit target-noise diagnostic if a single-continuation label exists.
    noise=None
    if s['ysingle'] is not None:
        noise={
            'single_target_name':s['single_name'],
            'repeated_target_name':s['y_name'],
            'single_vs_repeated_mse':float(mean_squared_error(y,s['ysingle'])),
            'single_vs_repeated_sign_disagreement':float(np.mean((s['ysingle']>0)!=(y>0))),
            'single_target_variance':float(np.var(s['ysingle'])),
            'repeated_target_variance':float(np.var(y)),
        }

    # Train deployable full-data versions of retained candidates.
    full_mean=HistGradientBoostingRegressor(max_iter=180,max_leaf_nodes=31,min_samples_leaf=35,l2_regularization=1.0,learning_rate=.045,random_state=SEED).fit(X,y)
    full_cls=HistGradientBoostingClassifier(max_iter=160,max_leaf_nodes=23,min_samples_leaf=35,l2_regularization=1.0,learning_rate=.045,random_state=SEED+100).fit(X,y>0)
    pm=y>0
    full_pos=HistGradientBoostingRegressor(max_iter=160,max_leaf_nodes=23,min_samples_leaf=25,l2_regularization=1.2,learning_rate=.045,random_state=SEED+200).fit(X[pm],y[pm])
    full_non=HistGradientBoostingRegressor(max_iter=160,max_leaf_nodes=23,min_samples_leaf=30,l2_regularization=1.2,learning_rate=.045,random_state=SEED+300).fit(X[~pm],y[~pm])
    for name,m in [('MEAN',full_mean),('BENEFIT_CLASSIFIER',full_cls),('POSITIVE_MAGNITUDE',full_pos),('NONPOSITIVE_MAGNITUDE',full_non)]:
        joblib.dump(m,ROOT/f'{PREFIX}_{name}_SEED_{SEED}.joblib',compress=3)

    best_name=max([k for k in methods if k!='exact_repeated_experience_ceiling'],
                  key=lambda k: metrics[k]['mean_policy_incremental_utility']-0.5*metrics[k]['mean_policy_regret'])
    result={
        'experiment':'R32 V39 cross-fitted distributional repeated-continuation INSPECT value',
        'source_dataset':npz.name,
        'selected_arrays':{k:s[k] for k in ['X_name','y_name','var_name','group_name','single_name']},
        'schema':s['schema'],'target_candidates':s['target_candidates'],'rows':n,'feature_dim':X.shape[1],
        'folds':fold_meta,'metrics':metrics,'target_noise':noise,'best_nonoracle_method':best_name,
        'best_nonoracle_metrics':metrics[best_name],
        'boundary':'REFERENCE_ONLY. Inputs are inherited persistent epistemic/candidate-support features. Targets are repeated delayed grounded-continuation utilities and experienced resource opportunity losses. No ambiguity, generator mode, evaluator state, fixed confidence threshold, or fixed probe count enters learner cognition. R27 remains canonical; native Zag reproduction is mandatory.'
    }
    atomic_json(ROOT/f'{PREFIX}_DISTRIBUTIONAL_CONTINUATION_VALUE_REFERENCE_ONLY.json',result)
    config={
        'status':'REFERENCE_ONLY_COMPONENT_EVALUATION', 'seed':SEED,
        'change_only':'replace noisy single-continuation action credit with cross-fitted distributional repeated-continuation value; retained representation/action set/cost model unchanged',
        'runtime_fixed_threshold':False,'runtime_fixed_probe_count':False,'native_promotion_allowed':False,
        'source_v38_dataset':npz.name,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    atomic_json(ROOT/f'{PREFIX}_CONFIG.json',config)

    b=metrics[best_name]; c=metrics['exact_repeated_experience_ceiling']; d=metrics['direct_repeated_mean']
    causal='TARGET_NOISE_REPAIR_SUPPORTED' if b['mean_policy_regret'] < .85*d['mean_policy_regret'] else 'TARGET_NOISE_REPAIR_NOT_CONFIRMED'
    gap=b['mean_policy_regret']-c['mean_policy_regret']
    interp=f'''# R32 V39 — Distributional Repeated-Continuation Value\n\nStatus: **REFERENCE_ONLY / {causal}**\n\nV39 held the retained candidate-support representation, learned resource shadow price, evidence action, and delayed-regret objective fixed. It changed only the INSPECT credit target from one sampled continuation to a cross-fitted distribution over repeated delayed grounded continuations.\n\n## Result\n\nThe best non-oracle method was **{best_name}**.\n\n- true-benefit crossing: **{b['true_positive_crossing']:.4f}**\n- false-positive crossing: **{b['false_positive_crossing']:.4f}**\n- selected realized value: **{b['selected_realized_value']:.4f}**\n- mean policy incremental utility: **{b['mean_policy_incremental_utility']:.4f}**\n- mean policy regret: **{b['mean_policy_regret']:.6f}**\n\nDirect repeated-mean regression regret was **{d['mean_policy_regret']:.6f}**. The exact repeated-experience ceiling regret is **{c['mean_policy_regret']:.6f}**; the remaining learned-to-ceiling gap is **{gap:.6f}**.\n\n## Causal classification\n\n**{causal.replace('_',' ').title()}.** This is a training-target/credit-noise test, not an architecture redesign. The retained temporal/provenance hypothesis population remains unchanged.\n\n## Decision rule for the next run\n\n- If the learned distributional method closes most of the exact-ceiling gap while lowering false positives, retain it and run a live forced reusable-probe hardening battery.\n- If the exact ceiling remains substantially stronger, the next causal arm must improve observable-state matching or preserve additional future-dynamics evidence; do not tune a confidence threshold.\n\nR27 remains canonical. Native Zag execution remains mandatory before promotion.\n'''
    atomic_text(ROOT/f'R32_EPISTEMIC_R31_MATCHED_V39_INTERPRETATION.md',interp)
    names=[Path(__file__).name,f'{PREFIX}_CONFIG.json',f'{PREFIX}_DISTRIBUTIONAL_CONTINUATION_VALUE_REFERENCE_ONLY.json',f'R32_EPISTEMIC_R31_MATCHED_V39_INTERPRETATION.md']+[f'{PREFIX}_{q}_SEED_{SEED}.joblib' for q in ['MEAN','BENEFIT_CLASSIFIER','POSITIVE_MAGNITUDE','NONPOSITIVE_MAGNITUDE']]
    sha='\n'.join(f'{hashlib.sha256((ROOT/n).read_bytes()).hexdigest()}  {n}' for n in names if (ROOT/n).exists())+'\n'
    atomic_text(ROOT/f'{PREFIX}_SHA256.txt',sha)
    print(json.dumps({'status':causal,'best':best_name,'metrics':b,'exact':c,'target_noise':noise},indent=2),flush=True)


if __name__=='__main__':
    try: main()
    except Exception as e:
        err={'status':'FAILED','error':repr(e),'traceback':traceback.format_exc()}
        atomic_json(ROOT/f'{PREFIX}_FAILED.json',err)
        print(json.dumps(err,indent=2),file=sys.stderr,flush=True)
        raise
