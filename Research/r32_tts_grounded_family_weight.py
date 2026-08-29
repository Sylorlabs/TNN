from __future__ import annotations
import sys,json
sys.path.insert(0,'/mnt/data/r32_epistemic')
import r32_tts_self_chunk_streaming as m
import r32_tts_raw_temporal_microscope as rt
import r32_tts_contrastive_families as f0
import numpy as np
from collections import Counter,defaultdict
from scipy.sparse import hstack
from sklearn.cluster import MiniBatchKMeans
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from pathlib import Path
OUT=Path('/mnt/data/r32_epistemic'); SPECS=[('intrinsic48',48,0.0),('ground2p5_48',48,2.5),('ground10_48',48,10.0),('ground30_48',48,30.0),('groundonly24',24,-1.0)]

def fmap_weight(motifs,cls,k,gw,seed):
 X=[]
 for q in motifs:
  g=np.array([cls[q].get(y,0) for y in range(len(m.ACTIONS))],float);g/=max(1e-9,g.sum())
  if gw<0:
   # grounding geometry + length/support-scale without acoustic identity; avoids a literal six-class table
   z=np.concatenate([g,np.array([len(q)/6.0, np.log1p(sum(cls[q].values()))/8.0])])
  else:
   h=np.bincount(np.asarray(q),minlength=m.K).astype(float);h/=max(1,h.sum());tr=np.zeros(64)
   for a,b in zip(q[:-1],q[1:]):tr[(a*31+b*17)%64]+=1
   if tr.sum():tr/=tr.sum()
   z=np.concatenate([h,tr,np.array([len(q)/6.0]),g*gw])
  X.append(z)
 X=StandardScaler().fit_transform(np.stack(X)); kk=min(k,len(motifs));lab=MiniBatchKMeans(kk,random_state=seed,n_init=5,batch_size=512,max_iter=200).fit_predict(X);return {q:int(a) for q,a in zip(motifs,lab)},kk

def run(seed):
 base,tests=m.world(seed);sc,km=m.fit_codebook(base,seed);pool=m.propose_pool(base,seed,sc,km);seen=Counter();cls=defaultdict(Counter);codes=[];Y=[]
 for spec in base:
  F,y=m.encounter(spec,seed,0);s=m.code(F,sc,km);codes.append(s);Y.append(y);m.update_stats(s,y,pool,seen,cls)
 motifs=m.active_motifs(seen,cls);by=m.idxmot(motifs);Y=np.asarray(Y);U,R=rt.raw_temporal(codes);out={'seed':seed,'motifs':len(motifs),'modes':{}}
 test=[(m.code(F,sc,km),y,g) for F,y,g in tests]
 for name,k,gw in SPECS:
  fm,kk=fmap_weight(motifs,cls,k,gw,seed+k+int(max(0,gw)*13));FC,_=f0.fam_sparse(codes,by,fm,kk); model=LogisticRegression(max_iter=600,C=1.5).fit(FC,Y);dual=LogisticRegression(max_iter=600,C=1.5).fit(hstack([R,FC],format='csr'),Y);z={};zd={}
  for cond in sorted(set(x[2] for x in test)):
   sub=[x for x in test if x[2]==cond];ss=[x[0] for x in sub];yy=np.asarray([x[1] for x in sub]);_,TR=rt.raw_temporal(ss);TC,_=f0.fam_sparse(ss,by,fm,kk);z[cond]=float(np.mean(model.predict(TC)==yy));zd[cond]=float(np.mean(dual.predict(hstack([TR,TC],format='csr'))==yy))
  out['modes'][name]=z;out['modes'][name+'_temporal_dual']=zd
 return out

def main():
 rows=[]
 for seed in range(33900,33904):
  r=run(seed);rows.append(r);(OUT/f'R32_TTS_GROUND_FAMILY_SEED_{seed}.json').write_text(json.dumps(r,indent=2));print('DONE',seed,flush=True)
 agg={}
 for mode in rows[0]['modes']:
  agg[mode]={c:float(np.mean([r['modes'][mode][c] for r in rows])) for c in rows[0]['modes'][mode]};agg[mode]['hard_mean']=float(np.mean(list(agg[mode].values())))
 out={'aggregate':agg,'rows':rows,'boundary':'REFERENCE_ONLY grounding-weight family ablation. Families are formed only from learner-recruited chunks and distributions of experienced grounded action consequences, optionally combined with intrinsic microstructure. No transcript, word/phoneme/token boundary, VAD, ASR, transformer or LLM enters cognition.'};(OUT/'R32_TTS_GROUNDED_FAMILY_WEIGHT_REFERENCE_ONLY.json').write_text(json.dumps(out,indent=2));print(json.dumps(agg,indent=2))
if __name__=='__main__':main()
