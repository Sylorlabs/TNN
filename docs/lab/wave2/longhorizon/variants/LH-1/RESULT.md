# LH-1 — Horizon ×10 (≈480 updates): RESULT

**Variant dir:** `variants/LH-1/` · **Evidence:** `EVIDENCE_20260919T221511Z/` · **Date:** 2026-09-19
**Seeds (fresh, documented):** learner `11001`, world/runtime `1101`, drift off (`LH_DRIFT_SEED=0`)
**Learner core:** `r34_learner_core.zag` byte-identical to canonical (`learner_core_unmodified=true`, `learner_core_isolation=true`). Harness-only changes in `r34_lh_harness.zag`.

## Hypothesis verdict: SUPPORTED

The delayed-credit rule is stable at 10× horizon. All prereg success criteria met:

| Check | Result |
|---|---|
| `train_updates == 480` | 480 == 480 ✓ (48/block × 10, one lineage, no restarts) |
| Per-block eval positives | **ea=16/16, eb=16/16 on all 10 blocks** |
| Determinism (two same-seed runs) | identical state fingerprint `fp=818888`, `lh_determinism=1`, world bytes equal |
| Return-A gate | `ra=15/16`, zero weight updates during return, `active=0` |
| Clamp pathology | none — max \|score\| = 18900 (s00), well under ±30000 |
| Controls (matched, fresh states) | disabled-update B: 12/24, updates=0; scrambled-reward A: 0/16 — both match the 48-update baseline exactly |
| Campaign failures | `LH_FAILURES=0`, runner `failures=0` |

Switch behavior is perfectly regular: 1 switch in block 0 (context 0→1 on first B-train), then exactly 2/block (1→0 at each A-train start, 0→1 at each B-train start), ending at `sw=19`. Scores grow near-linearly: s00 1900→18900, s11 1500→18400; wrong-cells sink: s01 −500→−4800, s10 −900→−5300.

## Method note (harness artifact found and fixed)

The first LH-1 run failed all `ea` probes (0/16) while `eb=16/16`: eval-A was run *after* B-training while `active=1`, so the probe read the B-context, not a learning failure. The harness was corrected so each eval immediately follows its regime's train (baseline acquire-gate semantics: train_A→eval_A→train_B→eval_B). Eval probes are context-relative — a fact Agent F should keep in mind for any probe design.

## What Agent F should know

- 10× horizon is a clean stability baseline: no drift, no saturation effects, deterministic to the fingerprint.
- The context-switch rule fires exactly when needed (2/block steady state) and never spuriously.
- Cost: ~2.3M cpu_us, 1.9MB RSS — trivial; longer horizons are cheap on this VM.

## ⚠️ Contamination notice — 2026-09-20 (R34 hidden-randomness remediation)

**Status: QUARANTINED.** The results in this document come from a training run
with `explore_enabled=1`, which engaged the hidden seeded LCG (`r34v3_rng`,
`(rng*997+7919) mod 1000003`) inside `r34_learner_core.zag`, driving 1-in-5
pseudo-random explore flips in `r34v3_choose` — hidden randomness in the AI's
decision path, violating the no-randomness law. This leg: LH-1, ≈480 updates (10× horizon), learner seed `11001`, world seed `1101`; training ran explore=1 (the `lh_train_regime` helper passes explore=1).
Verified by the r34 RNG probe (workstream 2/8), investigation commits
`072f25aa` / `4976cbf5` on branch `tnn-native-lab`; Micah's ruling: REMEDIATE.
The run is reproducible engineering evidence (byte-identical reruns hold) but
**not law-compliant evidence**. The stability verdict below stands recorded
but may not be cited as canonical — including the "delayed-credit rule is stable at 10× horizon" verdict (480 updates, 16/16 per block) — until clean
reruns (deliberate or state-varying exploration, no LCG) reproduce it.
The original text above is left intact for the record.
