#!/usr/bin/env python3
"""LI whitebox tracer: fixed fixture set through the frozen pipeline, per-stage dispositions.

Classes:
  A  - nf-a-01..20  (Type-A byte-identical novel truths)     from forkbase fixtures
  B  - nf-b-01..24  (Type-B paraphrased novel truths)        from forkbase fixtures
  P  - P1..P4       (paraphrase-sockpuppet falsehoods)       from R1 red-team battery
  X  - A9_xhost     (colluding byte-identical falsehood)     from R1 red-team battery
  K  - k-01..k-12   (already-known facts: 10 identical + 2 paraphrased) built locally

Pipeline per case: FETCH -> PARSE -> QUERY -> SELECT -> VERDICT(trace) -> STORE.
Every stage records an exact disposition code into dispositions.tsv.
Zero RNG. Deterministic: two runs must be byte-identical.

Usage: wb_driver.py <outdir>
"""
import os, re, sys, subprocess
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
FB = os.path.join(os.path.expanduser('~'), 'workspace', 'scratch-li-forkbase')
WEBG = os.path.join(HERE, 'webg_trace')
GUIDES = os.path.join(FB, 'guides')
BATTERY = os.path.join(os.path.expanduser('~'), 'workspace', 'tnn-lab',
                       'knowledge', 'web_guides', 'live_ingest',
                       'mode_trials', 'redteam', 'battery')
KNOWN = os.path.join(HERE, 'fixtures_known')

def host_of(url):
    try:
        h = urlparse(url).hostname or ''
    except Exception:
        h = ''
    return h.lower()

def toks(s):
    return re.findall(r'[a-z0-9]+', s.lower())

def split_sentences(text):
    lines = []
    for ln in text.split('\n'):
        s = ' '.join(ln.split())
        if not s or s.startswith('【') or s.startswith('Images:'):
            continue
        lines.append(s)
    out = []
    for s in re.split(r'(?<=[.!?])\s+', ' '.join(lines)):
        s = ' '.join(s.split())
        if len(toks(s)) < 4 or len(s) > 600:
            continue
        out.append(s)
        if len(out) >= 400:
            break
    return out

def run_bin(args, cwd):
    r = subprocess.run(args, capture_output=True, text=True, cwd=cwd)
    return r.returncode, r.stdout, r.stderr

# ---------- case loaders ----------
def load_fixture_cases():
    """From forkbase manifest (classes A/B). Returns list of (cid, cls, need, [(pid,url)])"""
    cases = []
    with open(os.path.join(FB, 'fixtures_novel', 'manifest_fixtures.txt')) as f:
        cur = None
        for line in f:
            line = line.rstrip('\n')
            if not line or line.startswith('#'):
                continue
            parts = line.split('|')
            if parts[0] == 'C':
                cid = parts[1]
                cls = 'A' if cid.startswith('nf-a-') else ('B' if cid.startswith('nf-b-') else 'C')
                cur = (cid, cls, '|'.join(parts[2:]), [])
                cases.append(cur)
            elif parts[0] == 'U':
                cur[3].append((parts[1] + '-p%d' % (len(cur[3]) + 1), '|'.join(parts[2:])))
    return cases

def load_fetch_status():
    st = {}
    p = os.path.join(FB, 'fixtures_novel', 'snap', 'manifest_fetch_status.txt')
    if os.path.exists(p):
        with open(p) as f:
            for line in f:
                line = line.rstrip('\n')
                if line.startswith('F|'):
                    _, cid, pid, url, ok, note = line.split('|', 5)
                    st[(cid, pid)] = (url, ok, note)
    return st

def load_fidelity():
    fid = {}
    p = os.path.join(FB, 'fixtures_novel', 'snap', 'snapshot_fidelity.txt')
    if os.path.exists(p):
        with open(p) as f:
            for line in f:
                line = line.rstrip('\n')
                if line.startswith('V|'):
                    parts = line.split('|', 4)
                    fid[(parts[1], parts[2])] = (parts[3], parts[4] if len(parts) > 4 else '')
    return fid

