#!/usr/bin/env python3
"""Crew C independent verification of the D1 battery's mechanical claims.
Independent Python replica (from frozen formulas) vs battery.zag outputs.
"""
import os

WORK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

def tok(i):
    n = 2 + (i % 4)
    return "".join(chr(97 + ((i * 7 + k * 13 + k * k) % 26)) for k in range(n))

def apply_rule(r, s):
    if r == 0: return s[::-1]
    if r == 1: return s[0] + s
    if r == 2: return s[1:] + s[:1] if s else ""
    if r == 3: return s[:-1]
    if r == 4: return s[0].upper() + s[1:] if s else ""
    return "".join(sorted(s))

def compose(parts, s):
    for r in parts: s = apply_rule(r, s)
    return s

def pairs():
    return [(p // 5, (p % 5) + (1 if (p % 5) >= (p // 5) else 0)) for p in range(30)]

def triples():
    out = []
    for t in range(120):
        i = t // 20; r1 = t % 20; ji = r1 // 4
        j = ji + (1 if ji >= i else 0)
        ki = r1 % 4; e0, e1 = (i, j) if i < j else (j, i)
        k = ki
        if k >= e0: k += 1
        if k >= e1: k += 1
        out.append((i, j, k))
    return out

def bigrams(s): return {s[i:i+2] for i in range(len(s) - 1)}

R = []
R.append("== 1. generator cross-check vs items.tsv ==")
gen = {}
with open(os.path.join(WORK, "items.tsv")) as f:
    for line in f:
        if line.startswith("P2"):
            d = dict(kv.split("=", 1) for kv in line.rstrip("\n").split("\t")[1:])
            if d["kind"] == "pair":
                key = ("pair", int(d["a"]), int(d["b"]), int(d["tok"]))
            else:
                key = ("triple", int(d["a"]), int(d["b"]), int(d["c"]), int(d["tok"]))
            gen[key] = (d["input"], d["expected"])
mism = 0
items = []
for p, (a, b) in enumerate(pairs()):
    for it in range(4):
        ti = 14 + p * 4 + it
        s = tok(ti); e = compose([a, b], s)
        items.append(((a, b), s, e, ti))
        if gen.get(("pair", a, b, ti)) != (s, e): mism += 1
for t3, (a, b, c) in enumerate(triples()):
    for it in range(4):
        ti = 134 + t3 * 4 + it
        s = tok(ti); e = compose([a, b, c], s)
        items.append(((a, b, c), s, e, ti))
        if gen.get(("triple", a, b, c, ti)) != (s, e): mism += 1
R.append(f"items={len(items)} (expect 600), mismatches vs items.tsv: {mism}")
assert len(set(triples())) == 120 and all(len(set(t)) == 3 for t in triples())
assert len(set(pairs())) == 30 and all(a != b for a, b in pairs())
R.append("pair/triple enumerations: 30 distinct pairs, 120 distinct triples, all i!=j / all-distinct")

R.append("== 2. chance arms re-scored ==")
null_rate = sum(1 for _, s, e, _ in items if s == e)
sr_rate = sum(1 for parts, s, e, _ in items if apply_rule(parts[0], s) == e)
R.append(f"NULL (identity) output-correct: {null_rate}/600 (reported 13)")
R.append(f"SINGLE-RULE (first part) output-correct: {sr_rate}/600 (reported 32)")
R.append(f"chance = max = {max(null_rate, sr_rate)}/600 = {max(null_rate, sr_rate)/600:.4f}; K1 line = {max(null_rate, sr_rate)/600 + 0.10:.4f}")

R.append("== 3. dumb strategies ==")
strats = {
    "identity": lambda p, s: s,
    "first-only": lambda p, s: apply_rule(p[0], s),
    "second-only": lambda p, s: apply_rule(p[1], s),
    "wrong-order": lambda p, s: compose(list(reversed(p)), s),
    "ascending": lambda p, s: compose(sorted(p), s),
    "descending": lambda p, s: compose(sorted(p, reverse=True), s),
}
for name, fn in strats.items():
    n = sum(1 for parts, s, e, _ in items if fn(parts, s) == e)
    R.append(f"  {name:12s} {n}/600")

R.append("== 4. period-52 + byte-identical counts ==")
per = all(tok(i + 52) == tok(i) for i in range(700))
R.append(f"exact period 52 over tok(0..751): {per}")
train = {tok(t) for t in range(6)}
p0dup = sum(1 for t in range(6, 14) if tok(t) in train)
p2dup = sum(1 for _, s, _, _ in items if s in train)
p3dup = sum(1 for t in range(614, 622) if tok(t) in train)
R.append(f"P0 inputs byte-identical to training: {p0dup}/48 (reported 0)")
R.append(f"P2 inputs byte-identical to training: {p2dup}/600 (reported 66)")
R.append(f"P3 inputs byte-identical to training: {p3dup}/8 (reported 0)")

R.append("== 5. K6 bigram audit ==")
train_strings = set()
for r in range(6):
    for t in range(6):
        s = tok(t); train_strings.add(s); train_strings.add(apply_rule(r, s))
train_bg = set().union(*(bigrams(s) for s in train_strings))
zero_pairs = []
for p, (a, b) in enumerate(pairs()):
    n = sum(1 for it in range(4) if not (bigrams(tok(14 + p * 4 + it)) & train_bg))
    if n == 0: zero_pairs.append((a, b))
R.append(f"pairs with zero bigram-clean inputs: {sorted(zero_pairs)} (reported [(0,4),(2,0),(3,1),(4,3),(5,4)])")

R.append("== 6. learner P0 re-score (last-word rule) ==")
def last_word(resp):
    w = resp.strip()
    w = w.split()[-1] if w.split() else ""
    return w.lower().rstrip(".").rstrip(",").rstrip("!")
got = 0; nrec = 0
with open(os.path.join(WORK, "run1", "resp_p0.txt")) as f:
    lines = f.read().split("\n")
i = 0
while i < len(lines):
    if lines[i].startswith("P0 "):
        _, rs, ts = lines[i].split(" "); r, t = int(rs), int(ts)
        resp = lines[i + 1] if i + 1 < len(lines) else ""
        exp = apply_rule(r, tok(t))
        if last_word(resp) == exp: got += 1
        nrec += 1; i += 2
    else: i += 1
R.append(f"re-scored P0: {got}/{nrec} (reported 0/48)")

R.append("== 7. shift-memorizer (strict, case-preserving) on 600 P2 items ==")
# memorizes only the 36 training input->output examples (all 6 rules, tok 0..5)
mem = {}
for r in range(6):
    for t in range(6):
        mem[(r, tok(t))] = apply_rule(r, tok(t))
def cshift(s, d):
    out = []
    for ch in s:
        if 'a' <= ch <= 'z': out.append(chr(97 + (ord(ch) - 97 + d) % 26))
        elif 'A' <= ch <= 'Z': out.append(chr(65 + (ord(ch) - 65 + d) % 26))
        else: out.append(ch)
    return "".join(out)
def shift_of(a, b):
    # Caesar shift d with shift(a,d)==b, or None
    for d in range(26):
        if cshift(a, d) == b: return d
    return None
def srule(r, x):
    # apply rule r to x using only memorized examples + shift detection
    for t in range(6):
        xt = tok(t)
        if len(xt) == len(x):
            d = shift_of(xt, x)
            if d is not None:
                return cshift(mem[(r, xt)], d)
    return None
def smem(parts, x):
    for r in parts:
        x = srule(r, x)
        if x is None: return None
    return x
sm_ok = sum(1 for parts, s, e, _ in items if smem(parts, s) == e)
R.append(f"strict shift-memorizer output-correct: {sm_ok}/600")
# per-pair breakdown for pairs
pair_sm = {}
for p, (a, b) in enumerate(pairs()):
    n = sum(1 for it in range(4)
            for parts, s, e, ti in [items[p * 4 + it]] if smem((a, b), s) == e)
    pair_sm[(a, b)] = n
bad_pairs = sorted([k for k, v in pair_sm.items() if v < 4])
R.append(f"pairs where shift-memorizer < 4/4: {bad_pairs}")

R.append("== 8. commutativity (audit's per-input definition) ==")
comm = []
for p, (a, b) in enumerate(pairs()):
    if all(compose([a, b], tok(14 + p * 4 + it)) == compose([b, a], tok(14 + p * 4 + it)) for it in range(4)):
        comm.append((a, b))
R.append(f"commuting pairs: {sorted(comm)} (reported [(1,3),(3,1),(3,4),(4,3)])")

txt = "\n".join(R)
print(txt)
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "rt_verify.txt"), "w") as f:
    f.write(txt + "\n")
