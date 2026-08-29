from __future__ import annotations

import json, math, os, sys, time
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
TEMPLATES=[d.TRAIN_TEMPLATES[0],old.CAL_TEMPLATE,old.LONG_TEMPLATE,old.POST_TEMPLATE,
           'although something else happened, {actor} must {action} the {object} now',
           'please observe while {actor} will carefully {action} the {object}']
VOICES=['en-wi','en-uk-rp','en-sc','en-uk-north','en-us']


def load_model(seed:int):
    ck=torch.load(OUT/f'R32_TEMPORAL_CHALLENGE_MODEL_{seed}.pt',map_location='cpu',weights_only=False)
    torch.manual_seed(seed);m=d.TemporalConvPAM();m.load_state_dict(ck['state_dict']);m.eval();return m


def probs(model,features,batch=96):
    class Mem(torch.utils.data.Dataset):
        def __len__(self):return len(features)
        def __getitem__(self,i):return features[i],0,'x'
    out=[]
    with torch.no_grad():
        for x,l,_,_ in DataLoader(Mem(),batch_size=batch,shuffle=False,collate_fn=d.collate,num_workers=0):
            z,_=model(x,l);out.append(torch.softmax(z,1).cpu().numpy())
    return np.concatenate(out) if out else np.empty((0,len(A)))


def entropy(p):return float(-(p*np.log(np.clip(p,1e-9,1))).sum()/math.log(len(p)))
def margin(p):
    q=np.sort(p);return float(q[-1]-q[-2])
def js(a,b):
    m=.5*(a+b);return float(.5*np.sum(a*np.log(np.clip(a,1e-9,1)/np.clip(m,1e-9,1)))+.5*np.sum(b*np.log(np.clip(b,1e-9,1)/np.clip(m,1e-9,1))))
def obs_feat(p):
    q=np.sort(p);return np.array([p.max(),q[-1]-q[-2],1-entropy(p),np.sum(p*p),q[-1],q[-2]],float)


def dev_specs(seed):
    specs,_=d.build_specs(seed,4);keys=sorted({(s.actor_i,s.action_i,s.object_i,s.voice,s.speed,s.pitch,s.template) for s in specs})
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
        dis=A[(s.action_i+2+s.object_i)%len(A)];tm='although someone '+dis+' nothing, {actor} {action} the {object} now'
        return old.custom_feature(s.actor,s.action,s.object_name,'en-uk-north',175,55,tm,seed,1),'acoustic_en_uk_north'
    return old.custom_feature(s.actor,s.action,s.object_name,'en-us',185,50,d.TRAIN_TEMPLATES[0],seed,1),'acoustic_en_us'


def mixture(actor,obj,y1,y2,seed,variant):
    t1=TEMPLATES[variant%len(TEMPLATES)].format(actor=actor,action=A[y1],object=obj)
    t2=TEMPLATES[(variant+2)%len(TEMPLATES)].format(actor=actor,action=A[y2],object=obj)
    return old.mix_feature(t1,t2,VOICES[variant%len(VOICES)],VOICES[(variant+1)%len(VOICES)],115+variant*13,215-variant*9,42+variant*4,68-variant*3,seed)


def train_obs_reliability(model,specs,seed):
    waves=[];truth=[];sources=[]
    for i,s in enumerate(specs[:180]):
        for kind in range(5):
            f,src=make_obs(s,seed+i*37+kind*100003,kind);waves.append(f);truth.append(s.action_i);sources.append(src)
    print('RELIABILITY_INFER',len(waves),flush=True);pp=probs(model,waves);truth=np.asarray(truth)
    X=np.stack([obs_feat(p) for p in pp]);y=(pp.argmax(1)==truth).astype(int)
    if len(np.unique(y))<2:raise RuntimeError('observation reliability target saturated')
    clf=make_pipeline(StandardScaler(),LogisticRegression(max_iter=800,class_weight='balanced')).fit(X,y)
    cnt=defaultdict(lambda:[2,2])
    for ok,src in zip(y,sources):cnt[src][0]+=int(ok);cnt[src][1]+=1
    trust={src:a/b for src,(a,b) in cnt.items()};trust['acoustic_global']=float(np.mean(list(trust.values())))
    rng=np.random.default_rng(seed+991);pc=(rng.random(800)<.965).astype(int);trust['physical_consequence']=(2+pc.sum())/(2+len(pc))
    return clf,trust,{'n':len(y),'error_rate':float(1-y.mean()),'source_trust':trust}


