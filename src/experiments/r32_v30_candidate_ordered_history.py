from __future__ import annotations

import hashlib
import json
import math
import sys
import time
from pathlib import Path

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
import r32_v29_resource_grounded_inspect_advantage as b

SEED=b.SEED
SOURCE=b.SOURCE
TRIALS=b.TRIALS
EPISODES_PER_MODE_RESOURCE=b.EPISODES_PER_MODE_RESOURCE
MODES=b.MODES
RESOURCE_REGIMES=b.RESOURCE_REGIMES


def safe_logit(p):
 q=np.clip(p,1e-6,1-1e-6);return np.log(q/(1-q)).reshape(-1,1)


def tv(a,b):return .5*float(np.abs(a-b).sum())


def seq_stats(vals):
 x=np.asarray(vals,float)
 if len(x)==0:return [0.,0.,0.,0.,0.,0.]
 return [float(x[-1]),float(x.mean()),float(x.std()),float(x[-1]-x[0]),float(np.min(x)),float(np.max(x))]


def discrete_entropy(seq,denom):
 if not seq:return 0.
 _,cnt=np.unique(np.asarray(seq,int),return_counts=True);p=cnt/cnt.sum()
 return float(-(p*np.log(p+1e-12)).sum()/max(1e-12,math.log(max(2,denom))))


def run_features(tops):
 if not tops:return [0.,0.,0.,0.,0.]
 n=len(tops);switch=sum(a!=b for a,b in zip(tops[:-1],tops[1:]))/max(1,n-1)
 ret=sum(tops[i]==tops[i-2] and tops[i]!=tops[i-1] for i in range(2,n))/max(1,n-2)
 longest=cur=1
 for i in range(1,n):
  if tops[i]==tops[i-1]:cur+=1;longest=max(longest,cur)
  else:cur=1
 vals,cnt=np.unique(tops,return_counts=True);mode=int(vals[np.argmax(cnt)]);mode_frac=float(cnt.max()/n)
 return [float(switch),float(ret),float(cur/n),float(longest/n),mode_frac],mode


def candidate_history_features(st,s):
 ids=[i for i,(q,_) in enumerate(st.hist) if q==s]
 n=len(ids);K=st.K
 # Dimension is fixed at 89. Features are candidate/source-specific summaries
 # of ordered retained evidence and posterior movement; no evaluator mode enters.
 if not ids:return np.zeros(89,dtype=float)
 vec=[st.hist[i][1] for i in ids];ps=[v.softmax(x) for x in vec]
 tops=[int(np.argmax(x)) for x in ps];marg=[v.margin(x) for x in ps];ents=[v.entropy(x) for x in ps]
 rs,mode=run_features(tops)
 pair=[tv(ps[i-1],ps[i]) for i in range(1,n)]
 allpair=[tv(ps[i],ps[j]) for i in range(n) for j in range(i+1,n)]
 cum=[];z=np.zeros(K)
 for x in vec:z+=x;cum.append(v.softmax(z.copy()))
 cmarg=[v.margin(x) for x in cum];cent=[v.entropy(x) for x in cum];ctops=[int(np.argmax(x)) for x in cum];crs,_=run_features(ctops)
 # Full-state posterior trajectory sampled immediately after candidate evidence.
 post=[st.post_hist[i] for i in ids]
 pmarg=[v.margin(x) for x in post];pent=[v.entropy(x) for x in post];ptops=[int(np.argmax(x)) for x in post];prs,_=run_features(ptops)
 ptv=[tv(post[i-1],post[i]) for i in range(1,n)]
 # Realized information movement when this candidate was observed.
 dm=[];de=[];dtop=[];dmove=[]
 uniform=np.ones(K)/K
 for idx,after in zip(ids,post):
  before=st.post_hist[idx-1] if idx>0 else uniform
  dm.append(v.margin(after)-v.margin(before));de.append(v.entropy(before)-v.entropy(after));dtop.append(float(np.argmax(after)!=np.argmax(before)));dmove.append(tv(before,after))
 # Candidate recent/global and relation to current live hypothesis.
 cand_global=v.softmax(np.sum(vec,axis=0));cand_recent=v.softmax(np.sum(vec[-min(3,n):],axis=0));gp=st.p(True);hist_top=int(np.argmax(gp))
 recent_global=tv(cand_recent,cand_global);last_global=tv(ps[-1],cand_global);cand_state=tv(cand_global,gp)
 last_mode=float(tops[-1]==mode);mode_state=float(mode==hist_top);last_state=float(tops[-1]==hist_top)
 trans=[]
 if n>=2:
  counts={}
  for a0,a1 in zip(tops[:-1],tops[1:]):counts[(a0,a1)]=counts.get((a0,a1),0)+1
  pp=np.asarray(list(counts.values()),float);pp/=pp.sum();trans_ent=float(-(pp*np.log(pp+1e-12)).sum()/max(1e-12,math.log(max(2,K*K))))
 else:trans_ent=0.
 f=[n/TRIALS,len(set(tops))/K,discrete_entropy(tops,K),trans_ent,*rs,
    *seq_stats(marg),*seq_stats(ents),float(np.mean(pair)) if pair else 0.,float(np.max(pair)) if pair else 0.,float(np.mean(allpair)) if allpair else 0.,float(np.max(allpair)) if allpair else 0.,
    *crs,*seq_stats(cmarg),*seq_stats(cent),
    *prs,*seq_stats(pmarg),*seq_stats(pent),float(np.mean(ptv)) if ptv else 0.,float(np.max(ptv)) if ptv else 0.,
    *seq_stats(dm),*seq_stats(de),float(np.mean(dtop)),*seq_stats(dmove),
    recent_global,last_global,cand_state,last_mode,mode_state,last_state,float(cand_global.max()),v.margin(cand_global),v.entropy(cand_global)]
 # Keep the complete ordered-history state. Feature count is asserted so source
 # changes cannot silently alter the model interface.
 f=np.asarray(f,float)
 if len(f)!=89:raise RuntimeError(f'candidate history feature dimension changed: {len(f)}')
 return f


