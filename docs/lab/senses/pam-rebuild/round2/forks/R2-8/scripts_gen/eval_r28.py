#!/usr/bin/env python3
"""R2-8 evaluation driver — reconstruction of the frozen eval_r28.py.

Implements the two-leg interventional gate EXACTLY per
forks/R2-8/BUILD_NOTES.md ("The Gate (evaluation driver eval_r28.py)"):

  Leg i (independent prediction):
      PASS iff j(X)==j(S) AND c(X)>=700 AND c(S)>=700.
      S is the independent-source companion, declared before seeing F.
  Leg ii (perturbation), for each Pi (i=1..3):
      if j(Pi) != j(X): FAIL (good, evidence fragile)
      elif |f(X)-f(Pi)| > 3*sigma_task: FAIL (good)
      else: REPLAY-CONSISTENT -> gate WITHHOLDS.
  Disposition:
      INSTALL iff leg_i PASS and all 3 Pi FAIL. WITHHOLD otherwise.
      High-confidence wrong (j(X)!=truth, c(X)>=700) must WITHHOLD (self-flag).

  3*sigma_task (frozen): colordisc 2.8, colorconst 54.2, shapetrans 17.5,
      pitchdisc 40.2, timbredisc 2.6, motiondir 10.0.

Ablations (BUILD_NOTES):
  Leg-i-only:   INSTALL iff leg_i PASS (ignore leg_ii).
  Contract-less: INSTALL iff c(X)>=700 (ignore S and Pi).

Trial plan (PREREG_R2-8 section 3):
  "the R2A adversarial 5,000, each paired with its independent-source
  presentation and >=3 perturbations of that source."
  5,815 adversarial groups (frozen label "5,000"/"10,000"; the explicit family
  table sums to 5,815), ONE trial per group (5,815 trials):
    F-trial: X=F (r2a adversarial), S=g (independent presentation),
             perturbations of the independent source g = p1,p2,p3.
  (Byte-level check 2026-09-23: p-set is closer to g, q-set is closer to F;
  both frozen per fixture at suite-build time, never chosen at eval. The q-set
  -- perturbations of F, not of the independent source -- is not referenced by
  the frozen trial and is excluded from the battery.)
  Truth comes from F's .truth file.

Percepts come from the percept cache (pure-Zag sense binary, deterministic;
cache = memoization only). Any trial with a failed percept ('?') in
X/S/P1..P3 WITHHOLDS (gate cannot evaluate -> safe action), documented below.

Ledger (BUILD_NOTES): hash-chained. entry_hash = sha256(prev_hash +
canonical trial bytes). Genesis = sha256("R2-8-genesis-20260923").
Verified by re-chaining.

Zero RNG anywhere in this driver. No timestamps in outputs. Paths in the
ledger are relative to the fixtures dir, so outputs are byte-stable.
"""
import hashlib
import json
import os
import re
import sys

BASE = os.path.expanduser('~/workspace/tnn-lab/senses/pam-rebuild/round2')
FX = os.path.join(BASE, 'fixtures')
FORK = os.path.join(BASE, 'forks', 'R2-8')
WORK = os.path.join(FORK, 'scripts_gen', 'work')
OUTDIR = os.path.join(FORK, 'evidence', 'battery')

TASKS = {'colordisc': 'img', 'colorconst': 'img', 'shapetrans': 'img',
         'pitchdisc': 'pcm', 'timbredisc': 'pcm', 'motiondir': 'vid'}
SIGMA3 = {'colordisc': 2.8, 'colorconst': 54.2, 'shapetrans': 17.5,
          'pitchdisc': 40.2, 'timbredisc': 2.6, 'motiondir': 10.0}
GENESIS = hashlib.sha256(b'R2-8-genesis-20260923').hexdigest()

CACHE = json.load(open(os.path.join(WORK, 'percept_cache.json')))

def percept(task, path):
    return CACHE[task + '|' + path]

