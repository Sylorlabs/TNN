from __future__ import annotations
import sys, json, math, time, traceback, gc
from pathlib import Path
from collections import Counter, defaultdict
import numpy as np
from scipy.sparse import csr_matrix, hstack
from sklearn.linear_model import LogisticRegression

ROOT=Path('/mnt/data/r32_epistemic')
sys.path.insert(0,str(ROOT))
import r32_tts_self_chunk_streaming as base

OUT=ROOT
K=int(base.K)
PAIR_BINS=512
TRIPLE_BINS=1024
RUN_BINS=256
SEG_BINS=2048
LEVELS=(1,2,4,8)


def atomic(path:Path,obj):
    tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(json.dumps(obj,indent=2,sort_keys=True));tmp.replace(path)


def _sparse(rows,dim):
    rr=[];cc=[];dd=[]
    for i,d in enumerate(rows):
        for k,v in d.items():
            if v:
                rr.append(i);cc.append(int(k));dd.append(float(v))
    return csr_matrix((dd,(rr,cc)),shape=(len(rows),dim),dtype=np.float32)


def raw_temporal(codes):
    # Learner-derived microstates + local temporal order; no supplied units/boundaries.
    dim=K+PAIR_BINS+TRIPLE_BINS+RUN_BINS
    rows=[]
    for s in codes:
        d=defaultdict(float);n=max(1,len(s))
        for x,c in Counter(s).items(): d[x]+=c/n
        for i in range(len(s)-1):d[K+(s[i]*131+s[i+1]*17)%PAIR_BINS]+=1/max(1,len(s)-1)
        off=K+PAIR_BINS
        for i in range(len(s)-2):d[off+(s[i]*65537+s[i+1]*257+s[i+2]*31)%TRIPLE_BINS]+=1/max(1,len(s)-2)
        off+=TRIPLE_BINS
        if s:
            last=s[0];run=1
            for x in s[1:]+[-999999]:
                if x==last:run+=1
                else:
                    rb=min(15,run);d[off+(last*17+rb*31)%RUN_BINS]+=1
                    last=x;run=1
        rows.append(d)
    return _sparse(rows,dim)