def load_battery_cases(names):
    cases = []
    for name in names:
        d = os.path.join(BATTERY, name)
        need = open(os.path.join(d, 'need.txt')).read().strip()
        hosts = {}
        with open(os.path.join(d, 'hosts.txt')) as f:
            for line in f:
                line = line.strip()
                if line and '|' in line:
                    pid, h = line.split('|', 1)
                    hosts[pid] = h
        pages = []
        for pid in sorted(hosts):
            p = os.path.join(d, 'pages', pid + '.txt')
            raw = open(p, encoding='utf-8', errors='replace').read().split('\n')
            title = raw[0][len('TITLE:'):].strip() if raw and raw[0].startswith('TITLE:') else pid
            sents = split_sentences('\n'.join(raw[1:]))
            pages.append((pid, title, 'https://%s/%s' % (hosts[pid], pid), sents))
        cls = 'P' if name.startswith('P') else 'X'
        cases.append((name, cls, need, pages, hosts))
    return cases

def load_known_cases():
    cases = []
    for cid in sorted(os.listdir(KNOWN)):
        d = os.path.join(KNOWN, cid)
        if not os.path.isdir(d):
            continue
        need = open(os.path.join(d, 'need.txt')).read().strip()
        hosts = {}
        with open(os.path.join(d, 'hosts.txt')) as f:
            for line in f:
                line = line.strip()
                if line and '|' in line:
                    pid, h = line.split('|', 1)
                    hosts[pid] = h
        pages = []
        for pid in sorted(hosts):
            p = os.path.join(d, 'pages', pid + '.txt')
            raw = open(p, encoding='utf-8', errors='replace').read().split('\n')
            title = raw[0][len('TITLE:'):].strip() if raw and raw[0].startswith('TITLE:') else pid
            sents = split_sentences('\n'.join(raw[1:]))
            pages.append((pid, title, 'https://%s/%s' % (hosts[pid], pid), sents))
        cls = 'K-para' if cid in ('k-11', 'k-12') else 'K'
        cases.append((cid, cls, need, pages, hosts))
    return cases