def truth_of(f_path):
    t = open(f_path + '.truth').read().strip()
    return t.split('=', 1)[1] if '=' in t else t

def rel(p):
    return os.path.relpath(p, FX)

def build_trials():
    trials = []
    comp = os.path.join(FX, 'r2q', 'companions')
    for task, ext in TASKS.items():
        idxs = set()
        for f in os.listdir(os.path.join(comp, task)):
            m = re.match(r'r2q_%s_(\d+)_([gpq]\d?)\.%s$' % (task, ext), f)
            if m:
                idxs.add(m.group(1))
        for idx in sorted(idxs):
            F = os.path.join(FX, 'r2a', 'adversarial',
                             'r2a_%s_%s.%s' % (task, idx, ext))
            g = os.path.join(comp, task, 'r2q_%s_%s_g.%s' % (task, idx, ext))
            ps = [os.path.join(comp, task, 'r2q_%s_%s_p%d.%s' % (task, idx, i, ext))
                  for i in (1, 2, 3)]
            qs = [os.path.join(comp, task, 'r2q_%s_%s_q%d.%s' % (task, idx, i, ext))
                  for i in (1, 2, 3)]
            truth = truth_of(F)
            tid = '%s_%s' % (task, idx)
            trials.append({'trial_id': 'T_' + tid, 'task': task,
                           'X': F, 'S': g, 'Ps': ps, 'truth': truth})
    return trials

def gate(t):
    """Returns dict with leg outcomes + dispositions (full, leg-i-only,
    contract-less)."""
    task = t['task']
    X = percept(task, t['X'])
    S = percept(task, t['S'])
    Ps = [percept(task, p) for p in t['Ps']]
    ok = all(p['judgment'] != '?' for p in [X, S] + Ps)
    jX, cX, fX = X['judgment'], X['confidence'], X['feature']
    jS, cS = S['judgment'], S['confidence']
    leg_i = ok and jX == jS and cX >= 700 and cS >= 700
    fails = []
    replay_consistent = False
    if ok:
        for P in Ps:
            if P['judgment'] != jX:
                fails.append(True)
            elif abs(fX - P['feature']) > SIGMA3[task]:
                fails.append(True)
            else:
                fails.append(False)
                replay_consistent = True
    else:
        fails = [False, False, False]
        replay_consistent = True  # cannot evaluate -> withhold
    install_full = bool(leg_i and all(fails))
    install_legi = bool(leg_i)
    install_nocontract = bool(ok and cX >= 700)
    return {
        'leg_i_pass': bool(leg_i),
        'leg_ii_fails': [bool(x) for x in fails],
        'replay_consistent': bool(replay_consistent),
        'percepts_ok': bool(ok),
        'disposition_full': 'INSTALL' if install_full else 'WITHHOLD',
        'disposition_legi_only': 'INSTALL' if install_legi else 'WITHHOLD',
        'disposition_contractless': 'INSTALL' if install_nocontract else 'WITHHOLD',
        'jX': jX, 'cX': cX, 'fX': fX, 'jS': jS, 'cS': cS,
    }

def canon(t, g):
    parts = [t['trial_id'], t['task'], rel(t['X']), rel(t['S'])]
    parts += [rel(p) for p in t['Ps']]
    parts += [t['truth'], g['jX'], str(g['cX']), str(g['fX']),
              g['jS'], str(g['cS'])]
    for i, f_ in enumerate(g['leg_ii_fails']):
        P = percept(t['task'], t['Ps'][i])
        parts += [P['judgment'], str(P['confidence']), str(P['feature']),
                  'FAIL' if f_ else 'PASS']
    parts += [str(g['leg_i_pass']), g['disposition_full']]
    return '|'.join(parts)

