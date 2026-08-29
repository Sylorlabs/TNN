import json,joblib,hashlib
from pathlib import Path
import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_squared_error,roc_auc_score
R=Path('/mnt/data/r32_epistemic');z=np.load(R/'R32_V24_HORIZON_DATA_SEED_9714.npz');X=z['X'];Y=z['Y'];E=z['episode'];H=z['horizons'];tr=E<330;va=~tr;met={'train_rows':int(tr.sum()),'validation_rows':int(va.sum()),'horizons':H.tolist(),'models':{}}
for i,h in enumerate(H):
 m=HistGradientBoostingRegressor(random_state=24024+int(h),max_iter=150,max_leaf_nodes=15,min_samples_leaf=18,l2_regularization=1.0,learning_rate=.05).fit(X[tr],Y[tr,i]);p=m.predict(X[va]);y=Y[va,i];d={'mse':float(mean_squared_error(y,p)),'target_mean':float(y.mean()),'pred_mean':float(p.mean()),'positive_rate':float(np.mean(y>0)),'pred_positive_rate':float(np.mean(p>0))}
 if len(np.unique(y>0))>1:d['positive_value_auc']=float(roc_auc_score(y>0,p))
 f=R/f'R32_V24_HORIZON_VALUE_H{int(h)}_SEED_9714.joblib';joblib.dump(m,f,compress=3);d['sha256']=hashlib.sha256(f.read_bytes()).hexdigest();met['models'][str(int(h))]=d
# policy-level validation: choose horizon with highest predicted continuation value versus true best horizon
mods=[joblib.load(R/f'R32_V24_HORIZON_VALUE_H{int(h)}_SEED_9714.joblib') for h in H];P=np.column_stack([m.predict(X[va]) for m in mods]);best=np.argmax(P,axis=1);true=np.argmax(Y[va],axis=1);chosen=Y[va][np.arange(va.sum()),best];oracle=Y[va][np.arange(va.sum()),true]
met['policy_validation']={'chosen_actual_mean':float(chosen.mean()),'oracle_actual_mean':float(oracle.mean()),'horizon_choice_accuracy':float(np.mean(best==true)),'positive_chosen_rate':float(np.mean(chosen>0)),'positive_oracle_rate':float(np.mean(oracle>0)),'predicted_best_mean':float(np.max(P,axis=1).mean())}
(R/'R32_V24_HORIZON_VALUE_VALIDATION.json').write_text(json.dumps(met,indent=2));print(json.dumps(met,indent=2))
