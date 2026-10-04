from __future__ import annotations
import sys, math, json, hashlib
from pathlib import Path
import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
sys.path.insert(0,'/mnt/data/r32_epistemic')
import r32_epistemic_r31_matched_v15b_REFERENCE_ONLY as base
from r32_epistemic_r31_matched_v15b_REFERENCE_ONLY import *

OUT=Path('/mnt/data/r32_epistemic')

class State(base.State):
 def clone(self):
  z=State(self.K,self.prov,self.temporal);z.score=self.score.copy();z.group_n=self.group_n.copy();z.seen=self.seen.copy();z.hist=[(s,e.copy()) for s,e in self.hist];z.post_hist=[p.copy() for p in self.post_hist];z.cost=self.cost;z.failed_gain=self.failed_gain;return z
 def epoch_score(self):
  # Preserve the historical/global hypothesis separately. This constructs a second
  # live hypothesis for the current epoch from the best ordered split, without a
  # threshold that makes it authoritative. Q-learning decides whether to commit it.
  n=len(self.hist)
  if n<2:return self.recent_score()
  ps=[softmax(v) for _,v in self.hist]
  def tv(a,b):return .5*float(np.abs(a-b).sum())
  best=(-1e9,max(1,n-1))
  for cut in range(1,n):
   pre=np.mean(ps[:cut],axis=0);post=np.mean(ps[cut:],axis=0)
   pv=float(np.mean([tv(ps[i-1],ps[i]) for i in range(1,cut)])) if cut>1 else 0.
   qv=float(np.mean([tv(ps[i-1],ps[i]) for i in range(cut+1,n)])) if n-cut>1 else 0.
   # contrast rewards a state change; post volatility penalizes treating noise as a new epoch.
   gain=tv(pre,post)-.30*pv-.60*qv
   if gain>best[0]:best=(gain,cut)
  cut=best[1];z=np.zeros(self.K);local={}
  for s,v in self.hist[cut:]:
   g=GROUP[s];k=local.get(g,0);w=1/(1+.70*k) if self.prov else 1.;z+=w*v;local[g]=k+1
  return z if np.any(z) else self.recent_score()
 def epoch_p(self):return softmax(self.epoch_score())

def initial_state(ep,env,route):
 st=State(len(env[5]),route in ('C','D'),route=='D')
 for s,v in ep.passive:
  if ep.avail[s]:st.add(s,v,ep.cost[s])
 return st

def q_feat(st,ep,safe,a_dec,env):
 f=base.q_feat(st,ep,safe,a_dec,env);sp=st.epoch_p();gp=softmax(st.score);rp=softmax(st.recent_score())
 return np.r_[f,margin(sp),float(sp.max()),float(np.argmax(sp)==np.argmax(gp)),float(np.argmax(sp)==np.argmax(rp))]

