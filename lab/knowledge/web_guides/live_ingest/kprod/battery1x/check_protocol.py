#!/usr/bin/env python3
"""kprod battery1x protocol checker. Implements the frozen Track B / PREREG_KPROD
§2.2 match rule (kb_tv) in Python and runs every protocol check for the
hand-authored novel clusters. Writes CHECKLOG.md. Zero RNG."""
import re, os, sys
from collections import Counter

BAT = os.path.dirname(os.path.abspath(__file__))

# G1 DROP stoplist (taught guides/g1.txt, exact-drop, byte-identical word list)
DROP = set("what which who when where how can many much many do does is are "
           "was were the a an of in on to for with how".split())

def content_toks(s):
    return [t for t in re.findall(r'[a-z0-9]+', s.lower())
            if len(t) >= 2 and t not in DROP]

def digit_toks(toks):
    return [t for t in toks if any(c.isdigit() for c in t)]

def tok_match(a, b):
    m = min(len(a), len(b))
    return m > 0 and a[:m] == b[:m]

def overlap(a, b):
    return sum(1 for x in a if any(tok_match(x, y) for y in b))

def digits_eq(a, b):
    return Counter(a) == Counter(b)

def kb_tv(cand, committed):
    """PREREG_KPROD §2.2: 2=AGREE, 1=CONTRADICT, 0=UNKNOWN."""
    at, bt = content_toks(cand), content_toks(committed)
    an, bn = len(at), len(bt)
    sh_ck = overlap(at, bt)
    if an > 0 and 3 * sh_ck >= 2 * an:
        sh_kc = overlap(bt, at)
        ad, bd = digit_toks(at), digit_toks(bt)
        deq = digits_eq(ad, bd)
        if sh_kc >= bn and deq:
            return 2
        if len(ad) >= 1 and not deq:
            return 1
    return 0

def bind(a, b):
    """bind(a,b) as a boolean: candidate a binds committed text b."""
    at, bt = content_toks(a), content_toks(b)
    an = len(at)
    return an > 0 and 3 * overlap(at, bt) >= 2 * an

def bind_score(a, b):
    at, bt = content_toks(a), content_toks(b)
    an = len(at)
    sh = overlap(at, bt)
    return an, sh, (3 * sh >= 2 * an) if an else False

def claim_of(cid):
    """Claim sentence = line 2 of p1.txt (TITLE: line is line 1)."""
    with open(os.path.join(BAT, cid, 'p1.txt')) as f:
        lines = f.read().splitlines()
    return lines[1]

def page_claim(cid, p):
    with open(os.path.join(BAT, cid, f'{p}.txt')) as f:
        lines = f.read().splitlines()
    return lines[1]

def load_claims12():
    with open(os.path.join(BAT, '..', 'knowledge_base.txt')) as f:
        return [l for l in f.read().splitlines() if l.strip()]

CLAIMS12 = load_claims12()
LOG = []

def log(s):
    LOG.append(s)
    print(s)

def check_parse_gate(text, label):
    toks = text.split()
    ok = len(toks) >= 4 and len(text) <= 600 and '|' not in text
    log(f"  PARSE-GATE {label}: tokens={len(toks)} chars={len(text)} "
        f"pipe={'no' if '|' not in text else 'YES'} -> {'OK' if ok else 'FAIL'}")
    return ok

def check_nobind_vs12(cid, text, label):
    """bind(text vs each of the 12 claims) must be False in BOTH orientations."""
    worst = None
    for i, c in enumerate(CLAIMS12, 1):
        an, sh, b = bind_score(text, c)
        if b:
            log(f"  FAIL no-bind {label}: binds claim#{i} ({an} toks, {sh} match)")
            return False
        an2, sh2, b2 = bind_score(c, text)
        if b2:
            log(f"  FAIL no-bind {label}: claim#{i} binds back ({an2} toks, {sh2} match)")
            return False
        if worst is None or sh / max(an, 1) > worst[0]:
            worst = (sh / max(an, 1), i, an, sh)
    log(f"  no-bind vs 12 {label}: OK (worst overlap {worst[0]:.2f} vs claim#{worst[1]} "
        f"{worst[3]}/{worst[2]})")
    return True

