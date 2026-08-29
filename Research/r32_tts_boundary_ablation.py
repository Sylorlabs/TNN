from __future__ import annotations
import gc,json,os
from pathlib import Path
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
import r32_tts_segmental_pam as d

OUT=Path('/mnt/data/r32_epistemic')
torch.set_num_threads(max(1,min(5,os.cpu_count() or 1)))
MODES=['learned','no_reset','periodic','pseudo_random','shifted_learned','all_reset']

class BoundaryAblationPAM(nn.Module):
    def __init__(self,mode:str,dim=49,hidden=80,classes=6):
        super().__init__();self.mode=mode
        self.front=nn.Sequential(
            nn.Conv1d(dim,hidden,7,stride=2,padding=3),nn.GELU(),
            nn.Conv1d(hidden,hidden,5,padding=4,dilation=2),nn.GELU(),
            nn.Conv1d(hidden,hidden,5,padding=8,dilation=4),nn.GELU())
        self.boundary=nn.Sequential(nn.Conv1d(hidden,32,3,padding=1),nn.GELU(),nn.Conv1d(32,1,1))
        self.out=nn.Sequential(nn.Linear(hidden*5,160),nn.GELU(),nn.Dropout(.18),nn.Linear(160,classes))
    def reset_mask(self,h,mask):
        learned=torch.sigmoid(self.boundary(h.transpose(1,2)).transpose(1,2).squeeze(-1))*mask
        T=h.shape[1]
        if self.mode=='learned': b=learned
        elif self.mode=='shifted_learned': b=torch.roll(learned,shifts=7,dims=1)*mask
        elif self.mode=='no_reset': b=torch.zeros_like(learned)
        elif self.mode=='all_reset': b=mask.float()
        else:
            t=torch.arange(T,device=h.device)
            if self.mode=='periodic': z=(t%6==0).float()
            else:
                z=(((t*1103515245+12345)%2147483647)%1000<165).float()
            b=z[None,:].expand(h.shape[0],-1)*mask
        return b
    def forward(self,x,lengths):
        h=self.front(x.transpose(1,2)).transpose(1,2)
        l=torch.div(lengths+1,2,rounding_mode='floor').clamp(min=1,max=h.shape[1]);mask=torch.arange(h.shape[1],device=h.device)[None,:]<l[:,None]
        b=self.reset_mask(h,mask)
        raw_max=h.masked_fill(~mask[:,:,None],-1e4).amax(1);raw_mean=(h*mask[:,:,None]).sum(1)/l[:,None]
        acc=torch.zeros((h.shape[0],h.shape[2]),device=h.device);count=torch.zeros((h.shape[0],1),device=h.device);states=[]
        for t in range(h.shape[1]):
            g=b[:,t:t+1];acc=h[:,t]+(1-g)*acc;count=1+(1-g)*count;states.append(acc/count.clamp(min=1))
        s=torch.stack(states,1);seg_max=s.masked_fill(~mask[:,:,None],-1e4).amax(1);seg_mean=(s*mask[:,:,None]).sum(1)/l[:,None];event=(h*b[:,:,None]).sum(1)/(b.sum(1,keepdim=True)+1e-5)
        return self.out(torch.cat([raw_max,raw_mean,seg_max,seg_mean,event],1)), b.sum()/mask.sum().clamp(min=1)

def eval_model(model,loader):
    model.eval();ok=n=0;by={};rates=[]
    with torch.no_grad():
        for x,l,y,c in loader:
            z,r=model(x,l);p=z.argmax(1);ok+=int((p==y).sum());n+=len(y);rates.append(float(r))
            for i,k in enumerate(c):a=by.setdefault(k,[0,0]);a[0]+=int(p[i]==y[i]);a[1]+=1
    return ok/max(1,n),{k:a/b for k,(a,b) in by.items()},float(np.mean(rates))

def train(model,tr,dev,seed,epochs=8):
    torch.manual_seed(seed);g=torch.Generator().manual_seed(seed)
    tl=DataLoader(tr,batch_size=32,shuffle=True,generator=g,collate_fn=d.collate,num_workers=0);dl=DataLoader(dev,batch_size=64,shuffle=False,collate_fn=d.collate,num_workers=0)
    opt=torch.optim.AdamW(model.parameters(),lr=1.8e-3,weight_decay=2e-4);best=None;bs=-1;hist=[]
    for ep in range(1,epochs+1):
        model.train();ls=[];rr=[]
        for x,l,y,_ in tl:
            opt.zero_grad(set_to_none=True);z,r=model(x,l);loss=F.cross_entropy(z,y)+(.004*r if model.mode=='learned' else 0);loss.backward();torch.nn.utils.clip_grad_norm_(model.parameters(),4);opt.step();ls.append(float(loss.detach()));rr.append(float(r.detach()))
        ac,_,_=eval_model(model,dl);hist.append({'epoch':ep,'loss':float(np.mean(ls)),'dev':ac,'reset_rate':float(np.mean(rr))})
        if ac>bs:bs=ac;best={k:v.detach().cpu().clone() for k,v in model.state_dict().items()}
        if ep in (1,2,4,8):print('EPOCH',model.mode,ep,hist[-1],flush=True)
    model.load_state_dict(best);return hist

def run(seed=35200):
    specs,test=d.build_specs(seed,2);rng=np.random.default_rng(seed);ix=np.arange(len(specs));rng.shuffle(ix);nd=max(240,int(.12*len(ix)));dv=set(map(int,ix[:nd]));tr=d.AcousticDataset([s for i,s in enumerate(specs) if i not in dv],seed);dev=d.AcousticDataset([s for i,s in enumerate(specs) if i in dv],seed+91);te=d.AcousticDataset(test,seed+193);loader=DataLoader(te,batch_size=64,shuffle=False,collate_fn=d.collate,num_workers=0)
    out={'seed':seed,'train_n':len(tr),'dev_n':len(dev),'test_n':len(te),'models':{}}
    for mi,mode in enumerate(MODES):
        print('MODEL',mode,flush=True);m=BoundaryAblationPAM(mode);hist=train(m,tr,dev,seed+mi*1000);acc,conds,rate=eval_model(m,loader);keys=['speaker_speed','hard_noise','heldout_comp',*d.TEST_TEMPLATES.keys()];hard=float(np.mean([conds[k] for k in keys]));out['models'][mode]={'overall':acc,'hard_mean':hard,'conditions':conds,'reset_rate':rate,'history':hist,'extreme_flags':[k for k,v in conds.items() if v in (0.,1.)]};print('RESULT',mode,out['models'][mode],flush=True);del m;gc.collect()
    (OUT/f'R32_BOUNDARY_ABLATION_SEED_{seed}.json').write_text(json.dumps(out,indent=2));return out

def main():
    row=run(35200);result={'result':row,'ranking':sorted([(v['hard_mean'],k) for k,v in row['models'].items()],reverse=True),'boundary':'REFERENCE_ONLY matched reset-process ablation. All variants preserve the same high-fidelity temporal path and same segment-state capacity; only reset placement differs. Learned reset receives no transcript, word/phoneme/chunk boundary, VAD, ASR, transformer, attention or LLM.'};(OUT/'R32_TTS_BOUNDARY_ABLATION_REFERENCE_ONLY.json').write_text(json.dumps(result,indent=2));print(json.dumps(result['ranking'],indent=2))
if __name__=='__main__':main()
