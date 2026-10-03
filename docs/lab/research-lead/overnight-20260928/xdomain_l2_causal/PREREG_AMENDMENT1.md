# PREREG AMENDMENT 1 (pre-implementation, transparent)

Filed 2026-10-02, before any implementation file is written. Re-freezes
the battery with one numeric correction. All kill bars K1-K10 unchanged.

## Correction

PREREG.md, "Inventory" teaching block, stated:

- D_COUNT: 11 -> 2; 21 -> 3.

This is wrong. The frozen world facts give each subject exactly one r=91
fact: (11,91,12) is the only r=91 fact with subject 11, and (21,91,22)
is the only r=91 fact with subject 21. Therefore:

- D_COUNT: 11 -> 1; 21 -> 1. Learned signature remains NODE -> NUM
  (homogeneous observations; the kind outcome is unchanged).

## Impact review

- No kill bar depends on the D_COUNT output values. In every arm,
  D_COUNT outputs (1) still differ from every query target (101, 102,
  999), so all TRY-PAIR / TRY-SINGLE failure expectations are unchanged.
- The teaching observations (11 -> 1, 21 -> 1) remain kind-homogeneous,
  so finalize_sig still yields NODE -> NUM.
- Mismatch-pair enumeration, adapter candidate order, and all
  ADAPT-TRY expectations are unaffected (D_COUNT is never an adapter
  candidate: its signature is NODE -> NUM).

## Reason

Caught during pre-implementation numeric verification of the frozen
world facts against the teaching block. Corrected before implementation,
not after results.
