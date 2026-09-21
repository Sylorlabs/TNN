from __future__ import annotations
import math, random, json, hashlib, time
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score
from sklearn.preprocessing import StandardScaler

ROOT=Path('/mnt/data/tnn-r31-endogenous-chunking')
OUT=ROOT/'results'; OUT.mkdir(parents=True,exist_ok=True)

# ---------------- Raw acoustic world: evaluator knows latent causes, learner does not. ----------------
@dataclass
class UnitSpec:
    f1: float; f2: float; f3: float; p1: float; p2: float; p3: float

class RawAcousticWorld:
    def __init__(self,seed:int,n_units=14,n_classes=6):
        self.seed=seed; self.rng=np.random.default_rng(seed)
        self.n_units=n_units; self.n_classes=n_classes
        self.specs=[]
        for i in range(n_units):
            # Frequencies overlap intentionally; individual acoustics are not trivial IDs.
            base=2.0 + (i%7)*0.42 + self.rng.normal(0,.035)
            self.specs.append(UnitSpec(base,base*1.7+self.rng.normal(0,.05),base*2.35+self.rng.normal(0,.07),
                                       *self.rng.uniform(0,2*np.pi,3)))
        # Recurring latent constructions. Chunk learner never receives them.
        self.constructions=[]
        for k in range(24):
            L=int(self.rng.integers(2,5))
            seq=tuple(int(x) for x in self.rng.integers(0,n_units,L))
            self.constructions.append(seq)
        # Hidden grounded effect weights; outcomes are experienced consequences, not language labels.
        self.effect=self.rng.normal(0,1,(n_units,3))
        self.pair_effect=self.rng.normal(0,.35,(n_units,n_units,3))
        self.class_proj=self.rng.normal(0,1,(n_classes,3))

    def sample_latent(self,rng:np.random.Generator,novel=False):
        # Build utterance from recurring constructions + occasional singleton; novel uses unseen recombinations.
        if novel:
            L=int(rng.integers(5,11)); return [int(x) for x in rng.integers(0,self.n_units,L)]
        parts=int(rng.integers(2,4)); seq=[]
        for _ in range(parts):
            if rng.random()<.82: seq.extend(self.constructions[int(rng.integers(0,len(self.constructions)))])
            else: seq.append(int(rng.integers(0,self.n_units)))
        return seq[:12]

    def consequence(self,seq):
        v=np.zeros(3)
        for i,u in enumerate(seq):
            v+=self.effect[u]
            if i: v+=self.pair_effect[seq[i-1],u]
        return int(np.argmax(self.class_proj@v))

    def _unit_wave(self,u:int,speaker:dict,rng:np.random.Generator,speed=1.0,hard=False):
        sp=self.specs[u]
        n=max(42,int((78+rng.normal(0,5))*speed))
        t=np.linspace(0,1,n,endpoint=False)
        fs=speaker['freq']
        # speaker changes pitch/timbre but identity structure remains recoverable
        x=(1.00*np.sin(2*np.pi*sp.f1*fs*t+sp.p1)+
           speaker['h2']*.62*np.sin(2*np.pi*sp.f2*fs*t+sp.p2)+
           speaker['h3']*.38*np.sin(2*np.pi*sp.f3*fs*t+sp.p3))
        env=np.sin(np.pi*np.clip(t,0,1))**(.45+speaker['env'])
        x*=env*speaker['amp']
        # mild nonlinear speaker tract
        x=np.tanh(x*speaker['nonlin'])
        if hard:
            x += .035*np.sin(2*np.pi*(sp.f1*.53+1.1)*t+rng.uniform(0,6.28))
        return x.astype(np.float32)

    def speaker(self,rng,shift=False):
        if shift:
            return dict(freq=float(rng.uniform(.78,1.24)),h2=float(rng.uniform(.35,1.05)),h3=float(rng.uniform(.15,.9)),
                        amp=float(rng.uniform(.65,1.35)),env=float(rng.uniform(.05,.55)),nonlin=float(rng.uniform(.8,1.55)))
        return dict(freq=float(rng.uniform(.9,1.1)),h2=float(rng.uniform(.5,.85)),h3=float(rng.uniform(.25,.65)),
                    amp=float(rng.uniform(.8,1.2)),env=float(rng.uniform(.1,.35)),nonlin=float(rng.uniform(.9,1.25)))

    def render(self,seq,rng,speaker_shift=False,condition='train'):
        spk=self.speaker(rng,speaker_shift)
        pieces=[]; boundaries=[]; cursor=0
        if condition=='speed_extreme': speed=float(rng.uniform(.58,1.48))
        else: speed=float(rng.uniform(.82,1.18))
        gap_range=(0,3)
        overlap=(.12,.28)
        noise=.018
        hard=False
        if condition=='silence_shift': gap_range=(7,18); overlap=(.05,.18); noise=.022
        elif condition=='no_gap': gap_range=(0,1); overlap=(.30,.52); noise=.028; hard=True
        elif condition=='hard_noise': gap_range=(0,5); overlap=(.2,.42); noise=.08; hard=True
        elif condition=='onset_damage': gap_range=(0,3); overlap=(.22,.42); noise=.035; hard=True
        elif condition=='train': gap_range=(0,7); overlap=(.12,.35); noise=.025
        out=np.zeros(0,dtype=np.float32)
        true_ends=[]
        for j,u in enumerate(seq):
            w=self._unit_wave(u,spk,rng,speed=float(speed*rng.uniform(.92,1.08)),hard=hard)
            if condition=='onset_damage' and len(w)>18:
                cut=int(rng.integers(3,12)); w=w[cut:]
            if j==0:
                out=w.copy()
            else:
                ov=min(len(out)//4,len(w)//4,max(2,int(min(len(out),len(w))*rng.uniform(*overlap))))
                if ov>0:
                    a=np.linspace(1,0,ov,dtype=np.float32); b=1-a
                    out[-ov:]=out[-ov:]*a+w[:ov]*b
                    out=np.concatenate([out,w[ov:]])
                else: out=np.concatenate([out,w])
            true_ends.append(len(out))
            if j<len(seq)-1:
                gap=int(rng.integers(gap_range[0],gap_range[1]+1))
                if gap: out=np.concatenate([out,np.zeros(gap,dtype=np.float32)])
        out += rng.normal(0,noise,len(out)).astype(np.float32)
        # random gain/offset; feature front end must normalize this generic nuisance.
        out=out*float(rng.uniform(.75,1.25))+float(rng.normal(0,.015))
        return out,true_ends

# Generic low-level acoustic front-end. These are local sensory measurements, not linguistic chunks.
def frame_features(w,frame=24,hop=8):
    if len(w)<frame: w=np.pad(w,(0,frame-len(w)))
    rows=[]
    for s in range(0,max(1,len(w)-frame+1),hop):
        x=w[s:s+frame]
        if len(x)<frame: x=np.pad(x,(0,frame-len(x)))
        x=x-float(x.mean()); sd=float(x.std())+1e-5; xn=x/sd
        fft=np.abs(np.fft.rfft(xn))
        bins=fft[1:8]/(fft[1:8].sum()+1e-6)
        zc=np.mean(np.signbit(xn[1:])!=np.signbit(xn[:-1]))
        slope=np.mean(np.abs(np.diff(xn)))
        energy=np.mean(np.abs(xn))
        rows.append(np.r_[bins,zc,slope,energy])
    return np.asarray(rows,dtype=np.float32)

@dataclass
class Example:
    micro: tuple
    outcome: int
    latent: tuple
    boundary_frames: tuple

# ---------------- Reversible chunkers ----------------
class BaseChunker:
    name='base'
    def fit(self,seqs,y=None): return self
    def segment(self,seq): raise NotImplementedError
    def reconstruct(self,chunks):
        out=[]
        for _,raw in chunks: out.extend(raw)
        return tuple(out)
    def unit_key(self,chunk): return chunk[0]

class RawMicroChunker(BaseChunker):
    name='raw_micro'
    def segment(self,seq): return [(('r',int(x)),(int(x),)) for x in seq]

class FixedWindowChunker(BaseChunker):
    def __init__(self,w=4): self.w=w; self.name=f'fixed_window_{w}'
    def fit(self,seqs,y=None):
        self.known=Counter(tuple(s[i:i+self.w]) for s in seqs for i in range(0,len(s)-self.w+1,self.w)); return self
    def segment(self,seq):
        out=[];i=0
        while i<len(seq):
            raw=tuple(seq[i:i+self.w]); key=('f',raw) if raw in self.known else ('lit',raw)
            out.append((key,raw));i+=self.w
        return out

class AdaptiveMDLChunker(BaseChunker):
    name='adaptive_mdl'
    def __init__(self,max_len=12,max_motifs=256,min_count=4,ground_alpha=0.0):
        self.max_len=max_len;self.max_motifs=max_motifs;self.min_count=min_count;self.ground_alpha=ground_alpha
        if ground_alpha: self.name='grounded_adaptive_mdl'
    def fit(self,seqs,y=None):
        counts=Counter(); class_counts=defaultdict(Counter)
        for si,s in enumerate(seqs):
            cls=None if y is None else int(y[si])
            L=len(s)
            # enumerate raw microstate spans. No evaluator boundary enters here.
            for n in range(2,min(self.max_len,L)+1):
                for i in range(L-n+1):
                    t=tuple(s[i:i+n]); counts[t]+=1
                    if cls is not None: class_counts[t][cls]+=1
        scored=[]
        ncls=(max(y)+1) if y is not None and len(y) else 1
        for t,c in counts.items():
            if c<self.min_count: continue
            savings=(len(t)-1)*c-(len(t)+3)
            if savings<=0: continue
            g=0.0
            if self.ground_alpha and y is not None:
                cc=class_counts[t]; total=sum(cc.values())
                # concentration above chance is grounded predictive utility, not a linguistic label.
                g=(max(cc.values())/total - 1.0/ncls) if total else 0
            score=savings+self.ground_alpha*g*c*len(t)
            scored.append((score,len(t),c,t,g))
        scored.sort(reverse=True)
        self.motifs=[]; seen=set()
        # Diversity filter prevents dictionary from being only nested variants of one phrase.
        for rec in scored:
            t=rec[3]
            if t in seen: continue
            self.motifs.append(t); seen.add(t)
            if len(self.motifs)>=self.max_motifs: break
        self.id={t:i for i,t in enumerate(self.motifs)}
        self.byfirst=defaultdict(list)
        for t,i in self.id.items(): self.byfirst[t[0]].append((len(t),t,i))
        for k in self.byfirst: self.byfirst[k].sort(reverse=True)
        self.scored=scored[:self.max_motifs]
        return self
    def segment(self,seq):
        out=[];i=0;N=len(seq)
        while i<N:
            hit=None
            for L,t,mid in self.byfirst.get(seq[i],[]):
                if i+L<=N and tuple(seq[i:i+L])==t:
                    hit=(L,t,mid);break
            if hit:
                L,t,mid=hit;out.append((('m',mid),t));i+=L
            else:
                raw=(int(seq[i]),);out.append((('r',raw[0]),raw));i+=1
        return out

class HierarchicalChunker(BaseChunker):
    name='hierarchical_mdl'
    def __init__(self,base=None,pair_merges=96): self.base=base or AdaptiveMDLChunker(max_motifs=220);self.pair_merges=pair_merges
    def fit(self,seqs,y=None):
        self.base.fit(seqs,y)
        pair=Counter()
        for s in seqs:
            c=self.base.segment(s); keys=[x[0] for x in c]
            for a,b in zip(keys,keys[1:]): pair[(a,b)]+=1
        scored=[]
        for p,c in pair.items():
            if c>=4: scored.append((c-3,c,p))
        scored.sort(reverse=True,key=lambda x:(x[0],x[1],str(x[2])))
        self.merges={p:i for i,(_,_,p) in enumerate(scored[:self.pair_merges])}
        return self
    def segment(self,seq):
        base=self.base.segment(seq);out=[];i=0
        while i<len(base):
            if i+1<len(base) and (base[i][0],base[i+1][0]) in self.merges:
                mid=self.merges[(base[i][0],base[i+1][0])]
                raw=base[i][1]+base[i+1][1];out.append((('h',mid),raw));i+=2
            else: out.append((('b',base[i][0]),base[i][1]));i+=1
        return out

class SurpriseChunker(BaseChunker):
    name='predictive_surprise'
    def __init__(self,q=.82): self.q=q
    def fit(self,seqs,y=None):
        trans=Counter(); prev=Counter()
        for s in seqs:
            for a,b in zip(s,s[1:]): trans[(a,b)]+=1;prev[a]+=1
        vals=[];self.p={}
        for (a,b),c in trans.items():
            p=(c+.25)/(prev[a]+.25*32);self.p[(a,b)]=p;vals.append(-math.log(p))
        self.th=float(np.quantile(vals,self.q)) if vals else 10
        segcounts=Counter()
        for s in seqs:
            for _,raw in self._segments_raw(s): segcounts[raw]+=1
        self.known={t:i for i,(t,c) in enumerate(segcounts.most_common(256)) if c>=3}
        return self
    def _segments_raw(self,seq):
        out=[];start=0
        for i in range(1,len(seq)):
            surpr=-math.log(self.p.get((seq[i-1],seq[i]),1e-5))
            if surpr>=self.th:
                raw=tuple(seq[start:i]);
                if raw: out.append((None,raw))
                start=i
        raw=tuple(seq[start:]);
        if raw: out.append((None,raw))
        return out
    def segment(self,seq):
        return [(('s',self.known[raw]) if raw in self.known else ('lit',hash(raw)%1000003),raw) for _,raw in self._segments_raw(seq)]

class RandomChunker(BaseChunker):
    name='random_chunks'
    def segment(self,seq):
        # deterministic pseudo-random lengths from local content to avoid state leakage
        out=[];i=0
        while i<len(seq):
            h=(sum((j+3)*int(x) for j,x in enumerate(seq[i:i+5]))+17*i)%7
            L=2+h;raw=tuple(seq[i:min(len(seq),i+L)]);out.append((('x',hash(raw)%1000003),raw));i+=L
        return out

# Evaluator-only privileged latent representation. Never offered to TNN.
class OracleLatent:
    name='oracle_latent_evaluator_only'

# ---------------- feature/evaluation helpers ----------------
def cosine(a,b):
    na=np.linalg.norm(a); nb=np.linalg.norm(b)
    return float(a@b/(na*nb+1e-9))

def chunk_vocab_features(chunker,seqs,fit_vocab=None,dim_pair=256):
    segs=[chunker.segment(s) for s in seqs]
    if fit_vocab is None:
        vc=Counter(k for seg in segs for k,_ in seg)
        vocab={k:i for i,(k,_) in enumerate(vc.most_common(384))}
    else: vocab=fit_vocab
    X=np.zeros((len(segs),len(vocab)+dim_pair),dtype=np.float32)
    for r,seg in enumerate(segs):
        ks=[k for k,_ in seg]
        for k in ks:
            if k in vocab: X[r,vocab[k]]+=1
        for a,b in zip(ks,ks[1:]):
            h=int(hashlib.blake2b(repr((a,b)).encode(),digest_size=4).hexdigest(),16)%dim_pair
            X[r,len(vocab)+h]+=1
        if len(ks): X[r]/=math.sqrt(len(ks))
    return X,vocab,segs

def boundary_f1(seg,hidden,tol=1):
    cb=[];p=0
    for _,raw in seg[:-1]: p+=len(raw);cb.append(p)
    hb=list(hidden)
    if not cb and not hb:return 1.0
    used=set();tp=0
    for x in cb:
        best=None
        for j,y in enumerate(hb):
            if j not in used and abs(x-y)<=tol and (best is None or abs(x-y)<best[0]):best=(abs(x-y),j)
        if best: used.add(best[1]);tp+=1
    pr=tp/max(1,len(cb));rc=tp/max(1,len(hb));return 2*pr*rc/(pr+rc) if pr+rc else 0

def micro_boundaries_from_samples(sample_ends,wlen,frame=24,hop=8):
    # approximate latent ends in frame-index space; evaluator-only.
    return tuple(sorted(set(max(1,int((e-frame/2)/hop)) for e in sample_ends[:-1] if e>frame/2 and (e-frame/2)/hop>0)))

def evaluate_seed(seed:int,ntrain=3200,ntest=700,npairs=160):
    t0=time.time(); world=RawAcousticWorld(seed)
    rng=np.random.default_rng(seed+100)
    raw_train=[]; ytr=[]; latent_train=[]; ends_train=[]
    for _ in range(ntrain):
        lat=world.sample_latent(rng,novel=False); w,e=world.render(lat,rng,False,'train')
        raw_train.append(w); ytr.append(world.consequence(lat));latent_train.append(tuple(lat));ends_train.append(e)
    # learn generic low-level microstate codebook from raw local features
    sample_idx=np.linspace(0,ntrain-1,min(1200,ntrain),dtype=int)
    F=np.vstack([frame_features(raw_train[i]) for i in sample_idx])
    scaler=StandardScaler().fit(F); Fs=scaler.transform(F)
    km=MiniBatchKMeans(n_clusters=32,random_state=seed,batch_size=2048,n_init=3,max_iter=120).fit(Fs)
    def encode(w): return tuple(int(x) for x in km.predict(scaler.transform(frame_features(w))))
    trseq=[encode(w) for w in raw_train]
    # tests by condition
    conditions=['matched','speaker_shift','no_gap','silence_shift','speed_extreme','hard_noise','onset_damage','novel_composition']
    tests={}
    for cond in conditions:
        xs=[];ys=[];latents=[];hbs=[]
        for _ in range(ntest):
            lat=world.sample_latent(rng,novel=(cond=='novel_composition'))
            c='train' if cond in ('matched','speaker_shift','novel_composition') else cond
            w,e=world.render(lat,rng,speaker_shift=(cond=='speaker_shift'),condition=c)
            xs.append(encode(w));ys.append(world.consequence(lat));latents.append(tuple(lat));hbs.append(micro_boundaries_from_samples(e,len(w)))
        tests[cond]=(xs,np.asarray(ys),latents,hbs)
    chunkers=[RawMicroChunker(),FixedWindowChunker(4),RandomChunker(),SurpriseChunker(),
              AdaptiveMDLChunker(max_motifs=256),HierarchicalChunker(),AdaptiveMDLChunker(max_motifs=256,ground_alpha=18.0)]
    results=[]
    for ch in chunkers:
        ch.fit(trseq,np.asarray(ytr))
        Xtr,vocab,trsegs=chunk_vocab_features(ch,trseq)
        # simple non-transformer grounded readout; chunker quality is judged by downstream utility, not unit labels.
        clf=LogisticRegression(max_iter=300,C=1.5,solver='lbfgs').fit(Xtr,np.asarray(ytr))
        # exact reversible reconstruction stress
        recon_ok=sum(ch.reconstruct(ch.segment(s))==tuple(s) for s in trseq[:300])/300
        rec={'chunker':ch.name,'reconstruction_exact':recon_ok,'vocab_size':len(vocab),
             'train_units_per_micro':float(sum(len(ch.segment(s)) for s in trseq[:500])/sum(len(s) for s in trseq[:500]))}
        lens=[len(raw) for s in trseq[:300] for _,raw in ch.segment(s)]
        rec['mean_chunk_len']=float(np.mean(lens));rec['p95_chunk_len']=float(np.quantile(lens,.95))
        for cond,(seqs,yy,lats,hbs) in tests.items():
            X,_,segs=chunk_vocab_features(ch,seqs,fit_vocab=vocab)
            pred=clf.predict(X);rec[f'{cond}_grounded_acc']=float(accuracy_score(yy,pred))
            # evaluator-only boundary microscope, not optimization target
            rec[f'{cond}_boundary_f1_evalonly']=float(np.mean([boundary_f1(seg,hb) for seg,hb in zip(segs,hbs)]))
        results.append(rec)
    # privileged latent upper bound for grounded consequence prediction
    def latent_feat(lats):
        X=np.zeros((len(lats),world.n_units+world.n_units*world.n_units),np.float32)
        for r,lat in enumerate(lats):
            for u in lat:X[r,u]+=1
            for a,b in zip(lat,lat[1:]):X[r,world.n_units+a*world.n_units+b]+=1
        return X
    oclf=LogisticRegression(max_iter=300,C=2).fit(latent_feat(latent_train),np.asarray(ytr))
    oracle={'chunker':'oracle_latent_evaluator_only','reconstruction_exact':None,'vocab_size':world.n_units,
            'train_units_per_micro':None,'mean_chunk_len':None,'p95_chunk_len':None}
    for cond,(seqs,yy,lats,hbs) in tests.items():oracle[f'{cond}_grounded_acc']=float(accuracy_score(yy,oclf.predict(latent_feat(lats))))
    results.append(oracle)
    # Paired stability/retrieval: same latent sequence two speakers versus distractors.
    retrieval={}
    for ch in chunkers:
        ch.fit(trseq,np.asarray(ytr));_,vocab,_=chunk_vocab_features(ch,trseq[:1000])
        A=[];B=[]
        for _ in range(npairs):
            lat=world.sample_latent(rng,False)
            w1,_=world.render(lat,rng,False,'train');w2,_=world.render(lat,rng,True,'train')
            A.append(encode(w1));B.append(encode(w2))
        XA,_,_=chunk_vocab_features(ch,A,fit_vocab=vocab);XB,_,_=chunk_vocab_features(ch,B,fit_vocab=vocab)
        correct=0; margins=[]
        for i in range(npairs):
            cand=[i]+[int(x) for x in rng.choice([j for j in range(npairs) if j!=i],size=19,replace=False)]
            sims=[cosine(XA[i],XB[j]) for j in cand]
            if int(np.argmax(sims))==0:correct+=1
            margins.append(sims[0]-max(sims[1:]))
        retrieval[ch.name]={'paired_retrieval_20way':correct/npairs,'mean_match_margin':float(np.mean(margins))}
    return {'seed':seed,'results':results,'paired_stability':retrieval,'seconds':time.time()-t0,
            'world':{'train':ntrain,'test_per_condition':ntest,'n_units_hidden_evalonly':world.n_units,'conditions':conditions}}

def main():
    seeds=[3101,3102,3103,3104,3105]
    allr=[]
    for s in seeds:
        r=evaluate_seed(s);allr.append(r)
        (OUT/f'chunking_seed_{s}.json').write_text(json.dumps(r,indent=2))
        print('DONE',s,'sec',round(r['seconds'],1),flush=True)
    # aggregate
    names=[r['chunker'] for r in allr[0]['results']]
    agg={}
    for name in names:
        rows=[next(x for x in r['results'] if x['chunker']==name) for r in allr]
        keys=set.intersection(*(set(x.keys()) for x in rows))-{'chunker'}
        agg[name]={}
        for k in sorted(keys):
            vals=[x[k] for x in rows if isinstance(x[k],(int,float)) and x[k] is not None]
            if vals:agg[name][k]={'mean':float(np.mean(vals)),'min':float(np.min(vals)),'max':float(np.max(vals))}
        if name!='oracle_latent_evaluator_only':
            st=[r['paired_stability'][name] for r in allr]
            for k in st[0]: agg[name][k]={'mean':float(np.mean([x[k] for x in st])),'min':float(np.min([x[k] for x in st])),'max':float(np.max([x[k] for x in st]))}
    # composite excludes evaluator boundary alignment and compression isn't allowed to dominate.
    for name,a in agg.items():
        if name=='oracle_latent_evaluator_only':continue
        hard=np.mean([a[f'{c}_grounded_acc']['mean'] for c in ['speaker_shift','no_gap','silence_shift','speed_extreme','hard_noise','onset_damage','novel_composition']])
        stability=a['paired_retrieval_20way']['mean']; comp=1-a['train_units_per_micro']['mean']; recon=a['reconstruction_exact']['mean']
        a['capability_composite']=float(.55*hard+.25*stability+.10*comp+.10*recon)
    order=sorted([(v.get('capability_composite',-1),k) for k,v in agg.items()],reverse=True)
    summary={'seeds':seeds,'aggregate':agg,'ranking':order,
             'claim_boundary':'External reference tournament only. Learners see raw waveforms, generic microfeatures, and grounded consequence; no word/phoneme/token/VAD boundaries. No transformer/LLM.'}
    (OUT/'chunking_tournament_summary.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps({'ranking':order},indent=2))
if __name__=='__main__':main()
