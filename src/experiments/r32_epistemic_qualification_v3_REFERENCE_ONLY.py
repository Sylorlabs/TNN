from __future__ import annotations
import json, math, hashlib, os
from dataclasses import dataclass
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
os.environ.setdefault('OMP_NUM_THREADS','1'); os.environ.setdefault('MKL_NUM_THREADS','1'); os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import numpy as np
from sklearn.linear_model import LogisticRegression

OUT=Path('/mnt/data/r32_epistemic'); OUT.mkdir(parents=True,exist_ok=True)
K=3; S=6
GROUP=np.array([0,0,1,1,2,3],int)
MOD=np.array([0,0,1,1,2,3],int)
COST=np.array([.08,.08,.16,.16,.34,1.40],float)
KINDS=[
 'clean_stable','near_twin','confident_wrong_first','correlated_wrong_two',
 'independent_clean_correction','genuine_ambiguity','delayed_distinguishing',
 'entity_replacement','apparent_replacement_reverses','noisy_sibling_testimony',
 'repeated_same_lineage_social','sensory_channel_loss','cost_too_high'
]
ECONOMIC_UNKNOWN={'genuine_ambiguity','cost_too_high'}
MISLEADING={'confident_wrong_first','correlated_wrong_two','independent_clean_correction','noisy_sibling_testimony','repeated_same_lineage_social'}


def softmax(x):
 z=x-np.max(x); e=np.exp(z); return e/(e.sum()+1e-12)
def ent(p):
 return float(-(p*np.log(p+1e-12)).sum()/math.log(len(p)))
def top2(score):
 o=np.argsort(score)[::-1]; return int(o[0]),int(o[1]),float(score[o[0]]-score[o[1]])

def ev(rng, winner, twin, strength=1.8, twin_strength=.18, noise=.10):
 x=rng.normal(0,noise,K); x[winner]+=strength; x[twin]+=twin_strength; return x

def amb_ev(rng,a,b,strength=1.12,noise=.08):
 x=rng.normal(0,noise,K); x[a]+=strength; x[b]+=strength; return x

@dataclass
class Episode:
 kind:str; initial:int; final:int; twin:int; obs:np.ndarray; avail:np.ndarray; valid:tuple[int,...]


