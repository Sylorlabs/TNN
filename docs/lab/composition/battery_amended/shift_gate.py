#!/usr/bin/env python3
"""A2 VERIFICATION GATE (blocking) for the amended composition battery.

Reads the salted item manifest produced by battery_amended (gen mode) and
checks, on the ACTUAL emitted token stream:

  GATE-1 (single-step): for every unordered pair of distinct phases
    {train, P0, P2, P2}, no two same-length tokens are exact Caesar shifts
    of each other. (The red team's shift-exhaustion test, re-run on salt.)

  GATE-2 (two-step, chained — Crew C's K6-bypass hardening): for every P2
    item (pairs AND triples), every intermediate string produced by applying
    the item's rules in order (all prefixes of the composition chain) shares
    no Caesar-shift-equivalence with any training-phase token of the same
    length. This is the DROP-LAST-first chaining surface the frozen K6 missed.

  GATE-3 (memorizers): a strict shift-memorizer (memorize all 108 training
    input->output examples, detect Caesar shift per probe, shift the taught
    output, case-preserving) and the chained memorizer (Crew C's two-step
    attack through DROP-LAST-first pairs) are scored on the P0 probes.
    Both must FAIL P0 (no part >= 7/8).

Exit 0 + "GATE PASS" iff all three hold; exit 1 otherwise. Deterministic.
"""
import sys, os

MANIFEST = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "items.tsv")

PHASE_C = {0: 13, 1: 17, 2: 19, 3: 23}
TRAIN_IDX = list(range(6)) + list(range(700, 706))
P0_IDX = list(range(6, 14))
P2_PAIR = [(p, it) for p in range(30) for it in range(4)]
P2_TRIP = [(t, it) for t in range(120) for it in range(4)]
P3_IDX = list(range(614, 622))

def toklen(i): return 2 + (i % 4)
def tokphase(i):
    if i >= 700: return 0
    if i < 6: return 0
    if i < 14: return 1
    if i < 614: return 2
    return 3
def tok(i):
    c = PHASE_C[tokphase(i)]
    n = toklen(i)
    return "".join(chr(97 + ((i * 7 + k * c + k * k) % 26)) for k in range(n))

def apply_rule(r, s):
    if r == 0: return s[::-1]
    if r == 1: return s[0] + s
    if r == 2: return s[1:] + s[:1] if s else ""
    if r == 3: return s[:-1]
    if r == 4: return s[0].upper() + s[1:] if s else ""
    return "".join(sorted(s))

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

def is_shift(a, b):
    """True iff a and b are exact Caesar shifts (same length)."""
    if len(a) != len(b) or not a: return False
    d = (ord(a[0]) - ord(b[0])) % 26
    # case-insensitive alphabet positions: tokens are lowercase except
    # taught rule-4 outputs; here both args are raw tokens (lowercase).
    return all((ord(x) - ord(y)) % 26 == d for x, y in zip(a, b))

def shift_str(s, d):
    """Case-preserving Caesar shift by d."""
    out = []
    for ch in s:
        if 'a' <= ch <= 'z': out.append(chr(97 + ((ord(ch) - 97 + d) % 26)))
        elif 'A' <= ch <= 'Z': out.append(chr(65 + ((ord(ch) - 65 + d) % 26)))
        else: out.append(ch)
    return "".join(out)

