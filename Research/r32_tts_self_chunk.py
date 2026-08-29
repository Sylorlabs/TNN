from __future__ import annotations
import os, subprocess, wave, json, math, random, hashlib
from pathlib import Path
from collections import Counter,defaultdict
import numpy as np
from scipy.io import wavfile
from scipy.signal import stft,resample_poly
from sklearn.cluster import MiniBatchKMeans
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
OUT=Path('/mnt/data/r32_epistemic'); CACHE=OUT/'tts_cache'; CACHE.mkdir(exist_ok=True)
ACTORS=['ava','ben','cora','drew']; VERBS=['moves','touches','pushes','holds']; OBJECTS=['amber cube','blue ring','green star','silver bar']
TRAIN_VOICES=['en-us','en-sc','en-uk-north']; TEST_VOICE='en-uk-rp'

def wav_for(actor,verb,obj,voice,speed,pitch=50):
 text=f'{actor} {verb} the {obj} now'
 key=hashlib.sha1(f'{text}|{voice}|{speed}|{pitch}'.encode()).hexdigest()[:16]; p=CACHE/f'{key}.wav'
 if not p.exists(): subprocess.run(['espeak','-v',voice,'-s',str(speed),'-p',str(pitch),'-w',str(p),text],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 sr,x=wavfile.read(p); x=x.astype(np.float32); x/=max(1.,float(np.max(np.abs(x))))
 return sr,x

def feats(sr,x,drop_silence=False,noise=0.0,rng=None):
 if noise>0:
  rng=np.random.default_rng(0) if rng is None else rng; x=x+rng.normal(0,noise,len(x)).astype(np.float32)
 nper=max(128,int(sr*.025)); hop=max(64,int(sr*.010)); nover=nper-hop
 f,t,z=stft(x,fs=sr,nperseg=nper,noverlap=nover,boundary=None,padded=False); mag=np.log1p(np.abs(z).T*20)
 # 20 pooled log spectral bands + energy, speaker-normalized per utterance
 edges=np.linspace(0,mag.shape[1],21,dtype=int); bands=np.stack([mag[:,edges[i]:max(edges[i]+1,edges[i+1])].mean(1) for i in range(20)],1)
 energy=np.log1p(np.sqrt(np.maximum(1e-9,np.mean(np.abs(z).T**2,1))))[:,None]
 F=np.concatenate([bands,energy],1); F=(F-F.mean(0,keepdims=True))/(F.std(0,keepdims=True)+1e-4)
 if drop_silence:
  # evaluator perturbation only: remove globally low-energy frames, no word boundaries exposed
  e=energy[:,0]; keep=e>np.quantile(e,.28); F=F[keep]
 return F.astype(np.float32)

def combos():
 out=[]
 for ai,a in enumerate(ACTORS):
  for vi,v in enumerate(VERBS):
   for oi,o in enumerate(OBJECTS):out.append((ai,vi,oi,a,v,o))
 return out

def heldout(ai,oi): return ((ai*3+oi)%4)==0

def collect(seed):
 r=np.random.default_rng(seed); train=[]; test=[]
 for ai,vi,oi,a,v,o in combos():
  if not heldout(ai,oi):
   for voice in TRAIN_VOICES:
    for speed in [145,175]:
     sr,x=wav_for(a,v,o,voice,speed,48+((ai+oi)%5));train.append((feats(sr,x),vi,'train'))
  # unseen voice + extreme speeds, all combos; mark heldout comp separately
  for speed in [118,205]:
   sr,x=wav_for(a,v,o,TEST_VOICE,speed,52);test.append((feats(sr,x),vi,'heldout_comp' if heldout(ai,oi) else 'speaker_speed'))
   test.append((feats(sr,x,drop_silence=True),vi,'silence_removed'))
   test.append((feats(sr,x,noise=.055,rng=r),vi,'noise'))
 return train,test

def codebook(train,seed,k=56):
 allf=np.concatenate([x for x,_,_ in train],0); sc=StandardScaler().fit(allf); X=sc.transform(allf)
 km=MiniBatchKMeans(k,random_state=seed,batch_size=4096,n_init=3,max_iter=160).fit(X)
 return sc,km

def codes(seq,sc,km): return tuple(map(int,km.predict(sc.transform(seq))))

def learn_motifs(train_codes,maxn=7,limit=600):
 stats=defaultdict(Counter); seen=Counter()
 for s,y,_ in train_codes:
  for n in range(2,min(maxn,len(s))+1):
   for i in range(len(s)-n+1):
    q=s[i:i+n];seen[q]+=1;stats[q][y]+=1
 cand=[]
 for q,N in seen.items():
  if N<6:continue
  c=stats[q]; purity=max(c.values())/N; base=.25
  # recurrence + grounded discriminative utility - storage cost; no surface boundary
  gain=(len(q)-1)*N-(len(q)+3); ground=max(0,purity-base)*math.log1p(N)*math.sqrt(len(q)); score=.0025*gain+ground
  if score>0.28:cand.append((score,q,purity,N))
 cand.sort(reverse=True,key=lambda z:z[0]);return [q for _,q,_,_ in cand[:limit]]

def longest_units(s,motifs):
 by=defaultdict(list)
 for j,q in enumerate(motifs):by[q[0]].append((len(q),j,q))
 for a in by:by[a].sort(reverse=True)
 out=[];i=0
 while i<len(s):
  hit=None
  for n,j,q in by.get(s[i],[]):
   if i+n<=len(s) and s[i:i+n]==q:hit=(j,n);break
  if hit is None:out.append(('r',s[i]));i+=1
  else:out.append(('m',hit[0]));i+=hit[1]
 return out

def raw_rep(s,k):
 h=np.bincount(np.asarray(s),minlength=k).astype(float);h/=max(1,h.sum());return h

def chunk_rep(s,motifs,k):
 u=longest_units(s,motifs);v=np.zeros(len(motifs)+k,float)
 for typ,j in u:
  if typ=='m':v[j]+=1
  else:v[len(motifs)+j]+=1
 if v.sum():v/=v.sum()
 return v,len(u)/max(1,len(s))

def eval_seed(seed):
 train,test=collect(seed);sc,km=codebook(train,seed)
 tc=[(codes(x,sc,km),y,g) for x,y,g in train];te=[(codes(x,sc,km),y,g) for x,y,g in test]
 motifs=learn_motifs(tc)
 Xraw=np.stack([raw_rep(s,km.n_clusters) for s,_,_ in tc]); y=np.array([y for _,y,_ in tc])
 Xch=[];rat=[]
 for s,_,_ in tc:
  v,r=chunk_rep(s,motifs,km.n_clusters);Xch.append(v);rat.append(r)
 Xch=np.stack(Xch); Xdu=np.concatenate([Xraw,Xch],1)
 models={
  'raw':LogisticRegression(max_iter=500,C=2).fit(Xraw,y),
  'chunk':LogisticRegression(max_iter=500,C=2).fit(Xch,y),
  'dual':LogisticRegression(max_iter=500,C=2).fit(Xdu,y)}
 res={'seed':seed,'motifs':len(motifs),'train_compression':1-float(np.mean(rat)),'conditions':{}}
 for g in sorted(set(z for _,_,z in te)):
  rows=[(s,y) for s,y,z in te if z==g];yr=np.array([y for _,y in rows]);R=np.stack([raw_rep(s,km.n_clusters) for s,_ in rows]);C=[];rr=[]
  for s,_ in rows:v,q=chunk_rep(s,motifs,km.n_clusters);C.append(v);rr.append(q)
  C=np.stack(C);D=np.concatenate([R,C],1)
  res['conditions'][g]={n:float(np.mean(m.predict(X)==yr)) for n,m,X in [('raw',models['raw'],R),('chunk',models['chunk'],C),('dual',models['dual'],D)]}
  res['conditions'][g]['compression']=1-float(np.mean(rr))
 return res

def main():
 rows=[]
 for s in range(4):
  rows.append(eval_seed(33200+s));print('DONE',33200+s,flush=True)
 conds=sorted(rows[0]['conditions']);agg={}
 for c in conds:
  agg[c]={k:float(np.mean([r['conditions'][c][k] for r in rows])) for k in ['raw','chunk','dual','compression']}
 agg['motifs']=float(np.mean([r['motifs'] for r in rows]));agg['train_compression']=float(np.mean([r['train_compression'] for r in rows]))
 out={'aggregate':agg,'rows':rows,'boundary':'REFERENCE_ONLY naturalistic TTS waveform test. eSpeak is an external data generator only. Learner receives raw waveform-derived generic spectral microstates plus grounded action consequence; no transcript, word/phoneme/chunk labels, VAD, ASR, tokenizer, transformer, or LLM enters learner cognition.'}
 (OUT/'R32_TTS_SELF_CHUNK_REFERENCE_ONLY.json').write_text(json.dumps(out,indent=2));print(json.dumps(agg,indent=2))
if __name__=='__main__':main()
