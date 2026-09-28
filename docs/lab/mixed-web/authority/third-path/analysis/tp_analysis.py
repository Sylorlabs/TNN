#!/usr/bin/env python3
"""TP-ANALYSIS: EV, wrong-install, S8 fiat, G2 control, T2 frontier, T3==T1.
Reads run0.log (5x byte-identical, oracle-verified) + tp_data.json."""
import json
import os
from collections import defaultdict
_HERE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_EV=os.path.join(_HERE,'evidence')

data = json.load(open(os.path.join(_EV,'tp_data.json')))
idm = json.load(open(os.path.join(_EV,'idmaps.json')))
aid = {v: int(k) for k, v in idm['ans'].items()}

# parse decisions: P|<path>|<thou>|<qid>|<dec>|<ch>|<rule>
dec = defaultdict(dict)  # (path,qid,thou) -> (dec,ch,rule)
for l in open(os.path.join(_EV,'run0.log')):
    if not l.startswith('P|'):
        continue
    _, path, thou, qid, d, ch, rule = l.rstrip('\n').split('|')
    dec[(path, qid, int(thou))] = (d, ch, rule)

qids = sorted(data.keys())
def block(q):
    return data[q]['block']
def gold(q):
    g = data[q]['gold']
    return None if g in (None, 'None') else aid[g]
def latent(q):
    g = data[q]['latent']
    return None if g in (None, 'None') else aid[g]
def rel(q):
    r = data[q]['rel']
    return None if r in (None, 'None') else float(r)

THOUS = [500, 667, 750, 833]
print("=== 1. T3 == T1 on all 220 envelopes (all thresholds) ===")
print("(comparing verdict+chosen; rule-code labels are path-specific by construction)")
diff = sum(1 for q in qids for t in THOUS
           if dec[('T1', q, t)][:2] != dec[('T3', q, t)][:2])
print(f"verdict/chosen differences T3 vs T1: {diff} / {220*4}")
rulediff = sum(1 for q in qids for t in THOUS
               if dec[('T1', q, t)][2].replace('T1', 'TX') !=
                  dec[('T3', q, t)][2].replace('T3', 'TX'))
print(f"rule-code differences after path-prefix normalization: {rulediff} / {220*4}")

print("\n=== 2. Block U: EV per reliability level (value +1/-1/0) ===")
U = [q for q in qids if block(q) == 'U']
levels = sorted({rel(q) for q in U})
print("level | n | T1@500 EV | T1@667 EV | T1@750 EV | T1@833 EV | D=2r-1")
for r in levels:
    qs = [q for q in U if rel(q) == r]
    row = [f"{r:.2f}", f"{len(qs)}"]
    for t in THOUS:
        v = 0
        for q in qs:
            d, ch, rule = dec[('T1', q, t)]
            if d == 'CONVERGE':
                v += 1 if int(ch) == gold(q) else -1
        row.append(f"{v/len(qs):+.2f}")
    row.append(f"{2*r-1:+.2f}")
    print(" | ".join(f"{x:>9}" for x in row))

print("\n=== 3. Block U: wrong-install rate per level (CONVERGE & wrong / 20) ===")
for t in THOUS:
    rs = []
    for r in levels:
        qs = [q for q in U if rel(q) == r]
        w = sum(1 for q in qs if dec[('T1', q, t)][0] == 'CONVERGE'
                and int(dec[('T1', q, t)][1]) != gold(q))
        f = sum(1 for q in qs if dec[('T1', q, t)][0] == 'CONVERGE')
        rs.append(f"{w}/{f}" if f else "-")
    print(f"T1@{t}: " + " ".join(f"{r:.2f}:{x}" for r, x in zip(levels, rs)))

print("\n=== 4. S8 fiat row (20 ties) ===")
S = [q for q in qids if block(q) == 'S']
for p in ('T1', 'T2', 'T3'):
    conv = sum(1 for q in S for t in THOUS if dec[(p, q, t)][0] == 'CONVERGE')
    wrong = sum(1 for q in S for t in THOUS
                if dec[(p, q, t)][0] == 'CONVERGE' and int(dec[(p, q, t)][1]) != latent(q))
    print(f"{p}: converges {conv}/{20*4}, wrong-guess {wrong}/{20*4}, "
          f"false-confidence {conv/(20*4)*100:.1f}%")

print("\n=== 5. G2 control (20 envelopes, no reliability) ===")
G = [q for q in qids if block(q) == 'G']
for p in ('T1', 'T2', 'T3'):
    fire = sum(1 for q in G for t in THOUS if dec[(p, q, t)][0] == 'CONVERGE')
    print(f"{p}: fire rate {fire}/{20*4}")

print("\n=== 6. T2 frontier: minimal rho to beat C (EV>0) and D (EV>2r-1) ===")
print("EV(T2)=rho(2q-1)-(1-rho)*delta ; beats C: rho>delta/(2q-1+delta) ; "
      "beats D: rho>(2r-1+delta)/(2q-1+delta)")
for q in (0.8, 0.9, 1.0):
    for delta in (0, 0.25, 0.5, 1.0):
        denom = 2*q - 1 + delta
        rc = delta / denom if denom > 0 else float('inf')
        cells = []
        for r in levels:
            need = (2*r - 1 + delta) / denom if denom > 0 else float('inf')
            cells.append("1.00+" if need > 1 else (f"{need:.2f}" if need > 0 else "0"))
        print(f"q={q} d={delta}: beatC rho>{rc:.3f} | beatD by level: " +
              " ".join(f"{r:.2f}:{c}" for r, c in zip(levels, cells)))
print("\nT2 time-to-resolution = 1/rho periods; deferred-forever mass = 1-rho")

print("\n=== 7. Threshold-gated EV per case over QUALIFYING levels (Block U) ===")
for t in THOUS:
    qs = [q for q in U if rel(q) >= t/1000]
    v = 0
    for q in qs:
        d, ch, rule = dec[('T1', q, t)]
        if d == 'CONVERGE':
            v += 1 if int(ch) == gold(q) else -1
    print(f"T1@{t}: {len(qs)} qualifying cases, EV/case {v/len(qs):+.3f}")
