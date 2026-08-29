from __future__ import annotations
import os,sys,math,json,hashlib
os.environ.setdefault('OMP_NUM_THREADS','1');os.environ.setdefault('MKL_NUM_THREADS','1');os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
sys.path.insert(0,'/mnt/data/r31_part2')
from dataclasses import dataclass
from collections import defaultdict,Counter
from pathlib import Path
import numpy as np
from sklearn.linear_model import LogisticRegression,Ridge
from sklearn.ensemble import HistGradientBoostingClassifier,HistGradientBoostingRegressor
import r31_sequential_evidence_abstention_REFERENCE_ONLY as r31
import r31_postrepair_part2b as b

OUT=Path('/mnt/data/r32_epistemic');OUT.mkdir(parents=True,exist_ok=True)
# Sources: acoustic initial, context, acoustic reinspection, sibling/social 1, sibling/social 2, physical 1, physical 2, physical decisive.
S=8
GROUP=np.array([0,1,0,2,2,3,4,5],int)
MOD=np.array([0,1,0,2,2,3,3,3],int)
BASE_COST=np.array([.02,.02,.10,.03,.03,.28,.36,.72],float)
KINDS=['clean_stable','speaker_shift','hard_noise','onset_damage','near_twin','confident_wrong_first','novel',
       'correlated_wrong_two','independent_clean_correction','genuine_ambiguity','delayed_distinguishing',
       'entity_replacement','apparent_replacement_reverses','noisy_sibling_testimony',
       'repeated_same_lineage_social','sensory_channel_loss','cost_too_high']
CORE=['speaker_shift','hard_noise','onset_damage','near_twin','confident_wrong_first','novel']
RESOLVABLE=[k for k in KINDS if k not in ('genuine_ambiguity','cost_too_high')]
MISLEADING=['confident_wrong_first','correlated_wrong_two','independent_clean_correction','noisy_sibling_testimony','repeated_same_lineage_social']


def softmax(x):
 z=x-np.max(x);e=np.exp(z);return e/(e.sum()+1e-12)
def entropy(p):return float(-(p*np.log(p+1e-12)).sum()/math.log(len(p)))
def margin(p):q=np.sort(p);return float(q[-1]-q[-2])
def logprob_fast(model,x):
 if hasattr(model,'coef_'):
  z=float(model.intercept_[0]+np.dot(model.coef_[0],x));z=max(-40.,min(40.,z));return 1/(1+math.exp(-z))
 return float(model.predict_proba(np.asarray(x).reshape(1,-1))[0,1])

def ctx_evidence(ctxclf,classes,idx,cv):return r31.context_evidence(ctxclf,classes,idx,cv)

def train_A(seed,env):
 w,rng,L,prot,ctxclf,classes,idx,sig,learned=env
 X1=[];Y1=[];X2=[];Y2=[];conds=['matched','hard_noise','near_twin','confwrong','speaker_shift','onset_damage']
 # Exact R31 delayed-regret calibration.
 for _ in range(9000):
  e=int(rng.integers(0,w.entities));unstable=rng.random()<.16;cond=str(rng.choice(conds));s,y=r31.generate_state(w,rng,e,cond,unstable)
  q=L.probs(s);cv=b.context_vec(prot,e,rng,amb=unstable);ctxv=ctx_evidence(ctxclf,classes,idx,cv);score=np.log(q+1e-8)+np.log(.2+.8*ctxv);pred1=int(classes[int(np.argmax(score))]);f1=r31.feats(score,ctxv);X1.append(f1);Y1.append(int((not unstable) and pred1==y))
  used=[];a=r31.select_action(score,learned,used);used.append(a);ty=(int(w.effect[e if rng.random()<.5 else (e^1)]) if unstable else y);obs=sig[idx[ty],a]+rng.normal(0,.65);oldtop=int(np.argmax(score));new=r31.action_update(score,obs,a,learned);gap=float(np.max(new)-np.partition(new,-2)[-2]);pred2=int(classes[int(np.argmax(new))]);f2=r31.feats(new,ctxv,oldtop,gap);X2.append(f2);Y2.append(int((not unstable) and pred2==y))
 return (LogisticRegression(max_iter=400,class_weight='balanced').fit(X1,Y1),LogisticRegression(max_iter=400,class_weight='balanced').fit(X2,Y2))

