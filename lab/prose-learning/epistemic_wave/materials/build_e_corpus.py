#!/usr/bin/env python3
"""Deterministic builder for epistemic-wave leg-(e) shakedown corpus grades 1-3.

Source: frozen championship train_grok.jsonl (12 planted false ids excluded,
title-less degenerate pubyear items excluded). Facts deduped by (category,
entity) — the championship repeats some facts (e.g. the alphabet block).
No RNG. Output files are frozen with the prereg; sha256 checksums recorded
in PREREG.md §11. NOTE: superseded for scored runs by the Gutenberg corpus
(§8.1); kept for harness shakedown only.
"""
import json, re, os

HERE = os.path.dirname(os.path.abspath(__file__))
TRAIN = '/home/hatch/workspace/tnn-lab/prose-learning/inputs/train_grok.jsonl'
FALSE_IDS = {3, 29, 55, 71, 80, 103, 117, 139, 163, 178, 205, 231}

def parse(sent):
    m = re.match(r'^The alphabet position of ([A-Z]) is (\d+)\.$', sent)
    if m: return ('alpha', m.group(1), int(m.group(2)),
                  f'What is the English alphabetic position of the letter {m.group(1)}?')
    m = re.match(r'^([A-Z]) has alphabet position (\d+)\.$', sent)
    if m: return ('alpha', m.group(1), int(m.group(2)),
                  f'What is the English alphabetic position of the letter {m.group(1)}?')
    m = re.match(r'^The letter count of (\S+) is (\d+)\.$', sent)
    if m: return ('wordlen', m.group(1), int(m.group(2)),
                  f'What is the length of the word "{m.group(1)}"?')
    m = re.match(r'^The publication year of (.+) is (\d+)\.$', sent)
    if m and m.group(1).strip():
        return ('pubyear', m.group(1), int(m.group(2)),
                f'In what year was {m.group(1)} published?')
    m = re.match(r'^The count of (.+) is (\d+)\.$', sent)
    if m: return ('open', m.group(1), int(m.group(2)),
                  f'How many {m.group(1)} are there?')
    return None

facts = []
for line in open(TRAIN):
    for r in json.loads(line):
        if r['id'] in FALSE_IDS:
            continue
        p = parse(r['sentence'])
        if p is None:
            continue
        facts.append({'fid': r['id'], 'cat': p[0], 'entity': p[1],
                      'value': p[2], 'probe': p[3], 'sentence': r['sentence']})
facts.sort(key=lambda f: f['fid'])
uniq, seen = [], set()
for f in facts:
    k = (f['cat'], f['entity'])
    if k not in seen:
        seen.add(k)
        uniq.append(f)
assert len(uniq) == 185, len(uniq)

ALT = {
    'alpha':   lambda e, v: f'The letter {e} sits at alphabet position {v}.',
    'wordlen': lambda e, v: f'The word "{e}" has {v} letters.',
    'pubyear': lambda e, v: f'{e} was published in {v}.',
    'open':    lambda e, v: f'There are {v} {e}.',
}
ALT2 = {
    'alpha':   lambda e, v: f'In the alphabet, {e} is number {v}.',
    'wordlen': lambda e, v: f'"{e}" is {v} letters long.',
    'pubyear': lambda e, v: f'The year {e} came out was {v}.',
    'open':    lambda e, v: f'{e}: {v} in total.',
}

def hedge(cat, entity, value):
    if cat == 'alpha':
        return f'The letter {entity} is probably at alphabet position {value}.'
    if cat == 'wordlen':
        return f'The word "{entity}" probably has {value} letters.'
    if cat == 'pubyear':
        return f'{entity} was probably published in {value}.'
    return f'There are probably {value} {entity}.'

def negate(cat, entity, value):
    wrong = value + 1
    if cat == 'alpha':
        return f'The letter {entity} is not at alphabet position {wrong}.', wrong
    if cat == 'wordlen':
        return f'The word "{entity}" does not have {wrong} letters.', wrong
    if cat == 'pubyear':
        return f'{entity} was not published in {wrong}.', wrong
    return f'There are not {wrong} {entity}.', wrong

# ---- Grade 1: 450 single-clause factual, unique sentences ----
g1 = []
for f in uniq:
    g1.append({'gid': '', 'sentence': f['sentence'], 'probe': f['probe'],
               'expected_value': f['value'], 'expected_status': 'asserted-fact',
               'fid': f['fid']})
    g1.append({'gid': '', 'sentence': ALT[f['cat']](f['entity'], f['value']),
               'probe': f['probe'], 'expected_value': f['value'],
               'expected_status': 'asserted-fact', 'fid': f['fid']})
for f in uniq[:80]:
    g1.append({'gid': '', 'sentence': ALT2[f['cat']](f['entity'], f['value']),
               'probe': f['probe'], 'expected_value': f['value'],
               'expected_status': 'asserted-fact', 'fid': f['fid']})
assert len(g1) == 450 and len({r['sentence'] for r in g1}) == 450
for i, r in enumerate(g1, 1):
    r['gid'] = f'G1-{i:03d}'

# ---- Grade 2: 250 compound factual, unique sentences ----
CONJ = [' and ', ', while ', '; ']
g2 = []
for n in range(250):
    a, b = uniq[n % 185], uniq[(n + 61) % 185]
    s2l = b['sentence'][0].lower() + b['sentence'][1:]
    sent = a['sentence'][:-1] + CONJ[n % 3] + s2l
    g2.append({'gid': '', 'sentence': sent,
               'probes': [a['probe'], b['probe']],
               'expected_values': [a['value'], b['value']],
               'expected_status': 'asserted-fact',
               'fids': [a['fid'], b['fid']]})
assert len({r['sentence'] for r in g2}) == 250
for i, r in enumerate(g2, 1):
    r['gid'] = f'G2-{i:03d}'

# ---- Grade 3: 150 hedged (75) / negated (75), distinct facts ----
g3 = []
for f in uniq[:75]:
    g3.append({'gid': '', 'kind': 'hedge',
               'sentence': hedge(f['cat'], f['entity'], f['value']),
               'probe': f['probe'], 'expected_value': f['value'],
               'expected_asserted_certain': False, 'fid': f['fid']})
for f in uniq[75:150]:
    sent, wrong = negate(f['cat'], f['entity'], f['value'])
    g3.append({'gid': '', 'kind': 'negation', 'sentence': sent,
               'probe': f['probe'], 'negated_value': wrong,
               'expected': 'must-not-return-asserted:' + str(wrong),
               'fid': f['fid']})
assert len(g3) == 150 and len({r['sentence'] for r in g3}) == 150
for i, r in enumerate(g3, 1):
    r['gid'] = f'G3-{i:03d}'

def write(name, rows):
    p = os.path.join(HERE, name)
    with open(p, 'w') as fh:
        for r in rows:
            fh.write(json.dumps(r) + '\n')
    print(name, len(rows))

write('e_grade1.jsonl', g1)
write('e_grade2.jsonl', g2)
write('e_grade3.jsonl', g3)
