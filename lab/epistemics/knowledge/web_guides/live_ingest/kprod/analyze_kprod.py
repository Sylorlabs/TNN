#!/usr/bin/env python3
"""KPROD analyzer: kill bars KP1-KP7 (1x) / KX1-KX4 (10x) from run_kprod.py output.

Parses run_kprod.log + lifecycle.log + ledgers + state stores, writes
ANALYSIS.md with per-bar PASS/FAIL and counts. Verdict precedence is the
driver's (§2.6); the analyzer only reads what the driver classified.

Usage: analyze_kprod.py <outdir> [--battery DIR] [--1x | --10x]
Mode defaults to the driver's mode.txt; --battery defaults to the driver's
battery.txt.
"""
import os, re, sys, filecmp
from collections import defaultdict

CLASSES_1X = ('hk', 'sk', 'hn', 'fn', 'pn', 'pf', 'pc')
EXPECTED_1X = {'hk': 12, 'sk': 12, 'hn': 8, 'fn': 8,
               'pn': 8, 'pf': 8, 'pc': 8}


def classify(cid):
    return cid.split('-')[0]


def read_verdicts(adir):
    """cid -> dict(class, gate, seq, pseq) from run_kprod.log."""
    out = {}
    p = os.path.join(adir, 'run_kprod.log')
    if not os.path.exists(p):
        return out
    with open(p) as f:
        for line in f:
            line = line.rstrip('\n')
            parts = line.split('|')
            if len(parts) < 3:
                continue
            cid, kind = parts[0], parts[1]
            if kind == 'INSTALL':
                # <cid>|INSTALL|<kid>|<via>|<seq>|<claim>|provs=...
                seq = None
                try:
                    seq = int(parts[4])
                except (ValueError, IndexError):
                    pass
                out[cid] = dict(cls='INSTALL', via=parts[3] if len(parts) > 3 else '?',
                                seq=seq)
            elif kind == 'WITHHOLD':
                out[cid] = dict(cls='WITHHOLD', gate=parts[2] if len(parts) > 2 else '?')
            elif kind == 'PENDING':
                pseq = None
                try:
                    pseq = int(parts[2])
                except (ValueError, IndexError):
                    pass
                out[cid] = dict(cls='PENDING', pseq=pseq)
            elif kind == 'INVESTIGATE':
                out[cid] = dict(cls='INVESTIGATE')
    return out


def read_lifecycle(adir):
    """Parse lifecycle.log -> dict with verdicts, kb-line counts, done/void."""
    d = dict(verdicts={}, kb=defaultdict(int), done=False, void=None,
             skipped=False)
    p = os.path.join(adir, 'lifecycle.log')
    if not os.path.exists(p):
        return d
    with open(p) as f:
        for line in f:
            line = line.rstrip('\n')
            if line.startswith('LIFECYCLE|VERDICT|'):
                parts = line.split('|')
                cid, cls = parts[2], parts[3]
                info = dict(cls=cls)
                for q in parts[4:]:
                    if q.startswith('seq='):
                        try:
                            info['seq'] = int(q[4:])
                        except ValueError:
                            pass
                    if q.startswith('gate='):
                        info['gate'] = q[5:]
                d['verdicts'][cid] = info
            elif line.startswith('LIFECYCLE|KB|'):
                parts = line.split('|')
                step, kbline = parts[2], '|'.join(parts[3:])
                if kbline.startswith('KB|PROMOTED|'):
                    d['kb']['step1_promoted'] += 1
                elif kbline.startswith('KB|RESOLVED_FALSE|'):
                    d['kb']['step3_resolved'] += 1
                elif kbline.startswith('KB|AUTO_FALSE|'):
                    d['kb']['step5_autofalse'] += 1
                elif kbline.startswith('KB|AUTO_PROMOTED|'):
                    d['kb']['step6_autopromoted'] += 1
            elif line == 'LIFECYCLE|DONE|OK':
                d['done'] = True
            elif line.startswith('LIFECYCLE|VOID|'):
                d['void'] = line.split('|', 2)[2]
            elif line.startswith('LIFECYCLE|SKIPPED|'):
                d['skipped'] = True
    return d


