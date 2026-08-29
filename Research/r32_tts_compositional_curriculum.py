from __future__ import annotations
import gc, json, os, random
from dataclasses import dataclass
from pathlib import Path
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
import r32_tts_segmental_pam as d
import r32_tts_dual_segmental_pam as dual

OUT=Path('/mnt/data/r32_epistemic')
torch.set_num_threads(max(1,min(5,os.cpu_count() or 1)))
BASE=['move','touch','push','hold','open','guide']
THIRD=d.base.ACTIONS
TRAIN_VOICES=['en-us','en-sc','en-uk-north']
TEST_VOICES=['en-uk-rp','en-wi']
TRAIN_SPEEDS=[145,185]
TEST_SPEEDS=[110,225]

SIMPLE='{actor} {target3} the {object} now'
TRAIN_CONTRAST=[
 'although {actor} may {distractor} the {object}, {actor} will {target} it now',
 '{actor} will {target} the {object}, not {distractor} it',
 'do not {distractor} it; let {actor} {target} the {object}',
]
TEST_CONTRAST={
 'contrast_instead':'the {object} is not for {actor} to {distractor}; instead {actor} must {target} it',
 'contrast_even_though':'{actor} should {target} the {object} even though someone said {distractor}',
 'contrast_after':'after considering {distractor}, {actor} chooses to {target} the {object}',
 'contrast_target_first':'{actor} must {target} the {object}; ignore the suggestion to {distractor}',
}

@dataclass(frozen=True)
class Spec:
 actor_i:int; target_i:int; distractor_i:int; object_i:int
 actor:str; object_name:str; voice:str; speed:int; pitch:int; template:str; condition:str; strength:int=0
 @property
 def text(self):
  return self.template.format(actor=self.actor,object=self.object_name,target=BASE[self.target_i],target3=THIRD[self.target_i],distractor=BASE[self.distractor_i])

def make_specs(seed:int,mixed:bool):
 tr=[];te=[]
 for ai,a in enumerate(d.base.ACTORS):
  for yi in range(len(BASE)):
   for oi,o in enumerate(d.base.OBJECTS):
    di=(yi+1+oi+ai)%len(BASE)
    if di==yi:di=(di+1)%len(BASE)
    if not d.base.hold(ai,oi):
     for v in TRAIN_VOICES:
      for sp in TRAIN_SPEEDS:
       tr.append(Spec(ai,yi,di,oi,a,o,v,sp,44+(ai*3+oi)%13,SIMPLE,'train_simple',0))
       if mixed:
        # Contexts vary, but the learner never receives the template identity.
        ti=(ai+oi+yi)%len(TRAIN_CONTRAST)
        tr.append(Spec(ai,yi,di,oi,a,o,v,sp,47+(yi*2+oi)%11,TRAIN_CONTRAST[ti],'train_contrast',1))
    for v in TEST_VOICES:
     for sp in TEST_SPEEDS:
      basecond='heldout_simple' if d.base.hold(ai,oi) else 'simple_shift'
      te.append(Spec(ai,yi,di,oi,a,o,v,sp,56,SIMPLE,basecond,0))
      te.append(Spec(ai,yi,di,oi,a,o,v,sp,56,SIMPLE,'simple_hard',3))
      for cond,t in TEST_CONTRAST.items():
       te.append(Spec(ai,yi,di,oi,a,o,v,sp,53,t,cond,2))
 # Extra target/distractor permutations prevent one fixed contrast pairing.
 rng=random.Random(seed);rng.shuffle(tr);rng.shuffle(te)
 return tr,te

class DS(Dataset):
 def __init__(self,specs,seed):self.s=specs;self.seed=seed;self.cache=[None]*len(specs)
 def __len__(self):return len(self.s)
 def __getitem__(self,i):
  x=self.cache[i];sp=self.s[i]
  if x is None:
   sr,w=d.synth_text(sp.text,sp.voice,sp.speed,sp.pitch)
   w=d.perturb(sr,w,self.seed+i*977+sp.actor_i*101+sp.target_i*17+sp.object_i,sp.strength)
   x=d.feature(sr,w);self.cache[i]=x
  return x,sp.target_i,sp.condition

def collate(b):return d.collate(b)

