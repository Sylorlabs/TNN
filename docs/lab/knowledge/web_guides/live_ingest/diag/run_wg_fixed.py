#!/usr/bin/env python3
"""WG-1 harness: the deterministic 'internet' + trial driver. Glue only — no reasoning.
Usage: run_wg.py <guided|blind> <battery_file> <outdir> <rep>
"""
import os, re, subprocess, sys, hashlib

HERE = "/home/hatch/workspace/tnn-lab/knowledge/web_guides"
WEBG = "/tmp/webg_fixed"
CORPUS = os.path.join(HERE, 'corpus', 'pages')
GUIDES = os.path.join(HERE, 'guides')
EMPTY_GUIDES = os.path.join(HERE, 'empty_guides')

def toks(s):
    return re.findall(r'[a-z0-9]+', s.lower())

def load_corpus():
    pages = {}
    for fn in sorted(os.listdir(CORPUS)):
        if not fn.endswith('.txt'):
            continue
        pid = fn[:-4]
        with open(os.path.join(CORPUS, fn)) as f:
            lines = [l.rstrip('\n') for l in f]
        title = lines[0].split('TITLE:', 1)[1].strip() if lines[0].startswith('TITLE:') else ''
        sents = [l for l in lines[1:] if l.strip()]
        pages[pid] = (title, sents)
    return pages

def search(query, pages, topn=5):
    qt = toks(query)
    scored = []
    for pid, (title, sents) in pages.items():
        body = ' '.join(sents)
        tl, bl = title.lower(), body.lower()
        score = 3 * sum(tl.count(t) for t in qt) + sum(bl.count(t) for t in qt)
        scored.append((-score, pid))
    scored.sort()
    out = []
    for neg, pid in scored[:topn]:
        title, sents = pages[pid]
        snip = sents[0]
        for s in sents:
            sl = s.lower()
            if any(t in sl for t in qt):
                snip = s
                break
        out.append((pid, title, snip[:160]))
    return out

def run_bin(args, inp_dir):
    r = subprocess.run(args, capture_output=True, text=True, cwd=HERE)
    return r.returncode, r.stdout

def main():
    arm, batfile, outdir, rep = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    os.makedirs(outdir, exist_ok=True)
    pages = load_corpus()
    guides_dir = GUIDES if arm == 'guided' else EMPTY_GUIDES
    os.makedirs(EMPTY_GUIDES, exist_ok=True)
    state_dir = os.path.join(outdir, f'state_{arm}_r{rep}')
    os.makedirs(state_dir, exist_ok=True)
    log = []
    log.append(f'RUN|{arm}|{os.path.basename(batfile)}|rep={rep}')

    rc, out = run_bin([WEBG, 'teach', guides_dir, state_dir], HERE)
    log.append(f'TEACH|rc={rc}')
    log.append(out.rstrip('\n'))
    if rc == 3:
        log.append('TEACH|VOID')
    assert rc in (0, 3), out[-500:]

    with open(batfile) as f:
        tasks = [l.rstrip('\n') for l in f if l.startswith('TASK|')]

    for t in tasks:
        parts = t.split('|')
        tid, need, expected, kind, adv = parts[1], parts[2], parts[3], parts[4], parts[5]
        extra = parts[6] if len(parts) > 6 else '-'
        log.append(f'==TASK|{tid}|{kind}|{need}')
        workdir = os.path.join(outdir, f'w_{arm}_{tid}_r{rep}')
        os.makedirs(workdir, exist_ok=True)
        need_file = os.path.join(workdir, 'need.txt')
        with open(need_file, 'w') as f:
            f.write(need + '\n')

        qargs = [WEBG, 'query', state_dir, need_file] + ([extra] if extra != '-' else [])
        rc, out = run_bin(qargs, HERE)
        assert rc == 0, out[-500:]
        queries = [l.split('|', 1)[1] for l in out.split('\n') if l.startswith('QUERY|')]
        assert queries, 'no QUERY emitted'
        # search each query; run select PER QUERY and union the opened pids
        # (multihop needs both entities' pages, not just the first query's top-3)
        opens = []
        seen_open = set()
        for qi, q in enumerate(queries):
            log.append(f'{tid}|QUERY|{q}')
            qres = os.path.join(workdir, f'results_q{qi}.txt')
            with open(qres, 'w') as f:
                f.write('Q|' + q + '\n')
                for pid, title, snip in search(q, pages):
                    f.write(f'R|{pid}|{title}|{snip}\n')
                    log.append(f'{tid}|RESULT|{pid}|{title}')
            rc, out = run_bin([WEBG, 'select', state_dir, qres], HERE)
            assert rc == 0, out[-500:]
            qopens = []
            for l in out.split('\n'):
                if l.startswith('OPEN|'):
                    qopens = l.split('|', 1)[1].split()
                log.append(f'{tid}|{l}' if l else f'{tid}|')
            assert qopens, 'no OPEN emitted'
            for pid in qopens:
                if pid not in seen_open:
                    seen_open.add(pid)
                    opens.append(pid)

        pages_file = os.path.join(workdir, 'pages.txt')
        with open(pages_file, 'w') as f:
            for pid in opens:
                title, sents = pages[pid]
                f.write(f'P|{pid}|{title}\n')
                for s in sents:
                    f.write(f'S|{s}\n')

        vargs = [WEBG, 'verdict', state_dir, need_file, pages_file, kind, queries[0]] + ([extra] if extra != '-' else [])
        rc, out = run_bin(vargs, HERE)
        assert rc == 0, out[-500:]
        for l in out.split('\n'):
            if l:
                log.append(f'{tid}|{l}')
        log.append(f'{tid}|EXPECTED|{expected}')

    blob = '\n'.join(log) + '\n'
    sha = hashlib.sha256(blob.encode()).hexdigest()
    with open(os.path.join(outdir, f'run_{arm}_{os.path.basename(batfile).replace(".txt","")}_r{rep}.log'), 'w') as f:
        f.write(blob)
    print(f'DONE|{arm}|{batfile}|rep={rep}|sha256={sha}')

if __name__ == '__main__':
    main()
