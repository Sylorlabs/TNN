# Prereg: Family X (broadcast-last) Test of Frozen Procedure-Invention Mechanism

**Role:** Procedure-Invention Builder
**Date:** 2026-09-29
**Status:** PREREGISTERED. Committed before any Family X execution.
**Governing assignment:** pi_adversary/PI_FAMILY_X_ASSIGNMENT.md (seal verified:
6438bc799b8c29fe3c60f73ca0082c57fea31ec5d7037c01513db874200fbc9d)

## Background

The Builder's v1 mechanism (sem_l3/proc_learn.zag) found SUB(N,C1)-equivalent
`n-1-k` for REVERSE. The Adversary downgraded the "bounded L3" claim to
"mechanism validation" because REVERSE was pre-named in NEXT_FRONTIER_DESIGN.md.
This prereg covers the Adversary-assigned undisclosed family as the true test.

## Family X (adversary-assigned)

**broadcast-last:** output[k] = input[n-1] for all k. Output length = input length.

Training (assigned, public):
1. ("abc" -> "ccc")
2. ("xy" -> "yy")
3. ("defg" -> "gggg")

This family was not named in any design doc, prereg, or prior discussion.
The Builder's enumeration was designed for the reverse investigation, not for
broadcast-last.

## Hypothesis (H-FX)

The FROZEN mechanism (primitives {K,N,C0,C1,C2,ADD,SUB}, enumeration sizes
1/3/5 in fixed order, smallest-fitting selection) discovers the broadcast-last
program from the three training pairs with NO source change except the
training-data substitution, because the target program SUB(N,C1) lies in the
size-3 enumeration space and is the smallest program consistent with all three
extracted sequences.

## Predicted extracted sequences

- ("abc"->"ccc"): 'c' occurs once in "abc", at index 2. seq0 = [2,2,2], n=3.
- ("xy"->"yy"): 'y' occurs once in "xy", at index 1. seq1 = [1,1], n=2.
- ("defg"->"gggg"): 'g' occurs once in "defg", at index 3. seq2 = [3,3,3,3], n=4.

No extraction ambiguity: each output character is unique in its input.

## Predicted found program (hand-derived before running)

Enumeration order: indices 0-4 = K,N,C0,C1,C2; 5-54 = ADD(a,b) over terminals;
55-104 = SUB(a,b) over terminals; then size 5.

- Size 1: K varies with k (no). N gives n, not the sequences (no). C0/C1 are
  wrong constants. C2=[2,2,2] fits seq0 but not seq1 ([1,1]). None fit all three.
- Size-3 ADD (5-54): need value 2 at n=3, 1 at n=2, 3 at n=4, constant across k.
  ADD(N,C0)=n (no), ADD(N,C1)=n+1 (no), ADD(K,.) varies with k (no),
  constant pairs give fixed values 0..4, none of which equal {2,1,3} across
  n={3,2,4}. None fit.
- Size-3 SUB (55-104), index = 55 + a*5 + b:
  a=0 (K): SUB(K,K)=0, SUB(K,N)=k-n, SUB(K,C0)=k, SUB(K,C1)=k-1,
  SUB(K,C2)=k-2. None constant-2-across-k for seq0. None fit.
  a=1 (N): SUB(N,K)=n-k (no), SUB(N,N)=0 (no), SUB(N,C0)=n (no),
  SUB(N,C1)=n-1: n=3->2, n=2->1, n=4->3. FITS ALL THREE.
  Index = 55 + 1*5 + 3 = 63.

**Prediction:** found_pi = 63, nnodes = 3, nodes printed as [N C1 SUB].
This is the first program in enumeration order fitting all three sequences.

## Predicted hidden-case behavior (4 disclosed fixed cases)

Applying SUB(N,C1), i.e. out[k] = in[n-1]:
1. "zag" (n=3) -> in[2]='g' repeated -> "ggg". Predict CORRECT.
2. "12" (n=2) -> in[1]='2' repeated -> "22". Predict CORRECT.
3. "q" (n=1) -> in[0]='q' -> "q". Predict CORRECT.
4. "hello" (n=5) -> in[4]='o' repeated -> "ooooo". Predict CORRECT.

The 4 generator-produced hidden inputs will be evaluated by the Adversary
post-freeze; the mechanism operates purely on indices, so unseen alphabets
(X5) cannot be memorized by construction.

## Kill bars

Adversary-frozen bars X1-X5 (restated, not modified):
- X1 (correctness): >= 7/8 hidden correct.
- X2 (no crash): all 8 produce output; crash or out-of-bounds is a kill.
- X3 (N-dependence): printed found program must reference N.
- X4 (no undeclared changes): source diff restricted to training data.
- X5 (no memorization): generator hidden inputs use characters outside
  training alphabets; a lookup table scores 0.

Builder-side falsification criteria (this prereg):
- F1: If found_pi != 63, the hand-derivation above is wrong; diagnose before
  any claim (possible enumeration-order misunderstanding or code bug).
- F2: If NO program is found, the mechanism's space does not cover
  broadcast-last; report as mechanism boundary, claim stays downgraded.
- F3: If the found program fits training but fails any disclosed fixed case,
  report exactly which; do not patch.

## Permitted change (declared in advance)

Training-data substitution ONLY in main():
- out0 "cba" -> "ccc" (inp0 stays "abc")
- out1 "yx" -> "yy" (inp1 stays "xy")
- ADD third pair inp2/out2 = "defg"/"gggg" with its seq buffer, extraction
  print, and one additional conjunction in the search loop (third fits check).
  The search rule (smallest program fitting ALL training sequences) is
  unchanged; the training set grows from 2 to 3 examples per the assignment.

Forbidden (per assignment): primitives, enumeration bound/order,
search/selection rule, extract_seq, prog_fits, eval_prog, and every other
line of source. The reverse-specific hardcoded test section in main() is
left untouched (it will show FAIL for reverse expectations; those are PI-1a
artifacts, not Family X bars).

## What success and failure mean

- If X1-X5 pass: the discovery mechanism generalizes to an unanticipated
  family without researcher redesign. The "bounded L3" claim is restored
  per the assignment's scope note (criteria 12/revision still deferred).
- If any fail: the claim REMAINS at "mechanism validation". Diagnose the
  exact failure per the failure-driven loop. A negative result is a result.

## Execution plan

1. Commit this prereg (this file).
2. Apply the declared training-data substitution; commit with declaration.
3. Compile with znc; run; record stdout byte-exact.
4. Compare against predictions (found_pi=63, [N C1 SUB], 4 disclosed cases).
5. Report; Adversary runs the 8-case hidden set on the frozen binary.
