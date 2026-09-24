#!/usr/bin/env python3
"""V-QUAR (H3) orchestration driver: prod/train runs + quarantine + merge gate.

Mirrors run_forkbase.py's cluster loop (teach -> query/select/verdict ->
ledgers) with two differences:
  * --binary prod|train selects the instrument (webg_prod / webg_train).
  * --train additionally collects QUAR|1 lines from verdict stdout, writes
    Q claim files + the quarantine ledger, then runs the merge gate
    (webg_merge) per claim.

Determinism contract: the glue chdir()s into the outdir before running any
instrument, and every instrument path is RELATIVE (state, work/<cid>/...,
quarantine/claims/...). The read-audit hashes path strings, so identical
relative layouts => byte-identical audit logs across passes. Absolute host
paths (snapdir, guides) never reach an instrument argv... except guides:
teach takes the guides dir, passed as a relative path from the outdir.

Stdout artifacts (compared byte-for-byte): knowledge_ledger.txt,
refusal_ledger.txt, run_li.log, quarantine_ledger.txt, claims/*,
merge_verdicts.txt, audit.log. Instrument stdout -> work/<cid>/*.out;
instrument stderr (audit lines) -> audit.log (concatenated, run order).

Python glue only; all reasoning is the Zag instrument. Zero RNG.

Usage: run_vquar.py --binary prod|train --guides <dir> --manifest <m>
                    --snapdir <s> --outdir <o> [--merge]
  --merge: after a train run, adjudicate every quarantined claim.
"""
import os, re, sys, hashlib, subprocess, argparse
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = {'prod': os.path.join(HERE, 'webg_prod'),
       'train': os.path.join(HERE, 'webg_train'),
       'merge': os.path.join(HERE, 'webg_merge')}

def host_of(url):
    try:
        h = urlparse(url).hostname or ''
    except Exception:
        h = ''
    return h.lower()

def toks(s):
    return re.findall(r'[a-z0-9]+', s.lower())

def fnv1a64(b):
    h = 14695981039346656037
    for x in b:
        h = ((h ^ x) * 1099511628211) & 0xFFFFFFFFFFFFFFFF
    return '%016x' % h

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

