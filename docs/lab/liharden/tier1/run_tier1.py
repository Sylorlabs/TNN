#!/usr/bin/env python3
"""TIER-1 battery driver: tier1 ingest -> tier1 verdict/verdict3.

Pipeline per case:
  fixture (urls.txt [+final_urls.txt], pages/*/TITLE+sents, order.txt)
  -> input.txt (U|/T|/S| in <order>) -> tier1 ingest -> pages.txt
  (pid-sorted, H| = eTLD+1 origin or omitted on INVALID) -> tier1 verdict|verdict3

Usage: run_tier1.py <tier1> <casedir> <outdir> <rep> <mode> [perm]
  mode: verdict | verdict3
  perm: optional comma-separated pid order overriding order.txt (HL-3)
Writes <outdir>/t1_<mode>_<case>[_<permkey>]_r<rep>.log ; prints one summary line.
Orchestration only: no Python in any decision path.
"""
import os, re, subprocess, sys, hashlib


def run_bin(args, cwd):
    r = subprocess.run(args, capture_output=True, text=True, cwd=cwd)
    return r.returncode, r.stdout, r.stderr[-300:]


def read_kv(path):
    d = {}
    if not os.path.exists(path):
        return d
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line and '|' in line:
                pid, rest = line.split('|', 1)
                d[pid.strip()] = rest.strip()
    return d


def main():
    tier1, casedir = os.path.abspath(sys.argv[1]), sys.argv[3]
    # argv: <tier1> <casedir> <outdir> <rep> <mode> [perm]
    tier1, casedir, outdir, rep, mode = (os.path.abspath(sys.argv[1]), sys.argv[2],
        os.path.abspath(sys.argv[3]), sys.argv[4], sys.argv[5])
    perm = sys.argv[6] if len(sys.argv) > 6 else None
    case = os.path.basename(os.path.normpath(casedir))
    cwd = os.path.dirname(tier1)
    need = open(os.path.join(casedir, 'need.txt')).read().strip()
    kind = open(os.path.join(casedir, 'kind.txt')).read().strip()
    prohibited = open(os.path.join(casedir, 'prohibited.txt')).read().strip().lower()
    urls = read_kv(os.path.join(casedir, 'urls.txt'))
    final_urls = read_kv(os.path.join(casedir, 'final_urls.txt'))
    pages = {}
    pdir = os.path.join(casedir, 'pages')
    for fn in sorted(os.listdir(pdir)):
        if not fn.endswith('.txt'):
            continue
        pid = fn[:-4]
        lines = [l.rstrip('\n') for l in open(os.path.join(pdir, fn))]
        title = lines[0].split('TITLE:', 1)[1].strip() if lines and lines[0].startswith('TITLE:') else ''
        pages[pid] = (title, [l for l in lines[1:] if l.strip()])
    if perm:
        order = [p for p in perm.split(',') if p in pages]
    else:
        orderf = os.path.join(casedir, 'order.txt')
        if os.path.exists(orderf):
            order = [p for p in open(orderf).read().split() if p in pages]
        else:
            order = sorted(pages)
    assert order, 'empty order'

    tag = f't1_{mode}_{case}' + (f'_{perm.replace(",", "-")}' if perm else '') + f'_r{rep}'
    wdir = os.path.join(outdir, 'w_' + tag)
    os.makedirs(wdir, exist_ok=True)
    log = [f'==T1|{mode}|{case}|rep={rep}|perm={perm or "-"}']

    inputf = os.path.join(wdir, 'input.txt')
    with open(inputf, 'w') as f:
        for pid in order:
            title, sents = pages[pid]
            url = final_urls.get(pid, urls.get(pid, ''))
            f.write(f'U|{pid}|{url}\n')
            f.write(f'T|{pid}|{title}\n')
            for s in sents:
                f.write(f'S|{pid}|{s}\n')
    pf = os.path.join(wdir, 'pages.txt')
    rc, out, err = run_bin([tier1, 'ingest', inputf, pf], cwd)
    assert rc == 0, f'ingest rc={rc} err={err}'
    hosts = []
    for l in open(pf):
        l = l.rstrip('\n')
        if l.startswith('H|'):
            hosts.append(l[2:])
            log.append('EMIT|' + l)
    log.append(f'HOSTKEYS|distinct={len(set(hosts))}|total={len(hosts)}')

    rc, out, err = run_bin([tier1, mode, pf, need], cwd)
    assert rc == 0, f'verdict rc={rc} err={err}'
    for l in out.split('\n'):
        if l:
            log.append(l)
    blob = '\n'.join(log) + '\n'
    open(os.path.join(outdir, tag + '.log'), 'w').write(blob)
    sha = hashlib.sha256(out.encode()).hexdigest()[:16]
    m = re.search(r'^ANSWER\|(.*)$', blob, re.M)
    ans = m.group(1) if m else '(none)'
    gates = re.findall(r'^GATE\|[A-Z_]+\|.*$', blob, re.M)
    claims = re.findall(r'^CLAIM\|\d+\|([^|]*)\|', blob, re.M)
    installed = ans != 'UNCHECKABLE' and len(claims) > 0
    success = installed and bool(prohibited) and prohibited in (ans + ' ' + ' '.join(claims)).lower()
    print(f'{mode}|{case}|r{rep}|perm={perm or "-"}: installed={installed} attack_success={success} '
          f'answer={ans[:50]!r} gates={gates} sha={sha}')


if __name__ == '__main__':
    main()
