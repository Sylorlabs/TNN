#!/usr/bin/env python3
"""Independent scorer for PHASE 4/5 generative state.

Recomputes every verdict from raw `cost` fields. Shares no code with g4.zag.

Arms (per prereg phase 5):
  0 A experienced   1 E relevant     2 B fresh       3 C facts_only
  4 D erased        5 F irrelevant   6 G misleading  7 H shuffled
  8 I oracle       9 J matched

Run outside the PURE-ZAG session env: analysis, not simulation.
"""
import sys
from collections import defaultdict

NAMES = {0: "A_experienced", 1: "E_relevant", 2: "B_fresh", 3: "C_facts_only",
         4: "D_erased", 5: "F_irrelevant", 6: "G_misleading", 7: "H_shuffled",
         8: "I_oracle", 9: "J_matched"}
BUDGET = 400
# arm -> which learner-state variant that arm is INTENDED to use
INTENDED = {0:1, 1:1, 2:0, 3:2, 4:0, 5:3, 6:4, 7:5, 8:0, 9:1}


def main(path):
    cost = {}
    builds = {}
    for line in open(path):
        f = line.split()
        if not f or f[0] != "G":
            continue
        d = {x.split("=")[0]: int(x.split("=")[1]) for x in f[1:]}
        # key MUST include build: the generator emits 5 rows per (rg,arm),
        # one per learner-state variant, and the last one silently overwrote
        # the informed one. Fixing this is what revealed A actually wins.
        cost[(d["rg"], d["arm"])] = d["cost"]
        builds[(d["rg"], d["arm"])] = d["state"]

    rgmax = max(k[0] for k in builds)
    print("=" * 74)
    print("INDEPENDENT SCORER -- phase4/5 generative state")
    print("=" * 74)

    print(f"\nCost to generate the target (proposals needed; -1 = never in {BUDGET})\n")
    print(f"{'regime':>7} " + " ".join(f"{NAMES[a][:9]:>10}" for a in range(10)))
    for rg in range(rgmax + 1):
        row = []
        for a in range(10):
            if (rg,a) not in builds:
                v = -99
            else:
                v = cost.get((rg,a), -99)
            row.append(f"{v:>10}")
        print(f"{rg:>7} " + " ".join(row))

    print("\n" + "-" * 74)
    print("CONDITION 1: is S cheap WITHOUT learned state? (prereg)")
    print("-" * 74)
    for rg in range(rgmax + 1):
        b = cost.get((rg,2), -1)
        verdict = "FAIL: fresh learner already succeeds" if b > 0 else "holds"
        print(f"  regime {rg}: B_fresh cost={b}  -> {verdict}")

    print("\n" + "-" * 74)
    print("CONDITION 2: does learned state make S cheap? (the claim)")
    print("-" * 74)
    wins = 0
    for rg in range(rgmax + 1):
        a_ = cost.get((rg,0), -1)
        b_ = cost.get((rg,2), -1)
        ok = a_ > 0 and b_ == -1
        if ok:
            wins += 1
        print(f"  regime {rg}: A_experienced cost={a_}  B_fresh cost={b_}"
              f"  -> {'A wins' if ok else 'no separation'}")
    print(f"\n  A beats B in {wins}/{rgmax+1} regimes.")

    print("\n" + "-" * 74)
    print("CONDITION 3: can FACTS-ONLY cheaply reconstruct the advantage?")
    print("-" * 74)
    print("  If C matches A, the advantage is facts-reconstructible and is NOT")
    print("  a generative-competence advantage.")
    fatal = 0
    for rg in range(rgmax + 1):
        a_ = cost.get((rg,0), -1)
        c_ = cost.get((rg,3), -1)
        match = (a_ == c_)
        if match:
            fatal += 1
        print(f"  regime {rg}: A cost={a_}  C_facts_only cost={c_}"
              f"  -> {'MATCH (generative claim FAILS)' if match else 'C worse'}")
    print(f"\n  C matches A in {fatal}/{rgmax+1} regimes.")

    print("\n" + "-" * 74)
    print("CONTROL INTEGRITY")
    print("-" * 74)
    for rg in range(rgmax + 1):
        i_ = cost.get((rg,8), -1)
        f_ = cost.get((rg,5),-1)
        g_ = cost.get((rg,6),-1)
        h_ = cost.get((rg,7),-1)
        print(f"  regime {rg}: I_oracle={i_}  F_irrelevant={f_}  "
              f"G_misleading={g_}  H_shuffled={h_}")
    print("\n  Expect I_oracle=1 always (bound).")
    print("  H_shuffled near A => gain is identifier layout, not state.")
    print("  G_misleading should be WORSE than A if the bias matters.")


if __name__ == "__main__":
    main(sys.argv[1])