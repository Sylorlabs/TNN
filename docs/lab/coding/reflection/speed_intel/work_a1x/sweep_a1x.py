#!/usr/bin/env python3
"""A1X sweep: budgets x 3 reruns on a battery dir with delib_si2.
Saves raw outputs (rep 1), per-budget cells, per-item verdict trajectories,
and a JSON summary. Zero RNG.
Usage: python3 sweep_a1x.py <epi_dir> <battery_name> <budgets_csv> <fam_json>
  fam_json: {"joke":[211,230],"sarcasm":[231,250],...} (inclusive ranges)
Run from work_a1x/.
"""
import subprocess, os, hashlib, json, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(HERE, 'delib_si2')
LINE = re.compile(r'^(\S+)\|(ENDORSE|WITHHOLD)\|preds=(\d+)\|recon=(\d)\|vflip=(\d)$')

def correct(iid, ver):
    if iid.startswith('F'):
        return ver == 'WITHHOLD'
    if iid.startswith('BC'):
        return ver == 'ENDORSE'
    return ver == 'WITHHOLD'

def main():
    epi_dir, bname, budgets_csv, fam_json, n_fixed = sys.argv[1:6]
    budgets = [int(x) for x in budgets_csv.split(',')]
    franges = json.load(open(fam_json))
    fams = {k: ['W%03d' % i for i in range(v[0], v[1] + 1)] for k, v in franges.items()}
    id2fam = {i: k for k, ids in fams.items() for i in ids}
    n_expected = sum(v[1] - v[0] + 1 for v in franges.values()) + int(n_fixed)
    files = [('b12_false.txt', 'false'), ('b12_true.txt', 'true'), ('c70.txt', 'c70')]
    os.chdir(HERE)
    outdir = os.path.join('epi', 'sweep_' + bname)
    os.makedirs(outdir, exist_ok=True)
    results = {'battery': bname, 'n_expected': n_expected, 'cells': {},
               'trajectories': {}}
    for budget in budgets:
        digests = []
        cells = []
        for rep in (1, 2, 3):
            all_items = {}
            tp = tr = tv = tn = 0
            for fname, stem in files:
                r = subprocess.run([BIN, os.path.relpath(epi_dir, HERE), str(budget), fname],
                                   capture_output=True, text=True, cwd=HERE)
                assert r.returncode == 0, (budget, rep, fname, r.stderr[:200])
                if rep == 1:
                    with open(os.path.join(outdir, 'out_b%d_%s.txt' % (budget, stem)), 'w') as f:
                        f.write(r.stdout)
                for line in r.stdout.splitlines():
                    m = LINE.match(line)
                    if m:
                        iid, ver, p, rc, vf = m.groups()
                        all_items[iid] = ver
                        tp += int(p); tr += int(rc); tv += int(vf); tn += 1
            assert tn == n_expected, (budget, rep, tn, n_expected)
            canon = '\n'.join('%s|%s' % (k, all_items[k]) for k in sorted(all_items))
            digests.append(hashlib.sha256(canon.encode()).hexdigest())
            if rep == 1:
                for iid, ver in all_items.items():
                    results['trajectories'].setdefault(iid, {})['b%d' % budget] = ver
            fam_score = {k: [0, 0] for k in fams}
            f_ok = t_ok = 0
            for iid, ver in all_items.items():
                ok = correct(iid, ver)
                if iid.startswith('F'):
                    f_ok += ok
                elif iid.startswith('BC'):
                    t_ok += ok
                else:
                    fam = id2fam.get(iid)
                    if fam:
                        fam_score[fam][1] += 1
                        fam_score[fam][0] += ok
            total_ok = f_ok + t_ok + sum(v[0] for v in fam_score.values())
            cells.append({'total': total_ok, 'n': tn,
                          'false': f_ok, 'true': t_ok,
                          'fams': {k: v[0] for k, v in fam_score.items()},
                          'fam_n': {k: v[1] for k, v in fam_score.items()},
                          'mean_preds': round(tp / tn, 3),
                          'recon_items': tr, 'vflips': tv,
                          'digest': digests[-1]})
        det = 'IDENTICAL' if len(set(digests)) == 1 else 'DIFFER'
        results['cells']['b%d' % budget] = {'runs': cells, 'determinism': det}
        c = cells[0]
        nf = int(n_fixed) // 2
        print('b%-3d total=%d/%d (%.1fpp) false=%d/%d true=%d/%d fams=%s mean_preds=%.3f recon=%d vflips=%d det=%s'
              % (budget, c['total'], c['n'], 100.0 * c['total'] / c['n'],
                 c['false'], nf, c['true'], nf,
                 ' '.join('%s:%d' % (k, v) for k, v in c['fams'].items()),
                 c['mean_preds'], c['recon_items'], c['vflips'], det), flush=True)
    json.dump(results, open(os.path.join(outdir, 'sweep_%s.json' % bname), 'w'),
              indent=1, sort_keys=True)
    print('wrote epi/sweep_%s/sweep_%s.json' % (bname, bname))

if __name__ == '__main__':
    main()
