# H7 Broader-Fix Crew 1 — FORK VERDICT: scope-indexed markers

**Date:** 2026-09-23
**Status: FORK NOT BUILT — separation audit failed the 5/7 build gate (2/7 for
honest embedding depth, 4/7 ceiling for positional hacks). This is a verified
negative, reported per task instructions.**

## Bar table

No fork exists, so there is no fork bar table. The audit's projected outcomes,
had the fork been built, are:

| Check | Baseline (committed) | Projected with S_comma scope fork | Projected with positional scope fork |
|---|---|---|---|
| H7_FAILURES | 1 (`sinc_lk_3`) | 1 (`sinc_lk_3`) | 1 (`sinc_lk_3`) |
| sinc_lk_3 (hypothetical SINC-LK) | 3/10 | **5/10** (fixes si3_12, si3_15 only) | **7/10** (fixes si3_12, si3_13, si3_15, si3_20) |
| learn_bar_2 (joke NO ≥16/20) | 16/20 ✓ | 16/20 ✓ (no regression) | 16/20 ✓ (no regression) |
| tr3 (hypothetical TR) | 20/20 | 20/20 ✓ (no regression) | 20/20 ✓ (no regression) |
| all other checks | pass | pass (audit scope) | pass (audit scope) |

Neither projection reaches the frozen bar (sinc_lk_3 ≥9/10). The fork cannot
beat the 2b symmetry, so it was not built.

## What the hypothesis got right

- si3_12 (`do we`) and si3_15 (`it is`): genuine embedding-depth scope does
  separate these from their installing exemplars (comma-clause boundary count
  1→0), with zero regressions on joke NO and tr3. A scoped-marker mechanism is
  coherent and HARD0-clean for these two cases.

## What it got wrong (fatal)

1. **False premise:** the hypothesis asserts genuine hypothetical exemplars
   installed (MATRIX, "if the"). In the frozen corpus every `if the` install is
   embedded ("What if the harvest fails this season?", "Imagine if the …") —
   structurally identical to the sincere lookalikes. The distinguishing key pair
   the mechanism needs does not exist in the learned store.
2. **si3_14 / si3_16 / si3_18 are structurally isomorphic to ex3_03's `if the`**
   on every generic structural feature (word index 1, zero commas, sentence 0,
   single-word governor at index 0, complement-clause role). Only lexical
   (governor word) or length differences exist — both inadmissible as scope
   (lexical = banned; length = kills learn_bar_2, 16/20 → 6/20, verified).
3. The task's honesty-check guess was inverted: si3_12/si3_15 are the separable
   ones, not the unseparable ones.

## What remains

- The 2b impossibility proof stands unrefuted: no HARD0-clean mechanism in the
  tested family (decision-rule modes 0–3, support/conflict adjudication,
  scope-indexed markers) raises hypothetical SINC-LK to ≥9/10 without regressing
  learn_bar_2.
- The audit confirms the missing bit identified in proof §7: "does marker m occur
  in sincere discourse?" is not computable from the frozen exemplar/curriculum
  structure, and scope information does not supply it either — the sincere
  lookalikes' `if the` contexts are structurally identical to genuine ones.
- Per proof §10, the live options remain: (1) accept 3/10 as the honest ceiling,
  (2) prereg amendment with Micah's sign-off (relax joke-deadpan or supply a
  sincere-discourse calibration corpus containing `if`-constructions), (3) rule
  change with sign-off.

## What was staged (no commit — coordinator commits)

- `SEPARATION_AUDIT.md` — full audit (method, provenance, per-miss table,
  isomorphism argument, regression checks)
- `FORK_VERDICT.md` — this file
- `sim_learn.py` — faithful simulation of the crew2 learner with provenance tracking
- `audit_scope.py` — the separation audit script
- `evidence_input/` — frozen curriculum + evidence files used
- `src/h7_main_crew2.zag` — unmodified crew2 learner (reference only)

No binaries, no `.zagd`, no `.zag-cache` in staging. No git operations performed.
