from __future__ import annotations
import hashlib,json,time,sys
from pathlib import Path
import numpy as np
ROOT=Path('/mnt/data/r32_epistemic');SEED=36036;H=6;PER=11;K=5
sys.path[:0]=['/mnt/data/r31_part2',str(ROOT)]
import r32_v32_predictive_dynamics_population as v32
FAMILIES={'entropy':5,'dominant_mass':6,'transition_rate':7,'longest_run':8,'same_current_top':9,'return_lag2':10}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def cols(offsets):return [hi*PER+off for hi in range(H) for off in offsets]
def main():
 t0=time.time();z32=np.load(ROOT/'R32_V32_PREDICTIVE_DYNAMICS_DATA_SEED_9714.npz');z33=np.load(ROOT/'R32_V33_LEARNED_GATING_DATA_SEED_9714.npz');z34=np.load(ROOT/'R32_V34_MULTISTEP_STATE_DATA_SEED_9714.npz');X=np.c_[z32['X_dynamics'].astype(np.float32),z33['gate_features'].astype(np.float32)];Y=z34['target_future_state_evaluator_only'].astype(np.float32);split=z32['split_code'].astype(int);adv=z32['advantage'].astype(float)
 arms={name:[off] for name,off in FAMILIES.items()};arms.update({'instability_triplet':[5,7,8],'commit_alignment_pair':[6,9],'instability_plus_return':[5,7,8,10],'all_scalar':[5,6,7,8,9,10]})
 res={}
 for i,(name,offs) in enumerate(arms.items()):
  cc=cols(offs);xx=np.c_[X,Y[:,cc]];print('V36_ARM',name,len(cc),flush=True);_,val=v32.fit(xx,adv,split,SEED+i*100);res[name]={'columns':cc,'offsets':offs,'metrics':val}
 v33=json.loads((ROOT/'R32_V33_LEARNED_PREDICTIVE_GATING_REFERENCE_ONLY.json').read_text())['action_value']['v32_plus_learned_gate'];allv=json.loads((ROOT/'R32_V35_EXACT_FUTURE_STATE_CEILING_REFERENCE_ONLY.json').read_text())['arms']['exact_scalar_dynamics_eval_only']
 out={'experiment':'R32 V36 exact scalar-family evaluator-only causal ablation','base_v33':v33,'v35_exact_all_scalar_reference':allv,'families':res,'ranking_expected_auc':sorted([{'family':n,'auc':v['metrics']['expected_advantage']['roc_auc'],'beneficial_cross':v['metrics']['expected_advantage']['true_positive_cross_zero'],'false_cross':v['metrics']['expected_advantage']['false_positive_cross_zero'],'selected_advantage':v['metrics']['expected_advantage']['actual_mean_selected'],'classifier_ap':v['metrics']['classifier']['average_precision']} for n,v in res.items()],key=lambda x:x['auc'],reverse=True),'seconds':time.time()-t0,'claim_boundary':'REFERENCE_ONLY evaluator-only target sufficiency ablation. Exact future scalar values are never runtime inputs.'};(ROOT/'R32_V36_EXACT_SCALAR_FAMILY_ABLATION_REFERENCE_ONLY.json').write_text(json.dumps(out,indent=2));cfg={'status':'REFERENCE_ONLY_EVAL_ONLY_SCALAR_CAUSAL_ABLATION','seed':SEED,'runtime_allowed':False,'source_sha256':sha(Path(__file__)),'native_promotion_allowed':False};(ROOT/'R32_V36_CONFIG.json').write_text(json.dumps(cfg,indent=2));(ROOT/'R32_V36_TRAINING.log').write_text(json.dumps({'ranking':out['ranking_expected_auc'],'seconds':out['seconds']},indent=2)+'\n');(ROOT/'R32_V36_DONE.flag').write_text('');print(json.dumps({'ranking':out['ranking_expected_auc'],'seconds':out['seconds']},indent=2))
if __name__=='__main__':main()
