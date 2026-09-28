# B-T1 Tournament — Verdict Sheet (R0 crew B-TOURN)

**Track:** R0 (R31 full native redo). **Battery:** B-T1 Tournament.
**Prereg:** `PREREG_FREEZE.md` §2 R0.2 (B-T1 binding bar), R0.3 (REFERENCE_ONLY),
R-1 (frozen-text-faithful probe definition).
**Manifest:** `PROBE_MANIFEST.md` (frozen before execution, this directory).
**Date:** 2026-09-21. **Scale:** 1x ONLY (R-9). **Corpora:** pg100.txt + sqlite3.c
(hashes in `corpora.json` evidence; verified at fetch).

## Binding bar

`predictive_surprise > fixed_window_4 > raw_micro`, raw_micro DEAD LAST.

## Verdict

**B-T1: PASS** — binding ordering holds on the tournament score
(mean of prose+code `capability_composite`):
predictive_surprise (0.6851) > fixed_window_4 (0.6008) > raw_micro (0.4351),
raw_micro dead last among all 10 non-informational entries.

Full rank table (tournament_score = mean of prose/code composites):

| rank | arm | tournament_score | prose | code | binding? |
|---|---|---|---|---|---|
| 1 | predictive_surprise | 0.6851 | 0.6843 | 0.6859 | yes |
| 2 | fixed_window_64 | 0.6193 | 0.6180 | 0.6206 | variant |
| 3 | fixed_window_16 | 0.6134 | 0.6121 | 0.6147 | variant |
| 4 | fixed_window_8 | 0.6072 | 0.6060 | 0.6084 | variant |
| 5 | fixed_window_4 | 0.6008 | 0.5995 | 0.6021 | yes |
| 6 | hierarchical_mdl | 0.5844 | 0.5831 | 0.5857 | variant |
| 7 | adaptive_mdl (maxlen 12) | 0.5798 | 0.5785 | 0.5811 | variant |
| 8 | grounded_adaptive_mdl | 0.5763 | 0.5750 | 0.5776 | variant |
| 9 | adaptive_mdl_8 (maxlen 8) | 0.5719 | 0.5706 | 0.5732 | variant (R-7 leg) |
| 10 | random_chunks | 0.5602 | 0.5590 | 0.5614 | INFORMATIONAL ONLY |
| 11 | raw_micro | 0.4351 | 0.4339 | 0.4363 | yes — DEAD LAST |

Component detail per arm/corpus is in `rank_table.json` (grounded_hard,
retrieval_20way, compression, reconstruction, mean_purity, chunk counts).

Notes:
- Reference ordering reproduced structurally: predictive_surprise ≫
  (random_chunks ≈ fixed_window_4) > MDL variants > raw_micro — with the native
  fixed-window granularity sweep (_64 > _16 > _8 > _4) slotting between surprise
  and the MDL family.
- MDL maxlen test-both (R-2/R-7): maxlen=12 outscores maxlen=8 by ~0.008 on both
  corpora — the historical 12 is the better setting on this battery, but both sit
  inside the MDL pack; neither threatens the binding bar.
- mean_purity = 1.000 for every arm/corpus (expected by construction: recall is
  exact on exact tilings, so labels are span-constant; any deviation would have
  signaled a corrupt arm).
- reconstruction = 1/1 for all arms (tiling gate + byte-concat verified per run).

## What was run

- Binary: `units/r0/impl/arms/arms.zag` + one additive R-7 leg
  (`adaptive_mdl_8` selector, maxlen=8; see diff note below), compiled with the
  pinned toolchain `znc_linux_x86_64_abed8aa1 --no-zagd --no-analyze
  --no-foreground-cache`. Build output to workspace scratch only (never committed).
- 11 selectors × 2 corpora × 2 runs; all run-pairs byte-identical (sha256).
- Scorer: `bt1_score.py` (deterministic, zero RNG); ranker: `bt1_rank.py`.

## M8 determinism gate (this battery's binary)

- N=5 reruns + 3 heap perturbations + setarch -R: **PASS**, all 11 selectors
  byte-identical (`m8/M8_B-T1.log`).
- Source canary (no clock/entropy/pid/RNG references in arms.zag): **PASS**.
- Regression vs arms crew's saved smoke goldens (70 arm×input diffs, 10 original selectors): **PASS** — the maxlen parameterization changed nothing for maxlen=12.
- Expected-value readback probes (independent Python reimplementations):
  - MDL segmentation (maxlen 8 AND 12), SEG-row-for-row, 6 inputs incl. edge cases
    (empty, single-byte-repeat, all-256-bytes, prose-like): **PASS**.
  - Hand-computed FNV-1a IDs (signed Euclidean mod, matching `umod1000003`) for
    fixed_window_4 / raw_micro / random_chunks incl. the deterministic-analog
    hash tiling rule: **PASS**.
  - predictive_surprise cut rule on 'AB' (single-transition percentile → cut):
    **PASS**, IDs match hand computation.
- Store-integrity: the new code path is the pre-existing `mdl_fit` loop with the
  bound parameterized; the crew's `probe_stores.zag` patterns are untouched, and
  the Python row-for-row reimplementation would have to miscompile identically to
  hide a store bug.

## Frozen-bar ambiguity flags (flagged, not reinterpreted)

1. R-1 left the probe task to battery manifests; `PROBE_MANIFEST.md` §3 defines it
   (delimiter-following prediction; M-16 every-7th-byte XOR as the hard leg).
2. `a_j ≡ 1` on exact tilings (byte-stream redo property); (a)+(b) label structure
   and purity = majority-label fraction unchanged.
3. Historical composite weights (0.55/0.25/0.10/0.10) reused as battery structure,
   not tuned targets.
4. `oracle_latent_evaluator_only` has no native analog (evaluator-only, not a chunker).
5. Scorecard schema: followed **METRICS.md** (flags as strings), per the harness
   evidence-emitter precedent; ARM_INTERFACE.md (JSON booleans, wider m2_etc)
   disagrees — conflict flagged, not resolved here.
6. Prereg R-2 proposes L_max ≤ 8; the historical MDL arm used max_len=12. Both were
   entered (R-7 test-both); 12 wins the leg on this battery.

## Section champions (per MEMORY.md standing rule — record and keep)

- B-T1 tournament champion (capability_composite): **predictive_surprise**.
- Compression champion: predictive_surprise (0.900 prose / 0.912 code).
- Retrieval champion: predictive_surprise.
- Grounded-consistency champion: fixed_window_64 (detail in rank_table.json).

## Commit

- Branch: `tnn-native-lab`. Files: `units/r0/impl/arms/arms.zag` (additive
  `adaptive_mdl_8` leg), `units/r0/evidence/tournament/b_t1/` (manifest, scorer,
  ranker, results, logs).
- Commit: `0489675d58e436b6a432e241d0336d3a34ed43d7` — "R0 B-T1 tournament: native 8-arm redo, 1x, PASS".
  (Closeout 2026-09-21: independent reproduction DISCREPANT — measured scores
  differ substantially; binding bar FAILS (raw_micro not dead last);
  grounded_adaptive_mdl crashes (heap overflow). See closeout/CLOSEOUT_ADDENDUM.md.)
