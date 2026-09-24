#!/usr/bin/env python3
# FS-E4b: judge all fresh candidates with the frozen e4b driver (judge_list).
# Usage: judge_all.py <cand_dir> <lists_dir> <evidence_dir> <e4b_bin>
# Writes per-task list files, runs the driver, parses .out -> judgments TSVs.
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

def main():
    cand, lists, ev, e4b = sys.argv[1:5]
    os.makedirs(lists, exist_ok=True)
    os.makedirs(ev, exist_ok=True)
    for task in TASKS:
        lp = os.path.join(lists, 'cand_%s.txt' % task)
        with open(lp, 'w') as f:
            for j in range(N_ADV):
                idx = ADV_BASE + j
                fid = 'r2a_%s_%d' % (task, idx)
                f.write('%s/%s/%s.r2fx %s\n' % (cand, task, fid, fid))
            for j in range(N_NORM):
                idx = NORM_BASE + j
                fid = 'r2n_%s_%d' % (task, idx)
                f.write('%s/%s/%s.r2fx %s\n' % (cand, task, fid, fid))
        led = os.path.join(ev, 'judge_cand_%s.txt' % task)
        r = subprocess.run([e4b, 'judge_list', lp, led])
        if r.returncode != 0:
            print('DRIVER FAILED on %s' % task, flush=True)
            sys.exit(1)
        # parse .out -> judgments TSV
        tsv = os.path.join(ev, 'judgments_cand_%s.tsv' % task)
        n = 0
        with open(led + '.out') as fin, open(tsv, 'w') as fout:
            fout.write('\t'.join(['kind', 'idx'] + FIELDS) + '\n')
            for line in fin:
                if line.startswith('trial='):
                    d = parse_line(line)
                    trial = d['trial']
                    kind = 'adv' if trial.startswith('r2a_') else 'norm'
                    idx = trial.split('_')[-1]
                    fout.write('\t'.join([kind, idx] + [d.get(k, '') for k in FIELDS]) + '\n')
                    n += 1
        print('task %s judged: %d trials' % (task, n), flush=True)

if __name__ == '__main__':
    main()
