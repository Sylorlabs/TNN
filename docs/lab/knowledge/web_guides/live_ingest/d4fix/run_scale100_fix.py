#!/usr/bin/env python3
"""LI-D4-FIX F1' scale leg: deterministic 100x synthetic leg (6400 clusters).

1x leg = 64 template clusters; 100x leg = 64 templates x 100 copies.
Even templates merge (active/passive diathesis -> INSTALL); odd templates
predicate-swap -> WITHHOLD. No RNG: all variation is counter-derived.
Two full runs of the 100x leg must be byte-identical, and 100x counts must
equal exactly 100x the 1x counts. D4 arm only (mechanism under test).
"""
import os, re, sys, hashlib, subprocess, filecmp, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
D4FIXBIN = os.path.join(HERE, 'src', 'd4fix_bin')
GUIDES = '/home/hatch/workspace/scratch-li-principles/arm_control/guides'

SUBJS = ['harbor team', 'quarry team', 'north crew', 'south crew',
         'east guild', 'west guild', 'river band', 'hill band']
# (present, past, participle) -- all forms in the frozen verb table
VERBS = [('beat', 'beat', 'beaten'), ('mark', 'marked', 'marked'),
         ('carry', 'carried', 'carried'), ('reach', 'reached', 'reached'),
         ('hide', 'hid', 'hidden'), ('break', 'broke', 'broken'),
         ('write', 'wrote', 'written'), ('lose', 'lost', 'lost')]
OBJS = ['granite stone', 'marble stone', 'copper coin', 'silver coin',
        'oak chest', 'pine chest', 'wool bale', 'silk bale']
ALT_VERBS = [('spin', 'spun', 'spun'), ('shake', 'shook', 'shaken'),
             ('wake', 'woke', 'woken'), ('steal', 'stole', 'stolen'),
             ('speak', 'spoke', 'spoken'), ('drive', 'drove', 'driven'),
             ('freeze', 'froze', 'frozen'), ('hide', 'hid', 'hidden')]

N_TMPL = 64
N_COPY = 100


def toks(s):
    return re.findall(r'[a-z0-9]+', s.lower())


def split_sentences(text):
    out = []
    for s in re.split(r'(?<=[.!?])\s+', ' '.join(text.split())):
        s = ' '.join(s.split())
        if len(toks(s)) < 4 or len(s) > 600:
            continue
        out.append(s)
    return out


def cluster_sentences(t, j):
    """Deterministic (template t, copy j) -> (need, [(pid,title,url,sents)..])."""
    subj = SUBJS[(t + j) % 8]
    obj = OBJS[(t * 3 + j) % 8]
    v = VERBS[t % 8]
    merge = (t % 2 == 0)
    s1 = 'The %s %s the %s.' % (subj, v[1], obj)
    if merge:
        s2 = 'The %s was %s by the %s.' % (obj, v[2], subj)
    else:
        av = ALT_VERBS[t % 8]
        s2 = 'The %s %s the %s.' % (subj, av[1], obj)
    need = 'which crew moved the %s' % obj
    pages = []
    for n, s in ((1, s1), (2, s2)):
        pid = 'sc-%02d-%03d-p%d' % (t, j, n)
        host = 'scale%dexample' % (n,)
        url = 'https://%s/%s' % (host, pid)
        filler = ('The ledger entry was filed at dawn.' if n == 1
                  else 'The ledger entry was filed at dusk.')
        pages.append((pid, 'scale %d/%d p%d' % (t, j, n), url,
                      split_sentences('%s %s' % (s, filler))))
    return need, pages


def run_bin(args):
    r = subprocess.run(args, capture_output=True, text=True, cwd=HERE)
    return r.returncode, r.stdout, r.stderr


