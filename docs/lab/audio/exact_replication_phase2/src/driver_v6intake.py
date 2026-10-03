#!/usr/bin/env python3
"""Phase-2 exact-replication driver: hear -> v5bin -> v6 -> emit10/emit11 -> cmp+measure.
Usage: driver.py <clip_list.txt> <outdir> [--jobs N]
clip_list.txt: one wav path per line (absolute).
Writes results.jsonl in outdir.
"""
import sys, os, subprocess, json, struct, hashlib
import numpy as np
from concurrent.futures import ThreadPoolExecutor

P2 = os.path.expanduser('~/workspace/exact_audio_replication/phase2')
SRC_V6 = os.path.expanduser('~/workspace/exact_audio_replication/intake_v6')
RAWBYTE = os.path.expanduser('~/workspace/rawbyte_longmem')
RESID = os.path.join(P2, 'build', 'resid')
REEMIT6 = os.path.join(P2, 'build', 'reemit6')
CORPUS = os.path.expanduser('~/workspace/audio_longhorizon/corpus')

# seal manifest for verification
SEAL = {}
try:
    man = json.load(open(os.path.join(CORPUS, 'SEAL_MANIFEST.json')))
    for e in man:
        SEAL[e['path']] = e['sha256']
except Exception as ex:
    print('seal manifest load failed:', ex, file=sys.stderr)

def read_wav(path):
    d = open(path, 'rb').read()
    off = 12
    while off + 8 < len(d):
        if d[off:off+4] == b'data':
            sz = struct.unpack('<I', d[off+4:off+8])[0]
            n = sz // 2
            return np.frombuffer(d[off+8:off+8+2*n], dtype='<i2').astype(np.float64)
        sz = struct.unpack('<I', d[off+4:off+8])[0]
        off += 8 + sz
    raise ValueError('no data')

def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    return r.returncode, r.stdout, r.stderr

def process(clip):
    name = os.path.splitext(os.path.basename(clip))[0]
    wd = os.path.join(OUTDIR, name)
    os.makedirs(wd, exist_ok=True)
    res = {'clip': clip, 'name': name}
    try:
        # seal check (manifest paths are 'corpus/...' relative to audio_longhorizon/)
        rel = 'corpus/' + os.path.relpath(clip, CORPUS)
        h = hashlib.sha256(open(clip, 'rb').read()).hexdigest()
        res['seal_sha'] = h
        res['seal_match'] = (SEAL.get(rel) == h)
        # 1. hear
        npz = os.path.join(wd, 'm.npz')
        env = dict(os.environ, PYTHONPATH=RAWBYTE)
        rc, out, err = run([sys.executable, os.path.join(SRC_V6, 'proto5g.py'),
                            'hear', clip, npz], env=env)
        if rc != 0:
            res['stage'] = 'hear'; res['err'] = err[-500:]; return res
        res['hear_log'] = out.strip().split('\n')
        # 2. npz -> RBLMEMv6 bin (repaired intake)
        v6b = os.path.join(wd, 'm.v6bin')
        rc, out, err = run([sys.executable, os.path.join(SRC_V6, 'npz_to_bin.py'),
                            npz, v6b], env=env)
        if rc != 0:
            res['stage'] = 'npz_to_bin'; res['err'] = err[-500:]; return res
        # 3. resid -> v6
        v6 = os.path.join(wd, 'm.v6')
        rc, out, err = run([RESID, v6b, clip, v6])
        res['resid_log'] = out.strip().split('\n')
        if rc != 0:
            res['stage'] = 'resid'; res['err'] = err[-500:]; return res
        # 4. exact emit (twice for determinism)
        ex1 = os.path.join(wd, 'exact.wav')
        ex2 = os.path.join(wd, 'exact2.wav')
        rc, out, err = run([REEMIT6, v6, '10', ex1])
        if rc != 0:
            res['stage'] = 'emit10'; res['err'] = err[-500:]; return res
        run([REEMIT6, v6, '10', ex2])
        # cmp full file
        d1 = open(clip, 'rb').read()
        d2 = open(ex1, 'rb').read()
        res['byte_identical'] = (d1 == d2)
        res['size_match'] = (len(d1) == len(d2))
        if d1 != d2:
            # find first diff
            for i, (a, b) in enumerate(zip(d1, d2)):
                if a != b:
                    res['first_diff_at'] = i
                    break
        d3 = open(ex2, 'rb').read()
        res['deterministic'] = (d2 == d3)
        # 5. semantic emit + measure
        sem = os.path.join(wd, 'sem.wav')
        rc, out, err = run([REEMIT6, v6, '11', sem])
        if rc != 0:
            res['stage'] = 'emit11'; res['err'] = err[-500:]; return res
        x = read_wav(clip); y = read_wav(sem)
        n = min(len(x), len(y))
        x, y = x[:n], y[:n]
        d = y - x
        res['sem_rms'] = float(np.sqrt((d**2).mean()))
        res['sem_maxd'] = float(np.abs(d).max())
        xm, ym = x - x.mean(), y - y.mean()
        den = np.sqrt((xm**2).sum() * (ym**2).sum()) + 1e-12
        res['sem_corr'] = float((xm*ym).sum() / den)
        res['stage'] = 'done'
    except Exception as ex:
        res['stage'] = 'exception'; res['err'] = repr(ex)[:500]
    return res

if __name__ == '__main__':
    clips = [l.strip() for l in open(sys.argv[1]) if l.strip()]
    OUTDIR = sys.argv[2]
    jobs = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    os.makedirs(OUTDIR, exist_ok=True)
    out_path = os.path.join(OUTDIR, 'results.jsonl')
    done_names = set()
    if os.path.exists(out_path):
        for l in open(out_path):
            try: done_names.add(json.loads(l)['name'])
            except: pass
    todo = [c for c in clips
            if os.path.splitext(os.path.basename(c))[0] not in done_names]
    print(f'{len(clips)} clips, {len(todo)} to do, {jobs} jobs', flush=True)
    with ThreadPoolExecutor(max_workers=jobs) as ex:
        for i, r in enumerate(ex.map(process, todo)):
            with open(out_path, 'a') as f:
                f.write(json.dumps(r) + '\n')
            bi = r.get('byte_identical')
            print(f"[{i+1}/{len(todo)}] {r['name']}: "
                  f"byte_identical={bi} sem_rms={r.get('sem_rms', -1):.1f} "
                  f"corr={r.get('sem_corr', -1):.4f} stage={r.get('stage')}",
                  flush=True)
    print('ALL DONE', flush=True)
