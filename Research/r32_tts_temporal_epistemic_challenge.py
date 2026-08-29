from __future__ import annotations

import json, math, os, random, sys, gc
from pathlib import Path
from dataclasses import replace
import numpy as np
import torch
from torch.utils.data import DataLoader
from sklearn.linear_model import LogisticRegression
from scipy.signal import resample

import r32_tts_segmental_pam as d

OUT=Path('/mnt/data/r32_epistemic')
torch.set_num_threads(max(1,min(5,os.cpu_count() or 1)))

CAL_TEMPLATE='without delay {actor} should carefully {action} the {object}'
LONG_TEMPLATE='before anything else and without unnecessary delay {actor} will carefully {action} the {object} right now'
POST_TEMPLATE='the thing {actor} will do to the {object} at this moment is {action}'


def probs(model, features, batch=64):
    class Mem(torch.utils.data.Dataset):
        def __len__(self):return len(features)
        def __getitem__(self,i):return features[i],0,'x'
    out=[];model.eval()
    with torch.no_grad():
        for x,l,_,_ in DataLoader(Mem(),batch_size=batch,shuffle=False,collate_fn=d.collate,num_workers=0):
            z,_=model(x,l);out.append(torch.softmax(z,1).cpu().numpy())
    return np.concatenate(out)

def entropy(p):return -(p*np.log(np.clip(p,1e-9,1))).sum(1)/math.log(p.shape[1])
def margin(p):
    q=np.sort(p,axis=1);return q[:,-1]-q[:,-2]
def js(a,b):
    m=.5*(a+b)
    kl=lambda x,y:(x*np.log(np.clip(x,1e-9,1)/np.clip(y,1e-9,1))).sum(1)
    return .5*kl(a,m)+.5*kl(b,m)
def rel_features(p1,p2):
    c=.5*(p1+p2);agree=(p1.argmax(1)==p2.argmax(1)).astype(float)
    return np.column_stack([p1.max(1),margin(p1),1-entropy(p1),agree,1-js(p1,p2),c.max(1),margin(c)])

def custom_feature(actor,action,obj,voice,speed,pitch,template,seed,strength=0):
    text=template.format(actor=actor,action=action,object=obj)
    sr,x=d.synth_text(text,voice,speed,pitch);x=d.perturb(sr,x,seed,strength);return d.feature(sr,x)

def mix_feature(text1,text2,voice1,voice2,speed1,speed2,pitch1,pitch2,seed):
    sr1,x1=d.synth_text(text1,voice1,speed1,pitch1);sr2,x2=d.synth_text(text2,voice2,speed2,pitch2)
    n=max(len(x1),len(x2));a=resample(x1,n).astype(np.float32);b=resample(x2,n).astype(np.float32)
    r=np.random.default_rng(seed);a=a*r.uniform(.88,1.12);b=b*r.uniform(.88,1.12);y=(a+b)/max(1e-6,np.max(np.abs(a+b)))
    y+=r.normal(0,.006,n).astype(np.float32);return d.feature(sr1,np.clip(y,-1,1).astype(np.float32))

def train_temporal(seed):
    specs,_=d.build_specs(seed,4);keys=sorted({(s.actor_i,s.action_i,s.object_i,s.voice,s.speed,s.pitch,s.template) for s in specs});rng=np.random.default_rng(seed);rng.shuffle(keys);devkeys=set(keys[:max(120,int(.12*len(keys)))])
    tr=[s for s in specs if (s.actor_i,s.action_i,s.object_i,s.voice,s.speed,s.pitch,s.template) not in devkeys]
    dv=[];seen=set()
    for s in specs:
        k=(s.actor_i,s.action_i,s.object_i,s.voice,s.speed,s.pitch,s.template)
        if k in devkeys and k not in seen and s.perturb_strength==0:dv.append(s);seen.add(k)
    trds=d.AcousticDataset(tr,seed);dvds=d.AcousticDataset(dv,seed+91);torch.manual_seed(seed);m=d.TemporalConvPAM();hist=d.train_model(m,trds,dvds,seed,epochs=14,batch_size=32)
    torch.save({'state_dict':m.state_dict(),'seed':seed,'history':hist},OUT/f'R32_TEMPORAL_CHALLENGE_MODEL_{seed}.pt')
    return m,dv

