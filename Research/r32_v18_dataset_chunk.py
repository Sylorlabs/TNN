from __future__ import annotations
import argparse, json, math, sys, hashlib
from pathlib import Path
import numpy as np
sys.path.insert(0,'/mnt/data/r31_part2');sys.path.insert(0,'/mnt/data/r32_epistemic')
import r31_sequential_evidence_abstention_REFERENCE_ONLY as r31
import r32_epistemic_r31_matched_v17_cached_REFERENCE_ONLY as v

COUNTERS=['normal_starts','resource_starts','source7_only','uncertain_unique','uncertain_nonconv','uncertain_unique_source7_only','regret_replay']

def generate(base_seed:int, train_seed:int, start:int, end:int, state_in:str|None, out_npz:str, state_out:str):
    env=r31.setup(base_seed);safe=v.train_A(base_seed,env)
    rng=np.random.default_rng(train_seed)
    ctr={k:0 for k in COUNTERS}
    if state_in:
        st=json.loads(Path(state_in).read_text()); assert st['next_j']==start; rng.bit_generator.state=st['rng_state'];ctr.update(st['counters'])
    X=[];yk=[];yc=[];ye=[];yu=[];yn=[];Xi=[];Yi=[]
    choices=v.KINDS+['genuine_ambiguity']*5+['delayed_distinguishing']*2+['entity_replacement']*2+['apparent_replacement_reverses']*2
    def action_feature(st,ep,s,cost,a0,f=None):
        if f is None:f=v.q_feat(st,ep,safe,a0,env)
        return np.r_[f,np.eye(v.S)[s],cost,st.group_n[v.GROUP[s]]/3]
    def candidates(st):
        full=int(env[5][int(np.argmax(st.p(True)))]);epoch=int(env[5][int(np.argmax(st.epoch_p()))]);return full,epoch
    def resource_start(ep,cons,base_state,a0,force7=False):
        rs=base_state.clone();mask=ep.avail.copy();keep_prob=float(rng.beta(1.25,2.0))
        for q in range(2,7):mask[q]=bool(mask[q] and rng.random()<keep_prob)
        mask[7]=bool(ep.avail[7])
        if force7:
            for q in range(2,7):mask[q]=False
        costs=ep.cost.copy()
        for q in range(2,v.S):costs[q]=float(costs[q]*np.exp(rng.uniform(math.log(.60),math.log(2.40))))
        ctr['resource_starts']+=1;only7=bool(mask[7] and not np.any(mask[2:7]));ctr['source7_only']+=int(only7);ent=v.entropy(rs.p(True))
        if ent>=.55:
            if cons is None:ctr['uncertain_nonconv']+=1
            else:ctr['uncertain_unique']+=1;ctr['uncertain_unique_source7_only']+=int(only7)
        return rs,a0,mask,costs,12
    def terminal_values(st,a0,cons):
        full,epoch=candidates(st);return (v.delayed_action_utility(a0,cons),v.delayed_action_utility(full,cons),v.delayed_action_utility(epoch,cons),0.0)
    for j in range(start,end):
        kind=str(rng.choice(choices));ep=v.make_ep(train_seed*100000+j*19+7,kind,env)
        if rng.random()<.68:ep.dev_dynamic_mode=int(rng.integers(0,6))
        adec,_,ap=v.run_A(ep,env,safe);cons=v.delayed_consensus(ep);starts=[]
        st=v.initial_state(ep,env,'D')
        for q,val in ap:st.add(q,val,ep.cost[q])
        starts.append((st,adec,ep.avail.copy(),ep.cost.copy(),10));ctr['normal_starts']+=1
        rs0=v.initial_state(ep,env,'D');radec=int(env[5][int(np.argmax(rs0.p(True)))])
        if rng.random()<.45:starts.append(resource_start(ep,cons,rs0,radec,False))
        u=v.entropy(rs0.p(True))
        if rng.random()<u:
            starts.append(resource_start(ep,cons,rs0,radec,bool(rng.random()<.5)));ctr['regret_replay']+=1
        for st,a0,mask,costs,stages in starts:
            used=[];path=[]
            for stage in range(stages):
                f=v.q_feat(st,ep,safe,a0,env);full,epoch=candidates(st)
                X.append(f);yk.append(v.delayed_action_utility(a0,cons));yc.append(v.delayed_action_utility(full,cons));ye.append(v.delayed_action_utility(epoch,cons));yu.append(0.0);yn.append(float(cons is None))
                available=[q for q in range(2,v.S) if mask[q] and (not st.seen[q] or q==7)]
                if not available:break
                if 7 in available and rng.random()<.62:q=7
                else:q=int(rng.choice(available))
                af=action_feature(st,ep,q,costs[q],a0,f);vv=v.obs_for_source(ep,q,st,env,used);z=st.clone();z.add(q,vv,costs[q]);term=max(terminal_values(z,a0,cons));path.append((af,float(costs[q]),term));st=z
            continuation=-1e9
            for af,cost,term in reversed(path):
                val=max(term,continuation)-cost;Xi.append(af);Yi.append(val);continuation=val
    arrs={k:np.asarray(val) for k,val in [('X',X),('yk',yk),('yc',yc),('ye',ye),('yu',yu),('yn',yn),('Xi',Xi),('Yi',Yi)]}
    np.savez_compressed(out_npz,**arrs)
    state={'base_seed':base_seed,'train_seed':train_seed,'next_j':end,'rng_state':rng.bit_generator.state,'counters':ctr,'rows':len(X),'inspect_rows':len(Xi),'chunk_sha256':hashlib.sha256(Path(out_npz).read_bytes()).hexdigest()}
    Path(state_out).write_text(json.dumps(state,indent=2));print(json.dumps(state,indent=2),flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--base-seed',type=int,default=9714);ap.add_argument('--train-seed',type=int,default=97208);ap.add_argument('--start',type=int,required=True);ap.add_argument('--end',type=int,required=True);ap.add_argument('--state-in');ap.add_argument('--out',required=True);ap.add_argument('--state-out',required=True);a=ap.parse_args();generate(a.base_seed,a.train_seed,a.start,a.end,a.state_in,a.out,a.state_out)