def reliability(clf,p):return float(clf.predict_proba(obs_feat(p)[None,:])[0,1])

def fuse(obs,relclf,trust):
    groups=defaultdict(list)
    for p,src in obs:groups[src].append(p)
    score=np.zeros(len(A));ws=[]
    for src,ps in groups.items():
        pg=np.mean(ps,0);r=float(np.mean([reliability(relclf,p) for p in ps]));t=trust.get(src,trust['acoustic_global']);w=max(.02,r*t)
        score+=w*np.log(np.clip(pg,1e-7,1));ws.append(w)
    z=np.exp(score-score.max());post=z/z.sum();return post,float(np.mean(ws) if ws else 0),len(groups)

def state_feat(post,prev,obs,relclf,trust,streak):
    rel=[reliability(relclf,p) for p,_ in obs];src=[s for _,s in obs];pred=[int(np.argmax(p)) for p,_ in obs]
    disagree=0 if len(pred)<2 else 1-max(pred.count(k) for k in set(pred))/len(pred)
    return np.array([post.max(),margin(post),1-entropy(post),np.mean(rel),np.min(rel),len(set(src))/len(src),1-disagree,1-(js(post,prev) if prev is not None else 0),streak/len(obs)],float)


def episode_features(obs,relclf,trust):
    posts=[];xs=[];bests=[];prev=None;last=-1;streak=0
    for z in obs:
        cur=obs[:len(posts)+1];post,_,_=fuse(cur,relclf,trust);b=int(np.argmax(post));streak=streak+1 if b==last else 1;last=b
        xs.append(state_feat(post,prev,cur,relclf,trust,streak));posts.append(post);bests.append(b);prev=post
    return posts,xs,bests


def build_meta(model,specs,relclf,trust,seed):
    stable_specs=specs[:150];unstable_specs=specs[:120]
    sw=[];smeta=[]
    for i,s in enumerate(stable_specs):
        row=[]
        for k in range(3):f,src=make_obs(s,seed+i*43+k*10007,k);sw.append(f);row.append((len(sw)-1,src))
        smeta.append((row,s.action_i))
    uw=[];umeta=[]
    for i,s in enumerate(unstable_specs):
        y2=(s.action_i+1+(i%4))%len(A);row=[]
        for k in range(3):uw.append(mixture(s.actor,s.object_name,s.action_i,y2,seed+700000+i*101+k*10009,k));row.append((len(uw)-1,f'mixture_source_{k}'))
        umeta.append((row,[s.action_i,y2,s.action_i,y2,s.action_i,y2]))
    print('META_STABLE_INFER',len(sw),flush=True);sp=probs(model,sw);print('META_UNSTABLE_INFER',len(uw),flush=True);up=probs(model,uw)
    rows=[];gains=[]
    for row,truth in smeta:
        obs=[(sp[i],src) for i,src in row];posts,xs,bests=episode_features(obs,relclf,trust)
        for k,x in enumerate(xs):
            safe=int(bests[k]==truth and all(z==truth for z in bests[k:]));gain=max(0,entropy(posts[k])-entropy(posts[k+1])) if k<2 else 0
            rows.append((x,safe,'stable'));gains.append((x,gain))
    for row,outcomes in umeta:
        obs=[(up[i],src) for i,src in row];posts,xs,bests=episode_features(obs,relclf,trust)
        for k,x in enumerate(xs):
            # Safe is derived from future grounded-outcome stability. Alternating
            # outcomes never license one unique commitment.
            future=outcomes[k:];safe=int(len(set(future))==1 and bests[k]==future[0]);gain=max(0,entropy(posts[k])-entropy(posts[k+1])) if k<2 else 0
            rows.append((x,safe,'unstable'));gains.append((x,gain))
    X=np.stack([z[0] for z in rows]);y=np.asarray([z[1] for z in rows]);safe=make_pipeline(StandardScaler(),LogisticRegression(max_iter=1000,class_weight='balanced')).fit(X,y)
    gain=make_pipeline(StandardScaler(),Ridge(alpha=2)).fit(np.stack([z[0] for z in gains]),np.asarray([z[1] for z in gains]))
    return safe,gain,{'n':len(y),'safe_rate':float(y.mean()),'stable_n':sum(z[2]=='stable' for z in rows),'unstable_n':sum(z[2]=='unstable' for z in rows)}


