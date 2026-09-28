#!/usr/bin/env python3
"""Run all adaptive sweep cells. Skips cells whose run.json already exists."""
import os, subprocess, sys

BASE = os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(__file__))))
# BASE = coding/reflection/speed_intel
SI = os.path.join(os.path.expanduser('~/workspace/tnn-lab'),
                  'coding/reflection/speed_intel')
ADAPT = os.path.join(SI, 'work_adaptive_code')
SWEEP = os.path.join(ADAPT, 'sweep_adapt')

FROZEN = os.path.join(SI, 'work_a1/battery_si.json')
FRESH = os.path.join(ADAPT, 'battery_adaptive_fresh.json')
CTL_DRIVER = os.path.join(SI, 'work_a1/driver_si.py')
ADAPT_DRIVER = os.path.join(ADAPT, 'driver_adapt.py')

cells = []
# (cell, battery, driver, extra_args)
for r in (2, 3):
    cells.append((f'ctl_frozen_r{r}', FROZEN, CTL_DRIVER, ['--budget', '4']))
    cells.append((f'a_frozen_r{r}', FROZEN, ADAPT_DRIVER, ['--policy', 'a']))
for p in 'bcde':
    for r in (1, 2, 3):
        cells.append((f'{p}_frozen_r{r}', FROZEN, ADAPT_DRIVER, ['--policy', p]))
for r in (1, 2, 3):
    cells.append((f'ctl_fresh_r{r}', FRESH, CTL_DRIVER, ['--budget', '4']))
for p in 'abcde':
    for r in (1, 2, 3):
        cells.append((f'{p}_fresh_r{r}', FRESH, ADAPT_DRIVER, ['--policy', p]))

done, skipped = 0, 0
for cell, battery, driver, extra in cells:
    out = os.path.join(SWEEP, cell, 'run.json')
    if os.path.exists(out):
        print(f'SKIP {cell} (run.json exists)', flush=True)
        skipped += 1
        continue
    wd = os.path.join(SWEEP, cell, 'run')
    os.makedirs(os.path.join(SWEEP, cell), exist_ok=True)
    cmd = [sys.executable, driver, battery] + extra + \
          ['--workdir', wd, '--out', out]
    print(f'RUN {cell}: {" ".join(cmd[-4:])}', flush=True)
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=SI)
    print(r.stdout.strip().split('\n')[-1] if r.stdout.strip() else '', flush=True)
    if r.returncode != 0:
        print(f'FAILED {cell}:\n{r.stderr[-2000:]}', flush=True)
        break
    done += 1
print(f'sweep done: {done} ran, {skipped} skipped', flush=True)
