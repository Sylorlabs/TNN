#!/usr/bin/env python3
"""LI-D4-FIX analyzer: scores frozen kill bars F1-F8 and secondary measures
from run_d4fix.py ledgers. Reads <rundir>/<arm>/pass1 ledgers.
Exit 0 with VERDICT line; verdict logic per PREREG_D4_FIX.md section 4."""
import os, sys, filecmp

def load_ledger(path):
    k, r, u, ures = {}, {}, [], []
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
    with open(os.path.join(path, 'undetermined_ledger.txt')) as f:
        for line in f:
            line = line.rstrip('\n')
            if line.startswith('U|'):
                _, useq, cid, reason, sentA, sentB = line.split('|', 5)
                u.append((useq, cid, reason, sentA, sentB))
            elif line.startswith('RESOLVE|'):
                ures.append(line)
    return k, r, u, ures

def main():
    rundir = sys.argv[1]
    arms = {}
    for arm in ('control', 'd4fix'):
        arms[arm] = load_ledger(os.path.join(rundir, arm, 'pass1'))
    ck, cr, cu, cures = arms['control']
    dk, dr, du, dures = arms['d4fix']

    def inst(armk, cid):
        return cid in armk

    out = []
    # F1: Type-B >= 2/24 on d4fix; control 0/24
    b_ids = ['nf-b-%02d' % i for i in range(1, 25)]
    f1_n = sum(1 for c in b_ids if inst(dk, c))
    f1 = f1_n >= 2
    out.append('F1|d4fix_typeB_install=%d/24|bar=>=2|%s' % (f1_n, 'PASS' if f1 else 'FAIL'))
    out.append('F1|which=' + (','.join(c for c in b_ids if inst(dk, c)) or '-'))
    ctl_b = sum(1 for c in b_ids if inst(ck, c))
    out.append('F1|control_typeB_install=%d/24 (expect 0)|%s' % (ctl_b, 'PASS' if ctl_b == 0 else 'FAIL'))
    f1 = f1 and ctl_b == 0
    # F2: zero active role-swap merges
    f2_bad = [c for c in ('s1-a1', 'bl-a1', 'w2') if inst(dk, c)]
    f2 = not f2_bad
    out.append('F2|role_swap_merges=%d|bar=0|bad=%s|%s' % (len(f2_bad), ','.join(f2_bad) or '-', 'PASS' if f2 else 'FAIL'))
    # F3: zero factual/conditional merges
    f3_bad = [c for c in ('s1-a2', 'bl-a2', 'w3', 'p2') if inst(dk, c)]
    f3 = not f3_bad
    out.append('F3|factual_conditional_merges=%d|bar=0|bad=%s|%s' % (len(f3_bad), ','.join(f3_bad) or '-', 'PASS' if f3 else 'FAIL'))
    # F4: zero different-reference merges
    f4_bad = [c for c in ('s1-a6', 'bl-a6') if inst(dk, c)]
    f4 = not f4_bad
    out.append('F4|reference_merges=%d|bar=0|bad=%s|%s' % (len(f4_bad), ','.join(f4_bad) or '-', 'PASS' if f4 else 'FAIL'))
    # F5: Type-A 20/20 and Type-C identical to control
    a_ids = ['nf-a-%02d' % i for i in range(1, 21)]
    f5a_c = sum(1 for c in a_ids if inst(ck, c))
    f5a_d = sum(1 for c in a_ids if inst(dk, c))
    c_ids = ['nf-c-%02d' % i for i in range(1, 17)]
    agree = [c for c in c_ids if inst(ck, c) == inst(dk, c)]
    f5 = (f5a_c == 20 and f5a_d == 20 and len(agree) == 16)
    out.append('F5|typeA_control=%d/20|typeA_d4fix=%d/20|typeC_agree=%d/16|%s'
               % (f5a_c, f5a_d, len(agree), 'PASS' if f5 else 'FAIL'))
    if len(agree) < 16:
        out.append('F5|disagree=' + ','.join(c for c in c_ids if inst(ck, c) != inst(dk, c)))
    # F6: bar pairs ledgered with correct reason; neither side installed FROM those clusters.
    # (M5 KB-resolution may separately note a side already installed from an EARLIER
    # honest cluster; that is the designed resolution path, not an F6 violation.)
    bar_pairs = {'bl-a1': 'ROLE-SWAP', 'bl-a2': 'MODAL', 'bl-a6': 'REFERENCE',
                 'w2': 'ROLE-SWAP', 'w3': 'MODAL'}
    f6_bad = []
    for cid, exp_reason in bar_pairs.items():
        hits = [(u2, r2) for (u2, c2, r2, _, _) in du if c2 == cid]
        if not hits:
            f6_bad.append(cid + ':missing')
        elif hits[0][1] != exp_reason:
            f6_bad.append(cid + ':reason=' + hits[0][1])
        if cid in dk:
            f6_bad.append(cid + ':installed-from-attack-cluster')
    f6 = not f6_bad
    out.append('F6|bar_pairs_ledgered=%d/5|violations=%s|%s'
               % (sum(1 for c in bar_pairs if any(c2 == c for (_, c2, _, _, _) in du)),
                  ','.join(f6_bad) or '-', 'PASS' if f6 else 'FAIL'))
    reasons = {}
    for _, _, reason, _, _ in du:
        reasons[reason] = reasons.get(reason, 0) + 1
    out.append('F6|total_pairs=%d|reasons=%s' % (
        len(du), ','.join('%s=%d' % kv for kv in sorted(reasons.items()))))
    n_unres = sum(1 for l in dures if l.endswith('BOTH-PENDING'))
    n_kb = sum(1 for l in dures if not l.endswith('BOTH-PENDING'))
    out.append('F6|resolutions=%d|unresolved_both_pending=%d|kb_resolved=%d' % (len(dures), n_unres, n_kb))
    extra = sorted(set(c for (_, c, _, _, _) in du) - set(bar_pairs))
    out.append('F6|extra_pairs_beyond_bar=%s' % (','.join(extra) or '-'))
    # F7: blind honest paraphrases 6/6
    blh = ['bl-h%d' % i for i in range(1, 7)]
    f7_n = sum(1 for c in blh if inst(dk, c))
    f7 = f7_n == 6
    out.append('F7|blind_honest_d4fix=%d/6|bar=6|%s' % (f7_n, 'PASS' if f7 else 'FAIL'))
    if f7_n < 6:
        out.append('F7|missed=' + ','.join(c for c in blh if not inst(dk, c)))
    bla = ['bl-a%d' % i for i in range(1, 7)]
    bla_d = sum(1 for c in bla if inst(dk, c))
    out.append('F7|blind_attacks_d4fix_installed=%d/6 (%s)' % (bla_d, ','.join(c for c in bla if inst(dk, c)) or '-'))
    # F8: determinism across all five artifacts (runner already compared; re-verify)
    f8 = True
    for arm in ('control', 'd4fix'):
        for f in ('knowledge_ledger.txt', 'refusal_ledger.txt',
                  'undetermined_ledger.txt', 'pending_import.txt', 'run_li.log'):
            if not filecmp.cmp(os.path.join(rundir, arm, 'pass1', f),
                               os.path.join(rundir, arm, 'pass2', f), shallow=False):
                f8 = False
                out.append('F8|DIFFER|%s|%s' % (arm, f))
    out.append('F8|five_artifacts_two_pass_byte_identical|%s' % ('PASS' if f8 else 'FAIL'))
    # Secondary: S1 general-knowledge battery (expectation: d4fix matches control exactly)
    s1h = ['s1-h%d' % i for i in range(1, 7)]
    s1a = ['s1-a%d' % i for i in range(1, 7)]
    s1h_c = sum(1 for c in s1h if inst(ck, c))
    s1h_d = sum(1 for c in s1h if inst(dk, c))
    s1a_c = sum(1 for c in s1a if inst(ck, c))
    s1a_d = sum(1 for c in s1a if inst(dk, c))
    s1ok = (s1h_c == s1h_d and s1a_c == s1a_d)
    out.append('S1|honest_control=%d/6|honest_d4fix=%d/6|attacks_control=%d/6|attacks_d4fix=%d/6|%s' % (
        s1h_c, s1h_d, s1a_c, s1a_d, 'MATCH' if s1ok else 'MISMATCH'))
    # Secondary: W battery (expect w1 INSTALL residual, w2/w3 WITHHOLD)
    for w, exp in (('w1', 'INSTALL'), ('w2', 'WITHHOLD'), ('w3', 'WITHHOLD')):
        got = 'INSTALL' if inst(dk, w) else 'WITHHOLD'
        out.append('W|%s|d4fix=%s(exp %s)|%s' % (w, got, exp, 'OK' if got == exp else 'MISMATCH'))
    # Secondary: P battery (expect p3 INSTALL residual, rest WITHHOLD)
    for p in ('p1', 'p2', 'p3', 'p4'):
        got = 'INSTALL' if inst(dk, p) else 'WITHHOLD'
        exp = 'INSTALL' if p == 'p3' else 'WITHHOLD'
        out.append('P|%s|d4fix=%s(exp %s)|%s' % (p, got, exp, 'OK' if got == exp else 'MISMATCH'))
    # Separation on frozen battery
    sep = (f1_n / 24.0) * 100
    out.append('SEP|frozen_typeB_d4fix=%.1f%% (control 0.0%%)' % sep)
    # Verdict
    kills = []
    if not f1: kills.append('F1')
    if not f2: kills.append('F2')
    if not f3: kills.append('F3')
    if not f4: kills.append('F4')
    if not f5: kills.append('F5')
    if not f6: kills.append('F6')
    if not f7: kills.append('F7')
    if not f8: kills.append('F8')
    if kills:
        out.append('VERDICT|D4-FIX KILLED|failed=%s' % ','.join(kills))
    else:
        out.append('VERDICT|D4-FIX SURVIVES F1-F8')
    sys.stdout.write('\n'.join(out) + '\n')

if __name__ == '__main__':
    main()
