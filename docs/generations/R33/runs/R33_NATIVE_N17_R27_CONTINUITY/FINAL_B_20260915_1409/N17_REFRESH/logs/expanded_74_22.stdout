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

class RawLearner:
 def __init__(self):self.clf=None
 def feat(self,s):
  f=np.zeros(128);h=np.zeros(32);t=np.zeros(32)
  for i,x in enumerate(s):
   h[x%32]+=1
   if i:t[(s[i-1]*31+x*17)%32]+=1
  z=np.concatenate([h,t]);z=z/(np.linalg.norm(z)+1e-9);f[:64]=z
  for i,x in enumerate(s):f[64+(x%32)]+=.12
  return f
 def fit(self,ep):self.clf=LogisticRegression(max_iter=500,C=2).fit(np.stack([self.feat(s) for s,y in ep]),np.array([y for s,y in ep]))
 def probs(self,s):return self.clf.predict_proba(self.feat(s).reshape(1,-1))[0]

def train_learners(seed):
 w=base.AcousticWorld(seed);rng=np.random.default_rng(seed+99);train=[]
 for _ in range(9000):
  e=int(rng.integers(0,w.entities));train.append(w.episode(e,rng,'matched'))
 raw=RawLearner();raw.fit(train)
 chunk=base.GroundLearner(base.ChunkBank(),'opaque');chunk.fit(train)
 dual=base.GroundLearner(base.ChunkBank(),'dual');dual.fit(train)
 prot,ctxclf=b.train_context(seed,w,train);classes=list(dual.clf.classes_);idx={int(x):i for i,x in enumerate(classes)};sig=c.build_action_world(seed,classes);learned=c.train_action_model(seed,classes,sig)
 return w,rng,train,{'raw_active':raw,'chunk_active':chunk,'dual_active':dual},prot,ctxclf,classes,idx,sig,learned

def probs_classes(L,s):return L.probs(s),list(L.clf.classes_)
def compression(L,episodes):
 if not hasattr(L,'bank'):return 0.0
 raw=sum(len(s) for s,y in episodes[:1000]);units=sum(len(L.bank.segment(s)) for s,y in episodes[:1000]);return 1-units/max(1,raw)

def run(seed):
 w,rng,train,learners,prot,ctxclf,classes,idx,sig,learned=train_learners(seed);out={}
 conds=['matched','speaker_shift','no_gap','silence_shift','hard_noise','onset_damage','near_twin','confwrong','novel']
 for name,L in learners.items():
  met={};req=0;N=1300
  for cond in conds:
   ok=0
   for _ in range(N):
    e=int(rng.integers(0,w.entities));s,y=w.episode(e,rng,cond);q,cls=probs_classes(L,s);cls=list(cls);li={int(z):i for i,z in enumerate(cls)};p=int(cls[int(np.argmax(q))]);sq=np.sort(q);margin=float(sq[-1]-sq[-2]);cv=b.context_vec(prot,e,rng);cp=ctxclf.predict_proba(cv.reshape(1,-1))[0];cc=int(ctxclf.classes_[int(np.argmax(cp))]);cm=float(np.sort(cp)[-1]-np.sort(cp)[-2]);ask=(margin<.22 or (p!=cc and cm>.12))
    if ask:
     req+=1;s2,_=w.episode(e,rng,'hard_noise' if cond!='matched' else 'matched');q=q+L.probs(s2);top=np.argsort(q)[-2:]
     # learned physical discriminator; remap candidate class indices to canonical action model classes
     ca=int(cls[top[-1]]);cb=int(cls[top[-2]]);ia=idx[ca];ib=idx[cb];a=int(np.argmax(np.abs(learned[ia]-learned[ib])));obs=sig[idx[y],a]+rng.normal(0,.65);score=np.log(q+1e-8)
     for ci,cval in enumerate(cls):score[ci]+=-((obs-learned[idx[int(cval)],a])**2)/(2*.85**2)
     p=int(cls[int(np.argmax(score))])
    ok+=p==y
   met[cond]=ok/N
  met['hard_mean']=float(np.mean([met[x] for x in ['speaker_shift','no_gap','hard_noise','onset_damage','near_twin','confwrong','novel']]));met['request_rate']=req/(N*len(conds));met['compression_gain']=compression(L,train);met['chunks']=len(L.bank.chunks) if hasattr(L,'bank') else 0
  out[name]=met
 return out

def main():
 from concurrent.futures import ProcessPoolExecutor,as_completed
 rows=[]
 with ProcessPoolExecutor(max_workers=4) as ex:
  fs={ex.submit(run,9900+i):9900+i for i in range(6)}
  for f in as_completed(fs):rows.append({'seed':fs[f],'result':f.result()});print('DONE',fs[f],flush=True)
 rows.sort(key=lambda x:x['seed']);names=['raw_active','chunk_active','dual_active'];keys=['matched','speaker_shift','no_gap','silence_shift','hard_noise','onset_damage','near_twin','confwrong','novel','hard_mean','request_rate','compression_gain','chunks'];agg={n:{k:float(np.mean([r['result'][n][k] for r in rows])) for k in keys} for n in names}
 out={'aggregate':agg,'rows':rows,'boundary':'REFERENCE_ONLY causal representation ablation. All routes get identical grounded context/reinspection/physical-probe opportunity. Raw route has no learned chunks; chunk route uses recruited reversible spans; dual retains both.'};(OUT/'R31_CHUNK_CAUSAL_ABLATION_REFERENCE_ONLY.json').write_text(json.dumps(out,indent=2));print(json.dumps(agg,indent=2))
if __name__=='__main__':main()
