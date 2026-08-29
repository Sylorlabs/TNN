import json,joblib,hashlib
from pathlib import Path
from collections import Counter
import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_squared_error,roc_auc_score
R=Path('/mnt/data/r32_epistemic');z=np.load(R/'R32_V18_V16MATCH_TRAINING_DATA_SEED_9714.npz');X=z['X'];Xi=z['Xi'];Yi=z['Yi'];cut=28656
keys=[r.tobytes() for r in X];cnt=Counter(keys);xmap={k:i for i,k in enumerate(keys) if cnt[k]==1};rows=[];vals=[];act=[]
for j,r in enumerate(Xi[:,:60]):
 k=r.tobytes()
 if k in xmap:rows.append(xmap[k]);vals.append(float(Yi[j]));act.append(Xi[j].copy())
rows=np.asarray(rows,int);vals=np.asarray(vals,float);act=np.asarray(act);order=np.argsort(rows);rows=rows[order];vals=vals[order];act=act[order];XX=X[rows]
v20=np.load(R/'R32_V20_WAIT_VALUE_DATA_SEED_9714.npz');assert np.array_equal(rows,v20['rows']);assert np.allclose(XX,v20['X']);assert np.allclose(vals,v20['wait_value'])
inspect=joblib.load(R/'R32_V19_BASE_INSPECT_SEED_9714.joblib');qi=inspect.predict(act)
wait=joblib.load(R/'R32_V21_WAIT_BENEFIT_SEED_9714.joblib');wm=json.loads((R/'R32_V21_WAIT_BENEFIT_VALIDATION.json').read_text());p=wait.predict_proba(XX)[:,1];qw=p*wm['mean_positive_return_train']+(1-p)*wm['mean_nonpositive_return_train']
F=np.column_stack([XX,qi,qw,qi-qw]);target=vals-qi;tr=rows<cut;va=~tr
m=HistGradientBoostingRegressor(random_state=23023,max_iter=140,max_leaf_nodes=19,min_samples_leaf=32,l2_regularization=1.2,learning_rate=.05).fit(F[tr],target[tr]);corr=m.predict(F[va]);fused=qi[va]+corr;actual=vals[va]
def auc(x):return float(roc_auc_score(actual>0,x))
met={'train_rows':int(tr.sum()),'validation_rows':int(va.sum()),'feature_dim':int(F.shape[1]),'raw_inspect_mse':float(mean_squared_error(actual,qi[va])),'wait_expected_mse':float(mean_squared_error(actual,qw[va])),'fused_residual_mse':float(mean_squared_error(actual,fused)),'raw_inspect_benefit_auc':auc(qi[va]),'wait_benefit_auc':auc(qw[va]),'fused_benefit_auc':auc(fused),'mean_residual_target_train':float(target[tr].mean()),'mean_pred_correction_validation':float(corr.mean()),'mean_fused_actual_beneficial':float(fused[actual>0].mean()),'mean_fused_actual_nonbeneficial':float(fused[actual<=0].mean()),'target':'actual grounded source-specific inspect return minus inherited recursive INSPECT Q; no mode/ambiguity label','features':'epistemic state + inherited INSPECT Q + V21 WAIT expected utility + their difference'}
f=R/'R32_V23_INSPECT_RESIDUAL_SEED_9714.joblib';joblib.dump(m,f,compress=3);met['sha256']=hashlib.sha256(f.read_bytes()).hexdigest();(R/'R32_V23_INSPECT_RESIDUAL_VALIDATION.json').write_text(json.dumps(met,indent=2));print(json.dumps(met,indent=2))
