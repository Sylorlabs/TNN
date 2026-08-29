from pathlib import Path
import json,subprocess,hashlib,os,time,shutil
r=Path('/mnt/data/r32_epistemic')
cur=json.loads((r/'R32_NATIVE_AUTHORITY_CURRENT.json').read_text()) if (r/'R32_NATIVE_AUTHORITY_CURRENT.json').exists() else {'status':'BLOCKED'}
out={'initial_status':cur}
z=r/'znc';src=r/'tnn_r32_epistemic_chunking.zag'
if cur.get('status')=='PASS' and z.exists() and src.exists():
 os.chmod(z,0o755);bins=[]
 for i in (1,2):
  b=r/f'tnn_r32_latest_native_{i}'
  q=subprocess.run([str(z),str(src),'-o',str(b)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=1200)
  item={'rc':q.returncode,'stdout':q.stdout.decode('utf-8','replace')[:5000],'stderr':q.stderr.decode('utf-8','replace')[:20000],'exists':b.exists()}
  if b.exists():item.update(size=b.stat().st_size,sha256=hashlib.sha256(b.read_bytes()).hexdigest());bins.append(b)
  out[f'compile_latest_{i}']=item
 if len(bins)==2:
  out['latest_deterministic_equal']=bins[0].read_bytes()==bins[1].read_bytes()
  runs=[]
  for j in range(3):
   q=subprocess.run([str(bins[0])],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=300)
   runs.append({'rc':q.returncode,'stdout':q.stdout.decode('utf-8','replace'),'stderr':q.stderr.decode('utf-8','replace')})
  out['runs']=runs;out['run_outputs_equal']=len({x['stdout'] for x in runs})==1 and len({x['stderr'] for x in runs})==1
  out['native_latest_pass']=out['latest_deterministic_equal'] and out['run_outputs_equal'] and all(x['rc']==0 for x in runs)
else:
 out['native_latest_pass']=False
 out['reason']='Initial authority gate did not pass or compiler/source missing.'
(r/'R32_NATIVE_LATEST_EVIDENCE.json').write_text(json.dumps(out,indent=2))
(r/('R32_NATIVE_LATEST_PASS.flag' if out['native_latest_pass'] else 'R32_NATIVE_LATEST_BLOCKED.flag')).write_text('1\n')
