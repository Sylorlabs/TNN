from __future__ import annotations
import hashlib,json
from pathlib import Path
import joblib,numpy as np
R=Path('/mnt/data/r32_epistemic')
import sys
sys.path[:0]=['/mnt/data/r31_part2',str(R)]
import r32_v32_predictive_dynamics_population as v

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
 pre=np.load(R/'R32_V32_PREDICTIVE_DYNAMICS_DATA_SEED_9714.npz');base=np.load(R/'R32_V30_CANDIDATE_HISTORY_DATA_SEED_9714.npz')
 assert np.array_equal(pre['split_code'],base['split_code'])
 assert np.max(np.abs(pre['advantage']-base['advantage']))==0
 xb=base['X_history'].astype(np.float32);pf=pre['predictive_features'].astype(np.float32);xd=np.c_[xb,pf]
 data={k:pre[k] for k in pre.files};data['X_base']=xb;data['X_dynamics']=xd
 tmp=R/'R32_V32_PREDICTIVE_DYNAMICS_DATA_SEED_9714.corrected.tmp.npz';np.savez_compressed(tmp,**data);tmp.replace(R/'R32_V32_PREDICTIVE_DYNAMICS_DATA_SEED_9714.npz')
 matched={'X_max_abs_delta':0.0,'advantage_max_abs_delta':0.0,'split_identical':True}
 models,val=v.fit(xd,data['advantage'].astype(float),data['split_code'],32032);files={}
 for n,m in models.items():
  p=R/f'R32_V32_{n.upper()}_SEED_9714.joblib';joblib.dump(m,p,compress=3);files[n]={'file':p.name,'sha256':sha(p)}
 old=json.loads((R/'R32_V30_CANDIDATE_HISTORY_VALIDATION.json').read_text())
 meta={'seed':v.SEED,'rows':len(data['advantage']),'episodes':int(np.max(data['episode_id'])+1),'base_feature_dim':xb.shape[1],'predictive_feature_dim':pf.shape[1],'augmented_feature_dim':xd.shape[1],'positive_rate':float(np.mean(data['advantage']>0)),'matched_v30':matched,'model_names':v.MODEL_NAMES,'checkpoint_reuse':'predictive features regenerated in rejected preliminary pass; base columns replaced by byte-matched V30 checkpoint before refit','learner_inputs':'V30 state plus prequentially weighted generic predictive-dynamics hypotheses over candidate raw evidence','forbidden_inputs':'mode/resource/trial identity, ambiguity label, true next outcome, future opportunities, final answer, fixed probe count'}
 val['dataset']=meta;val['dataset']['sha256']=sha(R/'R32_V32_PREDICTIVE_DYNAMICS_DATA_SEED_9714.npz');val['models']=files;val['next_outcome_prediction']=v.prediction_metrics(data);val['v30_reference']={'classifier':old['classifier'],'expected_advantage':old['expected_advantage'],'direct':old['direct_expected_advantage']};val['delta_vs_v30']={'classifier_auc':val['classifier']['roc_auc']-old['classifier']['roc_auc'],'classifier_ap':val['classifier']['average_precision']-old['classifier']['average_precision'],'expected_auc':val['expected_advantage']['roc_auc']-old['expected_advantage']['roc_auc'],'tp_cross':val['expected_advantage']['true_positive_cross_zero']-old['expected_advantage']['true_positive_cross_zero'],'fp_cross':val['expected_advantage']['false_positive_cross_zero']-old['expected_advantage']['false_positive_cross_zero'],'mean_pred_actual_positive':val['expected_advantage']['mean_actual_positive']-old['expected_advantage']['mean_actual_positive']}
 val['claim_boundary']='REFERENCE_ONLY matched dynamics-representation ablation. Predictive model evidence comes only from prequential loss on retained candidate observations; evaluator modes and true next outcomes are metrics only.'
 (R/'R32_V32_PREDICTIVE_DYNAMICS_VALIDATION.json').write_text(json.dumps(val,indent=2));cfg={'status':'REFERENCE_ONLY_MATCHED_DYNAMICS_REPRESENTATION','seed':v.SEED,'native_promotion_allowed':False,'runtime_fixed_threshold':False,'source_sha256':sha(R/'r32_v32_predictive_dynamics_population.py'),'completion_source_sha256':sha(Path(__file__)),'matched_v30':matched};(R/'R32_V32_CONFIG.json').write_text(json.dumps(cfg,indent=2));summary={'matched_v30':matched,'predictive_feature_dim':pf.shape[1],'next_outcome_ensemble':val['next_outcome_prediction']['ensemble'],'classifier':val['classifier'],'expected_advantage':val['expected_advantage'],'direct':val['direct'],'delta_vs_v30':val['delta_vs_v30']};(R/'R32_V32_TRAINING.log').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
