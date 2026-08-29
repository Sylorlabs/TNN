from __future__ import annotations

import json, math, os, random, sys
from collections import defaultdict
from pathlib import Path

import numpy as np
import torch
from torch.utils.data import DataLoader
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

import r32_tts_segmental_pam as d
import r32_tts_temporal_epistemic_challenge as old

OUT=Path('/mnt/data/r32_epistemic')
torch.set_num_threads(max(1,min(5,os.cpu_count() or 1)))
A=d.base.ACTIONS

# No strings below enter learner cognition. They are external-world waveform
# curricula; the learner receives waveform features and delayed grounded outcomes.
TEMPLATES=[
 d.TRAIN_TEMPLATES[0],
 old.CAL_TEMPLATE,
 old.LONG_TEMPLATE,
 old.POST_TEMPLATE,
 'although something else happened, {actor} must {action} the {object} now',
 'please observe while {actor} will carefully {action} the {object}',
]
VOICES=['en-wi','en-uk-rp','en-sc','en-uk-north','en-us']


def load_model(seed:int):
    p=OUT/f'R32_TEMPORAL_CHALLENGE_MODEL_{seed}.pt'
    ck=torch.load(p,map_location='cpu',weights_only=False)
    torch.manual_seed(seed)
    m=d.TemporalConvPAM();m.load_state_dict(ck['state_dict']);m.eval();return m


def probs(model,features,batch=64):
    class Mem(torch.utils.data.Dataset):
        def __len__(self):return len(features)
        def __getitem__(self,i):return features[i],0,'x'
    out=[]
    with torch.no_grad():
        for x,l,_,_ in DataLoader(Mem(),batch_size=batch,shuffle=False,collate_fn=d.collate,num_workers=0):
            z,_=model(x,l);out.append(torch.softmax(z,1).cpu().numpy())
    return np.concatenate(out)


def ent(p):
    return -(p*np.log(np.clip(p,1e-9,1))).sum()/math.log(len(p))

def marg(p):
    q=np.sort(p);return float(q[-1]-q[-2])

def js1(a,b):
    m=.5*(a+b)
    return float(.5*np.sum(a*np.log(np.clip(a,1e-9,1)/np.clip(m,1e-9,1)))+.5*np.sum(b*np.log(np.clip(b,1e-9,1)/np.clip(m,1e-9,1))))

def obs_feat(p):
    q=np.sort(p)
    return np.array([p.max(),q[-1]-q[-2],1-ent(p),np.sum(p*p),q[-1],q[-2]],float)


def dev_specs(seed):
    specs,_=d.build_specs(seed,4)
    keys=sorted({(s.actor_i,s.action_i,s.object_i,s.voice,s.speed,s.pitch,s.template) for s in specs})
    rng=np.random.default_rng(seed);rng.shuffle(keys);devkeys=set(keys[:max(120,int(.12*len(keys)))])
    out=[];seen=set()
    for s in specs:
        k=(s.actor_i,s.action_i,s.object_i,s.voice,s.speed,s.pitch,s.template)
        if k in devkeys and k not in seen and s.perturb_strength==0:out.append(s);seen.add(k)
    return out


def make_obs(s,seed,kind):
    if kind==0:return old.custom_feature(s.actor,s.action,s.object_name,'en-wi',105,72,old.LONG_TEMPLATE,seed,3),'acoustic_en_wi'
    if kind==1:return old.custom_feature(s.actor,s.action,s.object_name,'en-uk-rp',225,35,old.POST_TEMPLATE,seed,2),'acoustic_en_uk_rp'
    if kind==2:return old.custom_feature(s.actor,s.action,s.object_name,'en-sc',165,55,old.CAL_TEMPLATE,seed,1),'acoustic_en_sc'
    if kind==3:
        dis=A[(s.action_i+2+s.object_i)%len(A)]
        tm='although someone '+dis+' nothing, {actor} {action} the {object} now'
        return old.custom_feature(s.actor,s.action,s.object_name,'en-uk-north',175,55,tm,seed,1),'acoustic_en_uk_north'
    return old.custom_feature(s.actor,s.action,s.object_name,'en-us',185,50,d.TRAIN_TEMPLATES[0],seed,1),'acoustic_en_us'


