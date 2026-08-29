from __future__ import annotations
import os,sys,json,math,random
os.environ['OMP_NUM_THREADS']='1';os.environ['MKL_NUM_THREADS']='1';os.environ['OPENBLAS_NUM_THREADS']='1'
sys.path.insert(0,'/mnt/data/r31_part2')
import r31_postrepair_part2 as base
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.mixture import GaussianMixture
from collections import deque,Counter
from pathlib import Path
OUT=Path('/mnt/data/r31_part2')

class StableBank:
    def __init__(self,E=8,A=4,maxm=5):
        self.models=[base.RegimeModel(E,A)];self.active=0;self.maxm=maxm;self.hist=deque(maxlen=60);self.cool=0;self.spawns=0;self.switches=0
    def choose(self,e):return self.models[self.active].choose(e)
    def observe(self,e,a,r):
        errs=[m.error(e,a,r) for m in self.models]
        self.hist.append((e,a,r,errs)); self.cool=max(0,self.cool-1)
        if len(self.hist)>=40 and self.cool==0:
            means=[]
            for j in range(len(self.models)):
                means.append(float(np.mean([z[3][j] for z in self.hist])))
            best=int(np.argmin(means));cur=means[self.active]
            if best!=self.active and means[best]+.16<cur:
                self.active=best;self.switches+=1;self.cool=80;self.hist.clear()
            elif cur>.55 and min(means)>.42 and len(self.models)<self.maxm:
                self.models.append(base.RegimeModel(self.models[0].E,self.models[0].A));self.active=len(self.models)-1;self.spawns+=1;self.cool=120;self.hist.clear()
        self.models[self.active].observe(e,a,r)

def run_regime_stable(seed):
    rng=random.Random(seed); o=StableBank();seq=[0,1,0,2,1,0];phase=[]
    for reg in seq:
        ok=first=0
        for i in range(3000):
            e=rng.randrange(8);a=o.choose(e);r=base.physics(reg,e,a);ok+=r>0;first+=(r>0 and i<200);o.observe(e,a,r)
            if rng.random()<.18:
                aa=rng.randrange(4);rr=base.physics(reg,e,aa);o.observe(e,aa,rr)
        phase.append({'regime':reg,'online':ok/3000,'first200':first/200,'active':o.active,'models':len(o.models)})
    # Read-only retention: choose best stored model per regime by short internally-observed probe history, then score.
    retention=[]
    for reg in [0,1,2]:
        # probe 80 random action outcomes (environment feedback, no regime label) solely to select an existing model
        scores=np.zeros(len(o.models));counts=np.zeros(len(o.models));
        for _ in range(80):
            e=rng.randrange(8);a=rng.randrange(4);r=base.physics(reg,e,a)
            for j,m in enumerate(o.models):scores[j]+=m.error(e,a,r);counts[j]+=1
        m=o.models[int(np.argmin(scores/np.maximum(1,counts)))]
        ok=0
        for _ in range(1000):
            e=rng.randrange(8);ok+=base.physics(reg,e,m.choose(e))>0
        retention.append(ok/1000)
    return {'phase':phase,'retention':retention,'models':len(o.models),'spawns':o.spawns,'switches':o.switches}

def train_context(seed,w,train):
    rng=np.random.default_rng(seed+222)
    # context is independent grounded sensory state, noisy and not a label; each entity has a latent context prototype.
    prot=rng.normal(0,1,(w.entities,5)); X=[];y=[]
    for s,effect in train:
        # derive approximate entity candidates consistent with effect; choose one occurrence from world
        candidates=np.where(w.effect==effect)[0];e=int(rng.choice(candidates));X.append(prot[e]+rng.normal(0,.85,5));y.append(effect)
    clf=LogisticRegression(max_iter=400,C=.7).fit(np.asarray(X),np.asarray(y));return prot,clf

def context_vec(prot,e,rng,amb=False):
    if amb:
        return (prot[e]+prot[e^1])/2+rng.normal(0,1.05,prot.shape[1])
    return prot[e]+rng.normal(0,.85,prot.shape[1])

