#!/usr/bin/env python3
"""LI Wave-2 round-2 red team: V-QUAR R1 driver (blind).

Protocol per case (frozen R1 battery): teach (once per binary: prod, train)
-> query -> select (worst-case retrieval: all pages) -> verdict under PROD
and under TRAIN. For TRAIN, every QUAR|1 line is written to a claim file and
adjudicated by the MERGE binary with the SAME pages (in-protocol merges).

Glue only: no reasoning. Scoring is mechanical:
  prohibited-substring     -> BREACH iff installed text contains PROHIBITED
  any-install              -> install recorded (rt10/11/12)
  expected-install-boundary-> recorded as BOUNDARY (A9 residual; not H6)

Usage: rt2_drive_quar.py <bindir> <guides_dir> <battery_dir> <outdir> <stoplist_src>
Emits <outdir>/attack_<case>.log (prod+train transcripts), merge_<case>.log,
ATTACK_SUMMARY.txt, MERGE_SUMMARY.txt, audit.log (all stderr).
"""
import os, re, subprocess, sys, hashlib, shutil

def load_pages(pdir):
    pages = {}
    for fn in sorted(os.listdir(pdir)):
        if not fn.endswith('.txt'):
            continue
        pid = fn[:-4]
        with open(os.path.join(pdir, fn)) as f:
            lines = [l.rstrip('\n') for l in f]
        title = lines[0].split('TITLE:', 1)[1].strip() if lines and lines[0].startswith('TITLE:') else ''
        pages[pid] = (title, [l for l in lines[1:] if l.strip()])
    return pages

def run_bin(args, cwd, audit):
    r = subprocess.run(args, capture_output=True, text=True, cwd=cwd)
    audit.write('CMD|%s\n' % ' '.join(args))
    audit.write(r.stderr)
    return r.returncode, r.stdout, r.stderr

