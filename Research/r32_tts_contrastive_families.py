from __future__ import annotations
import sys,json,math
sys.path.insert(0,'/mnt/data/r32_epistemic')
import r32_tts_self_chunk_streaming as m
import numpy as np
from collections import Counter,defaultdict
from scipy.sparse import csr_matrix,hstack
from sklearn.cluster import MiniBatchKMeans
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from pathlib import Path
OUT=Path('/mnt/data/r32_epistemic');FAMS=[24,48,96]

def motif_sig(q,ground=None,gw=0.0):
 h=np.bincount(np.asarray(q),minlength=m.K).astype(float);h/=max(1,h.sum());tr=np.zeros(64,float)
 for a,b in zip(q[:-1],q[1:]):tr[(a*31+b*17)%64]+=1
 if tr.sum():tr/=tr.sum()
 z=[h,tr,np.array([len(q)/6.0])]
 if ground is not None:
  g=np.asarray(ground,float);g/=max(1e-9,g.sum());z.append(g*gw)
 return np.concatenate(z)

def fam_map(motifs,cls,k,grounded,seed):
 X=[]
 for q in motifs:
  g=[cls[q].get(y,0) for y in range(len(m.ACTIONS))]
  X.append(motif_sig(q,g if grounded else None,2.5 if grounded else 0))
 X=np.stack(X);X=StandardScaler().fit_transform(X);kk=min(k,len(motifs));lab=MiniBatchKMeans(kk,random_state=seed,n_init=5,batch_size=512,max_iter=200).fit_predict(X);return {q:int(a) for q,a in zip(motifs,lab)},kk

def fam_sparse(codes,by,fmap,kfam):
 rr=[];cc=[];dd=[];pr=[];pc=[];pd=[];rat=[]
 for row,s in enumerate(codes):
  u=m.segment(s,by);rat.append(len(u)/max(1,len(s)));c=Counter();p=Counter();prev=None
  for typ,q in u:
   if typ=='m':z=fmap[q]
   else:z=kfam+(q%m.K)
   c[z]+=1
   if prev is not None:p[(prev*131+z*17)%128]+=1
   prev=z
  den=max(1,len(u))
  for j,n in c.items():rr.append(row);cc.append(j);dd.append(n/den)
  for j,n in p.items():pr.append(row);pc.append(j);pd.append(n/max(1,len(u)-1))
 C=csr_matrix((dd,(rr,cc)),shape=(len(codes),kfam+m.K));P=csr_matrix((pd,(pr,pc)),shape=(len(codes),128));return hstack([C,P],format='csr'),float(np.mean(rat))

def run(seed):
 base,tests=m.world(seed);sc,km=m.fit_codebook(base,seed);pool=m.propose_pool(base,seed,sc,km);seen=Counter();cls=defaultdict(Counter);codes=[];Y=[]
 # One full developmental dose, matched to first streaming checkpoint.
 for spec in base:
  F,y=m.encounter(spec,seed,0);s=m.code(F,sc,km);codes.append(s);Y.append(y);m.update_stats(s,y,pool,seen,cls)
 motifs=m.active_motifs(seen,cls);by=m.idxmot(motifs);R,C,ratio=m.sparse_rows(codes,Y,by);Y=np.asarray(Y);test=[(m.code(F,sc,km),y,g) for F,y,g in tests]
 out={'seed':seed,'motifs':len(motifs),'compression':1-ratio,'modes':{}}
 # exact current self-chunk route
 exact=LogisticRegression(max_iter=500,C=1.5).fit(C,Y);dual=LogisticRegression(max_iter=500,C=1.5).fit(hstack([R,C],format='csr'),Y)
 for name,model,dualflag in [('exact',exact,False),('exact_dual',dual,True)]:
  z={}
  for g in sorted(set(x[2] for x in test)):
   sub=[x for x in test if x[2]==g];ss=[x[0] for x in sub];yy=np.array([x[1] for x in sub]);TR,TC,_=m.sparse_rows(ss,yy,by);X=hstack([TR,TC],format='csr') if dualflag else TC;z[g]=float(np.mean(model.predict(X)==yy))
  out['modes'][name]=z
 for grounded in [False,True]:
  for k in FAMS:
   fmap,kk=fam_map(motifs,cls,k,grounded,seed+k);FC,_=fam_sparse(codes,by,fmap,kk);FD=hstack([R,FC],format='csr');fm=LogisticRegression(max_iter=500,C=1.5).fit(FC,Y);dm=LogisticRegression(max_iter=500,C=1.5).fit(FD,Y);name=('grounded' if grounded else 'intrinsic')+f'_{k}'
   z={};zd={}
   for g in sorted(set(x[2] for x in test)):
    sub=[x for x in test if x[2]==g];ss=[x[0] for x in sub];yy=np.array([x[1] for x in sub]);TR,_,_=m.sparse_rows(ss,yy,by);TC,_=fam_sparse(ss,by,fmap,kk);z[g]=float(np.mean(fm.predict(TC)==yy));zd[g]=float(np.mean(dm.predict(hstack([TR,TC],format='csr'))==yy))
   out['modes'][name]=z;out['modes'][name+'_dual']=zd
 return out

def main():
 rows=[]
 for seed in range(33600,33604):rows.append(run(seed));(OUT/f'R32_TTS_FAMILY_SEED_{seed}.json').write_text(json.dumps(rows[-1],indent=2));print('DONE',seed,flush=True)
 modes=list(rows[0]['modes']);agg={}
 for mode in modes:
  agg[mode]={g:float(np.mean([r['modes'][mode][g] for r in rows])) for g in rows[0]['modes'][mode]};agg[mode]['hard_mean']=float(np.mean(list(agg[mode].values())))
 out={'aggregate':agg,'rows':rows,'boundary':'REFERENCE_ONLY naturalistic TTS self-chunk family test. Families are learned from recruited chunk intrinsic microstructure, optionally plus distributions of experienced grounded action consequences. No transcript, word/phoneme/token, VAD, ASR, transformer or LLM enters learner cognition.'};(OUT/'R32_TTS_CONTRASTIVE_FAMILIES_REFERENCE_ONLY.json').write_text(json.dumps(out,indent=2));print(json.dumps(agg,indent=2))
if __name__=='__main__':main()
