#!/usr/bin/env python3
"""TP-ORACLE: independent recomputation of every third-path decision and
ledger head from the frozen data. Fails (nonzero exit) on any mismatch.
Imports ONLY data (rows, qids, rel, golds) — reimplements the classifier,
policies, and hash chain separately from the Zag program.
"""
import json, hashlib, sys
import os
_HERE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_EV=os.path.join(_HERE,'evidence')


data = json.load(open(os.path.join(_EV,'tp_data.json')))
idm = json.load(open(os.path.join(_EV,'idmaps.json')))
# ans: id -> name ; need name -> id
aid = {v: int(k) for k, v in idm['ans'].items()}
qids = sorted(data.keys())
THOUS = [500, 667, 750, 833]
PNAME = {0: 'T1', 1: 'T2', 2: 'T3'}

def classify(rows, prim_dom):
    # rows: [(dom, ans, year)] with string values; work in ids
    if len(rows) != 4:
        return 0, -1
    maxy = max(r[2] for r in rows)
    # prim's newest answer
    pna = -1
    for d, a, y in rows:
        if d == prim_dom and y == maxy:
            pna = a
    if pna == -1:
        return 0, -1
    b = [a if y == maxy else -1 for d, a, y in rows]
    nmax = sum(1 for x in b if x != -1)
    seen = []
    for x in b:
        if x != -1 and x not in seen:
            seen.append(x)
    na = len(seen)
    nps = sum(1 for x in b if x == pna)
    if na == 3:
        return (1, pna) if (nmax == 3 and nps == 1) else (0, pna)
    if na == 2:
        if nmax == 4:
            return (2, pna) if nps == 2 else (0, pna)
        return (3, pna) if nps >= 2 else (0, pna)
    if nps >= 2:
        return 3, pna
    return 0, pna

def decide(path, thou, shape, rel, pna):
    # pna: integer answer id (or -1)
    dec, ch, rule = 'WITHHOLD', '-1', 'OOS'
    if shape == 1:
        if path == 0:
            if rel >= 0:
                if rel >= thou:
                    dec, ch, rule = 'CONVERGE', str(pna), 'T1-GATE'
                else:
                    rule = 'T1-GATE-BLOCK'
            else:
                rule = 'T1-NOREL'
        elif path == 1:
            rule = 'T2-SUSPECT'
        else:
            if rel >= 0 and rel >= thou:
                dec, ch, rule = 'CONVERGE', str(pna), 'T3-DELIB-GATE'
            else:
                rule = 'T3-DELIB-WITHHOLD'
    elif shape == 2:
        rule = {0: 'T1-TIEGUARD', 1: 'T2-SUSPECT', 2: 'T3-TIEGUARD'}[path]
    elif shape == 3:
        rule = 'OOS-CORROB'
    return dec, ch, rule

# expected stdout lines + ledger heads
# order: envelope (sorted qid) -> threshold -> path  [matches tp_decide]
exp_lines = []
chain = {0: [bytes(32), 0], 1: [bytes(32), 0], 2: [bytes(32), 0]}
for q in qids:
    v = data[q]
    prim_dom = v['rows'][0][0]
    shape, pna = classify(v['rows'], prim_dom)
    rel = -1 if v['rel'] in (None, 'None') else int(round(float(v['rel']) * 1000))
    pna_id = -1 if pna == -1 else aid[pna]
    for thou in THOUS:
        for path in (0, 1, 2):
            dec, ch, rule = decide(path, thou, shape, rel, pna_id)
            exp_lines.append(f"P|{PNAME[path]}|{thou}|{q}|{dec}|{ch}|{rule}")
            prev, seq = chain[path]
            e = prev + seq.to_bytes(8, 'little') + bytes([path]) + thou.to_bytes(4, 'little')
            e += q.encode() + b'\x00' + dec.encode() + b'\x00' + ch.encode() + b'\x00' + rule.encode() + b'\x00'
            chain[path] = [hashlib.sha256(e).digest(), seq + 1]
heads = {p: chain[p][0].hex() for p in (0, 1, 2)}

# read actual run
actual = open(os.path.join(_EV,'run0.log')).read().splitlines()
dec_lines = [l for l in actual if l.startswith('P|')]
errs = 0
if len(dec_lines) != len(exp_lines):
    print(f'COUNT MISMATCH: {len(dec_lines)} vs {len(exp_lines)}')
    errs += 1
for i, (a, e) in enumerate(zip(dec_lines, exp_lines)):
    if a != e:
        if errs < 5:
            print(f'LINE {i}: got {a!r} want {e!r}')
        errs += 1
# heads
for path in (0, 1, 2):
    line = [l for l in actual if l.startswith(f'H|{PNAME[path]}|')]
    assert len(line) == 1, line
    got = line[0].split('|')[2]
    if got != heads[path]:
        print(f'HEAD MISMATCH {PNAME[path]}: got {got} want {heads[path]}')
        errs += 1
# shape counts
shapes = {}
for q in qids:
    v = data[q]
    s, _ = classify(v['rows'], v['rows'][0][0])
    shapes[s] = shapes.get(s, 0) + 1
cline = [l for l in actual if l.startswith('C|')][0]
# C|1|200|2|20|3|0|0|0
parts = cline.split('|')
got_shapes = {1: int(parts[2]), 2: int(parts[4]), 3: int(parts[6]), 0: int(parts[8])}
for s in (0, 1, 2, 3):
    if got_shapes[s] != shapes.get(s, 0):
        print(f'SHAPE COUNT MISMATCH {s}: got {got_shapes[s]} want {shapes.get(s,0)}')
        errs += 1
print('oracle shapes:', shapes)
if errs:
    print(f'ORACLE FAIL: {errs} mismatches')
    sys.exit(1)
print('ORACLE PASS: all', len(exp_lines), 'decisions + 3 ledger heads + shape counts verified')
