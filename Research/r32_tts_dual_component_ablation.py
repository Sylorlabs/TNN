from __future__ import annotations
import gc,json,os
from pathlib import Path
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
import r32_tts_segmental_pam as d
OUT=Path('/mnt/data/r32_epistemic');torch.set_num_threads(max(1,min(5,os.cpu_count() or 1)))
MODES=['full','raw_only','segment_only_aux','event_only_aux','no_event','gate_mean','gate_reverse','gate_permute']

class ComponentPAM(nn.Module):
 def __init__(self,mode,dim=49,hid=80,classes=6):
  super().__init__();self.mode=mode
  self.front=nn.Sequential(nn.Conv1d(dim,hid,7,stride=2,padding=3),nn.GELU(),nn.Conv1d(hid,hid,5,padding=4,dilation=2),nn.GELU(),nn.Conv1d(hid,hid,5,padding=8,dilation=4),nn.GELU())
  self.boundary=nn.Sequential(nn.Conv1d(hid,32,3,padding=1),nn.GELU(),nn.Conv1d(32,1,1))
  self.out=nn.Sequential(nn.Linear(hid*5,160),nn.GELU(),nn.Dropout(.18),nn.Linear(160,classes))
 def gate_transform(self,b,mask):
  if self.mode=='gate_mean':
   m=b.sum(1,keepdim=True)/mask.sum(1,keepdim=True).clamp(min=1);return m*mask
  if self.mode=='gate_reverse':return torch.flip(b,[1])*mask
  if self.mode=='gate_permute':
   T=b.shape[1];t=torch.arange(T,device=b.device,dtype=torch.float32);key=torch.frac(torch.sin(t*12.9898)*43758.5453);idx=torch.argsort(key);return b[:,idx]*mask
  return b
 def forward(self,x,lengths):
  h=self.front(x.transpose(1,2)).transpose(1,2);l=torch.div(lengths+1,2,rounding_mode='floor').clamp(min=1,max=h.shape[1]);mask=torch.arange(h.shape[1],device=h.device)[None,:]<l[:,None]
  b=torch.sigmoid(self.boundary(h.transpose(1,2)).transpose(1,2).squeeze(-1))*mask;b=self.gate_transform(b,mask)
  raw_max=h.masked_fill(~mask[:,:,None],-1e4).amax(1);raw_mean=(h*mask[:,:,None]).sum(1)/l[:,None]
  acc=torch.zeros((h.shape[0],h.shape[2]),device=h.device);cnt=torch.zeros((h.shape[0],1),device=h.device);states=[]
  for t in range(h.shape[1]):
   g=b[:,t:t+1];acc=h[:,t]+(1-g)*acc;cnt=1+(1-g)*cnt;states.append(acc/cnt.clamp(min=1))
  s=torch.stack(states,1);seg_max=s.masked_fill(~mask[:,:,None],-1e4).amax(1);seg_mean=(s*mask[:,:,None]).sum(1)/l[:,None];event=(h*b[:,:,None]).sum(1)/(b.sum(1,keepdim=True)+1e-5);zero=torch.zeros_like(raw_max)
  if self.mode=='raw_only':seg_max=zero;seg_mean=zero;event=zero
  elif self.mode=='event_only_aux':seg_max=zero;seg_mean=zero
  elif self.mode in ('segment_only_aux','no_event'):event=zero
  z=self.out(torch.cat([raw_max,raw_mean,seg_max,seg_mean,event],1));return z,b.sum()/mask.sum().clamp(min=1)

def ev(m,dl):
 m.eval();ok=n=0;by={};rr=[]
 with torch.no_grad():
  for x,l,y,c in dl:
   z,r=m(x,l);p=z.argmax(1);ok+=int((p==y).sum());n+=len(y);rr.append(float(r))
   for i,k in enumerate(c):a=by.setdefault(k,[0,0]);a[0]+=int(p[i]==y[i]);a[1]+=1
 return ok/n,{k:a/b for k,(a,b) in by.items()},float(np.mean(rr))

def train(m,tr,dev,seed,epochs=5):
 torch.manual_seed(seed);g=torch.Generator().manual_seed(seed);tl=DataLoader(tr,batch_size=32,shuffle=True,generator=g,collate_fn=d.collate,num_workers=0);dl=DataLoader(dev,batch_size=64,shuffle=False,collate_fn=d.collate,num_workers=0);opt=torch.optim.AdamW(m.parameters(),lr=1.8e-3,weight_decay=2e-4);best=None;bs=-1;hist=[]
 for ep in range(1,epochs+1):
  m.train();ls=[];rs=[]
  for x,l,y,_ in tl:
   opt.zero_grad(set_to_none=True);z,r=m(x,l);loss=F.cross_entropy(z,y)+(.004*r if m.mode in ('full','no_event','segment_only_aux','event_only_aux') else 0);loss.backward();torch.nn.utils.clip_grad_norm_(m.parameters(),4);opt.step();ls.append(float(loss.detach()));rs.append(float(r.detach()))
  ac,_,_=ev(m,dl);hist.append({'epoch':ep,'loss':float(np.mean(ls)),'dev':ac,'gate_rate':float(np.mean(rs))})
  if ac>bs:bs=ac;best={k:v.detach().cpu().clone() for k,v in m.state_dict().items()}
  if ep in (1,2,3,4,5):print('EPOCH',m.mode,ep,hist[-1],flush=True)
  # The development split is only a stopping signal. Stop uniformly after two
  # consecutive saturated checks; hostile held-out conditions remain untouched.
  if ep>=2 and hist[-1]['dev']>=.999 and hist[-2]['dev']>=.999: break
 m.load_state_dict(best);return hist

def main(seed=35300):
 specs,test=d.build_specs(seed,2);rng=np.random.default_rng(seed);ix=np.arange(len(specs));rng.shuffle(ix);nd=max(240,int(.12*len(ix)));dv=set(map(int,ix[:nd]));tr=d.AcousticDataset([s for i,s in enumerate(specs) if i not in dv],seed);dev=d.AcousticDataset([s for i,s in enumerate(specs) if i in dv],seed+91);te=d.AcousticDataset(test,seed+193);dl=DataLoader(te,batch_size=64,shuffle=False,collate_fn=d.collate,num_workers=0);res={'seed':seed,'models':{}}
 for i,mode in enumerate(MODES):
  print('MODEL',mode,flush=True);m=ComponentPAM(mode);hist=train(m,tr,dev,seed+i*1000);ac,c,r=ev(m,dl);keys=['speaker_speed','hard_noise','heldout_comp',*d.TEST_TEMPLATES.keys()];hard=float(np.mean([c[k] for k in keys]));res['models'][mode]={'overall':ac,'hard_mean':hard,'conditions':c,'gate_rate':r,'history':hist,'extreme_flags':[k for k,v in c.items() if v in (0.,1.)]};print('RESULT',mode,res['models'][mode],flush=True);del m;gc.collect()
 out={'result':res,'ranking':sorted([(v['hard_mean'],k) for k,v in res['models'].items()],reverse=True),'boundary':'REFERENCE_ONLY matched dual-route component and gate-location ablation. No transcript, supplied boundary, VAD, ASR, transformer, attention, fixed tokenizer or LLM.'};(OUT/'R32_TTS_DUAL_COMPONENT_ABLATION_REFERENCE_ONLY.json').write_text(json.dumps(out,indent=2));(OUT/f'R32_DUAL_COMPONENT_SEED_{seed}.json').write_text(json.dumps(res,indent=2));print(json.dumps(out['ranking'],indent=2))
if __name__=='__main__':main()
