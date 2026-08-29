import numpy as np,json
from sklearn.linear_model import LogisticRegression
from pathlib import Path
OUT=Path('/mnt/data/r32_epistemic')

def gen(rng,n):
 X=rng.uniform(0,1,(n,7)) # novelty,recon_err,route_disagree,uncert,reuse,causal,source_conflict
 logit=-2.2+2.8*X[:,1]+2.4*X[:,2]+1.5*X[:,3]-1.2*X[:,4]+1.6*X[:,5]+1.8*X[:,6]
 p=1/(1+np.exp(-logit)); need=rng.random(n)<p
 # future value and access frequency
 value=.5+1.5*X[:,5]+1.1*X[:,0]+.8*X[:,6]+rng.uniform(0,.5,n)
 freq=1+rng.poisson(2+3*X[:,4],n)
 return X,need,value,freq

def heuristic(X):return (2.2*X[:,1]+1.8*X[:,2]+1.0*X[:,3]+1.4*X[:,5]+1.5*X[:,6]-.8*X[:,4])>2.15

def alloc(scores,budget_raw):
 k=int(round(budget_raw*len(scores)));sel=np.zeros(len(scores),bool)
 if k>0:sel[np.argsort(scores)[-k:]]=1
 return sel

def evaluate(X,need,value,freq,keep):
 # chunk always retains semantic gist; raw necessary for exact/near-twin future query
 exact=np.where(need,keep,1.0); semantic=np.ones(len(X))*0.985
 # failure on needed raw has high delayed regret; raw storage cost
 success=np.where(need,keep.astype(float),semantic)
 util=(success*value*freq).sum()/(value*freq).sum()-0.08*keep.mean()
 return {'utility':float(util),'exact_need_recall':float(exact[need].mean()) if need.any() else 1.,'semantic':float(semantic.mean()),'raw_fraction':float(keep.mean()),'delayed_regret':float(((need & ~keep)*value*freq).sum()/(value*freq).sum())}

def run(seed,budget):
 rng=np.random.default_rng(seed);Xd,nd,vd,fd=gen(rng,7000);Xt,nt,vt,ft=gen(rng,5000)
 clf=LogisticRegression(max_iter=500).fit(Xd,nd)
 learned=clf.predict_proba(Xt)[:,1]*(.7+vt)*(.6+np.sqrt(ft))
 hs=(2.2*Xt[:,1]+1.8*Xt[:,2]+Xt[:,3]+1.4*Xt[:,5]+1.5*Xt[:,6]-.8*Xt[:,4])*(.7+vt)
 out={}
 out['raw_all']=evaluate(Xt,nt,vt,ft,np.ones(len(Xt),bool))
 out['chunk_only']=evaluate(Xt,nt,vt,ft,np.zeros(len(Xt),bool))
 out['heuristic_default']=evaluate(Xt,nt,vt,ft,alloc(hs,budget))
 out['learned_regret_override']=evaluate(Xt,nt,vt,ft,alloc(learned,budget))
 # LRU-like raw keeping uses only reuse/frequency proxy, not semantic need
 out['lru_representation']=evaluate(Xt,nt,vt,ft,alloc(Xt[:,4],budget))
 return out

def main():
 rows=[]
 for b in [.2,.4,.6,.8]:
  for s in range(10):rows.append({'budget':b,'seed':81000+s,'result':run(81000+s,b)})
 agg={}
 for b in [.2,.4,.6,.8]:
  rr=[r for r in rows if r['budget']==b];agg[str(b)]={}
  for p in rr[0]['result']:
   agg[str(b)][p]={m:float(np.mean([r['result'][p][m] for r in rr])) for m in rr[0]['result'][p]}
 out={'aggregate':agg,'rows':rows,'boundary':'REFERENCE_ONLY chunk resource policy. Learned override is trained only from delayed exact-need outcomes; chunk/raw representation capabilities are generic. LRU representation is a control.'}
 (OUT/'R32_CHUNK_RESOURCE_REFERENCE_ONLY.json').write_text(json.dumps(out,indent=2));print(json.dumps(agg,indent=2))
if __name__=='__main__':main()
