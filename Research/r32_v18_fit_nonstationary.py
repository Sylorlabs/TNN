import json,joblib,hashlib
from pathlib import Path
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score,average_precision_score,brier_score_loss,log_loss
R=Path('/mnt/data/r32_epistemic');z=np.load(R/'R32_V18_V16MATCH_TRAINING_DATA_SEED_9714.npz');X=z['X'];y=z['yn'].astype(int);cut=28656
# Remove the two R31-decision relationship features; this latent hypothesis receives world/evidence dynamics only.
proj=lambda q:np.delete(q,[q.shape[1]-6,q.shape[1]-5],axis=1)
Xt=proj(X[:cut]);Xv=proj(X[cut:]);yt=y[:cut];yv=y[cut:]
m=HistGradientBoostingClassifier(random_state=18018,max_iter=120,max_leaf_nodes=15,min_samples_leaf=35,l2_regularization=1.0,learning_rate=.05).fit(Xt,yt)
p=m.predict_proba(Xv)[:,1]
metrics={'train_rows':len(Xt),'validation_rows':len(Xv),'train_positive_rate':float(yt.mean()),'validation_positive_rate':float(yv.mean()),'roc_auc':float(roc_auc_score(yv,p)),'average_precision':float(average_precision_score(yv,p)),'brier':float(brier_score_loss(yv,p)),'log_loss':float(log_loss(yv,p)),'mean_mass_nonconvergent':float(p[yv==1].mean()),'mean_mass_convergent':float(p[yv==0].mean()),'feature_dim':Xt.shape[1],'removed_qfeat_columns':[54,55],'target':'delayed grounded windows remain non-convergent; no evaluator ambiguity/mode label'}
joblib.dump(m,R/'R32_V18_NONSTATIONARY_HYPOTHESIS_SEED_9714.joblib',compress=3);metrics['model_sha256']=hashlib.sha256((R/'R32_V18_NONSTATIONARY_HYPOTHESIS_SEED_9714.joblib').read_bytes()).hexdigest();(R/'R32_V18_NONSTATIONARY_HYPOTHESIS_VALIDATION.json').write_text(json.dumps(metrics,indent=2));print(json.dumps(metrics,indent=2))
