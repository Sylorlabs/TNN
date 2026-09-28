#!/usr/bin/env python3
"""R2-8 percept cache repair: reuse valid stale entries, generate only what's
missing/invalid. Excludes the q-set (not used by the frozen trial).
"""
import json
import os
import re
import subprocess
import sys

BASE = os.path.expanduser('~/workspace/tnn-lab/senses/pam-rebuild/round2')
FX = os.path.join(BASE, 'fixtures')
FORK = os.path.join(BASE, 'forks', 'R2-8')
WORK = os.path.join(FORK, 'scripts_gen', 'work')
BIN = os.path.join(WORK, 'sense_r28')
TASKS = {'colordisc': 'img', 'colorconst': 'img', 'shapetrans': 'img',
         'pitchdisc': 'pcm', 'timbredisc': 'pcm', 'motiondir': 'vid'}

STALE = json.load(open(os.path.join(FORK, 'evidence', 'percept_cache.json')))

def needed_fixtures():
    items = []
    comp = os.path.join(FX, 'r2q', 'companions')
    for task, ext in TASKS.items():
        idxs = set()
        for f in os.listdir(os.path.join(comp, task)):
            m = re.match(r'r2q_%s_(\d+)_([gpq]\d?)\.%s$' % (task, ext), f)
            if m:
                idxs.add(m.group(1))
        for idx in sorted(idxs):
            # Battery: F, g, p1-p3 (NO q-set; not used by frozen trial)
            items.append((task, os.path.join(FX, 'r2a', 'adversarial',
                                             'r2a_%s_%s.%s' % (task, idx, ext))))
            for s in ['g', 'p1', 'p2', 'p3']:
                items.append((task, os.path.join(
                    comp, task, 'r2q_%s_%s_%s.%s' % (task, idx, s, ext))))
    # Recall: r2q recall (S=g, Ps) + r2n (X)
    rd = os.path.join(comp, 'recall')
    for f in sorted(os.listdir(rd)):
        m = re.match(r'r2q_recall_(shapetrans|timbredisc)_(\d+)_(g|p\d)\.(img|pcm)$', f)
        if m:
            items.append((m.group(1), os.path.join(rd, f)))
    for i in range(1008):
        items.append(('shapetrans', os.path.join(FX, 'r2n_shapetrans_%04d.img' % i)))
    for i in range(720):
        items.append(('timbredisc', os.path.join(FX, 'r2n_timbredisc_%04d.pcm' % i)))
    # Primary 370
    hd = os.path.expanduser('~/workspace/tnn-lab/senses/rebuild/harness/fixtures')
    hmap = [('t1_colordisc', 'colordisc', 'img'), ('t2_colorconst', 'colorconst', 'img'),
            ('t3_shapetrans', 'shapetrans', 'img'), ('t4_pitchdisc', 'pitchdisc', 'pcm'),
            ('t5_timbredisc', 'timbredisc', 'pcm'), ('t6_motiondir', 'motiondir', 'vid')]
    for sub, task, ext in hmap:
        pd = os.path.join(hd, sub, 'primary')
        for f in sorted(os.listdir(pd)):
            if f.endswith('.' + ext):
                items.append((task, os.path.join(pd, f)))
    # dedupe
    seen = set()
    out = []
    for t, p in items:
        k = t + '|' + p
        if k not in seen:
            seen.add(k)
            out.append((t, p))
    return out

def parse_out(s):
    d = {}
    for line in s.splitlines():
        if '=' in line and not line.startswith('debug_vec'):
            k, v = line.split('=', 1)
            d[k.strip()] = v.strip()
    if 'judgment' not in d:
        return None
    try:
        return {'judgment': d['judgment'],
                'confidence': int(d.get('confidence', -1)),
                'margin': int(d.get('margin', -1)),
                'feature': int(d.get('feature', -1)),
                'ops': int(d.get('ops', -1))}
    except ValueError:
        return None

def main():
    items = needed_fixtures()
    print('needed:', len(items), flush=True)
    # Partition into reusable vs to-generate
    reusable = {}
    to_gen = []
    for t, p in items:
        k = t + '|' + p
        v = STALE.get(k)
        if v and v.get('judgment', '?') != '?':
            reusable[k] = v
        else:
            to_gen.append((t, p))
    print('reusable from stale:', len(reusable), flush=True)
    print('to generate:', len(to_gen), flush=True)

    # Verify a sample of reusable entries against the binary
    import random
    sample = random.sample(list(reusable.keys()), min(50, len(reusable)))
    mismatch = 0
    for k in sample:
        t, p = k.split('|', 1)
        r = subprocess.run([BIN, t, p], capture_output=True, text=True, timeout=600)
        v = parse_out(r.stdout)
        sv = reusable[k]
        if (not v or v['judgment'] != sv['judgment'] or
                v['confidence'] != sv['confidence'] or
                v['feature'] != sv['feature']):
            mismatch += 1
            print('MISMATCH:', k, flush=True)
    print('sample verified: %d/%d match' % (len(sample) - mismatch, len(sample)),
          flush=True)
    if mismatch > 0:
        print('ABORT: stale cache does not match binary', flush=True)
        sys.exit(1)

    # Write reusable to output, then generate the rest in chunks
    out = dict(reusable)
    json.dump(out, open(os.path.join(WORK, 'percept_cache_reused.json'), 'w'))
    json.dump(to_gen, open(os.path.join(WORK, 'to_generate.json'), 'w'))
    print('wrote reused cache and to-generate list', flush=True)

if __name__ == '__main__':
    main()