def calibration(model,dev_specs,seed):
    rng=random.Random(seed);chosen=dev_specs[:]
    rng.shuffle(chosen);chosen=chosen[:min(480,len(chosen))]
    f1=[];f2=[];y=[]
    for i,s in enumerate(chosen):
        # First view is intentionally difficult; second is independent ordinary evidence.
        tmpl=CAL_TEMPLATE if i%2 else LONG_TEMPLATE
        f1.append(custom_feature(s.actor,s.action,s.object_name,'en-wi',105 if i%3 else 235,72,tmpl,seed+i*13,3 if i%4==0 else 2))
        f2.append(custom_feature(s.actor,s.action,s.object_name,'en-uk-rp',185,45,d.TRAIN_TEMPLATES[0],seed+70000+i,1))
        y.append(s.action_i)
    p1=probs(model,f1);p2=probs(model,f2);yy=np.asarray(y);X=rel_features(p1,p2);target=(p1.argmax(1)==yy).astype(int)
    # Balance delayed-correctness examples where possible; the target is eventual
    # grounded correctness, never an ambiguity/corruption label.
    clf=LogisticRegression(max_iter=500,class_weight='balanced').fit(X,target)
    r=clf.predict_proba(X)[:,1];comb=.5*(p1+p2);m1=margin(p1);m2=margin(comb)
    best=None
    for rt in np.linspace(.15,.9,31):
        for mt in np.linspace(.02,.45,23):
            commit1=(r>=rt)&(m1>=mt);pred=np.where(commit1,p1.argmax(1),comb.argmax(1));commit2=commit1|((r>=rt*.85)&(m2>=mt*.8));correct=(pred==yy)
            utility=np.mean(np.where(commit2,np.where(correct,1.,-3.),-.05))
            z=(utility,rt,mt,float(correct[commit2].mean()) if commit2.any() else 0.,float((~commit2).mean()))
            if best is None or z[0]>best[0]:best=z
    return clf,{'utility':best[0],'reliability_threshold':best[1],'margin_threshold':best[2],'committed_accuracy':best[3],'unknown_rate':best[4],'calibration_n':len(yy),'initial_error_rate':float(1-target.mean())}

def decide(clf,rt,mt,p1,p2):
    X=rel_features(p1,p2);r=clf.predict_proba(X)[:,1];c=.5*(p1+p2);c1=(r>=rt)&(margin(p1)>=mt);c2=(r>=rt*.85)&(margin(c)>=mt*.8);commit=c1|c2;pred=np.where(c1,p1.argmax(1),c.argmax(1));return pred,commit,r

