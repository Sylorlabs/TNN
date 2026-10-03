# Analogy test — verdict

**Worker:** ANALOGY (r34 remediation workstream). **Owner:** Micah.
**Prereg:** `PREREG_ANALOGY.md` (frozen 2026-09-20, committed before any test code).
**Evidence:** `EVIDENCE_ANALOGY_20260920T235317Z/` (receipt + six logs + static audit).
**Apparatus:** the remediated clean learner core — no RNG, 22-field logged state,
frozen explore rule.

## The question

Does state-driven variation in the remediated explore mechanism produce Micah's
predicted pattern — identical logged state replays byte-identically, different
logged history diverges exactly where the rule says, and repeated identical
stimuli produce adapted expression with the changed state fields nameable?

## Verdicts

- **P1 — PASS.** Same input protocol + same complete logged state → byte-identical
  behavior, 5/5 pairs, 0 mismatches across 1200 choose/accept cycles; the
  encode→decode→continue flight-recorder leg stayed lockstep; binary output
  byte-identical across invocations.
- **P2 — PASS.** Same protocol + different logged history (neg_streak 0 vs 3) →
  explore flags differed on exactly the 10 predicted episodes (of 12), every
  observed decision equaled the frozen rule's prediction from that arm's own
  logged state, exact predicted final field values on both arms, and all 15
  fields outside the causally-allowed set verified equal — divergence exactly
  where predicted, nowhere else.
- **P3 — PASS.** Four identical hi cycles → ex 0,0,0,1. The expression adapted at
  exactly the frozen disappointment threshold: pre-hi-#4 showed neg_streak=3 with
  margin=300 (uncertainty path provably uninvolved), obj flipped 0→1, budget
  10→9, explores 0→1. Every inter-hi logged transition proven to touch only the
  six predicted fields. The changed fields are named in the log.

## Overall analogy verdict: HOLDS for this mechanism

Kill bars K-A1…K-A4: none fired. No failures, no amendments, nothing softened.
For the remediated core, the analogy is confirmed as operationalized: variation
in expression comes only from logged state, and the complete logged record
replays byte-identically. Scope honesty: this certifies the explore mechanism,
not TNN as a whole; horizons and single-context scope are per the frozen prereg.
