# PREREG: FDCR COMPOSE Operator (H-COMPOSE)

**Date:** 2026-09-29
**Researcher:** FDCR COMPOSE Researcher (subagent)
**Status:** FROZEN (this commit). Implementation must follow, not precede.

## Background

FDCR (rep v2) implements FORM (shared-subset intersection parents), MERGE
(identical intents), SPLIT (contradiction-driven), GRADE/CONTEXTUALIZE.
COMPOSE was defined in PREREG_REP_V2.md as exploratory: "Given two concepts,
form a candidate with intent = union of intents." It was never implemented.

The F-A5 red-team finding confirmed: "union-intent concepts arise only as
leaf/SPLIT artifacts, never by deliberate composition of two concepts'
intents."

Baseline observation (pre-prereg, using committed `fdcr_learn` binary):
on a disambiguation fixture (kind=roller iff red AND round; each parent
dimension alone ambiguous), the system WITHHOLDS (0/1). The conjunction
concept {red,round} exists (as a leaf artifact with correct members), but
sibling inference accumulates conflicting evidence globally across all
candidates, so the correct specific evidence is vetoed by less specific
concepts.

## Theoretical prediction (recorded before implementation)

The researcher predicts H-COMPOSE will FAIL on utility, for the following
reason (redundancy argument):

1. A crisp union-intent composed concept C3 = I1 union I2 cannot enable a
   novel Step-1 (direct) held-out inference: Step-1 needs (rel,*) in
   intent(C3), but intent(C3) subset of subject features implies the fact
   was taught, which Step-0 already answers.
2. For Step-2 (sibling) inference, C3 needs at least 2 members with the
   target evidence. If 2+ entities have all features of I1 union I2, their
   leaf concepts share those features, so FORM/MERGE/subset-linking already
   provides a concept covering them. A deliberate union operator is therefore
   redundant for sibling-based inference in this architecture.
3. The observed baseline failure is inference-side (global ambiguity
   accumulation), not concept-side (the needed concept exists).

This prediction is recorded so that a negative result is informative rather
than a surprise, and a positive result (if the theory has a hole) is a
genuine discovery.

## Hypothesis H-COMPOSE

A deliberate union-intent COMPOSE operator (reason=6), run in the learning
fixpoint, recruits a concept C3 = union of intents of two existing concepts
C1, C2, and this composed concept enables a correct held-out inference that
the un-composed system cannot make.

## Operator specification (frozen)

In the learning fixpoint, after FORM/MERGE/SPLIT converge each iteration,
for each pair (C1, C2) of active concepts with ctx < 0:

- Let U = intent(C1) union intent(C2).
- Fire iff ALL of:
  1. Neither intent subsumes the other (not (I1 subset I2) and not (I2 subset I1)).
  2. |U| <= 6 (complexity bound).
  3. At least 1 entity has all features of U (non-vacuous).
  4. No active concept has intent EXACTLY equal to U (non-redundant).
  5. ncon < 256 (capacity).
- On fire: recruit C3 with intent = U, members = {entities whose features
  include all of U}, reason = 6, ctx = -1, parent = -1 initially.
  Then link: for any active concept Cx (ctx < 0, Cx != C3) with intent(Cx)
  a proper subset of U and no parent, set parent(Cx) = C3 (attach as child).
  If any active concept Cy has intent a proper superset of U, and C3 has no
  parent, set parent(C3) = the smallest such Cy.
- Set changed = 1 (fixpoint continues).
- No change to the probe-answering procedure (it must use C3 through the
  existing Step-1/Step-2 machinery for the test to be clean).

A compile-time constant COMPOSE_ON (1/0) gates the operator for ablation.
Source file: rep_v2/fdcr_learn.zag (modified in place; baseline binary
preserved separately for comparison).

## Kill bars (frozen)

Fixture `rep_v2/compose_fixtures/disambig.txt` (committed with prereg):
kind=roller iff (red AND round); each single dimension ambiguous; probe
subject e5 taught red+round with kind held out; expected roller.

- K-C1 (operator fires): With COMPOSE_ON=1, the concept dump contains at
  least one active concept with reason=6 whose intent is a union of two
  pre-existing concepts' intents. Verdict by white-box dump inspection.
- K-C2 (utility): With COMPOSE_ON=1, `Q e5 | kind` answers roller (1/1).
  Baseline (COMPOSE_ON=0) scores 0/1 WITHHOLD (verified pre-prereg).
- K-C3 (ablation): With COMPOSE_ON=0 (all else identical), the probe
  returns to 0/1 WITHHOLD. I.e., removing the operator impairs performance
  on this probe. (If K-C2 fails, K-C3 is moot and marked N/A.)
- K-C4 (precision, no harm): With COMPOSE_ON=1, scores on all six committed
  fixtures (k5, k2, k4, k3_merge, mini_world, ctx_test) are unchanged from
  baseline, AND the number of reason=6 concepts per fixture is < 12
  (bounded, no runaway composition).

## Verdict rules (frozen)

- H-COMPOSE SURVIVES iff K-C1, K-C2, K-C3, K-C4 all PASS.
- H-COMPOSE KILLED (utility) iff K-C2 fails: the operator does not enable
  the held-out inference. K-C1 reported separately (mechanics vs utility).
- If K-C2 passes but K-C3 fails (ablation shows no impairment), H-COMPOSE
  is DOWNGRADED to "operator fires but not load-bearing."
- K-C4 failure means the operator is HARMFUL (degrades existing behavior).

## Controls

- C-BASE: COMPOSE_ON=0 binary on disambig.txt. Expect 0/1 WITHHOLD
  (pre-verified). Confirms the probe is not trivially answerable.
- C-DET: Each fixture run 3x; outputs must be byte-identical.

## Allowed post-prereg actions

- Implement per spec. Fix build errors. No spec changes without amendment.
- If the operator as specified cannot build, file an amendment (rare).
- Bug fixes to the operator that do not change the frozen spec are allowed
  and must be documented in the result report.

## Fixture (frozen with this prereg)

See rep_v2/compose_fixtures/disambig.txt (committed here).
