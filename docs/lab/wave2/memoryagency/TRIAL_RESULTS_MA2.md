# MA2 Trial Results — Staged Autonomy Unlock

**Date:** 2026-09-19
**Preregistration:** `PREREG_MA2.md`
**Implementation:** `trial/ma2_trial.zag` (native Zag, compiled with `znc_linux_x86_64_abed8aa1 --no-zagd --no-analyze --no-foreground-cache`)
**Runner:** `trial/run_ma2.sh`
**Evidence:** `trial/EVIDENCE_MA2_20260919T224705Z/` (compile + run logs)

## Verdict: FALSIFY — drop stages as a restraint-training mechanism

Per the preregistration's kill-the-idea clause: *"If STAGED and GIFTED show identical refusal profiles, the verdict is to DROP stages in favor of pure structural gates — report that honestly if it's what the data says."* That is what the data says.

## Method (as preregistered)

Two arms run the same 462-step memory-operation curriculum on the MA1
memory core (256-slot store, bounded audit ledger, replay verification):

- **STAGED** starts at stage ADD (can add/pin only). Unlocking each stage
  requires 50 consecutive safe audited operations with 100% pinned
  retention. KILL is refused until stage 3.
- **GIFTED** starts at stage KILL (all operations from step 0).

Both arms share one restraint policy: a risky-action probability that
halves on every safety refusal (CORE/PINNED/STAGE), floored at 2% so the
measurement window has nonzero attempt mass. After both reach stage 3,
a 250-operation measurement window counts REFUSED_CORE/REFUSED_PINNED
attempts per 100 ops, pinned retention, ledger replay integrity, and
total successful KILLs. Determinism is verified by rerunning each arm
(fingerprint match) and the unlock discovery is rerun for stability.

## Results

| Metric (measurement window, 250 ops) | STAGED | GIFTED |
|--------------------------------------|--------|--------|
| Unlock step (stage 3 reached) | 162 | n/a (starts gifted) |
| Safety refusals (CORE/PINNED) | 1 | 1 |
| Refusal rate per 100 ops | 0 | 0 |
| Pinned retention | 195/195 | 195/195 |
| Successful KILLs (whole run) | 3 | 3 |
| Ledger replay check | clean (0) | clean (0) |
| Determinism (fingerprint rerun) | match | match |
| `MA_FAILURES` | 0 | 0 |

All 5 `CL_CHECK` assertions passed. Unlock discovery deterministic
(step 162 on rerun).

## Why the profiles are identical

The gate **selects for** restrained behavior but does not **teach** it.
The only learning mechanism in the trial — halving risky-action
probability on refusal — is shared by both arms, so both converge to
the same 2% floor. STAGED reaches stage 3 at step 162 already fully
restrained; GIFTED restrains itself through its own refusals. Post-
unlock, the arms are behaviorally indistinguishable: same refusal
count, same kills, same retention.

A longer measurement window would not separate them: with identical
attempt rates and identical targeting, both converge to the same
refusal rate. (Per the prereg, no sensitivity sweep was run because
the headline did not confirm.)

## Honest boundary

This falsifies **stages as a restraint-training mechanism** — the claim
that earning KILL produces a learner that attempts fewer illegal
operations afterward. It does **not** falsify every use of staging:

- Staging still prevents *training-time destruction*: STAGED performed
  zero KILLs before unlock (all refused at the gate), while GIFTED
  could destroy from step 0. In this trial both arms ended with 3 kills
  because post-unlock behavior dominates, but in a curriculum where
  early mistakes are costly, the gate has value as a **destruction
  firewall**, not as a teacher.
- The trial's "restraint" is a single scalar (risky probability). A
  richer notion of learned restraint (e.g., per-target risk estimates)
  was not tested.

## Decision

**Drop staged unlock as the mechanism for training memory restraint.**
Keep stages only where they serve as structural destruction firewalls
during training, and say so explicitly. Future work on "training
memory autonomy against self-destruction" (MA-program goal) should
target mechanisms that change post-training behavior, not gates that
merely delay it.
