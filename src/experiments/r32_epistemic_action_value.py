from __future__ import annotations
import json, math, os
from pathlib import Path
from dataclasses import dataclass
from collections import defaultdict
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

OUT=Path('/mnt/data/r32_epistemic')
K=4; S=6
GROUP=np.array([0,0,1,2,3,4],int)
COST=np.array([.12,.12,.18,.28,.42,.72],float)
KINDS=['stable','misleading','dependent_group','irreducible','weak_resolve','false_gain','switch_late','costly_resolution','near_twin','confwrong_multi']
AMBIG={'irreducible'}


def softmax(x):
    z=x-np.max(x);e=np.exp(z);return e/(e.sum()+1e-12)
def entropy(p):return float(-(p*np.log(p+1e-12)).sum()/math.log(len(p)))
def top2(score):
    o=np.argsort(score)[::-1];return int(o[0]),int(o[1]),float(score[o[0]]-score[o[1]])

@dataclass
class Episode:
    kind:str; true:int; twin:int; obs:np.ndarray; future1:np.ndarray; future2:np.ndarray

def evidence_draw(rng,kind,true,twin,source,final_true):
    e=rng.normal(0,.09,K)
    if kind=='stable': e[final_true]+=2.0+.08*source;e[twin]+=.12
    elif kind=='misleading':
        if source==0:e[twin]+=2.2;e[final_true]+=.22
        else:e[final_true]+=1.85+.08*source;e[twin]+=.15
    elif kind=='dependent_group':
        if GROUP[source]==0:e[twin]+=2.05;e[final_true]+=.25
        else:e[final_true]+=1.85+.10*source;e[twin]+=.12
    elif kind=='irreducible':e[final_true]+=1.02;e[twin]+=1.02
    elif kind=='weak_resolve':
        if source<3:e[final_true]+=1.15;e[twin]+=.92
        else:e[final_true]+=1.45+.08*source;e[twin]+=.65
    elif kind=='false_gain':
        if source==3:e[final_true]+=1.05;e[twin]+=1.0
        elif source==4:e[final_true]+=2.15;e[twin]+=.12
        else:e[final_true]+=1.45;e[twin]+=.50
    elif kind=='switch_late':
        if source<2:e[true]+=2.0;e[final_true]+=.12
        else:e[final_true]+=2.05;e[true]+=.10
    elif kind=='costly_resolution':
        if source==5:e[final_true]+=2.45;e[twin]+=.05
        else:e[final_true]+=1.10;e[twin]+=.94
    elif kind=='near_twin':
        strengths=[.22,.28,.38,.55,.78,1.20];q=strengths[source];e[final_true]+=1.1+q;e[twin]+=1.1-q/2
    elif kind=='confwrong_multi':
        if source in (0,1,2):e[twin]+=2.0;e[final_true]+=.30
        elif source==3:e[twin]+=1.6;e[final_true]+=.55
        else:e[final_true]+=2.25;e[twin]+=.08
    return e

def make_episode(rng,kind=None):
    kind=kind or str(rng.choice(KINDS));true=int(rng.integers(K));twin=(true+1+int(rng.integers(K-1)))%K;final=twin if kind=='switch_late' else true
    obs=np.stack([evidence_draw(rng,kind,true,twin,s,final) for s in range(S)])
    f1=np.stack([evidence_draw(rng,kind,true,twin,s,final) for s in range(S)])
    f2=np.stack([evidence_draw(rng,kind,true,twin,s,final) for s in range(S)])
    return Episode(kind,final,twin,obs,f1,f2)

class State:
    def __init__(self):self.score=np.zeros(K);self.seen=np.zeros(S,bool);self.group_n=np.zeros(5,int);self.prev_p=np.ones(K)/K;self.failed_gain=0;self.probes=0;self.cost=0.
    def add(self,s,e):
        g=GROUP[s];w=1/(1+self.group_n[g]*.85);self.score+=w*e;self.group_n[g]+=1;self.seen[s]=True;self.probes+=1;self.cost+=COST[s]
    def features(self):
        p=softmax(self.score);ss=np.sort(p)[::-1];margin=ss[0]-ss[1];vol=float(np.mean(np.abs(p-self.prev_p)));self.prev_p=p.copy();groups=np.count_nonzero(self.group_n);dep=float(self.group_n.max()/(self.group_n.sum()+1e-9)) if self.probes else 1.
        base=[margin,1-entropy(p),ss[0],ss[:2].sum(),groups/5,1-dep,vol,self.failed_gain/3,self.probes/S,self.cost/2]
        return np.array(base+list(self.seen.astype(float))+list(np.minimum(self.group_n,3)/3),float)

