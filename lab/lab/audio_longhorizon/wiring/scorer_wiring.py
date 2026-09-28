#!/usr/bin/env python3
# scorer_wiring.py — frozen scorer for PREREG_LH K-W1 / K-W2 (wiring ablation).
# FROZEN before scored runs. Offline Python: reads committed journal artifacts,
# never touches the per-episode path.
#
# K-W1 ABLATION-DEAD: live vs ablate-constant action distributions must differ
#   with p < 0.01 (permutation test, 10000 permutations, L1 distance between
#   normalized 5-action count vectors). p >= 0.01 -> KILLED.
# K-W2 ABLATION-DIRECTIONAL: on episodes where live and ablated actions differ,
#   sign(ablated_ord - live_ord) must agree >= 70% (i.e. the ablation pushes
#   actions in a consistent direction, tracking the descriptor change).
#   < 70% -> WIRING-DECORRELATED.
#
# Action ordinals (frozen wiring vocabulary v1):
#   QUERY=0, CONTINUE=1, NOTE_NEW=2, RECALL=2, ATTEND=3.
# Usage: scorer_wiring.py <journal_live> <journal_const> [<journal_shuffle>]
import sys, math, random

ORD = {"QUERY": 0, "CONTINUE": 1, "NOTE_NEW": 2, "RECALL": 2, "ATTEND": 3}
ACTIONS = ["QUERY", "CONTINUE", "NOTE_NEW", "RECALL", "ATTEND"]

def parse_journal(path):
    eps = []  # list of (turn, action_name, ordinal)
    turn = None
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("EP "):
                turn = int(line[3:].split()[0])
            elif line.startswith("ACTION "):
                name = line.split()[1]
                eps.append((turn, name, ORD[name]))
    return eps

def count_vec(eps):
    v = [0]*5
    for _, name, _ in eps:
        v[ACTIONS.index(name)] += 1
    return v

def l1(a, b):
    n1 = sum(a); n2 = sum(b)
    return sum(abs(x/n1 - y/n2) for x, y in zip(a, b))

def permutation_p(live_eps, const_eps, nperm=10000, seed=12345):
    # statistic: L1 distance between normalized action-count vectors
    obs = l1(count_vec(live_eps), count_vec(const_eps))
    combined = [("L", e) for e in live_eps] + [("C", e) for e in const_eps]
    nL = len(live_eps)
    rng = random.Random(seed)
    ge = 0
    for _ in range(nperm):
        rng.shuffle(combined)
        lv = [e for _, e in combined[:nL]]
        cv = [e for _, e in combined[nL:]]
        if l1(count_vec(lv), count_vec(cv)) >= obs - 1e-12:
            ge += 1
    return (ge + 1) / (nperm + 1), obs

def sign_agreement(live_eps, const_eps):
    diffs = []
    for (t1, _, o1), (t2, _, o2) in zip(live_eps, const_eps):
        assert t1 == t2, "episode order mismatch"
        if o1 != o2:
            diffs.append(o2 - o1)
    if not diffs:
        return 0.0, 0, []
    pos = sum(1 for d in diffs if d > 0)
    neg = sum(1 for d in diffs if d < 0)
    agree = max(pos, neg) / len(diffs)
    return agree, len(diffs), diffs

def main():
    if len(sys.argv) < 3:
        print("usage: scorer_wiring.py <journal_live> <journal_const> [<journal_shuffle>]")
        sys.exit(2)
    live = parse_journal(sys.argv[1])
    const = parse_journal(sys.argv[2])
    assert len(live) == len(const) and len(live) > 0, "episode count mismatch/empty"
    print(f"episodes: {len(live)}")
    print(f"live actions:    {count_vec(live)}  " + str([n for _, n, _ in live]))
    print(f"const actions:   {count_vec(const)}  " + str([n for _, n, _ in const]))

    p, obs = permutation_p(live, const)
    print(f"K-W1: perm p={p:.5f} (L1 obs={obs:.4f}, 10000 perms)")
    w1 = "PASS" if p < 0.01 else "KILLED"
    print(f"K-W1 verdict: {w1} (bar: p < 0.01)")

    agree, ndiff, diffs = sign_agreement(live, const)
    print(f"K-W2: differing episodes={ndiff}, sign agreement={agree:.3f}")
    print(f"  ordinal diffs (const-live): {diffs}")
    w2 = "PASS" if agree >= 0.70 else "WIRING-DECORRELATED"
    print(f"K-W2 verdict: {w2} (bar: >= 0.70)")

    if len(sys.argv) >= 4:
        shuf = parse_journal(sys.argv[3])
        ps, obss = permutation_p(live, shuf)
        print(f"shuffle supplementary: perm p={ps:.5f} (L1 obs={obss:.4f})")
        print(f"shuffle actions: {count_vec(shuf)}")

    overall = "WIRING-WORKS" if (w1 == "PASS" and w2 == "PASS") else "WIRING-FAILS"
    print(f"OVERALL: {overall}")
    sys.exit(0 if overall == "WIRING-WORKS" else 1)

if __name__ == "__main__":
    main()