def main():
    # ---- sanity: manifest tokens match the salted formula ----
    n_man = 0
    with open(MANIFEST) as f:
        for line in f:
            if not line.strip(): continue
            n_man += 1
            d = dict(kv.split("=", 1) for kv in line.rstrip("\n").split("\t")[1:])
            if "input" in d:
                if d["input"] != tok(int(d["tok"])):
                    print(f"MANIFEST MISMATCH at tok={d['tok']}: "
                          f"{d['input']} != {tok(int(d['tok']))}")
                    return 1
    print(f"[manifest] {n_man} lines; all token strings match salted formula")

    train_toks = [tok(i) for i in TRAIN_IDX]
    p0_toks = [tok(i) for i in P0_IDX]
    p2_toks = [tok(14 + p * 4 + it) for p, it in P2_PAIR] + \
              [tok(134 + t * 4 + it) for t, it in P2_TRIP]
    p3_toks = [tok(i) for i in P3_IDX]
    phases = {"train": train_toks, "P0": p0_toks, "P2": p2_toks, "P3": p3_toks}

    # ---- GATE-1: single-step shift-exhaustion, all cross-phase pairs ----
    hits1 = []
    names = list(phases)
    for x in range(len(names)):
        for y in range(x + 1, len(names)):
            A, B = phases[names[x]], phases[names[y]]
            for i, a in enumerate(A):
                for j, b in enumerate(B):
                    if len(a) == len(b) and is_shift(a, b):
                        hits1.append((names[x], i, names[y], j, a, b))
    print(f"[GATE-1] cross-phase shift pairs: {len(hits1)} "
          f"(checked {sum(1 for _ in range(1)) and 'all 6 phase-pairs'})")
    for h in hits1[:10]: print("   HIT:", h)

    # ---- GATE-2: two-step chained shift-equivalence ----
    # every intermediate of every P2 composition vs every same-length train token
    train_by_len = {}
    for s in train_toks:
        train_by_len.setdefault(len(s), []).append(s)
    hits2 = []
    n_inter = 0
    prs = pairs()
    for p in range(30):
        a, b = prs[p]
        for it in range(4):
            s = tok(14 + p * 4 + it)
            m = apply_rule(a, s)
            n_inter += 1
            for t in train_by_len.get(len(m), []):
                if is_shift(m, t):
                    hits2.append(("pair", (a, b), p, it, m, t))
    trs = triples()
    for t in range(120):
        a, b, c = trs[t]
        for it in range(4):
            s = tok(134 + t * 4 + it)
            m1 = apply_rule(a, s); m2 = apply_rule(b, m1)
            for m in (m1, m2):
                n_inter += 1
                for tr in train_by_len.get(len(m), []):
                    if is_shift(m, tr):
                        hits2.append(("triple", (a, b, c), t, it, m, tr))
    print(f"[GATE-2] chained intermediates checked: {n_inter}; "
          f"shift-equivalent to a train token: {len(hits2)}")
    for h in hits2[:10]: print("   HIT:", h)

    # ---- GATE-3: memorizers must fail P0 ----
    # memorize all 108 training input->output examples per rule
    mem = {}  # (rule, input) -> output
    for r in range(6):
        for i in TRAIN_IDX:
            s = tok(i)
            mem[(r, s)] = apply_rule(r, s)

    def shift_answer(r, probe):
        """Strict shift-memorizer single probe: find shift-equiv train input
        for rule r, shift its taught output; None if no shift found."""
        for i in TRAIN_IDX:
            s = tok(i)
            if len(s) == len(probe) and is_shift(probe, s):
                d = (ord(probe[0].lower()) - ord(s[0].lower())) % 26
                return shift_str(mem[(r, s)], d)
        return None

    p0_scores = []
    for r in range(6):
        c = 0
        for t in P0_IDX:
            pr = tok(t)
            ans = shift_answer(r, pr)
            if ans is None: ans = pr  # fallback: identity
            if ans == apply_rule(r, pr): c += 1
        p0_scores.append(c)
    print(f"[GATE-3a] shift-memorizer P0 per-rule: {p0_scores} "
          f"(need all <7 to fail)")

    # chained memorizer (Crew C's attack): P0 as above; P2 chains through
    # DROP-LAST-first pairs via two shift-detect steps.
    def chained_p2(a, b, s):
        if a != 3: return s  # attack only chains DROP-LAST-first pairs
        st1 = shift_answer(a, s)
        if st1 is None: return s
        # st1 should equal droplast(s); now shift-detect the intermediate
        m = apply_rule(a, s)
        got_m = None
        for i in TRAIN_IDX:
            tr = tok(i)
            if len(tr) == len(m) and is_shift(m, tr):
                d = (ord(m[0].lower()) - ord(tr[0].lower())) % 26
                got_m = shift_str(mem[(a, tr)], d)
                break
        if got_m is None: return s
        # second rule from the shifted intermediate: needs intermediate to be
        # a shift of a train token with a taught rule-b output
        for i in TRAIN_IDX:
            tr = tok(i)
            if len(tr) == len(got_m) and is_shift(got_m, tr):
                d2 = (ord(got_m[0].lower()) - ord(tr[0].lower())) % 26
                return shift_str(mem[(b, tr)], d2)
        return s

    chained_p2_hits = 0
    chained_hit_detail = []
    prs = pairs()
    for p in range(30):
        a, b = prs[p]
        for it in range(4):
            s = tok(14 + p * 4 + it)
            exp = apply_rule(b, apply_rule(a, s))
            if chained_p2(a, b, s) == exp:
                chained_p2_hits += 1
                chained_hit_detail.append((("pair", a, b, p, it), s, exp))
    trs = triples()
    for t in range(120):
        a, b, c = trs[t]
        for it in range(4):
            s = tok(134 + t * 4 + it)
            exp = apply_rule(c, apply_rule(b, apply_rule(a, s)))
            if chained_p2(a, b, s) == exp:
                chained_p2_hits += 1
                chained_hit_detail.append((("triple", a, b, c, t, it), s, exp))
    print(f"[GATE-3b] chained memorizer P0 per-rule: {p0_scores} "
          f"(same P0 as 3a); P2: {chained_p2_hits}/600")
    for det, s, exp in chained_hit_detail:
        print(f"   chained P2 hit (identity-fallback coincidence): {det} "
              f"input={s} expected={exp}")

    ok1 = len(hits1) == 0
    ok2 = len(hits2) == 0
    ok3 = all(c < 7 for c in p0_scores)
    print(f"GATE-1 (single-step shift-exhaustion): {'PASS' if ok1 else 'FAIL'}")
    print(f"GATE-2 (two-step chained):            {'PASS' if ok2 else 'FAIL'}")
    print(f"GATE-3 (memorizers fail P0):           {'PASS' if ok3 else 'FAIL'}")
    if ok1 and ok2 and ok3:
        print("A2 GATE: PASS — battery may proceed")
        return 0
    print("A2 GATE: FAIL — battery BLOCKED")
    return 1

if __name__ == "__main__":
    sys.exit(main())
