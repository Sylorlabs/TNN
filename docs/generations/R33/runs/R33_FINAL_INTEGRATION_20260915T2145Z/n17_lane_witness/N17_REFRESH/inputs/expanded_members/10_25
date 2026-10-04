from __future__ import annotations
import os,sys,json,math
os.environ['OMP_NUM_THREADS']='1';os.environ['MKL_NUM_THREADS']='1';os.environ['OPENBLAS_NUM_THREADS']='1'
sys.path.insert(0,'/mnt/data/r31_part2')
import r31_postrepair_part2 as base
import r31_postrepair_part2b as b
import r31_postrepair_part2c as c
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
OUT=Path('/mnt/data/r31_part2')

MAX_PROBES=4
PROBE_COST=.035

def entropy(p):
 p=np.maximum(p,1e-12);p=p/p.sum();return float(-(p*np.log(p)).sum()/math.log(len(p)))
def normprob(score):
 z=np.exp(score-np.max(score));return z/(z.sum()+1e-12)

def setup(seed):
 w=base.AcousticWorld(seed);rng=np.random.default_rng(seed+99);train=[]
 for _ in range(9000):
  e=int(rng.integers(0,w.entities));train.append(w.episode(e,rng,'matched'))
 L=base.GroundLearner(base.ChunkBank(),'dual');L.fit(train)
 prot,ctxclf=b.train_context(seed,w,train)
 classes=list(L.clf.classes_);idx={int(x):i for i,x in enumerate(classes)}
 sig=c.build_action_world(seed,classes);learned=c.train_action_model(seed,classes,sig)
 return w,rng,L,prot,ctxclf,classes,idx,sig,learned

def context_evidence(ctxclf,classes,idx,cv):
 cp=ctxclf.predict_proba(cv.reshape(1,-1))[0];v=np.zeros(len(classes))
 for i,z in enumerate(ctxclf.classes_):
  if int(z) in idx:v[idx[int(z)]]=cp[i]
 return v

def select_action(score,learned,used):
 top=np.argsort(score)[-2:];sep=np.abs(learned[top[-1]]-learned[top[-2]]);order=np.argsort(sep)[::-1]
 for a in order:
  if int(a) not in used:return int(a)
 return int(order[0])

def action_update(score,obs,a,learned,var=.85):
 s=score.copy()
 for ci in range(len(s)):s[ci]+=-((obs-learned[ci,a])**2)/(2*var**2)
 return s

def probe_inferred_class(obs,a,learned):
 return int(np.argmin(np.abs(learned[:,a]-obs)))

def feat_state(score,ctxv,probe_classes,top_history,last_gap):
 p=normprob(score);order=np.argsort(p);top=int(order[-1]);margin=float(p[order[-1]]-p[order[-2]])
 ctx=int(np.argmax(ctxv));sp=np.sort(ctxv);ctxmargin=float(sp[-1]-sp[-2]) if len(sp)>1 else 1.0
 n=len(probe_classes); uniq=len(set(probe_classes)) if n else 0
 if n:
  counts=np.bincount(np.asarray(probe_classes,dtype=int),minlength=len(p)).astype(float);vp=counts/counts.sum();vote_entropy=entropy(vp)
  vote_frac=float(counts.max()/counts.sum()); last_agree=float(probe_classes[-1]==top)
 else:
  vote_entropy=0.;vote_frac=0.;last_agree=0.
 changes=sum(int(top_history[i]!=top_history[i-1]) for i in range(1,len(top_history)))
 acoustic_ctx_agree=float(top==ctx)
 stable_top=float(len(top_history)<2 or top_history[-1]==top_history[-2])
 # No evaluator labels/condition IDs. Every feature is internally observable.
 return [margin,float(np.max(p)),1.0-entropy(p),acoustic_ctx_agree,ctxmargin,
         n/4.0,uniq/4.0,vote_frac,1.0-vote_entropy,last_agree,changes/4.0,stable_top,
         min(float(last_gap)/12.0,4.0)]

