from __future__ import annotations
import hashlib,json,time
from pathlib import Path
from typing import Any
import joblib,numpy as np
from sklearn.metrics import roc_auc_score,average_precision_score,mean_squared_error,mean_absolute_error
ROOT=Path('/mnt/data/r32_epistemic');SEED=43043
import sys;sys.path.insert(0,str(ROOT))
import r32_v32_predictive_dynamics_population as v32

STAGES=[('trial0',0,0),('trial1_2',1,2),('trial3_5',3,5),('trial6_11',6,11)]
MODES=['balanced_no_unique','biased_no_unique','stable_weak','unstable_then_stable','replacement','reversal','costly_stable']

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def safe_logit(p):q=np.clip(np.asarray(p,float),1e-6,1-1e-6);return np.log(q/(1-q)).reshape(-1,1)
def pred(models,X):
 clf=models['classifier'];cal=models['calibrator'];pos=models['positive'];neg=models['nonpositive'];raw=clf.predict_proba(X)[:,1];p=cal.predict_proba(safe_logit(raw))[:,1];qp=pos.predict(X);qn=neg.predict(X);return p*qp+(1-p)*qn

def metrics(a,ex):
 y=a>0;sel=ex>0
 return {'n':len(a),'positive_rate':float(y.mean()),'expected_advantage':{'mse':float(mean_squared_error(a,ex)),'mae':float(mean_absolute_error(a,ex)),'roc_auc':float(roc_auc_score(y,ex)),'average_precision':float(average_precision_score(y,ex)),'true_positive_cross_zero':float(np.mean(ex[y]>0)),'false_positive_cross_zero':float(np.mean(ex[~y]>0)),'predicted_inspect_rate':float(sel.mean()),'selected_actual_advantage':float(a[sel].mean()) if np.any(sel) else None,'mean_pred_actual_positive':float(ex[y].mean()),'mean_pred_actual_nonpositive':float(ex[~y].mean())}}

def main():
 t0=time.time();z32=np.load(ROOT/'R32_V32_PREDICTIVE_DYNAMICS_DATA_SEED_9714.npz');z33=np.load(ROOT/'R32_V33_LEARNED_GATING_DATA_SEED_9714.npz');z38=np.load(ROOT/'R32_V38_REPEATED_CONTINUATION_DATA_SEED_9714.npz');z40=np.load(ROOT/'R32_V40_HORIZON_HAZARD_DATA_SEED_9714.npz')
 Xaction=np.c_[z32['X_dynamics'].astype(np.float32),z33['gate_features'].astype(np.float32)];X=np.c_[Xaction,z40['predicted_pair'].astype(np.float32),z38['predicted_repeated_variance'].astype(np.float32),z40['hazard_features'].astype(np.float32)]
 a=z32['advantage'].astype(float);split=z32['split_code'].astype(int);trial=z32['trial_index'].astype(int);mode=z32['mode_evaluator_only'].astype(int);te=split>=8
 combined=np.full(te.sum(),np.nan);test_rows=np.where(te)[0];files={};stage_results={}
 for si,(name,lo,hi) in enumerate(STAGES):
  q=(trial>=lo)&(trial<=hi);idx=np.where(q)[0];print('V43_STAGE',name,len(idx),flush=True)
  models,val=v32.fit(X[idx],a[idx],split[idx],SEED+si*100)
  qte=te&q;loc=np.searchsorted(test_rows,np.where(qte)[0]);combined[loc]=pred(models,X[qte])
  stage_results[name]=metrics(a[qte],combined[loc]);files[name]={}
  for mn,m in models.items():
   p=ROOT/f'R32_V43_{name.upper()}_{mn.upper()}_SEED_9714.joblib';joblib.dump(m,p,compress=3);files[name][mn]={'file':p.name,'sha256':sha(p)}
 assert np.all(np.isfinite(combined))
 overall=metrics(a[te],combined);by_mode={};by_trial={}
 mt=mode[te];tt=trial[te];at=a[te]
 for i,n in enumerate(MODES):by_mode[n]=metrics(at[mt==i],combined[mt==i])
 for t in range(12):by_trial[str(t)]=metrics(at[tt==t],combined[tt==t])
 ref=json.loads((ROOT/'R32_V40_HORIZON_HAZARD_POPULATION_REFERENCE_ONLY.json').read_text())['action_value']['arms']['horizon_hazard_variance']
 r=ref['expected_advantage'];delta={'roc_auc':overall['expected_advantage']['roc_auc']-r['roc_auc'],'average_precision':overall['expected_advantage']['average_precision']-r['average_precision'],'tp_cross':overall['expected_advantage']['true_positive_cross_zero']-r['true_positive_cross_zero'],'fp_cross':overall['expected_advantage']['false_positive_cross_zero']-r['false_positive_cross_zero'],'selected_actual_advantage':overall['expected_advantage']['selected_actual_advantage']-r['selected_actual_advantage']}
 out={'experiment':'R32 V43 evaluator diagnostic: fixed learner-visible evidence-count stage specialists over unchanged V40 action state/targets','stages':STAGES,'overall':overall,'stage_results':stage_results,'by_trial':by_trial,'by_mode_evaluator_only':by_mode,'delta_vs_global_v40':delta,'model_files':files,'seconds':time.time()-t0,'boundary':'REFERENCE_ONLY DIAGNOSTIC. Stage is derived only from observed evidence count. Fixed stage bins are not a promoted runtime mechanism; they test whether global action-model interference causes early option-credit loss. Mode/ambiguity/resource labels are excluded from features.'}
 p=ROOT/'R32_V43_STAGE_SPECIALIST_DIAGNOSTIC_REFERENCE_ONLY.json';p.write_text(json.dumps(out,indent=2));cfg={'status':'REFERENCE_ONLY_STAGE_SPECIALIST_DIAGNOSTIC','fixed_stage_bins_promotable':False,'runtime_fixed_probe_count':False,'native_promotion_allowed':False,'source_sha256':sha(Path(__file__))};(ROOT/'R32_V43_CONFIG.json').write_text(json.dumps(cfg,indent=2));(ROOT/'R32_V43_TRAINING.log').write_text(json.dumps({'overall':overall,'delta_vs_global_v40':delta,'seconds':out['seconds']},indent=2)+'\n');print(json.dumps({'overall':overall,'delta':delta,'stage':stage_results},indent=2))
if __name__=='__main__':main()
