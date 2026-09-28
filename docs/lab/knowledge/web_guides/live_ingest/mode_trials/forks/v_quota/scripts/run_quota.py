#!/usr/bin/env python3
"""V-QUOTA fork driver (F4). Python glue only; all reasoning is the Zag instrument.

Batteries: R1 | C1C2 | H0. Each run: teach -> strict pass over the corpus ->
candidate ranking (frozen V-SCOUT order) -> <=5 quota slots -> ledgers +
quota_audit.txt. Zero RNG.

Usage: run_quota.py <R1|C1C2|H0> <outdir> [webg_bin]
Writes: run_quota.log, knowledge_ledger.txt (strict installs),
        refusal_ledger.txt (strict withholds), quota_ledger.txt
        (quota-attributable installs), quota_audit.txt, transcripts under
        work/<cid>/.
"""
import os, re, sys, hashlib, subprocess
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
WEBG_DEFAULT = os.path.join(HERE, 'webg_quota')
GUIDES = '/home/hatch/workspace/scratch-li-forkbase/guides'
STOPLIST = os.path.join(HERE, 'stoplist_para.txt')

def host_of(url):
    try:
        h = urlparse(url).hostname or ''
    except Exception:
        h = ''
    return h.lower()

def toks(s):
    return re.findall(r'[a-z0-9]+', s.lower())

def load_manifest(path):
    clusters, order = [], {}
    with open(path) as f:
        for line in f:
            line = line.rstrip('\n')
            if not line or line.startswith('#'):
                continue
            parts = line.split('|')
            if parts[0] == 'C':
                clusters.append([parts[1], '|'.join(parts[2:]), []])
                order[parts[1]] = len(clusters) - 1
            elif parts[0] == 'U':
                clusters[order[parts[1]]][2].append('|'.join(parts[2:]))
    return clusters

def load_fetch_status(snapdir):
    st = {}
    p = os.path.join(snapdir, 'manifest_fetch_status.txt')
    if os.path.exists(p):
        with open(p) as f:
            for line in f:
                line = line.rstrip('\n')
                if line.startswith('F|'):
                    _, cid, pid, url, ok, note = line.split('|', 5)
                    st[(cid, pid)] = (url, ok, note)
    return st

def load_fidelity(snapdir):
    fid = {}
    p = os.path.join(snapdir, 'snapshot_fidelity.txt')
    if os.path.exists(p):
        with open(p) as f:
            for line in f:
                line = line.rstrip('\n')
                if line.startswith('V|'):
                    parts = line.split('|', 4)
                    fid[(parts[1], parts[2])] = (parts[3], parts[4] if len(parts) > 4 else '')
    return fid

def split_sentences(text):
    lines = []
    for ln in text.split('\n'):
        s = ' '.join(ln.split())
        if not s or s.startswith('\u3010') or s.startswith('Images:'):
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

def teach(webg, guides, state_dir, log):
    os.makedirs(state_dir, exist_ok=True)
    rc, out, err = run_bin([webg, 'teach', guides, state_dir], HERE)
    log.append('TEACH|rc=%d' % rc)
    installed = [l for l in out.split('\n') if '|INSTALLED|' in l]
    rejected = [l for l in out.split('\n') if '|REJECTED|' in l]
    g7rej = any('G7|REJECTED' in l for l in rejected)
    inst_ids = []
    for l in installed:
        parts = l.split('|')
        if len(parts) >= 3 and parts[0].endswith('LEARN'):
            inst_ids.append(parts[1])
        elif len(parts) >= 2:
            inst_ids.append(parts[-2] if parts[-2].startswith('G') else parts[1])
    exact = (sorted(inst_ids) == ['G1', 'G2', 'G3', 'G4', 'G5', 'G6'])
    if rc == 3 or not g7rej or not exact:
        log.append('TEACH|VOID|installed=%s g7rej=%s' % (','.join(sorted(inst_ids)), g7rej))
        return False
    log.append('TEACH|VALID|G1-G6 installed exactly once each, G7 rejected')
    return True

def do_query(webg, state_dir, need_file):
    rc, out, err = run_bin([webg, 'query', state_dir, need_file], HERE)
    queries = [l.split('|', 1)[1] for l in out.split('\n') if l.startswith('QUERY|')]
    return rc, queries, out

