#!/usr/bin/env python3
"""Phase-3 full battery: resid3 + reemit63 (modes 10,11) for all 359 clips.
Keeps m3.v6 per clip; measures and deletes temp WAVs to save disk.
Writes results/phase3_battery.csv. Designed for xargs -P2 (one clip per call).
Usage: battery3.py <name>   (reads clip path from corpus_results_v6intake.csv)
"""
import struct, sys, os, csv, subprocess, math
import numpy as np

P2RUN = os.path.expanduser('~/workspace/exact_audio_replication/phase2/run/full_v6')
P3RUN = os.path.expanduser('~/workspace/exact_audio_replication/phase3/run/full_v3')
P3BUILD = os.path.expanduser('~/workspace/exact_audio_replication/phase3/build')
CSV = os.path.expanduser('~/workspace/exact_audio_replication/phase2/results/corpus_results_v6intake.csv')

def read_wav_samples(path):
    d = open(path, 'rb').read()
    off = 12
    while off + 8 < len(d):
        if d[off:off+4] == b'data':
            sz = struct.unpack('<I', d[off+4:off+8])[0]
            n = sz // 2
            return np.frombuffer(d[off+8:off+8+2*n], dtype='<i2').astype(np.float64)
        sz = struct.unpack('<I', d[off+4:off+8])[0]
        off += 8 + sz
    raise ValueError('no data: ' + path)

def main():
    name = sys.argv[1]
    rows = {r['name']: r for r in csv.DictReader(open(CSV))}
    r = rows[name]
    src = r['clip']
    p2d = os.path.join(P2RUN, name)
    wd = os.path.join(P3RUN, name)
    os.makedirs(wd, exist_ok=True)
    v6bin = os.path.join(p2d, 'm.v6bin')
    m3 = os.path.join(wd, 'm3.v6')
    # 1. hear
    cp = subprocess.run([os.path.join(P3BUILD, 'resid3'), v6bin, src, m3],
                        capture_output=True, text=True, timeout=600)
    # parse RESID3 lines for nres_rms, nimp, use_h, r2acc
    nres_rms, nimp, use_h, r2acc = float('nan'), -1, -1, 0.0
    for ln in cp.stdout.splitlines():
        if ln.startswith('RESID3 nres_rms='):
            nres_rms = float(ln.split('=')[1])
        if 'nimp=' in ln and ln.startswith('RESID3 n='):
            for tok in ln.split():
                if tok.startswith('nimp='): nimp = int(tok.split('=')[1])
                if tok.startswith('use_h='): use_h = int(tok.split('=')[1])
                if tok.startswith('r2acc='): r2acc = float(tok.split('=')[1])
    if cp.returncode != 0 or not os.path.exists(m3):
        print(f'{name}\tFAIL resid3 rc={cp.returncode} {cp.stdout[:200]} {cp.stderr[:200]}')
        return
    # 2. exact (mode 10) + cmp
    ex = os.path.join(wd, 'exact3.wav')
    subprocess.run([os.path.join(P3BUILD, 'reemit63'), m3, '10', ex],
                   capture_output=True, timeout=600)
    cpr = subprocess.run(['cmp', src, ex], capture_output=True)
    byte_ident = (cpr.returncode == 0)
    os.remove(ex)
    # 3. semantic (mode 11) + metrics
    sm = os.path.join(wd, 'sem3.wav')
    subprocess.run([os.path.join(P3BUILD, 'reemit63'), m3, '11', sm],
                   capture_output=True, timeout=600)
    x = read_wav_samples(src); y = read_wav_samples(sm)
    n = min(len(x), len(y)); x, y = x[:n], y[:n]
    e = y - x
    sem_rms = float(np.sqrt((e**2).mean()))
    sem_maxd = float(np.abs(e).max())
    xm, ym = x - x.mean(), y - y.mean()
    sem_corr = float((xm*ym).sum() / math.sqrt((xm**2).sum()*(ym**2).sum() + 1e-30))
    fsize = os.path.getsize(m3)
    # HF band check (12k+ excess)
    def bandfrac(s, sr, lo, hi):
        w = np.hanning(len(s)); X = np.abs(np.fft.rfft(s*w))**2
        fr = np.fft.rfftfreq(len(s), 1.0/sr)
        return X[(fr>=lo)&(fr<hi)].sum()/(X.sum()+1e-30)
    sr = 44100
    hf12_src = bandfrac(x, sr, 12000, 16000); hf12_sem = bandfrac(y, sr, 12000, 16000)
    hf16_src = bandfrac(x, sr, 16000, sr/2); hf16_sem = bandfrac(y, sr, 16000, sr/2)
    os.remove(sm)
    print(f'{name}\tOK\tbyte_ident={byte_ident}\tsem_rms={sem_rms:.2f}\tsem_corr={sem_corr:.4f}\t'
          f'sem_maxd={sem_maxd:.0f}\tnres_rms={nres_rms:.2f}\tnimp={nimp}\tuse_h={use_h}\t'
          f'r2acc={r2acc:.3f}\tfsize={fsize}\thf12x={hf12_sem/(hf12_src+1e-30):.3f}\thf16x={hf16_sem/(hf16_src+1e-30):.3f}')

if __name__ == '__main__':
    main()
