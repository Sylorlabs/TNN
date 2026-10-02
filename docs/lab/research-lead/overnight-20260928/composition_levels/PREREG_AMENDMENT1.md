# PREREG AMENDMENT 1: Composition Three Levels

Date: 2026-10-02. Before any experimental runs.
Status: Transparent amendment to PREREG.md (commit 4c15fe32d).

## What Changed

K1: "L1-TREAT ans=105 with COMP-SEGS n=2" -> "L1-TREAT ans=107
with COMP-SEGS n=2".

K3: "L1-REUSE ans=105" -> "L1-REUSE ans=107".

Test Design L1 section:
- X: was plen-2 [1,1] (11->12->13), now plen-3 [1,1,1] (11->12->13->14).
- Y: was plen-2 [2,2] (21->22->23), now plen-3 [2,2,2] (21->22->23->24).
- Z facts: was plen-4 (101->105), now plen-6 (101->107).
- Query: was (101,70,105), now (101,70,107).

L2 and L3 Z facts lengthened correspondingly (Z target 108 instead
of 106); their expected FAIL (-2) results are unchanged.

## Why

The prereg's plen-4 Z risked being solvable by trial alone, which
would weaken the L1-FRESH control (K2). A plen-6 Z exceeds trial's
practical construction bound, ensuring FRESH=-2 genuinely tests
whether composition (not trial) is necessary. This STRENGTHENS the
causal claim; it does not weaken any bar.

## When

Decided during driver implementation, before compilation and before
any runs. No results were known when this amendment was written.

## Impact

K1 and K3 are evaluated against ans=107 (not 105). All other kill
bars (K2, K4-K8) are unaffected. The scientific claim "L1 exact reuse
works via 2-segment composition" is unchanged; only the concrete
literal values differ.

This amendment is committed before the results commit, preserving
prereg-before-results ordering.
