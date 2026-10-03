# F2 Retry (AUTOSCI2) Promotion Assessment

Date: 2026-09-30. Assessor: F2 Promotion Worker (analysis only).

## Subject

- F2 v1: BUILD-FAIL `4ebde580a` (prereg `2a87efa77`); failure was K-AS5b,
  random control 1/20 on a weak transient World B goal, not a broken loop.
- F2 retry (AUTOSCI2): BUILD-PASS `1eb66765d` (prereg `b9ab0acb6`); harder
  World B goal B2 (sustained triple: three consecutive steps with Y=1 AND
  K=0); all seven kill bars K2-R1..K2-R7 PASS in both worlds; 3/3
  byte-identical per world; random control 0/20 in both worlds (B2 had
  0/160 calibration hits across 8 seeds); pure Zag; no em dashes.
- Classification (builder, undisputed): L2 structural learning (bounded).
  NOT L3. Not claimed as L3.

## Step-by-step assessment against the 11-step pipeline

### Step 1: Committed preregistration - COMPLETE

Prereg `b9ab0acb6` committed alone before any implementation file existed;
strict-ancestor ordering verified via `git merge-base --is-ancestor`.
The prereg discloses exactly what changed from F2 (World B goal predicate,
B2 planner, B2 control alphabet, observation budget 12 to 18) and freezes
all kill bars before execution.

### Step 2: Implementation - COMPLETE

`autosci2_learner.zag` + `world_a2.zag` + `world_b2.zag` committed as
`1eb66765d`. Pure Zag. Deterministic. No em dashes in wave documentation.

### Step 3: Sealed evaluation - COMPLETE

Worlds A and B are sealed (inherited from F2; the learner has no access to
the true rule sets, structural barrier verified by source audit). Frozen
kill bars K2-R1..K2-R7 executed as preregistered; all PASS in both worlds.
The harder B2 goal survived its own calibration (0/160 across 8 seeds) and
its frozen control (0/20, a priori seed 12345).

### Step 4: Independent reproduction from committed source - NOT DONE

No second worker has rebuilt the learner from the committed source and
reproduced the 3/3 byte-identical runs. This is the cheapest missing step
and should be scheduled first. A reproduction failure here would be
high-information.

### Step 5: Simple-baseline comparison - PARTIAL

Random-action control: DONE, and it is the load-bearing control for this
claim (0/20 World A, 0/20 World B with the generous 7-symbol alphabet that
includes observations, so the control is not vacuous).
Memorization / simpler-explanation control: NOT DONE. Open question: could
a nearest-neighbor or table-lookup strategy on the passive trace, combined
with random goal search, achieve the B2 goal at rates comparable to the
mechanism? The random control answers "not by luck"; it does not answer
"not by a simpler learner." A memorization control on the same frozen
protocol is needed before any SURVIVES claim.

### Step 6: Alternative-explanation attack - NOT DONE

The most plausible alternative explanations have not been attacked:
(a) The experiment search is iterative-deepening enumeration over a
researcher-supplied primitive alphabet to depth 6 (up to ~600K sequences
simulated in World A). The disagreement predicate selects among enumerated
candidates rather than constructing experiments from hypothesis structure.
This is the same enumerate-then-select family that H-CAUSALEXP-CONSTRUCT
was killed under (as an L3 claim) and that DDES was built to escape.
(b) It is unmeasured whether disagreement-driven selection is load-bearing
in F2: would a random or first-disagreeing-enough selection converge with
comparable observation cost? H-CAUSALEXP-CONSTRUCT's ablation showed its
disagreement filter was correctness-critical, but that result does not
transfer to this architecture without an F2-specific ablation.
An adversary should test (a) and (b) directly.

### Step 7: OOD test - NOT DONE

Worlds A and B are the same two families as F2. No evaluation on a novel
world family (different causal structure: e.g., a third variable in the
chain, inhibitory context, longer delays, multiple effect variables).
The mechanism's scope beyond its two development worlds is unmeasured.

### Step 8: Ablation - NOT DONE

No component of the loop has been removed to test necessity: the
disagreement-selection criterion, the 2-firing candidate filter, the
pure-simulation search, the cross-product hypothesis representation.
Necessity of the disagreement criterion is the highest-value ablation.

### Step 9: Transfer/reuse test - NOT DONE

Nothing learned in World A is reused in World B (separate runs). The
hypotheses are per-world rule sets; there is no persistent learner state
that carries structure forward. For an "autonomous scientist" that is
supposed to accumulate knowledge, this is a real gap: the current
mechanism is a per-world pipeline, not a continuing learner. Any transfer
claim would need a follow-up wave where World B runs with World A's
retained state.

### Step 10: Independent red team - NOT DONE

No independent adversary has been tasked with killing the BUILD-PASS.
Given step 6, the natural red-team brief is: show that the mechanism is
enumerate-and-select in disguise, or that a simpler control matches it.

### Step 11: Governance audit - NOT DONE

The builder performed a self-check (prereg ordering verified, purity
self-declared, owned paths only, local commits). No independent
governance audit has verified commit hygiene, byte-level purity, or the
absence of result-contaminated amendments. (No amendment was needed per
the result report; an audit would confirm this rather than discover it.)

## Structural ceiling (assessor's note)

Even with all 11 steps complete, the promotable verdict for this
architecture is bounded L2, never L3. The experiment "construction" is
iterative-deepening enumeration over a researcher-fixed primitive
alphabet with base-B counting; the disagreement predicate filters a
pre-enumerated stream rather than guiding synthesis from hypothesis
structure. The researcher owns the primitives, the delay range, the
context forms, the candidate filter, and the goal-planning alphabets.
DDES (repaired `17c97a2cd`) is the lane that attempts to escape this
family; F2 does not. Promotion should be framed as "bounded L2
SURVIVES," parallel to H-CAUSALEXP-CONSTRUCT's SURVIVES-AS-L2.

## Recommendation: DO NOT PROMOTE

BUILD-PASS stands as reported. SURVIVES is not warranted: 7 of 11 steps
are incomplete (steps 4, 6, 7, 8, 9, 10, 11; step 5 partial).

Suggested scheduling order for the remaining steps, by information per
unit effort:

1. Step 4 (independent reproduction): cheapest; do first. Kills or
   confirms the entire wave at low cost.
2. Step 5 completion (memorization control): the strongest remaining
   threat to the claim's meaning. A simpler-explanation win here would
   reframe the result as infrastructure, not discovery.
3. Steps 6/10 combined (adversary + red team): one adversarial worker
   with the brief in step 6, plus the disagreement-necessity ablation
   (step 8's highest-value item) folded in.
4. Step 7 (OOD): one novel world family, preregistered before design.
5. Step 9 (transfer): only if steps 1-4 pass; requires architectural
   work (persistent cross-world state), so treat as a follow-up wave
   (AUTOSCI3) rather than a promotion step for this wave.
6. Step 11 (governance audit): any time; independent of the science.

If steps 4, 5, and 6/10 all pass, the honest promotable verdict is
SURVIVES-AS-L2 (bounded). No L3 reading is available for this
architecture under Criterion 0.

## Verdict

PROMOTION-ASSESSED. F2 retry: BUILD-PASS confirmed against its frozen
bars; promotion to SURVIVES is BLOCKED pending steps 4-11. Recommended
next: independent reproduction, then memorization control, then combined
adversary/ablation.