def do_select(webg, state_dir, pages, query):
    # pages: list of (pid, title, url, sents)
    import tempfile
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False,
                                     dir='/home/hatch/workspace/scratch-li-f4') as f:
        rf = f.name
        f.write('Q|' + query + '\n')
        for pid, title, url, sents in pages:
            f.write('R|%s|%s|%s\n' % (pid, title, sents[0][:160] if sents else ''))
    rc, out, err = run_bin([webg, 'select', state_dir, rf], HERE)
    os.unlink(rf)
    opens = []
    for l in out.split('\n'):
        if l.startswith('OPEN|'):
            opens = l.split('|', 1)[1].split()
    return rc, opens, out

def parse_verdict(out):
    d = {}
    d['inj'] = [l.split('|', 2)[2] for l in out.split('\n') if l.startswith('FLAG|INJECTION|')]
    d['uncheckable'] = any(l.startswith('ANSWER|UNCHECKABLE') for l in out.split('\n'))
    d['answer'] = [l.split('|', 1)[1] for l in out.split('\n')
                   if l.startswith('ANSWER|') and l != 'ANSWER|UNCHECKABLE']
    d['claims'] = re.findall(r'^CLAIM\|\d+\|([^|]*)\|', out, re.M)
    d['provs'] = []
    for l in out.split('\n'):
        if l.startswith('PROV|1|'):
            p = l.split('|', 2)[2]
            if p not in d['provs']:
                d['provs'].append(p)
    d['src_gate'] = any(l.startswith('GATE|SRC_INDEPENDENCE|') for l in out.split('\n'))
    d['para_gate'] = [l.split('|', 2)[2] for l in out.split('\n') if l.startswith('GATE|PARA|')]
    d['quota_flags'] = [l for l in out.split('\n') if l.startswith('QUOTA|')]
    d['installed'] = (not d['uncheckable']) and len(d['claims']) > 0
    return d

def build_pages_txt(path, pages, opens):
    # pages: list of (pid, title, host, sents)
    with open(path, 'w') as f:
        for pid, title, host, sents in pages:
            if pid not in opens:
                continue
            f.write('P|%s|%s\n' % (pid, title))
            f.write('H|%s\n' % host)
            for s in sents:
                f.write('S|%s\n' % s)

