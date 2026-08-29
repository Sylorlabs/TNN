from __future__ import annotations
import numpy as np,json
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor,as_completed
from sklearn.linear_model import LogisticRegression
OUT=Path('/mnt/data/r32_epistemic');K=5;S=3
CONDS=['stable','single_switch','late_switch','switch_back','single_source_burst','rapid_two_switch']

def make(r,cond,T=90):
 a=int(r.integers(K)); b=(a+1+int(r.integers(K-1)))%K; c=(b+1+int(r.integers(K-1)))%K; st=np.array([a]*T)
 if cond=='single_switch':q=int(r.integers(22,38));st[q:]=b
 elif cond=='late_switch':q=int(r.integers(60,72));st[q:]=b
 elif cond=='switch_back':q1=int(r.integers(20,30));q2=int(r.integers(55,68));st[q1:q2]=b;st[q2:]=a
 elif cond=='rapid_two_switch':q1=int(r.integers(20,27));q2=q1+int(r.integers(9,15));st[q1:q2]=b;st[q2:]=c
 burst=int(r.integers(28,42)) if cond=='single_source_burst' else -1;rel=np.array([.70,.84,.94]);obs=[]
 for t,s in enumerate(st):
  src=t%S;e=r.normal(0,.28,K);e[s]+=1.48*rel[src]+.28
  if r.random()<(1-rel[src])*.18:
   w=(s+1+int(r.integers(K-1)))%K;e[w]+=1.15;e[s]-=.35
  if cond=='single_source_burst' and burst<=t<burst+12 and src==0:
   w=(a+1)%K;e[w]+=2.35;e[a]-=.9
  obs.append((src,e))
 return st,obs

def features(ring,cur):
 rs=np.sum([e for _,e in ring],0);o=np.argsort(rs)[::-1];top=int(o[0]);run=int(o[1]);margin=float(rs[top]-rs[run]);adv=[];support=0;tops=[]
 for s in range(S):
  vv=[e for q,e in ring if q==s]
  if vv:
   v=np.mean(vv,0);a=max(0.,float(v[top]-v[cur])) if cur>=0 else max(0.,float(v[top]-v[run]));adv.append(a);support+=a>.2;tops.append(int(np.argmax(v)))
 dom=max(adv)/(sum(adv)+1e-9) if adv else 1.;agree=max([tops.count(x) for x in set(tops)])/len(tops) if tops else 0.;curgap=float(rs[top]-rs[cur]) if cur>=0 else margin
 # interaction features remain generic evidence relationships, not hidden conditions
 return top,np.array([margin,dom,support/3.,agree,curgap,len(ring)/6.,margin*(1-dom),margin*agree,dom*(1-agree)],float)

def delayed_transient(ob,t,cand,cur,h=8):
 z=ob[t+1:min(len(ob),t+1+h)];by=[]
 for s in range(S):
  vv=[e for q,e in z if q==s]
  if vv:by.append(np.mean(vv,0))
 if len(by)<2:return None
 f=np.mean(by,0);adv=float(f[cand]-f[cur])
 if abs(adv)<.06:return None
 return int(adv<0) # 1 means caution/provenance should veto fast proposal

def train(seed):
 r=np.random.default_rng(seed);X=[];Y=[]
 for _ in range(2200):
  q=r.random();cond='single_source_burst' if q<.42 else ('stable' if q<.58 else CONDS[int(r.integers(1,len(CONDS)))])
  st,ob=make(r,cond);cur=-1;ring=[]
  if cond=='stable' and r.random()<.7:
   t0=int(r.integers(15,70));src0=int(r.integers(S));wrong=int(r.integers(K));dur=int(r.integers(3,9))
   for t in range(t0,min(len(ob),t0+dur)):
    src,e=ob[t]
    if src==src0:e=e.copy();e[wrong]+=float(r.uniform(1.4,2.6));ob[t]=(src,e)
  for t,(src,e) in enumerate(ob):
   ring.append((src,e.copy()));ring=ring[-6:];top,x=features(ring,cur)
   if cur<0:cur=top;continue
   if top!=cur and x[0]>.18:
    y=delayed_transient(ob,t,top,cur)
    if y is not None:X.append(x);Y.append(y)
   # neutral provisional development state update
   if top!=cur and x[0]>.9 and x[2]>=.66:cur=top
 X=np.asarray(X);Y=np.asarray(Y)
 # balance discovered transient vs persistent proposals without hidden labels
 i0=np.where(Y==0)[0];i1=np.where(Y==1)[0];m=min(len(i0),len(i1));sel=np.concatenate([r.choice(i0,m,False),r.choice(i1,m,False)]);r.shuffle(sel)
 clf=LogisticRegression(C=1.0,max_iter=700).fit(X[sel],Y[sel]);return clf,len(Y),float(Y.mean()),2*m

