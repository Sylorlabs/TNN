from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path
from typing import Any

import joblib
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, brier_score_loss, mean_absolute_error, mean_squared_error, roc_auc_score

ROOT=Path('/mnt/data/r32_epistemic')
sys.path[:0]=['/mnt/data/r31_part2',str(ROOT)]
import r31_sequential_evidence_abstention_REFERENCE_ONLY as r31
import r32_epistemic_r31_matched_v17_cached_REFERENCE_ONLY as v
import r32_v26_candidate_selected_conditional_advantage as e
import r32_v28_learned_resource_shadow_price as r
import r32_v28_complete_from_checkpoint as rf

SEED=9714
SOURCE=7
TRIALS=12
EPISODES_PER_MODE_RESOURCE=70
MODES=e.MODES
RESOURCE_REGIMES=r.RESOURCE_REGIMES


def safe_logit(p):
 q=np.clip(p,1e-6,1-1e-6);return np.log(q/(1-q)).reshape(-1,1)


def split_code(mode_i,resource_i,j):return int((j*7+mode_i*3+resource_i*5)%10)

def action_feature_base(st,ep,safe,a0,env,raw_cost,resource_feat):
 q=v.q_feat(st,ep,safe,a0,env)
 return np.r_[q,np.eye(v.S)[SOURCE],raw_cost,st.group_n[v.GROUP[SOURCE]]/3,resource_feat]


def generate():
 t0=time.time();env=r31.setup(SEED);safe=v.train_A(SEED,env);shadow=joblib.load(ROOT/'R32_V28_RESOURCE_SHADOW_MODEL_SEED_9714.joblib')
 Xbase=[];resource_features=[];adv=[];episode=[];split=[];mode_meta=[];resource_meta=[];trial_meta=[];actual_cost_meta=[];raw_cost_meta=[];cons_meta=[]
 eid=0;stats={}
 for mi,mode in enumerate(MODES):
  print('V29_GENERATE',mode,flush=True);vals=[]
  for ri,rname in enumerate(RESOURCE_REGIMES):
   for j in range(EPISODES_PER_MODE_RESOURCE):
    epseed=SEED*4_000_000+mi*300_000+ri*50_000+j
    ep=v.make_ep(epseed,'genuine_ambiguity',env);ep.avail[:]=False;ep.avail[0]=ep.avail[1]=ep.avail[SOURCE]=True
    params=e.world_params(epseed,mode);ep.cost[SOURCE]=params.cost;cons=e.delayed_consensus_from_outcomes(ep,mode,params)
    ctx=r.draw_context(SEED*50_000_000+mi*4_000_000+ri*500_000+j*53+23,ri);cache=rf.context_cache(ctx);budget=ctx.budget
    st=v.initial_state(ep,env,'D');a0=int(env[5][int(np.argmax(st.p(True)))]);used=[];path=[]
    for trial in range(TRIALS):
     cur=e.terminal_utility(st,a0,cons,env);resf=rf.fast_feature(ctx,cache,budget,params.cost);actual_cost=rf.fast_actual_loss(cache,budget,params.cost)
     feat=action_feature_base(st,ep,safe,a0,env,params.cost,resf);ev=e.source7_observation(ep,mode,params,st,env,used,trial);z=st.clone();z.add(SOURCE,ev,params.cost);nxt=e.terminal_utility(z,a0,cons,env)
     path.append((feat,resf,cur,nxt,actual_cost,params.cost,trial));st=z;budget=max(0.,budget-params.cost)
    cont=-1e9;local=[]
    for feat,resf,cur,nxt,actual_cost,raw_cost,trial in reversed(path):
     ret=max(nxt,cont)-actual_cost;local.append((feat,resf,float(ret-cur),actual_cost,raw_cost,trial));cont=ret
    local.reverse();sc=split_code(mi,ri,j)
    for feat,resf,a,ac,rc,tr in local:
     Xbase.append(feat);resource_features.append(resf);adv.append(a);episode.append(eid);split.append(sc);mode_meta.append(mi);resource_meta.append(ri);trial_meta.append(tr);actual_cost_meta.append(ac);raw_cost_meta.append(rc);cons_meta.append(int(cons is not None));vals.append(a)
    eid+=1
  q=np.asarray(vals);stats[mode]={'rows':len(q),'positive_rate':float(np.mean(q>0)),'mean_advantage':float(q.mean())}
 shadow_costs=np.maximum(0.,shadow.predict(np.asarray(resource_features)))
 data={'X':np.c_[np.asarray(Xbase,np.float32),shadow_costs.astype(np.float32)],'advantage':np.asarray(adv,np.float32),'episode_id':np.asarray(episode,np.int32),'split_code':np.asarray(split,np.int8),'mode_evaluator_only':np.asarray(mode_meta,np.int8),'resource_regime_evaluator_only':np.asarray(resource_meta,np.int8),'trial_index':np.asarray(trial_meta,np.int8),'actual_opportunity_loss':np.asarray(actual_cost_meta,np.float32),'predicted_shadow_cost':shadow_costs.astype(np.float32),'raw_cost':np.asarray(raw_cost_meta,np.float32),'delayed_consensus_evaluator_only':np.asarray(cons_meta,np.int8)}
 meta={'seed':SEED,'episodes':eid,'episodes_per_mode_resource':EPISODES_PER_MODE_RESOURCE,'rows':len(adv),'feature_dim':data['X'].shape[1],'positive_rate':float(np.mean(data['advantage']>0)),'mode_stats':stats,'seconds':time.time()-t0,'learner_inputs':'persistent epistemic state, source/provenance, raw cost, observed budget/history features, learned shadow cost','forbidden_inputs':'epistemic mode, resource regime, ambiguity label, future opportunities, final answer, fixed probe count'}
 return data,meta


