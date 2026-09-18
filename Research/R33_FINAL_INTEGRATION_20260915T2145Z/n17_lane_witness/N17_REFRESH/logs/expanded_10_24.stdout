from __future__ import annotations
import os,sys,json,math
os.environ['OMP_NUM_THREADS']='1';os.environ['MKL_NUM_THREADS']='1';os.environ['OPENBLAS_NUM_THREADS']='1'
sys.path.insert(0,'/mnt/data/r31_part2')
import r31_postrepair_part2 as base
import r31_postrepair_part2b as b
import r31_postrepair_part2c as c
import numpy as np
from sklearn.linear_model import LogisticRegression
from pathlib import Path
OUT=Path('/mnt/data/r31_part2')

def entropy(p):
 p=np.maximum(p,1e-9);p=p/p.sum();return float(-(p*np.log(p)).sum()/math.log(len(p)))
def normprob(score):
 z=np.exp(score-np.max(score));return z/(z.sum()+1e-9)

def setup(seed):
 w=base.AcousticWorld(seed);rng=np.random.default_rng(seed+99);train=[]
 for _ in range(9000):
  e=int(rng.integers(0,w.entities));train.append(w.episode(e,rng,'matched'))
 L=base.GroundLearner(base.ChunkBank(),'dual');L.fit(train);prot,ctxclf=b.train_context(seed,w,train);classes=list(L.clf.classes_);idx={int(x):i for i,x in enumerate(classes)}
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

def feats(score,ctxv,top_prev=-1,action_gap=0.0):
 p=normprob(score);order=np.argsort(p);top=int(order[-1]);margin=float(p[order[-1]]-p[order[-2]]);ctx=int(np.argmax(ctxv));ctxmargin=float(np.sort(ctxv)[-1]-np.sort(ctxv)[-2]);return [margin,float(np.max(p)),1.0-entropy(p),float(top==ctx),ctxmargin,float(top_prev<0 or top==top_prev),float(action_gap)]

def generate_state(w,rng,e,cond,unstable=False):
 if unstable:
  s,_=w.ambiguous(e,rng); return s,-1
 s,y=w.episode(e,rng,cond);return s,y

