from __future__ import annotations

import hashlib,json,math,sys,time
from pathlib import Path
import joblib,numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier,HistGradientBoostingRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score,brier_score_loss,mean_absolute_error,mean_squared_error,roc_auc_score

ROOT=Path('/mnt/data/r32_epistemic')
sys.path[:0]=['/mnt/data/r31_part2',str(ROOT)]
import r31_sequential_evidence_abstention_REFERENCE_ONLY as r31
import r32_epistemic_r31_matched_v17_cached_REFERENCE_ONLY as v
import r32_v26_candidate_selected_conditional_advantage as e
import r32_v28_learned_resource_shadow_price as r
import r32_v28_complete_from_checkpoint as rf
import r32_v29_resource_grounded_inspect_advantage as b
import r32_v30_candidate_ordered_history as h

SEED=b.SEED;SOURCE=b.SOURCE;TRIALS=b.TRIALS;EPISODES_PER_MODE_RESOURCE=b.EPISODES_PER_MODE_RESOURCE
MODES=b.MODES;RESOURCE_REGIMES=b.RESOURCE_REGIMES
MODEL_NAMES=['uniform','global','recent2','recent3','recent5','exp50','exp75','exp90','last','changepoint','transition1','transition2','parity2','phase3','return2']
M=len(MODEL_NAMES)

def norm(x):
 q=np.maximum(np.asarray(x,float),1e-9);return q/q.sum()
def smooth_mean(seq,K,alpha=.18):return norm(np.sum(seq,axis=0)+alpha) if len(seq) else np.ones(K)/K
def entropy(p):return float(-(p*np.log(p+1e-12)).sum()/math.log(len(p)))
def margin(p):q=np.sort(p);return float(q[-1]-q[-2])
def tv(a,c):return .5*float(np.abs(a-c).sum())
def js(a,c):m=.5*(a+c);return .5*float(np.sum(a*np.log((a+1e-12)/(m+1e-12)))+np.sum(c*np.log((c+1e-12)/(m+1e-12))))

def expmean(seq,K,decay):
 if not seq:return np.ones(K)/K
 w=np.asarray([decay**(len(seq)-1-i) for i in range(len(seq))]);return norm(np.sum(np.asarray(seq)*w[:,None],axis=0)+.18)

def changepoint_pred(seq,K):
 n=len(seq)
 if n<4:return smooth_mean(seq,K)
 best=(-1e9,n-1)
 for cut in range(1,n):
  pre=smooth_mean(seq[:cut],K);post=smooth_mean(seq[cut:],K)
  vol=np.mean([tv(seq[i-1],seq[i]) for i in range(cut+1,n)]) if n-cut>1 else 0.
  score=tv(pre,post)-.55*vol-.035*math.log1p(cut)
  if score>best[0]:best=(score,cut)
 return smooth_mean(seq[best[1]:],K)

def trans_pred(tops,K,order=1):
 n=len(tops)
 if n<=order:return np.ones(K)/K
 if order==1:
  C=np.full((K,K),.18)
  for x,y in zip(tops[:-1],tops[1:]):C[x,y]+=1
  return norm(C[tops[-1]])
 C=np.full((K,K,K),.12)
 for i in range(2,n):C[tops[i-2],tops[i-1],tops[i]]+=1
 return norm(C[tops[-2],tops[-1]])

def phase_pred(seq,K,period):
 n=len(seq);ids=[i for i in range(n) if i%period==n%period]
 return smooth_mean([seq[i] for i in ids],K) if ids else smooth_mean(seq,K)

def return_pred(seq,tops,K):
 n=len(seq)
 if n<3:return smooth_mean(seq,K)
 ret=np.mean([tops[i]==tops[i-2] for i in range(2,n)]);base=smooth_mean(seq,K);q=(1-ret)*base
 q[tops[-2]]+=ret;return norm(q)

