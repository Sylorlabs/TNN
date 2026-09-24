#!/usr/bin/env python3
"""PRINCIPLES-FIRST live-ingestion hypothesis test driver.

Two arms x two passes over the 60-cluster novel-facts battery plus the
4-cluster P red-team battery (paraphrased two-host falsehoods).

Per arm/pass: teach (validated) -> per-cluster query/select/verdict ->
knowledge/refusal ledgers + run log. Then byte-compare pass1 vs pass2.

Pure orchestration; all reasoning is the Zag instrument. Zero RNG.

Usage: run_principles.py <outdir>
"""
import os, re, sys, hashlib, subprocess, filecmp
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(os.path.dirname(HERE), 'scratch-li-forkbase', 'fixtures_novel')
MANIFEST = os.path.join(FIX, 'manifest_fixtures.txt')
SNAPDIR = os.path.join(FIX, 'snap')
PBAT = os.path.join(HERE, 'pbattery')

ARMS = {
    'control': dict(
        webg=os.path.join(HERE, 'bin', 'webg_control'),
        guides=os.path.join(HERE, 'arm_control', 'guides'),
        teach_exact=sorted(['G1', 'G2', 'G3', 'G4', 'G5', 'G6']),
    ),
    'principles': dict(
        webg=os.path.join(HERE, 'bin', 'webg_principles'),
        guides=os.path.join(HERE, 'arm_principles', 'guides'),
        teach_exact=sorted(['G1', 'G2', 'G3', 'G4', 'G5', 'G6',
                            'E1', 'E2', 'E3', 'E4', 'E5', 'E6']),
    ),
}

PCLS = ['p1', 'p2', 'p3', 'p4']


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


def load_p_clusters():
    """Red-team P battery: direct reads, hosts from hosts.txt. Pinned in prereg."""
    cls = []
    for cid in PCLS:
        d = os.path.join(PBAT, cid)
        with open(os.path.join(d, 'need.txt')) as f:
            need = f.read().strip()
        hosts = {}
        with open(os.path.join(d, 'hosts.txt')) as f:
            for line in f:
                line = line.strip()
                if line and '|' in line:
                    k, v = line.split('|', 1)
                    hosts[k.strip()] = v.strip()
        pages = []
        for n in (1, 2):
            pid = '%s-p%d' % (cid, n)
            host = hosts['p%d' % n]
            url = 'https://%s/%s' % (host, pid)
            with open(os.path.join(d, '%s-p%d.txt' % (cid, n)),
                      encoding='utf-8', errors='replace') as f:
                raw = f.read().split('\n')
            title = (raw[0][len('TITLE:'):].strip()
                     if raw and raw[0].startswith('TITLE:') else pid)
            sents = split_sentences('\n'.join(raw[1:]))
            pages.append((pid, title, url, sents))
        cls.append([cid, need, pages])
    return cls


def teach(webg, guides, state_dir, teach_exact, log):
    rc, out, err = run_bin([webg, 'teach', guides, state_dir], HERE)
    log.append('TEACH|rc=%d' % rc)
    for l in out.split('\n'):
        if l.startswith('LEARN|'):
            log.append('TEACH|' + l)
    installed = [l for l in out.split('\n') if '|INSTALLED|' in l]
    rejected = [l for l in out.split('\n') if '|REJECTED|' in l]
    g7rej = any('G7|REJECTED' in l for l in rejected)
    inst_ids = []
    for l in installed:
        parts = l.split('|')
        if len(parts) >= 3 and parts[0].endswith('LEARN'):
            inst_ids.append(parts[1])
        elif len(parts) >= 2:
            inst_ids.append(parts[-2] if parts[-2].startswith(('G', 'E')) else parts[1])
    if rc == 3 or not g7rej or sorted(inst_ids) != teach_exact:
        log.append('TEACH|VOID|installed=%s g7rej=%s' % (','.join(sorted(inst_ids)), g7rej))
        return False
    log.append('TEACH|VALID|installed=%s G7 rejected' % ','.join(sorted(inst_ids)))
    return True


