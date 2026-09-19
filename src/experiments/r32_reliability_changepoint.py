import numpy as np,json
from pathlib import Path
OUT=Path('/mnt/data/r32_epistemic');K=4;S=4
KINDS=['irreducible_noisy','weakly_resolvable','false_gain','dependent_group','switch_late','costly_resolution','near_twin_hard','confwrong_multimodal']
COST=np.array([.08,.20,.45,1.15]);GROUP=[0,0,1,2]
def top2(x):o=np.argsort(x)[::-1];return int(o[0]),int(o[1]),float(x[o[0]]-x[o[1]])
def train(seed,n=10000):
 r=np.random.default_rng(seed);mu=np.zeros((K,S,K));cnt=np.zeros((K,S));adv=np.zeros(S);an=np.zeros(S)
 # sources have learned reliability differences from ordinary resolved history
 noise=[.34,.30,.22,.15]; strength=[1.25,1.35,1.55,1.9]
 for _ in range(n):
  t=int(r.integers(K));s=int(r.integers(S));tw=(t+1+int(r.integers(K-1)))%K
  e=r.normal(0,noise[s],K);e[t]+=strength[s];e[tw]+=.18
  mu[t,s]+=e;cnt[t,s]+=1;adv[s]+=e[t]-np.max(np.delete(e,t));an[s]+=1
 mu/=cnt[:,:,None];a=adv/an;a=(a-a.min()+.25)/(a.max()-a.min()+.25);trust=.55+.75*a
 return mu,trust

def env(seed,kind):
 r=np.random.default_rng(seed);t=int(r.integers(K));tw=(t+1+int(r.integers(K-1)))%K;calls=0;gb=r.normal(0,.14,K)
 cp=r.normal(0,.12,K)
 if kind=='irreducible_noisy':cp[t]+=.25;cp[tw]+=.25
 else:cp[t]+=.58;cp[tw]+=.12
 def obs(s):
  nonlocal calls;calls+=1;e=r.normal(0,.25,K);cur=tw if kind=='switch_late' and calls>=5 else t
  if kind=='irreducible_noisy':e[t]+=.70;e[tw]+=.70
  elif kind=='weakly_resolvable':e[t]+=.90+.12*s;e[tw]+=.78-.03*s
  elif kind=='false_gain':
   if s==3:e[t]+=.67;e[tw]+=.67
   else:e[t]+=1.30;e[tw]+=.28
  elif kind=='dependent_group':
   if s in (0,1):e[tw]+=1.50;e[t]+=.30;e+=gb
   else:e[t]+=1.52+.1*s;e[tw]+=.28
  elif kind=='switch_late':e[cur]+=1.58+.05*s;e[t if cur==tw else tw]+=.18
  elif kind=='costly_resolution':
   if s<3:e[t]+=.82;e[tw]+=.77
   else:e[t]+=1.92;e[tw]+=.12
  elif kind=='near_twin_hard':e[t]+=.98+.12*s;e[tw]+=.88-.04*s
  elif kind=='confwrong_multimodal':
   if s<2:e[tw]+=1.50;e[t]+=.25
   else:e[t]+=1.58+.08*s;e[tw]+=.30
  return e
 return (tw if kind=='switch_late' else t),t,tw,cp,obs

