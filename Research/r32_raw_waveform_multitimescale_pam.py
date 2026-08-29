from __future__ import annotations
import os, json, hashlib, random, subprocess, glob, time, gc, math
from pathlib import Path
from dataclasses import dataclass
import numpy as np
from scipy.io import wavfile
from scipy.signal import resample_poly
import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader

ROOT=Path('/mnt/data/r32_epistemic');CACHE=ROOT/'raw_tts_cache';CACHE.mkdir(exist_ok=True)
ACTORS=['ava','ben','cora','drew','eli','fern']
ACTIONS=['move','touch','push','hold','open','guide']
OBJECTS=['amber cube','blue ring','green star','silver bar','ivory disk','red cone']
TRAIN_VOICES=['en-us','en-sc','en-uk-north','en-uk-wmids'];TEST_VOICES=['en-uk-rp','en-wi']
TRAIN_TEMPLATES=[
 '{actor} {action} the {object} now',
 'please {action} that {object} {actor}',
 '{actor} will {action} this {object}',
]
TEST_TEMPLATES=[
 '{action} the {object} now {actor}',
 'for {actor} the requested act is to {action} the {object}',
 '{actor} needs the {object}; the action is {action}',
]
SR=8000;MAX_SAMPLES=28000


def atomic(path,obj):
 tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(json.dumps(obj,indent=2,sort_keys=True));tmp.replace(path)

def synth(text,voice,speed,pitch):
 key=hashlib.sha1(f'{text}|{voice}|{speed}|{pitch}'.encode()).hexdigest()[:24];p=CACHE/f'{key}.wav'
 if not p.exists():
  tmp=CACHE/f'{key}.{os.getpid()}.wav';subprocess.run(['espeak','-v',voice,'-s',str(speed),'-p',str(pitch),'-w',str(tmp),text],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);tmp.replace(p)
 sr,x=wavfile.read(p);x=x.astype(np.float32);x/=max(1,float(np.max(np.abs(x))))
 if sr!=SR:x=resample_poly(x,SR,sr).astype(np.float32)
 return x