def run_cluster(webg, state_dir, workdir, cid, need, pages, log, kledger,
                rledger, gate_counts, kid_box):
    pages = list(pages)
    if len(pages) < 2:
        rledger.append('R|%s|NO_CORROBORATION|-|fewer than 2 pages available for cross-check|%s'
                       % (cid, ';'.join(u for _, _, u, _ in pages)))
        gate_counts['NO_CORROBORATION'] = gate_counts.get('NO_CORROBORATION', 0) + 1
        log.append('%s|WITHHOLD|NO_CORROBORATION|insufficient pages' % cid)
        return

    need_file = os.path.join(workdir, 'need.txt')
    with open(need_file, 'w') as f:
        f.write(need + '\n')

    rc, out, err = run_bin([webg, 'query', state_dir, need_file], HERE)
    with open(os.path.join(workdir, 'query.out'), 'w') as f:
        f.write(out)
    if rc != 0:
        rledger.append('R|%s|CRASH|-|query rc=%d %s|%s'
                       % (cid, rc, err[-200:], ';'.join(u for _, _, u, _ in pages)))
        gate_counts['CRASH'] = gate_counts.get('CRASH', 0) + 1
        log.append('%s|CRASH|query rc=%d' % (cid, rc))
        return
    queries = [l.split('|', 1)[1] for l in out.split('\n') if l.startswith('QUERY|')]
    if not queries:
        rledger.append('R|%s|PARSE_FAIL|-|query emitted no QUERY line|%s'
                       % (cid, ';'.join(u for _, _, u, _ in pages)))
        gate_counts['PARSE_FAIL'] = gate_counts.get('PARSE_FAIL', 0) + 1
        log.append('%s|PARSE_FAIL|no QUERY' % cid)
        return
    log.append('%s|QUERY|%s' % (cid, queries[0]))

    res_file = os.path.join(workdir, 'results.txt')
    with open(res_file, 'w') as f:
        f.write('Q|' + queries[0] + '\n')
        for pid, title, url, sents in pages:
            f.write('R|%s|%s|%s\n' % (pid, title, sents[0][:160]))
    rc, out, err = run_bin([webg, 'select', state_dir, res_file], HERE)
    with open(os.path.join(workdir, 'select.out'), 'w') as f:
        f.write(out)
    if rc != 0:
        rledger.append('R|%s|CRASH|-|select rc=%d %s|%s'
                       % (cid, rc, err[-200:], ';'.join(u for _, _, u, _ in pages)))
        gate_counts['CRASH'] = gate_counts.get('CRASH', 0) + 1
        log.append('%s|CRASH|select rc=%d' % (cid, rc))
        return
    opens = []
    for l in out.split('\n'):
        if l.startswith('OPEN|'):
            opens = l.split('|', 1)[1].split()
    log.append('%s|OPEN|%s' % (cid, ' '.join(opens)))
    if not opens:
        rledger.append('R|%s|SELECT_EMPTY|-|select opened no pages|%s'
                       % (cid, ';'.join(u for _, _, u, _ in pages)))
        gate_counts['SELECT_EMPTY'] = gate_counts.get('SELECT_EMPTY', 0) + 1
        log.append('%s|WITHHOLD|SELECT_EMPTY' % cid)
        return

    pages_file = os.path.join(workdir, 'pages.txt')
    with open(pages_file, 'w') as f:
        for pid, title, url, sents in pages:
            if pid not in opens:
                continue
            f.write('P|%s|%s\n' % (pid, title))
            f.write('H|%s\n' % host_of(url))
            for s in sents:
                f.write('S|%s\n' % s)

    rc, out, err = run_bin([webg, 'verdict', state_dir, need_file, pages_file,
                            'FACT', queries[0]], HERE)
    with open(os.path.join(workdir, 'verdict.out'), 'w') as f:
        f.write(out)
    if rc != 0:
        rledger.append('R|%s|CRASH|-|verdict rc=%d %s|%s'
                       % (cid, rc, err[-200:], ';'.join(u for _, _, u, _ in pages)))
        gate_counts['CRASH'] = gate_counts.get('CRASH', 0) + 1
        log.append('%s|CRASH|verdict rc=%d' % (cid, rc))
        return

    inj = [l.split('|', 2)[2] for l in out.split('\n') if l.startswith('FLAG|INJECTION|')]
    for p in inj:
        log.append('%s|FLAG|INJECTION|%s' % (cid, p))
    uncheckable = any(l.startswith('ANSWER|UNCHECKABLE') for l in out.split('\n'))
    answer = [l.split('|', 1)[1] for l in out.split('\n')
              if l.startswith('ANSWER|') and l != 'ANSWER|UNCHECKABLE']
    provs = []
    for l in out.split('\n'):
        if l.startswith('PROV|1|'):
            p = l.split('|', 2)[2]
            if p not in provs:
                provs.append(p)
    urlmap = {pid: url for pid, _, url, _ in pages}

    if uncheckable or not answer:
        gatel = [l for l in out.split('\n') if l.startswith('GATE|')]
        rledger.append('R|%s|NO_CORROBORATION|-|no sentence corroborated on >=2 pages%s%s|%s'
                       % (cid, ' (inj-flags: %s)' % ','.join(inj) if inj else '',
                          ' [%s]' % ';'.join(gatel) if gatel else '',
                          ';'.join(urlmap[p] for p in opens if p in urlmap)))
        gate_counts['NO_CORROBORATION'] = gate_counts.get('NO_CORROBORATION', 0) + 1
        log.append('%s|WITHHOLD|NO_CORROBORATION|inj=%s' % (cid, ','.join(inj)))
        return

    claim = answer[0]
    bad = [p for p in provs if p in inj]
    if bad:
        rledger.append('R|%s|INTEGRITY_VIOLATION|%s|claim cited injection-flagged page(s) %s; refused install|%s'
                       % (cid, claim, ','.join(bad), ';'.join(urlmap[p] for p in provs if p in urlmap)))
        gate_counts['INTEGRITY_VIOLATION'] = gate_counts.get('INTEGRITY_VIOLATION', 0) + 1
        log.append('%s|INTEGRITY_VIOLATION|cited %s' % (cid, ','.join(bad)))
        return
    if len(provs) >= 2:
        kid_box[0] += 1
        kid_s = 'LI-%04d' % kid_box[0]
        kledger.append('K|%s|%s|%s' % (kid_s, cid, claim))
        for p in provs:
            kledger.append('P|%s|%s|%s' % (kid_s, p, urlmap.get(p, '?')))
        log.append('%s|INSTALL|%s|%s|provs=%s' % (cid, kid_s, claim[:80], ','.join(provs)))
    else:
        rledger.append('R|%s|NO_CORROBORATION|%s|claim on 1 page only|%s'
                       % (cid, claim, ';'.join(urlmap[p] for p in provs if p in urlmap)))
        gate_counts['NO_CORROBORATION'] = gate_counts.get('NO_CORROBORATION', 0) + 1
        log.append('%s|WITHHOLD|NO_CORROBORATION|single-source' % cid)


