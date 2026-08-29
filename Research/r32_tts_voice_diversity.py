from __future__ import annotations
import sys,json,random
sys.path.insert(0,'/mnt/data/r32_epistemic')
import r32_tts_self_chunk_streaming as m
import r32_tts_raw_temporal_microscope as rt
import numpy as np
from collections import Counter,defaultdict
from scipy.sparse import hstack
from sklearn.cluster import MiniBatchKMeans
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from pathlib import Path
OUT=Path('/mnt/data/r32_epistemic')
SETS={
 'voices2':['en-us','en-sc'],
 'voices4':['en-us','en-sc','en-uk-north','en-uk-wmids'],
 'voices6':['en-us','en-sc','en-uk-north','en-uk-wmids','en-gb','en'],
 'voices6_pitch':['en-us','en-sc','en-uk-north','en-uk-wmids','en-gb','en'],
}
NTRAIN=2232

def make_pool(voices,pitchdiv=False):
 pool=[]
 pitches=[38,50,62] if pitchdiv else [50]
 for ai,a in enumerate(m.ACTORS):
  for y,v in enumerate(m.ACTIONS):
   for oi,o in enumerate(m.OBJECTS):
    if m.hold(ai,oi):continue
    for voice in voices:
     for sp in [135,165,195]:
      for pitch in pitches: pool.append((ai,y,oi,a,v,o,voice,sp,pitch))
 return pool

def make_tests(seed):
 tests=[]
 for ai,a in enumerate(m.ACTORS):
  for y,v in enumerate(m.ACTIONS):
   for oi,o in enumerate(m.OBJECTS):
    for voice in ['en-uk-rp','en-wi']:
     for sp in [105,225]:
      sr,x=m.synth(a,v,o,voice,sp,57); kind='heldout_comp' if m.hold(ai,oi) else 'speaker_speed';tests.append((m.feat(sr,x),y,kind));tests.append((m.feat(sr,x,drop=True),y,'low_energy_removed'));tests.append((m.feat(sr,x,noise=.07,seed=seed+ai*31+oi*7+sp),y,'hard_noise'))
 return tests

def run(seed,name):
 voices=SETS[name];pool=make_pool(voices,name.endswith('_pitch'));rng=np.random.default_rng(seed+len(name)*101)
 idx=rng.choice(len(pool),NTRAIN,replace=(len(pool)<NTRAIN));specs=[pool[int(i)] for i in idx]
 # fit learned microstate codebook from exactly the selected developmental samples
 parts=[]
 for spec in specs[:min(700,len(specs))]:
  F,_=m.encounter(spec,seed,0);parts.append(F[::max(1,len(F)//80)])
 X=np.concatenate(parts);sc=StandardScaler().fit(X);km=MiniBatchKMeans(m.K,random_state=seed,n_init=2,batch_size=4096,max_iter=120).fit(sc.transform(X))
 def code(F):return tuple(map(int,km.predict(sc.transform(F))))
 # candidate motif pool from selected experience only
 cnt=Counter()
 for spec in specs[:min(420,len(specs))]:
  F,_=m.encounter(spec,seed,0);s=code(F)
  for n in range(2,7):
   for i in range(0,len(s)-n+1,3):cnt[s[i:i+n]]+=1
 prop={q for q,_ in cnt.most_common(m.PROP_MAX)};seen=Counter();cls=defaultdict(Counter);codes=[];Y=[]
 for spec in specs:
  F,y=m.encounter(spec,seed,0);s=code(F);codes.append(s);Y.append(y);m.update_stats(s,y,prop,seen,cls)
 motifs=m.active_motifs(seen,cls);by=m.idxmot(motifs);Y=np.asarray(Y);U,R=rt.raw_temporal(codes);_,C,_=m.sparse_rows(codes,Y,by);D=hstack([R,C],format='csr')
 models={'raw_temporal':LogisticRegression(max_iter=600,C=1.5).fit(R,Y),'chunk':LogisticRegression(max_iter=600,C=1.5).fit(C,Y),'dual_temporal':LogisticRegression(max_iter=600,C=1.5).fit(D,Y)}
 tests=[(code(F),y,g) for F,y,g in make_tests(seed)];out={'seed':seed,'condition':name,'voices':len(voices),'train_n':len(Y),'motifs':len(motifs),'metrics':{}}
 for cond in sorted(set(z for _,_,z in tests)):
  sub=[x for x in tests if x[2]==cond];ss=[x[0] for x in sub];yy=np.asarray([x[1] for x in sub]);_,TR=rt.raw_temporal(ss);_,TC,_=m.sparse_rows(ss,yy,by);TD=hstack([TR,TC],format='csr');out['metrics'][cond]={k:float(np.mean(models[k].predict({'raw_temporal':TR,'chunk':TC,'dual_temporal':TD}[k])==yy)) for k in models}
 return out

def main():
 rows=[]
 for seed in range(34000,34003):
  for name in SETS:
   r=run(seed,name);rows.append(r);(OUT/f'R32_TTS_VOICE_{seed}_{name}.json').write_text(json.dumps(r,indent=2));print('DONE',seed,name,flush=True)
 agg={}
 for name in SETS:
  rr=[r for r in rows if r['condition']==name];agg[name]={}
  for route in ['raw_temporal','chunk','dual_temporal']:
   agg[name][route]={c:float(np.mean([r['metrics'][c][route] for r in rr])) for c in rr[0]['metrics']};agg[name][route]['hard_mean']=float(np.mean(list(agg[name][route].values())))
 out={'aggregate':agg,'rows':rows,'boundary':'REFERENCE_ONLY matched voice-diversity training experiment. Total developmental utterance count held fixed. eSpeak is waveform generator only; learner sees raw waveform-derived microstates, endogenous chunks and grounded action consequences. No transcript, word/phoneme/token boundary, VAD, ASR, transformer or LLM enters cognition.'};(OUT/'R32_TTS_VOICE_DIVERSITY_REFERENCE_ONLY.json').write_text(json.dumps(out,indent=2));print(json.dumps(agg,indent=2))
if __name__=='__main__':main()