def run_acoustic_context(seed):
    w=base.AcousticWorld(seed);rng=np.random.default_rng(seed+99)
    train=[]
    for _ in range(10000):
        e=int(rng.integers(0,w.entities));train.append(w.episode(e,rng,'matched'))
    bank=base.ChunkBank();L=base.GroundLearner(bank,'dual');L.fit(train)
    # context learner is grounded by ordinary consequence history, not evaluator acoustic units.
    prot,ctxclf=train_context(seed,w,train)
    # reliability learner adds acoustic/context disagreement and uncertainty, trained on later correctness only.
    rr=[]
    for _ in range(7000):
        e=int(rng.integers(0,w.entities));cond=rng.choice(['matched','hard_noise','near_twin','confwrong','speaker_shift'])
        s,y=w.episode(e,rng,cond);pa,ca,ma=L.pred(s);cv=context_vec(prot,e,rng);cp=ctxclf.predict_proba(cv.reshape(1,-1))[0];cc=int(ctxclf.classes_[int(np.argmax(cp))]);cm=float(np.partition(cp,-1)[-1]-np.partition(cp,-2)[-2]);
        rr.append([ma,ca,float(pa!=cc),cm,len(s)/40,int(pa==y)])
    rel=LogisticRegression(max_iter=400,class_weight='balanced').fit(np.asarray([x[:-1] for x in rr]),np.asarray([x[-1] for x in rr]))
    conds=['matched','speaker_shift','no_gap','silence_shift','hard_noise','onset_damage','near_twin','confwrong','novel']
    modes={k:{} for k in ['acoustic_active','context_active','always_reinspect']}
    for mode in modes:
        for cond in conds:
            ok=0;requests=0;N=1400
            for _ in range(N):
                e=int(rng.integers(0,w.entities));s,y=w.episode(e,rng,cond);p,cf,mg=L.pred(s);q1=L.probs(s)
                cv=context_vec(prot,e,rng);cp=ctxclf.predict_proba(cv.reshape(1,-1))[0];cc=int(ctxclf.classes_[int(np.argmax(cp))]);cm=float(np.partition(cp,-1)[-1]-np.partition(cp,-2)[-2])
                if mode=='acoustic_active':
                    rv=float(rel.predict_proba([[mg,cf,0.0,0.0,len(s)/40]])[0,1]); ask=rv<.64
                elif mode=='context_active':
                    rv=float(rel.predict_proba([[mg,cf,float(p!=cc),cm,len(s)/40]])[0,1]); ask=(rv<.68 or (p!=cc and cm>.12))
                else: ask=True
                if ask:
                    requests+=1;s2,_=w.episode(e,rng,'hard_noise' if cond!='matched' else 'matched');q2=L.probs(s2)
                    # context evidence remains independent and softly weighted rather than overriding acoustics.
                    amap={c:i for i,c in enumerate(L.clf.classes_)}; cvec=np.zeros_like(q1)
                    for i,c in enumerate(ctxclf.classes_):
                        if c in amap:cvec[amap[c]]=cp[i]
                    score=q1+q2+(0.7*cvec if mode=='context_active' else 0);p=int(L.clf.classes_[int(np.argmax(score))])
                ok+=p==y
            modes[mode][cond]=ok/N;modes[mode][cond+'_request']=requests/N
        # ambiguous context midpoint + mixed acoustic; abstain using learned reliability/conflict
        ab=0;N=1400
        for _ in range(N):
            e=int(rng.integers(0,w.entities));s,_=w.ambiguous(e,rng);p,cf,mg=L.pred(s);cv=context_vec(prot,e,rng,amb=True);cp=ctxclf.predict_proba(cv.reshape(1,-1))[0];cc=int(ctxclf.classes_[int(np.argmax(cp))]);cm=float(np.partition(cp,-1)[-1]-np.partition(cp,-2)[-2]);rv=float(rel.predict_proba([[mg,cf,float(p!=cc),cm,len(s)/40]])[0,1]);decision=-1 if rv<.58 or cf<.56 or cm<.08 else p;ab+=decision==-1
        modes[mode]['ambiguous_abstain']=ab/N
        modes[mode]['hard_mean']=float(np.mean([modes[mode][x] for x in ['speaker_shift','no_gap','hard_noise','onset_damage','near_twin','confwrong','novel']]))
    # correlated wrong two-view: two independently noisy observations both generated from twin; desired behavior is abstain under unresolved context conflict.
    for mode in modes:
        safe=0;N=1400
        for _ in range(N):
            e=int(rng.integers(0,w.entities));s,y=w.episode(e,rng,'confwrong');s2,_=w.episode(e,rng,'confwrong');q=L.probs(s)+L.probs(s2);p=int(L.clf.classes_[int(np.argmax(q))]);cf=float(np.max(q/2));cv=context_vec(prot,e,rng);cp=ctxclf.predict_proba(cv.reshape(1,-1))[0];cc=int(ctxclf.classes_[int(np.argmax(cp))]); conflict=p!=cc
            # safe means correct or abstain; never reward blind context override.
            if mode=='context_active' and conflict and cf>.7: decision=-1
            else: decision=p
            safe+= (decision==y or decision==-1)
        modes[mode]['correlated_wrong_safe']=safe/N
    return modes

