from __future__ import annotations
import json, math, random, statistics
from collections import Counter, defaultdict, deque
from pathlib import Path
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans

OUT=Path('/mnt/data/r31_part2')

# ----------------------------- self-chunk acoustic world -----------------------------
class AcousticWorld:
    def __init__(self, seed:int, entities=8, alphabet=32):
        self.rng=np.random.default_rng(seed); self.entities=entities; self.alphabet=alphabet
        # Each entity has 3 recurring spans. Near-twin pairs share two spans and differ in one.
        self.spans=[]
        for e in range(entities):
            pair=e//2
            shared1=tuple(int(x) for x in self.rng.integers(0,alphabet,5)) if e%2==0 else self.spans[e-1][0]
            shared2=tuple(int(x) for x in self.rng.integers(0,alphabet,4)) if e%2==0 else self.spans[e-1][1]
            unique=tuple(int(x) for x in self.rng.integers(0,alphabet,6))
            self.spans.append((shared1,shared2,unique))
        self.effect=np.array([(e*3+1)%5 for e in range(entities)])
    def episode(self,e:int,rng:np.random.Generator,cond='matched'):
        s1,s2,u=self.spans[e]
        order=[s1,s2,u] if rng.random()<.5 else [u,s1,s2]
        seq=[]
        for span in order:
            seq.extend(span)
            if cond=='silence_shift' and rng.random()<.8: seq.extend([31]*int(rng.integers(1,4)))
            elif cond=='matched' and rng.random()<.18: seq.append(31)
        # speaker transform = stable symbol permutation subset + occasional local jitter
        if cond in ('speaker_shift','hard_noise','near_twin','confwrong','onset_damage','novel'):
            shift=int(rng.integers(1,5)) if cond=='speaker_shift' else 0
            if shift: seq=[(x+shift)%31 if x!=31 else 31 for x in seq]
        if cond=='no_gap': seq=[x for x in seq if x!=31]
        if cond=='hard_noise':
            for i in range(len(seq)):
                if rng.random()<.16: seq[i]=int(rng.integers(0,31))
        if cond=='onset_damage': seq=seq[int(rng.integers(2,6)):]
        if cond=='near_twin':
            # Replace unique region with a partial mix from its twin, but not all evidence.
            twin=e^1; tu=self.spans[twin][2]
            pos=max(0,len(seq)-len(u)); seq[pos:pos+len(tu)]=list(tu)
            for i in range(len(seq)):
                if rng.random()<.05: seq[i]=int(rng.integers(0,31))
        if cond=='confwrong':
            # Strongly misleading first observation: acoustic body from twin.
            twin=e^1
            return self.episode(twin,rng,'hard_noise')[0], int(self.effect[e])
        if cond=='novel':
            rng.shuffle(seq)
        return tuple(seq), int(self.effect[e])
    def ambiguous(self,e:int,rng):
        twin=e^1
        a=list(self.episode(e,rng,'hard_noise')[0]); b=list(self.episode(twin,rng,'hard_noise')[0])
        m=min(len(a),len(b)); cut=m//2
        return tuple(a[:cut]+b[cut:]), -1

class ChunkBank:
    def __init__(self,max_span=8,min_seen=5,max_chunks=700):
        self.max_span=max_span; self.min_seen=min_seen; self.max_chunks=max_chunks
        self.stats=defaultdict(lambda: [0,Counter()]); self.chunks=[]; self.cset=set()
    def observe(self,s,ground):
        n=len(s)
        for L in range(2,min(self.max_span,n)+1):
            for i in range(n-L+1):
                sp=s[i:i+L]; z=self.stats[sp]; z[0]+=1; z[1][ground]+=1
    def promote(self):
        cand=[]
        for sp,(seen,c) in self.stats.items():
            if seen<self.min_seen: continue
            N=sum(c.values()); purity=max(c.values())/N if N else 0
            gain=(len(sp)-1)*seen-(len(sp)+3)
            # compression is admissible but cannot dominate grounding; impose purity evidence.
            utility=gain*0.02 + max(0,purity-.2)*math.log1p(seen)*len(sp)
            if purity>=.34 and utility>0: cand.append((utility,len(sp),seen,sp))
        cand.sort(reverse=True)
        for _,_,_,sp in cand:
            if sp not in self.cset:
                self.cset.add(sp); self.chunks.append(sp)
                if len(self.chunks)>=self.max_chunks: break
        self.chunks.sort(key=len,reverse=True)
    def segment(self,s):
        out=[]; i=0
        while i<len(s):
            found=None
            for sp in self.chunks:
                L=len(sp)
                if i+L<=len(s) and s[i:i+L]==sp: found=sp; break
            if found is None: out.append(('lit',s[i])); i+=1
            else: out.append(('c',found)); i+=len(found)
        return out
    @staticmethod
    def signature(span):
        h=np.zeros(32); t=np.zeros(32)
        for i,x in enumerate(span):
            h[x%32]+=1
            if i: t[(span[i-1]*31+x*17)%32]+=1
        z=np.concatenate([h,t]);
        return z/(np.linalg.norm(z)+1e-9)
    def features(self,s,route):
        seg=self.segment(s); f=np.zeros(256)
        # Hash learner-created chunks/literals into a stable associative feature bank.
        for typ,v in seg:
            if typ=='c': key=hash(v)%128; f[key]+=1.0
            else: f[128+(v%32)]+=.35
        if route in ('rich','dual','active'):
            # intrinsic stream microstructure, not evaluator boundary labels
            sig=self.signature(s); f[160:224]+=sig
        if route in ('dual','active'):
            # high-fidelity microstate bypass
            for i,x in enumerate(s): f[224+(x%32)]+=0.12
        return f