def generate():
 t0=time.time();env=r31.setup(SEED);safe=v.train_A(SEED,env);shadow=joblib.load(ROOT/'R32_V28_RESOURCE_SHADOW_MODEL_SEED_9714.joblib')
 Xbase=[];Xhist=[];resource_features=[];adv=[];episode=[];split=[];mode_meta=[];resource_meta=[];trial_meta=[];actual_cost_meta=[];raw_cost_meta=[];cons_meta=[]
 eid=0;stats={}
 for mi,mode in enumerate(MODES):
  print('V30_GENERATE',mode,flush=True);vals=[]
  for ri,rname in enumerate(RESOURCE_REGIMES):
   for j in range(EPISODES_PER_MODE_RESOURCE):
    epseed=SEED*4_000_000+mi*300_000+ri*50_000+j
    ep=v.make_ep(epseed,'genuine_ambiguity',env);ep.avail[:]=False;ep.avail[0]=ep.avail[1]=ep.avail[SOURCE]=True
    params=e.world_params(epseed,mode);ep.cost[SOURCE]=params.cost;cons=e.delayed_consensus_from_outcomes(ep,mode,params)
    ctx=r.draw_context(SEED*50_000_000+mi*4_000_000+ri*500_000+j*53+23,ri);cache=rf.context_cache(ctx);budget=ctx.budget
    st=v.initial_state(ep,env,'D');a0=int(env[5][int(np.argmax(st.p(True)))]);used=[];path=[]
    for trial in range(TRIALS):
     cur=e.terminal_utility(st,a0,cons,env);resf=rf.fast_feature(ctx,cache,budget,params.cost);actual_cost=rf.fast_actual_loss(cache,budget,params.cost)
     base=b.action_feature_base(st,ep,safe,a0,env,params.cost,resf);hist=candidate_history_features(st,SOURCE)
     ev=e.source7_observation(ep,mode,params,st,env,used,trial);z=st.clone();z.add(SOURCE,ev,params.cost);nxt=e.terminal_utility(z,a0,cons,env)
     path.append((base,hist,resf,cur,nxt,actual_cost,params.cost,trial));st=z;budget=max(0.,budget-params.cost)
    cont=-1e9;local=[]
    for base,hist,resf,cur,nxt,actual_cost,raw_cost,trial in reversed(path):
     ret=max(nxt,cont)-actual_cost;local.append((base,hist,resf,float(ret-cur),actual_cost,raw_cost,trial));cont=ret
    local.reverse();sc=b.split_code(mi,ri,j)
    for base,hist,resf,a,ac,rc,tr in local:
     Xbase.append(base);Xhist.append(hist);resource_features.append(resf);adv.append(a);episode.append(eid);split.append(sc);mode_meta.append(mi);resource_meta.append(ri);trial_meta.append(tr);actual_cost_meta.append(ac);raw_cost_meta.append(rc);cons_meta.append(int(cons is not None));vals.append(a)
    eid+=1
  q=np.asarray(vals);stats[mode]={'rows':len(q),'positive_rate':float(np.mean(q>0)),'mean_advantage':float(q.mean())}
 shadow_costs=np.maximum(0.,shadow.predict(np.asarray(resource_features)))
 xb=np.c_[np.asarray(Xbase,np.float32),shadow_costs.astype(np.float32)]
 xh=np.c_[xb,np.asarray(Xhist,np.float32)]
 old=np.load(ROOT/'R32_V29_RESOURCE_GROUNDED_INSPECT_DATA_SEED_9714.npz')
 matched={'X_max_abs_delta':float(np.max(np.abs(xb-old['X']))),'advantage_max_abs_delta':float(np.max(np.abs(np.asarray(adv,np.float32)-old['advantage']))),'split_identical':bool(np.array_equal(np.asarray(split,np.int8),old['split_code']))}
 data={'X_base':xb,'X_history':xh,'candidate_history':np.asarray(Xhist,np.float32),'advantage':np.asarray(adv,np.float32),'episode_id':np.asarray(episode,np.int32),'split_code':np.asarray(split,np.int8),'mode_evaluator_only':np.asarray(mode_meta,np.int8),'resource_regime_evaluator_only':np.asarray(resource_meta,np.int8),'trial_index':np.asarray(trial_meta,np.int8),'actual_opportunity_loss':np.asarray(actual_cost_meta,np.float32),'predicted_shadow_cost':shadow_costs.astype(np.float32),'raw_cost':np.asarray(raw_cost_meta,np.float32),'delayed_consensus_evaluator_only':np.asarray(cons_meta,np.int8)}
 meta={'seed':SEED,'episodes':eid,'rows':len(adv),'base_feature_dim':xb.shape[1],'history_feature_dim':len(Xhist[0]),'augmented_feature_dim':xh.shape[1],'positive_rate':float(np.mean(data['advantage']>0)),'mode_stats':stats,'matched_v29':matched,'seconds':time.time()-t0,'learner_inputs':'V29 inputs plus candidate-specific ordered retained evidence/posterior/information-gain history','forbidden_inputs':'epistemic mode, resource regime, ambiguity label, future opportunities, final answer, fixed probe count'}
 return data,meta