@dataclass
class Ep:
 kind:str;seed:int;e:int;twin:int;target:int;target_idx:int;twin_target:int;twin_idx:int
 passive:list;ctxv:np.ndarray;avail:np.ndarray;cost:np.ndarray;phys_outcomes:list;phys_noise:np.ndarray;future_a:list;future_b:list


def score_social(rng,K,fav,other,strength=1.55,noise=.10):
 x=rng.normal(0,noise,K);x[fav]+=strength;x[other]+=.18;return x

def future_outcomes(rng,kind,target,twin_target,n=7):
 if kind=='genuine_ambiguity':
  return [target if rng.random()<.5 else twin_target for _ in range(n)]
 return [target]*n

def delayed_consensus(ep):
 def one(z):
  c=Counter(z);v,n=c.most_common(1)[0];return v,n/len(z)
 a,fa=one(ep.future_a);c,fc=one(ep.future_b)
 return (a if a==c and min(fa,fc)>=.80 else None)

def make_ep(seed,kind,env):
 w,_,L,prot,ctxclf,classes,idx,sig,learned=env;rng=np.random.default_rng(seed);K=len(classes);e=int(rng.integers(0,w.entities));tw=e^1;ye=int(w.effect[e]);yt=int(w.effect[tw]);target=ye;acond='matched';ctx_entity=e;ctx_amb=False;reinspect='hard_noise';reinspect_entity=e
 if kind in ['speaker_shift','hard_noise','onset_damage','near_twin','novel']:acond=kind
 if kind in ['confident_wrong_first','correlated_wrong_two','independent_clean_correction']:acond='confwrong'
 if kind=='genuine_ambiguity':ctx_amb=True
 if kind=='delayed_distinguishing':ctx_amb=True
 if kind=='entity_replacement':target=yt;reinspect_entity=tw;reinspect='hard_noise'
 if kind=='apparent_replacement_reverses':reinspect_entity=tw;reinspect='hard_noise'
 if kind=='sensory_channel_loss':acond='matched'
 if kind=='cost_too_high':ctx_amb=True
 # initial acoustic
 if kind in ('genuine_ambiguity','delayed_distinguishing','cost_too_high'):
  s,_=w.ambiguous(e,rng)
 else:s,_=w.episode(e,rng,acond)
 q=L.probs(s);aq=np.log(q+1e-8)
 cv=b.context_vec(prot,ctx_entity,rng,amb=ctx_amb);ctxv=ctx_evidence(ctxclf,classes,idx,cv);cq=np.log(.2+.8*ctxv)
 # reinspection, same acoustic lineage. In correlated wrong it is also wrong; in independent correction it is clean.
 if kind=='correlated_wrong_two':s2,_=w.episode(e,rng,'confwrong')
 elif kind=='independent_clean_correction':s2,_=w.episode(e,rng,'matched')
 elif kind in ('genuine_ambiguity','cost_too_high'):s2,_=w.ambiguous(e,rng)
 elif kind=='delayed_distinguishing':s2,_=w.ambiguous(e,rng)
 else:s2,_=w.episode(reinspect_entity,rng,reinspect)
 rscore=np.log(L.probs(s2)+1e-8)
 ti=idx[target];twi=idx[yt if target==ye else ye]
 passive=[(0,aq),(1,cq)]
 # temporal second acoustic is passive only when the condition explicitly contains a second observation/state transition.
 if kind in ('correlated_wrong_two','independent_clean_correction','entity_replacement','apparent_replacement_reverses'):passive.append((2,rscore))
 # social claims. Two claims share lineage group 2.
 if kind=='noisy_sibling_testimony':
  passive.append((3,score_social(rng,K,ti,twi,1.25,.22))); fav=ti if rng.random()<.58 else twi;other=twi if fav==ti else ti;passive.append((4,score_social(rng,K,fav,other,1.20,.25)))
 elif kind=='repeated_same_lineage_social':
  passive.append((3,score_social(rng,K,twi,ti,2.10,.09)));passive.append((4,score_social(rng,K,twi,ti,2.00,.09)))
 elif kind=='apparent_replacement_reverses':
  passive.append((3,score_social(rng,K,twi,ti,1.65,.10)))
 avail=np.ones(S,bool);cost=BASE_COST.copy()
 if kind=='sensory_channel_loss':avail[0]=avail[2]=False;passive=[z for z in passive if z[0] not in (0,2)]
 # source 2 remains actively available when not already observed.
 # Physical outcomes are grounded consequences, not labels supplied to policy.
 phys=[target,target,target]
 if kind=='genuine_ambiguity':phys=[ye if rng.random()<.5 else yt for _ in range(3)]
 elif kind=='apparent_replacement_reverses':phys=[ye,ye,ye]
 elif kind=='entity_replacement':phys=[yt,yt,yt]
 # delayed distinguishing: only the last physical source has sharp information; first two are masked in obs generator.
 if kind=='cost_too_high':cost[7]=2.40
 elif kind=='delayed_distinguishing':cost[7]=.58
 noise=rng.normal(0,1,(3,learned.shape[1]))
 fa=future_outcomes(rng,kind,target,yt if target==ye else ye);fb=future_outcomes(rng,kind,target,yt if target==ye else ye)
 return Ep(kind,seed,e,tw,target,idx[target],(yt if target==ye else ye),twi,passive,ctxv,avail,cost,phys,noise,fa,fb)