def ev(m,loader):
 m.eval();ok=n=0;by={}
 with torch.no_grad():
  for x,l,y,c in loader:
   z,_=m(x,l);p=z.argmax(1);ok+=int((p==y).sum());n+=len(y)
   for i,k in enumerate(c):a=by.setdefault(k,[0,0]);a[0]+=int(p[i]==y[i]);a[1]+=1
 return ok/n,{k:a/b for k,(a,b) in by.items()}

def train(m,tr,dev,seed,max_epochs=5):
 torch.manual_seed(seed);g=torch.Generator().manual_seed(seed)
 tl=DataLoader(tr,batch_size=32,shuffle=True,generator=g,collate_fn=collate,num_workers=0)
 dl=DataLoader(dev,batch_size=64,shuffle=False,collate_fn=collate,num_workers=0)
 opt=torch.optim.AdamW(m.parameters(),lr=1.8e-3,weight_decay=2e-4);best=None;bs=-1;hist=[]
 for ep in range(1,max_epochs+1):
  m.train();ls=[]
  for x,l,y,_ in tl:
   opt.zero_grad(set_to_none=True);z,st=m(x,l);loss=F.cross_entropy(z,y)
   if isinstance(st,dict) and 'boundary_rate' in st:loss=loss+.004*st['boundary_rate']
   loss.backward();torch.nn.utils.clip_grad_norm_(m.parameters(),4);opt.step();ls.append(float(loss.detach()))
  ac,_=ev(m,dl);hist.append({'epoch':ep,'loss':float(np.mean(ls)),'dev':ac});print('EPOCH',ep,hist[-1],flush=True)
  if ac>bs:bs=ac;best={k:v.detach().cpu().clone() for k,v in m.state_dict().items()}
  if ep>=2 and hist[-1]['dev']>=.999 and hist[-2]['dev']>=.999:break
 m.load_state_dict(best);return hist

def run(seed=35400):
 out={'seed':seed,'models':{}}
 for curriculum in ['simple','mixed']:
  specs,test=make_specs(seed,curriculum=='mixed');rng=np.random.default_rng(seed+(1 if curriculum=='mixed' else 0));ix=np.arange(len(specs));rng.shuffle(ix);nd=max(240,int(.12*len(ix)));dv=set(map(int,ix[:nd]));tr=DS([s for i,s in enumerate(specs) if i not in dv],seed);dev=DS([s for i,s in enumerate(specs) if i in dv],seed+91);te=DS(test,seed+193);test_loader=DataLoader(te,batch_size=64,shuffle=False,collate_fn=collate,num_workers=0)
  for arch in ['temporal','dual']:
   name=f'{arch}_{curriculum}';print('MODEL',name,'N',len(tr),flush=True)
   m=d.TemporalConvPAM() if arch=='temporal' else dual.DualSegmentalTemporalPAM(False)
   hist=train(m,tr,dev,seed+(0 if arch=='temporal' else 5000)+(0 if curriculum=='simple' else 10000));acc,c=ev(m,test_loader)
   hardkeys=['simple_hard','heldout_simple',*TEST_CONTRAST.keys()];hard=float(np.mean([c[k] for k in hardkeys]));out['models'][name]={'overall':acc,'hard_mean':hard,'conditions':c,'history':hist,'extreme_flags':[k for k,v in c.items() if v in (0.,1.)]};print('RESULT',name,out['models'][name],flush=True);del m;gc.collect()
 (OUT/f'R32_COMPOSITIONAL_CURRICULUM_SEED_{seed}.json').write_text(json.dumps(out,indent=2));return out

def main():
 rows=[run(35400),run(35401)];agg={}
 for n in rows[0]['models']:
  agg[n]={'overall':float(np.mean([r['models'][n]['overall'] for r in rows])),'hard_mean':float(np.mean([r['models'][n]['hard_mean'] for r in rows])),'conditions':{k:float(np.mean([r['models'][n]['conditions'][k] for r in rows])) for k in rows[0]['models'][n]['conditions']}}
 obj={'aggregate':agg,'rows':rows,'boundary':'REFERENCE_ONLY architecture-vs-training factorial on continuous TTS with two-action contrast constructions. Learner sees waveform and grounded action consequence only; no transcript, action word, template ID, token, supplied boundary, VAD, ASR, transformer, attention, graph, or LLM enters cognition.'};(OUT/'R32_TTS_COMPOSITIONAL_CURRICULUM_REFERENCE_ONLY.json').write_text(json.dumps(obj,indent=2));print(json.dumps(agg,indent=2))
if __name__=='__main__':main()
