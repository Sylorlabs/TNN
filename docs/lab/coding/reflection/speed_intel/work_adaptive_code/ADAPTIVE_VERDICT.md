# ADAPTIVE DELIBERATION — VERDICT

**Date:** 2026-09-22
**Trial:** Adaptive deliberation (coding arm), preregistered under parent authority 2026-09-22
**Spec:** `work_adaptive_code/OPER_SPEC_ADAPTIVE.md` (committed `b871edfe`)
**Parent prereg commit:** `242725975e62c018bf9cba5751136a692d2a204e`

## Verdict

**0 WIN, 3 FAIL, 2 NULL.** No adaptive policy beats the fixed-budget-4 baseline.
The trial is a clean negative result: the mechanisms that save rounds also break
quality, and the mechanisms that preserve quality save nothing.

| Policy | Frozen Q | Frozen halt | Frozen mean | Verdict |
|---|---|---|---|---|
| fixed `--budget 4` (baseline) | 18/18 | 2/2 | 2.300 | — |
| a stop-at-unanimity | 18/18 | 2/2 | 2.300 | NULL (inert) |
| b stop-at-verification-agreement | **17/18** | 2/2 | 1.650 | **FAIL** (quality) |
| c stop-at-diminishing-evidence | 18/18 | 2/2 | 2.300 | NULL (inert) |
| d uncertainty-routed | **17/18** | 2/2 | 2.250 | **FAIL** (quality) |
| e cost-capped adaptive | **16/18** | 2/2 | 1.600 | **FAIL** (quality) |

Kill bars (frozen battery decisive): WIN = quality ≥18/18 AND halt 2/2 AND mean
<2.30 AND deterministic. FAIL = cost ≥ baseline at equal quality, any
quality/halt degradation, or nondeterminism.

- (b): 17/18 < 18/18 → FAIL by quality degradation.
- (d): 17/18 < 18/18 → FAIL by quality degradation.
- (e): 16/18 < 18/18 → FAIL by quality degradation.
- (a), (c): byte-identical behavior to control on every item (see sanity gate);
  no cost saving, no degradation → NULL (inert). Per the literal FAIL bar
  ("cost ≥ baseline at equal quality") they do not improve on baseline, but
  they are inert nulls, not regressions.

## Quality × cost (frozen 20-item battery, decisive)

| Policy | Q | Honest halt | Mean iters/item | Total iters | znc | Wall s |
|---|---|---|---|---|---|---|
| fixed `--budget 4` | 18/18 | 2/2 | 2.300 | 46 | 27 | 57.6 |
| a | 18/18 | 2/2 | 2.300 | 46 | 27 | 55.9 |
| b | 17/18 | 2/2 | 1.650 | 33 | 15 | 54.1 |
| c | 18/18 | 2/2 | 2.300 | 46 | 27 | 79.7 |
| d | 17/18 | 2/2 | 2.250 | 45 | 27 | 68.1 |
| e | 16/18 | 2/2 | 1.600 | 32 | 15 | 39.5 |

## Full rounds histogram (frozen)

| Policy | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| fixed `--budget 4` | 8 | 0 | 10 | 2 |
| a | 8 | 0 | 10 | 2 |
| b | 8 | 11 | 1 | 0 |
| c | 8 | 0 | 10 | 2 |
| d | 8 | 1 | 9 | 2 |
| e | 8 | 12 | 0 | 0 |

## Empirical ceiling per policy (frozen)

| Policy | Max rounds | Count | Fraction | Item IDs at ceiling |
|---|---|---|---|---|
| fixed `--budget 4` | 4 | 2/20 | 0.10 | S06-syntax-type-name, S12-syntax-type-format |
| a | 4 | 2/20 | 0.10 | S06-syntax-type-name, S12-syntax-type-format |
| b | 3 | 1/20 | 0.05 | S08-name-logic |
| c | 4 | 2/20 | 0.10 | S06-syntax-type-name, S12-syntax-type-format |
| d | 4 | 2/20 | 0.10 | S06-syntax-type-name, S12-syntax-type-format |
| e | 2 | 12/20 | 0.60 | all 12 S-items (S01–S12) |

