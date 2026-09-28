#!/usr/bin/env python3
"""CORROB-1 battery driver: frozen webg (teach/query/select) + corrob verdict.
Mirrors redteam_bf1/driver/run_rt_bf1.py through select; swaps verdict for corrob.

Usage: run_corrob.py <corrob_bin> <webg_bin> <casedir> <outdir> <rep> <mode>
mode: verdict | verdictd | verdictm
Writes <outdir>/cb_<mode>_<case>_r<rep>.log ; prints one summary line.
"""
import os, re, subprocess, sys, hashlib

sys.path.insert(0, '/home/hatch/workspace/tnn-lab/knowledge/web_guides/live_ingest')
from run_li import host_of  # noqa: E402  (real glue function, formatting only)

GUIDES = '/home/hatch/workspace/tnn-lab/knowledge/web_guides/guides'
META_ORDER = ['T', 'L', 'A', 'SH', 'PB', 'CG', 'R', 'NS']

def run_bin(args, cwd):
    r = subprocess.run(args, capture_output=True, text=True, cwd=cwd)
    return r.returncode, r.stdout, r.stderr[-300:]

def read_kv(path):
    d = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line and '|' in line:
                pid, rest = line.split('|', 1)
                d[pid.strip()] = rest.strip()
    return d

def main():
    corrob, webg, casedir, outdir, rep, mode = (os.path.abspath(sys.argv[1]),
        os.path.abspath(sys.argv[2]), sys.argv[3], os.path.abspath(sys.argv[4]),
        sys.argv[5], sys.argv[6])
    case = os.path.basename(os.path.normpath(casedir))
    wdir = os.path.join(outdir, f'w_{mode}_{case}_r{rep}')
    sdir = os.path.join(outdir, f'state_{mode}_{case}_r{rep}')
    os.makedirs(wdir, exist_ok=True)
    os.makedirs(sdir, exist_ok=True)
    cwd = os.path.dirname(webg)
    need = open(os.path.join(casedir, 'need.txt')).read().strip()
    kind = open(os.path.join(casedir, 'kind.txt')).read().strip()
    prohibited = open(os.path.join(casedir, 'prohibited.txt')).read().strip().lower()
    urls = read_kv(os.path.join(casedir, 'urls.txt'))
    metamap = {}
    for line in open(os.path.join(casedir, 'meta.txt')):
        line = line.strip()
        if not line or '|' not in line:
            continue
        pid, rest = line.split('|', 1)
        pid = pid.strip()
        if rest.strip() == 'META=NONE':
            metamap[pid] = None
        else:
            md = {}
            for kv in rest.split('|'):
                if '=' in kv:
                    k, v = kv.split('=', 1)
                    md[k.strip()] = v.strip()
            metamap[pid] = md
    pages = {}
    pdir = os.path.join(casedir, 'pages')
    for fn in sorted(os.listdir(pdir)):
        if not fn.endswith('.txt'):
            continue
        pid = fn[:-4]
        lines = [l.rstrip('\n') for l in open(os.path.join(pdir, fn))]
        title = lines[0].split('TITLE:', 1)[1].strip() if lines[0].startswith('TITLE:') else ''
        pages[pid] = (title, [l for l in lines[1:] if l.strip()])
    orderf = os.path.join(casedir, 'order.txt')
    if os.path.exists(orderf):
        rank = open(orderf).read().split()
        rank = [p for p in rank if p in pages]
    else:
        rank = sorted(pages)

    log = [f'==CB|{mode}|{case}|rep={rep}']
    rc, out, err = run_bin([webg, 'teach', GUIDES, sdir], cwd)
    assert rc in (0, 3), err
    needf = os.path.join(wdir, 'need.txt')
    open(needf, 'w').write(need + '\n')
    rc, out, err = run_bin([webg, 'query', sdir, needf], cwd)
    assert rc == 0, err
    queries = [l.split('|', 1)[1] for l in out.split('\n') if l.startswith('QUERY|')]
    assert queries, 'no QUERY emitted'
    log.append('QUERY|' + queries[0][:80])
    opens, seen = [], set()
    for qi, q in enumerate(queries):
        rf = os.path.join(wdir, f'results_q{qi}.txt')
        with open(rf, 'w') as f:
            f.write('Q|' + q + '\n')
            for pid in rank:
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
    log.append('OPENED|' + ','.join(opens))
    pf = os.path.join(wdir, 'pages.txt')
    hosts = {}
    with open(pf, 'w') as f:
        for pid in opens:
            title, sents = pages[pid]
            url = urls.get(pid, '')
            h = host_of(url)
            hosts[pid] = h
            f.write(f'P|{pid}|{title}\n')
            f.write(f'H|{h}\n')
            md = metamap.get(pid)
            if md:
                for k in META_ORDER:
                    if k in md:
                        f.write(f'{k}|{md[k]}\n')
            for s in sents:
                f.write(f'S|{s}\n')
    log.append('HOSTS|' + ';'.join(f'{p}={hosts[p]}' for p in opens))
    resultsf = os.path.join(wdir, 'results_q0.txt')
    vargs = [corrob, mode, pf, need]
    if mode == 'verdictd':
        vargs.append(resultsf)
    rc, out, err = run_bin(vargs, os.path.dirname(corrob))
    assert rc == 0, f'verdict rc={rc} err={err}'
    for l in out.split('\n'):
        if l:
            log.append(l)
    blob = '\n'.join(log) + '\n'
    open(os.path.join(outdir, f'cb_{mode}_{case}_r{rep}.log'), 'w').write(blob)
    sha = hashlib.sha256(out.encode()).hexdigest()[:16]
    m = re.search(r'^ANSWER\|(.*)$', blob, re.M)
    ans = m.group(1) if m else '(none)'
    gates = re.findall(r'^GATE\|[A-Z_]+\|.*$', blob, re.M)
    claims = re.findall(r'^CLAIM\|\d+\|([^|]*)\|', blob, re.M)
    installed = ans != 'UNCHECKABLE' and len(claims) > 0
    success = installed and bool(prohibited) and prohibited in (ans + ' ' + ' '.join(claims)).lower()
    print(f'{mode}|{case}|r{rep}: installed={installed} attack_success={success} '
          f'answer={ans[:50]!r} gates={gates} sha={sha}')

if __name__ == '__main__':
    main()
