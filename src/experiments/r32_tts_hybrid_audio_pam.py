from __future__ import annotations
import sys,json
sys.path.insert(0,'/mnt/data/r32_epistemic')
import r32_tts_self_chunk_streaming as m
import r32_tts_raw_temporal_microscope as rt
import r32_tts_contrastive_families as fam
import numpy as np
from collections import Counter,defaultdict
from scipy.sparse import hstack
from sklearn.linear_model import LogisticRegression
from pathlib import Path
OUT=Path('/mnt/data/r32_epistemic')
FAM_SPECS=[('intrinsic96',96,False),('grounded48',48,True)]

def acc(model,X,y): return float(np.mean(model.predict(X)==y))

def run(seed):
 base,tests=m.world(seed); sc,km=m.fit_codebook(base,seed); pool=m.propose_pool(base,seed,sc,km)
 seen=Counter(); cls=defaultdict(Counter); codes=[];Y=[]
 for spec in base:
  F,y=m.encounter(spec,seed,0); s=m.code(F,sc,km); codes.append(s);Y.append(y);m.update_stats(s,y,pool,seen,cls)
 motifs=m.active_motifs(seen,cls); by=m.idxmot(motifs); Y=np.asarray(Y)
 U,R=rt.raw_temporal(codes); _,C,_=m.sparse_rows(codes,Y,by)
 models={
   'raw_unigram':LogisticRegression(max_iter=600,C=1.5).fit(U,Y),
   'raw_temporal':LogisticRegression(max_iter=600,C=1.5).fit(R,Y),
   'exact_chunk':LogisticRegression(max_iter=600,C=1.5).fit(C,Y),
   'raw_temporal_exact_dual':LogisticRegression(max_iter=600,C=1.5).fit(hstack([R,C],format='csr'),Y),
 }
 famstate={}
 for name,k,g in FAM_SPECS:
  fmap,kk=fam.fam_map(motifs,cls,k,g,seed+k+(1000 if g else 0)); FC,_=fam.fam_sparse(codes,by,fmap,kk)
  models[name]=LogisticRegression(max_iter=600,C=1.5).fit(FC,Y)
  models[name+'_temporal_dual']=LogisticRegression(max_iter=600,C=1.5).fit(hstack([R,FC],format='csr'),Y)
  famstate[name]=(fmap,kk)
 test=[(m.code(F,sc,km),y,g) for F,y,g in tests]
 out={'seed':seed,'motifs':len(motifs),'conditions':{}}
 for cond in sorted(set(z for _,_,z in test)):
  sub=[x for x in test if x[2]==cond]; ss=[x[0] for x in sub]; yy=np.asarray([x[1] for x in sub]); TU,TR=rt.raw_temporal(ss);_,TC,_=m.sparse_rows(ss,yy,by)
  z={'raw_unigram':acc(models['raw_unigram'],TU,yy),'raw_temporal':acc(models['raw_temporal'],TR,yy),'exact_chunk':acc(models['exact_chunk'],TC,yy),'raw_temporal_exact_dual':acc(models['raw_temporal_exact_dual'],hstack([TR,TC],format='csr'),yy)}
  for name,_,_ in FAM_SPECS:
   fmap,kk=famstate[name]; FC,_=fam.fam_sparse(ss,by,fmap,kk);z[name]=acc(models[name],FC,yy);z[name+'_temporal_dual']=acc(models[name+'_temporal_dual'],hstack([TR,FC],format='csr'),yy)
  out['conditions'][cond]=z
 return out

def main():
 rows=[]
 for seed in range(33800,33804):
  r=run(seed); rows.append(r); (OUT/f'R32_TTS_HYBRID_SEED_{seed}.json').write_text(json.dumps(r,indent=2));print('DONE',seed,flush=True)
 keys=list(rows[0]['conditions'][next(iter(rows[0]['conditions']))]); agg={}
 for k in keys:
  agg[k]={c:float(np.mean([r['conditions'][c][k] for r in rows])) for c in rows[0]['conditions']}; agg[k]['hard_mean']=float(np.mean(list(agg[k].values())))
 out={'aggregate':agg,'rows':rows,'boundary':'REFERENCE_ONLY hybrid acoustic PAM microscope. Learner receives raw TTS waveform-derived generic microstates, local temporal transitions, endogenous chunks, and grounded action consequences only. Chunk families are learned from chunk intrinsic structure and optionally consequence distributions. No transcript, word/phoneme/token/chunk boundary, VAD, ASR, transformer or LLM enters cognition.'}; (OUT/'R32_TTS_HYBRID_AUDIO_PAM_REFERENCE_ONLY.json').write_text(json.dumps(out,indent=2));print(json.dumps(agg,indent=2))
if __name__=='__main__':main()
