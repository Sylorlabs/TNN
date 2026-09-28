#!/usr/bin/env python3
"""Regenerate v6 with header-aware resid, re-test exact (skips hear).
Usage: retest.py <clip_list> <rundir> [--jobs N]
Assumes <rundir>/<name>/m.v5bin exists. Updates results.jsonl (fresh)."""
import sys, os, subprocess, json, struct, hashlib
import numpy as np
from concurrent.futures import ThreadPoolExecutor

P2 = os.path.expanduser('~/workspace/exact_audio_replication/phase2')
RESID = os.path.join(P2, 'build', 'resid')
REEMIT6 = os.path.join(P2, 'build', 'reemit6')
CORPUS = os.path.expanduser('~/workspace/audio_longhorizon/corpus')
SEAL = {}
man = json.load(open(os.path.join(CORPUS, 'SEAL_MANIFEST.json')))
for e in man:
    SEAL[e['path']] = e['sha256']

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
        rel = 'corpus/' + os.path.relpath(clip, CORPUS)
        h = hashlib.sha256(open(clip, 'rb').read()).hexdigest()
        res['seal_sha'] = h
        res['seal_match'] = (SEAL.get(rel) == h)
        v5b = os.path.join(wd, 'm.v5bin')
        if not os.path.exists(v5b):
            res['stage'] = 'no_v5bin'; return res
        v6 = os.path.join(wd, 'm.v6')
        rc, out, err = run([RESID, v5b, clip, v6])
        res['resid_log'] = out.strip().split('\n')
        if rc != 0:
            res['stage'] = 'resid'; res['err'] = err[-500:]; return res
        ex1 = os.path.join(wd, 'exact.wav')
        ex2 = os.path.join(wd, 'exact2.wav')
        rc, out, err = run([REEMIT6, v6, '10', ex1])
        if rc != 0:
            res['stage'] = 'emit10'; res['err'] = err[-500:]; return res
        run([REEMIT6, v6, '10', ex2])
        d1 = open(clip, 'rb').read()
        d2 = open(ex1, 'rb').read()
        res['byte_identical'] = (d1 == d2)
        res['size_match'] = (len(d1) == len(d2))
        if d1 != d2:
            for i, (a, b) in enumerate(zip(d1, d2)):
                if a != b:
                    res['first_diff_at'] = i
                    break
            # check PCM-only identity
            x = read_wav(clip); y = read_wav(ex1)
            res['pcm_identical'] = bool((x == y).all())
        d3 = open(ex2, 'rb').read()
        res['deterministic'] = (d2 == d3)
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
    jobs = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    os.makedirs(OUTDIR, exist_ok=True)
    out_path = os.path.join(OUTDIR, 'results.jsonl')
    # fresh results (old format invalid)
    if os.path.exists(out_path):
        os.rename(out_path, out_path + '.oldfmt.bak')
    print(f'{len(clips)} clips, {jobs} jobs (retest, hear skipped)', flush=True)
    with ThreadPoolExecutor(max_workers=jobs) as ex:
        for i, r in enumerate(ex.map(process, clips)):
            with open(out_path, 'a') as f:
                f.write(json.dumps(r) + '\n')
            bi = r.get('byte_identical')
            print(f"[{i+1}/{len(clips)}] {r['name']}: byte_identical={bi} "
                  f"pcm_identical={r.get('pcm_identical')} stage={r.get('stage')}",
                  flush=True)
    print('ALL DONE', flush=True)
