#!/usr/bin/env python3
"""Crew C curriculum driver: train / control / retention / held-out runs.
Usage: run.py <mode> [ep_start ep_end]
  modes: train-v1 | train-neg | train-pos | heldout-v1 | heldout-neg |
         heldout-pos | heldout-nv | retention-v1 | smoke
Memory files live in the run dir; learn is skipped for -neg and retention.
"""
import hashlib
import json
import os
import subprocess
import sys

import gen
from gen import write_op_spec
import score as scorer

KBC = os.path.expanduser('~/workspace/kb_control/crewC/kbc_bin')
WORK = os.path.expanduser('~/workspace/kb_control/crewC/runs')


def sh(args):
    r = subprocess.run(args, capture_output=True, text=True, timeout=60)
    return r


def run_op(kbc_mode, spec, img_in, mem, trace_out, img_out):
    r = sh([KBC, kbc_mode, spec, img_in, mem, trace_out, img_out])
    rc = None
    for line in r.stdout.splitlines():
        if line.startswith('RC '):
            rc = int(line.split()[1])
    return rc, r


def run_learn(spec, trace, verdict, mem_in, mem_out):
    r = sh([KBC, 'learn', spec, trace, verdict, mem_in, mem_out])
    rc = None
    for line in r.stdout.splitlines():
        if line.startswith('RC '):
            rc = int(line.split()[1])
    return rc


def mem_sha(path):
    if not os.path.exists(path):
        return 'absent'
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()[:16]


def run_episode(idx, regime, rundir, mem, learn_on, kbc_mode='operate', tag=''):
    epdir = os.path.join(rundir, f'ep{idx:05d}{tag}')
    os.makedirs(epdir, exist_ok=True)
    sp0, img0, meta = gen.build_episode(idx, regime, epdir)
    ops = meta['ops']
    results = []
    img_cur = img0
    for j, op in enumerate(ops):
        if j > 0:
            sp = write_op_spec(epdir, j, op, img_cur, meta['frozen_hints'],
                               lambda jj, be: meta['frozen_hint_used'],
                               meta['chunk'], idx * 10, len(ops))
        else:
            sp = sp0
        trace = os.path.join(epdir, f'trace{j}.txt')
        img_next = os.path.join(epdir, f'img{j + 1}.bin')
        verdict = os.path.join(epdir, f'verdict{j}.txt')
        rc, _ = run_op(kbc_mode, sp, img_cur, mem, trace, img_next)
        assert rc == 0, f'operate rc={rc} ep={idx} op={j}'
        res = scorer.score_op(sp, img_cur, img_next, trace, verdict)
        res.update({'ep': idx, 'op_idx': j, 'fam': meta['fam'],
                    'op': op['op'], 'slot': op['slot']})
        results.append(res)
        if learn_on:
            mem_next = os.path.join(epdir, f'mem_after{j}.mem')
            rc2 = run_learn(sp, trace, verdict, mem, mem_next)
            assert rc2 == 0, f'learn rc={rc2} ep={idx} op={j}'
            # carry the updated memory forward
            with open(mem_next, 'rb') as f, open(mem, 'wb') as g:
                g.write(f.read())
        img_cur = img_next
    return results


def summarize(results):
    s = {'n': len(results), 'fail': 0, 'clean': 0, 'process_viol': 0,
         'refuse_ok': 0, 'false_refuse': 0, 'refuse_bad': 0,
         'replans': 0, 'compliant': 0}
    for r in results:
        o = r['outcome']
        if o == 'CLEAN':
            s['clean'] += 1
            if not r['compliant']:
                s['process_viol'] += 1
            else:
                s['compliant'] += 1
        elif o == 'COLLATERAL':
            s['fail'] += 1
        elif o == 'REFUSE_OK':
            s['refuse_ok'] += 1
            s['compliant'] += 1
        elif o == 'REFUSE_BAD':
            s['refuse_bad'] += 1
            s['fail'] += 1
        elif o == 'FALSE_REFUSE':
            s['false_refuse'] += 1
        if r['replanned']:
            s['replans'] += 1
    return s


