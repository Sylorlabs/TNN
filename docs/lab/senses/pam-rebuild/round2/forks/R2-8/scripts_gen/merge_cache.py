#!/usr/bin/env python3
"""Merge reused cache + generated chunks into the full percept cache."""
import json
import os

FORK = os.path.expanduser('~/workspace/tnn-lab/senses/pam-rebuild/round2/forks/R2-8')
WORK = os.path.join(FORK, 'scripts_gen', 'work')

def main():
    out = json.load(open(os.path.join(WORK, 'percept_cache_reused.json')))
    print('reused:', len(out), flush=True)
    for c in range(4):
        p = os.path.join(WORK, 'gen_chunk_%d.json' % c)
        d = json.load(open(p))
        print('chunk %d:' % c, len(d), flush=True)
        out.update(d)
    print('total:', len(out), flush=True)
    # check for failures
    bad = sum(1 for v in out.values() if v.get('judgment', '?') == '?')
    print('failed percepts:', bad, flush=True)
    json.dump(out, open(os.path.join(WORK, 'percept_cache.json'), 'w'))
    print('wrote percept_cache.json', flush=True)

if __name__ == '__main__':
    main()
