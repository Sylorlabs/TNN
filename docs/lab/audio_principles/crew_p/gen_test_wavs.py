#!/usr/bin/env python3
"""Generate ALL test WAVs for Crew P from the frozen manifest.

Deterministic, zero RNG (LCG for noise). Reads manifest_p.json.
Writes to test_wavs/. DO NOT RUN before the manifest is committed.
"""
import json, math, os, wave
import numpy as np

SR = 44100
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'test_wavs')

def write_wav(path, x):
    pk = np.abs(x).max() or 1.0
    g = 20000.0 / pk
    xi = np.clip(np.round(x * g), -32768, 32767).astype(np.int16)
    w = wave.open(path, 'wb')
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(xi.tobytes()); w.close()

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

def lcg(n, seed):
    x = seed
    out = np.zeros(n)
    for i in range(n):
        x = (1103515245 * x + 12345) & 0x7fffffff
        out[i] = (x / 2 ** 30) - 1.0
    return out

def onepole(x, fc):
    a = math.exp(-2 * math.pi * fc / SR)
    y = np.zeros_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc = (1 - a) * x[i] + a * acc
        y[i] = acc
    return y

POOLS = {'p0': [1.0, 0.30, 0.10], 'p1': [1.0, 0.15, 0.05, 0.02]}

def gen_pitchrel(q):
    h = POOLS[q['pool']]
    a = tone(q['f0a'], 2.0, h)
    b = tone(q['f0b'], 2.0, h)
    return [(q['qid'] + '_A.wav', a), (q['qid'] + '_B.wav', b)]

def gen_pitchabs(q):
    h = POOLS[q['pool']]
    return [(q['qid'] + '.wav', tone(q['f0'], 2.0, h))]

def gen_env(q):
    h = POOLS[q['pool']]
    if q['cls'] == 'flat':
        x = tone(q['f0'], 2.0, h)
    elif q['cls'] == 'rise':
        x = tone(q['f0'], 2.0, h, env=lambda u: 10 ** ((-12.0 + 12.0 * u) / 20.0))
    else:
        x = tone(q['f0'], 2.0, h, env=lambda u: 10 ** ((0.0 - 12.0 * u) / 20.0))
    return [(q['qid'] + '.wav', x)]

def gen_rhy(q):
    bf = 660.0 if q['pool'] == 'p0' else 520.0
    def render(onsets):
        x = np.zeros(int(SR * 2.0))
        for t0 in onsets:
            s = int(t0 * SR)
            n = int(SR * 0.04)
            for i in range(n):
                if s + i < len(x):
                    e = math.sin(math.pi * i / n) ** 2
                    x[s + i] += e * math.sin(2 * math.pi * bf * i / SR)
        return x
    sw = [0, 0.4, 0.667, 1.067, 1.333, 1.733]
    ev = [0, 0.333, 0.667, 1.0, 1.333, 1.667]
    a = render(sw if q['a_swung'] else ev)
    b = render(sw if q['b_swung'] else ev)
    return [(q['qid'] + '_A.wav', a), (q['qid'] + '_B.wav', b)]

def gen_hf(q):
    h = POOLS[q['pool']]
    n = int(SR * 2.0)
    base = tone(220.0, 2.0, h)
    nz = lcg(n, 12345)
    lp = onepole(nz, 2000.0)
    hnz = lcg(n, 67890)
    hf = hnz - onepole(hnz, 8000.0)
    base /= (np.abs(base).max() or 1)
    lp /= (np.abs(lp).max() or 1)
    hf /= (np.abs(hf).max() or 1)
    hi = base + 0.3 * lp + 0.2 * hf
    lo = base + 0.3 * lp + 0.1 * hf
    a = hi if q['a_high'] else lo
    b = lo if q['a_high'] else hi
    return [(q['qid'] + '_A.wav', a), (q['qid'] + '_B.wav', b)]

def gen_pr4(q):
    w = wave.open('/home/hatch/workspace/v5work/%s.wav' % q['kid'], 'rb')
    raw = w.readframes(w.getnframes()); w.close()
    x = np.frombuffer(raw, dtype=np.int16).astype(np.float64)
    start = int(q['start_s'] * SR)
    seg = x[start:start + 2 * SR]
    return [(q['qid'] + '.wav', seg)]

def gen_pr5(q, inv_by_uid):
    ua = inv_by_uid[q['uid_a']]
    ub = inv_by_uid[q['uid_b']]
    def clip(u):
        w = wave.open('/home/hatch/workspace/v5work/%s.wav' % u['tag'], 'rb')
        raw = w.readframes(w.getnframes()); w.close()
        x = np.frombuffer(raw, dtype=np.int16).astype(np.float64)
        seg = x[u['start']:u['end']]
        # center in 2 s
        out = np.zeros(int(SR * 2.0))
        s = (len(out) - len(seg)) // 2
        out[s:s + len(seg)] = seg
        return out
    return [(q['qid'] + '_A.wav', clip(ua)), (q['qid'] + '_B.wav', clip(ub))]

def main():
    import hashlib
    man = json.load(open(os.path.join(HERE, 'manifest_p.json')))
    inv = json.load(open('/home/hatch/workspace/audio_round3/build_bf2/inventory_table.json'))
    inv_by_uid = {u['uid']: u for u in inv}
    os.makedirs(OUT, exist_ok=True)
    files = []
    gen = {'pitchrel': gen_pitchrel, 'pitchabs': gen_pitchabs, 'env': gen_env,
           'rhy': gen_rhy, 'hf': gen_hf}
    for name, qs in man['batteries'].items():
        for q in qs:
            for fn, x in gen[name](q):
                p = os.path.join(OUT, fn)
                write_wav(p, x)
                files.append(fn)
    for q in man['pr4']:
        for fn, x in gen_pr4(q):
            p = os.path.join(OUT, fn)
            write_wav(p, x)
            files.append(fn)
    for q in man['pr5']:
        for fn, x in gen_pr5(q, inv_by_uid):
            p = os.path.join(OUT, fn)
            write_wav(p, x)
            files.append(fn)
    # sealed SHA manifest
    sha = {}
    for fn in sorted(files):
        h = hashlib.sha256(open(os.path.join(OUT, fn), 'rb').read()).hexdigest()
        sha[fn] = h
    json.dump(sha, open(os.path.join(HERE, 'test_wavs_sha256.json'), 'w'), indent=1)
    print('wrote %d test wavs' % len(files))

if __name__ == '__main__':
    main()
