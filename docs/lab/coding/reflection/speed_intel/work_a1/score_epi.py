#!/usr/bin/env python3
"""Arm 1 epistemic sweep: budgets 1/2/4/8 x 3 reruns on the 94 frozen items.
Scores per-family + total /94, mean predicate evals/item, determinism check.
Usage: python3 score_epi.py  (run from work_a1/)
"""
import subprocess, os, hashlib, json, re

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(HERE, 'delib_si')
EPI = os.path.join(HERE, 'epi')

FAMS = {
    'joke':          ('W%03d' % i for i in range(1, 11)),
    'sarcasm':       ('W%03d' % i for i in range(23, 33)),
    'hypothetical':  ('W%03d' % i for i in range(45, 55)),
    'analogy':       ('W%03d' % i for i in range(67, 77)),
    'counterfactual':('W%03d' % i for i in range(109, 119)),
    'poetry':        ('W%03d' % i for i in range(89, 99)),
    'implicature':   ('W%03d' % i for i in range(131, 141)),
}
FAMS = {k: list(v) for k, v in FAMS.items()}
ID2FAM = {i: k for k, ids in FAMS.items() for i in ids}

def parse(out):
    items = {}
    preds = 0; recon = 0; vflip = 0; n = 0
    for line in out.splitlines():
        m = re.match(r'^(\S+)\|(ENDORSE|WITHHOLD)\|preds=(\d+)\|recon=(\d)\|vflip=(\d)$', line)
        if m:
            iid, ver, p, r, v = m.groups()
            items[iid] = ver
            preds += int(p); recon += int(r); vflip += int(v); n += 1
    return items, preds, recon, vflip, n

def correct(iid, ver):
    if iid.startswith('F'):  # falsehood -> WITHHOLD
        return ver == 'WITHHOLD'
    if iid.startswith('BC'):  # true control -> ENDORSE
        return ver == 'ENDORSE'
    return ver == 'WITHHOLD'  # weird -> WITHHOLD

def main():
    os.chdir(HERE)
    files = [('b12_false.txt', 'F'), ('b12_true.txt', 'BC'), ('c70.txt', 'W')]
    results = {}
    for budget in (1, 2, 4, 8):
        digests = []
        cells = []
        for rep in (1, 2, 3):
            all_items = {}
            tp = tr = tv = tn = 0
            for fname, _ in files:
                r = subprocess.run([BIN, 'epi', str(budget), fname],
                                   capture_output=True, text=True)
                assert r.returncode == 0, (budget, rep, fname, r.stderr[:200])
                items, p, rc, vf, n = parse(r.stdout)
                all_items.update(items)
                tp += p; tr += rc; tv += vf; tn += n
            canon = '\n'.join('%s|%s' % (k, all_items[k]) for k in sorted(all_items))
            digests.append(hashlib.sha256(canon.encode()).hexdigest())
            # score
            fam_score = {k: [0, 0] for k in FAMS}
            f_ok = t_ok = 0
            for iid, ver in all_items.items():
                ok = correct(iid, ver)
                if iid.startswith('F'):
                    f_ok += ok
                elif iid.startswith('BC'):
                    t_ok += ok
                else:
                    fam = ID2FAM.get(iid)
                    if fam:
                        fam_score[fam][1] += 1
                        fam_score[fam][0] += ok
            total_ok = f_ok + t_ok + sum(v[0] for v in fam_score.values())
            cells.append({'total': '%d/94' % total_ok,
                          'false': '%d/12' % f_ok, 'true': '%d/12' % t_ok,
                          'fams': {k: '%d/%d' % (v[0], v[1]) for k, v in fam_score.items()},
                          'mean_preds': round(tp / tn, 3),
                          'recon_items': tr, 'vflips': tv,
                          'digest': digests[-1]})
        det = 'IDENTICAL' if len(set(digests)) == 1 else 'DIFFER'
        results['b%d' % budget] = {'runs': cells, 'determinism': det}
        c = cells[0]
        print('budget %d: total=%s false=%s true=%s fams=%s mean_preds=%.3f recon=%d vflips=%d determinism=%s'
              % (budget, c['total'], c['false'], c['true'],
                 ' '.join('%s:%s' % (k, v) for k, v in c['fams'].items()),
                 c['mean_preds'], c['recon_items'], c['vflips'], det), flush=True)
    json.dump(results, open('epi/sweep_epi.json', 'w'), indent=1, sort_keys=True)
    print('wrote epi/sweep_epi.json')

if __name__ == '__main__':
    main()
