import numpy as np,json
from pathlib import Path
OUT=Path('/mnt/data/r32_epistemic');K=5;S=3
CONDS=['stable','single_switch','late_switch','switch_back','single_source_burst','rapid_two_switch']
def make(r,cond,T=75):
 a=int(r.integers(K));b=(a+1+int(r.integers(K-1)))%K;c=(b+1+int(r.integers(K-1)))%K;st=[a]*T
 if cond=='single_switch':q=int(r.integers(20,35));st[q:]=[b]*(T-q)
 elif cond=='late_switch':q=int(r.integers(52,62));st[q:]=[b]*(T-q)
 elif cond=='switch_back':q1=int(r.integers(18,27));q2=int(r.integers(46,57));st[q1:q2]=[b]*(q2-q1);st[q2:]=[a]*(T-q2)
 elif cond=='rapid_two_switch':q1=int(r.integers(18,25));q2=q1+int(r.integers(9,14));st[q1:q2]=[b]*(q2-q1);st[q2:]=[c]*(T-q2)
 burst=int(r.integers(24,36)) if cond=='single_source_burst' else -1
 obs=[]
 for t,s in enumerate(st):
  src=t%S;e=r.normal(0,.25,K);e[s]+=1.55
  if r.random()<.05:
   w=(s+1+int(r.integers(K-1)))%K;e[w]+=1.25;e[s]-=.45
  if cond=='single_source_burst' and burst<=t<burst+12 and src==0:
   w=(a+1)%K;e[w]+=2.2;e[a]-=.85
  obs.append((src,e))
 return np.array(st),obs
class Fast:
 def __init__(self):self.cur=-1;self.hist=[];self.cand=-1;self.streak=0;self.sw=0
 def step(self,src,e):
  self.hist.append(e);self.hist=self.hist[-3:];rs=np.sum(self.hist,0);o=np.argsort(rs)[::-1];top=int(o[0]);m=rs[o[0]]-rs[o[1]]
  if self.cur<0:self.cur=top;return self.cur
  if top!=self.cur and m>.8:
   if self.cand==top:self.streak+=1
   else:self.cand=top;self.streak=1
   if self.streak>=1:self.cur=top;self.sw+=1;self.streak=0;self.cand=-1
  else:self.streak=0;self.cand=-1
  return self.cur
class Prov:
 def __init__(self):self.cur=-1;self.ring=[];self.cand=-1;self.streak=0;self.sw=0
 def step(self,src,e):
  self.ring.append((src,e.copy()));self.ring=self.ring[-9:]
  # each provenance source gets one averaged vote in recent evidence
  by={}
  for s,x in self.ring:by.setdefault(s,[]).append(x)
  votes={s:np.mean(v,0) for s,v in by.items()};rs=sum(votes.values(),np.zeros(K));o=np.argsort(rs)[::-1];top=int(o[0]);m=rs[o[0]]-rs[o[1]]
  if self.cur<0:self.cur=top;return self.cur
  # count independent source support for candidate over current
  support=sum(1 for v in votes.values() if v[top]-v[self.cur]>.35)
  if top!=self.cur and m>.85 and support>=2:
   if self.cand==top:self.streak+=1
   else:self.cand=top;self.streak=1
   if self.streak>=2:self.cur=top;self.sw+=1;self.streak=0;self.cand=-1
  else:self.streak=max(0,self.streak-1)
  return self.cur
def run(seed):
 r=np.random.default_rng(seed);out={'seed':seed,'fast':{},'prov':{}}
 for cond in CONDS:
  data={'fast':[],'prov':[]}
  for _ in range(180):
   st,ob=make(r,cond)
   for n,m in [('fast',Fast()),('prov',Prov())]:
    pr=np.array([m.step(s,e) for s,e in ob]);ts=np.sum(st[1:]!=st[:-1]);ps=np.sum(pr[1:]!=pr[:-1]);ds=[]
    for t in np.where(st[1:]!=st[:-1])[0]+1:
     h=np.where(pr[t:]==st[t])[0];ds.append(int(h[0]) if len(h) else len(st)-t)
    data[n].append((np.mean(pr==st),max(0,ps-ts),np.mean(ds) if ds else 0,ps))
  for n in data:
   a=np.array(data[n]);out[n][cond]={'accuracy':float(a[:,0].mean()),'false_switches':float(a[:,1].mean()),'delay':float(a[:,2].mean()),'switches':float(a[:,3].mean())}
 return out
def main():
 rows=[run(90000+i) for i in range(10)];agg={n:{} for n in ['fast','prov']}
 for n in agg:
  for c in CONDS:
   for m in ['accuracy','false_switches','delay','switches']:agg[n][f'{c}_{m}']=float(np.mean([r[n][c][m] for r in rows]))
  agg[n]['mean_accuracy']=float(np.mean([agg[n][f'{c}_accuracy'] for c in CONDS]))
 out={'aggregate':agg,'rows':rows,'boundary':'REFERENCE_ONLY. Temporal change candidate requires corroboration from independent observable evidence sources; source IDs are provenance channels, not evaluator state labels.'};(OUT/'R32_TEMPORAL_PROVENANCE_REFERENCE_ONLY.json').write_text(json.dumps(out,indent=2));print(json.dumps(agg,indent=2))
if __name__=='__main__':main()
