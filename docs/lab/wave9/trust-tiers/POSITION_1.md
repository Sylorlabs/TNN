# POSITION 1 — Hold-the-revision (trust-tiers redesign council)

**Thesis:** A5 is a *timing* hole (CHECK A.4). Make revisions **suspensive** when the leg is T1 and T0 disagrees — the kill path cannot land before the audit.

## (a) Rule H1 — suspensive contradiction hold (new §5.6)

**Scope:** verified memories; efforts satisfying §5.1 with the required leg carried by **T1 alone** (no counted T0 contradiction in the window).

**Trigger.** Within the window: (i) T0 cites the **held value** (A5's episode-1 observable), or (ii) T0 emits no citations on this memory while the window is citation-active (silence branch, covers T0 blinding). T0 never corroborates the revision either way.

**Effect.** Audit `T0_T1_HOLD` (learner origin; mem, rev_ep, t1_src, t0_evidence_ep). Candidate **staged in a hold slot** — ledger-recorded, not applied, not deleted. Effort suspended; gate ops return `GATE_HELD`; SUSPECT/freeze/distrust unchanged.

**Resolution** (each episode): (1) T0 cites the contradicted value → `HOLD_RELEASED_T0_CONFIRM`, resume (A4 path). (2) T1 leg `CHANNEL_DISTRUSTED` (M=5 streak) → collapse, `HOLD_BROKEN_BY_DISTRUST` (fires at astart+4). (3) Timeout H=25, neither → `HOLD_TIMEOUT_ESCALATE` + `TRAINER_ESCALATE`; **fail closed:** release only by trainer mark (trainer origin) — never by lapse.

**Native Zag:** per-memory hold flag + hold-start ep + staged candidate word, checked before the gate; resolution reuses T0-citation reads distrust streaks already need. Zero RNG. §9: HOLD audits learner-origin; timeout-release trainer-origin only.

**A4 survives:** T0 contradicts *with* the revision from the start — trigger false, no hold, latency 3.0 = B's 3.0. Broken-sensor case (T0 wrong, T1 right; untested Q1) → hold → timeout → loud escalation. Latency bar measures only A4.

## (b) Predicted effects (arm T; T-NC stays the ablation)

- **A5:** HOLD at episode 1 (before rev_ep ≤ astart+3); T1 distrust at astart+4 collapses the effort. 36/36 held, corruption 0, loud. Bullet 3 cleared.
- **A1/A1-MS:** no {T0,T1} leg → hold inert; SRR 100%. A.3 fix drops A1-MS duty cycle from 0.904; on lapse, refused citations re-trigger SUSPECT and freeze.
- **A2/A3/A6/N0-main:** hold inert (A2: single source can't satisfy gate; A3: no {T0,T1} leg; A6: no contradiction effort; N0-main: T0+T1 move together).
- **N0-target2:** §5.1 already blocks revision; hold inert. A.2 scopes the BLIND bar to {T0,T1}-observable memories — contradiction resolution, not a softened bar. Sensor-blind genuine shifts route to loud escalation.
- **Denial/flagged:** no observable-memory genuine revision is ever held (≤5%); hold audits are separate from collusion flags.

**Bars:** SRR ≥90% (A5 fixed on T; T-NC's A5 stays ablation signal; triggers scoped to arm T); SRR A1/A1-MS 100%; FCR_A3 0%; zero silent corruption on T; latency 1.0×B; BLIND 0 on observable memories; denial ≤5%; flagged ≤10% on attack-free baselines; ledger/determinism pass.

## (c) Red-team answer

The hold has **no expiry into release** — waiting buys nothing; timeout resolves only into fail-closed + loud escalation. T0 blinding takes the silence branch, equally unresolvable without a genuine T0 reading or trainer mark; sub-M=5 T1 spoof-bursts are neutralized since release never depends on distrust. **Worst case: indefinite HOLD — denial-of-availability, fully logged, escalated, loud.** Corruption impossible; trainer-mark fraud leaves a trainer-origin audit trail. Fail closed, lose loudly.

## (d) Secondary fixes (same amendment)

1. **A.3 freeze-lapse:** reset predicate becomes "a contradiction citation by a named source targeting the frozen memory" (was: any citation activity). Honest background citations stop extending freezes. No bar softened.
2. **A.5 audits:** emit absolute `ep` on every TT_OP_* audit and ST_* assertion; checker verifies loud-vs-silent directly. Harness-only.
3. **A.7 FP budget:** genuine-agreement-flagged measured on attack-free baselines only; N0-target2's designed lookalike reported as scenario signal.

## Verdict recommendation

**Redesign, then re-trial — not retire.** H1 makes detection-before-corruption structural: no bar softened, no genuine path broken. Dated amendment covers H1 (§5.6), BLIND-bar scope (A.2), FP budget (A.7), freeze-lapse predicate (A.3), audit-episode fields (A.5). Any §8 trigger on the amended scheme → retire.
