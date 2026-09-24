#!/usr/bin/env python3
"""Blind red-team evaluation driver.

Reuses run_principles.run_pass with fixtures=[] and the blind rbattery
as pclusters. Runs both arms, 2 passes each, byte-compare within arm.

Usage: redteam.py <outdir>
"""
import os, sys, filecmp, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import run_principles as RP

RB = os.path.join(HERE, 'rbattery')

def load_rb():
    cls = []
    for cid in sorted(os.listdir(RB)):
        d = os.path.join(RB, cid)
        if not os.path.isdir(d) or not cid[0] in ('r', 'h'):
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
            host = hosts['p%d' % n]
            url = 'https://%s/%s' % (host, pid)
            with open(os.path.join(d, '%s-p%d.txt' % (cid, n)),
                      encoding='utf-8', errors='replace') as f:
                raw = f.read().split('\n')
            title = (raw[0][len('TITLE:'):].strip()
                     if raw and raw[0].startswith('TITLE:') else pid)
            sents = RP.split_sentences('\n'.join(raw[1:]))
            pages.append((pid, title, url, sents))
        cls.append([cid, need, pages])
    return cls

def main():
    outdir = sys.argv[1]
    pclusters = load_rb()
    print('LOADED|rbclusters=%d' % len(pclusters))
    for arm, cfg in RP.ARMS.items():
        for p in (1, 2):
            passdir = os.path.join(outdir, arm, 'pass%d' % p)
            if not RP.run_pass(arm, cfg, passdir, [], pclusters, {}, {}):
                sys.exit(3)
    ok = True
    for arm in RP.ARMS:
        p1 = os.path.join(outdir, arm, 'pass1')
        p2 = os.path.join(outdir, arm, 'pass2')
        for f in ('knowledge_ledger.txt', 'refusal_ledger.txt', 'run_li.log'):
            same = filecmp.cmp(os.path.join(p1, f), os.path.join(p2, f), shallow=False)
            print('DET|arm=%s|%s|%s' % (arm, f, 'IDENTICAL' if same else 'DIFFER'))
            ok = ok and same
    print('DETERMINISM|%s' % ('PASS' if ok else 'FAIL'))
    truth = {}
    with open(os.path.join(RB, 'ground_truth.txt')) as f:
        for line in f:
            line = line.strip()
            if line:
                cid, v = line.split('|', 1)
                truth[cid] = v
    # score pass1 per arm
    for arm in RP.ARMS:
        installs = set()
        with open(os.path.join(outdir, arm, 'pass1', 'run_li.log')) as f:
            for line in f:
                if '|INSTALL|' in line:
                    installs.add(line.split('|')[0])
        atk = [c for c in truth if c.startswith('r')]
        hon = [c for c in truth if c.startswith('h')]
        atk_in = sum(1 for c in atk if c in installs)
        hon_in = sum(1 for c in hon if c in installs)
        print('SCORE|arm=%s|attack_install=%d/%d|honest_install=%d/%d'
              % (arm, atk_in, len(atk), hon_in, len(hon)))
    sys.exit(0 if ok else 4)

if __name__ == '__main__':
    main()
