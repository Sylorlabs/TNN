#!/usr/bin/env python3
"""Battery-property verification instrument for MATH R2 (NOT an engine).

Mechanically checks the authored batteries' claimed properties using only
forward closure under S_MP + S_UI + language-level CONTRA (F and not(F)
-> false). It implements NO referee, NO contradiction tolerance, NO PBC
search, NO learning: it cannot produce engine verdicts, only battery
property measurements.

Checks:
  B4X: target derivable; min derivation depth >= 3 (PBC items: verified via
       the documented assumption -> false, +1 for the S_PBC step).
  B5X: (a) sealed verdict == closure verdict on premises + BASE store;
       (b) under the INJECTED store the false endpoint is derivable in
       exactly L hops and contradicted by the trusted premise;
       (c) ablation: removing ANY single false rule breaks the false
       derivation (proves every hop is needed);
       (d) no single false rule's consequent is contradicted by trusted
       content (single-hop detection insufficient).
  B6X: >= 100 DISTINCT store items on the shortest derivation path.
  B7F: NL 6-gram wash against round-1 traces (no B7F wording appears there).

Deterministic: claims iterated in sorted order; no RNG; no dict-order
dependence. Exit 0 iff all checks pass.
"""
import os
import re
import sys

BAT = os.path.dirname(os.path.abspath(__file__))
TRACES = os.path.expanduser("~/workspace/tnn-lab/math_logic/traces")

# ---------------- claim language ----------------

TOKEN = re.compile(r"\s*(\?[0-9]+|[A-Za-z_][A-Za-z0-9_]*|\(|\)|,)\s*")

def tokenize(s):
    toks, i = [], 0
    while i < len(s):
        m = TOKEN.match(s, i)
        if not m or m.end() == i:
            raise ValueError("bad char at %d in %r" % (i, s))
        toks.append(m.group(1))
        i = m.end()
    return toks

class P:
    def __init__(self, toks):
        self.t = toks
        self.i = 0
    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else None
    def next(self):
        x = self.t[self.i]; self.i += 1; return x

def parse_term(p):
    t = p.next()
    if t.startswith("?"):
        return ("var", t)
    if not re.fullmatch(r"[a-z][a-z0-9_]*", t):
        raise ValueError("bad term head %r" % t)
    if p.peek() == "(":
        p.next()
        args = [parse_term(p)]
        while p.peek() == ",":
            p.next(); args.append(parse_term(p))
        assert p.next() == ")"
        return ("fn", t, tuple(args))
    return ("const", t)

def parse_formula(p):
    t = p.next()
    if t == "false":
        return ("false",)
    if t in ("not", "imp", "and", "or"):
        assert p.next() == "("
        a = parse_formula(p)
        if t == "not":
            assert p.next() == ")"
            return ("not", a)
        assert p.next() == ","
        b = parse_formula(p)
        assert p.next() == ")"
        return (t, a, b)
    if t == "forall":
        assert p.next() == "("
        v = p.next()
        assert p.next() == ","
        body = parse_formula(p)
        assert p.next() == ")"
        return ("forall", v, body)
    if t.startswith("?"):
        raise ValueError("schema var in ground claim")
    if not re.fullmatch(r"[a-z][a-z0-9_]*", t):
        raise ValueError("bad atom head %r" % t)
    if p.peek() == "(":
        p.next()
        args = [parse_term(p)]
        while p.peek() == ",":
            p.next(); args.append(parse_term(p))
        assert p.next() == ")"
        return ("atom", t, tuple(args))
    return ("atom", t, ())

def parse(s):
    p = P(tokenize(s))
    f = parse_formula(p)
    assert p.peek() is None, "trailing tokens in %r" % s
    return f

def fmt(f):
    k = f[0]
    if k == "false": return "false"
    if k == "not": return "not(%s)" % fmt(f[1])
    if k in ("imp", "and", "or"): return "%s(%s,%s)" % (k, fmt(f[1]), fmt(f[2]))
    if k == "forall": return "forall(%s,%s)" % (f[1], fmt(f[2]))
    if k == "atom":
        return f[1] if not f[2] else "%s(%s)" % (f[1], ",".join(fmt(a) for a in f[2]))
    if k == "const": return f[1]
    if k == "var": return f[1]
    if k == "fn": return "%s(%s)" % (f[1], ",".join(fmt(a) for a in f[2]))
    raise ValueError(k)

