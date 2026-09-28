#!/usr/bin/env python3
"""Cuing / novelty audit for the D1 battery UNDER THE AMENDED PREREG.

Deterministic, zero RNG. Salted generator (A2): byte = 97+(7i+C*k+k^2)%26,
C: train=13, P0=17, P2=19, P3=23.

Checks:
 1. Teaching mass (from run1/teach_log.txt): every example line's input token
    is a training token {0..5, 700..705}; no P0/P2/P3 input appears; no P2
    expected output appears verbatim (novelty verification, frozen §5).
 2. Driver-vs-gen cross-check, WIDENED per Crew C (all sections: TEACH x72,
    P0 x48, P1 x150, P2 x600, P3 x8) against items_amended.tsv from the
    fixed binary.
 3. Dumb (non-composing) strategy rates over all 600 P2 items.
 4. Pair commutativity (empirical on P2 inputs); verifies P5/P6 (rules 4,5)
    commute with nothing (A5.1).
 5. K6 bigram analysis under the SALTED generator: per-pair bigram-clean
    input counts -> the covered-pair set (A4).
 6. A5 items: commuting fraction of the item set; soft-item count
    (items where >=2 of {identity,first-only,second-only,wrong-order} match);
    per-pair P4 table + per-length breakdown data (A5.3 pick: breakdown).
"""
import sys, os

AMENDED = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(AMENDED, "..", "battery")

PHASE_C = {0: 13, 1: 17, 2: 19, 3: 23}
def tokphase(i):
    if i >= 700: return 0
    if i < 6: return 0
    if i < 14: return 1
    if i < 614: return 2
    return 3
def tok(i):
    c = PHASE_C[tokphase(i)]
    n = 2 + (i % 4)
    return "".join(chr(97 + ((i * 7 + k * c + k * k) % 26)) for k in range(n))

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

NAMES = ["reverse", "dupfirst", "rotleft", "droplast", "upperfirst", "sortchars"]

