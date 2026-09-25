#!/usr/bin/env python3
"""KPROD driver: live-ingestion knowledge-first production path.

Two arms x two passes over the kprod battery (default battery1x/).
Arm K: teach (frozen contract) + deliberate kbcommit, pending-diversion active.
Arm N: teach only, no knowledge -> frozen BF1 behavior.

Per arm/pass: Phase 0 teach -> [K: kbcommit] -> Phase 1 cluster verdicts
(query/select/verdict; `*b` follow-up clusters skipped, Phase-2 only) ->
[K, 1x only: Phase 2 scripted lifecycle] -> ledgers + run log.
Phase 3: pass-2 rerun of Phases 0-2 in a fresh state dir; byte-compare
pass1 vs pass2 across run logs, ledgers, knowledge.txt, pending.txt,
resolved.txt (exit 4 on any diff).

With --bf1 <frozen-binary>: after each N-arm pass, replays the N-arm
Phase-1 verdicts with the frozen BF1 binary into bf1_pass<N>/bf1.log so the
analyzer can prove KP7 (Arm N frozen-identity).

Pure orchestration; all reasoning is the Zag instrument. Zero RNG.

Usage: run_kprod.py <outdir> [--battery DIR] [--kb FILE] [--guides DIR]
                       [--no-lifecycle] [--bf1 PATH] [--force-10x]

Exit codes: 0 ok; 3 VOID (teach/kbcommit/lifecycle/frozen-replay failure);
4 determinism diff between passes.
"""
import os, re, sys, hashlib, subprocess, filecmp, shutil
from urllib.parse import urlparse

KPROD = os.path.dirname(os.path.abspath(__file__))
WEBG = os.path.join(KPROD, 'bin', 'instrument_kprod')
BATTERY_DEFAULT = os.path.join(KPROD, 'battery1x')
KB_DEFAULT = os.path.join(KPROD, 'knowledge_base.txt')
GUIDES_DEFAULT = os.path.join(KPROD, 'shake', 'guides')

TEACH_EXACT = sorted(['G1', 'G2', 'G3', 'G4', 'G5', 'G6'])
FOLLOWUP_RE = re.compile(r'.*\db$')   # pn-01b, pc-05b, ... -> Phase 2 only


def host_of(url):
    try:
        h = urlparse(url).hostname or ''
    except Exception:
        h = ''
    return h.lower()


def toks(s):
    return re.findall(r'[a-z0-9]+', s.lower())


def run_bin(args, cwd):
    r = subprocess.run(args, capture_output=True, text=True, cwd=cwd)
    return r.returncode, r.stdout, r.stderr


def load_clusters(battery):
    cls = []
    for cid in sorted(os.listdir(battery)):
        d = os.path.join(battery, cid)
        if not os.path.isdir(d):
            continue
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
            with open(os.path.join(d, 'p%d.txt' % n),
                      encoding='utf-8', errors='replace') as f:
                raw = f.read().split('\n')
            title = (raw[0][len('TITLE:'):].strip()
                     if raw and raw[0].startswith('TITLE:') else pid)
            sents = split_sentences('\n'.join(raw[1:]))
            pages.append((pid, title, url, sents))
        cls.append([cid, need, pages])
    return cls


def split_sentences(text):
    lines = []
    for ln in text.split('\n'):
        s = ' '.join(ln.split())
        if not s or s.startswith('TITLE:'):
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


def teach(webg, guides, state_dir, log):
    rc, out, err = run_bin([webg, 'teach', guides, state_dir], KPROD)
    log.append('TEACH|rc=%d' % rc)
    for l in out.split('\n'):
        if l.startswith('LEARN|'):
            log.append('TEACH|' + l)
    if rc != 0:
        log.append('TEACH|VOID|rc=%d' % rc)
        return False
    installed = {}
    for l in out.split('\n'):
        m = re.match(r'LEARN\|(G\d+)\|INSTALLED\|', l)
        if m:
            installed[m.group(1)] = installed.get(m.group(1), 0) + 1
    g7rej = any(re.match(r'LEARN\|G7\|REJECTED\|', l) for l in out.split('\n'))
    ok = (sorted(installed.keys()) == TEACH_EXACT
          and all(installed[g] == 1 for g in TEACH_EXACT)
          and g7rej)
    if not ok:
        log.append('TEACH|VOID|installed=%s g7rej=%s'
                   % (','.join('%s:%d' % t for t in sorted(installed.items())), g7rej))
        return False
    log.append('TEACH|VALID|installed=%s G7 rejected' % ','.join(TEACH_EXACT))
    return True


def count_claims(kbfile):
    n = 0
    with open(kbfile, encoding='utf-8', errors='replace') as f:
        for line in f:
            if line.strip():
                n += 1
    return n


