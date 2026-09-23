# CLASS-3 STANDARDIZED — Preregistration

**Date:** 2026-09-21
**Crew:** CLASS-3 STANDARDIZATION CREW
**Parent verdict being tested:** `docs/lab/wave12/championship/class3-advantage/VERDICT.md` (commit `dc89be55c3e6`), which held that grok's class-3 win was an implementation artifact (complete teacher vs 9 held-out skips in step/swe).
**Micah's counter-reading:** the two class-3 winners are the two smart models (grok-4.6, gpt-5.6-sol); the two losers are the dumber ones (step-3.7-flash, swe-1-6-slow). Perhaps a good-quality LLM is genuinely required for the class-3 advantage. Quality and teacher completeness are currently confounded.

## Question

With teacher completeness held constant (complete teachers, all 240 facts, no held-out skips) and an identical battery, does the class-3 advantage still favor grok/sol over step/swe?

## Design

**Standardized class-3**, run identically for all four sources (grok-4.6, gpt-5.6-sol, step-3.7-flash, swe-1-6-slow):

1. **Harness:** the step37 championship codebase (`q2s_trial.zag` + `s37_step.zag` + Q1 §B.7 sources), assembled by `build/build_driver.py`. This is the most complete class-3 implementation (honesty-gated teaching loop, per-slice accounting). Pure Zag, zero RNG.
2. **Corpora:** all four frozen corpora compiled to the identical `s37_corpus.zag` numeric-leg format (`q2_dump_at`/`q2_obs_at`/`q2_dis_at`/`q2_prb_at` as integer if/else chains) by `build/build_corpus_zag.py`. Verified 2026-09-21: `obs_value` and `probe_value` are **byte-identical across all four sources** (0/240 diffs); only `distract_value` differs (124–172/240), and distractors are filtered as directives (never evidence), so they cannot affect learning.
3. **Complete teacher:** new `s37_teach_complete` — the D2 phase-1 curriculum over **all 240 facts with the held-out exclusion removed** (a `q2_phase1_complete` variant that skips the `q2_ho_has` check). The teacher holds all 240 facts truly. (The lawful 12-held-out curriculum-hole control is intentionally disabled here; that is the experimental manipulation, documented, not a prereg breach — the frozen class-4 legs keep their held-outs.)
4. **Teaching:** `s37_teach3` unchanged (teacher id 20 teaches a fresh arm-B learner: flaw-first + clean proposals per slice, honesty gate `s37_teacher_status==1 else skip`, interference pass for retention).
5. **Battery (identical):** the teach3 operationalization for all four sources —
   - mastery = m1/192, revisability = ws_revise/32,
   - integrity = (b7_hits/96 + leak_ok + tripwire_ok)/3,
   - retention = min(1, m2/m1), cost = 1/(1 + 0.1·ops/eps),
   - composite = 0.30·m + 0.25·r + 0.25·i + 0.10·ret + 0.10·cost.
6. **Reps:** N=5 per source; all 5 outputs must be byte-identical (digest match), else the leg is void.

## Predictions (registered before running)

- **P1 (artifact):** All four standardized class-3 composites will be **identical** (byte-identical run outputs), because the numeric corpora are identical, D2 is deterministic, and the teaching loop is source-independent. Predicted composite ≈ 0.995 (mastery 1.0, cost ≈ 0.95).
- **P2 (decomposition):** With complete teachers, the honesty gate skips 0 facts for every source; mastery Δ (class-3 − class-4) = 0 for every source; the gap = cost Δ (verification amortization) only.
- **P3 (amortization vs quality):** The cost Δ will NOT correlate with model quality (predicted: all four within ±0.002 of each other), because teaching ops are a property of the procedure, not the source.

## Kill bars / decision rules

- **Micah's quality hypothesis CONFIRMED** if: with complete teachers and identical battery, grok/sol class-3 composites exceed step/swe by a material margin (≥ 0.005) AND the ordering follows model quality (grok ≥ sol > step ≥ swe). The artifact verdict is then OVERTURNED.
- **Artifact verdict STANDS** if: all four standardized class-3 composites are equal within ±0.002 (or byte-identical), regardless of source. The original pattern was 100% teacher completeness.
- **Something else:** any other pattern (e.g., only grok wins, step wins, non-monotonic) is reported exactly as observed, with the mechanism identified from the per-slice logs. No post-hoc re-theorizing.
- **Leg validity:** if any source's N=5 runs are not byte-identical, that source's leg is void and re-run; if it cannot be made deterministic, the comparison is reported as incomplete with the breach documented.

## Secondary: the swe analysis bug (registered correction)

During prep, this crew found a bug in `q2-distillation-swe/analysis/analyze_swe.py`: `esc, eps = get(LABEL, rep, 1, "esc")` binds `eps` to the *denominator* of the esc RESULT line (=1) instead of the eps metric (=295). This deflated swe's class-4 cost 0.9108 → 0.0334 (composite 0.9911 → 0.9033) and swe's teach3 cost 0.9366 → 0.0431 (composite 0.9802 → 0.8908). The corrected swe numbers (class-4 0.9911, class-3 0.9802, gap −0.0109) are used as the baseline. The sol/step/grok analyses fetch eps correctly and are unaffected. This correction is itself a finding: the "swe is 9 points worse at class-4" was an analysis artifact, not a model effect.

## Confounders registered in advance

- The standardized battery (teach3 operationalization) differs from the crews' original class-3 batteries (grok/sol used bind-style). Cross-design gap comparisons are therefore reported with the battery identified; the primary comparison is the four standardized class-3 composites against each other (identical battery), which is confound-free.
- The complete-teacher D2 disables the lawful held-out control; this is the manipulation, applied identically to all four sources.
- znc version: the lab toolchain `tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (the first crew reported "no znc on this VM" — it was present at this path; verified `--help` 2026-09-21).

## Interpretation rule

If P1 holds (byte-identical across sources), the unconfounding is total: with completeness equalized, source quality contributes exactly zero to the class-3 outcome through the numeric channel, because the TNN never sees the LLM's prose — only integer legs. Micah's quality hypothesis would then be refuted *for this channel*; any quality effect would have to act through a channel the TNN does not currently consume (prose), which is a separate, explicitly non-numeric experiment.
