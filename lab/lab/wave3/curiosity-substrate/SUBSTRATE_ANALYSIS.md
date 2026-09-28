# Curiosity v1 — what it ACTUALLY computes (read from source, not summaries)

Agent: Wave-3 curiosity-substrate investigator · 2026-09-20 UTC
Source: `sylorlabs/TNN` branch `tnn-native-lab`,
`docs/generations/R34/runs/R34_NATIVE_QUALIFICATION_STAGE_20260916/r34_curiosity_progress_v1.zag`
(blob `c094a6415536a99cb0a7b290c12fb308c451b608`, 3624 bytes, local copy at `/tmp/curiosity/`).
Tests: same dir, `r34_curiosity_progress_v1_tests.zag` (1608 bytes).

## Verdict on the survey summary

The RULES_SURVEY.md summary is accurate. No surprises in the source.

## Mechanism, function by function

The module is a per-slot scalar-error dynamics tracker. Slots are plain
indices into four parallel arrays the *caller* allocates and owns:
`fast:[]f32`, `slow:[]f32`, `count:[]i32`, `last_seen:[]i64`.

- **`r34c1_init`** — sets `fast=slow=initial_error`, `count=0`,
  `last_seen=-1` for every slot. Validates shapes (all arrays same
  length, `initial_error` finite and ≥ 0). Returns `0 / -340401 / -340402`
  (`OK / SHAPE / NUMERIC`).
- **`r34c1_observe_error(slot, step, error, fast_rate, slow_rate)`** —
  the only learning update in the module:
  `fast ← (1−fr)·fast + fr·error`, `slow ← (1−sr)·slow + sr·error`,
  `count++`, `last_seen=step`. Validates `error ≥ 0`, finite,
  `rates ∈ [0,1]`, and that the results are finite.
- **`r34c1_mean_age(step)`** — mean over slots of `step − last_seen`
  (seen slots) or `step+1` (never-seen), plus 1. Staleness normalizer.
- **`r34c1_score(slot, step, novelty_scale)`** — the curiosity signal:
  `score = |slow − fast| + [novelty_scale / (1 + count)] · (1 + age / mean_age)`.
  Per the author's own comment: `|slow−fast|` treats improvement and
  contradiction symmetrically; stable noise has high raw error but little
  dynamics separation; novelty is deliberately sqrt-free and conservative.
- **`r34c1_state_equal`** — exact bitwise equality over all four arrays
  (determinism / checkpoint support).

## What it does NOT do (honest gaps — these decide the trial)

1. **The caller supplies `error`.** The module computes no predictions,
   holds no hypotheses, models no uncertainty. "Curiosity" here is a scalar
   functional of an externally supplied error stream. Any claim about
   directed information-seeking lives or dies in the *caller*, not here.
2. **`|slow−fast|` detects change in error rate, not uncertainty.**
   A slot with high but perfectly stable error scores ~0 dynamics; a slot
   whose error is falling (or rising) scores high. It cannot distinguish
   "my predictor is improving" from "the world got easier".
3. **Novelty is pure visit-count** (`1/(1+count)`), content-free.
4. **Staleness grows with age regardless of informativeness** — re-probe
   pressure is unconditional, so it can produce churn, not just
   re-verification.
5. **No RNG anywhere in the substrate.** Already compliant with the
   no-randomness program law: deterministic given state and inputs.

## Compile status on the pinned lab compiler (new finding)

The verbatim repo source **does not compile** with
`znc_linux_x86_64_abed8aa1` (this is part of why it was "never wired"):

- `r34c1_finite` uses float literal `1.0e300` → `error: float literal
  magnitude out of supported range`. Probed: the compiler accepts f64
  literals up to `1.0e18`, rejects `1.0e19` and above.
- The repo tests use `zalloc(3)` → `let initializer type mismatch`
  (no `zalloc` on this compiler).

The lab port (`curiosity_v1_native.zag`, this dir) is logic-identical with
exactly two mechanical changes: `1.0e300` → `1.0e18` in the finiteness
guard (documented at the line), and malloc-based array allocation in the
test/trial harness (`_zag_malloc` + typed slice, proven pattern). No
arithmetic, no rates, no scoring formula changed.

## The question the trial must answer

The substrate is a well-formed *signal* (learning-progress dynamics +
count-novelty + staleness), but it contains zero hypotheses and zero
uncertainty of its own. Wired to the smallest honest caller (a 1-bit
persistence predictor per option, fully deterministic), does the closed
loop exhibit **directed information-seeking on the basis of the system's
own error dynamics** — or does the score reduce to novelty-with-a-fancy-name
(or noise-chasing)? The preregistered falsification criteria are in
PREREG.md.
