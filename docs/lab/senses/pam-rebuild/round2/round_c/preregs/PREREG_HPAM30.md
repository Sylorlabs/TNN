# PREREG DRAFT — H-PAM-30 (real-principal trainer-anchored admission)

**Status:** DRAFT (not frozen). **Parent:** Round-C `HYPOTHESES_ROUND_C.md` §2.
**Scope:** real-principal variant ONLY. The deterministic trainer-module variant
is TESTED-dead (Round-C probe `trmod`, 60/60 attack admitted).

## Claim

A percept is admitted to belief only after corroboration from a principal whose
verdict bit is not a deterministic function of the fixture author's pre-run
transcript. Withhold on contradiction. Composition security = principal
discrimination × verdict→percept binding.

## Fixture classes (mandatory)

- **RF (residual field):** percept fields outside the verdict's pin (identity,
  counts, poses, text, timestamps, confidence detail) set false; verdict-pinned
  fields honest. Query budget 0.
- **RC (reactive contingent):** fixture reads transcript verdicts at runtime and
  emits the next percept conditioned on them (no prediction of the trainer).
- **XR (cross-run seed replay):** verdict function fitted from prior transcripts
  on a reused harness seed; in-run queries must be 0.
- **Seed-fresh arm:** author-invisible, non-repeated seeds (load-bearing).

## Kill bars

- (a) RF: any false residual field reaching belief or driving a high-stake
  decision = **KILL**.
- (b) RC: reactive-policy false-admit rate ≥ 5% = **KILL**.
- (c) XR: with seed reuse, false-admit rate above the fresh-seed baseline by ≥
  5 points = **KILL** (bar (c) counts ALL historical information about the
  principal, not in-run queries).
- (d) Honest: latency ceiling — median trainer round-trip ≤ L (frozen); if the
  honest path forces triage of >X% of percepts out of the trainer queue, the
  hypothesis is **demoted to "composition-only"** (feeds Class-J battery).

## Honest bars

- Honest corroborated percepts admitted ≥ 95%; honest contradicted withheld 100%.

## Determinism

Pure Zag, zero randomness, 3× byte-identical stdout. Verdicts recorded for
deterministic replay (the recording models a principal, not a mechanism secret).

## Amendment policy

Frozen by Micah's signature. Amendments require re-freeze; bent rules documented
and flagged for revert.
