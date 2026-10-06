#!/usr/bin/env python3
"""Independent scorer for P5-meta4 (successor to p5meta3).

Acquisition is measured on queries NEVER OBSERVED in the prior phase, so a
retained-fact cache cannot replay and M4 becomes a real test of machinery. Recomputes every bar from raw acquisition
costs. Shares no code with m5.zag.

arms: 0 FRESH 1 RELEVANT 2 IRRELEVANT 3 MISLEADING 4 META_ABLATED 5 ORACLE_META

Run outside the PURE-ZAG session env: analysis, not simulation.
"""
import sys

ARMS = {0: "FRESH", 1: "RELEVANT", 2: "IRRELEVANT",
        3: "MISLEADING", 4: "META_ABLATED", 5: "ORACLE_META"}
FAMS = 4


def main(path):
    acq = {}
    pk = {}
    for line in open(path):
        f = line.split()
        if not f or f[0] != "FP":
            continue
        d = {}
        for x in f[1:]:
            if "=" not in x:
                continue
            k, v = x.split("=", 1)
            d[k] = int(v) if v.lstrip("-").isdigit() else v
        acq[(d["regime"], d["arm"])] = d["acq"]
        pk[(d["regime"], d["arm"])] = d["pk"]

    print("=" * 74)
    print("INDEPENDENT SCORER -- P5-meta4 learning-to-learn")
    print("=" * 74)

    print("\nAcquisition cost (trials to 3 consecutive correct; 40 = never)\n")
    hdr = f"{'family':>8}" + "".join(f"{ARMS[a]:>14}" for a in range(6))
    print(hdr)
    for fm in range(FAMS):
        row = f"{fm:>8}"
        for a in range(6):
            row += f"{acq.get((fm, a), -1):>14}"
        print(row)

    def mean(a):
        return sum(acq.get((fm, a), 40) for fm in range(FAMS)) / FAMS

    print("\n" + "-" * 74)
    print("BARS")
    print("-" * 74)

    m1 = all(acq.get((fm, 1), 40) < acq.get((fm, 0), 0) for fm in range(FAMS))
    print(f"M1 RELEVANT < FRESH in every family            : {m1}")
    print(f"     RELEVANT mean {mean(1):.2f}  vs  FRESH mean {mean(0):.2f}")

    diffs = [abs(acq.get((fm, 2), 0) - acq.get((fm, 0), 0)) for fm in range(FAMS)]
    m2 = all(d <= 1 for d in diffs)
    print(f"\nM2 IRRELEVANT neutral (|diff| <= 1 per family)  : {m2}")
    print(f"     per-family diffs {diffs}   IRRELEVANT mean {mean(2):.2f}")

    mis = [acq.get((fm, 3), 40) for fm in range(FAMS)]
    frs = [acq.get((fm, 0), 40) for fm in range(FAMS)]
    m3a = all(m >= f for m, f in zip(mis, frs))
    m3b = all(m <= f for m, f in zip(mis, frs))
    print(f"\nM3 MISLEADING harmful (>= FRESH)               : {m3a}")
    print(f"   or revised to <= FRESH                       : {m3b}")
    print(f"     MISLEADING mean {mean(3):.2f}  vs  FRESH mean {mean(0):.2f}")

    # M4 is substantive only if ablating MACH COSTS something. lost==0 means the
    # speedup survived the ablation entirely -> the prior acted as a fact cache.
    lost = sum(acq.get((fm, 4), 0) - acq.get((fm, 1), 0) for fm in range(FAMS))
    m4 = lost > 0
    print(f"\nM4 META_ABLATED loses the RELEVANT advantage   : {m4}")
    print(f"     cost of ablation, total trials: {lost}")
    print(f"     META_ABLATED mean {mean(4):.2f}  vs  RELEVANT mean {mean(1):.2f}")
    if lost == 0:
        print("     *** ablation cost ZERO: the speedup is a RETAINED-FACT CACHE ***")

    m5 = all(acq.get((fm, 5), 99) <= acq.get((fm, 1), 0) for fm in range(FAMS))
    print(f"\nM5 ORACLE_META <= RELEVANT (sanity)             : {m5}")
    print(f"     ORACLE mean {mean(5):.2f}  RELEVANT mean {mean(1):.2f}")

    print("\n" + "=" * 74)
    print("VERDICT")
    print("=" * 74)
    if m1 and m4 and m2:
        print("""
M1, M4 and M2 all hold: relevant prior reduces acquisition cost, ablating the
learned machinery removes the speedup, and irrelevant prior is neutral.

That is the signature of learning-to-learn rather than a cache -- but note the
ablation removes MACH entirely, so what survived the ablation is whatever the
FACTS lookup alone provides. If META_ABLATED equals FRESH, the prior contributed
only retained facts and the 'speedup' was never machinery.""")
    elif m1 and not m4:
        print("""
NEGATIVE: M1 holds but M4 FAILS. Ablating the learned machinery (MACH) while
KEEPING the retained facts cost ZERO extra trials. The acquisition speedup is
therefore RETAINED TASK STATE -- a cache of (query,answer) pairs -- and not
learned learning machinery. Per the prereg this is explicitly NOT meta-learning.""")
    else:
        print("""
NEGATIVE. On the prereg's own rule the prior is not learning-to-learn. See the
per-bar output above for which bar failed and why.""")
    if not m2:
        print("\nM2 FAILS: irrelevant prior was NOT neutral -- it changed acquisition.")
    if not m3a and not m3b:
        print("\nM3 FAILS: misleading prior neither hurt nor was revised.")


if __name__ == "__main__":
    main(sys.argv[1])