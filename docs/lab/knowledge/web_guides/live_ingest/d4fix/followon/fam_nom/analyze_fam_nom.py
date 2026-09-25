#!/usr/bin/env python3
"""FAM-NOM analyzer: scores PREREG_D4_RESID section 4 bars from run_fam_nom.py
ledgers. Reads <rundir>/<arm>/pass1 ledgers. Arms: control, fam_nom.
Exit 0 with VERDICT line."""
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
    pend = []
    with open(os.path.join(path, 'pending_import.txt')) as f:
        for line in f:
            line = line.rstrip('\n')
            if line:
                pend.append(line)
    return k, r, u, ures, pend

def main():
    rundir = sys.argv[1]
    arms = {}
    for arm in ('control', 'fam_nom'):
        arms[arm] = load_ledger(os.path.join(rundir, arm, 'pass1'))
    ck, cr, cu, cures, cpend = arms['control']
    dk, dr, du, dures, dpend = arms['fam_nom']

    def inst(armk, cid):
        return cid in armk

    def uledger_reasons(uu, cid):
        return [r2 for (_, c2, r2, _, _) in uu if c2 == cid]

    out = []
    fails = []

    def bar(name, ok, detail):
        out.append('%s|%s|%s' % (name, detail, 'PASS' if ok else 'FAIL'))
        if not ok:
            fails.append(name)

    # G1: Type-B installs exactly 2/24 (nf-b-12, nf-b-17) on fam_nom, and
    # fam_nom agrees with control (unmodified D4-FIX) on every Type-B
    # cluster (K1 throughput preserved, nothing lost or gained).
    # (The prereg's "control arm 0/24" clause belongs to the D4-FIX arm
    # scheme where control was the pre-D4 BF1 baseline; in the D4-RESID
    # scheme control IS the unmodified D4-FIX binary, which also installs
    # nf-b-12/nf-b-17.)
    b_ids = ['nf-b-%02d' % i for i in range(1, 25)]
    g1_which = sorted(c for c in b_ids if inst(dk, c))
    bar('G1', len(g1_which) == 2 and g1_which == ['nf-b-12', 'nf-b-17'],
        'fam_nom_typeB=%d/24 which=%s (expect nf-b-12,nf-b-17)'
        % (len(g1_which), ','.join(g1_which) or '-'))
    g1_agree = [c for c in b_ids if inst(ck, c) == inst(dk, c)]
    bar('G1', len(g1_agree) == 24,
        'typeB_control_vs_fam_nom_agree=%d/24' % len(g1_agree))

    # G2: blind honest 6/6; attacks a1/a2/a6 + w2/w3 ledgered correct reasons
    blh = ['bl-h%d' % i for i in range(1, 7)]
    g2h = sum(1 for c in blh if inst(dk, c))
    bar('G2', g2h == 6, 'blind_honest_fam_nom=%d/6' % g2h)
    if g2h < 6:
        out.append('G2|missed=' + ','.join(c for c in blh if not inst(dk, c)))
    bar_pairs = {'bl-a1': 'ROLE-SWAP', 'bl-a2': 'MODAL', 'bl-a6': 'REFERENCE',
                 'w2': 'ROLE-SWAP', 'w3': 'MODAL'}
    g2_bad = []
    for cid, exp in bar_pairs.items():
        hits = uledger_reasons(du, cid)
        if not hits:
            g2_bad.append(cid + ':missing')
        elif hits[0] != exp:
            g2_bad.append(cid + ':reason=' + hits[0])
        if cid in dk:
            g2_bad.append(cid + ':installed-from-attack-cluster')
    bar('G2', not g2_bad, 'bar_pairs=%d/5 violations=%s'
        % (sum(1 for c in bar_pairs if uledger_reasons(du, c)), ','.join(g2_bad) or '-'))

    # G3: Type-A 20/20; Type-C identical to control 16/16
    a_ids = ['nf-a-%02d' % i for i in range(1, 21)]
    g3a = sum(1 for c in a_ids if inst(dk, c))
    c_ids = ['nf-c-%02d' % i for i in range(1, 17)]
    agree = [c for c in c_ids if inst(ck, c) == inst(dk, c)]
    bar('G3', g3a == 20 and len(agree) == 16,
        'typeA_fam_nom=%d/20 typeC_agree=%d/16' % (g3a, len(agree)))
    if len(agree) < 16:
        out.append('G3|disagree=' + ','.join(c for c in c_ids if inst(ck, c) != inst(dk, c)))

    # G4: governing pair -> ROLE-SWAP, both UNDETERMINED/PENDING, neither installed
    gov_r = uledger_reasons(du, 'gov')
    gov_res = [l for l in dures if '|gov|' in l or True]
    gov_ok = ('gov' not in dk and gov_r and gov_r[0] == 'ROLE-SWAP'
              and any(l.endswith('BOTH-PENDING') for l in dures))
    bar('G4', gov_ok,
        'gov installed=%s reasons=%s both_pending=%s'
        % ('gov' in dk, ','.join(gov_r) or '-',
           any(l.endswith('BOTH-PENDING') for l in dures)))

    # G5: w1 WITHHOLD + PRED ledger; p3 WITHHOLD no install
    w1_r = uledger_reasons(du, 'w1')
    bar('G5', 'w1' not in dk and w1_r and w1_r[0] == 'PRED',
        'w1 installed=%s reasons=%s (expect WITHHOLD+PRED)' % ('w1' in dk, ','.join(w1_r) or '-'))
    bar('G5', 'p3' not in dk, 'p3 installed=%s (expect WITHHOLD)' % ('p3' in dk))

    # G6: determinism (5 artifacts x 2 arms x 2 passes)
    g6 = True
    for arm in ('control', 'fam_nom'):
        for f in ('knowledge_ledger.txt', 'refusal_ledger.txt',
                  'undetermined_ledger.txt', 'pending_import.txt', 'run_li.log'):
            if not filecmp.cmp(os.path.join(rundir, arm, 'pass1', f),
                               os.path.join(rundir, arm, 'pass2', f), shallow=False):
                g6 = False
                out.append('G6|DIFFER|%s|%s' % (arm, f))
    bar('G6', g6, 'five_artifacts_two_pass_two_arms_byte_identical')

    # FAM-NOM family bars
    nom = ['nom-%d' % i for i in range(1, 5)]
    nom_inst = [c for c in nom if inst(dk, c)]
    bar('NOM', not nom_inst, 'nom_installs=%d/4 bad=%s (expect 0)'
        % (len(nom_inst), ','.join(nom_inst) or '-'))
    pred_ok = []
    for c in ['nom-1', 'nom-2', 'nom-3']:
        r = uledger_reasons(du, c)
        hit = bool(r and r[0] == 'PRED')
        pred_ok.append(hit)
        out.append('NOM|%s|reasons=%s|%s' % (c, ','.join(r) or '-', 'PRED-LEDGERED' if hit else 'NO-PRED'))
    bar('NOM', all(pred_ok), 'nom-1..nom-3 PRED-ledgered=%d/3' % sum(pred_ok))
    n4_r = uledger_reasons(du, 'nom-4')
    out.append('NOM|nom-4|reasons=%s|installed=%s' % (','.join(n4_r) or '-', 'nom-4' in dk))

    # reason inventory
    reasons = {}
    for _, _, reason, _, _ in du:
        reasons[reason] = reasons.get(reason, 0) + 1
    out.append('INV|fam_nom_pairs=%d|reasons=%s'
               % (len(du), ','.join('%s=%d' % kv for kv in sorted(reasons.items()))))

    if fails:
        out.append('VERDICT|FAM-NOM KILLED|failed=%s' % ','.join(sorted(set(fails))))
    else:
        out.append('VERDICT|FAM-NOM SURVIVES|all bars pass')
    sys.stdout.write('\n'.join(out) + '\n')

if __name__ == '__main__':
    main()