def make_episode(rng,kind=None):
 kind=kind or str(rng.choice(KINDS)); initial=int(rng.integers(K)); twin=(initial+1+int(rng.integers(K-1)))%K
 final=initial; obs=np.zeros((S,K)); avail=np.ones(S,bool); valid=(initial,)
 if kind=='clean_stable':
  for s in range(S): obs[s]=ev(rng,initial,twin,2.05+.08*s,.10,.09)
 elif kind=='near_twin':
  for s in range(S-1): obs[s]=ev(rng,initial,twin,.78+.10*s,.62,.11)
  obs[5]=ev(rng,initial,twin,2.55,.04,.07)
 elif kind=='confident_wrong_first':
  obs[0]=ev(rng,twin,initial,2.7,.12,.07)
  for s in range(1,S): obs[s]=ev(rng,initial,twin,2.05+.05*s,.15,.09)
 elif kind=='correlated_wrong_two':
  obs[0]=ev(rng,initial,twin,1.20,.72,.10); obs[1]=ev(rng,initial,twin,1.10,.78,.10)
  obs[2]=ev(rng,twin,initial,2.45,.10,.07); obs[3]=ev(rng,twin,initial,2.35,.12,.07)
  obs[4]=ev(rng,initial,twin,2.15,.12,.08); obs[5]=ev(rng,initial,twin,2.65,.04,.06)
 elif kind=='independent_clean_correction':
  obs[0]=ev(rng,twin,initial,2.35,.18,.08); obs[1]=ev(rng,twin,initial,1.85,.28,.10)
  obs[2]=ev(rng,initial,twin,1.25,.70,.11); obs[3]=ev(rng,initial,twin,1.35,.62,.11)
  obs[4]=ev(rng,initial,twin,2.25,.10,.08); obs[5]=ev(rng,initial,twin,2.65,.04,.06)
 elif kind=='genuine_ambiguity':
  for s in range(S): obs[s]=amb_ev(rng,initial,twin,1.10+.03*s,.07)
  valid=tuple(sorted((initial,twin)))
 elif kind=='delayed_distinguishing':
  for s in range(S-1): obs[s]=amb_ev(rng,initial,twin,1.05,.09)
  obs[5]=ev(rng,initial,twin,2.85,.02,.05)
 elif kind=='entity_replacement':
  final=twin; valid=(final,)
  obs[0]=ev(rng,initial,final,2.55,.08,.06); obs[1]=ev(rng,initial,final,2.15,.15,.08)
  obs[2]=ev(rng,final,initial,1.45,.50,.10); obs[3]=ev(rng,final,initial,1.65,.42,.10)
  obs[4]=ev(rng,final,initial,2.45,.08,.07); obs[5]=ev(rng,final,initial,2.85,.03,.05)
 elif kind=='apparent_replacement_reverses':
  obs[0]=ev(rng,initial,twin,2.25,.10,.07); obs[1]=ev(rng,initial,twin,1.95,.18,.08)
  obs[2]=ev(rng,twin,initial,2.25,.12,.07); obs[3]=ev(rng,twin,initial,1.95,.20,.09)
  obs[4]=ev(rng,initial,twin,2.40,.08,.07); obs[5]=ev(rng,initial,twin,2.75,.04,.05)
 elif kind=='noisy_sibling_testimony':
  obs[0]=ev(rng,initial,twin,1.15,.78,.13); obs[1]=ev(rng,initial,twin,1.20,.74,.13)
  obs[2]=ev(rng,twin,initial,1.65,.55,.18); obs[3]=ev(rng,initial,twin,1.45,.62,.18)
  obs[4]=ev(rng,initial,twin,2.05,.15,.09); obs[5]=ev(rng,initial,twin,2.55,.05,.07)
 elif kind=='repeated_same_lineage_social':
  obs[0]=ev(rng,initial,twin,1.05,.82,.12); obs[1]=ev(rng,initial,twin,1.10,.78,.12)
  obs[2]=ev(rng,twin,initial,2.55,.08,.06); obs[3]=ev(rng,twin,initial,2.50,.08,.06)
  obs[4]=ev(rng,initial,twin,2.15,.12,.08); obs[5]=ev(rng,initial,twin,2.65,.04,.06)
 elif kind=='sensory_channel_loss':
  avail[0]=avail[1]=False
  obs[2]=ev(rng,initial,twin,1.55,.46,.11); obs[3]=ev(rng,initial,twin,1.50,.48,.11)
  obs[4]=ev(rng,initial,twin,2.10,.12,.08); obs[5]=ev(rng,initial,twin,2.60,.05,.06)
 elif kind=='cost_too_high':
  for s in range(S-1): obs[s]=amb_ev(rng,initial,twin,1.08,.09)
  obs[5]=ev(rng,initial,twin,1.75,.35,.10)
 else: raise ValueError(kind)
 return Episode(kind,initial,final,twin,obs,avail,valid)

