# Preregistration: Content-Conditional Procedure Discovery

**Date:** 2026-09-29 07:35 PDT
**Researcher:** Content-Conditional Procedure Researcher (subagent)
**Branch:** tnn-native-lab
**Status:** FROZEN (committed before implementation)

## Hypothesis

**H-CC:** The procedure discovery mechanism (proc_learn.zag) can be extended
with content-conditional programs of the form IF(input[0]==v, A, B), where A
and B are index programs from the existing search space, such that:

1. The extended search space remains tractable (<100k programs).
2. The search directly finds the content-conditional program for the
   H-REVISE counterexample without the Revision Bridge.
3. No regression: simple cases (reverse, broadcast-last) still find base
   programs.
4. No hallucination: simple cases do not get spurious conditionals.

## Background

From PROC_REVISION_RESULT.md (H-REVISE KILLED):
- Program signature P(k,n)->index cannot express "IF input[0]=='x'".
- Mathematical proof: P(k,3)=2 and P(k,3)=0 contradictory for identical inputs.
- Five revision capabilities absent, including conditional representation.

The Revision Bridge works around this with IF/ELSE, but it is a separate
mechanism. This experiment tests whether the program search itself can be
extended to find content-conditional programs directly.

## Design

### Extended Program Language

**Base programs** (unchanged): 1055 programs from {K,N,C0,C1,C2,ADD,SUB},
size <= 5. Signature: P(k,n) -> index.

**Conditional programs**: IF(EQ0(v), A, B)
- Predicate EQ0(v): true iff input[0] == v, where v is a byte value.
- Branches A, B: base programs of size <= 3 (55 programs: 5 size-1 + 50 size-3).
- Semantics: if input[0]==v then evaluate A(k,n) else evaluate B(k,n).
- Signature: P(k,n,input) -> index.

**Candidate values v**: Distinct bytes appearing at position 0 across all
training inputs. Extracted from data, not hardcoded.

**Search space size**:
- Base: 1055
- Conditional: V * 55 * 55, where V = distinct pos-0 bytes in training.
- For H-REVISE training: V=3 ('a','x','d'), so 3*3025=9075 conditionals.
- Total: 10,130. Well under 100k.

**Search order** (prevents hallucination):
1. Phase 1: Search base programs (smallest first). If found, DONE.
2. Phase 2: Only if no base program fits, search conditionals
   (ordered by then_size+else_size, then pred_val, then indices).

This two-phase order guarantees K-CC4 by construction: simple cases find
base programs and never consider conditionals.

### Predicted Program for H-REVISE

Training:
- ("abc"->"ccc"): broadcast-last, seq [2,2,2], n=3
- ("xy"->"yy"): broadcast-last, seq [1,1], n=2
- ("defg"->"gggg"): broadcast-last, seq [3,3,3,3], n=4
- ("xab"->"xxx"): broadcast-first (counterexample), seq [0,0,0], n=3

Predicted: IF(input[0]=='x', C0, SUB(N,C1))
- THEN branch C0: size 1, program index 2 (C0 is 3rd terminal: K=0,N=1,C0=2)
- ELSE branch SUB(N,C1): size 3, this is broadcast-last
- Predicate v='x' (120)

## Kill Bars (frozen)

**K-CC1 (Tractability):** Total enumerated programs < 100,000.
FAIL if >= 100k.

**K-CC2 (Finds conditional):** Search finds a program of form
IF(input[0]=='x', C0, SUB(N,C1)) (or semantically equivalent) that correctly
handles all 4 training sequences including the counterexample.
FAIL if NO PROGRAM FOUND or wrong program.

**K-CC3 (No regression):** On pure reverse training ("abc"->"cba",
"def"->"fed"), search finds the base program n-1-k (not a conditional).
On pure broadcast-last training, finds n-1 (not a conditional).
FAIL if regression.

**K-CC4 (No hallucination):** For training data where a base program fits,
the found program MUST be a base program (Phase 1 success), never a
conditional. FAIL if conditional returned when base suffices.

## Test Cases

1. **H-REVISE counterexample**: 4 sequences (3 broadcast-last + 1 broadcast-first).
   Expect: conditional program found.

2. **Pure reverse**: ("abc"->"cba"), ("def"->"fed").
   Expect: base program n-1-k, no conditional.

3. **Pure broadcast-last**: ("abc"->"ccc"), ("xy"->"yy").
   Expect: base program n-1, no conditional.

4. **Program count**: Verify total < 100k.

## What Success Looks Like

Search finds IF(input[0]=='x', C0, SUB(N,C1)) directly for the H-REVISE
case, while still finding simple base programs for simple cases. This
would show the program search can subsume the Revision Bridge for
content-conditional procedures.

## What Failure Looks Like

- Search space explodes (>=100k).
- Cannot find the conditional program.
- Hallucinates conditionals for simple cases.
- Regression on reverse/broadcast-last.

## Scope Limitations (acknowledged upfront)

1. Predicates limited to position 0. Other positions not tested.
2. Branches limited to size <= 3. Larger branches not enumerated.
3. Single predicate only (no nested IFs, no AND/OR).
4. Candidate values from training data only.

These are principled bounds for tractability, not ad-hoc patches.
Future work can extend them if this succeeds.

## Pure Zag Compliance

Implementation, compilation, execution in Zag only. No Python.
Toolchain: znc 2026.07.0-dev.

## Commit Order

1. This prereg (FROZEN).
2. Implementation.
3. Results.
