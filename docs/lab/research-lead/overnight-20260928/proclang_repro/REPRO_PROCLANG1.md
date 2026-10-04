# H-PROCLANG1 Independent Reproduction Report

Verdict: REPRODUCED

Reproduction worker: independent subagent (step 4 of 11-step frontier promotion pipeline).
Date: 2026-09-29.
Builder result commit: 647b4096c7c3c0fa5a553354643d92251e29361a
Prereg commit: bd883d969c6786d90ead5a84b61a093991903382

## Method

1. Extracted proclang1.zag from the committed blob at 647b4096c via git show.
   The working tree was not used.
2. Compiled with frozen toolchain znc 2026.07.0-dev (edition 2026) at
   /home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc.
   Build succeeded; native binary, 50388 bytes main, 0 external tools.
3. Ran the binary 3 times. All three runs exited 0 with empty stderr.
4. md5 of all three runs: e6b87d123bdb3497e94afb9be0cfc3ae.
   md5 of the committed PROCLANG1_RAW.txt at 647b4096c: e6b87d123bdb3497e94afb9be0cfc3ae.
   3/3 byte-identical by cmp.
5. git merge-base --is-ancestor bd883d969 647b4096c: confirmed strict ancestor.
6. Prereg file PREREG_PROCLANG1.md exists at bd883d969.
   proclang1.zag does NOT exist at bd883d969. Implementation followed prereg.
7. Scanned commit range bd883d969..647b4096c for .py files: none found.

No Python was used anywhere in this verification (bash, git, znc, md5sum, cmp only).

## Kill-bar verification (frozen bars from committed PREREG_PROCLANG1.md)

K-P1-1 (impossibility, empirical): PASS.
  AFFINE_LEMMA checked=2955 ok=2955. Phase A on T1: best=ID mismatches=20 (>= 1).
K-P1-2 (invention + hidden success): PASS.
  INVENT op=COND_T1 t=0 left=MUL -1 right=ID. T1 HIDDEN n=2001 correct=2001.
K-P1-3 (white-box trace): PASS.
  TRACE trigger_residual=20 train_before=20 train_after=0 lib_size=1,
  SPLIT_SCAN n_thresh=43 best_t=0, op name COND_T1, encodings present.
K-P1-4 (ablation): PASS.
  ABLATION prog=ID train_mismatches=20 n=2001 correct=1001 (< 2001/2001).
K-P1-5 (reuse): PASS.
  T2: REVISE old=COND_T4 new=COND_T2 t=0. T2 HIDDEN n=2001 correct=2001.
K-P1-6 (transfer): PASS.
  T3: REVISE t=1 (re-learned in new coordinates). T3 HIDDEN n=2001 correct=2001.
K-P1-7 (revision): PASS.
  T4: CUR_OP_TRAIN_MISMATCHES op=COND_T1 n=41 (contradiction shown).
  REVISE old=COND_T1 new=COND_T4 t=3. T4 HIDDEN n=2001 correct=2001.
K-P1-8 (determinism): PASS.
  3/3 byte-identical, exit 0, md5 e6b87d123bdb3497e94afb9be0cfc3ae.
K-P1-9 (memorization control): PASS.
  BASELINE table n=2001 correct=41 (< 2001/2001).

9/9 PASS. The builder's BUILD-PASS verdict is confirmed by independent
reproduction from committed source.

## Observations (non-blocking)

- K-P1-9 prereg text says "expected 1/2001" for the table baseline, but the
  run shows 41/2001. The 41 come from the 41 training x values in [-20, 20]
  that also fall inside the hidden range [-1000, 1000]; exact-match table
  gets those right and emits 0 elsewhere. The frozen bar is "< 2001/2001",
  which is satisfied, so this is a prereg-text inaccuracy, not a bar failure.
- T2 and T3 were achieved via REVISE events (re-invention within the COND
  family) rather than literal INVENT events; the bar allows "INVENT or REVISE".
- The central caveat stands: the threshold-scan + reification machinery is
  researcher-supplied; what is learner-created is the trigger response and
  the COND operator content. The independent adversary should attack this
  machinery-vs-content boundary at step 6/10.

## Disposition

H-PROCLANG1 proceeds to step 5 (simple-baseline comparison) of the promotion
pipeline. This report is a reproduction confirmation only; it is not a
SURVIVES claim.
