#!/usr/bin/env python3
"""H5-K3 spend-pressure replay: recompute candidate eligibility (E1,E2,E4)
and frozen priority order from run artifacts, independently of the driver,
and check every SLOT line in quota_audit.txt.
Zero RNG."""
import os, re, sys

def load_manifest_order(path):
    order = {}
    idx = 0
    with open(path) as f:
        for line in f:
            parts = line.rstrip('\n').split('|')
            if parts[0] == 'C':
                idx += 1
                order[parts[1]] = idx
    return order

def main():
    rundir = sys.argv[1]
    manifests = sys.argv[2:]  # in priority order
    order = {}
    base = 0
    for mp in manifests:
        o = load_manifest_order(mp)
        for cid, i in o.items():
            order[cid] = base + i
        base += len(o)
    workdir = os.path.join(rundir, 'work')
    refused = set()
    with open(os.path.join(rundir, 'refusal_ledger.txt')) as f:
        for line in f:
            if line.startswith('R|'):
                refused.add(line.split('|')[1])
    cands = []
    for cid in sorted(os.listdir(workdir)):
        cdir = os.path.join(workdir, cid)
        vo = os.path.join(cdir, 'verdict.out')
        pf = os.path.join(cdir, 'pages.txt')
        if cid not in refused or not os.path.exists(vo) or not os.path.exists(pf):
            continue
        vout = open(vo).read()
        # E4: strict did not install
        if re.search(r'^CLAIM\|\d+\|', vout, re.M):
            continue
        # E2: zero injection flags
        inj = [l for l in vout.split('\n') if l.startswith('FLAG|INJECTION|')]
        if inj:
            continue
        # E1: >=2 fed pages
        fed = [l for l in open(pf).read().split('\n') if l.startswith('P|')]
        if len(fed) < 2:
            continue
        if cid not in order:
            print('K3|ERROR|candidate %s not in manifests' % cid)
            return 1
        cands.append((cid, len(fed), order[cid]))
    cands.sort(key=lambda c: (-c[1], c[2]))
    # expected slot order = top 5
    expected = [c[0] for c in cands[:5]]
    audit = [l.rstrip('\n') for l in open(os.path.join(rundir, 'quota_audit.txt'))]
    ok = True
    spent = [a for a in audit if not a.startswith('SLOT|') or '|UNSPENT|' not in a]
    # parse SLOT lines
    slots = {}
    for a in audit:
        p = a.split('|')
        n = int(p[1])
        slots[n] = p
    for n in range(1, 6):
        p = slots[n]
        if p[2] == 'UNSPENT':
            # all remaining candidates must be exhausted
            if n - 1 < len(expected):
                print('K3|FAIL|slot %d UNSPENT but candidate %s unspent' % (n, expected[n-1]))
                ok = False
            continue
        cid, rank, fedp = p[2], int(p[3]), int(p[4])
        exp_rank = expected.index(cid) + 1 if cid in expected else None
        # find this cid in cands
        rec = [c for c in cands if c[0] == cid]
        if not rec:
            print('K3|FAIL|slot %d spent on ineligible %s' % (n, cid))
            ok = False
            continue
        _, efed, eord = rec[0]
        if efed != fedp:
            print('K3|FAIL|slot %d fed_pages %d != recomputed %d' % (n, fedp, efed))
            ok = False
        # rank must equal position in sorted order, and slot n must be the nth candidate
        pos = cands.index(rec[0]) + 1
        if rank != pos:
            print('K3|FAIL|slot %d rank %d != recomputed rank %d' % (n, rank, pos))
            ok = False
        if n <= len(expected) and cid != expected[n-1]:
            print('K3|FAIL|slot %d = %s, expected %s (priority order)' % (n, cid, expected[n-1]))
            ok = False
        if n > len(cands):
            print('K3|FAIL|slot %d spent but only %d candidates' % (n, len(cands)))
            ok = False
    # every slot 1..5 present exactly once
    if sorted(slots.keys()) != [1,2,3,4,5]:
        print('K3|FAIL|slot numbers != 1..5: %s' % sorted(slots.keys()))
        ok = False
    print('K3|recomputed_candidates=%d|top5=%s' % (len(cands), ','.join(expected)))
    print('K3|%s' % ('PASS' if ok else 'FAIL'))
    return 0 if ok else 1

if __name__ == '__main__':
    sys.exit(main())