def fetch_fixture(cid, urls, log, rledger, gate_counts, fstat, fid):
    pages = []
    for i, url in enumerate(urls):
        pid = '%s-p%d' % (cid, i + 1)
        key = (cid, pid)
        if key in fstat:
            furl, ok, note = fstat[key]
            if furl != url:
                log.append('%s|URLMISMATCH|%s|manifest=%s|snapshot=%s' % (cid, pid, url, furl))
                url = furl
        else:
            furl, ok, note = url, ('ok' if os.path.exists(
                os.path.join(SNAPDIR, cid, pid + '.txt')) else 'FAIL'), ''
        if ok != 'ok' or not os.path.exists(os.path.join(SNAPDIR, cid, pid + '.txt')):
            rledger.append('R|%s|UNSUPPORTED_FETCH|-|fetch failed: %s|%s'
                           % (cid, note or 'no snapshot', url))
            gate_counts['UNSUPPORTED_FETCH'] = gate_counts.get('UNSUPPORTED_FETCH', 0) + 1
            log.append('%s|FETCH|FAIL|%s|%s' % (cid, pid, note or 'no snapshot'))
            continue
        verdict, reason = fid.get((cid, pid), ('UNVERIFIED', 'no fidelity record'))
        if verdict != 'VERIFIED':
            log.append('SNAPSHOT_UNVERIFIED|%s|%s|%s' % (cid, pid, reason))
            rledger.append('R|%s|SNAPSHOT_UNVERIFIED|-|excluded from instrument input: fidelity unverified (%s)|%s'
                           % (cid, reason or 'no reason given', url))
            gate_counts['SNAPSHOT_UNVERIFIED'] = gate_counts.get('SNAPSHOT_UNVERIFIED', 0) + 1
            log.append('%s|FETCH|UNVERIFIED|%s' % (cid, pid))
            continue
        with open(os.path.join(SNAPDIR, cid, pid + '.txt'),
                  encoding='utf-8', errors='replace') as f:
            raw = f.read().split('\n')
        title = raw[0][len('TITLE:'):].strip() if raw and raw[0].startswith('TITLE:') else pid
        sents = split_sentences('\n'.join(raw[1:]))
        if not sents:
            rledger.append('R|%s|PARSE_FAIL|-|no sentences after split|%s' % (cid, url))
            gate_counts['PARSE_FAIL'] = gate_counts.get('PARSE_FAIL', 0) + 1
            log.append('%s|FETCH|EMPTY|%s' % (cid, pid))
            continue
        pages.append((pid, title, url, sents))
        log.append('%s|FETCH|ok|%s|%d sentences' % (cid, pid, len(sents)))
    return pages


