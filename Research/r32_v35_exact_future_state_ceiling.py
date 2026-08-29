from __future__ import annotations
import hashlib,json,time,sys
from pathlib import Path
import joblib,numpy as np
ROOT=Path('/mnt/data/r32_epistemic');SEED=35035;K=5;H=6;PER=11
sys.path[:0]=['/mnt/data/r31_part2',str(ROOT)]
import r32_v32_predictive_dynamics_population as v32

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(prefix,models):
 out={}
 for n,m in models.items():
  p=ROOT/f'R32_V35_{prefix}_{n.upper()}_EVAL_ONLY_SEED_9714.joblib';joblib.dump(m,p,compress=3);out[n]={'file':p.name,'sha256':sha(p)}
 return out

def main():
 t0=time.time();z32=np.load(ROOT/'R32_V32_PREDICTIVE_DYNAMICS_DATA_SEED_9714.npz');z33=np.load(ROOT/'R32_V33_LEARNED_GATING_DATA_SEED_9714.npz');z34=np.load(ROOT/'R32_V34_MULTISTEP_STATE_DATA_SEED_9714.npz')
 split=z32['split_code'].astype(int);adv=z32['advantage'].astype(float);X=np.c_[z32['X_dynamics'].astype(np.float32),z33['gate_features'].astype(np.float32)];Y=z34['target_future_state_evaluator_only'].astype(np.float32);P=z34['predicted_future_state'].astype(np.float32)
 assert X.shape[1]==413 and Y.shape[1]==71 and np.array_equal(split,z34['split_code'])
 dist=[];scalar=[]
 for hi in range(H):
  st=hi*PER;dist.extend(range(st,st+K));scalar.extend(range(st+K,st+PER))
 dist.extend(range(H*PER,H*PER+K))
 arms={
  'predicted_future_state':np.c_[X,P],
  'exact_distributions_eval_only':np.c_[X,Y[:,dist]],
  'exact_scalar_dynamics_eval_only':np.c_[X,Y[:,scalar]],
  'exact_all_future_state_eval_only':np.c_[X,Y],
 }
 results={};models={}
 for i,(name,xx) in enumerate(arms.items()):
  print('V35_ARM',name,xx.shape,flush=True);mm,v=v32.fit(xx,adv,split,SEED+i*100);results[name]=v;models[name]=save(name.upper(),mm)
 v33=json.loads((ROOT/'R32_V33_LEARNED_PREDICTIVE_GATING_REFERENCE_ONLY.json').read_text())['action_value']['v32_plus_learned_gate']
 result={'experiment':'R32 V35 exact future-state evaluator-only ceiling audit','base_v33':v33,'arms':results,'delta_vs_v33':{},'models':models,'dataset':{'rows':len(split),'base_dim':X.shape[1],'exact_all_dim':Y.shape[1],'exact_distribution_dim':len(dist),'exact_scalar_dim':len(scalar),'learner_runtime_allowed':False},'claim_boundary':'REFERENCE_ONLY evaluator-only sufficiency audit. Exact future outcomes are never learner inputs and these models cannot be used at runtime or promoted.'}
 for name,v in results.items():
  result['delta_vs_v33'][name]={'classifier_auc':v['classifier']['roc_auc']-v33['classifier']['roc_auc'],'classifier_ap':v['classifier']['average_precision']-v33['classifier']['average_precision'],'expected_auc':v['expected_advantage']['roc_auc']-v33['expected_advantage']['roc_auc'],'beneficial_cross_zero':v['expected_advantage']['true_positive_cross_zero']-v33['expected_advantage']['true_positive_cross_zero'],'nonbeneficial_cross_zero':v['expected_advantage']['false_positive_cross_zero']-v33['expected_advantage']['false_positive_cross_zero'],'selected_realized_advantage':v['expected_advantage']['actual_mean_selected']-v33['expected_advantage']['actual_mean_selected']}
 result['seconds']=time.time()-t0;(ROOT/'R32_V35_EXACT_FUTURE_STATE_CEILING_REFERENCE_ONLY.json').write_text(json.dumps(result,indent=2));cfg={'status':'REFERENCE_ONLY_EVALUATOR_ONLY_SUFFICIENCY_AUDIT','seed':SEED,'runtime_allowed':False,'native_promotion_allowed':False,'source_sha256':sha(Path(__file__))};(ROOT/'R32_V35_CONFIG.json').write_text(json.dumps(cfg,indent=2));(ROOT/'R32_V35_TRAINING.log').write_text(json.dumps({'delta_vs_v33':result['delta_vs_v33'],'arms':results,'seconds':result['seconds']},indent=2)+'\n');(ROOT/'R32_V35_DONE.flag').write_text('');print(json.dumps({'delta_vs_v33':result['delta_vs_v33'],'arms':results,'seconds':result['seconds']},indent=2))
if __name__=='__main__':main()
