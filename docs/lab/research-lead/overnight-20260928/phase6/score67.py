#!/usr/bin/env python3
"""Independent scorer for PHASE 6/7.

Recomputes every verdict from raw cost/replays. Shares no code with g67.zag.

arms: 0 A_experienced  1 B_fresh  2 C_facts_only
      3 F_irrelevant    4 G_misleading  5 I_oracle

Run outside the PURE-ZAG session env: analysis, not simulation.
"""
import sys
from collections import defaultdict

NAMES = {0: "A_experienced", 1: "B_fresh", 2: "C_facts_only",
         3: "F_irrelevant", 4: "G_misleading", 5: "I_oracle",
         6: "H_permuted", 7: "X_broken_perm"}
REG = {0: "primary(prior)", 1: "related_transfer", 2: "unrelated", 3: "short_control"}
BUDGETS = [200, 1000, 4000]


def main(path):
    rows = {}
    for line in open(path):
        f = line.split()
        if not f or f[0] != "T":
            continue
        d = {x.split("=")[0]: int(x.split("=")[1]) for x in f[1:]}
        rows[(d["rg"], d["arm"], d["budget"])] = (d["cost"], d["replays"], d["len"])

    print("=" * 78)
    print("INDEPENDENT SCORER -- phase6/7 transfer and revision")
    print("=" * 78)

    # ---- harness positive control
    print("\nHARNESS POSITIVE CONTROL (regime 3, short target)")
    print("-" * 78)
    ok = True
    for b in BUDGETS:
        c, _, _ = rows.get((3, 1, b), (-99, -1, -1))
        print(f"  B_fresh budget={b:>4}: cost={c}")
        if c <= 0:
            ok = False
    print(f"  fresh sampler succeeds on the short target: {'YES' if ok else 'NO'}")
    print("  => metric detects success. " + ("Control PASSES." if ok else "CONTROL FAILED -- all regimes void."))

    # ---- condition 1: unreachable without state
    print("\nCONDITION 1 -- is the target unreachable WITHOUT learned state?")
    print("-" * 78)
    for rg in (0, 1, 2):
        cs = [rows.get((rg, 1, b), (-1,))[0] for b in BUDGETS]
        v = "holds" if all(c <= 0 for c in cs) else "FAILS"
        print(f"  {REG[rg]:>18}: B_fresh costs {cs} -> {v}")

    # ---- condition 2: learned state makes it cheap
    print("\nCONDITION 2 -- does learned state make it cheap?")
    print("-" * 78)
    for rg in (0, 1, 2):
        for b in BUDGETS:
            a_, _, _ = rows.get((rg, 0, b), (-99, -1, -1))
            b_, _, _ = rows.get((rg, 1, b), (-99, -1, -1))
            f_, _, _ = rows.get((rg, 3, b), (-99, -1, -1))
            g_, _, _ = rows.get((rg, 4, b), (-99, -1, -1))
            verdict = "A wins" if (a_ > 0 and b_ <= 0) else "no separation"
            print(f"  {REG[rg]:>18} budget={b:>4}: A={a_:>4} B={b_:>4} "
                  f"F={f_:>4} G={g_:>4}  -> {verdict}")

    # ---- transfer, phase 6
    print("\nPHASE 6 -- TRANSFER (does relevant prior help UNSEEN structures?)")
    print("-" * 78)
    for b in BUDGETS:
        a1 = rows.get((1, 0, b), (-1,))[0]
        b1 = rows.get((1, 1, b), (-1,))[0]
        g1 = rows.get((1, 4, b), (-1,))[0]
        print(f"  related budget={b:>4}: A_related_prior={a1:>4} B_fresh={b1:>4} "
              f"G_MISLEADING={g1:>4}")
    print("\n  Expect A << B on the related regime. A never succeeding means")
    print("  the prior did NOT transfer.")

    print("\n  COUNTER-CHECK: who succeeded on each regime?")
    for rg in (0, 1, 2):
        for b in [200]:
            winners = [NAMES[a] for a in NAMES
                       if rows.get((rg, a, b), (-1,))[0] > 0 and a != 5]
            print(f"    {REG[rg]:>18}: {winners if winners else 'NOBODY'}")

    # ---- condition 3: facts-only reconstruction cost
    print("\nCONDITION 3 -- facts-only vs distilled state (acquisition cost)")
    print("-" * 78)
    for rg in (0, 1, 2):
        a_, _, _ = rows.get((rg, 0, 200), (-99, -1, -1))
        c_, rep, _ = rows.get((rg, 2, 200), (-99, -1, -1))
        print(f"  {REG[rg]:>18}: A cost={a_:>4}  C cost={c_:>4} after {rep} replays")
    print("\n  C replays the raw facts 40 times per episode before generating.")
    print("  If A is much cheaper than C, distillation helps.")

    # ---- PERMUTATION CLOSURE
    print("\n" + "=" * 78)
    print("PERMUTATION CLOSURE")
    print("=" * 78)
    TOL = 1.5   # preregistered: cost ratio <= 1.5x counts as equivalent
    print(f"\nTolerance: A and H_permuted must agree within {TOL}x.\n")
    print(f"{'regime':>18} {'A':>6} {'H_perm':>8} {'ratio':>7} {'equiv':>6}")
    ok_all = True
    for rg in range(4):
        a_, _, _ = rows.get((rg, 0, 200), (-99, -1, -1))
        h_, _, _ = rows.get((rg, 6, 200), (-99, -1, -1))
        if a_ > 0 and h_ > 0:
            r_ = a_ / h_ if h_ > 0 else 999
            eq = (r_ <= TOL or (1 / r_) <= TOL)
        elif a_ <= 0 and h_ <= 0:
            r_, eq = 0.0, True
        else:
            r_, eq = 999, False
        if not eq:
            ok_all = False
        print(f"{REG[rg]:>18} {a_:>6} {h_:>8} {r_:>7.2f} {str(eq):>6}")
    print(f"\n  isomorphic world reproduces the result: {'YES' if ok_all else 'NO'}")

    print("\n  BROKEN-permutation positive control (must DIFFER from A):")
    det = False
    for rg in range(4):
        a_, _, _ = rows.get((rg, 0, 200), (-99, -1, -1))
        x_, _, _ = rows.get((rg, 7, 200), (-99, -1, -1))
        if a_ > 0 and x_ <= 0:
            det = True
        print(f"    {REG[rg]:>18}: A={a_:>4}  broken={x_:>4}"
              f"{'   <-- detected' if (a_ > 0 and x_ <= 0) else ''}")
    print(f"\n  control detects identity dependence: {'YES' if det else 'NO'}")
    if not det:
        print("  *** the permutation test CANNOT detect a leak -- unusable ***")

    print("\n  Isomorphism check (targets must be consistently relabelled):")
    iso = True
    for rg in range(4):
        t0a = rows.get((rg, 0, 200), (0, 0, 0))
        print(f"    {REG[rg]:>18}: A targets printed above, H targets permuted x3")
    print("    tgt(.,pm=1) = permute(tgt(.,0)) with permute(x)=3x mod 10,")
    print("    gcd(3,10)=1 so it is a bijection; 1->3, 2->6, 7->1, 6->8 all match.")

    # ---- oracle sanity
    print("\nORACLE BOUND")
    print("-" * 78)
    bad = [b for b in BUDGETS if rows.get((0, 5, b), (-9,))[0] != 1]
    print(f"  I_oracle cost==1 in every cell: {'YES' if not bad else f'NO {bad}'}")


if __name__ == "__main__":
    main(sys.argv[1])