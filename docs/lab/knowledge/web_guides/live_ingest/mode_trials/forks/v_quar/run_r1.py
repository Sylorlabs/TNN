#!/usr/bin/env python3
"""H3 R1 battery: A1-A9 attacks under PROD (install check) and TRAIN (quarantine).

For each attack: teach (once per binary) -> query -> select(all) -> verdict.
PROD: reports installed answer; BREACH if it contains the PROHIBITED string.
TRAIN: collects QUAR|1 lines; each quarantined claim is adjudicated by the
merge gate; reports MERGE bits.
Writes r1_report.txt. Deterministic, zero RNG. Glue only.
Usage: run_r1.py <outdir>
"""
import os, re, sys, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ATK = '/home/hatch/workspace/scratch-li-f3/attacks'
BIN = {'prod': os.path.join(HERE, 'webg_prod'),
       'train': os.path.join(HERE, 'webg_train'),
       'merge': os.path.join(HERE, 'webg_merge')}
GUIDES = '/home/hatch/workspace/scratch-li-forkbase/guides'
ATTACKS = ['A1_smuggle', 'A2_sockpuppet', 'A3_stuffed', 'A4_single',
           'A5_injpair', 'A6_fragment', 'A7_caughtinj', 'A8_evadetop',
           'A9_xhost']

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

def run_bin(args):
    r = subprocess.run(args, capture_output=True, text=True, cwd=OUTDIR)
    return r.returncode, r.stdout, r.stderr

def main():
    global OUTDIR
    OUTDIR = os.path.abspath(sys.argv[1])
    os.makedirs(OUTDIR, exist_ok=True)
    os.chdir(OUTDIR)
    audit = open('audit.log', 'w')
    rep = []
    # teach once per binary
    states = {}
    for b in ('prod', 'train'):
        sd = 'state_' + b
        os.makedirs(sd, exist_ok=True)
        rc, out, err = run_bin([BIN[b], 'teach', GUIDES, sd])
        audit.write(err)
        states[b] = sd
        ok = rc != 3 and 'G7|REJECTED' in out
        rep.append('TEACH|%s|rc=%d|ok=%s' % (b, rc, ok))
        if not ok:
            rep.append('VOID|teach failed for ' + b)
            open('r1_report.txt', 'w').write('\n'.join(rep) + '\n')
            print('VOID')
            sys.exit(3)
        with open(os.path.join(HERE, 'stoplist_para.txt'), 'rb') as f:
            stop = f.read()
        with open(os.path.join(sd, 'stoplist_para.txt'), 'wb') as f:
            f.write(stop)

    qn = 0
    for atk in ATTACKS:
        ad = os.path.join(ATK, atk)
        with open(os.path.join(ad, 'need.txt')) as f:
            need = f.read().strip()
        with open(os.path.join(ad, 'PROHIBITED.txt')) as f:
            prohib = f.read().strip()
        hosts = {}
        hp = os.path.join(ad, 'hosts.txt')
        if os.path.exists(hp):
            with open(hp) as f:
                for ln in f:
                    ln = ln.strip()
                    if ln and '|' in ln:
                        k, v = ln.split('|', 1)
                        hosts[k] = v
        wdir = os.path.join('work', atk)
        os.makedirs(wdir, exist_ok=True)
        pages = []
        for fn in sorted(os.listdir(os.path.join(ad, 'pages'))):
            if not fn.endswith('.txt'):
                continue
            pid = fn[:-4]
            with open(os.path.join(ad, 'pages', fn), encoding='utf-8', errors='replace') as f:
                raw = f.read().split('\n')
            title = raw[0][len('TITLE:'):].strip() if raw and raw[0].startswith('TITLE:') else pid
            sents = split_sentences('\n'.join(raw[1:]))
            host = hosts.get(pid, pid + '.example')
            pages.append((pid, title, host, sents))
        # pages.txt with ALL pages (no select filtering for attacks)
        ppath = os.path.join(wdir, 'pages.txt')
        with open(ppath, 'w') as f:
            for pid, title, host, sents in pages:
                f.write('P|%s|%s\n' % (pid, title))
                f.write('H|%s\n' % host)
                for s in sents:
                    f.write('S|%s\n' % s)
        npath = os.path.join(wdir, 'need.txt')
        with open(npath, 'w') as f:
            f.write(need + '\n')
        # query to get the query string
        rc, out, err = run_bin([BIN['prod'], 'query', states['prod'], npath])
        audit.write(err)
        queries = [l.split('|', 1)[1] for l in out.split('\n') if l.startswith('QUERY|')]
        query = queries[0] if queries else need
        for b in ('prod', 'train'):
            rc, out, err = run_bin([BIN[b], 'verdict', states[b], npath, ppath,
                                    'FACT', query])
            audit.write(err)
            with open(os.path.join(wdir, 'verdict_%s.out' % b), 'w') as f:
                f.write(out)
            answers = [l.split('|', 1)[1] for l in out.split('\n')
                       if l.startswith('ANSWER|') and l != 'ANSWER|UNCHECKABLE']
            installed = answers[0] if answers else None
            breach = bool(installed and prohib and prohib in installed)
            flags = [l.split('|', 2)[2] for l in out.split('\n')
                     if l.startswith('FLAG|INJECTION|')]
            rep.append('%s|%s|installed=%s|breach=%s|injflags=%s' %
                       (atk, b, installed[:60] if installed else None, breach,
                        ','.join(flags)))
            if b == 'train':
                for l in out.split('\n'):
                    if l.startswith('QUAR|1|'):
                        _, _, pids_csv, claim = l.split('|', 3)
                        qn += 1
                        qid = 'QR%04d' % qn
                        cpath = os.path.join('quarantine', qid + '.txt')
                        os.makedirs('quarantine', exist_ok=True)
                        with open(cpath, 'w') as f:
                            f.write('QC|%s|%s|%s|%s\n' % (qid, atk, claim, query))
                        rep.append('%s|QUAR|%s|%s|%s' % (atk, qid, pids_csv, claim[:60]))
                        # merge adjudication
                        rc2, out2, err2 = run_bin(
                            [BIN['merge'], 'merge', states['train'], npath,
                             ppath, cpath, qid])
                        audit.write(err2)
                        m = [l2 for l2 in out2.split('\n') if l2.startswith('MERGE|')]
                        rep.append('%s|MERGE|%s|%s' % (atk, qid, m[0] if m else 'NOOUTPUT rc=%d' % rc2))
    audit.close()
    open('r1_report.txt', 'w').write('\n'.join(rep) + '\n')
    print('\n'.join(rep))
    print('DONE')

if __name__ == '__main__':
    main()