# ---------------- term universe / subst ----------------

def subterms(f, bound=()):
    """All subterms of a formula, excluding occurrences of forall-bound names."""
    k = f[0]
    if k in ("const",):
        return set() if f[1] in bound else {(f)}
    if k == "var":
        return set()
    if k == "fn":
        s = set()
        for a in f[2]:
            s |= subterms(a, bound)
        if not any(True for _ in iter_free_vars(f, bound)):
            s.add(f)
        return s
    if k == "atom":
        s = set()
        for a in f[2]:
            s |= subterms(a, bound)
        return s
    if k == "not":
        return subterms(f[1], bound)
    if k in ("imp", "and", "or"):
        return subterms(f[1], bound) | subterms(f[2], bound)
    if k == "forall":
        return subterms(f[2], bound + (f[1],))
    return set()

def iter_free_vars(f, bound=()):
    k = f[0]
    if k == "const":
        if f[1] not in bound:
            yield f
        return
    if k in ("var",):
        return
    if k == "fn":
        for a in f[2]:
            yield from iter_free_vars(a, bound)
        return
    if k == "atom":
        for a in f[2]:
            yield from iter_free_vars(a, bound)
        return
    if k == "not":
        yield from iter_free_vars(f[1], bound); return
    if k in ("imp", "and", "or"):
        yield from iter_free_vars(f[1], bound)
        yield from iter_free_vars(f[2], bound); return
    if k == "forall":
        yield from iter_free_vars(f[2], bound + (f[1],)); return

def ground_terms(memory):
    ts = set()
    for f in memory:
        ts |= subterms(f)
    return sorted(ts, key=fmt)

def subst(f, var, term, bound=()):
    k = f[0]
    if k == "const":
        return term if (f[1] == var and var not in bound) else f
    if k in ("var", "false"):
        return f
    if k == "fn":
        return ("fn", f[1], tuple(subst(a, var, term, bound) for a in f[2]))
    if k == "atom":
        return ("atom", f[1], tuple(subst(a, var, term, bound) for a in f[2]))
    if k == "not":
        return ("not", subst(f[1], var, term, bound))
    if k in ("imp", "and", "or"):
        return (k, subst(f[1], var, term, bound), subst(f[2], var, term, bound))
    if k == "forall":
        if f[1] == var:
            return f
        return ("forall", f[1], subst(f[2], var, term, bound + (f[1],)))
    raise ValueError(k)

# ---------------- forward closure ----------------

def closure(seed_claims, max_levels=200, max_claims=60000):
    """BFS forward closure under S_MP + S_UI + CONTRA.
    Returns (levels: dict claim->level, parent: dict claim->(rule, refs))."""
    mem = []           # sorted list of claims
    have = set()
    level = {}
    parent = {}
    def add(f, lv, rule, refs):
        if f in have:
            return False
        if len(have) >= max_claims:
            raise RuntimeError("claim cap hit")
        have.add(f); mem.append(f); level[f] = lv; parent[f] = (rule, refs)
        return True
    for s in sorted(seed_claims, key=fmt):
        add(s, 0, "SEED", ())
    for lv in range(1, max_levels + 1):
        new = []
        terms = ground_terms(mem)
        imps = sorted([f for f in mem if f[0] == "imp"], key=fmt)
        foralls = sorted([f for f in mem if f[0] == "forall"], key=fmt)
        # S_MP: for each ground G and imp(A,B) with A == G
        gset = have
        for impf in imps:
            a, b = impf[1], impf[2]
            if a in gset:
                new.append((b, "S_MP", (a, impf)))
        # S_UI: forall(v,body), v a plain name
        for ff in foralls:
            v, body = ff[1], ff[2]
            if not re.fullmatch(r"[a-z][a-z0-9_]*", v):
                continue
            for t in terms:
                if fmt(t) == v:
                    continue
                new.append((subst(body, v, t), "S_UI", (ff, t)))
        # CONTRA: F and not(F)
        for f in mem:
            nf = ("not", f)
            if nf in gset:
                new.append((("false",), "CONTRA", (f, nf)))
        added = 0
        for f, rule, refs in sorted(new, key=lambda x: fmt(x[0])):
            if add(f, lv, rule, refs):
                added += 1
        if added == 0:
            break
    return level, parent

