import os,sys,json,numpy as np
os.environ['OMP_NUM_THREADS']='1';os.environ['MKL_NUM_THREADS']='1';os.environ['OPENBLAS_NUM_THREADS']='1'
sys.path.insert(0,'/mnt/data/r31_part2')
import r31_postrepair_part2 as m
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
OUT=Path('/mnt/data/r31_part2')
def work(s):
    a={'seed':s,'routes':m.run_acoustic(s)}; p={'seed':s,**m.run_polysemy(s)}
    r=[{'seed':s,'kind':k,**m.run_regime(s,k)} for k in ['overwrite','bank']]
    return a,p,r
def main():
    acoust=[];polys=[];regimes=[]
    with ProcessPoolExecutor(max_workers=4) as ex:
        futs={ex.submit(work,9100+i):9100+i for i in range(8)}
        for f in as_completed(futs):
            a,p,r=f.result();acoust.append(a);polys.append(p);regimes.extend(r);print('DONE',a['seed'],flush=True)
    acoust.sort(key=lambda x:x['seed']);polys.sort(key=lambda x:x['seed']);regimes.sort(key=lambda x:(x['seed'],x['kind']))
    agg={}
    for route in ['opaque','rich','dual','active']:
        keys=['matched','speaker_shift','no_gap','silence_shift','hard_noise','onset_damage','near_twin','confwrong','novel','ambiguous_abstain','hard_mean']
        agg[route]={k:float(np.mean([r['routes'][route][k] for r in acoust])) for k in keys};agg[route]['chunks']=float(np.mean([r['routes'][route]['chunks'] for r in acoust]))
    regagg={}
    for kind in ['overwrite','bank']:
        rr=[x for x in regimes if x['kind']==kind]
        regagg[kind]={'mean_online':float(np.mean([np.mean([p['online'] for p in x['phase']]) for x in rr])),'return_first200':float(np.mean([np.mean([x['phase'][j]['first200'] for j in [2,4,5]]) for x in rr])),'retention':[float(np.mean([x['retention'][j] for x in rr])) for j in range(3)],'models':float(np.mean([x['models'] for x in rr])),'spawns':float(np.mean([x['spawns'] for x in rr])),'switches':float(np.mean([x['switches'] for x in rr]))}
    polyagg={k:float(np.mean([x[k] for x in polys])) for k in ['blind','context_specialized','chosen_splits','specialization_purity']}
    out={'acoustic_routes':agg,'acoustic_seeds':acoust,'regime':regagg,'regime_rows':regimes,'polysemy':polyagg,'polysemy_rows':polys,'boundary':'REFERENCE_ONLY post-repair R31. Raw/self-chunk evidence + grounded consequences only; no phoneme/word/token/VAD/chunk boundary or regime IDs.'}
    (OUT/'R31_INTEGRATED_V2_PART2_REFERENCE_ONLY.json').write_text(json.dumps(out,indent=2));print(json.dumps({'acoustic':agg,'regime':regagg,'polysemy':polyagg},indent=2))
if __name__=='__main__':main()
