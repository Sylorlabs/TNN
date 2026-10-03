from pathlib import Path
import json, joblib
import numpy as np
from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss, mean_absolute_error
ROOT=Path('/mnt/data/r32_epistemic')
z=np.load(ROOT/'R32_V29_RESOURCE_GROUNDED_INSPECT_DATA_SEED_9714.npz')
X=z['X'];a=z['advantage'].astype(float);y=(a>0).astype(int);s=z['split_code'];te=s>=8
clf=joblib.load(ROOT/'R32_V29_CLASSIFIER_SEED_9714.joblib');cal=joblib.load(ROOT/'R32_V29_CALIBRATOR_SEED_9714.joblib');pos=joblib.load(ROOT/'R32_V29_POSITIVE_SEED_9714.joblib');neg=joblib.load(ROOT/'R32_V29_NONPOSITIVE_SEED_9714.joblib')
def logit(p):
 q=np.clip(p,1e-6,1-1e-6);return np.log(q/(1-q)).reshape(-1,1)
raw=clf.predict_proba(X[te])[:,1];p=cal.predict_proba(logit(raw))[:,1];qp=pos.predict(X[te]);qn=neg.predict(X[te]);ex=p*qp+(1-p)*qn
at=a[te];yt=y[te];mode=z['mode_evaluator_only'][te];res=z['resource_regime_evaluator_only'][te];trial=z['trial_index'][te]
MODES=['balanced_no_unique','biased_no_unique','stable_weak','unstable_then_stable','replacement','reversal','costly_stable']
RES=['generous','balanced','scarce','low_value','volatile']
def block(mask):
 yy=yt[mask];aa=at[mask];pp=p[mask];rr=raw[mask];qpp=qp[mask];qnn=qn[mask];ee=ex[mask]
 d={'n':int(mask.sum()),'positive_rate':float(yy.mean()),'raw_p_mean':float(rr.mean()),'cal_p_mean':float(pp.mean()),'actual_mean':float(aa.mean()),'qp_mean':float(qpp.mean()),'qn_mean':float(qnn.mean()),'expected_mean':float(ee.mean()),'inspect_rate':float(np.mean(ee>0)),'false_positive_rate':float(np.mean(ee[yy==0]>0)) if np.any(yy==0) else None,'true_positive_rate':float(np.mean(ee[yy==1]>0)) if np.any(yy==1) else None}
 if len(set(yy))>1:d['auc_p']=float(roc_auc_score(yy,pp));d['auc_ex']=float(roc_auc_score(yy,ee));d['ap_p']=float(average_precision_score(yy,pp))
 if np.any(yy==1):d['positive']={'p':float(pp[yy==1].mean()),'qp':float(qpp[yy==1].mean()),'qn':float(qnn[yy==1].mean()),'ex':float(ee[yy==1].mean()),'actual':float(aa[yy==1].mean())}
 if np.any(yy==0):d['nonpositive']={'p':float(pp[yy==0].mean()),'qp':float(qpp[yy==0].mean()),'qn':float(qnn[yy==0].mean()),'ex':float(ee[yy==0].mean()),'actual':float(aa[yy==0].mean())}
 return d
out={'overall':block(np.ones_like(yt,dtype=bool)),'by_mode':{n:block(mode==i) for i,n in enumerate(MODES)},'by_resource':{n:block(res==i) for i,n in enumerate(RES)},'by_trial':{str(i):block(trial==i) for i in range(12)}}
# calibration bins, equal-frequency
order=np.argsort(p);bins=[]
for idx in np.array_split(order,10):bins.append({'n':len(idx),'mean_p':float(p[idx].mean()),'actual_positive':float(yt[idx].mean()),'mean_advantage':float(at[idx].mean()),'mean_expected':float(ex[idx].mean())})
out['calibration_deciles']=bins
# Decompose cross-zero boundary p*qp+(1-p)*qn > 0 => p > -qn/(qp-qn)
thr=np.where(qp>qn,-qn/(qp-qn),np.inf);out['boundary']={'threshold_mean_positive':float(np.mean(thr[yt==1])),'p_mean_positive':float(np.mean(p[yt==1])),'threshold_mean_nonpositive':float(np.mean(thr[yt==0])),'p_mean_nonpositive':float(np.mean(p[yt==0])),'positive_p_minus_boundary_mean':float(np.mean(p[yt==1]-thr[yt==1])),'nonpositive_p_minus_boundary_mean':float(np.mean(p[yt==0]-thr[yt==0]))}
(ROOT/'R32_V29_VALUE_COMPOSITION_DIAGNOSTIC.json').write_text(json.dumps(out,indent=2));print(json.dumps({'overall':out['overall'],'boundary':out['boundary'],'calibration_deciles':bins},indent=2))
