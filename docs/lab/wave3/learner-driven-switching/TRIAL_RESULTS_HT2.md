# TRIAL_RESULTS_HT2 — the learner-driven switching trial (RUN 2026-09-19/20)

## Verdict: POSITIVE

The HT2 learner — which holds an explicit hypothesis, raises doubt only
on recorded contradiction, and probes/switches only on deliberately
issued evidence — passes Micah's acceptance test (the randomized
switching curriculum does not fail) **and** the designed adversarial
curriculum with every preregistered expectation met exactly, including
all four adversarial signatures. 38/38 checks, byte-identical reruns,
zero `CL_CHECK` mismatches.

## What ran

One native binary (`ht2/trial_ht2.zag` → `ht2_trial_linux`), three arms
on curriculum R plus HT2 on curriculum A. Runner: `ht2/run_ht2.sh`.

- **HT2** — mechanism (`ctx_core.zag`, byte-identical to HT1) + the new
  learner-driven trigger (`ht2_learner.zag`): doubt → deliberate
  verification → explain / falsify → test alternatives in deterministic
  slot order → one educated novel guess → overturn on failure.
- **HT1R** — fidelity control: HT1's protocol-fixed policy copied
  verbatim from `trial_ht1.zag`, identical flip sequence and noise seed.
- **TOY** — R34 v3 core, unmodified: expected-negative control.
- **HT2 on A** — fully designed adversarial curriculum, zero RNG.

Program-law static checks (in the runner, before compile): the learner's
decision file contains **no randomness source and no clock source** —
decisions are functions of (hypothesis state, recorded evidence) only.
`ctx_core.zag` / `toy_core.zag` / `substrate/` verified byte-identical
to HT1's; the trigger is new, the mechanism is not.

## Curriculum R (randomized; 10 true flips, 15% channel noise)

| arm | switches | collapsed blocks | end R0 | end R1 | blocks |
|---|---|---|---|---|---|
| HT2 | 11 | 0 | 16/16 | 16/16 | 16,16,16,16,16,16 |
| HT1R | 11 | 0 | 16/16 | 16/16 | 16,16,16,16,16,16 |
| TOY | 357 | 2 | 16/16 | **0/16** | 0,16,16,16,0,16 |

- **HT1R fidelity confirmed**: reproduces HT1's reported CTX numbers
  exactly (11 / 0 / 16 / 16) — the harness is faithful, the flip
  sequence is HT1's.
- **Toy control stressed**: 357-switch storm, two collapsed blocks,
  one endpoint regime at 0/16 — HT1's toy signature reproduced, so the
  comparison is valid (criterion 9).
- **HT2 internals (R)**: 12 doubts = 10 flips + 1 settle-regime switch
  + 1 noise-induced false doubt; 11 falsified → 11 switches (bounded:
  11 ≤ 2×10); **1 explained** — a false doubt whose verification
  confirmed the hypothesis, producing zero switches by learner decision;
  1 educated guess (the first flip, with only partition 0 live: smallest
  non-live label proposed, tested, committed). Zero overturns on R
  (no false falsification survived to the guess stage).

Headline outcomes match HT1 exactly; the difference is internal and
structural: HT2 issues probe batches only when doubt is recorded
(steady-state episodes cost zero investigative work), and it can
*withhold* a switch — a move HT1's protocol has no vocabulary for.

## Curriculum A (designed adversarial; zero RNG)

Totals: doubts 13, switches 11, explained 1, overturned 1, guesses 2,
collapsed blocks 1, endpoints 16/16 both regimes. Per-episode
attribution (designed → observed):

| event | designed intent | observed |
|---|---|---|
| A1 (eps 3, 30): isolated lies | 0 doubts, 0 switches | 0 doubts, 0 switches ✓ |
| A2 (ep 15): pre-flip burst on the *correct* hypothesis | exactly 1 doubt, 0 switches, explained | doubt@15, switch@17 on the real flip, `n_explained=1` ✓ |
| A3 (flip 1→0 @22, masking 22–24) | switch ≤3 episodes after honest evidence resumes (≤ep 26); block@24 collapses (preregistered) | switch@25; blocks `16,16,0,16,16,16` — only block 3 (@24) collapsed ✓ |
| A4 (ep 38): forced noisy verification on the correct hypothesis | 0 switches, exactly 1 overturned falsification, full ledger chain | doubt@38, `TEST_ALT(fail) → GUESS(fail) → OVERTURN → COMMITTED`, 0 switches ✓ |

- Doubt episodes: `{6,11,15,17,25,28,33,37,38,41,44,47}` — exactly the
  10 flips + A2 + A4, nothing else. Switch episodes:
  `{6,11,17,25,28,33,37,41,44,47}` — exactly the 10 R-phase flips,
  with A3's recovery on the first honest episode (25).
- Audit invariants (`ctx_audit_clean_refusals`, `ctx_replay_check`,
  `ctx_switch_verified_scan`) pass on both arms; `ht2_causal_check`
  passes — every probe and every switch in the decision ledger is
  causally preceded by recorded evidence, and the check was proven to
  fail on forged unfalsified-switch ledgers (negative unit tests).

## Unit tests (8/8)

`unit_refusals` (HT1 mechanism invariants) plus seven HT2 learner
tests: no-doubt-without-contradiction, explained contradiction,
falsify→test-alternative→switch, educated guess, overturn after failed
alternatives and failed guess, backoff-then-retrigger, and causal-check
negatives (forged ledgers fail).

## What this does NOT show

The 8-bit passive rate is a curriculum parameter (the learner doesn't
choose what the world presents); alternative scan order is lowest-slot
first (deliberate simplification); partitions are never killed;
2 regimes only; BACKOFF is unit-tested, not curriculum-tested; the
4-slot/256-entry caps are engineering limits, not tested under
pressure. On R the headline numbers tie HT1 — the claim is about *how*
the decisions are made (evidence-triggered, doubt-gated, withholding),
not a higher score.

## Scale statement

Decision cost: O(partitions) per doubt episode, O(1) per steady-state
episode (zero probe batches when committed — investigative cost follows
world adversity, not time); no accumulators (no drift); deterministic
given state. Named next test, not run: **HT2-SCALE** (16 partitions,
4 regimes, 480-episode designed curriculum, slot-pressure events,
ledger caps ×20, ring-ledger observation design).

## Evidence

- `ht2/EVIDENCE_20260920T002554Z/` — compile log, two byte-identical
  run outputs (`SHA256SUMS`: `82ec0302…`), per-check results.
- `ht2/ht2_learner.zag` — the learner (static-checked: no RNG, no clock).
- `ht2/trial_ht2.zag`, `ht2/run_ht2.sh` — trial driver and runner.
- Preregistration (unchanged since before the first run):
  `PREREG_HT2.md`; design: `TRIGGER_DESIGN.md`.

## Recommendation

**Keep HT2 as the switching line.** The learner now owns probe/switch
timing with white-box, replayable justification for every action, and
it withstood the designed adversarial battery (withholding, overturn,
masking recovery) while matching HT1 on the randomized acceptance
test. Next: HT2-SCALE for the slot-pressure and ledger-capacity
questions, and MA-KILL unification (partitions the learner can retire)
before any larger claim.
