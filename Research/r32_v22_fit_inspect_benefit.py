import json,joblib,hashlib
from pathlib import Path
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score,average_precision_score,brier_score_loss
R=Path('/mnt/data/r32_epistemic');z=np.load(R/'R32_V18_V16MATCH_TRAINING_DATA_SEED_9714.npz');X=z['Xi'];ret=z['Yi'];cut=28656;tr=np.arange(len(X))<cut;va=~tr;y=(ret>0).astype(int)
m=HistGradientBoostingClassifier(random_state=22022,max_iter=140,max_leaf_nodes=19,min_samples_leaf=32,l2_regularization=1.0,learning_rate=.05).fit(X[tr],y[tr]);p=m.predict_proba(X[va])[:,1];pos=float(ret[tr][y[tr]==1].mean());neg=float(ret[tr][y[tr]==0].mean());q=p*pos+(1-p)*neg
met={'train_rows':int(tr.sum()),'validation_rows':int(va.sum()),'train_beneficial_rate':float(y[tr].mean()),'validation_beneficial_rate':float(y[va].mean()),'roc_auc_beneficial_inspect':float(roc_auc_score(y[va],p)),'average_precision':float(average_precision_score(y[va],p)),'brier':float(brier_score_loss(y[va],p)),'mean_positive_return_train':pos,'mean_nonpositive_return_train':neg,'mean_expected_q_actual_beneficial':float(q[y[va]==1].mean()),'mean_expected_q_actual_nonbeneficial':float(q[y[va]==0].mean()),'positive_expected_q_rate_beneficial':float(np.mean(q[y[va]==1]>0)),'positive_expected_q_rate_nonbeneficial':float(np.mean(q[y[va]==0]>0)),'utility_formula':'P(inspect_beneficial)*mean_positive_return + (1-P)*mean_nonpositive_return','target':'actual episodic backward source-specific inspect return > 0; no mode/ambiguity label'}
f=R/'R32_V22_INSPECT_BENEFIT_SEED_9714.joblib';joblib.dump(m,f,compress=3);met['sha256']=hashlib.sha256(f.read_bytes()).hexdigest();(R/'R32_V22_INSPECT_BENEFIT_VALIDATION.json').write_text(json.dumps(met,indent=2));print(json.dumps(met,indent=2))