def process_corpus_cluster(webg, state_dir, outdir, cid, need, urls, snapdir,
                           fstat, fid, kledger, rledger, gate_counts, log,
                           manifest_idx, cand_recs):
    """One manifest cluster: fetch gates -> query -> select -> verdict.
    Appends candidate record to cand_recs if withheld and E1/E2-eligible."""
    workdir = os.path.join(outdir, 'work', cid)
    os.makedirs(workdir, exist_ok=True)
    pages = []
    for i, url in enumerate(urls):
        pid = '%s-p%d' % (cid, i + 1)
        key = (cid, pid)
        if key in fstat:
            furl, ok, note = fstat[key]
            if furl != url:
                log.append('%s|URLMISMATCH|%s' % (cid, pid))
                url = furl
        else:
            furl, ok, note = url, ('ok' if os.path.exists(
                os.path.join(snapdir, cid, pid + '.txt')) else 'FAIL'), ''
        if ok != 'ok' or not os.path.exists(os.path.join(snapdir, cid, pid + '.txt')):
            rledger.append('R|%s|UNSUPPORTED_FETCH|-|fetch failed: %s|%s'
                           % (cid, note or 'no snapshot', url))
            gate_counts['UNSUPPORTED_FETCH'] = gate_counts.get('UNSUPPORTED_FETCH', 0) + 1
            continue
        verdict, reason = fid.get((cid, pid), ('UNVERIFIED', 'no fidelity record'))
        if verdict != 'VERIFIED':
            rledger.append('R|%s|SNAPSHOT_UNVERIFIED|-|excluded: %s|%s' % (cid, reason, url))
            gate_counts['SNAPSHOT_UNVERIFIED'] = gate_counts.get('SNAPSHOT_UNVERIFIED', 0) + 1
            continue
        with open(os.path.join(snapdir, cid, pid + '.txt'), encoding='utf-8', errors='replace') as f:
            raw = f.read().split('\n')
        title = raw[0][len('TITLE:'):].strip() if raw and raw[0].startswith('TITLE:') else pid
        sents = split_sentences('\n'.join(raw[1:]))
        if not sents:
            rledger.append('R|%s|PARSE_FAIL|-|no sentences|%s' % (cid, url))
            gate_counts['PARSE_FAIL'] = gate_counts.get('PARSE_FAIL', 0) + 1
            continue
        pages.append((pid, title, host_of(url), sents, url))
        log.append('%s|FETCH|ok|%s|%d sentences' % (cid, pid, len(sents)))
    if len(pages) < 2:
        rledger.append('R|%s|NO_CORROBORATION|-|fewer than 2 pages available|%s'
                       % (cid, ';'.join(urls)))
        gate_counts['NO_CORROBORATION'] = gate_counts.get('NO_CORROBORATION', 0) + 1
        log.append('%s|WITHHOLD|NO_CORROBORATION|insufficient pages' % cid)
        return
    need_file = os.path.join(workdir, 'need.txt')
    with open(need_file, 'w') as f:
        f.write(need + '\n')
    rc, queries, qout = do_query(webg, state_dir, need_file)
    with open(os.path.join(workdir, 'query.out'), 'w') as f:
        f.write(qout)
    if rc != 0 or not queries:
        rledger.append('R|%s|CRASH|-|query failed|' % cid)
        gate_counts['CRASH'] = gate_counts.get('CRASH', 0) + 1
        return
    log.append('%s|QUERY|%s' % (cid, queries[0]))
    rc, opens, sout = do_select(webg, state_dir,
                                [(p[0], p[1], p[4], p[3]) for p in pages], queries[0])
    with open(os.path.join(workdir, 'select.out'), 'w') as f:
        f.write(sout)
    if rc != 0 or not opens:
        rledger.append('R|%s|SELECT_EMPTY|-|select opened no pages|' % cid)
        gate_counts['SELECT_EMPTY'] = gate_counts.get('SELECT_EMPTY', 0) + 1
        log.append('%s|WITHHOLD|SELECT_EMPTY' % cid)
        return
    pages_file = os.path.join(workdir, 'pages.txt')
    build_pages_txt(pages_file, [(p[0], p[1], p[2], p[3]) for p in pages], opens)
    fed = [p for p in pages if p[0] in opens]
    rc, out, err = run_bin([webg, 'verdict', state_dir, need_file, pages_file,
                            'FACT', queries[0]], HERE)
    with open(os.path.join(workdir, 'verdict.out'), 'w') as f:
        f.write(out)
    if rc != 0:
        rledger.append('R|%s|CRASH|-|verdict rc=%d|' % (cid, rc))
        gate_counts['CRASH'] = gate_counts.get('CRASH', 0) + 1
        return
    v = parse_verdict(out)
    urlmap = {p[0]: p[4] for p in pages}
    if v['installed'] and len(v['provs']) >= 2:
        kledger.append(('K', cid, v['answer'][0] if v['answer'] else '',
                        list(v['provs']), urlmap))
        log.append('%s|INSTALL|STRICT|%s' % (cid, (v['answer'][0][:80] if v['answer'] else '')))
    else:
        reason = 'NO_CORROBORATION'
        if v['inj']:
            reason = 'INJ_WITHHOLD'
        rledger.append('R|%s|%s|-|strict withheld%s|' % (cid, reason,
                         ' inj=' + ','.join(v['inj']) if v['inj'] else ''))
        gate_counts[reason] = gate_counts.get(reason, 0) + 1
        log.append('%s|WITHHOLD|%s|inj=%s' % (cid, reason, ','.join(v['inj'])))
        # candidate eligibility E1+E2 (E3 inside instrument, E4 automatic)
        if len(fed) >= 2 and not v['inj']:
            cand_recs.append({'cid': cid, 'fed_pages': len(fed),
                              'manifest_idx': manifest_idx,
                              'need_file': need_file, 'pages_file': pages_file,
                              'query': queries[0], 'kind': 'FACT'})

