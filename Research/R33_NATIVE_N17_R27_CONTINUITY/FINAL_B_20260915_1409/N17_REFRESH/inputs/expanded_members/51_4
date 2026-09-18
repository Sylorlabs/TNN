from __future__ import annotations
import json, hashlib, traceback, sys, math
from pathlib import Path
import joblib
import numpy as np
from sklearn.ensemble import ExtraTreesRegressor, ExtraTreesClassifier, HistGradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, roc_auc_score, average_precision_score
from sklearn.model_selection import KFold, GroupKFold, train_test_split
from sklearn.preprocessing import StandardScaler

ROOT=Path('/mnt/data/r32_epistemic');SEED=9714;PREFIX='R32_V40'
sys.path.insert(0,str(ROOT))
import r32_v39_distributional_continuation_value as v39


def atomic_json(p,o):
 t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(o,indent=2));t.replace(p)
def atomic_text(p,s):
 t=p.with_suffix(p.suffix+'.tmp');t.write_text(s);t.replace(p)

def splitter(n,groups):
 if groups is not None and len(np.unique(groups))>=5:return list(GroupKFold(5).split(np.arange(n),groups=groups))
 return list(KFold(5,shuffle=True,random_state=SEED).split(np.arange(n)))

def util(y,p):return float(np.mean(np.where(p>0,y,0)))
def metrics(y,p,name):
 d=v39.metric_block(y,p,name)
 return d