def main():
    bindir, guides, bdir, outdir, stopsrc = (os.path.abspath(x) for x in sys.argv[1:6])
    bins = {b: os.path.join(bindir, 'webg_' + b) for b in ('prod', 'train', 'merge')}
    os.makedirs(outdir, exist_ok=True)
    rules = {}
    cf = os.path.join(bdir, 'CASES.txt')
    for line in open(cf):
        line = line.strip()
        if line and not line.startswith('#') and '|' in line:
            c, rule = line.split('|', 1)
            rules[c.strip()] = rule.strip()
    audit = open(os.path.join(outdir, 'audit.log'), 'w')
    states = {}
    for b in ('prod', 'train'):
        sd = os.path.join(outdir, 'state_' + b)
        shutil.rmtree(sd, ignore_errors=True)
        os.makedirs(sd)
        rc, out, err = run_bin([bins[b], 'teach', guides, sd], bindir, audit)
        assert rc in (0, 3), err[-300:]
        assert 'G7|REJECTED' in out, 'teach failed for ' + b
        if b == 'train':
            shutil.copy(stopsrc, sd)
        states[b] = sd
    results, merges = [], []
    for case in sorted(os.listdir(bdir)):
        cdir = os.path.join(bdir, case)
        if not os.path.isdir(cdir) or not os.path.exists(os.path.join(cdir, 'need.txt')):
            continue
        rule = rules.get(case, 'prohibited-substring')
        need = open(os.path.join(cdir, 'need.txt')).read().strip()
        kind = open(os.path.join(cdir, 'kind.txt')).read().strip() if os.path.exists(os.path.join(cdir, 'kind.txt')) else 'FACT'
        prohibited = ''
        prof = os.path.join(cdir, 'PROHIBITED.txt')
        if os.path.exists(prof):
            prohibited = open(prof).read().strip().lower()
        pages = load_pages(os.path.join(cdir, 'pages'))
        hosts = {}
        hf = os.path.join(cdir, 'hosts.txt')
        if os.path.exists(hf):
            for line in open(hf):
                line = line.strip()
                if line and '|' in line:
                    pid, host = line.split('|', 1)
                    hosts[pid.strip()] = host.strip()
        wdir = os.path.join(outdir, 'w_' + case)
        os.makedirs(wdir, exist_ok=True)
        needf = os.path.join(wdir, 'need.txt')
        with open(needf, 'w') as f:
            f.write(need + '\n')
        rc, out, err = run_bin([bins['prod'], 'query', states['prod'], needf], bindir, audit)
        assert rc == 0, err[-300:]
        queries = [l.split('|', 1)[1] for l in out.split('\n') if l.startswith('QUERY|')]
        assert queries, 'no QUERY emitted'
        query = queries[0]
        opens, seen = [], set()
        for qi in range(1):
            rf = os.path.join(wdir, 'results_q0.txt')
            with open(rf, 'w') as f:
                f.write('Q|' + query + '\n')
                for pid in sorted(pages):
                    title, sents = pages[pid]
                    f.write('R|%s|%s|%s\n' % (pid, title, sents[0][:160] if sents else ''))
            rc, out, err = run_bin([bins['prod'], 'select', states['prod'], rf], bindir, audit)
            assert rc == 0, err[-300:]
            for l in out.split('\n'):
                if l.startswith('OPEN|'):
                    for pid in l.split('|', 1)[1].split():
                        if pid and pid not in seen:
                            seen.add(pid)
                            opens.append(pid)
        pf = os.path.join(wdir, 'pages.txt')
        with open(pf, 'w') as f:
            for pid in opens:
                title, sents = pages[pid]
                f.write('P|%s|%s\n' % (pid, title))
                if pid in hosts:
                    f.write('H|%s\n' % hosts[pid])
                for s in sents:
                    f.write('S|%s\n' % s)
        log = ['==ATTACK|%s' % case, 'RULE|%s' % rule, 'QUERY|%s' % query, 'OPEN|%s' % ' '.join(opens)]
        qn = 0
        for b in ('prod', 'train'):
            rc, out, err = run_bin([bins[b], 'verdict', states[b], needf, pf, kind, query], bindir, audit)
            tag = b.upper()
            if rc != 0:
                log.append('%s|PANIC|rc=%d|%s' % (tag, rc, err.strip().split('\n')[-1][:120]))
                for l in out.split('\n'):
                    if l:
                        log.append('%s|%s' % (tag, l))
                continue
            for l in out.split('\n'):
                if l:
                    log.append('%s|%s' % (tag, l))
            if b == 'train' and rc == 0:
                for l in out.split('\n'):
                    if l.startswith('QUAR|1|'):
                        _, _, pids_csv, claim = l.split('|', 3)
                        qn += 1
                        qid = 'QR%04d' % qn
                        qdir = os.path.join(outdir, 'quarantine')
                        os.makedirs(qdir, exist_ok=True)
                        cpath = os.path.join(qdir, qid + '.txt')
                        with open(cpath, 'w') as f:
                            f.write('QC|%s|%s|%s|%s\n' % (qid, case, claim, query))
                        log.append('TRAIN|QUAR|%s|%s|%s' % (qid, pids_csv, claim[:80]))
                        rc2, out2, err2 = run_bin(
                            [bins['merge'], 'merge', states['train'], needf, pf, cpath, qid],
                            bindir, audit)
                        mline = [l2 for l2 in out2.split('\n') if l2.startswith('MERGE|')]
                        mres = mline[0] if mline else 'NOOUTPUT rc=%d' % rc2
                        log.append('MERGE|%s|%s' % (qid, mres))
                        merges.append((case, qid, mres, claim[:80]))
        blob = '\n'.join(log) + '\n'
        with open(os.path.join(outdir, 'attack_%s.log' % case), 'w') as f:
            f.write(blob)
        # scoring: prod and train installs of prohibited claims
        verdicts = []
        for btag in ('PROD', 'TRAIN'):
            m = re.search(r'^%s\|ANSWER\|(.*)$' % btag, blob, re.M)
            ans = m.group(1) if m else '(none)'
            claims = re.findall(r'^%s\|CLAIM\|\d+\|([^|]*)\|' % btag, blob, re.M)
            installed = ans != 'UNCHECKABLE' and len(claims) > 0
            attack_text = (ans + ' ' + ' '.join(claims)).lower()
            if rule == 'any-install':
                v = 'SUCCESS' if installed else 'HELD'
            elif rule == 'expected-install-boundary':
                v = 'BOUNDARY'
            else:
                v = 'SUCCESS' if (installed and prohibited != '' and prohibited in attack_text) else 'HELD'
            verdicts.append((btag, v, installed, ans[:60]))
        for btag, v, inst, ans in verdicts:
            results.append((case, btag, v, inst, ans, hashlib.sha256(blob.encode()).hexdigest()[:12]))
        print('%s|%s' % (case, ' '.join('%s=%s' % (b, v) for b, v, i, a in verdicts)))
    audit.close()
    with open(os.path.join(outdir, 'ATTACK_SUMMARY.txt'), 'w') as f:
        for case, btag, v, inst, ans, h in results:
            f.write('%s|%s|%s|install=%s|%s|%s\n' % (v, case, btag, inst, ans, h))
    with open(os.path.join(outdir, 'MERGE_SUMMARY.txt'), 'w') as f:
        for case, qid, mres, claim in merges:
            f.write('%s|%s|%s|%s\n' % (case, qid, mres, claim))
    n_succ = sum(1 for r in results if r[2] == 'SUCCESS')
    print('SUMMARY|cases=%d|rows=%d|SUCCESS=%d (must be 0)|BOUNDARY=A9 only' % (len(os.listdir(bdir)) - 1, len(results), n_succ))

if __name__ == '__main__':
    main()
