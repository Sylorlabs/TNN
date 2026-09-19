# PREREG P1 — STRUCT-PROMOTE: schema-faithful structural revision learner

Status: PREREGISTERED 2026-09-19. Not yet implemented (candidate for Agent E
long-horizon wave or wave 3).

## Hypothesis

The R27 brain's actual learning operation — `diagnosis → proposal → measured
accuracy delta → PROMOTE/rollback` over structural state — can be implemented
as a native online rule, and it will show strictly better endpoint retention
(no pointwise/cohort damage) than R34's in-place additive updates, because
damage is quarantined in the candidate until measured.

## Rule mechanics

- Two 2×2 score tables: **accepted** (drives decisions) and **candidate**
  (receives all experience updates, R34-style additive ±100).
- **Diagnosis trigger:** negative non-explore reward, or a probe-window timer
  (every K=16 episodes), proposes the candidate's current argmax policy as a
  structural revision.
- **Measurement:** run the candidate's policy for a probe window of K
  episodes with learning frozen; record **per-arm** success counts.
- **PROMOTE gate (the E51AJ law):** promote (copy candidate → accepted) iff
  candidate's per-arm endpoint success ≥ accepted's per-arm success **on every
  arm** — aggregate improvement with any arm's regression = rollback.
  Else rollback (discard candidate, re-fork from accepted).
- **Ledger:** every decision recorded as
  `(diagnosis, proposal, base_per_arm, candidate_per_arm, decision)` —
  the native analog of `self_revision_history`.

## Predicted observable difference vs R34

- Fewer "ever-lost" arm successes across A→B→A (the E51AJ metric): R34's
  in-place updates can and do overwrite; P1 cannot regress any arm by
  construction of the gate.
- Slower initial acquisition (probe windows cost episodes) in exchange for
  monotonic per-arm endpoints.

## Falsification criteria

- If the gate never promotes over a 200-episode A/B/A run (threshold too
  strict to learn anything), the mechanism is rejected as vacuous.
- If per-arm endpoints are *worse* than R34's on any seed, the structural
  framing adds nothing over additive updates — reject.
- If probe windows dominate wall-clock (K too large relative to learning
  signal), downscale before claiming anything.

## Controls

Same world, same seeds, same A/B/return protocol as the P2/P3 trials.
Baseline = R34 rule (already run). Report per-arm endpoint success, promotion
count, rollback count, episodes-to-criterion per regime.
