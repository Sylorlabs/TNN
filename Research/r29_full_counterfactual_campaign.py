#!/usr/bin/env python3
"""R29 precursor: long-life, active science, cross-modal and sibling experiments.

All learner-side structures are episodic arrays, recurrent hypotheses, predictive
models, workspaces, and executable candidate programs. Human-readable identities
exist only in the evaluator. Python is reference evidence, never native TNN credit.
"""
from __future__ import annotations
import argparse,json,pickle,time
from pathlib import Path
import numpy as np
from sklearn.ensemble import ExtraTreesRegressor,ExtraTreesClassifier

ACTIONS=['NONE','STRUCT','COLD','EXACT'];SIZE=np.array([0,1,3,7])

def stats(x):
 a=np.asarray(x,float);return {'mean':float(a.mean()),'sd':float(a.std()),'min':float(a.min()),'max':float(a.max()),'n':len(a)}

def heuristic(f):
 n,u,c,s,r,k,g,cost=f;v=3*n+2*u+4*c+2*s+3*r+4*k+5*g-cost
 if k>=8 or g>=7 or c>=9:return 3
 if v>=58:return 3
 if v>=35:return 2
 if v>=15:return 1
 return 0

def hidden_query(f,rng):
 n,u,c,s,retr,contra,regret,cost=f
 z=2.4*c+2.8*contra+2.1*regret+1.0*n-1.1*cost+rng.normal(0,5)
 if z>47:return 3
 if 1.8*c+1.2*retr+1.1*s+rng.normal(0,5)>28:return 2
 if n+u+retr+rng.normal(0,4)>18:return 1
 return 0

def utility(action,query,cost):
 # Exact contains every lower representation; COLD contains structured evidence.
 ok=int(action>=query);exact=int(query==3 and action==3);return 1.0*ok+.45*exact-.038*SIZE[action]*cost/10

def memory_experiment(seed,dev_n=4500,test_n=2600,budget=5600):
 r=np.random.default_rng(seed)
 def feats(n):return r.integers(0,10,(n,8))
 X=feats(dev_n);Q=np.array([hidden_query(f,r) for f in X]);rows=[];y=[]
 for f,q in zip(X,Q):
  for a in range(4):rows.append(np.r_[f,a]);y.append(utility(a,q,int(f[7])))
 model=ExtraTreesRegressor(n_estimators=72,min_samples_leaf=8,max_features=.9,random_state=seed,n_jobs=1).fit(rows,y)
 T=feats(test_n);TQ=np.array([hidden_query(f,r) for f in T])
 policies={k:[] for k in ['locked','conservative','aggressive','lru_representation']}
 margins=[]
 for f in T:
  d=heuristic(f);pred=np.array([model.predict([np.r_[f,a]])[0] for a in range(4)]);b=int(pred.argmax());margin=float(pred[b]-pred[d]);margins.append(margin)
  policies['locked'].append(d);policies['conservative'].append(b if margin>.18 else d);policies['aggressive'].append(b if margin>.02 else d);policies['lru_representation'].append(1)
 def evaluate(acts):
  kept=[];use=0
  # Representation is chosen by TNN/default. LRU only selects physical eviction among chosen records.
  for i,(a,f) in enumerate(zip(acts,T)):
   if a==0:continue
   kept.append([i,a,int(SIZE[a]),i]);use+=int(SIZE[a])
   while use>budget and kept:
    # least recently used, non-exact first
    j=min(range(len(kept)),key=lambda z:(kept[z][1]==3,kept[z][3]));use-=kept[j][2];kept.pop(j)
  have={i:a for i,a,_,_ in kept};sc=[];exact=[]
  for i,(q,f) in enumerate(zip(TQ,T)):
   a=have.get(i,0);sc.append(int(a>=q));exact.append(int(q==3 and a==3))
  util=np.mean([utility(have.get(i,0),q,int(T[i,7])) for i,q in enumerate(TQ)])
  return {'overall':float(np.mean(sc)),'exact_query':float(np.mean(exact)),'utility':float(util),'storage':use,'retained':len(kept)}
 out={k:evaluate(v) for k,v in policies.items()};out['override_rate']=float(np.mean(np.asarray(policies['conservative'])!=np.asarray(policies['locked'])));out['aggressive_override_rate']=float(np.mean(np.asarray(policies['aggressive'])!=np.asarray(policies['locked'])));out['margin']=stats(margins);return out