def run(seed):
 w,rng,L,prot,ctxclf,classes,idx,sig,learned=setup(seed)
 # Delayed-regret calibration. Training never exposes condition names to policy; only internal evidence features and eventual correctness/stability.
 X1=[];Y1=[];X2=[];Y2=[]
 conds=['matched','hard_noise','near_twin','confwrong','speaker_shift','onset_damage']
 for _ in range(9000):
  e=int(rng.integers(0,w.entities));unstable=rng.random()<.16;cond=str(rng.choice(conds));s,y=generate_state(w,rng,e,cond,unstable)
  q=L.probs(s);cv=b.context_vec(prot,e,rng,amb=unstable);ctxv=context_evidence(ctxclf,classes,idx,cv);score=np.log(q+1e-8)+np.log(.2+.8*ctxv);pred1=int(classes[int(np.argmax(score))]);f1=feats(score,ctxv);X1.append(f1);Y1.append(int((not unstable) and pred1==y))
  used=[];a=select_action(score,learned,used);used.append(a)
  if unstable:
   te=e if rng.random()<.5 else (e^1);ty=int(w.effect[te])
  else:ty=y
  obs=sig[idx[ty],a]+rng.normal(0,.65);oldtop=int(np.argmax(score));new=action_update(score,obs,a,learned);gap=float(np.max(new)-np.partition(new,-2)[-2]);pred2=int(classes[int(np.argmax(new))]);f2=feats(new,ctxv,oldtop,gap);X2.append(f2);Y2.append(int((not unstable) and pred2==y))
 safe1=LogisticRegression(max_iter=400,class_weight='balanced').fit(X1,Y1);safe2=LogisticRegression(max_iter=400,class_weight='balanced').fit(X2,Y2)
 evalconds=['matched','speaker_shift','hard_noise','onset_damage','near_twin','confwrong','novel']
 out={}
 probes=[]
 for cond in evalconds:
  correct=safe=abst=0;N=1800
  for _ in range(N):
   e=int(rng.integers(0,w.entities));s,y=w.episode(e,rng,cond);q=L.probs(s);cv=b.context_vec(prot,e,rng);ctxv=context_evidence(ctxclf,classes,idx,cv);score=np.log(q+1e-8)+np.log(.2+.8*ctxv);pred=int(classes[int(np.argmax(score))]);f1=feats(score,ctxv);ps1=float(safe1.predict_proba([f1])[0,1]);used=[];nprobe=0
   if ps1<.83:
    a=select_action(score,learned,used);used.append(a);obs=sig[idx[y],a]+rng.normal(0,.65);oldtop=int(np.argmax(score));score=action_update(score,obs,a,learned);nprobe=1;f2=feats(score,ctxv,oldtop,float(np.max(score)-np.partition(score,-2)[-2]));ps2=float(safe2.predict_proba([f2])[0,1]);pred=int(classes[int(np.argmax(score))])
    if ps2<.76:
     a=select_action(score,learned,used);used.append(a);obs=sig[idx[y],a]+rng.normal(0,.65);score=action_update(score,obs,a,learned);nprobe=2;pred=int(classes[int(np.argmax(score))]);p=normprob(score);margin=float(np.sort(p)[-1]-np.sort(p)[-2]); decision=-1 if margin<.32 else pred
    else:decision=pred
   else:decision=pred
   probes.append(nprobe);correct+=decision==y;abst+=decision==-1;safe+=(decision==y or decision==-1)
  out[cond]={'correct':correct/N,'abstain':abst/N,'safe':safe/N}
 # Correlated wrong: both acoustic views can lie. Physical consequences are independent ground truth; unresolved cases should abstain.
 correct=safe=abst=0;N=1800
 for _ in range(N):
  e=int(rng.integers(0,w.entities));s,y=w.episode(e,rng,'confwrong');q=L.probs(s);cv=b.context_vec(prot,e,rng);ctxv=context_evidence(ctxclf,classes,idx,cv);score=np.log(q+1e-8)+np.log(.2+.8*ctxv);used=[]
  for z in range(2):
   a=select_action(score,learned,used);used.append(a);obs=sig[idx[y],a]+rng.normal(0,.72);score=action_update(score,obs,a,learned,.9)
  p=normprob(score);margin=float(np.sort(p)[-1]-np.sort(p)[-2]);pred=int(classes[int(np.argmax(p))]);decision=-1 if margin<.28 else pred;correct+=decision==y;abst+=decision==-1;safe+=(decision==y or decision==-1)
 out['correlated_wrong']={'correct':correct/N,'abstain':abst/N,'safe':safe/N}
 # Ambiguous unstable referent: two physical probes can disagree because the latent source changes; policy should detect instability and abstain.
 abst=safe=0;N=1800
 for _ in range(N):
  e=int(rng.integers(0,w.entities));s,_=w.ambiguous(e,rng);q=L.probs(s);cv=b.context_vec(prot,e,rng,amb=True);ctxv=context_evidence(ctxclf,classes,idx,cv);score=np.log(q+1e-8)+np.log(.2+.8*ctxv);used=[];tops=[];obsclasses=[]
  for z in range(2):
   a=select_action(score,learned,used);used.append(a);te=e if rng.random()<.5 else (e^1);ty=int(w.effect[te]);obs=sig[idx[ty],a]+rng.normal(0,.8);score=action_update(score,obs,a,learned,.95);tops.append(int(np.argmax(score)));obsclasses.append(ty)
  p=normprob(score);margin=float(np.sort(p)[-1]-np.sort(p)[-2]);instable=(obsclasses[0]!=obsclasses[1] or tops[0]!=tops[1]);decision=-1 if instable or margin<.4 else int(classes[int(np.argmax(p))]);abst+=decision==-1;safe+=decision==-1
 out['ambiguous']={'abstain':abst/N,'safe':safe/N}
 out['mean_probes']=float(np.mean(probes));out['hard_correct_mean']=float(np.mean([out[x]['correct'] for x in ['speaker_shift','hard_noise','onset_damage','near_twin','confwrong','novel']]))
 return out

def main():
 from concurrent.futures import ProcessPoolExecutor,as_completed
 rows=[]
 with ProcessPoolExecutor(max_workers=4) as ex:
  fs={ex.submit(run,9700+i):9700+i for i in range(8)}
  for f in as_completed(fs):rows.append({'seed':fs[f],'result':f.result()});print('DONE',fs[f],flush=True)
 rows.sort(key=lambda x:x['seed']); keys=['matched','speaker_shift','hard_noise','onset_damage','near_twin','confwrong','novel','correlated_wrong','ambiguous']
 agg={}
 for k in keys:
  fields=rows[0]['result'][k].keys();agg[k]={f:float(np.mean([r['result'][k][f] for r in rows])) for f in fields}
 agg['mean_probes']=float(np.mean([r['result']['mean_probes'] for r in rows]));agg['hard_correct_mean']=float(np.mean([r['result']['hard_correct_mean'] for r in rows]))
 out={'aggregate':agg,'rows':rows,'boundary':'REFERENCE_ONLY sequential metacognitive evidence. Commit safety is learned from delayed correctness/stability using only internal evidence features. Physical probe selection maximizes learned predicted consequence separation. No acoustic/token/phoneme/VAD/chunk/corruption labels at test.'};(OUT/'R31_SEQUENTIAL_EVIDENCE_ABSTENTION_REFERENCE_ONLY.json').write_text(json.dumps(out,indent=2));print(json.dumps(agg,indent=2))
if __name__=='__main__':main()
