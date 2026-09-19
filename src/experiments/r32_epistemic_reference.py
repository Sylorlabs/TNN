import numpy as np, json, math
from sklearn.linear_model import LogisticRegression
from pathlib import Path
OUT=Path('/mnt/data/r32_epistemic')

KINDS=['stable','misleading','correlated_wrong','ambiguous','drift','crossmodal_conflict','switch']
SOURCES=4

def softmax(x):
    z=x-np.max(x); e=np.exp(z); return e/(e.sum()+1e-12)

def entropy(p):
    return float(-(p*np.log(p+1e-12)).sum()/math.log(len(p)))

def make_case(rng,K=4,kind=None):
    kind=kind or rng.choice(KINDS)
    true=int(rng.integers(K)); twin=(true+1+int(rng.integers(K-1)))%K
    obs=[]
    T=5
    for t in range(T):
        src=t%SOURCES
        e=np.zeros(K)
        if kind=='ambiguous':
            a,b=true,twin
            e[a]=1.0+rng.normal(0,.16); e[b]=1.0+rng.normal(0,.16)
            e+=rng.normal(0,.08,K)
        elif kind=='correlated_wrong':
            if t<3:
                src=0
                e[twin]=2.0+rng.normal(0,.12); e[true]=.35+rng.normal(0,.08)
            else:
                e[true]=2.2+rng.normal(0,.12); e[twin]=.2+rng.normal(0,.08)
        elif kind=='misleading':
            if t==0:
                e[twin]=2.1+rng.normal(0,.12); e[true]=.3+rng.normal(0,.1)
            else:
                e[true]=1.9+rng.normal(0,.14); e[twin]=.2+rng.normal(0,.1)
        elif kind=='crossmodal_conflict':
            if src in (0,1): e[twin]=1.55+rng.normal(0,.15); e[true]=.55+rng.normal(0,.12)
            else: e[true]=2.0+rng.normal(0,.12); e[twin]=.2+rng.normal(0,.1)
        elif kind=='drift':
            if t<2: e[true]=1.8+rng.normal(0,.12)
            else:
                e[true]=1.0+rng.normal(0,.2); e[twin]=.9+rng.normal(0,.2)
        elif kind=='switch':
            # real source changes after t1; final state is twin
            if t<2: e[true]=1.9+rng.normal(0,.1)
            else: e[twin]=2.0+rng.normal(0,.12)
        else:
            e[true]=2.0+rng.normal(0,.12); e[twin]=.15+rng.normal(0,.08)
        e+=rng.normal(0,.06,K)
        obs.append((src,e))
    final_true=twin if kind=='switch' else true
    return {'kind':kind,'true':final_true,'initial':true,'twin':twin,'obs':obs}

class Pop:
    def __init__(self,K=4,dep=True): self.K=K; self.dep=dep; self.reset()
    def reset(self): self.score=np.zeros(self.K); self.src_n=np.zeros(SOURCES,int); self.hist=[]
    def step(self,src,e):
        self.src_n[src]+=1
        w=1.0/(self.src_n[src]**0.75) if self.dep else 1.0
        self.score += w*e
        p=softmax(self.score)
        self.hist.append(p.copy())
        return p
    def feats(self):
        p=softmax(self.score); s=np.sort(p)[::-1]; margin=s[0]-s[1]
        ent=entropy(p); indep=np.count_nonzero(self.src_n)/SOURCES
        if len(self.hist)>=2: vol=float(np.mean(np.abs(self.hist[-1]-self.hist[-2])))
        else: vol=0.0
        # dependence concentration, unresolved top2 mass and disagreement proxy
        dep=float(self.src_n.max()/(self.src_n.sum()+1e-9)) if self.src_n.sum() else 1.0
        top2=float(s[:2].sum())
        return np.array([margin,1-ent,indep,1-dep,1-vol,s[0],1-top2],float)

class Baseline:
    def __init__(self,K=4): self.K=K
    def run(self,c):
        score=np.zeros(self.K); probes=0
        for src,e in c['obs']:
            probes+=1; score+=e; p=softmax(score); s=np.sort(p)[::-1]
            if probes>=2 and s[0]-s[1]>.38: return int(np.argmax(p)),probes
        p=softmax(score); s=np.sort(p)[::-1]
        return (int(np.argmax(p)) if s[0]-s[1]>.22 else -1),probes

