#!/usr/bin/env python3
"""Generate the to-generate list in chunks."""
import json
import os
import subprocess
import sys

FORK = os.path.expanduser('~/workspace/tnn-lab/senses/pam-rebuild/round2/forks/R2-8')
WORK = os.path.join(FORK, 'scripts_gen', 'work')
BIN = os.path.join(WORK, 'sense_r28')

def parse_out(s):
    d = {}
    for line in s.splitlines():
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

def main():
    chunk, nchunks = int(sys.argv[1]), int(sys.argv[2])
    to_gen = json.load(open(os.path.join(WORK, 'to_generate.json')))
    mine = [x for i, x in enumerate(to_gen) if i % nchunks == chunk]
    print('chunk %d/%d: %d fixtures' % (chunk, nchunks, len(mine)), flush=True)
    out = {}
    for i, (t, p) in enumerate(mine):
        try:
            r = subprocess.run([BIN, t, p], capture_output=True, text=True,
                               timeout=600)
            out[t + '|' + p] = parse_out(r.stdout)
        except Exception:
            out[t + '|' + p] = {'judgment': '?', 'confidence': -1,
                                'margin': -1, 'feature': -1, 'ops': -1}
        if (i + 1) % 100 == 0:
            print('chunk %d: %d/%d' % (chunk, i + 1, len(mine)), flush=True)
    json.dump(out, open(os.path.join(WORK, 'gen_chunk_%d.json' % chunk), 'w'))
    print('chunk %d done' % chunk, flush=True)

if __name__ == '__main__':
    main()
