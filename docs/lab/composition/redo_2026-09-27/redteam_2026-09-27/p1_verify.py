"""Independent P1 verification against the COMMITTED drive_redo.py spec.
Rule order (part r+1): 0 reverse, 1 dupfirst, 2 rotleft, 3 droplast, 4 upperfirst, 5 sortchars.
Pairs:   p in 0..29: a=pair_pi(p), b=pair_pj(p), s=tok(14+4p)   [salt C=19]
Triples: t in 0..119: (i,j,k)=triple_pijk(t), s=tok(134+4t)     [salt C=19]
Valid sets recomputed with an independent Python oracle (true rules);
engine answers parsed from committed resp_p1.txt.
"""
import re, itertools, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from family_check import apply_prog

PROG = {  # induced programs (first-consistent), cross-checked vs test_srule.zag
    0: (0, 0, 1, 0, 0, 0, 0, 0),    # reverse
    1: (0, 1, 3, 1, 0, 0, 0, 0),    # dupfirst
    2: (0, 0, 2, 0, 0, 0, 0, 0),    # rotleft
    3: (0, -1, 0, 0, 0, 0, 0, 0),   # droplast
    4: (0, 0, 0, 0, 0, 1, 0, 0),    # upperfirst
    5: (1, 0, 0, 0, 0, 0, 0, 0),    # sortchars
}
NAMES = ["reverse", "dupfirst", "rotleft", "droplast", "upperfirst", "sortchars"]

def true_rule(r, s):
    if r == 0: return s[::-1]
    if r == 1: return s[:1] + s
    if r == 2: return s[1:] + s[:1]
    if r == 3: return s[:-1]
    if r == 4: return s[:1].upper() + s[1:]
    return bytes(sorted(s))

def compose(parts, s):
    for r in parts: s = true_rule(r, s)
    return s

def tok(i):
    c = 19  # all P1 tokens have 14 <= i < 614
    n = 2 + (i % 4)
    return bytes(97 + ((i * 7 + k * c + k * k) % 26) for k in range(n))

def pair_pi(p): return p // 5
def pair_pj(p):
    pi = p // 5; q = p % 5
    return q + 1 if q >= pi else q
def triple_pijk(t):
    i = t // 20; r1 = t % 20
    ji = r1 // 4
    j = ji + 1 if ji >= i else ji
    r2 = r1 % 4
    rem = [x for x in range(6) if x != i and x != j]
    return (i, j, rem[r2])

def _evdir():
    # walk up from this script to find the repo evidence dir
    d = os.path.dirname(os.path.abspath(__file__))
    for _ in range(8):
        cand = os.path.join(d, "docs", "lab", "composition", "redo_2026-09-27")
        if os.path.isdir(cand):
            return cand
        d = os.path.dirname(d)
    return "docs/lab/composition/redo_2026-09-27"  # fallback: repo-relative
EVDIR = _evdir()

def main():
    # sanity: induced programs == true rules on all P1 tokens
    for idx in [14 + 4 * p for p in range(30)] + [134 + 4 * t for t in range(120)]:
        s = tok(idx)
        for r in range(6):
            assert apply_prog(list(s), *PROG[r]) == true_rule(r, s), (r, s)
    print("induced==true on all 150 P1 tokens: OK")
    tot = valid = strict = amb = 0
    bad = []
    for run in ("run1", "run2", "run3"):
        lines = open(os.path.join(EVDIR, run, "resp_p1.txt")).read().splitlines()
        items = [ln for ln in lines if ln.startswith("P1 ")]
        assert len(items) == 150, (run, len(items))
        for ln in items:
            m = re.match(r"P1 (pair|triple) ([\d,]+) tok (\d+) want=(\[[\d, ]+\]) valid=(\[.*\]) gotnums=(\[[\d, ]+\]) pass_valid=(\d) pass_strict=(\d)", ln)
            kind, ab, ti, want_s, valid_s, got_s, pv, ps = m.groups()
            idxs = [int(x) for x in ab.split(",")]
            want = [int(x) for x in re.findall(r"\d+", want_s)]
            got = [int(x) for x in re.findall(r"\d+", got_s)]
            rec_valid = eval(valid_s)
            s = tok(int(ti)); y = compose([w - 1 for w in want], s)
            mine = sorted([[x + 1 for x in seq] for seq in
                           itertools.permutations(range(6), len(want))
                           if compose(seq, s) == y])
            if mine != sorted(rec_valid):
                bad.append((run, kind, ab, ti, "valid-list mismatch", mine, rec_valid))
                continue
            tot += 1
            if got in mine: valid += 1
            else: bad.append((run, kind, ab, ti, "got not in valid set", got, mine))
            if got == want: strict += 1
            if len(mine) > 1: amb += 1
            assert int(pv) == (1 if got in mine else 0)
            assert int(ps) == (1 if got == want else 0)
    print(f"runs checked: 3; items={tot} valid_set_hits={valid} strict_hits={strict} ambiguous={amb}")
    for b in bad[:10]: print("BAD:", b)

if __name__ == "__main__":
    main()
