from __future__ import annotations
import gc,json,os,sys
from pathlib import Path
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
import r32_tts_segmental_pam as d

OUT=Path('/mnt/data/r32_epistemic')
torch.set_num_threads(max(1,min(5,os.cpu_count() or 1)))

class DualSegmentalTemporalPAM(nn.Module):
    """Raw temporal evidence plus a learner-owned contiguous segment route.

    The high-fidelity route is never removed. A boundary process supplies a second
    compressed state route. No human boundary, transcript, word, phoneme, VAD or
    fixed chunk target exists. The optional predictive term compares the gate only
    with learner-internal temporal surprise.
    """
    def __init__(self,predictive:bool,dim:int=49,hidden:int=80,classes:int=6):
        super().__init__();self.predictive=predictive
        self.front=nn.Sequential(
            nn.Conv1d(dim,hidden,7,stride=2,padding=3),nn.GELU(),
            nn.Conv1d(hidden,hidden,5,padding=4,dilation=2),nn.GELU(),
            nn.Conv1d(hidden,hidden,5,padding=8,dilation=4),nn.GELU(),
        )
        self.boundary=nn.Sequential(nn.Conv1d(hidden,32,3,padding=1),nn.GELU(),nn.Conv1d(32,1,1))
        self.out=nn.Sequential(nn.Linear(hidden*5,160),nn.GELU(),nn.Dropout(.18),nn.Linear(160,classes))
    def forward(self,x,lengths):
        h=self.front(x.transpose(1,2)).transpose(1,2)
        l=torch.div(lengths+1,2,rounding_mode='floor').clamp(min=1,max=h.shape[1])
        mask=torch.arange(h.shape[1],device=h.device)[None,:] < l[:,None]
        b=torch.sigmoid(self.boundary(h.transpose(1,2)).transpose(1,2).squeeze(-1))*mask
        raw_max=h.masked_fill(~mask[:,:,None],-1e4).amax(1)
        raw_mean=(h*mask[:,:,None]).sum(1)/l[:,None]
        acc=torch.zeros((h.shape[0],h.shape[2]),device=h.device);count=torch.zeros((h.shape[0],1),device=h.device);states=[]
        for t in range(h.shape[1]):
            g=b[:,t:t+1];acc=h[:,t]+(1-g)*acc;count=1+(1-g)*count;states.append(acc/count.clamp(min=1))
        s=torch.stack(states,1)
        seg_max=s.masked_fill(~mask[:,:,None],-1e4).amax(1)
        seg_mean=(s*mask[:,:,None]).sum(1)/l[:,None]
        event=(h*b[:,:,None]).sum(1)/(b.sum(1,keepdim=True)+1e-5)
        logits=self.out(torch.cat([raw_max,raw_mean,seg_max,seg_mean,event],1))
        delta=torch.zeros_like(b)
        if h.shape[1]>1:
            q=(h[:,1:]-h[:,:-1]).pow(2).mean(-1).sqrt();valid=mask[:,1:];q=q*valid
            mean=q.sum(1,keepdim=True)/valid.sum(1,keepdim=True).clamp(min=1);q=(q/(mean*2.2+1e-5)).clamp(0,1);delta[:,1:]=q
        pred_loss=F.mse_loss(b[mask],delta.detach()[mask]) if bool(mask.any()) else b.sum()*0
        return logits,{'boundary_rate':b.sum()/mask.sum().clamp(min=1),'predictive_loss':pred_loss}

def prepare(seed:int):
    specs,test=d.build_specs(seed,2);rng=np.random.default_rng(seed);ix=np.arange(len(specs));rng.shuffle(ix);nd=max(240,int(.12*len(ix)));dv=set(map(int,ix[:nd]))
    tr=d.AcousticDataset([s for i,s in enumerate(specs) if i not in dv],seed)
    dev=d.AcousticDataset([s for i,s in enumerate(specs) if i in dv],seed+91)
    te=d.AcousticDataset(test,seed+193);return tr,dev,te

def evaluate(model,loader):
    model.eval();ok=0;n=0;by={};br=[]
    with torch.no_grad():
        for x,l,y,conds in loader:
            z,st=model(x,l);p=z.argmax(1);ok+=int((p==y).sum());n+=len(y);br.append(float(st['boundary_rate']))
            for i,c in enumerate(conds):a=by.setdefault(c,[0,0]);a[0]+=int(p[i]==y[i]);a[1]+=1
    return ok/max(1,n),{'conditions':{k:v[0]/v[1] for k,v in by.items()},'boundary_rate':float(np.mean(br))}

def train(model,tr,dev,seed:int,epochs:int=12):
    torch.manual_seed(seed);gen=torch.Generator().manual_seed(seed)
    tl=DataLoader(tr,batch_size=32,shuffle=True,generator=gen,collate_fn=d.collate,num_workers=0)
    dl=DataLoader(dev,batch_size=64,shuffle=False,collate_fn=d.collate,num_workers=0)
    opt=torch.optim.AdamW(model.parameters(),lr=1.8e-3,weight_decay=2e-4);best=None;bs=-1.;hist=[]
    for ep in range(1,epochs+1):
        model.train();ls=[];br=[];pl=[]
        for x,l,y,_ in tl:
            opt.zero_grad(set_to_none=True);z,st=model(x,l);loss=F.cross_entropy(z,y)+.004*st['boundary_rate']
            if model.predictive:loss=loss+.035*st['predictive_loss']
            loss.backward();torch.nn.utils.clip_grad_norm_(model.parameters(),4.0);opt.step();ls.append(float(loss.detach()));br.append(float(st['boundary_rate'].detach()));pl.append(float(st['predictive_loss'].detach()))
        ac,_=evaluate(model,dl);h={'epoch':ep,'loss':float(np.mean(ls)),'dev_acc':ac,'boundary_rate':float(np.mean(br)),'predictive_loss':float(np.mean(pl))};hist.append(h)
        if ac>bs:bs=ac;best={k:v.detach().cpu().clone() for k,v in model.state_dict().items()}
        if ep in (1,2,4,8,12):print('EPOCH',ep,h,flush=True)
    model.load_state_dict(best);return hist

def run(seed:int,name:str):
    predictive=name=='dual_predictive_segmental';init_seed=seed+(21000 if predictive else 11000);torch.manual_seed(init_seed);model=DualSegmentalTemporalPAM(predictive)
    tr,dev,te=prepare(seed);hist=train(model,tr,dev,init_seed);loader=DataLoader(te,batch_size=64,shuffle=False,collate_fn=d.collate,num_workers=0);acc,detail=evaluate(model,loader)
    hard_keys=['speaker_speed','hard_noise','heldout_comp',*d.TEST_TEMPLATES.keys()];hard=float(np.mean([detail['conditions'][k] for k in hard_keys]))
    out={'seed':seed,'model':name,'train_n':len(tr),'dev_n':len(dev),'test_n':len(te),'overall':acc,'hard_mean':hard,**detail,'history':hist,'extreme_flags':[k for k,v in detail['conditions'].items() if v in (0.,1.)]}
    p=OUT/f'R32_DUAL_SEGMENTAL_SEED_{seed}_{name}.json';p.write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2),flush=True);return out

if __name__=='__main__':run(int(sys.argv[1]),sys.argv[2])
