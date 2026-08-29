import numpy as np, json, math
from pathlib import Path
OUT=Path('/mnt/data/r32_epistemic')
KINDS=['stable','misleading','correlated_wrong','ambiguous','crossmodal_conflict','near_twin']
K=4; S=4

def softmax(x):
    z=x-np.max(x); e=np.exp(z); return e/(e.sum()+1e-12)

def train_model(seed,n=8000):
    rng=np.random.default_rng(seed)
    # generic expected evidence signatures learned from grounded resolved experience
    base=np.zeros((K,S,K)); cnt=np.zeros((K,S))
    for _ in range(n):
        true=int(rng.integers(K)); src=int(rng.integers(S))
        e=rng.normal(0,.10,K); e[true]+=2.0+0.15*src
        base[true,src]+=e; cnt[true,src]+=1
    base/=cnt[:,:,None]
    return base

def make_env(rng,kind,model):
    true=int(rng.integers(K)); twin=(true+1+int(rng.integers(K-1)))%K
    # source-specific actual evidence generator; learner does not know kind
    def obs(src):
        e=rng.normal(0,.10,K)
        if kind=='ambiguous':
            # world itself does not discriminate this pair, even across modalities
            e[true]+=1.05; e[twin]+=1.05
        elif kind=='correlated_wrong':
            if src==0: e[twin]+=2.3; e[true]+=.15
            else: e[true]+=2.05+.1*src; e[twin]+=.10
        elif kind=='misleading':
            if src==0: e[twin]+=2.1; e[true]+=.25
            else: e[true]+=2.0; e[twin]+=.15
        elif kind=='crossmodal_conflict':
            if src in (0,1): e[twin]+=1.75; e[true]+=.45
            else: e[true]+=2.1; e[twin]+=.10
        elif kind=='near_twin':
            # acoustic-ish source0 weakly discriminates, grounded action source3 strongly
            if src==0: e[true]+=1.15; e[twin]+=.90
            elif src==1: e[true]+=1.35; e[twin]+=.75
            elif src==2: e[true]+=1.55; e[twin]+=.55
            else: e[true]+=2.2; e[twin]+=.10
        else: e[true]+=2.0+.1*src; e[twin]+=.10
        return e
    return true,twin,obs

def top2(score):
    order=np.argsort(score)[::-1]; return int(order[0]),int(order[1]),float(score[order[0]]-score[order[1]])

def expected_sep(mu,a,b,s):
    return float(np.linalg.norm(mu[a,s]-mu[b,s]))

def run_r31(true,twin,obs,maxp=4):
    score=np.zeros(K); used=[]
    for s in range(maxp):
        src=s%S; used.append(src); score+=obs(src); a,b,m=top2(score)
        if len(used)>=2 and m>1.25: return a,len(used),False
    a,b,m=top2(score)
    if m<.65: return -1,len(used),True
    return a,len(used),False

def run_r32(true,twin,obs,mu,maxp=4):
    score=np.zeros(K); used=[]; failed_gain=0; provenance=set(); last_margin=0.0
    # initial raw/acoustic view
    src=0; e=obs(src); used.append(src); provenance.add(src); score+=e
    for step in range(1,maxp+1):
        a,b,m=top2(score)
        # learned-world expected information gain for untried independent sources
        cand=[]
        for s in range(S):
            if s in provenance: continue
            cand.append((expected_sep(mu,a,b,s),s))
        best_gain,best_src=max(cand) if cand else (0.0,-1)
        # if evidence is already strong and not contradicted by failed high-value probes, commit
        if len(provenance)>=2 and m>1.35 and failed_gain==0:
            return a,len(used),False,failed_gain
        # economically no useful new observation or repeated expected probes failed to reduce uncertainty
        if (best_src<0 or best_gain<1.0) and m<1.0:
            return -1,len(used),True,failed_gain
        if failed_gain>=2 and len(provenance)>=3 and m<1.35:
            return -1,len(used),True,failed_gain
        if best_src<0: break
        before=m; e=obs(best_src); used.append(best_src); provenance.add(best_src); score+=e
        _,_,after=top2(score)
        # high predicted separation that fails to improve margin = model mismatch / unresolved-state evidence
        if best_gain>=1.5 and after-before < .35: failed_gain+=1
        elif after-before>.65 and failed_gain>0: failed_gain-=1
        last_margin=after
    a,b,m=top2(score)
    if (failed_gain>=1 and m<1.2) or m<.6: return -1,len(used),True,failed_gain
    return a,len(used),False,failed_gain