class State:
 def __init__(self,K,prov=False,temporal=False):
  self.K=K;self.prov=prov;self.temporal=temporal;self.score=np.zeros(K);self.group_n=np.zeros(6,int);self.seen=np.zeros(S,bool);self.hist=[];self.post_hist=[];self.cost=0.;self.failed_gain=0
 def clone(self):
  z=State(self.K,self.prov,self.temporal);z.score=self.score.copy();z.group_n=self.group_n.copy();z.seen=self.seen.copy();z.hist=[(s,e.copy()) for s,e in self.hist];z.post_hist=[p.copy() for p in self.post_hist];z.cost=self.cost;z.failed_gain=self.failed_gain;return z
 def add(self,s,v,cost):
  g=GROUP[s];w=1/(1+.9*self.group_n[g]) if self.prov else 1.;self.score+=w*v;self.group_n[g]+=1;self.seen[s]=True;self.hist.append((s,v.copy()));self.cost+=cost;self.post_hist.append(self.p(self.temporal).copy())
 def recent_score(self):
  if not self.hist:return self.score.copy()
  z=np.zeros(self.K)
  for s,v in self.hist[-3:]:
   # recency window still discounts duplicate lineage locally.
   n=sum(1 for q,_ in self.hist[-3:] if GROUP[q]==GROUP[s]);z+=v/(1+.55*max(0,n-1)) if self.prov else v
  return z
 def p(self,full=False):
  if not full:return softmax(self.score)
  # Recent evidence is a change hypothesis, not unconditional replacement authority.
  rp=softmax(self.recent_score());gp=softmax(self.score);return .48*gp+.52*rp
 def feats(self,full=False):
  p=self.p(full);gp=softmax(self.score);groups=np.count_nonzero(self.group_n);dep=self.group_n.max()/max(1,self.group_n.sum());f=[margin(p),float(p.max()),1-entropy(p),entropy(p),len(self.hist)/S,groups/6,1-dep,self.cost/3.5,self.failed_gain/3]
  f+=list(self.seen.astype(float));f+=list(np.minimum(self.group_n,3)/3)
  if full:
   rp=softmax(self.recent_score());glob=int(np.argmax(gp));recent=int(np.argmax(rp));tops=[]
   for m in range(4):
    vv=[v for src,v in self.hist if MOD[src]==m]
    if vv:tops.append(int(np.argmax(np.sum(vv,axis=0))))
   agree=(sum(x==int(np.argmax(p)) for x in tops)/len(tops)) if tops else 0.
   # Persistent posterior trajectory: generic instability, not a condition detector.
   ph=self.post_hist
   if len(ph)>=2:
    pt=[int(np.argmax(x)) for x in ph];sw=sum(a!=b for a,b in zip(pt[:-1],pt[1:]))/max(1,len(pt)-1)
    tv=[.5*float(np.abs(a-b).sum()) for a,b in zip(ph[:-1],ph[1:])];ee=[entropy(x) for x in ph];mm=[margin(x) for x in ph]
    ret=sum(pt[i]==pt[i-2] and pt[i]!=pt[i-1] for i in range(2,len(pt)))/max(1,len(pt)-2)
    traj=[sw,float(np.mean(tv)),float(np.max(tv)),float(np.mean(ee)),float(np.std(ee)),float(ee[-1]-ee[0]),float(np.mean(mm)),float(np.std(mm)),float(mm[-1]-mm[0]),ret]
   else:traj=[0.]*10
   # Within-modality and within-lineage disagreement. Repeated physical or social
   # evidence must not vanish merely because vectors cancel in the accumulated score.
   def js(a,b):
    aa=softmax(a);bb=softmax(b);m=.5*(aa+bb);return .5*float(np.sum(aa*np.log((aa+1e-12)/(m+1e-12)))+np.sum(bb*np.log((bb+1e-12)/(m+1e-12))))
   modal_js=[];modal_div=[]
   for m in range(4):
    vv=[v for src,v in self.hist if MOD[src]==m]
    if len(vv)>=2:
     modal_div.append(len(set(int(np.argmax(v)) for v in vv))/len(vv))
     for i in range(len(vv)):
      for j in range(i+1,len(vv)):modal_js.append(js(vv[i],vv[j]))
   group_js=[]
   for g in range(6):
    vv=[v for src,v in self.hist if GROUP[src]==g]
    if len(vv)>=2:
     for i in range(len(vv)):
      for j in range(i+1,len(vv)):group_js.append(js(vv[i],vv[j]))
   disagree=[float(np.mean(modal_js)) if modal_js else 0.,float(np.max(modal_js)) if modal_js else 0.,float(np.mean(modal_div)) if modal_div else 0.,float(np.mean(group_js)) if group_js else 0.,float(np.max(group_js)) if group_js else 0.]
   f += [margin(rp),float(rp.max()),float(glob==recent),agree,float(len(set(tops))/max(1,len(tops)))]+traj+disagree
  return np.asarray(f,float)
 def candfeat(self,c,full=False):
  p=self.p(full);gp=softmax(self.score);rp=softmax(self.recent_score());return np.r_[self.feats(full),p[c],gp[c],rp[c],float(c==np.argmax(gp)),float(c==np.argmax(rp))]

