from __future__ import annotations
import sys,json,hashlib,math,time
from pathlib import Path
import numpy as np
sys.path.insert(0,'/mnt/data/r31_part2');sys.path.insert(0,'/mnt/data/r32_epistemic')
import r31_sequential_evidence_abstention_REFERENCE_ONLY as r31
import r32_epistemic_r31_matched_v17_cached_REFERENCE_ONLY as v
R=Path('/mnt/data/r32_epistemic');H=[1,2,4,8];BASE_T=[0,2,4,6]

def main(seed=9714,n_ep=450):
 t0=time.time();env=r31.setup(seed);safe=v.train_A(seed,env);rng=np.random.default_rng(24024);F=[];Y=[];E=[];C=[];NC=[]
 kinds=['clean_stable','speaker_shift','hard_noise','near_twin','confident_wrong_first','genuine_ambiguity','delayed_distinguishing','entity_replacement','apparent_replacement_reverses']
 for j in range(n_ep):
  ep=v.make_ep(seed*100000+2400000+j*37,str(rng.choice(kinds)),env);ep.dev_dynamic_mode=int(rng.integers(0,6));ep.avail[7]=True;ep.cost[7]=float(.22*np.exp(rng.uniform(math.log(.55),math.log(4.0))))
  cons=v.delayed_consensus(ep);st=v.initial_state(ep,env,'D');a_dec=int(env[5][int(np.argmax(st.p(True)))]);used=[];states=[];cands=[]
  for t in range(max(BASE_T)+max(H)+1):
   states.append(v.q_feat(st,ep,safe,a_dec,env));cands.append(int(env[5][int(np.argmax(st.p(True))) ]))
   vv=v.obs_for_source(ep,7,st,env,used);st.add(7,vv,ep.cost[7])
  for bt in BASE_T:
   f=np.r_[states[bt],ep.cost[7]];yy=[]
   for h in H:
    cand=cands[bt+h];term=max(v.delayed_action_utility(cand,cons),v.delayed_action_utility(-1,cons));yy.append(term-h*ep.cost[7])
   F.append(f);Y.append(yy);E.append(j);C.append(-1 if cons is None else int(cons));NC.append(int(cons is None))
  if (j+1)%100==0:print('EP',j+1,flush=True)
 F=np.asarray(F);Y=np.asarray(Y);E=np.asarray(E);C=np.asarray(C);NC=np.asarray(NC);p=R/'R32_V24_HORIZON_DATA_SEED_9714.npz';np.savez_compressed(p,X=F,Y=Y,episode=E,consensus=C,nonconvergent=NC,horizons=np.asarray(H));meta={'seed':seed,'episodes':n_ep,'rows':len(F),'feature_dim':F.shape[1],'horizons':H,'base_trial_offsets':BASE_T,'nonconvergent_rate':float(NC.mean()),'cost_mean':float(F[:,-1].mean()),'cost_min':float(F[:,-1].min()),'cost_max':float(F[:,-1].max()),'seconds':time.time()-t0,'target':'best delayed grounded terminal action utility after h additional same-lineage consequence trials minus exact h*trial_cost; UNKNOWN utility 0; no generator mode/ambiguity label enters features','source7_dynamic_modes':'generator-only stationary, balanced stochastic, biased stochastic, step change, reversal, unstable-then-stable'};meta['sha256']=hashlib.sha256(p.read_bytes()).hexdigest();(R/'R32_V24_HORIZON_DATA_META.json').write_text(json.dumps(meta,indent=2));print(json.dumps(meta,indent=2))
if __name__=='__main__':main()
