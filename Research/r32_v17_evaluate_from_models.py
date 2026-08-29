from __future__ import annotations
import sys,json,hashlib,joblib
from pathlib import Path
import numpy as np
sys.path.insert(0,'/mnt/data/r31_part2');sys.path.insert(0,'/mnt/data/r32_epistemic')
import r31_sequential_evidence_abstention_REFERENCE_ONLY as r31
import r32_epistemic_r31_matched_v17_cached_REFERENCE_ONLY as v
# Reuse the exact V16 forced battery functions; redirect its global v to cached V17.
import r32_v16_reusable_probe_hardening_REFERENCE_ONLY as h
h.v=v
ROOT=Path('/mnt/data/r32_epistemic')
def load_models():
 names=['KEEP','COMMIT','EPOCH','UNKNOWN','INSPECT'];ms=[joblib.load(ROOT/f'R32_V17_MODEL_{n}_SEED_9714.joblib') for n in names]
 meta=json.loads((ROOT/'R32_V17_TRAINING_DATA_SEED_9714_META.json').read_text());return (*ms,meta)
def main(seed=9714,n=100):
 env=r31.setup(seed);safe=v.train_A(seed,env);models=load_models();res={m:h.eval_mode(seed,m,env,models,safe,n) for m in h.MODES};agg={'seed':seed,'n_per_mode':n,'training':models[-1],'modes':res,'summary':{}}
 for arm in ['one_shot','reusable']:
  agg['summary'][arm]={'no_unique_unknown':float(np.mean([res[m][arm]['unknown'] for m in ['balanced_no_unique','biased_no_unique']])), 'resolvable_success':float(np.mean([res[m][arm]['success'] for m in ['stable_weak','unstable_then_stable','replacement','reversal']])), 'costly_unknown':res['costly_stable'][arm]['unknown'], 'wrong_commit':float(np.mean([res[m][arm]['wrong_commit'] for m in h.MODES])), 'mean_trials':float(np.mean([res[m][arm]['mean_trials'] for m in h.MODES])), 'runaway':float(np.mean([res[m][arm]['runaway'] for m in h.MODES]))}
 agg['boundary']='REFERENCE_ONLY V17. V16 architecture/current-epoch hypothesis/credit/runtime unchanged; only delayed-nonconvergent high-uncertainty replay support is balanced. Checkpointed generation preserves exact RNG state/counters; cached feature implementation was parity-checked at max abs delta 0 on the tested trajectory. No mode/state/ambiguity label or fixed runtime probe count.'
 p=ROOT/f'R32_V17_REUSABLE_PROBE_HARDENING_SEED_{seed}.json';p.write_text(json.dumps(agg,indent=2));print(json.dumps(agg['summary'],indent=2));print('SHA',hashlib.sha256(p.read_bytes()).hexdigest())
if __name__=='__main__':main(int(sys.argv[1]) if len(sys.argv)>1 else 9714,int(sys.argv[2]) if len(sys.argv)>2 else 100)