def spend_quota(webg, state_dir, outdir, cand_recs, qledger, log):
    """Spend <=5 slots in frozen priority order. Returns audit lines."""
    cands = sorted(cand_recs, key=lambda c: (-c['fed_pages'], c['manifest_idx']))
    audit = []
    spent = 0
    for rank, c in enumerate(cands, start=1):
        if spent >= 5:
            break
        spent += 1
        cid = c['cid']
        workdir = os.path.join(outdir, 'work', cid)
        rc, out, err = run_bin([webg, 'quota', state_dir, c['need_file'],
                                c['pages_file'], c['query'], STOPLIST], HERE)
        with open(os.path.join(workdir, 'quota.out'), 'w') as f:
            f.write(out)
        v = parse_verdict(out)
        win = False
        claim_or_reason = 'no-passing-pair'
        pids = '-'
        if v['quota_flags']:
            qf = v['quota_flags'][0]
            if 'NO-CANDIDATE' in qf:
                claim_or_reason = 'NO-CANDIDATE'
            elif 'INJECTED' in qf:
                claim_or_reason = 'INJECTED'
            elif 'STRICT-WOULD-INSTALL' in qf:
                claim_or_reason = 'STRICT-WOULD-INSTALL'
            elif 'STOPLIST-FAIL' in qf:
                claim_or_reason = 'STOPLIST-FAIL'
        # driver install rule: GATE|PARA| + >=2 PROV|1| + no injection flags
        if v['para_gate'] and len(v['provs']) >= 2 and not v['inj'] and v['answer']:
            win = True
            claim_or_reason = v['answer'][0].replace('|', '/').replace('\n', ' ')
            pids = ','.join(v['provs'])
            qledger.append(('K', cid, v['answer'][0], list(v['provs'])))
            log.append('%s|INSTALL|QUOTA|slot=%d|%s' % (cid, spent, v['answer'][0][:80]))
        else:
            log.append('%s|QUOTA|LOSE|slot=%d|%s' % (cid, spent, claim_or_reason))
        audit.append('SLOT|%d|%s|%d|%d|%s|%s|GATE|PARA|%s'
                     % (spent, cid, rank, c['fed_pages'],
                        'WIN' if win else 'LOSE', claim_or_reason, pids))
    for n in range(spent + 1, 6):
        audit.append('SLOT|%d|UNSPENT|no-more-eligible-candidates' % n)
        log.append('SLOT|%d|UNSPENT' % n)
    return audit

def write_ledgers(outdir, kledger, rledger, qledger, audit):
    kid = 0
    with open(os.path.join(outdir, 'knowledge_ledger.txt'), 'w') as f:
        for tag, cid, claim, provs, urlmap in kledger:
            kid += 1
            kid_s = 'LI-%04d' % kid
            f.write('K|%s|%s|%s\n' % (kid_s, cid, claim))
            for p in provs:
                f.write('P|%s|%s|%s\n' % (kid_s, p, urlmap.get(p, '?')))
    with open(os.path.join(outdir, 'refusal_ledger.txt'), 'w') as f:
        for r in rledger:
            f.write(r + '\n')
    with open(os.path.join(outdir, 'quota_ledger.txt'), 'w') as f:
        qid = 0
        for tag, cid, claim, provs in qledger:
            qid += 1
            kid_s = 'LQ-%04d' % qid
            f.write('K|%s|%s|QUOTA|%s\n' % (kid_s, cid, claim))
            for p in provs:
                f.write('P|%s|%s\n' % (kid_s, p))
    with open(os.path.join(outdir, 'quota_audit.txt'), 'w') as f:
        for a in audit:
            f.write(a + '\n')

