# PREREG: Generality Bias for Procedure Discovery (H-GENBIAS)

**Date:** 2026-09-29
**Status:** FROZEN (committed before implementation)
**Hypothesis H-GENBIAS:** Adding an N-preference generality bias to procedure
discovery search order will cause uniform-length training to yield general
programs (n-1-k) instead of length-specific overfits (3-K), without regressing
on varied training or other tasks.

## Background

- H-STRESS diagnosis (DIAG_RESULT.md, commit a448f834a): slot 0 stored `3-K`
  (not `n-1-k`) because E1 training was uniform length (n=4). The discovery
  search (`pdiscover_direct`) enumerates 1055 programs in fixed syntactic order
  and returns the first fitter. `3-K` (program 250) precedes `n-1-k`
  (program 608). No generality bias exists.
- CC-A3 adversary independently found the same mode: spurious `2-K` fit.
- H-UNIFIED passed 9/9 because its training mixed lengths (n=3, n=2), which
  forced the general program.

## Proposed Fix (Option 1: N-first enumeration preference)

Restructure the final search loop of `pdiscover_direct` (and `pdiscover_dry`
for consistency) into two passes over the already-enumerated program list:

- Pass 1: consider only programs referencing N (node type 1 present),
  in original enumeration order. Return first fitter.
- Pass 2: consider only programs NOT referencing N, in original
  enumeration order. Return first fitter.

Rationale: a program referencing the sequence length N is structurally
capable of generalizing across lengths; a constant-only program cannot adapt
to length. This is a search-order bias only. It changes no program semantics,
adds no new programs, and never performs worse than the old behavior on
Pass 2 fallback.

A helper `prog_uses_n(prog_store, prog_index, pi)` detects N-reference by
scanning node types. A helper `try_discover_pass(..., want_n)` runs one pass.

## Kill Bars (frozen)

- K-G1 (overfit fixed): Uniform n=4 reverse training ("abcd>dcba;efgh>hgfe")
  yields a program that correctly reverses inputs of lengths 2,3,4,5,6,7
  (in particular "hello"->"olleh"). The old code yields `3-K` and fails n=5.
- K-G2 (no regression): Mixed-length reverse ("abc>cba;xy>yx"),
  broadcast-last ("abc>ccc;xy>yy"), broadcast-first ("xqw>xxx;abc>aaa"),
  and identity ("abc>abc;xy>xy") all still discover working programs,
  verified by correct application on multiple lengths.
- K-G3 (stress survives): Re-run of the H-STRESS 16-event sequence with the
  fixed discovery: slot 0 retains a working reverse (K-S3 passes).
  Full K-S1..K-S4 re-evaluation documented; the pre-existing F-LEAK
  (bridge-full slot waste, predicted in the H-STRESS prereg) is out of scope
  and remains a separate known bug.
- K-G4 (determinism): All test runs byte-identical across 3 consecutive runs
  (md5-verified).

## What Counts as Failure

- K-G1 fails if uniform n=4 training still yields a length-specific program.
- K-G2 fails if any previously-working task breaks.
- If N-first ordering introduces a NEW overfit mode (an N-using fitter that
  does not generalize), that is documented as a finding; K-G1 still fails
  unless the found program generalizes.

## Scope

- Bounded to the discovery search order. Not L3 evidence.
- Files: new test harness `genbias_test.zag`; fix ported to
  `unified_learn.zag` (frontier) and `stress_learn.zag` (K-G3 re-run).
- Pure Zag. No Python.

## Commit Order

This prereg is committed before any implementation commit.
