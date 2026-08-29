from __future__ import annotations
import hashlib,json,sys,time
from pathlib import Path
import joblib,numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier,HistGradientBoostingRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.isotonic import IsotonicRegression
from sklearn.metrics import roc_auc_score,average_precision_score,brier_score_loss,mean_squared_error,mean_absolute_error
R=Path('/mnt/data/r32_epistemic');SEED=9714

def logit(p):q=np.clip(p,1e-6,1-1e-6);return np.log(q/(1-q)).reshape(-1,1)
def onehot(x,n):return np.eye(n,dtype=np.float32)[x.astype(int)]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def met_sign(y,p):return {'roc_auc':float(roc_auc_score(y,p)),'average_precision':float(average_precision_score(y,p)),'brier':float(brier_score_loss(y,p)),'mean_p_positive':float(p[y==1].mean()),'mean_p_nonpositive':float(p[y==0].mean())}
def met_value(a,p):
 y=a>0;sel=p>0
 return {'mse':float(mean_squared_error(a,p)),'mae':float(mean_absolute_error(a,p)),'roc_auc':float(roc_auc_score(y,p)),'mean_pred_positive':float(p[y].mean()),'mean_pred_nonpositive':float(p[~y].mean()),'tp_cross':float(np.mean(p[y]>0)),'fp_cross':float(np.mean(p[~y]>0)),'inspect_rate':float(sel.mean()),'actual_mean_selected':float(a[sel].mean()) if np.any(sel) else None,'selected_positive_precision':float(y[sel].mean()) if np.any(sel) else None}

def fit_arm(name,X,a,split):
 y=(a>0).astype(int);tr=split<=5;ca=(split==6)|(split==7);te=split>=8
 print('V31_FIT',name,'dim',X.shape[1],flush=True);t0=time.time()
 clf=HistGradientBoostingClassifier(random_state=31031,max_iter=175,max_leaf_nodes=27,min_samples_leaf=24,l2_regularization=1.,learning_rate=.05).fit(X[tr],y[tr])
 rawca=clf.predict_proba(X[ca])[:,1];cal=LogisticRegression(max_iter=1000).fit(logit(rawca),y[ca]);p=cal.predict_proba(logit(clf.predict_proba(X[te])[:,1]))[:,1]
 reg=HistGradientBoostingRegressor(random_state=31032,max_iter=205,max_leaf_nodes=27,min_samples_leaf=24,l2_regularization=1.,learning_rate=.05).fit(X[tr|ca],a[tr|ca]);q=reg.predict(X[te])
 iso=IsotonicRegression(increasing=True,out_of_bounds='clip',y_min=-5,y_max=1).fit(rawca,a[ca]);u=iso.predict(clf.predict_proba(X[te])[:,1])
 files={}
 for tag,m in [('classifier',clf),('calibrator',cal),('direct',reg),('monotonic_utility',iso)]:
  pth=R/f'R32_V31_{name.upper()}_{tag.upper()}_SEED_9714.joblib';joblib.dump(m,pth,compress=3);files[tag]={'file':pth.name,'sha256':sha(pth)}
 return {'feature_dim':X.shape[1],'rows':{'train':int(tr.sum()),'calibration':int(ca.sum()),'test':int(te.sum())},'positive_rate':{'train':float(y[tr].mean()),'calibration':float(y[ca].mean()),'test':float(y[te].mean())},'sign_classifier':met_sign(y[te],p),'direct_value':met_value(a[te],q),'monotonic_utility':met_value(a[te],u),'seconds':time.time()-t0,'files':files}

def main():
 z=np.load(R/'R32_V30_CANDIDATE_HISTORY_DATA_SEED_9714.npz');X=z['X_history'].astype(np.float32);a=z['advantage'].astype(float);s=z['split_code'];actual=z['actual_opportunity_loss'].astype(np.float32)[:,None]
 hidden=np.c_[onehot(z['mode_evaluator_only'],7),onehot(z['resource_regime_evaluator_only'],5),onehot(z['trial_index'],12)]
 arms={'learner_history':X,'plus_actual_opportunity_loss_EVAL_ONLY':np.c_[X,actual],'plus_hidden_dynamics_EVAL_ONLY':np.c_[X,hidden],'plus_both_EVAL_ONLY':np.c_[X,actual,hidden]}
 out={'experiment':'R32 V31 state-aliasing ceiling audit','seed':SEED,'arms':{},'boundaries':{'learner_history':'valid learner-visible V30 state','actual_opportunity_loss':'EVALUATOR ONLY; future resource opportunity loss unavailable at decision','hidden_dynamics':'EVALUATOR ONLY; mode/resource/trial identity forbidden to cognition'}}
 for name,xx in arms.items():out['arms'][name]=fit_arm(name,xx,a,s)
 base=out['arms']['learner_history'];out['deltas_vs_learner']={}
 for name,q in out['arms'].items():
  if name=='learner_history':continue
  out['deltas_vs_learner'][name]={'classifier_auc':q['sign_classifier']['roc_auc']-base['sign_classifier']['roc_auc'],'classifier_ap':q['sign_classifier']['average_precision']-base['sign_classifier']['average_precision'],'direct_auc':q['direct_value']['roc_auc']-base['direct_value']['roc_auc'],'direct_tp_cross':q['direct_value']['tp_cross']-base['direct_value']['tp_cross'],'direct_fp_cross':q['direct_value']['fp_cross']-base['direct_value']['fp_cross'],'monotonic_tp_cross':q['monotonic_utility']['tp_cross']-base['monotonic_utility']['tp_cross'],'monotonic_fp_cross':q['monotonic_utility']['fp_cross']-base['monotonic_utility']['fp_cross']}
 out['claim_boundary']='REFERENCE_ONLY causal ceiling audit. Evaluator-only arms diagnose missing state but cannot enter TNN cognition or support promotion.'
 p=R/'R32_V31_STATE_ALIASING_CEILING_REFERENCE_ONLY.json';p.write_text(json.dumps(out,indent=2));cfg={'status':'REFERENCE_ONLY_CAUSAL_CEILING_AUDIT','seed':SEED,'native_promotion_allowed':False,'source_sha256':sha(Path(__file__))};(R/'R32_V31_CONFIG.json').write_text(json.dumps(cfg,indent=2));(R/'R32_V31_TRAINING.log').write_text(json.dumps({'deltas_vs_learner':out['deltas_vs_learner'],'arms':{k:{'sign':v['sign_classifier'],'direct':v['direct_value'],'monotonic':v['monotonic_utility']} for k,v in out['arms'].items()}},indent=2)+'\n');print(json.dumps({'deltas':out['deltas_vs_learner'],'arms':{k:{'sign':v['sign_classifier'],'direct':v['direct_value'],'monotonic':v['monotonic_utility']} for k,v in out['arms'].items()}},indent=2))
if __name__=='__main__':main()