def main():
 npz=v39.locate_v38_npz();z=np.load(npz,allow_pickle=True);s=v39.select_arrays(z);X=s['X'];y=s['y'];g=s['groups'];n=len(y);cv=splitter(n,g)
 pred_hgb=np.zeros(n);pred_et=np.zeros(n);pred_et_risk=np.zeros(n);pred_hybrid=np.zeros(n);pred_resid=np.zeros(n);pred_mix=np.zeros(n)
 lambdas=[];folds=[]
 for fi,(tr,te) in enumerate(cv):
  # Fit global baseline.
  h=HistGradientBoostingRegressor(max_iter=180,max_leaf_nodes=31,min_samples_leaf=35,l2_regularization=1.0,learning_rate=.045,random_state=SEED+fi).fit(X[tr],y[tr])
  ph=h.predict(X[te]);pred_hgb[te]=ph
  # Observable-state neighborhoods via extremely randomized partitions.
  et=ExtraTreesRegressor(n_estimators=220,max_features=.75,min_samples_leaf=12,max_depth=None,n_jobs=4,random_state=SEED+100+fi).fit(X[tr],y[tr])
  tree=np.stack([q.predict(X[te]) for q in et.estimators_]);pe=tree.mean(0);sd=tree.std(0);pred_et[te]=pe
  # Learn the risk conversion only from delayed utility on an inner held-out slice.
  tri,vi=train_test_split(tr,test_size=.20,random_state=SEED+200+fi)
  eti=ExtraTreesRegressor(n_estimators=160,max_features=.75,min_samples_leaf=12,n_jobs=4,random_state=SEED+300+fi).fit(X[tri],y[tri])
  tv=np.stack([q.predict(X[vi]) for q in eti.estimators_]);mv=tv.mean(0);sv=tv.std(0)
  grid=[0.,.05,.10,.15,.20,.30,.45]
  lam=max(grid,key=lambda a:util(y[vi],mv-a*sv));lambdas.append(lam);pred_et_risk[te]=pe-lam*sd
  # Hybrid global/local and residual learner.
  pred_hybrid[te]=.5*ph+.5*pe
  rh=y[tr]-h.predict(X[tr])
  er=ExtraTreesRegressor(n_estimators=180,max_features=.75,min_samples_leaf=16,n_jobs=4,random_state=SEED+400+fi).fit(X[tr],rh)
  pred_resid[te]=ph+er.predict(X[te])
  # Separate sign and magnitude using the same local partitions.
  cl=ExtraTreesClassifier(n_estimators=220,max_features=.75,min_samples_leaf=12,n_jobs=4,class_weight='balanced',random_state=SEED+500+fi).fit(X[tr],y[tr]>0)
  pp=cl.predict_proba(X[te])[:,1];pos=y[tr]>0
  ep=ExtraTreesRegressor(n_estimators=180,max_features=.75,min_samples_leaf=10,n_jobs=4,random_state=SEED+600+fi).fit(X[tr][pos],y[tr][pos])
  en=ExtraTreesRegressor(n_estimators=180,max_features=.75,min_samples_leaf=14,n_jobs=4,random_state=SEED+700+fi).fit(X[tr][~pos],y[tr][~pos])
  pred_mix[te]=pp*ep.predict(X[te])+(1-pp)*en.predict(X[te])
  folds.append({'fold':fi,'train':len(tr),'test':len(te),'lambda_delayed_utility':lam})
 methods={'global_hgb':pred_hgb,'local_extra_trees':pred_et,'local_delayed_utility_risk':pred_et_risk,'global_local_hybrid':pred_hybrid,'global_plus_local_residual':pred_resid,'local_sign_magnitude_mixture':pred_mix,'exact_repeated_experience_ceiling':y.copy()}
 met={k:metrics(y,p,k) for k,p in methods.items()}
 best=max([k for k in methods if k!='exact_repeated_experience_ceiling'],key=lambda k:met[k]['mean_policy_incremental_utility']-.5*met[k]['mean_policy_regret'])
 # Full retained candidate.
 full=ExtraTreesRegressor(n_estimators=320,max_features=.75,min_samples_leaf=12,n_jobs=4,random_state=SEED).fit(X,y);joblib.dump(full,ROOT/f'{PREFIX}_LOCAL_ENSEMBLE_SEED_{SEED}.joblib',compress=3)
 base=met['global_hgb'];b=met[best];ceil=met['exact_repeated_experience_ceiling']
 relative=(base['mean_policy_regret']-b['mean_policy_regret'])/max(1e-12,base['mean_policy_regret'])
 classification='OBSERVABLE_STATE_MODEL_REPAIR_SUPPORTED' if relative>=.15 else 'FUTURE_DYNAMICS_ALIASING_REMAINS'
 out={'experiment':'R32 V40 cross-fitted observable-state neighborhood continuation value','source_dataset':npz.name,'selected_arrays':{k:s[k] for k in ['X_name','y_name','var_name','group_name','single_name']},'rows':n,'feature_dim':X.shape[1],'folds':folds,'learned_risk_lambda_mean':float(np.mean(lambdas)),'metrics':met,'best_nonoracle_method':best,'best_nonoracle_metrics':b,'baseline_global_metrics':base,'relative_regret_reduction_vs_global':relative,'causal_classification':classification,'boundary':'REFERENCE_ONLY. Models receive only retained observable epistemic/candidate-support state and repeated delayed grounded-continuation utility. Generator modes, ambiguity labels, evaluator future state, fixed confidence thresholds, and fixed probe counts are absent. R27 remains canonical; native Zag reproduction mandatory.'}
 atomic_json(ROOT/f'{PREFIX}_OBSERVABLE_STATE_NEIGHBORHOODS_REFERENCE_ONLY.json',out)
 atomic_json(ROOT/f'{PREFIX}_CONFIG.json',{'status':'REFERENCE_ONLY_COMPONENT_EVALUATION','seed':SEED,'change_only':'cross-fitted local observable-state continuation neighborhoods; representation, shadow price, action set, and repeated targets unchanged','runtime_fixed_threshold':False,'runtime_fixed_probe_count':False,'native_promotion_allowed':False,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'source_dataset':npz.name})
 interp=f'''# R32 V40 — Observable-State Continuation Neighborhoods\n\nStatus: **REFERENCE_ONLY / {classification}**\n\nV40 held V38/V39 repeated-continuation targets, retained candidate-support state, provenance, temporal hypotheses, and learned resource shadow price fixed. It changed only the function approximator: global prediction was compared with cross-fitted local ensemble neighborhoods over the same observable state.\n\n## Result\n\nBest non-oracle method: **{best}**.\n\n- true-benefit crossing: **{b['true_positive_crossing']:.4f}**\n- false-positive crossing: **{b['false_positive_crossing']:.4f}**\n- selected realized value: **{b['selected_realized_value']:.4f}**\n- mean policy utility: **{b['mean_policy_incremental_utility']:.4f}**\n- mean regret: **{b['mean_policy_regret']:.6f}**\n- global-model regret: **{base['mean_policy_regret']:.6f}**\n- relative regret reduction: **{relative:.2%}**\n- exact repeated-experience ceiling regret: **{ceil['mean_policy_regret']:.6f}**\n\n## Causal classification\n\n**{classification.replace('_',' ').title()}.** If local neighborhoods materially beat the global model, the principal defect was model/credit smoothing. Otherwise observably similar states still imply different future evidence values, and the next representation must preserve additional causal/future-dynamics state rather than adding thresholds.\n\nR27 remains canonical. Native Zag qualification remains mandatory.\n'''
 atomic_text(ROOT/f'R32_EPISTEMIC_R31_MATCHED_V40_INTERPRETATION.md',interp)
 names=[Path(__file__).name,f'{PREFIX}_CONFIG.json',f'{PREFIX}_OBSERVABLE_STATE_NEIGHBORHOODS_REFERENCE_ONLY.json',f'{PREFIX}_LOCAL_ENSEMBLE_SEED_{SEED}.joblib','R32_EPISTEMIC_R31_MATCHED_V40_INTERPRETATION.md']
 atomic_text(ROOT/f'{PREFIX}_SHA256.txt','\n'.join(f'{hashlib.sha256((ROOT/n).read_bytes()).hexdigest()}  {n}' for n in names if (ROOT/n).exists())+'\n')
 print(json.dumps({'classification':classification,'best':best,'metrics':b,'baseline':base,'relative_regret_reduction':relative},indent=2),flush=True)
if __name__=='__main__':
 try:main()
 except Exception as e:
  atomic_json(ROOT/f'{PREFIX}_FAILED.json',{'status':'FAILED','error':repr(e),'traceback':traceback.format_exc()});raise