def kbcommit(webg, kbfile, state_dir, log):
    expect = count_claims(kbfile)
    rc, out, err = run_bin([webg, 'kbcommit', kbfile, state_dir], KPROD)
    commits = [l for l in out.split('\n') if l.startswith('KB|COMMIT|')]
    log.append('KBCOMMIT|rc=%d|commits=%d|expected=%d' % (rc, len(commits), expect))
    for l in commits:
        log.append('KBCOMMIT|' + l)
    if rc != 0 or len(commits) != expect:
        log.append('KBCOMMIT|VOID|rc=%d commits=%d expected=%d'
                   % (rc, len(commits), expect))
        return False
    log.append('KBCOMMIT|VALID|%d claims deliberately committed' % len(commits))
    return True


def classify_verdict(out):
    """§2.6 precedence. Returns dict(class, seq, pseq, gate, claim, provs,
    kb_lines, investigate)."""
    lines = [l for l in out.split('\n') if l]
    corrob = [l for l in lines if l.startswith('KB|CORROBORATED|')]
    agree = [l for l in lines if l.startswith('KB|AGREE|')]
    contra = [l for l in lines if l.startswith('GATE|KB_CONTRADICTION|')]
    resfalse = [l for l in lines if l.startswith('GATE|KB_RESOLVED_FALSE|')]
    pending = [l for l in lines if l.startswith('GATE|KB_PENDING|')]
    kbpending = [l for l in lines if l.startswith('KB|PENDING|')]
    answers = [l.split('|', 1)[1] for l in lines
               if l.startswith('ANSWER|')
               and l not in ('ANSWER|UNVERIFIED', 'ANSWER|UNCHECKABLE')]
    provs = []
    for l in lines:
        if l.startswith('PROV|1|'):
            p = l.split('|', 2)[2]
            if p not in provs:
                provs.append(p)
    seq = None
    if corrob:
        try:
            seq = int(corrob[0].split('|')[2])
        except (ValueError, IndexError):
            seq = None
    elif agree:
        try:
            seq = int(agree[0].split('|')[2])
        except (ValueError, IndexError):
            seq = None
    pseq = None
    if kbpending:
        try:
            pseq = int(kbpending[0].split('|')[2])
        except (ValueError, IndexError):
            pseq = None
    d = dict(seq=seq, pseq=pseq, provs=provs,
             claim=answers[0] if answers else None)
    if corrob or agree:
        d['class'] = 'INSTALL'
        d['via'] = 'KB'
        return d
    if contra:
        d['class'] = 'WITHHOLD'
        d['gate'] = 'KB_CONTRADICTION'
        return d
    if resfalse:
        d['class'] = 'WITHHOLD'
        d['gate'] = 'KB_RESOLVED_FALSE'
        return d
    if pending:
        d['class'] = 'PENDING'
        return d
    if any(l == 'ANSWER|UNCHECKABLE' for l in lines):
        d['class'] = 'WITHHOLD'
        d['gate'] = 'NO_CORROBORATION'
        return d
    if answers:
        d['class'] = 'INSTALL'
        d['via'] = 'FROZEN'
        d['frozen_install_in_K'] = True
        return d
    d['class'] = 'WITHHOLD'
    d['gate'] = 'INVESTIGATE'
    d['investigate'] = True
    return d


def read_pending(state_dir):
    """Parse pending.txt -> list of (pseq, claim, pidcsv)."""
    out = []
    p = os.path.join(state_dir, 'pending.txt')
    if not os.path.exists(p):
        return out
    with open(p, encoding='utf-8', errors='replace') as f:
        for line in f:
            line = line.rstrip('\n')
            if not line.startswith('PB|'):
                continue
            parts = line.split('|')
            if len(parts) < 4:
                continue
            try:
                out.append((int(parts[1]), parts[2], parts[3]))
            except ValueError:
                continue
    return out


