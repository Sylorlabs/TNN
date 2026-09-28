#!/usr/bin/env python3
"""LI-1 ingestion driver: runs the GENUINE learning path (frozen webg instrument)
over snapshotted live-web pages. Glue only: fetch/split/format/orchestrate.
All reasoning (query formulation, selection, claim extraction, corroboration,
injection scan, verdict) is the Zag instrument.

Usage: run_li.py <manifest> <snapdir> <outdir>
  manifest: urls manifest (C| / U| lines)
  snapdir:  corpus_snap/ tree (written by the fetch step, never re-fetched)
  outdir:   run outputs (state/, work/, knowledge_ledger.txt, refusal_ledger.txt, run_li.log)

Determinism: no timestamps anywhere; manifest order preserved; two runs over the
same snapshot must be byte-identical (SHA256 printed at the end).
"""
import os, re, sys, hashlib, subprocess
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
WEBG = os.environ.get('REDTEAM_WEBG', os.path.join(PARENT, 'webg'))
GUIDES = os.path.normpath(os.path.join(PARENT, '..', '..', 'guides'))

GATES = ('INJECTION_FLAG', 'NO_CORROBORATION', 'PARSE_FAIL', 'GATE_MISFIRE',
         'CRASH', 'UNSUPPORTED_FETCH', 'SELECT_EMPTY', 'INTEGRITY_VIOLATION')


def host_of(url):
    """Registrable host for the source-independence gate. Formatting only."""
    try:
        h = urlparse(url).hostname or ''
    except Exception:
        h = ''
    return h.lower()


def toks(s):
    return re.findall(r'[a-z0-9]+', s.lower())


def load_manifest(path):
    clusters = []          # (cid, need, [urls])
    order = {}
    with open(path) as f:
        for line in f:
            line = line.rstrip('\n')
            if not line or line.startswith('#'):
                continue
            parts = line.split('|')
            if parts[0] == 'C':
                cid, need = parts[1], '|'.join(parts[2:])
                clusters.append([cid, need, []])
                order[cid] = len(clusters) - 1
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


def split_sentences(text):
    """Deterministic sentence splitter. Formatting only, no reasoning."""
    lines = []
    for ln in text.split('\n'):
        s = ' '.join(ln.split())
        if not s:
            continue
        if s.startswith('【') or s.startswith('Images:'):
            continue
        lines.append(s)
    blob = ' '.join(lines)
    raw = re.split(r'(?<=[.!?])\s+', blob)
    out = []
    for s in raw:
        s = ' '.join(s.split())
        if len(toks(s)) < 4:
            continue
        if len(s) > 600:
            continue
        out.append(s)
        if len(out) >= 400:
            break
    return out


def run_bin(args, cwd):
    r = subprocess.run(args, capture_output=True, text=True, cwd=cwd)
    return r.returncode, r.stdout, r.stderr


