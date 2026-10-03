import importlib.util,sys,time,json,numpy as np
p='/mnt/data/r32_exec/r32_epistemic_r31_matched_v5.py'
spec=importlib.util.spec_from_file_location('v5',p);v=importlib.util.module_from_spec(spec);sys.modules['v5']=v;spec.loader.exec_module(v)
SEED=9710; N=36
# Regret tuples: (wrong_commit_reward, unnecessary_unknown_reward)
# Correct commit and correct UNKNOWN are +1. Values are developmental regret semantics, not confidence thresholds.
REGRETS={'current':(-3.0,-0.25),'wrong2_unknown1':(-2.0,-1.0),'symmetric':(-1.0,-1.0),'wrong2_unknown1p5':(-2.0,-1.5)}

def ddec(st,models,ep,safe,env,wr,ur):
 sm,rm,gm,_=models;f=v.meta_feat(st,ep,safe,True);ps=float(sm.predict_proba(f.reshape(1,-1))[0,1]);pr=float(rm.predict_proba(f.reshape(1,-1))[0,1]);cand=int(np.argmax(st.p(True)))
 uc=ps*1+(1-ps)*wr; uu=(1-pr)*1+pr*ur
 return cand,uc,uu,ps,pr,f

def runD(ep,env,models,safe,a_probes,wr,ur):
 st=v.initial_state(ep,env,'D');used=[]
 for s,x in a_probes:st.add(s,x,ep.cost[s])
 while True:
  c,uc,uu,ps,pr,f=ddec(st,models,ep,safe,env,wr,ur);best=(-1,-1e9,0.)
  for s in range(2,v.S):
   if not ep.avail[s] or st.seen[s]:continue
   gp=v.gain_pred(st,models,ep,s,True,safe);dep=1/(1+.9*st.group_n[v.GROUP[s]]);modal=1.12 if not any(v.MOD[q]==v.MOD[s] for q,_ in st.hist) else .82
   net=3.8*max(0.,gp)*dep*modal-ep.cost[s]
   if net>best[1]:best=(s,net,gp)
  if best[0]>=0 and best[1]>0:
   s=best[0];before=v.margin(st.p(True));x=v.obs_for_source(ep,s,st,env,used);st.add(s,x,ep.cost[s]);after=v.margin(st.p(True))
   if best[2]>.04 and after-before<.01:st.failed_gain+=1
   elif after-before>.12 and st.failed_gain:st.failed_gain-=1
   continue
  return (int(env[5][c]) if uc>=uu else -1),st

t0=time.time();env=v.r31.setup(SEED);safe=v.train_A(SEED,env);models=v.train_D(SEED*10+68,env,safe,1200)
# freeze matched episode panel and A acquisitions
panel=[]
for ki,k in enumerate(v.KINDS):
 for j in range(N):
  ep=v.make_ep(SEED*10000000+ki*100000+j,k,env); a,ast,ap=v.run_A(ep,env,safe);panel.append((ep,a,ast,ap))
out={'seed':SEED,'n_per_condition':N,'training':models[3],'regrets':{},'elapsed_train_panel':time.time()-t0}
core={'speaker_shift','hard_noise','onset_damage','near_twin','confident_wrong_first','novel'}
res=set(v.KINDS)-{'genuine_ambiguity'}
for name,(wr,ur) in REGRETS.items():
 vals={}
 by={k:[] for k in v.KINDS}
 for ep,a,ast,ap in panel:
  d,st=runD(ep,env,models,safe,ap,wr,ur);by[ep.kind].append((ep,d,st))
 for k,sub in by.items():
  if k=='genuine_ambiguity': vals[k]={'abstain':float(np.mean([d==-1 for ep,d,st in sub])),'wrong':float(np.mean([d!=-1 for ep,d,st in sub]))}
  else: vals[k]={'correct':float(np.mean([d==ep.target for ep,d,st in sub])),'abstain':float(np.mean([d==-1 for ep,d,st in sub])),'wrong':float(np.mean([d not in(-1,ep.target) for ep,d,st in sub]))}
 out['regrets'][name]={
  'wrong_reward':wr,'unnecessary_unknown_reward':ur,
  'core_hard':float(np.mean([vals[k]['correct'] for k in core])),
  'expanded_resolvable':float(np.mean([vals[k]['correct'] for k in res])),
  'ambiguity':float(vals['genuine_ambiguity']['abstain']),
  'unnecessary_abstain':float(np.mean([vals[k]['abstain'] for k in res])),
  'mean_wrong':float(np.mean([vals[k]['wrong'] for k in vals]))}
out['elapsed']=time.time()-t0
open('/mnt/data/r32_epistemic/R32_EPISTEMIC_REGRET_SWEEP_SEED_9710.json','w').write(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
