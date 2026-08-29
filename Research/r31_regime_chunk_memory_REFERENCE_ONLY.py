from __future__ import annotations
import json, random, math
from collections import Counter, defaultdict, deque
from pathlib import Path
import numpy as np
OUT=Path('/mnt/data/tnn-r31-endogenous-chunking/results'); OUT.mkdir(parents=True,exist_ok=True)
COMMON=(4,7,4,9); ALT=(8,5,8,6); NEW=(12,3,12,8,12); CTXA=(1,1); CTXB=(2,2); TAILS=[(5,6),(6,5),(10,11),(11,10)]

def make(rng,regime):
    ctx=CTXA if rng.random()<.5 else CTXB
    q=rng.random()
    if q<.22: core=NEW; y=2
    elif q<.47: core=ALT; y=1
    else:
        core=COMMON
        if regime==0: y=0
        elif regime==1: y=0 if ctx==CTXA else 1
        else: y=2 if ctx==CTXB else 0
    pre=tuple(rng.randrange(13,21) for _ in range(rng.randrange(0,3))); post=tuple(rng.randrange(13,21) for _ in range(rng.randrange(0,3)))
    return pre+ctx+core+rng.choice(TAILS)+post,y

class SpanModel:
    def __init__(self): self.stats=defaultdict(Counter)
    def observe(self,s,y):
        for n in range(2,min(9,len(s))+1):
            for i in range(len(s)-n+1): self.stats[tuple(s[i:i+n])][y]+=1
    def predict_scores(self,s):
        v=np.zeros(3,float)
        for n in range(2,min(9,len(s))+1):
            for i in range(len(s)-n+1):
                c=self.stats.get(tuple(s[i:i+n]));
                if not c: continue
                N=sum(c.values()); purity=max(c.values())/N
                if N<3 or purity<.58: continue
                wt=(purity-1/3)*math.log1p(N)*math.sqrt(n)
                for y,k in c.items(): v[y]+=wt*k/N
        return v
    def predict(self,s):
        v=self.predict_scores(s); return int(v.argmax()) if v.max()>0 else 0
    def confidence_true(self,s,y):
        v=self.predict_scores(s)
        if v.max()<=0:return .33
        z=np.exp(v-v.max());p=z/(z.sum()+1e-9);return float(p[y])

class Overwrite:
    def __init__(self): self.m=SpanModel()
    def step(self,s,y,learn=True):
        p=self.m.predict(s)
        if learn:self.m.observe(s,y)
        return p,0

class RegimeBank:
    # Multiple consequence memories over a shared raw-span/chunk substrate.
    # No phase label is supplied. New regimes are recruited only after sustained prediction failure.
    def __init__(self,max_regimes=4,spawn_window=10,spawn_err=.55,switch_evidence=2):
        self.models=[SpanModel()]; self.active=0; self.max_regimes=max_regimes
        self.err=deque(maxlen=spawn_window); self.spawn_err=spawn_err; self.switch_evidence=switch_evidence
        self.alt_votes=Counter(); self.spawned=0; self.switches=0
    def _pred_all(self,s): return [m.predict(s) for m in self.models]
    def step(self,s,y,learn=True):
        ps=self._pred_all(s); p=ps[self.active]; wrong=int(p!=y); self.err.append(wrong)
        # Evidence for an already learned alternate regime arrives from observed consequence, not a hidden regime id.
        for j,q in enumerate(ps):
            if j!=self.active and q==y and p!=y:self.alt_votes[j]+=1
            elif j!=self.active:self.alt_votes[j]=max(0,self.alt_votes[j]-1)
        candidates=[j for j,v in self.alt_votes.items() if v>=self.switch_evidence]
        if candidates:
            j=max(candidates,key=lambda x:self.alt_votes[x]); self.active=j; self.alt_votes.clear(); self.err.clear(); self.switches+=1
        elif len(self.err)==self.err.maxlen and sum(self.err)/len(self.err)>=self.spawn_err and len(self.models)<self.max_regimes:
            # Recruit a new consequence regime; old model is preserved exactly.
            nm=SpanModel(); self.models.append(nm); self.active=len(self.models)-1; self.err.clear(); self.alt_votes.clear(); self.spawned+=1
        if learn:self.models[self.active].observe(s,y)
        return p,self.active

def pretrain(obj,seed,n=2500):
    r=random.Random(seed)
    for _ in range(n): s,y=make(r,0); obj.step(s,y,True)

def stream(obj,seed,regime,n,learn=True):
    r=random.Random(seed);ok=0; by100=[]
    for i in range(n):
        s,y=make(r,regime);p,_=obj.step(s,y,learn);ok+=p==y
        if (i+1)%100==0:by100.append(ok/(i+1))
    return ok/n,by100

def eval_static(obj,seed,regime,n=1200):
    r=random.Random(seed);ok=0
    # do not update; for bank use current active regime only
    for _ in range(n):
        s,y=make(r,regime)
        if isinstance(obj,RegimeBank):p=obj.models[obj.active].predict(s)
        else:p=obj.m.predict(s)
        ok+=p==y
    return ok/n

def run(seed):
    out=[]
    for kind in ['overwrite','regime_bank']:
        o=Overwrite() if kind=='overwrite' else RegimeBank()
        pretrain(o,seed*10+1)
        a0=eval_static(o,seed*100+1,0)
        b_online,bcurve=stream(o,seed*100+2,1,10000,True)
        b_final=eval_static(o,seed*100+3,1)
        # World flips back to original regime. Consequence feedback remains ordinary experienced feedback.
        a_return,acurve=stream(o,seed*100+4,0,1200,True)
        a_final=eval_static(o,seed*100+5,0)
        # Then a third regime, to see whether this scales beyond a binary toggle.
        c_online,ccurve=stream(o,seed*100+6,2,3000,True)
        c_final=eval_static(o,seed*100+7,2)
        out.append(dict(seed=seed,kind=kind,a_initial=a0,b_online=b_online,b_final=b_final,a_return_online=a_return,a_return_final=a_final,c_online=c_online,c_final=c_final,
                        b_first100=bcurve[0],a_return_first100=acurve[0],c_first100=ccurve[0],
                        regimes=(len(o.models) if kind=='regime_bank' else 1),spawned=(o.spawned if kind=='regime_bank' else 0),switches=(o.switches if kind=='regime_bank' else 0)))
    return out

def main():
    rows=[]
    for s in range(7200,7212): rows+=run(s);print('DONE',s,flush=True)
    agg={}
    for k in ['overwrite','regime_bank']:
        rr=[x for x in rows if x['kind']==k]
        agg[k]={q:float(np.mean([x[q] for x in rr])) for q in ['a_initial','b_online','b_final','a_return_online','a_return_final','c_online','c_final','b_first100','a_return_first100','c_first100','regimes','spawned','switches']}
    payload={'rows':rows,'aggregate':agg,'boundary':'REFERENCE_ONLY. Regime identity is never supplied. Learner recruits/switches consequence memories from ordinary prediction errors and experienced outcomes; raw recurring spans are shared.'}
    (OUT/'regime_chunk_memory.json').write_text(json.dumps(payload,indent=2));print(json.dumps(agg,indent=2))
if __name__=='__main__':main()
