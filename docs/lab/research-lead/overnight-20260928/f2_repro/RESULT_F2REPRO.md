# RESULT_F2REPRO: Independent Reproduction of F2 Retry (AUTOSCI2)

Date: 2026-09-30. Prereg: 43873953a (committed alone before any
reproduction work). Source commit: 1eb66765d.

## Verdict: REPRODUCED

All three kill bars pass.

## Method (as preregistered)

1. Extracted the three .zag files verbatim from frozen commit 1eb66765d
   into scratch (source md5s: learner de95a49350f42122da5fb0a8dd445eba,
   world_a2 c04a3db3f0e07e69c4314cc3bcaa6adb, world_b2
   46af7dddc67297c7b0830778d7ea83c2). No modifications.
2. Concatenated autosci2_learner.zag + world_a2.zag (run_a.zag) and
   autosci2_learner.zag + world_b2.zag (run_b.zag), matching the world file
   comments ("Concatenate AFTER autosci2_learner.zag").
3. Compiled with znc (native binary). Executed each world 3 times.
4. Compared stdout md5s against the frozen reported md5s.

## Results

| World | Runs | md5 (reproduced) | md5 (reported) | Match |
|-------|------|------------------|----------------|-------|
| A | 3/3 byte-identical | 156d4ea8fefa74443502d5592ac89e91 | 156d4ea8fefa74443502d5592ac89e91 | YES |
| B | 3/3 byte-identical | 52cd392ca369bbdfcb3f3f9c0ffd5ac7 | 52cd392ca369bbdfcb3f3f9c0ffd5ac7 | YES |

Key verdict lines reproduced exactly (World A): NHYP 6, SURVIVORS [0,2]
exhausted=1, GOAL_REAL 1, RANDOM_BASELINE 0/20, OBS_USED 6. (World B):
NHYP 2, PLAN_B2 M=[SX,CK,W,SX,W,SX] full_len=15, GOAL_REAL_B2 1
obs=[1,0,1,0,1,0], RANDOM_BASELINE_B2 0/20, OBS_USED 7. All match
RESULT_AUTOSCI2.md.

## Kill bar verdicts

- K1 (non-author independence): PASS. The reproduction was performed by an
  agent who did not author the AUTOSCI2 implementation, working only from
  the committed files, used verbatim with no edits. The build required no
  undocumented flags or steps beyond the preregistered concatenation.
- K2 (result match): PASS. Both world md5s match the frozen report across
  3/3 byte-identical runs.
- K3 (purity): PASS. Only znc, bash, and core shell utilities (cat, md5sum,
  grep, cp) were used. No Python at any stage. Zero em-dash bytes in wave
  documentation (byte-checked).

## Notes

- A live .git/index.lock blocked the first prereg commit attempt; the lock
  was waited out (not removed) per standing rule, and the commit then
  succeeded. No reproduction work preceded the prereg commit.
- Build binaries were 115499 bytes (A) and 98137 bytes (B); exit 0, zero
  stderr on all runs.
- Promotion pipeline step 4 (independent reproduction) is now COMPLETE for
  F2 retry. Remaining recommended steps: memorization control (done:
  5d0fd8c9e), combined adversary + ablation, OOD, transfer, governance
  audit.

## Files

- PREREG_F2REPRO.md (43873953a)
- F2REPRO_RAW_A.txt (World A reproduced run, md5 156d4ea8...)
- F2REPRO_RAW_B.txt (World B reproduced run, md5 52cd392c...)
- RESULT_F2REPRO.md (this file)
