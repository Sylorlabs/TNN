from __future__ import annotations
import os,sys,json,math,hashlib
from pathlib import Path
from collections import defaultdict
import numpy as np
sys.path.insert(0,'/mnt/data/r31_part2');sys.path.insert(0,'/mnt/data/r32_epistemic')
import r32_epistemic_r31_matched_v10_REFERENCE_ONLY as v10
import r31_sequential_evidence_abstention_REFERENCE_ONLY as r31

OUT=Path('/mnt/data/r32_epistemic')
MODES=['balanced_no_unique','biased_no_unique','stable_weak','unstable_then_stable','replacement','reversal','costly_stable']

def prepare_ep(seed,mode,env):
    ep=v10.make_ep(seed,'genuine_ambiguity',env)
    ep.avail[:]=False;ep.avail[0]=True;ep.avail[1]=True;ep.avail[7]=True
    ep.cost[7]=2.40 if mode=='costly_stable' else (.42 if mode in ('balanced_no_unique','biased_no_unique') else .36)
    return ep

def outcome_for(ep,mode,trial):
    r=np.random.default_rng(ep.seed*9176+trial*17011+37)
    if mode=='balanced_no_unique':return ep.target if r.random()<.5 else ep.twin_target
    if mode=='biased_no_unique':return ep.target if r.random()<.70 else ep.twin_target
    if mode in ('stable_weak','costly_stable'):return ep.target
    if mode=='unstable_then_stable':return (ep.target if trial%2==0 else ep.twin_target) if trial<4 else ep.target
    if mode=='replacement':return ep.target if trial<2 else ep.twin_target
    if mode=='reversal':return ep.twin_target if trial<2 else ep.target
    raise ValueError(mode)

def obs7(ep,mode,st,env,used):
    *_,classes,idx,sig,learned=env;trial=int(st.group_n[v10.GROUP[7]])
    outcome=outcome_for(ep,mode,trial);a=r31.select_action(st.score,learned,used);used.append(a)
    rr=np.random.default_rng(ep.seed*2029+trial*12347+a*31+97)
    sigma=1.00 if mode=='stable_weak' else (.78 if mode in ('balanced_no_unique','biased_no_unique','unstable_then_stable') else .68)
    obs=sig[idx[outcome],a]+float(rr.normal(0,sigma))
    v=np.array([-((obs-learned[ci,a])**2)/(2*(.95 if 'no_unique' in mode else .88)**2) for ci in range(len(classes))])
    return v,outcome

def run(ep,mode,env,models,safe,reuse):
    st=v10.initial_state(ep,env,'D');classes=env[5];a_dec=int(classes[int(np.argmax(st.p(True)))]);used=[];outcomes=[]
    for step in range(40):
        cand,qk,qc,qu,_=v10.d_values(st,models,ep,safe,a_dec,env)
        best=('keep',qk); 
        if qc>best[1]:best=('commit',qc)
        if qu>best[1]:best=('unknown',qu)
        can=ep.avail[7] and (reuse or not st.seen[7])
        if can:
            qi=v10.inspect_value(st,models,ep,7,safe,a_dec,env)
            if qi>best[1]:best=('inspect',qi)
        if best[0]=='inspect':
            vv,o=obs7(ep,mode,st,env,used);st.add(7,vv,ep.cost[7]);outcomes.append(o);continue
        if best[0]=='keep':return a_dec,st,outcomes,False
        if best[0]=='commit':return cand,st,outcomes,False
        return -1,st,outcomes,False
    return -999,st,outcomes,True

def desired(ep,mode):
    if mode in ('balanced_no_unique','biased_no_unique','costly_stable'):return -1
    if mode=='replacement':return ep.twin_target
    return ep.target

def eval_mode(seed,mode,env,models,safe,n=120):
    out={}
    for reuse in [False,True]:
        d=defaultdict(float);trials=[];switch_delay=[]
        for j in range(n):
            ep=prepare_ep(seed*100000+MODES.index(mode)*1000+j,mode,env);dec,st,obs,runaway=run(ep,mode,env,models,safe,reuse);want=desired(ep,mode)
            d['success']+=dec==want;d['unknown']+=dec==-1;d['wrong_commit']+=dec not in (-1,want);d['runaway']+=runaway;d['cost']+=st.cost;trials.append(len(obs))
            if mode=='replacement' and obs:
                # first trial index at which accumulated posterior favors replacement target
                preds=[int(env[5][int(np.argmax(p))]) for p in st.post_hist]
                hit=next((i for i,x in enumerate(preds) if x==ep.twin_target),len(preds));switch_delay.append(hit)
        out['reusable' if reuse else 'one_shot']={k:float(v/n) for k,v in d.items()}
        out['reusable' if reuse else 'one_shot']['mean_trials']=float(np.mean(trials));out['reusable' if reuse else 'one_shot']['max_trials']=int(np.max(trials));out['reusable' if reuse else 'one_shot']['switch_delay']=float(np.mean(switch_delay)) if switch_delay else 0.
    return out

def main(seed=9714,n=120):
    env=r31.setup(seed);safe=v10.train_A(seed,env);models=v10.train_D(seed*10+68,env,safe,2200);res={m:eval_mode(seed,m,env,models,safe,n) for m in MODES}
    agg={'seed':seed,'n_per_mode':n,'training':models[4],'modes':res,'summary':{}}
    for arm in ['one_shot','reusable']:
        agg['summary'][arm]={
            'no_unique_unknown':float(np.mean([res[m][arm]['unknown'] for m in ['balanced_no_unique','biased_no_unique']])),
            'resolvable_success':float(np.mean([res[m][arm]['success'] for m in ['stable_weak','unstable_then_stable','replacement','reversal']])),
            'costly_unknown':res['costly_stable'][arm]['unknown'],
            'wrong_commit':float(np.mean([res[m][arm]['wrong_commit'] for m in MODES])),
            'mean_trials':float(np.mean([res[m][arm]['mean_trials'] for m in MODES])),
            'runaway':float(np.mean([res[m][arm]['runaway'] for m in MODES])),
        }
    agg['boundary']='REFERENCE_ONLY post-challenge. The learner sees only ambiguous passive evidence, a reusable grounded consequence apparatus with explicit same-lineage provenance and cost, and its learned V10 residual action values. Mode names/state schedules are evaluator-only. No ambiguity label, fixed runtime probe count, transformer/tokenizer/VAD, or graph cognition.'
    p=OUT/f'R32_V10_REUSABLE_PROBE_HARDENING_SEED_{seed}.json';p.write_text(json.dumps(agg,indent=2));print(json.dumps(agg['summary'],indent=2));print('SHA',hashlib.sha256(p.read_bytes()).hexdigest())
if __name__=='__main__':main(int(sys.argv[1]) if len(sys.argv)>1 else 9714,int(sys.argv[2]) if len(sys.argv)>2 else 120)