def physical_vec(ep,source,st,env,used_actions):
 *_,classes,idx,sig,learned=env;slot=source-5
 # Source 7 is a reusable physical consequence experiment. Repeated trials are
 # new observations with the same apparatus lineage/provenance and full cost.
 # No fixed trial count is part of learner policy.
 trial=int(st.group_n[GROUP[source]]) if source==7 else 0
 if source==7:
  rr=np.random.default_rng(ep.seed*1009+trial*9176+71)
  outcome=(ep.target if ep.kind!='genuine_ambiguity' or rr.random()<.5 else ep.twin_target)
 else:outcome=ep.phys_outcomes[slot]
 # Delayed/cost cases deliberately make early physical observations observationally equivalent.
 if ep.kind in ('delayed_distinguishing','cost_too_high') and source in (5,6):
  z=np.zeros(len(classes));z[ep.target_idx]+=.18;z[ep.twin_idx]+=.18;return z,-1
 score=st.score if len(st.hist) else np.zeros(len(classes));a=r31.select_action(score,learned,used_actions);used_actions.append(a)
 if source==7:
  rr=np.random.default_rng(ep.seed*2029+trial*12347+a*31+97);eps=float(rr.normal(0,.80 if ep.kind=='genuine_ambiguity' else .65))
 else:eps=float(ep.phys_noise[slot,a]*(.80 if ep.kind=='genuine_ambiguity' else .65))
 obs=sig[idx[outcome],a]+eps;v=np.array([-((obs-learned[ci,a])**2)/(2*(.85 if ep.kind!='genuine_ambiguity' else .95)**2) for ci in range(len(classes))]);return v,a

def obs_for_source(ep,s,st,env,used_actions):
 if s in (5,6,7):return physical_vec(ep,s,st,env,used_actions)[0]
 if s==2:
  for q,v in ep.passive:
   if q==2:return v.copy()
  # active clean acoustic reinspection for ordinary cases
  w,_,L,*_=env;r=np.random.default_rng(ep.e*100003+ep.twin*97+13);ss,_=w.episode(ep.e,r,'hard_noise');return np.log(L.probs(ss)+1e-8)
 if s in (3,4):
  for q,v in ep.passive:
   if q==s:return v.copy()
  return np.zeros(st.K)
 for q,v in ep.passive:
  if q==s:return v.copy()
 return np.zeros(st.K)

