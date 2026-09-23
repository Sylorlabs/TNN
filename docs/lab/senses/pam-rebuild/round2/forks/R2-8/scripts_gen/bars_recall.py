#!/usr/bin/env python3
"""R2-8 recall bar (kill bar 3) — CORRECTED per PREREG_R2-8 section 3.

PREREG_R2-8 s3: "The two held-out recall tasks (shapetrans, timbredisc):
recall measured on the R2A normal fixtures of those tasks, with ground-truth
installs."

Kill bar 3 (section 5): "True-install recall >= 70% on the two held-out tasks
(shapetrans, timbredisc; denominator: correct percepts in those tasks). Below
kills."

Trial structure (from the frozen suite layout):
  X    = r2n_<task>_<idx>          (R2A normal fixture; truth from .truth file)
  S    = r2q_recall_<task>_<idx>_g (independent-source presentation)
  Ps   = r2q_recall_<task>_<idx>_p1..p3 (perturbations of S)
  Paired by index. shapetrans: idx 0..1007 (1,008 trials). timbredisc: idx
  0..719 (720 trials; R2A normal has 720). Total 1,728 recall trials.

  Gate (frozen BUILD_NOTES semantics): INSTALL iff leg_i PASS
  (j(X)==j(S), both conf>=700) AND all 3 perturbations FAIL
  (j(Pi)!=j(X) or |f(X)-f(Pi)|>3sigma_task).
  Denominator: trials where j(X)==truth ("correct percepts").

Ground truth comes from the R2A normal .truth files (not inferred).
"""
import json
import os

BASE = os.path.expanduser('~/workspace/tnn-lab/senses/pam-rebuild/round2')
FX = os.path.join(BASE, 'fixtures')
FORK = os.path.join(BASE, 'forks', 'R2-8')
WORK = os.path.join(FORK, 'scripts_gen', 'work')
OUTDIR = os.path.join(FORK, 'evidence', 'battery')

SIGMA3 = {'shapetrans': 17.5, 'timbredisc': 2.6}
CACHE = json.load(open(os.path.join(WORK, 'percept_cache.json')))

def P(task, path):
    return CACHE[task + '|' + path]

def truth_of(path):
    t = open(path + '.truth').read().strip()
    return t.split('=', 1)[1] if '=' in t else t

def main():
    rd = os.path.join(FX, 'r2q', 'companions', 'recall')
    per_task = {}
    tot_denom = tot_num = tot_trials = 0
    for task, ext, n in (('shapetrans', 'img', 1008), ('timbredisc', 'pcm', 720)):
        denom = num = 0
        for i in range(n):
            idx = '%04d' % i
            Xp = os.path.join(FX, 'r2n_%s_%s.%s' % (task, idx, ext))
            Sp = os.path.join(rd, 'r2q_recall_%s_%s_g.%s' % (task, idx, ext))
            Pps = [os.path.join(rd, 'r2q_recall_%s_%s_p%d.%s' % (task, idx, k, ext))
                   for k in (1, 2, 3)]
            truth = truth_of(Xp)
            X = P(task, Xp)
            S = P(task, Sp)
            Ps = [P(task, p) for p in Pps]
            tot_trials += 1
            if X['judgment'] == '?' or X['judgment'] != truth:
                continue
            denom += 1
            ok = (S['judgment'] != '?' and all(p['judgment'] != '?' for p in Ps))
            leg_i = (ok and X['judgment'] == S['judgment']
                     and X['confidence'] >= 700 and S['confidence'] >= 700)
            fails = 0
            if ok:
                for p in Ps:
                    if p['judgment'] != X['judgment']:
                        fails += 1
                    elif abs(p['feature'] - X['feature']) > SIGMA3[task]:
                        fails += 1
            if leg_i and fails == 3:
                num += 1
        per_task[task] = {'trials': n, 'correct': denom, 'installed': num,
                          'recall_pct': round(100.0 * num / denom, 2) if denom else 0.0}
        tot_denom += denom
        tot_num += num
    recall = 100.0 * tot_num / tot_denom if tot_denom else 0.0
    out = {
        'n_recall_trials': tot_trials,
        'trial_structure': 'X=r2n_N (R2A normal, truth from .truth), S=r2q_recall_N_g, Ps=p1..p3',
        'recall_correct': tot_denom,
        'recall_installed': tot_num,
        'recall_pct': round(recall, 2),
        'recall_bar_pct': 70.0,
        'recall_pass': bool(recall >= 70.0),
        'per_task': per_task,
    }
    os.makedirs(OUTDIR, exist_ok=True)
    json.dump(out, open(os.path.join(OUTDIR, 'recall.json'), 'w'),
              indent=2, sort_keys=True)
    print(json.dumps(out, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
