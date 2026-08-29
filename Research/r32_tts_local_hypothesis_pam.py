from __future__ import annotations

import json, os, random, sys, gc
from pathlib import Path
from collections import defaultdict

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader

import r32_tts_segmental_pam as d
import r32_tts_temporal_epistemic_challenge as challenge

OUT=Path('/mnt/data/r32_epistemic')
torch.set_num_threads(max(1,min(5,os.cpu_count() or 1)))
A=d.base.ACTIONS

class Rows(Dataset):
    def __init__(self,specs,seed):
        self.specs=list(specs);self.seed=seed;self.cache=[None]*len(self.specs)
    def __len__(self):return len(self.specs)
    def __getitem__(self,i):
        x=self.cache[i]
        if x is None:
            x=d.make_feature(self.specs[i],self.seed);self.cache[i]=x
        return x,self.specs[i].action_i,self.specs[i].condition

class FeatureRows(Dataset):
    def __init__(self,features,labels,conds=None):
        self.f=features;self.y=labels;self.c=conds or ['x']*len(labels)
    def __len__(self):return len(self.y)
    def __getitem__(self,i):return self.f[i],self.y[i],self.c[i]

class LocalHypothesisPAM(nn.Module):
    """Frozen non-transformer temporal substrate plus local grounded evidence.

    Whole-experience action consequences train a local evidence head with
    multiple-instance pooling. No local boundary, transcript, acoustic-unit,
    mixture or ambiguity target is supplied.
    """
    def __init__(self,checkpoint):
        super().__init__()
        base=d.TemporalConvPAM();base.load_state_dict(checkpoint['state_dict'])
        self.conv=base.conv
        for p in self.conv.parameters():p.requires_grad=False
        self.local=nn.Conv1d(80,len(A),1)
    def unfreeze_last(self):
        for p in self.conv[4].parameters():p.requires_grad=True
    def forward(self,x,lengths,topk=7):
        h=self.conv(x.transpose(1,2))                    # B,H,T
        local=self.local(h).transpose(1,2)               # B,T,C
        lens=torch.div(lengths+1,2,rounding_mode='floor').clamp(min=1,max=local.shape[1])
        mask=torch.arange(local.shape[1],device=local.device)[None,:] < lens[:,None]
        z=local.masked_fill(~mask[:,:,None],-1e4)
        k=min(topk,local.shape[1])
        utter=z.topk(k,dim=1).values.mean(1)              # local MIL aggregation
        return utter,local,mask,h.transpose(1,2)

def train_phase(model,train,dev,seed,epochs,lr,joint=False):
    if joint:model.unfreeze_last()
    torch.manual_seed(seed)
    opt=torch.optim.AdamW([p for p in model.parameters() if p.requires_grad],lr=lr,weight_decay=2e-4)
    tl=DataLoader(train,batch_size=48,shuffle=True,generator=torch.Generator().manual_seed(seed+13),collate_fn=d.collate,num_workers=0)
    dl=DataLoader(dev,batch_size=80,shuffle=False,collate_fn=d.collate,num_workers=0)
    best=None;bestacc=-1.;hist=[]
    for ep in range(1,epochs+1):
        model.train();losses=[]
        for x,l,y,_ in tl:
            opt.zero_grad(set_to_none=True);u,loc,mask,_=model(x,l)
            loss=F.cross_entropy(u,y)
            # Generic local-evidence sparsity: a grounded hypothesis should be
            # supported by a limited interval, not every frame. No target interval.
            py=torch.softmax(loc,2);true=py.gather(2,y[:,None,None].expand(-1,py.shape[1],1)).squeeze(2)
            sparse=(true*mask).sum(1)/(mask.sum(1).clamp(min=1))
            loss=loss+0.003*sparse.mean()
            loss.backward();torch.nn.utils.clip_grad_norm_(model.parameters(),4);opt.step();losses.append(float(loss.detach()))
        acc=evaluate_top1(model,dl)
        hist.append({'phase':'joint' if joint else 'head','epoch':ep,'loss':float(np.mean(losses)),'dev_top1':acc})
        if acc>bestacc:bestacc=acc;best={k:v.detach().cpu().clone() for k,v in model.state_dict().items()}
        print('PHASE',hist[-1],flush=True)
    model.load_state_dict(best);return hist,bestacc

