from __future__ import annotations
import numpy as np,json
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor,as_completed
from sklearn.linear_model import LogisticRegression
OUT=Path('/mnt/data/r32_epistemic');K=5;S=3;CONDS=['stable','single_switch','late_switch','switch_back','single_source_burst','rapid_two_switch'];COSTS=[.15,.5,1.5,3.0]

def make(r,cond,T=90):
 a=int(r.integers(K));b=(a+1+int(r.integers(K-1)))%K;c=(b+1+int(r.integers(K-1)))%K;st=np.array([a]*T)
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

def evidence(ring,cur):
 rs=np.sum([e for _,e in ring],0);o=np.argsort(rs)[::-1];top=int(o[0]);run=int(o[1]);margin=float(rs[top]-rs[run]);adv=[];sup=0;tops=[]
 for s in range(S):
  vv=[e for q,e in ring[-4:] if q==s]
  if vv:
   v=np.mean(vv,0);a=max(0.,float(v[top]-v[cur])) if cur>=0 else max(0.,float(v[top]-v[run]));adv.append(a);sup+=a>.25;tops.append(int(np.argmax(v)))
 dom=max(adv)/(sum(adv)+1e-9) if adv else 1.;agree=max([tops.count(x) for x in set(tops)])/len(tops) if tops else 0.;curgap=float(rs[top]-rs[cur]) if cur>=0 else margin
 return top,margin,dom,sup,agree,curgap

def future_adv(ob,t,cand,cur,h=8):
 z=ob[t+1:min(len(ob),t+1+h)];by=[]
 for s in range(S):
  vv=[e for q,e in z if q==s]
  if vv:by.append(np.mean(vv,0))
 if len(by)<2:return None
 f=np.mean(by,0);return float(f[cand]-f[cur])

def train(seed):
 r=np.random.default_rng(seed);X=[];Y=[]
 for _ in range(2000):
  q=r.random();cond='single_source_burst' if q<.38 else ('stable' if q<.50 else CONDS[int(r.integers(1,len(CONDS)))]);risk=float(r.choice(COSTS));st,ob=make(r,cond);cur=-1;ring=[]
  for t,(src,e) in enumerate(ob):
   ring.append((src,e.copy()));ring=ring[-6:];top,margin,dom,sup,agree,curgap=evidence(ring,cur)
   if cur<0:cur=top;continue
   fast=(top!=cur and margin>.8);prov=(top!=cur and margin>.78 and (dom<.72 or sup>=2))
   if fast!=prov:
    a=future_adv(ob,t,top,cur)
    if a is not None and abs(a)>.05:
     # Actual physical-error cost is represented by risk; delayed future evidence tells
     # whether the candidate persists. Target is policy utility, not hidden state label.
     uswitch=(a if a>0 else risk*a);ustay=(-.55*a if a>0 else .15*(-a));choose_prov=int((ustay if not prov else uswitch) > (uswitch if fast else ustay))
     x=np.array([margin,dom,sup/3.,agree,curgap,risk,margin*(1-dom),risk*dom,risk*(1-agree)],float);X.append(x);Y.append(choose_prov)
   if fast:cur=top
 X=np.asarray(X);Y=np.asarray(Y);i0=np.where(Y==0)[0];i1=np.where(Y==1)[0]
 if not len(i0) or not len(i1):raise RuntimeError('one-class')
 m=min(len(i0),len(i1));sel=np.concatenate([r.choice(i0,m,False),r.choice(i1,m,False)]);r.shuffle(sel);clf=LogisticRegression(C=1,max_iter=600).fit(X[sel],Y[sel]);return clf,len(Y),float(Y.mean()),2*m

class Policy:
 def __init__(self,mode,clf=None,risk=.5):self.mode=mode;self.clf=clf;self.risk=risk;self.cur=-1;self.r=[];self.sw=0
 def step(self,s,e):
  self.r.append((s,e.copy()));self.r=self.r[-6:];top,margin,dom,sup,agree,curgap=evidence(self.r,self.cur)
  if self.cur<0:self.cur=top;return self.cur
  fast=(top!=self.cur and margin>.8);prov=(top!=self.cur and margin>.78 and (dom<.72 or sup>=2))
  choose=fast
  if self.mode=='prov':choose=prov
  elif self.mode=='meta' and fast!=prov:
   x=np.array([margin,dom,sup/3.,agree,curgap,self.risk,margin*(1-dom),self.risk*dom,self.risk*(1-agree)],float);useprov=float(self.clf.predict_proba(x[None])[0,1])>=.5;choose=prov if useprov else fast
  if choose and top!=self.cur:self.cur=top;self.sw+=1
  return self.cur

def eval_seed(seed):
 clf,n,pos,bal=train(seed*10+1);r=np.random.default_rng(seed*10+2);out={'seed':seed,'train_n':n,'target_prov_rate':pos,'balanced_n':bal}
 for mode in ['fast','prov','meta']:
  out[mode]={}
  for risk in COSTS:
   rows=[]
   for cond in CONDS:
    for _ in range(100):
     st,ob=make(r,cond);m=Policy(mode,clf,risk);pr=np.array([m.step(s,e) for s,e in ob]);true_sw=int(np.sum(st[1:]!=st[:-1]));pred_sw=int(np.sum(pr[1:]!=pr[:-1]));false=max(0,pred_sw-true_sw);delays=[]
     for t in np.where(st[1:]!=st[:-1])[0]+1:
      hit=np.where(pr[t:]==st[t])[0];delays.append(int(hit[0]) if len(hit) else len(st)-t)
     acc=float(np.mean(pr==st));delay=float(np.mean(delays) if delays else 0);util=acc-risk*false/len(st)-.08*delay/len(st);rows.append((acc,false,delay,util))
   a=np.asarray(rows);out[mode][str(risk)]={'accuracy':float(a[:,0].mean()),'false_switches':float(a[:,1].mean()),'delay':float(a[:,2].mean()),'utility':float(a[:,3].mean())}
 return out

def main():
 rows=[]
 with ProcessPoolExecutor(max_workers=2) as ex:
  fs={ex.submit(eval_seed,99000+i):i for i in range(8)}
  for f in as_completed(fs):rows.append(f.result());print('DONE',fs[f],flush=True)
 rows.sort(key=lambda x:x['seed']);agg={m:{} for m in ['fast','prov','meta']}
 for m in agg:
  for risk in COSTS:
   agg[m][str(risk)]={k:float(np.mean([r[m][str(risk)][k] for r in rows])) for k in ['accuracy','false_switches','delay','utility']}
  agg[m]['mean_utility']=float(np.mean([agg[m][str(r)]['utility'] for r in COSTS]))
 out={'aggregate':agg,'rows':rows,'boundary':'REFERENCE_ONLY risk-sensitive switch-policy experiment. Observable downstream error cost and delayed independent evidence train a meta-policy choosing fast vs provenance-veto behavior; hidden world-state/switch labels are evaluator-only.'};(OUT/'R32_LEARNED_SWITCH_POLICY_V5_RISK_REFERENCE_ONLY.json').write_text(json.dumps(out,indent=2));print(json.dumps(agg,indent=2))
if __name__=='__main__':main()