def run_cluster(webg, state_dir, workdir, cid, need, pages, log, kledger,
                rledger, pledger, gate_counts, kid_box, cmp_lines=None):
    pages = list(pages)
    if len(pages) < 2:
        rledger.append('R|%s|NO_CORROBORATION|-|fewer than 2 pages available for cross-check|%s'
                       % (cid, ';'.join(u for _, _, u, _ in pages)))
        gate_counts['NO_CORROBORATION'] = gate_counts.get('NO_CORROBORATION', 0) + 1
        log.append('%s|WITHHOLD|NO_CORROBORATION|insufficient pages' % cid)
        return dict(ok=False, reason='insufficient pages')

    need_file = os.path.join(workdir, 'need.txt')
    with open(need_file, 'w') as f:
        f.write(need + '\n')

    rc, out, err = run_bin([webg, 'query', state_dir, need_file], KPROD)
    with open(os.path.join(workdir, 'query.out'), 'w') as f:
        f.write(out)
    if rc != 0:
        rledger.append('R|%s|CRASH|-|query rc=%d %s|%s'
                       % (cid, rc, err[-200:], ';'.join(u for _, _, u, _ in pages)))
        gate_counts['CRASH'] = gate_counts.get('CRASH', 0) + 1
        log.append('%s|CRASH|query rc=%d' % (cid, rc))
        return dict(ok=False, reason='query rc=%d' % rc)
    queries = [l.split('|', 1)[1] for l in out.split('\n') if l.startswith('QUERY|')]
    if not queries:
        rledger.append('R|%s|PARSE_FAIL|-|query emitted no QUERY line|%s'
                       % (cid, ';'.join(u for _, _, u, _ in pages)))
        gate_counts['PARSE_FAIL'] = gate_counts.get('PARSE_FAIL', 0) + 1
        log.append('%s|PARSE_FAIL|no QUERY' % cid)
        return dict(ok=False, reason='no QUERY line')
    log.append('%s|QUERY|%s' % (cid, queries[0]))

    res_file = os.path.join(workdir, 'results.txt')
    with open(res_file, 'w') as f:
        f.write('Q|' + queries[0] + '\n')
        for pid, title, url, sents in pages:
            f.write('R|%s|%s|%s\n' % (pid, title, sents[0][:160] if sents else ''))
    rc, out, err = run_bin([webg, 'select', state_dir, res_file], KPROD)
    with open(os.path.join(workdir, 'select.out'), 'w') as f:
        f.write(out)
    if rc != 0:
        rledger.append('R|%s|CRASH|-|select rc=%d %s|%s'
                       % (cid, rc, err[-200:], ';'.join(u for _, _, u, _ in pages)))
        gate_counts['CRASH'] = gate_counts.get('CRASH', 0) + 1
        log.append('%s|CRASH|select rc=%d' % (cid, rc))
        return dict(ok=False, reason='select rc=%d' % rc)
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
        return dict(ok=False, reason='select empty')

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
                            'FACT', queries[0], ''], KPROD)
    with open(os.path.join(workdir, 'verdict.out'), 'w') as f:
        f.write(out)
    if cmp_lines is not None:
        cmp_lines.append('CMP|%s' % cid)
        cmp_lines.extend(l for l in out.strip('\n').split('\n') if l)
    if rc != 0:
        rledger.append('R|%s|CRASH|-|verdict rc=%d %s|%s'
                       % (cid, rc, err[-200:], ';'.join(u for _, _, u, _ in pages)))
        gate_counts['CRASH'] = gate_counts.get('CRASH', 0) + 1
        log.append('%s|CRASH|verdict rc=%d' % (cid, rc))
        return dict(ok=False, reason='verdict rc=%d' % rc)

    v = classify_verdict(out)
    v['ok'] = True
    lines = out.split('\n')
    inj = [l.split('|', 2)[2] for l in lines if l.startswith('FLAG|INJECTION|')]
    for p in inj:
        log.append('%s|FLAG|INJECTION|%s' % (cid, p))
    for l in lines:
        if l.startswith('KB|AGREE|'):
            log.append('%s|%s' % (cid, l))
    urlmap = {pid: url for pid, _, url, _ in pages}
    urls = ';'.join(urlmap[p] for p in opens if p in urlmap)

    if v['class'] == 'PENDING':
        pseq, claim = v['pseq'], None
        pidcsv = ''
        m = re.match(r'KB\|PENDING\|\d+\|(.+)', next(
            (l for l in lines if l.startswith('KB|PENDING|')), ''))
        if m:
            pidcsv = m.group(1)
        for pp, cl, pc in read_pending(state_dir):
            if pp == pseq:
                claim, pidcsv = cl, pc
                break
        pledger.append('D|%s|%s|%s|%s' % (cid, pseq if pseq is not None else '?',
                                         pidcsv, claim if claim else '-'))
        log.append('%s|PENDING|%s|%s|%s' % (cid, pseq, pidcsv,
                                           (claim or '-')[:80]))
        return v

    if v['class'] == 'WITHHOLD':
        gate = v.get('gate', 'UNKNOWN')
        claim = v.get('claim') or '-'
        rledger.append('R|%s|%s|%s|%s|%s'
                       % (cid, gate, claim,
                          'inj-flags: %s' % ','.join(inj) if inj else '-',
                          urls))
        gate_counts[gate] = gate_counts.get(gate, 0) + 1
        log.append('%s|WITHHOLD|%s|%s' % (cid, gate, (claim or '-')[:80]))
        return v

    # INSTALL
    claim = v.get('claim') or '-'
    provs = v['provs']
    bad = [p for p in provs if p in inj]
    if bad:
        rledger.append('R|%s|INTEGRITY_VIOLATION|%s|claim cited injection-flagged page(s) %s; refused install|%s'
                       % (cid, claim, ','.join(bad),
                          ';'.join(urlmap[p] for p in provs if p in urlmap)))
        gate_counts['INTEGRITY_VIOLATION'] = gate_counts.get('INTEGRITY_VIOLATION', 0) + 1
        log.append('%s|INTEGRITY_VIOLATION|cited %s' % (cid, ','.join(bad)))
        v['class'] = 'WITHHOLD'
        v['gate'] = 'INTEGRITY_VIOLATION'
        return v
    minprovs = 1 if v.get('via') == 'KB' else 2
    if len(provs) >= minprovs:
        kid_box[0] += 1
        kid_s = 'KB-%04d' % kid_box[0]
        if v.get('via') == 'KB':
            kledger.append('K|%s|%s|%s|KB|%s' % (kid_s, cid, claim, v.get('seq')))
        else:
            kledger.append('K|%s|%s|%s' % (kid_s, cid, claim))
            log.append('%s|FROZEN_INSTALL_IN_K|%s' % (cid, kid_s))
        for p in provs:
            kledger.append('P|%s|%s|%s' % (kid_s, p, urlmap.get(p, '?')))
        log.append('%s|INSTALL|%s|%s|%s|%s|provs=%s'
                   % (cid, kid_s, v.get('via'), v.get('seq'),
                      claim[:80], ','.join(provs)))
    else:
        rledger.append('R|%s|NO_CORROBORATION|%s|install-class but %d provs (< %d)|%s'
                       % (cid, claim, len(provs), minprovs, urls))
        gate_counts['NO_CORROBORATION'] = gate_counts.get('NO_CORROBORATION', 0) + 1
        log.append('%s|WITHHOLD|NO_CORROBORATION|install-class-too-few-provs' % cid)
        v['class'] = 'WITHHOLD'
        v['gate'] = 'NO_CORROBORATION'
    return v


