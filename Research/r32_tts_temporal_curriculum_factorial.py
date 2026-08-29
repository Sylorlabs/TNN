from __future__ import annotations
import json, math, os, sys, time
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np, torch
import torch.nn as nn
from torch.utils.data import DataLoader,Dataset
import r32_tts_segmental_pam as d

OUT=Path('/mnt/data/r32_epistemic');torch.set_num_threads(max(1,min(5,os.cpu_count() or 1)))
ACTORS=d.base.ACTORS;A=d.base.ACTIONS;OBJECTS=d.base.OBJECTS
POLICIES=['repeated_matched','balanced_diverse','hard_diverse']
NTRAIN=5676
DIV_VOICES=['en-us','en','en-sc','en-uk-north','en-uk-wmids']
DIV_SPEED=[115,145,175,205,235];DIV_PITCH=[28,45,62,78]
DIV_TEMPLATES=[
 '{actor} {action} the {object} now',
 'now {actor} should {action} the {object} carefully',
 'before anything else, {actor} will {action} the {object}',
 'the {object} is ready and {actor} must {action} it',
 'please observe as {actor} begins to {action} the {object}',
 'when ready, {actor} can {action} the {object}',
]

class Mem(Dataset):
 def __init__(self,rows):self.rows=rows
 def __len__(self):return len(self.rows)
 def __getitem__(self,i):return self.rows[i]

def feature_rows(specs):return [(d.feat(d.synth(s),s.perturb_seed,s.perturb_strength),s.action_i,s.condition) for s in specs]

def common_dev(seed):
 specs,_=d.build_specs(seed+701,1);dv=[s for s in specs if s.split=='dev']
 return dv[:min(900,len(dv))]

