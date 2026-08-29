from __future__ import annotations
import hashlib,json,time,sys
from pathlib import Path
import joblib,numpy as np
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score
ROOT=Path('/mnt/data/r32_epistemic');SEED=37037;H=6;PER=11
sys.path[:0]=['/mnt/data/r31_part2',str(ROOT)]
import r32_v32_predictive_dynamics_population as v32

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pair_cols():
 # dominant mass (offset 6) and fraction equal current top (offset 9), grouped by horizon
 return [hi*PER+off for hi in range(H) for off in (6,9)]
def model(seed):
 return ExtraTreesRegressor(n_estimators=150,max_depth=21,min_samples_leaf=10,max_features=.65,n_jobs=6,random_state=seed)
def regret_weights(a,mask):
 scale=float(np.median(np.abs(a[mask])))+1e-6
 return np.clip(.35+np.abs(a)/scale,.35,8.).astype(np.float32),scale
def crossfit(X,Y,split,a,kind,seed):
 tr=split<=5;pred=np.empty_like(Y,dtype=np.float32);folds=[np.isin(split,[0,3]),np.isin(split,[1,4]),np.isin(split,[2,5])];meta=[];w,scale=regret_weights(a,tr)
 for fi,hold in enumerate(folds):
  fit=tr&~hold;h=tr&hold;m=model(seed+fi);t=time.time();kw={'sample_weight':w[fit]} if kind=='weighted' else {};m.fit(X[fit],Y[fit],**kw);pred[h]=m.predict(X[h]);meta.append({'fold':fi,'seconds':time.time()-t,'fit_rows':int(fit.sum()),'hold_rows':int(h.sum())})
 final=model(seed+20);t=time.time();kw={'sample_weight':w[tr]} if kind=='weighted' else {};final.fit(X[tr],Y[tr],**kw);pred[~tr]=final.predict(X[~tr]);meta.append({'final_seconds':time.time()-t,'train_rows':int(tr.sum())})
 return np.clip(pred,0,1).astype(np.float32),final,{'kind':kind,'regret_weight_scale':scale,'weight_train_mean':float(w[tr].mean()),'weight_positive_mean':float(w[tr&(a>0)].mean()),'weight_nonpositive_mean':float(w[tr&(a<=0)].mean()),'fits':meta}
def metrics(Y,P,split,a):
 te=split>=8;pos=te&(a>0);neg=te&(a<=0);absq=np.abs(a[te]);cut=float(np.quantile(absq,.75));critical=te&(np.abs(a)>=cut)
 out={'overall':{'mse':float(mean_squared_error(Y[te],P[te])),'mae':float(mean_absolute_error(Y[te],P[te])),'r2':float(r2_score(Y[te],P[te],multioutput='variance_weighted'))},'decision_positive':{'n':int(pos.sum()),'mae':float(mean_absolute_error(Y[pos],P[pos]))},'decision_nonpositive':{'n':int(neg.sum()),'mae':float(mean_absolute_error(Y[neg],P[neg]))},'high_regret_quartile':{'n':int(critical.sum()),'cut':cut,'mae':float(mean_absolute_error(Y[critical],P[critical]))},'by_horizon':{}}
 for hi,h in enumerate([1,2,3,5,8,12]):
  out['by_horizon'][str(h)]={'dominant_mass_mae':float(np.mean(np.abs(Y[te,2*hi]-P[te,2*hi]))),'same_current_support_mae':float(np.mean(np.abs(Y[te,2*hi+1]-P[te,2*hi+1]))),'same_current_support_positive_mae':float(np.mean(np.abs(Y[pos,2*hi+1]-P[pos,2*hi+1])))}
 return out
def save_action(prefix,mods):
 out={}
 for n,m in mods.items():
  p=ROOT/f'R32_V37_{prefix}_{n.upper()}_SEED_9714.joblib';joblib.dump(m,p,compress=3);out[n]={'file':p.name,'sha256':sha(p)}
 return out