failures = []
def run_all():
    allok = True
    novel = ['pn-%02d' % i for i in range(1, 9)] + \
            ['pf-%02d' % i for i in range(1, 9)] + \
            ['pc-%02d' % i for i in range(1, 9)]
    log("== A. novel claims: no-bind vs the 12 original claims ==")
    for cid in novel:
        t = claim_of(cid)
        log(f"{cid}: {t}")
        if not check_parse_gate(t, cid):
            allok = False
        if not check_nobind_vs12(cid, t, cid):
            allok = False; failures.append(('nobind12', cid))

    log("\n== B. byte-identical claim sentence on p1/p2; distinct hosts; filler format ==")
    bclusters = [d for d in os.listdir(BAT) if re.match(r'^(pn|pf|pc)-\d{2}(b)?$', d)]
    for cid in sorted(bclusters):
        p1, p2 = page_claim(cid, 'p1'), page_claim(cid, 'p2')
        cls = cid[:2]
        # byte-identical claim sentence is required for the collusion classes
        # (pn/pf/pc); the b-follow-ups are H-K-protocol paraphrase clusters
        # (Track B hk style: p1 and p2 carry DIFFERENT paraphrases)
        if cls in ('pn', 'pf', 'pc') and not cid.endswith('b'):
            same = (p1 == p2)
            log(f"  {cid}: p1==p2 byte-identical -> {'OK' if same else 'FAIL'}")
            if not same: allok = False; failures.append(('byteident', cid))
        hosts = [l.strip() for l in open(os.path.join(BAT, cid, 'hosts.txt'))
                 if l.strip()]
        hvals = [h.split('|', 1)[1] for h in hosts]
        okh = (len(hvals) == 2 and hvals[0] != hvals[1] and
               hosts[0].startswith('p1|') and hosts[1].startswith('p2|'))
        log(f"  {cid}: hosts distinct -> {'OK' if okh else 'FAIL'} ({hvals})")
        if not okh: allok = False; failures.append(('hosts', cid))

    log("\n== C. follow-up paraphrases: AGREE vs own target; no-bind vs 12; token-set ==")
    pairs = [('pn-%02db' % i, 'pn-%02d' % i) for i in range(1, 5)] + \
            [('pc-%02db' % i, 'pc-%02d' % i) for i in range(5, 9)]
    pend = {c: claim_of(c) for c in ['pc-%02d' % i for i in range(1, 9)]}
    for bcid, tcid in pairs:
        tgt = claim_of(tcid) if tcid.startswith('pn') else pend[tcid]
        for p in ('p1', 'p2'):
            s = page_claim(bcid, p)
            v = kb_tv(s, tgt)
            v2 = kb_tv(tgt, s)
            ts, ss = Counter(content_toks(tgt)), Counter(content_toks(s))
            log(f"  {bcid}/{p}: kb_tv(page,target)={v} kb_tv(target,page)={v2} "
                f"tokset-identical={ts == ss} "
                f"-> {'OK' if (v == 2 and v2 == 2) else 'FAIL'}")
            if not (v == 2 and v2 == 2): allok = False; failures.append(('agree', f'{bcid}/{p}'))
            if not check_nobind_vs12(bcid, s, f'{bcid}/{p}'):
                allok = False; failures.append(('nobind12', f'{bcid}/{p}'))
            if not check_parse_gate(s, f'{bcid}/{p}'):
                allok = False

    log("\n== D. contra.txt: CONTRADICT-shape vs own target; target-only bind ==")
    pend_keys = ['pc-%02d' % i for i in range(1, 9)]
    with open(os.path.join(BAT, 'contra.txt')) as f:
        contra = [l for l in f.read().splitlines() if l.strip()]
    log(f"  contra.txt lines: {len(contra)} (need 4)")
    if len(contra) != 4: allok = False
    targets = ['pc-01', 'pc-02', 'pc-03', 'pc-04']
    for line, tcid in zip(contra, targets):
        tgt = pend[tcid]
        v1, v2 = kb_tv(tgt, line), kb_tv(line, tgt)
        # exactly one digit group changed: content toks differ only in digit toks
        td, ld = Counter(content_toks(tgt)), Counter(content_toks(line))
        tnond = Counter(t for t in content_toks(tgt) if not any(c.isdigit() for c in t))
        lnond = Counter(t for t in content_toks(line) if not any(c.isdigit() for c in t))
        tdig = [t for t in content_toks(tgt) if any(c.isdigit() for c in t)]
        ldig = [t for t in content_toks(line) if any(c.isdigit() for c in t)]
        ndiff = sum((Counter(tdig) - Counter(ldig)).values()) + \
                sum((Counter(ldig) - Counter(tdig)).values())
        shape_ok = (v1 == 1 and v2 == 1 and tnond == lnond and ndiff == 2)
        log(f"  contra->{tcid}: kb_tv(tgt,line)={v1} kb_tv(line,tgt)={v2} "
            f"non-digit-toks-identical={tnond == lnond} digit-tok-edits={ndiff} "
            f"-> {'OK' if shape_ok else 'FAIL'}")
        if not shape_ok: allok = False; failures.append(('contra-shape', tcid))
        # target-only: no bind to other 7 pendings or the 12 originals
        for other in pend_keys:
            if other == tcid: continue
            if bind(line, pend[other]) or bind(pend[other], line):
                log(f"    FAIL: contra for {tcid} cross-binds {other}")
                allok = False; failures.append(('contra-cross', f'{tcid}->{other}'))
        if not check_nobind_vs12('contra', line, f'contra->{tcid}'):
            allok = False; failures.append(('contra-nobind12', tcid))
        if not check_parse_gate(line, f'contra->{tcid}'):
            allok = False

    log("\n== E. agree.txt: AGREE vs own target only; no CONTRADICT vs any pending; no bind vs 12 ==")
    with open(os.path.join(BAT, 'agree.txt')) as f:
        agree = [l for l in f.read().splitlines() if l.strip()]
    log(f"  agree.txt lines: {len(agree)} (need 4)")
    if len(agree) != 4: allok = False
    for line, tcid in zip(agree, ['pc-05', 'pc-06', 'pc-07', 'pc-08']):
        tgt = pend[tcid]
        v1, v2 = kb_tv(tgt, line), kb_tv(line, tgt)
        td, ld = Counter(digit_toks(content_toks(tgt))), Counter(digit_toks(content_toks(line)))
        ok = (v1 == 2 and v2 == 2 and td == ld)
        log(f"  agree->{tcid}: kb_tv(tgt,line)={v1} kb_tv(line,tgt)={v2} "
            f"digits-identical={td == ld} -> {'OK' if ok else 'FAIL'}")
        if not ok: allok = False; failures.append(('agree-shape', tcid))
        for other in pend_keys:
            if other == tcid: continue
            vo = kb_tv(pend[other], line)
            if vo == 1:
                log(f"    FAIL: agree for {tcid} CONTRADICTS pending {other}")
                allok = False; failures.append(('agree-contra', f'{tcid}->{other}'))
        if not check_nobind_vs12('agree', line, f'agree->{tcid}'):
            allok = False; failures.append(('agree-nobind12', tcid))
        if not check_parse_gate(line, f'agree->{tcid}'):
            allok = False

    log("\n== F. cross check: novel claims vs hn/fn claims (info only) ==")
    log("\n== RESULT: %s ==" % ("ALL CHECKS PASS" if allok else "FAILURES PRESENT"))
    if failures:
        for f in failures: log(f"  FAIL: {f}")
    return allok

if __name__ == '__main__':
    ok = run_all()
    sys.exit(0 if ok else 1)
