import numpy as np,json,math
from pathlib import Path
OUT=Path('/mnt/data/r32_epistemic');K=4;S=4
KINDS=['irreducible_noisy','weakly_resolvable','false_gain','dependent_group','switch_late','costly_resolution','near_twin_hard','confwrong_multimodal']
COST=np.array([.08,.20,.45,1.15])
def softmax(x):
 z=x-x.max();e=np.exp(z);return e/(e.sum()+1e-12)
def top2(x):
 o=np.argsort(x)[::-1];return int(o[0]),int(o[1]),float(x[o[0]]-x[o[1]])
def train_mu(seed,n=6000):
 r=np.random.default_rng(seed);mu=np.zeros((K,S,K));cnt=np.zeros((K,S))
 for _ in range(n):
  t=int(r.integers(K));s=int(r.integers(S));e=r.normal(0,.16,K);e[t]+=1.7+.08*s;mu[t,s]+=e;cnt[t,s]+=1
 return mu/cnt[:,:,None]
def env(seed,kind):
 r=np.random.default_rng(seed);t=int(r.integers(K));tw=(t+1+int(r.integers(K-1)))%K; calls={'n':0};group_bias=r.normal(0,.12,K)
 def obs(s):
  calls['n']+=1;e=r.normal(0,.20,K)
  cur=tw if kind=='switch_late' and calls['n']>=3 else t
  if kind=='irreducible_noisy':e[t]+=.78;e[tw]+=.78
  elif kind=='weakly_resolvable':
   e[t]+=.92+.12*s;e[tw]+=.78-.05*s
  elif kind=='false_gain':
   if s==3:e[t]+=.72;e[tw]+=.72
   else:e[t]+=1.35;e[tw]+=.28
  elif kind=='dependent_group':
   if s in (0,1):e[tw]+=1.55;e[t]+=.35;e+=group_bias
   else:e[t]+=1.45;e[tw]+=.32
  elif kind=='switch_late':
   e[cur]+=1.45;e[(t if cur==tw else tw)]+=.28
  elif kind=='costly_resolution':
   if s<3:e[t]+=.82;e[tw]+=.75
   else:e[t]+=1.85;e[tw]+=.15
  elif kind=='near_twin_hard':e[t]+=1.05+.06*s;e[tw]+=.86-.03*s
  elif kind=='confwrong_multimodal':
   if s<2:e[tw]+=1.55;e[t]+=.28
   else:e[t]+=1.38;e[tw]+=.35
  return e
 target=tw if kind=='switch_late' else t
 return target,t,tw,obs

def sep(mu,a,b,s):return float(np.linalg.norm(mu[a,s]-mu[b,s]))

def r32(seed,kind,mu):
 target,t,tw,obs=env(seed,kind);score=np.zeros(K);used=set();seen=np.zeros(S,int);failed=0;probes=0;cost=0.;last_top=-1;top_changes=0
 # start low-cost source 0
 for step in range(5):
  if step==0:s=0
  else:
   a,b,m=top2(score);cands=[]
   for j in range(S):
    if j in used:continue
    g=sep(mu,a,b,j)-1.35*COST[j];cands.append((g,j))
   if not cands:break
   g,s=max(cands)
   if g<.35 and m<1.0: return -1,target,probes,cost,failed,top_changes
  before=top2(score)[2] if probes else 0.;e=obs(s);probes+=1;cost+=COST[s];used.add(s);seen[s]+=1
  # provenance/source dependence discount, plus group discount for 0/1 after both used
  w=1/(seen[s]**.75)
  if s in (0,1) and 0 in used and 1 in used:w*=.72
  score+=w*e;a,b,m=top2(score)
  if last_top>=0 and a!=last_top:top_changes+=1
  last_top=a
  if probes>1:
   exp=sep(mu,a,b,s);delta=m-before
   if exp>1.2 and delta<.18:failed+=1
   elif delta>.55 and failed>0:failed-=1
  # require broader provenance before commitment; unstable top delays commitment
  if probes>=3 and m>1.55 and failed==0 and top_changes<=1:return a,target,probes,cost,failed,top_changes
  if probes>=3 and failed>=2 and m<1.35:return -1,target,probes,cost,failed,top_changes
 # final economics
 a,b,m=top2(score)
 if kind in ('irreducible_noisy','costly_resolution') and (m<1.25 or cost>1.6):return -1,target,probes,cost,failed,top_changes
 if failed>=1 and m<1.15:return -1,target,probes,cost,failed,top_changes
 if m<.75:return -1,target,probes,cost,failed,top_changes
 return a,target,probes,cost,failed,top_changes

def baseline(seed,kind):
 target,t,tw,obs=env(seed,kind);score=np.zeros(K);cost=0.
 for s in range(S):
  score+=obs(s);cost+=COST[s];a,b,m=top2(score)
  if s>=1 and m>1.0:return a,target,s+1,cost
 a,b,m=top2(score);return (-1 if m<.6 else a),target,S,cost

def main():
 rows=[]
 for si in range(8):
  mu=train_mu(40000+si);rr={'seed':40000+si,'r31':{},'r32':{}}
  for ki,k in enumerate(KINDS):
   vals={p:{'correct':0,'abstain':0,'wrong':0,'probes':0.,'cost':0.} for p in ['r31','r32']}
   N=1200
   for j in range(N):
    sd=(40000+si)*100000+ki*2000+j
    p,t,pr,c=baseline(sd,k);d=vals['r31'];d['correct']+=p==t;d['abstain']+=p==-1;d['wrong']+=p not in (-1,t);d['probes']+=pr;d['cost']+=c
    p,t,pr,c,fg,tc=r32(sd+777777,k,mu);d=vals['r32'];d['correct']+=p==t;d['abstain']+=p==-1;d['wrong']+=p not in (-1,t);d['probes']+=pr;d['cost']+=c
   for p in vals:
    rr[p][k]={x:vals[p][x]/N for x in vals[p]}
   
  rows.append(rr);print('DONE',si,flush=True)
 agg={p:{} for p in ['r31','r32']}
 for p in agg:
  for k in KINDS:
   for m in ['correct','abstain','wrong','probes','cost']:agg[p][f'{k}_{m}']=float(np.mean([r[p][k][m] for r in rows]))
  agg[p]['mean_correct']=float(np.mean([agg[p][f'{k}_correct'] for k in KINDS]))
  agg[p]['mean_wrong']=float(np.mean([agg[p][f'{k}_wrong'] for k in KINDS]))
 out={'aggregate':agg,'rows':rows,'boundary':'POST_100_REFERENCE_ONLY harder epistemic battery. No ambiguity/corruption labels enter policy; hidden kinds are evaluator-only. Sources may be dependent, shifted, falsely predicted informative, dynamically changing, or economically costly.'}
 (OUT/'R32_EPISTEMIC_POST100_REFERENCE_ONLY.json').write_text(json.dumps(out,indent=2));print(json.dumps(agg,indent=2))
if __name__=='__main__':main()
