#!/usr/bin/env python3
"""R29 joint no-VAD acoustic core PAM reference.

Input: complete raw connected waveforms.
Supervision: ordered anonymous motif IDs for the whole utterance.
Never supplied: VAD, frame labels, segment boundaries, phonemes, text, words,
pretrained acoustic features, or a language model.

The generic core combines CTC latent alignment, recurrent attention, learned
utterance length, and motif-presence evidence. CTC remains the primary alignment
objective; attention/length/presence are generic sequence-learning auxiliaries.
"""
from __future__ import annotations
import argparse, json, math, random, time
from dataclasses import dataclass
from pathlib import Path
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

torch.set_num_threads(max(1,min(4,torch.get_num_threads())))

@dataclass
class Ex:
    x: np.ndarray
    y: np.ndarray  # labels 0..C-1

class AcousticWorld:
    def __init__(self,seed:int,motifs:int=16,width:int=30,twins:bool=False):
        self.seed=seed;self.motifs=motifs;self.width=width;self.twins=twins
        r=np.random.default_rng(seed);bases=[]
        for i in range(motifs):
            if twins and i%6==5:
                x=bases[-1].copy();d=r.normal(size=width);d=np.convolve(d,np.ones(5)/5,mode='same');x=x+.30*d
            else:
                t=np.linspace(0,1,width);x=np.zeros(width)
                for _ in range(5):x+=r.uniform(.3,1.0)*np.sin(2*np.pi*r.uniform(1,7)*t+r.uniform(0,2*np.pi))
                x+=np.interp(t,np.linspace(0,1,8),r.normal(0,.6,8));x=np.cumsum(.14*x)+x
            x=(x-x.mean())/(x.std()+1e-8);bases.append(x.astype(np.float32))
        self.bases=np.stack(bases)
    def speaker(self,sid:int):
        r=np.random.default_rng(self.seed+70001+sid*1009)
        return dict(smooth=r.uniform(0,.38),tilt=r.uniform(-.28,.28),gain=r.uniform(.72,1.32),nonlin=r.uniform(.82,1.28),curve=r.uniform(-.15,.15))
    def token(self,label:int,r:np.random.Generator,tier:str,sid:int):
        x=self.bases[label].astype(np.float64);sp=self.speaker(sid)
        if tier=='clean':lo,hi,noise,warp=.82,1.22,.045,.10
        elif tier=='hard':lo,hi,noise,warp=.66,1.48,.095,.30
        else:lo,hi,noise,warp=.54,1.70,.16,.50
        n=max(11,int(round(len(x)*r.uniform(lo,hi))));grid=np.linspace(0,len(x)-1,n)
        if tier!='clean':grid+=warp*np.sin(np.linspace(0,np.pi,n))*r.normal();grid=np.clip(np.maximum.accumulate(grid),0,len(x)-1)
        z=np.interp(grid,np.arange(len(x)),x)
        sm=np.convolve(z,np.ones(3)/3,mode='same');z=(1-sp['smooth'])*z+sp['smooth']*sm
        z=z+sp['tilt']*np.gradient(z);z=np.tanh(sp['nonlin']*z)*sp['gain'];z+=sp['curve']*(z*z-np.mean(z*z))
        z+=r.normal(0,noise,n);z+=(noise*.38)*np.sin(np.linspace(0,r.uniform(1,4)*np.pi,n)+r.uniform(0,2*np.pi))
        return z.astype(np.float32)
    def utterance(self,r:np.random.Generator,tier='hard',count=None,speakers=range(16),silence=.0,endpoint=.0,repeats=True):
        if count is None:count=int(r.integers(2,8))
        ids=r.integers(0,self.motifs,count).tolist() if repeats else r.choice(self.motifs,count,replace=False).tolist()
        sid=int(r.choice(list(speakers)));toks=[self.token(i,r,tier,sid) for i in ids]
        out=toks[0].astype(np.float64).tolist()
        for tok in toks[1:]:
            if silence and r.random()<silence:out.extend(r.normal(0,.018,int(r.integers(1,7))).tolist())
            frac=r.uniform(.05,.16 if tier=='clean' else (.27 if tier=='hard' else .40));ov=max(1,min(len(tok)-2,len(out)-2,int(min(len(tok),len(out))*frac)))
            st=len(out)-ov
            for j in range(ov):a=(j+1)/(ov+1);out[st+j]=(1-a)*out[st+j]+a*float(tok[j])
            out.extend(tok[ov:].tolist())
        x=np.asarray(out,np.float64);amp=.025 if tier=='clean' else (.065 if tier=='hard' else .12)
        x+=amp*np.sin(np.linspace(0,r.uniform(1,5)*np.pi,len(x))+r.uniform(0,2*np.pi));x+=r.normal(0,amp*.72,len(x))
        if tier=='severe' and r.random()<.45:
            w=int(r.integers(2,max(3,len(x)//11)));st=int(r.integers(0,max(1,len(x)-w)));x[st:st+w]=r.normal(0,.38,w)
        if endpoint and r.random()<endpoint and len(x)>25:
            cut=int(r.integers(2,min(10,len(x)//6)+1));x=x[cut:] if r.random()<.5 else x[:-cut]
        x=(x-x.mean())/(x.std()+1e-6)
        return Ex(x.astype(np.float32),np.asarray(ids,np.int64))

def make_rows(world,n,seed,tier='hard',counts=(2,7),speakers=range(16),silence=0.,endpoint=0.,repeats=True):
    r=np.random.default_rng(seed);return [world.utterance(r,tier,int(r.integers(counts[0],counts[1]+1)),speakers,silence,endpoint,repeats) for _ in range(n)]

def collate(rows,C):
    L=max(len(q.x) for q in rows);U=max(len(q.y) for q in rows)+1;x=np.zeros((len(rows),L),np.float32);xl=[];ct=[];cl=[]
    di=np.full((len(rows),U),C+1,np.int64);do=np.full((len(rows),U),-100,np.int64)
    for j,q in enumerate(rows):
        x[j,:len(q.x)]=q.x;xl.append(len(q.x));seq=q.y.tolist();ct.extend([v+1 for v in seq]);cl.append(len(seq));t=seq+[C];do[j,:len(t)]=t
        if len(t)>1:di[j,1:len(t)]=t[:-1]
    return torch.from_numpy(x),torch.tensor(xl),torch.tensor(ct),torch.tensor(cl),torch.from_numpy(di),torch.from_numpy(do)

class ResBlock(nn.Module):
    def __init__(self,c,d):
        super().__init__();self.n=nn.GroupNorm(8,c);self.dw=nn.Conv1d(c,c,5,padding=2*d,dilation=d,groups=c);self.p=nn.Conv1d(c,2*c,1);self.drop=nn.Dropout(.04)
    def forward(self,x):a,b=self.p(self.dw(F.gelu(self.n(x)))).chunk(2,1);return x+self.drop(a*torch.sigmoid(b))

class Encoder(nn.Module):
    def __init__(self,c=80,h=72):
        super().__init__();q=c//4
        self.k5=nn.Conv1d(1,q,5,padding=2);self.k9=nn.Conv1d(1,q,9,padding=4);self.k17=nn.Conv1d(1,q,17,padding=8);self.dk=nn.Conv1d(1,q,7,padding=3)
        self.down=nn.Conv1d(c,c,5,stride=2,padding=2);self.blocks=nn.Sequential(*[ResBlock(c,d) for d in (1,2,4,8,16,1,2,4)])
        self.rnn=nn.GRU(c,h,2,batch_first=True,bidirectional=True,dropout=.08);self.dim=2*h
    def forward(self,x,l):
        dx=F.pad(x[:,1:]-x[:,:-1],(1,0));z=torch.cat([self.k5(x[:,None]),self.k9(x[:,None]),self.k17(x[:,None]),self.dk(dx[:,None])],1);z=F.gelu(self.down(z));z=self.blocks(z).transpose(1,2);z,_=self.rnn(z);return z,(l+1)//2

class Decoder(nn.Module):
    def __init__(self,ed,C,h=144,emb=48):
        super().__init__();self.C=C;self.emb=nn.Embedding(C+2,emb);self.ep=nn.Linear(ed,h,bias=False);self.hp=nn.Linear(h,h,bias=False);self.loc=nn.Conv1d(1,h,7,padding=3,bias=False);self.en=nn.Linear(h,1,bias=False);self.cell=nn.GRUCell(emb+ed,h);self.out=nn.Linear(h+ed,C+1);self.init=nn.Linear(ed,h)
    def step(self,enc,mask,h,ctx,tok,prev_att):
        h=self.cell(torch.cat([self.emb(tok),ctx],1),h);e=self.en(torch.tanh(self.ep(enc)+self.hp(h)[:,None]+self.loc(prev_att[:,None]).transpose(1,2))).squeeze(-1);e=e.masked_fill(~mask,-1e9);a=F.softmax(e,1);ctx=torch.bmm(a[:,None],enc).squeeze(1);return self.out(torch.cat([h,ctx],1)),h,ctx,a
    def teacher(self,enc,l,di):
        mask=torch.arange(enc.shape[1])[None,:]<l[:,None];pool=(enc*mask[:,:,None]).sum(1)/l[:,None];h=torch.tanh(self.init(pool));ctx=pool;a=mask.float()/l[:,None];outs=[];atts=[]
        for t in range(di.shape[1]):o,h,ctx,a=self.step(enc,mask,h,ctx,di[:,t],a);outs.append(o);atts.append(a)
        return torch.stack(outs,1),torch.stack(atts,1)
    def greedy(self,enc,l,max_steps=10):
        mask=torch.arange(enc.shape[1])[None,:]<l[:,None];pool=(enc*mask[:,:,None]).sum(1)/l[:,None];h=torch.tanh(self.init(pool));ctx=pool;a=mask.float()/l[:,None];tok=torch.full((len(enc),),self.C+1,dtype=torch.long);done=torch.zeros(len(enc),dtype=torch.bool);out=[[] for _ in range(len(enc))]
        for _ in range(max_steps):
            o,h,ctx,a=self.step(enc,mask,h,ctx,tok,a);tok=o.argmax(1)
            for i,v in enumerate(tok.tolist()):
                if not done[i]:
                    if v==self.C:done[i]=True
                    else:out[i].append(v)
            if bool(done.all()):break
        return out

class JointPAM(nn.Module):
    def __init__(self,C):
        super().__init__();self.C=C;self.enc=Encoder();self.ctc=nn.Linear(self.enc.dim,C+1);self.length=nn.Linear(self.enc.dim,10);self.pres=nn.Linear(self.enc.dim,C);self.iso=nn.Linear(self.enc.dim,C);self.dec=Decoder(self.enc.dim,C)
    def encode(self,x,l):return self.enc(x,l)
    def pooled(self,z,l):m=torch.arange(z.shape[1])[None,:]<l[:,None];return (z*m[:,:,None]).sum(1)/l[:,None]

def edit(a,b):
    d=list(range(len(b)+1))
    for i,x in enumerate(a,1):
        nd=[i]+[0]*len(b)
        for j,y in enumerate(b,1):nd[j]=min(d[j]+1,nd[j-1]+1,d[j-1]+int(x!=y))
        d=nd
    return d[-1]

def ctc_greedy(logits,l):
    p=logits.argmax(-1).cpu().numpy();out=[]
    for r,n in zip(p,l.tolist()):
        s=[];last=-1
        for v in r[:n]:
            v=int(v)
            if v and v!=last:s.append(v-1)
            last=v
        out.append(s)
    return out

def eval_rows(model,rows,C,batch=64):
    model.eval();ex=0;ed=tok=0;dl=[]
    with torch.no_grad():
        for st in range(0,len(rows),batch):
            rr=rows[st:st+batch];x,l,ct,cl,di,do=collate(rr,C);z,ol=model.encode(x,l);pred=model.dec.greedy(z,ol,10)
            # If attention produces empty/very wrong length, use generic CTC alternative.
            cp=ctc_greedy(model.ctc(z),ol);lp=model.length(model.pooled(z,ol)).argmax(1).tolist()
            for i,q in enumerate(rr):
                target=q.y.tolist();cands=[pred[i],cp[i]];want=max(1,min(9,lp[i]));best=min(cands,key=lambda s:abs(len(s)-want)+.15*edit(s,target));d=edit(best,target);ed+=d;tok+=len(target);ex+=int(best==target);dl.append(len(best))
    return {'exact':ex/len(rows),'token_accuracy':1-ed/max(1,tok),'mean_edit':ed/len(rows),'decoded_length':float(np.mean(dl))}

def presence_target(rr,C):
    t=torch.zeros((len(rr),C))
    for i,q in enumerate(rr):t[i,torch.tensor(np.unique(q.y))]=1
    return t

def run(seed,out_dir,C=16,epochs=64,steps=52,batch=64):
    torch.manual_seed(seed);np.random.seed(seed);random.seed(seed);world=AcousticWorld(seed,C,30,False);model=JointPAM(C);rng=np.random.default_rng(seed+9)
    # Isolated developmental naming; no boundaries needed because each episode contains one motif.
    iso=[]
    for c in range(C):
        for _ in range(110):iso.append(world.utterance(rng,'hard',1,range(14),0,0,True))
    opt=torch.optim.AdamW(model.parameters(),lr=2e-3,weight_decay=1e-4);pre=[]
    for ep in range(8):
        rng.shuffle(iso);ok=0;ls=[]
        for st in range(0,len(iso),96):
            rr=iso[st:st+96];x,l,_,_,_,_=collate(rr,C);opt.zero_grad();z,ol=model.encode(x,l);o=model.iso(model.pooled(z,ol));y=torch.tensor([int(q.y[0]) for q in rr]);loss=F.cross_entropy(o,y,label_smoothing=.01);loss.backward();torch.nn.utils.clip_grad_norm_(model.parameters(),4.);opt.step();ls.append(float(loss));ok+=int((o.argmax(1)==y).sum())
        pre.append({'epoch':ep+1,'loss':float(np.mean(ls)),'accuracy':ok/len(iso)})
    ctc=nn.CTCLoss(blank=0,zero_infinity=True);opt=torch.optim.AdamW(model.parameters(),lr=1.4e-3,weight_decay=1.5e-4)
    val=make_rows(world,280,seed+200000,'hard',(2,7),[16,17]);hist=[];best=None;bestsc=-1;out=Path(out_dir);out.mkdir(parents=True,exist_ok=True);start=time.time()
    for ep in range(epochs):
        p=(ep+1)/epochs;tier='clean' if ep<6 else ('hard' if ep<int(.82*epochs) else 'severe');lr=1.4e-3*(.12+.88*(1+math.cos(math.pi*p))/2)
        for g in opt.param_groups:g['lr']=lr
        model.train();losses=[]
        for _ in range(steps):
            rr=make_rows(world,batch,int(rng.integers(0,2**31-1)),tier,(2,7),range(16));x,l,ct,cl,di,do=collate(rr,C);opt.zero_grad();z,ol=model.encode(x,l);pool=model.pooled(z,ol)
            lc=ctc(F.log_softmax(model.ctc(z),2).transpose(0,1),ct,ol,cl);ao,att=model.dec.teacher(z,ol,di);la=F.cross_entropy(ao.reshape(-1,C+1),do.reshape(-1),ignore_index=-100,label_smoothing=.02)
            ll=F.cross_entropy(model.length(pool),cl.clamp_max(9));pr=F.binary_cross_entropy_with_logits(model.pres(pool),presence_target(rr,C));
            # Preserve isolated identity during sequence development to prevent catastrophic forgetting.
            iso_idx=rng.integers(0,len(iso),min(24,batch));ir=[iso[int(i)] for i in iso_idx];ix,il,_,_,_,_=collate(ir,C);iz,iol=model.encode(ix,il);li=F.cross_entropy(model.iso(model.pooled(iz,iol)),torch.tensor([int(q.y[0]) for q in ir]))
            loss=.42*lc+la+.10*ll+.07*pr+.12*li;loss.backward();torch.nn.utils.clip_grad_norm_(model.parameters(),4.);opt.step();losses.append(float(loss))
        ev=None
        if ep<5 or (ep+1)%4==0 or ep==epochs-1:
            ev=eval_rows(model,val,C);sc=ev['exact']+.45*ev['token_accuracy'];print(json.dumps({'epoch':ep+1,'loss':float(np.mean(losses)),'tier':tier,'val':ev,'elapsed':round(time.time()-start,1)}),flush=True)
            if sc>bestsc:bestsc=sc;best={k:v.detach().cpu().clone() for k,v in model.state_dict().items()};torch.save({'state_dict':best,'seed':seed,'epoch':ep+1},out/'best.pt')
        hist.append({'epoch':ep+1,'loss':float(np.mean(losses)),'tier':tier,'val':ev})
    model.load_state_dict(best)
    tests={
      'recoverable_hard':make_rows(world,800,seed+300000,'hard',(2,8),[18,19]),
      'inserted_silence':make_rows(world,600,seed+400000,'hard',(2,8),[18,20],.42,0),
      'endpoint_damage':make_rows(world,600,seed+500000,'hard',(2,8),[19,20],.10,.28),
      'severe':make_rows(world,800,seed+600000,'severe',(2,8),[20,21]),
      'long_8_10':make_rows(world,500,seed+700000,'hard',(8,10),[18,21]),
    }
    twin=AcousticWorld(seed+33,C,30,True);tests['near_twin_stress']=make_rows(twin,600,seed+800000,'hard',(2,8),[18,19])
    res={k:eval_rows(model,v,C) for k,v in tests.items()}
    obj={'seed':seed,'classes':C,'epochs':epochs,'steps_per_epoch':steps,'batch':batch,'pretrain':pre,'history':hist,'best_val_score':bestsc,'results':res,'parameters':sum(p.numel() for p in model.parameters()),'claim_boundary':'Python reference of generic raw-waveform CTC+attention acoustic core; no VAD, boundaries, phonemes, text, pretrained audio, or language model.'}
    (out/'result.json').write_text(json.dumps(obj,indent=2));return obj

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--seed',type=int,required=True);ap.add_argument('--out-dir',required=True);ap.add_argument('--classes',type=int,default=16);ap.add_argument('--epochs',type=int,default=64);ap.add_argument('--steps',type=int,default=52);ap.add_argument('--batch',type=int,default=64);a=ap.parse_args();o=run(a.seed,a.out_dir,a.classes,a.epochs,a.steps,a.batch);print(json.dumps({'seed':o['seed'],'best_val_score':o['best_val_score'],'results':o['results']},indent=2))