def clone_state(st):
    z=State();z.score=st.score.copy();z.seen=st.seen.copy();z.group_n=st.group_n.copy();z.prev_p=st.prev_p.copy();z.failed_gain=st.failed_gain;z.probes=st.probes;z.cost=st.cost;return z

def suffix_outcome(st,ep,arr):
    z=clone_state(st)
    for s in range(S):
        if not z.seen[s]:z.add(s,arr[s])
    a,b,m=top2(z.score);return a,m

def delayed_targets(st,ep):
    a1,m1=suffix_outcome(st,ep,ep.future1);a2,m2=suffix_outcome(st,ep,ep.future2);now=top2(st.score)[0]
    resolvable=int(a1==a2 and min(m1,m2)>.42)
    commit_safe=int(resolvable and now==a1)
    return commit_safe,resolvable,a1 if resolvable else -1

def gain_features(st,source):
    return np.r_[st.features(),np.eye(S)[source],COST[source],st.group_n[GROUP[source]]/3]

def collect_training(seed,n=6500):
    rng=np.random.default_rng(seed);X=[];yc=[];yr=[];Xg=[];yg=[]
    for _ in range(n):
        ep=make_episode(rng);st=State();order=rng.permutation(S)
        for step,s in enumerate(order):
            # record before next evidence once at least one observation exists
            if st.probes:
                f=st.features();c,r,_=delayed_targets(st,ep);X.append(f);yc.append(c);yr.append(r)
                _,_,before=top2(st.score)
                for q in range(S):
                    if st.seen[q]:continue
                    z=clone_state(st);z.add(q,(ep.future1[q]+ep.future2[q])/2);_,_,after=top2(z.score);Xg.append(gain_features(st,q));yg.append(after-before)
            st.add(int(s),ep.obs[int(s)])
    return np.asarray(X),np.asarray(yc),np.asarray(yr),np.asarray(Xg),np.asarray(yg)

def train_models(seed):
    X,yc,yr,Xg,yg=collect_training(seed)
    common=dict(n_estimators=180,max_depth=11,min_samples_leaf=8,class_weight='balanced_subsample',n_jobs=1,random_state=seed)
    commit=RandomForestClassifier(**common).fit(X,yc);resolve=RandomForestClassifier(**common).fit(X,yr)
    gain=RandomForestRegressor(n_estimators=160,max_depth=11,min_samples_leaf=7,n_jobs=1,random_state=seed+1).fit(Xg,yg)
    return commit,resolve,gain,{'states':len(X),'gain_rows':len(Xg),'commit_rate':float(yc.mean()),'resolve_rate':float(yr.mean())}

def choose_source(st,gain):
    best=(-1e9,-1,0.)
    for s in range(S):
        if st.seen[s]:continue
        g=float(gain.predict(gain_features(st,s)[None,:])[0]);net=g-.22*COST[s]
        if net>best[0]:best=(net,s,g)
    return best

def run_learned(ep,models,params):
    commit,resolve,gain=models;ct,rt,gt,maxp=params;st=State();st.add(0,ep.obs[0])
    while True:
        f=st.features();pc=float(commit.predict_proba(f[None,:])[0,1]);pr=float(resolve.predict_proba(f[None,:])[0,1]);a,b,m=top2(st.score)
        if st.probes>=2 and pc>=ct:return a,st
        net,s,pred=choose_source(st,gain)
        if st.probes<maxp and s>=0 and net>=gt:
            before=m;st.add(s,ep.obs[s]);after=top2(st.score)[2]
            if pred>.28 and after-before<.08:st.failed_gain+=1
            elif after-before>.35 and st.failed_gain:st.failed_gain-=1
            continue
        if pr<rt:return -1,st
        if pc>=ct-.12:return a,st
        return -1,st

def run_fixed(ep,maxp=5):
    st=State();st.add(0,ep.obs[0])
    for s in [3,4,2,5,1]:
        a,b,m=top2(st.score)
        if st.probes>=2 and m>.80:return a,st
        if st.probes>=maxp:break
        st.add(s,ep.obs[s])
    a,b,m=top2(st.score);return (a if m>.42 else -1),st

def delayed_utility(pred,st,ep):
    _,res,final=delayed_targets(st,ep)
    if res:
        u=1 if pred==final else (-.45 if pred==-1 else -3)
    else:u=1 if pred==-1 else -1.2
    return u-.06*st.cost