def predictions(seq,K):
 n=len(seq);tops=[int(np.argmax(x)) for x in seq];u=np.ones(K)/K
 return [u,smooth_mean(seq,K),smooth_mean(seq[-2:],K),smooth_mean(seq[-3:],K),smooth_mean(seq[-5:],K),expmean(seq,K,.50),expmean(seq,K,.75),expmean(seq,K,.90),(norm(seq[-1]+.08) if n else u),changepoint_pred(seq,K),trans_pred(tops,K,1),trans_pred(tops,K,2),phase_pred(seq,K,2),phase_pred(seq,K,3),return_pred(seq,tops,K)]

def predictive_features(st,s):
 seq=[v.softmax(x) for q,x in st.hist if q==s];K=st.K;n=len(seq);pred=predictions(seq,K)
 # Prequential evidence for each dynamics hypothesis.
 losses=np.zeros(M)
 if n>=2:
  for t in range(1,n):
   pp=predictions(seq[:t],K);target=seq[t]
   for j,q in enumerate(pp):losses[j]+=-float(np.sum(target*np.log(q+1e-12)))
 avg=losses/max(1,n-1);lw=-losses;lw-=lw.max();w=np.exp(np.clip(lw,-50,0));w/=w.sum()
 ens=norm(np.sum(np.asarray(pred)*w[:,None],axis=0));gp=st.p(True);ep=st.epoch_p();gt=int(np.argmax(gp));et=int(np.argmax(ep));last=int(np.argmax(seq[-1])) if n else gt;mode=last
 if n:
  tops=[int(np.argmax(x)) for x in seq];vals,cnt=np.unique(tops,return_counts=True);mode=int(vals[np.argmax(cnt)])
 mt=[int(np.argmax(q)) for q in pred];dis=[js(q,ens) for q in pred];ent=[entropy(q) for q in pred];mar=[margin(q) for q in pred]
 family=[float(w[[0,1]].sum()),float(w[[2,3,4,5,6,7,8]].sum()),float(w[9]),float(w[[10,11]].sum()),float(w[[12,13,14]].sum())]
 rel=[]
 for q in pred:rel.extend([q[gt],q[et],q[last],q[mode],float(q.max()),margin(q),entropy(q)])
 feat=np.asarray([n/TRIALS,*w.tolist(),*(math.log(K)-avg).tolist(),*family,ens.max(),margin(ens),entropy(ens),ens[gt],ens[et],ens[last],ens[mode],float(np.argmax(ens)==gt),float(np.argmax(ens)==last),float(np.mean(np.asarray(mt)==gt)),float(np.sum(w*(np.asarray(mt)==gt))),float(np.mean(dis)),float(np.max(dis)),float(np.sum(w*np.asarray(dis))),float(np.sum(w*np.asarray(ent))),float(np.sqrt(np.sum(w*(np.asarray(ent)-np.sum(w*np.asarray(ent)))**2))),float(np.sum(w*np.asarray(mar))),float(np.sqrt(np.sum(w*(np.asarray(mar)-np.sum(w*np.asarray(mar)))**2))),1-ens[last],(ens[tops[-2]] if n>=2 else ens[last]),*rel],float)
 return feat,ens,np.asarray(pred),w,avg