def cluster_claim_text(battery, cid):
    """The authored claim sentence: first non-empty, non-TITLE line of p1.
    Returns None when the cluster/page is absent."""
    p = os.path.join(battery, cid, 'p1.txt')
    if not os.path.exists(p):
        return None
    with open(p, encoding='utf-8', errors='replace') as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith('TITLE:'):
                continue
            return s
    return None


def resolve_pseqs(state_dir, battery, cids, pseq_by_cid=None):
    """Map cluster ids -> pending pseqs by claim-text match on
    PB|<pseq>|<claim>|<pidcsv> lines. The instrument lowercases the stored
    claim, so the match is case-insensitive; when pseq_by_cid (the Phase-1
    run-log record) is given, the resolved pseq must agree with it.
    Returns (dict, error)."""
    pend = read_pending(state_dir)
    out, err = {}, None
    for c in cids:
        claim = cluster_claim_text(battery, c)
        if claim is None:
            err = 'no claim text for %s' % c
            break
        want = claim.lower()
        hits = [p for p, cl, _ in pend if cl.lower() == want]
        if len(hits) != 1:
            err = 'claim match for %s -> %d pending entries' % (c, len(hits))
            break
        if pseq_by_cid is not None and pseq_by_cid.get(c) != hits[0]:
            err = ('pseq mismatch for %s: pending.txt=%d phase1-log=%s'
                   % (c, hits[0], pseq_by_cid.get(c)))
            break
        out[c] = hits[0]
    return out, err


