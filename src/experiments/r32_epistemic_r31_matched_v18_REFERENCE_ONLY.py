from __future__ import annotations
import sys,json,hashlib,joblib
from pathlib import Path
import numpy as np
sys.path.insert(0,'/mnt/data/r32_epistemic')
from r32_epistemic_r31_matched_v17_cached_REFERENCE_ONLY import *
import r32_epistemic_r31_matched_v17_cached_REFERENCE_ONLY as v17base
OUT=Path('/mnt/data/r32_epistemic')

def nonstationary_world_features(q):
 # q_feat ends with [R31-is-UNKNOWN, R31-agrees-with-global, epoch_margin,
 # epoch_peak, epoch==global, epoch==recent]. Remove the two policy-relation
 # fields so the temporal hypothesis is grounded only in evidence/world dynamics.
 return np.delete(np.asarray(q),[len(q)-6,len(q)-5])

def nonstationary_mass(q,model):
 return float(model.predict_proba(nonstationary_world_features(q)[None,:])[0,1])

def augmented_q_feat(st,ep,safe,a_dec,env,nonstat):
 q=v17base.q_feat(st,ep,safe,a_dec,env);m=nonstationary_mass(q,nonstat);return np.r_[q,m],m

def d_values(st,models,ep,safe,a_dec,env):
 keep,commit,epoch,unknown,inspect,nonstat,_=models;f,m=augmented_q_feat(st,ep,safe,a_dec,env,nonstat);full=int(env[5][int(np.argmax(st.p(True)))]);epc=int(env[5][int(np.argmax(st.epoch_p()))]);qk=float(keep.predict(f[None,:])[0]);qf=float(commit.predict(f[None,:])[0]);qe=float(epoch.predict(f[None,:])[0]);qu=float(unknown.predict(f[None,:])[0]);return (epc if qe>qf else full),qk,max(qf,qe),qu,f

def inspect_value(st,models,ep,s,safe,a_dec,env):
 f,_=augmented_q_feat(st,ep,safe,a_dec,env,models[5]);gf=np.r_[f,np.eye(S)[s],ep.cost[s],st.group_n[GROUP[s]]/3];return float(models[4].predict(gf[None,:])[0])

def load_models(root=OUT):
 names=['KEEP','COMMIT','EPOCH','UNKNOWN','INSPECT'];ms=[joblib.load(root/f'R32_V18_MODEL_{n}_SEED_9714.joblib') for n in names];non=joblib.load(root/'R32_V18_NONSTATIONARY_HYPOTHESIS_SEED_9714.joblib');meta=json.loads((root/'R32_V18_TRAINING_META.json').read_text());return (*ms,non,meta)
