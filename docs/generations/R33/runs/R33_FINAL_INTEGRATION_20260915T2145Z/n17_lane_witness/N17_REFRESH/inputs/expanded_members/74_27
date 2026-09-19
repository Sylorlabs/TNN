from __future__ import annotations
import os,sys,json,math
os.environ['OMP_NUM_THREADS']='1';os.environ['MKL_NUM_THREADS']='1';os.environ['OPENBLAS_NUM_THREADS']='1'
sys.path.insert(0,'/mnt/data/r31_part2')
import r31_postrepair_part2 as base
import r31_postrepair_part2b as b
import numpy as np
from sklearn.linear_model import LogisticRegression
from pathlib import Path
OUT=Path('/mnt/data/r31_part2')

def build_action_world(seed,classes):
    rng=np.random.default_rng(seed+700)
    # numeric physical consequences; signatures are deliberately nontrivial but separated.
    sig=rng.normal(0,1,(len(classes),5))*2
    # ensure every class pair has at least one clearly discriminating action
    for i in range(len(classes)):sig[i,(i*2)%5]+=3.5
    return sig

def train_action_model(seed,classes,sig):
    rng=np.random.default_rng(seed+701); sums=np.zeros_like(sig);n=np.zeros_like(sig)
    # ordinary exploratory interactions, no test-time class label supplied.
    for _ in range(12000):
        ci=int(rng.integers(0,len(classes)));a=int(rng.integers(0,5));obs=sig[ci,a]+rng.normal(0,.55);sums[ci,a]+=obs;n[ci,a]+=1
    return sums/np.maximum(1,n)