def initial_state(ep,env,route):
 K=len(env[5]);st=State(K,route in ('C','D'),route=='D')
 for s,v in ep.passive:
  if ep.avail[s]:st.add(s,v,ep.cost[s])
 return st

def legacy_safe(st,ep,safe):
 safe1,_=safe
 return float(safe1.predict_proba([r31.feats(st.score,ep.ctxv)])[0,1])

def meta_feat(st,ep,safe,full=True):
 p=st.p(full);gp=softmax(st.score);rp=softmax(st.recent_score());c=int(np.argmax(p));legacy=legacy_safe(st,ep,safe)
 return np.r_[st.feats(full),legacy,float(c==np.argmax(gp)),float(c==np.argmax(rp)),p[c]]

def delayed_action_utility(decision,cons):
 # Generic regret economics. UNKNOWN is the neutral zero-regret fallback; it is
 # never rewarded from an ambiguity label and never penalized merely because
 # later experience eventually becomes resolvable. Commit utility is learned
 # only from delayed grounded outcomes: correct +1, wrong -2, and committing
 # when independent delayed outcomes fail to establish a unique state is -1.2.
 # Observation actions pay their actual costs through the Bellman backup.
 if decision==-1:return 0.0
 if cons is None:return -1.2
 return 1.0 if int(decision)==int(cons) else -2.0

def q_feat(st,ep,safe,a_dec,env):
 f=meta_feat(st,ep,safe,True);full_label=int(env[5][int(np.argmax(st.p(True)))])
 return np.r_[f,float(a_dec==-1),float(a_dec!=-1 and full_label==a_dec)]

def train_D(seed,env,safe,n=2200):
 rng=np.random.default_rng(seed);X=[];yk=[];yc=[];yu=[];trans=[]
 # Curriculum generation may contain difficult/underdetermined experiences, but
 # those names never enter learner features or targets. Terminal action targets
 # use delayed grounded outcomes only. Inspection credit is learned from the
 # NEXT EVIDENCE STATE, not from oracle-best delayed utility after probing.
 choices=KINDS+['genuine_ambiguity']*5+['delayed_distinguishing']*2+['entity_replacement']*2+['apparent_replacement_reverses']*2
 for j in range(n):
  kind=str(rng.choice(choices));ep=make_ep(seed*100000+j*19+7,kind,env);adec,_,ap=run_A(ep,env,safe);st=initial_state(ep,env,'D')
  for q,v in ap:st.add(q,v,ep.cost[q])
  cons=delayed_consensus(ep);used=[]
  # Exploration depth is a training-data coverage bound only. Runtime has no
  # fixed probe count and must stop because learned action value falls below a
  # terminal alternative once repeated evidence stops improving the state.
  for stage in range(10):
   f=q_feat(st,ep,safe,adec,env);cand=int(env[5][int(np.argmax(st.p(True)))])
   X.append(f);yk.append(delayed_action_utility(adec,cons));yc.append(delayed_action_utility(cand,cons));yu.append(delayed_action_utility(-1,cons))
   available=[q for q in range(2,S) if ep.avail[q] and (not st.seen[q] or q==7)]
   if not available:break
   # Save actual next-state transitions for fitted action-value credit. The
   # delayed outcome supervises terminal Qs, but INSPECT never receives oracle
   # access to which terminal action will later prove best.
   for q in available:
    tmp=[];vv=obs_for_source(ep,q,st,env,tmp);z=st.clone();z.add(q,vv,ep.cost[q]);nf=q_feat(z,ep,safe,adec,env)
    gf=np.r_[f,np.eye(S)[q],ep.cost[q],st.group_n[GROUP[q]]/3]
    trans.append((gf,nf,float(ep.cost[q])))
   q=int(rng.choice(available));vv=obs_for_source(ep,q,st,env,used);st.add(q,vv,ep.cost[q])
 common=dict(max_iter=135,max_leaf_nodes=21,min_samples_leaf=22,l2_regularization=1.0,learning_rate=.055)
 keep=HistGradientBoostingRegressor(random_state=seed,**common).fit(np.asarray(X),np.asarray(yk))
 commit=HistGradientBoostingRegressor(random_state=seed+1,**common).fit(np.asarray(X),np.asarray(yc))
 unknown=HistGradientBoostingRegressor(random_state=seed+2,**common).fit(np.asarray(X),np.asarray(yu))
 # Bellman-style one-step backup from the observed next evidence state. If a
 # reusable same-lineage trial does not improve predicted terminal utility, its
 # value is terminal utility minus its full observation cost and it loses to
 # stopping. This directly repairs V8's runaway oracle-credit pathology.
 Xi=np.asarray([q[0] for q in trans]);NXT=np.asarray([q[1] for q in trans]);CC=np.asarray([q[2] for q in trans],float)
 qk=keep.predict(NXT);qc=commit.predict(NXT);qu=unknown.predict(NXT);yi=np.maximum.reduce([qk,qc,qu])-CC
 inspect=HistGradientBoostingRegressor(random_state=seed+3,max_iter=145,max_leaf_nodes=23,min_samples_leaf=24,l2_regularization=1.2,learning_rate=.055).fit(Xi,yi)
 return keep,commit,unknown,inspect,{'decision_rows':len(X),'inspect_rows':len(Xi),'keep_mean':float(np.mean(yk)),'commit_mean':float(np.mean(yc)),'unknown_mean':float(np.mean(yu)),'inspect_target_mean':float(np.mean(yi)),'inspect_target_min':float(np.min(yi)),'inspect_target_max':float(np.max(yi)),'credit':'NEXT_STATE_BELLMAN_TERMINAL_MINUS_COST'}

