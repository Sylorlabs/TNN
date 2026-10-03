# PREREG: Outlier-Excluding Grammar Induction (UNFROZEN)

Worker: Grammar Outlier-Exclusion Worker. Date: 2026-10-02.
Lane: unfrozen variant of the grammar induction machinery
(commit dce5d3d43, ledger C222). Frozen dirs read only, never modified.

## Vulnerability under repair

Grammar transfer (grammar_transfer/REPORT.md, W5a/W5b) proved the
induction machinery transfers to EXL2 byte identical, but found the
denial of learning flaw: ONE bad example poisons the whole batch.

* W5a: one deceptive BUILD fact (2,45,P(9,9)) with no licensor makes
  gi_induce return 0. No grammar written.
* W5b: one bogus decomp relation 46 licensing (3,45,P(4,1)) pushes the
  distinct licensor count to 3, tripping the nlic<=2 guard. Return 0.

Induction refuses to hallucinate but also refuses to learn. A single
adversarial example is a denial of learning attack. This preregisters
an outlier excluding induction variant and its test battery BEFORE any
implementation is written.

## Hypothesis

H-OUTLIER-1: A majority consistency exclusion procedure, computed from
the learner's own example profiles with no researcher hardcoded
relation ids or deception signatures, repairs the denial of learning
flaw: clean batches induce the identical grammar as before, poisoned
batches induce the correct grammar while excluding and flagging the
minority contradicting examples, and genuinely ambiguous batches are
refused with an explicit ambiguity report rather than a silent pick.

## Exclusion criterion (learner derived)

gi_induce2(W, rep) replaces the fail closed gi_induce. All thresholds
are computed from the batch and the learner's fact store. No relation
ids, no deception signatures, and no per world constants appear in the
procedure.

1. Per example licensor profile. For each live BUILD fact (T,45,P)
   with P decoding to (a,b): S_i = { r2 != 45 : live fact (T,r2,P) }.
   An undecodable P yields the empty profile.

2. Minority unlicensed exclusion. Let U = examples with empty
   profiles, L = examples with nonempty profiles. If |L| = 0, refuse
   (code 1). If |U| > 0 and |U| < |L|, exclude U as minority
   unlicensed and continue on L, flagging each excluded example
   (T, P, why=unlicensed). If |U| >= |L| > 0, refuse (code 2):
   the batch is majority unlicensed or tied, not a minority outlier.

3. Majority consistent licensor set. Over licensed examples, enumerate
   nonempty subsets of the distinct observed licensor relations
   (first seen order, compute cap 10 relations). A set C is viable iff
   it covers a strict majority of licensed examples, where covering
   means every covered example has a nonempty profile contained in C.
   Among viable sets choose by: (a) smallest cardinality,
   (b) largest coverage, (c) largest cross target attestation, defined
   as the sum over relations of the count of distinct subjects T with
   a live (T,r,.) fact anywhere in the learner's experience. If two
   viable sets tie on all three keys, the batch is ambiguous: refuse
   (code 4) and report the tie. If no viable set exists, refuse
   (code 3). If the winning set has more than 2 relations, refuse
   (code 5): the type 70 grammar node layout holds at most 2
   licensors, a pre existing machinery limit, unchanged.

4. Inconsistent profile exclusion. Licensed examples whose profile is
   not contained in the winning set are excluded and flagged
   (T, P, why=inconsistent).

5. Literal ranges and node write are unchanged from gi_induce except
   they run over the winning licensor set and record nbuild as the
   included example count. The type 70 node layout is unchanged.

Rationale for key (c): genuine licensor relations are attested across
many targets in the learner's full decomp experience (43 and 44 each
span all 10 EXL2 targets); a smuggled relation is attested only where
the deceiver taught it. This breaks ties between a genuine set and a
piggybacked bogus set without any hardcoded ids.

## Test battery (EXL2 world, TRAIN {1,3,5,7}, TEST {0,2,4,6,8,9})

All arms use full EXL2 eval and decomp teaching. P(a,b) = a*16+b.

* Arm A (clean): 4 canonical BUILD examples. Predicted: GI2-INDUCED=1,
  0 excluded, grammar line identical to transfer W1
  (nbuild=4 nlic=2 lic=44,43 a=[0,9] b=[0,9] maxlinks=1), battery 6/6
  valid. Original gi_induce on the same world: 1 (sanity).
* Arm B (one unlicensed deceiver): A + (2,45,P(9,9)) with no licensor.
  Predicted: GI2-INDUCED=1, same grammar, battery 6/6, exactly 1
  excluded (T=2, P=153, why=unlicensed). Original gi_induce: 0
  (reproduces the W5a denial of learning on the same batch).