@torch.no_grad()
def evaluate_top1(model,loader):
    model.eval();ok=n=0
    for x,l,y,_ in loader:
        u,_,_,_=model(x,l);ok+=int((u.argmax(1)==y).sum());n+=len(y)
    return ok/max(1,n)

@torch.no_grad()
def collect_scores(model,loader):
    model.eval();U=[];S=[];P=[];Y=[];C=[]
    for x,l,y,c in loader:
        u,loc,mask,_=model(x,l);prob=torch.softmax(loc,2)
        # Presence is top-k local support, independent for every hypothesis.
        q=prob.masked_fill(~mask[:,:,None],0)
        k=min(7,q.shape[1]);pres=q.topk(k,dim=1).values.mean(1)
        peak=q.argmax(1)
        U.append(torch.softmax(u,1).cpu().numpy());S.append(pres.cpu().numpy());P.append(peak.cpu().numpy());Y.extend(y.tolist());C.extend(c)
    return np.concatenate(U),np.concatenate(S),np.concatenate(P),np.asarray(Y),C

def choose_presence_threshold(scores,y):
    pos=scores[np.arange(len(y)),y]
    neg=scores[np.arange(len(y))[:,None],np.arange(scores.shape[1])[None,:]]
    neg=neg[np.arange(scores.shape[1])[None,:]!=y[:,None]]
    best=None
    for t in np.linspace(float(np.quantile(neg,.70)),float(np.quantile(pos,.30)),61):
        tp=float((pos>=t).mean());fp=float((neg>=t).mean());utility=tp-1.5*fp
        z=(utility,float(t),tp,fp)
        if best is None or z[0]>best[0]:best=z
    return {'threshold':best[1],'true_presence':best[2],'false_presence':best[3],'utility':best[0]}

def ordinary_specs(seed):
    _,test=d.build_specs(seed,2)
    return test

def mixture_features(seed,nrep=40):
    feats=[];pairs=[];conds=[]
    actors=d.base.ACTORS[:4];objs=d.base.OBJECTS[:4]
    for yi in range(len(A)):
        yj=(yi+1)%len(A);actor=actors[yi%len(actors)];obj=objs[(yi*3)%len(objs)]
        for rep in range(nrep):
            t1=d.TRAIN_TEMPLATES[0].format(actor=actor,action=A[yi],object=obj)
            t2=d.TRAIN_TEMPLATES[0].format(actor=actor,action=A[yj],object=obj)
            feats.append(challenge.mix_feature(t1,t2,'en-wi','en-uk-rp',110+(rep%3)*35,215-(rep%3)*30,42,72,seed+yi*1000+rep))
            pairs.append((yi,yj));conds.append('equal_mixture')
    return feats,pairs,conds

