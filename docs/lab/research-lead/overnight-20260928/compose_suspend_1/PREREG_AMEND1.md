# PREREG_AMEND1.md -- loop-guard correction (committed before any implementation commit)

Date: 2026-10-03. Status: FROZEN (amends PREREG.md Section 1.2).

## What changed

PREREG.md Section 1.2 specified the assembly loop guard as: "a
(need-kind, producer-id) pair already on the open need stack fails
that producer choice immediately."

A debug build of the as-specified guard (before any kill-bar run)
enumerated 42 candidates for Q1 instead of the walkthrough's
sequence, because the guard permits depth-2 same-producer nesting:
m0's sub-need call returns [m0(C)] via direct close even when
(m0's need, m0) is on the stack, and the outer m0 frame then forms
m0(m0(C)). Concretely the Q1 candidate list contained
m1(m0(m0(C))) etc., and demand would execute X twice
(X(202)=211 and X(211)=-2), falsifying F-B3's exec[m0]==1 which the
COMPOSE-GENERAL-1 walkthrough (5.4) requires: Y's alternatives must
be exactly [Y(C202), Y(X(C202))].

## Replacement rule (frozen)

The loop guard is path-based: a producer already on the current
root-to-leaf derivation path fails that producer choice ENTIRELY
(no direct close, no sub-need expansion). The need stack therefore
holds producer ids, not (need, producer) pairs.

## Why this is still general (no shape knowledge)

The rule quantifies only over producer identity along the current
path: "never apply the same structure twice on one derivation
path." It mentions no diamond, fan-out, chain, or domain. It
reproduces the 5.4 walkthrough exactly (Q1: 20 candidates;
Y-alts = [Y(C), Y(X(C))]) and preserves the CHAIN3 nesting the
prereg requires (c1(c0(C)) is allowed because c0 != c1; only the
same producer re-applying to its own output path is blocked).
Termination is still guaranteed (path length <= inventory size);
SMAX remains as a backup cap.

## Effect on frozen predictions

None of the Section 3 kill-bar predictions change; the amendment
makes F-B3's exec[m0]==1 achievable as specified. The regression
bars are unaffected (verified by re-tracing CHAIN3, FANIN,
PARTIAL, Q2 under the path guard before this amendment).