# ---------------- file loading ----------------

def load_store(path):
    claims = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                line = line.split(":", 1)[1].strip()
            claims.append(parse(line))
    return claims

def load_form(path):
    pid = store = target = None
    premises, mode = [], None
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("ID:"): pid = line[3:].strip()
            elif line.startswith("STORE:"): store = line[6:].strip()
            elif line == "PREMISES:": mode = "P"
            elif line == "TARGET:": mode = "T"
            elif line == "": mode = None if mode == "T" else mode
            elif mode == "P": premises.append(parse(line))
            elif mode == "T": target = parse(line)
    return pid, store, premises, target

def store_path(store_field):
    # STORE fields resolve relative to docs/lab/math_logic/
    return os.path.expanduser("~/workspace/tnn-lab/math_logic/" + store_field)

# ---------------- per-battery checks ----------------

PBC_ASSUME = {
    "B4X_05": "closes(shop3)",
    "B4X_07": "mammal(nemo9)",
    "B4X_10": "before(t2,t1)",
    "B4X_13": "fire(kitchen2)",
    "B4X_14": "liar(zoe5)",
    "B6X_03": "not(z9)",
}

def check_b4x():
    print("== B4X ==")
    ok = True
    for n in range(1, 16):
        pid = "B4X_%02d" % n
        _, store, premises, target = load_form(os.path.join(BAT, "b4x", pid + ".form"))
        sclaims = load_store(store_path(store))
        seed = sclaims + premises
        assume = PBC_ASSUME.get(pid)
        if assume:
            seed = seed + [parse(assume)]
        level, parent = closure(seed)
        if assume:
            good = ("false",) in level
            depth = level.get(("false",), -1) + 1  # +1 for the S_PBC step
            note = "PBC: false@%d (+1 S_PBC)" % level.get(("false",), -1)
        else:
            good = target in level
            depth = level.get(target, -1)
            note = "depth %d" % depth
        status = "OK" if (good and depth >= 3) else "FAIL"
        if status == "FAIL": ok = False
        print("  %s %-4s derivable=%s %s" % (pid, status, good, note))
    return ok

def shortest_store_items(pid, store_claims, premises, target, assume=None):
    seed = store_claims + premises + ([parse(assume)] if assume else [])
    level, parent = closure(seed)
    goal = ("false",) if assume else target
    if goal not in level:
        return None, None
    store_set = set(store_claims)
    used = set()
    stack = [goal]
    seen = set()
    while stack:
        c = stack.pop()
        if c in seen: continue
        seen.add(c)
        if c in store_set:
            used.add(fmt(c))
        _, refs = parent.get(c, (None, ()))
        for r in refs:
            if isinstance(r, tuple):
                stack.append(r)
    return level[goal], len(used)

