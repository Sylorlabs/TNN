#!/usr/bin/env python3
"""PREREG_SI_A1X section 2 VERDICT-IDENTITY GATE.
delib_si2 (full-int budget parser) vs delib_si_ref (pristine frozen source)
at budgets 1/2/4/8 on the frozen-94 and a1r-94 batteries, 3 reruns each.
Canonical digest = sha256 over sorted 'ID|verdict' lines.
PASS requires byte-identical digests in all 24 cells. Any FAIL -> STOP.
Usage: python3 identity_gate.py  (run from work_a1x/)
"""
import subprocess, os, hashlib, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, 'delib_si_ref')
NEW = os.path.join(HERE, 'delib_si2')
SI = os.path.dirname(HERE)

BATTERIES = {
    'frozen-94': os.path.join(SI, 'work_a1', 'epi'),
    'a1r-94': os.path.join(SI, 'work_a1r', 'epi'),
}
FILES = ['b12_false.txt', 'b12_true.txt', 'c70.txt']
LINE = re.compile(r'^(\S+)\|(ENDORSE|WITHHOLD)\|preds=(\d+)\|recon=(\d)\|vflip=(\d)$')

def run(binpath, epidir, budget):
    items = {}
    preds = recon = vflip = 0
    for fn in FILES:
        r = subprocess.run([binpath, os.path.relpath(epidir, HERE), str(budget), fn],
                           capture_output=True, text=True, cwd=HERE)
        assert r.returncode == 0, (binpath, budget, fn, r.stderr[:200])
        for line in r.stdout.splitlines():
            m = LINE.match(line)
            if m:
                iid, ver, p, rc, vf = m.groups()
                items[iid] = (ver, p, rc, vf)
    canon = '\n'.join('%s|%s' % (k, items[k][0]) for k in sorted(items))
    full = '\n'.join('%s|%s|%s|%s|%s' % (k, *items[k]) for k in sorted(items))
    return (hashlib.sha256(canon.encode()).hexdigest(),
            hashlib.sha256(full.encode()).hexdigest(), len(items))

def main():
    fails = 0
    for bname, epidir in BATTERIES.items():
        for budget in (1, 2, 4, 8):
            for rep in (1, 2, 3):
                d_ref, f_ref, n_ref = run(REF, epidir, budget)
                d_new, f_new, n_new = run(NEW, epidir, budget)
                ok = (d_ref == d_new) and (n_ref == n_new == 94)
                # full-field digest must also match: preds/recon/vflip identical
                ok = ok and (f_ref == f_new)
                print('%s b%d rep%d: verdicts %s, full-fields %s, n=%d -> %s'
                      % (bname, budget, rep,
                         'MATCH' if d_ref == d_new else 'DIFFER',
                         'MATCH' if f_ref == f_new else 'DIFFER',
                         n_new, 'PASS' if ok else 'FAIL'), flush=True)
                if not ok:
                    fails += 1
    print('IDENTITY GATE: %s' % ('PASS (24/24 cells)' if fails == 0 else 'FAIL (%d)' % fails))
    sys.exit(1 if fails else 0)

if __name__ == '__main__':
    main()
