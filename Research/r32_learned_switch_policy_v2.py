import numpy as np, json
from pathlib import Path
from sklearn.linear_model import LogisticRegression
OUT=Path('/mnt/data/r32_epistemic'); K=5; S=3
CONDS=['stable','single_switch','late_switch','switch_back','single_source_burst','rapid_two_switch']

def make(r,cond,T=90):
 a=int(r.integers(K)); b=(a+1+int(r.integers(K-1)))%K; c=(b+1+int(r.integers(K-1)))%K; st=np.array([a]*T)
 if cond=='single_switch': q=int(r.integers(22,38)); st[q:]=b
 elif cond=='late_switch': q=int(r.integers(60,72)); st[q:]=b
 elif cond=='switch_back': q1=int(r.integers(20,30)); q2=int(r.integers(55,68)); st[q1:q2]=b; st[q2:]=a
 elif cond=='rapid_two_switch': q1=int(r.integers(20,27)); q2=q1+int(r.integers(9,15)); st[q1:q2]=b; st[q2:]=c
 burst=int(r.integers(28,42)) if cond=='single_source_burst' else -1
 # source reliabilities are learnable latent properties, not state labels
 rel=np.array([.70,.84,.94])
 obs=[]
 for t,s in enumerate(st):
  src=t%S; e=r.normal(0,.28,K); e[s]+=1.48*rel[src]+.28
  if r.random()<(1-rel[src])*.18:
   w=(s+1+int(r.integers(K-1)))%K; e[w]+=1.15; e[s]-=.35
  if cond=='single_source_burst' and burst<=t<burst+12 and src==0:
   w=(a+1)%K; e[w]+=2.35; e[a]-=.9
  obs.append((src,e))
 return st,obs

def features(ring,cur):
 rs=np.sum([e for _,e in ring],0); o=np.argsort(rs)[::-1]; top=int(o[0]); run=int(o[1]); margin=float(rs[top]-rs[run])
 adv=[]; support=0
 for s in range(S):
  vv=[e for q,e in ring if q==s]
  if vv:
   v=np.mean(vv,0); a=max(0.,float(v[top]-v[cur])) if cur>=0 else max(0.,float(v[top]-v[run])); adv.append(a); support+=a>.2
 dom=max(adv)/(sum(adv)+1e-9) if adv else 1.0
 # disagreement/volatility across source-specific argmaxes
 tops=[]
 for s in range(S):
  vv=[e for q,e in ring if q==s]
  if vv: tops.append(int(np.argmax(np.mean(vv,0))))
 agree=(max([tops.count(x) for x in set(tops)]) / len(tops)) if tops else 0
 curgap=float(rs[top]-rs[cur]) if cur>=0 else margin
 return top,np.array([margin,dom,support/3.0,agree,curgap,len(ring)/6.0],float)

def future_consensus(ob, t, cand, cur=None, horizon=7):
    # Counterfactual delayed credit from future independent evidence: would future evidence
    # support switching to cand more than staying with cur? No hidden state label is used.
    z=ob[t+1:min(len(ob),t+1+horizon)]
    if len(z)<3 or cur is None:return None
    by=[]
    for src in range(S):
        vv=[e for q,e in z if q==src]
        if vv: by.append(np.mean(vv,axis=0))
    if len(by)<2:return None
    future=np.mean(by,axis=0)
    advantage=float(future[cand]-future[cur])
    # ignore genuinely unresolved development cases rather than manufacture a label
    if abs(advantage)<.08:return None
    return int(advantage>0)

def train(seed):
 r=np.random.default_rng(seed); X=[];Y=[]
 for _ in range(850):
  cond=CONDS[int(r.integers(len(CONDS)))]; st,ob=make(r,cond); cur=-1; ring=[]
  for t,(src,e) in enumerate(ob):
   ring.append((src,e.copy())); ring=ring[-6:]; top,x=features(ring,cur)
   if cur<0:cur=top; continue
   if top!=cur and x[0]>.35:
    y=future_consensus(ob,t,top,cur)
    if y is not None:X.append(x);Y.append(y)
   # development runtime uses conservative provisional update only to diversify states
   if top!=cur and x[0]>.9 and x[2]>=.66:cur=top
 if len(set(Y))<2:return None
 clf=LogisticRegression(C=.6,max_iter=500,class_weight='balanced').fit(np.array(X),np.array(Y))
 return clf, len(Y), float(np.mean(Y))

