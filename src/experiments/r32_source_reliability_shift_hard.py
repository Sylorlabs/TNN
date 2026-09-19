from __future__ import annotations
import numpy as np,json
from pathlib import Path
OUT=Path('/mnt/data/r32_epistemic');K=5;S=3
CONDS=['dominant_flip','correlated_flip','state_and_source_shift','flip_return']

def world(r,cond,T=240):
    state=int(r.integers(K)); other=(state+1+int(r.integers(K-1)))%K
    obs=[]
    for t in range(T):
        # source 0 is seen 60% of the time and begins highly reliable
        u=r.random();src=0 if u<.60 else (1 if u<.82 else 2)
        rel=[.94,.73,.68]
        if cond in ['dominant_flip','correlated_flip'] and t>=100: rel=[.15,.80,.76]
        if cond=='flip_return':
            if 75<=t<165:rel=[.12,.80,.74]
        if cond=='state_and_source_shift' and t>=105:
            state=other; rel=[.18,.82,.74]
        e=r.normal(0,.42,K);e[state]+=.55+1.05*rel[src]
        if r.random()>rel[src]:
            w=other if src==0 else int(r.integers(K));
            if w==state:w=(w+1)%K
            e[w]+=1.75;e[state]-=.45
        # correlated wrong bursts between 0 and 1
        if cond=='correlated_flip' and t>=100 and (t//8)%4==0 and src in [0,1]:
            e[other]+=1.45;e[state]-=.35
        obs.append((src,e,state))
    return obs

class Model:
 def __init__(self,kind):self.kind=kind;self.trust=np.array([.9,.72,.68]) if kind!='equal' else np.ones(S);self.score=np.zeros(K);self.hist=[];self.pending=[];self.t=0
 def step(self,src,e):
  self.t+=1; self.score=.78*self.score+self.trust[src]*e; pred=int(np.argmax(self.score)); self.hist.append((src,e.copy()))
  if len(self.hist)>18:self.hist.pop(0)
  if self.kind=='adaptive':
   self.pending.append((self.t,src,int(np.argmax(e))))
   if len(self.pending)>10:
    _,s,claim=self.pending.pop(0)
    # independent evidence consensus excludes source s entirely
    oth=[x for q,x in self.hist if q!=s]
    if len(oth)>=3:
     cons=int(np.argmax(np.mean(oth,axis=0)));reward=1 if claim==cons else -1
     self.trust[s]=float(np.clip(self.trust[s]+.055*reward,.05,1.25))
  return pred

def eval_seed(seed):
 r=np.random.default_rng(seed);out={'seed':seed}
 for c in CONDS:
  out[c]={}
  for kind in ['equal','fixed','adaptive']:
   acc=[];post=[];wrong=[];trust=[]
   for rep in range(160):
    ob=world(r,c);m=Model(kind);ok=[]
    for t,(s,e,y) in enumerate(ob):
     p=m.step(s,e);ok.append(p==y);wrong.append(p!=y and t>115)
    acc.append(np.mean(ok));post.append(np.mean(ok[120:]));trust.append(m.trust.copy())
   out[c][kind]={'accuracy':float(np.mean(acc)),'post_shift':float(np.mean(post)),'wrong':float(np.mean(wrong)),'trust':np.mean(trust,axis=0).tolist()}
 return out

def main():
 rows=[eval_seed(97500+i) for i in range(10)];agg={}
 for c in CONDS:
  agg[c]={}
  for k in ['equal','fixed','adaptive']:
   agg[c][k]={m:float(np.mean([r[c][k][m] for r in rows])) for m in ['accuracy','post_shift','wrong']}
 out={'aggregate':agg,'rows':rows,'boundary':'REFERENCE_ONLY post-100 source-reliability challenge. Learner receives only source identity, evidence vectors, and delayed independent-source agreement; hidden source reliability and evaluator world state are test-only.'}
 (OUT/'R32_SOURCE_RELIABILITY_SHIFT_HARD_REFERENCE_ONLY.json').write_text(json.dumps(out,indent=2));print(json.dumps(agg,indent=2))
if __name__=='__main__':main()