class State:
 def __init__(self,provenance=False,temporal=False):
  self.provenance=provenance; self.temporal=temporal; self.score=np.zeros(K); self.seen=np.zeros(S,bool); self.group_n=np.zeros(4,int); self.cost=0.; self.post=[]; self.ehist=[]; self.failed_gain=0
 def add(self,s,e):
  g=GROUP[s]; w=1.0/(1.0+.95*self.group_n[g]) if self.provenance else 1.0
  self.score += w*e; self.group_n[g]+=1; self.seen[s]=True; self.cost+=COST[s]; self.ehist.append((int(s),e.copy()))
  self.post.append(softmax(self.score.copy()))
 def recent_score(self):
  if not self.ehist:return self.score.copy()
  rs=np.zeros(K)
  for s,e in self.ehist[-3:]:
   g=GROUP[s]; same=sum(1 for q,_ in self.ehist[-3:] if GROUP[q]==g); w=1.0/(1+.6*max(0,same-1)) if self.provenance else 1.0
   rs+=w*e
  return rs
 def base_features(self,full=False):
  p=softmax(self.score); order=np.argsort(p)[::-1]; margin=float(p[order[0]]-p[order[1]])
  groups=int(np.count_nonzero(self.group_n)); dep=float(self.group_n.max()/(self.group_n.sum()+1e-9)) if self.group_n.sum() else 1.0
  vol=float(np.mean([np.mean(np.abs(self.post[i]-self.post[i-1])) for i in range(1,len(self.post))])) if len(self.post)>1 else 0.
  f=[margin,float(p[order[0]]),1-ent(p),ent(p),len(self.ehist)/S,groups/4,1-dep,self.cost/2.2,vol,self.failed_gain/3]
  f+=list(self.seen.astype(float)); f+=list(np.minimum(self.group_n,3)/3)
  if full:
   rp=softmax(self.recent_score()); ro=np.argsort(rp)[::-1]; rmargin=float(rp[ro[0]]-rp[ro[1]])
   glob=int(order[0]); recent=int(ro[0]); modtops=[]
   for m in range(4):
    z=np.zeros(K); anym=False
    for s,e in self.ehist:
     if MOD[s]==m:z+=e;anym=True
    if anym:modtops.append(int(np.argmax(z)))
   agree=(sum(x==glob for x in modtops)/len(modtops)) if modtops else 0.
   f += [rmargin,float(rp[ro[0]]),float(glob==recent),agree,float(len(set(modtops))) if modtops else 0.]
  return np.asarray(f,float)
 def candidate_features(self,cand,full=False):
  p=softmax(self.score); rp=softmax(self.recent_score()); b=self.base_features(full)
  return np.r_[b,p[cand],rp[cand] if full else p[cand],float(cand==np.argmax(p)),float(cand==np.argmax(rp)) if full else 1.0]


def initial_source(ep):
 for s in range(S):
  if ep.avail[s]:return s
 return -1

def candidate_set(st,full):
 p=softmax(st.score); o=list(np.argsort(p)[::-1][:2])
 if full:
  r=int(np.argmax(st.recent_score()))
  if r not in o:o.append(r)
 return [int(x) for x in o]

def delayed_unique(ep): return len(ep.valid)==1

def collect(seed,provenance,full,n=2200):
 rng=np.random.default_rng(seed); Xc=[];yc=[];Xr=[];yr=[]; src_gain=np.zeros(S);src_n=np.zeros(S);src_rel=np.zeros(S);rel_n=np.zeros(S)
 for _ in range(n):
  ep=make_episode(rng); st=State(provenance,full); order=[s for s in rng.permutation(S) if ep.avail[s]]
  for s in order:
   # labels are derived from delayed consequence equivalence (ep.valid), never kind name.
   if st.ehist:
    Xr.append(st.base_features(full));yr.append(int(delayed_unique(ep)))
    for cand in candidate_set(st,full):Xc.append(st.candidate_features(cand,full));yc.append(int(len(ep.valid)==1 and cand==ep.valid[0]))
    if len(ep.valid)==1:
     target=ep.valid[0];before=softmax(st.score)[target];z=State(provenance,full);z.score=st.score.copy();z.seen=st.seen.copy();z.group_n=st.group_n.copy();z.cost=st.cost;z.post=[x.copy() for x in st.post];z.ehist=[(q,e.copy()) for q,e in st.ehist];z.add(int(s),ep.obs[int(s)]);after=softmax(z.score)[target];src_gain[s]+=max(-.05,after-before);src_n[s]+=1
   if len(ep.valid)==1:
    src_rel[s]+=int(np.argmax(ep.obs[s])==ep.valid[0]);rel_n[s]+=1
   st.add(int(s),ep.obs[int(s)])
 Xc=np.asarray(Xc);yc=np.asarray(yc);Xr=np.asarray(Xr);yr=np.asarray(yr)
 cm=LogisticRegression(max_iter=260,class_weight='balanced',C=.8).fit(Xc,yc)
 rm=LogisticRegression(max_iter=260,class_weight='balanced',C=.8).fit(Xr,yr)
 gain=np.divide(src_gain,np.maximum(src_n,1)); rel=np.divide(src_rel,np.maximum(rel_n,1))
 return cm,rm,gain,rel,{'candidate_rows':len(yc),'resolve_rows':len(yr),'unique_rate':float(yr.mean()),'gain':gain.tolist(),'reliability':rel.tolist()}

def model_prob(cm,x):
 z=float(cm.intercept_[0]+np.dot(cm.coef_[0],x)); return 1.0/(1.0+math.exp(-max(-40.0,min(40.0,z))))