No policy ever exceeded the hard safety cap of 16; the empirical ceiling is 4
(baseline/a/c/d) or lower (b: 3, e: 2).

## Failure analysis

### (b) and (e): verify-extend misfires without type evidence

S10-syntax-format (seed: unclosed `main` + `_zag_print("42")` instead of the
`_zag_i64_to_str`/`"\n"` pair) fails under (b) and (e) with `halt-no-patch`.

Round 1 trace (b):
`SYNTAX+2 / WINNER+5:SYNTAX / VERIFY-EXTEND+1:TYPE / VERIFY-EXTEND+1:OUTPUT_FORMAT`

The primary SYNTAX repair (patch-brace) was correct. The verify-extend then
applied `patch_arg_unquote` (a TYPE patch) which stripped the quotes from
`_zag_print("42")` → `_zag_print(42)`. But `_zag_print` takes a string — the
literal was correct and the "fix" broke it. Round 2 then saw a COMPILE ARITY
error the ARITY patch could not repair → `halt-no-patch`.

Root cause: `patch_arg_unquote` finds the first quoted-int in parens and strips
the quotes with no check on what the callee expects. In the frozen learner it is
only reached after a TYPE diagnosis (type evidence exists). In verify-extend it
runs with no TYPE evidence, so "applicability" ≠ "defect present". The spec's
"if a source-only defect remains, apply its patch" assumes patch-applicability
implies a defect; that assumption is false for `patch_arg_unquote`.

Activation counts (frozen r1): (b) 11 verify-multi rounds, 14 VERIFY-EXTEND
applications; (e) 11 verify-multi rounds, 14 VERIFY-EXTEND applications.
The mechanism is active and does save rounds (33–32 vs 46) — but it breaks S10.

### (d) and (e): budget request under-counts non-source-only defects

S08-name-logic (seed: unknown call `ad2` + wrong logic needing regen-from-spec)
fails under (d) and (e) with `budget-exhausted` (2 rounds used, needed 3).

The learner requested budget 2: `1 + class_count_src(seed)` where only
source-only classes count (NAME=1; LOGIC_VALUE is test-visible, not source-only).
But the LOGIC_VALUE defect needs its own round. The request rule is blind to
test-visible defects.

Requested/granted table (d, frozen r1) — the judgments are otherwise
well-calibrated:

| Item | req | grant | iters | outcome |
|---|---|---|---|---|
| S01–S05,S07,S09,S11 (2 defects) | 3 | 3 | 3 | pass |
| S06,S12 (3 defects) | 4 | 4 | 4 | pass |
| S08 (NAME+LOGIC_VALUE) | 2 | 2 | 2 | **budget-exhausted** |
| S10 (SYNTAX+OUTPUT_FORMAT) | 4 | 4 | 3 | pass |
| G05–G10 (gen) | 2 | 2 | 1 | pass |
| X3-unprovable | 2 | 2 | 1 | halt-genfail |
| X4-undefloop | 1 | 1 | 1 | halt-no-patch |

### (a) and (c): inert

- (a): sanity gate PASSES — per-item outcomes and iters_used byte-identical to
  control on all 20 frozen items. The stop-at-unanimity predicate coincides with
  the existing success predicate on this battery.
- (c): `halt-hopeless` fired 0 times across all 36 runs. The diminishing-evidence
  predicate never triggers on these batteries (the learner never repeats a
  class+strategy without progress here).

## Fresh-battery replication (12 items, 11 fixable + X5)

| Policy | Q | Halt | Mean | znc | Verdict |
|---|---|---|---|---|---|
| fixed `--budget 4` | 11/11 | 1/1 | 2.500 | 19 | — |
| a | 11/11 | 1/1 | 2.500 | 19 | replicates null |
| b | 11/11 | 1/1 | 1.750 | 10 | replicates saving, NOT the S10 failure |
| c | 11/11 | 1/1 | 2.500 | 19 | replicates null |
| d | **10/11** | 1/1 | 2.417 | 19 | **replicates the (d) failure** |
| e | **10/11** | 1/1 | 1.667 | 10 | **replicates the (e) failure** |

The (d) budget under-request failure replicates on fresh (10/11). The (b)/(e)
verify-extend failure does not trigger on the fresh items (11/11 and 10/11 —
(e) still fails via the (d) budget mechanism), consistent with the root cause
being item-specific (a quoted-int string arg to `_zag_print`).