def fit_two_stage(X,a,split,seed):
 y=(a>0).astype(int);tr=split<=5;ca=(split==6)|(split==7);te=split>=8
 clf=HistGradientBoostingClassifier(random_state=seed,max_iter=210,max_leaf_nodes=27,min_samples_leaf=26,l2_regularization=1.,learning_rate=.05).fit(X[tr],y[tr])
 rawca=clf.predict_proba(X[ca])[:,1];cal=LogisticRegression(max_iter=1000).fit(safe_logit(rawca),y[ca])
 pos=HistGradientBoostingRegressor(random_state=seed+1,max_iter=190,max_leaf_nodes=23,min_samples_leaf=20,l2_regularization=.8,learning_rate=.05).fit(X[tr&(y==1)],a[tr&(y==1)])
 neg=HistGradientBoostingRegressor(random_state=seed+2,max_iter=190,max_leaf_nodes=23,min_samples_leaf=28,l2_regularization=1.,learning_rate=.05).fit(X[tr&(y==0)],a[tr&(y==0)])
 raw=clf.predict_proba(X[te])[:,1];p=cal.predict_proba(safe_logit(raw))[:,1];qp=pos.predict(X[te]);qn=neg.predict(X[te]);ex=p*qp+(1-p)*qn;yt=y[te];at=a[te]
 out={'rows':{'train':int(tr.sum()),'calibration':int(ca.sum()),'test':int(te.sum())},'positive_rate':{'train':float(y[tr].mean()),'calibration':float(y[ca].mean()),'test':float(yt.mean())},'classifier':{'roc_auc':float(roc_auc_score(yt,p)),'average_precision':float(average_precision_score(yt,p)),'brier':float(brier_score_loss(yt,p))},'conditional':{'positive_mae':float(mean_absolute_error(at[yt==1],qp[yt==1])),'negative_mae':float(mean_absolute_error(at[yt==0],qn[yt==0])),'mean_positive_component_actual_positive':float(qp[yt==1].mean()),'mean_negative_component_actual_nonpositive':float(qn[yt==0].mean())},'expected_advantage':{'mse':float(mean_squared_error(at,ex)),'mae':float(mean_absolute_error(at,ex)),'roc_auc':float(roc_auc_score(yt,ex)),'mean_actual_positive':float(ex[yt==1].mean()),'mean_actual_nonpositive':float(ex[yt==0].mean()),'true_positive_cross_zero':float(np.mean(ex[yt==1]>0)),'false_positive_cross_zero':float(np.mean(ex[yt==0]>0)),'predicted_inspect_rate':float(np.mean(ex>0))}}
 return {'classifier':clf,'calibrator':cal,'positive':pos,'nonpositive':neg},out,{'test_mask':te,'p':p,'qp':qp,'qn':qn,'expected':ex}


