#!/usr/bin/env python3
"""Resume leg100x_b after interruption: rebuilds full ledgers deterministically.

For every (t,j) in order 0..63 x 0..99:
- if workdir exists: re-run query+verdict on saved need/pages (deterministic)
- else: run the full query/select/verdict pipeline
Writes knowledge_ledger.txt / refusal_ledger.txt identical to a fresh run.
Zero RNG.
"""
import os, subprocess, sys
from urllib.parse import urlparse

sys.path.insert(0, '/home/hatch/workspace/d4')
import run_scale100 as R

HERE = '/home/hatch/workspace/d4'
LEGDIR = os.path.join(HERE, 'work', 'scale', 'leg100x_b')
WORKDIR = os.path.join(LEGDIR, 'work')
STATE = os.path.join(LEGDIR, 'state')


def run_bin(args):
    r = subprocess.run(args, capture_output=True, text=True, cwd=HERE)
    return r.returncode, r.stdout, r.stderr


def do_verdict(cid, nf, pf):
    rc, out, _ = run_bin(['./src/d4_bin', 'query', STATE, nf])
    queries = [l.split('|', 1)[1] for l in out.split('\n') if l.startswith('QUERY|')]
    assert rc == 0 and queries, (cid, 'query')
    rc, out, _ = run_bin(['./src/d4_bin', 'verdict', STATE, nf, pf, 'FACT', queries[0]])
    assert rc == 0, (cid, 'verdict', rc)
    uncheck = any(l.startswith('ANSWER|UNCHECKABLE') for l in out.split('\n'))
    answer = [l.split('|', 1)[1] for l in out.split('\n')
              if l.startswith('ANSWER|') and l != 'ANSWER|UNCHECKABLE']
    provs = []
    for l in out.split('\n'):
        if l.startswith('PROV|1|'):
            p = l.split('|', 2)[2]
            if p not in provs:
                provs.append(p)
    if not uncheck and answer and len(provs) >= 2:
        return ('INSTALL', answer[0])
    return ('WITHHOLD', None)


def main():
    kledger, rledger = [], []
    kid = 0
    n_new = 0
    for t in range(64):
        for j in range(100):
            cid = 'sc-%02d-%03d' % (t, j)
            wd = os.path.join(WORKDIR, cid)
            nf = os.path.join(wd, 'need.txt')
            pf = os.path.join(wd, 'pages.txt')
            if os.path.exists(pf):
                status, claim = do_verdict(cid, nf, pf)
            else:
                n_new += 1
                need, pages = R.cluster_sentences(t, j)
                os.makedirs(wd, exist_ok=True)
                open(nf, 'w').write(need + '\n')
                rc, out, _ = run_bin(['./src/d4_bin', 'query', STATE, nf])
                queries = [l.split('|', 1)[1] for l in out.split('\n') if l.startswith('QUERY|')]
                assert rc == 0 and queries, (cid, 'query')
                rf = os.path.join(wd, 'results.txt')
                with open(rf, 'w') as f:
                    f.write('Q|' + queries[0] + '\n')
                    for pid, title, url, sents in pages:
                        f.write('R|%s|%s|%s\n' % (pid, title, sents[0][:160]))
                rc, out, _ = run_bin(['./src/d4_bin', 'select', STATE, rf])
                assert rc == 0, (cid, 'select', rc)
                opens = [l.split('|', 1)[1].split() for l in out.split('\n') if l.startswith('OPEN|')]
                opens = opens[0] if opens else []
                with open(pf, 'w') as f:
                    for pid, title, url, sents in pages:
                        if pid not in opens:
                            continue
                        try:
                            h = urlparse(url).hostname or ''
                        except Exception:
                            h = ''
                        f.write('P|%s|%s\nH|%s\n' % (pid, title, h.lower()))
                        for s in sents:
                            f.write('S|%s\n' % s)
                status, claim = do_verdict(cid, nf, pf)
            if status == 'INSTALL':
                kid += 1
                kledger.append('K|LI-%04d|%s|%s' % (kid, cid, claim))
            else:
                rledger.append('R|%s|NO_CORROBORATION' % cid)
        if t % 8 == 7:
            print('RESUME|t=%d|install=%d|withhold=%d|new=%d' % (
                t, len(kledger), len(rledger), n_new), flush=True)
    with open(os.path.join(LEGDIR, 'knowledge_ledger.txt'), 'w') as f:
        f.write('\n'.join(kledger) + ('\n' if kledger else ''))
    with open(os.path.join(LEGDIR, 'refusal_ledger.txt'), 'w') as f:
        f.write('\n'.join(rledger) + ('\n' if rledger else ''))
    print('RESUME|DONE|install=%d|withhold=%d' % (len(kledger), len(rledger)), flush=True)


if __name__ == '__main__':
    main()
