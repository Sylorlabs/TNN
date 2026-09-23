# PREREG — hypothesis-driven exploration (HDE v1)

Status: PREREGISTERED 2026-09-19, before any run. Amended same day for
Micah's program-law update (Amendment A1, §7).

## Hypotheses

- **H1 (main):** An explorer that spends its budget ONLY on tests derived
  from live, explicitly-represented hypotheses (H_ARM / H_SWITCH /
  H_RECRUIT, evidence-prioritized) finds the same structure as ε-greedy in
  fewer test episodes, with no RNG anywhere in its decision path.
- **H2:** Its remaining test episodes are mostly confirmatory
  (explore-success rate > baseline's ~50%), because tests are derived from
  claims, not coins.
- **H3:** The advantage concentrates where exploration is pure waste
  (long stable regimes) and where recurrence rewards partitioning
  (repeated regime flips); it vanishes where both agents hit the
  information ceiling (2-episode regime segments).

## Mechanism (frozen)

DESIGN.md §"The loop". Thresholds: CONFIRM support≥3, REFUTE refute≥2,
test budget 3, H_RECRUIT after ≥1 displacement, H_SWITCH when the other
context holds a CONFIRMED incumbent, moot rule (no challenger test once
the incumbent hit max observed reward), exhaustion backstop. Fixed
lowest-index tie-break. No RNG in the core; static grep check in evidence.

## Arms

- **HDE core** (`impl/hyp_core/`): the mechanism above, zero RNG.
- **Baseline** (`impl/baseline/`): wave-2 R34 rule, fixed ε=1/5 with LCG —
  the adversarial baseline being beaten (randomness-as-baseline is
  allowed; it is not part of the system under test).

## Curricula (designed, no RNG; world outcomes are deterministic in (regime, action))

All: base(16, frozen) → train → evalA(16, frozen, detection on) →
evalB(16, frozen, detection on) → returnA(16, frozen, detection on).
Train phases: learn=1, switching=1, exploration=1.

| id | train | n |
|----|-------|---|
| std | A(40) → B(40) — exact wave-2 protocol | 80 |
| single | A(16) → B(16) | 32 |
| flap | A(16) → [B(4),A(4)]×3 | 40 |
| walk | A(16) → B(16) → A(8) → B(8) | 48 |
| storm | A(16) → [B(2),A(2)]×6 | 40 |

## Metrics

Per curriculum per arm: positives per phase; `explores` (test episodes);
`expl_pos` (test episodes yielding +1); hypotheses confirmed / refuted
(core only); switches; contexts. Derived: train positives total,
explore-success rate = expl_pos/explores, confirmed/explores.

## Predicted directional outcomes (hand-derived from the mechanism)

- **std:** core train positives > baseline (fewer wasted flips);
  core explores < baseline; endpoints 16/16, 16/16, 15/16 both.
- **single:** core ≥ baseline (parity or small win).
- **flap:** near-parity predicted (±2; see Amendment A2 — 4-episode
  segments deny both agents consolidation; core wins on explore
  count/success rate rather than positives).
- **walk:** core > baseline (recurrence + no exploration waste).
- **storm:** no significant difference (both near the detection ceiling;
  2-episode segments < confirmation thresholds for any learner).
- **determinism:** two identical core runs → byte-identical TRL lines.
- **engagement:** hyp_confirmed > 0 in every curriculum.

## Falsification criteria

- **F1 (the "randomness with extra steps" test):** if core total train
  positives across all curricula ≤ baseline total → REJECT H1.
- **F2:** if core explores ≥ baseline explores AND core positives ≤
  baseline positives on the same curriculum → REJECT as randomness with
  extra steps.
- **F3:** if any `rng`/`RNG`/`random` token is found in
  `impl/hyp_core/learner_core.zag` → REJECT (program-law violation).
- **F4:** if two identical core runs differ in any TRL output line →
  REJECT the determinism claim.
- **F5:** if hyp_confirmed == 0 across all curricula → the hypothesis
  machinery was inert → REJECT.
- **Accept** requires: F1–F5 all pass AND core beats baseline on std and
  walk (the predicted-win curricula) AND explore-success rate(core) >
  explore-success rate(baseline).

## Honest negatives this prereg will record

Whichever way it goes: per-curriculum positives, explores, hypothesis
verdicts, and the verdict (POSITIVE/NEGATIVE/MIXED) with the mechanism
that produced it.

## §7 Amendment A1 (2026-09-19, Micah's program-law update)

The original design already avoided RNG in the core, but the amendment
makes it law rather than taste: (a) the LCG/state-rng is deleted from the
HDE core entirely — no `rng` field, no seeded init, tie-breaks fixed;
(b) "deterministic given state" is verified by rerun-diff, not asserted;
(c) the baseline's RNG is explicitly the beaten adversary, not part of
the system; (d) curricula are fully designed sequences — no seeded RNG
generates the environment. If a trial was already run before this
amendment, it would be re-run; none was (this prereg precedes all runs).

## §8 Amendment A2 (2026-09-19, prereg-stage mechanism refinement)

Smoke-testing (single-curriculum runs during implementation, before the
full trial) revealed two flaws in the preregistered priority rule:

1. **H_ARM-first destroys confirmed knowledge.** Resolving a lone-context
   surprise by re-learning the arm inside the same context overwrites the
   incumbent; on return to the earlier regime the frozen learner scored
   0/16 (vs baseline's 15/16 via context preservation). Replaced with
   **preservation before revision**: a lone-context surprise proposes
   H_RECRUIT first; H_ARM is the fallback if the partition test fails.
   The displacement-count rule is deleted.
2. **Inconclusive tests need escalation.** A challenger archived with
   mixed evidence inside one budget (some confirms, some refutes) is the
   signature of the world moving mid-test; grinding the arm question
   wastes the budget. Now escalates to H_SWITCH/H_RECRUIT.

Flap prediction adjusted: 4-episode segments are shorter than the
confirmation thresholds, denying both agents consolidation; the mechanism
now predicts near-parity (±2) on flap rather than a core win. The
predicted wins remain std and walk; storm remains predicted parity.

## §9 Amendment A3 (2026-09-19, post-observation mechanism repair)

The full A1+A2 trial ran clean (all curricula exit 0, deterministic), but
endpoint measurement exposed a defect the training totals hid: on
`single` and `walk`, frozen `evalB`/`evalA` scored 0/16 despite the
knowledge being present in the registry. Root cause, confirmed by
claim-state dumps: **spurious refutation**. When a regime change surprised
the incumbent, the triggering negative incremented the incumbent's refute
counter *before* the surprise handler attributed the surprise to the
context level (H_RECRUIT/H_SWITCH). Two regime-change negatives were
enough to REFUTE a claim with 20+ supports, destroying the very knowledge
the context switch was meant to preserve. The frozen detector then found
no confirmed claim to switch to.

A3 adds the **attribution rule** (credit assignment): evidence is counted
first (`h_count`), then the surprise handler decides attribution; when it
forms a cross-context hypothesis, the triggering negative is reassigned
from the arm level to the context level (the refute increment is undone)
before keep/discard transitions run (`h_transitions`). A negative
explained by "wrong context" is not evidence for "wrong arm". This is a
principled refinement, not tuning: it applies uniformly to all curricula
and follows directly from the hypothesis→test→evidence loop (evidence
must be attributed to the hypothesis it actually bears on).

Two implementation defects were also repaired in A3:
1. **Stale cross-context state in frozen mode.** A detection switch
   (`x_st==2`) formed during `learn==0` never resolved, because
   resolution lived inside the `learn==1` branch; the stuck state blocked
   all later frozen switches. One-shot hypotheses now resolve whenever
   their test executes, in any mode (seeding stays learning-gated).
2. **Spent double-count.** Splitting `h_update` into `h_count`/`h_transitions`
   briefly counted test spend twice (once at derive, once at count),
   archiving challengers after 2 tests. Spend is counted once, at derive.

Protocol conformance: the storm curriculum ran 11 segments (38 episodes);
the prereg specifies `[B(2),A(2)]×6` = 12 segments (40 episodes). The
12th segment (`tA7`) was added to both drivers and storm re-run.

The full five-curriculum trial was re-run from scratch under A1+A2+A3.
Results below are for the A3 mechanism; the A1+A2 endpoint failures are
retained as the developmental observation that motivated A3, not as
trial outcomes.
