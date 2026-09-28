#!/usr/bin/env python3
# FS-E4b fresh candidate draw (frozen procedure from PREREG_FS-E4b, committed a9a48b3f).
# Deterministic: fixed index orders, generator splitmix streams. NO random module.
# Usage: draw_e4b.py <cand_dir>
# Resumable: fixtures already recorded in gen_ledger.e4b.jsonl are skipped.
import sys, os, hashlib, json

sys.path.insert(0, '/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/forks/R2-7/src')
import gen_r2a

MASTER = 20260923
TASKS = [('colordisc', 0), ('colorconst', 1), ('pitchdisc', 3),
         ('timbredisc', 4), ('motiondir', 5)]
N_ADV = 8000
ADV_BASE = 200000
N_NORM = 1500
NORM_BASE = 100000

def draw_task(task, tidx, cand, ledger_path):
    done = set()
    if os.path.exists(ledger_path):
        with open(ledger_path) as f:
            for line in f:
                line = line.strip()
                if line:
                    done.add(json.loads(line)['id'])
    ledger = open(ledger_path, 'a')
    new_task = 0
    fams = [f for _, f in gen_r2a.GEN[tidx][2]]

    def emit(kind, idx, fam):
        fid = ('r2a_%s_%d' % (task, idx)) if kind == 'adv' else ('r2n_%s_%d' % (task, idx))
        if fid in done:
            return False
        gen = gen_r2a.GEN[tidx][0]
        rng = gen_r2a.Rng(gen_r2a.stream_seed(MASTER, (500 if kind == 'adv' else 400) + tidx, idx))
        f, g, truth = gen(rng, fam, idx)
        path = os.path.join(cand, task, fid + '.r2fx')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        gen_r2a.write_r2fx(path, tidx, idx, fam, f, g)
        gen_r2a.write_truth(path + '.truth', truth)
        h = hashlib.sha256(open(path, 'rb').read()).hexdigest()
        rec = {'id': fid, 'task': task, 'kind': kind, 'idx': idx,
               'family': fam, 'truth': truth, 'sha256': h}
        ledger.write(json.dumps(rec) + '\n')
        return True

    for j in range(N_ADV):
        idx = ADV_BASE + j
        fam = fams[j % len(fams)]
        if emit('adv', idx, fam):
            new_task += 1
    for j in range(N_NORM):
        idx = NORM_BASE + j
        if emit('norm', idx, 0):
            new_task += 1
    ledger.close()
    print('task %s done (+%d new)' % (task, new_task), flush=True)
    return new_task


def main():
    cand = sys.argv[1]
    os.makedirs(cand, exist_ok=True)
    arg = sys.argv[2] if len(sys.argv) > 2 else None
    if arg == 'finalize':
        # concatenate per-task ledgers in TASKS order -> gen_ledger.e4b.jsonl
        # and write the sorted manifest. Deterministic.
        out = open(os.path.join(cand, 'gen_ledger.e4b.jsonl'), 'w')
        man = []
        for task, _ in TASKS:
            lp = os.path.join(cand, 'gen_ledger.e4b.%s.jsonl' % task)
            with open(lp) as f:
                for line in f:
                    out.write(line)
                    r = json.loads(line)
                    man.append('%s  ./%s/%s.r2fx\n' % (r['sha256'], r['task'], r['id']))
        out.close()
        with open(os.path.join(cand, 'MANIFEST.e4b_cand.sha256'), 'w') as f:
            f.writelines(sorted(man))
        print('finalized: %d fixtures' % len(man), flush=True)
        return
    tasks = TASKS
    if arg:
        tasks = [(t, i) for t, i in TASKS if t == arg]
        assert tasks, 'unknown task %s' % arg
    for task, tidx in tasks:
        lp = os.path.join(cand, 'gen_ledger.e4b.%s.jsonl' % task)
        draw_task(task, tidx, cand, lp)

if __name__ == '__main__':
    main()