def run_lifecycle(webg, state_dir, adir, battery, log, kledger, rledger,
                  pledger, gate_counts, kid_box):
    """Phase 2 fixed lifecycle script (K arm, 1x). Logs to lifecycle.log.
    Any expectation miss -> VOID."""
    ll = []
    ok = [True]
    pseq_by_cid = {}
    for l in log:
        m = re.match(r'^([A-Za-z0-9][A-Za-z0-9-]*)\|PENDING\|(\d+)\|', l)
        if m:
            pseq_by_cid[m.group(1)] = int(m.group(2))

    def void(reason):
        ll.append('LIFECYCLE|VOID|%s' % reason)
        log.append('LIFECYCLE|VOID|%s' % reason)
        ok[0] = False

    def kb_lines(tag, out):
        for l in out.split('\n'):
            if l.startswith('KB|'):
                ll.append('LIFECYCLE|KB|%s|%s' % (tag, l))

    def pending_claims():
        return {cl for _, cl, _ in read_pending(state_dir)}

    # --- Step 1: kbtest true on pn-01..pn-04 pendings ---
    ll.append('LIFECYCLE|STEP|1|kbtest-true|pn-01..pn-04')
    t1 = ['pn-0%d' % i for i in (1, 2, 3, 4)]
    pseq1, err = resolve_pseqs(state_dir, battery, t1, pseq_by_cid)
    if err:
        void('step1 resolve: %s' % err)
    else:
        n_prom = 0
        for c in t1:
            rc, out, _err = run_bin([webg, 'kbtest', state_dir,
                                     str(pseq1[c]), 'true'], KPROD)
            ll.append('LIFECYCLE|KBTEST|step1|%s|pseq=%d|rc=%d'
                      % (c, pseq1[c], rc))
            kb_lines('step1', out)
            m = re.search(r'^KB\|PROMOTED\|%d\|(\d+)$' % pseq1[c],
                          out, re.M)
            if rc != 0 or not m:
                void('step1 kbtest true %s pseq=%d rc=%d' % (c, pseq1[c], rc))
                break
            n_prom += 1
        if ok[0] and n_prom != 4:
            void('step1 expected 4 PROMOTED, got %d' % n_prom)
        if ok[0]:
            gone = all(p not in [p for p, _, _ in read_pending(state_dir)]
                       for p in pseq1.values())
            if not gone:
                void('step1 promoted pseqs still in pending.txt')

    # --- Step 2: verdict pn-01b..pn-04b -> INSTALL, agree-seq > 12 ---
    if ok[0]:
        ll.append('LIFECYCLE|STEP|2|verdict|pn-01b..pn-04b')
        by_cid = {c: (need, pages) for c, need, pages in CLUSTERS}
        for c in ['pn-0%db' % i for i in (1, 2, 3, 4)]:
            if c not in by_cid:
                void('step2 cluster %s missing from battery' % c)
                break
            need, pages = by_cid[c]
            workdir = os.path.join(adir, 'work_phase2', c)
            os.makedirs(workdir, exist_ok=True)
            v = run_cluster(webg, state_dir, workdir, c, need, pages, log,
                            kledger, rledger, pledger, gate_counts, kid_box)
            seq = v.get('seq')
            ll.append('LIFECYCLE|VERDICT|%s|%s|seq=%s'
                      % (c, v.get('class'), seq))
            if not v.get('ok') or v.get('class') != 'INSTALL' or \
               not isinstance(seq, int) or seq <= 12:
                void('step2 %s expected INSTALL seq>12, got %s seq=%s'
                     % (c, v.get('class'), seq))
                break

    # --- Step 3: kbtest false on pf-01..pf-08 pendings ---
    if ok[0]:
        ll.append('LIFECYCLE|STEP|3|kbtest-false|pf-01..pf-08')
        t3 = ['pf-0%d' % i for i in range(1, 9)]
        pseq3, err = resolve_pseqs(state_dir, battery, t3, pseq_by_cid)
        if err:
            void('step3 resolve: %s' % err)
        else:
            n_res = 0
            for c in t3:
                rc, out, _err = run_bin([webg, 'kbtest', state_dir,
                                         str(pseq3[c]), 'false'], KPROD)
                ll.append('LIFECYCLE|KBTEST|step3|%s|pseq=%d|rc=%d'
                          % (c, pseq3[c], rc))
                kb_lines('step3', out)
                m = re.search(r'^KB\|RESOLVED_FALSE\|%d$' % pseq3[c],
                              out, re.M)
                if rc != 0 or not m:
                    void('step3 kbtest false %s pseq=%d rc=%d'
                         % (c, pseq3[c], rc))
                    break
                n_res += 1
            if ok[0] and n_res != 8:
                void('step3 expected 8 RESOLVED_FALSE, got %d' % n_res)

    # --- Step 4: re-verdict pf-01..pf-08 -> WITHHOLD GATE|KB_RESOLVED_FALSE ---
    if ok[0]:
        ll.append('LIFECYCLE|STEP|4|re-verdict|pf-01..pf-08')
        by_cid = {c: (need, pages) for c, need, pages in CLUSTERS}
        for c in ['pf-0%d' % i for i in range(1, 9)]:
            if c not in by_cid:
                void('step4 cluster %s missing from battery' % c)
                break
            need, pages = by_cid[c]
            workdir = os.path.join(adir, 'work_phase2', c + '_re')
            os.makedirs(workdir, exist_ok=True)
            v = run_cluster(webg, state_dir, workdir, c, need, pages, log,
                            kledger, rledger, pledger, gate_counts, kid_box)
            ll.append('LIFECYCLE|VERDICT|%s|%s|gate=%s'
                      % (c, v.get('class'), v.get('gate')))
            if not v.get('ok') or v.get('class') != 'WITHHOLD' or \
               v.get('gate') != 'KB_RESOLVED_FALSE':
                void('step4 %s expected WITHHOLD/KB_RESOLVED_FALSE, got %s/%s'
                     % (c, v.get('class'), v.get('gate')))
                break

    # --- Step 5: kbcommit contra.txt -> 4x KB|AUTO_FALSE, 4 pendings gone ---
    if ok[0]:
        ll.append('LIFECYCLE|STEP|5|kbcommit|contra.txt')
        before = pending_claims()
        targets = {'pc-0%d' % i: cluster_claim_text(battery, 'pc-0%d' % i).lower()
                   for i in (1, 2, 3, 4)}
        contra = os.path.join(battery, 'contra.txt')
        rc, out, _err = run_bin([webg, 'kbcommit', contra, state_dir], KPROD)
        ll.append('LIFECYCLE|KBCOMMIT|step5|rc=%d' % rc)
        kb_lines('step5', out)
        n_af = len(re.findall(r'^KB\|AUTO_FALSE\|\d+$', out, re.M))
        n_co = len(re.findall(r'^KB\|COMMIT\|\d+$', out, re.M))
        ll.append('LIFECYCLE|STEP|5|auto_false=%d|commits=%d' % (n_af, n_co))
        after = pending_claims()
        removed = before - after
        if rc != 0 or n_af != 4 or n_co != 4:
            void('step5 expected rc=0 4 AUTO_FALSE 4 COMMIT, got rc=%d af=%d co=%d'
                 % (rc, n_af, n_co))
        elif removed != set(targets.values()):
            void('step5 removed-set mismatch: %d removed, expected pc-01..04'
                 % len(removed))

    # --- Step 6: kbcommit agree.txt -> 4x KB|AUTO_PROMOTED ---
    if ok[0]:
        ll.append('LIFECYCLE|STEP|6|kbcommit|agree.txt')
        before = pending_claims()
        targets = {'pc-0%d' % i: cluster_claim_text(battery, 'pc-0%d' % i).lower()
                   for i in (5, 6, 7, 8)}
        agree = os.path.join(battery, 'agree.txt')
        rc, out, _err = run_bin([webg, 'kbcommit', agree, state_dir], KPROD)
        ll.append('LIFECYCLE|KBCOMMIT|step6|rc=%d' % rc)
        kb_lines('step6', out)
        n_ap = len(re.findall(r'^KB\|AUTO_PROMOTED\|\d+\|\d+$', out, re.M))
        n_co = len(re.findall(r'^KB\|COMMIT\|\d+$', out, re.M))
        ll.append('LIFECYCLE|STEP|6|auto_promoted=%d|commits=%d' % (n_ap, n_co))
        after = pending_claims()
        removed = before - after
        if rc != 0 or n_ap != 4 or n_co != 4:
            void('step6 expected rc=0 4 AUTO_PROMOTED 4 COMMIT, got rc=%d ap=%d co=%d'
                 % (rc, n_ap, n_co))
        elif removed != set(targets.values()):
            void('step6 removed-set mismatch: %d removed, expected pc-05..08'
                 % len(removed))
        elif ok[0]:
            # pn-05..08 must still be pending
            keep = {cluster_claim_text(battery, 'pn-0%d' % i).lower() for i in (5, 6, 7, 8)}
            if not keep.issubset(after):
                void('step6 pn-05..08 not all still pending')

    # --- Step 7: verdict pc-05b..pc-08b -> INSTALL, agree-seq > 12 ---
    if ok[0]:
        ll.append('LIFECYCLE|STEP|7|verdict|pc-05b..pc-08b')
        by_cid = {c: (need, pages) for c, need, pages in CLUSTERS}
        for c in ['pc-0%db' % i for i in (5, 6, 7, 8)]:
            if c not in by_cid:
                void('step7 cluster %s missing from battery' % c)
                break
            need, pages = by_cid[c]
            workdir = os.path.join(adir, 'work_phase2', c)
            os.makedirs(workdir, exist_ok=True)
            v = run_cluster(webg, state_dir, workdir, c, need, pages, log,
                            kledger, rledger, pledger, gate_counts, kid_box)
            seq = v.get('seq')
            ll.append('LIFECYCLE|VERDICT|%s|%s|seq=%s'
                      % (c, v.get('class'), seq))
            if not v.get('ok') or v.get('class') != 'INSTALL' or \
               not isinstance(seq, int) or seq <= 12:
                void('step7 %s expected INSTALL seq>12, got %s seq=%s'
                     % (c, v.get('class'), seq))
                break

    if ok[0]:
        ll.append('LIFECYCLE|DONE|OK')
        log.append('LIFECYCLE|DONE|OK')
    with open(os.path.join(adir, 'lifecycle.log'), 'w') as f:
        f.write('\n'.join(ll) + '\n')
    return ok[0]


