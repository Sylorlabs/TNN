#!/usr/bin/env python3
import argparse,json
from pathlib import Path
import torch, numpy as np
import speech_joint_core_r29 as j

def make_condition(world,seed,name,n):
 if name=='recoverable_hard':return j.make_rows(world,n,seed+300000,'hard',(2,8),[18,19])
 if name=='inserted_silence':return j.make_rows(world,n,seed+400000,'hard',(2,8),[18,20],.42,0)
 if name=='endpoint_damage':return j.make_rows(world,n,seed+500000,'hard',(2,8),[19,20],.10,.28)
 if name=='severe':return j.make_rows(world,n,seed+600000,'severe',(2,8),[20,21])
 if name=='long_8_10':return j.make_rows(world,n,seed+700000,'hard',(8,10),[18,21])
 if name=='long_11_14':return j.make_rows(world,n,seed+710000,'hard',(11,14),[22,23])
 if name=='near_twin_stress':
  twin=j.AcousticWorld(seed+33,16,30,True);return j.make_rows(twin,n,seed+800000,'hard',(2,8),[18,19])
 if name=='severe_silence_endpoint':return j.make_rows(world,n,seed+900000,'severe',(2,9),[22,23],.45,.35)
 if name=='no_repeats':return j.make_rows(world,n,seed+910000,'hard',(2,8),[18,19],0,0,False)
 if name=='repeat_dense':
  r=np.random.default_rng(seed+920000);rows=[]
  for _ in range(n):
   c=int(r.integers(3,9));q=world.utterance(r,'hard',c,[18,19],0,0,True)
   if c>=3:q.y[1]=q.y[0]
   rows.append(q)
  return rows
 raise ValueError(name)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--seed',type=int,required=True);ap.add_argument('--checkpoint',required=True);ap.add_argument('--condition',required=True);ap.add_argument('--n',type=int,default=600);ap.add_argument('--out',required=True);a=ap.parse_args()
 w=j.AcousticWorld(a.seed,16,30,False);m=j.JointPAM(16);ck=torch.load(a.checkpoint,map_location='cpu',weights_only=False);m.load_state_dict(ck['state_dict']);rows=make_condition(w,a.seed,a.condition,a.n);res=j.eval_rows(m,rows,16,64);obj={'seed':a.seed,'checkpoint_epoch':ck.get('epoch'),'condition':a.condition,'trials':len(rows),'metrics':res,'claim_boundary':'Raw connected waveform; no VAD or boundaries. Python reference checkpoint evaluation.'};Path(a.out).parent.mkdir(parents=True,exist_ok=True);Path(a.out).write_text(json.dumps(obj,indent=2));print(json.dumps(obj,indent=2))
if __name__=='__main__':main()
