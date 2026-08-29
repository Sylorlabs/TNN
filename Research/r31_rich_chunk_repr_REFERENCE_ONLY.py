from __future__ import annotations
import json,math,time,hashlib
from pathlib import Path
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from r31_chunking_tournament import RawAcousticWorld,frame_features,AdaptiveMDLChunker,HierarchicalChunker,SurpriseChunker,RawMicroChunker,chunk_vocab_features
OUT=Path('/mnt/data/tnn-r31-endogenous-chunking/results')

def hidx(obj,n):return int(hashlib.blake2b(repr(obj).encode(),digest_size=4).hexdigest(),16)%n
# Chunk intrinsic representation: no one-hot chunk vocabulary required.
def intrinsic_features(chunker,seqs):
    D=32+16+64+96+128
    X=np.zeros((len(seqs),D),np.float32)
    for r,s in enumerate(seqs):
        seg=chunker.segment(s); off=0
        # exact residual microstate evidence (generic sensory content, not a unit label)
        for x in s:X[r,off+(int(x)%32)]+=1
        off+=32
        keys=[]
        for _,raw in seg:
            L=min(16,len(raw));X[r,off+L-1]+=1
            sig=(raw[0],raw[-1],min(8,len(raw)))
            X[r,off+16+hidx(sig,64)]+=1
            for a,b in zip(raw,raw[1:]):X[r,off+16+64+hidx((a,b),96)]+=1
            keys.append(sig)
        off+=16+64+96
        for a,b in zip(keys,keys[1:]):X[r,off+hidx((a,b),128)]+=1
        X[r]/=math.sqrt(max(1,len(s)))
    return X

def run(seed=12001,ntrain=2200,ntest=450):
    t0=time.time();world=RawAcousticWorld(seed);rng=np.random.default_rng(seed+5)
    raws=[];ys=[]
    for _ in range(ntrain):
        lat=world.sample_latent(rng,False);w,_=world.render(lat,rng,False,'train');raws.append(w);ys.append(world.consequence(lat))
    F=np.vstack([frame_features(w) for w in raws[::3]])
    sc=StandardScaler().fit(F);km=MiniBatchKMeans(32,random_state=seed,n_init=2,batch_size=1024,max_iter=100).fit(sc.transform(F))
    enc=lambda w: tuple(int(x) for x in km.predict(sc.transform(frame_features(w))))
    tr=[enc(w) for w in raws];y=np.array(ys)
    tests={}
    for cond in ['matched','speaker_shift','no_gap','silence_shift','hard_noise','novel_composition']:
        ss=[];yy=[]
        for _ in range(ntest):
            lat=world.sample_latent(rng,cond=='novel_composition');c='train' if cond in ('matched','speaker_shift','novel_composition') else cond
            w,_=world.render(lat,rng,cond=='speaker_shift',c);ss.append(enc(w));yy.append(world.consequence(lat))
        tests[cond]=(ss,np.array(yy))
    chunkers=[RawMicroChunker(),AdaptiveMDLChunker(max_motifs=220),HierarchicalChunker(AdaptiveMDLChunker(max_motifs=200),80),SurpriseChunker()]
    rows=[]
    for ch in chunkers:
        ch.fit(tr,y)
        # ID-only current framing
        Xi,v,_=chunk_vocab_features(ch,tr);ci=LogisticRegression(max_iter=250,C=1.4).fit(Xi,y)
        # intrinsic rich framing
        Xr=intrinsic_features(ch,tr);cr=LogisticRegression(max_iter=250,C=1.4).fit(Xr,y)
        rec={'chunker':ch.name,'compression':1-sum(len(ch.segment(s)) for s in tr[:500])/sum(len(s) for s in tr[:500])}
        for cond,(ss,yy) in tests.items():
            XX,_,_=chunk_vocab_features(ch,ss,fit_vocab=v);rec[f'{cond}_id']=float(accuracy_score(yy,ci.predict(XX)))
            rec[f'{cond}_rich']=float(accuracy_score(yy,cr.predict(intrinsic_features(ch,ss))))
        rec['hard_id']=float(np.mean([rec[f'{c}_id'] for c in tests if c!='matched']))
        rec['hard_rich']=float(np.mean([rec[f'{c}_rich'] for c in tests if c!='matched']))
        rows.append(rec);print(ch.name,round(rec['hard_id'],4),round(rec['hard_rich'],4),flush=True)
    out={'seed':seed,'rows':rows,'seconds':time.time()-t0,'boundary':'Reference ablation. Rich chunk state is computed from intrinsic raw microstructure; no learned linguistic vocabulary or evaluator boundaries.'}
    (OUT/'rich_chunk_representation.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
if __name__=='__main__':run()