def make_traj(w,rng,L,prot,ctxclf,classes,idx,sig,learned,cond,unstable):
 e=int(rng.integers(0,w.entities))
 if unstable:s,_=w.ambiguous(e,rng); y=None
 else:s,y=w.episode(e,rng,cond)
 q=L.probs(s);cv=b.context_vec(prot,e,rng,amb=unstable);ctxv=context_evidence(ctxclf,classes,idx,cv)
 score=np.log(q+1e-8)+np.log(.2+.8*ctxv)
 used=[];probe_classes=[];top_history=[int(np.argmax(score))];last_gap=0.
 states=[]
 for stage in range(MAX_PROBES+1):
  pred=int(classes[int(np.argmax(score))]);correct=(not unstable and pred==y)
  states.append((feat_state(score,ctxv,probe_classes,top_history,last_gap),correct,unstable,pred))
  if stage==MAX_PROBES:break
  a=select_action(score,learned,used);used.append(a)
  if unstable:
   te=e if rng.random()<.5 else (e^1);ty=int(w.effect[te])
  else:ty=y
  obs=sig[idx[ty],a]+rng.normal(0,.68)
  probe_classes.append(probe_inferred_class(obs,a,learned))
  score=action_update(score,obs,a,learned,.9)
  top_history.append(int(np.argmax(score)))
  last_gap=float(np.max(score)-np.partition(score,-2)[-2])
 return states

def train_policy(seed,w,rng,L,prot,ctxclf,classes,idx,sig,learned):
 conds=['matched','hard_noise','near_twin','confwrong','speaker_shift','onset_damage','novel']
 X=[];Y=[]
 # Generate complete trajectories. Action targets are derived by backward scalar utility,
 # not condition/ambiguity names. Hidden world state is used only to deliver delayed reward.
 for _ in range(13000):
  unstable=bool(rng.random()<.20);cond=str(rng.choice(conds));st=make_traj(w,rng,L,prot,ctxclf,classes,idx,sig,learned,cond,unstable)
  V=[0.]*(MAX_PROBES+1);A=[2]*(MAX_PROBES+1) # 0 commit, 1 continue, 2 abstain
  for t in range(MAX_PROBES,-1,-1):
   _,correct,unst,_=st[t]
   u_commit=1.0 if correct else -1.45
   # Abstention is safe but has opportunity cost. On irresolvable experiences delayed
   # regret is low; on correctly resolvable experiences unnecessary abstention costs more.
   if unst:u_abst=.48
   elif correct:u_abst=-.34
   else:u_abst=.10
   vals=[u_commit,-999.,u_abst]
   if t<MAX_PROBES:vals[1]=V[t+1]-PROBE_COST
   a=int(np.argmax(vals));V[t]=vals[a];A[t]=a
  for t in range(MAX_PROBES+1):X.append(st[t][0]);Y.append(A[t])
 clf=RandomForestClassifier(n_estimators=140,max_depth=11,min_samples_leaf=10,class_weight='balanced_subsample',random_state=seed,n_jobs=1,max_features=.8).fit(X,Y)
 return clf

def decide_one(w,rng,L,prot,ctxclf,classes,idx,sig,learned,policy,e,cond,unstable=False):
 if unstable:s,_=w.ambiguous(e,rng);y=None
 else:s,y=w.episode(e,rng,cond)
 q=L.probs(s);cv=b.context_vec(prot,e,rng,amb=unstable);ctxv=context_evidence(ctxclf,classes,idx,cv);score=np.log(q+1e-8)+np.log(.2+.8*ctxv)
 used=[];probe_classes=[];top_history=[int(np.argmax(score))];last_gap=0.;nprobe=0
 while True:
  f=feat_state(score,ctxv,probe_classes,top_history,last_gap);a=int(policy.predict([f])[0]);pred=int(classes[int(np.argmax(score))])
  if a==0:return pred,nprobe
  if a==2 or nprobe>=MAX_PROBES:return -1,nprobe
  act=select_action(score,learned,used);used.append(act)
  if unstable:
   te=e if rng.random()<.5 else (e^1);ty=int(w.effect[te])
  else:ty=y
  obs=sig[idx[ty],act]+rng.normal(0,.68);probe_classes.append(probe_inferred_class(obs,act,learned));score=action_update(score,obs,act,learned,.9);top_history.append(int(np.argmax(score)));last_gap=float(np.max(score)-np.partition(score,-2)[-2]);nprobe+=1

