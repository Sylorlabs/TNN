from pathlib import Path
import json,joblib
import numpy as np
from sklearn.isotonic import IsotonicRegression
from sklearn.metrics import roc_auc_score,mean_squared_error,mean_absolute_error
R=Path('/mnt/data/r32_epistemic');z=np.load(R/'R32_V30_CANDIDATE_HISTORY_DATA_SEED_9714.npz');X=z['X_history'];a=z['advantage'].astype(float);y=a>0;s=z['split_code'];ca=(s==6)|(s==7);te=s>=8
clf=joblib.load(R/'R32_V30_CLASSIFIER_SEED_9714.joblib');raw_ca=clf.predict_proba(X[ca])[:,1];raw_te=clf.predict_proba(X[te])[:,1]
iso=IsotonicRegression(increasing=True,out_of_bounds='clip',y_min=-4,y_max=1).fit(raw_ca,a[ca]);ui=iso.predict(raw_te)
posmean=float(a[ca][y[ca]].mean());negmean=float(a[ca][~y[ca]].mean());
# calibrated sign probability from V30
cal=joblib.load(R/'R32_V30_CALIBRATOR_SEED_9714.joblib')
def logit(p):q=np.clip(p,1e-6,1-1e-6);return np.log(q/(1-q)).reshape(-1,1)
p=cal.predict_proba(logit(raw_te))[:,1];ug=p*posmean+(1-p)*negmean
at=a[te];yt=y[te]
def met(q):return {'mse':float(mean_squared_error(at,q)),'mae':float(mean_absolute_error(at,q)),'auc':float(roc_auc_score(yt,q)),'mean_pred_positive':float(q[yt].mean()),'mean_pred_nonpositive':float(q[~yt].mean()),'tp_cross':float(np.mean(q[yt]>0)),'fp_cross':float(np.mean(q[~yt]>0)),'inspect_rate':float(np.mean(q>0)),'actual_mean_when_selected':float(at[q>0].mean()) if np.any(q>0) else None,'precision_positive':float(yt[q>0].mean()) if np.any(q>0) else None}
# threshold-free policy utility is q>0; also summarize score deciles
order=np.argsort(raw_te);bins=[]
for ids in np.array_split(order,12):bins.append({'raw_score':float(raw_te[ids].mean()),'actual_positive_rate':float(yt[ids].mean()),'actual_advantage':float(at[ids].mean()),'isotonic_utility':float(ui[ids].mean())})
out={'calibration_rows':int(ca.sum()),'test_rows':int(te.sum()),'calibration_conditional_means':{'positive':posmean,'nonpositive':negmean},'isotonic_utility':met(ui),'global_mixture':met(ug),'score_bins':bins,'isotonic_knots':{'x':iso.X_thresholds_.tolist(),'y':iso.y_thresholds_.tolist()}}
(R/'R32_V30_MONOTONIC_UTILITY_DIAGNOSTIC.json').write_text(json.dumps(out,indent=2));joblib.dump(iso,R/'R32_V30_MONOTONIC_UTILITY_DIAGNOSTIC.joblib',compress=3);print(json.dumps(out,indent=2))
