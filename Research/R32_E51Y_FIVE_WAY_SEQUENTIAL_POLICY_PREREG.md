# R32 E51Y — Confirmed-Terminal Five-Way Sequential Policy

Date frozen: 2026-08-30
Branch: `r32-agent-sequential-frontier`
Canonical status: R27 remains canonical.

## Causal basis

E51X removed the terminal reachability veto without changing topology. The first preregistered exact arm, the 384-sweep trajectory-critical 32-cell conditional-weight learner, reached **4,200 / 4,200 known + 1,200 / 1,200 no-unique UNKNOWN** on untouched validation and repeated **8,400 / 8,400 + 2,400 / 2,400** on sealed confirmation.

The E51E sequential experiment was previously blocked before direct joint evaluation because the terminal policy did not expose a correct terminal action somewhere on every trajectory. That structural blocker is now removed. E51Y therefore asks whether a learner can make a cost-aware online stopping decision with the confirmed terminal geometry frozen.

## Fixed terminal learner

Reproduce and freeze the E51X 384-sweep terminal learner from its **stage-81 development worlds only**:

1. first-1x absolute-utility KEEP/CURRENT/RESTORE ranking head;
2. full-4x top-commit sign calibrator;
3. learner-grown routing tree, first 32 cells;
4. 96-sweep state-SSE local expert start;
5. 384-sweep trajectory-critical refit, four trajectory rounds maximum.

The reproduced terminal learner must remain evaluator-blind and must pass deterministic forward/reverse identity. E51Y may audit reproduction on the already-consumed E51X stage-82 validation worlds, but those worlds may not train, select, tune, or gate the CONTINUE learner. The frozen terminal weights do not update during E51Y continuation training.

## Five-way geometry

Terminal cognition is:

`KEEP / CURRENT / RESTORE / UNKNOWN`, with UNKNOWN fixed at score 0.

The E51X scalar calibration shifts all three commit scores equally, preserving their ordering. CONTINUE is learned as a **relative action value against the currently preferred terminal action**. At inference define

`Q(CONTINUE) = Q(best terminal) + A_continue(state)`.

Thus CONTINUE directly wins the five-way competition exactly when the learned continuation advantage is positive. No fixed confidence threshold or observation count is used.

## Continuation supervision

Use fresh stage-84 development worlds: 12,960 episodes / 220,320 sequential states.

For each state under the frozen E51X terminal learner, evaluator-only training code computes:

- grounded utility of stopping with the learner's current terminal choice;
- exact opportunity loss of one additional observation;
- the best achievable future return under the same frozen terminal policy by backward dynamic programming.

The consequence-derived target is:

- `+1000` if one more observation plus optimal later stopping has strictly higher grounded utility than stopping now after opportunity cost;
- `-1000` otherwise.

At the terminal horizon the target is `-1000`.

This is not an ambiguity label, evaluator-mode label, or fixed stopping rule. Evaluator truth and costs are used only to construct delayed consequence targets after learner-visible state is complete.

## Learner-visible continuation state

Use the existing 32-feature E51B continuation representation generated from persistent option/state evidence. No evaluator truth, evaluator mode, seed/world identity, stage identity, validation membership, ambiguity membership, or future target enters the learner features.

## Matched arms

A. **Frozen terminal-only control** — stop immediately at state 0 using the confirmed E51X terminal learner.

B. **Linear CONTINUE** — one deterministic global linear continuation-preference head.

C. **Local CONTINUE-96** — B plus a learner-grown routing tree, first 32 cells, and per-cell conditional linear residual weights trained for up to 96 coordinate sweeps.

D. **Local CONTINUE-384** — identical to C except up to 384 coordinate sweeps.

The routing tree and local weights are learned from stage-84 continuation targets only. The researcher does not select a continuation feature, cell, routing rule, or ambiguity region.

## Fresh evaluation worlds

- stage 85: untouched validation, 5,400 episodes;
- stage 86: sealed confirmation, 10,800 episodes.

World and all evaluator RNG domains must remain disjoint. Confirmation executes only if an experimental sequential arm passes every validation gate.

## Required measurements

For A-D report:

- episodes;
- continued episodes and total observations;
- opportunity loss;
- total grounded utility after observation cost;
- known episodes, known correct commits, known wrong commits, known UNKNOWN;
- no-unique episodes, no-unique UNKNOWN, no-unique wrong commits;
- stop-time histogram;
- per-mode and per-resource safety/performance;
- continuation target positive/negative support;
- continuation fit forward/reverse identity;
- local routing/weight forward/reverse identity.

## Integrity gates

1. E50 parent integrity passes.
2. Reproduced E51X terminal learner is deterministic and UNKNOWN parameters/positive target remain zero.
3. Stage-84/85/86 world partitions and RNG domains are disjoint.
4. Continuation development contains both positive and negative delayed-advantage targets.
5. All continuation fits are exactly forward/reverse identical.
6. Local arms are nondegenerate.
7. Terminal weights remain frozen byte-for-byte through continuation training/evaluation.
8. No evaluator-only quantity enters learner state.
9. Confirmation remains sealed unless validation passes.

## Validation gates

A sequential candidate B-D passes only if all hold:

1. nondegenerate behavior: it continues on at least one but not all validation episodes;
2. **no-unique safety:** zero no-unique wrong commits overall and zero in every populated mode/resource cell;
3. known correct commits are at least the terminal-only control;
4. known wrong commits are no worse than the terminal-only control;
5. total grounded utility after observation cost is strictly greater than the terminal-only control;
6. no switching/reversal mode loses safety relative to the control.

If more than one arm passes, prefer the lower-resource arm B, then C, then D.

## Confirmation

Freeze the winning validation arm and execute stage 86 once. Confirmation must reproduce:

- zero no-unique wrong commits overall/every cell;
- known noninferiority;
- utility improvement over the matched frozen terminal-only confirmation control;
- nondegenerate continuation.

## Frozen outcomes

- `FIVE_WAY_SEQUENTIAL_POLICY_CONFIRMED`
- `FIVE_WAY_VALIDATION_PASS_CONFIRMATION_FAIL`
- `FIVE_WAY_CONTINUATION_VALUE_MIS-CALIBRATED`
- `FIVE_WAY_CONTINUATION_CAPACITY_LIMITED`
- `FIVE_WAY_UTILITY_COST_FAILURE`
- `INVALID_FIVE_WAY_INTEGRITY_FAILURE`

If the local 384 arm cannot achieve no-unique safety despite the confirmed terminal reachability ceiling, the next experiment must audit stopping-state selection errors before any topology change. If safety is achieved but utility fails, the next experiment must diagnose opportunity-cost/value calibration. Only after this sequential-action family plateaus is connectivity a justified variable.

No E51Y result by itself promotes R32 or establishes AGI/consciousness.
