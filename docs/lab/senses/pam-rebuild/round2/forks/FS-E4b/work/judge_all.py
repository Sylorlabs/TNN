#!/usr/bin/env python3
# FS-E4b: judge all fresh candidates with the frozen e4b driver (judge_list).
# Usage: judge_all.py <cand_dir> <lists_dir> <evidence_dir> <e4b_bin> [task]
# Writes per-task list files, runs the driver, parses .out -> judgments TSVs.
# Resumable: skips fixtures already present in the cumulative .out.
import sys, os, subprocess

TASKS = ['colordisc', 'colorconst', 'pitchdisc', 'timbredisc', 'motiondir']
N_ADV = 8000
ADV_BASE = 200000
N_NORM = 1500
NORM_BASE = 100000

FIELDS = ['trial', 'task', 'truth', 'formF', 'formG', 'chal', 'base', 'booster', 'ops']

def parse_line(line):
    d = {}
    for tok in line.strip().split():
        if '=' in tok:
            k, v = tok.split('=', 1)
            d[k] = v
    return d

def done_trials(outf):
    done = set()
    if os.path.exists(outf):
        with open(outf) as f:
            for line in f:
                if line.startswith('trial='):
                    d = parse_line(line)
                    if 'trial' in d:
                        done.add(d['trial'])
    return done

def main():
    cand, lists, ev, e4b = sys.argv[1:5]
    only = sys.argv[5] if len(sys.argv) > 5 else None
    os.makedirs(lists, exist_ok=True)
    os.makedirs(ev, exist_ok=True)
    tasks = [t for t in TASKS if only is None or t == only]
    for task in tasks:
        outf = os.path.join(ev, 'judge_cand_%s.txt.out' % task)
        done = done_trials(outf)
        lp = os.path.join(lists, 'cand_%s.txt' % task)
        todo = []
        for j in range(N_ADV):
            idx = ADV_BASE + j
            fid = 'r2a_%s_%d' % (task, idx)
            if fid not in done:
                todo.append('%s/%s/%s.r2fx %s\n' % (cand, task, fid, fid))
        for j in range(N_NORM):
            idx = NORM_BASE + j
            fid = 'r2n_%s_%d' % (task, idx)
            if fid not in done:
                todo.append('%s/%s/%s.r2fx %s\n' % (cand, task, fid, fid))
        if not todo:
            print('task %s already complete (%d trials)' % (task, len(done)), flush=True)
        else:
            with open(lp, 'w') as f:
                f.writelines(todo)
            led = os.path.join(ev, 'judge_cand_%s_tmp.txt' % task)
            r = subprocess.run([e4b, 'judge_list', lp, led])
            if r.returncode != 0:
                print('DRIVER FAILED on %s' % task, flush=True)
                sys.exit(1)
            # append new results to cumulative .out
            with open(led + '.out') as fin, open(outf, 'a') as fout:
                for line in fin:
                    fout.write(line)
            os.remove(led + '.out')
            # remove temp ledger if exists
            if os.path.exists(led):
                os.remove(led)
            print('task %s judged +%d (total %d)' % (task, len(todo), len(done) + len(todo)), flush=True)
        # parse cumulative .out -> judgments TSV
        tsv = os.path.join(ev, 'judgments_cand_%s.tsv' % task)
        n = 0
        with open(outf) as fin, open(tsv, 'w') as fout:
            fout.write('\t'.join(['kind', 'idx'] + FIELDS) + '\n')
            for line in fin:
                if line.startswith('trial='):
                    d = parse_line(line)
                    trial = d['trial']
                    kind = 'adv' if trial.startswith('r2a_') else 'norm'
                    idx = trial.split('_')[-1]
                    fout.write('\t'.join([kind, idx] + [d.get(k, '') for k in FIELDS]) + '\n')
                    n += 1
        print('task %s TSV: %d trials' % (task, n), flush=True)

if __name__ == '__main__':
    main()
