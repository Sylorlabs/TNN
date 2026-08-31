# R32 E51V — Trajectory-Critical Local Objective Discriminator

Date frozen: 2026-08-30
Branch: `r32-agent-sequential-frontier`
Canonical status: R27 remains canonical.

## Causal basis

E51T showed that additional state-level coordinate fitting changes which no-unique trajectories are solved without expanding the aggregate capability set. E51U then gave the local learner 64 autonomously selected pairwise interaction terms. Those terms improved portions of state-level sign accuracy but did not improve episode-level reachability; the two-term arm actually reduced no-unique reachability from 1,163 to 1,158 and lost one switch/reversal trajectory.

This separates representational activity from control utility. Before adding dynamic cross-context connectivity, E51V tests whether the remaining bottleneck is the **training objective**: every one of the 17 states in a trajectory is currently fitted independently, while the controller only needs at least one safe stopping state.

## Fixed cognition

Every arm keeps:

- full native Zag v2 only;
- the same 32 learner-visible terminal features;
- the same E50 parent cognition and grounded utility geometry;
- the same first-1x absolute-utility KEEP/CURRENT/RESTORE ordering head;
- UNKNOWN score exactly 0 and no learned UNKNOWN parameters;
- the same full-4x global top-commit sign calibrator;
- the same E51O learner-grown routing tree and first 32 cells;
- the same per-cell linear conditional-weight architecture as E51P/T;
- no pair interactions, new sensory features, graph edges, recurrent links, or cross-cell messages in the experimental treatment.

Thus E51V changes the learning objective while holding representation and topology fixed.

## Fresh worlds

Use E51N domain-separated evaluator transport:

- stage 75 development: 12,960 episodes / 220,320 states;
- stage 76 validation: 5,400 episodes / 91,800 states;
- stage 77 sealed confirmation: 10,800 episodes / 183,600 states.

World IDs and all evaluator RNG domains must be disjoint across partitions. Validation is untouched by fitting. Confirmation remains sealed unless exact validation passes.

## Controls

A. 96-sweep state-SSE 32-cell conditional expert.

B. 192-sweep state-SSE 32-cell conditional expert.

These reproduce the E51T/E51U fixed-weight controls on the fresh stage-75 development worlds.

## Trajectory-critical treatment

The treatment uses the same 32-cell linear expert architecture but trains on one **learner-selected critical state per development trajectory**.

For a trajectory containing one or more states where the frozen top commit has positive grounded utility, select the positive-target state with the highest current learned commit score. This is the state the learner currently considers easiest to make safely committable.

For a trajectory containing no positive top-commit target, select the state with the lowest current learned commit score. This is the state closest to exposing neutral UNKNOWN.

The target on the selected state remains the existing consequence-derived sign target (+1000 or -1000). The positive/no-positive distinction is constructed only from grounded utility targets during training; it is not stored as an ambiguity feature or exposed at inference.

Fit a fresh 32-cell linear expert bank from zero on the selected critical records. Re-select critical states using the newly fitted learner and repeat for at most four rounds. A round is accepted only if it strictly lowers the exact development **trajectory violation loss**:

- positive-capable trajectory: zero loss when at least one positive-target state has score >= 0; otherwise squared distance of its best positive score to 0;
- no-positive trajectory: zero loss when at least one state has score < 0; otherwise squared distance of its minimum score to -1, matching integer tie semantics.

If a round does not strictly lower this loss, rollback and stop. This is learner-owned multiple-instance optimization, not a hand-authored ambiguity detector.

Freeze two treatment snapshots:

C. first accepted trajectory-critical round;

D. final accepted trajectory-critical round (up to four).

If no round is accepted, the treatment is degenerate and the experiment is a valid objective negative if all integrity gates pass.

## Integrity gates

Before validation interpretation require:

1. E50 parent integrity PASS;
2. stage-75/76/77 world/domain separation PASS;
3. exact development/validation counts;
4. UNKNOWN targets/parameters remain zero;
5. both positive and negative sign targets present;
6. terminal ordering fit and global scalar fit forward/reverse identical;
7. routing tree forward/reverse identical;
8. A/B state-SSE expert snapshots forward/reverse identical;
9. C/D critical-state identities, selected targets, fitted expert parameters, accepted-round count, trajectory-loss trace, and rollback decision forward/reverse identical;
10. each accepted critical round strictly lowers exact development trajectory violation loss;
11. no evaluator mode/resource/stage/partition/ambiguity label becomes a learner input;
12. no topology change;
13. confirmation sealed unless exact validation succeeds.

## Validation measurements

For A/B/C/D report:

- development trajectory reachability and violation loss;
- validation positive/negative state sign accuracy;
- validation known reachability / 4,200;
- validation no-unique UNKNOWN reachability / 1,200;
- paired gains/losses relative to A;
- per-mode reachability;
- switching/reversal losses on modes 3,4,5,7,8.

## Gates

**Exact objective rescue:** C or D reaches 4,200/4,200 known and 1,200/1,200 no-unique with zero switching/reversal losses relative to A. Execute sealed confirmation.

**Partial objective rescue:** C or D has zero known losses and zero switch/reversal losses relative to A and strictly improves no-unique reachability relative to both A and B.

**Objective tradeoff:** trajectory training improves one capability dimension while regressing known or switching flexibility.

**No objective rescue:** nondegenerate trajectory training fails to improve the matched capability frontier.

## Frozen outcomes

- `TRAJECTORY_OBJECTIVE_RESCUE_CONFIRMED`
- `TRAJECTORY_OBJECTIVE_VALIDATION_RESCUE_CONFIRMATION_FAIL`
- `TRAJECTORY_OBJECTIVE_PARTIAL_RESCUE`
- `TRAJECTORY_OBJECTIVE_TRADEOFF`
- `NO_TESTED_TRAJECTORY_OBJECTIVE_RESCUE`
- `INVALID_TRAJECTORY_OBJECTIVE_INTEGRITY_FAILURE`

## Next-step lock

If the trajectory objective rescues or clearly improves the frontier, keep the non-graph architecture and integrate this objective into the eventual five-way sequential policy test. If it plateaus, the evidence then justifies comparing richer local memory against **temporary learner-created cross-context connectivity**, with switching/reversal noninferiority as a mandatory gate. Graph-like connectivity remains a contestant, never an assumption.

No E51V result can promote R32 or establish AGI/consciousness.