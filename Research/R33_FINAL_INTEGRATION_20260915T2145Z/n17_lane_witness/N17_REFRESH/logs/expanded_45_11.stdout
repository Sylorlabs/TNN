from __future__ import annotations
import hashlib,json,time
from collections import defaultdict
from pathlib import Path
import numpy as np
ROOT=Path('/mnt/data/r32_epistemic')
import sys;sys.path[:0]=['/mnt/data/r31_part2',str(ROOT)]
import r31_sequential_evidence_abstention_REFERENCE_ONLY as r31
import r32_epistemic_r31_matched_v17_cached_REFERENCE_ONLY as v
import r32_v26_candidate_selected_conditional_advantage as world
import r32_v28_learned_resource_shadow_price as resource
import r32_v28_complete_from_checkpoint as resource_fast
import r32_v39_candidate_recurrent_temporal_pam as v39
import r32_v41_live_horizon_hazard_qualification as live

TRIALS=12

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def episode_oracle(epseed,mode,ri,env,safe,models):
 ep=v.make_ep(epseed,'genuine_ambiguity',env);ep.avail[:]=False;ep.avail[0]=ep.avail[1]=ep.avail[live.SOURCE]=True;params=world.world_params(epseed,mode);ep.cost[live.SOURCE]=params.cost
 ctxseed=live.EVAL_SEED*70_000_000+live.MODES.index(mode)*5_000_000+ri*700_000+(epseed%100000)*71+41;ctx=resource.draw_context(ctxseed,ri);cache=resource_fast.context_cache(ctx);budget=ctx.budget
 st=v.initial_state(ep,env,'D');a0=int(env[5][int(np.argmax(st.p(True))) ]);cons=world.delayed_consensus_from_outcomes(ep,mode,params);used=[];path=[];controller=[];evaluator=[]
 for trial in range(TRIALS+1):
  dec,choice,qs,um=live.terminal_values(st,ep,safe,a0,env,models);controller.append({'trial':trial,'decision':int(dec),'choice':choice,'unresolved_mass':um,'q':qs});evaluator.append(float(world.terminal_utility(st,a0,cons,env)))
  if trial==TRIALS:break
  cur=evaluator[-1];actual_loss=float(resource_fast.fast_actual_loss(cache,budget,params.cost));vec,action=v39.evidence_and_action(ep,mode,params,st,env,used,trial);z=st.clone();z.add(live.SOURCE,vec,params.cost);nxt=float(world.terminal_utility(z,a0,cons,env));path.append((cur,nxt,actual_loss));st=z;budget=max(0.,budget-params.cost)
 cont=-1e9;advs=[]
 for cur,nxt,cost in reversed(path):
  ret=max(nxt,cont)-cost;advs.append(float(ret-cur));cont=ret
 advs.reverse();want=live.desired(ep,mode)
 first_eval=next((i for i,u in enumerate(evaluator) if u>=.999),None);first_ctrl=next((q['trial'] for q in controller if q['decision']==want),None)
 return {'initial_option_advantage':advs[0],'option_advantage_by_trial':advs,'oracle_initial_beneficial':bool(advs[0]>0),'evaluator_terminal_utility_by_trial':evaluator,'first_evaluator_resolved_trial':first_eval,'first_terminal_controller_correct_trial':first_ctrl,'consensus_evaluator_only':cons,'desired':int(want),'raw_probe_cost':params.cost,'resource_regime_evaluator_only':live.RESOURCE_REGIMES[ri]}