def run_range(mode, ep_start, ep_end):
    base = mode.split('-')[0]
    regime = {'train': 'train', 'heldout': 'heldout', 'retention': 'retention',
              'smoke': 'train'}[base]
    learn_on = mode in ('train-v1', 'heldout-v1', 'smoke')
    kbc_mode = 'operate_nv' if mode.endswith('-nv') else 'operate'
    rundir = os.path.join(WORK, mode)
    os.makedirs(rundir, exist_ok=True)
    mem = os.path.join(rundir, 'memory.mem')
    if mode == 'train-pos' and not os.path.exists(mem):
        with open(mem, 'w') as f:
            f.write('KBC1MEM\nLESSON 0 4 8 90\nCLEAN_STREAK 0\nCOLLATERAL 0\n'
                    'DIVERSE 0\nLASTSIT -1\n')
    if mode in ('heldout-v1', 'retention-v1', 'heldout-nv'):
        # continue from the trained memory
        src = os.path.join(WORK, 'train-v1', 'memory.mem')
        assert os.path.exists(src), 'train first'
        with open(src, 'rb') as f, open(mem, 'wb') as g:
            g.write(f.read())
    if mode in ('heldout-pos',):
        src = os.path.join(WORK, 'train-pos', 'memory.mem')
        with open(src, 'rb') as f, open(mem, 'wb') as g:
            g.write(f.read())
    if mode in ('heldout-neg',):
        src = os.path.join(WORK, 'train-neg', 'memory.mem')
        if os.path.exists(src):
            with open(src, 'rb') as f, open(mem, 'wb') as g:
                g.write(f.read())
    allres = []
    curve = []
    for idx in range(ep_start, ep_end):
        res = run_episode(idx, regime, rundir, mem, learn_on, kbc_mode)
        allres.extend(res)
        if mode.startswith('train') and idx % 10 == 9:
            w = allres[-30:] if len(allres) >= 30 else allres
            s = summarize(w)
            curve.append({'ep_end': idx, 'fail_rate': s['fail'] / max(1, s['n']),
                          'compliant_rate': s['compliant'] / max(1, s['n']),
                          'mem': mem_sha(mem)})
            print(f'  ep {idx}: fail_rate={curve[-1]["fail_rate"]:.3f} '
                  f'compliant={curve[-1]["compliant_rate"]:.3f} mem={curve[-1]["mem"]}',
                  flush=True)
        if idx % 50 == 49:
            print(f'  ... ep {idx} done', flush=True)
    summ = summarize(allres)
    out = {'mode': mode, 'range': [ep_start, ep_end], 'summary': summ,
           'curve': curve, 'mem_final': mem_sha(mem)}
    with open(os.path.join(rundir, f'results_{ep_start}_{ep_end}.json'), 'w') as f:
        json.dump(out, f, indent=1)
    # also dump per-episode outcomes for the learning-curve plot
    with open(os.path.join(rundir, f'eps_{ep_start}_{ep_end}.jsonl'), 'w') as f:
        for r in allres:
            f.write(json.dumps({k: r[k] for k in
                                ('ep', 'op_idx', 'fam', 'op', 'slot', 'outcome',
                                 'fail', 'compliant', 'missing_steps', 'notes',
                                 'replanned', 'predict_src', 'sit', 'faked',
                                 'changed', 'collateral')}) + '\n')
    print(f'{mode}[{ep_start},{ep_end}): ' + json.dumps(summ))
    return out


if __name__ == '__main__':
    mode = sys.argv[1]
    a = int(sys.argv[2]) if len(sys.argv) > 2 else None
    b = int(sys.argv[3]) if len(sys.argv) > 3 else None
    defaults = {
        'train-v1': (0, 260), 'train-neg': (0, 260), 'train-pos': (0, 60),
        'heldout-v1': (1000, 1060), 'heldout-neg': (1000, 1060),
        'heldout-pos': (1000, 1060), 'heldout-nv': (1000, 1060),
        'retention-v1': (2000, 3000), 'smoke': (0, 12),
    }
    if a is None:
        a, b = defaults[mode]
    run_range(mode, a, b)