* Arm C (two minority deceivers): B + bogus (3,46,P(4,1)) and
  (3,45,P(4,1)) (W5b style, profile {43,46}). Predicted:
  GI2-INDUCED=1, same grammar, battery 6/6, exactly 2 excluded:
  (T=2, P=153, unlicensed) and (T=3, P=65, inconsistent).
* Arm D (50/50 split, disjoint vocabularies): BUILD batch = 2 clean
  ((1,45,P(1,1)) profile {44}, (3,45,P(3,0)) profile {43}) + 2
  deceivers ((5,45,P(9,9)) and (7,45,P(8,8)), each licensed only by a
  bogus 46 fact, profiles {46}). Predicted: GI2-INDUCED=0, refusal
  code 4 (ambiguous tie: {43,46} vs {44,46} tie on size, coverage,
  and attestation), no grammar node, battery NOGRAMMAR. The learner
  must NOT silently pick one side.
* Arm E (adversarial: majority poisoning): A + 5 deceivers on targets
  {0,2,4,6,8}, each (T,45,P)+(T,46,P) with P chosen so no genuine
  licensor exists (profiles {46}, disjoint). 9 examples, deceivers
  are the strict majority. Predicted: the excluder is DEFEATED.
  GI2-INDUCED=1 with the bogus grammar lic={46} (nbuild=9), battery
  0/6 valid (no 46 fact verifies against eval knowledge; classes 0).
  This arm is expected to demonstrate the fundamental limit, and its
  pass condition is that the defeat occurs exactly as predicted and
  is reported, not hidden.
* Arm F (adversarial: coordinated piggyback minority): A + 2
  deceivers sharing one bogus relation 46 and piggybacking on genuine
  44 ((9,45,P(9,1))+(9,46,P(9,1)) profile {44,46},
  (2,45,P(4,2))+(2,46,P(4,2)) profile {44,46}). Predicted: the
  attestation tiebreak holds. GI2-INDUCED=1, grammar {44,43},
  battery 6/6, exactly 2 excluded (T=9,P=145 and T=2,P=66,
  why=inconsistent).
* Arm G (extra probe: piggyback 50/50): 2 clean + 2 deceivers with
  profiles {44,46} (piggybacked, (5,45,P(5,1)) and (7,45,P(7,1))).
  Predicted: limitation demonstrated. GI2-INDUCED=1 with lic={44,46},
  the clean (3,45,P(3,0)) example wrongly excluded as inconsistent.
  Piggybacking at exactly 50/50 flips the majority; documented as a
  residual vulnerability, not a pass.

## Pass fail bars (frozen)

* Arms A, B, C, F: every predicted field must match exactly
  (induced flag, grammar line, exclusion list, battery count).
  Any mismatch FAILS the mechanism.
* Arm D: must refuse with code 4 and write no grammar node. Silent
  induction FAILS the mechanism.
* Arm E: must produce the predicted defeat (bogus lic={46} grammar,
  0/6 battery). If the excluder instead resists majority poisoning,
  the prediction is falsified and the analysis is rewritten; a
  silent bogus induction reported as success FAILS.
* Arm G: predicted limitation must reproduce as stated.
* Determinism: 3/3 runs byte identical (SHA-256). Any divergence
  FAILS.
* Adversarial analysis (test 5 of the mission): E demonstrates
  majority poisoning defeat; G demonstrates piggyback 50/50
  defeat; F shows coordinated minority piggyback is still caught.
  Residual boundary: an adversary whose bogus relation is attested
  across as many targets as genuine relations is no longer an
  outlier by any learner visible measure; the excluder cannot and
  should not exclude it.

## Constraints (standing)

Unfrozen lane only. Frozen dirs read only. Pure Zag: no Python or
other interpreters in the worker PATH (safebin guard, Step 0 of
NAMECHECK.md). New code defines no print helpers (reuses the byte
copied base emit/e64); stdout bytes verified. Zero em/en dashes in
docs. 0 modes/bridges/handlers. No hardcoded deception signatures.
Commits local only, explicit pathspecs, nothing pushed. Prereg commit
strictly precedes the implementation commit.

## Deliverables

PREREG.md (this file, committed first and alone), NAMECHECK.md,
go_base.zag (byte copy of gt_base.zag), go_patch.zag (byte copy of
gt_patch.zag plus appended gi_induce2 and helpers), go_driver.zag,
go_build.sh, go_bin, go_run1/2/3.txt, REPORT.md. Verdict:
GRAMMAR-OUTLIER-COMPLETE with exclusion criterion analysis and
adversarial test.
