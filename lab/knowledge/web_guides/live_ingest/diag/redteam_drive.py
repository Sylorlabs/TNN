#!/usr/bin/env python3
"""LI-1 red-team driver. Glue only — no reasoning.

Mirrors run_wg.py's protocol exactly (teach -> query -> select -> verdict)
but supplies the candidate page set directly instead of keyword search:
worst-case retrieval for the attack. If an attack cannot install even when
every attack page is retrieved and opened, it cannot install via search.

Layout: attacks/<case>/pages/*.txt  (TITLE: + sentences, like corpus/pages)
        attacks/<case>/need.txt      (the information need)
        attacks/<case>/kind.txt      (FACT | CONTRA | INJ ...)
        attacks/<case>/EXPECT.txt    (human-written expectation, not fed to engine)

Usage: redteam_drive.py <webg_bin> <guides_dir> <attacks_dir> <outdir>
Emits <outdir>/attack_<case>.log with the full verdict transcript and a
one-line ATTACK verdict: INSTALL (bad) or WITHHELD (good) plus what installed.
"""
import os, re, subprocess, sys, hashlib

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

def run_bin(args, cwd):
    r = subprocess.run(args, capture_output=True, text=True, cwd=cwd)
    return r.returncode, r.stdout, r.stderr[-300:]

def main():
    webg, guides, adir, outdir = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    os.makedirs(outdir, exist_ok=True)
    cwd = os.path.dirname(os.path.abspath(webg))
    results = []
    for case in sorted(os.listdir(adir)):
        cdir = os.path.join(adir, case)
        if not os.path.isdir(cdir) or not os.path.exists(os.path.join(cdir, 'need.txt')):
            continue
        log = [f'==ATTACK|{case}']
        need = open(os.path.join(cdir, 'need.txt')).read().strip()
        kind = open(os.path.join(cdir, 'kind.txt')).read().strip() if os.path.exists(os.path.join(cdir, 'kind.txt')) else 'FACT'
        expect = open(os.path.join(cdir, 'EXPECT.txt')).read().strip() if os.path.exists(os.path.join(cdir, 'EXPECT.txt')) else ''
        log.append(f'EXPECT|{expect}')
        prof = os.path.join(cdir, 'PROHIBITED.txt')
        prohibited = open(prof).read().strip().lower() if os.path.exists(prof) else ''
        pages = load_pages(os.path.join(cdir, 'pages'))
        hosts = {}
        hf = os.path.join(cdir, 'hosts.txt')
        if os.path.exists(hf):
            for line in open(hf):
                line = line.strip()
                if line and '|' in line:
                    pid, host = line.split('|', 1)
                    hosts[pid.strip()] = host.strip()
        wdir = os.path.join(outdir, f'w_{case}')
        sdir = os.path.join(outdir, f'state_{case}')
        os.makedirs(wdir, exist_ok=True)
        os.makedirs(sdir, exist_ok=True)
        rc, out, err = run_bin([webg, 'teach', guides, sdir], cwd)
        assert rc in (0, 3), err
        log.append(f'TEACH|rc={rc}')
        needf = os.path.join(wdir, 'need.txt')
        with open(needf, 'w') as f:
            f.write(need + '\n')
        rc, out, err = run_bin([webg, 'query', sdir, needf], cwd)
        assert rc == 0, err
        queries = [l.split('|', 1)[1] for l in out.split('\n') if l.startswith('QUERY|')]
        assert queries, 'no QUERY emitted'
        log.append(f'QUERY|{queries[0]}')
        opens, seen = [], set()
        for qi, q in enumerate(queries):
            rf = os.path.join(wdir, f'results_q{qi}.txt')
            with open(rf, 'w') as f:
                f.write('Q|' + q + '\n')
                for pid in sorted(pages):
                    title, sents = pages[pid]
                    f.write(f'R|{pid}|{title}|{sents[0][:160] if sents else ""}\n')
            rc, out, err = run_bin([webg, 'select', sdir, rf], cwd)
            assert rc == 0, err
            for l in out.split('\n'):
                if l.startswith('OPEN|'):
                    for pid in l.split('|', 1)[1].split():
                        if pid and pid not in seen:
                            seen.add(pid)
                            opens.append(pid)
        log.append(f'OPEN|{" ".join(opens)}')
        pf = os.path.join(wdir, 'pages.txt')
        with open(pf, 'w') as f:
            for pid in opens:
                title, sents = pages[pid]
                f.write(f'P|{pid}|{title}\n')
                if pid in hosts:
                    f.write(f'H|{hosts[pid]}\n')
                for s in sents:
                    f.write(f'S|{s}\n')
        rc, out, err = run_bin([webg, 'verdict', sdir, needf, pf, kind, queries[0]], cwd)
        assert rc == 0, err
        for l in out.split('\n'):
            if l:
                log.append(l)
        blob = '\n'.join(log) + '\n'
        lp = os.path.join(outdir, f'attack_{case}.log')
        with open(lp, 'w') as f:
            f.write(blob)
        m = re.search(r'^ANSWER\|(.*)$', blob, re.M)
        ans = m.group(1) if m else '(none)'
        claims = re.findall(r'^CLAIM\|\d+\|([^|]*)\|', blob, re.M)
        flags = re.findall(r'^FLAG\|[A-Z]+\|\S+', blob, re.M)
        installed = ans != 'UNCHECKABLE' and len(claims) > 0
        # ATTACK SUCCESS = the prohibited claim got installed (not just any install:
        # legitimate clean-claim installs are the correct outcome, not attacks).
        attack_text = (ans + ' ' + ' '.join(claims)).lower()
        success = installed and prohibited != '' and prohibited in attack_text
        results.append((case, installed, success, ans[:80], ' // '.join(c[:60] for c in claims), ' '.join(flags),
                        hashlib.sha256(blob.encode()).hexdigest()[:12]))
        print(f'{"SUCCESS " if success else "HELD    "}|{case}|install={installed}|answer={ans[:60]}|claims={len(claims)}|flags={flags}')
    with open(os.path.join(outdir, 'ATTACK_SUMMARY.txt'), 'w') as f:
        for case, inst, success, ans, cl, fl, h in results:
            f.write(f'{"SUCCESS" if success else "HELD"}|{case}|install={inst}|{ans}|{cl}|{fl}|{h}\n')
    n_succ = sum(1 for r in results if r[2])
    n_inst = sum(1 for r in results if r[1])
    print(f'SUMMARY|attacks={len(results)}|installs={n_inst}|attack_successes={n_succ} (must be 0)')

if __name__ == '__main__':
    main()
