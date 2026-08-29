from __future__ import annotations
import sys,json,joblib
from pathlib import Path
import numpy as np
sys.path.insert(0,'/mnt/data/r32_epistemic')
from r32_epistemic_r31_matched_v17_cached_REFERENCE_ONLY import *
import r32_epistemic_r31_matched_v17_cached_REFERENCE_ONLY as v16base
OUT=Path('/mnt/data/r32_epistemic')
def unresolved_world_features(q):return np.delete(np.asarray(q),[len(q)-6,len(q)-5])
def unresolved_mass(q,nonstat):return float(nonstat.predict_proba(unresolved_world_features(q)[None,:])[0,1])
def unresolved_action_value(m):return m*1.0+(1-m)*(-1.2)
def d_values(st,models,ep,safe,a_dec,env):
 keep,commit,epoch,unknown,inspect,nonstat,waitclf,_=models;q=v16base.q_feat(st,ep,safe,a_dec,env);full=int(env[5][int(np.argmax(st.p(True)))]);epc=int(env[5][int(np.argmax(st.epoch_p()))]);qk=float(keep.predict(q[None,:])[0]);qf=float(commit.predict(q[None,:])[0]);qe=float(epoch.predict(q[None,:])[0]);qu0=float(unknown.predict(q[None,:])[0]);qur=unresolved_action_value(unresolved_mass(q,nonstat));return (epc if qe>qf else full),qk,max(qf,qe),max(qu0,qur),q
def inspect_value(st,models,ep,s,safe,a_dec,env):
 q=v16base.q_feat(st,ep,safe,a_dec,env);gf=np.r_[q,np.eye(S)[s],ep.cost[s],st.group_n[GROUP[s]]/3];return float(models[4].predict(gf[None,:])[0])
def future_wait_value(st,models,ep,safe,a_dec,env):
 q=v16base.q_feat(st,ep,safe,a_dec,env);p=float(models[6].predict_proba(q[None,:])[0,1]);meta=models[7]['wait_benefit_validation'];return p*meta['mean_positive_return_train']+(1-p)*meta['mean_nonpositive_return_train']
def load_models(root=OUT):
 names=['KEEP','COMMIT','EPOCH','UNKNOWN','INSPECT'];ms=[joblib.load(root/f'R32_V19_BASE_{n}_SEED_9714.joblib') for n in names];non=joblib.load(root/'R32_V18_NONSTATIONARY_HYPOTHESIS_SEED_9714.joblib');wait=joblib.load(root/'R32_V21_WAIT_BENEFIT_SEED_9714.joblib');meta=json.loads((root/'R32_V21_TRAINING_META.json').read_text());return (*ms,non,wait,meta)
