from pathlib import Path
import json,joblib
import numpy as np
ROOT=Path('/mnt/data/r32_epistemic')
import sys
sys.path.insert(0,str(ROOT))
import r32_v32_predictive_dynamics_population as v32
z32=np.load(ROOT/'R32_V32_PREDICTIVE_DYNAMICS_DATA_SEED_9714.npz')
z38=np.load(ROOT/'R32_V38_REPEATED_CONTINUATION_DATA_SEED_9714.npz')
z40=np.load(ROOT/'R32_V40_HORIZON_HAZARD_DATA_SEED_9714.npz')
z33=np.load(ROOT/'R32_V33_LEARNED_GATING_DATA_SEED_9714.npz')
Xaction=np.c_[z32['X_dynamics'].astype(np.float32),z33['gate_features'].astype(np.float32)]
X=np.c_[Xaction,z40['predicted_pair'].astype(np.float32),z38['predicted_repeated_variance'].astype(np.float32),z40['hazard_features'].astype(np.float32)]
a=z32['advantage'].astype(float);te=z32['split_code']>=8
clf=joblib.load(ROOT/'R32_V40_HORIZON_HAZARD_VARIANCE_CLASSIFIER_SEED_9714.joblib');cal=joblib.load(ROOT/'R32_V40_HORIZON_HAZARD_VARIANCE_CALIBRATOR_SEED_9714.joblib');pos=joblib.load(ROOT/'R32_V40_HORIZON_HAZARD_VARIANCE_POSITIVE_SEED_9714.joblib');neg=joblib.load(ROOT/'R32_V40_HORIZON_HAZARD_VARIANCE_NONPOSITIVE_SEED_9714.joblib')
def logit(p):q=np.clip(p,1e-6,1-1e-6);return np.log(q/(1-q)).reshape(-1,1)
raw=clf.predict_proba(X[te])[:,1];p=cal.predict_proba(logit(raw))[:,1];ex=p*pos.predict(X[te])+(1-p)*neg.predict(X[te])
at=a[te];mode=z32['mode_evaluator_only'][te].astype(int);res=z32['resource_regime_evaluator_only'][te].astype(int);trial=z32['trial_index'][te].astype(int)
MODES=['balanced_no_unique','biased_no_unique','stable_weak','unstable_then_stable','replacement','reversal','costly_stable'];RES=['generous','balanced','scarce','low_value','volatile']
out={'overall':{},'by_mode_trial':{},'by_mode_resource_trial0':{},'prechange_dynamic':{}}
positive=at>0
def met(q):
 y=positive[q]
 return {'n':int(q.sum()),'actual_positive_rate':float(y.mean()) if q.sum() else None,'actual_mean_advantage':float(at[q].mean()) if q.sum() else None,'predicted_positive_rate':float(np.mean(ex[q]>0)) if q.sum() else None,'tp':float(np.mean(ex[q & positive]>0)) if np.any(q & positive) else None,'fp':float(np.mean(ex[q & ~positive]>0)) if np.any(q & ~positive) else None,'mean_predicted':float(ex[q].mean()) if q.sum() else None,'selected_actual':float(at[q][ex[q]>0].mean()) if np.any(ex[q]>0) else None}
for mi,m in enumerate(MODES):
 out['by_mode_trial'][m]={}
 for t in range(12):out['by_mode_trial'][m][str(t)]=met((mode==mi)&(trial==t))
 out['by_mode_resource_trial0'][m]={}
 for ri,rn in enumerate(RES):out['by_mode_resource_trial0'][m][rn]=met((mode==mi)&(res==ri)&(trial==0))
for m in ['unstable_then_stable','replacement','reversal']:
 mi=MODES.index(m);q=(mode==mi)&(trial<=5);out['prechange_dynamic'][m]=met(q)
(ROOT/'R32_V42_PRECHANGE_OPTION_CREDIT_DIAGNOSTIC.json').write_text(json.dumps(out,indent=2))
print(json.dumps({'trial0':{m:out['by_mode_trial'][m]['0'] for m in MODES},'prechange_dynamic':out['prechange_dynamic']},indent=2))
