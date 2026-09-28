#!/usr/bin/env python3
"""TRACK B driver: Micah's knowledge hypothesis.

Two arms x two passes over the 40-cluster KB battery.
Arm K: teach (frozen contract) + deliberate kbcommit (12 claims), prior active.
Arm N: teach only, no knowledge.txt -> prior skipped (frozen BF1 behavior).

Per arm/pass: teach -> [kbcommit] -> per-cluster query/select/verdict ->
knowledge/refusal ledgers + run log. Then byte-compare pass1 vs pass2.

Pure orchestration; all reasoning is the Zag instrument. Zero RNG.

Usage: run_kb.py <outdir>
"""
import os, re, sys, hashlib, subprocess, filecmp
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
BAT = os.path.join(HERE, 'battery')
WEBG = os.path.join(HERE, 'bin', 'instrument_kb')
GUIDES = os.path.join(HERE, 'guides')
KBFILE = os.path.join(HERE, 'knowledge_base.txt')
KB_EXPECT = 12

ARMS = {
    'K': dict(webg=WEBG, guides=GUIDES, knowledge=True,
              teach_exact=sorted(['G1', 'G2', 'G3', 'G4', 'G5', 'G6'])),
    'N': dict(webg=WEBG, guides=GUIDES, knowledge=False,
              teach_exact=sorted(['G1', 'G2', 'G3', 'G4', 'G5', 'G6'])),
}


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


def load_clusters():
    cls = []
    for cid in sorted(os.listdir(BAT)):
        d = os.path.join(BAT, cid)
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


def kbcommit(webg, state_dir, log):
    rc, out, err = run_bin([webg, 'kbcommit', KBFILE, state_dir], HERE)
    commits = [l for l in out.split('\n') if l.startswith('KB|COMMIT|')]
    log.append('KBCOMMIT|rc=%d|commits=%d' % (rc, len(commits)))
    for l in commits:
        log.append('KBCOMMIT|' + l)
    if rc != 0 or len(commits) != KB_EXPECT:
        log.append('KBCOMMIT|VOID|rc=%d commits=%d expected=%d' % (rc, len(commits), KB_EXPECT))
        return False
    log.append('KBCOMMIT|VALID|%d claims deliberately committed' % len(commits))
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
            f.write('R|%s|%s|%s\n' % (pid, title, sents[0][:160] if sents else ''))
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

    lines = out.split('\n')
    inj = [l.split('|', 2)[2] for l in lines if l.startswith('FLAG|INJECTION|')]
    for p in inj:
        log.append('%s|FLAG|INJECTION|%s' % (cid, p))
    kb_corrob = [l for l in lines if l.startswith('KB|CORROBORATED|')]
    kb_contra = [l for l in lines if l.startswith('GATE|KB_CONTRADICTION|')]
    kb_agree = [l for l in lines if l.startswith('KB|AGREE|')]
    for l in kb_agree:
        log.append('%s|%s' % (cid, l))
    uncheckable = any(l.startswith('ANSWER|UNCHECKABLE') for l in lines)
    answer = [l.split('|', 1)[1] for l in lines
              if l.startswith('ANSWER|') and l != 'ANSWER|UNCHECKABLE']
    provs = []
    for l in lines:
        if l.startswith('PROV|1|'):
            p = l.split('|', 2)[2]
            if p not in provs:
                provs.append(p)
    urlmap = {pid: url for pid, _, url, _ in pages}

    # --- KB prior dispositions (frozen prereg §11.3 driver rules) ---
    if kb_contra:
        seq = kb_contra[0].split('|')[2] if '|' in kb_contra[0] else '?'
        rledger.append('R|%s|KB_CONTRADICTION|-|candidate contradicts committed claim KB|%s|%s'
                       % (cid, seq, ';'.join(urlmap[p] for p in opens if p in urlmap)))
        gate_counts['KB_CONTRADICTION'] = gate_counts.get('KB_CONTRADICTION', 0) + 1
        log.append('%s|WITHHOLD|KB_CONTRADICTION|seq=%s' % (cid, seq))
        return
    if kb_corrob:
        seq = kb_corrob[0].split('|')[2] if '|' in kb_corrob[0] else '?'
        claim = answer[0] if answer else '-'
        bad = [p for p in provs if p in inj]
        if bad:
            rledger.append('R|%s|INTEGRITY_VIOLATION|%s|claim cited injection-flagged page(s) %s; refused install|%s'
                           % (cid, claim, ','.join(bad), ';'.join(urlmap[p] for p in provs if p in urlmap)))
            gate_counts['INTEGRITY_VIOLATION'] = gate_counts.get('INTEGRITY_VIOLATION', 0) + 1
            log.append('%s|INTEGRITY_VIOLATION|cited %s' % (cid, ','.join(bad)))
            return
        # knowledge base is the corroborating source: >=1 prov suffices
        if provs:
            kid_box[0] += 1
            kid_s = 'KB-%04d' % kid_box[0]
            kledger.append('K|%s|%s|%s|KB|%s' % (kid_s, cid, claim, seq))
            for p in provs:
                kledger.append('P|%s|%s|%s' % (kid_s, p, urlmap.get(p, '?')))
            log.append('%s|INSTALL|%s|KB|%s|%s|provs=%s' % (cid, kid_s, seq, claim[:80], ','.join(provs)))
        else:
            rledger.append('R|%s|NO_CORROBORATION|%s|KB-corroborated but zero provs|%s'
                           % (cid, claim, ';'.join(urlmap[p] for p in opens if p in urlmap)))
            gate_counts['NO_CORROBORATION'] = gate_counts.get('NO_CORROBORATION', 0) + 1
            log.append('%s|WITHHOLD|NO_CORROBORATION|kb-zero-provs' % cid)
        return

    # --- frozen path ---
    if uncheckable or not answer:
        gatel = [l for l in lines if l.startswith('GATE|')]
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
        kid_s = 'KB-%04d' % kid_box[0]
        kledger.append('K|%s|%s|%s' % (kid_s, cid, claim))
        for p in provs:
            kledger.append('P|%s|%s|%s' % (kid_s, p, urlmap.get(p, '?')))
        log.append('%s|INSTALL|%s|%s|provs=%s' % (cid, kid_s, claim[:80], ','.join(provs)))
    else:
        rledger.append('R|%s|NO_CORROBORATION|%s|claim on 1 page only|%s'
                       % (cid, claim, ';'.join(urlmap[p] for p in provs if p in urlmap)))
        gate_counts['NO_CORROBORATION'] = gate_counts.get('NO_CORROBORATION', 0) + 1
        log.append('%s|WITHHOLD|NO_CORROBORATION|single-source' % cid)


