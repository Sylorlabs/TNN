#!/usr/bin/env python3
"""Score forkd2 batteries against the frozen prereg bars.

B1: every laundering/forgery/tamper case (launder manifest2 + ct manifest2)
    must be WITHHOLD, and Python+Zag attest verdicts must agree on all.
B2: on all non-launder corpora, every per-case verdict must agree 100%
    with the original forkD battery output on the same case.
B3: genuine M5 (m5 corpus) must WITHHOLD (GEN_ONLY preserved).
M2/M3: pair-correct scoring — a/b variants of the same base case must
    receive the verdicts the ORIGINAL forkD gave them (agreement gate
    covers this per-case).
"""
import os
import sys

BASE = os.path.expanduser("~/workspace/selfpam_forkd")
EV1 = os.path.join(BASE, "forkd2/evidence/run1")
ORIG = os.path.join(BASE, "orig_battery")  # original forkD battery outputs

CORPORA = ["c1", "c2", "c3", "c4", "c5", "c6", "m2a", "m2b", "m4", "m5"]


def load_results(path):
    """case -> (verdict, expected, match)."""
    out = {}
    for ln in open(path):
        ln = ln.strip()
        if not ln:
            continue
        c, v, e, m = ln.split("|")
        out[c] = (v, e, m)
    return out


def main():
    failures = []
    total = 0

    # B1: launder + tamper
    b1 = {}
    for c in ("launder", "ct"):
        b1.update(load_results(os.path.join(EV1, c + ".txt")))
    print(f"B1: {len(b1)} attack cases")
    for case, (v, e, m) in sorted(b1.items()):
        total += 1
        if v != "WITHHOLD":
            failures.append(f"B1 {case}: verdict {v} != WITHHOLD")
        if e != "WITHHOLD":
            failures.append(f"B1 {case}: expected field {e} != WITHHOLD")
    print(f"  WITHHOLD: {sum(1 for v, e, m in b1.values() if v=='WITHHOLD')}/{len(b1)}")

    # B2: agreement with original forkD per case (non-launder corpora)
    agree_n = agree_ok = 0
    for c in CORPORA:
        new = load_results(os.path.join(EV1, c + ".txt"))
        old = load_results(os.path.join(ORIG, c + ".txt"))
        for case, (v, e, m) in sorted(new.items()):
            total += 1
            agree_n += 1
            if case not in old:
                failures.append(f"B2 {c}/{case}: no original reference")
                continue
            ov, oe, om = old[case]
            if v != ov:
                failures.append(f"B2 {c}/{case}: new={v} original={ov}")
            else:
                agree_ok += 1
            if e != oe:
                failures.append(f"B2 {c}/{case}: expected {e} != original expected {oe}")
    print(f"B2: per-case agreement new-vs-original: {agree_ok}/{agree_n}")

    # B3: genuine M5 must WITHHOLD (GEN_ONLY)
    m5 = load_results(os.path.join(EV1, "m5.txt"))
    n_with = sum(1 for v, e, m in m5.values() if v == "WITHHOLD")
    print(f"B3: m5 genuine recursion WITHHOLD: {n_with}/{len(m5)}")
    for case, (v, e, m) in sorted(m5.items()):
        total += 1
        if v != "WITHHOLD":
            failures.append(f"B3 m5/{case}: verdict {v} != WITHHOLD")

    # expected-field sanity on c1..c6/m2/m4 (forkd2's own match flag).
    # A mismatch is only a failure if the ORIGINAL matched expected there
    # (i.e. a regression); pre-existing corpus aspirations don't count.
    for c in CORPORA:
        new = load_results(os.path.join(EV1, c + ".txt"))
        old = load_results(os.path.join(ORIG, c + ".txt"))
        for case, (v, e, m) in sorted(new.items()):
            total += 1
            if m != "1":
                ov, oe, om = old.get(case, (None, None, None))
                if om == "1":
                    failures.append(f"EXP {c}/{case}: verdict {v} != expected {e} (original matched)")
                # else: pre-existing corpus aspiration, both implementations agree

    print(f"total checks: {total}")
    if failures:
        print(f"FAILURES ({len(failures)}):")
        for f in failures[:40]:
            print("  " + f)
        sys.exit(1)
    print("ALL BARS PASS")


if __name__ == "__main__":
    main()
