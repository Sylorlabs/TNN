#!/usr/bin/env python3
# Independent Python twin of delib_vol.zag's learning + decision logic.
# Used to (a) verify the Zag engine behaviorally, (b) expose internals
# (scores, distinctiveness) the binary doesn't print.
# Feature extraction mirrors xfeat exactly:
#   unigrams len>=3, adjacent bigrams (words len>=1, joined by _),
#   first_<w>, qmark, exclam. Per-utterance dedup.
import re, sys

def xfeat(low):
    feats = []
    seen = set()
    def add(s):
        if s not in seen:
            seen.add(s); feats.append(s)
    words = re.findall(r"[a-z]+", low)
    prev = None
    for i, w in enumerate(words):
        if len(w) >= 3: add(w)
        if prev is not None: add(prev + "_" + w)
        if i == 0: add("first_" + w)
        prev = w
    if "?" in low: add("qmark")
    if "!" in low: add("exclam")
    return feats

CONCEPTS = ['sarcasm','hypothetical','counterfactual','analogy','poetry','implicature','joke']

def load_tables(workdir, rung, mode, swap=False):
    # returns (tables, nc): tables[c] = {feature: count}, nc[c] = n examples
    tables, nc = [], []
    for ci, c in enumerate(CONCEPTS):
        if mode == 'sarconly' and ci != 0:
            tables.append({}); nc.append(0); continue
        lines = [l.rstrip('\n') for l in open(f"{workdir}/examples/ex_{c}.txt") if l.strip()]
        take = min(rung, len(lines))
        sel = lines[:take]
        if swap: sel = sel[::-1]
        t = {}
        for utt in sel:
            for f in xfeat(utt.lower()):
                t[f] = t.get(f, 0) + 1
        tables.append(t); nc.append(take)
    return tables, nc

def concept_hit(low, tables, nc, detail=False):
    feats = xfeat(low)
    ncon = len(CONCEPTS)
    for c in range(ncon):
        if nc[c] == 0: continue
        score, bestd, matched = 0, 0, []
        for f in feats:
            dfc = tables[c].get(f, 0)
            if dfc:
                dfo = sum(tables[q].get(f, 0) for q in range(ncon) if q != c)
                prev = (1000 * dfc) // nc[c]
                disc = (1000 * dfc) // (dfc + dfo)
                w = (prev * disc) // 1000
                score += w
                if disc > bestd: bestd = disc
                matched.append((f, dfc, dfo, prev, disc, w))
        if score >= 500 and bestd >= 750:
            if detail: return True, c, score, bestd, matched
            return True
    if detail: return False, -1, 0, 0, []
    return False

def predict_file(workdir, rung, mode, items_path, swap=False):
    tables, nc = load_tables(workdir, rung, mode, swap)
    out = []
    for line in open(items_path):
        line = line.rstrip('\n')
        if not line or '|' not in line: continue
        iid, utt = line.split('|', 1)
        out.append((iid, 'WITHHOLD' if concept_hit(utt.lower(), tables, nc) else 'ENDORSE'))
    return out

if __name__ == '__main__':
    # usage: twin.py <workdir> <rung> <mode> <items> ; prints ID|VERDICT lines
    wd, rung, mode, items = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
    for iid, v in predict_file(wd, rung, mode, items):
        print(f"{iid}|{v}")
