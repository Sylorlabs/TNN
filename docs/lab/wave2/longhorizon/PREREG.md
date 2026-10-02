# Wave 2 — Long-Horizon Developmental Runs: Preregistration

**Agent:** E · **Date:** 2026-09-19 · **Branch:** `tnn-native-lab`
**Apparatus:** R34 v3 continual learner, Linux port (failures=0), extended natively on this VM.
**Philosophy (user direction):** long horizons test long-term learning and capability;
intelligence should emerge developmentally, like humans — not like an LLM.
Short runs can show *something*; only long runs show whether learning compounds.

## Apparatus recap (what the learner IS — white box)

- State: 2×2 score table (context × object) + counts, LCG rng, `updates`,
  `active` context, `contexts` ∈ {1,3}, one delayed-credit `pending` slot,
  `decisions`/`switches`/`outcomes`.
- Update rule: on delayed outcome, `score += reward*100`, clamped ±30000;
  `updates += 1`. Negative reward on a positively-scored cell with no
  exploration triggers a context switch (1→3 latent contexts max).
- Exploration: 1-in-5 random flip when enabled.
- Baseline: 48 updates over A(24)+B(24); gates: 16/16 positives post-train,
  return-A 15/16 with zero updates during return, determinism, checkpoint
  continuity, corruption refusal.

## Laws binding every variant (from DO_NOT_REPEAT.md — non-negotiable)

1. **Evaluator discipline (H-07):** fresh seeds per variant, documented;
   determinism check (two same-seed runs → `r34v3_equal`); matched controls;
   consumed probes never reused as fresh validation.
2. **No newborn restarts:** one lineage continues per variant; accepted floors
   are regression constraints, never reset to hide interference.
3. **Endpoint retention, never aggregate-only (E51 law):** report positives
   per regime and per replica at endpoint. Aggregate gains never cancel
   pointwise damage.
4. **Learner-core isolation:** `r34_learner_core.zag` stays unmodified.
   Any new learner core is a new named file with the same isolation check.
5. **Keep workloads small and harnessed** (znc self-host unqualified).

## What counts as "learning" vs noise (global)

- **Learning:** eval positives at/above the 48-update baseline gates at far
  longer horizons; new capabilities the 48-update run does not show
  (e.g. multi-regime retention, saturation-robust discrimination);
  deterministic reproduction (same seed → identical state fingerprint).
- **Noise:** eval positives within ±1 of the disabled-update control
  (12/24 on B) or the scrambled-reward control (0/16 on A); non-reproducible
  fingerprints; positives that collapse on return-to-regime.

## Variants

### LH-1 — Horizon ×10 (≈480 updates)
- **Hypothesis:** the delayed-credit rule stays stable at 10× horizon; eval
  positives remain ≥16/16 per regime; no update-count drift.
- **Config:** repeat the A(24-train)/B(24-train) block 10× in one lineage,
  eval probes interleaved per block, seeds fixed and documented.
- **Success:** `train_updates == 480`, per-block eval positives ≥16/16,
  determinism holds, no clamp-pathology in `R34V3_STATE` fingerprints.

### LH-2 — Horizon ×40 (≈1920 updates)
- **Hypothesis:** scores saturate at the ±30000 clamp (~300 updates/cell);
  the question is whether a saturated learner still discriminates or goes
  rigid. Either outcome is informative — rigidity is a *finding*, not a failure.
- **Config:** as LH-1, 40 blocks.
- **Success criteria:** report saturation point (updates at which each cell
  pins), post-saturation eval positives, and whether return-A retention
  degrades vs LH-1. Flag clamp-rigidity as a candidate mechanism for Agent F.

### LH-3 — Horizon ×100 (≈4800 updates) + slow regime drift
- **Hypothesis:** at very long horizons the learner either stabilizes into a
  durable two-context policy or oscillates; drift exposes which.
- **Config:** 100 blocks; every 10 blocks the regime mapping is perturbed
  (documented, seeded). If `world.zag` supports only regimes 0/1, drift is
  implemented as seeded reward-timing jitter instead — do NOT hack the world
  to invent regimes; record the constraint.
- **Success:** stability classification (stable / oscillating / collapsed)
  with fingerprint evidence; per-decile eval positives.

### LH-4 — Multi-return curriculum (A→B→A→B→A…)
- **Hypothesis:** the 3-context capacity supports repeated returns;
  A-retention stays ≥15/16 after every return (extends the `return_A_retained`
  gate across many cycles).
