#!/usr/bin/env python3
"""ARM INVARIANT AUDIT -- the systemic defect class.

Repeated defect in this lane: an arm does not execute the state/mechanism its
label claims. It happened at least four times:
  * phase4: "shuffled" arm silently duplicated treatment A
  * phase6: armBuild had no case for arms 6,7 -> fell through to fresh
  * phase10: permutation arm had fld=0 -> received no state at all
  * phase10: principle field was the ONLY field written -> arms crippled

This auditor verifies EXECUTION IDENTITY from the state a run actually used,
not from names. Every arm must emit a causal fingerprint:

  FP <arm> <state_hash> <cfg_hash> <space_hash> <perm_hash>

state_hash  : hash of the learner-state buffer contents the arm really used
cfg_hash    : hash of the mechanism configuration (which fields increment)
space_hash  : hash of the candidate/construction space definition
perm_hash   : hash of the permutation actually applied

The auditor then enforces structural invariants over the raw table:
  I1  no duplicate (experiment, regime, arm, seed) rows
  I2  no missing arms in any (experiment, regime, seed) cell
  I3  arms declared IDENTICAL really have equal fingerprints
  I4  arms declared DIFFERENT really have different fingerprints
  I5  a shuffled/permuted arm's fingerprint != the treatment it copies
  I6  an ERASED arm's fingerprint == the FRESH arm's where intended
  I7  fingerprints are present and well-formed for every row

Usage:  arm_audit.py <raw-file> [--spec spec.json]
Exit 0 = all invariants hold.
"""
import sys
import hashlib
from collections import defaultdict

REQUIRED = ("arm", "state", "cfg", "space", "perm")


def parse(line):
    f = line.split()
    if not f or f[0] != "FP":
        return None
    d = {}
    for tok in f[1:]:
        if "=" in tok:
            k, v = tok.split("=", 1)
            d[k] = v
    return d


def load(path):
    rows = []
    for n, line in enumerate(open(path), 1):
        d = parse(line)
        if d:
            for k in REQUIRED:
                if k not in d:
                    sys.stderr.write(f"FAIL I7 line {n}: fingerprint missing {k}\n")
                    return None
            rows.append(d)
    return rows


def cell(d):
    return (d.get("exp", "?"), d.get("regime", "?"), d.get("seed", "0"))


def audit(rows, spec):
    fails = []

    # I1 duplicates
    seen = defaultdict(int)
    for d in rows:
        seen[cell(d) + (d["arm"],)] += 1
    dups = {k: v for k, v in seen.items() if v > 1}
    if dups:
        fails.append(("I1", f"duplicate rows: {sorted(dups)[:6]}"))

    # I2 missing arms
    by_cell = defaultdict(set)
    for d in rows:
        by_cell[cell(d)].add(d["arm"])
    expected = set(spec.get("arms", []))
    for c, got in by_cell.items():
        miss = expected - got
        if miss and expected:
            fails.append(("I2", f"cell {c} missing arms {sorted(miss)}"))

    # I3 / I4 declared identity relations
    fp = {}
    for d in rows:
        fp[(cell(d), d["arm"])] = (d["state"], d["cfg"], d["space"], d["perm"])
    for c, arms in by_cell.items():
        for a, b in spec.get("identical", []):
            if a in arms and b in arms:
                if fp[(c, a)] != fp[(c, b)]:
                    fails.append(("I3", f"{c}: {a} declared=={b} but fingerprints differ"))
        for a, b in spec.get("different", []):
            if a in arms and b in arms:
                if fp[(c, a)] == fp[(c, b)]:
                    fails.append(("I4", f"{c}: {a} declared!={b} but fingerprints IDENTICAL "
                                        f"(arm did not run its own state)"))

    # I5 permuted arm must not equal its source
    for a, src in spec.get("permuted_from", {}).items():
        for c, arms in by_cell.items():
            if a in arms and src in arms:
                if fp[(c, a)] == fp[(c, src)]:
                    fails.append(("I5", f"{c}: permuted arm {a} is IDENTICAL to {src}"))

    # I6 erased == fresh where intended
    for a, b in spec.get("erased_equals", []):
        for c, arms in by_cell.items():
            if a in arms and b in arms:
                if fp[(c, a)] != fp[(c, b)]:
                    fails.append(("I6", f"{c}: erased {a} != fresh {b}"))

    return fails


def main():
    path = sys.argv[1]
    spec_path = None
    if "--spec" in sys.argv:
        spec_path = sys.argv[sys.argv.index("--spec") + 1]
    import json
    spec = json.load(open(spec_path)) if spec_path else {}

    rows = load(path)
    if rows is None:
        print("RESULT=FAIL (I7 malformed fingerprints)")
        sys.exit(1)
    if not rows:
        print("RESULT=FAIL (no FP rows found -- generator emits no fingerprints)")
        sys.exit(1)

    fails = audit(rows, spec)
    print(f"fingerprint rows: {len(rows)}")
    if not fails:
        print("RESULT=PASS all arm-execution invariants hold")
        sys.exit(0)
    seen_i = set()
    for i, msg in fails:
        if i not in seen_i:
            seen_i.add(i)
            print(f"{i} VIOLATION: {msg}")
    print(f"RESULT=FAIL violations={len(fails)}")
    sys.exit(1)


if __name__ == "__main__":
    main()
