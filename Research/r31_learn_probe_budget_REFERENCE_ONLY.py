from __future__ import annotations
import os,sys,json,math
os.environ['OMP_NUM_THREADS']='1';os.environ['MKL_NUM_THREADS']='1';os.environ['OPENBLAS_NUM_THREADS']='1'
sys.path.insert(0,'/mnt/data/r31_part2')
import r31_postrepair_part2 as base
import r31_postrepair_part2b as b
import r31_postrepair_part2c as c
import numpy as np
from pathlib import Path
OUT=Path('/mnt/data/r31_part2')

def normprob(s):z=np.exp(s-np.max(s));return z/(z.sum()+1e-9)
def setup(seed):
 w=base.AcousticWorld(seed);rng=np.random.default_rng(seed+99);train=[]
 for _ in range(9000):
  e=int(rng.integers(0,w.entities));train.append(w.episode(e,rng,'matched'))
 L=base.GroundLearner(base.ChunkBank(),'dual');L.fit(train);prot,ctxclf=b.train_context(seed,w,train);classes=list(L.clf.classes_);idx={int(x):i for i,x in enumerate(classes)};sig=c.build_action_world(seed,classes);learned=c.train_action_model(seed,classes,sig);return w,rng,L,prot,ctxclf,classes,idx,sig,learned
def ctxev(ctxclf,classes,idx,cv):
 cp=ctxclf.predict_proba(cv.reshape(1,-1))[0];v=np.zeros(len(classes))
 for i,z in enumerate(ctxclf.classes_):
  if int(z) in idx:v[idx[int(z)]]=cp[i]
 return v
def action(score,learned,used):
 top=np.argsort(score)[-2:];sep=np.abs(learned[top[-1]]-learned[top[-2]]);order=np.argsort(sep)[::-1]
 for a in order:
  if int(a) not in used:return int(a)
 return int(order[0])
def update(score,obs,a,learned,var=.9):
 s=score.copy()
 for ci in range(len(s)):s[ci]+=-((obs-learned[ci,a])**2)/(2*var**2)
 return s

def episode_trace(w,rng,L,prot,ctxclf,classes,idx,sig,learned,e,kind,maxp):
 unstable=kind=='ambiguous'
 if unstable:s,_=w.ambiguous(e,rng);y=-1;cv=b.context_vec(prot,e,rng,amb=True)
 else:s,y=w.episode(e,rng,kind);cv=b.context_vec(prot,e,rng)
 score=np.log(L.probs(s)+1e-8)+np.log(.2+.8*ctxev(ctxclf,classes,idx,cv));used=[];trace=[]
 for pno in range(maxp+1):
  p=normprob(score);order=np.argsort(p);top=int(order[-1]);margin=float(p[order[-1]]-p[order[-2]]);trace.append((top,margin,score.copy()))
  if pno==maxp:break
  a=action(score,learned,used);used.append(a)
  if unstable:te=e if rng.random()<.5 else (e^1);ty=int(w.effect[te])
  else:ty=y
  obs=sig[idx[ty],a]+rng.normal(0,.75 if unstable else .65);score=update(score,obs,a,learned,.95 if unstable else .85)
 return y,trace

def decide(trace,classes,maxp,stable_req,margin):
 # stop at earliest stable run of same top hypothesis with enough posterior separation
 for k in range(len(trace)):
  top,mg,_=trace[k]
  if mg<margin:continue
  if stable_req<=1: return int(classes[top]),k
  if k+1>=stable_req and all(trace[j][0]==top for j in range(k-stable_req+1,k+1)):return int(classes[top]),k
 # evidence never stabilized enough
 return -1,min(maxp,len(trace)-1)

def eval_policy(data,classes,pol,cost=.025):
 maxp,stable,margin=pol;correct=abst_amb=wrong=probes=0;stableN=ambN=0
 for kind,y,tr in data:
  d,p=decide(tr[:maxp+1],classes,maxp,stable,margin);probes+=p
  if kind=='ambiguous':ambN+=1;abst_amb+=d==-1
  else:stableN+=1;correct+=d==y;wrong+=(d!=-1 and d!=y)
 corr=correct/max(1,stableN);ab=abst_amb/max(1,ambN);pr=probes/max(1,len(data));util=corr+ab-0.6*(wrong/max(1,stableN))-cost*pr
 return {'correct':corr,'ambiguous_abstain':ab,'wrong_commit':wrong/max(1,stableN),'mean_probes':pr,'utility':util}

def run(seed):
 w,rng,L,prot,ctxclf,classes,idx,sig,learned=setup(seed);kinds=['matched','hard_noise','near_twin','confwrong','speaker_shift','onset_damage']
 def make(N):
  d=[]
  for _ in range(N):
   amb=rng.random()<.28;kind='ambiguous' if amb else str(rng.choice(kinds));e=int(rng.integers(0,w.entities));y,tr=episode_trace(w,rng,L,prot,ctxclf,classes,idx,sig,learned,e,kind,5);d.append((kind,y,tr))
  return d
 dev=make(4500);test=make(4500);grid=[]
 for mp in [2,3,4,5]:
  for st in [2,3]:
   for mg in [.18,.28,.38,.48]:grid.append(((mp,st,mg),eval_policy(dev,classes,(mp,st,mg))))
 best=max(grid,key=lambda x:x[1]['utility']);chosen=best[0];return {'chosen':chosen,'dev':best[1],'test':eval_policy(test,classes,chosen),'fixed2':eval_policy(test,classes,(2,2,.28))}
def main():
 from concurrent.futures import ProcessPoolExecutor,as_completed
 rows=[]
 with ProcessPoolExecutor(max_workers=4) as ex:
  fs={ex.submit(run,10100+i):10100+i for i in range(6)}
  for f in as_completed(fs):rows.append({'seed':fs[f],**f.result()});print('DONE',fs[f],flush=True)
 rows.sort(key=lambda x:x['seed']);agg={}
 for k in ['test','fixed2']:
  agg[k]={m:float(np.mean([r[k][m] for r in rows])) for m in ['correct','ambiguous_abstain','wrong_commit','mean_probes','utility']}
 agg['chosen_max_probes']=float(np.mean([r['chosen'][0] for r in rows]));agg['chosen_stability']=float(np.mean([r['chosen'][1] for r in rows]));agg['chosen_margin']=float(np.mean([r['chosen'][2] for r in rows]))
 out={'aggregate':agg,'rows':rows,'boundary':'REFERENCE_ONLY. Probe budget/stability/margin selected only on developmental delayed utility (correct stable outcome + abstain unstable evidence - wrong commitment - observation cost). No ambiguity/corruption label is available to the decision policy at test.'};(OUT/'R31_LEARNED_PROBE_BUDGET_REFERENCE_ONLY.json').write_text(json.dumps(out,indent=2));print(json.dumps(agg,indent=2))
if __name__=='__main__':main()