- **Config:** 12 alternations, 24-train per visit, return-eval with updates
  disabled after each return (mirrors the existing return gate).
- **Success:** per-return retention counts; any return <15/16 is a
  retention failure to report per the E51 law, not averaged away.

### LH-5 — Reward-corruption ramp (credit robustness)
- **Hypothesis:** the delayed-credit rule degrades gracefully with partial
  reward corruption, with a measurable knee.
- **Config:** corruption probability ramp 0% / 10% / 25% / 50% (seeded flips
  of the delayed reward sign), 480 updates each, else LH-1 protocol.
- **Success:** eval-positives vs corruption-rate curve; the knee point is the
  result. If 10% corruption collapses learning, that is a fragility finding.

### LH-6 — Scaled learner core (4×4 table, more contexts) — CONDITIONAL
- **Hypothesis:** the update rule scales beyond 2×2 without redesign.
- **Config:** new `r34v4_learner_core.zag` (4 contexts × 4 objects), same
  isolation check, LH-1 protocol.
- **Gate:** runs only if LH-1/LH-2 show stable learning. If the 2×2 learner
  is unstable at horizon, scaling it is banned until Agent F diagnoses why.

### LH-7 — Rapid-alternation interference (A/B every 4 episodes)
- **Hypothesis:** rapid switching causes interference the slow protocol hides;
  per-regime endpoint retention reveals it (E51-style).
- **Config:** 120 rapid cycles × 4 episodes, eval probes per regime every 10
  cycles, updates always on.
- **Success:** per-regime endpoint retention counts; interference declared if
  either regime's endpoint positives drop >2 below its slow-protocol level.

## Execution

- Variants live in `variants/LH-N/` (copied lab tree, modified harness).
- Each variant: `EVIDENCE_<stamp>/` bundle (commands, stdouts, exits,
  SHA256SUMS, RECEIPT.txt) mirroring the R34 evidence pattern.
- **Compute policy:** these binaries run in milliseconds; run freely.
  Take clear wins on the spot. Debatable tradeoffs → stop and flag with numbers.
- Nothing pushes to git. Results reported per variant with blockers.

## Amendment 2026-09-19 — Agent F rules-lab intake

- **P3 ADAPTIVE-EPS adopted as the default exploration rule** for all
  long-horizon variants going forward, replacing R34's fixed 1/5 ε-greedy.
  F's trials (3 seeds): training positives strictly ≥ baseline, ~53% fewer
  exploratory episodes, identical endpoints. Mechanics: exploration period
  p init 5; on learned negative reward p=max(2,p−1); on positive
  p=min(20,p+1); integer math only. Source:
  `../ruleslab/PREREG_P3_ADAPTIVE_EPS.md`, `../ruleslab/TRIAL_RESULTS.md`,
  impl at `../ruleslab/impl/p3_adaptive_eps/`.
- **P2 TWO-SPEED rejected** (systematic negative, 3/3 seeds). Do not rerun
  as-is. Recorded here so no future agent re-derives it.
- **P1 STRUCT-PROMOTE queued** — schema-faithful structural-revision learner
  (accepted/candidate tables, per-arm PROMOTE gate implementing the E51AJ
  law, revision ledger). Preregistered at `../ruleslab/PREREG_P1_STRUCT_PROMOTE.md`;
  needs 200+ episode horizons, i.e. long-horizon scope. Next in queue after
  P3 adoption is verified at horizon.

## ⚠️ Contamination notice — 2026-09-20 (R34 hidden-randomness remediation)

**Status: QUARANTINED.** The trials preregistered here (LH-1 through LH-7) were
executed with training phases running `explore_enabled=1`, engaging the hidden
seeded LCG (`r34v3_rng`) in `r34v3_choose` — a violation of the no-randomness
law (r34 RNG probe, workstream 2/8, commits `072f25aa` / `4976cbf5` on branch
`tnn-native-lab`; Micah's ruling: REMEDIATE). The hypotheses below remain on
record, but their verdicts (in the variant RESULT.md files) may not be cited as
canonical — including "delayed-credit stability at 10×/40×/100× horizons
(480/1920/4800 updates, 16/16)" and the noisy-reward fragility knee — until
clean reruns exist (deliberate or state-varying exploration, no LCG).
The original text above is left intact for the record.