def battery_R1(webg, outdir):
    """A1..A9 (teach->query->select->verdict) then rt01/rt02/rt10/rt11/rt12
    (frozen need.txt + pages.txt)."""
    log = ['LI-QUOTA|battery=R1']
    state_dir = os.path.join(outdir, 'state')
    if not teach(webg, GUIDES, state_dir, log):
        return False, log
    kledger, rledger, qledger = [], [], []
    gate_counts = {}
    cand_recs = []
    adir = '/home/hatch/workspace/tnn-lab/knowledge/web_guides/live_ingest/diag/attacks'
    cases = sorted(d for d in os.listdir(adir)
                   if os.path.isdir(os.path.join(adir, d))
                   and os.path.exists(os.path.join(adir, d, 'need.txt')))
    midx = 0
    for case in cases:
        midx += 1
        cdir = os.path.join(adir, case)
        workdir = os.path.join(outdir, 'work', case)
        os.makedirs(workdir, exist_ok=True)
        need = open(os.path.join(cdir, 'need.txt')).read().strip()
        kind = open(os.path.join(cdir, 'kind.txt')).read().strip() \
            if os.path.exists(os.path.join(cdir, 'kind.txt')) else 'FACT'
        pages = {}
        pdir = os.path.join(cdir, 'pages')
        for fn in sorted(os.listdir(pdir)):
            if not fn.endswith('.txt'):
                continue
            pid = fn[:-4]
            with open(os.path.join(pdir, fn)) as f:
                lines = [l.rstrip('\n') for l in f]
            title = lines[0].split('TITLE:', 1)[1].strip() \
                if lines and lines[0].startswith('TITLE:') else ''
            pages[pid] = (title, [l for l in lines[1:] if l.strip()])
        hosts = {}
        hf = os.path.join(cdir, 'hosts.txt')
        if os.path.exists(hf):
            for line in open(hf):
                line = line.strip()
                if line and '|' in line:
                    pid, host = line.split('|', 1)
                    hosts[pid.strip()] = host.strip()
        need_file = os.path.join(workdir, 'need.txt')
        with open(need_file, 'w') as f:
            f.write(need + '\n')
        rc, queries, qout = do_query(webg, state_dir, need_file)
        with open(os.path.join(workdir, 'query.out'), 'w') as f:
            f.write(qout)
        if rc != 0 or not queries:
            rledger.append('R|%s|CRASH|-|query failed|' % case)
            continue
        plist = [(pid, t, '', s) for pid, (t, s) in pages.items() if s]
        rc, opens, sout = do_select(webg, state_dir, plist, queries[0])
        with open(os.path.join(workdir, 'select.out'), 'w') as f:
            f.write(sout)
        if rc != 0 or not opens:
            rledger.append('R|%s|SELECT_EMPTY|-|-|' % case)
            continue
        pages_file = os.path.join(workdir, 'pages.txt')
        build_pages_txt(pages_file,
                        [(pid, t, hosts.get(pid, ''), s) for pid, (t, s) in pages.items()],
                        opens)
        fed = [pid for pid in opens if pages.get(pid, ('', []))[1]]
        rc, out, err = run_bin([webg, 'verdict', state_dir, need_file,
                                pages_file, kind, queries[0]], HERE)
        with open(os.path.join(workdir, 'verdict.out'), 'w') as f:
            f.write(out)
        v = parse_verdict(out)
        log.append('%s|STRICT|installed=%s|inj=%s|answer=%s'
                   % (case, v['installed'], ','.join(v['inj']),
                      (v['answer'][0][:60] if v['answer'] else 'UNCHECKABLE')))
        if v['installed'] and len(v['provs']) >= 2:
            kledger.append(('K', case, v['answer'][0] if v['answer'] else '',
                            list(v['provs']), {}))
        else:
            rledger.append('R|%s|WITHHOLD|-|strict withheld inj=%s|'
                           % (case, ','.join(v['inj'])))
            if len(fed) >= 2 and not v['inj']:
                cand_recs.append({'cid': case, 'fed_pages': len(fed),
                                  'manifest_idx': midx, 'need_file': need_file,
                                  'pages_file': pages_file, 'query': queries[0],
                                  'kind': kind})
    # live cases: frozen artifacts
    rtdir = '/home/hatch/workspace/tnn-lab/knowledge/web_guides/live_ingest/redteam_test1/work'
    for case in ['rt01', 'rt02', 'rt10', 'rt11', 'rt12']:
        midx += 1
        cdir = os.path.join(rtdir, case)
        workdir = os.path.join(outdir, 'work', case)
        os.makedirs(workdir, exist_ok=True)
        need = open(os.path.join(cdir, 'need.txt')).read().strip()
        need_file = os.path.join(workdir, 'need.txt')
        with open(need_file, 'w') as f:
            f.write(need + '\n')
        qout = open(os.path.join(cdir, 'query.out')).read()
        with open(os.path.join(workdir, 'query.out'), 'w') as f:
            f.write(qout)
        queries = [l.split('|', 1)[1] for l in qout.split('\n') if l.startswith('QUERY|')]
        if not queries:
            rledger.append('R|%s|CRASH|-|no frozen query|' % case)
            continue
        pages_file = os.path.join(workdir, 'pages.txt')
        with open(pages_file, 'w') as f:
            f.write(open(os.path.join(cdir, 'pages.txt')).read())
        fed = [l for l in open(pages_file).read().split('\n') if l.startswith('P|')]
        rc, out, err = run_bin([webg, 'verdict', state_dir, need_file,
                                pages_file, 'FACT', queries[0]], HERE)
        with open(os.path.join(workdir, 'verdict.out'), 'w') as f:
            f.write(out)
        v = parse_verdict(out)
        log.append('%s|STRICT|installed=%s|inj=%s|answer=%s'
                   % (case, v['installed'], ','.join(v['inj']),
                      (v['answer'][0][:60] if v['answer'] else 'UNCHECKABLE')))
        if v['installed'] and len(v['provs']) >= 2:
            kledger.append(('K', case, v['answer'][0] if v['answer'] else '',
                            list(v['provs']), {}))
        else:
            rledger.append('R|%s|WITHHOLD|-|strict withheld inj=%s|'
                           % (case, ','.join(v['inj'])))
            if len(fed) >= 2 and not v['inj']:
                cand_recs.append({'cid': case, 'fed_pages': len(fed),
                                  'manifest_idx': midx, 'need_file': need_file,
                                  'pages_file': pages_file, 'query': queries[0],
                                  'kind': 'FACT'})
    audit = spend_quota(webg, state_dir, outdir, cand_recs, qledger, log)
    write_ledgers(outdir, kledger, rledger, qledger, audit)
    log.append('SUMMARY|battery=R1|cases=%d|strict_installed=%d|withheld=%d|quota_installed=%d'
               % (midx, len(kledger), len(rledger), len(qledger)))
    return True, log