def run(seed=35400):
    model,dev=train_temporal(seed);clf,cal=calibration(model,dev,seed+500);rt=cal['reliability_threshold'];mt=cal['margin_threshold']
    # Resolvable hostile conditions.
    items=[]
    actors=d.base.ACTORS[:3];objects=d.base.OBJECTS[:3];voices=['en-wi','en-uk-rp']
    for ai,a in enumerate(actors):
      for yi,act in enumerate(d.base.ACTIONS):
       for oi,obj in enumerate(objects):
        distract=d.base.ACTIONS[(yi+2+oi)%len(d.base.ACTIONS)]
        specs=[
          ('extreme_voice',a,act,obj,voices[(ai+oi)%2],85 if oi%2==0 else 255,25 if ai%2==0 else 80,d.TRAIN_TEMPLATES[0],2),
          ('long_filler',a,act,obj,'en-uk-rp',205,61,LONG_TEMPLATE,1),
          ('postposed',a,act,obj,'en-wi',125,43,POST_TEMPLATE,1),
          ('distractor_before',a,act,obj,'en-uk-rp',175,55,f'although someone {distract} nothing, '+'{actor} {action} the {object} now',1),
          ('distractor_after',a,act,obj,'en-wi',165,55,'{actor} {action} the {object} now, while someone '+distract+' nothing',1),
          ('strong_noise',a,act,obj,'en-wi',215,70,d.TRAIN_TEMPLATES[0],3),
        ]
        for j,z in enumerate(specs):items.append((z,yi,seed+ai*10000+yi*1000+oi*100+j))
    f1=[];f2=[];ys=[];conds=[]
    for (cond,a,act,obj,v,sp,p,tmpl,strength),y,s0 in items:
        f1.append(custom_feature(a,act,obj,v,sp,p,tmpl,s0,strength))
        # Independent second view uses a different source/template, not the same corrupted lineage.
        f2.append(custom_feature(a,act,obj,'en-uk-north' if v!='en-uk-north' else 'en-sc',185,49,CAL_TEMPLATE,s0+9999,1))
        ys.append(y);conds.append(cond)
    p1=probs(model,f1);p2=probs(model,f2);pred,commit,rel=decide(clf,rt,mt,p1,p2);ys=np.asarray(ys)
    by={}
    for cond in sorted(set(conds)):
        ix=np.asarray([c==cond for c in conds]);by[cond]={'correct_committed':float(np.mean((pred[ix]==ys[ix])&commit[ix])),'commit_rate':float(commit[ix].mean()),'accuracy_when_committed':float((pred[ix][commit[ix]]==ys[ix][commit[ix]]).mean()) if commit[ix].any() else 0.,'raw_first_accuracy':float((p1[ix].argmax(1)==ys[ix]).mean()),'two_view_accuracy':float((.5*(p1[ix]+p2[ix])).argmax(1).astype(int).reshape(-1).shape[0] and ((.5*(p1[ix]+p2[ix])).argmax(1)==ys[ix]).mean())}
    # True no-unique-answer mixtures. Two independent mixture sources contain the
    # same pair but different voices/templates. No ambiguity label is supplied to
    # the learned reliability model.
    af1=[];af2=[]
    pairs=[]
    for yi in range(len(d.base.ACTIONS)):
      yj=(yi+1)%len(d.base.ACTIONS);a=actors[yi%len(actors)];obj=objects[(yi*2)%len(objects)]
      for rep in range(20):
        t1=d.TRAIN_TEMPLATES[0].format(actor=a,action=d.base.ACTIONS[yi],object=obj);t2=d.TRAIN_TEMPLATES[0].format(actor=a,action=d.base.ACTIONS[yj],object=obj)
        af1.append(mix_feature(t1,t2,'en-wi','en-uk-rp',125,205,45,70,seed+900000+yi*100+rep))
        q1=LONG_TEMPLATE.format(actor=a,action=d.base.ACTIONS[yi],object=obj);q2=POST_TEMPLATE.format(actor=a,action=d.base.ACTIONS[yj],object=obj)
        af2.append(mix_feature(q1,q2,'en-sc','en-uk-north',185,155,55,50,seed+910000+yi*100+rep));pairs.append((yi,yj))
    ap1=probs(model,af1);ap2=probs(model,af2);apred,acommit,arel=decide(clf,rt,mt,ap1,ap2)
    ambiguous={'unknown_rate':float((~acommit).mean()),'commit_rate':float(acommit.mean()),'mean_reliability':float(arel.mean()),'pair_member_commit_rate':float(np.mean([apred[i] in pairs[i] for i in range(len(pairs))]))}
    # Same-lineage misinformation: five repetitions of one wrong acoustic claim
    # versus one independent correct grounded observation. Provenance grouping
    # counts the repeated lineage once.
    naive=[];grouped=[]
    for yi,act in enumerate(d.base.ACTIONS):
      w=(yi+3)%len(d.base.ACTIONS);a=actors[yi%3];obj=objects[yi%3]
      wrong=custom_feature(a,d.base.ACTIONS[w],obj,'en-wi',175,55,d.TRAIN_TEMPLATES[0],seed+930000+yi,1)
      right=custom_feature(a,act,obj,'en-uk-rp',185,55,CAL_TEMPLATE,seed+940000+yi,1)
      pw=probs(model,[wrong])[0];pr=probs(model,[right])[0];naive.append(int(((5*pw+pr)/6).argmax()==yi));grouped.append(int(((pw+pr)/2).argmax()==yi))
    provenance={'naive_repeated_source_recovery':float(np.mean(naive)),'source_grouped_recovery':float(np.mean(grouped))}
    out={'seed':seed,'calibration':cal,'resolvable':by,'ambiguous':ambiguous,'provenance':provenance,'boundary':'REFERENCE_ONLY non-transformer temporal-PAM epistemic challenge. Reliability is trained only from delayed grounded correctness of difficult developmental observations. No ambiguity/corruption label, transcript, token, word/phoneme/chunk boundary, VAD, ASR, attention/transformer, or LLM enters cognition. Ambiguous mixture and source-lineage identities are evaluator-only qualification metadata.'}
    (OUT/f'R32_TEMPORAL_EPISTEMIC_CHALLENGE_SEED_{seed}.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));return out

if __name__=='__main__':run(int(sys.argv[1]) if len(sys.argv)>1 else 35400)
