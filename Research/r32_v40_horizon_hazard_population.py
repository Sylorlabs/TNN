from __future__ import annotations
import hashlib,json,math,time
from pathlib import Path
import joblib,numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor

ROOT=Path('/mnt/data/r32_epistemic');SEED=40040;H=np.array([1,2,3,5,8,12],float)
import sys
sys.path[:0]=['/mnt/data/r31_part2',str(ROOT)]
import r32_v32_predictive_dynamics_population as v32
import r32_v37_regret_weighted_candidate_support as v37

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def base_features(z32,z33,z39):
 seq=z39['sequence_prefix'].astype(np.float32);length=z39['lengths'].astype(float);n=len(length)
 flat=seq.reshape(n,-1);ens=z33['learned_ensemble_next_prediction'].astype(np.float32);top=np.argmax(ens,axis=1);oh=np.eye(5,dtype=np.float32)[top]
 # Prequential model state is learner-visible; no evaluator dynamics identity enters.
 return np.c_[flat,z33['gate_features'].astype(np.float32),z33['learned_model_weights'].astype(np.float32),z33['predicted_model_next_loss'].astype(np.float32),ens,oh,length[:,None]/12,(12-length)[:,None]/12]

def expand_horizon(X, trial):
 n=len(X);hh=np.tile(H,n);remain=np.repeat(12-np.clip(trial,0,11),len(H))
 hf=np.c_[hh/12,np.log1p(hh)/np.log(13),np.minimum(hh,remain)/np.maximum(1,remain),remain/12]
 return np.c_[np.repeat(X,len(H),axis=0),hf].astype(np.float32)

def crossfit(Xh,Y,split,seed):
 n=len(split);P=np.zeros_like(Y,dtype=np.float32);meta=[];models=[]
 folds=[np.isin(split,[0,3]),np.isin(split,[1,4]),np.isin(split,[2,5])]
 pars=dict(max_iter=170,max_leaf_nodes=31,min_samples_leaf=42,l2_regularization=1.0,learning_rate=.055,early_stopping=True,validation_fraction=.08,n_iter_no_change=10)
 for fi,hold in enumerate(folds):
  fit=(split<=5)&~hold;pred=(split<=5)&hold
  fm=np.repeat(fit,len(H));pm=np.repeat(pred,len(H));print('V40_FOLD',fi,int(fm.sum()),int(pm.sum()),flush=True)
  m=HistGradientBoostingRegressor(random_state=seed+fi,**pars).fit(Xh[fm],Y.reshape(-1)[fm]);P[pred]=m.predict(Xh[pm]).reshape(pred.sum(),len(H));meta.append({'fold':fi,'iterations':int(m.n_iter_)});models.append(m)
 fit=split<=5;pred=split>=6;fm=np.repeat(fit,len(H));pm=np.repeat(pred,len(H));print('V40_FINAL',int(fm.sum()),int(pm.sum()),flush=True)
 m=HistGradientBoostingRegressor(random_state=seed+20,**pars).fit(Xh[fm],Y.reshape(-1)[fm]);P[pred]=m.predict(Xh[pm]).reshape(pred.sum(),len(H));meta.append({'final_iterations':int(m.n_iter_)})
 return np.clip(P,0,1),m,meta

def interleave(dom,sup):
 out=np.empty((len(dom),12),np.float32);out[:,0::2]=dom;out[:,1::2]=sup;return out

def hazard_features(dom,sup):
 ds=np.diff(sup,axis=1);dd=np.diff(dom,axis=1);leave=np.maximum(0,-ds);ret=np.maximum(0,ds)
 return np.c_[sup,dom,ds,dd,leave,ret,sup[:,-1,None],dom[:,-1,None],sup.min(1)[:,None],sup.max(1)[:,None],leave.sum(1)[:,None],ret.sum(1)[:,None],(sup[:,-1]-sup[:,0])[:,None],(dom[:,-1]-dom[:,0])[:,None]].astype(np.float32)

def save_action(prefix,models):
 out={}
 for n,m in models.items():p=ROOT/f'R32_V40_{prefix}_{n.upper()}_SEED_9714.joblib';joblib.dump(m,p,compress=3);out[n]={'file':p.name,'sha256':sha(p)}
 return out