def eval_policy(seed):
 w,rng,L,prot,ctxclf,classes,idx,sig,learned=setup(seed);policy=train_policy(seed,w,rng,L,prot,ctxclf,classes,idx,sig,learned)
 conds=['matched','speaker_shift','hard_noise','onset_damage','near_twin','confwrong','novel'];out={};probes=[]
 for cond in conds:
  correct=abst=safe=0;N=2200
  for _ in range(N):
   e=int(rng.integers(0,w.entities));d,n=decide_one(w,rng,L,prot,ctxclf,classes,idx,sig,learned,policy,e,cond,False);_,y=w.episode(e,np.random.default_rng(0),cond) if False else (None,None)
   # regenerate target identity directly; AcousticWorld grounding target is stable entity effect.
   # actual episode label depends only on entity's grounded effect, not corruption.
   y=int(w.effect[e]);correct+=d==y;abst+=d==-1;safe+=(d==y or d==-1);probes.append(n)
  out[cond]={'correct':correct/N,'abstain':abst/N,'safe':safe/N}
 # genuinely unstable referent: no unique correct answer over the evidence interval
 abst=0;N=2600;ap=[]
 for _ in range(N):
  e=int(rng.integers(0,w.entities));d,n=decide_one(w,rng,L,prot,ctxclf,classes,idx,sig,learned,policy,e,'matched',True);abst+=d==-1;ap.append(n)
 out['ambiguous']={'abstain':abst/N};out['mean_probes']=float(np.mean(probes));out['ambig_mean_probes']=float(np.mean(ap));out['hard_correct_mean']=float(np.mean([out[x]['correct'] for x in ['speaker_shift','hard_noise','onset_damage','near_twin','confwrong','novel']]))
 # Inspect learned action usage, useful for diagnosing collapse into always-commit/always-abstain.
 return out

def main():
 rows=[]
 with ProcessPoolExecutor(max_workers=4) as ex:
  fs={ex.submit(eval_policy,10300+i):10300+i for i in range(8)}
  for f in as_completed(fs):rows.append({'seed':fs[f],'result':f.result()});print('DONE',fs[f],flush=True)
 rows.sort(key=lambda x:x['seed']);keys=['matched','speaker_shift','hard_noise','onset_damage','near_twin','confwrong','novel']
 agg={}
 for k in keys:
  agg[k]={f:float(np.mean([r['result'][k][f] for r in rows])) for f in ['correct','abstain','safe']}
 agg['ambiguous']={'abstain':float(np.mean([r['result']['ambiguous']['abstain'] for r in rows]))}
 agg['mean_probes']=float(np.mean([r['result']['mean_probes'] for r in rows]));agg['ambig_mean_probes']=float(np.mean([r['result']['ambig_mean_probes'] for r in rows]));agg['hard_correct_mean']=float(np.mean([r['result']['hard_correct_mean'] for r in rows]))
 out={'aggregate':agg,'rows':rows,'boundary':'REFERENCE_ONLY state-dependent learned commit/continue/abstain. Policy receives only internal acoustic/context/probe-consistency features. Training signal is delayed scalar utility/cost; no ambiguity/corruption label is a learner feature. Raw/chunk dual architecture unchanged.'}
 (OUT/'R31_STATE_DEPENDENT_PROBE_POLICY_REFERENCE_ONLY.json').write_text(json.dumps(out,indent=2));print(json.dumps(agg,indent=2))
if __name__=='__main__':main()