def check_b5x():
    print("== B5X ==")
    ok = True
    base = load_store(os.path.join(BAT, "knowledge", "KB_B5X_BASE.md"))
    base_set = set(base)
    for L in (2, 3, 4):
        inj = load_store(os.path.join(BAT, "knowledge", "KB_B5X_L%d.md" % L))
        false_rules = [c for c in inj if c not in base_set]
        assert len(false_rules) == 20 * L, (L, len(false_rules))
        for i in range(1, 21):
            pid = "B5X_L%d_%02d" % (L, i)
            _, store, premises, target = load_form(os.path.join(BAT, "b5x", pid + ".form"))
            kind = "D" if (i % 5) in (1, 2, 3) else "W"
            # (a) sealed verdict == closure verdict on BASE store
            blvl, _ = closure(base + premises)
            sealed = "DERIVED" if target in blvl else "WITHHELD"
            expect = "DERIVED" if kind == "D" else "WITHHELD"
            a_ok = (sealed == expect)
            # (b) injected: false endpoint derivable in exactly L hops, contradicted
            s, t, u, fs = None, None, None, None
            # recover atoms from problem id deterministically
            s = "sd%d_%02d" % (L, i)
            fL = "fd%d_%02d_%d" % (L, i, L)
            chain = [s] + ["fd%d_%02d_%d" % (L, i, k) for k in range(1, L + 1)]
            my_rules = [parse("imp(%s,%s)" % (chain[k], chain[k + 1])) for k in range(L)]
            ilvl, _ = closure(inj + premises)
            fLf = parse(fL)
            b_ok = (fLf in ilvl and ilvl[fLf] == L and
                    parse("not(%s)" % fL) in ilvl)  # trusted premise contradicts
            # (c) ablation: drop any single false rule -> endpoint underivable
            c_ok = True
            for drop in my_rules:
                alvl, _ = closure([c for c in inj if c != drop] + premises)
                if fLf in alvl:
                    c_ok = False
            # (d) single-hop insufficiency: no intermediate consequent contradicted
            #     by trusted content (premises + base)
            trusted = set(base + premises)
            d_ok = True
            for k in range(1, L):
                if parse("not(fd%d_%02d_%d)" % (L, i, k)) in trusted:
                    d_ok = False
            # each single false rule is individually consistent: its consequent
            # is not contradicted by trusted content (same check, k=1..L-1 covers
            # all but endpoint; endpoint IS contradicted - that is the point)
            status = "OK" if (a_ok and b_ok and c_ok and d_ok) else "FAIL"
            if status == "FAIL": ok = False
            if status == "FAIL" or (L == 2 and i <= 2):
                print("  %s %-4s kind=%s sealed=%s false@L=%s ablation=%s singlehop-insuff=%s"
                      % (pid, status, kind, sealed, b_ok, c_ok, d_ok))
    print("  (only failures + L2 samples shown; all others checked silently)")
    return ok

def check_b6x():
    print("== B6X ==")
    ok = True
    expect_items = {"B6X_01": 120, "B6X_02": 110, "B6X_03": 101}
    for pid in ("B6X_01", "B6X_02", "B6X_03"):
        _, store, premises, target = load_form(os.path.join(BAT, "b6x", pid + ".form"))
        sclaims = load_store(store_path(store))
        assume = PBC_ASSUME.get(pid)
        depth, nitems = shortest_store_items(pid, sclaims, premises, target, assume)
        good = depth is not None and nitems >= 100
        status = "OK" if good else "FAIL"
        if not good: ok = False
        print("  %s %-4s depth=%s distinct_store_items=%s (need>=100)" % (pid, status, depth, nitems))
    return ok

def ngrams(words, n):
    return {" ".join(words[i:i + n]) for i in range(len(words) - n + 1)}

def check_b7f_wash():
    print("== B7F wash ==")
    traces = []
    for n in range(1, 23):
        p = os.path.join(TRACES, "TRACE_P%02d.txt" % n)
        with open(p) as f:
            traces.append(f.read().lower())
    corpus = "\n".join(traces)
    corpus_grams = set()
    for t in traces:
        corpus_grams |= ngrams(re.findall(r"[a-z]+", t), 6)
    nl_path = os.path.join(BAT, "sealed", "SEALED_B7F_NL.md")
    with open(nl_path) as f:
        text = f.read()
    problems = re.findall(r"## (B7F_\d+) \[[^\]]+\]\n(.+?)(?=\n## |\Z)", text, re.S)
    assert len(problems) == 20, len(problems)
    ok = True
    for pid, nl in problems:
        grams = ngrams(re.findall(r"[a-z]+", nl.lower()), 6)
        hit = grams & corpus_grams
        status = "OK" if not hit else "FAIL"
        if hit: ok = False
        print("  %s %-4s (%d 6-grams checked%s)" % (pid, status, len(grams),
              "; COLLISION: %s" % sorted(hit)[:3] if hit else ""))
    return ok

def main():
    ok = True
    ok &= check_b4x()
    ok &= check_b5x()
    ok &= check_b6x()
    ok &= check_b7f_wash()
    print("ALL CHECKS PASS" if ok else "SOME CHECKS FAILED")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
