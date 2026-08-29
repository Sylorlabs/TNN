from __future__ import annotations
import gc,json,os,sys
from pathlib import Path
import numpy as np
import torch
from torch.utils.data import DataLoader

import r32_tts_segmental_pam as d

OUT=Path('/mnt/data/r32_epistemic')
torch.set_num_threads(max(1,min(5,os.cpu_count() or 1)))
DOSES=[1,2,4]

def key(s): return (s.actor_i,s.action_i,s.object_i,s.voice,s.speed,s.pitch,s.template)

def run(seed:int):
    all_specs,test_specs=d.build_specs(seed,max(DOSES))
    keys=sorted({key(s) for s in all_specs})
    rng=np.random.default_rng(seed); rng.shuffle(keys)
    dev_keys=set(keys[:max(120,int(.12*len(keys)))])
    test_ds=d.AcousticDataset(test_specs,seed+193)
    rows=[]
    for dose in DOSES:
        tr_specs=[s for s in all_specs if key(s) not in dev_keys and s.perturb_strength<dose]
        # Development is fixed clean experience from held-out developmental keys.
        dv_specs=[]
        seen=set()
        for s in all_specs:
            k=key(s)
            if k in dev_keys and k not in seen and s.perturb_strength==0:
                dv_specs.append(s);seen.add(k)
        tr=d.AcousticDataset(tr_specs,seed)
        dv=d.AcousticDataset(dv_specs,seed+91)
        torch.manual_seed(seed+100*dose)
        model=d.TemporalConvPAM()
        hist=d.train_model(model,tr,dv,seed+100*dose,epochs=12,batch_size=32)
        te=DataLoader(test_ds,batch_size=64,shuffle=False,collate_fn=d.collate,num_workers=0)
        overall,detail=d.evaluate(model,te)
        hard_keys=['speaker_speed','hard_noise','heldout_comp',*d.TEST_TEMPLATES.keys()]
        hard=float(np.mean([detail['conditions'][k] for k in hard_keys]))
        row={'seed':seed,'dose':dose,'train_n':len(tr),'dev_n':len(dv),'overall':overall,'hard_mean':hard,**detail,'history':hist,'extreme_flags':[k for k,v in detail['conditions'].items() if v in (0.,1.)]}
        rows.append(row)
        (OUT/f'R32_TEMPORAL_DOSE_SEED_{seed}_D{dose}.json').write_text(json.dumps(row,indent=2))
        print('DOSE_RESULT',json.dumps({k:row[k] for k in ['seed','dose','train_n','overall','hard_mean','conditions','extreme_flags']}),flush=True)
        del model,tr,dv;gc.collect()
    out={'seed':seed,'rows':rows,'boundary':'REFERENCE_ONLY frozen non-transformer temporal-PAM training-dose curve. Architecture and evaluation are fixed; only the amount/diversity of raw-waveform developmental exposure changes. No transcript, token, word/phoneme/chunk boundary, VAD, ASR, attention/transformer, or LLM enters cognition.'}
    (OUT/f'R32_TEMPORAL_DOSE_CURVE_SEED_{seed}.json').write_text(json.dumps(out,indent=2));return out

if __name__=='__main__':
    seed=int(sys.argv[1]) if len(sys.argv)>1 else 35300
    run(seed)
