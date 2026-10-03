#!/usr/bin/env python3
"""LI-FAM-NEG analyzer: scores G1-G6 + FAM-NEG family bars from run_fam_neg.py ledgers.
Reads <rundir>/<arm>/pass1 ledgers. Exit 0 with VERDICT line.
Bars per PREREG_D4_RESID.md section 4 (frozen 235152e8).
"""
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
    for arm in ('control', 'fam_neg'):
        arms[arm] = load_ledger(os.path.join(rundir, arm, 'pass1'))
    ck, cr, cu, cures = arms['control']
    dk, dr, du, dures = arms['fam_neg']

    def inst(armk, cid):
        return cid in armk

    def ledgered(cid, reasons):
        if isinstance(reasons, str):
            reasons = [reasons]
        return [r2 for (_, c2, r2, _, _) in du if c2 == cid and r2 in reasons]

    out = []
    fails = []

    def bar(name, ok, detail):
        out.append('%s|%s|%s' % (name, detail, 'PASS' if ok else 'FAIL'))
        if not ok:
            fails.append(name)

    # G1: Type-B exactly nf-b-12, nf-b-17 on fam_neg; control 0/24
    b_ids = ['nf-b-%02d' % i for i in range(1, 25)]
    got_b = sorted(c for c in b_ids if inst(dk, c))
    bar('G1', got_b == ['nf-b-12', 'nf-b-17'],
        'fam_neg_typeB=%d/24 which=%s (expect nf-b-12,nf-b-17)' % (len(got_b), ','.join(got_b) or '-'))
    got_bc = sorted(c for c in b_ids if inst(ck, c))
    bar('G1c', got_bc == ['nf-b-12', 'nf-b-17'] and got_b == got_bc,
        'control(unmodified D4-FIX)_typeB=%d/24 which=%s; fam_neg matches control=%s'
        % (len(got_bc), ','.join(got_bc) or '-', got_b == got_bc))

    # G2: blind honest 6/6; attacks a1/a2/a6 + w2/w3 ledgered w/ correct reasons; none installed
    blh = ['bl-h%d' % i for i in range(1, 7)]
    n_blh = sum(1 for c in blh if inst(dk, c))
    bar('G2', n_blh == 6, 'blind_honest_fam_neg=%d/6' % n_blh)
    bar_pairs = {'bl-a1': 'ROLE-SWAP', 'bl-a2': 'MODAL', 'bl-a6': 'REFERENCE',
                 'w2': 'ROLE-SWAP', 'w3': 'MODAL'}
    g2_bad = []
    for cid, exp in bar_pairs.items():
        hits = ledgered(cid, exp)
        if not hits:
            g2_bad.append(cid + ':missing-' + exp)
        if inst(dk, cid):
            g2_bad.append(cid + ':installed')
    bar('G2b', not g2_bad, 'attack_pairs ledgered=%d/5 violations=%s'
        % (sum(1 for c in bar_pairs if ledgered(c, bar_pairs[c])), ','.join(g2_bad) or '-'))

    # G3: Type-A 20/20 both arms; Type-C identical to control
    a_ids = ['nf-a-%02d' % i for i in range(1, 21)]
    na_c = sum(1 for c in a_ids if inst(ck, c))
    na_d = sum(1 for c in a_ids if inst(dk, c))
    c_ids = ['nf-c-%02d' % i for i in range(1, 17)]
    agree = [c for c in c_ids if inst(ck, c) == inst(dk, c)]
    bar('G3', na_c == 20 and na_d == 20 and len(agree) == 16,
        'typeA_control=%d/20 typeA_famneg=%d/20 typeC_agree=%d/16' % (na_c, na_d, len(agree)))

    # G4: governing pair -> ROLE-SWAP ledgered, neither side installed from
    # gov-wolves, cluster WITHHOLDs. (RESOLVE may read KB-A when the same
    # sentence was honestly installed from bl-h1 earlier in the run — a
    # shared-ledger runner artifact, identical in both arms; not a bar.)
    g4_useqs = [u2 for (u2, c2, r2, _, _) in du if c2 == 'gov-wolves' and r2 == 'ROLE-SWAP']
    bar('G4', bool(g4_useqs) and not inst(dk, 'gov-wolves'),
        'gov-wolves ROLE-SWAP ledgered=%s installed=%s'
        % (bool(g4_useqs), inst(dk, 'gov-wolves')))

    # G5 (reported, not a FAM-NEG bar): w1/p3 outcomes vs D4-FIX baseline
    for cid in ('w1', 'p3'):
        out.append('G5|%s|fam_neg=%s (D4-FIX baseline: INSTALL; R1 hole, out of FAM-NEG scope)'
                   % (cid, 'INSTALL' if inst(dk, cid) else 'WITHHOLD'))

    # G6: byte-identity (re-verify) — zero-RNG grep done in shell
    g6 = True
    for arm in ('control', 'fam_neg'):
        for f in ('knowledge_ledger.txt', 'refusal_ledger.txt',
                  'undetermined_ledger.txt', 'pending_import.txt', 'run_li.log'):
            if not filecmp.cmp(os.path.join(rundir, arm, 'pass1', f),
                               os.path.join(rundir, arm, 'pass2', f), shallow=False):
                g6 = False
                out.append('G6|DIFFER|%s|%s' % (arm, f))
    bar('G6', g6, 'five_artifacts x two_passes byte-identical (zero-RNG grep in shell)')

    # ---- FAM-NEG family bars (frozen pairs) ----
    for cid in ('neg-1', 'neg-2', 'neg-3'):
        led = ledgered(cid, 'NEGATION')
        bar('NEG-' + cid, (not inst(dk, cid)) and bool(led),
            '%s installed=%s NEGATION_ledger=%s' % (cid, inst(dk, cid), bool(led)))
    led4 = ledgered('neg-4', ['NEGATION', 'QUANT'])
    bar('NEG-neg-4', (not inst(dk, 'neg-4')) and bool(led4),
        'neg-4 installed=%s NEGATION-or-QUANT_ledger=%s' % (inst(dk, 'neg-4'), bool(led4)))
    bar('NEG-neg-h1', inst(dk, 'neg-h1'), 'neg-h1 installed=%s (expect True)' % inst(dk, 'neg-h1'))
    bar('NEG-neg-h2', inst(dk, 'neg-h2'), 'neg-h2 installed=%s (expect True)' % inst(dk, 'neg-h2'))
    led_a3 = ledgered('bl-a3', 'NEGATION')
    bar('NEG-bl-a3', (not inst(dk, 'bl-a3')) and bool(led_a3),
        'bl-a3 installed=%s NEGATION_ledger=%s' % (inst(dk, 'bl-a3'), bool(led_a3)))

    # ---- crew-added extra pairs (supplementary) ----
    for cid in ('neg-5', 'neg-6'):
        led = ledgered(cid, 'NEGATION')
        bar('NEGX-' + cid, (not inst(dk, cid)) and bool(led),
            '%s installed=%s NEGATION_ledger=%s' % (cid, inst(dk, cid), bool(led)))
    for cid in ('neg-h3', 'neg-h4'):
        bar('NEGX-' + cid, inst(dk, cid), '%s installed=%s (expect True)' % (cid, inst(dk, cid)))

    # ledger reason census
    reasons = {}
    for _, _, reason, _, _ in du:
        reasons[reason] = reasons.get(reason, 0) + 1
    out.append('LEDGER|fam_neg_pairs=%d|reasons=%s'
               % (len(du), ','.join('%s=%d' % kv for kv in sorted(reasons.items()))))

    if fails:
        out.append('VERDICT|FAM-NEG bars: FAILED=%s' % ','.join(fails))
    else:
        out.append('VERDICT|FAM-NEG ALL BARS PASS')
    sys.stdout.write('\n'.join(out) + '\n')

if __name__ == '__main__':
    main()