def best_candidate(st,cm,full):
 best=(-1.,-1)
 for c in candidate_set(st,full):
  pc=model_prob(cm,st.candidate_features(c,full))
  if pc>best[0]:best=(pc,c)
 return best

def choose_inspect(st,ep,gain,full,ordered=False):
 p=softmax(st.score); h=ent(p); avail=[s for s in range(S) if ep.avail[s] and not st.seen[s]]
 if not avail:return (-1,-1e9,0.)
 if ordered:
  s=avail[0];dep=(1/(1+.95*st.group_n[GROUP[s]])) if st.provenance else 1.;g=max(0.,gain[s])*h*dep;return s,4*g-COST[s],g
 best=(-1,-1e9,0.)
 for s in avail:
  dep=1/(1+.95*st.group_n[GROUP[s]])
  # unseen modalities and physical consequence probes carry independent value.
  modal_seen=any(MOD[q]==MOD[s] for q,_ in st.ehist);ind=1.15 if not modal_seen else .82
  g=max(0.,gain[s])*h*dep*ind
  net=4*g-COST[s]
  if net>best[1]:best=(s,net,g)
 return best

def run_policy(ep,models,route):
 provenance=route in ('C','D'); full=route=='D'; cm,rm,gain,rel,_=models
 st=State(provenance,full); s0=initial_source(ep); st.add(s0,ep.obs[s0])
 if route=='A':
  # R31-style bounded sequential stopping control: confidence thresholds + two grounded probes.
  p=softmax(st.score);m=np.sort(p)[-1]-np.sort(p)[-2]
  if m<.58:
   for s in [4,5]:
    if ep.avail[s] and not st.seen[s]:st.add(s,ep.obs[s]);p=softmax(st.score);m=np.sort(p)[-1]-np.sort(p)[-2]
    if m>=.46:break
  p=softmax(st.score);m=np.sort(p)[-1]-np.sort(p)[-2];pred=int(np.argmax(p));return (pred if m>=.27 else -1),st
 while True:
  pc,cand=best_candidate(st,cm,full); pr=model_prob(rm,st.base_features(full))
  u_commit=4*pc-3
  u_unknown=1-1.6*pr
  stop=max(u_commit,u_unknown)
  s,net,g=choose_inspect(st,ep,gain,full,ordered=(route in ('B','C')))
  if s>=0 and stop+net>stop and net>0:
   before=top2(st.score)[2];st.add(s,ep.obs[s]);after=top2(st.score)[2]
   if g>.08 and after-before<.025:st.failed_gain+=1
   elif after-before>.20 and st.failed_gain:st.failed_gain-=1
   continue
  return (cand if u_commit>=u_unknown else -1),st

def fit_routes(seed):
 # A shares the no-provenance learned source statistics only for comparable diagnostics; its stopping logic is fixed R31-style.
 B=collect(seed*10+1,False,False);C=collect(seed*10+2,True,False);D=collect(seed*10+3,True,True)
 return {'A':B,'B':B,'C':C,'D':D}