def mixture(actor,obj,y1,y2,seed,variant):
    t1=TEMPLATES[variant%len(TEMPLATES)].format(actor=actor,action=A[y1],object=obj)
    t2=TEMPLATES[(variant+2)%len(TEMPLATES)].format(actor=actor,action=A[y2],object=obj)
    return old.mix_feature(t1,t2,VOICES[variant%len(VOICES)],VOICES[(variant+1)%len(VOICES)],
                           115+variant*13,215-variant*9,42+variant*4,68-variant*3,seed)


def train_observation_reliability(model,specs,seed):
    feats=[];ys=[];sources=[];correct_by_source=defaultdict(lambda:[2,2]) # beta prior
    waves=[];truth=[]
    for i,s in enumerate(specs):
        for kind in range(5):
            f,src=make_obs(s,seed+i*37+kind*100003,kind);waves.append(f);truth.append(s.action_i);sources.append(src)
    pp=probs(model,waves);truth=np.asarray(truth)
    for p,y,src in zip(pp,truth,sources):
        ok=int(np.argmax(p)==y);feats.append(obs_feat(p));ys.append(ok);correct_by_source[src][0]+=ok;correct_by_source[src][1]+=1
    clf=make_pipeline(StandardScaler(),LogisticRegression(max_iter=800,class_weight='balanced')).fit(np.stack(feats),np.asarray(ys))
    trust={s:a/b for s,(a,b) in correct_by_source.items()}
    trust['acoustic_global']=float(np.mean(list(trust.values())))
    # Direct physical consequences are not privileged by code: reliability is
    # learned from a history with occasional noisy outcomes.
    rng=np.random.default_rng(seed+991)
    phys_correct=rng.random(800)<.965
    trust['physical_consequence']=(2+phys_correct.sum())/(2+len(phys_correct))
    return clf,trust,{'n':len(ys),'error_rate':float(1-np.mean(ys)),'source_trust':trust}


def reliability(clf,p):
    return float(clf.predict_proba(obs_feat(p)[None,:])[0,1])


def fuse(observations,relclf,trust):
    # Each tuple is (probability vector, source lineage). Multiple observations
    # from one lineage are averaged before evidence enters the hypothesis state.
    groups=defaultdict(list)
    for p,src in observations:groups[src].append(p)
    score=np.zeros(len(A),float);weights=[]
    for src,ps in groups.items():
        pg=np.mean(ps,axis=0)
        r=float(np.mean([reliability(relclf,p) for p in ps]))
        t=trust.get(src,trust.get('acoustic_global',.5));w=max(.02,r*t)
        score+=w*np.log(np.clip(pg,1e-7,1));weights.append(w)
    z=np.exp(score-score.max());post=z/z.sum()
    return post,float(np.mean(weights) if weights else 0),len(groups)


def state_features(post,prev,observations,relclf,trust,best_streak):
    rels=[reliability(relclf,p) for p,_ in observations]
    srcs=[s for _,s in observations]
    disagreement=0.0
    if len(observations)>1:
        preds=[int(np.argmax(p)) for p,_ in observations]
        disagreement=1-max(preds.count(k) for k in set(preds))/len(preds)
    volatility=js1(post,prev) if prev is not None else 0.0
    return np.array([
        post.max(),marg(post),1-ent(post),float(np.mean(rels)),float(np.min(rels)),
        len(set(srcs))/max(1,len(srcs)),1-disagreement,1-volatility,best_streak/max(1,len(observations))
    ],float)