def repeated(seed):
 specs,_=d.build_specs(seed,2);tr=[s for s in specs if s.split=='train']
 if len(tr)<NTRAIN:tr=(tr*((NTRAIN+len(tr)-1)//len(tr)))
 return tr[:NTRAIN]

def diverse(seed,hard=False):
 rng=np.random.default_rng(seed+(999 if hard else 0));rows=[];comb=[(ai,yi,oi) for ai in range(len(ACTORS)) for yi in range(len(A)) for oi in range(len(OBJECTS))]
 rng.shuffle(comb);i=0
 while len(rows)<NTRAIN:
  ai,yi,oi=comb[i%len(comb)];cycle=i//len(comb);i+=1
  if hard:
   voice=DIV_VOICES[(cycle+ai+oi)%len(DIV_VOICES)];speed=DIV_SPEED[(cycle*2+yi)%len(DIV_SPEED)];pitch=DIV_PITCH[(cycle+ai+yi)%len(DIV_PITCH)];strength=2+(cycle+oi)%2
   template=DIV_TEMPLATES[(cycle+yi+oi)%len(DIV_TEMPLATES)]
  else:
   voice=DIV_VOICES[(cycle+ai+yi)%len(DIV_VOICES)];speed=DIV_SPEED[(cycle+oi)%len(DIV_SPEED)];pitch=DIV_PITCH[(cycle+yi)%len(DIV_PITCH)];strength=(cycle+ai+oi)%3
   template=DIV_TEMPLATES[(cycle+ai+yi+oi)%len(DIV_TEMPLATES)]
  text=template.format(actor=ACTORS[ai],action=A[yi],object=OBJECTS[oi])
  rows.append(d.Spec(text,ai,yi,oi,ACTORS[ai],A[yi],OBJECTS[oi],voice,speed,pitch,template,seed*1000003+i*7919,strength,'train','development'))
 return rows

def train(seed,policy):
 t0=time.time();specs=repeated(seed) if policy=='repeated_matched' else diverse(seed,policy=='hard_diverse');dv=common_dev(seed)
 print('DATA',policy,len(specs),len(dv),flush=True);trrows=feature_rows(specs);dvrows=feature_rows(dv);torch.manual_seed(seed+POLICIES.index(policy)*1000);m=d.TemporalConvPAM()
 tl=DataLoader(Mem(trrows),batch_size=64,shuffle=True,collate_fn=d.collate,num_workers=0,generator=torch.Generator().manual_seed(seed+31));dl=DataLoader(Mem(dvrows),batch_size=96,shuffle=False,collate_fn=d.collate,num_workers=0)
 opt=torch.optim.AdamW(m.parameters(),lr=1.5e-3,weight_decay=2e-4);best=None;bestacc=-1;hist=[]
 for ep in range(7):
  m.train();lossn=0;n=0
  for x,l,y,_ in tl:
   opt.zero_grad();z,_=m(x,l);loss=nn.functional.cross_entropy(z,y);loss.backward();torch.nn.utils.clip_grad_norm_(m.parameters(),5);opt.step();lossn+=loss.item()*len(y);n+=len(y)
  m.eval();ok=tot=0
  with torch.no_grad():
   for x,l,y,_ in dl:z,_=m(x,l);ok+=(z.argmax(1)==y).sum().item();tot+=len(y)
  acc=ok/max(1,tot);hist.append({'epoch':ep+1,'loss':lossn/n,'dev':acc});print('EPOCH',policy,ep+1,lossn/n,acc,flush=True)
  if acc>bestacc:bestacc=acc;best={k:v.detach().clone() for k,v in m.state_dict().items()}
 m.load_state_dict(best);m.eval();ch=d.challenge_specs(seed+9000);cr=feature_rows(ch);by=defaultdict(lambda:[0,0])
 with torch.no_grad():
  for x,l,y,c in DataLoader(Mem(cr),batch_size=96,shuffle=False,collate_fn=d.collate,num_workers=0):
   z,_=m(x,l);p=z.argmax(1)
   for pp,yy,cc in zip(p.tolist(),y.tolist(),c):by[cc][0]+=int(pp==yy);by[cc][1]+=1
 acc={k:a/n for k,(a,n) in by.items()};hard=float(np.mean(list(acc.values())));worst=float(min(acc.values()));flags=[k for k,v in acc.items() if v in (0,1)]
 dist={'voices':dict(Counter(s.voice for s in specs)),'strength':dict(Counter(str(s.perturb_strength) for s in specs)),'templates':len(set(s.template for s in specs))}
 out={'seed':seed,'policy':policy,'train_n':len(specs),'dev_n':len(dv),'dev_best':bestacc,'history':hist,'condition_accuracy':acc,'hard_mean':hard,'worst_condition':worst,'extreme_flags':flags,'training_distribution':dist,'seconds':time.time()-t0,'boundary':'REFERENCE_ONLY frozen non-transformer temporal-PAM curriculum factorial. Architecture, optimizer, encounter count, evaluation and seeds are matched; only waveform-experience distribution changes. Text/templates are external TTS world generators only. No transcript/token/word/phoneme/chunk boundary/VAD/ASR/attention/transformer/LLM enters learner cognition.'}
 (OUT/f'R32_TEMPORAL_CURRICULUM_{policy}_SEED_{seed}.json').write_text(json.dumps(out,indent=2));torch.save({'state_dict':best,'seed':seed,'policy':policy},OUT/f'R32_TEMPORAL_CURRICULUM_{policy}_MODEL_{seed}.pt');print('RESULT',policy,hard,worst,flags,flush=True);return out

def main(seed):
 rows=[]
 for p in POLICIES:rows.append(train(seed,p))
 out={'seed':seed,'results':{r['policy']:{k:r[k] for k in ['hard_mean','worst_condition','dev_best','extreme_flags','seconds']} for r in rows},'ranking':sorted([(r['hard_mean'],r['worst_condition'],r['policy']) for r in rows],reverse=True),'boundary':rows[0]['boundary']}
 (OUT/f'R32_TEMPORAL_CURRICULUM_FACTORIAL_SEED_{seed}.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
if __name__=='__main__':main(int(sys.argv[1]) if len(sys.argv)>1 else 35500)
