#!/usr/bin/env python3
"""Crew E (independent red team) verification suite for the D1 AMENDED run.

Written from the enacted amendments A1-A7 + frozen prereg, NOT from Crew D's
code. Reads the ACTUAL committed items.tsv (not a regenerated stream) for
every check that the A2 gate claims about "the actual emitted token stream".

Covers: salt formula (full 878 lines), A2 GATE-1/GATE-2 on actual strings,
the 16 chained-P2 hits item-by-item, affine memorizer attack, chance-arm
re-scoring, dumb-strategy family incl. fourth-strategy search, ascending
analysis, K6 bigram audit, soft-item count, P5/P4 commutation, palindromes,
isograms.
"""
import sys, os, itertools

AMENDED = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
ITEMS = os.path.join(AMENDED, "items.tsv")

# ---- A2 enacted formula ----
PHASE_C = {"train": 13, "P0": 17, "P2": 19, "P3": 23}
def phase_of(tokidx):
    if tokidx >= 700: return "train"
    if tokidx < 6: return "train"
    if tokidx < 14: return "P0"
    if tokidx < 614: return "P2"
    return "P3"
def tok_formula(i):
    c = PHASE_C[phase_of(i)]
    n = 2 + (i % 4)
    return "".join(chr(97 + ((i * 7 + k * c + k * k) % 26)) for k in range(n))

RULES = ["reverse", "dupfirst", "rotleft", "droplast", "upperfirst", "sortchars"]
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
# A3/A6 pair enumerator: fixed, documented order (i,j), i != j
def pairs():
    out = []
    for i in range(6):
        for j in range(6):
            if j != i: out.append((i, j))
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
def bigrams(s): return {s[i:i+2] for i in range(len(s) - 1)}
def is_shift(a, b):
    if len(a) != len(b) or not a: return False
    d = (ord(a[0]) - ord(b[0])) % 26
    return all((ord(x) - ord(y)) % 26 == d for x, y in zip(a, b))

# ---- load committed items.tsv ----
def load():
    rows = []
    with open(ITEMS) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip(): continue
            tag = line.split("\t", 1)[0]
            d = dict(kv.split("=", 1) for kv in line.split("\t")[1:])
            rows.append((tag, d))
    return rows

