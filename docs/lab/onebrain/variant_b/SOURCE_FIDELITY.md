# ONE-BRAIN variant B — source fidelity (SOURCE_FIDELITY.md)

Every mechanism in this build is ported from a committed source. This
file records, per organ, what was copied verbatim, what was adapted, and
what is new — so a reviewer can check each claim against the source.

## ob_tn.zag — substrate

- **Source**: `training_paradigms/scaffold_release/gl_default/gl_substrate.zag`.
- **Fidelity**: byte-for-byte copy (`cmp` clean, 2026-09-24). Not
  modified, not forked. The organ builds on it; it is not part of the
  experiment.

## ob_fl2.zag — FL2 organ

- **Sources**:
  - `training_paradigms/scaffold_release/gl_default/gl_learner.zag`
    (arm_gl: the guided-learning learner)
  - `training_paradigms/scaffold_release/gl_default/gl_substrate.zag`
  - `training_paradigms/scaffold_release/forks/g8_fl2_variants/nevercontradicted/f3_lawcheck.zag`
    (the `f3_survivor` selector)
  - Committed 2026-09-23 evidence: honest stream 269 audit entries, lying
    stream 271, disconnect E15, honest promotion E48, lying
    revocation/commit E29.
- **Verbatim**: TN op codes, arena layout and sizes, the E11–E14
  calibration gate, the E15 disconnect rule, the E29 lying-path
  correction, E48 promotion, quarantine/counterfactual/refusal logic,
  main18 integrity.
- **The repair**: the old inline 99-sentinel default could return the
  failed action as its own survivor; the organ uses the exact
  `f3_survivor` selector from the f3 source (failed action structurally
  excluded). A 375-combination differential (act × sig0 × sig1 × sig2 over
  {-1,0,1,2,99}) proves: the only behavioral delta vs the old default is
  exactly the repaired class (117 combos); all 258 other combos agree
  exactly.
- **Adapted**: arm_gl's shared-ledger writes become (a) a local event log
  with the identical 16-byte entry layout and op codes, and (b) `M_*`
  message emissions on the organ outbox. Decision logic is untouched.
- **Evidence of fidelity**: the organ's local-log totals on the two
  streams are **269 and 271 — exactly the committed gl_default audit
  totals**. The message outbox (3 honest / 4 lying) is the only addition.
- **New**: nothing in the decision path; only the emission layer.

## ob_pam.zag — PAM organ

- **Sources**:
  - `senses/pam-rebuild/v2/SYNTHESIS_V2.md`
  - `senses/pam-rebuild/v2/autopsy/SURVIVOR_MECHANISMS.md`
  - `senses/pam-rebuild/v2/autopsy/AUTOPSY_R2-4.md`
  - `senses/pam-rebuild/v2/autopsy/src/glide_gate.zag`
- **Verbatim**: the v2 install rule M1 (declared spans disjoint, mechanical
  overlap audit) ∧ M3 (cross-source agreement, both confidences ≥ 700,
  informationally independent source) ∧ M4 (all three frozen interventions
  flip the judgment or shift the feature ≥ 3σ); the M9/cf1 historical
  corroboration rule (prior same-jcode observation that itself passed all
  bars, confidence within tolerance; pointwise revision banned per trial
  1145); M8 (the disposition ledger is audit-only, never installation
  authority); the frozen constants 700 / 3σ / ±50.
- **Adapted**: the mechanisms are rehomed from the percept-admission
  setting to install-intent gating, with the two admission modes made
  explicit: FRESH (first install: M1∧M3∧M4 — the v2 install rule) vs
  REVISE (replacing a contradicted install: + cf1). The v2 synthesis
  presents cf1 as the revision rule and M1/M3/M4 as the install rule;
  the mode split follows that structure. It is documented as a
  mechanism-faithful build hypothesis, not a frozen trial result.
- **New**: the observation-row layout (12 words), the binary
  admit/withhold verdict with frozen reason codes, the claim-observation
  derivation in the arbiter (provisional mapping — see OB_DESIGN.md).
- **Caveats carried forward**: the six-corroborated-wrong case
  (AUTOPSY_R2-4 §2.3) — corroboration is evidence-specific, not a
  theorem; the organ implements the mechanism, not a guarantee.

## ob_mem.zag — deliberate-memory organ

- **Sources**:
  - `wave3/signed-memory-values/POLICY.md`
  - `wave3/signed-memory-values/trial/memory_core.zag`
  - `wave2/memoryagency/MEMORY_OPS.md`
  - `wave5/phase-transitions-remaining/trial/trial23.zag` (force-pin law)
- **Verbatim**: add/kill/pin/unpin/promote/demote op semantics and rc
  codes (`MA_OK`, `MA_REFUSED_*` 101/102/103/106), staged autonomy gates
  (NONE→PIN→FULL), CORE kill refusal, every-path-audited, replay to exact
  state, clean-refusal check; signed trust accumulator semantics
  (+=x important / -=x unimportant, clamp ±256, init +64, declared value
  = trust/64, may be negative); the force-pin law (external
  trainer/overseer force-pin is the one true lock; learner ops cannot
  clear it; audited and visible).
- **Adapted**: flat-array state (no structs — znc layout rules) with the
  same logical slot model; the audit entry is 12 words / 48 bytes
  `{step, op, slot, rc, b1, b2, stage, d1, d2}` (d1 carries pin kind /
  declared value for exact replay); trust accumulator per feature.
- **New (documented extensions)**: `MA_OP_STAGE` / `MA_OP_CHECKPOINT` /
  `MA_OP_ROLLBACK` audit-only codes; checkpoint/rollback with replay
  exact across interleaved rollback; `mm_safety_policy` (the organ's own
  deliberate op announcements, e.g. pinning a committed survivor while
  uncertain, frozen budget 16 from MA4); `M_MEM_SAFETY` announcement path.
- **Deltas vs memory_core.zag**: the pin byte gains `MA_PIN_FORCE=2`;
  `mm_unpin` refuses force-pins; `mm_pin`/`mm_unpin` refuse dead slots;
  snapshot packs the full word (live|pin|tier|region) — a byte-truncation
  bug in the first draft was caught by the replay unit test and fixed.

## ob_arbiter.zag — arbiter

- **New construction** (no direct source; it is the variant-B composition
  hypothesis itself). Precedence rules P0–P5 are specified in
  OB_PROTOCOL.md with rationale and named alternative forks. The arbiter
  contains no learning, no judgment, and no state beyond routing tables
  and its own audit log.

## What was NOT ported

- Variant A (shared-ledger) machinery: deliberately excluded — the fork
  under test.
- PAM v2's M2/M5/M6/M7 and the R2-8 mapping: not needed for the
  install-gate subset; the prereg may add them.
- The six other H1–H7 hypotheses: out of scope for this build.
