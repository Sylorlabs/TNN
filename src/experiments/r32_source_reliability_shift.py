from __future__ import annotations
import numpy as np, json
from pathlib import Path
OUT=Path('/mnt/data/r32_epistemic');K=5;S=4
CONDS=['stable','source_flip','source_swap','flip_return']

def rel_schedule(cond,t,T):
    a=np.array([.92,.82,.70,.60],float)
    if cond=='stable': return a
    if cond=='source_flip':
        if t>=T//2:a[0]=.18;a[3]=.91
    elif cond=='source_swap':
        if t>=T//3:a=np.array([.55,.35,.93,.72])
    elif cond=='flip_return':
        if T//3<=t<2*T//3:a[0]=.15;a[2]=.94
    return a

def make(r,cond,T=180):
    state=int(r.integers(K)); obs=[]
    for t in range(T):
        src=t%S; rel=rel_schedule(cond,t,T)[src]
        e=r.normal(0,.30,K);e[state]+=.42+1.30*rel
        if r.random()>(rel):
            w=(state+1+int(r.integers(K-1)))%K;e[w]+=1.65;e[state]-=.35
        obs.append((src,e,state))
    return obs

def norm(v):
    z=np.exp(v-v.max());return z/(z.sum()+1e-9)

class FixedTrust:
    def __init__(self):self.trust=np.array([.95,.85,.75,.65]);self.score=np.zeros(K)
    def step(self,src,e):
        self.score=.88*self.score+self.trust[src]*e;return int(np.argmax(self.score))

class Equal:
    def __init__(self):self.score=np.zeros(K)
    def step(self,src,e):self.score=.88*self.score+e;return int(np.argmax(self.score))

class Adaptive:
    def __init__(self):
        self.trust=np.ones(S)*.75;self.score=np.zeros(K);self.pending=[];self.t=0
    def step(self,src,e):
        self.t+=1
        self.score=.88*self.score+self.trust[src]*e; pred=int(np.argmax(self.score))
        self.pending.append((self.t,src,int(np.argmax(e))))
        # delayed independent evidence: compare old source claim to consensus of other-source
        # evidence accumulated later. No hidden source-reliability/state label is used.
        if len(self.pending)>10:
            tt,s,c=self.pending.pop(0)
            # current population estimate is discounted for the source being trained
            q=self.score-self.trust[s]*e*.15; consensus=int(np.argmax(q))
            reward=1 if c==consensus else -1
            self.trust[s]=float(np.clip(self.trust[s]+.035*reward,.08,1.25))
        return pred

def run(seed):
    r=np.random.default_rng(seed);out={'seed':seed}
    for cond in CONDS:
        out[cond]={}
        for name,ctor in [('equal',Equal),('fixed',FixedTrust),('adaptive',Adaptive)]:
            acc=[];recover=[];trusts=[]
            for rep in range(120):
                ob=make(r,cond);m=ctor();ok=[]
                for t,(s,e,y) in enumerate(ob):ok.append(m.step(s,e)==y)
                acc.append(np.mean(ok))
                if cond!='stable':
                    cp=90 if cond=='source_flip' else 60
                    if cond=='flip_return':cp=60
                    arr=np.asarray(ok[cp:]); # first run of 8/10 correct after source change
                    hit=len(arr)
                    for j in range(max(0,len(arr)-10)):
                        if arr[j:j+10].mean()>=.8:hit=j;break
                    recover.append(hit)
                if hasattr(m,'trust'):trusts.append(m.trust.copy())
            out[cond][name]={'accuracy':float(np.mean(acc)),'recovery':float(np.mean(recover)) if recover else 0.0,'final_trust':np.mean(trusts,axis=0).tolist() if trusts else None}
    return out

def main():
    rows=[run(97000+i) for i in range(10)];agg={}
    for c in CONDS:
        agg[c]={}
        for m in ['equal','fixed','adaptive']:
            agg[c][m]={'accuracy':float(np.mean([r[c][m]['accuracy'] for r in rows])),'recovery':float(np.mean([r[c][m]['recovery'] for r in rows]))}
    out={'aggregate':agg,'rows':rows,'boundary':'REFERENCE_ONLY dynamic source-trust challenge. Adaptive trust is revised only from delayed agreement with independently accumulated evidence; hidden source reliability and evaluator state are never learner inputs.'}
    (OUT/'R32_SOURCE_RELIABILITY_SHIFT_REFERENCE_ONLY.json').write_text(json.dumps(out,indent=2));print(json.dumps(agg,indent=2))
if __name__=='__main__':main()