def safe_logit(p):q=np.clip(p,1e-6,1-1e-6);return np.log(q/(1-q)).reshape(-1,1)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def generate():
 t0=time.time();env=r31.setup(SEED);safe=v.train_A(SEED,env);shadow=joblib.load(ROOT/'R32_V28_RESOURCE_SHADOW_MODEL_SEED_9714.joblib')
 Xbase=[];Xdyn=[];resource_features=[];adv=[];split=[];episode=[];mode_meta=[];resource_meta=[];trial_meta=[];actual_cost_meta=[];raw_cost_meta=[];cons_meta=[];true_next=[];ens_next=[];model_next=[];weights=[];losses=[]
 eid=0
 for mi,mode in enumerate(MODES):
  print('V32_GENERATE',mode,flush=True)
  for ri,rname in enumerate(RESOURCE_REGIMES):
   for j in range(EPISODES_PER_MODE_RESOURCE):
    epseed=SEED*4_000_000+mi*300_000+ri*50_000+j;ep=v.make_ep(epseed,'genuine_ambiguity',env);ep.avail[:]=False;ep.avail[0]=ep.avail[1]=ep.avail[SOURCE]=True
    params=e.world_params(epseed,mode);ep.cost[SOURCE]=params.cost;cons=e.delayed_consensus_from_outcomes(ep,mode,params);ctx=r.draw_context(SEED*50_000_000+mi*4_000_000+ri*500_000+j*53+23,ri);cache=rf.context_cache(ctx);budget=ctx.budget
    st=v.initial_state(ep,env,'D');a0=int(env[5][int(np.argmax(st.p(True)))]);used=[];path=[]
    for trial in range(TRIALS):
     cur=e.terminal_utility(st,a0,cons,env);resf=rf.fast_feature(ctx,cache,budget,params.cost);ac=rf.fast_actual_loss(cache,budget,params.cost);base=b.action_feature_base(st,ep,safe,a0,env,params.cost,resf);hist=h.candidate_history_features(st,SOURCE);dyn,ens,pp,ww,ll=predictive_features(st,SOURCE)
     outcome=e.world_outcome(ep,mode,params,trial);oi=env[6][outcome]
     ev=e.source7_observation(ep,mode,params,st,env,used,trial);z=st.clone();z.add(SOURCE,ev,params.cost);nxt=e.terminal_utility(z,a0,cons,env)
     path.append((base,hist,dyn,resf,cur,nxt,ac,params.cost,trial,oi,ens,pp,ww,ll));st=z;budget=max(0.,budget-params.cost)
    cont=-1e9;local=[]
    for row in reversed(path):
     base,hist,dyn,resf,cur,nxt,ac,rc,tr,oi,ens,pp,ww,ll=row;ret=max(nxt,cont)-ac;local.append((base,hist,dyn,resf,float(ret-cur),ac,rc,tr,oi,ens,pp,ww,ll));cont=ret
    local.reverse();sc=b.split_code(mi,ri,j)
    for base,hist,dyn,resf,a,ac,rc,tr,oi,ens,pp,ww,ll in local:
     Xbase.append(np.r_[base,hist]);Xdyn.append(dyn);resource_features.append(resf);adv.append(a);split.append(sc);episode.append(eid);mode_meta.append(mi);resource_meta.append(ri);trial_meta.append(tr);actual_cost_meta.append(ac);raw_cost_meta.append(rc);cons_meta.append(int(cons is not None));true_next.append(oi);ens_next.append(ens);model_next.append(pp);weights.append(ww);losses.append(ll)
    eid+=1
 shadow_cost=np.maximum(0.,shadow.predict(np.asarray(resource_features))).astype(np.float32);xb=np.c_[np.asarray(Xbase,np.float32),shadow_cost];xd=np.c_[xb,np.asarray(Xdyn,np.float32)]
 old=np.load(ROOT/'R32_V30_CANDIDATE_HISTORY_DATA_SEED_9714.npz');matched={'X_max_abs_delta':float(np.max(np.abs(xb-old['X_history']))),'advantage_max_abs_delta':float(np.max(np.abs(np.asarray(adv,np.float32)-old['advantage']))),'split_identical':bool(np.array_equal(np.asarray(split,np.int8),old['split_code']))}
 data={'X_base':xb,'X_dynamics':xd,'predictive_features':np.asarray(Xdyn,np.float32),'advantage':np.asarray(adv,np.float32),'split_code':np.asarray(split,np.int8),'episode_id':np.asarray(episode,np.int32),'mode_evaluator_only':np.asarray(mode_meta,np.int8),'resource_regime_evaluator_only':np.asarray(resource_meta,np.int8),'trial_index':np.asarray(trial_meta,np.int8),'actual_opportunity_loss':np.asarray(actual_cost_meta,np.float32),'raw_cost':np.asarray(raw_cost_meta,np.float32),'delayed_consensus_evaluator_only':np.asarray(cons_meta,np.int8),'true_next_outcome_evaluator_only':np.asarray(true_next,np.int8),'ensemble_next_prediction':np.asarray(ens_next,np.float32),'model_next_predictions':np.asarray(model_next,np.float32),'model_weights':np.asarray(weights,np.float32),'model_prequential_avg_loss':np.asarray(losses,np.float32)}
 meta={'seed':SEED,'rows':len(adv),'episodes':eid,'base_feature_dim':xb.shape[1],'predictive_feature_dim':len(Xdyn[0]),'augmented_feature_dim':xd.shape[1],'positive_rate':float(np.mean(data['advantage']>0)),'matched_v30':matched,'model_names':MODEL_NAMES,'seconds':time.time()-t0,'learner_inputs':'V30 state plus prequentially weighted generic predictive-dynamics hypotheses over candidate raw evidence','forbidden_inputs':'mode/resource/trial identity, ambiguity label, true next outcome, future opportunities, final answer, fixed probe count'}
 return data,meta