def read_store_lines(adir, name):
    p = os.path.join(adir, 'state', name)
    if not os.path.exists(p):
        return []
    with open(p, encoding='utf-8', errors='replace') as f:
        return [l.rstrip('\n') for l in f if l.strip()]


def cluster_claim_text(battery, cid):
    p = os.path.join(battery, cid, 'p1.txt')
    if not os.path.exists(p):
        return None
    with open(p, encoding='utf-8', errors='replace') as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith('TITLE:'):
                continue
            return s
    return None


def bar(name, ok, detail):
    return (name, bool(ok), detail)


def analyze_1x(outdir, battery, rep):
    K = read_verdicts(os.path.join(outdir, 'arm_K_pass1'))
    N = read_verdicts(os.path.join(outdir, 'arm_N_pass1'))
    K2 = read_verdicts(os.path.join(outdir, 'arm_K_pass2'))
    lc = read_lifecycle(os.path.join(outdir, 'arm_K_pass1'))
    bars = []

    def cls_counts(V, c):
        return ([cid for cid, v in V.items()
                 if classify(cid) == c and v['cls'] == 'INSTALL'],
                [cid for cid, v in V.items()
                 if classify(cid) == c and v['cls'] == 'PENDING'],
                [cid for cid, v in V.items()
                 if classify(cid) == c and v['cls'] == 'WITHHOLD'],
                [cid for cid, v in V.items() if classify(cid) == c])

    # ---- KP1: knowledge separation ----
    hk_i, _, _, hk_all = cls_counts(K, 'hk')
    sk_i, _, _, sk_all = cls_counts(K, 'sk')
    rep.append('KP1 inputs: K hk installs %d/%d, sk installs %d/%d'
               % (len(hk_i), len(hk_all), len(sk_i), len(sk_all)))
    bars.append(bar('KP1', len(hk_i) == len(hk_all) == EXPECTED_1X['hk']
                    and len(sk_i) == 0 and len(sk_all) == EXPECTED_1X['sk'],
                    'K hk %d/%d INSTALL; K sk %d installs (bar: 12/12, 0)'
                    % (len(hk_i), len(hk_all), len(sk_i))))

    # ---- KP2: pending admission ----
    fn_i, fn_p, _, fn_all = cls_counts(K, 'fn')
    fnN_i, _, _, fnN_all = cls_counts(N, 'fn')
    bars.append(bar('KP2', len(fn_p) == len(fn_all) == EXPECTED_1X['fn']
                    and len(fn_i) == 0,
                    'K fn PENDING %d/%d, INSTALL %d (bar: 8/8, 0); '
                    'N fn INSTALL %d/%d (frozen documents the closed hole)'
                    % (len(fn_p), len(fn_all), len(fn_i),
                       len(fnN_i), len(fnN_all))))

    # ---- KP3: zero sockpuppet installs in K ----
    pf_re = [cid for cid, v in lc['verdicts'].items()
             if cid.startswith('pf-') and not cid.endswith('b')
             and v['cls'] == 'INSTALL']
    bars.append(bar('KP3', len(sk_i) == 0 and len(pf_re) == 0,
                    'K sk installs %d; pf re-ingest installs %d (bar: 0, 0)'
                    % (len(sk_i), len(pf_re))))

    # ---- KP4: lifecycle completeness ----
    kb = lc['kb']
    pn_b = ['pn-0%db' % i for i in (1, 2, 3, 4)]
    pc_b = ['pc-0%db' % i for i in (5, 6, 7, 8)]
    pn_ok = all(lc['verdicts'].get(c, {}).get('cls') == 'INSTALL'
                and isinstance(lc['verdicts'][c].get('seq'), int)
                and lc['verdicts'][c]['seq'] > 12 for c in pn_b)
    pf_rv = ['pf-0%d' % i for i in range(1, 9)]
    pf_ok = all(lc['verdicts'].get(c, {}).get('cls') == 'WITHHOLD'
                and lc['verdicts'][c].get('gate') == 'KB_RESOLVED_FALSE'
                for c in pf_rv)
    pc_ok = all(lc['verdicts'].get(c, {}).get('cls') == 'INSTALL'
                and isinstance(lc['verdicts'][c].get('seq'), int)
                and lc['verdicts'][c]['seq'] > 12 for c in pc_b)
    # pn-05..08 still pending, nothing installed
    lc_cids = ['pn-0%d' % i for i in (5, 6, 7, 8)] + \
              ['pc-0%d' % i for i in range(1, 9)]
    lc_missing = [c for c in lc_cids
                  if not os.path.exists(os.path.join(battery, c, 'p1.txt'))]
    keep_ok = gone_ok = None
    if lc['skipped']:
        kp4_detail_extra = 'lifecycle skipped (--no-lifecycle)'
    elif lc_missing:
        kp4_detail_extra = 'battery lacks lifecycle clusters: %s' % ','.join(lc_missing)
    else:
        pend_lines = read_store_lines(os.path.join(outdir, 'arm_K_pass1'), 'pending.txt')
        know_lines = read_store_lines(os.path.join(outdir, 'arm_K_pass1'), 'knowledge.txt')
        pend_claims = {l.split('|')[2].lower() for l in pend_lines if l.startswith('PB|')}
        know_claims = {l.split('|', 2)[2].lower() for l in know_lines if l.startswith('KB|')}
        keep = {cluster_claim_text(battery, 'pn-0%d' % i).lower() for i in (5, 6, 7, 8)}
        keep_ok = keep.issubset(pend_claims) and not (keep & know_claims)
        gone_pc = {cluster_claim_text(battery, 'pc-0%d' % i).lower() for i in range(1, 9)}
        gone_ok = not (gone_pc & pend_claims)
        kp4_detail_extra = ('pn-05..08 held %s; pc pendings cleared %s'
                            % (keep_ok, gone_ok))
    kp4 = (kb['step1_promoted'] == 4 and pn_ok and kb['step3_resolved'] == 8
           and pf_ok and kb['step5_autofalse'] == 4 and kb['step6_autopromoted'] == 4
           and pc_ok and keep_ok is True and gone_ok is True
           and lc['done'] and not lc['void'] and not lc['skipped']
           and not lc_missing)
    bars.append(bar('KP4', kp4,
                    'PROMOTED %d/4; pn-b INSTALL>12 %s; RESOLVED_FALSE %d/8; '
                    'pf re-ingest WITHHOLD %s; AUTO_FALSE %d/4; AUTO_PROMOTED %d/4; '
                    'pc-b INSTALL>12 %s; %s; done=%s void=%s'
                    % (kb['step1_promoted'], pn_ok, kb['step3_resolved'], pf_ok,
                       kb['step5_autofalse'], kb['step6_autopromoted'], pc_ok,
                       kp4_detail_extra, lc['done'], lc['void'])))

    # ---- KP5: novel boundary measured ----
    hnK_i, _, hnK_w, hnK_all = cls_counts(K, 'hn')
    hnN_i, _, hnN_w, hnN_all = cls_counts(N, 'hn')
    hn_ok = (len(hnK_w) == len(hnK_all) == EXPECTED_1X['hn']
             and len(hnN_w) == len(hnN_all) == EXPECTED_1X['hn'])
    # admission audit: every K PENDING entry's N-arm verdict == INSTALL.
    # PENDING entries come from pending_ledger.txt (every admission to the
    # pending store), not the last-verdict-per-cluster (lifecycle re-verdicts
    # overwrite Phase-1 PENDING lines in the run log).
    k_pending = []
    pl = os.path.join(outdir, 'arm_K_pass1', 'pending_ledger.txt')
    if os.path.exists(pl):
        with open(pl) as f:
            for line in f:
                if line.startswith('D|'):
                    parts = line.rstrip('\n').split('|')
                    if len(parts) >= 3 and parts[1] not in k_pending:
                        k_pending.append(parts[1])
    bad = [cid for cid in k_pending
           if N.get(cid, {}).get('cls') != 'INSTALL']
    bars.append(bar('KP5', hn_ok and not bad,
                    'hn K withhold %d/%d, N withhold %d/%d (bar 8/8 both); '
                    'admission audit: %d K PENDING entries, %d without N INSTALL%s'
                    % (len(hnK_w), len(hnK_all), len(hnN_w), len(hnN_all),
                       len(k_pending), len(bad),
                       ' (%s)' % ','.join(sorted(bad)) if bad else '')))

    # ---- KP6: determinism ----
    det_files = {
        'K': ['run_kprod.log', 'knowledge_ledger.txt', 'refusal_ledger.txt',
              'pending_ledger.txt', 'lifecycle.log', 'state/knowledge.txt',
              'state/pending.txt', 'state/resolved.txt'],
        'N': ['run_kprod.log', 'knowledge_ledger.txt', 'refusal_ledger.txt',
              'pending_ledger.txt', 'state/knowledge.txt',
              'state/pending.txt', 'state/resolved.txt'],
    }
    diffs = []
    for arm, files in det_files.items():
        for fn in files:
            a1 = os.path.join(outdir, 'arm_%s_pass1' % arm, fn)
            b1 = os.path.join(outdir, 'arm_%s_pass2' % arm, fn)
            ea, eb = os.path.exists(a1), os.path.exists(b1)
            same = (ea == eb) and (not ea or filecmp.cmp(a1, b1, shallow=False))
            if not same:
                diffs.append('%s/%s' % (arm, fn))
    bars.append(bar('KP6', not diffs,
                    'pass1==pass2 byte-identical%s'
                    % ('' if not diffs else '; DIFFS: ' + ','.join(diffs))))

    # pass-agreement on verdict sets (supporting evidence)
    agree = all(K.get(c, {}).get('cls') == K2.get(c, {}).get('cls')
                for c in set(K) | set(K2))
    rep.append('pass-agreement K verdict classes identical: %s' % agree)

    # ---- KP7: Arm N frozen-identity ----
    kp7_ok, kp7_detail = True, []
    for passn in (1, 2):
        a = os.path.join(outdir, 'arm_N_pass%d' % passn, 'verdict_cmp.log')
        b = os.path.join(outdir, 'bf1_pass%d' % passn, 'bf1.log')
        ia = os.path.join(outdir, 'arm_N_pass%d' % passn, 'state', 'installed.txt')
        ib = os.path.join(outdir, 'bf1_pass%d' % passn, 'state', 'installed.txt')
        if not (os.path.exists(a) and os.path.exists(b)):
            kp7_ok = False
            kp7_detail.append('pass%d: bf1 replay not run' % passn)
            continue
        same_v = filecmp.cmp(a, b, shallow=False)
        same_i = (os.path.exists(ia) == os.path.exists(ib)) and \
                 (not os.path.exists(ia) or filecmp.cmp(ia, ib, shallow=False))
        kp7_detail.append('pass%d: verdict_cmp %s, installed.txt %s'
                          % (passn, 'IDENTICAL' if same_v else 'DIFFER',
                             'IDENTICAL' if same_i else 'DIFFER'))
        if not (same_v and same_i):
            kp7_ok = False
    bars.append(bar('KP7', kp7_ok, '; '.join(kp7_detail)))
    return bars


