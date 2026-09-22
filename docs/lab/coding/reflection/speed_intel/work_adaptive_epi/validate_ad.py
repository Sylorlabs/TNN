#!/usr/bin/env python3
"""Validation gates OPER_SPEC §8 (pre-trial):
1. policy x == delib_si budget-2 (verdicts+preds) on all 94 frozen items.
2. policy c == delib_si budget-4 (verdicts+preds) on all 94 frozen items.
3. fresh-item ledger spot-check vs FRESH_NOTES hand-derived expectations.
"""
import subprocess, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
AD = os.path.join(HERE, 'delib_ad')
SI = os.path.join(HERE, '..', 'work_a1', 'delib_si')
EPI = os.path.join(HERE, '..', 'work_a1', 'epi')

def run(binpath, workdir, arg, fname):
    r = subprocess.run([binpath, workdir, arg, fname],
                       capture_output=True, text=True)
    assert r.returncode == 0, (binpath, arg, fname, r.stderr[:300])
    return r.stdout

def parse(out, extended):
    items = {}
    for line in out.splitlines():
        if extended:
            m = re.match(r'^(\S+)\|(ENDORSE|WITHHOLD)\|preds=(\d+)\|recon=(\d)\|vflip=(\d)\|rounds=(\d+)$', line)
            if m:
                items[m.group(1)] = (m.group(2), int(m.group(3)), int(m.group(4)), int(m.group(5)), int(m.group(6)))
        else:
            m = re.match(r'^(\S+)\|(ENDORSE|WITHHOLD)\|preds=(\d+)\|recon=(\d)\|vflip=(\d)$', line)
            if m:
                items[m.group(1)] = (m.group(2), int(m.group(3)), int(m.group(4)), int(m.group(5)))
    return items

def gate(name, ad_pol, si_budget):
    ok = True
    for fname in ('b12_false.txt', 'b12_true.txt', 'c70.txt'):
        a = parse(run(AD, EPI, ad_pol, fname), True)
        s = parse(run(SI, EPI, str(si_budget), fname), False)
        assert set(a) == set(s), (name, fname, 'id sets differ')
        for iid in a:
            av, ap, ar, avf, ard = a[iid]
            sv, sp, sr, svf = s[iid]
            if (av, ap, ar, avf) != (sv, sp, sr, svf):
                print('  MISMATCH %s %s: ad=%s si=%s' % (fname, iid, a[iid], s[iid]))
                ok = False
    print('gate %s: %s' % (name, 'PASS' if ok else 'FAIL'))
    return ok

def gate3():
    # hand-derived expectations: id -> (verdict, preds, recon, vflip, rounds) for policy a
    exp = {
        # fresh false: kf fires -> R0 unanimous withhold stop
        **{'FFF%02d' % i: ('WITHHOLD', 3, 0, 0, 1) for i in range(1, 13)},
        # fresh true kt items: R0 unanimous endorse stop
        'FTT01': ('ENDORSE', 3, 0, 0, 1), 'FTT02': ('ENDORSE', 3, 0, 0, 1),
        'FTT03': ('ENDORSE', 3, 0, 0, 1), 'FTT04': ('ENDORSE', 3, 0, 0, 1),
        # plain true: E1 -> R1, no matcher -> endorse
        'FTT05': ('ENDORSE', 9, 0, 0, 2), 'FTT06': ('ENDORSE', 9, 0, 0, 2),
        'FTT07': ('ENDORSE', 9, 0, 0, 2), 'FTT08': ('ENDORSE', 9, 0, 0, 2),
        'FTT09': ('ENDORSE', 9, 0, 0, 2),
        # true traps: kt -> R0 stop endorse (matcher never consulted)
        'FTT10': ('ENDORSE', 3, 0, 0, 1), 'FTT11': ('ENDORSE', 3, 0, 0, 1),
        'FTT12': ('ENDORSE', 3, 0, 0, 1),
        # joke absurd: R0 stop withhold
        'FW001': ('WITHHOLD', 3, 0, 0, 1), 'FW002': ('WITHHOLD', 3, 0, 0, 1),
        'FW003': ('WITHHOLD', 3, 0, 0, 1), 'FW004': ('WITHHOLD', 3, 0, 0, 1),
        # sarcasm/hypothetical/analogy/counterfactual/poetry/implicature plain:
        # E1 -> R1, matcher fires, cm2=0 -> withhold, halt
        'FW005': ('WITHHOLD', 10, 0, 0, 2), 'FW006': ('WITHHOLD', 10, 0, 0, 2),
        'FW007': ('WITHHOLD', 10, 0, 0, 2),
        'FW009': ('WITHHOLD', 10, 0, 0, 2), 'FW010': ('WITHHOLD', 10, 0, 0, 2),
        'FW011': ('WITHHOLD', 10, 0, 0, 2),
        'FW013': ('WITHHOLD', 10, 0, 0, 2), 'FW014': ('WITHHOLD', 10, 0, 0, 2),
        'FW015': ('WITHHOLD', 10, 0, 0, 2),
        'FW017': ('WITHHOLD', 10, 0, 0, 2), 'FW018': ('WITHHOLD', 10, 0, 0, 2),
        'FW019': ('WITHHOLD', 10, 0, 0, 2),
        'FW021': ('WITHHOLD', 10, 0, 0, 2), 'FW022': ('WITHHOLD', 10, 0, 0, 2),
        'FW023': ('WITHHOLD', 10, 0, 0, 2),
        'FW025': ('WITHHOLD', 10, 0, 0, 2), 'FW026': ('WITHHOLD', 10, 0, 0, 2),
        'FW027': ('WITHHOLD', 10, 0, 0, 2),
        # tie traps: matcher + cm2 -> R2 tie -> keep withhold
        'FW008': ('WITHHOLD', 11, 1, 0, 3), 'FW012': ('WITHHOLD', 11, 1, 0, 3),
        'FW016': ('WITHHOLD', 11, 1, 0, 3), 'FW020': ('WITHHOLD', 11, 1, 0, 3),
        'FW024': ('WITHHOLD', 11, 1, 0, 3),
        # FW028 kt-poisoning: kt -> R0 stop endorse (WRONG per label, by design)
        'FW028': ('ENDORSE', 3, 0, 0, 1),
    }
    got = {}
    for fname in ('fresh_false.txt', 'fresh_true.txt', 'fresh_weird.txt'):
        got.update(parse(run(AD, 'fresh', 'a', fname), True))
    ok = True
    assert set(got) == set(exp), 'id sets differ'
    for iid, e in exp.items():
        if got[iid] != e:
            print('  LEDGER MISMATCH %s: got=%s exp=%s' % (iid, got[iid], e))
            ok = False
    print('gate fresh-ledger (policy a): %s' % ('PASS' if ok else 'FAIL'))
    return ok

os.chdir(HERE)
g1 = gate('x==2x', 'x', 2)
g2 = gate('c==4x', 'c', 4)
g3 = gate3()
sys.exit(0 if (g1 and g2 and g3) else 1)
