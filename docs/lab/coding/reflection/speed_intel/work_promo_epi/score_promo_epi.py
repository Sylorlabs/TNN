#!/usr/bin/env python3
"""P5 verification scorer: mainline delib_sa arm=2 x3 reruns on frozen 94 items.
Parses `ID|ENDORSE|WITHHOLD` (+SUMMARY footer) lines, scores vs frozen key:
  F* -> WITHHOLD, BC* -> ENDORSE, W* -> WITHHOLD (with per-family breakdown).
Frozen expectations: total 59/94, false 12/12, true 12/12,
families joke 5/10, sarcasm 3/10, hypothetical 5/10, analogy 3/10,
counterfactual 9/10, poetry 5/10, implicature 5/10; reruns byte-identical.
"""
import os, re, hashlib, json

HERE = os.path.dirname(os.path.abspath(__file__))
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
EXPECT = {'total': 59, 'false': 12, 'true': 12,
          'joke': 5, 'sarcasm': 3, 'hypothetical': 5, 'analogy': 3,
          'counterfactual': 9, 'poetry': 5, 'implicature': 5}

def correct(iid, ver):
    if iid.startswith('F'):
        return ver == 'WITHHOLD'
    if iid.startswith('BC'):
        return ver == 'ENDORSE'
    return ver == 'WITHHOLD'

def main():
    os.chdir(HERE)
    results = {}
    for rep in (1, 2, 3):
        items = {}
        for base in ('b12_false', 'b12_true', 'c70'):
            for line in open('run%d/%s.out' % (rep, base)):
                m = re.match(r'^(\S+)\|(ENDORSE|WITHHOLD)$', line.strip())
                if m:
                    items[m.group(1)] = m.group(2)
        assert len(items) == 94, (rep, len(items))
        canon = '\n'.join('%s|%s' % (k, items[k]) for k in sorted(items))
        dg = hashlib.sha256(canon.encode()).hexdigest()
        fam = {k: [0, 0] for k in FAMS}
        f_ok = t_ok = 0
        for iid, ver in items.items():
            ok = correct(iid, ver)
            if iid.startswith('F'):
                f_ok += ok
            elif iid.startswith('BC'):
                t_ok += ok
            else:
                f = ID2FAM.get(iid)
                fam[f][1] += 1; fam[f][0] += ok
        total = f_ok + t_ok + sum(v[0] for v in fam.values())
        got = {'total': total, 'false': f_ok, 'true': t_ok}
        got.update({k: v[0] for k, v in fam.items()})
        results['rep%d' % rep] = {'scores': got, 'digest': dg,
                                  'match_expect': got == EXPECT}
        print('rep%d: total=%d/94 false=%d/12 true=%d/12 %s digest=%s match_expect=%s'
              % (rep, total, f_ok, t_ok,
                 ' '.join('%s:%d/10' % (k, fam[k][0]) for k in FAMS),
                 dg, got == EXPECT))
    dgs = [results['rep%d' % r]['digest'] for r in (1, 2, 3)]
    det = 'IDENTICAL' if len(set(dgs)) == 1 else 'DIFFER'
    all_match = all(results['rep%d' % r]['match_expect'] for r in (1, 2, 3))
    print('rerun determinism:', det)
    print('VERDICT:', 'PASS' if (det == 'IDENTICAL' and all_match) else 'FAIL')
    json.dump(results, open('scores_promo_epi.json', 'w'), indent=1, sort_keys=True)

if __name__ == '__main__':
    main()