def fit_direct(X,a,split,seed):
 tr=split<=7;te=split>=8;y=a>0
 m=HistGradientBoostingRegressor(random_state=seed,max_iter=230,max_leaf_nodes=27,min_samples_leaf=25,l2_regularization=1.,learning_rate=.045,loss='squared_error').fit(X[tr],a[tr])
 p=m.predict(X[te]);yt=y[te];at=a[te]
 return m,{'mse':float(mean_squared_error(at,p)),'mae':float(mean_absolute_error(at,p)),'roc_auc':float(roc_auc_score(yt,p)),'mean_actual_positive':float(p[yt].mean()),'mean_actual_nonpositive':float(p[~yt].mean()),'true_positive_cross_zero':float(np.mean(p[yt]>0)),'false_positive_cross_zero':float(np.mean(p[~yt]>0)),'predicted_inspect_rate':float(np.mean(p>0))}


def by_slices(data,pred):
 te=data['split_code']>=8;a=data['advantage'][te];y=a>0;mode=data['mode_evaluator_only'][te];res=data['resource_regime_evaluator_only'][te];out={'mode':{},'resource':{}}
 for i,n in enumerate(MODES):
  q=mode==i;out['mode'][n]={'n':int(q.sum()),'positive_rate':float(y[q].mean()),'inspect_rate':float(np.mean(pred[q]>0)),'tp_cross':float(np.mean(pred[q&y]>0)) if np.any(q&y) else None,'fp_cross':float(np.mean(pred[q&~y]>0)) if np.any(q&~y) else None,'mean_pred':float(pred[q].mean()),'mean_actual':float(a[q].mean())}
 for i,n in enumerate(RESOURCE_REGIMES):
  q=res==i;out['resource'][n]={'n':int(q.sum()),'positive_rate':float(y[q].mean()),'inspect_rate':float(np.mean(pred[q]>0)),'tp_cross':float(np.mean(pred[q&y]>0)) if np.any(q&y) else None,'fp_cross':float(np.mean(pred[q&~y]>0)) if np.any(q&~y) else None,'mean_pred':float(pred[q].mean()),'mean_actual':float(a[q].mean())}
 return out


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
 data,meta=generate();dp=ROOT/'R32_V30_CANDIDATE_HISTORY_DATA_SEED_9714.npz';np.savez_compressed(dp,**data)
 models,val,raw=fit_two_stage(data['X_history'],data['advantage'].astype(float),data['split_code'],30030)
 direct,dval=fit_direct(data['X_history'],data['advantage'].astype(float),data['split_code'],30040)
 files={}
 for n,m in {**models,'direct':direct}.items():
  p=ROOT/f'R32_V30_{n.upper()}_SEED_9714.joblib';joblib.dump(m,p,compress=3);files[n]={'file':p.name,'sha256':sha(p)}
 val['direct_expected_advantage']=dval;val['dataset']=meta;val['dataset']['sha256']=sha(dp);val['models']=files;val['slices_two_stage']=by_slices(data,raw['expected'])
 old=json.loads((ROOT/'R32_V29_RESOURCE_GROUNDED_ADVANTAGE_VALIDATION.json').read_text());val['v29_reference']={'classifier':old['classifier'],'expected_advantage':old['expected_advantage']};val['delta_vs_v29']={'classifier_auc':val['classifier']['roc_auc']-old['classifier']['roc_auc'],'average_precision':val['classifier']['average_precision']-old['classifier']['average_precision'],'expected_auc':val['expected_advantage']['roc_auc']-old['expected_advantage']['roc_auc'],'tp_cross':val['expected_advantage']['true_positive_cross_zero']-old['expected_advantage']['true_positive_cross_zero'],'fp_cross':val['expected_advantage']['false_positive_cross_zero']-old['expected_advantage']['false_positive_cross_zero'],'mean_pred_on_actual_positive':val['expected_advantage']['mean_actual_positive']-old['expected_advantage']['mean_actual_positive']}
 val['claim_boundary']='REFERENCE_ONLY matched representation ablation. V30 changes only candidate-specific ordered raw-history features; trajectories, delayed opportunity-loss targets, shadow price, splits, and two-stage model family are held fixed. No mode/resource/ambiguity label enters learner features.'
 (ROOT/'R32_V30_CANDIDATE_HISTORY_VALIDATION.json').write_text(json.dumps(val,indent=2));cfg={'status':'REFERENCE_ONLY_MATCHED_REPRESENTATION_ABLATION','seed':SEED,'runtime_fixed_threshold':False,'native_promotion_allowed':False,'source_sha256':sha(Path(__file__)),'matched_v29':meta['matched_v29']};(ROOT/'R32_V30_CONFIG.json').write_text(json.dumps(cfg,indent=2));summary={'matched_v29':meta['matched_v29'],'history_feature_dim':meta['history_feature_dim'],'classifier':val['classifier'],'expected_advantage':val['expected_advantage'],'direct':dval,'delta_vs_v29':val['delta_vs_v29']};(ROOT/'R32_V30_TRAINING.log').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
