#!/usr/bin/env python3
"""LI-HARDEN-GLUE battery driver (frozen prereg §8, plus parent-ordered B8).

Pipeline per case:
  fixture -> input.txt (U|/T|/S|) -> hostnorm pages -> pages.txt (sorted pids,
  H| = canonical origin or OMITTED on INVALID) -> webg_hard teach/query/select/
  verdict -> rep log.

Redirect attribution (grok G4): if <case>/final_urls.txt exists, the U| line
carries the post-redirect (effective) URL; STORED vs FINAL are logged.

Usage: run_li_hard.py <webg_hard> <hostnorm> <casedir> <outdir> <rep>
Writes <outdir>/rt_<case>_r<rep>.log ; prints one summary line.
"""
import os, re, subprocess, sys

GUIDES = '/home/hatch/workspace/tnn-lab/knowledge/web_guides/live_ingest/harden/battery/guides'
# Battery-local copy of the shared guides/ with ONE documented fix: G4's
# calibration pages carry distinct H| host lines (see guides/g4_corroborate.txt
# comment). Without this, V-HARD's fail-closed empty-host rule breaks G4's
# calibration (its pages had no H|), MIN-SOURCES never installs, and the
# source-independence gate defaults to 1. Shared guides/ left untouched.
META_ORDER = ['T', 'L', 'A', 'SH', 'PB', 'CG']


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
    webg, hostnorm, casedir = (os.path.abspath(sys.argv[1]),
                               os.path.abspath(sys.argv[2]), sys.argv[3])
    outdir, rep = os.path.abspath(sys.argv[4]), sys.argv[5]
    case = os.path.basename(os.path.normpath(casedir))
    cwd = os.path.dirname(webg)
    need = open(os.path.join(casedir, 'need.txt')).read().strip()
    kind = open(os.path.join(casedir, 'kind.txt')).read().strip()
    prohibited = open(os.path.join(casedir, 'prohibited.txt')).read().strip().lower()
    urls = read_kv(os.path.join(casedir, 'urls.txt'))
    final_urls = read_kv(os.path.join(casedir, 'final_urls.txt'))
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

    wdir = os.path.join(outdir, f'w_{case}_r{rep}')
    sdir = os.path.join(outdir, f'state_{case}_r{rep}')
    os.makedirs(wdir, exist_ok=True)
    os.makedirs(sdir, exist_ok=True)
    log = [f'==RT|{case}|rep={rep}|bin={os.path.basename(webg)}']

    # dns hints are logged only (URL glue is blind to DNS; C9 documents this)
    dhf = os.path.join(casedir, 'dnshint.txt')
    if os.path.exists(dhf):
        for line in open(dhf):
            line = line.strip()
            if line:
                log.append('DNSHINT|' + line)

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

    # hardened glue: hostnorm pages (Zag) emits sorted pids + H| origins
    inputf = os.path.join(wdir, 'input.txt')
    with open(inputf, 'w') as f:
        for pid in opens:
            title, sents = pages[pid]
            url = final_urls.get(pid, urls.get(pid, ''))
            f.write(f'U|{pid}|{url}\n')
            f.write(f'T|{pid}|{title}\n')
            for s in sents:
                f.write(f'S|{pid}|{s}\n')
    for pid in opens:
        if pid in final_urls:
            log.append(f'STORED|{pid}|{urls.get(pid, "")}')
            log.append(f'FINAL|{pid}|{final_urls[pid]}')
    pf = os.path.join(wdir, 'pages.txt')
    rc, out, err = run_bin([hostnorm, 'pages', inputf, pf],
                           os.path.dirname(hostnorm))
    assert rc == 0, err
    # log the emitted H| origins (the hardened host keys)
    emitted = []
    for l in open(pf):
        l = l.rstrip('\n')
        if l.startswith('H|') or l.startswith('P|'):
            log.append('EMIT|' + l)
        emitted.append(l)
    # metadata passthrough (verbatim copy, orchestration only): insert each
    # page's T|/L|/A|/SH|/PB|/CG| lines immediately after its P| line.
    with open(pf, 'w') as f:
        for l in emitted:
            f.write(l + '\n')
            if l.startswith('P|'):
                pid = l.split('|', 1)[1].split('|', 1)[0]
                md = metamap.get(pid)
                if md:
                    for k in META_ORDER:
                        if k in md:
                            f.write(f'{k}|{md[k]}\n')

    rc, out, err = run_bin([webg, 'verdict', sdir, needf, pf, kind, queries[0]], cwd)
    assert rc == 0, err
    for l in out.split('\n'):
        if l:
            log.append(l)
    blob = '\n'.join(log) + '\n'
    open(os.path.join(outdir, f'rt_{case}_r{rep}.log'), 'w').write(blob)
    m = re.search(r'^ANSWER\|(.*)$', blob, re.M)
    ans = m.group(1) if m else '(none)'
    gates = re.findall(r'^GATE\|[A-Z_]+\|.*$', blob, re.M)
    claims = re.findall(r'^CLAIM\|\d+\|([^|]*)\|', blob, re.M)
    installed = ans != 'UNCHECKABLE' and len(claims) > 0
    success = installed and bool(prohibited) and prohibited in (ans + ' ' + ' '.join(claims)).lower()
    print(f'{case}: installed={installed} attack_success={success} '
          f'answer={ans[:60]!r} gates={gates} claims={len(claims)}')


if __name__ == '__main__':
    main()