class GroundLearner:
    def __init__(self,bank,route): self.bank=bank; self.route=route; self.clf=None
    def fit(self,episodes):
        for s,y in episodes:self.bank.observe(s,y)
        self.bank.promote()
        X=np.stack([self.bank.features(s,self.route) for s,y in episodes]); y=np.array([y for s,y in episodes])
        self.clf=LogisticRegression(max_iter=500,C=2.0).fit(X,y)
    def probs(self,s): return self.clf.predict_proba(self.bank.features(s,self.route).reshape(1,-1))[0]
    def pred(self,s):
        p=self.probs(s); return int(self.clf.classes_[int(np.argmax(p))]), float(np.max(p)), float(np.partition(p,-2)[-1]-np.partition(p,-2)[-2])

class Reliability:
    # Learns whether first internal decision will survive later independent evidence.
    def __init__(self): self.clf=LogisticRegression(max_iter=300,class_weight='balanced')
    def fit(self,rows):
        X=[];y=[]
        for margin,conf,disagree,length,correct in rows:X.append([margin,conf,disagree,length/40]);y.append(correct)
        self.clf.fit(X,y)
    def score(self,margin,conf,disagree,length): return float(self.clf.predict_proba([[margin,conf,disagree,length/40]])[0,1])

def run_acoustic(seed):
    w=AcousticWorld(seed); rng=np.random.default_rng(seed+99)
    train=[]
    for _ in range(10000):
        e=int(rng.integers(0,w.entities)); train.append(w.episode(e,rng,'matched'))
    routes={}
    for route in ['opaque','rich','dual','active']:
        bank=ChunkBank(); L=GroundLearner(bank,'dual' if route=='active' else route); L.fit(train); routes[route]=L
    # reliability training uses eventual correctness and disagreement across chunk/raw routes; no corruption labels.
    relrows=[]
    for _ in range(5000):
        e=int(rng.integers(0,w.entities)); cond=rng.choice(['matched','hard_noise','near_twin','confwrong','speaker_shift'])
        s,y=w.episode(e,rng,cond); pa,ca,ma=routes['dual'].pred(s); pr,cr,mr=routes['rich'].pred(s)
        relrows.append((ma,ca,float(pa!=pr),len(s),int(pa==y)))
    R=Reliability(); R.fit(relrows)
    conds=['matched','speaker_shift','no_gap','silence_shift','hard_noise','onset_damage','near_twin','confwrong','novel']
    out={r:{} for r in routes}
    for route,L in routes.items():
        for cond in conds:
            ok=0;N=1200
            for _ in range(N):
                e=int(rng.integers(0,w.entities));s,y=w.episode(e,rng,cond);p,cf,mg=L.pred(s)
                if route=='active':
                    pr,_,_=routes['rich'].pred(s); rv=R.score(mg,cf,float(p!=pr),len(s))
                    if rv<.68:
                        s2,_=w.episode(e,rng,'hard_noise' if cond!='matched' else 'matched'); q1=L.probs(s);q2=L.probs(s2); cls=L.clf.classes_;p=int(cls[int(np.argmax(q1+q2))])
                ok+=p==y
            out[route][cond]=ok/N
        # ambiguous: correct action is abstention if max confidence / reliability insufficient
        abst=0;N=1200
        for _ in range(N):
            e=int(rng.integers(0,w.entities));s,_=w.ambiguous(e,rng);p,cf,mg=L.pred(s)
            if route=='active':
                pr,_,_=routes['rich'].pred(s);rv=R.score(mg,cf,float(p!=pr),len(s));decision=-1 if rv<.58 or cf<.58 else p
            else: decision=-1 if cf<.48 else p
            abst+=decision==-1
        out[route]['ambiguous_abstain']=abst/N
        out[route]['hard_mean']=float(np.mean([out[route][x] for x in ['speaker_shift','no_gap','hard_noise','onset_damage','near_twin','confwrong','novel']]))
        out[route]['chunks']=len(L.bank.chunks)
    return out

