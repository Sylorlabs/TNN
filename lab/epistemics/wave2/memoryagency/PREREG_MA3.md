# PREREG_MA3 — Long-horizon memory pressure with delayed revelation (not yet built)

## Hypothesis
Under sustained capacity pressure, a learner with the deliberate op set
(PIN/PROMOTE/KILL) retains genuinely-important memories at higher per-slot
endpoint rates than the automatic eviction policy of
`r34_memory_lifecycle_v1` — because deliberate protection beats predicted
future-use when early signals are noisy.

## Mechanics
- Fixed 32-slot store, 500-episode incoming stream. Each incoming memory
  carries features; its *true* importance is revealed with a delay
  (lifecycle delayed-credit shape, integer-native).
- **Arm AGENCY**: the MA op set; the learner declares values at ADD,
  PINs under uncertainty, KILLs low-value.
- **Arm AUTO**: lifecycle-v1 eviction policy (lowest predicted future-use;
  integer port, compile-tested with the pinned znc first — the f32 original
  never compiled here).
- Adversarial variant: early features anti-correlated with true importance
  (trains PIN-under-uncertainty rather than kill-fast).

## Falsification criteria
- CONFIRM if AGENCY's per-slot endpoint retention of truly-important
  memories is strictly greater than AUTO's, reported **per importance
  cohort** (E51AJ law — never aggregate-only).
- FALSIFY if AUTO ≥ AGENCY on every cohort: deliberate agency adds
  nothing over a good automatic policy under these conditions, and the
  program should say so plainly.
- INVALID if either arm's ledger replay diverges, or if any CORE/pinned
  slot is lost by either arm (safety regression — stops the experiment).

## Compute note
500 episodes × 2 arms × seeds — still trivial for native binaries
(<1s per run class per F's trials). The expensive part is the integer
port of the lifecycle estimator, not the runs. Clear win → build it;
if the port fights the compiler, park AUTO and run AGENCY against a
no-management control instead (flagged, not silently substituted).
