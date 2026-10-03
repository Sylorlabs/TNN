# Preregistration: Procedure Invention via Compositional Index-Program Search

**Date:** 2026-09-29 07:15 PDT
**Status:** FROZEN (before implementation)
**Builder:** Procedure-Invention Builder (subagent)
**Branch:** tnn-native-lab

## Architectural Hypothesis

**H-PROC:** A learner can invent reusable string-transformation procedures by:
1. Extracting index sequences from input-output examples (output[k] = input[idx[k]]).
2. Searching a compositional space of index programs (functions of position k and length n).
3. Selecting the smallest program that reproduces all observed sequences.
4. Storing the program as an executable procedure for novel inputs.

**Mechanism family:** P-E (structure-growth search) with P-B (trace compression) elements.

## Index Program Language

An index program computes output position mapping: given (k, n), return input index.

**Terminals:**
- `K`: output position (0 <= k < m, where m = output length)
- `N`: input length
- `C0`, `C1`, `C2`: small constants (0, 1, 2)

**Operators:**
- `ADD(a, b)`: a + b
- `SUB(a, b)`: a - b

**Examples (not in source as named procedures):**
- Identity: `K`
- Reverse: `SUB(SUB(N, C1), K)` = n-1-k

**Search:** Enumerate all programs up to size 5 (nodes), test each against
observed index sequences from training examples. Select smallest that fits all.

## Why This Is Not a Menu

The search space contains all compositional programs up to size 5 from
{ K, N, C0, C1, C2, ADD, SUB }. This is hundreds of candidates, not a named list.
The learner must discover which composition fits the data. The specific solution
(e.g., `SUB(SUB(N,C1),K)`) is not stored or named in source.

## Test Families

### PI-1a: Reverse (primary)
- Train: ("abc"→"cba"), ("def"→"fed"), ("xy"→"yx"), ("hello"→"olleh")
- Hidden: ("zag"→"gaz"), ("12345"→"54321"), ("q"→"q")
- Expected invented program: `SUB(SUB(N,C1),K)`

### PI-1b: Identity (control for generality)
- Train: ("abc"→"abc"), ("xy"→"xy")
- Hidden: ("hello"→"hello")
- Expected invented program: `K`
- **Purpose:** Proves mechanism is not reverse-specific. If it only works for
  reverse, H-PROC is KILLED.

## L3 Procedure Criteria (from directive, adapted)

1. Final procedure not in source: The specific program (e.g., n-1-k) is not
   written as a named procedure. Only primitives and search exist.
2. Not enumerated as complete candidate: Search space is compositional (100s of
   programs), not a menu.
3. Created after experience: Program selected based on training examples.
4. Persistent state: Program stored as data structure, printable.
5. White-box trace: Search log shows candidates tested and selection.
6. Hidden instances solved: Test on unseen strings.
7. Ablation: Without the invented program, cannot solve (baseline: memorization).
8. Reused later: Apply to multiple hidden cases.
9. Transfers: Works on different alphabets (letters vs digits).
10. Beats memorization: Memorization baseline fails on hidden (not in training).
11. Red team: Independent adversary (separate agent) attacks.
12. Revision: (Deferred; not in v1 scope. Documented as limitation.)

## Kill Bars (frozen)

**K-P1 (Reverse-specificity):** If mechanism solves PI-1a (reverse) but fails
PI-1b (identity), then it is reverse-tuned, not general. H-PROC KILLED.

**K-P2 (Menu):** If the effective search space is < 20 distinct programs (i.e.,
the "compositional" claim is false and it's really a tiny menu), H-PROC KILLED.
(Measured by counting candidates actually generated.)

**K-P3 (Memorization):** If a pure memorization baseline (store training pairs,
output WITHHOLD on unseen) achieves equal hidden-test score, H-PROC provides
no advantage. H-PROC KILLED for utility (though mechanism may still be L3).

**K-P4 (Source contamination):** If governance audit finds "reverse", "n-1-k",
or equivalent logic hardcoded (not via search), H-PROC INVALID.

**K-P5 (Single-character):** If hidden test with single char ("q"→"q") fails,
the program does not handle edge cases. H-PROC WEAKENED (not killed, but
bounded).

## Success Bars

H-PROC SURVIVES (v1) if:
- PI-1a: 3/3 hidden correct (including single-char).
- PI-1b: 1/1 hidden correct.
- K-P1 through K-P4 all pass (not killed).
- Search space > 20 programs (K-P2).
- Memorization baseline scores 0/3 on hidden (K-P3).

This constitutes **bounded L3** for procedure invention (criteria 1-11 except 12).

## Implementation Plan

1. Implement index-sequence extractor (Zag).
2. Implement program enumerator (size-bounded search).
3. Implement verifier (test program against sequences).
4. Implement applier (use program to transform novel input).
5. Test PI-1a, PI-1b.
6. Implement memorization baseline for K-P3.
7. Commit with full trace.

## Pure Zag

All implementation, search, and testing in Zag. No Python.

## Frozen

No thresholds adjusted post-hoc. If bars are wrong, amend transparently and re-freeze.
