#!/usr/bin/env python3
"""Full CORROB-1 battery: all cases x 3 modes x 2 reps. Parallel via xargs.
Usage: run_battery.sh (this file is imported for case lists; the .sh drives it)
"""
import os, glob

RT = os.path.expanduser('~/workspace/tnn-lab/knowledge/web_guides/live_ingest/redteam_bf1/cases')
FX = os.path.expanduser('~/workspace/liharden/corrob/fixtures')

def all_cases():
    rt = sorted(glob.glob(os.path.join(RT, '*')))
    fx = sorted(glob.glob(os.path.join(FX, '*')))
    return [(os.path.basename(p), p) for p in rt if os.path.isdir(p)] + \
           [(os.path.basename(p), p) for p in fx if os.path.isdir(p)]

if __name__ == '__main__':
    for name, path in all_cases():
        print(f'{name}\t{path}')
    print(f'total={len(all_cases())}', flush=True)