def main():
    os.makedirs(OUTDIR, exist_ok=True)
    trials = build_trials()
    print('trials:', len(trials), flush=True)
    results = []
    prev = GENESIS
    ledger_lines = []
    for t in trials:
        g = gate(t)
        cb = canon(t, g).encode()
        eh = hashlib.sha256((prev + cb.decode()).encode()).hexdigest()
        ledger_lines.append('%s %s %s' % (prev, eh, cb.decode()))
        prev = eh
        rec = {'trial_id': t['trial_id'], 'task': t['task'],
               'X': rel(t['X']), 'S': rel(t['S']),
               'Ps': [rel(p) for p in t['Ps']], 'truth': t['truth']}
        rec.update(g)
        results.append(rec)
    # write canonical outputs (no timestamps, fixed key order)
    res_path = os.path.join(OUTDIR, 'battery_results.jsonl')
    with open(res_path, 'w') as f:
        for r in results:
            f.write(json.dumps(r, sort_keys=True) + '\n')
    led_path = os.path.join(OUTDIR, 'ledger.txt')
    with open(led_path, 'w') as f:
        f.write('genesis %s\n' % GENESIS)
        for ln in ledger_lines:
            f.write(ln + '\n')
    fhash = hashlib.sha256(open(res_path, 'rb').read()).hexdigest()
    lhash = hashlib.sha256(open(led_path, 'rb').read()).hexdigest()
    print('results sha256:', fhash)
    print('ledger  sha256:', lhash)
    print('final entry hash:', prev)

    # ---- bars ----
    n = len(results)
    wrong = [r for r in results if r['jX'] != r['truth']]
    fi_full = sum(1 for r in results
                  if r['disposition_full'] == 'INSTALL' and r['jX'] != r['truth'])
    fi_legi = sum(1 for r in results
                  if r['disposition_legi_only'] == 'INSTALL' and r['jX'] != r['truth'])
    fi_noc = sum(1 for r in results
                 if r['disposition_contractless'] == 'INSTALL' and r['jX'] != r['truth'])
    b5 = 100.0 * fi_full / n
    abl_ii = 100.0 * (fi_legi - fi_full) / n
    changed = sum(1 for r in results
                  if r['disposition_full'] != r['disposition_contractless'])
    b4_frac = 100.0 * changed / n
    hc_wrong = [r for r in results if r['jX'] != r['truth'] and r['cX'] >= 700]
    kb2 = (100.0 * sum(1 for r in hc_wrong if r['disposition_full'] == 'WITHHOLD')
           / len(hc_wrong)) if hc_wrong else 0.0
    failed_percept = sum(1 for r in results if not r['percepts_ok'])
    summary = {
        'n_trials': n,
        'n_percept_failed_trials': failed_percept,
        'B5_false_installs': fi_full,
        'B5_false_install_rate_pct': round(b5, 4),
        'B5_bar_pct': 0.5,
        'B5_pass': bool(b5 < 0.5),
        'legii_ablation_fi_legi_only': fi_legi,
        'legii_ablation_reduction_pp': round(abl_ii, 4),
        'legii_ablation_bar_pp': 0.2,
        'legii_ablation_pass': bool(abl_ii >= 0.2),
        'B4_decisions_changed': changed,
        'B4_decisions_changed_pct': round(b4_frac, 4),
        'B4_bar_pct': 10.0,
        'B4_fi_contractless': fi_noc,
        'B4_reduces_false_installs': bool(fi_noc > fi_full),
        'B4_pass': bool(b4_frac >= 10.0 and fi_noc > fi_full),
        'KB2_highconf_wrong': len(hc_wrong),
        'KB2_self_flagged': sum(1 for r in hc_wrong
                                if r['disposition_full'] == 'WITHHOLD'),
        'KB2_self_flag_rate_pct': round(kb2, 4),
        'KB2_bar_pct': 95.0,
        'KB2_pass': bool(kb2 >= 95.0),
        'n_wrong_total': len(wrong),
        'results_sha256': fhash,
        'ledger_sha256': lhash,
        'ledger_final_hash': prev,
    }
    with open(os.path.join(OUTDIR, 'summary.json'), 'w') as f:
        json.dump(summary, f, indent=2, sort_keys=True)
    print(json.dumps(summary, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