def fit(X,a,s,seed):
 y=(a>0).astype(int);tr=s<=5;ca=(s==6)|(s==7);te=s>=8
 clf=HistGradientBoostingClassifier(random_state=seed,max_iter=210,max_leaf_nodes=27,min_samples_leaf=24,l2_regularization=1.,learning_rate=.05).fit(X[tr],y[tr]);cal=LogisticRegression(max_iter=1000).fit(safe_logit(clf.predict_proba(X[ca])[:,1]),y[ca]);p=cal.predict_proba(safe_logit(clf.predict_proba(X[te])[:,1]))[:,1]
 pos=HistGradientBoostingRegressor(random_state=seed+1,max_iter=190,max_leaf_nodes=23,min_samples_leaf=20,l2_regularization=.8,learning_rate=.05).fit(X[tr&(y==1)],a[tr&(y==1)]);neg=HistGradientBoostingRegressor(random_state=seed+2,max_iter=190,max_leaf_nodes=23,min_samples_leaf=28,l2_regularization=1.,learning_rate=.05).fit(X[tr&(y==0)],a[tr&(y==0)]);qp=pos.predict(X[te]);qn=neg.predict(X[te]);ex=p*qp+(1-p)*qn;yt=y[te];at=a[te]
 direct=HistGradientBoostingRegressor(random_state=seed+3,max_iter=220,max_leaf_nodes=27,min_samples_leaf=24,l2_regularization=1.,learning_rate=.05).fit(X[tr|ca],a[tr|ca]);dq=direct.predict(X[te])
 def vm(q):return {'mse':float(mean_squared_error(at,q)),'mae':float(mean_absolute_error(at,q)),'roc_auc':float(roc_auc_score(yt,q)),'mean_actual_positive':float(q[yt].mean()),'mean_actual_nonpositive':float(q[~yt].mean()),'true_positive_cross_zero':float(np.mean(q[yt]>0)),'false_positive_cross_zero':float(np.mean(q[~yt]>0)),'predicted_inspect_rate':float(np.mean(q>0)),'actual_mean_selected':float(at[q>0].mean()) if np.any(q>0) else None}
 val={'rows':{'train':int(tr.sum()),'calibration':int(ca.sum()),'test':int(te.sum())},'classifier':{'roc_auc':float(roc_auc_score(yt,p)),'average_precision':float(average_precision_score(yt,p)),'brier':float(brier_score_loss(yt,p))},'expected_advantage':vm(ex),'direct':vm(dq)}
 return {'classifier':clf,'calibrator':cal,'positive':pos,'nonpositive':neg,'direct':direct},val

