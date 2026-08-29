from __future__ import annotations
import sys,json,hashlib
sys.path.insert(0,'/mnt/data/r32_epistemic')
import r32_tts_self_chunk_streaming as m
import numpy as np
from collections import Counter,defaultdict
from scipy.sparse import csr_matrix,hstack
from sklearn.linear_model import LogisticRegression
from pathlib import Path
OUT=Path('/mnt/data/r32_epistemic');B2=512;B3=1024

def raw_temporal(codes):
 rr=[];cc=[];dd=[];br=[];bc=[];bd=[];tr=[];tc=[];td=[]
 for row,s in enumerate(codes):
  n=max(1,len(s));c=Counter(s)
  for j,v in c.items():rr.append(row);cc.append(j);dd.append(v/n)
  c2=Counter((s[i]*131+s[i+1]*17)%B2 for i in range(len(s)-1))
  for j,v in c2.items():br.append(row);bc.append(j);bd.append(v/max(1,len(s)-1))
  c3=Counter((s[i]*65537+s[i+1]*257+s[i+2]*31)%B3 for i in range(len(s)-2))
  for j,v in c3.items():tr.append(row);tc.append(j);td.append(v/max(1,len(s)-2))
 U=csr_matrix((dd,(rr,cc)),shape=(len(codes),m.K));P=csr_matrix((bd,(br,bc)),shape=(len(codes),B2));T=csr_matrix((td,(tr,tc)),shape=(len(codes),B3));return U,hstack([U,P,T],format='csr')

def run(seed):
 base,tests=m.world(seed);sc,km=m.fit_codebook(base,seed);pool=m.propose_pool(base,seed,sc,km);seen=Counter();cls=defaultdict(Counter);codes=[];Y=[]
 for spec in base:
  F,y=m.encounter(spec,seed,0);s=m.code(F,sc,km);codes.append(s);Y.append(y);m.update_stats(s,y,pool,seen,cls)
 motifs=m.active_motifs(seen,cls);by=m.idxmot(motifs);U,R=raw_temporal(codes);_,C,_=m.sparse_rows(codes,Y,by);D=hstack([R,C],format='csr');Y=np.asarray(Y)
 models={'raw_unigram':LogisticRegression(max_iter=500,C=1.5).fit(U,Y),'raw_temporal':LogisticRegression(max_iter=500,C=1.5).fit(R,Y),'chunk':LogisticRegression(max_iter=500,C=1.5).fit(C,Y),'dual_temporal':LogisticRegression(max_iter=500,C=1.5).fit(D,Y)}
 te=[(m.code(F,sc,km),y,g) for F,y,g in tests];out={'seed':seed,'motifs':len(motifs),'conditions':{}}
 for g in sorted(set(z for _,_,z in te)):
  sub=[x for x in te if x[2]==g];ss=[x[0] for x in sub];yy=np.array([x[1] for x in sub]);TU,TR=raw_temporal(ss);_,TC,_=m.sparse_rows(ss,yy,by);TD=hstack([TR,TC],format='csr');out['conditions'][g]={
   'raw_unigram':float(np.mean(models['raw_unigram'].predict(TU)==yy)),'raw_temporal':float(np.mean(models['raw_temporal'].predict(TR)==yy)),'chunk':float(np.mean(models['chunk'].predict(TC)==yy)),'dual_temporal':float(np.mean(models['dual_temporal'].predict(TD)==yy))}
 return out

def main():
 rows=[]
 for seed in range(33700,33704):rows.append(run(seed));(OUT/f'R32_TTS_TEMPORAL_SEED_{seed}.json').write_text(json.dumps(rows[-1],indent=2));print('DONE',seed,flush=True)
 agg={}
 for g in rows[0]['conditions']:
  agg[g]={k:float(np.mean([r['conditions'][g][k] for r in rows])) for k in ['raw_unigram','raw_temporal','chunk','dual_temporal']}
 for k in ['raw_unigram','raw_temporal','chunk','dual_temporal']:agg['hard_mean_'+k]=float(np.mean([agg[g][k] for g in rows[0]['conditions']]))
 out={'aggregate':agg,'rows':rows,'boundary':'REFERENCE_ONLY temporal-information microscope. Raw route uses learner-derived acoustic microstates plus local transition/short-sequence statistics, not human linguistic units. No transcript, word/phoneme/chunk boundary, VAD, ASR, tokenizer, transformer or LLM enters learner cognition.'};(OUT/'R32_TTS_RAW_TEMPORAL_MICROSCOPE_REFERENCE_ONLY.json').write_text(json.dumps(out,indent=2));print(json.dumps(agg,indent=2))
if __name__=='__main__':main()
