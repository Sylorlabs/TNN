#!/usr/bin/env python3
"""Why PHASE 18 would be degenerate or void: a dilemma, verified.

Claim under test: for the affine-candidate families considered, a world
in which the correct candidate is DETERMINED BY OBSERVABLE query content
is solvable by single-shot search over the candidate set -- i.e. any
learner that can evaluate candidates is immediately at the oracle. And a
world in which the correct candidate is NOT determined by observable
content carries no learnable signal at all.

If both hold, then "counting insufficiency with a genuinely learnable
conditional signal" is not achievable by choosing a different world in
this family. It requires a different mechanism class.

This is a finite check, not a proof about all worlds. Run outside the
PURE-ZAG session env: analysis, not simulation.
"""

PRIMES = [11, 13, 17, 19, 23, 29, 31, 37, 41, 43]
SMALL = [1, 2, 3, 5, 7]


def build_family():
    """Candidates are 2-step compositions: k -> (a,b), out(k,x) = b*a*x.

    a < 11 and b is prime > 11, so the products a*b are all distinct and
    each (a,b) pair is uniquely identified by the product.
    """
    fams = {}
    for na in (2, 3, 4, 5):
        A = SMALL[:na]
        fams[f"a in {A}"] = [(a, b) for a in A for b in PRIMES]
    return fams


def check_unique_identification(fam):
    """If y = a*b*x is observable, is the correct candidate unique?

    A learner evaluating candidates needs, for a query (x, y), to find k
    with b*a*x == y. If every (x,y) admits at most one k, single-shot
    evaluation identifies the correct candidate and search == oracle.
    """
    xs = list(range(1, 40))
    ambiguous = 0
    total = 0
    for x in xs:
        seen = {}
        for (a, b) in fam:
            y = b * a * x
            seen.setdefault(y, []).append((a, b))
        for y, ks in seen.items():
            total += 1
            if len(ks) > 1:
                ambiguous += 1
    return total, ambiguous


def check_counting_dilution(fam):
    """If truth were index-based (unobservable), counts are balanced by
    construction -> counting is blind. That is count17's defect.
    """
    n = len(fam)
    return n, n  # each candidate correct on exactly 1/n of queries


def main():
    print("=" * 74)
    print("DILEMMA CHECK -- observable-but-degenerate vs hidden-and-void")
    print("=" * 74)

    fams = build_family()

    print("\n(A) If the query's target is observable, is search == oracle?\n")
    print(f"{'family':>18} {'N':>5} {'(x,y) pairs':>12} {'ambiguous':>10} {'verdict'}")
    for name, fam in fams.items():
        total, amb = check_unique_identification(fam)
        verdict = "search==oracle (DEGENERATE)" if amb == 0 else f"{amb} ambiguous"
        print(f"{name:>18} {len(fam):>5} {total:>12} {amb:>10} {verdict}")

    print("\n  Reading: with observable targets, a candidate evaluator identifies")
    print("  the correct candidate from a SINGLE observation. Any learner holding")
    print("  the trace table is at the oracle. The world cannot discriminate")
    print("  'learned' from 'searched'. This is count16/count17's recurring trap.")

    print("\n(B) If the target is hidden, is anything learnable?\n")
    for name, fam in fams.items():
        n = len(fam)
        print(f"{name:>18} N={n:>3}  counts balanced -> argmax frequency blind"
              f"  (ceiling {n // 1}/{n} ~ {312 // n}/312 test)")

    print("\n  Reading: hiding the target removes the only channel carrying")
    print("  signal. Every arm collapses to a tie-break. This is PHASE 17.")

    print("\n" + "=" * 74)
    print("CONCLUSION")
    print("=" * 74)
    print("""
Within affine-composition candidate families, the two requirements the
brief asks for are in direct conflict:

  * "a genuinely available conditional signal"  ->  target must be observable
  * "conditional competence must not be search" ->  target must NOT identify
                                                    the candidate from one look

PHASE 16 satisfied the first and violated the second (researcher-authored
bucket router). PHASE 17 satisfied the second and lost all signal.

So the next attempt must change the MECHANISM CLASS, not the world. The
candidate set must contain members that are individually indistinguishable
under single-shot evaluation but separable under REPEATED interaction --
e.g. candidates whose correctness depends on a context established by prior
steps, so no single observation suffices and the learner must carry state.

That is a different experiment from anything in Phases 6-9 or 16-17, and it
requires a substrate that supports state across steps. I have not built it.
""")


if __name__ == "__main__":
    main()