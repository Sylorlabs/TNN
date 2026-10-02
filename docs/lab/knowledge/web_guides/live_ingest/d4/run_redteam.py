#!/usr/bin/env python3
"""Red-team battery harness: runs an arbitrary battery (pbattery format)
through control and d4 arms and reports per-cluster verdicts.

Usage: python3 run_redteam.py <battery_dir> <outdir>
<battery_dir>/<cid>/{need.txt,hosts.txt,<cid>-p1.txt,<cid>-p2.txt}

The red-team author must NOT read ~/workspace/d4/src/ (implementation),
the verb table, or any D4 internals. This harness is the only interface.
"""
import os, re, sys, subprocess
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
ARMS = {'control': os.path.join(HERE, 'src', 'control_bin'),
        'd4': os.path.join(HERE, 'src', 'd4_bin')}
GUIDES = '/home/hatch/workspace/scratch-li-principles/arm_control/guides'


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


def host_of(url):
    try:
        return (urlparse(url).hostname or '').lower()
    except Exception:
        return ''


def run_bin(args):
    r = subprocess.run(args, capture_output=True, text=True, cwd=HERE)
    return r.returncode, r.stdout, r.stderr


def load_battery(batdir):
    cls = []
    for cid in sorted(os.listdir(batdir)):
        d = os.path.join(batdir, cid)
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
            url = 'https://%s/%s' % (hosts['p%d' % n], pid)
            with open(os.path.join(d, '%s-p%d.txt' % (cid, n)),
                      encoding='utf-8', errors='replace') as f:
                raw = f.read().split('\n')
            title = (raw[0][len('TITLE:'):].strip()
                     if raw and raw[0].startswith('TITLE:') else pid)
            pages.append((pid, title, url, split_sentences('\n'.join(raw[1:]))))
        cls.append((cid, need, pages))
    return cls


def run_arm(arm, binary, clusters, outdir):
    os.makedirs(os.path.join(outdir, arm, 'work'), exist_ok=True)
    state = os.path.join(outdir, arm, 'state')
    os.makedirs(state, exist_ok=True)
    rc, out, err = run_bin([binary, 'teach', GUIDES, state])
    assert rc == 0, ('teach', arm, rc, err[-200:])
    verdicts = {}
    for cid, need, pages in clusters:
        wd = os.path.join(outdir, arm, 'work', cid)
        os.makedirs(wd, exist_ok=True)
        nf = os.path.join(wd, 'need.txt')
        open(nf, 'w').write(need + '\n')
        rc, out, _ = run_bin([binary, 'query', state, nf])
        queries = [l.split('|', 1)[1] for l in out.split('\n') if l.startswith('QUERY|')]
        if rc != 0 or not queries:
            verdicts[cid] = 'ERROR'
            continue
        rf = os.path.join(wd, 'results.txt')
        with open(rf, 'w') as f:
            f.write('Q|' + queries[0] + '\n')
            for pid, title, url, sents in pages:
                f.write('R|%s|%s|%s\n' % (pid, title, sents[0][:160]))
        rc, out, _ = run_bin([binary, 'select', state, rf])
        opens = [l.split('|', 1)[1].split() for l in out.split('\n') if l.startswith('OPEN|')]
        opens = opens[0] if opens else []
        pf = os.path.join(wd, 'pages.txt')
        with open(pf, 'w') as f:
            for pid, title, url, sents in pages:
                if pid not in opens:
                    continue
                f.write('P|%s|%s\nH|%s\n' % (pid, title, host_of(url)))
                for s in sents:
                    f.write('S|%s\n' % s)
        rc, out, _ = run_bin([binary, 'verdict', state, nf, pf, 'FACT', queries[0]])
        uncheck = any(l.startswith('ANSWER|UNCHECKABLE') for l in out.split('\n'))
        answer = [l.split('|', 1)[1] for l in out.split('\n')
                  if l.startswith('ANSWER|') and l != 'ANSWER|UNCHECKABLE']
        provs = []
        for l in out.split('\n'):
            if l.startswith('PROV|1|'):
                p = l.split('|', 2)[2]
                if p not in provs:
                    provs.append(p)
        verdicts[cid] = ('INSTALL|%s' % answer[0][:100] if (not uncheck and answer and len(provs) >= 2)
                         else 'WITHHOLD')
    return verdicts


def main():
    batdir, outdir = sys.argv[1], sys.argv[2]
    clusters = load_battery(batdir)
    print('LOADED|clusters=%d' % len(clusters))
    res = {arm: run_arm(arm, binary, clusters, outdir) for arm, binary in ARMS.items()}
    for cid, _, _ in clusters:
        print('RT|%s|control=%s|d4=%s' % (cid, res['control'][cid], res['d4'][cid]))


if __name__ == '__main__':
    main()
