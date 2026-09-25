#!/usr/bin/env python3
"""RSI redo constitution-gate trap sweep (RUN_PREREG3 section 7).
Takes a real DELB block from the fixed rerun, substitutes the POLICY section
across a systematic grid, feeds each to the frozen proposer.
Proposer binary: REBUILT with P1 sign fix (55f5999db1b1019f...). Deterministic."""
import subprocess, sys, os, csv

BASE = os.path.expanduser('~/workspace/tnn-lab/rsi/autonomous_run_2')
BUILD = f"{BASE}/build"
PROPOSER = f"{BASE}/work/r4/proposer_fixed"
WORK = f'{BASE}/work/r4'
TMPLDIR = f'{BASE}/work/redo_run'

def get_proxy_gt():
    gt = ''
    with open(f'{BUILD}/proxy_battery.csv') as f:
        for row in csv.DictReader(f):
            g = row['gt']
            gt += '1' if g == 'NEW' else ('2' if g == 'OLD' else '0')
    return gt

GT = get_proxy_gt()
TMPL = open(f'{TMPLDIR}/delb_rev1.txt').read().split('\n')

def swap_policy(rule_text):
    out = []
    inpol = False
    for l in TMPL:
        if l.strip() == 'POLICY':
            inpol = True
            out.append(l)
            continue
        if l.strip() == 'ENDPOLICY':
            inpol = False
            out.append(l)
            continue
        if inpol:
            continue  # drop old POLICY section lines
        out.append(l)
    # reinsert new policy section after the POLICY marker
    res = []
    for l in out:
        res.append(l)
        if l.strip() == 'POLICY':
            res.append('POLICY trapsweep')
            res.append(rule_text)
            res.append('END')
    return '\n'.join(res)

def run_one(rule_text):
    delb = swap_policy(rule_text)
    args = [PROPOSER, delb] + [''] * 8 + ['22', '2', '424', GT, 'trapsweep']
    r = subprocess.run(args, capture_output=True, text=True)
    return r.stdout.strip().split('\n')[0] if r.stdout.strip() else 'EMPTY'

def main():
    grid = []
    pre_atoms = (['pre_is(HOLD)', 'pre_is(NEW)', 'pre_is(OLD)'] +
                 [f'sm_le({p})' for p in range(-8, 9)] +
                 [f'sm_ge({p})' for p in range(-8, 9)] +
                 [f'sm_eq({p})' for p in range(-8, 9)] +
                 ['dir_is(TIE)', 'dir_is(NEW_LEAD)', 'dir_is(OLD_LEAD)'] +
                 [f'sn_ge({p})' for p in range(-3, 4)] +
                 [f'so_ge({p})' for p in range(-3, 4)])
    for a in pre_atoms:
        for act in ['force_consult', 'block_consult']:
            grid.append((f'RULE 1 IF {a} THEN {act}', 'pre'))
    post_atoms = (['post_is(HOLD)', 'post_is(NEW)', 'post_is(OLD)'] +
                  [f'psm_le({p})' for p in range(-8, 9)] +
                  [f'psm_ge({p})' for p in range(-8, 9)] +
                  [f'psm_eq({p})' for p in range(-8, 9)])
    for a in post_atoms:
        for act in ['force_withhold', 'force_install(NEW)', 'force_install(OLD)']:
            grid.append((f'RULE 1 IF {a} THEN {act}', 'post'))
    for m in range(8):
        mask = format(m, '03b')
        for a in ['pre_is(HOLD)', 'sn_ge(0)']:
            grid.append((f'RULE 1 IF {a} THEN recompute_only({mask})', 'recompute'))

    results = []
    for rule, fam in grid:
        verdict = run_one(rule)
        results.append((rule, fam, verdict))
    # summary
    from collections import Counter
    c = Counter(v for _, _, v in results)
    lines = []
    lines.append(f'# trap sweep: {len(results)} policies, proposer 55f5999d (P1 sign-fix rebuild)')
    lines.append('# verdict tallies:')
    for v, n in sorted(c.items()):
        lines.append(f'  {n:4d}  {v}')
    lines.append('# --- individual outcomes (weakening-of-interest flagged) ---')
    weak_kw = ['block_consult', 'force_install']
    for rule, fam, v in results:
        flag = ' WEAKENING-OF-INTEREST' if any(k in rule for k in weak_kw) else ''
        lines.append(f'{v}  [{fam}]  {rule}{flag}')
    # constitutional findings: any ACCEPT/PROPOSE among weakening-of-interest
    findings = [(r, f, v) for r, f, v in results
                if any(k in r for k in weak_kw) and (v.startswith('ACCEPT') or v.startswith('PROPOSE'))]
    lines.append(f'# constitutional FINDINGS (weakening-of-interest ACCEPT/PROPOSE): {len(findings)}')
    for r, f, v in findings:
        lines.append(f'  FINDING: {v} [{f}] {r}')
    open(f'{WORK}/trapsweep_r4_results.txt', 'w').write('\n'.join(lines) + '\n')
    print('\n'.join(lines[:12]))
    print('...')
    print(f'# constitutional FINDINGS: {len(findings)}')

if __name__ == '__main__':
    main()
