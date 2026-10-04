#!/usr/bin/env python3
"""C2 fixture driver for V-PARA. Glue only — no reasoning.

Runs each nf-b-* (Type-B honest) and nf-c-* (Type-C withhold controls) cluster
through teach -> query -> select -> verdict, using the snapshot pages directly.
Hosts are derived from the manifest URLs (src-a.example vs src-b.example, etc.)

Usage: c2_drive.py <webg_bin> <guides_dir> <fixtures_dir> <outdir>
"""
import os, re, subprocess, sys, hashlib
from urllib.parse import urlparse

def run_bin(args, cwd):
    r = subprocess.run(args, capture_output=True, text=True, cwd=cwd)
    return r.returncode, r.stdout, r.stderr[-300:]

def load_manifest(mpath):
    clusters = {}
    cur = None
    for line in open(mpath):
        line = line.strip()
        if line.startswith('C|'):
            _, cid, need = line.split('|', 2)
            cur = cid
            clusters[cid] = {'need': need, 'urls': []}
        elif line.startswith('U|') and cur:
            _, cid, url = line.split('|', 2)
            clusters[cid]['urls'].append(url)
    return clusters

def main():
    webg, guides, fxdir, outdir = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    os.makedirs(outdir, exist_ok=True)
    cwd = os.path.dirname(os.path.abspath(webg))
    snap = os.path.join(fxdir, 'snap')
    clusters = load_manifest(os.path.join(fxdir, 'manifest_fixtures.txt'))
    # ground truth
    gt = {}
    for line in open(os.path.join(fxdir, 'ground_truth.md')):
        m = re.match(r'\|\s*([A-Z]-\d+)\s*\|\s*(nf-[a-z]-\d+)\s*\|', line)
        if m:
            parts = [p.strip() for p in line.strip().strip('|').split('|')]
            gt[m.group(2)] = (parts[0], parts[2], parts[4])  # fact, type, verdict
    results = []
    for cid in sorted(clusters):
        if not cid.startswith('nf-b-') and not cid.startswith('nf-c-'):
            continue
        c = clusters[cid]
        log = [f'==C2|{cid}']
        wdir = os.path.join(outdir, f'w_{cid}')
        sdir = os.path.join(outdir, f'state_{cid}')
        os.makedirs(wdir, exist_ok=True)
        os.makedirs(sdir, exist_ok=True)
        rc, out, err = run_bin([webg, 'teach', guides, sdir], cwd)
        assert rc in (0, 3), err
        needf = os.path.join(wdir, 'need.txt')
        with open(needf, 'w') as f:
            f.write(c['need'] + '\n')
        rc, out, err = run_bin([webg, 'query', sdir, needf], cwd)
        assert rc == 0, err
        queries = [l.split('|', 1)[1] for l in out.split('\n') if l.startswith('QUERY|')]
        assert queries, 'no QUERY emitted'
        # build pages.txt directly from snapshots (worst-case: all pages)
        pf = os.path.join(wdir, 'pages.txt')
        with open(pf, 'w') as f:
            for url in c['urls']:
                host = urlparse(url).hostname or 'unknown'
                # snapshot file: snap/<cid>/<cid>-pN.txt
                m = re.search(r'/(p\d+)$', url)
                pnum = m.group(1) if m else 'p1'
                spath = os.path.join(snap, cid, f'{cid}-{pnum}.txt')
                lines = [l.rstrip('\n') for l in open(spath)]
                title = lines[0].split('TITLE:', 1)[1].strip() if lines[0].startswith('TITLE:') else cid
                pid = f'{cid}-{pnum}'
                f.write(f'P|{pid}|{title}\n')
                f.write(f'H|{host}\n')
                for s in lines[1:]:
                    if s.strip():
                        f.write(f'S|{s.strip()}\n')
        rc, out, err = run_bin([webg, 'verdict', sdir, needf, pf, 'FACT', queries[0]], cwd)
        assert rc == 0, err
        for l in out.split('\n'):
            if l:
                log.append(l)
        blob = '\n'.join(log) + '\n'
        lp = os.path.join(outdir, f'c2_{cid}.log')
        with open(lp, 'w') as f:
            f.write(blob)
        m = re.search(r'^ANSWER\|(.*)$', blob, re.M)
        ans = m.group(1) if m else '(none)'
        installed = ans != 'UNCHECKABLE'
        exp = gt.get(cid, ('?', '?', '?'))[2] if cid in gt else '?'
        match = (installed and exp == 'INSTALL') or (not installed and exp == 'WITHHOLD')
        results.append((cid, installed, exp, match, ans[:70], hashlib.sha256(blob.encode()).hexdigest()[:12]))
        print(f'{"OK " if match else "MISS"}|{cid}|install={installed}|exp={exp}|{ans[:50]}')
    with open(os.path.join(outdir, 'C2_SUMMARY.txt'), 'w') as f:
        for cid, inst, exp, match, ans, h in results:
            f.write(f'{"OK" if match else "MISS"}|{cid}|install={inst}|exp={exp}|{ans}|{h}\n')
    n_ok = sum(1 for r in results if r[3])
    print(f'SUMMARY|cases={len(results)}|match={n_ok}')

if __name__ == '__main__':
    main()
