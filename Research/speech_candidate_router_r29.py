#!/usr/bin/env python3
"""Learned target-blind reliability router for the R29 acoustic core.

CTC is the default/core inference path. The mutable router may select the
attention candidate only from internal evidence learned during development.
No transcript is consulted at test-time selection.
"""
import argparse,json,math
from pathlib import Path
import numpy as np, torch
import torch.nn.functional as F
from sklearn.ensemble import ExtraTreesClassifier
import speech_joint_core_r29 as j


def edit(a,b):return j.edit(a,b)

def attn_decode_conf(model,z,l,max_steps=20):
 dec=model.dec;mask=torch.arange(z.shape[1])[None,:]<l[:,None];pool=(z*mask[:,:,None]).sum(1)/l[:,None];h=torch.tanh(dec.init(pool));ctx=pool;a=mask.float()/l[:,None];tok=torch.full((len(z),),dec.C+1,dtype=torch.long);done=torch.zeros(len(z),dtype=torch.bool);out=[[] for _ in range(len(z))];logs=[[] for _ in range(len(z))]
 for _ in range(max_steps):
  o,h,ctx,a=dec.step(z,mask,h,ctx,tok,a);lp=F.log_softmax(o,1);tok=lp.argmax(1)
  for i,v in enumerate(tok.tolist()):
   if not done[i]:
    logs[i].append(float(lp[i,v]));
    if v==dec.C:done[i]=True
    else:out[i].append(v)
  if bool(done.all()):break
 return out,[float(np.mean(q)) if q else -20. for q in logs]

def signal_features(x,L):
 q=x[:L].numpy();d=np.diff(q);m=q.mean();s=q.std()+1e-8;k=float(np.mean(((q-m)/s)**4));spike=float(np.quantile(abs(d),.98)/(np.median(abs(d))+.02));return [L/200.,float(s),float(np.std(d)),k/10.,spike/10.]

def batch_candidates(model,rows,C,batch=48):
 records=[]
 for st in range(0,len(rows),batch):
  rr=rows[st:st+batch];x,l,_,_,_,_=j.collate(rr,C)
  with torch.no_grad():
   z,ol=model.encode(x,l);ctlog=model.ctc(z);cp=j.ctc_greedy(ctlog,ol);ap,aconf=attn_decode_conf(model,z,ol,20);pool=model.pooled(z,ol);ll=F.softmax(model.length(pool),1);pp=torch.sigmoid(model.pres(pool));prob=F.softmax(ctlog,2)
  for i,q in enumerate(rr):
   T=int(ol[i]);p=prob[i,:T];blank=float(p[:,0].mean());ent=float((-(p*(p+1e-9).log()).sum(1)).mean());mx=float(p[:,1:].max(1).values.mean());predlen=int(ll[i].argmax());lenconf=float(ll[i].max());lenent=float(-(ll[i]*(ll[i]+1e-9).log()).sum());
   a=ap[i];c=cp[i]
   def presence_score(seq):
    target=np.zeros(C);target[list(set(seq))]=1 if seq else 0;pr=pp[i].numpy();return float(np.mean(target*pr+(1-target)*(1-pr)))
   f=[len(a),len(c),predlen,abs(len(a)-predlen),abs(len(c)-predlen),edit(a,c),aconf[i],blank,ent,mx,lenconf,lenent,presence_score(a),presence_score(c)]+signal_features(x[i],int(l[i]))
   records.append({'features':f,'attn':a,'ctc':c,'truth':q.y.tolist()})
 return records

def condition(world,seed,name,n,speakers):
 if name=='hard':return j.make_rows(world,n,seed,'hard',(2,8),speakers)
 if name=='silence':return j.make_rows(world,n,seed,'hard',(2,8),speakers,.42,0)
 if name=='endpoint':return j.make_rows(world,n,seed,'hard',(2,8),speakers,.10,.28)
 if name=='severe':return j.make_rows(world,n,seed,'severe',(2,8),speakers)
 if name=='long':return j.make_rows(world,n,seed,'hard',(8,10),speakers)
 if name=='severe_long':return j.make_rows(world,n,seed,'severe',(8,10),speakers,.20,.10)
 raise ValueError(name)