def run_arm(arm, clusters, outdir, passn):
    cfg = ARMS[arm]
    adir = os.path.join(outdir, 'arm_%s_pass%d' % (arm, passn))
    os.makedirs(os.path.join(adir, 'work'), exist_ok=True)
    state_dir = os.path.join(adir, 'state')
    os.makedirs(state_dir, exist_ok=True)
    log, kledger, rledger, gate_counts = [], [], [], {}
    kid_box = [0]
    if not teach(cfg['webg'], cfg['guides'], state_dir, cfg['teach_exact'], log):
        log.append('ARM|%s|VOID|teach' % arm)
        write_all(adir, log, kledger, rledger, gate_counts)
        return False
    if cfg['knowledge']:
        if not kbcommit(cfg['webg'], state_dir, log):
            log.append('ARM|%s|VOID|kbcommit' % arm)
            write_all(adir, log, kledger, rledger, gate_counts)
            return False
    for cid, need, pages in clusters:
        workdir = os.path.join(adir, 'work', cid)
        os.makedirs(workdir, exist_ok=True)
        run_cluster(cfg['webg'], state_dir, workdir, cid, need, pages, log,
                    kledger, rledger, gate_counts, kid_box)
    log.append('ARM|%s|DONE|installs=%d withholds=%d gates=%s'
               % (arm, len([l for l in kledger if l.startswith('K|')]),
                  len(rledger), gate_counts))
    write_all(adir, log, kledger, rledger, gate_counts)
    return True


def write_all(adir, log, kledger, rledger, gate_counts):
    with open(os.path.join(adir, 'run_kb.log'), 'w') as f:
        f.write('\n'.join(log) + '\n')
    with open(os.path.join(adir, 'knowledge_ledger.txt'), 'w') as f:
        f.write('\n'.join(kledger) + '\n')
    with open(os.path.join(adir, 'refusal_ledger.txt'), 'w') as f:
        f.write('\n'.join(rledger) + '\n')


def sha_of(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()


def main():
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    clusters = load_clusters()
    print('clusters: %d' % len(clusters), flush=True)
    ok = True
    for arm in ('K', 'N'):
        for passn in (1, 2):
            print('arm %s pass %d...' % (arm, passn), flush=True)
            if not run_arm(arm, clusters, outdir, passn):
                print('VOID: arm %s pass %d' % (arm, passn), flush=True)
                ok = False
    # KB5: byte-identity within arm across passes
    det_ok = True
    for arm in ('K', 'N'):
        for fn in ('run_kb.log', 'knowledge_ledger.txt', 'refusal_ledger.txt'):
            a = os.path.join(outdir, 'arm_%s_pass1' % arm, fn)
            b = os.path.join(outdir, 'arm_%s_pass2' % arm, fn)
            same = filecmp.cmp(a, b, shallow=False)
            print('DETERMINISM|%s|%s|%s' % (arm, fn, 'IDENTICAL' if same else 'DIFFER'), flush=True)
            if not same:
                det_ok = False
    print('SHAS:', flush=True)
    for arm in ('K', 'N'):
        for passn in (1, 2):
            for fn in ('run_kb.log', 'knowledge_ledger.txt', 'refusal_ledger.txt'):
                p = os.path.join(outdir, 'arm_%s_pass%d' % (arm, passn), fn)
                print('SHA|%s|%s' % (os.path.basename(os.path.dirname(p)) + '/' + fn, sha_of(p)), flush=True)
    if not ok:
        sys.exit(3)
    if not det_ok:
        sys.exit(4)
    print('DONE', flush=True)


if __name__ == '__main__':
    main()
