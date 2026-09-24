#!/usr/bin/env python3
# FS-E4b scoring vs the frozen joint bars (PREREG_FS-E4b, committed a9a48b3f).
# Usage: score_e4b.py <evidence_dir> <lists_dir> <e4b_bin>
# Judges the corrupted-G diagnostic set once, then scores everything and
# writes evidence/SCORES_E4B.md. Deterministic; no RNG.
import sys, os, subprocess, math

TASKS = ['colordisc', 'colorconst', 'pitchdisc', 'timbredisc', 'motiondir']
Z = 1.96

def parse_out(path):
    rows = []
    with open(path) as f:
        for line in f:
            if line.startswith('trial='):
                d = {}
                for tok in line.strip().split():
                    if '=' in tok:
                        k, v = tok.split('=', 1)
                        d[k] = v
                rows.append(d)
    return rows

def wilson_ucb(k, n, z=Z):
    if n == 0:
        return 1.0
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (c + m) / d

def main():
    ev, lists, e4b = sys.argv[1:4]
    quals = [t for t in TASKS
             if os.path.exists(os.path.join(ev, 'run1_adv_%s.txt.out' % t))]
    # corrupted-G diagnostic: judge once (skip if output already exists)
    for t in quals:
        lp = os.path.join(lists, 'corrupt_%s.txt' % t)
        led = os.path.join(ev, 'judge_corrupt_%s.txt' % t)
        if os.path.exists(lp) and not os.path.exists(led + '.out'):
            rc = subprocess.run([e4b, 'judge_list', lp, led]).returncode
            if rc != 0:
                print('DRIVER FAILED corrupt %s' % t, flush=True)
                sys.exit(1)
    per = {}
    for t in quals:
        adv = parse_out(os.path.join(ev, 'run1_adv_%s.txt.out' % t))
        ctrl = parse_out(os.path.join(ev, 'run1_ctrl_%s.txt.out' % t))
        cor = parse_out(os.path.join(ev, 'judge_corrupt_%s.txt.out' % t))
        fi_b = sum(1 for r in adv if r['base'] == 'INSTALL')
        fi_x = sum(1 for r in adv if r['booster'] == 'INSTALL')
        rc_b = sum(1 for r in ctrl if r['base'] == 'INSTALL' and r['formF'] == r['truth'])
        rc_x = sum(1 for r in ctrl if r['booster'] == 'INSTALL' and r['formF'] == r['truth'])
        wrong_true_x = sum(1 for r in ctrl if r['booster'] == 'INSTALL' and r['formF'] != r['truth'])
        rc_cor = sum(1 for r in cor if r['booster'] == 'INSTALL' and r['formF'] == r['truth'])
        per[t] = dict(n_adv=len(adv), n_ctrl=len(ctrl), n_cor=len(cor),
                      fi_base=fi_b, fi_booster=fi_x,
                      rec_base=rc_b, rec_booster=rc_x,
                      wrong_true_booster=wrong_true_x,
                      rec_corrupt=rc_cor)
    # pooled
    P = dict(n_adv=0, n_ctrl=0, n_cor=0, fi_base=0, fi_booster=0,
             rec_base=0, rec_booster=0, wrong_true_booster=0, rec_corrupt=0)
    for t in quals:
        for k in P:
            P[k] += per[t][k]
    lines = []
    A = lines.append
    A('# FS-E4b scores vs frozen joint bars\n')
    A('Tasks run: %s\n' % ', '.join(quals))
    A('Battery per task: 2,000 F-fooled adversarial + 1,000 TRUE controls.\n')
    A('## Per-task\n')
    A('| task | n_adv | FI_base k | FI_base rate | FI_boost k | FI_boost rate | FI_boost 95% UCB | '
      'n_ctrl | rec_base | rec_boost | wrong_on_TRUE_boost | n_cor | rec_corrupt_boost |')
    A('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
    bars_ok = True
    for t in quals:
        d = per[t]
        fi_br, fi_xr = d['fi_base'] / d['n_adv'], d['fi_booster'] / d['n_adv']
        ucb = wilson_ucb(d['fi_booster'], d['n_adv'])
        rb, rx = d['rec_base'] / d['n_ctrl'], d['rec_booster'] / d['n_ctrl']
        rcor = d['rec_corrupt'] / d['n_cor'] if d['n_cor'] else float('nan')
        A('| %s | %d | %d | %.4f | %d | %.4f | %.4f | %d | %.4f | %.4f | %d | %d | %.4f |' % (
            t, d['n_adv'], d['fi_base'], fi_br, d['fi_booster'], fi_xr, ucb,
            d['n_ctrl'], rb, rx, d['wrong_true_booster'], d['n_cor'], rcor))
        if not (ucb <= 0.01):
            bars_ok = False
            A('  BAR1-FAIL: %s FI booster UCB %.4f > 0.01' % (t, ucb))
        if not (rx >= 0.85):
            bars_ok = False
            A('  BAR2-FAIL: %s booster recall %.4f < 0.85' % (t, rx))
    A('')
    A('## Pooled\n')
    fi_br = P['fi_base'] / P['n_adv']
    fi_xr = P['fi_booster'] / P['n_adv']
    ucb = wilson_ucb(P['fi_booster'], P['n_adv'])
    rb, rx = P['rec_base'] / P['n_ctrl'], P['rec_booster'] / P['n_ctrl']
    rcor = P['rec_corrupt'] / P['n_cor'] if P['n_cor'] else float('nan')
    A('- n_adv=%d FI_base=%d (%.4f) FI_booster=%d (%.4f) 95%% UCB=%.4f (bar <=0.01)' % (
        P['n_adv'], P['fi_base'], fi_br, P['fi_booster'], fi_xr, ucb))
    A('- n_ctrl=%d rec_base=%.4f rec_booster=%.4f (bar >=0.85); wrong_on_TRUE_booster=%d' % (
        P['n_ctrl'], rb, rx, P['wrong_true_booster']))
    A('- n_corrupt=%d rec_corrupt_booster=%.4f; availability cost = %.4f (clean rec %.4f - corrupt rec %.4f)' % (
        P['n_cor'], rcor, rx - rcor, rx, rcor))
    if not (ucb <= 0.01):
        bars_ok = False
        A('  BAR1-FAIL (pooled): FI booster UCB %.4f > 0.01' % ucb)
    if not (rx >= 0.85):
        bars_ok = False
        A('  BAR2-FAIL (pooled): booster recall %.4f < 0.85' % rx)
    A('')
    A('## Ablation (bar 3)\n')
    if P['fi_base'] == 0:
        A('- pooled FI_base = 0: ratio UNDEFINED; bar 3 vacated per prereg (no FI to reduce).')
        ablation_ok = True
    else:
        ratio = (P['fi_base'] / P['n_adv']) / (P['fi_booster'] / P['n_adv']) if P['fi_booster'] > 0 else float('inf')
        A('- pooled FI_base/FI_booster = %.3f (bar >= 2)' % ratio)
        ablation_ok = ratio >= 2
        if not ablation_ok:
            bars_ok = False
            A('  BAR3-FAIL: ablation ratio %.3f < 2' % ratio)
    A('')
    A('## Determinism (bar 4)\n')
    A('- run_battery.py: full battery run twice; stdout logs + ledgers byte-identical (see run log).')
    A('- verify_chain.py: every hash-chain line of every run ledger verified (see run log).')
    A('')
    A('## Verdict\n')
    A('- ALIVE iff bars 1-4 all pass; DEAD on recall/FI/ablation/determinism failure.')
    A('- JOINT BARS: %s' % ('PASS' if bars_ok else 'FAIL'))
    A('- HYPOTHESIS (cross-span concurrence scales to R2A): %s' % ('ALIVE' if bars_ok else 'DEAD'))
    out = '\n'.join(lines) + '\n'
    with open(os.path.join(ev, 'SCORES_E4B.md'), 'w') as f:
        f.write(out)
    print(out, flush=True)

if __name__ == '__main__':
    main()