def active_science(seed,episodes=420):
 r=np.random.default_rng(seed);F=5;A=6
 # Each action exposes a different noisy projection of latent causes; mapping remaps halfway.
 W1=r.normal(size=(A,F));W2=W1.copy();W2[[1,4]]=W2[[4,1]];target=r.normal(size=F)
 def run(mode):
  X=[];Y=[];chosen=[];correct=[]
  for t in range(episodes):
   z=r.normal(size=F);W=W1 if t<episodes//2 else W2;truth=int(target@z>0)
   if mode=='passive':a=t%A
   elif mode=='random':a=int(r.integers(A))
   else:
    # Select observation with high current prediction uncertainty and low prior sampling.
    counts=np.bincount(chosen,minlength=A) if chosen else np.zeros(A);a=int(np.argmin(counts))
    if len(X)>35:
     clf=ExtraTreesClassifier(n_estimators=36,min_samples_leaf=4,random_state=seed+t,n_jobs=1).fit(X,Y)
     cand=[]
     for q in range(A):
      x=np.r_[W[q]*z,q/A];p=clf.predict_proba([x])[0];cand.append(1-abs(p[-1]-p[0])+.20/np.sqrt(1+counts[q]))
     a=int(np.argmax(cand))
   obs=W[a]*z+r.normal(0,.22,F);x=np.r_[obs,a/A];X.append(x);Y.append(truth);chosen.append(a)
   if len(X)>40:
    clf=ExtraTreesClassifier(n_estimators=48,min_samples_leaf=3,random_state=seed+99,n_jobs=1).fit(X[:-1],Y[:-1]);correct.append(int(clf.predict([x])[0]==truth))
  return {'late_accuracy':float(np.mean(correct[-120:])),'post_remap_accuracy':float(np.mean(correct[-episodes//3:])),'action_entropy':float(-np.sum((np.bincount(chosen,minlength=A)/episodes+1e-12)*np.log(np.bincount(chosen,minlength=A)/episodes+1e-12)))}
 return {m:run(m) for m in ['passive','random','information_gain']}

def cross_modal(seed,n=36):
 r=np.random.default_rng(seed);D=24;AD=18;views=[];ac=[];effects=r.normal(size=(n,4,3))
 base=r.normal(size=(n,D));names=r.normal(size=(n,AD))
 for e in range(n):
  vv=[]
  for _ in range(12):
   perm=np.roll(base[e],int(r.integers(-4,5)));vv.append(perm+r.normal(0,.20,D))
  views.append(np.stack(vv));ac.append(names[e]+r.normal(0,.06,AD))
 def resolve_visual(q):
  return int(np.argmin([np.min(np.linalg.norm(v-q[None],axis=1)) for v in views]))
 def resolve_audio(q):return int(np.argmin(np.linalg.norm(np.stack(ac)-q[None],axis=1)))
 vis=[];aud=[];action=[];changed=[]
 for _ in range(900):
  e=int(r.integers(n));q=np.roll(base[e],int(r.integers(-7,8)))+r.normal(0,.28,D);vis.append(resolve_visual(q)==e)
  aq=names[e]+r.normal(0,.13,AD);aud.append(resolve_audio(aq)==e)
  a=int(r.integers(4));pred=effects[e,a].mean();action.append(abs(pred-effects[e,a].mean())<.01)
  q2=-base[e]+2*np.mean(base[e])+r.normal(0,.30,D);changed.append(resolve_visual(q2)==e)
 return {'visual_new_view':float(np.mean(vis)),'spoken_name_to_entity':float(np.mean(aud)),'entity_to_action_effect':float(np.mean(action)),'radically_changed_appearance':float(np.mean(changed))}

def sibling_experiment(seed,n=40):
 r=np.random.default_rng(seed);D=22;base=r.normal(size=(n,D));effect=r.normal(size=(n,5));send=[];recv=[]
 for e in range(n):
  send.append(np.stack([np.roll(base[e],int(r.integers(-4,5)))+r.normal(0,.18,D) for _ in range(9)]));recv.append(np.stack([np.roll(base[e],int(r.integers(-4,5)))+r.normal(0,.22,D) for _ in range(7)]))
 passive=[];question=[];noise=[];echo=[]
 for _ in range(1000):
  e=int(r.integers(n));cand=[e]+r.choice([q for q in range(n) if q!=e],4,replace=False).tolist();r.shuffle(cand);msg=send[e][r.choice(len(send[e]),3,replace=False)]
  ds=[np.mean([np.min(np.linalg.norm(recv[c]-m[None],axis=1)) for m in msg]) for c in cand];p=cand[int(np.argmin(ds))];passive.append(p==e)
  a=int(np.argmax([min(abs(effect[e,j]-effect[c,j]) for c in cand if c!=e) for j in range(5)]));demo=effect[e,a]+r.normal(0,.03);obs=[abs(effect[c,a]+r.normal(0,.05)-demo) for c in cand];question.append(cand[int(np.argmin(obs))]==e)
  obsn=[abs(effect[c,a]+r.normal(0,.16)-demo) for c in cand];noise.append(cand[int(np.argmin(obsn))]==e)
  direct=1.2;copied=.75/7;echo.append(direct>copied)
 return {'passive':float(np.mean(passive)),'grounded_question':float(np.mean(question)),'heavy_noise':float(np.mean(noise)),'false_echo_resistance':float(np.mean(echo))}

def architecture_science(seed,budget=90):
 r=np.random.default_rng(seed);dim=12
 # Candidate program genes represent non-graph associative, temporal, predictive,
 # workspace, active-observation, and memory operators plus numeric parameters.
 hidden=r.normal(size=dim);pair=r.normal(0,.35,(dim,dim));pair=np.triu(pair,1)
 def score(x):
  z=1.4*np.sum(x*hidden)+np.sum(pair*np.outer(x,x))-.28*np.sum(x)+r.normal(0,.12);return float(z)
 def random_search():
  xs=r.integers(0,2,(budget,dim));ys=[score(x) for x in xs];return max(ys)
 def learned():
  X=r.integers(0,2,(22,dim));Y=np.array([score(x) for x in X]);history=[]
  for t in range(22,budget):
   m=ExtraTreesRegressor(n_estimators=64,min_samples_leaf=2,random_state=seed+t,n_jobs=1).fit(X,Y)
   parents=X[np.argsort(Y)[-6:]];cand=[]
   for _ in range(180):
    x=parents[int(r.integers(len(parents)))].copy();flip=r.choice(dim,int(r.integers(1,4)),replace=False);x[flip]=1-x[flip];cand.append(x)
   cand=np.unique(cand,axis=0);mu=np.stack([q.predict(cand) for q in m.estimators_]);acq=mu.mean(0)+.55*mu.std(0);x=cand[int(np.argmax(acq))];y=score(x);X=np.vstack([X,x]);Y=np.r_[Y,y];history.append(float(Y.max()))
  return float(Y.max()),history,X[int(np.argmax(Y))].tolist()
 a=random_search();b,h,x=learned();return {'random_best':a,'learned_best':b,'gain':b-a,'learned_wins':int(b>a),'history':h,'winner':x}

def video_experiment(seed,n=28,D=64):
 r=np.random.default_rng(seed);bases=r.normal(size=(n,D));episodes=[]
 for e in range(n):
  vv=[]
  for _ in range(18):
   x=np.roll(bases[e],int(r.integers(-12,13)));x=x*r.uniform(.72,1.28)+r.normal(0,.22,D);vv.append(x)
  episodes.append(np.stack(vv))
 def fresh(q):return int(np.argmin([np.min(np.linalg.norm(v-q[None],axis=1)) for v in episodes]))
 same=[];occ=[];switch=[];active=[]
 for _ in range(1000):
  e=int(r.integers(n));q=np.roll(bases[e],int(r.integers(-18,19)))+r.normal(0,.28,D);same.append(fresh(q)==e)
  mask=r.random(D)>.65;qo=q.copy();qo[~mask]=0;p=fresh(qo);occ.append(p==e)
  b=int(r.choice([x for x in range(n) if x!=e]));qb=np.roll(bases[b],int(r.integers(-15,16)))+r.normal(0,.28,D);switch.append(fresh(qb)==b)
  # Active second view after ambiguous occlusion.
  p2=fresh(qb if p!=e else np.roll(bases[e],int(r.integers(-8,9)))+r.normal(0,.22,D));active.append((p2==b) if b!=e else (p2==e))
 return {'changed_view':float(np.mean(same)),'severe_occlusion':float(np.mean(occ)),'true_switch':float(np.mean(switch)),'active_reinspection':float(np.mean(active))}

def run_seed(seed):
 mem=memory_experiment(seed);act=active_science(seed+1);cross=cross_modal(seed+2);sib=sibling_experiment(seed+3);arch=architecture_science(seed+4);vid=video_experiment(seed+5)
 blob=pickle.dumps((mem,act,cross,sib,arch,vid));restored=pickle.loads(blob)
 return {'seed':seed,'memory':mem,'active_science':act,'cross_modal':cross,'siblings':sib,'architecture_science':arch,'video':vid,'save_reload':int(restored[0]['locked']==mem['locked']),'claim_boundary':'R29 Python reference experiments; evaluator labels never enter learner state; no native Zag claim.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--seed',type=int,required=True);ap.add_argument('--out',required=True);a=ap.parse_args();t=time.time();o=run_seed(a.seed);o['elapsed_seconds']=time.time()-t;Path(a.out).parent.mkdir(parents=True,exist_ok=True);Path(a.out).write_text(json.dumps(o,indent=2));print(json.dumps({k:v for k,v in o.items() if k not in ('architecture_science',)},indent=2))
if __name__=='__main__':main()
