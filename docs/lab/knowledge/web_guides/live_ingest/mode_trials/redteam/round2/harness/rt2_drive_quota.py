#!/usr/bin/env python3
"""LI Wave-2 red-team follow-up: V-QUOTA full-R1 driver (incl. P1-P4).

Blind re-execution of the frozen V-QUOTA protocol on the full 18-case R1
battery. Strict pass -> candidate collection (E1+E2, E3 inside the binary)
-> <=5 quota slots in frozen priority order -> mechanical H5-K1/H6 scoring.

Pure Zag for all harness reasoning; Python only formats/orchestrates/scores
frozen rules. Zero randomness. Deterministic: two passes must be byte-identical.

Usage: rt2_drive_quota.py <bindir> <guides> <battery> <outdir> <stoplist>
"""
import os, re, sys, shutil, hashlib, subprocess

MANIFEST = ['A1_smuggle', 'A2_sockpuppet', 'A3_stuffed', 'A4_single',
            'A5_injpair', 'A6_fragment', 'A7_caughtinj', 'A8_evadetop',
            'A9_xhost', 'P1_paratower', 'P2_paraboil', 'P3_parabones',
            'P4_parabird', 'rt01', 'rt02', 'rt10', 'rt11', 'rt12']

def run_bin(args, cwd, audit):
    r = subprocess.run(args, capture_output=True, text=True, cwd=cwd)
    audit.write('CMD|%s\n' % ' '.join(args))
    audit.write(r.stderr)
    return r.returncode, r.stdout, r.stderr

def teach(webg, guides, state_dir, audit, log):
    os.makedirs(state_dir, exist_ok=True)
    rc, out, err = run_bin([webg, 'teach', guides, state_dir], os.path.dirname(webg), audit)
    log.append('TEACH|rc=%d' % rc)
    installed = [l for l in out.split('\n') if '|INSTALLED|' in l]
    g7rej = any('G7|REJECTED' in l for l in out.split('\n') if '|REJECTED|' in l)
    ids = []
    for l in installed:
        p = l.split('|')
        ids.append(p[1] if len(p) >= 3 and p[1].startswith('G') else p[-2])
    ok = (rc in (0, 3)) and g7rej and sorted(ids) == ['G1', 'G2', 'G3', 'G4', 'G5', 'G6']
    log.append('TEACH|%s' % ('VALID' if ok else 'VOID ids=%s g7rej=%s' % (ids, g7rej)))
    assert ok, 'teach failed'
    return state_dir

def do_query(webg, sd, needf, audit):
    rc, out, err = run_bin([webg, 'query', sd, needf], os.path.dirname(webg), audit)
    qs = [l.split('|', 1)[1] for l in out.split('\n') if l.startswith('QUERY|')]
    assert rc == 0 and qs, 'query failed: ' + err[-200:]
    return qs[0], out

def do_select(webg, sd, pages, query, audit, tmpdir):
    rf = os.path.join(tmpdir, 'results.txt')
    with open(rf, 'w') as f:
        f.write('Q|' + query + '\n')
        for pid, title, sents in pages:
            f.write('R|%s|%s|%s\n' % (pid, title, sents[0][:160] if sents else ''))
    rc, out, err = run_bin([webg, 'select', sd, rf], os.path.dirname(webg), audit)
    assert rc == 0, 'select failed: ' + err[-200:]
    opens = []
    for l in out.split('\n'):
        if l.startswith('OPEN|'):
            opens = l.split('|', 1)[1].split()
    return opens, out

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
    d['para_gate'] = [l.split('|', 2)[2] for l in out.split('\n') if l.startswith('GATE|PARA|')]
    d['quota_flags'] = [l for l in out.split('\n') if l.startswith('QUOTA|')]
    d['installed'] = (not d['uncheckable']) and len(d['claims']) > 0
    return d