def train_D(seed,env,safe,n=2200):
 rng=np.random.default_rng(seed);X=[];yk=[];yc=[];ye=[];yu=[];Xi=[];Yi=[]
 normal_starts=resource_starts=source7_only=uncertain_unique=uncertain_nonconv=uncertain_unique_source7_only=regret_replay=extra_nonconv_replay=0
 choices=KINDS+['genuine_ambiguity']*5+['delayed_distinguishing']*2+['entity_replacement']*2+['apparent_replacement_reverses']*2
 def action_feature(st,ep,s,cost,a0):return np.r_[q_feat(st,ep,safe,a0,env),np.eye(S)[s],cost,st.group_n[GROUP[s]]/3]
 def candidates(st):
  full=int(env[5][int(np.argmax(st.p(True)))]);epoch=int(env[5][int(np.argmax(st.epoch_p()))]);return full,epoch
 def resource_start(ep,cons,base_state,a0,force7=False):
  nonlocal resource_starts,source7_only,uncertain_unique,uncertain_nonconv,uncertain_unique_source7_only
  rs=base_state.clone();mask=ep.avail.copy();keep_prob=float(rng.beta(1.25,2.0))
  for q in range(2,7):mask[q]=bool(mask[q] and rng.random()<keep_prob)
  mask[7]=bool(ep.avail[7])
  if force7:
   for q in range(2,7):mask[q]=False
  costs=ep.cost.copy()
  for q in range(2,S):costs[q]=float(costs[q]*np.exp(rng.uniform(math.log(.60),math.log(2.40))))
  resource_starts+=1;only7=bool(mask[7] and not np.any(mask[2:7]));source7_only+=int(only7);ent=entropy(rs.p(True))
  if ent>=.55:
   if cons is None:uncertain_nonconv+=1
   else:uncertain_unique+=1;uncertain_unique_source7_only+=int(only7)
  return rs,a0,mask,costs,12
 def terminal_values(st,a0,cons):
  full,epoch=candidates(st)
  return (delayed_action_utility(a0,cons),delayed_action_utility(full,cons),delayed_action_utility(epoch,cons),0.0)
 for j in range(n):
  kind=str(rng.choice(choices));ep=make_ep(seed*100000+j*19+7,kind,env)
  if rng.random()<.68:ep.dev_dynamic_mode=int(rng.integers(0,6))
  adec,_,ap=run_A(ep,env,safe);cons=delayed_consensus(ep);starts=[]
  st=initial_state(ep,env,'D')
  for q,v in ap:st.add(q,v,ep.cost[q])
  starts.append((st,adec,ep.avail.copy(),ep.cost.copy(),10));normal_starts+=1
  rs0=initial_state(ep,env,'D');radec=int(env[5][int(np.argmax(rs0.p(True)))])
  if rng.random()<.45:starts.append(resource_start(ep,cons,rs0,radec,False))
  u=entropy(rs0.p(True))
  if rng.random()<u:
   starts.append(resource_start(ep,cons,rs0,radec,bool(rng.random()<.5)));regret_replay+=1
  # V17: delayed-outcome balancing only. If present evidence is highly uncertain
  # and later grounded windows remain non-convergent, add replay until that
  # support approaches delayed-unique support. No generator/ambiguity label is used.
  if cons is None and u>=.55:
   extra=0
   while uncertain_nonconv < int(.90*max(1,uncertain_unique)) and extra<2:
    starts.append(resource_start(ep,cons,rs0,radec,bool(rng.random()<.5)));extra_nonconv_replay+=1;extra+=1
  for st,a0,mask,costs,stages in starts:
   used=[];path=[]
   for stage in range(stages):
    f=q_feat(st,ep,safe,a0,env);full,epoch=candidates(st)
    X.append(f);yk.append(delayed_action_utility(a0,cons));yc.append(delayed_action_utility(full,cons));ye.append(delayed_action_utility(epoch,cons));yu.append(0.0)
    available=[q for q in range(2,S) if mask[q] and (not st.seen[q] or q==7)]
    if not available:break
    if 7 in available and rng.random()<.62:q=7
    else:q=int(rng.choice(available))
    af=action_feature(st,ep,q,costs[q],a0);vv=obs_for_source(ep,q,st,env,used);z=st.clone();z.add(q,vv,costs[q]);path.append((af,float(costs[q]),z.clone(),a0,cons));st=z
   continuation=-1e9
   for af,cost,z,a0,cons0 in reversed(path):
    term=max(terminal_values(z,a0,cons0));val=max(term,continuation)-cost;Xi.append(af);Yi.append(val);continuation=val
 common=dict(max_iter=140,max_leaf_nodes=23,min_samples_leaf=24,l2_regularization=1.0,learning_rate=.055);X=np.asarray(X)
 keep=HistGradientBoostingRegressor(random_state=seed,**common).fit(X,np.asarray(yk));commit=HistGradientBoostingRegressor(random_state=seed+1,**common).fit(X,np.asarray(yc));epoch=HistGradientBoostingRegressor(random_state=seed+2,**common).fit(X,np.asarray(ye));unknown=HistGradientBoostingRegressor(random_state=seed+3,**common).fit(X,np.asarray(yu))
 Xi=np.asarray(Xi);Yi=np.asarray(Yi);ipar=dict(max_iter=170,max_leaf_nodes=27,min_samples_leaf=22,l2_regularization=1.0,learning_rate=.055);inspect=HistGradientBoostingRegressor(random_state=seed+20,**ipar).fit(Xi,Yi)
 meta={'decision_rows':len(X),'inspect_rows':len(Xi),'keep_mean':float(np.mean(yk)),'commit_blend_mean':float(np.mean(yc)),'commit_epoch_mean':float(np.mean(ye)),'unknown_mean':0.0,'inspect_target_mean':float(np.mean(Yi)),'inspect_target_min':float(np.min(Yi)),'inspect_target_max':float(np.max(Yi)),'credit':'EPISODIC_BACKWARD_MULTI_STEP_REGRET_WITH_SEPARATE_CURRENT_EPOCH_COMMIT','normal_starts':normal_starts,'resource_starts':resource_starts,'source7_only_resource_starts':source7_only,'regret_replay_starts':regret_replay,'extra_nonconvergent_replay_starts':extra_nonconv_replay,'uncertain_unique_resource_starts':uncertain_unique,'uncertain_nonconvergent_resource_starts':uncertain_nonconv,'support_ratio_nonconv_to_unique':float(uncertain_nonconv/max(1,uncertain_unique)),'uncertain_unique_source7_only':uncertain_unique_source7_only}
 return keep,commit,epoch,unknown,inspect,meta

def d_values(st,models,ep,safe,a_dec,env):
 keep,commit,epoch,unknown,inspect,_=models;f=q_feat(st,ep,safe,a_dec,env);full=int(env[5][int(np.argmax(st.p(True)))]);epc=int(env[5][int(np.argmax(st.epoch_p()))])
 qk=float(keep.predict(f[None,:])[0]);qf=float(commit.predict(f[None,:])[0]);qe=float(epoch.predict(f[None,:])[0]);qu=float(unknown.predict(f[None,:])[0])
 if qe>qf:return epc,qk,qe,qu,f
 return full,qk,qf,qu,f

def inspect_value(st,models,ep,s,safe,a_dec,env):
 f=q_feat(st,ep,safe,a_dec,env);gf=np.r_[f,np.eye(S)[s],ep.cost[s],st.group_n[GROUP[s]]/3];return float(models[4].predict(gf[None,:])[0])