def d_values(st,models,ep,safe,a_dec,env):
 keep,commit,unknown,inspect,_=models;f=q_feat(st,ep,safe,a_dec,env);cand=int(env[5][int(np.argmax(st.p(True)))])
 qk=float(keep.predict(f.reshape(1,-1))[0]);qc=float(commit.predict(f.reshape(1,-1))[0]);qu=float(unknown.predict(f.reshape(1,-1))[0])
 return cand,qk,qc,qu,f

def inspect_value(st,models,ep,s,safe,a_dec,env):
 f=q_feat(st,ep,safe,a_dec,env);gf=np.r_[f,np.eye(S)[s],ep.cost[s],st.group_n[GROUP[s]]/3]
 return float(models[3].predict(gf.reshape(1,-1))[0])

def run_A(ep,env,safe):
 w,rng,L,prot,ctxclf,classes,idx,sig,learned=env;safe1,safe2=safe
 st=State(len(classes),False,False)
 # A receives the same passive observations but has no provenance/temporal representation.
 for s,v in ep.passive:
  if ep.avail[s]:st.add(s,v,ep.cost[s])
 score=st.score.copy();used=[];probes=[];tops=[];outs=[]
 # R31 explicit ambiguous/correlated tests keep their exact two-grounded-probe behavior.
 if ep.kind in ('genuine_ambiguity','correlated_wrong_two'):
  for src in (5,6):
   v,a=physical_vec(ep,src,st,env,used);score+=v;st.add(src,v,ep.cost[src]);probes.append((src,v));tops.append(int(np.argmax(score)));outs.append(ep.phys_outcomes[src-5])
  p=softmax(score);mg=margin(p);pred=int(classes[int(np.argmax(p))])
  if ep.kind=='genuine_ambiguity':dec=-1 if (len(set(outs))>1 or len(set(tops))>1 or mg<.4) else pred
  else:dec=-1 if mg<.28 else pred
  return dec,st,probes
 f1=r31.feats(score,ep.ctxv);ps1=float(safe1.predict_proba([f1])[0,1]);pred=int(classes[int(np.argmax(score))])
 if ps1<.83:
  src=5;v,a=physical_vec(ep,src,st,env,used);old=int(np.argmax(score));score+=v;st.add(src,v,ep.cost[src]);probes.append((src,v));f2=r31.feats(score,ep.ctxv,old,float(np.max(score)-np.partition(score,-2)[-2]));ps2=float(safe2.predict_proba([f2])[0,1]);pred=int(classes[int(np.argmax(score))])
  if ps2<.76:
   src=6;v,a=physical_vec(ep,src,st,env,used);score+=v;st.add(src,v,ep.cost[src]);probes.append((src,v));p=softmax(score);dec=-1 if margin(p)<.32 else int(classes[int(np.argmax(p))])
  else:dec=pred
 else:dec=pred
 return dec,st,probes