def main():
    manifest, snapdir, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
    os.makedirs(outdir, exist_ok=True)
    state_dir = os.path.join(outdir, 'state')
    os.makedirs(state_dir, exist_ok=True)
    log = []
    log.append('LI-RUN|manifest=%s' % os.path.basename(manifest))

    # ---- teach once (replicate WG-1 teach validation: G1-G6 in, G7 out) ----
    rc, out, err = run_bin([WEBG, 'teach', GUIDES, state_dir], HERE)
    log.append('TEACH|rc=%d' % rc)
    for l in out.split('\n'):
        if l.startswith('LEARN|'):
            log.append('TEACH|' + l)
    installed = [l for l in out.split('\n') if '|INSTALLED|' in l]
    rejected = [l for l in out.split('\n') if '|REJECTED|' in l]
    g7rej = any('G7|REJECTED' in l for l in rejected)
    if rc == 3 or not g7rej or len(installed) < 6:
        log.append('TEACH|VOID')
        blob = '\n'.join(log) + '\n'
        with open(os.path.join(outdir, 'run_li.log'), 'w') as f:
            f.write(blob)
        print('VOID|teach validation failed rc=%d g7rej=%s installed=%d' % (rc, g7rej, len(installed)))
        sys.exit(3)
    log.append('TEACH|VALID|G1-G6 installed, G7 rejected')

    clusters = load_manifest(manifest)
    fstat = load_fetch_status(snapdir)
    kledger, rledger = [], []
    kid = 0
    n_install = 0
    gate_counts = {}
    integrity_violations = []

    for cid, need, urls in clusters:
        workdir = os.path.join(outdir, 'work', cid)
        os.makedirs(workdir, exist_ok=True)
        # pages available in snapshot
        pages = []  # (pid, title, url, sentences)
        for i, url in enumerate(urls):
            pid = '%s-p%d' % (cid, i + 1)
            key = (cid, pid)
            snap = os.path.join(snapdir, cid, pid + '.txt')
            if key in fstat:
                furl, ok, note = fstat[key]
            else:
                furl, ok, note = url, ('ok' if os.path.exists(snap) else 'FAIL'), ''
            if ok != 'ok' or not os.path.exists(snap):
                rledger.append('R|%s|UNSUPPORTED_FETCH|-|fetch failed: %s|%s'
                               % (cid, note or 'no snapshot', url))
                gate_counts['UNSUPPORTED_FETCH'] = gate_counts.get('UNSUPPORTED_FETCH', 0) + 1
                log.append('%s|FETCH|FAIL|%s|%s' % (cid, pid, note or 'no snapshot'))
                continue
            with open(snap, encoding='utf-8', errors='replace') as f:
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

        if len(pages) < 2:
            rledger.append('R|%s|NO_CORROBORATION|-|fewer than 2 pages available for cross-check|%s'
                           % (cid, ';'.join(urls)))
            gate_counts['NO_CORROBORATION'] = gate_counts.get('NO_CORROBORATION', 0) + 1
            log.append('%s|WITHHOLD|NO_CORROBORATION|insufficient pages' % cid)
            continue

        need_file = os.path.join(workdir, 'need.txt')
        with open(need_file, 'w') as f:
            f.write(need + '\n')

        rc, out, err = run_bin([WEBG, 'query', state_dir, need_file], HERE)
        with open(os.path.join(workdir, 'query.out'), 'w') as f:
            f.write(out)
        if rc != 0:
            rledger.append('R|%s|CRASH|-|query rc=%d %s|%s'
                           % (cid, rc, err[-200:], ';'.join(u for _, _, u, _ in pages)))
            gate_counts['CRASH'] = gate_counts.get('CRASH', 0) + 1
            log.append('%s|CRASH|query rc=%d' % (cid, rc))
            continue
        queries = [l.split('|', 1)[1] for l in out.split('\n') if l.startswith('QUERY|')]
        if not queries:
            rledger.append('R|%s|PARSE_FAIL|-|query emitted no QUERY line|%s'
                           % (cid, ';'.join(u for _, _, u, _ in pages)))
            gate_counts['PARSE_FAIL'] = gate_counts.get('PARSE_FAIL', 0) + 1
            log.append('%s|PARSE_FAIL|no QUERY' % cid)
            continue
        log.append('%s|QUERY|%s' % (cid, queries[0]))

        # select over the cluster's pages (G2: open 2-3, skip dupe titles)
        res_file = os.path.join(workdir, 'results.txt')
        with open(res_file, 'w') as f:
            f.write('Q|' + queries[0] + '\n')
            for pid, title, url, sents in pages:
                f.write('R|%s|%s|%s\n' % (pid, title, sents[0][:160]))
        rc, out, err = run_bin([WEBG, 'select', state_dir, res_file], HERE)
        with open(os.path.join(workdir, 'select.out'), 'w') as f:
            f.write(out)
        if rc != 0:
            rledger.append('R|%s|CRASH|-|select rc=%d %s|%s'
                           % (cid, rc, err[-200:], ';'.join(u for _, _, u, _ in pages)))
            gate_counts['CRASH'] = gate_counts.get('CRASH', 0) + 1
            log.append('%s|CRASH|select rc=%d' % (cid, rc))
            continue
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
            continue

        pages_file = os.path.join(workdir, 'pages.txt')
        with open(pages_file, 'w') as f:
            for pid, title, url, sents in pages:
                if pid not in opens:
                    continue
                f.write('P|%s|%s\n' % (pid, title))
                f.write('H|%s\n' % host_of(url))
                for s in sents:
                    f.write('S|%s\n' % s)

        rc, out, err = run_bin([WEBG, 'verdict', state_dir, need_file, pages_file,
                                'FACT', queries[0]], HERE)
        with open(os.path.join(workdir, 'verdict.out'), 'w') as f:
            f.write(out)
        if rc != 0:
            rledger.append('R|%s|CRASH|-|verdict rc=%d %s|%s'
                           % (cid, rc, err[-200:], ';'.join(u for _, _, u, _ in pages)))
            gate_counts['CRASH'] = gate_counts.get('CRASH', 0) + 1
            log.append('%s|CRASH|verdict rc=%d' % (cid, rc))
            continue

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
            unchecked = [l.split('|', 1)[1] for l in out.split('\n') if l.startswith('UNCHECKED|')]
            gatel = [l for l in out.split('\n') if l.startswith('GATE|')]
            rledger.append('R|%s|NO_CORROBORATION|-|no sentence corroborated on >=2 pages%s%s|%s'
                           % (cid, ' (inj-flags: %s)' % ','.join(inj) if inj else '',
                              ' [%s]' % ';'.join(gatel) if gatel else '',
                              ';'.join(urlmap[p] for p in opens if p in urlmap)))
            gate_counts['NO_CORROBORATION'] = gate_counts.get('NO_CORROBORATION', 0) + 1
            log.append('%s|WITHHOLD|NO_CORROBORATION|inj=%s' % (cid, ','.join(inj)))
            continue

        claim = answer[0]
        bad = [p for p in provs if p in inj]
        if bad:
            # integrity veto: never install a claim citing an injected page
            integrity_violations.append((cid, claim, bad))
            rledger.append('R|%s|INTEGRITY_VIOLATION|%s|claim cited injection-flagged page(s) %s; refused install|%s'
                           % (cid, claim, ','.join(bad), ';'.join(urlmap[p] for p in provs if p in urlmap)))
            gate_counts['INTEGRITY_VIOLATION'] = gate_counts.get('INTEGRITY_VIOLATION', 0) + 1
            log.append('%s|INTEGRITY_VIOLATION|cited %s' % (cid, ','.join(bad)))
            continue
        if len(provs) >= 2:
            kid += 1
            kid_s = 'LI-%04d' % kid
            kledger.append('K|%s|%s|%s' % (kid_s, cid, claim))
            for p in provs:
                kledger.append('P|%s|%s|%s' % (kid_s, p, urlmap.get(p, '?')))
            n_install += 1
            log.append('%s|INSTALL|%s|%s|provs=%s' % (cid, kid_s, claim[:80], ','.join(provs)))
        else:
            rledger.append('R|%s|NO_CORROBORATION|%s|claim on 1 page only|%s'
                           % (cid, claim, ';'.join(urlmap[p] for p in provs if p in urlmap)))
            gate_counts['NO_CORROBORATION'] = gate_counts.get('NO_CORROBORATION', 0) + 1
            log.append('%s|WITHHOLD|NO_CORROBORATION|single-source' % cid)

    with open(os.path.join(outdir, 'knowledge_ledger.txt'), 'w') as f:
        f.write('\n'.join(kledger) + ('\n' if kledger else ''))
    with open(os.path.join(outdir, 'refusal_ledger.txt'), 'w') as f:
        f.write('\n'.join(rledger) + ('\n' if rledger else ''))
    log.append('SUMMARY|clusters=%d|installed=%d|withheld=%d|gates=%s|integrity_violations=%d'
               % (len(clusters), n_install, len(rledger),
                  ','.join('%s=%d' % kv for kv in sorted(gate_counts.items())),
                  len(integrity_violations)))
    blob = '\n'.join(log) + '\n'
    with open(os.path.join(outdir, 'run_li.log'), 'w') as f:
        f.write(blob)
    sha = hashlib.sha256(blob.encode()).hexdigest()
    kl = hashlib.sha256(('\n'.join(kledger) + '\n').encode()).hexdigest() if kledger else hashlib.sha256(b'').hexdigest()
    rl = hashlib.sha256(('\n'.join(rledger) + '\n').encode()).hexdigest() if rledger else hashlib.sha256(b'').hexdigest()
    print('DONE|clusters=%d|installed=%d|withheld=%d|sha_log=%s|sha_knowledge=%s|sha_refusal=%s'
          % (len(clusters), n_install, len(rledger), sha, kl, rl))


if __name__ == '__main__':
    main()
