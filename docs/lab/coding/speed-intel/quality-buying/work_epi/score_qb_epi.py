#!/usr/bin/env python3
"""QB-EPI sweep: modes d0..d5 x 3 reruns on the frozen 94-item A1R battery.

Battery files are read from work_a1r/epi/ (byte-identical reuse, never copied).
Binary: work_epi/delib_qb, run with cwd=work_a1r and workdir='epi'.
Usage: python3 score_qb_epi.py   (run from work_epi/)
Writes: logs/out_<mode>_<stem>_r<rep>.txt, sweep_qb_epi.json
"""
import subprocess, os, hashlib, json, re, time, resource

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(HERE, 'delib_qb')
A1R = os.path.join(os.path.dirname(HERE), '..', '..',
                   'reflection', 'speed_intel', 'work_a1r')
A1R = os.path.normpath(A1R)
EPI = os.path.join(A1R, 'epi')
LOGS = os.path.join(HERE, 'logs')

FAMS = {
    'joke':           ['W%03d' % i for i in range(141, 151)],
    'sarcasm':        ['W%03d' % i for i in range(151, 161)],
    'hypothetical':   ['W%03d' % i for i in range(161, 171)],
    'analogy':        ['W%03d' % i for i in range(171, 181)],
    'poetry':         ['W%03d' % i for i in range(181, 191)],
    'counterfactual': ['W%03d' % i for i in range(191, 201)],
    'implicature':    ['W%03d' % i for i in range(201, 211)],
}
ID2FAM = {i: k for k, ids in FAMS.items() for i in ids}

ITEMS = json.load(open(os.path.join(EPI, 'battery_a1r_items.json')))
INTENDED = {it['id']: it['correct'] for it in ITEMS['items']}
assert len(INTENDED) == 94

LINE = re.compile(r'^(\S+)\|(ENDORSE|WITHHOLD)\|preds=(\d+)\|recon=(\d+)\|vflip=(\d+)(.*)$')

def parse(out, mode):
    items = {}
    preds = 0; n = 0
    extra = {}
    for line in out.splitlines():
        m = LINE.match(line)
        if m:
            iid, ver, p = m.group(1), m.group(2), int(m.group(3))
            items[iid] = ver
            extra[iid] = m.group(6)
            preds += p; n += 1
    return items, preds, n, extra

def child_cpu():
    r = resource.getrusage(resource.RUSAGE_CHILDREN)
    return r.ru_utime + r.ru_stime

def main():
    os.makedirs(LOGS, exist_ok=True)
    files = [('b12_false.txt', 'false'), ('b12_true.txt', 'true'), ('c70.txt', 'c70')]
    results = {}
    for mode in ('d0', 'd1', 'd2', 'd3', 'd4', 'd5'):
        digests = []
        cells = []
        for rep in (1, 2, 3):
            all_items = {}
            tp = 0; tn = 0
            wall = 0.0; cpu = 0.0
            raws = {}
            for fname, stem in files:
                t0 = time.perf_counter(); c0 = child_cpu()
                r = subprocess.run([BIN, 'epi', mode, fname],
                                   capture_output=True, text=True, cwd=A1R)
                wall += time.perf_counter() - t0
                cpu += child_cpu() - c0
                assert r.returncode == 0, (mode, rep, fname, r.stderr[:200])
                raws[stem] = r.stdout
                with open(os.path.join(LOGS, 'out_%s_%s_r%d.txt' % (mode, stem, rep)), 'w') as f:
                    f.write(r.stdout)
                items, p, n, _ = parse(r.stdout, mode)
                all_items.update(items)
                tp += p; tn += n
            assert tn == 94, (mode, rep, tn)
            canon = '\n'.join('%s|%s' % (k, all_items[k]) for k in sorted(all_items))
            digests.append(hashlib.sha256(canon.encode()).hexdigest())
            fam_score = {k: [0, 0] for k in FAMS}
            f_ok = t_ok = 0
            for iid, ver in all_items.items():
                ok = (ver == INTENDED[iid])
                if iid.startswith('F'):
                    f_ok += ok
                elif iid.startswith('BC'):
                    t_ok += ok
                else:
                    fam = ID2FAM.get(iid)
                    if fam:
                        fam_score[fam][1] += 1
                        fam_score[fam][0] += ok
            total_ok = f_ok + t_ok + sum(v[0] for v in fam_score.values())
            cells.append({'rep': rep,
                          'total': total_ok,
                          'false': f_ok, 'true': t_ok,
                          'fams': {k: v[0] for k, v in fam_score.items()},
                          'mean_preds': round(tp / tn, 3),
                          'preds_total': tp,
                          'wall_s': round(wall, 3),
                          'cpu_s': round(cpu, 3),
                          'digest': digests[-1]})
        det = 'IDENTICAL' if len(set(digests)) == 1 else 'DIFFER'
        results[mode] = {'runs': cells, 'determinism': det}
        c = cells[0]
        print('mode %s: Q_e=%d/94 false=%d/12 true=%d/12 fams=%s mean_preds=%.3f '
              'wall=%.3fs cpu=%.3fs determinism=%s'
              % (mode, c['total'], c['false'], c['true'],
                 ' '.join('%s:%d/10' % (k, v) for k, v in c['fams'].items()),
                 c['mean_preds'], c['wall_s'], c['cpu_s'], det), flush=True)
    json.dump(results, open(os.path.join(HERE, 'sweep_qb_epi.json'), 'w'),
              indent=1, sort_keys=True)
    print('wrote sweep_qb_epi.json')

if __name__ == '__main__':
    main()