def main():
    rows = load()
    by_tag = {}
    for tag, d in rows: by_tag.setdefault(tag, []).append(d)
    print(f"loaded {len(rows)} rows: " +
          ", ".join(f"{t}={len(v)}" for t, v in sorted(by_tag.items())))
    assert len(rows) == 878, "row count != 878"

    # ============ ATTACK 2: salt formula on ALL 878 token strings ============
    mism = []
    for tag, d in rows:
        if "tok" in d and "input" in d:
            if d["input"] != tok_formula(int(d["tok"])):
                mism.append((tag, d.get("tok"), d["input"], tok_formula(int(d["tok"]))))
    print(f"[A2-formula] token mismatches vs enacted formula: {len(mism)}/878")
    for m in mism[:10]: print("   MISMATCH:", m)

    # isogram check on all token inputs
    noniso = [(tag, d["tok"], d["input"]) for tag, d in rows
              if "input" in d and len(set(d["input"])) != len(d["input"])]
    print(f"[A2-isogram] non-isogram token inputs: {len(noniso)}")
    for m in noniso[:10]: print("   NON-ISOGRAM:", m)

    # palindromes in P3 (I24 claim: tok 614 'iggi', 618 'kiik')
    pals = [(d["tok"], d["input"]) for d in by_tag["P3"]
            if d["input"] == d["input"][::-1]]
    print(f"[A2-pal] P3 palindromes: {pals} (I24 claims 614/iggi, 618/kiik)")

    # A2 side-effect claim: P2 tokens differ from training tokens at every k>=1
    train_inputs = {d["input"] for d in by_tag["TEACH"]}
    p2_inputs = [d["input"] for d in by_tag["P2"]]
    viol = 0
    for s in p2_inputs:
        for t in train_inputs:
            if len(s) == len(t) and all(s[k] == t[k] for k in range(1, len(s))):
                viol += 1; break
    print(f"[A2-sidefx] P2 inputs identical to a train input at all k>=1: {viol}/600")

    # ============ P1/P2 structural check vs enumerators ============
    prs, trs = pairs(), triples()
    p1p = [d for d in by_tag["P1"] if d["kind"] == "pair"]
    p1t = [d for d in by_tag["P1"] if d["kind"] == "triple"]
    p1m = sum(1 for p, d in enumerate(p1p) if (int(d["a"]), int(d["b"])) != prs[p])
    p1m += sum(1 for t, d in enumerate(p1t)
               if (int(d["a"]), int(d["b"]), int(d["c"])) != trs[t])
    print(f"[struct] P1 pair/triple records vs enumerator: {len(p1p)}/{len(p1t)}, mism={p1m}")
    lab = [d for d in by_tag["P1"] if any(n in str(d) for n in RULES)]
    print(f"[struct] P1 lines with semantic labels: {len(lab)} (A3: must be 0)")

    p2p = [d for d in by_tag["P2"] if d["kind"] == "pair"]
    p2t = [d for d in by_tag["P2"] if d["kind"] == "triple"]
    print(f"[struct] P2 pair items={len(p2p)} triple items={len(p2t)}")
    # verify expected outputs recomputed from (pair, input)
    m2 = 0; exp_bad = []
    for p, (a, b) in enumerate(prs):
        for it in range(4):
            d = p2p[p*4+it]
            e = compose([a, b], d["input"])
            if d["expected"] != e:
                m2 += 1; exp_bad.append((p, a, b, it, d["input"], d["expected"], e))
    for t, (a, b, c) in enumerate(trs):
        for it in range(4):
            d = p2t[t*4+it]
            e = compose([a, b, c], d["input"])
            if d["expected"] != e:
                m2 += 1; exp_bad.append((t, a, b, c, it, d["input"], d["expected"], e))
    print(f"[struct] P2 expected-output mismatches (recomputed): {m2}/600")
    for m in exp_bad[:8]: print("   EXP MISMATCH:", m)
    # verify P2 inputs sit at the documented token indices
    idx_bad = 0
    for p in range(30):
        for it in range(4):
            if p2p[p*4+it]["input"] != tok_formula(14 + p*4 + it): idx_bad += 1
    for t in range(120):
        for it in range(4):
            if p2t[t*4+it]["input"] != tok_formula(134 + t*4 + it): idx_bad += 1
    print(f"[struct] P2 input index-layout mismatches: {idx_bad}/600")

    # ============ ATTACK 1a: GATE-1 on ACTUAL committed strings ============
    phase_toks = {"train": [], "P0": [], "P2": [], "P3": []}
    for tag, d in rows:
        if tag in ("TEACH", "P0", "P2", "P3") and "input" in d:
            # TEACH rows are train phase
            ph = "train" if tag == "TEACH" else tag
            phase_toks[ph].append(d["input"])
    # dedupe note: TEACH has duplicate input tokens across rules (same tok)
    print(f"[G1] actual token counts: " +
          ", ".join(f"{k}={len(v)}" for k, v in phase_toks.items()))
    hits1 = []
    names = list(phase_toks)
    for x in range(len(names)):
        for y in range(x+1, len(names)):
            A = sorted(set(phase_toks[names[x]])); B = sorted(set(phase_toks[names[y]]))
            for a in A:
                for b in B:
                    if is_shift(a, b):
                        hits1.append((names[x], names[y], a, b))
    print(f"[G1] cross-phase shift pairs on ACTUAL items.tsv strings: {len(hits1)}")
    for h in hits1[:10]: print("   HIT:", h)

    # ============ ATTACK 1b: GATE-2 on actual intermediates ============
    train_set = sorted(set(phase_toks["train"]))
    train_by_len = {}
    for s in train_set: train_by_len.setdefault(len(s), []).append(s)
    hits2 = []; n_inter = 0
    for p, (a, b) in enumerate(prs):
        for it in range(4):
            s = p2p[p*4+it]["input"]
            m = apply_rule(a, s); n_inter += 1
            for t in train_by_len.get(len(m), []):
                if is_shift(m, t): hits2.append(("pair", a, b, p, it, m, t))
    for t, (a, b, c) in enumerate(trs):
        for it in range(4):
            s = p2t[t*4+it]["input"]
            m1 = apply_rule(a, s); m2 = apply_rule(b, m1)
            for m in (m1, m2):
                n_inter += 1
                for tr in train_by_len.get(len(m), []):
                    if is_shift(m, tr): hits2.append(("triple", a, b, c, t, it, m, tr))
    print(f"[G2] chained intermediates: {n_inter}; shift-equiv to train: {len(hits2)}")
    for h in hits2[:10]: print("   HIT:", h)

    # ============ ATTACK 1c: the 16 chained-P2 hits, item by item ============
    # replicate Crew D's chained memorizer (shift-based, identity fallback)
    train_idx = list(range(6)) + list(range(700, 706))
    train_tok_str = [tok_formula(i) for i in train_idx]
    mem = {}
    for r in range(6):
        for s in train_tok_str: mem[(r, s)] = apply_rule(r, s)
    def shift_str(s, d):
        out = []
        for ch in s:
            if 'a' <= ch <= 'z': out.append(chr(97 + (ord(ch)-97+d) % 26))
            elif 'A' <= ch <= 'Z': out.append(chr(65 + (ord(ch)-65+d) % 26))
            else: out.append(ch)
        return "".join(out)
    def shift_answer(r, probe):
        for s in train_tok_str:
            if len(s) == len(probe) and is_shift(probe, s):
                d = (ord(probe[0]) - ord(s[0])) % 26
                return shift_str(mem[(r, s)], d)
        return None
    def chained_p2(a, b, s):
        if a != 3: return s
        if shift_answer(a, s) is None: return s
        m = apply_rule(a, s)
        got = None
        for tr in train_tok_str:
            if len(tr) == len(m) and is_shift(m, tr):
                d = (ord(m[0]) - ord(tr[0])) % 26
                got = shift_str(mem[(a, tr)], d); break
        if got is None: return s
        for tr in train_tok_str:
            if len(tr) == len(got) and is_shift(got, tr):
                d2 = (ord(got[0]) - ord(tr[0])) % 26
                return shift_str(mem[(b, tr)], d2)
        return s
    hits = []
    for p, (a, b) in enumerate(prs):
        for it in range(4):
            d = p2p[p*4+it]; s, e = d["input"], d["expected"]
            if chained_p2(a, b, s) == e:
                hits.append(("pair", a, b, p, it, s, e, s == e))
    for t, (a, b, c) in enumerate(trs):
        for it in range(4):
            d = p2t[t*4+it]; s, e = d["input"], d["expected"]
            if chained_p2(a, b, s) == e:
                hits.append(("triple", a, b, c, t, it, s, e, s == e))
    print(f"[G3b] chained memorizer P2 hits: {len(hits)}/600 (reported 16)")
    non_ident = [h for h in hits if not h[-1]]
    print(f"       of which input!=expected (genuine chain candidates): {len(non_ident)}")
    for h in non_ident: print("   GENUINE?:", h)
    ident = [h for h in hits if h[-1]]
    print(f"       identity coincidences: {len(ident)}")
    # did the memorizer EVER actually chain (non-fallback path taken)?
    # (shift_answer always None given G1=0, so no — state it)

    # ============ ATTACK 1d: AFFINE memorizer (offset+slope per token) ============
    def affine_fit(p, t):
        """Return (a,b) with p[k]==t[k]+a+b*k (mod 26) for all k, or None."""
        if len(p) != len(t) or len(p) < 2: return None
        a = (ord(p[0]) - ord(t[0])) % 26
        b = (ord(p[1]) - ord(t[1]) - a) % 26
        if all((ord(p[k]) - ord(t[k])) % 26 == (a + b*k) % 26 for k in range(len(p))):
            return (a, b)
        return None
    def affine_str(s, a, b):
        out = []
        for k, ch in enumerate(s):
            if 'a' <= ch <= 'z': out.append(chr(97 + (ord(ch)-97+a+b*k) % 26))
            elif 'A' <= ch <= 'Z': out.append(chr(65 + (ord(ch)-65+a+b*k) % 26))
            else: out.append(ch)
        return "".join(out)
    def affine_answer(r, probe):
        for s in train_tok_str:
            f = affine_fit(probe, s)
            if f:
                a, b = f
                return affine_str(mem[(r, s)], a, b)
        return None
    p0_aff = []
    for r in range(6):
        c = 0
        for t in range(6, 14):
            pr = tok_formula(t)
            ans = affine_answer(r, pr)
            if ans is None: ans = pr
            if ans == apply_rule(r, pr): c += 1
        p0_aff.append(c)
    print(f"[affine] P0 per-rule: {p0_aff} (gate needs all <7 to FAIL)")
    # chained affine through commuting pairs
    def chained_aff(a, b, s):
        # step 1: map s -> train, shift intermediate; step 2: map intermediate
        for tr in train_tok_str:
            f = affine_fit(s, tr)
            if not f: continue
            a1, b1 = f
            m = apply_rule(a, s)
            # predicted intermediate = affine(mem[(a,tr)])
            pred_m = affine_str(mem[(a, tr)], a1, b1)
            if pred_m != m: continue  # fit must reproduce the true intermediate
            for tr2 in train_tok_str:
                f2 = affine_fit(pred_m, tr2)
                if not f2: continue
                a2, b2 = f2
                return affine_str(mem[(b, tr2)], a2, b2)
        return s
    aff_hits = []
    for p, (a, b) in enumerate(prs):
        for it in range(4):
            d = p2p[p*4+it]; s, e = d["input"], d["expected"]
            if chained_aff(a, b, s) == e:
                aff_hits.append((a, b, p, it, s, e, s == e))
    print(f"[affine] chained P2 hits: {len(aff_hits)}/600")
    per_pair = {}
    for h in aff_hits: per_pair[h[0:2]] = per_pair.get(h[0:2], 0) + 1
    print(f"           per-pair: {sorted(per_pair.items())}")

    # ============ ATTACK 3: chance arms re-scored from items.tsv ============
    items = []
    for p, (a, b) in enumerate(prs):
        for it in range(4):
            d = p2p[p*4+it]; items.append(((a, b), d["input"], d["expected"]))
    for t, (a, b, c) in enumerate(trs):
        for it in range(4):
            d = p2t[t*4+it]; items.append(((a, b, c), d["input"], d["expected"]))
    assert len(items) == 600
    strategies = {
        "identity(null)": lambda p, s: s,
        "first-only(singlerule)": lambda p, s: apply_rule(p[0], s),
        "wrong-order": lambda p, s: compose(list(reversed(p)), s),
        "ascending": lambda p, s: compose(sorted(p), s),
        "descending": lambda p, s: compose(sorted(p, reverse=True), s),
    }
    print("[chance] dumb-strategy rates (independent):")
    for name, fn in strategies.items():
        r = sum(1 for parts, s, e in items if fn(parts, s) == e)
        print(f"    {name:24s} {r:3d}/600 = {r/600:.4f}")
    # ascending: is it quasi-correct? count items where sorted(parts)==list(parts)
    asc_quasi = sum(1 for parts, s, e in items if list(parts) == sorted(parts))
    print(f"    (items where pair/triple already index-sorted: {asc_quasi}/600)")

    # per-rule-only strategies (each single rule as the whole answer)
    print("[chance] single-rule-as-answer rates:")
    for r in range(6):
        n = sum(1 for parts, s, e in items if apply_rule(r, s) == e)
        print(f"    rule {r} ({RULES[r]:10s}): {n:3d}/600 = {n/600:.4f}")

    # FOURTH dumb strategy search: fixed transformations not using presented parts
    cands = {}
    # case variants / reversals / sorts of the INPUT
    cands["upper-all"] = lambda s: s.upper()
    cands["lower-all"] = lambda s: s.lower()
    cands["reverse-input"] = lambda s: s[::-1]
    cands["sort-input"] = lambda s: "".join(sorted(s))
    cands["sort-desc-input"] = lambda s: "".join(sorted(s, reverse=True))
    cands["rotleft-input"] = lambda s: s[1:] + s[:1]
    cands["dupfirst-input"] = lambda s: s[0] + s
    cands["droplast-input"] = lambda s: s[:-1]
    # two-step fixed combos
    cands["rev+sort"] = lambda s: "".join(sorted(s[::-1]))
    cands["upperfirst-input"] = lambda s: s[0].upper() + s[1:]
    print("[chance] fixed-transformation (part-blind) strategy search:")
    best = []
    for name, fn in cands.items():
        n = sum(1 for parts, s, e in items if fn(s) == e)
        best.append((n, name))
    for n, name in sorted(best, reverse=True)[:6]:
        print(f"    {name:20s} {n:3d}/600 = {n/600:.4f}")
    # wrong-order components: which pairs drive it? commuting + soft
    wo_hits = [(parts, s, e) for parts, s, e in items
               if compose(list(reversed(parts)), s) == e]
    print(f"[chance] wrong-order hits={len(wo_hits)}; pair items: "
          f"{sum(1 for p,_,_ in wo_hits if len(p)==2)}, triple: "
          f"{sum(1 for p,_,_ in wo_hits if len(p)==3)}")

    # ============ ATTACK 3b: soft items (I20) ============
    fns = {"identity": lambda p, s: s,
           "first-only": lambda p, s: apply_rule(p[0], s),
           "second-only": lambda p, s: apply_rule(p[1], s),
           "wrong-order": lambda p, s: compose(list(reversed(p)), s)}
    soft = [(parts, s, e) for parts, s, e in items
            if sum(1 for fn in fns.values() if fn(parts, s) == e) >= 2]
    by_len = {}
    for _, s, _ in soft: by_len[len(s)] = by_len.get(len(s), 0) + 1
    print(f"[soft] I20 claim 22/600; independent: {len(soft)}/600, "
          f"by_len={dict(sorted(by_len.items()))}")

    # ============ ATTACK 6: K6 bigram audit from items.tsv ============
    train_strings = set()
    for d in by_tag["TEACH"]:
        train_strings.add(d["input"]); train_strings.add(d["expected"])
    train_bg = set()
    for s in train_strings: train_bg |= bigrams(s)
    uncovered = []
    per_pair_n = {}
    for p, (a, b) in enumerate(prs):
        n = sum(1 for it in range(4)
                if not (bigrams(p2p[p*4+it]["input"]) & train_bg))
        per_pair_n[(a, b)] = n
        if n == 0: uncovered.append((a, b))
    print(f"[K6] covered pairs: {30-len(uncovered)}/30 (claim 30/30); "
          f"uncovered: {uncovered}")
    print(f"     min bigram-clean per pair: {min(per_pair_n.values())} "
          f"(claim >=2)")
    dist = {}
    for v in per_pair_n.values(): dist[v] = dist.get(v, 0) + 1
    print(f"     distribution: {dict(sorted(dist.items()))}")

    # ============ commutativity (I19) ============
    comm = []
    for p, (a, b) in enumerate(prs):
        if all(compose([a, b], p2p[p*4+it]["input"]) ==
               compose([b, a], p2p[p*4+it]["input"]) for it in range(4)):
            comm.append((a, b))
    print(f"[comm] commuting pairs on actual P2 inputs: {sorted(comm)} "
          f"(I19 claims (1,3),(3,1),(3,4),(4,3))")

    # ============ I23 check: (0,5)/(5,0) identity coincidence ============
    for p, (a, b) in [(4, (0, 5)), (25, (5, 0))]:
        det = []
        for it in range(4):
            s = p2p[p*4+it]["input"]; e = p2p[p*4+it]["expected"]
            det.append((s, e, s == e))
        print(f"[I23] pair {a,b} pidx={p}: {det}")

    print("DONE")

if __name__ == "__main__":
    main()