def run_arm(arm, clusters_p1, outdir, passn, kbfile, guides, no_lifecycle,
            is_10x):
    adir = os.path.join(outdir, 'arm_%s_pass%d' % (arm, passn))
    os.makedirs(os.path.join(adir, 'work'), exist_ok=True)
    state_dir = os.path.join(adir, 'state')
    os.makedirs(state_dir, exist_ok=True)
    log, kledger, rledger, pledger, gate_counts = [], [], [], [], {}
    kid_box = [0]
    if not teach(WEBG, guides, state_dir, log):
        log.append('ARM|%s|VOID|teach' % arm)
        write_all(adir, log, kledger, rledger, pledger)
        return False, None
    if arm == 'K':
        if not kbcommit(WEBG, kbfile, state_dir, log):
            log.append('ARM|%s|VOID|kbcommit' % arm)
            write_all(adir, log, kledger, rledger, pledger)
            return False, None
    cmp_lines = [] if (arm == 'N' and BF1BIN) else None
    for cid, need, pages in clusters_p1:
        workdir = os.path.join(adir, 'work', cid)
        os.makedirs(workdir, exist_ok=True)
        run_cluster(WEBG, state_dir, workdir, cid, need, pages, log,
                    kledger, rledger, pledger, gate_counts, kid_box,
                    cmp_lines=cmp_lines)
    if arm == 'K' and not is_10x:
        if no_lifecycle:
            with open(os.path.join(adir, 'lifecycle.log'), 'w') as f:
                f.write('LIFECYCLE|SKIPPED|no-lifecycle\n')
            log.append('LIFECYCLE|SKIPPED|no-lifecycle')
        else:
            try:
                lc_ok = run_lifecycle(WEBG, state_dir, adir, BATTERY, log,
                                      kledger, rledger, pledger, gate_counts,
                                      kid_box)
            except Exception as e:  # fail-closed: an unforeseen lifecycle
                lc_ok = False       # exception is VOID, not a traceback
                log.append('LIFECYCLE|VOID|lifecycle-exc|%r' % (e,))
            if not lc_ok:
                log.append('ARM|%s|VOID|lifecycle' % arm)
                write_all(adir, log, kledger, rledger, pledger)
                return False, None
    log.append('ARM|%s|DONE|installs=%d withholds=%d pendings=%d gates=%s'
               % (arm, len([l for l in kledger if l.startswith('K|')]),
                  len(rledger),
                  len([l for l in pledger if l.startswith('D|')]),
                  gate_counts))
    write_all(adir, log, kledger, rledger, pledger)
    return True, cmp_lines


