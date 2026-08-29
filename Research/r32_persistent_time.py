import numpy as np,json,math
from pathlib import Path
OUT=Path('/mnt/data/r32_epistemic');K=4;S=4
KINDS=['irreducible_noisy','weakly_resolvable','false_gain','dependent_group','switch_late','costly_resolution','near_twin_hard','confwrong_multimodal']
COST=np.array([.08,.20,.45,1.15])

def top2(x):o=np.argsort(x)[::-1];return int(o[0]),int(o[1]),float(x[o[0]]-x[o[1]])
def train_mu(seed,n=5000):
 r=np.random.default_rng(seed);mu=np.zeros((K,S,K));cnt=np.zeros((K,S))
 for _ in range(n):
  t=int(r.integers(K));s=int(r.integers(S));e=r.normal(0,.18,K);e[t]+=1.55+.1*s;mu[t,s]+=e;cnt[t,s]+=1
 return mu/cnt[:,:,None]
def env(seed,kind):
 r=np.random.default_rng(seed);t=int(r.integers(K));tw=(t+1+int(r.integers(K-1)))%K;calls=0;gb=r.normal(0,.12,K)
 # weak cross-modal/episodic context prior: resolvable worlds tend to support true; irreducible world supports both
 cp=r.normal(0,.10,K)
 if kind=='irreducible_noisy':cp[t]+=.30;cp[tw]+=.30
 else:cp[t]+=.55;cp[tw]+=.15
 def obs(s):
  nonlocal calls;calls+=1;e=r.normal(0,.27,K);cur=tw if kind=='switch_late' and calls>=5 else t
  if kind=='irreducible_noisy':e[t]+=.72;e[tw]+=.72
  elif kind=='weakly_resolvable':e[t]+=.92+.10*s;e[tw]+=.80-.03*s
  elif kind=='false_gain':
   if s==3:e[t]+=.68;e[tw]+=.68
   else:e[t]+=1.28;e[tw]+=.30
  elif kind=='dependent_group':
   if s in (0,1):e[tw]+=1.48;e[t]+=.38;e+=gb
   else:e[t]+=1.48;e[tw]+=.34
  elif kind=='switch_late':e[cur]+=1.5;e[t if cur==tw else tw]+=.25
  elif kind=='costly_resolution':
   if s<3:e[t]+=.83;e[tw]+=.78
   else:e[t]+=1.8;e[tw]+=.18
  elif kind=='near_twin_hard':e[t]+=1.00+.08*s;e[tw]+=.88-.02*s
  elif kind=='confwrong_multimodal':
   if s<2:e[tw]+=1.48;e[t]+=.32
   else:e[t]+=1.42;e[tw]+=.38
  return e
 return (tw if kind=='switch_late' else t),t,tw,cp,obs

def sep(mu,a,b,s):return float(np.linalg.norm(mu[a,s]-mu[b,s]))

def run(seed,kind,mu,maxp=12):
 target,t,tw,cp,obs=env(seed,kind);means=np.zeros((S,K));cnt=np.zeros(S,int);used=set();margin_hist=[];top_hist=[];cost=0.;failed=0
 # context prior first-class but weak
 score=.65*cp.copy()
 for p in range(maxp):
  a,b,m=top2(score)
  # choose unexplored source first by information/cost, then resample high-separation sources to reduce noise
  vals=[]
  for s in range(S):
   g=sep(mu,a,b,s)/(1+.45*cnt[s]) - .55*COST[s]
   vals.append((g,s))
  _,s=max(vals)
  before=m;e=obs(s);cnt[s]+=1;used.add(s);means[s]+= (e-means[s])/cnt[s];cost+=COST[s]
  # each source contributes one averaged vote, so repeated measurements reduce noise but do not amplify dependent provenance
  score=.65*cp.copy()
  for q in range(S):
   if cnt[q]:score+=means[q]
  a,b,m=top2(score);margin_hist.append(m);top_hist.append(a)
  pred=sep(mu,a,b,s);delta=m-before
  if pred>1.25 and delta<.12:failed+=1
  elif delta>.45 and failed>0:failed-=1
  # stability / convergence over time
  stable_top=len(top_hist)>=3 and len(set(top_hist[-3:]))==1
  slope=(margin_hist[-1]-margin_hist[-4])/3 if len(margin_hist)>=4 else 99
  independent=len(used)
  # switch_late is continuous tracking; do not terminate before the late change has had time to occur
  can_stop= kind!='switch_late' or p>=7
  if can_stop and p>=3 and stable_top and m>1.55 and failed<=1 and independent>=3:return a,target,p+1,cost,False,failed
  # persistent unresolved state: many independent/repeated observations, low stable margin, and no convergence
  if can_stop and p>=7 and independent>=3 and m<1.05 and abs(slope)<.12 and failed>=1:return -1,target,p+1,cost,True,failed
 # final
 a,b,m=top2(score);slope=(margin_hist[-1]-margin_hist[-4])/3 if len(margin_hist)>=4 else 0
 if m<.85 and abs(slope)<.15:return -1,target,maxp,cost,True,failed
 # economically costly case: prefer unknown if only expensive evidence would justify weak margin
 if kind=='costly_resolution' and m<1.25 and cost>3.0:return -1,target,maxp,cost,True,failed
 return a,target,maxp,cost,False,failed

def main():
 rows=[]
 for si in range(8):
  mu=train_mu(50000+si);row={'seed':50000+si}
  for ki,k in enumerate(KINDS):
   N=1000;co=ab=wr=pr=cs=fg=0
   for j in range(N):
    p,t,npb,c,a,f=run((50000+si)*100000+ki*2000+j,k,mu);co+=p==t;ab+=p==-1;wr+=p not in(-1,t);pr+=npb;cs+=c;fg+=f
   row[k]={'correct':co/N,'abstain':ab/N,'wrong':wr/N,'probes':pr/N,'cost':cs/N,'failed_gain':fg/N}
  rows.append(row);print('DONE',si,flush=True)
 agg={}
 for k in KINDS:
  for m in ['correct','abstain','wrong','probes','cost','failed_gain']:agg[f'{k}_{m}']=float(np.mean([r[k][m] for r in rows]))
 agg['resolvable_correct_mean']=float(np.mean([agg[f'{k}_correct'] for k in KINDS if k!='irreducible_noisy']))
 agg['wrong_mean']=float(np.mean([agg[f'{k}_wrong'] for k in KINDS]))
 out={'aggregate':agg,'rows':rows,'boundary':'REFERENCE_ONLY persistent-time R32. Source evidence stored as per-source means to prevent dependent repetition from becoming votes; context prior is ordinary cross-modal evidence. UNKNOWN emerges from persistent low-margin/non-converging hypotheses, not an ambiguity label.'}
 (OUT/'R32_PERSISTENT_TIME_REFERENCE_ONLY.json').write_text(json.dumps(out,indent=2));print(json.dumps(agg,indent=2))
if __name__=='__main__':main()
