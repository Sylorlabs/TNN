from pathlib import Path
import json,os,time
try: import psutil
except Exception: raise SystemExit(0)
ROOT=Path('/mnt/data/r32_epistemic')
targets=['r32_segmental_replicate.py','r32_tts_elastic_temporal_pam.py','r32_epistemic_equivalence.py','r32_epistemic_learned_models.py','r32_raw_waveform_multitimescale_pam.py','r32_integrated_life_250k.py']
rows=[]
for p in psutil.process_iter(['pid','cmdline','create_time','cpu_percent','memory_info']):
 try:
  cmd=p.info['cmdline'] or []
  hit=next((x for x in targets if any(os.path.basename(c)==x for c in cmd)),None)
  if not hit:continue
  p.cpu_percent(None);rows.append((p,hit))
 except Exception:pass
time.sleep(10)
out=[]
for p,hit in rows:
 try:
  cpu=p.cpu_percent(None);rss=p.memory_info().rss;elapsed=time.time()-p.create_time()
  logs=list(ROOT.glob('*SEGMENTAL*log')) if 'segmental' in hit else list(ROOT.glob(f'*{hit.split(".")[0]}*log'))
  newest=max((x.stat().st_mtime for x in logs),default=p.create_time());stale=time.time()-newest
  action='healthy'
  if elapsed>1800 and cpu<0.3 and stale>1800:
   p.terminate();action='terminated_stalled'
  out.append({'pid':p.pid,'script':hit,'cpu_10s':cpu,'rss':rss,'elapsed':elapsed,'log_stale':stale,'action':action})
 except Exception as e:out.append({'pid':getattr(p,'pid',-1),'script':hit,'error':repr(e)})
(ROOT/'R32_TASK_HEALTH.json').write_text(json.dumps({'at':time.time(),'rows':out},indent=2))
