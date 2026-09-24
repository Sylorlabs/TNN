#!/usr/bin/env python3
# FS-E4b availability-cost diagnostic: corrupted-G TRUE variants.
# Per TRUE battery trial (task t, truth T): F-span = TRUE F bytes (clean),
# G-span = F-span bytes of the first F-fooled adv candidate of task t (idx
# order) whose fooled judgment != T (family=9 marker).
# Usage: corrupt_g.py <cand_dir> <evidence_dir> <lists_dir> <corrupt_dir>
# Writes fixtures + corrupt manifest + per-task judge lists; prints coverage.
import sys, os, struct, hashlib, json

TASKS = ['colordisc', 'colorconst', 'pitchdisc', 'timbredisc', 'motiondir']

def read_spans(path):
    b = open(path, 'rb').read()
    magic, task, index, family, fo, fl, go, gl = struct.unpack('<8I', b[:32])
    assert magic == 0x52324658, path
    return task, index, family, b[fo:fo+fl], b[go:go+gl]

def main():
    cand, ev, lists, cord = sys.argv[1:5]
    os.makedirs(cord, exist_ok=True)
    man = []
    report = {}
    for task in TASKS:
        # fooled pool: idx order, from candidate judgments
        fooled = []
        with open(os.path.join(ev, 'judgments_cand_%s.tsv' % task)) as f:
            head = f.readline().rstrip('\n').split('\t')
            for line in f:
                r = dict(zip(head, line.rstrip('\n').split('\t')))
                if r['kind'] == 'adv' and r['formF'] != r['truth']:
                    fooled.append(r)
        fooled.sort(key=lambda r: int(r['idx']))
        # map truth T -> first fooled candidate with formF != T
        by_truth = {}
        # TRUE battery trials
        ctrls = []
        with open(os.path.join(ev, 'battery_e4b.tsv')) as f:
            head = f.readline().rstrip('\n').split('\t')
            for line in f:
                r = dict(zip(head, line.rstrip('\n').split('\t')))
                if r['task'] == task and r['split'] == 'ctrl':
                    ctrls.append(r)
        ctrls.sort(key=lambda r: int(r['idx']))
        lp = os.path.join(lists, 'corrupt_%s.txt' % task)
        n_ok, n_missing = 0, 0
        with open(lp, 'w') as lf:
            for c in ctrls:
                T = c['truth']
                if T not in by_truth:
                    hit = None
                    for fr in fooled:
                        if fr['formF'] != T:
                            hit = fr
                            break
                    by_truth[T] = hit
                fr = by_truth[T]
                if fr is None:
                    n_missing += 1
                    continue
                tpath = '%s/%s/%s.r2fx' % (cand, task, c['trial'])
                apath = '%s/%s/%s.r2fx' % (cand, task, fr['trial'])
                t_task, t_idx, _, f_true, _ = read_spans(tpath)
                _, _, _, f_adv, _ = read_spans(apath)
                assert len(f_adv) == len(f_true), (task, len(f_adv), len(f_true))
                fl = len(f_true)
                fo, go, gl = 32, 32 + fl, len(f_adv)
                head = struct.pack('<8I', 0x52324658, t_task, t_idx, 9, fo, fl, go, gl)
                body = head + f_true + f_adv
                fid = 'cor_%s_%s' % (task, c['idx'])
                p = os.path.join(cord, task, fid + '.r2fx')
                os.makedirs(os.path.dirname(p), exist_ok=True)
                open(p, 'wb').write(body)
                open(p + '.truth', 'w').write('truth=%s\n' % T)
                h = hashlib.sha256(body).hexdigest()
                man.append('%s  ./%s/%s.r2fx\n' % (h, task, fid))
                lf.write('%s %s\n' % (p, fid))
                n_ok += 1
        report[task] = {'n_ctrl': len(ctrls), 'built': n_ok, 'missing_donor': n_missing}
    with open(os.path.join(ev, 'MANIFEST.e4b_corrupt.sha256'), 'w') as f:
        f.writelines(sorted(man))
    print(json.dumps(report, indent=1), flush=True)

if __name__ == '__main__':
    main()
