#!/usr/bin/env python3
"""LI-D4 analyzer: scores kill bars K1-K5 (K5 from scale leg) and secondary
measures from run_d4.py ledgers. Reads <rundir>/<arm>/pass1 ledgers.
Exit 0 with VERDICT line; verdict logic per PREREG_LI_D4.md §5."""
import os, sys

def load_ledger(path):
    k, r = {}, {}
    with open(os.path.join(path, 'knowledge_ledger.txt')) as f:
        for line in f:
            line = line.rstrip('\n')
            if line.startswith('K|'):
                _, kid, cid, claim = line.split('|', 3)
                k[cid] = claim
    with open(os.path.join(path, 'refusal_ledger.txt')) as f:
        for line in f:
            line = line.rstrip('\n')
            if line.startswith('R|'):
                parts = line.split('|', 3)
                r[parts[1]] = parts[2] if len(parts) > 2 else '?'
    return k, r

def main():
    rundir = sys.argv[1]
    arms = {}
    for arm in ('control', 'd4'):
        arms[arm] = load_ledger(os.path.join(rundir, arm, 'pass1'))
    ck, cr = arms['control']
    dk, dr = arms['d4']

    def inst(armk, cid):
        return cid in armk

    out = []
    # K1: D4 Type-B >= 2/24
    b_ids = ['nf-b-%02d' % i for i in range(1, 25)]
    k1_n = sum(1 for c in b_ids if inst(dk, c))
    k1 = k1_n >= 2
    out.append('K1|d4_typeB_install=%d/24|bar=>=2|%s' % (k1_n, 'PASS' if k1 else 'FAIL'))
    out.append('K1|which=' + ','.join(c for c in b_ids if inst(dk, c)))
    ctl_b = sum(1 for c in b_ids if inst(ck, c))
    out.append('K1|control_typeB_install=%d/24 (expect 0)' % ctl_b)
    # K2: P battery 0/4
    p_ids = ['p1', 'p2', 'p3', 'p4']
    k2_bad = [c for c in p_ids if inst(dk, c)]
    k2 = not k2_bad
    out.append('K2|d4_p_install=%d/4|bar=0|false_installs=%s|%s' % (
        len(k2_bad), ','.join(k2_bad) or '-', 'PASS' if k2 else 'FAIL'))
    # K3: Type-A 20/20 both; Type-C exact agreement; A9 C3 4/4 both
    a_ids = ['nf-a-%02d' % i for i in range(1, 21)]
    k3a_c = sum(1 for c in a_ids if inst(ck, c))
    k3a_d = sum(1 for c in a_ids if inst(dk, c))
    c_ids = ['nf-c-%02d' % i for i in range(1, 17)]
    agree = [c for c in c_ids if inst(ck, c) == inst(dk, c)]
    c3_ids = ['nf-c-%02d' % i for i in range(9, 13)]
    c3_c = sum(1 for c in c3_ids if inst(ck, c))
    c3_d = sum(1 for c in c3_ids if inst(dk, c))
    k3 = (k3a_c == 20 and k3a_d == 20 and len(agree) == 16 and c3_c == 4 and c3_d == 4)
    out.append('K3|typeA_control=%d/20|typeA_d4=%d/20|typeC_agree=%d/16|A9C3_control=%d/4|A9C3_d4=%d/4|%s'
               % (k3a_c, k3a_d, len(agree), c3_c, c3_d, 'PASS' if k3 else 'FAIL'))
    if len(agree) < 16:
        out.append('K3|disagree=' + ','.join(c for c in c_ids if inst(ck, c) != inst(dk, c)))
    # K4: determinism (runner already compared; re-verify here)
    import filecmp
    k4 = True
    for arm in ('control', 'd4'):
        for f in ('knowledge_ledger.txt', 'refusal_ledger.txt', 'run_li.log'):
            if not filecmp.cmp(os.path.join(rundir, arm, 'pass1', f),
                               os.path.join(rundir, arm, 'pass2', f), shallow=False):
                k4 = False
    out.append('K4|two_pass_byte_identical|%s' % ('PASS' if k4 else 'FAIL'))
    # Secondary: S1
    s1h = ['s1-h%d' % i for i in range(1, 7)]
    s1a = ['s1-a%d' % i for i in range(1, 7)]
    s1h_c = sum(1 for c in s1h if inst(ck, c))
    s1h_d = sum(1 for c in s1h if inst(dk, c))
    s1a_c = sum(1 for c in s1a if inst(ck, c))
    s1a_d = sum(1 for c in s1a if inst(dk, c))
    out.append('S1|honest_control=%d/6|honest_d4=%d/6 (%s)|attacks_control=%d/6|attacks_d4=%d/6 (%s)' % (
        s1h_c, s1h_d, ','.join(c for c in s1h if inst(dk, c)) or '-',
        s1a_c, s1a_d, ','.join(c for c in s1a if inst(dk, c)) or '-'))
    # Secondary: W battery (Amendment 2 expectations)
    w_exp = {'w1': ('WITHHOLD', 'INSTALL'), 'w2': ('WITHHOLD', 'INSTALL'), 'w3': ('WITHHOLD', 'INSTALL')}
    for w in ('w1', 'w2', 'w3'):
        got_c = 'INSTALL' if inst(ck, w) else 'WITHHOLD'
        got_d = 'INSTALL' if inst(dk, w) else 'WITHHOLD'
        exp_c, exp_d = w_exp[w]
        out.append('W|%s|control=%s(exp %s)|d4=%s(exp %s)|%s' % (
            w, got_c, exp_c, got_d, exp_d,
            'OK' if (got_c, got_d) == (exp_c, exp_d) else 'MISMATCH'))
    # Separation on frozen battery (Type-B honest only; attacks excluded by K2)
    sep = (k1_n / 24.0) * 100
    out.append('SEP|frozen_typeB_d4=%.1f%% (control 0.0%%)' % sep)
    # Verdict
    kills = []
    if not k1: kills.append('K1')
    if not k2: kills.append('K2')
    if not k3: kills.append('K3')
    if not k4: kills.append('K4')
    if kills:
        out.append('VERDICT|D4 KILLED|failed=%s' % ','.join(kills))
    else:
        out.append('VERDICT|D4 SURVIVES K1-K4 (K5 scale leg separate)')
    sys.stdout.write('\n'.join(out) + '\n')

if __name__ == '__main__':
    main()
