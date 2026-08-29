from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path
from typing import Any

import joblib
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

ROOT = Path('/mnt/data/r32_epistemic')
sys.path[:0] = ['/mnt/data/r31_part2', str(ROOT)]
import r32_v28_learned_resource_shadow_price as base


def table(cost: np.ndarray, reward: np.ndarray, max_budget: float) -> np.ndarray:
    cap = max(0, int(round(float(max_budget) / base.UNIT)))
    dp = np.zeros(cap + 1, dtype=float)
    for c, u in zip(cost, reward):
        w = max(1, int(round(float(c) / base.UNIT)))
        if w <= cap:
            dp[w:] = np.maximum(dp[w:], dp[:-w] + float(u))
    return dp


def lookup(dp: np.ndarray, budget: float) -> float:
    i = min(len(dp) - 1, max(0, int(round(float(budget) / base.UNIT))))
    return float(dp[i])


def context_cache(ctx: base.ResourceContext) -> dict[str, Any]:
    c = ctx.history_cost
    r = ctx.history_reward
    density = r / np.maximum(c, 1e-6)
    recent_n = min(5, len(c))
    return {
        'n': len(c),
        'cmean': float(np.mean(c)), 'cstd': float(np.std(c)), 'cmin': float(np.min(c)), 'cmax': float(np.max(c)),
        'cq': np.quantile(c, [0.25, 0.50, 0.75]).astype(float),
        'rmean': float(np.mean(r)), 'rstd': float(np.std(r)), 'rmin': float(np.min(r)), 'rmax': float(np.max(r)),
        'rq': np.quantile(r, [0.25, 0.50, 0.75]).astype(float),
        'dmean': float(np.mean(density)), 'dstd': float(np.std(density)), 'dmax': float(np.max(density)),
        'sumc': float(np.sum(c)), 'sumr': float(np.sum(r)),
        'recent_c': float(np.mean(c[-recent_n:])), 'recent_r': float(np.mean(r[-recent_n:])),
        'hist_dp': table(c, r, ctx.budget),
        'future_dp': table(ctx.future_cost, ctx.future_reward, ctx.budget),
    }


def fast_feature(ctx: base.ResourceContext, cache: dict[str, Any], budget: float, action_cost: float) -> np.ndarray:
    hv = lookup(cache['hist_dp'], budget)
    ha = lookup(cache['hist_dp'], max(0.0, budget - action_cost))
    hl = max(0.0, hv - ha)
    return np.asarray([
        action_cost, budget, action_cost / max(budget, 1e-6), cache['n'] / 20.0,
        cache['cmean'], cache['cstd'], cache['cmin'], cache['cmax'], *cache['cq'],
        cache['rmean'], cache['rstd'], cache['rmin'], cache['rmax'], *cache['rq'],
        cache['dmean'], cache['dstd'], cache['dmax'], cache['sumc'] / max(budget, 1e-6), cache['sumr'],
        float(np.mean(ctx.history_cost <= budget)), cache['recent_c'], cache['recent_r'], hv, hl, hl / max(action_cost, 1e-6),
    ], dtype=float)


def fast_actual_loss(cache: dict[str, Any], budget: float, action_cost: float) -> float:
    before = lookup(cache['future_dp'], budget)
    after = lookup(cache['future_dp'], max(0.0, budget - action_cost))
    return max(0.0, before - after)


def validation_from_checkpoint(data: Any, model: Any) -> dict[str, Any]:
    test = data['split_code'] >= 8
    train = data['split_code'] <= 7
    X = data['X']; y = data['opportunity_loss'].astype(float); c = data['raw_cost'].astype(float)
    pred = np.maximum(0.0, model.predict(X[test])); yt = y[test]; ct = c[test]
    alpha = float(np.dot(c[train], y[train]) / max(1e-12, np.dot(c[train], c[train])))
    out = {
        'rows': {'train': int(np.sum(train)), 'test': int(np.sum(test))}, 'feature_dim': int(X.shape[1]),
        'adaptive_model': {'mse': float(mean_squared_error(yt,pred)), 'mae': float(mean_absolute_error(yt,pred)), 'r2': float(r2_score(yt,pred)), 'mean_predicted_loss': float(np.mean(pred)), 'mean_actual_loss': float(np.mean(yt))},
        'baselines': {
            'raw_scale_1_0': {'mse': float(mean_squared_error(yt,ct)), 'mae': float(mean_absolute_error(yt,ct))},
            'audit_scale_0_55': {'mse': float(mean_squared_error(yt,.55*ct)), 'mae': float(mean_absolute_error(yt,.55*ct))},
            'learned_global_scalar': {'alpha':alpha,'mse':float(mean_squared_error(yt,alpha*ct)),'mae':float(mean_absolute_error(yt,alpha*ct))},
        }, 'by_regime_evaluator_only': {}, 'by_budget_pressure_quintile': []}
    rr=data['regime_evaluator_only'][test]
    for i,name in enumerate(base.RESOURCE_REGIMES):
        m=rr==i
        out['by_regime_evaluator_only'][name]={'n':int(np.sum(m)),'mean_actual_loss':float(np.mean(yt[m])),'mean_predicted_loss':float(np.mean(pred[m])),'mean_actual_multiplier':float(np.mean(yt[m]/np.maximum(ct[m],1e-6))),'mean_predicted_multiplier':float(np.mean(pred[m]/np.maximum(ct[m],1e-6))),'mae':float(mean_absolute_error(yt[m],pred[m]))}
    pressure=X[test,2];order=np.argsort(pressure)
    for q,ids in enumerate(np.array_split(order,5)):
        out['by_budget_pressure_quintile'].append({'quintile':q,'n':int(len(ids)),'mean_cost_over_budget':float(np.mean(pressure[ids])),'mean_actual_multiplier':float(np.mean(yt[ids]/np.maximum(ct[ids],1e-6))),'mean_predicted_multiplier':float(np.mean(pred[ids]/np.maximum(ct[ids],1e-6))),'mae':float(mean_absolute_error(yt[ids],pred[ids]))})
    return out