def main():
 t0=time.time();env=r31.setup(live.ENV_SEED);safe=v.train_A(live.ENV_SEED,env);models=live.LiveModels();z=json.loads((ROOT/'R32_V41_LIVE_HORIZON_HAZARD_QUALIFICATION_REFERENCE_ONLY.json').read_text());rows=z['rows']
 unique={}
 for q in rows:
  k=(q['episode_seed'],q['mode'],q['resource_index'])
  if k not in unique:unique[k]=episode_oracle(*k,env,safe,models)
 enriched=[]
 for q in rows:
  k=(q['episode_seed'],q['mode'],q['resource_index']);r=dict(q);r.update(unique[k]);r['initial_acquired']=bool(q['trials']>0);enriched.append(r)
 summary={'oracle':{},'arms':{},'by_mode_resource':{}}
 vals=list(unique.values());summary['oracle']={'episodes':len(vals),'initial_beneficial_rate':float(np.mean([x['oracle_initial_beneficial'] for x in vals])),'mean_initial_advantage':float(np.mean([x['initial_option_advantage'] for x in vals])),'first_evaluator_resolved_trial_distribution':{},'first_terminal_controller_correct_trial_distribution':{}}
 for field,key in [('first_evaluator_resolved_trial','first_evaluator_resolved_trial_distribution'),('first_terminal_controller_correct_trial','first_terminal_controller_correct_trial_distribution')]:
  c=defaultdict(int)
  for x in vals:c['none' if x[field] is None else str(x[field])]+=1
  summary['oracle'][key]=dict(c)
 for arm in ['v38','v40']:
  rr=[x for x in enriched if x['arm']==arm and x['reuse']];pos=[x for x in rr if x['oracle_initial_beneficial']];neg=[x for x in rr if not x['oracle_initial_beneficial']];respos=[x for x in pos if x['mode'] in ('stable_weak','unstable_then_stable','replacement','reversal')];nuniq=[x for x in rr if x['mode'] in ('balanced_no_unique','biased_no_unique')]
  summary['arms'][arm]={'n':len(rr),'oracle_positive_n':len(pos),'oracle_positive_acquisition_recall':float(np.mean([x['initial_acquired'] for x in pos])),'oracle_positive_final_success':float(np.mean([x['correct'] for x in pos])),'oracle_positive_success_given_acquired':float(np.mean([x['correct'] for x in pos if x['initial_acquired']])) if any(x['initial_acquired'] for x in pos) else None,'oracle_positive_mean_trials':float(np.mean([x['trials'] for x in pos])),'oracle_nonpositive_false_acquisition':float(np.mean([x['initial_acquired'] for x in neg])),'oracle_nonpositive_final_unknown':float(np.mean([x['unknown'] for x in neg])),'resolvable_oracle_positive_n':len(respos),'resolvable_oracle_positive_acquisition_recall':float(np.mean([x['initial_acquired'] for x in respos])) if respos else None,'resolvable_oracle_positive_final_success':float(np.mean([x['correct'] for x in respos])) if respos else None,'no_unique_false_acquisition':float(np.mean([x['initial_acquired'] for x in nuniq])),'no_unique_final_unknown':float(np.mean([x['unknown'] for x in nuniq]))}
 summary['by_mode_resource']={}
 for mode in live.MODES:
  summary['by_mode_resource'][mode]={}
  for ri,rn in enumerate(live.RESOURCE_REGIMES):
   uu=[x for k,x in unique.items() if k[1]==mode and k[2]==ri];summary['by_mode_resource'][mode][rn]={'n':len(uu),'initial_beneficial_rate':float(np.mean([x['oracle_initial_beneficial'] for x in uu])),'mean_initial_advantage':float(np.mean([x['initial_option_advantage'] for x in uu])),'mean_first_evaluator_resolved_trial':float(np.mean([x['first_evaluator_resolved_trial'] for x in uu if x['first_evaluator_resolved_trial'] is not None])) if any(x['first_evaluator_resolved_trial'] is not None for x in uu) else None,'mean_first_terminal_controller_correct_trial':float(np.mean([x['first_terminal_controller_correct_trial'] for x in uu if x['first_terminal_controller_correct_trial'] is not None])) if any(x['first_terminal_controller_correct_trial'] is not None for x in uu) else None}
 out={'experiment':'R32 V44 evaluator-only audit of fresh V41 initial multi-trial option benefit','summary':summary,'episodes':[{'episode_seed':k[0],'mode':k[1],'resource_index':k[2],**v} for k,v in unique.items()],'arm_rows':enriched,'seconds':time.time()-t0,'boundary':'REFERENCE_ONLY evaluator diagnostic. Delayed consensus, desired answer, resource regime, and exact future option advantage are metrics only and never enter V38/V40 runtime decisions.'}
 (ROOT/'R32_V44_ORACLE_BENEFICIAL_FRESH_STREAM_AUDIT_REFERENCE_ONLY.json').write_text(json.dumps(out,indent=2));cfg={'status':'REFERENCE_ONLY_EVALUATOR_DIAGNOSTIC','fresh_evaluation_seed':live.EVAL_SEED,'native_promotion_allowed':False,'source_sha256':sha(Path(__file__))};(ROOT/'R32_V44_CONFIG.json').write_text(json.dumps(cfg,indent=2));(ROOT/'R32_V44_TRAINING.log').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