# ----------------------------- recurring regime world -----------------------------
class RegimeModel:
    def __init__(self,entities=8,actions=4):
        self.E=entities;self.A=actions;self.sum=np.zeros((entities,actions));self.n=np.zeros((entities,actions))
    def pred_effect(self,e,a): return self.sum[e,a]/self.n[e,a] if self.n[e,a]>0 else 0.0
    def choose(self,e):
        vals=[self.pred_effect(e,a) if self.n[e,a]>2 else -1e4 for a in range(self.A)]
        return int(np.argmax(vals)) if max(vals)>-9999 else 0
    def observe(self,e,a,r):self.sum[e,a]+=r;self.n[e,a]+=1
    def error(self,e,a,r):return abs(self.pred_effect(e,a)-r)

class RegimeBank:
    def __init__(self,E=8,A=4,maxm=5):
        self.models=[RegimeModel(E,A)];self.active=0;self.maxm=maxm;self.err=deque(maxlen=80);self.switches=0;self.spawns=0
    def choose(self,e): return self.models[self.active].choose(e)
    def observe(self,e,a,r):
        errs=[m.error(e,a,r) for m in self.models]
        best=int(np.argmin(errs)); cur=errs[self.active]
        self.err.append(cur)
        # Re-activate old model if it persistently explains new feedback much better.
        if best!=self.active and len(self.err)>=20 and errs[best]+.22<cur:
            self.active=best;self.switches+=1
        elif len(self.err)==80 and np.mean(self.err)>.58 and len(self.models)<self.maxm:
            self.models.append(RegimeModel(self.models[0].E,self.models[0].A));self.active=len(self.models)-1;self.spawns+=1;self.err.clear()
        self.models[self.active].observe(e,a,r)

