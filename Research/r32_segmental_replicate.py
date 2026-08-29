from __future__ import annotations
import importlib.util, json, traceback, sys, time
from pathlib import Path

ROOT = Path('/mnt/data/r32_epistemic')
SRC = ROOT / 'r32_tts_segmental_pam.py'
LOG = ROOT / 'R32_SEGMENTAL_REPLICATION_TRAINING.log'

spec = importlib.util.spec_from_file_location('segmod', SRC)
if spec is None or spec.loader is None:
    raise RuntimeError(f'Cannot import {SRC}')
mod = importlib.util.module_from_spec(spec)
sys.modules['segmod'] = mod
spec.loader.exec_module(mod)

if not hasattr(mod, 'run'):
    raise RuntimeError('r32_tts_segmental_pam.py has no run(seed) function')

def atomic_json(path: Path, obj) -> None:
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(obj, indent=2, sort_keys=True))
    tmp.replace(path)

all_rows=[]
for seed in range(35001, 35005):
    outp = ROOT / f'R32_SEGMENTAL_PAM_SEED_{seed}.json'
    if outp.exists():
        try:
            row=json.loads(outp.read_text())
            all_rows.append(row)
            with LOG.open('a') as f: f.write(f'SKIP_EXISTING {seed}\n')
            continue
        except Exception:
            pass
    t=time.time()
    try:
        row=mod.run(seed)
        if not isinstance(row, dict):
            row={'seed':seed,'result':row}
        row.setdefault('seed',seed)
        row['elapsed_seconds']=time.time()-t
        atomic_json(outp,row)
        all_rows.append(row)
        with LOG.open('a') as f:
            f.write(f'DONE {seed} seconds={row["elapsed_seconds"]:.3f}\n')
            f.flush()
    except Exception as e:
        err={'seed':seed,'error':repr(e),'traceback':traceback.format_exc(),'elapsed_seconds':time.time()-t}
        atomic_json(ROOT / f'R32_SEGMENTAL_PAM_SEED_{seed}_ERROR.json',err)
        with LOG.open('a') as f:
            f.write(f'ERROR {seed} {repr(e)}\n{err["traceback"]}\n')
            f.flush()
        raise

# Generic recursive numeric aggregation keyed by route/condition metrics.
def collect_numeric(rows):
    buckets={}
    def walk(obj,prefix=()):
        if isinstance(obj,dict):
            for k,v in obj.items():
                if k in {'seed','elapsed_seconds'}: continue
                walk(v,prefix+(str(k),))
        elif isinstance(obj,(int,float)) and not isinstance(obj,bool):
            buckets.setdefault(prefix,[]).append(float(obj))
    for r in rows: walk(r)
    agg={}
    for p,vals in buckets.items():
        if len(vals)==len(rows):
            cur=agg
            for key in p[:-1]: cur=cur.setdefault(key,{})
            cur[p[-1]]={'mean':sum(vals)/len(vals),'min':min(vals),'max':max(vals),'n':len(vals)}
    return agg

summary={'seeds':[r.get('seed') for r in all_rows], 'n':len(all_rows), 'aggregate':collect_numeric(all_rows),
         'boundary':'REFERENCE_ONLY replication of non-transformer temporal vs learner-gated segmental PAM on raw TTS waveforms. No transcript/word/phoneme/chunk boundary/VAD/ASR/tokenizer/transformer/LLM enters learner cognition.'}
atomic_json(ROOT/'R32_TTS_SEGMENTAL_RECURRENT_PAM_REPLICATION_REFERENCE_ONLY.json',summary)
print(json.dumps(summary,indent=2))