def run_BC(ep,env,route,a_dec,a_probes):
 st=initial_state(ep,env,route)
 for s,v in a_probes:st.add(s,v,ep.cost[s])
 if a_dec==-1:return -1,st
 return int(env[5][int(np.argmax(st.p(False)))]),st

def run_D(ep,env,models,safe,a_probes,a_dec):
 # Residual epistemic control. Evidence acquired by qualified R31 is never discarded,
 # and KEEP_R31 remains one learned action alongside current commit, inspect, UNKNOWN.
 st=initial_state(ep,env,'D');used=[];diagnostic_steps=0
 for s,v in a_probes:st.add(s,v,ep.cost[s])
 while True:
  diagnostic_steps+=1
  if diagnostic_steps>40:raise RuntimeError('evaluator safety: runaway observation loop; learner failed to stop economically')
  cand,qk,qc,qu,f=d_values(st,models,ep,safe,a_dec,env);best_name='keep';best_val=qk;best_src=-1
  if qc>best_val:best_name='commit';best_val=qc
  if qu>best_val:best_name='unknown';best_val=qu
  for s in range(2,S):
   if not ep.avail[s] or (st.seen[s] and s!=7):continue
   qi=inspect_value(st,models,ep,s,safe,a_dec,env)
   if qi>best_val:best_name='inspect';best_val=qi;best_src=s
  if best_name=='inspect':
   v=obs_for_source(ep,best_src,st,env,used);st.add(best_src,v,ep.cost[best_src]);continue
  if best_name=='keep':return a_dec,st
  if best_name=='commit':return cand,st
  return -1,st

def eval_seed(seed,n=220):
 env=r31.setup(seed);safe=train_A(seed,env);dmod=train_D(seed*10+68,env,safe,2200);rng=np.random.default_rng(seed*1000+33);out={r:{} for r in 'ABCD'}
 for ki,kind in enumerate(KINDS):
  rows=[]
  for j in range(n):
   ep=make_ep(seed*10000000+ki*100000+j,kind,env);a,ast,ap=run_A(ep,env,safe);bdec,bst=run_BC(ep,env,'B',a,ap);cdec,cst=run_BC(ep,env,'C',a,ap);ddec,dst=run_D(ep,env,dmod,safe,ap,a);rows.append((ep,(a,ast),(bdec,bst),(cdec,cst),(ddec,dst)))
  for ri,route in enumerate('ABCD',start=1):
   d=defaultdict(float);ents=[];un=[];ind=[]
   for z in rows:
    ep=z[0];dec,st=z[ri];unique=ep.kind!='genuine_ambiguity'
    if ep.kind=='genuine_ambiguity':d['ambiguity_abstain']+=dec==-1;d['wrong_commit']+=dec!=-1
    elif ep.kind=='cost_too_high':d['rational_cost_abstain']+=dec==-1;d['correct']+=dec==ep.target;d['wrong_commit']+=dec not in(-1,ep.target);d['abstain']+=dec==-1
    else:d['correct']+=dec==ep.target;d['wrong_commit']+=dec not in(-1,ep.target);d['abstain']+=dec==-1
    if ep.kind in MISLEADING:d['recovery']+=dec==ep.target
    if ep.kind=='entity_replacement':
     d['switch_correct']+=dec==ep.target;preds=[int(env[5][int(np.argmax(p))]) for p in st.post_hist];hit=next((i for i,x in enumerate(preds) if x==ep.target),len(preds));d['switch_delay']+=hit
    if ep.kind=='apparent_replacement_reverses':d['false_switch']+=dec==ep.twin_target
    d['cost']+=st.cost;d['sources']+=len(st.hist);d['reusable_trials']+=st.group_n[GROUP[7]];ind.append(np.count_nonzero(st.group_n));
    if st.hist:
     ents.extend(entropy(p) for p in st.post_hist)
     un.append(1-st.p(route=='D').max())
   dd={k:v/n for k,v in d.items()};dd['independent_sources']=float(np.mean(ind));dd['entropy_over_time']=float(np.mean(ents));dd['final_unresolved_mass']=float(np.mean(un));out[route][kind]=dd
 for r in 'ABCD':
  rr=out[r];out[r]['summary']={'core_hard_correct':float(np.mean([rr[k].get('correct',0) for k in CORE])), 'expanded_resolvable_correct':float(np.mean([rr[k].get('correct',0) for k in RESOLVABLE])), 'genuine_ambiguity_abstention':rr['genuine_ambiguity'].get('ambiguity_abstain',0), 'wrong_commit':float(np.mean([rr[k].get('wrong_commit',0) for k in KINDS])), 'unnecessary_abstention':float(np.mean([rr[k].get('abstain',0) for k in RESOLVABLE])), 'mean_cost':float(np.mean([rr[k].get('cost',0) for k in KINDS])), 'independent_sources':float(np.mean([rr[k]['independent_sources'] for k in KINDS])), 'misleading_recovery':float(np.mean([rr[k].get('recovery',0) for k in MISLEADING])), 'switch_correct':rr['entity_replacement'].get('switch_correct',0), 'switch_delay':rr['entity_replacement'].get('switch_delay',0), 'false_switch':rr['apparent_replacement_reverses'].get('false_switch',0), 'entropy_over_time':float(np.mean([rr[k]['entropy_over_time'] for k in KINDS])), 'final_unresolved_mass':float(np.mean([rr[k]['final_unresolved_mass'] for k in KINDS])), 'cost_rational_abstain':rr['cost_too_high'].get('rational_cost_abstain',0), 'reusable_trials':float(np.mean([rr[k].get('reusable_trials',0) for k in KINDS]))}
 return {'seed':seed,'training':{'D':dmod[4]},'routes':out}