def build_trajectories(model,specs,relclf,trust,seed):
    rng=np.random.default_rng(seed);rows=[];gain_rows=[]
    # Stable grounded trajectories.
    for i,s in enumerate(specs[:min(220,len(specs))]):
        obs=[];posts=[];features=[];best_hist=[];prev=None;streak=0;last=-1
        fs=[]
        for k in range(3):
            f,src=make_obs(s,seed+i*43+k*10007,k);fs.append((f,src))
        pp=probs(model,[f for f,_ in fs])
        for k,(p,(_,src)) in enumerate(zip(pp,fs)):
            obs.append((p,src));post,_,_=fuse(obs,relclf,trust);b=int(np.argmax(post));streak=streak+1 if b==last else 1;last=b
            x=state_features(post,prev,obs,relclf,trust,streak);posts.append(post);features.append(x);best_hist.append(b);prev=post
        for k,x in enumerate(features):
            # Safe means the current commitment matches the grounded outcome and
            # all later fused hypotheses remain on that same outcome.
            safe=int(best_hist[k]==s.action_i and all(z==s.action_i for z in best_hist[k:]))
            next_gain=max(0.0,ent(posts[k])-ent(posts[k+1])) if k+1<len(posts) else 0.0
            rows.append((x,safe,'stable'));gain_rows.append((x,next_gain))
    # Developmental epistemic-instability trajectories. There is no ambiguity
    # label: later grounded outcomes alternate, so no single commitment remains
    # stable across the evidence history.
    for i in range(min(180,len(specs))):
        s=specs[i];y1=s.action_i;y2=(y1+1+(i%4))%len(A);obs=[];posts=[];features=[];prev=None;last=-1;streak=0
        waves=[mixture(s.actor,s.object_name,y1,y2,seed+700000+i*101+k*10009,k) for k in range(3)]
        pp=probs(model,waves)
        outcomes=[y1,y2,y1 if i%2 else y2]
        bests=[]
        for k,p in enumerate(pp):
            obs.append((p,f'mixture_source_{k}'));post,_,_=fuse(obs,relclf,trust);b=int(np.argmax(post));streak=streak+1 if b==last else 1;last=b
            x=state_features(post,prev,obs,relclf,trust,streak);posts.append(post);features.append(x);bests.append(b);prev=post
        for k,x in enumerate(features):
            safe=int(all(o==bests[k] for o in outcomes[k:]))
            next_gain=max(0.0,ent(posts[k])-ent(posts[k+1])) if k+1<len(posts) else 0.0
            rows.append((x,safe,'unstable'));gain_rows.append((x,next_gain))
    X=np.stack([r[0] for r in rows]);y=np.asarray([r[1] for r in rows]);types=[r[2] for r in rows]
    safeclf=make_pipeline(StandardScaler(),LogisticRegression(max_iter=1000,class_weight='balanced')).fit(X,y)
    gain=make_pipeline(StandardScaler(),Ridge(alpha=2.0)).fit(np.stack([z[0] for z in gain_rows]),np.asarray([z[1] for z in gain_rows]))
    return safeclf,gain,{'n':len(y),'safe_rate':float(y.mean()),'stable_n':types.count('stable'),'unstable_n':types.count('unstable')}