class Fast:
 def __init__(self):self.cur=-1;self.r=[];self.sw=0
 def propose(self,s,e):
  self.r.append((s,e.copy()));self.r=self.r[-4:];rs=np.sum([x for _,x in self.r[-3:]],0);o=np.argsort(rs)[::-1];return int(o[0]),float(rs[o[0]]-rs[o[1]])
 def step(self,s,e):
  top,m=self.propose(s,e)
  if self.cur<0:self.cur=top
  elif top!=self.cur and m>.8:self.cur=top;self.sw+=1
  return self.cur
class Prov:
 def __init__(self):self.cur=-1;self.r=[];self.sw=0
 def step(self,s,e):
  self.r.append((s,e.copy()));self.r=self.r[-4:];rs=np.sum([x for _,x in self.r],0);o=np.argsort(rs)[::-1];top=int(o[0]);m=float(rs[o[0]]-rs[o[1]])
  if self.cur<0:self.cur=top;return self.cur
  adv=[];sup=0
  for q in range(S):
   vv=[x for z,x in self.r if z==q]
   if vv:
    v=np.mean(vv,0);a=max(0.,float(v[top]-v[self.cur]));adv.append(a);sup+=a>.25
  dom=max(adv)/(sum(adv)+1e-9) if adv else 1
  if top!=self.cur and m>.78 and (dom<.72 or sup>=2):self.cur=top;self.sw+=1
  return self.cur
class Meta:
 def __init__(self,clf):self.clf=clf;self.cur=-1;self.r=[];self.sw=0
 def step(self,s,e):
  self.r.append((s,e.copy()));self.r=self.r[-6:];top,x=features(self.r,self.cur)
  if self.cur<0:self.cur=top;return self.cur
  if top==self.cur:return self.cur
  # fast candidate qualification
  if x[0]<=.8:return self.cur
  risk=float(self.clf.predict_proba(x[None])[0,1])
  if risk<.5: # use fast path
   self.cur=top;self.sw+=1;return self.cur
  # use provenance-veto path when learned transient risk is high
  adv=[];sup=0
  for q in range(S):
   vv=[z for src,z in self.r[-4:] if src==q]
   if vv:
    v=np.mean(vv,0);a=max(0.,float(v[top]-v[self.cur]));adv.append(a);sup+=a>.25
  dom=max(adv)/(sum(adv)+1e-9) if adv else 1
  if dom<.72 or sup>=2:self.cur=top;self.sw+=1
  return self.cur

def eval_seed(seed):
 clf,n,pos,bal=train(seed*10+1);r=np.random.default_rng(seed*10+2);out={'seed':seed,'train_n':n,'transient_rate':pos,'balanced_n':bal}
 for name,ctor in [('fast',Fast),('prov',Prov),('meta',lambda:Meta(clf))]:
  out[name]={}
  for cond in CONDS:
   a=[]
   for _ in range(220):
    st,ob=make(r,cond);m=ctor();pr=np.array([m.step(s,e) for s,e in ob]);true_sw=np.sum(st[1:]!=st[:-1]);pred_sw=np.sum(pr[1:]!=pr[:-1]);delays=[]
    for t in np.where(st[1:]!=st[:-1])[0]+1:
     hit=np.where(pr[t:]==st[t])[0];delays.append(int(hit[0]) if len(hit) else len(st)-t)
    a.append((np.mean(pr==st),max(0,pred_sw-true_sw),np.mean(delays) if delays else 0,pred_sw))
   a=np.asarray(a);out[name][cond]={'accuracy':float(a[:,0].mean()),'false_switches':float(a[:,1].mean()),'delay':float(a[:,2].mean()),'switches':float(a[:,3].mean())}
 return out

def main():
 rows=[]
 with ProcessPoolExecutor(max_workers=3) as ex:
  fs={ex.submit(eval_seed,98000+i):i for i in range(10)}
  for f in as_completed(fs):rows.append(f.result());print('DONE',fs[f],flush=True)
 rows.sort(key=lambda x:x['seed']);agg={n:{} for n in ['fast','prov','meta']}
 for n in agg:
  for c in CONDS:
   for m in ['accuracy','false_switches','delay','switches']:agg[n][f'{c}_{m}']=float(np.mean([r[n][c][m] for r in rows]))
  agg[n]['mean_accuracy']=float(np.mean([agg[n][f'{c}_accuracy'] for c in CONDS]));agg[n]['utility']=agg[n]['mean_accuracy']-.015*np.mean([agg[n][f'{c}_false_switches'] for c in CONDS])
 out={'aggregate':agg,'rows':rows,'boundary':'REFERENCE_ONLY. Meta-policy learns whether a provisional switch is transient from delayed independent evidence, then selects fast vs provenance-veto behavior. No hidden world state/switch label enters learner features or delayed target.'}
 (OUT/'R32_LEARNED_SWITCH_POLICY_V4_REFERENCE_ONLY.json').write_text(json.dumps(out,indent=2));print(json.dumps(agg,indent=2))
if __name__=='__main__':main()
