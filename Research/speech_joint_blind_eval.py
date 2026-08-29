#!/usr/bin/env python3
"""Target-blind evaluation for the R29 joint acoustic core.

Candidate selection uses only learned CTC, attention, length, and presence evidence.
The transcript is used only after selection to score correctness. An oracle selector
is retained solely to quantify the inflation in the rejected earlier evaluator.
"""
import argparse,json
from pathlib import Path
import numpy as np, torch
import torch.nn as nn, torch.nn.functional as F
import speech_joint_core_r29 as j


def build_candidate_io(cands,C):
 U=max(1,max(len(s) for s in cands)+1);di=torch.full((len(cands),U),C+1,dtype=torch.long);do=torch.full((len(cands),U),-100,dtype=torch.long);flat=[];lens=[]
 for i,s in enumerate(cands):
  t=list(s)+[C];do[i,:len(t)]=torch.tensor(t)
  if len(t)>1:di[i,1:len(t)]=torch.tensor(t[:-1])
  flat.extend([q+1 for q in s]);lens.append(len(s))
 return di,do,torch.tensor(flat,dtype=torch.long),torch.tensor(lens,dtype=torch.long)

def model_scores(model,z,ol,cands,C):
 B=len(cands);di,do,flat,tl=build_candidate_io(cands,C)
 ao,_=model.dec.teacher(z,ol,di);ce=F.cross_entropy(ao.transpose(1,2),do,reduction='none',ignore_index=-100).sum(1)/(tl+1).clamp_min(1)
 logp=F.log_softmax(model.ctc(z),2).transpose(0,1);ctc=nn.CTCLoss(blank=0,zero_infinity=False,reduction='none')
 # Empty target sequences are given a blank-only CTC score manually.
 ctc_scores=torch.empty(B)
 non=torch.where(tl>0)[0]
 if len(non):
  # Build concatenated targets for selected rows.
  ff=[]
  for i in non.tolist():ff.extend([q+1 for q in cands[i]])
  ctc_scores[non]=ctc(logp[:,non],torch.tensor(ff),ol[non],tl[non])/tl[non].float().clamp_min(1)
 emp=torch.where(tl==0)[0]
 if len(emp):ctc_scores[emp]=-logp[:,emp,0].mean(0)
 pool=model.pooled(z,ol);ln=F.cross_entropy(model.length(pool),tl.clamp_max(model.length.out_features-1),reduction='none')
 pt=torch.zeros((B,C))
 for i,s in enumerate(cands):
  if s:pt[i,torch.tensor(sorted(set(s)))]=1
 pr=F.binary_cross_entropy_with_logits(model.pres(pool),pt,reduction='none').mean(1)
 # Same relative objective families used during training; all terms normalized.
 return (.42*ctc_scores+ce+.10*ln+.07*pr).detach().cpu().numpy(),{'ctc':ctc_scores.detach().cpu().numpy(),'attn':ce.detach().cpu().numpy(),'length':ln.detach().cpu().numpy(),'presence':pr.detach().cpu().numpy()}

def edit(a,b):return j.edit(a,b)
def metrics(pred,rows):
 ed=0;tok=0;ex=0;ins=dele=sub=0
 for p,q in zip(pred,rows):
  y=q.y.tolist();d=edit(p,y);ed+=d;tok+=len(y);ex+=p==y
  # Coarse attribution: length difference plus residual substitutions.
  if len(p)>len(y):ins+=len(p)-len(y)
  elif len(p)<len(y):dele+=len(y)-len(p)
  sub+=max(0,d-abs(len(p)-len(y)))
 return {'exact':ex/len(rows),'token_accuracy':1-ed/max(1,tok),'mean_edit':ed/len(rows),'insertions':ins,'deletions':dele,'substitution_residual':sub}

def evaluate(model,rows,C,batch=48):
 att=[];ctc=[];blind=[];oracle=[];agree=[];margins=[]
 for st in range(0,len(rows),batch):
  rr=rows[st:st+batch];x,l,_,_,_,_=j.collate(rr,C)
  with torch.no_grad():
   z,ol=model.encode(x,l);a=model.dec.greedy(z,ol,20);c=j.ctc_greedy(model.ctc(z),ol)
   # Score the two candidates independently per sample by duplicating its encoder.
   for i,q in enumerate(rr):
    cand=[a[i],c[i]]
    zz=z[i:i+1].repeat(2,1,1);oo=ol[i:i+1].repeat(2);sc,_=model_scores(model,zz,oo,cand,C);pick=int(np.argmin(sc));blind.append(cand[pick]);margins.append(float(abs(sc[0]-sc[1])));att.append(a[i]);ctc.append(c[i]);agree.append(a[i]==c[i]);oracle.append(min(cand,key=lambda s:edit(s,q.y.tolist())))
 return {'blind_selected':metrics(blind,rows),'attention_only':metrics(att,rows),'ctc_only':metrics(ctc,rows),'oracle_rejected':metrics(oracle,rows),'candidate_agreement':float(np.mean(agree)),'selection_margin':{'mean':float(np.mean(margins)),'p10':float(np.quantile(margins,.1)),'p50':float(np.quantile(margins,.5))}}

def condition(world,seed,name,n):
 if name=='recoverable_hard':return j.make_rows(world,n,seed+300000,'hard',(2,8),[18,19])
 if name=='inserted_silence':return j.make_rows(world,n,seed+400000,'hard',(2,8),[18,20],.42,0)
 if name=='endpoint_damage':return j.make_rows(world,n,seed+500000,'hard',(2,8),[19,20],.10,.28)
 if name=='severe':return j.make_rows(world,n,seed+600000,'severe',(2,8),[20,21])
 if name=='long_8_10':return j.make_rows(world,n,seed+700000,'hard',(8,10),[18,21])
 raise ValueError(name)

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--seed',type=int,required=True);ap.add_argument('--checkpoint',required=True);ap.add_argument('--condition',required=True);ap.add_argument('--n',type=int,default=400);ap.add_argument('--out',required=True);a=ap.parse_args();w=j.AcousticWorld(a.seed,16,30,False);m=j.JointPAM(16);ck=torch.load(a.checkpoint,map_location='cpu',weights_only=False);m.load_state_dict(ck['state_dict']);r=condition(w,a.seed,a.condition,a.n);res=evaluate(m,r,16);obj={'seed':a.seed,'checkpoint_epoch':ck.get('epoch'),'condition':a.condition,'trials':len(r),'results':res,'claim_boundary':'Target-blind raw-waveform selection. Oracle selector retained only as rejected inflation control.'};Path(a.out).parent.mkdir(parents=True,exist_ok=True);Path(a.out).write_text(json.dumps(obj,indent=2));print(json.dumps(obj,indent=2))