def precompute_policy_episodes(model,specs,seed):
    stable_specs=specs[:70];unstable_specs=specs[:70];waves=[];episodes=[]
    for i,s in enumerate(stable_specs):
        row=[]
        for k in range(3):f,src=make_obs(s,seed+i*31+k*1009,k);waves.append(f);row.append((len(waves)-1,src))
        episodes.append((row,s.action_i,True))
    for i,s in enumerate(unstable_specs):
        y2=(s.action_i+2+(i%3))%len(A);row=[]
        for k in range(3):waves.append(mixture(s.actor,s.object_name,s.action_i,y2,seed+900000+i*71+k*1009,k));row.append((len(waves)-1,f'mix_{k}'))
        episodes.append((row,-1,False))
    print('POLICY_INFER',len(waves),flush=True);pp=probs(model,waves)
    return [([(pp[i],src) for i,src in row],truth,stable) for row,truth,stable in episodes]


def choose_policy(episodes,relclf,trust,safeclf,gainclf):
    cached=[]
    for obsall,truth,isstable in episodes:
        posts,xs,bests=episode_features(obsall,relclf,trust);sp=[float(safeclf.predict_proba(x[None,:])[0,1]) for x in xs];eg=[max(0,float(gainclf.predict(x[None,:])[0])) for x in xs];cached.append((truth,isstable,bests,sp,eg))
    best=None
    for ct in np.linspace(.48,.94,24):
      for gt in np.linspace(0,.12,17):
        util=[]
        for truth,isstable,bests,sp,eg in cached:
          dec=-1;used=3
          for k in range(3):
            if sp[k]>=ct:dec=bests[k];used=k+1;break
            if k==2 or eg[k]<=gt:dec=-1;used=k+1;break
          score=(1 if dec==truth else (-3 if dec>=0 else -.25)) if isstable else (1 if dec<0 else -3);score-=.025*used;util.append(score)
        z=(float(np.mean(util)),float(ct),float(gt))
        if best is None or z[0]>best[0]:best=z
    return {'utility':best[0],'commit_threshold':best[1],'gain_threshold':best[2]}


def run_episode(obs,relclf,trust,safeclf,gainclf,ct,gt):
    posts,xs,bests=episode_features(obs,relclf,trust);trace=[]
    for k,x in enumerate(xs):
        sp=float(safeclf.predict_proba(x[None,:])[0,1]);eg=max(0,float(gainclf.predict(x[None,:])[0]));trace.append({'step':k+1,'best':bests[k],'margin':margin(posts[k]),'entropy':entropy(posts[k]),'safe':sp,'gain':eg})
        if sp>=ct:return bests[k],k+1,trace
        if k==2 or eg<=gt:return -1,k+1,trace
    return -1,3,trace


