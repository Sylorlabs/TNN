#!/usr/bin/env python3
"""Independent strict-§2 reference for operative-utterance understanding.
Derived directly from ~/workspace/onebrain_corrreader/PREREG.md §2 (frozen).
Returns per-token operative statuses: 0 non-trigger, 1 operative, 2 quoted,
3 reported, 4 hypothetical, 5 negated, 6 hedged, 7 no-pattern.
"""
import sys

TRIGGERS = {"no", "actually", "meant", "correction"}
SPEECHVERBS = {"say","said","says","saying","tell","told","tells","telling",
  "write","wrote","writes","writing","claim","claimed","claims","claiming",
  "state","stated","states","think","thought","thinks","thinking",
  "believe","believes","mention","mentioned","mentions","report","reported",
  "reports","ask","asked","asks","asking"}
THIRDSUBJ = {"he","she","they","him","her","them","his","their","friend",
  "friends","mother","father","brother","sister","man","woman","guy","person",
  "people","teacher","doctor","boss","neighbor","john","mary","dad","mom",
  "buddy","colleague","wife","husband","son","daughter"}
CONDS = {"if","suppose","supposing","whether","unless","assuming","provided"}
NEGS = {"never","not","nobody","none","hardly","scarcely","barely","didn",
  "don","doesn","isn","aren","wasn","weren","haven","hasn","hadn","won",
  "wouldn","couldn","shouldn","mustn","needn","daren","no"}
NEGSTEMS = {"can","don","didn","doesn","isn","aren","wasn","weren","haven",
  "hasn","hadn","won","wouldn","couldn","shouldn","mustn","needn","daren","ain"}
HEDGES = {"maybe","perhaps","might","possibly","could","probably",
  "presumably","apparently","seems","seem"}
HEDGEVERBS = {"think","guess","believe","suppose"}
ARTICLES = {"a","the","my","this","that"}
DISCOURSE = {"well","oh","uh","um","ah","okay","ok","right","so"}

def isal(c):
    return ('0' <= c <= '9') or ('a' <= c <= 'z') or ('A' <= c <= 'Z')

def tokenize(q):
    # UNCAPPED: ou_operative's internal clause/sentence scans (ou_ntok /
    # ou_tok_at) are byte-based and see past token 96. The 96-cap applies
    # only to which tokens ou_annotate visits (the qtok table + ann array).
    toks = []
    i, n = 0, len(q)
    while i < n:
        while i < n and not isal(q[i]):
            i += 1
        if i < n:
            s = i
            while i < n and isal(q[i]):
                i += 1
            toks.append((s, i))  # (off, end)
    return toks

def tok_text(q, t):
    return q[t[0]:t[1]]

def in_quotes(q, off):
    dq = sq = False
    for i in range(off):
        c = q[i]
        if c == '"':
            dq = not dq
        elif c == "'":
            pa = i > 0 and isal(q[i-1])
            na = i + 1 < len(q) and isal(q[i+1])
            if not (pa and na):
                sq = not sq
    return dq or sq

def clause_bounds(q, off, ln):
    cs, ce = 0, len(q)
    i = off - 1
    while i >= 0:
        if q[i] in ';?!.\n':
            cs = i + 1
            break
        i -= 1
    j = off + ln
    while j < len(q):
        if q[j] in ';?!.\n':
            ce = j
            break
        j += 1
    return cs, ce

def sent_bounds(q, off, ln):
    ss, se = 0, len(q)
    i = off - 1
    while i >= 0:
        if q[i] in ';?!.':
            ss = i + 1
            break
        i -= 1
    j = off + ln
    while j < len(q):
        if q[j] in ';?!.':
            se = j
            break
        j += 1
    return ss, se

def toks_in(q, s, e):
    return [t for t in tokenize(q) if t[0] >= s and t[1] <= e]

