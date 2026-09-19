from pathlib import Path
import json,subprocess,time
R=Path('/mnt/data/r32_epistemic')

def running(pat):
 q=subprocess.run(['pgrep','-f',pat],stdout=subprocess.PIPE,text=True);return any(x.strip().isdigit() for x in q.stdout.split())
def atomic(p,o):
 t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(o,indent=2,sort_keys=True));t.replace(p)
def flatten(obj,p=()):
 out={}
 if isinstance(obj,dict):
  for k,v in obj.items():out.update(flatten(v,p+(str(k),)))
 elif isinstance(obj,(int,float)) and not isinstance(obj,bool):out[p]=float(obj)
 return out
def aggregate(rows):
 bs={}
 for x in rows:
  for k,v in flatten(x).items():bs.setdefault(k,[]).append(v)
 out={}
 for k,v in bs.items():
  if len(v)==len(rows):
   cur=out
   for q in k[:-1]:cur=cur.setdefault(q,{})
   cur[k[-1]]={'mean':sum(v)/len(v),'min':min(v),'max':max(v),'n':len(v)}
 return out
status={}
# Segmental
p=R/'R32_TTS_SEGMENTAL_RECURRENT_PAM_REPLICATION_REFERENCE_ONLY.json';seeds=sorted(R.glob('R32_SEGMENTAL_PAM_SEED_35*.json'))
if not p.exists() and not running('r32_segmental_replicate.py') and seeds:
 rows=[]
 for x in seeds:
  try:rows.append(json.loads(x.read_text()))
  except:pass
 if rows:atomic(p,{'seeds':[x.get('seed') for x in rows],'n':len(rows),'aggregate':aggregate(rows),'partial':True,'boundary':'REFERENCE_ONLY partial recovery; run process ended before planned seed count.'})
status['segmental']={'running':running('r32_segmental_replicate.py'),'seeds':len(seeds),'summary':p.exists()}
# Elastic
p=R/'R32_TTS_ELASTIC_TEMPORAL_PAM_REFERENCE_ONLY.json';seeds=sorted(R.glob('R32_ELASTIC_TEMPORAL_PAM_SEED_*.json'))
if not p.exists() and not running('r32_tts_elastic_temporal_pam.py') and seeds:
 rows=[]
 for x in seeds:
  try:rows.append(json.loads(x.read_text()))
  except:pass
 if rows:
  routes=list(rows[0].get('hard_mean',{}));agg={k:{'hard_mean':sum(z['hard_mean'][k] for z in rows)/len(rows)} for k in routes};atomic(p,{'aggregate':agg,'rows':rows,'partial':True,'boundary':'REFERENCE_ONLY partial recovery.'})
status['elastic']={'running':running('r32_tts_elastic_temporal_pam.py'),'seeds':len(seeds),'summary':p.exists()}
# Epistemic
p=R/'R32_EPISTEMIC_EQUIVALENCE_REFERENCE_ONLY.json';seeds=sorted(R.glob('R32_EPISTEMIC_EQUIVALENCE_SEED_*.json'))
if not p.exists() and not running('r32_epistemic_equivalence.py') and seeds:
 rows=[]
 for x in seeds:
  try:rows.append(json.loads(x.read_text()))
  except:pass
 if rows:
  pols=rows[0]['policies'].keys();agg={}
  for pol in pols:
   agg[pol]={}
   for cond in rows[0]['policies'][pol]:
    agg[pol][cond]={k:sum(z['policies'][pol][cond][k] for z in rows)/len(rows) for k in rows[0]['policies'][pol][cond]}
  atomic(p,{'aggregate':agg,'rows':rows,'partial':True,'boundary':'REFERENCE_ONLY partial recovery.'})
status['epistemic']={'running':running('r32_epistemic_equivalence.py'),'seeds':len(seeds),'summary':p.exists()}
atomic(R/'R32_RESCUE_STATUS.json',status)
