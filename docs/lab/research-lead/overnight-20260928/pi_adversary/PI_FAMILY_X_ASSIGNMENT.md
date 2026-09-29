# Adversary Family Assignment: Family X (Undisclosed Procedure Test)

**Authority:** Frozen G1 (PI_ADVERSARY_PREREG.md). Assigned after Governance
Auditor flagged that the Builder's reverse target was pre-named in
NEXT_FRONTIER_DESIGN.md.
**Date assigned:** 2026-09-29
**Status:** ASSIGNED. Builder's claim downgraded (see below) until this test passes.

## Claim Downgrade

The Builder's preregistered "bounded L3" claim for procedure invention is
hereby DOWNGRADED to **"mechanism validation"** effective immediately.

Reason: the evaluation family (REVERSE) was enumerated in NEXT_FRONTIER_DESIGN.md
("Target procedure: REVERSE") before the Builder's prereg. A claim of
"not enumerated beforehand" cannot stand on a pre-named target.

The claim may be restored to "bounded L3" only if the Builder's FROZEN
mechanism (no source changes except training-data substitution, declared
below) passes Family X.

## Family X Definition

**Name (adversary-assigned):** broadcast-last

**Transformation:** Every output character equals the LAST input character.
output[k] = input[n-1] for all k. Output length equals input length.

**Examples:**
- "abc" -> "ccc"
- "xy" -> "yy"
- "defg" -> "gggg"

**Why this family:**
1. Not named in any design doc, prereg, or prior discussion (verified by grep;
   "broadcast" appears nowhere in the research record).
2. Not reverse, identity, swap, rotation, deletion, duplication, or interleaving.
3. Expressible in the Builder's stated index-program space: SUB(N,C1).
   (Fairness: the test measures discovery, not architectural scope.)
4. Unanticipated: forces N-dependent discovery. Constant-index programs
   (C0/C1/C2) are eliminated by varying input lengths across training examples.
5. Non-degenerate as a learning problem: the learner must use N (input length),
   combine it with SUB and C1, and reject smaller constant programs.

## Training Examples (assigned, public to Builder)

The Builder shall train ONLY on these three examples for Family X:
1. ("abc" -> "ccc")
2. ("xy" -> "yy")
3. ("defg" -> "gggg")

Rationale for varying lengths (3, 2, 4): across all three, the only
size<=5 programs fitting every extracted sequence are semantically
SUB(N,C1) (n-1). Constant programs fit at most one length each.

## What the Builder May and May Not Change

**MAY change (declared in commit message):**
- Training examples in main() (substitute the three Family X pairs for the
  reverse pairs). Training data is the learner's input, not the learner.

**MAY NOT change:**
- Primitive set {K, N, C0, C1, C2, ADD, SUB}
- Enumeration bound (size <= 5) and enumeration order
- Search/selection rule (smallest fitting program)
- extract_seq, prog_fits, eval_prog logic
- Anything else in source

Any other source change invalidates the run. The Adversary will diff the
Builder's Family X commit against the reverse commit (proc_learn.zag as
reproduced: /tmp/proc_learn_adv build) and reject undeclared changes.

**Required:** The Builder commits the Family X version with the exact
training-data diff declared, then FREEZES. No further source changes before
hidden testing.

## Hidden Tests (sealed per G4)

Hidden tests DO NOT EXIST YET. After the Builder's Family X freeze commit,
the Adversary will:
1. Pick a fresh 64-bit seed, publish it with the report.
2. Generate 4 additional inputs via pi_adversary/gen_hidden_inputs.sh
   (frozen generator), plus the 4 fixed hidden cases below.
3. Compute expected outputs with an independent reference implementation.
4. Run the Builder's FROZEN binary on all 8 hidden inputs.
5. Report PASS/FAIL.

**Fixed hidden cases (disclosed now; still unseen by the learner):**
1. "zag" -> "ggg"
2. "12" -> "22" (digit alphabet: mini transfer within family)
3. "q" -> "q" (single character edge)
4. "hello" -> "ooooo" (longer input; repeated chars fine at apply time)

## Pass Bars (frozen)

- **X1 (correctness):** >= 7/8 hidden correct.
- **X2 (no crash):** all 8 produce output; any crash or out-of-bounds is a kill.
- **X3 (N-dependence):** the printed found program must reference N
  (else it is a constant-index hack that cannot generalize; kill).
- **X4 (no undeclared changes):** source diff restricted to training data (kill
  on violation).
- **X5 (no memorization):** the 4 generator-produced hidden inputs use
  characters outside the training alphabets; a lookup table scores 0.

If X1-X5 pass, the "bounded L3" claim is RESTORED for the mechanism
(family-agnostic discovery demonstrated on an unanticipated family).
If any fail, the claim REMAINS at "mechanism validation" and the specific
failure is diagnosed per the failure-driven loop.

## Scope Note

Passing Family X does not by itself establish full L3 (criteria 12/revision
remains deferred per Builder prereg; the affine-space narrowness question is
separately under RT2 investigation). It establishes that the discovery
mechanism generalizes beyond pre-named families, which is the necessary
condition for lifting the enumeration downgrade.
