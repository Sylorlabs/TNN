from __future__ import annotations
import hashlib,json,time
from pathlib import Path
import joblib,numpy as np
from sklearn.metrics import roc_auc_score,average_precision_score,mean_squared_error,mean_absolute_error
ROOT=Path('/mnt/data/r32_epistemic')
STAGES=[('trial0',0,0),('trial1_2',1,2),('trial3_5',3,5),('trial6_11',6,11)]
MODES=['balanced_no_unique','biased_no_unique','stable_weak','unstable_then_stable','replacement','reversal','costly_stable']
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def safe_logit(p):q=np.clip(np.asarray(p,float),1e-6,1-1e-6);return np.log(q/(1-q)).reshape(-1,1)
def load(name):return {k:joblib.load(ROOT/f'R32_V43_{name.upper()}_{k.upper()}_SEED_9714.joblib') for k in ['classifier','calibrator','positive','nonpositive','direct']}
def pred(m,X):
 raw=m['classifier'].predict_proba(X)[:,1];p=m['calibrator'].predict_proba(safe_logit(raw))[:,1];return p*m['positive'].predict(X)+(1-p)*m['nonpositive'].predict(X)
def metrics(a,ex):
 y=a>0;sel=ex>0;both=len(np.unique(y))>1
 return {'n':len(a),'positive_rate':float(y.mean()),'expected_advantage':{'mse':float(mean_squared_error(a,ex)),'mae':float(mean_absolute_error(a,ex)),'roc_auc':float(roc_auc_score(y,ex)) if both else None,'average_precision':float(average_precision_score(y,ex)) if np.any(y) else None,'true_positive_cross_zero':float(np.mean(ex[y]>0)) if np.any(y) else None,'false_positive_cross_zero':float(np.mean(ex[~y]>0)) if np.any(~y) else None,'predicted_inspect_rate':float(sel.mean()),'selected_actual_advantage':float(a[sel].mean()) if np.any(sel) else None,'mean_pred_actual_positive':float(ex[y].mean()) if np.any(y) else None,'mean_pred_actual_nonpositive':float(ex[~y].mean()) if np.any(~y) else None}}
def main():
 z32=np.load(ROOT/'R32_V32_PREDICTIVE_DYNAMICS_DATA_SEED_9714.npz');z33=np.load(ROOT/'R32_V33_LEARNED_GATING_DATA_SEED_9714.npz');z38=np.load(ROOT/'R32_V38_REPEATED_CONTINUATION_DATA_SEED_9714.npz');z40=np.load(ROOT/'R32_V40_HORIZON_HAZARD_DATA_SEED_9714.npz')
 Xaction=np.c_[z32['X_dynamics'].astype(np.float32),z33['gate_features'].astype(np.float32)];X=np.c_[Xaction,z40['predicted_pair'].astype(np.float32),z38['predicted_repeated_variance'].astype(np.float32),z40['hazard_features'].astype(np.float32)]
 a=z32['advantage'].astype(float);split=z32['split_code'].astype(int);trial=z32['trial_index'].astype(int);mode=z32['mode_evaluator_only'].astype(int);te=split>=8;test_rows=np.where(te)[0];combined=np.full(te.sum(),np.nan);stage_results={};files={}
 for name,lo,hi in STAGES:
  q=(trial>=lo)&(trial<=hi);qte=te&q;loc=np.searchsorted(test_rows,np.where(qte)[0]);m=load(name);combined[loc]=pred(m,X[qte]);stage_results[name]=metrics(a[qte],combined[loc]);files[name]={k:{'file':f'R32_V43_{name.upper()}_{k.upper()}_SEED_9714.joblib','sha256':sha(ROOT/f'R32_V43_{name.upper()}_{k.upper()}_SEED_9714.joblib')} for k in m}
 assert np.all(np.isfinite(combined));at=a[te];mt=mode[te];tt=trial[te];overall=metrics(at,combined);by_mode={n:metrics(at[mt==i],combined[mt==i]) for i,n in enumerate(MODES)};by_trial={str(t):metrics(at[tt==t],combined[tt==t]) for t in range(12)}
 refarm=json.loads((ROOT/'R32_V40_HORIZON_HAZARD_POPULATION_REFERENCE_ONLY.json').read_text())['action_value']['arms']['horizon_hazard_variance'];r=refarm['expected_advantage'];delta={'roc_auc':overall['expected_advantage']['roc_auc']-r['roc_auc'],'tp_cross':overall['expected_advantage']['true_positive_cross_zero']-r['true_positive_cross_zero'],'fp_cross':overall['expected_advantage']['false_positive_cross_zero']-r['false_positive_cross_zero'],'selected_actual_advantage':overall['expected_advantage']['selected_actual_advantage']-r['actual_mean_selected']}
 out={'experiment':'R32 V43 evaluator diagnostic: fixed learner-visible evidence-count stage specialists over unchanged V40 action state/targets','stages':STAGES,'overall':overall,'stage_results':stage_results,'by_trial':by_trial,'by_mode_evaluator_only':by_mode,'delta_vs_global_v40':delta,'model_files':files,'boundary':'REFERENCE_ONLY DIAGNOSTIC. Stage is derived only from observed evidence count. Fixed stage bins are not a promoted runtime mechanism; they test whether global action-model interference causes early option-credit loss. Mode/ambiguity/resource labels are excluded from features.'}
 (ROOT/'R32_V43_STAGE_SPECIALIST_DIAGNOSTIC_REFERENCE_ONLY.json').write_text(json.dumps(out,indent=2));cfg={'status':'REFERENCE_ONLY_STAGE_SPECIALIST_DIAGNOSTIC','fixed_stage_bins_promotable':False,'runtime_fixed_probe_count':False,'native_promotion_allowed':False,'source_sha256':sha(ROOT/'r32_v43_stage_specialist_diagnostic.py'),'completion_source_sha256':sha(Path(__file__))};(ROOT/'R32_V43_CONFIG.json').write_text(json.dumps(cfg,indent=2));(ROOT/'R32_V43_TRAINING.log').write_text(json.dumps({'overall':overall,'delta_vs_global_v40':delta},indent=2)+'\n');print(json.dumps({'overall':overall,'delta':delta,'stage':stage_results},indent=2))
if __name__=='__main__':main()