def tune(models,seed):
    # Delayed utility selects stopping behavior; hidden scenario labels never enter.
    # Use a coarse search, then refine locally around the best region rather than
    # wasting most compute on nearly identical threshold tuples.
    rng=np.random.default_rng(seed);coarse_eps=[make_episode(rng) for _ in range(800)];grid=[]
    for ct in [.70,.82,.90]:
      for rt in [.30,.48,.64]:
       for gt in [-.02,.07,.14]:
        for mp in [3,4,5]:
         q=(ct,rt,gt,mp);u=np.mean([delayed_utility(*run_learned(e,models,q),e) for e in coarse_eps]);grid.append((u,q))
    _,b=max(grid,key=lambda x:x[0]);ref_eps=[make_episode(rng) for _ in range(1200)];ref=[]
    for dc in [-.05,0,.05]:
      for dr in [-.08,0,.08]:
       for dg in [-.05,0,.05]:
        for dm in [-1,0,1]:
         q=(float(np.clip(b[0]+dc,.55,.97)),float(np.clip(b[1]+dr,.15,.82)),float(np.clip(b[2]+dg,-.12,.25)),int(np.clip(b[3]+dm,2,7)))
         u=np.mean([delayed_utility(*run_learned(e,models,q),e) for e in ref_eps]);ref.append((u,q))
    return max(ref,key=lambda x:x[0])

def eval_policy(seed,models,params,n=900):
    rng=np.random.default_rng(seed);out={}
    for kind in KINDS:
        d=defaultdict(float)
        for _ in range(n):
            ep=make_episode(rng,kind);pred,st=run_learned(ep,models,params);d['probes']+=st.probes;d['cost']+=st.cost
            if kind in AMBIG:d['abstain']+=pred==-1;d['wrong']+=pred!=-1
            else:d['correct']+=pred==ep.true;d['abstain']+=pred==-1;d['wrong']+=pred not in (-1,ep.true)
        out[kind]={k:v/n for k,v in d.items()}
    return out

def eval_fixed(seed,n=900):
    rng=np.random.default_rng(seed);out={}
    for kind in KINDS:
        d=defaultdict(float)
        for _ in range(n):
            ep=make_episode(rng,kind);pred,st=run_fixed(ep);d['probes']+=st.probes;d['cost']+=st.cost
            if kind in AMBIG:d['abstain']+=pred==-1;d['wrong']+=pred!=-1
            else:d['correct']+=pred==ep.true;d['abstain']+=pred==-1;d['wrong']+=pred not in (-1,ep.true)
        out[kind]={k:v/n for k,v in d.items()}
    return out

def summarize(rows,key):
    kinds=KINDS;agg={}
    for k in kinds:
        mets=set().union(*(r[key][k].keys() for r in rows));agg[k]={m:float(np.mean([r[key][k].get(m,0) for r in rows])) for m in mets}
    resolv=[k for k in kinds if k not in AMBIG];agg['summary']={'resolvable_correct':float(np.mean([agg[k]['correct'] for k in resolv])),'resolvable_wrong':float(np.mean([agg[k]['wrong'] for k in resolv])),'ambiguity_abstain':float(np.mean([agg[k]['abstain'] for k in AMBIG])),'mean_probes':float(np.mean([agg[k]['probes'] for k in kinds])),'mean_cost':float(np.mean([agg[k]['cost'] for k in kinds]))}
    return agg

def main():
    rows=[]
    for i in range(6):
        seed=36000+i;commit,resolve,gain,meta=train_models(seed*10+1);best=tune((commit,resolve,gain),seed*10+2);learn=eval_policy(seed*100+3,(commit,resolve,gain),best[1]);fixed=eval_fixed(seed*100+3);row={'seed':seed,'training':meta,'chosen':best[1],'dev_utility':best[0],'learned':learn,'fixed':fixed};rows.append(row);print('DONE',seed,best,flush=True)
    out={'aggregate':{'learned':summarize(rows,'learned'),'fixed':summarize(rows,'fixed')},'rows':rows,'boundary':'REFERENCE_ONLY persistent non-graph epistemic action-value learner. Commit, expected future resolvability and source value are trained only from delayed independent evidence stability and grounded consequences. No ambiguity/corruption/world-state label is a learner feature or decision input. No transformer, tokenization, VAD, graph or LLM.'};(OUT/'R32_EPISTEMIC_ACTION_VALUE_REFERENCE_ONLY.json').write_text(json.dumps(out,indent=2));print(json.dumps(out['aggregate'],indent=2))
if __name__=='__main__':main()