def train_commit(seed,dep=True,K=4):
    rng=np.random.default_rng(seed); X=[];y=[]
    # delayed correctness only on cases that eventually have an observed state; no ambiguity label used
    for _ in range(3500):
        kind=rng.choice(['stable','misleading','correlated_wrong','crossmodal_conflict','drift','switch'])
        c=make_case(rng,K,kind); m=Pop(K,dep)
        for src,e in c['obs']:
            p=m.step(src,e); X.append(m.feats()); y.append(int(np.argmax(p)==c['true']))
    clf=LogisticRegression(max_iter=700,class_weight='balanced').fit(np.asarray(X),np.asarray(y))
    return clf

def run_policy(c,clf,dep=True,K=4,maxp=5):
    m=Pop(K,dep); probes=0
    for src,e in c['obs']:
        probes+=1; p=m.step(src,e); safe=float(clf.predict_proba(m.feats()[None,:])[0,1]); s=np.sort(p)[::-1]
        # commit only when delayed-history reliability AND current population concentration agree
        if probes>=2 and safe>=.78 and s[0]-s[1]>=.20: return int(np.argmax(p)),probes,m.feats()
    # persistent hypothesis mass: UNKNOWN when top alternatives remain materially alive or evidence is source-dependent/volatile
    f=m.feats(); p=softmax(m.score); s=np.sort(p)[::-1]
    safe=float(clf.predict_proba(f[None,:])[0,1])
    if safe<.67 or s[0]-s[1]<.17 or f[2]<.50: return -1,probes,f
    return int(np.argmax(p)),probes,f

def eval_one(seed,kind,policy,n=1200):
    rng=np.random.default_rng(seed); correct=abst=wrong=probes=0
    for _ in range(n):
        c=make_case(rng,4,kind)
        if policy=='baseline': pred,pr=Baseline().run(c)
        else:
            clf,dep=policy; pred,pr,_=run_policy(c,clf,dep)
        probes+=pr
        if kind=='ambiguous':
            abst += pred==-1; wrong += pred!=-1
        else:
            correct += pred==c['true']; wrong += pred not in (-1,c['true']); abst += pred==-1
    return {'correct':correct/n if kind!='ambiguous' else None,'ambiguous_abstain':abst/n if kind=='ambiguous' else None,'wrong_commit':wrong/n,'abstain':abst/n,'mean_probes':probes/n}

def main():
    rows=[]
    for si in range(8):
        seed=32000+si
        clf_dep=train_commit(seed*10+1,True); clf_nodep=train_commit(seed*10+2,False)
        for name,pol in [('r31_threshold','baseline'),('hyp_population',(clf_dep,True)),('hyp_no_dependence',(clf_nodep,False))]:
            d={'seed':seed,'policy':name}
            for ki,k in enumerate(KINDS): d[k]=eval_one(seed*100+ki,k,pol)
            rows.append(d)
        print('DONE',seed,flush=True)
    agg={}
    for name in ['r31_threshold','hyp_population','hyp_no_dependence']:
        rr=[r for r in rows if r['policy']==name]; a={}
        for k in KINDS:
            for m in ['correct','ambiguous_abstain','wrong_commit','abstain','mean_probes']:
                vals=[r[k][m] for r in rr if r[k][m] is not None]
                if vals:a[f'{k}_{m}']=float(np.mean(vals))
        stable=[k for k in KINDS if k!='ambiguous']
        a['hard_correct_mean']=float(np.mean([a[f'{k}_correct'] for k in stable]))
        a['overall_wrong_commit']=float(np.mean([a[f'{k}_wrong_commit'] for k in KINDS]))
        agg[name]=a
    out={'aggregate':agg,'rows':rows,'boundary':'REFERENCE_ONLY. Persistent non-graph hypothesis population. Commit reliability trained only from delayed correctness on resolvable development histories; no ambiguity label is supplied to learner. Repeated same-source evidence is dependency-discounted.'}
    (OUT/'R32_EPISTEMIC_HYPOTHESIS_REFERENCE_ONLY.json').write_text(json.dumps(out,indent=2)); print(json.dumps(agg,indent=2))
if __name__=='__main__': main()
