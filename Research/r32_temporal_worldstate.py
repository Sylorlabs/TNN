import numpy as np,json,itertools
from pathlib import Path
OUT=Path('/mnt/data/r32_epistemic');K=5
CONDS=['stable','single_switch','late_switch','switch_back','false_burst','rapid_two_switch']

def make_stream(rng,cond,T=60):
 a=int(rng.integers(K)); b=(a+1+int(rng.integers(K-1)))%K; c=(b+1+int(rng.integers(K-1)))%K
 states=[a]*T
 if cond=='single_switch':
  q=int(rng.integers(18,32));states[q:]=[b]*(T-q)
 elif cond=='late_switch':
  q=int(rng.integers(43,52));states[q:]=[b]*(T-q)
 elif cond=='switch_back':
  q1=int(rng.integers(16,24));q2=int(rng.integers(37,45));states[q1:q2]=[b]*(q2-q1);states[q2:]=[a]*(T-q2)
 elif cond=='rapid_two_switch':
  q1=int(rng.integers(15,23));q2=q1+int(rng.integers(7,12));states[q1:q2]=[b]*(q2-q1);states[q2:]=[c]*(T-q2)
 # evidence: dual raw/chunk + grounded context abstraction, occasionally misleading
 obs=[]
 burst_start=int(rng.integers(20,35)) if cond=='false_burst' else -1
 for t,s in enumerate(states):
  e=rng.normal(0,.28,K); e[s]+=1.55
  if rng.random()<.07:
   w=(s+1+int(rng.integers(K-1)))%K;e[w]+=1.35;e[s]-=.55
  if cond=='false_burst' and burst_start<=t<burst_start+4:
   w=(a+1)%K;e[w]+=2.0;e[a]-=.75
  obs.append(e)
 return np.array(states),np.array(obs)

class Continuity:
 def __init__(self):self.cur=-1;self.score=np.zeros(K)
 def step(self,e):
  self.score=.90*self.score+e
  top=int(np.argmax(self.score))
  if self.cur<0:self.cur=top
  # sticky continuity
  if top!=self.cur and self.score[top]-self.score[self.cur]>3.0:self.cur=top
  return self.cur

class Temporal:
 def __init__(self,w,thr,streak,decay):self.w=w;self.thr=thr;self.req=streak;self.decay=decay;self.cur=-1;self.long=np.zeros(K);self.hist=[];self.streak=0;self.cand=-1;self.switches=0
 def step(self,e):
  self.long=self.decay*self.long+e;self.hist.append(e.copy());self.hist=self.hist[-self.w:]
  recent=np.sum(self.hist,axis=0); rt=int(np.argmax(recent)); order=np.argsort(recent)[::-1]; margin=recent[order[0]]-recent[order[1]]
  if self.cur<0:self.cur=rt;return self.cur
  # candidate change hypothesis competes with continuation; retain both until evidence persists
  if rt!=self.cur and margin>=self.thr:
   if self.cand==rt:self.streak+=1
   else:self.cand=rt;self.streak=1
   if self.streak>=self.req:self.cur=rt;self.switches+=1;self.streak=0;self.cand=-1;self.long=.35*self.long+recent
  else:
   self.streak=max(0,self.streak-1)
   if self.streak==0:self.cand=-1
  return self.cur

def score_params(seed,p,devN=70):
 r=np.random.default_rng(seed);acc=[];fs=[];delay=[]
 for _ in range(devN):
  cond=r.choice(CONDS);st,ob=make_stream(r,cond);m=Temporal(*p);pred=[]
  for e in ob:pred.append(m.step(e))
  pred=np.array(pred);acc.append(np.mean(pred==st))
  true_sw=np.sum(st[1:]!=st[:-1]);fs.append(max(0,m.switches-true_sw))
 return float(np.mean(acc)-.025*np.mean(fs))
def choose(seed):
 grid=list(itertools.product([3,4,5,6],[.7,1.0,1.3,1.6],[1,2,3],[.86,.92,.96]))
 vals=[score_params(seed,p,35) for p in grid];return grid[int(np.argmax(vals))]
def eval_seed(seed):
 p=choose(seed+99);r=np.random.default_rng(seed);out={'seed':seed,'chosen':p,'continuity':{},'temporal':{}}
 for cond in CONDS:
  rows={'continuity':[],'temporal':[]}
  for j in range(120):
   st,ob=make_stream(r,cond)
   for name,m in [('continuity',Continuity()),('temporal',Temporal(*p))]:
    pred=[]
    for e in ob:pred.append(m.step(e))
    pred=np.array(pred);true_sw=int(np.sum(st[1:]!=st[:-1]));sw=int(np.sum(pred[1:]!=pred[:-1]));
    # detection delay after each real switch
    delays=[]
    for t in np.where(st[1:]!=st[:-1])[0]+1:
     target=st[t];hits=np.where(pred[t:]==target)[0];delays.append(int(hits[0]) if len(hits) else len(st)-t)
    rows[name].append((np.mean(pred==st),max(0,sw-true_sw),np.mean(delays) if delays else 0,sw))
  for name in rows:
   a=np.array(rows[name]);out[name][cond]={'online_accuracy':float(a[:,0].mean()),'false_switches':float(a[:,1].mean()),'detection_delay':float(a[:,2].mean()),'switches':float(a[:,3].mean())}
 return out
def main():
 rows=[eval_seed(70000+i) for i in range(10)];agg={n:{} for n in ['continuity','temporal']}
 for n in agg:
  for c in CONDS:
   for m in ['online_accuracy','false_switches','detection_delay','switches']:agg[n][f'{c}_{m}']=float(np.mean([r[n][c][m] for r in rows]))
  agg[n]['mean_accuracy']=float(np.mean([agg[n][f'{c}_online_accuracy'] for c in CONDS]))
 out={'aggregate':agg,'rows':rows,'boundary':'REFERENCE_ONLY. Temporal change-hypothesis parameters selected on separate developmental streams using delayed online correctness/false-switch consequences. No test regime/switch labels enter runtime policy.'}
 (OUT/'R32_TEMPORAL_WORLDSTATE_REFERENCE_ONLY.json').write_text(json.dumps(out,indent=2));print(json.dumps(agg,indent=2))
if __name__=='__main__':main()