def ou_operative(q, off, ln):
    w = tok_text(q, (off, off + ln))
    if w not in TRIGGERS:
        return 0
    # R1
    if in_quotes(q, off):
        return 2
    # R2
    cs, ce = clause_bounds(q, off, ln)
    ctoks = toks_in(q, cs, ce)
    ti = next(i for i, t in enumerate(ctoks) if t[0] == off)
    n = len(ctoks)
    ss, se = sent_bounds(q, off, ln)
    stoks = toks_in(q, ss, se)
    ts = next(i for i, t in enumerate(stoks) if t[0] == off)
    is_no, is_act, is_meant, is_corr = (w == "no", w == "actually",
                                       w == "meant", w == "correction")
    blocked = 0
    # R3 reported
    for v in range(ts):
        if blocked:
            break
        vw = tok_text(q, stoks[v])
        if vw in SPEECHVERBS:
            for s in range(max(0, v - 3), v):
                if tok_text(q, stoks[s]) in THIRDSUBJ:
                    blocked = 3
                    break
        if not blocked and vw == "according":
            for x in range(v + 1, min(v + 3, len(stoks))):
                if tok_text(q, stoks[x]) == "to":
                    blocked = 3
                    break
    # R4 hypothetical
    if not blocked:
        for h in range(ts):
            if tok_text(q, stoks[h]) in CONDS:
                blocked = 4
                break
    # R5 negated
    if not blocked and is_meant:
        for g in range(max(0, ti - 3), ti):
            gw = tok_text(q, ctoks[g])
            if gw in NEGS:
                skip = False
                if gw == "no":
                    if g == 0:
                        skip = True
                    elif g + 1 < n and tok_text(q, ctoks[g + 1]) in ("i", "we"):
                        skip = True
                if not skip:
                    blocked = 5
                    break
            if not blocked and gw == "t" and g - 1 >= 0:
                if tok_text(q, ctoks[g - 1]) in NEGSTEMS:
                    blocked = 5
                    break
    # R6 hedged
    if not blocked:
        for e in range(max(0, ti - 4), ti):
            ew = tok_text(q, ctoks[e])
            if ew in HEDGES:
                blocked = 6
                break
            if ew == "i" and e + 1 < n and \
               tok_text(q, ctoks[e + 1]) in HEDGEVERBS:
                blocked = 6
                break
    if blocked:
        return blocked  # 3..6
    # R7 positive patterns
    if is_no:
        if all(tok_text(q, ctoks[p]) in DISCOURSE for p in range(ti)):
            lim = min(ti + 4, n - 1)
            for m in range(ti + 1, lim + 1):
                mw = tok_text(q, ctoks[m])
                if mw in ("i", "we") and m + 1 <= ti + 4 and m + 1 < n and \
                   tok_text(q, ctoks[m + 1]) in ("mean", "meant"):
                    return 1
                if mw == "correction":
                    return 1
    if is_act:
        has_iwe = has_vm = False
        for m2 in range(max(0, ti - 3), min(ti + 3, n - 1) + 1):
            if m2 == ti:
                continue
            mw = tok_text(q, ctoks[m2])
            if mw in ("i", "we"):
                has_iwe = True
            if mw in ("mean", "meant"):
                has_vm = True
        if has_iwe and has_vm:
            return 1
    if is_meant:
        for m3 in range(max(0, ti - 3), ti):
            if tok_text(q, ctoks[m3]) in ("i", "we"):
                return 1
    if is_corr:
        if ti == 0:
            return 1
        if tok_text(q, ctoks[ti - 1]) in ARTICLES:
            nb = q[off + ln] if off + ln < ce else ""
            if nb == ":" or nb == ",":
                return 1
            elif ti == n - 1:
                return 1
    return 7

def annotate(q):
    q = q.lower()
    toks = tokenize(q)
    # the probe/core only annotates the first 96 tokens (qtok cap)
    return ([ou_operative(q, s, e - s) for (s, e) in toks[:96]],
            [q[s:e] for (s, e) in toks[:96]])

if __name__ == "__main__":
    q = sys.argv[1]
    sts, toks = annotate(q)
    for j, (t, s) in enumerate(zip(toks, sts)):
        print(f"{j}: '{t}' st={s}")
