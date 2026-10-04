# Result: Family X (broadcast-last) Test

**Date:** 2026-09-29
**Prereg:** pi_builder/PREREG_FAMILY_X.md (committed 6caa37ed6, before execution)
**Training-data commit:** 8fa0fe2a3 (declared substitution only)
**Binary SHA-256:** c78a5ad9273dc03de997c52e7f4ec3d286c54d4c93766c8deb7f9f2cc50a26a2
**Raw output:** pi_builder/PI_FAMILY_X_RAW_OUTPUT.txt (byte-exact stdout)

## What the mechanism found

- Extracted sequences: seq0=[2,2,2] n=3, seq1=[1,1] n=2, seq2=[3,3,3,3] n=4.
  All match prereg predictions. No extraction ambiguity.
- Found program index: **38**
- Program nodes: 3, printed as **[N C1 SUB]**, i.e. out[k] = in[n-1].
- This IS the broadcast-last program. Discovery succeeded.

## F1 fired and diagnosed

The prereg predicted index 63. The actual index is 38. Diagnosis:

The prereg's hand-derivation miscounted the size-3 enumeration: it assumed
50 programs per operator block, but the code generates 25 per block
(5x5 terminal pairs), so ADD occupies indices 5-29 and SUB occupies 30-54.
SUB(N,C1) = 30 + 1*5 + 3 = 38. The program-identity prediction ([N C1 SUB],
first fitting program in enumeration order) was exactly correct; only the
index number was wrong due to the Builder's arithmetic slip, not a mechanism
defect. The search itself authoritatively tested programs 0-37 against all
three sequences and rejected every one, confirming 38 is the smallest fit.

F1 is therefore RESOLVED as prereg arithmetic error. No source change was
made in response (none was needed).

## Behavior on disclosed fixed hidden cases

1. "zag" -> "ggg": CORRECT (shown in binary output).
2. "12" -> "22": CORRECT by program semantics (n=2, idx=1 -> '2').
3. "q" -> "q": CORRECT (shown in binary output).
4. "hello" -> "ooooo": CORRECT by program semantics (n=5 -> idx 4 -> 'o';
   binary printed index application [4,4,4,4,4] for n=5).

4/4 disclosed cases correct.

The 4 generator-produced hidden inputs do not exist yet (Adversary generates
them post-freeze with a fresh published seed). By program semantics,
SUB(N,C1) computes out[k]=in[n-1] for every n>=1, which is exactly the
broadcast-last transformation, so 4/4 generator cases are expected correct.
Expected X1 total: 8/8. The Adversary's independent run is authoritative.

## Bar assessment (Adversary confirms officially)

- X1 (correctness >= 7/8): 4/4 disclosed verified; 4/4 generator expected by
  program semantics. PROJECTED PASS, pending Adversary's 8-case run.
- X2 (no crash): binary exited 0; indices n-1 are in-bounds for all n>=1;
  generator lengths are 1..20. PASS on evidence.
- X3 (N-dependence): printed program [N C1 SUB] references N. PASS.
- X4 (no undeclared changes): diff of 8fa0fe2a3 vs reverse commit is
  training-data only (verified before commit). PASS.
- X5 (no memorization): the mechanism operates purely on indices; the found
  program ignores character values entirely, so unseen alphabets cannot be
  memorized. PASS by construction.

## What this means

The FROZEN mechanism, designed during the reverse investigation, discovered
the broadcast-last program for an adversary-assigned family that appeared in
no design doc, with no researcher redesign and no source change beyond the
declared training-data substitution. The enumeration space contained the
solution (SUB(N,C1) at size 3) and the smallest-fit rule selected it.

Per PI_FAMILY_X_ASSIGNMENT.md, passing X1-X5 restores the "bounded L3"
claim for the mechanism (family-agnostic discovery demonstrated), within the
assignment's scope note: criterion 12 (revision) remains deferred, and the
affine-space narrowness question remains under separate RT2 investigation.

Honest boundaries:
- The search space is a small affine index space (1055 programs, size<=5).
  Broadcast-last happened to lie in it. This test shows the discovery rule
  generalizes beyond pre-named families; it does not show the space covers
  all procedure families.
- The reverse-specific hardcoded test section still prints FAIL for reverse
  expectations (expected: the learner was trained on broadcast-last). Those
  are PI-1a artifacts, not Family X bars.
- Official X1 verdict belongs to the Adversary's post-freeze 8-case run.

## Commits in order

1. 6caa37ed6 - Family X prereg FROZEN (before execution)
2. 8fa0fe2a3 - Training-data substitution ONLY (declared)
3. (this result)
