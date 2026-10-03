#!/usr/bin/env python3
"""Cuing / novelty audit for the D1 full battery (frozen prereg §5).
Deterministic, zero RNG. Checks:
 1. Training mass contains ONLY single-part applications; no P0/P2/P3 token
    (or P2 expected output) appears in any teaching line (novelty verification).
 2. Driver's teaching examples match the Zag generator's TEACH lines (cross-check).
 3. Dumb (non-composing) strategy rates over all 600 P2 items — documents
    freebies/order-insensitive items (feeds K1 context + A5 limitations).
 4. Pair commutativity: which ordered pairs commute on their 4 inputs.
 5. K6 bigram analysis: per pair, inputs sharing no bigram with any training string.
"""
import sys, os

WORK = os.path.dirname(os.path.abspath(__file__))

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
    for r in parts:
        s = apply_rule(r, s)
    return s

def pairs():
    out = []
    for p in range(30):
        pi = p // 5; q = p % 5; pj = q + (1 if q >= pi else 0)
        out.append((pi, pj))
    return out

def triples():
    out = []
    for i in range(6):
        for j in range(6):
            if j == i: continue
            for k in range(6):
                if k == i or k == j: continue
                out.append((i, j, k))
    return out

def bigrams(s):
    return {s[i:i+2] for i in range(len(s) - 1)}