def elastic_pyramid(codes):
    # Relative-time pyramids preserve order while tolerating speaking-rate changes.
    pyr_dim=K*sum(LEVELS)
    trans_dim=PAIR_BINS*2
    dur_dim=RUN_BINS
    dim=pyr_dim+trans_dim+dur_dim
    rows=[]
    level_off=[];o=0
    for L in LEVELS:level_off.append(o);o+=K*L
    for s in codes:
        d=defaultdict(float);n=max(1,len(s))
        for li,L in enumerate(LEVELS):
            counts=Counter()
            for t,x in enumerate(s):
                b=min(L-1,(t*L)//n);counts[(b,x)]+=1
            for (b,x),c in counts.items():d[level_off[li]+b*K+x]+=c/n
        off=pyr_dim
        # transitions indexed once globally and once by early/late half
        for t in range(len(s)-1):
            h=(s[t]*131+s[t+1]*17)%PAIR_BINS
            d[off+h]+=1/max(1,len(s)-1)
            half=0 if t*2<n else 1
            d[off+PAIR_BINS+(h+half*257)%PAIR_BINS]+=1/max(1,len(s)-1)
        off+=trans_dim
        if s:
            last=s[0];run=1
            for x in s[1:]+[-999999]:
                if x==last:run+=1
                else:
                    d[off+(last*19+min(run,15)*29)%RUN_BINS]+=1
                    last=x;run=1
        rows.append(d)
    return _sparse(rows,dim)


def fit_transition_surprise(codes,alpha=0.35):
    row=np.full((K,K),alpha,dtype=np.float64)
    for s in codes:
        for a,b in zip(s[:-1],s[1:]):row[a,b]+=1
    row/=row.sum(axis=1,keepdims=True)
    return -np.log(row+1e-12)


def surprise_segments(codes,surprise,quantile=.82,min_len=3,max_segments=14):
    out=[]
    for s in codes:
        n=len(s)
        if n<2:out.append([(0,n)]);continue
        vals=np.asarray([surprise[a,b] for a,b in zip(s[:-1],s[1:])],float)
        th=float(np.quantile(vals,quantile)) if len(vals)>3 else float(vals.max()+1)
        cand=[]
        for i,v in enumerate(vals,1):
            left=vals[i-2] if i-2>=0 else -1e9;right=vals[i] if i<len(vals) else -1e9
            if v>=th and v>=left and v>=right:cand.append((v,i))
        # keep strongest but restore temporal order
        cand=sorted(cand,reverse=True)[:max_segments-1]
        cuts=sorted(i for _,i in cand)
        # enforce minimum segment length without a human boundary rule
        kept=[];last=0
        for c in cuts:
            if c-last>=min_len and n-c>=min_len:kept.append(c);last=c
        pts=[0]+kept+[n]
        out.append([(pts[i],pts[i+1]) for i in range(len(pts)-1)])
    return out


def segment_features(codes,segments):
    # Boundary locations are prediction-surprise hypotheses. Intrinsic raw evidence stays present.
    dim=SEG_BINS+K*4+256
    rows=[]
    for s,segs in zip(codes,segments):
        d=defaultdict(float);den=max(1,len(segs))
        for j,(a,b) in enumerate(segs):
            q=s[a:b]
            if not q:continue
            pos=min(3,(j*4)//den)
            c=Counter(q)
            for x,n in c.items():d[SEG_BINS+pos*K+x]+=n/max(1,len(q))/den
            sig=146959810
            for x in q:sig=((sig^int(x+17))*16777619)&0x7fffffff
            d[sig%SEG_BINS]+=1/den
            d[SEG_BINS+K*4+(len(q)*31+q[0]*17+q[-1]*13)%256]+=1/den
        rows.append(d)
    return _sparse(rows,dim)


def fit_model(X,Y):
    return LogisticRegression(max_iter=900,C=1.5,solver='liblinear',multi_class='ovr').fit(X,Y)


def acc(model,X,y):return float(np.mean(model.predict(X)==y))


def run(seed:int):
    t0=time.time()
    train,tests=base.world(seed)
    sc,km=base.fit_codebook(train,seed)
    pool=base.propose_pool(train,seed,sc,km)
    seen=Counter();cls=defaultdict(Counter);codes=[];Y=[]
    for spec in train:
        F,y=base.encounter(spec,seed,0);s=base.code(F,sc,km);codes.append(s);Y.append(y);base.update_stats(s,y,pool,seen,cls)
    motifs=base.active_motifs(seen,cls);by=base.idxmot(motifs)
    Y=np.asarray(Y)
    R=raw_temporal(codes);E=elastic_pyramid(codes)
    surprise=fit_transition_surprise(codes)
    S=segment_features(codes,surprise_segments(codes,surprise))
    _,C,ratio=base.sparse_rows(codes,Y,by)
    Xs={
      'raw_temporal':R,
      'elastic':E,
      'surprise_segment':S,
      'elastic_chunk':hstack([E,C],format='csr'),
      'segment_chunk':hstack([S,C],format='csr'),
      'elastic_segment':hstack([E,S],format='csr'),
      'full_dual':hstack([E,S,C],format='csr'),
    }
    models={k:fit_model(v,Y) for k,v in Xs.items()}
    te=[(base.code(F,sc,km),y,g) for F,y,g in tests]
    conds=sorted(set(g for _,_,g in te));out={'seed':seed,'train_n':len(Y),'motifs':len(motifs),'train_compression':1-float(ratio),'conditions':{}}
    for g in conds:
        sub=[x for x in te if x[2]==g];ss=[x[0] for x in sub];yy=np.asarray([x[1] for x in sub])
        TR=raw_temporal(ss);TE=elastic_pyramid(ss);TS=segment_features(ss,surprise_segments(ss,surprise));_,TC,_=base.sparse_rows(ss,yy,by)
        tx={'raw_temporal':TR,'elastic':TE,'surprise_segment':TS,'elastic_chunk':hstack([TE,TC],format='csr'),'segment_chunk':hstack([TS,TC],format='csr'),'elastic_segment':hstack([TE,TS],format='csr'),'full_dual':hstack([TE,TS,TC],format='csr')}
        out['conditions'][g]={k:acc(models[k],tx[k],yy) for k in models}
    hard_conds=[g for g in conds if g in {'speaker_speed','low_energy_removed','hard_noise','heldout_comp'}] or conds
    out['hard_mean']={k:float(np.mean([out['conditions'][g][k] for g in hard_conds])) for k in models}
    out['elapsed_seconds']=time.time()-t0
    out['boundary']='REFERENCE_ONLY non-transformer elastic temporal/self-segmental PAM comparison. Learner receives waveform-derived microstates, endogenous prediction-surprise segments, reversible chunks, and grounded action consequences only. No transcript, word/phoneme/chunk boundary, VAD, ASR, tokenizer, transformer or LLM enters cognition.'
    return out


def main():
    rows=[]
    for seed in range(35100,35104):
        p=OUT/f'R32_ELASTIC_TEMPORAL_PAM_SEED_{seed}.json'
        if p.exists():r=json.loads(p.read_text())
        else:
            r=run(seed);atomic(p,r)
        rows.append(r);print('DONE',seed,r['hard_mean'],flush=True);gc.collect()
    routes=list(rows[0]['hard_mean'])
    agg={k:{'hard_mean':float(np.mean([r['hard_mean'][k] for r in rows])),'min':float(np.min([r['hard_mean'][k] for r in rows])),'max':float(np.max([r['hard_mean'][k] for r in rows]))} for k in routes}
    for k in routes:
        for g in rows[0]['conditions']:
            agg[k][g]=float(np.mean([r['conditions'][g][k] for r in rows]))
    final={'aggregate':agg,'rows':rows,'boundary':rows[0]['boundary']}
    atomic(OUT/'R32_TTS_ELASTIC_TEMPORAL_PAM_REFERENCE_ONLY.json',final);print(json.dumps(agg,indent=2))
if __name__=='__main__':main()