# ---------- pipeline ----------
def main():
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    state_dir = os.path.join(outdir, 'state')
    os.makedirs(state_dir, exist_ok=True)

    disp = ['case\tclass\tfetch\tparse\tquery\tselect\tblind\tinj_flags\t'
            'n_candidates\tclusters\twinner_count\tminsrc\tverdict\tprovs\tstore\tstore_gate']

    rc, out, _ = run_bin([WEBG, 'teach', GUIDES, state_dir], HERE)
    assert rc == 0 and 'G7|REJECTED' in out, 'teach void: rc=%d' % rc

    fstat = load_fetch_status()
    fid = load_fidelity()
    kid = 0

    def run_case(cid, cls, need, pages_direct, hosts_direct):
        """pages_direct: None for fixture-manifest cases, else [(pid,title,url,sents)]."""
        nonlocal kid
        workdir = os.path.join(outdir, 'work', cid)
        os.makedirs(workdir, exist_ok=True)
        fetch = 'ok'
        pages = []
        if pages_direct is None:
            # fixture-manifest path with fetch-status + fidelity gates
            snapbase = os.path.join(FB, 'fixtures_novel', 'snap', cid)
            for (pid, url) in case_urls[cid]:
                key = (cid, pid)
                if key in fstat:
                    furl, ok, note = fstat[key]
                    if furl != url:
                        url = furl
                else:
                    furl, ok, note = url, ('ok' if os.path.exists(
                        os.path.join(snapbase, pid + '.txt')) else 'FAIL'), ''
                if ok != 'ok' or not os.path.exists(os.path.join(snapbase, pid + '.txt')):
                    return disp_row(cid, cls, 'UNSUPPORTED_FETCH', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'WITHHOLD', 'UNSUPPORTED_FETCH')
                verdict, reason = fid.get((cid, pid), ('UNVERIFIED', 'no record'))
                if verdict != 'VERIFIED':
                    return disp_row(cid, cls, 'SNAPSHOT_UNVERIFIED', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'WITHHOLD', 'SNAPSHOT_UNVERIFIED')
                raw = open(os.path.join(snapbase, pid + '.txt'), encoding='utf-8', errors='replace').read().split('\n')
                title = raw[0][len('TITLE:'):].strip() if raw and raw[0].startswith('TITLE:') else pid
                sents = split_sentences('\n'.join(raw[1:]))
                pages.append((pid, title, url, sents))
        else:
            fetch = 'direct'
            for (pid, title, url, sents) in pages_direct:
                if not sents:
                    return disp_row(cid, cls, fetch, 'PARSE_FAIL', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'WITHHOLD', 'PARSE_FAIL')
                pages.append((pid, title, url, sents))

        parse_s = '%d pages, %d sents' % (len(pages), sum(len(s) for _, _, _, s in pages))
        if pages_direct is None and any(len(s) == 0 for _, _, _, s in pages):
            return disp_row(cid, cls, fetch, 'PARSE_FAIL', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'WITHHOLD', 'PARSE_FAIL')
        if len(pages) < 2:
            return disp_row(cid, cls, fetch, parse_s, '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'WITHHOLD', 'NO_CORROBORATION:insufficient-pages')

        need_file = os.path.join(workdir, 'need.txt')
        with open(need_file, 'w') as f:
            f.write(need + '\n')
        rc, out, err = run_bin([WEBG, 'query', state_dir, need_file], HERE)
        with open(os.path.join(workdir, 'query.out'), 'w') as f:
            f.write(out)
        if rc != 0:
            return disp_row(cid, cls, fetch, parse_s, 'CRASH', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'WITHHOLD', 'CRASH:query')
        queries = [l.split('|', 1)[1] for l in out.split('\n') if l.startswith('QUERY|')]
        if not queries:
            return disp_row(cid, cls, fetch, parse_s, 'no-QUERY', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'WITHHOLD', 'PARSE_FAIL:query')
        query_s = queries[0][:60]

        res_file = os.path.join(workdir, 'results.txt')
        with open(res_file, 'w') as f:
            f.write('Q|' + queries[0] + '\n')
            for pid, title, url, sents in pages:
                f.write('R|%s|%s|%s\n' % (pid, title, sents[0][:160]))
        rc, out, err = run_bin([WEBG, 'select', state_dir, res_file], HERE)
        with open(os.path.join(workdir, 'select.out'), 'w') as f:
            f.write(out)
        if rc != 0:
            return disp_row(cid, cls, fetch, parse_s, query_s, 'CRASH', '-', '-', '-', '-', '-', '-', '-', '-', 'WITHHOLD', 'CRASH:select')
        opens = []
        for l in out.split('\n'):
            if l.startswith('OPEN|'):
                opens = l.split('|', 1)[1].split()
        select_s = 'OPEN %s' % ','.join(opens) if opens else 'SELECT_EMPTY'
        if not opens:
            return disp_row(cid, cls, fetch, parse_s, query_s, select_s, '-', '-', '-', '-', '-', '-', '-', '-', 'WITHHOLD', 'SELECT_EMPTY')

        pages_file = os.path.join(workdir, 'pages.txt')
        urlmap = {}
        with open(pages_file, 'w') as f:
            for pid, title, url, sents in pages:
                if pid not in opens:
                    continue
                urlmap[pid] = url
                f.write('P|%s|%s\n' % (pid, title))
                f.write('H|%s\n' % host_of(url))
                for s in sents:
                    f.write('S|%s\n' % s)
        rc, out, err = run_bin([WEBG, 'tverdict', state_dir, need_file, pages_file,
                                'FACT', queries[0]], HERE)
        with open(os.path.join(workdir, 'tverdict.out'), 'w') as f:
            f.write(out)
        if rc != 0:
            return disp_row(cid, cls, fetch, parse_s, query_s, select_s, '-', '-', '-', '-', '-', '-', '-', '-', 'WITHHOLD', 'CRASH:verdict')

        # parse trace + verdict lines
        blind = '?'
        inj = []
        cands = []
        clusters = []
        minsrc = '?'
        winner = '?'
        for l in out.split('\n'):
            if l.startswith('TRACE|BLIND|'):
                blind = l.split('|')[2]
            elif l.startswith('TRACE|INJ|'):
                inj.append(l.split('|')[2])
            elif l.startswith('TRACE|CAND|'):
                cands.append(l.split('|', 3)[3][:50] if '|' in l else '')
            elif l.startswith('TRACE|CLUSTER|'):
                parts = l.split('|')
                clusters.append('c%s=%s(pg%s)' % (parts[2], parts[3].split('=')[1], parts[5].split('=')[1]))
            elif l.startswith('TRACE|MINSRC|'):
                minsrc = l.split('|')[2]
            elif l.startswith('TRACE|WINNER|'):
                winner = l.split('|')[2].split('=')[1]
        inj_s = ','.join(inj) if inj else 'none'
        uncheckable = any(l.startswith('ANSWER|UNCHECKABLE') for l in out.split('\n'))
        answer = [l.split('|', 1)[1] for l in out.split('\n')
                  if l.startswith('ANSWER|') and l != 'ANSWER|UNCHECKABLE']
        provs = []
        for l in out.split('\n'):
            if l.startswith('PROV|1|'):
                p = l.split('|', 2)[2]
                if p not in provs:
                    provs.append(p)
        n_cand = str(len(cands))
        clu_s = ';'.join(clusters) if clusters else 'none'

        if uncheckable or not answer:
            return disp_row(cid, cls, fetch, parse_s, query_s, select_s, blind, inj_s,
                            n_cand, clu_s, winner, minsrc, 'UNCHECKABLE', str(len(provs)),
                            'WITHHOLD', 'NO_CORROBORATION')
        claim = answer[0]
        bad = [p for p in provs if p in inj]
        if bad:
            return disp_row(cid, cls, fetch, parse_s, query_s, select_s, blind, inj_s,
                            n_cand, clu_s, winner, minsrc, 'ANSWER(cited-inj)', str(len(provs)),
                            'WITHHOLD', 'INTEGRITY_VIOLATION')
        if len(provs) >= 2:
            kid += 1
            return disp_row(cid, cls, fetch, parse_s, query_s, select_s, blind, inj_s,
                            n_cand, clu_s, winner, minsrc, 'ANSWER', str(len(provs)),
                            'INSTALL', 'INSTALL')
        return disp_row(cid, cls, fetch, parse_s, query_s, select_s, blind, inj_s,
                        n_cand, clu_s, winner, minsrc, 'ANSWER(single-prov)', str(len(provs)),
                        'WITHHOLD', 'NO_CORROBORATION:single-source')

    def disp_row(cid, cls, fetch, parse, query, select, blind, inj, n_cand, clu,
                winner, minsrc, verdict, provs, store, gate):
        return '\t'.join([cid, cls, fetch, parse, query, select, blind, inj,
                           n_cand, clu, winner, minsrc, verdict, provs, store, gate])

    # (i)+(ii): fixture classes A/B from forkbase manifest
    all_cases = load_fixture_cases()
    global case_urls
    case_urls = {}
    for cid, cls, need, urls in all_cases:
        case_urls[cid] = urls
    for cid, cls, need, urls in all_cases:
        if cls in ('A', 'B'):
            disp.append(run_case(cid, cls, need, None, None))
    # (iii)+(iv): battery P1-P4, A9
    for cid, cls, need, pages, hosts in load_battery_cases(
            ['P1_paratower', 'P2_paraboil', 'P3_parabones', 'P4_parabird', 'A9_xhost']):
        disp.append(run_case(cid, cls, need, pages, hosts))
    # (v): known facts
    for cid, cls, need, pages, hosts in load_known_cases():
        disp.append(run_case(cid, cls, need, pages, hosts))

    with open(os.path.join(outdir, 'dispositions.tsv'), 'w') as f:
        f.write('\n'.join(disp) + '\n')
    print('DONE|cases=%d' % (len(disp) - 1))

if __name__ == '__main__':
    main()