def run(seed):
    w=base.AcousticWorld(seed);rng=np.random.default_rng(seed+99)
    train=[]
    for _ in range(9000):
        e=int(rng.integers(0,w.entities));train.append(w.episode(e,rng,'matched'))
    L=base.GroundLearner(base.ChunkBank(),'dual');L.fit(train)
    prot,ctxclf=b.train_context(seed,w,train)
    classes=list(L.clf.classes_);cidx={int(c):i for i,c in enumerate(classes)}
    sig=build_action_world(seed,classes); learned=train_action_model(seed,classes,sig)
    # reliability from later independent correctness plus cross-modal disagreement.
    X=[];Y=[]
    for _ in range(6500):
        e=int(rng.integers(0,w.entities));cond=rng.choice(['matched','hard_noise','near_twin','confwrong','speaker_shift']);s,y=w.episode(e,rng,cond);p,cf,mg=L.pred(s);cv=b.context_vec(prot,e,rng);cp=ctxclf.predict_proba(cv.reshape(1,-1))[0];cc=int(ctxclf.classes_[int(np.argmax(cp))]);cm=float(np.partition(cp,-1)[-1]-np.partition(cp,-2)[-2]);X.append([mg,cf,float(p!=cc),cm,len(s)/40]);Y.append(int(p==y))
    rel=LogisticRegression(max_iter=400,class_weight='balanced').fit(X,Y)
    conditions=['matched','hard_noise','onset_damage','near_twin','confwrong','speaker_shift','novel']
    modes={m:{} for m in ['context_reinspect','consequence_probe']}
    for mode in modes:
        for cond in conditions:
            ok=0;req=0;N=1600
            for _ in range(N):
                e=int(rng.integers(0,w.entities));s,y=w.episode(e,rng,cond);q=L.probs(s);p=int(classes[int(np.argmax(q))]);cf=float(np.max(q));qs=np.sort(q);mg=float(qs[-1]-qs[-2]);cv=b.context_vec(prot,e,rng);cp=ctxclf.predict_proba(cv.reshape(1,-1))[0];cc=int(ctxclf.classes_[int(np.argmax(cp))]);cm=float(np.sort(cp)[-1]-np.sort(cp)[-2]);rv=float(rel.predict_proba([[mg,cf,float(p!=cc),cm,len(s)/40]])[0,1]);ask=(rv<.68 or (p!=cc and cm>.1))
                if ask:
                    req+=1
                    # first get another acoustic view
                    s2,_=w.episode(e,rng,'hard_noise' if cond!='matched' else 'matched');q=q+L.probs(s2)
                    if mode=='consequence_probe':
                        # choose physical action maximizing expected separation of top candidate effects.
                        top=np.argsort(q)[-2:];a=int(np.argmax(np.abs(learned[top[-1]]-learned[top[-2]])))
                        truei=cidx[y];obs=sig[truei,a]+rng.normal(0,.65)
                        # Bayesian-like generic evidence update from learned consequence error.
                        q=np.log(q+1e-8)
                        for ci in range(len(classes)):q[ci]+=-((obs-learned[ci,a])**2)/(2*.85**2)
                    # softly include independent context evidence
                    cvec=np.zeros(len(classes))
                    for i,c in enumerate(ctxclf.classes_):
                        if int(c) in cidx:cvec[cidx[int(c)]]=cp[i]
                    if mode=='context_reinspect':q=q+0.7*cvec
                    else:q=q+np.log(0.2+0.8*cvec)
                    p=int(classes[int(np.argmax(q))])
                ok+=p==y
            modes[mode][cond]=ok/N;modes[mode][cond+'_request']=req/N
        modes[mode]['hard_mean']=float(np.mean([modes[mode][x] for x in ['hard_noise','onset_damage','near_twin','confwrong','speaker_shift','novel']]))
        # correlated wrong: action probe should either correct or abstain rather than trusting two misleading utterances
        safe=0;correct=0;abst=0;N=1600
        for _ in range(N):
            e=int(rng.integers(0,w.entities));s,y=w.episode(e,rng,'confwrong');s2,_=w.episode(e,rng,'confwrong');q=L.probs(s)+L.probs(s2);cv=b.context_vec(prot,e,rng);cp=ctxclf.predict_proba(cv.reshape(1,-1))[0];cc=int(ctxclf.classes_[int(np.argmax(cp))]);
            if mode=='consequence_probe':
                top=np.argsort(q)[-2:];a=int(np.argmax(np.abs(learned[top[-1]]-learned[top[-2]])));obs=sig[cidx[y],a]+rng.normal(0,.65);score=np.log(q+1e-8)
                for ci in range(len(classes)):score[ci]+=-((obs-learned[ci,a])**2)/(2*.85**2)
                cvec=np.zeros(len(classes))
                for i,c in enumerate(ctxclf.classes_):
                    if int(c) in cidx:cvec[cidx[int(c)]]=cp[i]
                score+=np.log(0.2+0.8*cvec);order=np.argsort(score);margin=score[order[-1]]-score[order[-2]];pred=int(classes[order[-1]])
                # unresolved crossmodal conflict + low posterior separation => abstain
                decision=-1 if margin<.65 else pred
            else:
                pred=int(classes[int(np.argmax(q))]);decision=-1 if pred!=cc else pred
            correct+=decision==y;abst+=decision==-1;safe+=(decision==y or decision==-1)
        modes[mode]['correlated_wrong_correct']=correct/N;modes[mode]['correlated_wrong_abstain']=abst/N;modes[mode]['correlated_wrong_safe']=safe/N
        # ambiguous mixed referent: consequence itself alternates between competing grounded states, so confident commitment is bad.
        ab=0;N=1600
        for _ in range(N):
            e=int(rng.integers(0,w.entities));s,_=w.ambiguous(e,rng);q=L.probs(s);top=np.argsort(q)[-2:]
            if mode=='consequence_probe':
                a=int(np.argmax(np.abs(learned[top[-1]]-learned[top[-2]])));true_e=e if rng.random()<.5 else (e^1);truey=int(w.effect[true_e]);obs=sig[cidx[truey],a]+rng.normal(0,.8);score=np.log(q+1e-8)
                for ci in range(len(classes)):score[ci]+=-((obs-learned[ci,a])**2)/(2*.95**2)
                order=np.argsort(score);margin=score[order[-1]]-score[order[-2]];decision=-1 if margin<1.15 else int(classes[order[-1]])
            else:
                qs=np.sort(q);decision=-1 if qs[-1]-qs[-2]<.22 else int(classes[int(np.argmax(q))])
            ab+=decision==-1
        modes[mode]['ambiguous_abstain']=ab/N
    return modes

def main():
    from concurrent.futures import ProcessPoolExecutor,as_completed
    rows=[]
    with ProcessPoolExecutor(max_workers=4) as ex:
        fs={ex.submit(run,9500+i):9500+i for i in range(8)}
        for f in as_completed(fs):r=f.result();rows.append({'seed':fs[f],'modes':r});print('DONE',fs[f],flush=True)
    rows.sort(key=lambda x:x['seed']); modes=['context_reinspect','consequence_probe'];keys=['matched','hard_noise','onset_damage','near_twin','confwrong','speaker_shift','novel','hard_mean','correlated_wrong_correct','correlated_wrong_abstain','correlated_wrong_safe','ambiguous_abstain']
    agg={m:{k:float(np.mean([r['modes'][m][k] for r in rows])) for k in keys} for m in modes}
    out={'aggregate':agg,'rows':rows,'boundary':'REFERENCE_ONLY. Consequence probe is selected by top-hypothesis predicted physical-effect separation learned from exploratory interaction. No token/phoneme/VAD/chunk/corruption/identity labels are supplied at test.'};(OUT/'R31_ACTIVE_CONSEQUENCE_PROBE_REFERENCE_ONLY.json').write_text(json.dumps(out,indent=2));print(json.dumps(agg,indent=2))
if __name__=='__main__':main()
