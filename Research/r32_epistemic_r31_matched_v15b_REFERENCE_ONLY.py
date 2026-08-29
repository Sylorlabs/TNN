from __future__ import annotations
import sys, math, json, hashlib
from pathlib import Path
import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
sys.path.insert(0,'/mnt/data/r32_epistemic')
import r32_epistemic_r31_matched_v14b_REFERENCE_ONLY as base
from r32_epistemic_r31_matched_v14b_REFERENCE_ONLY import *

OUT=Path('/mnt/data/r32_epistemic')

def train_D(seed,env,safe,n=2200):
 rng=np.random.default_rng(seed);X=[];yk=[];yc=[];yu=[];Xi=[];Yi=[]
 normal_starts=resource_starts=source7_only=uncertain_unique=uncertain_nonconv=uncertain_unique_source7_only=regret_replay=0
 choices=KINDS+['genuine_ambiguity']*5+['delayed_distinguishing']*2+['entity_replacement']*2+['apparent_replacement_reverses']*2
 def action_feature(st,ep,s,cost,a0):
  f=q_feat(st,ep,safe,a0,env);return np.r_[f,np.eye(S)[s],cost,st.group_n[GROUP[s]]/3]
 def resource_start(ep,cons,base_state,a0,force7=False):
  nonlocal resource_starts,source7_only,uncertain_unique,uncertain_nonconv,uncertain_unique_source7_only
  rs=base_state.clone();mask=ep.avail.copy();keep_prob=float(rng.beta(1.25,2.0))
  for q in range(2,7):mask[q]=bool(mask[q] and rng.random()<keep_prob)
  mask[7]=bool(ep.avail[7])
  if force7:
   for q in range(2,7):mask[q]=False
  costs=ep.cost.copy()
  for q in range(2,S):costs[q]=float(costs[q]*np.exp(rng.uniform(math.log(.60),math.log(2.40))))
  resource_starts+=1;only7=bool(mask[7] and not np.any(mask[2:7]));source7_only+=int(only7)
  ent=entropy(rs.p(True))
  if ent>=.55:
   if cons is None:uncertain_nonconv+=1
   else:uncertain_unique+=1;uncertain_unique_source7_only+=int(only7)
  return rs,a0,mask,costs,12
 def terminal_values(st,a0,cons):
  cand=int(env[5][int(np.argmax(st.p(True)))])
  return (delayed_action_utility(a0,cons),delayed_action_utility(cand,cons),0.0)
 for j in range(n):
  kind=str(rng.choice(choices));ep=make_ep(seed*100000+j*19+7,kind,env)
  if rng.random()<.68:ep.dev_dynamic_mode=int(rng.integers(0,6))
  adec,_,ap=run_A(ep,env,safe);cons=delayed_consensus(ep);starts=[]
  st=initial_state(ep,env,'D')
  for q,v in ap:st.add(q,v,ep.cost[q])
  starts.append((st,adec,ep.avail.copy(),ep.cost.copy(),10));normal_starts+=1
  rs0=initial_state(ep,env,'D');radec=int(env[5][int(np.argmax(rs0.p(True)))])
  if rng.random()<.45:starts.append(resource_start(ep,cons,rs0,radec,False))
  # Delayed-outcome-balanced regret replay: non-convergent histories are eligible
  # for the same high-uncertainty replay as later-unique histories. The learner is
  # never given a mode/ambiguity label; eligibility uses only its current entropy,
  # while terminal utility still comes from delayed grounded outcomes.
  u=entropy(rs0.p(True))
  if rng.random()<u:
   starts.append(resource_start(ep,cons,rs0,radec,bool(rng.random()<.5)));regret_replay+=1
  for st,a0,mask,costs,stages in starts:
   used=[];path=[]
   for stage in range(stages):
    f=q_feat(st,ep,safe,a0,env);cand=int(env[5][int(np.argmax(st.p(True)))])
    X.append(f);yk.append(delayed_action_utility(a0,cons));yc.append(delayed_action_utility(cand,cons));yu.append(0.0)
    available=[q for q in range(2,S) if mask[q] and (not st.seen[q] or q==7)]
    if not available:break
    # Exploratory developmental behavior: repeated source-7 trials are sampled often when
    # available, so delayed multi-trial outcomes can assign credit backward. This is
    # exploration during development, not a runtime probe-count rule.
    if 7 in available and rng.random()<.62:q=7
    else:q=int(rng.choice(available))
    af=action_feature(st,ep,q,costs[q],a0);vv=obs_for_source(ep,q,st,env,used);z=st.clone();z.add(q,vv,costs[q]);path.append((af,float(costs[q]),z.clone(),a0,cons));st=z
   # Episodic backward return. At every reached next state the learner can terminate
   # with KEEP/COMMIT/UNKNOWN or continue along the actually experienced sequence.
   continuation=-1e9
   for af,cost,z,a0,cons0 in reversed(path):
    term=max(terminal_values(z,a0,cons0))
    best=max(term,continuation)
    val=best-cost
    Xi.append(af);Yi.append(val);continuation=val
 common=dict(max_iter=140,max_leaf_nodes=23,min_samples_leaf=24,l2_regularization=1.0,learning_rate=.055)
 X=np.asarray(X);keep=HistGradientBoostingRegressor(random_state=seed,**common).fit(X,np.asarray(yk));commit=HistGradientBoostingRegressor(random_state=seed+1,**common).fit(X,np.asarray(yc));unknown=HistGradientBoostingRegressor(random_state=seed+2,**common).fit(X,np.asarray(yu))
 Xi=np.asarray(Xi);Yi=np.asarray(Yi);ipar=dict(max_iter=170,max_leaf_nodes=27,min_samples_leaf=22,l2_regularization=1.0,learning_rate=.055)
 inspect=HistGradientBoostingRegressor(random_state=seed+20,**ipar).fit(Xi,Yi)
 return keep,commit,unknown,inspect,{'decision_rows':len(X),'inspect_rows':len(Xi),'keep_mean':float(np.mean(yk)),'commit_mean':float(np.mean(yc)),'unknown_mean':0.0,'inspect_target_mean':float(np.mean(Yi)),'inspect_target_min':float(np.min(Yi)),'inspect_target_max':float(np.max(Yi)),'credit':'EPISODIC_BACKWARD_MULTI_STEP_GROUNDED_REGRET_MINUS_REAL_COST','normal_starts':normal_starts,'resource_starts':resource_starts,'source7_only_resource_starts':source7_only,'regret_replay_starts':regret_replay,'uncertain_unique_resource_starts':uncertain_unique,'uncertain_nonconvergent_resource_starts':uncertain_nonconv,'uncertain_unique_source7_only':uncertain_unique_source7_only}

def eval_seed(seed,n=220):
 old=base.train_D;base.train_D=train_D
 try:return base.eval_seed(seed,n)
 finally:base.train_D=old

def run_one(seed,n=220):
 z=eval_seed(seed,n);p=OUT/f'R32_EPISTEMIC_R31_MATCHED_V15B_SEED_{seed}.json';p.write_text(json.dumps(z,indent=2));return z