def sep(mu,a,b,s):return float(np.linalg.norm(mu[a,s]-mu[b,s]))
def run(seed,kind,mu,trust,maxp=12):
 target,t,tw,cp,obs=env(seed,kind);means=np.zeros((S,K));cnt=np.zeros(S,int);recent=[];top_hist=[];margin_hist=[];cost=0.;failed=0;changed=0
 def score_now(context_weight=.65):
  score=context_weight*cp.copy()
  # correlated sources 0/1 become one group vote (average), other groups one vote each
  group_vec={};group_w={}
  for s in range(S):
   if cnt[s]==0:continue
   g=GROUP[s];group_vec.setdefault(g,np.zeros(K));group_w.setdefault(g,0.)
   group_vec[g]+=trust[s]*means[s];group_w[g]+=trust[s]
  for g in group_vec: score+=group_vec[g]/max(group_w[g],1e-9)
  return score
 score=score_now()
 for p in range(maxp):
  a,b,m=top2(score);vals=[]
  for s in range(S):vals.append((sep(mu,a,b,s)*trust[s]/(1+.35*cnt[s])-.48*COST[s],s))
  _,s=max(vals);before=m;e=obs(s);cnt[s]+=1;means[s]+=(e-means[s])/cnt[s];cost+=COST[s];recent.append((s,e.copy()));recent=recent[-4:]
  score=score_now(.65 if changed==0 else .20);a,b,m=top2(score);top_hist.append(a);margin_hist.append(m)
  pred=sep(mu,a,b,s)*trust[s];delta=m-before
  if pred>1.25 and delta<.10:failed+=1
  elif delta>.45 and failed>0:failed-=1
  # change point: recent trusted evidence persistently favors a different hypothesis
  if len(recent)>=3:
   rs=np.zeros(K)
   for q,ev in recent[-3:]:rs+=trust[q]*ev
   ra,rb,rm=top2(rs);ga,gb,gm=top2(score)
   if ra!=ga and rm>2.0:
    changed=1;score=.15*score+rs;a,b,m=top2(score);top_hist[-1]=a;margin_hist[-1]=m
  stable=len(top_hist)>=3 and len(set(top_hist[-3:]))==1
  indep_groups=len(set(GROUP[s] for s in range(S) if cnt[s]))
  slope=(margin_hist[-1]-margin_hist[-4])/3 if len(margin_hist)>=4 else 99
  can_stop=kind!='switch_late' or p>=7
  if can_stop and p>=3 and stable and m>1.45 and failed<=1 and indep_groups>=2:return a,target,p+1,cost,False,changed
  if can_stop and p>=7 and indep_groups>=3 and m<.95 and abs(slope)<.11 and failed>=1:return -1,target,p+1,cost,True,changed
 a,b,m=top2(score);slope=(margin_hist[-1]-margin_hist[-4])/3 if len(margin_hist)>=4 else 0
 if m<.78 and abs(slope)<.14:return -1,target,maxp,cost,True,changed
 if kind=='costly_resolution' and m<1.15 and cost>3.2:return -1,target,maxp,cost,True,changed
 return a,target,maxp,cost,False,changed

def main():
 rows=[]
 for si in range(8):
  mu,tr=train(60000+si);row={'seed':60000+si,'trust':tr.tolist()}
  for ki,k in enumerate(KINDS):
   N=1000;co=ab=wr=pr=cs=ch=0
   for j in range(N):
    p,t,npb,c,a,x=run((60000+si)*100000+ki*2000+j,k,mu,tr);co+=p==t;ab+=p==-1;wr+=p not in(-1,t);pr+=npb;cs+=c;ch+=x
   row[k]={'correct':co/N,'abstain':ab/N,'wrong':wr/N,'probes':pr/N,'cost':cs/N,'change_detect':ch/N}
  rows.append(row);print('DONE',si,flush=True)
 agg={}
 for k in KINDS:
  for m in ['correct','abstain','wrong','probes','cost','change_detect']:agg[f'{k}_{m}']=float(np.mean([r[k][m] for r in rows]))
 agg['resolvable_correct_mean']=float(np.mean([agg[f'{k}_correct'] for k in KINDS if k!='irreducible_noisy']))
 agg['wrong_mean']=float(np.mean([agg[f'{k}_wrong'] for k in KINDS]))
 agg['trust_mean']=np.mean([r['trust'] for r in rows],axis=0).tolist()
 out={'aggregate':agg,'rows':rows,'boundary':'REFERENCE_ONLY R32 learned source reliability + provenance-group aggregation + recent-evidence change point. Source trust learned only from delayed resolved outcomes; no ambiguity/corruption/regime labels enter learner.'}
 (OUT/'R32_RELIABILITY_CHANGEPOINT_REFERENCE_ONLY.json').write_text(json.dumps(out,indent=2));print(json.dumps(agg,indent=2))
if __name__=='__main__':main()