def aggregate(rows):
 a={}
 for r in 'ABCD':
  a[r]={k:float(np.mean([x['routes'][r]['summary'][k] for x in rows])) for k in rows[0]['routes'][r]['summary']};a[r]['conditions']={}
  for kind in KINDS:
   mets=set().union(*(x['routes'][r][kind].keys() for x in rows));a[r]['conditions'][kind]={m:float(np.mean([x['routes'][r][kind].get(m,0) for x in rows])) for m in mets}
 return a

def run_one(seed,n=220):
 z=eval_seed(seed,n);p=OUT/f'R32_EPISTEMIC_R31_MATCHED_V10_SEED_{seed}.json';p.write_text(json.dumps(z,indent=2));return z

def main():
 seeds=[9710,9711,9712,9713,9714,9715];rows=[]
 for s in seeds:
  z=run_one(s);rows.append(z);print('DONE',s,json.dumps({r:z['routes'][r]['summary'] for r in 'ABCD'}),flush=True)
 agg=aggregate(rows);out={'experiment':'R32 epistemic qualification V10 neutral-abstention Bellman-credit reusable consequence-probe residual action values anchored to actual R31 evidence machinery','seeds':seeds,'routes':{'A':'actual R31 learned sequential stopping logic','B':'persistent hypothesis population on exactly A-acquired evidence with unchanged R31 stop/UNKNOWN decision','C':'B + provenance dependence, unchanged R31 stop/UNKNOWN decision','D':'residual action-value controller: KEEP_R31 / COMMIT_CURRENT / INSPECT(source) / UNKNOWN learned from delayed grounded regret; provenance + temporal/change + cross-modal state retained'},'aggregate':agg,'rows':rows,'r31_anchor':{'aggregate_hard_correct':.9697800925925926,'ambiguity_abstain':.5717361111111111,'exact_replay_seed_9700_delta':0.0},'training_boundary':'REFERENCE_ONLY. B/C/D policy features never contain condition, ambiguity, replacement, corruption, or evaluator labels. D Q targets for KEEP_R31, COMMIT_CURRENT, INSPECT(source), and UNKNOWN derive only from two delayed grounded-consequence windows, delayed regret, and experienced observation cost. Condition names are evaluator/world-generation only. No graph cognition, transformer, tokenizer/BPE, next-token objective, supplied VAD/phoneme/word/chunk boundary.','claim_boundary':'Cannot promote canonical TNN without native Zag reproduction.'};p=OUT/'R32_EPISTEMIC_R31_MATCHED_V10_REFERENCE_ONLY.json';p.write_text(json.dumps(out,indent=2));print(json.dumps(agg,indent=2));print('SHA256',hashlib.sha256(p.read_bytes()).hexdigest())
if __name__=='__main__':main()