def fast_apply(model: Any, rows: list[dict[str, Any]]) -> dict[str, Any]:
    arms=['raw_1_0','fixed_0_55','learned_shadow'];by={};pooled=[]
    for ridx,rname in enumerate(base.RESOURCE_REGIMES):
        feats=[];episodes=[]
        for j,row in enumerate(rows):
            ctx=base.draw_context(base.SEED*30_000_000+ridx*1_000_000+j*43+19,ridx);cache=context_cache(ctx);budget=ctx.budget;actual=[];raw=[]
            start=len(feats)
            for _,_,cost in row['path']:
                feats.append(fast_feature(ctx,cache,budget,cost));actual.append(fast_actual_loss(cache,budget,cost));raw.append(cost);budget=max(0.0,budget-cost)
            episodes.append((row,start,len(feats),actual,raw))
        pred=np.maximum(0.0,model.predict(np.asarray(feats)))
        rec=[]
        for row,s,e,actual,raw in episodes:
            predicted=pred[s:e].tolist();actual_adv,_=base.backward_advantage(row['path'],actual)
            rec.append({'mode':row['mode'],'need':row['need'],'actual_advantage':actual_adv,'predicted_advantage':{
                'raw_1_0':base.backward_advantage(row['path'],raw)[0],
                'fixed_0_55':base.backward_advantage(row['path'],[.55*x for x in raw])[0],
                'learned_shadow':base.backward_advantage(row['path'],predicted)[0]}})
        by[rname]=base.summarize_decisions(rec,arms);pooled.extend(rec);print('APPLICATION_DONE',rname,flush=True)
    return {'by_resource_regime_evaluator_only':by,'pooled':base.summarize_decisions(pooled,arms)}


def sha(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    t0=time.time();data=np.load(ROOT/'R32_V28_RESOURCE_SHADOW_DATA_SEED_9714.npz');model=joblib.load(ROOT/'R32_V28_RESOURCE_SHADOW_MODEL_SEED_9714.joblib');validation=validation_from_checkpoint(data,model)
    _,_,rows=base.build_epistemic_paths();application=fast_apply(model,rows)
    result={'experiment':'R32 V28 learned resource shadow price from delayed opportunity loss','validation':validation,'epistemic_cost_application_audit':application,'meta':{'resource_episodes':base.N_RESOURCE_EPISODES,'resource_regimes_evaluator_only':base.RESOURCE_REGIMES,'epistemic_modes_evaluator_only':base.EPISTEMIC_MODES,'epistemic_episodes_per_mode':120,'runtime_fixed_cost_multiplier':False,'learner_features_exclude_resource_regime':True,'target':'delayed optimal future opportunity value before spending minus after spending','seconds':time.time()-t0,'dataset_sha256':sha(ROOT/'R32_V28_RESOURCE_SHADOW_DATA_SEED_9714.npz'),'model_sha256':sha(ROOT/'R32_V28_RESOURCE_SHADOW_MODEL_SEED_9714.joblib')},'claim_boundary':'REFERENCE_ONLY component qualification. Hidden resource regime and future opportunity list are excluded from learner input. Epistemic application holds evidence trajectories fixed and audits cost conversion; it is not a promoted runtime policy.'}
    (ROOT/'R32_V28_RESOURCE_SHADOW_PRICE_REFERENCE_ONLY.json').write_text(json.dumps(result,indent=2))
    config={'status':'REFERENCE_ONLY_RESOURCE_SHADOW_COMPONENT_COMPLETE','seed':base.SEED,'resource_episodes':base.N_RESOURCE_EPISODES,'runtime_fixed_multiplier':False,'native_promotion_allowed':False,'source_sha256':sha(Path(__file__)),'base_source_sha256':sha(ROOT/'r32_v28_learned_resource_shadow_price.py')}
    (ROOT/'R32_V28_CONFIG.json').write_text(json.dumps(config,indent=2))
    summary={'adaptive_validation':validation['adaptive_model'],'baselines':validation['baselines'],'pooled_epistemic_application':application['pooled']};(ROOT/'R32_V28_TRAINING.log').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