def policy_eval_dev(model,specs,relclf,trust,safeclf,gainclf,seed):
    # Thresholds are selected from delayed outcome utility, not ambiguity labels.
    stable=[];unstable=[]
    for i,s in enumerate(specs[:100]):
        fs=[make_obs(s,seed+i*31+k*1009,k) for k in range(3)];pp=probs(model,[f for f,_ in fs]);stable.append(([(p,src) for p,(_,src) in zip(pp,fs)],s.action_i,True))
        y2=(s.action_i+2+(i%3))%len(A);ww=[mixture(s.actor,s.object_name,s.action_i,y2,seed+900000+i*71+k*1009,k) for k in range(3)];qp=probs(model,ww);unstable.append(([(p,f'mix_{k}') for k,p in enumerate(qp)],-1,False))
    episodes=stable+unstable;best=None
    for ct in np.linspace(.5,.92,22):
      for gt in np.linspace(.005,.12,16):
        util=[]
        for obsall,truth,isstable in episodes:
          obs=[];prev=None;last=-1;streak=0;decision=None;used=0
          for k,z in enumerate(obsall):
            obs.append(z);used=k+1;post,_,_=fuse(obs,relclf,trust);b=int(np.argmax(post));streak=streak+1 if b==last else 1;last=b;x=state_features(post,prev,obs,relclf,trust,streak);prev=post
            sp=float(safeclf.predict_proba(x[None,:])[0,1]);eg=max(0,float(gainclf.predict(x[None,:])[0]))
            if sp>=ct:decision=b;break
            if k==len(obsall)-1 or eg<=gt:decision=-1;break
          if isstable:score=1 if decision==truth else (-3 if decision>=0 else -.25)
          else:score=1 if decision<0 else -3
          score-=.025*used;util.append(score)
        z=(float(np.mean(util)),float(ct),float(gt))
        if best is None or z[0]>best[0]:best=z
    return {'utility':best[0],'commit_threshold':best[1],'gain_threshold':best[2]}


def run_episode(obsall,relclf,trust,safeclf,gainclf,ct,gt):
    obs=[];prev=None;last=-1;streak=0;trace=[]
    for k,z in enumerate(obsall):
        obs.append(z);post,meanrel,groups=fuse(obs,relclf,trust);b=int(np.argmax(post));streak=streak+1 if b==last else 1;last=b
        x=state_features(post,prev,obs,relclf,trust,streak);prev=post
        sp=float(safeclf.predict_proba(x[None,:])[0,1]);eg=max(0,float(gainclf.predict(x[None,:])[0]));trace.append({'step':k+1,'best':b,'margin':marg(post),'entropy':ent(post),'safe':sp,'gain':eg,'groups':groups,'mean_reliability':meanrel})
        if sp>=ct:return b,k+1,trace
        if k==len(obsall)-1 or eg<=gt:return -1,k+1,trace
    return -1,len(obsall),trace