def run_bin(args):
    r = subprocess.run(args, capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--binary', required=True, choices=('prod', 'train'))
    ap.add_argument('--guides', required=True)
    ap.add_argument('--manifest', required=True)
    ap.add_argument('--snapdir', required=True)
    ap.add_argument('--outdir', required=True)
    ap.add_argument('--merge', action='store_true')
    a = ap.parse_args()
    if a.merge and a.binary != 'train':
        print('VOID|--merge requires --binary train')
        sys.exit(3)

    outdir = os.path.abspath(a.outdir)
    os.makedirs(outdir, exist_ok=True)
    os.makedirs(os.path.join(outdir, 'work'), exist_ok=True)
    # guides as a relative path from the outdir: same string every pass.
    guides_rel = os.path.relpath(os.path.abspath(a.guides), outdir)
    audit = open(os.path.join(outdir, 'audit.log'), 'w')

    os.chdir(outdir)  # all instrument paths below are relative
    state_dir = 'state'
    os.makedirs(state_dir, exist_ok=True)
    log = ['LI-RUN|manifest=%s' % os.path.basename(a.manifest),
           'LI-RUN|binary=%s' % a.binary]

    rc, out, err = run_bin([BIN[a.binary], 'teach', guides_rel, state_dir])
    audit.write(err)
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
            inst_ids.append(parts[-2] if parts[-2].startswith('G') else parts[1])
    exact_teach = (sorted(inst_ids) == ['G1', 'G2', 'G3', 'G4', 'G5', 'G6'])
    if rc == 3 or not g7rej or not exact_teach:
        log.append('TEACH|VOID|installed=%s g7rej=%s' % (','.join(sorted(inst_ids)), g7rej))
        with open('run_li.log', 'w') as f:
            f.write('\n'.join(log) + '\n')
        audit.close()
        print('VOID|teach validation failed rc=%d g7rej=%s installed=%s (need G1-G6 exactly once each)'
              % (rc, g7rej, ','.join(sorted(inst_ids))))
        sys.exit(3)
    log.append('TEACH|VALID|G1-G6 installed exactly once each, G7 rejected')

    # stoplist for the quarantine path (TRAIN only; harmless for PROD)
    with open(os.path.join(HERE, 'stoplist_para.txt'), 'rb') as f:
        stop = f.read()
    with open(os.path.join(state_dir, 'stoplist_para.txt'), 'wb') as f:
        f.write(stop)

    clusters = load_manifest(a.manifest)
    fstat = load_fetch_status(a.snapdir)
    fid = load_fidelity(a.snapdir)
    kledger, rledger, qledger = [], [], []
    qclaims = []  # (qid, cid, pids_csv, claim, query, need_rel, pages_rel)
    qseq, qprev, qn = 0, '0' * 16, 0
    kid, n_install = 0, 0
    gate_counts = {}

    for cid, need, urls in clusters:
        workdir = os.path.join('work', cid)
        os.makedirs(workdir, exist_ok=True)
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
                    os.path.join(a.snapdir, cid, pid + '.txt')) else 'FAIL'), ''
            if ok != 'ok' or not os.path.exists(os.path.join(a.snapdir, cid, pid + '.txt')):
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
            with open(os.path.join(a.snapdir, cid, pid + '.txt'), encoding='utf-8', errors='replace') as f:
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

        rc, out, err = run_bin([BIN[a.binary], 'query', state_dir, need_file])
        audit.write(err)
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

        res_file = os.path.join(workdir, 'results.txt')
        with open(res_file, 'w') as f:
            f.write('Q|' + queries[0] + '\n')
            for pid, title, url, sents in pages:
                f.write('R|%s|%s|%s\n' % (pid, title, sents[0][:160]))
        rc, out, err = run_bin([BIN[a.binary], 'select', state_dir, res_file])
        audit.write(err)
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

        rc, out, err = run_bin([BIN[a.binary], 'verdict', state_dir, need_file, pages_file,
                                'FACT', queries[0]])
        audit.write(err)
        with open(os.path.join(workdir, 'verdict.out'), 'w') as f:
            f.write(out)
        if rc != 0:
            rledger.append('R|%s|CRASH|-|verdict rc=%d %s|%s'
                           % (cid, rc, err[-200:], ';'.join(u for _, _, u, _ in pages)))
            gate_counts['CRASH'] = gate_counts.get('CRASH', 0) + 1
            log.append('%s|CRASH|verdict rc=%d' % (cid, rc))
            continue

        # quarantine collection (TRAIN only)
        for l in out.split('\n'):
            if l.startswith('QUAR|1|'):
                _, _, pids_csv, claim = l.split('|', 3)
                qn += 1
                qid = 'Q%04d' % qn
                qclaims.append((qid, cid, pids_csv, claim, queries[0],
                                need_file, pages_file))
                log.append('%s|QUARANTINED|%s|%s|%s' % (cid, qid, pids_csv, claim[:80]))
        for l in out.split('\n'):
            if l.startswith('GATE|PARA|'):
                log.append('%s|GATE|%s' % (cid, l))

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
            continue

        claim = answer[0]
        bad = [p for p in provs if p in inj]
        if bad:
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

    # quarantine ledger + claim files (TRAIN only)
    # Q chain uses SHA-256, separate from P chains (H3: separate SHA chains).
    if a.binary == 'train' and qclaims:
        os.makedirs(os.path.join('quarantine', 'claims'), exist_ok=True)
        for (qid, cid, pids_csv, claim, query, need_file, pages_file) in qclaims:
            qseq += 1
            csha = hashlib.sha256(claim.encode()).hexdigest()
            row = 'Q|%d|%s|%s|%s|%s|%s' % (qseq, qid, cid, pids_csv, csha, qprev)
            qledger.append(row)
            qprev = hashlib.sha256(row.encode()).hexdigest()
            cpath = os.path.join('quarantine', 'claims', qid + '.txt')
            with open(cpath, 'w') as f:
                f.write('QC|%s|%s|%s|%s\n' % (qid, cid, claim, query))
        log.append('QUAR|SUMMARY|claims=%d' % len(qclaims))

    with open('knowledge_ledger.txt', 'w') as f:
        f.write('\n'.join(kledger) + ('\n' if kledger else ''))
    with open('refusal_ledger.txt', 'w') as f:
        f.write('\n'.join(rledger) + ('\n' if rledger else ''))
    if a.binary == 'train':
        with open('quarantine_ledger.txt', 'w') as f:
            f.write('\n'.join(qledger) + ('\n' if qledger else ''))

    # merge gate (TRAIN + --merge)
    mlines = []
    if a.merge:
        for (qid, cid, pids_csv, claim, query, need_file, pages_file) in qclaims:
            cpath = os.path.join('quarantine', 'claims', qid + '.txt')
            rc, out, err = run_bin([BIN['merge'], 'merge', state_dir, need_file,
                                    pages_file, cpath, qid])
            audit.write(err)
            got = [l for l in out.split('\n') if l.startswith('MERGE|')]
            mlines.extend(got)
            log.append('%s|MERGE|%s|%s' % (cid, qid, got[0] if got else 'NOOUTPUT rc=%d' % rc))
        with open('merge_verdicts.txt', 'w') as f:
            f.write('\n'.join(mlines) + ('\n' if mlines else ''))
        log.append('MERGE|SUMMARY|adjudicated=%d|merged=%d'
                   % (len(mlines), sum(1 for l in mlines if l.endswith('|1'))))

    log.append('SUMMARY|clusters=%d|installed=%d|withheld=%d|quarantined=%d|gates=%s|integrity_violations=%d'
               % (len(clusters), n_install, len(rledger), len(qclaims),
                  ','.join('%s=%d' % kv for kv in sorted(gate_counts.items())), 0))
    blob = '\n'.join(log) + '\n'
    with open('run_li.log', 'w') as f:
        f.write(blob)
    kl = hashlib.sha256(('\n'.join(kledger) + '\n').encode()).hexdigest() if kledger else hashlib.sha256(b'').hexdigest()
    rl = hashlib.sha256(('\n'.join(rledger) + '\n').encode()).hexdigest() if rledger else hashlib.sha256(b'').hexdigest()
    audit.close()
    print('DONE|clusters=%d|installed=%d|withheld=%d|quarantined=%d|sha_log=%s|sha_knowledge=%s|sha_refusal=%s'
          % (len(clusters), n_install, len(rledger), len(qclaims),
             hashlib.sha256(blob.encode()).hexdigest(), kl, rl))

if __name__ == '__main__':
    main()