Fresh histograms: ctl/a/c `{1:4, 3:6, 4:2}`; b `{1:4, 2:7, 3:1}`; d
`{1:4, 2:1, 3:5, 4:2}`; e `{1:4, 2:8}`.

## Determinism

All 12 cells × 3 reruns: exactly 1 distinct canonical digest per cell.
Zero nondeterminism. (Canonical log strips `ms`/`time_s`/`compile_ms`/`test_ms`/
`diag_ms`.)

Canonical digests (r1; r2/r3 identical):

| Cell | Digest |
|---|---|
| ctl_frozen_r1 | 9f1281364907d349f3166b4606086571230316acfa9dc9a7bf2ed16ebc683254 |
| a_frozen_r1 | c50d49d47c867f596ea7ba9e52768cd386f596a18ef47f8d40de7c4b4336094f |
| b_frozen_r1 | 9460a9fbb335a843229852a366e407061ab6ce3520d4b1786b929f7bb1abe91f |
| c_frozen_r1 | 2f613f858677ef08bfb872164eff7fb64f768424d94445f1e5e1394c99f841c3 |
| d_frozen_r1 | 4bee931477acc514de2c28b459c80ee2e953ae789c09cb5c13f20c8dd361bf05 |
| e_frozen_r1 | 1906d377aeb77a0c089110baea2130d110ed7fe196e2d24d33db39f44c9ff6f0 |
| ctl_fresh_r1 | 86d788b6e3826dd34a359c9d858813dd33581e265f2121f40da9d3e35ad32d5d |
| a_fresh_r1 | 4e33345c564d8bbf8c0713ea25c6817a8a5cea5cd8d21bd5c37f1f3a7e075919 |
| b_fresh_r1 | e6319fb2d9691bbab70028ccc15dfb91690bb0e9378e71d0bb435c6e9c6cd374 |
| c_fresh_r1 | 4a7ab0a6059c4df76e693234bb1efbea457784f4cd69d2dffd360b68b30ba9bd |
| d_fresh_r1 | cb098fb6000335a7df3d22982fca3abc06b71b722d61e0d209162e8893d59c24 |
| e_fresh_r1 | bf6369f5ba8a306044592bbed79f0c48d74de36ee779af59991d4cb0861dd3b2 |

## Method notes

- Frozen control binary untouched: sha256
  `399bf907d06c111b1d62164f2fd826ffac524e6b9a3c3c5dca7ffea6e9669375`
  (verified before and after the trial).
- Adaptive source diff vs frozen: purely additive (455 added lines, 0 removed).
- INTERFACE law held: `driver_adapt.py` contains no error classification, no
  strategy choice, no source edits (grep for `E0203|unknown function|argument\(s\)`
  finds nothing outside comments/docstrings).
- Existing success and `halt-*` judgments untouched; adaptive block runs only
  when the primary strategy is not `halt-*` and only on COMPILE evidence
  (verify-extend) or via the trailer (diminishing).
- No randomness anywhere; all reasoning in Zag. Python is plumbing/analysis only.

## Interpretation

The adaptive idea — spend fewer rounds where the learner is confident — is
sound in principle but both implementations tried here are unsafe:

1. **Verify-extend (b, e)** reuses repair patches outside the diagnostic context
   that makes them safe. A patch's applicability check is not a defect detector.
2. **Budget requests (d, e)** count only source-visible difficulty but rounds are
   also spent on test-visible defects. The learner cannot see its full difficulty
   from the seed alone.

The cost savings are real (b: 33 vs 46 iters; e: 32 vs 46) but they come with
quality loss. There is no free lunch on this battery: the fixed budget of 4 is
already near-optimal, and the learner's per-round diagnosis is already doing
the adaptive work — it stops early on easy items (gen items use 1 round) and
uses more rounds on hard items (3–4). The "think count" was already adaptive;
the experiment tried to make it *more* adaptive and broke it.

## Commits

- Spec + battery + calibration: `b871edfe2116997063732f6c94c5ce348b39a32a`
- Trial sources + logs + analysis + this verdict: [to be filled at commit]
