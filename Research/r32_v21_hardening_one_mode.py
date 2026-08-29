import sys,json,time
from pathlib import Path
sys.path.insert(0,'/mnt/data/r31_part2');sys.path.insert(0,'/mnt/data/r32_epistemic')
import r31_sequential_evidence_abstention_REFERENCE_ONLY as r31
import r32_epistemic_r31_matched_v21_REFERENCE_ONLY as v
import r32_v21_reusable_probe_hardening_REFERENCE_ONLY as h
seed=int(sys.argv[1]);mode=sys.argv[2];n=int(sys.argv[3]);t=time.time()
env=r31.setup(seed);safe=v.train_A(seed,env);models=v.load_models();res=h.eval_mode(seed,mode,env,models,safe,n)
out={'seed':seed,'mode':mode,'n':n,'result':res,'seconds':time.time()-t}
p=Path('/mnt/data/r32_epistemic')/f'R32_V21_HARDENING_MODE_{mode}_SEED_{seed}.json';p.write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2),flush=True)
