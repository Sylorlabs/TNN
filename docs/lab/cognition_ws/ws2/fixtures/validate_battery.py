#!/usr/bin/env python3
# Build-time validator for the WS2 probe battery (NOT part of the Zag battery).
# Replicates lib.zag tokenize(): lowercase, split on non-alnum.
import re, sys

def toks(s):
    return re.findall(r'[a-z0-9]+', s.lower())

corpus_path, queries_path = sys.argv[1], sys.argv[2]
items = []  # (id, domain, type, subject, text)
with open(corpus_path) as f:
    for ln in f:
        ln = ln.rstrip('\n')
        if not ln or ln.startswith('#'):
            continue
        assert ln.count('|') == 4, f'bad corpus line: {ln}'
        assert '|' not in ln.split('|', 4)[4] or True
        i, d, t, s, x = ln.split('|', 4)
        items.append((i, d, t, s, x))

def hay(it):
    i, d, t, s, x = it
    return set(toks(x + ' ' + s + ' ' + d + ' ' + t))

by_id = {}
for it in items:
    by_id.setdefault(it[0], []).append(it)

queries = []
with open(queries_path) as f:
    for ln in f:
        ln = ln.rstrip('\n')
        if not ln or ln.startswith('#'):
            continue
        assert ln.count('|') == 7, f'bad query line: {ln}'
        q = ln.split('|', 7)
        queries.append(q)

errs = []
# duplicate-id fixture
assert len(by_id.get('PD01', [])) == 2, 'PD01 must appear twice in corpus'

for q in queries:
    qid, split, cls, th, dh, sh, text, gold = q
    qt = set(toks(text))
    if qid.startswith('QN'):
        assert gold == '', f'{qid}: negative probe must have empty gold'
        for it in items:
            ov = qt & hay(it)
            if ov:
                errs.append(f'{qid}: NEG query overlaps item {it[0]}: {sorted(ov)}')
    elif qid.startswith('QP') and qid[2].isdigit():
        it = by_id[gold][0]
        ov = qt & hay(it)
        if ov:
            errs.append(f'{qid}: PARA query overlaps gold {gold}: {sorted(ov)}')
    else:
        # sanity: query must be token-matchable against its gold
        its = by_id.get(gold, [])
        if not its:
            errs.append(f'{qid}: gold {gold} not in corpus')
            continue
        # for QPD01 the installed one is the FIRST line
        it = its[0]
        if qid == 'QPD01':
            # second line's text must be the query target; first line installed
            assert 'second lodestone' in its[1][4], 'QPD01 fixture changed'
            assert 'first lodestone' in its[0][4], 'QPD01 fixture changed'
            continue
        ov = qt & hay(it)
        if not ov:
            errs.append(f'{qid}: query has zero overlap with gold {gold}')
    if qid.startswith('QX1'):
        it = by_id[gold][0]
        if dh == it[1]:
            errs.append(f'{qid}: dhint must mismatch item domain for X1 gate test')

if errs:
    print('VALIDATION FAILED:')
    for e in errs:
        print(' ', e)
    sys.exit(1)
print(f'OK: {len(items)} items ({len(by_id)} ids), {len(queries)} queries; '
      'PARA zero-overlap, NEG zero-overlap-all, X1 dhint-mismatch all hold.')