def prediction_metrics(data):
 te=data['split_code']>=8;y=data['true_next_outcome_evaluator_only'][te];ens=data['ensemble_next_prediction'][te];mods=data['model_next_predictions'][te];trial=data['trial_index'][te];mode=data['mode_evaluator_only'][te]
 out={'ensemble':{'top1':float(np.mean(np.argmax(ens,axis=1)==y)),'nll':float(np.mean(-np.log(ens[np.arange(len(y)),y]+1e-12))),'brier':float(np.mean(np.sum((ens-np.eye(ens.shape[1])[y])**2,axis=1)))},'models':{},'by_mode':{},'by_trial':{}}
 for j,n in enumerate(MODEL_NAMES):q=mods[:,j];out['models'][n]={'top1':float(np.mean(np.argmax(q,axis=1)==y)),'nll':float(np.mean(-np.log(q[np.arange(len(y)),y]+1e-12)))}
 for i,n in enumerate(MODES):q=mode==i;out['by_mode'][n]={'n':int(q.sum()),'top1':float(np.mean(np.argmax(ens[q],axis=1)==y[q])),'nll':float(np.mean(-np.log(ens[q][np.arange(q.sum()),y[q]]+1e-12)))}
 for i in range(TRIALS):q=trial==i;out['by_trial'][str(i)]={'n':int(q.sum()),'top1':float(np.mean(np.argmax(ens[q],axis=1)==y[q])),'nll':float(np.mean(-np.log(ens[q][np.arange(q.sum()),y[q]]+1e-12)))}
 return out

def main():
 data,meta=generate();dp=ROOT/'R32_V32_PREDICTIVE_DYNAMICS_DATA_SEED_9714.npz';np.savez_compressed(dp,**data);models,val=fit(data['X_dynamics'],data['advantage'].astype(float),data['split_code'],32032);files={}
 for n,m in models.items():p=ROOT/f'R32_V32_{n.upper()}_SEED_9714.joblib';joblib.dump(m,p,compress=3);files[n]={'file':p.name,'sha256':sha(p)}
 old=json.loads((ROOT/'R32_V30_CANDIDATE_HISTORY_VALIDATION.json').read_text());val['dataset']=meta;val['dataset']['sha256']=sha(dp);val['models']=files;val['next_outcome_prediction']=prediction_metrics(data);val['v30_reference']={'classifier':old['classifier'],'expected_advantage':old['expected_advantage'],'direct':old['direct_expected_advantage']};val['delta_vs_v30']={'classifier_auc':val['classifier']['roc_auc']-old['classifier']['roc_auc'],'classifier_ap':val['classifier']['average_precision']-old['classifier']['average_precision'],'expected_auc':val['expected_advantage']['roc_auc']-old['expected_advantage']['roc_auc'],'tp_cross':val['expected_advantage']['true_positive_cross_zero']-old['expected_advantage']['true_positive_cross_zero'],'fp_cross':val['expected_advantage']['false_positive_cross_zero']-old['expected_advantage']['false_positive_cross_zero'],'mean_pred_actual_positive':val['expected_advantage']['mean_actual_positive']-old['expected_advantage']['mean_actual_positive']}
 val['claim_boundary']='REFERENCE_ONLY matched dynamics-representation ablation. Predictive model evidence comes only from prequential loss on retained candidate observations; evaluator modes and true next outcomes are metrics only.';(ROOT/'R32_V32_PREDICTIVE_DYNAMICS_VALIDATION.json').write_text(json.dumps(val,indent=2));cfg={'status':'REFERENCE_ONLY_MATCHED_DYNAMICS_REPRESENTATION','seed':SEED,'native_promotion_allowed':False,'runtime_fixed_threshold':False,'source_sha256':sha(Path(__file__)),'matched_v30':meta['matched_v30']};(ROOT/'R32_V32_CONFIG.json').write_text(json.dumps(cfg,indent=2));summary={'matched_v30':meta['matched_v30'],'predictive_feature_dim':meta['predictive_feature_dim'],'next_outcome_ensemble':val['next_outcome_prediction']['ensemble'],'classifier':val['classifier'],'expected_advantage':val['expected_advantage'],'direct':val['direct'],'delta_vs_v30':val['delta_vs_v30']};(ROOT/'R32_V32_TRAINING.log').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