def run_pass(arm, cfg, passdir, fixtures, pclusters, fstat, fid):
    os.makedirs(passdir, exist_ok=True)
    state_dir = os.path.join(passdir, 'state')
    os.makedirs(state_dir, exist_ok=True)
    log = ['LI-PRUN|arm=%s|fixtures=60|pclusters=4' % arm]

    if not teach(cfg['webg'], cfg['guides'], state_dir, cfg['teach_exact'], log):
        with open(os.path.join(passdir, 'run_li.log'), 'w') as f:
            f.write('\n'.join(log) + '\n')
        print('VOID|arm=%s teach validation failed' % arm)
        return False

    kledger, rledger = [], []
    kid_box = [0]
    gate_counts = {}

    for cid, need, urls in fixtures:
        workdir = os.path.join(passdir, 'work', cid)
        os.makedirs(workdir, exist_ok=True)
        pages = fetch_fixture(cid, urls, log, rledger, gate_counts, fstat, fid)
        run_cluster(cfg['webg'], state_dir, workdir, cid, need, pages, log,
                    kledger, rledger, gate_counts, kid_box)

    for cid, need, pages in pclusters:
        workdir = os.path.join(passdir, 'work', cid)
        os.makedirs(workdir, exist_ok=True)
        log.append('%s|REDSRC|direct red-team battery read (pinned in prereg)' % cid)
        run_cluster(cfg['webg'], state_dir, workdir, cid, need, pages, log,
                    kledger, rledger, gate_counts, kid_box)

    n_install = sum(1 for l in kledger if l.startswith('K|'))
    with open(os.path.join(passdir, 'knowledge_ledger.txt'), 'w') as f:
        f.write('\n'.join(kledger) + ('\n' if kledger else ''))
    with open(os.path.join(passdir, 'refusal_ledger.txt'), 'w') as f:
        f.write('\n'.join(rledger) + ('\n' if rledger else ''))
    log.append('SUMMARY|arm=%s|clusters=%d|installed=%d|withheld=%d|gates=%s'
               % (arm, len(fixtures) + len(pclusters), n_install, len(rledger),
                  ','.join('%s=%d' % kv for kv in sorted(gate_counts.items()))))
    blob = '\n'.join(log) + '\n'
    with open(os.path.join(passdir, 'run_li.log'), 'w') as f:
        f.write(blob)
    print('DONE|arm=%s|passdir=%s|clusters=%d|installed=%d|withheld=%d|sha_log=%s'
          % (arm, passdir, len(fixtures) + len(pclusters), n_install, len(rledger),
             hashlib.sha256(blob.encode()).hexdigest()))
    return True


def main():
    outdir = sys.argv[1]
    fixtures = load_manifest(MANIFEST)
    fstat = load_fetch_status(SNAPDIR)
    fid = load_fidelity(SNAPDIR)
    pclusters = load_p_clusters()
    print('LOADED|fixtures=%d|pclusters=%d' % (len(fixtures), len(pclusters)))

    for arm, cfg in ARMS.items():
        for p in (1, 2):
            passdir = os.path.join(outdir, arm, 'pass%d' % p)
            if not run_pass(arm, cfg, passdir, fixtures, pclusters, fstat, fid):
                sys.exit(3)

    # determinism: pass1 vs pass2 byte-identical per arm
    ok = True
    for arm in ARMS:
        p1 = os.path.join(outdir, arm, 'pass1')
        p2 = os.path.join(outdir, arm, 'pass2')
        for f in ('knowledge_ledger.txt', 'refusal_ledger.txt', 'run_li.log'):
            same = filecmp.cmp(os.path.join(p1, f), os.path.join(p2, f), shallow=False)
            print('DET|arm=%s|%s|%s' % (arm, f, 'IDENTICAL' if same else 'DIFFER'))
            ok = ok and same
    print('DETERMINISM|%s' % ('PASS' if ok else 'FAIL'))
    sys.exit(0 if ok else 4)


if __name__ == '__main__':
    main()