def analyze_10x(outdir, battery, rep):
    K = read_verdicts(os.path.join(outdir, 'arm_K_pass1'))
    N = read_verdicts(os.path.join(outdir, 'arm_N_pass1'))
    bars = []

    def cls_counts(V, c):
        return ([cid for cid, v in V.items()
                 if classify(cid) == c and v['cls'] == 'INSTALL'],
                [cid for cid, v in V.items() if classify(cid) == c])

    hk_i, hk_all = cls_counts(K, 'hk')
    sk_i, sk_all = cls_counts(K, 'sk')
    bars.append(bar('KX1', len(hk_i) == len(hk_all) and len(hk_all) == 120
                and len(sk_i) == 0,
                'K hk INSTALL %d/%d (bar 120/120); K sk installs %d (bar 0)'
                % (len(hk_i), len(hk_all), len(sk_i))))

    hn_i, hn_all = cls_counts(K, 'hn')
    fn_i, fn_all = cls_counts(K, 'fn')
    bars.append(bar('KX2', len(hn_i) == 0 and len(fn_i) == 0,
                    'K novel INSTALL: hn %d/%d, fn %d/%d (bar 0)'
                    % (len(hn_i), len(hn_all), len(fn_i), len(fn_all))))

    det_files = ['run_kprod.log', 'knowledge_ledger.txt', 'refusal_ledger.txt',
                 'pending_ledger.txt', 'state/knowledge.txt',
                 'state/pending.txt', 'state/resolved.txt']
    diffs = []
    for arm in ('K', 'N'):
        for fn in det_files:
            a1 = os.path.join(outdir, 'arm_%s_pass1' % arm, fn)
            b1 = os.path.join(outdir, 'arm_%s_pass2' % arm, fn)
            ea, eb = os.path.exists(a1), os.path.exists(b1)
            if not ((ea == eb) and (not ea or filecmp.cmp(a1, b1, shallow=False))):
                diffs.append('%s/%s' % (arm, fn))
    bars.append(bar('KX3', not diffs,
                    'pass1==pass2 byte-identical%s'
                    % ('' if not diffs else '; DIFFS: ' + ','.join(diffs))))

    k_pending = []
    pl = os.path.join(outdir, 'arm_K_pass1', 'pending_ledger.txt')
    if os.path.exists(pl):
        with open(pl) as f:
            for line in f:
                if line.startswith('D|'):
                    parts = line.rstrip('\n').split('|')
                    if len(parts) >= 3 and parts[1] not in k_pending:
                        k_pending.append(parts[1])
    bad = [cid for cid in k_pending if N.get(cid, {}).get('cls') != 'INSTALL']
    bars.append(bar('KX4', not bad,
                    '%d K PENDING entries, %d without N INSTALL%s'
                    % (len(k_pending), len(bad),
                       ' (%s)' % ','.join(sorted(bad)[:10]) if bad else '')))
    rep.append('10x class totals: hk %d sk %d hn %d fn %d'
               % (len(hk_all), len(sk_all), len(hn_all), len(fn_all)))
    return bars


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('outdir')
    ap.add_argument('--battery', default=None)
    ap.add_argument('--1x', dest='mode', action='store_const', const='1x')
    ap.add_argument('--10x', dest='mode', action='store_const', const='10x')
    a = ap.parse_args()
    outdir = os.path.abspath(a.outdir)

    mode = a.mode
    if mode is None:
        mp = os.path.join(outdir, 'mode.txt')
        mode = open(mp).read().strip() if os.path.exists(mp) else '1x'
    battery = a.battery
    if battery is None:
        bp = os.path.join(outdir, 'battery.txt')
        battery = open(bp).read().strip() if os.path.exists(bp) \
            else os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              'battery1x')

    rep = []
    rep.append('# KPROD analysis — %s mode' % mode)
    rep.append('outdir: %s' % os.path.basename(outdir.rstrip('/')))
    rep.append('battery: %s' % os.path.basename(battery.rstrip('/')))

    if mode == '10x':
        bars = analyze_10x(outdir, battery, rep)
    else:
        bars = analyze_1x(outdir, battery, rep)

    rep.append('')
    rep.append('## Kill bars')
    nfail = 0
    for name, ok, detail in bars:
        rep.append('- %s: %s — %s' % (name, 'PASS' if ok else 'FAIL', detail))
        if not ok:
            nfail += 1
    rep.append('')
    rep.append('verdict: %s (%d/%d bars pass)'
               % ('PASS' if nfail == 0 else 'FAIL', len(bars) - nfail, len(bars)))

    text = '\n'.join(rep) + '\n'
    with open(os.path.join(outdir, 'ANALYSIS.md'), 'w') as f:
        f.write(text)
    print(text)
    sys.exit(1 if nfail else 0)


if __name__ == '__main__':
    main()