def physics(reg,e,a):
    best=(e*3 + reg*2 + (e//2)*reg)%4
    return 1.0 if a==best else -0.4

def run_regime(seed,kind):
    rng=random.Random(seed); E=8; A=4
    obj=RegimeModel(E,A) if kind=='overwrite' else RegimeBank(E,A)
    seq=[0,1,0,2,1,0]
    phase=[]
    for reg in seq:
        ok=0; first=0;N=3000
        for i in range(N):
            e=rng.randrange(E); a=obj.choose(e) if kind=='bank' else obj.choose(e); r=physics(reg,e,a)
            ok+=r>0; first+=(r>0 and i<200)
            if kind=='bank':obj.observe(e,a,r)
            else: obj.observe(e,a,r)
            # exploration to learn unseen actions
            if rng.random()<.18:
                aa=rng.randrange(A);rr=physics(reg,e,aa)
                if kind=='bank':obj.observe(e,aa,rr)
                else:obj.observe(e,aa,rr)
        phase.append({'regime':reg,'online':ok/N,'first200':first/200})
    # no-update retention probe: for each regime ask if selected action is correct
    ret=[]
    for reg in [0,1,2]:
        ok=0
        for _ in range(1000):
            e=rng.randrange(E);a=obj.choose(e);ok+=physics(reg,e,a)>0
        ret.append(ok/1000)
    return {'phase':phase,'retention':ret,'models':len(obj.models) if kind=='bank' else 1,'spawns':obj.spawns if kind=='bank' else 0,'switches':obj.switches if kind=='bank' else 0}

# ----------------------------- context/polysemy split -----------------------------
def run_polysemy(seed):
    rng=np.random.default_rng(seed)
    # Same recurrent raw chunk means different consequence under two observable context clouds.
    base=np.array([4,7,4,9,6,5]); contexts=[np.array([-1.,-.8]),np.array([1.,.8])]
    X=[];Y=[];C=[]
    for i in range(8000):
        c=int(rng.integers(0,2)); ctx=contexts[c]+rng.normal(0,.35,2); noise=base.copy();
        if rng.random()<.15:noise[int(rng.integers(0,len(base)))]=int(rng.integers(0,13))
        # raw chunk microstructure deliberately same-ish; outcome flips with learned context.
        y=c
        feat=np.concatenate([np.bincount(noise,minlength=13)[:13],ctx])
        X.append(feat);Y.append(y);C.append(ctx)
    X=np.asarray(X);Y=np.asarray(Y);C=np.asarray(C)
    # no split/context-blind chunk model
    blind=LogisticRegression(max_iter=300).fit(X[:6000,:13],Y[:6000])
    blind_acc=float((blind.predict(X[6000:,:13])==Y[6000:]).mean())
    # learner chooses number of context specializations by BIC-like unsupervised silhouette proxy.
    bestk=1;bestscore=-1e9;bestkm=None
    for k in [1,2,3,4]:
        km=KMeans(k,n_init=10,random_state=seed).fit(C[:6000]); inertia=km.inertia_; score=-inertia-25*k*math.log(6000)
        if score>bestscore:bestscore=score;bestk=k;bestkm=km
    labs=bestkm.predict(C[:6000]); testlabs=bestkm.predict(C[6000:])
    # per-specialization consequence memories
    pred=np.zeros(2000,dtype=int)
    maps={}
    for k in range(bestk):
        yy=Y[:6000][labs==k]; maps[k]=Counter(yy).most_common(1)[0][0] if len(yy) else 0
    for i,k in enumerate(testlabs):pred[i]=maps[int(k)]
    split_acc=float((pred==Y[6000:]).mean())
    purity=float(np.mean([max(Counter(Y[:6000][labs==k]).values())/max(1,(labs==k).sum()) for k in range(bestk)]))
    return {'blind':blind_acc,'context_specialized':split_acc,'chosen_splits':bestk,'specialization_purity':purity}

def main():
    acoust=[]; regimes=[]; polys=[]
    for i in range(8):
        s=9100+i; acoust.append({'seed':s,'routes':run_acoustic(s)}); polys.append({'seed':s,**run_polysemy(s)})
        for kind in ['overwrite','bank']: regimes.append({'seed':s,'kind':kind,**run_regime(s,kind)})
        print('DONE',s,flush=True)
    agg={}
    for route in ['opaque','rich','dual','active']:
        keys=['matched','speaker_shift','no_gap','silence_shift','hard_noise','onset_damage','near_twin','confwrong','novel','ambiguous_abstain','hard_mean']
        agg[route]={k:float(np.mean([r['routes'][route][k] for r in acoust])) for k in keys}
        agg[route]['chunks']=float(np.mean([r['routes'][route]['chunks'] for r in acoust]))
    regagg={}
    for kind in ['overwrite','bank']:
        rr=[x for x in regimes if x['kind']==kind]
        regagg[kind]={'mean_online':float(np.mean([np.mean([p['online'] for p in x['phase']]) for x in rr])),
                      'return_first200':float(np.mean([np.mean([x['phase'][j]['first200'] for j in [2,4,5]]) for x in rr])),
                      'retention': [float(np.mean([x['retention'][j] for x in rr])) for j in range(3)],
                      'models':float(np.mean([x['models'] for x in rr])),'spawns':float(np.mean([x['spawns'] for x in rr])),'switches':float(np.mean([x['switches'] for x in rr]))}
    polyagg={k:float(np.mean([x[k] for x in polys])) for k in ['blind','context_specialized','chosen_splits','specialization_purity']}
    out={'acoustic_routes':agg,'acoustic_seeds':acoust,'regime':regagg,'regime_rows':regimes,'polysemy':polyagg,'polysemy_rows':polys,
         'boundary':'REFERENCE_ONLY post-repair R31. Learner receives raw/self-chunk microstates plus ordinary grounded consequences. No phoneme/word/token/VAD/chunk boundary or regime IDs. 0/100 results require post-challenge.'}
    (OUT/'R31_INTEGRATED_V2_PART2_REFERENCE_ONLY.json').write_text(json.dumps(out,indent=2))
    print(json.dumps({'acoustic':agg,'regime':regagg,'polysemy':polyagg},indent=2))
if __name__=='__main__':main()