def main():
    bindir, guides, bdir, outdir, stoplist = (os.path.abspath(x) for x in sys.argv[1:6])
    manifest_file = os.path.abspath(sys.argv[6]) if len(sys.argv) > 6 else None
    manifest = [l.strip() for l in open(manifest_file) if l.strip() and not l.startswith('#')] \
        if manifest_file else MANIFEST
    webg = os.path.join(bindir, 'webg_quota')
    os.makedirs(outdir, exist_ok=True)
    tmpdir = os.path.join(outdir, 'tmp')
    os.makedirs(tmpdir, exist_ok=True)
    audit = open(os.path.join(outdir, 'audit.log'), 'w')
    log = ['LI-QUOTA-RT2|battery=R1-full-P1P4']
    sd = teach(webg, guides, os.path.join(outdir, 'state'), audit, log)
    # frozen stoplist must be present in state dir (quota reads it via stoppath arg)
    kledger, rledger, qledger, cand_recs = [], [], [], []
    midx = 0
    for case in manifest:
        midx += 1
        cdir = os.path.join(bdir, case)
        assert os.path.isdir(cdir), 'missing case ' + case
        wdir = os.path.join(outdir, 'work', case)
        os.makedirs(wdir, exist_ok=True)
        need = open(os.path.join(cdir, 'need.txt')).read().strip()
        kind = open(os.path.join(cdir, 'kind.txt')).read().strip() \
            if os.path.exists(os.path.join(cdir, 'kind.txt')) else 'FACT'
        pages = {}
        for fn in sorted(os.listdir(os.path.join(cdir, 'pages'))):
            if not fn.endswith('.txt'):
                continue
            pid = fn[:-4]
            lines = [l.rstrip('\n') for l in open(os.path.join(cdir, 'pages', fn))]
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
        needf = os.path.join(wdir, 'need.txt')
        with open(needf, 'w') as f:
            f.write(need + '\n')
        query, qout = do_query(webg, sd, needf, audit)
        with open(os.path.join(wdir, 'query.out'), 'w') as f:
            f.write(qout)
        plist = [(pid, t, s) for pid, (t, s) in pages.items() if s]
        opens, sout = do_select(webg, sd, plist, query, audit, tmpdir)
        with open(os.path.join(wdir, 'select.out'), 'w') as f:
            f.write(sout)
        pf = os.path.join(wdir, 'pages.txt')
        with open(pf, 'w') as f:
            for pid in opens:
                title, sents = pages[pid]
                f.write('P|%s|%s\n' % (pid, title))
                f.write('H|%s\n' % hosts.get(pid, ''))
                for s in sents:
                    f.write('S|%s\n' % s)
        fed = [pid for pid in opens if pages.get(pid, ('', []))[1]]
        rc, out, err = run_bin([webg, 'verdict', sd, needf, pf, kind, query],
                               bindir, audit)
        with open(os.path.join(wdir, 'verdict.out'), 'w') as f:
            f.write(out)
        v = parse_verdict(out)
        ans = v['answer'][0][:60] if v['answer'] else 'UNCHECKABLE'
        loginstall = '%s|STRICT|installed=%s|inj=%s|answer=%s|fed=%d' % (
            case, v['installed'], ','.join(v['inj']), ans, len(fed))
        log.append(loginstall)
        print(loginstall)
        if v['installed'] and len(v['provs']) >= 2:
            kledger.append((case, v['answer'][0], list(v['provs'])))
        else:
            rledger.append((case, ','.join(v['inj'])))
            if len(fed) >= 2 and not v['inj']:
                cand_recs.append({'cid': case, 'fed_pages': len(fed),
                                  'manifest_idx': midx, 'need_file': needf,
                                  'pages_file': pf, 'query': query})
    # ---- spend <=5 slots in frozen priority order ----
    cands = sorted(cand_recs, key=lambda c: (-c['fed_pages'], c['manifest_idx']))
    qaudit = []
    log.append('CANDIDATES|%s' % ' '.join(
        '%s(fed=%d,rank=%d)' % (c['cid'], c['fed_pages'], r)
        for r, c in enumerate(cands, 1)))
    print('CANDIDATES:', [(c['cid'], c['fed_pages']) for c in cands])
    spent = 0
    for rank, c in enumerate(cands, 1):
        if spent >= 5:
            break
        spent += 1
        cid = c['cid']
        qwdir = os.path.join(outdir, 'work', cid)
        rc, out, err = run_bin(
            [webg, 'quota', sd, c['need_file'], c['pages_file'], c['query'], stoplist],
            bindir, audit)
        with open(os.path.join(qwdir, 'quota.out'), 'w') as f:
            f.write(out)
        v = parse_verdict(out)
        win = False
        reason = 'no-passing-pair'
        pids = '-'
        if v['quota_flags']:
            qf = v['quota_flags'][0]
            for tag in ('NO-CANDIDATE', 'INJECTED', 'STRICT-WOULD-INSTALL', 'STOPLIST-FAIL'):
                if tag in qf:
                    reason = tag
        if v['para_gate'] and len(v['provs']) >= 2 and not v['inj'] and v['answer']:
            win = True
            reason = v['answer'][0].replace('|', '/')
            pids = ','.join(v['provs'])
            qledger.append((cid, v['answer'][0], list(v['provs'])))
            log.append('%s|QUOTA|WIN|slot=%d|%s' % (cid, spent, v['answer'][0][:80]))
        else:
            log.append('%s|QUOTA|LOSE|slot=%d|%s' % (cid, spent, reason))
        qaudit.append('SLOT|%d|%s|%d|%d|%s|%s|GATE|PARA|%s' % (
            spent, cid, rank, c['fed_pages'], 'WIN' if win else 'LOSE', reason, pids))
        print('%s|slot=%d|%s|%s' % (cid, spent, 'WIN' if win else 'LOSE', reason[:60]))
    for n in range(spent + 1, 6):
        qaudit.append('SLOT|%d|UNSPENT|no-more-eligible-candidates' % n)
    # ---- H5-K1 / H6 scoring ----
    k1_kills, h6_notes = [], []
    for cid, claim, provs in qledger:
        prof = os.path.join(bdir, cid, 'PROHIBITED.txt')
        prohibited = open(prof).read().strip().lower() if os.path.exists(prof) else ''
        if prohibited and prohibited in claim.lower():
            k1_kills.append((cid, claim[:80]))
    audit.close()
    with open(os.path.join(outdir, 'quota_audit.txt'), 'w') as f:
        f.write('\n'.join(qaudit) + '\n')
    with open(os.path.join(outdir, 'RUNLOG.txt'), 'w') as f:
        f.write('\n'.join(log) + '\n')
    with open(os.path.join(outdir, 'KLEDGER.txt'), 'w') as f:
        for cid, claim, provs in kledger:
            f.write('K|%s|%s|%s\n' % (cid, claim[:120], ','.join(provs)))
    with open(os.path.join(outdir, 'QLEDGER.txt'), 'w') as f:
        for cid, claim, provs in qledger:
            f.write('Q|%s|%s|%s\n' % (cid, claim[:120], ','.join(provs)))
    with open(os.path.join(outdir, 'SCORES.txt'), 'w') as f:
        f.write('strict_installed=%d\n' % len(kledger))
        f.write('withheld=%d\n' % len(rledger))
        f.write('candidates=%d\n' % len(cands))
        f.write('slots_spent=%d\n' % spent)
        f.write('quota_installed=%d\n' % len(qledger))
        f.write('H5K1_KILLS=%d\n' % len(k1_kills))
        for cid, claim in k1_kills:
            f.write('H5K1|%s|%s\n' % (cid, claim))
    print('SUMMARY|strict=%d withheld=%d cands=%d spent=%d quota_inst=%d H5K1=%d'
          % (len(kledger), len(rledger), len(cands), spent, len(qledger), len(k1_kills)))

if __name__ == '__main__':
    main()
