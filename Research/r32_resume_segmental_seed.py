from __future__ import annotations
import gc,json,sys
from pathlib import Path
import numpy as np
from torch.utils.data import DataLoader
import r32_tts_segmental_pam as d

OUT=Path('/mnt/data/r32_epistemic')

def prepare(seed:int):
    specs,test=d.build_specs(seed,2)
    rng=np.random.default_rng(seed);ix=np.arange(len(specs));rng.shuffle(ix)
    nd=max(240,int(.12*len(ix)));dv=set(map(int,ix[:nd]))
    tr=d.AcousticDataset([s for i,s in enumerate(specs) if i not in dv],seed)
    dev=d.AcousticDataset([s for i,s in enumerate(specs) if i in dv],seed+91)
    te=d.AcousticDataset(test,seed+193)
    return tr,dev,te

def run(seed:int,name:str):
    tr,dev,te=prepare(seed)
    if name=='temporal_conv': offset=0
    elif name=='segmental_recurrent': offset=10000
    else: raise ValueError(name)
    import torch
    torch.manual_seed(seed+offset)
    if name=='temporal_conv': model=d.TemporalConvPAM()
    elif name=='segmental_recurrent': model=d.SegmentalRecurrentPAM()
    hist=d.train_model(model,tr,dev,seed+offset,epochs=12)
    loader=DataLoader(te,batch_size=64,shuffle=False,collate_fn=d.collate,num_workers=0)
    acc,detail=d.evaluate(model,loader)
    hard_keys=['speaker_speed','hard_noise','heldout_comp',*d.TEST_TEMPLATES.keys()]
    hard=float(np.mean([detail['conditions'][k] for k in hard_keys]))
    out={'seed':seed,'model':name,'train_n':len(tr),'dev_n':len(dev),'test_n':len(te),'overall':acc,'hard_mean':hard,**detail,'history':hist,'extreme_flags':[k for k,v in detail['conditions'].items() if v in (0.,1.)]}
    p=OUT/f'R32_SEGMENTAL_PAM_SEED_{seed}_{name}.json';p.write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2),flush=True)

if __name__=='__main__':run(int(sys.argv[1]),sys.argv[2])
