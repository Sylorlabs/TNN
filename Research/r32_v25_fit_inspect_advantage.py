import json,joblib,hashlib
from pathlib import Path
from collections import Counter
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier,HistGradientBoostingRegressor
from sklearn.metrics import roc_auc_score,average_precision_score,brier_score_loss,mean_squared_error
R=Path('/mnt/data/r32_epistemic');z=np.load(R/'R32_V18_V16MATCH_TRAINING_DATA_SEED_9714.npz');X=z['X'];Xi=z['Xi'];Yi=z['Yi'];yn=z['yn'].astype(int);cut=28656
keys=[r.tobytes() for r in X];cnt=Counter(keys);xmap={k:i for i,k in enumerate(keys) if cnt[k]==1};rows=[];act=[];ival=[]
for j,r in enumerate(Xi[:,:60]):
 k=r.tobytes()
 if k in xmap:rows.append(xmap[k]);act.append(Xi[j].copy());ival.append(float(Yi[j]))
rows=np.asarray(rows,int);act=np.asarray(act);ival=np.asarray(ival,float);o=np.argsort(rows);rows=rows[o];act=act[o];ival=ival[o]
unres=np.where(yn[rows]==1,1.0,-1.2);term=np.maximum.reduce([z['yk'][rows],z['yc'][rows],z['ye'][rows],z['yu'][rows],unres]);adv=ival-term;y=(adv>0).astype(int);tr=rows<cut;va=~tr
clf=HistGradientBoostingClassifier(random_state=25025,max_iter=160,max_leaf_nodes=19,min_samples_leaf=30,l2_regularization=1.1,learning_rate=.05).fit(act[tr],y[tr]);p=clf.predict_proba(act[va])[:,1];pos=float(adv[tr][y[tr]==1].mean());neg=float(adv[tr][y[tr]==0].mean());q=p*pos+(1-p)*neg
reg=HistGradientBoostingRegressor(random_state=25026,max_iter=160,max_leaf_nodes=19,min_samples_leaf=30,l2_regularization=1.1,learning_rate=.05).fit(act[tr],adv[tr]);qr=reg.predict(act[va])
met={'train_rows':int(tr.sum()),'validation_rows':int(va.sum()),'train_advantage_positive_rate':float(y[tr].mean()),'validation_advantage_positive_rate':float(y[va].mean()),'roc_auc_advantage_classifier':float(roc_auc_score(y[va],p)),'average_precision':float(average_precision_score(y[va],p)),'brier':float(brier_score_loss(y[va],p)),'mean_positive_advantage_train':pos,'mean_nonpositive_advantage_train':neg,'classifier_expected_advantage_mse':float(mean_squared_error(adv[va],q)),'regressor_advantage_mse':float(mean_squared_error(adv[va],qr)),'regressor_advantage_auc':float(roc_auc_score(y[va],qr)),'classifier_positive_expected_adv_rate_actual_positive':float(np.mean(q[y[va]==1]>0)),'classifier_positive_expected_adv_rate_actual_nonpositive':float(np.mean(q[y[va]==0]>0)),'mean_expected_adv_actual_positive':float(q[y[va]==1].mean()),'mean_expected_adv_actual_nonpositive':float(q[y[va]==0].mean()),'target':'delayed realized source-specific INSPECT return minus best delayed terminal action utility (KEEP/COMMIT/EPOCH/UNKNOWN/UNRESOLVED); no mode/ambiguity label','feature':'source-specific action feature = current epistemic state + source provenance/cost/dependence'}
for name,m in [('CLASSIFIER',clf),('REGRESSOR',reg)]:
 f=R/f'R32_V25_INSPECT_ADVANTAGE_{name}_SEED_9714.joblib';joblib.dump(m,f,compress=3);met[name.lower()+'_sha256']=hashlib.sha256(f.read_bytes()).hexdigest()
(R/'R32_V25_INSPECT_ADVANTAGE_VALIDATION.json').write_text(json.dumps(met,indent=2));print(json.dumps(met,indent=2))