def eval_seed(seed,n=1400):
    rng=np.random.default_rng(seed); mu=train_model(seed+999)
    out={}
    for kind in KINDS:
        stats={k:{'correct':0,'abstain':0,'wrong':0,'probes':0,'failed_gain':0} for k in ['r31','r32']}
        for _ in range(n):
            true,twin,obs=make_env(rng,kind,mu)
            p,pr,ab=run_r31(true,twin,obs); d=stats['r31']; d['probes']+=pr; d['abstain']+=ab; d['wrong']+=p not in (-1,true); d['correct']+=p==true
            # new independent env with same hidden true/twin distribution but fresh evidence, to avoid policy consuming same RNG path unfairly
            # rebind explicit true/twin by custom closure
            def obs2(src, _rng=rng, _kind=kind, _true=true, _twin=twin):
                e=_rng.normal(0,.10,K)
                if _kind=='ambiguous': e[_true]+=1.05; e[_twin]+=1.05
                elif _kind=='correlated_wrong':
                    if src==0:e[_twin]+=2.3;e[_true]+=.15
                    else:e[_true]+=2.05+.1*src;e[_twin]+=.10
                elif _kind=='misleading':
                    if src==0:e[_twin]+=2.1;e[_true]+=.25
                    else:e[_true]+=2.0;e[_twin]+=.15
                elif _kind=='crossmodal_conflict':
                    if src in (0,1):e[_twin]+=1.75;e[_true]+=.45
                    else:e[_true]+=2.1;e[_twin]+=.10
                elif _kind=='near_twin':
                    if src==0:e[_true]+=1.15;e[_twin]+=.90
                    elif src==1:e[_true]+=1.35;e[_twin]+=.75
                    elif src==2:e[_true]+=1.55;e[_twin]+=.55
                    else:e[_true]+=2.2;e[_twin]+=.10
                else:e[_true]+=2.0+.1*src;e[_twin]+=.10
                return e
            p,pr,ab,fg=run_r32(true,twin,obs2,mu); d=stats['r32']; d['probes']+=pr; d['abstain']+=ab; d['wrong']+=p not in (-1,true); d['correct']+=p==true; d['failed_gain']+=fg
        for pol in stats:
            for x in stats[pol]: stats[pol][x]/=n
        out[kind]=stats
    return {'seed':seed,'results':out}

def main():
    rows=[eval_seed(33000+i) for i in range(8)]
    agg={p:{} for p in ['r31','r32']}
    for p in agg:
        for kind in KINDS:
            for m in ['correct','abstain','wrong','probes','failed_gain']:
                vals=[r['results'][kind][p][m] for r in rows]
                agg[p][f'{kind}_{m}']=float(np.mean(vals))
        agg[p]['resolvable_correct_mean']=float(np.mean([agg[p][f'{k}_correct'] for k in KINDS if k!='ambiguous']))
        agg[p]['ambiguous_abstain']=agg[p]['ambiguous_abstain']
        agg[p]['wrong_mean']=float(np.mean([agg[p][f'{k}_wrong'] for k in KINDS]))
    out={'aggregate':agg,'rows':rows,'boundary':'REFERENCE_ONLY. Observation sources chosen by learned expected consequence/evidence separation. Persistent failed-information-gain is treated as epistemic model-mismatch evidence. No ambiguity label, token boundary, VAD, graph, transformer, or LLM.'}
    (OUT/'R32_ACTIVE_EPISTEMIC_REFERENCE_ONLY.json').write_text(json.dumps(out,indent=2));print(json.dumps(agg,indent=2))
if __name__=='__main__':main()