def run_poly_harder(seed):
    rng=np.random.default_rng(seed);basechunk=np.array([4,7,4,9,6,5]);mu=[np.array([-1.,-.6]),np.array([1.,.6])]
    C=[];Y=[]
    for i in range(9000):
        c=int(rng.integers(0,2));C.append(mu[c]+rng.normal(0,.75,2));Y.append(c)
    C=np.asarray(C);Y=np.asarray(Y)
    # Choose splits by unsupervised Gaussian-mixture BIC, no hidden context IDs.
    models=[]
    for k in range(1,6):
        g=GaussianMixture(k,covariance_type='full',random_state=seed,n_init=3).fit(C[:6500]);models.append((g.bic(C[:6500]),g))
    _,g=min(models,key=lambda x:x[0]); tr=g.predict(C[:6500]);te=g.predict(C[6500:]);maps={}
    for k in range(g.n_components):
        yy=Y[:6500][tr==k];maps[k]=Counter(yy).most_common(1)[0][0] if len(yy) else 0
    pred=np.array([maps[int(k)] for k in te]);acc=float((pred==Y[6500:]).mean());
    blind=max(np.mean(Y[6500:]==0),np.mean(Y[6500:]==1));pur=float(np.mean([max(Counter(Y[:6500][tr==k]).values())/max(1,(tr==k).sum()) for k in range(g.n_components)]))
    return {'blind':float(blind),'context_specialized':acc,'chosen_splits':g.n_components,'specialization_purity':pur}

def work(seed):return {'seed':seed,'acoustic':run_acoustic_context(seed),'regime':run_regime_stable(seed),'poly':run_poly_harder(seed)}
def main():
    from concurrent.futures import ProcessPoolExecutor,as_completed
    rows=[]
    with ProcessPoolExecutor(max_workers=4) as ex:
        fs={ex.submit(work,9300+i):9300+i for i in range(8)}
        for f in as_completed(fs):r=f.result();rows.append(r);print('DONE',r['seed'],flush=True)
    rows.sort(key=lambda x:x['seed'])
    modes=['acoustic_active','context_active','always_reinspect'];conds=['matched','speaker_shift','no_gap','silence_shift','hard_noise','onset_damage','near_twin','confwrong','novel','ambiguous_abstain','correlated_wrong_safe','hard_mean']
    ac={m:{c:float(np.mean([r['acoustic'][m][c] for r in rows])) for c in conds} for m in modes}
    rg={'mean_online':float(np.mean([np.mean([p['online'] for p in r['regime']['phase']]) for r in rows])),'return_first200':float(np.mean([np.mean([r['regime']['phase'][j]['first200'] for j in [2,4,5]]) for r in rows])),'retention':[float(np.mean([r['regime']['retention'][j] for r in rows])) for j in range(3)],'models':float(np.mean([r['regime']['models'] for r in rows])),'spawns':float(np.mean([r['regime']['spawns'] for r in rows])),'switches':float(np.mean([r['regime']['switches'] for r in rows]))}
    po={k:float(np.mean([r['poly'][k] for r in rows])) for k in ['blind','context_specialized','chosen_splits','specialization_purity']}
    out={'acoustic':ac,'stable_regime':rg,'polysemy_harder':po,'rows':rows,'boundary':'REFERENCE_ONLY R31 Part2b. Cross-modal context is an independently noisy learned state grounded through ordinary consequences; no evaluator identity/corruption/token/chunk/regime labels. Correlated wrong rewards correct-or-abstain, never context override.'}
    (OUT/'R31_INTEGRATED_V2_PART2B_REFERENCE_ONLY.json').write_text(json.dumps(out,indent=2));print(json.dumps({'acoustic':ac,'stable_regime':rg,'polysemy':po},indent=2))
if __name__=='__main__':main()
