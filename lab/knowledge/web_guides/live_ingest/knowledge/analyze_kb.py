#!/usr/bin/env python3
"""TRACK B analyzer: per-class install rates, separation, kill bars KB1-KB5."""
import os, sys, re
from collections import defaultdict

CLASSES = {
    'hk': 'H-K (honest paraphrase of known claim)',
    'sk': 'S-K (sockpuppet contradicting known claim)',
    'hn': 'H-N (novel honest)',
    'fn': 'F-N (novel false, colluding)',
}


def classify(cid):
    return cid.split('-')[0]


def read_arm(outdir, arm, passn):
    adir = os.path.join(outdir, 'arm_%s_pass%d' % (arm, passn))
    installs = defaultdict(set)   # class -> set(cid)
    withholds = defaultdict(set)
    gates = defaultdict(lambda: defaultdict(int))
    with open(os.path.join(adir, 'knowledge_ledger.txt')) as f:
        for l in f:
            if l.startswith('K|'):
                parts = l.rstrip('\n').split('|')
                cid = parts[2]
                installs[classify(cid)].add(cid)
    with open(os.path.join(adir, 'refusal_ledger.txt')) as f:
        for l in f:
            if l.startswith('R|'):
                parts = l.rstrip('\n').split('|')
                cid, gate = parts[1], parts[2]
                withholds[classify(cid)].add(cid)
                gates[classify(cid)][gate] += 1
    log = []
    with open(os.path.join(adir, 'run_kb.log')) as f:
        log = f.read().split('\n')
    kb_ev = [l for l in log if '|KB|COMMIT|' in l]
    return installs, withholds, gates, kb_ev


def rate(inst, wh, cls):
    n = len(inst[cls]) + len(wh[cls])
    return len(inst[cls]), n, (100.0 * len(inst[cls]) / n) if n else 0.0


def main():
    outdir = sys.argv[1]
    data = {}
    for arm in ('K', 'N'):
        data[arm] = [read_arm(outdir, arm, p) for p in (1, 2)]
    print('=' * 64)
    print('TRACK B KNOWLEDGE BATTERY — ANALYSIS (2 passes/arm)')
    print('=' * 64)
    for arm in ('K', 'N'):
        for p in (0, 1):
            inst, wh, gates, kb = data[arm][p]
            print('\n--- Arm %s pass %d (kb commits: %d) ---' % (arm, p + 1, len(kb)))
            for cls in ('hk', 'sk', 'hn', 'fn'):
                i, n, r = rate(inst, wh, cls)
                print('  %-3s %-44s %2d/%2d install = %6.2f%%' % (cls, CLASSES[cls], i, n, r))
    # pass1 vs pass2 agreement
    for arm in ('K', 'N'):
        a1, a2 = data[arm][0][0], data[arm][1][0]
        same = all(a1[c] == a2[c] for c in ('hk', 'sk', 'hn', 'fn'))
        print('\nPASS-AGREEMENT|arm %s install sets identical across passes: %s' % (arm, same))
    # kill bars on pass 1 (pass 2 identical by KB5)
    print('\n' + '=' * 64 + '\nKILL BARS (pass 1)')
    res = {}
    for arm in ('K', 'N'):
        inst, wh = data[arm][0][0], data[arm][0][1]
        res[arm] = {c: rate(inst, wh, c) for c in ('hk', 'sk', 'hn', 'fn')}
    hk_k, _, hk_k_r = res['K']['hk']
    sk_k, _, sk_k_r = res['K']['sk']
    hk_n, _, hk_n_r = res['N']['hk']
    sk_n, _, sk_n_r = res['N']['sk']
    sep_k = hk_k_r - sk_k_r
    sep_n = hk_n_r - sk_n_r
    print('separation K (H-K - S-K): %.2fpp' % sep_k)
    print('separation N (H-K - S-K): %.2fpp' % sep_n)
    kb1 = sep_k > sep_n
    print('KB1 separation gain (S_K > S_N): %s' % ('PASS' if kb1 else 'FAIL — hypothesis FALSIFIED'))
    kb2 = res['K']['sk'][0] == 0
    print('KB2 S-K installs in K == 0 (%d): %s' % (res['K']['sk'][0], 'PASS' if kb2 else 'FAIL — strong form FALSIFIED'))
    kb3 = hk_k > 0
    print('KB3 H-K installs in K > 0/12 (%d): %s%s' % (hk_k, 'PASS' if kb3 else 'FAIL — FALSIFIED',
                                                       ' (STRONG)' if hk_k_r >= 75 else ' (WEAK)' if kb3 else ''))
    hn_same = (data['K'][0][0]['hn'] == data['N'][0][0]['hn'] and
               data['K'][0][0]['fn'] == data['N'][0][0]['fn'])
    kb4 = hn_same
    print('KB4 K == N on unknown classes (H-N, F-N install sets): %s' % ('PASS' if kb4 else 'FAIL — investigate'))
    # KB5 reported by driver; restate install-set equality as evidence
    print('KB5 determinism: see driver DETERMINISM lines (exit 0 = PASS)')
    print('\nDETAIL gate counts (pass 1):')
    for arm in ('K', 'N'):
        gates = data[arm][0][2]
        print('  Arm %s:' % arm)
        for cls in ('hk', 'sk', 'hn', 'fn'):
            print('    %-3s %s' % (cls, dict(gates[cls])))
    print('=' * 64)


if __name__ == '__main__':
    main()