def evaluate(seed=35400):
    t0=time.time();model=load_model(seed);specs=dev_specs(seed);print('SPECS',len(specs),flush=True)
    rel,trust,relmeta=train_obs_reliability(model,specs,seed+2000);print('RELIABILITY_DONE',relmeta,flush=True)
    safe,gain,metameta=build_meta(model,specs,rel,trust,seed+4000);print('META_DONE',metameta,flush=True)
    episodes=precompute_policy_episodes(model,specs,seed+6000);policy=choose_policy(episodes,rel,trust,safe,gain);print('POLICY_DONE',policy,flush=True)
    actors=d.base.ACTORS[:3];objects=d.base.OBJECTS[:3];waves=[];cases=[]
    for ai,a in enumerate(actors):
      for y,act in enumerate(A):
       for oi,obj in enumerate(objects):
        dis=A[(y+2+oi)%len(A)]
        forms=[('extreme_voice','en-wi',82,24,d.TRAIN_TEMPLATES[0],3),('long_filler','en-uk-rp',215,61,old.LONG_TEMPLATE,2),('postposed','en-wi',120,43,old.POST_TEMPLATE,1),('distractor_before','en-uk-rp',175,55,'although someone '+dis+' nothing, {actor} {action} the {object} now',1),('distractor_after','en-wi',165,55,'{actor} {action} the {object} now, while someone '+dis+' nothing',1),('strong_noise','en-wi',215,70,d.TRAIN_TEMPLATES[0],3)]
        for ci,(cond,v,sp,p,tm,strength) in enumerate(forms):
            row=[]
            for k,(vv,ss,pp,tt) in enumerate([(v,sp,p,tm),('en-uk-north',185,49,old.CAL_TEMPLATE),('en-sc',155,58,d.TRAIN_TEMPLATES[0])]):
                waves.append(old.custom_feature(a,act,obj,vv,ss,pp,tt,seed+ai*100000+y*10000+oi*1000+ci*100+k,strength if k==0 else 1));row.append((len(waves)-1,f'acoustic_{vv}_{k}'))
            cases.append((cond,y,row))
    amb=[]
    for y1 in range(len(A)):
      y2=(y1+1)%len(A);a=actors[y1%3];obj=objects[(y1*2)%3]
      for rep in range(30):
        row=[]
        for k in range(3):waves.append(mixture(a,obj,y1,y2,seed+1200000+y1*1000+rep*10+k,k));row.append((len(waves)-1,f'independent_mix_{k}'))
        amb.append((y1,y2,row))
    prov=[]
    for y,act in enumerate(A):
        w=(y+3)%len(A);a=actors[y%3];obj=objects[y%3];waves.append(old.custom_feature(a,A[w],obj,'en-wi',175,55,d.TRAIN_TEMPLATES[0],seed+1500000+y,1));prov.append((y,w,len(waves)-1))
    print('QUAL_INFER',len(waves),flush=True);pp=probs(model,waves)
    ct=policy['commit_threshold'];gt=policy['gain_threshold'];cond=defaultdict(list);tr=[]
    for name,y,row in cases:
        obs=[(pp[i],src) for i,src in row];dec,used,trace=run_episode(obs,rel,trust,safe,gain,ct,gt);cond[name].append((dec==y,dec<0,used));tr.append({'condition':name,'truth':y,'decision':dec,'trace':trace})
    resolvable={k:{'correct':float(np.mean([z[0] for z in v])),'unknown':float(np.mean([z[1] for z in v])),'mean_observations':float(np.mean([z[2] for z in v]))} for k,v in cond.items()}
    av=[];atr=[]
    for y1,y2,row in amb:
        obs=[(pp[i],src) for i,src in row];dec,used,trace=run_episode(obs,rel,trust,safe,gain,ct,gt);av.append((dec<0,dec in (y1,y2),used));atr.append({'pair':[y1,y2],'decision':dec,'trace':trace})
    ambiguous={'unknown_rate':float(np.mean([z[0] for z in av])),'pair_member_commit_rate':float(np.mean([z[1] for z in av])),'mean_observations':float(np.mean([z[2] for z in av]))}
    naive=[];grouped=[];trusted=[]
    for y,w,i in prov:
        pw=pp[i];physical=np.full(len(A),.015/(len(A)-1));physical[y]=.985
        naive.append(int(np.argmax((5*pw+physical)/6)==y));grouped.append(int(np.argmax((pw+physical)/2)==y));post,_,_=fuse([(pw,'wrong_acoustic_lineage')]*5+[(physical,'physical_consequence')],rel,trust);trusted.append(int(np.argmax(post)==y))
    provenance={'naive_recovery':float(np.mean(naive)),'grouped_recovery':float(np.mean(grouped)),'learned_trust_grouped_recovery':float(np.mean(trusted)),'learned_trust':trust}
    out={'seed':seed,'seconds':time.time()-t0,'observation_reliability':relmeta,'meta_training':metameta,'policy':policy,'resolvable':resolvable,'ambiguous':ambiguous,'provenance':provenance,'sample_resolvable_traces':tr[:12],'sample_ambiguous_traces':atr[:12],'boundary':'REFERENCE_ONLY batched persistent epistemic-population v2. Observation reliability, source trust, commitment stability, and expected information gain are learned from delayed grounded outcomes and future hypothesis stability. No ambiguity/corruption label, transcript, token, word/phoneme/chunk boundary, VAD, ASR, attention/transformer, or LLM enters cognition. Test metadata is evaluator-only.'}
    (OUT/f'R32_TEMPORAL_EPISTEMIC_POPULATION_V2_FAST_SEED_{seed}.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:out[k] for k in ['seconds','observation_reliability','meta_training','policy','resolvable','ambiguous','provenance']},indent=2));return out

if __name__=='__main__':evaluate(int(sys.argv[1]) if len(sys.argv)>1 else 35400)