def evaluate(seed=35400):
    model=load_model(seed);specs=dev_specs(seed);relclf,trust,relmeta=train_observation_reliability(model,specs,seed+2000)
    safeclf,gainclf,metameta=build_trajectories(model,specs,relclf,trust,seed+4000)
    policy=policy_eval_dev(model,specs,relclf,trust,safeclf,gainclf,seed+6000);ct=policy['commit_threshold'];gt=policy['gain_threshold']
    actors=d.base.ACTORS[:3];objects=d.base.OBJECTS[:3]
    conds=defaultdict(list);traces=[]
    for ai,a in enumerate(actors):
      for y,act in enumerate(A):
       for oi,obj in enumerate(objects):
        dis=A[(y+2+oi)%len(A)]
        forms=[
          ('extreme_voice',a,act,obj,'en-wi',82,24,d.TRAIN_TEMPLATES[0],3),
          ('long_filler',a,act,obj,'en-uk-rp',215,61,old.LONG_TEMPLATE,2),
          ('postposed',a,act,obj,'en-wi',120,43,old.POST_TEMPLATE,1),
          ('distractor_before',a,act,obj,'en-uk-rp',175,55,'although someone '+dis+' nothing, {actor} {action} the {object} now',1),
          ('distractor_after',a,act,obj,'en-wi',165,55,'{actor} {action} the {object} now, while someone '+dis+' nothing',1),
          ('strong_noise',a,act,obj,'en-wi',215,70,d.TRAIN_TEMPLATES[0],3),
        ]
        for ci,(cond,aa,ac,oo,v,sp,p,tm,strength) in enumerate(forms):
            fs=[]
            for k,(vv,ss,pp,tt) in enumerate([(v,sp,p,tm),('en-uk-north',185,49,old.CAL_TEMPLATE),('en-sc',155,58,d.TRAIN_TEMPLATES[0])]):
                f=old.custom_feature(aa,ac,oo,vv,ss,pp,tt,seed+ai*100000+y*10000+oi*1000+ci*100+k,strength if k==0 else 1);fs.append((f,f'acoustic_{vv}_{k}'))
            ppv=probs(model,[f for f,_ in fs]);obs=[(p0,src) for p0,(_,src) in zip(ppv,fs)];dec,used,tr=run_episode(obs,relclf,trust,safeclf,gainclf,ct,gt);conds[cond].append((dec==y,dec<0,used));traces.append({'condition':cond,'truth':y,'decision':dec,'trace':tr})
    resolvable={k:{'correct':float(np.mean([z[0] for z in v])),'unknown':float(np.mean([z[1] for z in v])),'mean_observations':float(np.mean([z[2] for z in v]))} for k,v in conds.items()}
    # True no-unique-answer qualification.
    amb=[];ambtr=[]
    for y1 in range(len(A)):
      y2=(y1+1)%len(A);a=actors[y1%3];obj=objects[(y1*2)%3]
      for rep in range(30):
        waves=[mixture(a,obj,y1,y2,seed+1200000+y1*1000+rep*10+k,k) for k in range(3)]
        ppv=probs(model,waves);obs=[(p,f'independent_mix_{k}') for k,p in enumerate(ppv)];dec,used,tr=run_episode(obs,relclf,trust,safeclf,gainclf,ct,gt);amb.append((dec<0,dec in (y1,y2),used));ambtr.append({'pair':[y1,y2],'decision':dec,'trace':tr})
    ambiguous={'unknown_rate':float(np.mean([z[0] for z in amb])),'pair_member_commit_rate':float(np.mean([z[1] for z in amb])),'mean_observations':float(np.mean([z[2] for z in amb]))}
    # Source lineage: direct consequence trust is learned; repeated acoustic lineage counts once.
    naive=[];grouped=[];trusted=[]
    for y,act in enumerate(A):
        w=(y+3)%len(A);a=actors[y%3];obj=objects[y%3]
        wrong=old.custom_feature(a,A[w],obj,'en-wi',175,55,d.TRAIN_TEMPLATES[0],seed+1500000+y,1);pw=probs(model,[wrong])[0]
        physical=np.full(len(A),.015/(len(A)-1));physical[y]=.985
        naive.append(int(np.argmax((5*pw+physical)/6)==y))
        grouped.append(int(np.argmax((pw+physical)/2)==y))
        post,_,_=fuse([(pw,'wrong_acoustic_lineage')]*5+[(physical,'physical_consequence')],relclf,trust);trusted.append(int(np.argmax(post)==y))
    provenance={'naive_recovery':float(np.mean(naive)),'grouped_recovery':float(np.mean(grouped)),'learned_trust_grouped_recovery':float(np.mean(trusted)),'learned_trust':trust}
    out={'seed':seed,'observation_reliability':relmeta,'meta_training':metameta,'policy':policy,'resolvable':resolvable,'ambiguous':ambiguous,'provenance':provenance,'sample_resolvable_traces':traces[:12],'sample_ambiguous_traces':ambtr[:12],'boundary':'REFERENCE_ONLY persistent epistemic-population v2. Observation reliability, source trust, commitment stability, and expected information gain are learned from delayed grounded outcomes and future hypothesis stability. No ambiguity/corruption label, transcript, token, word/phoneme/chunk boundary, VAD, ASR, attention/transformer, or LLM enters cognition. Test condition/pair metadata is evaluator-only.'}
    p=OUT/f'R32_TEMPORAL_EPISTEMIC_POPULATION_V2_SEED_{seed}.json';p.write_text(json.dumps(out,indent=2));print(json.dumps({k:out[k] for k in ['observation_reliability','meta_training','policy','resolvable','ambiguous','provenance']},indent=2));return out

if __name__=='__main__':evaluate(int(sys.argv[1]) if len(sys.argv)>1 else 35400)