def main():
 t0=time.time();z32=np.load(ROOT/'R32_V32_PREDICTIVE_DYNAMICS_DATA_SEED_9714.npz');z33=np.load(ROOT/'R32_V33_LEARNED_GATING_DATA_SEED_9714.npz');z34=np.load(ROOT/'R32_V34_MULTISTEP_STATE_DATA_SEED_9714.npz');split=z32['split_code'].astype(int);a=z32['advantage'].astype(float);X=np.c_[z32['X_dynamics'].astype(np.float32),z33['gate_features'].astype(np.float32)];cc=pair_cols();Y=z34['target_future_state_evaluator_only'][:,cc].astype(np.float32);generic=z34['predicted_future_state'][:,cc].astype(np.float32)
 print('V37_UNWEIGHTED',flush=True);unw,mu,metau=crossfit(X,Y,split,a,'unweighted',SEED)
 print('V37_WEIGHTED',flush=True);wei,mw,metaw=crossfit(X,Y,split,a,'weighted',SEED+100)
 print('V37_RESIDUAL_WEIGHTED',flush=True);res_target=Y-generic;res,mr,metar=crossfit(np.c_[X,generic],res_target,split,a,'weighted',SEED+200);res=np.clip(generic+res,0,1)
 preds={'generic_v34_pair':generic,'specialized_unweighted':unw,'specialized_regret_weighted':wei,'specialized_weighted_residual':res};pm={n:metrics(Y,p,split,a) for n,p in preds.items()}
 arms={};files={}
 for i,(n,p) in enumerate(preds.items()):
  print('V37_ACTION',n,flush=True);mods,val=v32.fit(np.c_[X,p],a,split,SEED+500+i*100);arms[n]=val;files[n]=save_action(n.upper(),mods)
 exact=json.loads((ROOT/'R32_V36_EXACT_SCALAR_FAMILY_ABLATION_REFERENCE_ONLY.json').read_text())['families']['commit_alignment_pair']['metrics'];v33=json.loads((ROOT/'R32_V33_LEARNED_PREDICTIVE_GATING_REFERENCE_ONLY.json').read_text())['action_value']['v32_plus_learned_gate']
 model_files={}
 for name,m in [('unweighted',mu),('regret_weighted',mw),('weighted_residual',mr)]:
  p=ROOT/f'R32_V37_SUPPORT_{name.upper()}_SEED_9714.joblib';joblib.dump(m,p,compress=3);model_files[name]={'file':p.name,'sha256':sha(p)}
 dp=ROOT/'R32_V37_CANDIDATE_SUPPORT_DATA_SEED_9714.npz';np.savez_compressed(dp,target_pair_evaluator_only=Y,generic_v34_pair=generic,specialized_unweighted=unw,specialized_regret_weighted=wei,specialized_weighted_residual=res,split_code=split.astype(np.int8),episode_id=z32['episode_id'])
 out={'experiment':'R32 V37 specialized future candidate-support prediction with delayed regret weighting','target_columns':cc,'prediction_metrics':pm,'training_meta':{'unweighted':metau,'regret_weighted':metaw,'weighted_residual':metar},'action_value':{'v33_reference':v33,'exact_pair_ceiling_evaluator_only':exact,'arms':arms,'delta_vs_v33':{n:{'classifier_auc':v['classifier']['roc_auc']-v33['classifier']['roc_auc'],'classifier_ap':v['classifier']['average_precision']-v33['classifier']['average_precision'],'expected_auc':v['expected_advantage']['roc_auc']-v33['expected_advantage']['roc_auc'],'beneficial_cross':v['expected_advantage']['true_positive_cross_zero']-v33['expected_advantage']['true_positive_cross_zero'],'false_cross':v['expected_advantage']['false_positive_cross_zero']-v33['expected_advantage']['false_positive_cross_zero'],'selected_advantage':v['expected_advantage']['actual_mean_selected']-v33['expected_advantage']['actual_mean_selected']} for n,v in arms.items()},'models':files},'models':model_files,'data':{'file':dp.name,'sha256':sha(dp)},'seconds':time.time()-t0,'claim_boundary':'REFERENCE_ONLY. Specialized targets come from delayed experienced future outcomes. Training weights use only absolute delayed decision regret; no ambiguity, world-mode, resource-regime, trial identity, or final answer is a feature.'};(ROOT/'R32_V37_REGRET_WEIGHTED_CANDIDATE_SUPPORT_REFERENCE_ONLY.json').write_text(json.dumps(out,indent=2));cfg={'status':'REFERENCE_ONLY_MATCHED_REGRET_WEIGHTED_SUPPORT_PREDICTION','seed':SEED,'runtime_fixed_probe_count':False,'native_promotion_allowed':False,'source_sha256':sha(Path(__file__))};(ROOT/'R32_V37_CONFIG.json').write_text(json.dumps(cfg,indent=2));(ROOT/'R32_V37_TRAINING.log').write_text(json.dumps({'prediction_metrics':pm,'action_delta':out['action_value']['delta_vs_v33'],'seconds':out['seconds']},indent=2)+'\n');(ROOT/'R32_V37_DONE.flag').write_text('');print(json.dumps({'prediction_metrics':pm,'action_delta':out['action_value']['delta_vs_v33'],'seconds':out['seconds']},indent=2))
if __name__=='__main__':main()
