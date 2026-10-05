#!/usr/bin/env python3
"""Independent scorer for PHASE 17.

Parses the raw output of c17 and computes EVERY verdict. It shares no code
with the generator and never reads a verdict emitted by it.

Usage: python3 score17.py <raw-file>
"""
import sys
from collections import defaultdict

ARMS = {
    0: "COUNT", 1: "RECENCY", 2: "RANDOM", 3: "FIXED_CTX",
    4: "FACTS_ONLY", 5: "EXHAUSTIVE", 6: "LEARNED", 7: "SHUFFLED", 8: "ORACLE",
}
BOUNDS = {"EXHAUSTIVE", "ORACLE"}
NS = [5, 10, 20, 30, 50]

# Analytically derived BEFORE execution (prereg): a query-blind rule emits one
# fixed candidate, and each candidate is correct on ceil(H/N) test queries, so
# any query-blind arm is capped at that number regardless of N.
def query_blind_ceiling(n):
    q = 625 - 313            # 312 test contexts
    return -(-q // n)        # ceil(q/n)


def main(path):
    hits = defaultdict(int)      # (rg,n,arm) -> correct
    total = defaultdict(int)     # (rg,n,arm) -> trials
    counts = {}                  # (rg,n) -> {cand: count}
    # recency / regime analysis: correct-by-position within regime 2
    early = defaultdict(int); early_tot = defaultdict(int)
    late = defaultdict(int); late_tot = defaultdict(int)

    cur_rg = cur_n = None
    for line in open(path):
        f = line.split()
        if not f:
            continue
        if f[0] == "SECTION":
            d = {x.split("=")[0]: int(x.split("=")[1]) for x in f[1:]}
            cur_rg, cur_n = d["regime"], d["N"]
            counts[(cur_rg, cur_n)] = {}
        elif f[0] == "COUNT" and cur_rg is not None:
            counts[(cur_rg, cur_n)][int(f[1])] = int(f[2])
        elif f[0] == "Q":
            d = {x.split("=")[0]: int(x.split("=")[1]) for x in f[1:]}
            key = (d["rg"], d["N"], d["arm"])
            total[key] += 1
            if d["chosen"] == d["truth"]:
                hits[key] += 1
                if d["rg"] == 2:
                    b = early if d["t"] < 400 else late
                    b[(d["N"], d["arm"])] += 1
            if d["rg"] == 2:
                b = early_tot if d["t"] < 400 else late_tot
                b[(d["N"], d["arm"])] += 1

    print("=" * 78)
    print("INDEPENDENT SCORER -- all verdicts recomputed from raw chosen/truth")
    print("=" * 78)

    print("\nQ-A/Q-B: does any arm beat the analytic query-blind ceiling?\n")
    print(f"{'rg':>3} {'N':>4} {'ceiling':>8} " + " ".join(f"{ARMS[a]:>11}" for a in ARMS))
    beats = []
    for rg in (0, 1, 2):
        for n in NS:
            ceil_ = query_blind_ceiling(n)
            row = []
            for a in ARMS:
                c = hits.get((rg, n, a), 0)
                row.append(f"{c:>11}")
            mark = ""
            qb = [ARMS[a] for a in (0, 1, 3) if hits.get((rg, n, a), 0) > ceil_]
            if qb:
                mark = "  <-- QUERY-BLIND ARM EXCEEDS CEILING: BUG"
            print(f"{rg:>3} {n:>4} {ceil_:>8} " + " ".join(row) + mark)
            for a in (6, 7):
                if hits.get((rg, n, a), 0) > ceil_:
                    beats.append((rg, n, ARMS[a], hits[(rg, n, a)]))
    if any(m for rg in (0, 1, 2) for n in NS
           for m in [any(hits.get((rg, n, a), 0) > query_blind_ceiling(n) for a in (0, 1, 3))]):
        print("\n*** INVARIANT VIOLATED: a query-blind arm beat its own bound.")
        print("*** The generator's ceiling is wrong; verdicts below are suspect.")
    else:
        print("\nInvariant OK: no query-blind arm exceeds its analytic ceiling.")

    print("\nLearned arms that strictly exceed the ceiling:\n")
    if not beats:
        print("  NONE. LEARNED and SHUFFLED never beat query-blind selection.")
    for rg, n, name, c in beats:
        print(f"  regime {rg} N={n:>3}: {name} = {c} > ceiling {query_blind_ceiling(n)}")

    print("\nQ-C: is the LEARNED gain real, or a researcher-authored router?\n")
    for rg in (0, 1, 2):
        for n in NS:
            d = hits.get((rg, n, 6), 0) - hits.get((rg, n, 7), 0)
            print(f"  regime {rg} N={n:>3}: LEARNED={hits.get((rg,n,6),0):>4} "
                  f"SHUFFLED={hits.get((rg,n,7),0):>4}  delta={d:>4}")
    print("\n  If LEARNED >> SHUFFLED, the gain comes from the trace-matching")
    print("  rule, not from identifier layout. If they match, it is layout luck.")

    print("\nQ-D: transfer -- does LEARNED hold up as N grows?\n")
    for rg in (0, 1, 2):
        seq = [hits.get((rg, n, 6), 0) for n in NS]
        ceils = [query_blind_ceiling(n) for n in NS]
        print(f"  regime {rg} LEARNED across N={NS}: {seq}")
        print(f"          ceilings               : {ceils}")

    print("\nQ-E: does misleading/regime-change experience get revised? (regime 2)\n")
    for n in NS:
        le, lt = hits.get((2, n, 6), 0), 0
        e_t, l_t = early_tot.get((n, 6), 0), late_tot.get((n, 6), 0)
        le = early.get((n, 6), 0)
        lt = late.get((n, 6), 0)
        ce, cl = early.get((n, 0), 0), late.get((n, 0), 0)
        print(f"  N={n:>3}  LEARNED early {le}/{e_t} late {lt}/{l_t}"
              f"   |   COUNT early {ce}/{early_tot.get((n,0),0)}"
              f" late {cl}/{late_tot.get((n,0),0)}")
    print("\n  A mechanism that revises should not be worse after the change.")

    print("\n\nBOUNDS (not competitors): EXHAUSTIVE and ORACLE are search ceilings.\n")
    for rg in (0,):
        for n in NS:
            print(f"  regime {rg} N={n:>3}: EXHAUSTIVE={hits.get((rg,n,5),0):>4} "
                  f"ORACLE={hits.get((rg,n,8),0):>4}  (312 trials each)")


if __name__ == "__main__":
    main(sys.argv[1])