import json,joblib,hashlib
from pathlib import Path
from collections import Counter,defaultdict,deque
import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_squared_error,roc_auc_score
R=Path('/mnt/data/r32_epistemic');z=np.load(R/'R32_V18_V16MATCH_TRAINING_DATA_SEED_9714.npz');X=z['X'];Xi=z['Xi'];Yi=z['Yi'];yn=z['yn'].astype(int);cut=28656
# Exact prefix match. Exclude duplicated state-feature keys so action returns cannot be assigned across indistinguishable duplicated rows arbitrarily.
keys=[r.tobytes() for r in X];cnt=Counter(keys);xmap={k:i for i,k in enumerate(keys) if cnt[k]==1};rows=[];vals=[]
for j,r in enumerate(Xi[:,:60]):
 k=r.tobytes()
 if k in xmap:rows.append(xmap[k]);vals.append(float(Yi[j]))
rows=np.asarray(rows,int);vals=np.asarray(vals,float);order=np.argsort(rows);rows=rows[order];vals=vals[order];XX=X[rows];yy=yn[rows]
tr=rows<cut;va=~tr;m=HistGradientBoostingRegressor(random_state=20020,max_iter=140,max_leaf_nodes=19,min_samples_leaf=32,l2_regularization=1.0,learning_rate=.05).fit(XX[tr],vals[tr]);p=m.predict(XX[va]);conv=1-yy[va]
met={'total_unique_states':len(rows),'excluded_duplicate_state_rows':int(len(X)-len(rows)),'train_rows':int(tr.sum()),'validation_rows':int(va.sum()),'validation_mse':float(mean_squared_error(vals[va],p)),'roc_auc_future_convergence_using_wait_value':float(roc_auc_score(conv,p)),'mean_pred_wait_nonconvergent':float(p[yy[va]==1].mean()),'mean_pred_wait_convergent':float(p[yy[va]==0].mean()),'positive_pred_wait_nonconvergent':float(np.mean(p[yy[va]==1]>0)),'positive_pred_wait_convergent':float(np.mean(p[yy[va]==0]>0)),'actual_positive_wait_nonconvergent':float(np.mean(vals[va][yy[va]==1]>0)),'actual_positive_wait_convergent':float(np.mean(vals[va][yy[va]==0]>0)),'feature_dim':XX.shape[1],'target':'episodic backward multi-step observation return net of experienced cost; no mode/ambiguity label'}
f=R/'R32_V20_FUTURE_WAIT_VALUE_SEED_9714.joblib';joblib.dump(m,f,compress=3);met['sha256']=hashlib.sha256(f.read_bytes()).hexdigest();(R/'R32_V20_FUTURE_WAIT_VALUE_VALIDATION.json').write_text(json.dumps(met,indent=2));np.savez_compressed(R/'R32_V20_WAIT_VALUE_DATA_SEED_9714.npz',rows=rows,X=XX,wait_value=vals,yn=yy);print(json.dumps(met,indent=2))