def main():
    rundir = os.path.join(AMENDED, "run1")
    # ---- 1. teaching-mass scan ----
    teach = []
    with open(os.path.join(rundir, "teach_log.txt")) as f:
        for line in f:
            line = line.rstrip("\n")
            if "\t" in line:
                teach.append(line.split("\t", 1)[1])
    train_toks = {tok(t) for t in list(range(6)) + list(range(700, 706))}
    n_example = 0
    bad_inputs = []
    for tl in teach:
        low = tl.lower().rstrip(".")
        # example lines: "the <name> of <tok> is <exp>."
        if low.startswith("the ") and " of " in low and " is " in low \
           and not low.startswith("the letters of"):
            n_example += 1
            inp = low.split(" of ", 1)[1].split(" is ", 1)[0]
            if inp not in train_toks:
                bad_inputs.append((tl, inp))
    print(f"[1a] teaching example lines: {n_example} (P0 sessions + samples session, "
          f"6 rules x 12 taught examples each); non-train input tokens: {len(bad_inputs)}")
    for tl, w in bad_inputs[:10]:
        print(f"    BAD INPUT: {tl} :: {w}")
    # byte-identical inputs across phases (A2 side effect: must be gone)
    p0_toks = {tok(t) for t in range(6, 14)}
    p2_toks = {tok(14 + p * 4 + it) for p in range(30) for it in range(4)} | \
              {tok(134 + t * 4 + it) for t in range(120) for it in range(4)}
    p3_toks = {tok(t) for t in range(614, 622)}
    print(f"[1b] P0 inputs byte-identical to training: {len(p0_toks & train_toks)}/48; "
          f"P2: {len(p2_toks & train_toks)}/600; P3: {len(p3_toks & train_toks)}/8")
    # P2 expected outputs verbatim in teaching mass
    p2exp = set()
    for p, (a, b) in enumerate(pairs()):
        for it in range(4):
            p2exp.add(compose([a, b], tok(14 + p * 4 + it)))
    for t, (a, b, c) in enumerate(triples()):
        for it in range(4):
            p2exp.add(compose([a, b, c], tok(134 + t * 4 + it)))
    teach_words = set()
    for tl in teach:
        teach_words.update(tl.lower().rstrip(".").split())
    exp_leaks = sorted(p2exp & teach_words - train_toks -
                       {w.strip(".,") for w in teach_words})
    # single letters occur as ordinary words in teaching text (articles etc.),
    # so only expected outputs of length >= 2 count as novelty leaks
    exp_leaks = sorted(e for e in (p2exp & teach_words - train_toks) if len(e) >= 2)
    print(f"[1c] P2 expected outputs verbatim in teaching mass: {len(exp_leaks)}")
    for w in exp_leaks[:12]:
        print(f"    EXP LEAK: {w}")

    # ---- 2. driver-vs-gen cross-check (WIDENED: all sections) ----
    gen = {}
    with open(os.path.join(AMENDED, "items.tsv")) as f:
        for line in f:
            if not line.strip(): continue
            tag = line.split("\t", 1)[0]
            d = dict(kv.split("=", 1) for kv in line.rstrip("\n").split("\t")[1:])
            gen.setdefault(tag, []).append(d)
    mism = 0
    # TEACH: 72 = 6 rules x (tok 0..5, 700..705)
    exp_teach = {}
    for r in range(6):
        for t in list(range(6)) + list(range(700, 706)):
            exp_teach[(r, t)] = (tok(t), apply_rule(r, tok(t)))
    got_teach = {(int(d["rule"]), int(d["tok"])): (d["input"], d["expected"])
                 for d in gen.get("TEACH", [])}
    for k, v in exp_teach.items():
        if got_teach.get(k) != v:
            mism += 1; print(f"    TEACH MISMATCH {k}: {v} vs {got_teach.get(k)}")
    print(f"[2a] TEACH: {len(got_teach)}/72 match, {mism} mismatches")
    # P0: 48
    m0 = 0
    for d in gen.get("P0", []):
        r, t = int(d["rule"]), int(d["tok"])
        if (d["input"], d["expected"]) != (tok(t), apply_rule(r, tok(t))):
            m0 += 1
    print(f"[2b] P0: {len(gen.get('P0', []))}/48 lines, {m0} mismatches")
    # P1: 150 neutral-index records
    m1 = 0
    prs, trs = pairs(), triples()
    p1p = [d for d in gen.get("P1", []) if d["kind"] == "pair"]
    p1t = [d for d in gen.get("P1", []) if d["kind"] == "triple"]
    for p, d in enumerate(p1p):
        if (int(d["a"]), int(d["b"])) != prs[p]: m1 += 1
    for t, d in enumerate(p1t):
        if (int(d["a"]), int(d["b"]), int(d["c"])) != trs[t]: m1 += 1
    # no semantic labels anywhere in P1 lines
    lab = [d for d in gen.get("P1", [])
           if any(nm in str(d) for nm in NAMES)]
    print(f"[2c] P1: {len(p1p)} pair + {len(p1t)} triple records, {m1} mismatches, "
          f"{len(lab)} lines with semantic labels")
    # P2: 600
    m2 = 0
    p2p = [d for d in gen.get("P2", []) if d["kind"] == "pair"]
    p2t = [d for d in gen.get("P2", []) if d["kind"] == "triple"]
    for p, (a, b) in enumerate(prs):
        for it in range(4):
            d = p2p[p * 4 + it]
            s = tok(14 + p * 4 + it)
            if (d["input"], d["expected"]) != (s, compose([a, b], s)): m2 += 1
    for t, (a, b, c) in enumerate(trs):
        for it in range(4):
            d = p2t[t * 4 + it]
            s = tok(134 + t * 4 + it)
            if (d["input"], d["expected"]) != (s, compose([a, b, c], s)): m2 += 1
    print(f"[2d] P2: {len(p2p)} pair + {len(p2t)} triple items, {m2} mismatches")
    # P3: 8
    m3 = sum(1 for d in gen.get("P3", []) if d["input"] != tok(int(d["tok"])))
    print(f"[2e] P3: {len(gen.get('P3', []))}/8 lines, {m3} mismatches")

    # ---- 3. dumb strategies over 600 P2 items ----
    items = []
    for p, (a, b) in enumerate(prs):
        for it in range(4):
            s = tok(14 + p * 4 + it)
            items.append(((a, b), s, compose([a, b], s)))
    for t, (a, b, c) in enumerate(trs):
        for it in range(4):
            s = tok(134 + t * 4 + it)
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
    }
    print("[3] dumb-strategy output-correct rates over 600 P2 items (salted):")
    for name, fn in strategies.items():
        r = rate(fn)
        print(f"    {name:12s} {r:3d}/600 = {r/600:.4f}")

    # ---- 4. commutativity ----
    print("[4] commuting pairs (pi∘pj == pj∘pi on all 4 salted inputs):")
    commuting = []
    for p, (a, b) in enumerate(prs):
        ok = all(compose([a, b], tok(14 + p * 4 + it)) ==
                 compose([b, a], tok(14 + p * 4 + it)) for it in range(4))
        if ok:
            commuting.append((a, b))
            print(f"    pair ({a},{b}) COMMUTES")
    # A5.1: P5/P6 (rules 4,5) must commute with nothing
    bad56 = [(a, b) for (a, b) in commuting if a in (4, 5) or b in (4, 5)]
    print(f"    P5/P6-involved commuting pairs: {bad56 if bad56 else 'NONE - OK'}")
    # commuting fraction of the item set
    comm_pair_items = len(commuting) * 4
    # triple items where full reversal coincides with forward (empirical)
    comm_trip = 0
    for t, (a, b, c) in enumerate(trs):
        for it in range(4):
            s = tok(134 + t * 4 + it)
            if compose([a, b, c], s) == compose([c, b, a], s):
                comm_trip += 1
    print(f"    commuting fraction: pair-items {comm_pair_items}/120, "
          f"triple-items reversal-coincident {comm_trip}/480")

    # ---- 5. K6 bigram analysis (salted) -> covered-pair set ----
    train_strings = set()
    for r in range(6):
        for t in list(range(6)) + list(range(700, 706)):
            s = tok(t)
            train_strings.add(s); train_strings.add(apply_rule(r, s))
    train_bg = set()
    for s in train_strings:
        train_bg |= bigrams(s)
    print("[5] K6 (salted): per-pair bigram-clean input counts (of 4):")
    uncovered = []
    for p, (a, b) in enumerate(prs):
        n = sum(1 for it in range(4)
                if not (bigrams(tok(14 + p * 4 + it)) & train_bg))
        flag = ""
        if n == 0:
            uncovered.append((a, b)); flag = "  <-- ZERO bigram-clean (EXCLUDED from K6)"
        print(f"    pair ({a},{b}): {n}/4{flag}")
    print(f"    covered pairs: {30 - len(uncovered)}/30; excluded: {uncovered}")

    # ---- 6. A5 soft-item count ----
    fns = {
        "identity": lambda p, s: s,
        "first-only": lambda p, s: apply_rule(p[0], s),
        "second-only": lambda p, s: apply_rule(p[1], s),
        "wrong-order": lambda p, s: compose(list(reversed(p)), s),
    }
    soft = [(parts, s, e) for parts, s, e in items
            if sum(1 for fn in fns.values() if fn(parts, s) == e) >= 2]
    print(f"[6] A5 soft items (>=2 dumb strategies coincide): {len(soft)}/600")
    by_len = {}
    for _, s, _ in soft:
        by_len[len(s)] = by_len.get(len(s), 0) + 1
    print(f"    by input length: {dict(sorted(by_len.items()))}")

if __name__ == "__main__":
    main()
