from __future__ import annotations
import json,random,math
from collections import Counter,defaultdict,deque
from pathlib import Path
import numpy as np
OUT=Path('/mnt/data/tnn-r31-endogenous-chunking/results')
COMMON=(4,7,4,9); COMMON_TWIN=(4,7,5,9); ALT=(8,5,8,6); NEW=(12,3,12,8,12); CTXA=(1,1);CTXB=(2,2);TAIL=[(5,6),(6,5),(10,11),(11,10)]
def make(r,regime,noise=.12):
 ctx=CTXA if r.random()<.5 else CTXB;q=r.random()
 if q<.18: core=NEW;y=2
 elif q<.36:core=ALT;y=1
 else:
  core=COMMON if r.random()<.82 else COMMON_TWIN
  if regime==0:y=0 if core==COMMON else 1
  elif regime==1:y=(0 if ctx==CTXA else 1) if core==COMMON else (1 if ctx==CTXA else 2)
  elif regime==2:y=(0 if ctx==CTXA else 2) if core==COMMON else (2 if ctx==CTXA else 1)
  else:y=(1 if ctx==CTXA else 0) if core==COMMON else (2 if ctx==CTXA else 0)
 if r.random()<noise:y=r.choice([z for z in range(3) if z!=y])
 pre=tuple(r.randrange(13,22) for _ in range(r.randrange(0,3)));post=tuple(r.randrange(13,22) for _ in range(r.randrange(0,3)))
 return pre+ctx+core+r.choice(TAIL)+post,y
class M:
 def __init__(self):self.s=defaultdict(Counter)
 def observe(self,x,y):
  for n in range(2,min(8,len(x))+1):
   for i in range(len(x)-n+1):self.s[tuple(x[i:i+n])][y]+=1
 def scores(self,x):
  v=np.zeros(3,float)
  for n in range(2,min(8,len(x))+1):
   for i in range(len(x)-n+1):
    c=self.s.get(tuple(x[i:i+n]));
    if not c:continue
    N=sum(c.values());pur=max(c.values())/N
    if N<4 or pur<.48:continue
    w=max(0,pur-1/3)*math.log1p(N)*math.sqrt(n)
    for y,k in c.items():v[y]+=w*k/N
  return v
 def pred(self,x):v=self.scores(x);return int(v.argmax()) if v.max()>0 else 0
class Over:
 def __init__(self):self.m=M()
 def step(self,x,y):p=self.m.pred(x);self.m.observe(x,y);return p
class Bank:
 def __init__(self,window=24,err=.42,votes=4,maxr=6,replay=False):
  self.mm=[M()];self.a=0;self.e=deque(maxlen=window);self.err=err;self.votes=votes;self.av=Counter();self.maxr=maxr;self.spawn=0;self.switch=0;self.replay=replay;self.buf=[deque(maxlen=500) for _ in range(maxr)]
 def step(self,x,y):
  ps=[m.pred(x) for m in self.mm];p=ps[self.a];self.e.append(p!=y)
  for j,q in enumerate(ps):
   if j!=self.a and q==y and p!=y:self.av[j]+=1
   else:self.av[j]=max(0,self.av[j]-1)
  cand=[j for j,v in self.av.items() if v>=self.votes]
  if cand:
   self.a=max(cand,key=self.av.get);self.av.clear();self.e.clear();self.switch+=1
  elif len(self.e)==self.e.maxlen and sum(self.e)/len(self.e)>=self.err and len(self.mm)<self.maxr:
   self.mm.append(M());self.a=len(self.mm)-1;self.av.clear();self.e.clear();self.spawn+=1
  self.mm[self.a].observe(x,y);self.buf[self.a].append((x,y))
  if self.replay and len(self.mm)>1:
   # sparse replay preserves old regime traces without sharing evaluator regime IDs
   for j in range(len(self.mm)):
    if j!=self.a and self.buf[j] and random.random()<.03:
     ox,oy=self.buf[j][random.randrange(len(self.buf[j]))];self.mm[j].observe(ox,oy)
  return p
 def pred_active(self,x):return self.mm[self.a].pred(x)
def train0(o,seed,n=4000):
 r=random.Random(seed)
 for _ in range(n):x,y=make(r,0);o.step(x,y)
def phase(o,seed,reg,n):
 r=random.Random(seed);ok=0;first=0
 for i in range(n):x,y=make(r,reg);p=o.step(x,y);ok+=p==y;first+= (p==y) if i<200 else 0
 return ok/n,first/200
def evalreg(o,seed,reg,n=1500):
 r=random.Random(seed);ok=0
 for _ in range(n):
  x,y=make(r,reg);p=o.pred_active(x) if isinstance(o,Bank) else o.m.pred(x);ok+=p==y
 return ok/n
def run(seed,kind):
 o=Over() if kind=='overwrite' else Bank(replay=(kind=='bank_replay'))
 train0(o,seed*20+1);base=evalreg(o,seed*30+2,0)
 seq=[]
 for pi,reg in enumerate([1,0,2,1,3,0]):
  online,first=phase(o,seed*100+10+pi,reg,3500 if reg!=0 else 1200);final=evalreg(o,seed*100+50+pi,reg);seq.append({'regime':reg,'online':online,'first200':first,'final':final})
 # explicit old-regime retention after all switches without updating
 retention=[evalreg(o,seed*100+90+r,r) for r in range(4)]
 return {'seed':seed,'kind':kind,'base':base,'sequence':seq,'retention':retention,'retention_mean':float(np.mean(retention)),'regimes':len(o.mm) if isinstance(o,Bank) else 1,'spawned':o.spawn if isinstance(o,Bank) else 0,'switches':o.switch if isinstance(o,Bank) else 0}
def main():
 rows=[]
 for s in range(10):
  for k in ['overwrite','bank','bank_replay']:rows.append(run(7400+s,k))
  print('DONE',7400+s,flush=True)
 agg={}
 for k in ['overwrite','bank','bank_replay']:
  rr=[x for x in rows if x['kind']==k];agg[k]={'base':float(np.mean([x['base'] for x in rr])),'retention_mean':float(np.mean([x['retention_mean'] for x in rr])),'retention_by_regime':[float(np.mean([x['retention'][j] for x in rr])) for j in range(4)],'switch_final_mean':float(np.mean([np.mean([z['final'] for z in x['sequence']]) for x in rr])),'switch_first200_mean':float(np.mean([np.mean([z['first200'] for z in x['sequence']]) for x in rr])),'regimes':float(np.mean([x['regimes'] for x in rr])),'spawned':float(np.mean([x['spawned'] for x in rr])),'switches':float(np.mean([x['switches'] for x in rr]))}
 out={'rows':rows,'aggregate':agg,'boundary':'REFERENCE_ONLY hard regime challenge: near-twin spans, 12% consequence noise, recurrent regime returns. No regime IDs supplied to learner.'};(OUT/'regime_chunk_memory_hard.json').write_text(json.dumps(out,indent=2));print(json.dumps(agg,indent=2))
if __name__=='__main__':main()