class Learned:
 def __init__(self,clf): self.clf=clf; self.cur=-1; self.ring=[]; self.sw=0
 def step(self,src,e):
  self.ring.append((src,e.copy())); self.ring=self.ring[-6:]; top,x=features(self.ring,self.cur)
  if self.cur<0:self.cur=top;return self.cur
  if top!=self.cur and x[0]>.38:
   p=float(self.clf.predict_proba(x[None])[0,1])
   # probability itself is learned; fixed 0.5 is simply classifier decision boundary
   if p>=.5:self.cur=top;self.sw+=1
  return self.cur
class Fast:
 def __init__(self):self.cur=-1;self.r=[];self.sw=0
 def step(self,s,e):
  self.r.append(e.copy());self.r=self.r[-3:];rs=np.sum(self.r,0);o=np.argsort(rs)[::-1];top=int(o[0]);m=rs[o[0]]-rs[o[1]]
  if self.cur<0:self.cur=top
  elif top!=self.cur and m>.8:self.cur=top;self.sw+=1
  return self.cur
class Prov:
 def __init__(self):self.cur=-1;self.r=[];self.sw=0
 def step(self,s,e):
  self.r.append((s,e.copy()));self.r=self.r[-4:];rs=np.sum([x for _,x in self.r],0);o=np.argsort(rs)[::-1];top=int(o[0]);m=rs[o[0]]-rs[o[1]]
  if self.cur<0:self.cur=top;return self.cur
  adv=[];sup=0
  for q in range(S):
   vv=[x for z,x in self.r if z==q]
   if vv:
    v=np.mean(vv,0);a=max(0.,float(v[top]-v[self.cur]));adv.append(a);sup+=a>.25
  dom=max(adv)/(sum(adv)+1e-9) if adv else 1
  if top!=self.cur and m>.78 and (dom<.72 or sup>=2):self.cur=top;self.sw+=1
  return self.cur

def eval_seed(seed):
 tr=train(seed*10+1); assert tr is not None;clf,n,pos=tr;r=np.random.default_rng(seed*10+2);out={'seed':seed,'train_n':n,'train_positive':pos,'coef':clf.coef_[0].tolist()}
 for name,ctor in [('fast',Fast),('prov',Prov),('learned',lambda:Learned(clf))]:
  out[name]={}
  for cond in CONDS:
   rows=[]
   for _ in range(220):
    st,ob=make(r,cond);m=ctor();pr=np.array([m.step(s,e) for s,e in ob]);true_sw=int(np.sum(st[1:]!=st[:-1]));pred_sw=int(np.sum(pr[1:]!=pr[:-1]));delays=[]
    for t in np.where(st[1:]!=st[:-1])[0]+1:
     hit=np.where(pr[t:]==st[t])[0];delays.append(int(hit[0]) if len(hit) else len(st)-t)
    rows.append((np.mean(pr==st),max(0,pred_sw-true_sw),np.mean(delays) if delays else 0,pred_sw))
   a=np.array(rows);out[name][cond]={'accuracy':float(a[:,0].mean()),'false_switches':float(a[:,1].mean()),'delay':float(a[:,2].mean()),'switches':float(a[:,3].mean())}
 return out

def main():
 rows=[eval_seed(96000+i) for i in range(10)];agg={n:{} for n in ['fast','prov','learned']}
 for n in agg:
  for c in CONDS:
   for m in ['accuracy','false_switches','delay','switches']:agg[n][f'{c}_{m}']=float(np.mean([r[n][c][m] for r in rows]))
  agg[n]['mean_accuracy']=float(np.mean([agg[n][f'{c}_accuracy'] for c in CONDS]))
  # utility penalizes false switching while keeping online correctness primary
  agg[n]['utility']=agg[n]['mean_accuracy']-.015*sum(agg[n][f'{c}_false_switches'] for c in CONDS)/len(CONDS)
 out={'aggregate':agg,'rows':rows,'boundary':'REFERENCE_ONLY. Learned switch policy uses only internal evidence features; training target is counterfactual future independent-source evidence advantage, never hidden world-state/switch labels. Evaluator truth is test-only.'}
 (OUT/'R32_LEARNED_SWITCH_POLICY_V2_REFERENCE_ONLY.json').write_text(json.dumps(out,indent=2));print(json.dumps(agg,indent=2))
if __name__=='__main__':main()