def summarize(pred,records):
 ed=tok=ex=0
 for p,r in zip(pred,records):y=r['truth'];d=edit(p,y);ed+=d;tok+=len(y);ex+=p==y
 return {'exact':ex/len(records),'token_accuracy':1-ed/max(1,tok),'mean_edit':ed/len(records)}

def run(seed,checkpoint,dev_each=350,test_each=300):
 C=16;w=j.AcousticWorld(seed,C,30,False);m=j.JointPAM(C);ck=torch.load(checkpoint,map_location='cpu',weights_only=False);m.load_state_dict(ck['state_dict']);conds=['hard','silence','endpoint','severe','long','severe_long']
 dev=[]
 for k,nm in enumerate(conds):dev+=batch_candidates(m,condition(w,seed+10000+k*1000,nm,dev_each,[14,15,16,17]),C)
 X=[];Y=[];ties=0
 for r in dev:
  da=edit(r['attn'],r['truth']);dc=edit(r['ctc'],r['truth'])
  if da==dc:ties+=1;continue
  X.append(r['features']);Y.append(int(dc<da))
 clf=ExtraTreesClassifier(n_estimators=240,min_samples_leaf=5,max_features=.8,class_weight='balanced',random_state=seed,n_jobs=1).fit(X,Y)
 tests={};importance=clf.feature_importances_.tolist();names=['attn_len','ctc_len','pred_len','attn_len_gap','ctc_len_gap','candidate_edit','attn_logprob','ctc_blank','ctc_entropy','ctc_nonblank_max','length_conf','length_entropy','attn_presence','ctc_presence','wave_len','wave_std','derivative_std','kurtosis','spike_ratio']
 for k,nm in enumerate(conds):
  rec=batch_candidates(m,condition(w,seed+50000+k*1000,nm,test_each,[18,19,20,21]),C);pro=clf.predict_proba([r['features'] for r in rec]);choose=[];correct=0;non_tie=0
  for r,p in zip(rec,pro):
   # CTC remains default unless learned evidence favors attention confidently.
   use_ctc=bool(p[1]>=.52);choose.append(r['ctc'] if use_ctc else r['attn']);da=edit(r['attn'],r['truth']);dc=edit(r['ctc'],r['truth'])
   if da!=dc:correct+=int((dc<da)==use_ctc);non_tie+=1
  tests[nm]={'ctc':summarize([r['ctc'] for r in rec],rec),'attention':summarize([r['attn'] for r in rec],rec),'learned_router':summarize(choose,rec),'oracle_control':summarize([min([r['attn'],r['ctc']],key=lambda q:edit(q,r['truth'])) for r in rec],rec),'selection_accuracy_non_ties':correct/max(1,non_tie),'ctc_selection_rate':float(np.mean(pro[:,1]>=.52))}
 return {'seed':seed,'checkpoint_epoch':ck.get('epoch'),'development_examples':len(dev),'development_non_ties':len(Y),'development_ties':ties,'feature_importance':dict(sorted(zip(names,importance),key=lambda x:x[1],reverse=True)),'tests':tests,'decision':'CTC_CORE_DEFAULT_LEARNED_ATTENTION_OVERRIDE','claim_boundary':'Router learned on developmental consequences; selection uses internal evidence only at test. Python reference, no VAD/boundaries.'}

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--seed',type=int,required=True);ap.add_argument('--checkpoint',required=True);ap.add_argument('--out',required=True);ap.add_argument('--dev-each',type=int,default=350);ap.add_argument('--test-each',type=int,default=300);a=ap.parse_args();o=run(a.seed,a.checkpoint,a.dev_each,a.test_each);Path(a.out).parent.mkdir(parents=True,exist_ok=True);Path(a.out).write_text(json.dumps(o,indent=2));print(json.dumps(o,indent=2))