def write_all(adir, log, kledger, rledger, pledger):
    with open(os.path.join(adir, 'run_kprod.log'), 'w') as f:
        f.write('\n'.join(log) + '\n')
    with open(os.path.join(adir, 'knowledge_ledger.txt'), 'w') as f:
        f.write('\n'.join(kledger) + '\n')
    with open(os.path.join(adir, 'refusal_ledger.txt'), 'w') as f:
        f.write('\n'.join(rledger) + '\n')
    with open(os.path.join(adir, 'pending_ledger.txt'), 'w') as f:
        f.write('\n'.join(pledger) + '\n')


def run_bf1_replay(bf1bin, guides, clusters_p1, outdir, passn):
    """Frozen BF1 replay of the N-arm Phase-1 verdicts (KP7 evidence)."""
    bdir = os.path.join(outdir, 'bf1_pass%d' % passn)
    os.makedirs(os.path.join(bdir, 'work'), exist_ok=True)
    state_dir = os.path.join(bdir, 'state')
    os.makedirs(state_dir, exist_ok=True)
    log = []
    if not teach(bf1bin, guides, state_dir, log):
        with open(os.path.join(bdir, 'bf1.log'), 'w') as f:
            f.write('BF1|VOID|teach\n')
        return False
    cmp_lines = []
    kledger, rledger, pledger, gate_counts, kid_box = [], [], [], {}, [0]
    for cid, need, pages in clusters_p1:
        workdir = os.path.join(bdir, 'work', cid)
        os.makedirs(workdir, exist_ok=True)
        v = run_cluster(bf1bin, state_dir, workdir, cid, need, pages, log,
                        kledger, rledger, pledger, gate_counts, kid_box,
                        cmp_lines=cmp_lines)
        if not v.get('ok'):
            with open(os.path.join(bdir, 'bf1.log'), 'w') as f:
                f.write('BF1|VOID|cluster %s: %s\n' % (cid, v.get('reason')))
            return False
    with open(os.path.join(bdir, 'bf1.log'), 'w') as f:
        f.write('\n'.join(cmp_lines) + '\n')
    return True


