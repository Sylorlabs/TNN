import json,joblib,hashlib
from pathlib import Path
import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import roc_auc_score,mean_squared_error
R=Path('/mnt/data/r32_epistemic');z=np.load(R/'R32_V18_V16MATCH_TRAINING_DATA_SEED_9714.npz');X=z['X'];yn=z['yn'].astype(int);cut=28656
proj=lambda q:np.delete(q,[q.shape[1]-6,q.shape[1]-5],axis=1)
y=np.where(yn==1,1.0,-1.2);Xt=proj(X[:cut]);Xv=proj(X[cut:]);yt=y[:cut];yv=y[cut:];nv=yn[cut:]
m=HistGradientBoostingRegressor(random_state=19019,max_iter=120,max_leaf_nodes=15,min_samples_leaf=35,l2_regularization=1.0,learning_rate=.05).fit(Xt,yt);p=m.predict(Xv)
metrics={'train_rows':len(Xt),'validation_rows':len(Xv),'target_nonconvergent':1.0,'target_later_resolved':-1.2,'validation_nonconvergent_rate':float(nv.mean()),'roc_auc_using_action_value':float(roc_auc_score(nv,p)),'mse':float(mean_squared_error(yv,p)),'mean_q_nonconvergent':float(p[nv==1].mean()),'mean_q_convergent':float(p[nv==0].mean()),'positive_q_rate_nonconvergent':float(np.mean(p[nv==1]>0)),'positive_q_rate_convergent':float(np.mean(p[nv==0]>0)),'feature_dim':Xt.shape[1],'removed_qfeat_columns':[54,55],'training_signal':'delayed grounded convergence/non-convergence regret only; no ambiguity/mode label'}
f=R/'R32_V19_UNRESOLVED_TEMPORAL_ACTION_SEED_9714.joblib';joblib.dump(m,f,compress=3);metrics['sha256']=hashlib.sha256(f.read_bytes()).hexdigest();(R/'R32_V19_UNRESOLVED_TEMPORAL_ACTION_VALIDATION.json').write_text(json.dumps(metrics,indent=2));print(json.dumps(metrics,indent=2))
