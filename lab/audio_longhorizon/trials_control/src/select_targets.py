#!/usr/bin/env python3
"""select_targets.py — offline harness step 2 (Phase B2b).

Selects disjoint target sets from the sealed corpus measurement table.
Deterministic (SHA-ordered within strata). Writes:
  targets/pitch40.txt, targets/env40.txt, targets/pros40.txt,
  targets/loop20.txt, targets/batch160.txt, targets/loopfresh20.txt,
  targets/SELECTION.json

Batch layout (160 lines, depths 1..160):
   1-40   M pitch40        (control: pitch axis)
  41-80   M env40          (control: envelope axis)
  81-120  M pros40         (control: prosody axis)
 121-140  L loop20         (closed loop, deep state)
 141-160  M pitch40[0:20]  (depth probe: identical refs re-run at depth 141+)

loopfresh20.txt: the same 20 loop refs as L-lines (fresh-state loop run).
"""
import json, hashlib, os

BASE = '/home/hatch/workspace/audio_longhorizon'
T = os.path.join(BASE, 'trials_control', 'targets')


def sha_order(rs):
    return sorted(rs, key=lambda r: hashlib.sha256(r['clip_id'].encode()).hexdigest())


rows = json.load(open(os.path.join(T, 'clip_measure.json')))
used = set()
sel = {}


def take(rs, n, key):
    rs = [r for r in sha_order(rs) if r['clip_id'] not in used]
    out = rs[:n]
    assert len(out) == n, f'{key}: only {len(out)}/{n}'
    for r in out:
        used.add(r['clip_id'])
    sel[key] = [r['clip_id'] for r in out]
    return out


def spread(rs, n, f):
    """systematic spread: f0/cv-sorted, every kth. deterministic."""
    rs = sorted([r for r in rs if r['clip_id'] not in used], key=f)
    idx = [int(round(i * (len(rs) - 1) / (n - 1))) for i in range(n)]
    out = [rs[i] for i in idx]
    assert len({r['clip_id'] for r in out}) == n, 'spread collision'
    for r in out:
        used.add(r['clip_id'])
    return out


# --- PITCH axis (40): voiced, f0 125..1200, spread across range ---
pc = [r for r in rows if 125 <= r['f0_hz'] <= 1200 and r['voiced_frac'] >= 0.3
      and r['dur_s'] <= 4.0 and r['cls'] != 'lowf0']
pitch = spread(pc, 40, lambda r: r['f0_hz'])
sel['pitch40'] = [r['clip_id'] for r in pitch]

# --- ENVELOPE axis (40): 13 rise / 14 flat / 13 decay ---
ec = [r for r in rows if r['dur_s'] <= 4.0 and r['clip_id'] not in used]
env = (take([r for r in ec if r['env'] == 'rise'], 13, 'env_rise') +
       take([r for r in ec if r['env'] == 'flat'], 14, 'env_flat') +
       take([r for r in ec if r['env'] == 'decay'], 13, 'env_decay'))
sel['env40'] = [r['clip_id'] for r in env]

# --- PROSODY axis (40): cv spread, voiced material only ---
prc = [r for r in rows if 0.015 <= r['cv'] <= 0.5 and r['f0_hz'] >= 125
       and r['voiced_frac'] >= 0.2 and r['dur_s'] <= 5.0
       and r['cls'] in ('prosody', 'speech', 'child')
       and r['clip_id'] not in used]
pros = spread(prc, 40, lambda r: r['cv'])
sel['pros40'] = [r['clip_id'] for r in pros]

# --- LOOP (20): 16 voiced spread + 4 lowf0 ---
lc = [r for r in rows if r['f0_hz'] >= 125 and r['voiced_frac'] >= 0.25
      and r['dur_s'] <= 5.0 and r['clip_id'] not in used]
loop16 = spread(lc, 16, lambda r: r['f0_hz'])
low = [r for r in rows if r['cls'] == 'lowf0' and r['clip_id'] not in used]
loop4 = take(low, 4, 'loop_lowf0')
loop = loop16 + loop4
sel['loop20'] = [r['clip_id'] for r in loop]


def wpath(r):
    return os.path.join(BASE, r['path'])


def write_list(name, lines):
    p = os.path.join(T, name)
    open(p, 'w').write('\n'.join(lines) + '\n')
    print('wrote', p, len(lines), 'lines')


write_list('pitch40.txt', ['M ' + wpath(r) for r in pitch])
write_list('env40.txt', ['M ' + wpath(r) for r in env])
write_list('pros40.txt', ['M ' + wpath(r) for r in pros])
write_list('loop20.txt', ['L ' + wpath(r) for r in loop])
batch = (['M ' + wpath(r) for r in pitch] +
         ['M ' + wpath(r) for r in env] +
         ['M ' + wpath(r) for r in pros] +
         ['L ' + wpath(r) for r in loop] +
         ['M ' + wpath(r) for r in pitch[:20]])
write_list('batch160.txt', batch)
write_list('loopfresh20.txt', ['L ' + wpath(r) for r in loop])

# summary stats for the runlog
def stats(rs):
    f0s = [r['f0_hz'] for r in rs]
    return dict(n=len(rs), f0_min=round(min(f0s), 1), f0_max=round(max(f0s), 1),
                classes={k: sum(1 for r in rs if r['cls'] == k) for k in
                         sorted({r['cls'] for r in rs})})

summary = dict(pitch40=stats(pitch), env40=stats(env), pros40=stats(pros),
               loop20=stats(loop),
               env_classes={e: sum(1 for r in env if r['env'] == e)
                            for e in ('rise', 'flat', 'decay')},
               prosody_cv=[round(r['cv'], 4) for r in pros],
               pitch_f0=[round(r['f0_hz'], 1) for r in pitch])
json.dump(dict(selection=sel, summary=summary,
               measure_sha='91dfbe4b39b778e60daf59492ecba7f03823fd0b5d9c002ecf64bc7b36e44127'),
          open(os.path.join(T, 'SELECTION.json'), 'w'), indent=1)
print(json.dumps(summary, indent=1))