def sha_of(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()


COMPARE_FILES_K = ['run_kprod.log', 'knowledge_ledger.txt',
                   'refusal_ledger.txt', 'pending_ledger.txt',
                   'lifecycle.log', 'state/knowledge.txt',
                   'state/pending.txt', 'state/resolved.txt']
COMPARE_FILES_N = ['run_kprod.log', 'knowledge_ledger.txt',
                   'refusal_ledger.txt', 'pending_ledger.txt',
                   'state/knowledge.txt', 'state/pending.txt',
                   'state/resolved.txt']


def main():
    global BATTERY, BF1BIN, CLUSTERS
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('outdir')
    ap.add_argument('--battery', default=BATTERY_DEFAULT)
    ap.add_argument('--kb', default=KB_DEFAULT)
    ap.add_argument('--guides', default=GUIDES_DEFAULT)
    ap.add_argument('--no-lifecycle', action='store_true')
    ap.add_argument('--bf1', default=None)
    ap.add_argument('--force-10x', action='store_true')
    a = ap.parse_args()

    BATTERY = os.path.abspath(a.battery)
    BF1BIN = os.path.abspath(a.bf1) if a.bf1 else None
    kbfile = os.path.abspath(a.kb)
    guides = os.path.abspath(a.guides)
    outdir = os.path.abspath(a.outdir)
    os.makedirs(outdir, exist_ok=True)

    is_10x = a.force_10x or os.path.basename(kbfile) == 'claims120.txt'
    with open(os.path.join(outdir, 'mode.txt'), 'w') as f:
        f.write('10x\n' if is_10x else '1x\n')
    with open(os.path.join(outdir, 'battery.txt'), 'w') as f:
        f.write(BATTERY + '\n')
    with open(os.path.join(outdir, 'kb.txt'), 'w') as f:
        f.write(kbfile + '\n')

    CLUSTERS = load_clusters(BATTERY)
    clusters_p1 = [c for c in CLUSTERS if not FOLLOWUP_RE.match(c[0])]
    n_skip = len(CLUSTERS) - len(clusters_p1)
    print('clusters: %d (phase1: %d, phase2-only: %d) mode=%s' %
          (len(CLUSTERS), len(clusters_p1), n_skip, '10x' if is_10x else '1x'),
          flush=True)

    ok = True
    for arm in ('K', 'N'):
        for passn in (1, 2):
            print('arm %s pass %d...' % (arm, passn), flush=True)
            good, cmp_lines = run_arm(arm, clusters_p1, outdir, passn,
                                      kbfile, guides, a.no_lifecycle, is_10x)
            if not good:
                print('VOID: arm %s pass %d' % (arm, passn), flush=True)
                ok = False
            if arm == 'N' and BF1BIN:
                adir = os.path.join(outdir, 'arm_N_pass%d' % passn)
                with open(os.path.join(adir, 'verdict_cmp.log'), 'w') as f:
                    f.write('\n'.join(cmp_lines or []) + '\n')
                print('bf1 replay pass %d...' % passn, flush=True)
                if not run_bf1_replay(BF1BIN, guides, clusters_p1, outdir, passn):
                    print('VOID: bf1 replay pass %d' % passn, flush=True)
                    ok = False
    # Phase 3: byte-identity within arm across passes
    det_ok = True
    for arm, files in (('K', COMPARE_FILES_K), ('N', COMPARE_FILES_N)):
        for fn in files:
            a1 = os.path.join(outdir, 'arm_%s_pass1' % arm, fn)
            b1 = os.path.join(outdir, 'arm_%s_pass2' % arm, fn)
            if not os.path.exists(a1) and not os.path.exists(b1):
                same = True
            elif not os.path.exists(a1) or not os.path.exists(b1):
                same = False
            else:
                same = filecmp.cmp(a1, b1, shallow=False)
            print('DETERMINISM|%s|%s|%s' % (arm, fn,
                                           'IDENTICAL' if same else 'DIFFER'),
                  flush=True)
            if not same:
                det_ok = False
    print('SHAS:', flush=True)
    for arm in ('K', 'N'):
        for passn in (1, 2):
            for fn in ('run_kprod.log', 'knowledge_ledger.txt',
                       'refusal_ledger.txt', 'pending_ledger.txt'):
                p = os.path.join(outdir, 'arm_%s_pass%d' % (arm, passn), fn)
                print('SHA|%s|%s' % (os.path.basename(os.path.dirname(p))
                                     + '/' + fn, sha_of(p)), flush=True)
    if not ok:
        sys.exit(3)
    if not det_ok:
        sys.exit(4)
    print('DONE', flush=True)


if __name__ == '__main__':
    main()
