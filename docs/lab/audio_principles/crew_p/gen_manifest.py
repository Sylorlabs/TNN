#!/usr/bin/env python3
"""Generate the FROZEN test manifest for Crew P (audio principles).

Deterministic, zero RNG. Writes manifest_p.json with:
  - 4 main batteries (pitchrel/abs, env, rhy) + P-R3 (hf): analytic labels
  - P-R4: 40 kid segments, labels from frozen analyzer (analyze.py) on the
    segment bytes (computed in-memory; no test WAV file is written here)
  - P-R5: 40 inventory unit pairs, labels from frozen inventory table f0_med
  - P-R1: +1dB perturbation spec; dither subsets
All labels are fixed BEFORE any test WAV file exists.
"""
import json, math, os, sys, wave, struct, tempfile
import numpy as np

sys.path.insert(0, '/home/hatch/workspace/audio_round2/shared')
import analyze as AN

SR = 44100
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'manifest_p.json')

def tone(f0, dur, harms, env=None):
    n = int(SR * dur)
    x = np.zeros(n)
    for i in range(n):
        t = i / SR
        v = 0.0
        for h, a in enumerate(harms, start=1):
            v += a * math.sin(2 * math.pi * f0 * h * t)
        if env:
            v *= env(i / n)
        x[i] = v
    return x

def to_pcm16(x):
    pk = np.abs(x).max() or 1.0
    g = 20000.0 / pk
    return np.clip(np.round(x * g), -32768, 32767).astype(np.int16)

POOLS = {'p0': [1.0, 0.30, 0.10], 'p1': [1.0, 0.15, 0.05, 0.02]}

def recipe_pitchrel(i):
    s = (i * 7) % 30
    f0a = 110.0 * 2 ** (s / 12.0)
    d = [4, -4, 3, -3, 2, -2][i % 6]
    f0b = f0a * 2 ** (d / 12.0)
    pool = 'p0' if i < 50 else 'p1'
    return dict(f0a=f0a, f0b=f0b, pool=pool,
                label='A' if f0a > f0b else 'B')

def recipe_pitchabs(i):
    k = (i * 7) % 24
    f0 = 110.0 * 2 ** (k / 12.0)
    pool = 'p0' if i < 30 else 'p1'
    return dict(k=k, f0=f0, pool=pool, label=k)

def recipe_env(i):
    cls = ['flat', 'rise', 'decay'][i % 3]
    pool = 'p0' if i < 30 else 'p1'
    return dict(cls=cls, f0=220.0, pool=pool, label=cls)

def recipe_rhy(i):
    # 6 eighth-notes at 90 BPM (8th=1/3 s); swing 1.5:1 (long 0.4, short 0.267)
    pool = 'p0' if i < 50 else 'p1'
    a_swung = (i % 4 < 2)   # i=0,1,4,5,... -> A swung; else B swung
    return dict(a_swung=a_swung, b_swung=not a_swung, pool=pool,
                label='A' if a_swung else 'B')

def recipe_hf(i):
    # A/B share base (220 Hz + lowpassed noise); differ only in 8-16 kHz noise ±6dB
    a_high = (i % 2 == 0)
    pool = 'p0' if i < 10 else 'p1'
    return dict(a_high=a_high, pool=pool, label='A' if a_high else 'B')

def main():
    man = {'batteries': {}, 'pr4': [], 'pr5': [], 'pr1': {}, 'dither': {}}
    # analytic batteries
    for name, n, fn in [('pitchrel', 100, recipe_pitchrel),
                        ('pitchabs', 60, recipe_pitchabs),
                        ('env', 60, recipe_env),
                        ('rhy', 100, recipe_rhy),
                        ('hf', 20, recipe_hf)]:
        qs = []
        for i in range(n):
            r = fn(i)
            r['qid'] = '%s:%04d' % (name, i)
            qs.append(r)
        man['batteries'][name] = qs
    # P-R4: 40 kid segments, analyzer labels (in-memory)
    kids = ['kida', 'kidb', 'kidc', 'kidc2', 'kidd', 'kide']
    # use 5 files x 8 segments
    kid_files = ['kida', 'kidb', 'kidc', 'kidd', 'kide']
    pr4 = []
    for fi, kf in enumerate(kid_files):
        w = wave.open('/home/hatch/workspace/v5work/%s.wav' % kf, 'rb')
        raw = w.readframes(w.getnframes()); w.close()
        x = np.frombuffer(raw, dtype=np.int16).astype(np.float64)
        for j in range(8):
            start = int(j * 4.0 * SR)
            seg = x[start:start + 2 * SR]
            # analyzer on in-memory segment via temp file (ephemeral, not a test WAV)
            pcm = np.clip(seg, -32768, 32767).astype(np.int16)
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tf:
                tpath = tf.name
            ww = wave.open(tpath, 'wb')
            ww.setnchannels(1); ww.setsampwidth(2); ww.setframerate(SR)
            ww.writeframes(pcm.tobytes()); ww.close()
            m, gates = AN.analyze(tpath)
            os.unlink(tpath)
            bits = [1 if m['frac_static'] >= 0.15 else 0,
                    1 if 0.7 <= m['hnr_db'] <= 12.0 else 0,
                    1 if 0.003 <= m['prosody'] <= 0.25 else 0]
            pr4.append(dict(qid='pr4:%04d' % (fi * 8 + j), kid=kf,
                            start_s=j * 4.0, label=''.join(map(str, bits)),
                            analyzer=dict(frac_static=m['frac_static'],
                                          hnr_db=m['hnr_db'], prosody=m['prosody'])))
    man['pr4'] = pr4
    # P-R5: 40 inventory pairs, labels from frozen table f0_med
    inv = json.load(open('/home/hatch/workspace/audio_round3/build_bf2/inventory_table.json'))
    v = [u for u in inv if u['voiced'] and 80 <= u['f0_med'] < 1200 and u['dur_ms'] >= 150]
    v.sort(key=lambda u: u['f0_med'])
    pr5 = []
    for i in range(40):
        a, b = v[i], v[i + 37]
        pr5.append(dict(qid='pr5:%04d' % i, uid_a=a['uid'], uid_b=b['uid'],
                        f0_a=a['f0_med'], f0_b=b['f0_med'],
                        label='A' if a['f0_med'] > b['f0_med'] else 'B'))
    man['pr5'] = pr5
    # P-R1: +1dB perturbation spec (20 per subtest, first 20 qids of each battery)
    man['pr1'] = dict(db=1.0, n_per_subtest=20,
                      qids={name: ['%s:%04d' % (name, i) for i in range(20)]
                            for name in ['pitchrel', 'pitchabs', 'env', 'rhy']})
    # dither subsets: 20 qids per subtest (deterministic: qids 20..39)
    man['dither'] = {name: ['%s:%04d' % (name, i) for i in range(20, 40)]
                     for name in ['pitchrel', 'pitchabs', 'env', 'rhy']}
    # dev-pool file SHAs (development renders, not test material)
    import hashlib
    devdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dev')
    dev_sha = {}
    for fn in sorted(os.listdir(devdir)):
        if fn.endswith('.wav'):
            h = hashlib.sha256(open(os.path.join(devdir, fn), 'rb').read()).hexdigest()
            dev_sha[fn] = h
    man['dev_pool_sha256'] = dev_sha
    json.dump(man, open(OUT, 'w'), indent=1)
    print('wrote', OUT, 'batteries:',
          {k: len(v) for k, v in man['batteries'].items()},
          'pr4:', len(pr4), 'pr5:', len(pr5))

if __name__ == '__main__':
    main()
