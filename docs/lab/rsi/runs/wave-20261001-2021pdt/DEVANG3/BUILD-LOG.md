# DEVANG3 Build Log

## File Creation Order
1. `devang3.zag`: Copied from DEVANG2 baseline (1065 lines, unedited).
2. `NAMECHECK.md`: Step 0b appended (safebin, toolchain verification).
3. `devang3.zag`: Implementation edits (see below).
4. `devang3`: Built binary via pinned znc.
5. `dev_segb.txt`: Dev segmentation utterances (12, builder-designed).
6. `dev_segb_key.txt`: Dev segmentation key.
7. `dev_sealc.txt`: Dev Family C episodes (2 train, 2 test).
8. `fama_run*.log`, `det*.log`: Test logs.
9. `IMPLEMENTATION.md`: Implementation report.
10. `BUILD-LOG.md`: This file.

## Implementation Edit History
1. Header comment: Updated to describe DEVANG3 design, W layout, controls.
2. W layout comment: Updated (lexicon counts are the statistics).
3. Added `seg_dp_raw`: C0 control segmenter (DEVANG2 bigram DP).
4. Rewrote `seg_dp`: Lexicon-frequency DP with Pitman-Yor inspired scoring.
   - Cold start: 3-char chunks while nlex<10.
   - Scoring: new=-50+ilog(L+1)*5; seen=ilog(c)*10-30+ilog(L+1)*5 (-40 if L==1).
5. Simplified `learn_update`: Removed seg_int/seg_bnd updates for learner
   (rawmode=0). Kept rawmode=1 branch for C0 (raw bytes to seg_int).
6. Added `k1_count` helper: Counts 10 K1 words in lexicon.
7. Added sealed interface:
   - `parse_ints2`, `sealc_parse_ep`: File parsing helpers.
   - `mode_segb`: Train on Family A, segment file utterances.
   - `sealc_train_one`, `sealc_test_one`: Family C episode handlers.
   - `mode_sealc`: Family C evaluation (continuing/fresh, 5 variants).
   - `main` argv dispatch: fama (default), segb, segb-abl, sealc, sealc-fresh.
8. Updated `main` fama mode:
   - W allocation 7392 -> 10104 (2 sites).
   - Added C0 training/test section (uses seg_dp_raw).
   - Added C2 K1 snapshot (t==59).
   - Added K_C0 verdict computation and reporting.
   - Added K_ABL-A verdict (degradation check).
   - Changed BUILD-PASS/FAIL to DEV-PASS/FAIL (Family A dev bars).
9. Iterative tuning (documented):
   - Initial: seg_int/seg_bnd with boundary reward (10x scaling bug).
   - Fix 1: Corrected reward scaling (removed *10). K1 1/10 -> 2/10.
   - Redesign: Switched to lexicon-frequency DP (mechanism freedom).
   - Fix 2: 3-char chunk cold start (was single-char). K1 0/10 -> 10/10.
   - All tuning within prereg mechanism freedom; bars unchanged.

## Toolchain Notes
- Pinned znc: `/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
- `_zag_strcmp` returns 1 when strings are EQUAL (inverted vs C).
- `_zag_read_file` returns `[]u8` with `.len<0` on failure.
- Identifier `ullen` is reserved/builtin; renamed to `fulen` in `sealc_test_one`.
- Safebin active; `which python3` returns nothing (verified).

## Test Results Summary
- Fama mode: DEV-PASS (K1 10/10, K8 pass, K_C0 pass, 7/7 sub-bars).
- Determinism: 3/3 byte-identical (sha256 logs match).
- Segb dev: 12/12 correct (learner), 7/12 (ablation).
- Sealc dev: Interface validated (1/2 on tiny dev file).
