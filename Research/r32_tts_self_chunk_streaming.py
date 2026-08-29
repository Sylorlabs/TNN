from __future__ import annotations
import os,glob,subprocess,hashlib,math,json,gc
from pathlib import Path
from collections import Counter,defaultdict
import numpy as np
from scipy.io import wavfile
from scipy.signal import stft,resample_poly
from scipy.sparse import csr_matrix,hstack
from sklearn.cluster import MiniBatchKMeans
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

OUT=Path('/mnt/data/r32_epistemic'); CACHE=OUT/'tts_cache_v2'; CACHE.mkdir(exist_ok=True)
ACTORS=['ava','ben','cora','drew','eli','fern'];ACTIONS=['moves','touches','pushes','holds','opens','guides'];OBJECTS=['amber cube','blue ring','green star','silver bar','ivory disk','red cone']
TRAIN_VOICES=['en-us','en-sc','en-uk-north','en-uk-wmids'];TEST_VOICES=['en-uk-rp','en-wi'];SPEEDS=[135,165,195];DOSES=[1,2,4,8]
K=72;PROP_MAX=5000;MOTIF_MAX=900;CHASH=1536;PHASH=256

def key_for(a,v,o,voice,speed,pitch):return hashlib.sha1(f'{a} {v} the {o} now|{voice}|{speed}|{pitch}'.encode()).hexdigest()[:20]
def synth(a,v,o,voice,speed,pitch):
 key=key_for(a,v,o,voice,speed,pitch); hits=glob.glob(str(CACHE/f'{key}.*.wav'))
 p=Path(hits[0]) if hits else CACHE/f'{key}.{os.getpid()}.wav'
 if not p.exists():subprocess.run(['espeak','-v',voice,'-s',str(speed),'-p',str(pitch),'-w',str(p),f'{a} {v} the {o} now'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 try:sr,x=wavfile.read(p)
 except Exception:
  p.unlink(missing_ok=True);subprocess.run(['espeak','-v',voice,'-s',str(speed),'-p',str(pitch),'-w',str(p),f'{a} {v} the {o} now'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);sr,x=wavfile.read(p)
 x=x.astype(np.float32);x/=max(1.,float(np.max(np.abs(x))));return sr,x

def pert(sr,x,seed,rep):
 if rep==0:return x
 r=np.random.default_rng(seed*10007+rep*977);rate=float(r.uniform(.88,1.12));den=100;num=max(60,int(round(rate*den)));y=resample_poly(x,den,num).astype(np.float32)
 y+=r.normal(0,.007+.002*min(rep,4),len(y)).astype(np.float32)
 if rep>=3:
  seg=max(256,len(y)//10);g=r.uniform(.80,1.20,12);idx=np.minimum(np.arange(len(y))//seg,11);y*=g[idx]
 return np.clip(y,-1,1).astype(np.float32)

def feat(sr,x,drop=False,noise=0,seed=0):
 if noise:x=x+np.random.default_rng(seed).normal(0,noise,len(x)).astype(np.float32)
 nper=max(128,int(sr*.025));hop=max(64,int(sr*.010));_,_,z=stft(x,fs=sr,nperseg=nper,noverlap=nper-hop,boundary=None,padded=False);mag=np.log1p(np.abs(z).T*20);edges=np.linspace(0,mag.shape[1],25,dtype=int);b=np.stack([mag[:,edges[i]:max(edges[i]+1,edges[i+1])].mean(1) for i in range(24)],1);e=np.log1p(np.sqrt(np.maximum(1e-9,np.mean(np.abs(z).T**2,1))))[:,None];d=np.vstack([np.zeros((1,24)),np.diff(b,axis=0)]);F=np.concatenate([b,d,e],1);F=(F-F.mean(0))/(F.std(0)+1e-4)
 if drop:F=F[e[:,0]>np.quantile(e[:,0],.32)]
 return F.astype(np.float32)
def hold(ai,oi):return ((ai*5+oi*3)%7)==0

def world(seed):
 base=[];tests=[];r=np.random.default_rng(seed)
 for ai,a in enumerate(ACTORS):
  for yi,v in enumerate(ACTIONS):
   for oi,o in enumerate(OBJECTS):
    if not hold(ai,oi):
     for voice in TRAIN_VOICES:
      for sp in SPEEDS:base.append((ai,yi,oi,a,v,o,voice,sp,44+((ai*3+oi)%13)))
    for voice in TEST_VOICES:
     for sp in [105,225]:
      sr,x=synth(a,v,o,voice,sp,57);kind='heldout_comp' if hold(ai,oi) else 'speaker_speed';tests.append((feat(sr,x),yi,kind));tests.append((feat(sr,x,drop=True),yi,'low_energy_removed'));tests.append((feat(sr,x,noise=.07,seed=seed+ai*31+oi*7+sp),yi,'hard_noise'))
 return base,tests

def encounter(spec,seed,rep):
 ai,y,oi,a,v,o,voice,sp,pitch=spec;sr,x=synth(a,v,o,voice,sp,pitch);return feat(sr,pert(sr,x,seed+ai*101+oi*17+y*13+sp,rep)),y

def fit_codebook(base,seed):
 r=np.random.default_rng(seed);idx=r.choice(len(base),min(650,len(base)),replace=False);parts=[]
 for j in idx:
  F,_=encounter(base[j],seed,0); parts.append(F[::max(1,len(F)//80)])
 X=np.concatenate(parts);sc=StandardScaler().fit(X);km=MiniBatchKMeans(K,random_state=seed,n_init=2,batch_size=4096,max_iter=120).fit(sc.transform(X));return sc,km
def code(F,sc,km):return tuple(map(int,km.predict(sc.transform(F))))

def propose_pool(base,seed,sc,km):
 r=np.random.default_rng(seed+99);idx=r.choice(len(base),min(320,len(base)),replace=False);cnt=Counter()
 for j in idx:
  F,_=encounter(base[j],seed,0);s=code(F,sc,km)
  for n in range(2,7):
   for i in range(0,len(s)-n+1,3):cnt[s[i:i+n]]+=1
 return {q for q,_ in cnt.most_common(PROP_MAX)}

def update_stats(s,y,pool,seen,cls):
 for n in range(2,7):
  for i in range(0,len(s)-n+1,2):
   q=s[i:i+n]
   if q in pool:seen[q]+=1;cls[q][y]+=1

def active_motifs(seen,cls):
 cand=[];prior=1/len(ACTIONS)
 for q,N in seen.items():
  if N<8:continue
  c=cls[q];pur=max(c.values())/N;ground=max(0,pur-prior)*math.log1p(N)*math.sqrt(len(q));gain=min(1.,.001*max(0,(len(q)-1)*N-(len(q)+3)))
  if ground>.18:cand.append((ground+gain,q))
 cand.sort(reverse=True);return [q for _,q in cand[:MOTIF_MAX]]
def idxmot(m):
 by=defaultdict(list)
 for q in m:by[q[0]].append((len(q),q))
 for z in by:by[z].sort(reverse=True)
 return by
def segment(s,by):
 out=[];i=0
 while i<len(s):
  hit=None
  for n,q in by.get(s[i],[]):
   if i+n<=len(s) and s[i:i+n]==q:hit=q;break
  if hit is None:out.append(('r',s[i]));i+=1
  else:out.append(('m',hit));i+=len(hit)
 return out

def hq(q,mod,salt):return int.from_bytes(hashlib.blake2b(repr((salt,q)).encode(),digest_size=8).digest(),'little')%mod

def sparse_rows(codes,labels,by):
 rr=[];cc=[];dd=[];cr=[];cc2=[];dd2=[];pr=[];pc=[];pd=[];rat=[]
 for row,s in enumerate(codes):
  c=Counter(s)
  for j,n in c.items():rr.append(row);cc.append(j);dd.append(n/len(s))
  u=segment(s,by);rat.append(len(u)/max(1,len(s)));cu=Counter();pa=Counter();prev=None
  for typ,q in u:
   z=('m',q) if typ=='m' else ('r',q);h=hq(z,CHASH,1);cu[h]+=1
   if prev is not None:pa[hq((prev,z),PHASH,2)]+=1
   prev=z
  denom=max(1,len(u))
  for j,n in cu.items():cr.append(row);cc2.append(j);dd2.append(n/denom)
  for j,n in pa.items():pr.append(row);pc.append(j);pd.append(n/max(1,len(u)-1))
 R=csr_matrix((dd,(rr,cc)),shape=(len(codes),K));C=csr_matrix((dd2,(cr,cc2)),shape=(len(codes),CHASH));P=csr_matrix((pd,(pr,pc)),shape=(len(codes),PHASH));return R,hstack([C,P],format='csr'),float(np.mean(rat))

def run(seed):
 base,tests=world(seed);sc,km=fit_codebook(base,seed);pool=propose_pool(base,seed,sc,km);seen=Counter();cls=defaultdict(Counter);allcodes=[];labels=[];rows=[];prev=0
 testcodes=[(code(F,sc,km),y,g) for F,y,g in tests]
 for dose in DOSES:
  for rep in range(prev,dose):
   for j,spec in enumerate(base):
    F,y=encounter(spec,seed,rep);s=code(F,sc,km);allcodes.append(s);labels.append(y);update_stats(s,y,pool,seen,cls)
  prev=dose;m=active_motifs(seen,cls);by=idxmot(m);R,C,ratio=sparse_rows(allcodes,labels,by);Y=np.asarray(labels);D=hstack([R,C],format='csr')
  models={'raw':LogisticRegression(max_iter=500,C=1.5).fit(R,Y),'chunk':LogisticRegression(max_iter=500,C=1.5).fit(C,Y),'dual':LogisticRegression(max_iter=500,C=1.5).fit(D,Y)}
  met={'seed':seed,'dose':dose,'train_n':len(Y),'motifs':len(m),'proposals':len(pool),'train_compression':1-ratio,'conditions':{}}
  for g in sorted(set(x[2] for x in testcodes)):
   sub=[x for x in testcodes if x[2]==g];tc=[x[0] for x in sub];ty=np.array([x[1] for x in sub]);TR,TC,tr=sparse_rows(tc,ty,by);TD=hstack([TR,TC],format='csr');met['conditions'][g]={'raw':float(np.mean(models['raw'].predict(TR)==ty)),'chunk':float(np.mean(models['chunk'].predict(TC)==ty)),'dual':float(np.mean(models['dual'].predict(TD)==ty)),'compression':1-tr}
  rows.append(met);(OUT/f'R32_TTS_STREAM_SEED_{seed}.json').write_text(json.dumps(rows,indent=2));print('SEED',seed,'DOSE',dose,'N',len(Y),'M',len(m),flush=True);gc.collect()
 return rows

def main():
 allr=[]
 # sequential by design: avoids OOM and preserves each completed seed checkpoint
 for seed in range(33500,33504):allr.extend(run(seed));print('DONE',seed,flush=True)
 agg={}
 for d in DOSES:
  rr=[x for x in allr if x['dose']==d];z={'train_n':float(np.mean([x['train_n'] for x in rr])),'motifs':float(np.mean([x['motifs'] for x in rr])),'train_compression':float(np.mean([x['train_compression'] for x in rr]))}
  for g in rr[0]['conditions']:
   for route in ['raw','chunk','dual','compression']:z[f'{g}_{route}']=float(np.mean([x['conditions'][g][route] for x in rr]))
  z['hard_mean_raw']=float(np.mean([z[f'{g}_raw'] for g in ['speaker_speed','low_energy_removed','hard_noise','heldout_comp']]));z['hard_mean_chunk']=float(np.mean([z[f'{g}_chunk'] for g in ['speaker_speed','low_energy_removed','hard_noise','heldout_comp']]));z['hard_mean_dual']=float(np.mean([z[f'{g}_dual'] for g in ['speaker_speed','low_energy_removed','hard_noise','heldout_comp']]));agg[str(d)]=z
 out={'aggregate':agg,'rows':allr,'boundary':'REFERENCE_ONLY bounded streaming TTS self-chunk dose curve. Fixed learned microstate codebook, capped proposal pool, reversible self-chunks, raw bypass, sparse grounded readouts. eSpeak generates waveforms only; no transcript, linguistic unit, VAD, ASR, tokenizer, transformer or LLM enters learner cognition.'};(OUT/'R32_TTS_SELF_CHUNK_STREAMING_REFERENCE_ONLY.json').write_text(json.dumps(out,indent=2));print(json.dumps(agg,indent=2))
if __name__=='__main__':main()
