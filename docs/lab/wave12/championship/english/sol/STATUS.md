# SOL English Box — Status (2026-09-21, recovery complete)

## COMPLETE: corpus frozen, all three legs built and run N=5 byte-identical

### Capture recovery (2026-09-21, parent ruling applied)

- Batch 19 captured cleanly on the FIRST attempt (gpt-5.6-sol, temp 0,
  seed 42; raw sha256 prefix `6a6825e8b0b71ea4`); ids 228-239 all parse;
  id 231 reproduces the supplied false value `7` (true `8`).
- Batch 18 resolved WITHOUT a 5th attempt: per the parent ruling, rows were
  parsed mechanically per-ID across the preserved attempts. Attempt 3
  (raw sha256 prefix `d75a76b6d0a1ff69`) yields 11 clean ids and id 222;
  id 226 is valid in attempt 3 despite failing attempts 1, 2, and the
  recovery run (raw sha256 prefix `f0c8a36fa9495b06`).
- Every id 216-227 has at least one strictly-parseable raw row, so the
  union needs NO withholdings: **withheld_ids = []**, taught scope 240/240.
  The `withheld`/`E_format` machinery exists and is live in all three legs
  (MUSE_WITHHELD_N=0, `withheld` battery 0/0 skipped-clean).

### Frozen corpus

- `corpus/corpus.json` sha256
  `41aa8f5be15f778034cfce63250233468d364f52b318a02f63a87ac7459015d7`
  (240 dump rows, 240 teach rows; `SHA256.txt` matches; `withheld_ids.json`
  records the empty set).
- Faithfulness (independent scorer, `ERROR_INVENTORY.md`):
  E_dump=0, E_obs=0, E_prb=0, E_format=0; 12/12 false supplied values
  reproduced word-perfect, 0 flagged/corrected; one retained quirk —
  id 185 distract_value == obs_value (64) while the distractor text says 72.

### Domain/port repairs found during recovery (mechanical, not bar changes)

1. **Category-3 width bug (found by experiment, fixed):** the sol port wrote
   `q2_cat_n`/`muse_t_cat_n` = 48 for all 4 categories, but the English box
   is 48/48/48/96 (count-fact = ids 144..239; the muse-native source this
   ports returns 96 for cat 3). Symptom in the pre-fix smoke run:
   d1=33/40, rev_false=10/12, r2=35/40, e90 never reached — exactly the
   ids 192..239 (including false ids 205, 231) never taught. After the fix:
   d1=40/40, rev_false=12/12, r2=40/40, e90=210 reached, eps=295.
2. legA `q2_teach` gained the withheld skip (byte-identical copy discipline
   kept: `legs/shared/muse_teach.zag` copied to legB/legC).
3. legB/legC expectations changed to 240-MUSE_WITHHELD_N; legC clean-mastery
   denominator excludes withheld ids.

### Runs (all exit 0, N=5 byte-identical, real corpus SHA in every log)

- legA: bind M2 reps 0-11 @scale 1 + rep 0 @scale 10, btrap M2 reps 0-11
  @scale 1 — 25 configs × 5 runs, all byte-identical.
- legB: `sol_b7_direct_bin` × 5 — §B.7: 96/96 flaw hits (8/8 slices pass),
  MUSEB_COMPLETE.
- legC: `sol_teacher_leg_bin` × 5 — 96/96 flaw hits, 160/160 clean adopted,
  mastery 192/192, blocked 0, MUSEC_COMPLETE.
- Static no-RNG scan: PASS on all compiled sources (1 dead-reference note
  in muse-native's uncompiled q2_trial.zag only).

### Remaining in this task

- M2 Track-5 analysis → class-4 composite (pending btrap logs).
- `SOL_ENGLISH_VERDICT.md`, `~/workspace/NIGHT_RUN_2026-09-21.md` append,
  commit of data/evidence/docs to `tnn-native-lab`
  (`docs/lab/wave12/championship/english/sol/`).

## Files

- sol/capture_batch19.py, sol/build_corpus_final.py, sol/build_domain.py,
  sol/build_gen.py, sol/score_faithfulness.py, sol/ERROR_INVENTORY.md,
  sol/corpus/* (frozen corpus + raw attempts + batch19_retries.json),
  sol/legs/{legA,legB,legC,shared}/src/*.zag (real-corpus builds),
  sol/legs/*/run_leg*.sh, sol/legs/*/evidence/logs/* (N=5 logs + SHA256SUMS),
  sol/legs/legA/analysis/analyze_m2.py, sol/evidence/norng_scan.txt.
- Binaries (`build/*_bin`) and `.zagd` are NOT committed.