def run(seed=35400):
    ck=torch.load(OUT/f'R32_TEMPORAL_CHALLENGE_MODEL_{seed}.pt',map_location='cpu',weights_only=False)
    specs,_=d.build_specs(seed,2)
    # Split unique physical utterance identities so perturb variants do not leak.
    keys=sorted({(s.actor_i,s.action_i,s.object_i,s.voice,s.speed,s.pitch,s.template) for s in specs})
    rng=np.random.default_rng(seed+77);rng.shuffle(keys);dvkeys=set(keys[:max(180,int(.15*len(keys)))])
    tr=[s for s in specs if (s.actor_i,s.action_i,s.object_i,s.voice,s.speed,s.pitch,s.template) not in dvkeys]
    dv=[];seen=set()
    for s in specs:
        k=(s.actor_i,s.action_i,s.object_i,s.voice,s.speed,s.pitch,s.template)
        if k in dvkeys and k not in seen and s.perturb_strength==0:dv.append(s);seen.add(k)
    train=Rows(tr,seed);dev=Rows(dv,seed+91)
    torch.manual_seed(seed+12345);model=LocalHypothesisPAM(ck)
    h1,b1=train_phase(model,train,dev,seed+100,8,2e-3,False)
    h2,b2=train_phase(model,train,dev,seed+200,4,3e-4,True)
    devloader=DataLoader(dev,batch_size=80,shuffle=False,collate_fn=d.collate,num_workers=0)
    du,ds,dp,dy,dc=collect_scores(model,devloader);thr=choose_presence_threshold(ds,dy)
    # Ordinary hard tests.
    ordinary=Rows(ordinary_specs(seed+901),seed+991)
    ol=DataLoader(ordinary,batch_size=80,shuffle=False,collate_fn=d.collate,num_workers=0)
    ou,oscore,opeak,oy,oc=collect_scores(model,ol);pred=ou.argmax(1);present=oscore>=thr['threshold'];by={}
    for cond in sorted(set(oc)):
        ix=np.asarray([c==cond for c in oc]);by[cond]={'top1':float((pred[ix]==oy[ix]).mean()),'false_multi_rate':float((present[ix].sum(1)>1).mean()),'true_present':float(present[ix,np.asarray(oy[ix])].mean())}
    # Equal mixtures, evaluator-only pair checks.
    mf,pairs,mc=mixture_features(seed+800000);ml=DataLoader(FeatureRows(mf,[0]*len(mf),mc),batch_size=80,shuffle=False,collate_fn=d.collate,num_workers=0)
    mu,ms,mp,_,_=collect_scores(model,ml);local_top2=np.argsort(ms,axis=1)[:,-2:];global_top2=np.argsort(mu,axis=1)[:,-2:]
    pair_recall=[];gpair=[];both=[];sep=[]
    for i,(a,b) in enumerate(pairs):
        pair={a,b};pair_recall.append(set(local_top2[i])==pair);gpair.append(set(global_top2[i])==pair);both.append(ms[i,a]>=thr['threshold'] and ms[i,b]>=thr['threshold']);sep.append(abs(int(mp[i,a])-int(mp[i,b]))/max(1,mu.shape[1]))
    mixture={'n':len(pairs),'local_pair_top2_recall':float(np.mean(pair_recall)),'global_pair_top2_recall':float(np.mean(gpair)),'both_present_rate':float(np.mean(both)),'mean_peak_index_distance_raw':float(np.mean([abs(int(mp[i,a])-int(mp[i,b])) for i,(a,b) in enumerate(pairs)])),'false_single_rate':float(np.mean(np.sum(ms>=thr['threshold'],axis=1)<2))}
    flags=[f'ordinary:{c}:{k}' for c,z in by.items() for k,v in z.items() if v in (0.,1.)]+[f'mixture:{k}' for k,v in mixture.items() if isinstance(v,float) and v in (0.,1.)]
    out={'seed':seed,'train_n':len(train),'dev_n':len(dev),'head_best':b1,'joint_best':b2,'presence_calibration':thr,'ordinary':by,'mixture':mixture,'history':h1+h2,'extreme_flags':flags,'boundary':'REFERENCE_ONLY local multi-hypothesis acoustic PAM. A frozen non-transformer temporal substrate and local evidence head are trained only from whole grounded action outcomes with multiple-instance pooling. No transcript, token, phoneme, word/chunk boundary, VAD, ASR, mixture/ambiguity label, attention/transformer or LLM enters learner cognition.'}
    (OUT/f'R32_LOCAL_HYPOTHESIS_PAM_SEED_{seed}.json').write_text(json.dumps(out,indent=2));torch.save({'state_dict':model.state_dict(),'seed':seed,'presence':thr},OUT/f'R32_LOCAL_HYPOTHESIS_PAM_MODEL_{seed}.pt');print(json.dumps(out,indent=2));return out

if __name__=='__main__':run(int(sys.argv[1]) if len(sys.argv)>1 else 35400)