def run_leg(legdir, copies, tag):
    """copies: list of j values. Returns (n_install, n_withhold)."""
    if os.path.exists(legdir):
        shutil.rmtree(legdir)
    os.makedirs(os.path.join(legdir, 'state'))
    os.makedirs(os.path.join(legdir, 'work'))
    rc, out, err = run_bin([D4FIXBIN, 'teach', GUIDES, os.path.join(legdir, 'state')])
    assert rc == 0, ('teach', rc, err[-300:])
    kledger, rledger = [], []
    kid = 0
    from urllib.parse import urlparse
    for t in range(N_TMPL):
        for j in copies:
            cid = 'sc-%02d-%03d' % (t, j)
            need, pages = cluster_sentences(t, j)
            wd = os.path.join(legdir, 'work', cid)
            os.makedirs(wd)
            nf = os.path.join(wd, 'need.txt')
            open(nf, 'w').write(need + '\n')
            rc, out, err = run_bin([D4FIXBIN, 'query', os.path.join(legdir, 'state'), nf])
            assert rc == 0, (cid, 'query', rc)
            queries = [l.split('|', 1)[1] for l in out.split('\n') if l.startswith('QUERY|')]
            assert queries, (cid, 'no QUERY')
            rf = os.path.join(wd, 'results.txt')
            with open(rf, 'w') as f:
                f.write('Q|' + queries[0] + '\n')
                for pid, title, url, sents in pages:
                    f.write('R|%s|%s|%s\n' % (pid, title, sents[0][:160]))
            rc, out, err = run_bin([D4FIXBIN, 'select', os.path.join(legdir, 'state'), rf])
            assert rc == 0, (cid, 'select', rc)
            opens = [l.split('|', 1)[1].split() for l in out.split('\n') if l.startswith('OPEN|')]
            opens = opens[0] if opens else []
            pf = os.path.join(wd, 'pages.txt')
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
            rc, out, err = run_bin([D4FIXBIN, 'verdict', os.path.join(legdir, 'state'),
                                    nf, pf, 'FACT', queries[0]])
            assert rc == 0, (cid, 'verdict', rc)
            uncheckable = any(l.startswith('ANSWER|UNCHECKABLE') for l in out.split('\n'))
            answer = [l.split('|', 1)[1] for l in out.split('\n')
                      if l.startswith('ANSWER|') and l != 'ANSWER|UNCHECKABLE']
            provs = []
            for l in out.split('\n'):
                if l.startswith('PROV|1|'):
                    p = l.split('|', 2)[2]
                    if p not in provs:
                        provs.append(p)
            if not uncheckable and answer and len(provs) >= 2:
                kid += 1
                kledger.append('K|LI-%04d|%s|%s' % (kid, cid, answer[0]))
            else:
                rledger.append('R|%s|NO_CORROBORATION' % cid)
    with open(os.path.join(legdir, 'knowledge_ledger.txt'), 'w') as f:
        f.write('\n'.join(kledger) + ('\n' if kledger else ''))
    with open(os.path.join(legdir, 'refusal_ledger.txt'), 'w') as f:
        f.write('\n'.join(rledger) + ('\n' if rledger else ''))
    n_i, n_w = len(kledger), len(rledger)
    print('LEG|%s|copies=%d|install=%d|withhold=%d' % (tag, len(copies), n_i, n_w),
          flush=True)
    return n_i, n_w


def sha_tree(d):
    h = hashlib.sha256()
    for f in ('knowledge_ledger.txt', 'refusal_ledger.txt'):
        with open(os.path.join(d, f), 'rb') as fh:
            h.update(fh.read())
    return h.hexdigest()


def main():
    outdir = sys.argv[1]
    i1, w1 = run_leg(os.path.join(outdir, 'leg1x'), [0], '1x')
    i100a, w100a = run_leg(os.path.join(outdir, 'leg100x_a'), list(range(N_COPY)), '100x_a')
    i100b, w100b = run_leg(os.path.join(outdir, 'leg100x_b'), list(range(N_COPY)), '100x_b')
    same = (sha_tree(os.path.join(outdir, 'leg100x_a')) ==
            sha_tree(os.path.join(outdir, 'leg100x_b')))
    ratio = (i100a == 100 * i1 and w100a == 100 * w1)
    print('K5|two_runs_byte_identical=%s|counts_100x=%s (100x: %d/%d; 100*1x: %d/%d)' % (
        same, ratio, i100a, w100a, 100 * i1, 100 * w1))
    print('K5|%s' % ('PASS' if (same and ratio) else 'FAIL'))
    sys.exit(0 if (same and ratio) else 5)


if __name__ == '__main__':
    main()