def damage(x,cond,r):
 y=x.copy()
 if cond=='clean':return y
 if cond=='noise':y+=r.normal(0,.025,len(y)).astype(np.float32)
 elif cond=='hard_noise':y+=r.normal(0,.055,len(y)).astype(np.float32)
 elif cond=='onset_loss':y[:min(len(y)//4,3200)]=0
 elif cond=='low_energy_removed':y[np.abs(y)<np.quantile(np.abs(y),.42)]=0
 elif cond=='dropout':
  for _ in range(3):
   n=max(100,len(y)//14);s=int(r.integers(0,max(1,len(y)-n)));y[s:s+n]=0
 elif cond=='reverb':
  delay=220;z=y.copy();z[delay:]+=0.35*y[:-delay];y=z
 return np.clip(y,-1,1)

@dataclass(frozen=True)
class Spec:
 text:str;action:int;voice:str;speed:int;pitch:int;condition:str;seed:int

def make_specs(seed):
 r=random.Random(seed);train=[]
 for i in range(2400):
  a=r.randrange(len(ACTIONS));actor=r.choice(ACTORS);obj=r.choice(OBJECTS);tpl=r.choice(TRAIN_TEMPLATES)
  train.append(Spec(tpl.format(actor=actor,action=ACTIONS[a],object=obj),a,r.choice(TRAIN_VOICES),r.choice([135,165,195]),r.choice([38,50,62]),'clean',seed*100000+i))
 dev=[]
 for i in range(360):
  a=i%len(ACTIONS);actor=ACTORS[(i//6)%len(ACTORS)];obj=OBJECTS[(i//36)%len(OBJECTS)];tpl=TRAIN_TEMPLATES[i%len(TRAIN_TEMPLATES)]
  dev.append(Spec(tpl.format(actor=actor,action=ACTIONS[a],object=obj),a,TRAIN_VOICES[i%len(TRAIN_VOICES)],165,50,'noise',seed*200000+i))
 tests={}
 conditions={
  'heldout_layout':(TEST_VOICES,[150,180],[42,58],'clean'),
  'speaker_speed':(TEST_VOICES,[110,230],[35,70],'noise'),
  'hard_noise':(TEST_VOICES,[150,190],[45,60],'hard_noise'),
  'onset_loss':(TEST_VOICES,[150,190],[45,60],'onset_loss'),
  'low_energy_removed':(TEST_VOICES,[150,190],[45,60],'low_energy_removed'),
  'dropout':(TEST_VOICES,[150,190],[45,60],'dropout'),
  'reverb':(TEST_VOICES,[150,190],[45,60],'reverb'),
 }
 for cond,(voices,speeds,pitches,dmg) in conditions.items():
  z=[]
  for i in range(360):
   a=i%len(ACTIONS);actor=ACTORS[(i//6)%len(ACTORS)];obj=OBJECTS[(i//36)%len(OBJECTS)];tpl=TEST_TEMPLATES[(i//72)%len(TEST_TEMPLATES)]
   z.append(Spec(tpl.format(actor=actor,action=ACTIONS[a],object=obj),a,voices[i%len(voices)],speeds[(i//2)%len(speeds)],pitches[(i//3)%len(pitches)],dmg,seed*300000+hash(cond)%10000+i))
  tests[cond]=z
 return train,dev,tests

class AudioDS(Dataset):
 def __init__(self,specs,augment=False):self.specs=specs;self.augment=augment
 def __len__(self):return len(self.specs)
 def __getitem__(self,i):
  s=self.specs[i];x=synth(s.text,s.voice,s.speed,s.pitch);r=np.random.default_rng(s.seed+(i*13 if self.augment else 0));x=damage(x,s.condition,r)
  if self.augment:
   x=damage(x,'noise',r)
   if r.random()<.25:x=damage(x,'dropout',r)
  n=min(MAX_SAMPLES,len(x));y=np.zeros(MAX_SAMPLES,np.float32);y[:n]=x[:n]
  return torch.from_numpy(y),int(n),s.action

def collate(batch):
 x=torch.stack([a for a,_,_ in batch]);n=torch.tensor([b for _,b,_ in batch]);y=torch.tensor([c for _,_,c in batch]);return x,n,y

class ConvEncoder(nn.Module):
 def __init__(self,dim=96):
  super().__init__();self.net=nn.Sequential(nn.Conv1d(1,32,21,5,10),nn.GELU(),nn.Conv1d(32,64,11,4,5),nn.GELU(),nn.Conv1d(64,dim,7,2,3),nn.GELU(),nn.GroupNorm(8,dim))
 def forward(self,x,n):
  h=self.net(x[:,None,:]).transpose(1,2);ln=torch.clamp((n+39)//40,min=1,max=h.shape[1]);return h,ln

class PlainPAM(nn.Module):
 def __init__(self,dim=96,hidden=96):
  super().__init__();self.enc=ConvEncoder(dim);self.rnn=nn.GRU(dim,hidden,batch_first=True);self.head=nn.Linear(hidden*2,len(ACTIONS))
 def forward(self,x,n):
  h,ln=self.enc(x,n);z,_=self.rnn(h);mask=torch.arange(z.shape[1],device=z.device)[None,:]<ln[:,None];mean=(z*mask[:,:,None]).sum(1)/ln[:,None];last=z[torch.arange(len(z),device=z.device),ln-1];return self.head(torch.cat([mean,last],1)),None

class MultiTimescalePAM(nn.Module):
 # Fast recurrent evidence remains intact; a learned soft gate updates a slower state.
 # The gate is not a supplied boundary and never discards the fast route.
 def __init__(self,dim=96,hidden=96):
  super().__init__();self.enc=ConvEncoder(dim);self.cell=nn.GRUCell(dim,hidden);self.gate=nn.Sequential(nn.Linear(hidden*2,hidden//2),nn.Tanh(),nn.Linear(hidden//2,1));self.head=nn.Linear(hidden*3,len(ACTIONS));nn.init.constant_(self.gate[-1].bias,-1.25)
 def forward(self,x,n):
  seq,ln=self.enc(x,n);B,T,D=seq.shape;fast=torch.zeros(B,self.cell.hidden_size,device=x.device);slow=torch.zeros_like(fast);sumfast=torch.zeros_like(fast);gates=[]
  for t in range(T):
   new=self.cell(seq[:,t],fast);delta=torch.abs(new-fast);g=torch.sigmoid(self.gate(torch.cat([new,delta],1)))
   valid=(t<ln).float()[:,None];g=g*valid;slow=slow*(1-g)+new*g;fast=new*valid+fast*(1-valid);sumfast+=fast*valid;gates.append(g)
  mean=sumfast/ln[:,None];logits=self.head(torch.cat([mean,fast,slow],1));G=torch.cat(gates,1);resource=G.mean();smooth=torch.mean(torch.abs(G[:,1:]-G[:,:-1])) if T>1 else resource*0
  return logits,(resource,smooth,G)

def train_model(kind,train,dev,seed,epochs=14):
 torch.manual_seed(seed);np.random.seed(seed);device=torch.device('cpu');m=PlainPAM() if kind=='plain' else MultiTimescalePAM();m.to(device);opt=torch.optim.AdamW(m.parameters(),lr=2e-3,weight_decay=1e-4);lossfn=nn.CrossEntropyLoss();tr=DataLoader(AudioDS(train,True),batch_size=24,shuffle=True,num_workers=0,collate_fn=collate);dv=DataLoader(AudioDS(dev),batch_size=32,shuffle=False,num_workers=0,collate_fn=collate);hist=[];best=None;bestacc=-1
 for ep in range(1,epochs+1):
  m.train();tot=ok=lossn=0;gs=[]
  for x,n,y in tr:
   opt.zero_grad();log,aux=m(x,n);loss=lossfn(log,y)
   if aux is not None:
    resource,smooth,_=aux;loss=loss+0.004*resource+0.001*smooth;gs.append(float(resource.detach()))
   loss.backward();nn.utils.clip_grad_norm_(m.parameters(),3);opt.step();tot+=len(y);ok+=int((log.argmax(1)==y).sum());lossn+=float(loss.detach())*len(y)
  m.eval();dtotal=dok=0
  with torch.no_grad():
   for x,n,y in dv:log,_=m(x,n);dtotal+=len(y);dok+=int((log.argmax(1)==y).sum())
  row={'epoch':ep,'train_acc':ok/tot,'train_loss':lossn/tot,'dev_acc':dok/dtotal,'gate_mean':float(np.mean(gs)) if gs else None};hist.append(row);print(kind,row,flush=True)
  if row['dev_acc']>bestacc:bestacc=row['dev_acc'];best={k:v.detach().cpu().clone() for k,v in m.state_dict().items()}
 if best:m.load_state_dict(best)
 return m,hist

def evaluate(m,specs):
 dl=DataLoader(AudioDS(specs),batch_size=32,shuffle=False,num_workers=0,collate_fn=collate);m.eval();ok=tot=0;g=[]
 with torch.no_grad():
  for x,n,y in dl:
   log,aux=m(x,n);ok+=int((log.argmax(1)==y).sum());tot+=len(y)
   if aux is not None:g.append(float(aux[0]))
 return {'accuracy':ok/tot,'n':tot,'gate_mean':float(np.mean(g)) if g else None}

def run(seed):
 t=time.time();train,dev,tests=make_specs(seed);out={'seed':seed,'models':{}}
 for kind in ('plain','multitimescale'):
  m,h=train_model(kind,train,dev,seed+(0 if kind=='plain' else 1000));z={'history':h,'dev_best':max(x['dev_acc'] for x in h),'conditions':{k:evaluate(m,v) for k,v in tests.items()}}
  z['hard_mean']=float(np.mean([q['accuracy'] for q in z['conditions'].values()]));out['models'][kind]=z
  torch.save(m.state_dict(),ROOT/f'R32_RAW_WAVE_{kind.upper()}_SEED_{seed}.pt');atomic(ROOT/f'R32_RAW_WAVE_{kind.upper()}_SEED_{seed}.json',z);gc.collect()
 out['elapsed_seconds']=time.time()-t;out['boundary']='REFERENCE_ONLY raw-waveform causal convolution/recurrent PAM. Soft slow-state gates are learner-controlled and do not receive transcript, word/phoneme/chunk boundary, VAD, ASR, tokenizer, transformer or LLM inputs.';return out

def main():
 seed=37000;p=ROOT/f'R32_RAW_WAVEFORM_MULTITIMESCALE_SEED_{seed}.json'
 out=run(seed);atomic(p,out);print(json.dumps({'seed':seed,'plain':out['models']['plain']['hard_mean'],'multitimescale':out['models']['multitimescale']['hard_mean']},indent=2))
if __name__=='__main__':main()
