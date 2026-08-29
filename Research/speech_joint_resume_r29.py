#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math,random,time
from pathlib import Path
import numpy as np, torch
import torch.nn as nn, torch.nn.functional as F
import speech_joint_core_r29 as j

def run(seed,checkpoint,out_dir,start_epoch,end_epoch,total_epochs=64,steps=52,batch=64,final_eval=True):
 torch.manual_seed(seed);np.random.seed(seed);random.seed(seed);world=j.AcousticWorld(seed,16,30,False);model=j.JointPAM(16)
 ck=torch.load(checkpoint,map_location='cpu',weights_only=False);model.load_state_dict(ck['state_dict']);assert ck['seed']==seed
 rng=np.random.default_rng(seed+9+start_epoch*100003)
 iso=[]
 for c in range(16):
  for _ in range(110):iso.append(world.utterance(rng,'hard',1,range(14),0,0,True))
 ctc=nn.CTCLoss(blank=0,zero_infinity=True);opt=torch.optim.AdamW(model.parameters(),lr=7e-4,weight_decay=1.5e-4)
 val=j.make_rows(world,280,seed+200000,'hard',(2,7),[16,17]);base=j.eval_rows(model,val,16);bestsc=base['exact']+.45*base['token_accuracy'];best={k:v.detach().cpu().clone() for k,v in model.state_dict().items()};bestep=start_epoch
 out=Path(out_dir);out.mkdir(parents=True,exist_ok=True);hist=[];t0=time.time()
 print(json.dumps({'resume_from':start_epoch,'base_val':base,'base_score':bestsc}),flush=True)
 for ep in range(start_epoch,end_epoch):
  p=(ep+1)/total_epochs;tier='clean' if ep<6 else ('hard' if ep<int(.82*total_epochs) else 'severe');lr=1.4e-3*(.12+.88*(1+math.cos(math.pi*p))/2)
  for g in opt.param_groups:g['lr']=lr
  model.train();losses=[]
  for _ in range(steps):
   rr=j.make_rows(world,batch,int(rng.integers(0,2**31-1)),tier,(2,7),range(16));x,l,ct,cl,di,do=j.collate(rr,16);opt.zero_grad();z,ol=model.encode(x,l);pool=model.pooled(z,ol)
   lc=ctc(F.log_softmax(model.ctc(z),2).transpose(0,1),ct,ol,cl);ao,att=model.dec.teacher(z,ol,di);la=F.cross_entropy(ao.reshape(-1,17),do.reshape(-1),ignore_index=-100,label_smoothing=.02)
   ll=F.cross_entropy(model.length(pool),cl.clamp_max(9));pr=F.binary_cross_entropy_with_logits(model.pres(pool),j.presence_target(rr,16))
   idx=rng.integers(0,len(iso),min(24,batch));ir=[iso[int(i)] for i in idx];ix,il,_,_,_,_=j.collate(ir,16);iz,iol=model.encode(ix,il);li=F.cross_entropy(model.iso(model.pooled(iz,iol)),torch.tensor([int(q.y[0]) for q in ir]))
   loss=.42*lc+la+.10*ll+.07*pr+.12*li;loss.backward();torch.nn.utils.clip_grad_norm_(model.parameters(),4.);opt.step();losses.append(float(loss))
  ev=j.eval_rows(model,val,16);sc=ev['exact']+.45*ev['token_accuracy'];row={'epoch':ep+1,'loss':float(np.mean(losses)),'tier':tier,'val':ev,'score':sc,'elapsed':time.time()-t0};hist.append(row);print(json.dumps(row),flush=True)
  if sc>bestsc:bestsc=sc;bestep=ep+1;best={k:v.detach().cpu().clone() for k,v in model.state_dict().items()}
  torch.save({'state_dict':best,'seed':seed,'epoch':bestep,'best_val_score':bestsc},out/'best.pt')
 model.load_state_dict(best);tests={}
 if final_eval:
  sets={
   'recoverable_hard':j.make_rows(world,800,seed+300000,'hard',(2,8),[18,19]),
   'inserted_silence':j.make_rows(world,600,seed+400000,'hard',(2,8),[18,20],.42,0),
   'endpoint_damage':j.make_rows(world,600,seed+500000,'hard',(2,8),[19,20],.10,.28),
   'severe':j.make_rows(world,800,seed+600000,'severe',(2,8),[20,21]),
   'long_8_10':j.make_rows(world,500,seed+700000,'hard',(8,10),[18,21]),
  }
  twin=j.AcousticWorld(seed+33,16,30,True);sets['near_twin_stress']=j.make_rows(twin,600,seed+800000,'hard',(2,8),[18,19])
  tests={k:j.eval_rows(model,v,16) for k,v in sets.items()}
 obj={'seed':seed,'resumed_from_epoch':start_epoch,'end_epoch':end_epoch,'best_epoch':bestep,'best_val_score':bestsc,'base_val':base,'history':hist,'results':tests,'claim_boundary':'Resumed Python reference of generic raw-waveform CTC+attention core; no VAD, boundaries, phonemes, text, pretrained audio, or language model.'}
 (out/'segment_result.json').write_text(json.dumps(obj,indent=2));print(json.dumps({'best_epoch':bestep,'best_val_score':bestsc,'results':tests},indent=2));return obj

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--seed',type=int,required=True);ap.add_argument('--checkpoint',required=True);ap.add_argument('--out-dir',required=True);ap.add_argument('--start-epoch',type=int,required=True);ap.add_argument('--end-epoch',type=int,required=True);ap.add_argument('--steps',type=int,default=52);ap.add_argument('--batch',type=int,default=64);ap.add_argument('--no-final-eval',action='store_true');a=ap.parse_args();run(a.seed,a.checkpoint,a.out_dir,a.start_epoch,a.end_epoch,64,a.steps,a.batch,not a.no_final_eval)