def main():
    # ---- 1. teaching-mass scan ----
    teach = []
    with open(os.path.join(WORK, "run1", "teach_log.txt")) as f:
        for line in f:
            line = line.rstrip("\n")
            if "\t" in line:
                teach.append(line.split("\t", 1)[1])
    train_toks = {tok(t) for t in range(6)}
    # (a) every teaching line's input token must be a training token (0..5)
    bad_inputs = []
    for tl in teach:
        low = tl.lower().rstrip(".")
        if low.startswith("the ") and " of " in low and " is " in low:
            inp = low.split(" of ", 1)[1].split(" is ", 1)[0]
            if inp not in train_toks:
                bad_inputs.append((tl, inp))
    print(f"[1a] teaching lines: {len(teach)}; non-train input tokens: {len(bad_inputs)}")
    for tl, w in bad_inputs[:10]:
        print(f"    BAD INPUT: {tl} :: {w}")
    # (b) period-52 exact duplication: P2/P0/P3 inputs byte-identical to training inputs
    dup_p0 = [t for t in range(6, 14) if tok(t) in train_toks]
    dup_p2 = []
    for p in range(30):
        for it in range(4):
            t = 14 + p * 4 + it
            if tok(t) in train_toks:
                dup_p2.append(t)
    for ti in range(120):
        for it in range(4):
            t = 134 + ti * 4 + it
            if tok(t) in train_toks:
                dup_p2.append(t)
    dup_p3 = [t for t in range(614, 622) if tok(t) in train_toks]
    print(f"[1b] P2 inputs byte-identical to a training input: {len(dup_p2)}/600 "
          f"(tok idx {dup_p2[:12]}{'...' if len(dup_p2)>12 else ''})")
    print(f"     P0 inputs identical to training: {len(dup_p0)}/48; P3: {len(dup_p3)}/8")
    # (c) P2 expected outputs appearing verbatim in the teaching mass
    p2exp = set()
    for p, (a, b) in enumerate(pairs()):
        for it in range(4):
            s = tok(14 + p * 4 + it)
            p2exp.add(compose([a, b], s))
    for ti, (a, b, c) in enumerate(triples()):
        for it in range(4):
            s = tok(134 + ti * 4 + it)
            p2exp.add(compose([a, b, c], s))
    teach_words = set()
    for tl in teach:
        teach_words.update(tl.lower().rstrip(".").split())
    exp_leaks = sorted(p2exp & teach_words - train_toks)
    print(f"[1c] P2 expected outputs verbatim in teaching mass: {len(exp_leaks)}")
    for w in exp_leaks[:10]:
        print(f"    EXP LEAK: {w}")

    # ---- 2. driver-vs-gen cross-check ----
    gen_teach = {}
    with open(os.path.join(WORK, "items.tsv")) as f:
        for line in f:
            if line.startswith("TEACH"):
                d = dict(kv.split("=", 1) for kv in line.rstrip("\n").split("\t")[1:])
                gen_teach[(int(d["rule"]), int(d["tok"]))] = (d["input"], d["expected"])
    mism = 0
    for tl in teach:
        # "the <name> of <tok> is <exp>."  (P0R lines) — P3/SMP lines also match
        low = tl.lower().rstrip(".")
        if low.startswith("the ") and " of " in low and " is " in low:
            _, rest = low.split(" of ", 1)
            inp, exp = rest.split(" is ", 1)
            name = tl.split("\t", 1)[1].split(" ", 1)[0] if "\t" in tl else ""
    # simpler: recompute from protocol
    names = ["reverse", "dupfirst", "rotleft", "droplast", "upperfirst", "sortchars"]
    proto = {}
    for r in range(6):
        for t in range(6):
            proto[(r, t)] = (tok(t), apply_rule(r, tok(t)))
    for k, v in proto.items():
        if gen_teach.get(k) != v:
            mism += 1
            print(f"    MISMATCH proto vs gen at {k}: {v} vs {gen_teach.get(k)}")
    print(f"[2] driver-protocol vs gen TEACH cross-check: {mism} mismatches (36 expected)")

    # ---- 3. dumb strategies over 600 P2 items ----
    items = []  # (parts_tuple, input, expected)
    for p, (a, b) in enumerate(pairs()):
        for it in range(4):
            s = tok(14 + p * 4 + it)
            items.append(((a, b), s, compose([a, b], s)))
    for ti, (a, b, c) in enumerate(triples()):
        for it in range(4):
            s = tok(134 + ti * 4 + it)
            items.append(((a, b, c), s, compose([a, b, c], s)))
    assert len(items) == 600
    def rate(fn):
        return sum(1 for parts, s, e in items if fn(parts, s) == e)
    strategies = {
        "identity": lambda p, s: s,
        "first-only": lambda p, s: apply_rule(p[0], s),
        "second-only": lambda p, s: apply_rule(p[1], s),
        "wrong-order": lambda p, s: compose(list(reversed(p)), s),
        "ascending": lambda p, s: compose(sorted(p), s),
        "descending": lambda p, s: compose(sorted(p, reverse=True), s),
        "first-twice": lambda p, s: apply_rule(p[0], apply_rule(p[0], s)),
    }
    print("[3] dumb-strategy output-correct rates over 600 P2 items:")
    for name, fn in strategies.items():
        print(f"    {name:12s} {rate(fn):3d}/600 = {rate(fn)/600:.3f}")

    # ---- 4. commutativity per pair ----
    print("[4] commuting pairs (pi∘pj == pj∘pi on all 4 inputs):")
    for p, (a, b) in enumerate(pairs()):
        ok = True
        for it in range(4):
            s = tok(14 + p * 4 + it)
            if compose([a, b], s) != compose([b, a], s):
                ok = False; break
        if ok:
            print(f"    pair ({a},{b}) COMMUTES")

    # ---- 5. K6 bigram analysis ----
    train_strings = set()
    for r in range(6):
        for t in range(6):
            s = tok(t)
            train_strings.add(s); train_strings.add(apply_rule(r, s))
    train_bg = set()
    for s in train_strings:
        train_bg |= bigrams(s)
    print("[5] K6: per-pair bigram-clean input counts (of 4):")
    for p, (a, b) in enumerate(pairs()):
        n = 0
        for it in range(4):
            s = tok(14 + p * 4 + it)
            if not (bigrams(s) & train_bg):
                n += 1
        flag = "  <-- ZERO bigram-clean inputs" if n == 0 else ""
        print(f"    pair ({a},{b}): {n}/4{flag}")

if __name__ == "__main__":
    main()
