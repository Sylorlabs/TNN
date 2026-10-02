import sys,time,json,joblib,hashlib
from pathlib import Path
import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
R=Path('/mnt/data/r32_epistemic');z=np.load(R/'R32_V18_V16MATCH_TRAINING_DATA_SEED_9714.npz');name=sys.argv[1];seed=97208
if name in ('keep','commit','epoch','unknown'):
 X=z['X'];key={'keep':'yk','commit':'yc','epoch':'ye','unknown':'yu'}[name];y=z[key];off={'keep':0,'commit':1,'epoch':2,'unknown':3}[name];m=HistGradientBoostingRegressor(random_state=seed+off,max_iter=140,max_leaf_nodes=23,min_samples_leaf=24,l2_regularization=1.0,learning_rate=.055)
elif name=='inspect':
 X=z['Xi'];y=z['Yi'];m=HistGradientBoostingRegressor(random_state=seed+20,max_iter=170,max_leaf_nodes=27,min_samples_leaf=22,l2_regularization=1.0,learning_rate=.055)
else:raise SystemExit(name)
t=time.time();m.fit(X,y);p=R/f'R32_V19_BASE_{name.upper()}_SEED_9714.joblib';joblib.dump(m,p,compress=3);o={'model':name,'rows':len(X),'feature_dim':X.shape[1],'target_mean':float(y.mean()),'fit_seconds':time.time()-t,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()};(R/f'R32_V19_BASE_{name.upper()}_SEED_9714.json').write_text(json.dumps(o,indent=2));print(json.dumps(o,indent=2))