def eval_seed(seed,n=300):
 models=fit_routes(seed);rng=np.random.default_rng(seed*1000+17);out={r:{} for r in 'ABCD'}
 for kind in KINDS:
  episodes=[make_episode(rng,kind) for _ in range(n)]
  for route in 'ABCD':
   d=defaultdict(float);ents=[];unmass=[];ind=[]
   for ep in episodes:
    pred,st=run_policy(ep,models[route],route);unique=len(ep.valid)==1
    if unique:
     d['correct']+=pred==ep.valid[0];d['wrong_commit']+=pred not in(-1,ep.valid[0]);d['abstain']+=pred==-1
    else:
     d['ambiguity_abstain']+=pred==-1;d['wrong_commit']+=pred!=-1;d['abstain']+=pred==-1
    if kind=='cost_too_high':d['rational_cost_abstain']+=pred==-1
    if kind in MISLEADING:d['recovery']+=pred==ep.valid[0]
    if kind=='entity_replacement':d['switch_correct']+=pred==ep.valid[0];d['switch_delay']+=max(0,len(st.ehist)-2)
    if kind=='apparent_replacement_reverses':d['false_switch']+=pred==ep.twin
    d['cost']+=st.cost;d['sources']+=len(st.ehist);ind.append(np.count_nonzero(st.group_n));
    if st.post:ents.extend(ent(p) for p in st.post);p=st.post[-1];unmass.append(1-float(np.max(p)))
   dd={k:v/n for k,v in d.items()};dd['independent_sources']=float(np.mean(ind));dd['entropy_over_time']=float(np.mean(ents));dd['final_unresolved_mass']=float(np.mean(unmass));out[route][kind]=dd
 # summaries
 for route in 'ABCD':
  rr=out[route];res=[k for k in KINDS if k not in ECONOMIC_UNKNOWN]
  out[route]['summary']={
   'resolvable_correct':float(np.mean([rr[k].get('correct',0) for k in res])),
   'genuine_ambiguity_abstention':rr['genuine_ambiguity'].get('ambiguity_abstain',0),
   'wrong_commit':float(np.mean([rr[k].get('wrong_commit',0) for k in KINDS])),
   'unnecessary_abstention':float(np.mean([rr[k].get('abstain',0) for k in res])),
   'mean_cost':float(np.mean([rr[k].get('cost',0) for k in KINDS])),
   'independent_sources':float(np.mean([rr[k]['independent_sources'] for k in KINDS])),
   'misleading_recovery':float(np.mean([rr[k].get('recovery',0) for k in MISLEADING])),
   'switch_correct':rr['entity_replacement'].get('switch_correct',0),
   'switch_delay':rr['entity_replacement'].get('switch_delay',0),
   'false_switch':rr['apparent_replacement_reverses'].get('false_switch',0),
   'entropy_over_time':float(np.mean([rr[k]['entropy_over_time'] for k in KINDS])),
   'final_unresolved_mass':float(np.mean([rr[k]['final_unresolved_mass'] for k in KINDS])),
   'cost_rational_abstain':rr['cost_too_high'].get('rational_cost_abstain',0),
  }
 train={r:models[r][4] for r in 'BCD'}
 return {'seed':seed,'training':train,'routes':out}

def aggregate(rows):
 agg={}
 for route in 'ABCD':
  agg[route]={};keys=rows[0]['routes'][route]['summary'].keys()
  for k in keys:agg[route][k]=float(np.mean([x['routes'][route]['summary'][k] for x in rows]))
  agg[route]['conditions']={}
  for kind in KINDS:
   mets=set().union(*(x['routes'][route][kind].keys() for x in rows));agg[route]['conditions'][kind]={m:float(np.mean([x['routes'][route][kind].get(m,0) for x in rows])) for m in mets}
 return agg

def main():
 seeds=[36100+i for i in range(6)];rows=[]
 with ProcessPoolExecutor(max_workers=min(5,len(seeds))) as ex:
  fs={ex.submit(eval_seed,s):s for s in seeds}
  for f in as_completed(fs):
   s=fs[f];rows.append(f.result());print('DONE',s,flush=True)
 rows.sort(key=lambda x:x['seed']);agg=aggregate(rows)
 out={'experiment':'R32 epistemic qualification v3','routes':{
  'A':'R31-style bounded sequential stopping control','B':'persistent hypothesis population, no provenance discount','C':'persistent hypotheses + provenance dependence','D':'full epistemic: provenance + temporal/recent hypotheses + cross-modal state + learned expected information gain + physical consequence option + unresolved mass'},
  'seeds':seeds,'aggregate':agg,'rows':rows,
  'training_boundary':'REFERENCE_ONLY. Policy features never include condition/scenario/ambiguity labels. Commit and resolvability are learned from delayed consequence equivalence and regret; source values are learned from delayed probability improvement. Evaluator-only kind names are used only for stratified reporting. No graph cognition, transformer, tokenizer/BPE, next-token objective, supplied VAD, phoneme/word/chunk boundaries.',
  'claim_boundary':'Reference experiment only; cannot promote canonical TNN without native Zag reproduction.'}
 p=OUT/'R32_EPISTEMIC_QUALIFICATION_V3_REFERENCE_ONLY.json';p.write_text(json.dumps(out,indent=2));
 print(json.dumps({r:agg[r] for r in 'ABCD'},indent=2))
 print('SHA256',hashlib.sha256(p.read_bytes()).hexdigest())
if __name__=='__main__':main()