def main():
 t0=time.time();z32=np.load(ROOT/'R32_V32_PREDICTIVE_DYNAMICS_DATA_SEED_9714.npz');z33=np.load(ROOT/'R32_V33_LEARNED_GATING_DATA_SEED_9714.npz');z38=np.load(ROOT/'R32_V38_REPEATED_CONTINUATION_DATA_SEED_9714.npz');z39=np.load(ROOT/'R32_V39_RECURRENT_TEMPORAL_DATA_SEED_9714.npz')
 split=z32['split_code'].astype(int);adv=z32['advantage'].astype(float);Y=z38['repeated_mean_target'].astype(np.float32);Yvar=z38['predicted_repeated_variance'].astype(np.float32);dom=Y[:,0::2];sup=Y[:,1::2]
 X=base_features(z32,z33,z39);Xh=expand_horizon(X,z32['trial_index'].astype(int));print('V40_SUPPORT',Xh.shape,flush=True);Ps,ms,smeta=crossfit(Xh,sup,split,SEED);print('V40_DOMINANT',flush=True);Pd,md,dmeta=crossfit(Xh,dom,split,SEED+100)
 pair=interleave(Pd,Ps);hz=hazard_features(Pd,Ps);Xaction=np.c_[z32['X_dynamics'].astype(np.float32),z33['gate_features'].astype(np.float32)]
 arms={};files={};variants=[('horizon_pair_variance',np.c_[Xaction,pair,Yvar]),('horizon_hazard_variance',np.c_[Xaction,pair,Yvar,hz]),('hybrid_extra_hazard',np.c_[Xaction,z38['predicted_repeated_mean'],Yvar,pair,hz])]
 for i,(name,xx) in enumerate(variants):
  print('V40_ACTION',name,flush=True);models,val=v32.fit(xx,adv,split,SEED+300+i*100);arms[name]=val;files[name]=save_action(name.upper(),models)
 r38=json.loads((ROOT/'R32_V38_REPEATED_CONTINUATION_CREDIT_REFERENCE_ONLY.json').read_text());ref=r38['action_value']['arms']['predicted_mean_variance'];predmetrics={'v38_extra_trees_mean':r38['prediction_metrics']['repeated_mean_prediction'],'horizon_conditioned_mean':v37.metrics(Y,pair,split,adv)};deltas={}
 for n,val in arms.items():deltas[n]={'expected_auc':val['expected_advantage']['roc_auc']-ref['expected_advantage']['roc_auc'],'beneficial_cross':val['expected_advantage']['true_positive_cross_zero']-ref['expected_advantage']['true_positive_cross_zero'],'false_cross':val['expected_advantage']['false_positive_cross_zero']-ref['expected_advantage']['false_positive_cross_zero'],'selected_advantage':val['expected_advantage']['actual_mean_selected']-ref['expected_advantage']['actual_mean_selected']}
 sp=ROOT/'R32_V40_HORIZON_SUPPORT_MODEL_SEED_9714.joblib';dp=ROOT/'R32_V40_HORIZON_DOMINANT_MODEL_SEED_9714.joblib';joblib.dump(ms,sp,compress=3);joblib.dump(md,dp,compress=3);dat=ROOT/'R32_V40_HORIZON_HAZARD_DATA_SEED_9714.npz';np.savez_compressed(dat,predicted_support=Ps,predicted_dominant=Pd,predicted_pair=pair,hazard_features=hz,split_code=split.astype(np.int8),episode_id=z32['episode_id'])
 out={'experiment':'R32 V40 explicit horizon-conditioned persistence/change hypothesis population','architecture':{'hypotheses':['current-state persistence by horizon','change/leave hazard','return-to-prior hazard','future dominant-mass stability'],'weights':'learned from delayed outcomes only','graph':False,'transformer':False},'features':{'base_dim':int(X.shape[1]),'horizon_expanded_dim':int(Xh.shape[1]),'hazard_dim':int(hz.shape[1])},'training':{'support':smeta,'dominant':dmeta},'prediction_metrics':predmetrics,'action_value':{'v38_reference':ref,'arms':arms,'delta_vs_v38':deltas,'models':files},'artifacts':{'support_model':{'file':sp.name,'sha256':sha(sp)},'dominant_model':{'file':dp.name,'sha256':sha(dp)},'data':{'file':dat.name,'sha256':sha(dat)}},'seconds':time.time()-t0,'training_boundary':'Horizon and retained ordered evidence are learner-visible. Persistence/change/return quantities are learned from delayed observed outcomes; no generator mode or ambiguity label is provided.','claim_boundary':'REFERENCE_ONLY; native Zag execution required for promotion.'}
 rp=ROOT/'R32_V40_HORIZON_HAZARD_POPULATION_REFERENCE_ONLY.json';rp.write_text(json.dumps(out,indent=2));cfg={'status':'REFERENCE_ONLY_HORIZON_HAZARD_POPULATION','seed':SEED,'episode_disjoint_crossfit':True,'runtime_fixed_threshold':False,'native_promotion_allowed':False,'source_sha256':sha(Path(__file__))};(ROOT/'R32_V40_CONFIG.json').write_text(json.dumps(cfg,indent=2));summary={'prediction':predmetrics,'action_delta':deltas,'seconds':out['seconds']};(ROOT/'R32_V40_TRAINING.log').write_text(json.dumps(summary,indent=2)+'\n');(ROOT/'R32_V40_DONE.flag').write_text('');print(json.dumps(summary,indent=2),flush=True)
if __name__=='__main__':main()