def battery_C1C2(webg, outdir):
    log = ['LI-QUOTA|battery=C1C2']
    state_dir = os.path.join(outdir, 'state')
    if not teach(webg, GUIDES, state_dir, log):
        return False, log
    kledger, rledger, qledger = [], [], []
    gate_counts = {}
    cand_recs = []
    base = '/home/hatch/workspace/tnn-lab/knowledge/web_guides/live_ingest'
    c1m = os.path.join(base, 'li-1/urls_manifest_cu.txt')
    c1s = os.path.join(base, 'corpus_snap_full')
    c2m = '/home/hatch/workspace/scratch-li-forkbase/fixtures_novel/manifest_fixtures.txt'
    c2s = '/home/hatch/workspace/scratch-li-forkbase/fixtures_novel/snap'
    midx = 0
    for manifest, snapdir in [(c1m, c1s), (c2m, c2s)]:
        clusters = load_manifest(manifest)
        fstat = load_fetch_status(snapdir)
        fid = load_fidelity(snapdir)
        for cid, need, urls in clusters:
            midx += 1
            process_corpus_cluster(webg, state_dir, outdir, cid, need, urls,
                                   snapdir, fstat, fid, kledger, rledger,
                                   gate_counts, log, midx, cand_recs)
    audit = spend_quota(webg, state_dir, outdir, cand_recs, qledger, log)
    write_ledgers(outdir, kledger, rledger, qledger, audit)
    log.append('SUMMARY|battery=C1C2|clusters=%d|strict_installed=%d|withheld=%d|quota_installed=%d|gates=%s'
               % (midx, len(kledger), len(rledger), len(qledger),
                  ','.join('%s=%d' % kv for kv in sorted(gate_counts.items()))))
    return True, log

def battery_H0(webg, outdir):
    log = ['LI-QUOTA|battery=H0']
    state_dir = os.path.join(outdir, 'state')
    if not teach(webg, GUIDES, state_dir, log):
        return False, log
    kledger, rledger, qledger = [], [], []
    gate_counts = {}
    cand_recs = []
    h0dir = os.path.join(HERE, 'h0_fixtures')
    manifest = os.path.join(h0dir, 'manifest_h0.txt')
    clusters = load_manifest(manifest)
    fstat = load_fetch_status(h0dir)
    fid = load_fidelity(h0dir)
    midx = 0
    for cid, need, urls in clusters:
        midx += 1
        process_corpus_cluster(webg, state_dir, outdir, cid, need, urls,
                               h0dir, fstat, fid, kledger, rledger,
                               gate_counts, log, midx, cand_recs)
    audit = spend_quota(webg, state_dir, outdir, cand_recs, qledger, log)
    write_ledgers(outdir, kledger, rledger, qledger, audit)
    log.append('SUMMARY|battery=H0|clusters=%d|strict_installed=%d|withheld=%d|quota_installed=%d'
               % (midx, len(kledger), len(rledger), len(qledger)))
    return True, log

def main():
    battery, outdir = sys.argv[1], sys.argv[2]
    webg = sys.argv[3] if len(sys.argv) > 3 else WEBG_DEFAULT
    os.makedirs(outdir, exist_ok=True)
    fn = {'R1': battery_R1, 'C1C2': battery_C1C2, 'H0': battery_H0}[battery]
    ok, log = fn(webg, outdir)
    with open(os.path.join(outdir, 'run_quota.log'), 'w') as f:
        f.write('\n'.join(log) + '\n')
    blob = '\n'.join(log) + '\n'
    print('RESULT|battery=%s|ok=%s|sha256=%s' % (battery, ok, hashlib.sha256(blob.encode()).hexdigest()))
    sys.exit(0 if ok else 3)

if __name__ == '__main__':
    main()
