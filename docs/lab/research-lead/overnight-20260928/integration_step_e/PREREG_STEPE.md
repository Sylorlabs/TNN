# PREREG: Integration Step E - Port FDCR Concept Operators into the Concept Layer

**Date:** 2026-09-30
**Worker:** Integration Step E Worker
**Status:** FROZEN. Committed before any implementation.

## Mission

Close Gap G3 from the Integration Scout (INVENTORY.md, commit e6f140b64):
"FDCR concept machinery was never integrated into any continuing learner."

The scout's target architecture specifies:
"Layer 1, segmentation and concepts: DEVINT1 S1-S4 segmentation plus FDCR
operators (FORM/MERGE/SPLIT) ported in, replacing DEVINT1's smaller inventory."

## Background findings (from investigation)

1. FDCR concept operators live in `unified_fdcr8.zag` as 21 `con_` functions:
   FORM (`con_form`), MERGE (`con_merge_into`, `con_merge_check`),
   member lookup (`con_find_member`, `con_find_member_str`),
   string interning (`con_intern`, `con_str_at`),
   accessors, `con_init`, `con_count`, `con_vote_concept`.
   That file SURVIVES 51/51 on its own kill bars (commit 11918217a).

2. In `unified_fdcr8.zag`, the concept operators are exercised ONLY on
   scratch workspaces (W5-W12, fresh 65536-byte buffers per test). The
   continuing workspace W runs the procedure/causal curriculum; its
   `con_init(W)` call initializes concept storage that the curriculum
   never feeds. The scout's G3 is ACCURATE: the operators are not wired
   into any continuing learning loop.

3. The Step D merged curriculum (`integration_step_d/merged_curriculum.zag`,
   commit 83ead74cb) is the integration line. Its DEVINT1 section builds
   concepts via `conc_touch` (24 slots x 32B, pattern-count only, no
   FORM/MERGE operators). This is the "smaller inventory" the scout
   wants replaced.

## What will be built

A new binary `fdcr_concept_layer.zag` in `integration_step_e/`:

1. Based on `integration_step_d/merged_curriculum.zag` (copied verbatim,
   then modified only in the DEVINT1 section; DEVINT2 section untouched).
2. FDCR core operators ported from `unified_fdcr8.zag`:
   `con_slot`, accessors, `con_init`, `con_intern`, `con_str_at`,
   `con_form`, `con_merge_into`, `con_merge_check`,
   `con_find_member`, `con_find_member_str`, `con_count`.
3. Workspace adaptation: DEVINT1 uses a 16384-byte W. FDCR concept store
   placed at verified-free region:
   - FDCR_CONCEPT_BASE = 14336 (8 slots x 76B = 608B, ends 14944)
   - FDCR_STR_BASE = 14944 (string intern area, 1024B, ends 15968)
   - Free: 15968..16384
   The DP scratch area ends by 14016 in practice; 14336 is clear.
4. Wiring: in `process_nofeed`, each segmented morpheme is fed to FDCR
   `con_form` on the persistent W, with features = [morpheme bytes,
   length class, position class] as interned strings. The existing
   `conc_touch` inventory is KEPT (not removed) so stage outputs remain
   comparable; FDCR runs alongside as the new concept layer.
5. A test section `fdcr_selftest(W)` in main verifies FORM/MERGE on a
   scratch workspace.

## Disclosed scoping decisions

1. NOADD vote/drop machinery (`noadd_record`, `noadd_drop_clear`,
   `noadd_*`, ~15 functions) is NOT ported. It serves the
   H-FDCR-UNIFIED procedure-voting layer, not concept formation.
   In the ported `con_form`/`con_merge_into`, those two call sites
   become no-ops. The FORM/MERGE operators function correctly as
   concept operators without them.
2. SPLIT/GRADE/CONTEXTUALIZE: the scout names them, but the committed
   source contains only FORM and MERGE operators (verified by
   inspection of `unified_fdcr8.zag`: no split/grade/context functions
   exist). Only what exists in source is ported. No new operators
   are invented.
3. `conc_touch` is kept alongside FDCR (not replaced) in this step.
   Full replacement is a follow-up; this step proves the operators
   run in the continuing loop.

## Frozen kill bars

- K-E1: `fdcr_concept_layer.zag` compiles with znc, zero errors.
- K-E2: DEVINT1 stages S1-S11 complete. Stage outputs match the Step D
  baseline except the S3-CONCEPTS section, which additionally reports
  the FDCR concept count.
- K-E3: DEVINT2 stages S1-S7 complete, output identical to Step D
  baseline (section untouched).
- K-E4 (FORM): in `fdcr_selftest`, feeding the same entity with the
  same features twice returns the same concept id (no duplicate);
  feeding the same entity with different features creates a new
  concept.
- K-E5 (MERGE): in `fdcr_selftest`, two concepts with identical
  feature sets are merged by `con_merge_check` into one.
- K-E6: 3/3 runs byte-identical (md5 recorded).
- K-E7: Pure Zag. Zero Python at any stage. Zero em-dash bytes in
  loop documentation (verified via od/grep).

## Method

Prereg committed alone first. Implementation only after. Owned path
only: `docs/lab/research-lead/overnight-20260928/integration_step_e/`.
Commits local, not pushed.
