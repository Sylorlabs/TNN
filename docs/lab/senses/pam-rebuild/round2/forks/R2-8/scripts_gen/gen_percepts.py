#!/usr/bin/env python3
"""R2-8 percept generator (test-harness glue, NOT in TNN decision path).

Runs the frozen pure-Zag sense binary on every fixture needed by the R2-8
battery and caches (judgment, confidence, margin, feature, ops) as JSON.

The percept itself is pure Zag (src/sense_r28.zag), zero RNG, deterministic.
This script is memoization only: the battery driver consumes the cache.
Determinism of the binary is verified separately (scripts_gen/verify_det.py).

Usage:
  python3 gen_percepts.py <chunk> <nchunks>   # writes percept_cache.<chunk>.json
  python3 gen_percepts.py merge               # merges into percept_cache.json
"""
import json, os, re, subprocess, sys

BASE = os.path.expanduser('~/workspace/tnn-lab/senses/pam-rebuild/round2')
FX = os.path.join(BASE, 'fixtures')
FORK = os.path.join(BASE, 'forks', 'R2-8')
BIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'work', 'sense_r28')
TASKS = {'colordisc': 'img', 'colorconst': 'img', 'shapetrans': 'img',
         'pitchdisc': 'pcm', 'timbredisc': 'pcm', 'motiondir': 'vid'}

def parse_out(out):
    d = {}
    for line in out.splitlines():
        if '=' in line and not line.startswith('debug_vec'):
            k, v = line.split('=', 1)
            d[k.strip()] = v.strip()
    if 'judgment' not in d:
        return {'judgment': '?', 'confidence': -1, 'margin': -1,
                'feature': -1, 'ops': -1}
    try:
        return {'judgment': d['judgment'],
                'confidence': int(d.get('confidence', -1)),
                'margin': int(d.get('margin', -1)),
                'feature': int(d.get('feature', -1)),
                'ops': int(d.get('ops', -1))}
    except ValueError:
        return {'judgment': '?', 'confidence': -1, 'margin': -1,
                'feature': -1, 'ops': -1}

def run_one(task, path):
    try:
        r = subprocess.run([BIN, task, path], capture_output=True,
                           text=True, timeout=600)
        return parse_out(r.stdout)
    except Exception:
        return {'judgment': '?', 'confidence': -1, 'margin': -1,
                'feature': -1, 'ops': -1}

def fixture_list():
    items = []
    comp = os.path.join(FX, 'r2q', 'companions')
    for task, ext in TASKS.items():
        idxs = set()
        for f in os.listdir(os.path.join(comp, task)):
            m = re.match(r'r2q_%s_(\d+)_([gpq]\d?)\.%s$' % (task, ext), f)
            if m:
                idxs.add(m.group(1))
        for idx in sorted(idxs):
            F = os.path.join(FX, 'r2a', 'adversarial',
                             'r2a_%s_%s.%s' % (task, idx, ext))
            items.append((task, F))
            for s in ['g', 'p1', 'p2', 'p3', 'q1', 'q2', 'q3']:
                items.append((task, os.path.join(
                    comp, task, 'r2q_%s_%s_%s.%s' % (task, idx, s, ext))))
    # recall set: independent source (S=g) + perturbations (Ps=p1..p3) for the
    # RECALL trials, where X = the R2A normal fixture (PREREG_R2-8 s3).
    rd = os.path.join(comp, 'recall')
    if os.path.isdir(rd):
        for f in sorted(os.listdir(rd)):
            m = re.match(r'r2q_recall_(shapetrans|timbredisc)_(\d+)_(g|p\d)\.(img|pcm)$', f)
            if m:
                items.append((m.group(1), os.path.join(rd, f)))
    # R2A normal fixtures used as X in the RECALL trials (PREREG_R2-8 s3:
    # "recall measured on the R2A normal fixtures of those tasks").
    # Paired by index with the r2q recall set: shapetrans 0..1007, timbredisc 0..719.
    for i in range(1008):
        items.append(('shapetrans', os.path.join(FX, 'r2n_shapetrans_%04d.img' % i)))
    for i in range(720):
        items.append(('timbredisc', os.path.join(FX, 'r2n_timbredisc_%04d.pcm' % i)))
    # 370 harness primary (B1/B2/B3)
    hd = os.path.expanduser('~/workspace/tnn-lab/senses/rebuild/harness/fixtures')
    hmap = [('t1_colordisc', 'colordisc', 'img'), ('t2_colorconst', 'colorconst', 'img'),
            ('t3_shapetrans', 'shapetrans', 'img'), ('t4_pitchdisc', 'pitchdisc', 'pcm'),
            ('t5_timbredisc', 'timbredisc', 'pcm'), ('t6_motiondir', 'motiondir', 'vid')]
    for sub, task, ext in hmap:
        pd = os.path.join(hd, sub, 'primary')
        for f in sorted(os.listdir(pd)):
            if f.endswith('.' + ext):
                items.append((task, os.path.join(pd, f)))
    # dedupe, stable order
    seen = set()
    out = []
    for t, p in items:
        k = t + '|' + p
        if k not in seen:
            seen.add(k)
            out.append((t, p))
    return out

def main():
    if len(sys.argv) == 2 and sys.argv[1] == 'merge':
        merged = {}
        for f in sorted(os.listdir('.')):
            if re.match(r'percept_cache\.\d+\.json$', f):
                merged.update(json.load(open(f)))
        json.dump(merged, open('percept_cache.json', 'w'), sort_keys=True)
        print('merged', len(merged), 'entries -> percept_cache.json')
        return
    chunk, nchunks = int(sys.argv[1]), int(sys.argv[2])
    items = fixture_list()
    mine = [it for i, it in enumerate(items) if i % nchunks == chunk]
    print('chunk %d/%d: %d fixtures' % (chunk, nchunks, len(mine)), flush=True)
    out = {}
    for i, (task, path) in enumerate(mine):
        out[task + '|' + path] = run_one(task, path)
        if (i + 1) % 50 == 0:
            print('chunk %d: %d/%d' % (chunk, i + 1, len(mine)), flush=True)
    json.dump(out, open('percept_cache.%d.json' % chunk, 'w'), sort_keys=True)
    print('chunk %d done: %d entries' % (chunk, len(out)), flush=True)

if __name__ == '__main__':
    main()