def fit(data):
 X=data['X'];a=data['advantage'].astype(float);y=(a>0).astype(int);s=data['split_code'];tr=s<=5;ca=(s==6)|(s==7);te=s>=8
 clf=HistGradientBoostingClassifier(random_state=29029,max_iter=210,max_leaf_nodes=27,min_samples_leaf=26,l2_regularization=1.,learning_rate=.05).fit(X[tr],y[tr]);rawca=clf.predict_proba(X[ca])[:,1];pl=LogisticRegression(max_iter=1000).fit(safe_logit(rawca),y[ca])
 pos=HistGradientBoostingRegressor(random_state=29030,max_iter=190,max_leaf_nodes=23,min_samples_leaf=20,l2_regularization=.8,learning_rate=.05).fit(X[tr&(y==1)],a[tr&(y==1)])
 neg=HistGradientBoostingRegressor(random_state=29031,max_iter=190,max_leaf_nodes=23,min_samples_leaf=28,l2_regularization=1.,learning_rate=.05).fit(X[tr&(y==0)],a[tr&(y==0)])
 raw=clf.predict_proba(X[te])[:,1];p=pl.predict_proba(safe_logit(raw))[:,1];qp=pos.predict(X[te]);qn=neg.predict(X[te]);ex=p*qp+(1-p)*qn;yt=y[te];at=a[te]
 out={'rows':{'train':int(tr.sum()),'calibration':int(ca.sum()),'test':int(te.sum())},'positive_rate':{'train':float(y[tr].mean()),'calibration':float(y[ca].mean()),'test':float(yt.mean())},'classifier':{'roc_auc':float(roc_auc_score(yt,p)),'average_precision':float(average_precision_score(yt,p)),'brier':float(brier_score_loss(yt,p))},'conditional':{'positive_mae':float(mean_absolute_error(at[yt==1],qp[yt==1])),'negative_mae':float(mean_absolute_error(at[yt==0],qn[yt==0])),'mean_positive_component_actual_positive':float(qp[yt==1].mean()),'mean_negative_component_actual_nonpositive':float(qn[yt==0].mean())},'expected_advantage':{'mse':float(mean_squared_error(at,ex)),'mae':float(mean_absolute_error(at,ex)),'roc_auc':float(roc_auc_score(yt,ex)),'mean_actual_positive':float(ex[yt==1].mean()),'mean_actual_nonpositive':float(ex[yt==0].mean()),'true_positive_cross_zero':float(np.mean(ex[yt==1]>0)),'false_positive_cross_zero':float(np.mean(ex[yt==0]>0)),'predicted_inspect_rate':float(np.mean(ex>0))},'by_resource_regime_evaluator_only':{},'by_mode_evaluator_only':{}}
 rr=data['resource_regime_evaluator_only'][te];mm=data['mode_evaluator_only'][te]
 for i,name in enumerate(RESOURCE_REGIMES):
  q=rr==i;out['by_resource_regime_evaluator_only'][name]={'n':int(q.sum()),'actual_positive_rate':float(yt[q].mean()),'predicted_inspect_rate':float(np.mean(ex[q]>0)),'true_positive_cross_zero':float(np.mean(ex[q&(yt==1)]>0)) if np.any(q&(yt==1)) else None,'false_positive_cross_zero':float(np.mean(ex[q&(yt==0)]>0)) if np.any(q&(yt==0)) else None,'mean_expected_advantage':float(ex[q].mean()),'mean_actual_advantage':float(at[q].mean())}
 for i,name in enumerate(MODES):
  q=mm==i;out['by_mode_evaluator_only'][name]={'n':int(q.sum()),'actual_positive_rate':float(yt[q].mean()),'predicted_inspect_rate':float(np.mean(ex[q]>0)),'true_positive_cross_zero':float(np.mean(ex[q&(yt==1)]>0)) if np.any(q&(yt==1)) else None,'false_positive_cross_zero':float(np.mean(ex[q&(yt==0)]>0)) if np.any(q&(yt==0)) else None,'mean_expected_advantage':float(ex[q].mean()),'mean_actual_advantage':float(at[q].mean())}
 return {'classifier':clf,'calibrator':pl,'positive':pos,'nonpositive':neg},out


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
 data,meta=generate();dp=ROOT/'R32_V29_RESOURCE_GROUNDED_INSPECT_DATA_SEED_9714.npz';np.savez_compressed(dp,**data);models,val=fit(data);files={}
 for n,m in models.items():
  p=ROOT/f'R32_V29_{n.upper()}_SEED_9714.joblib';joblib.dump(m,p,compress=3);files[n]={'file':p.name,'sha256':sha(p)}
 val['dataset']=meta;val['dataset']['sha256']=sha(dp);val['models']=files;val['v26_reference']={'positive_rate':.05454545454545454,'auc':.8716440384581418,'mean_expected_on_positive':-.25691878452581307,'true_positive_cross_zero':.015463917525773196,'false_positive_cross_zero':.0031410622501427754};val['claim_boundary']='REFERENCE_ONLY. Advantage target subtracts actual delayed resource opportunity loss. Resource regime/future opportunities and epistemic generator mode are evaluator-only.'
 (ROOT/'R32_V29_RESOURCE_GROUNDED_ADVANTAGE_VALIDATION.json').write_text(json.dumps(val,indent=2));cfg={'status':'REFERENCE_ONLY_VALIDATION','seed':SEED,'resource_shadow_model_sha256':sha(ROOT/'R32_V28_RESOURCE_SHADOW_MODEL_SEED_9714.joblib'),'runtime_fixed_multiplier':False,'native_promotion_allowed':False,'source_sha256':sha(Path(__file__))};(ROOT/'R32_V29_CONFIG.json').write_text(json.dumps(cfg,indent=2));summary={'positive_rate':meta['positive_rate'],**val['classifier'],**val['expected_advantage']};(ROOT/'R32_V29_TRAINING.log').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
