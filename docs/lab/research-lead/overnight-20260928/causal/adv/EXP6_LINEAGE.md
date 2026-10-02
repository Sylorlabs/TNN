# H-EXP6 Commit Lineage Correction

Date: 2026-09-29.

## What happened

My seven H-EXP6 files (staged by me, not yet committed by me)
were swept into commit 13a501fa9 ("PREREG H-ROUTER5 FROZEN:
task-family consistency repair for X-R4-1 swap evasion") by a
concurrent worker's broad-pathspec commit during a
.git/index.lock contention window. The commit message names
only the H-ROUTER5 prereg; the H-EXP6 files are present under
that message.

## Verification

- All seven files verified byte-identical between my working
  copies and the committed blobs (cmp): exp_invent6.zag,
  EXP6_RESULT.md, evidence/exp6_s1_raw.txt,
  evidence/exp6_s2_raw.txt, evidence/exp6_s0_raw.txt,
  evidence/exp6_a1_raw.txt, evidence/exp6_f1_raw.txt.
- Prereg ordering preserved: 1b7a17201 (PREREG H-EXP6 FROZEN,
  committed alone before any implementation) is a strict
  ancestor of 13a501fa9 (verified via
  git merge-base --is-ancestor).
- No H-EXP6 file content was altered by the sweep; only the
  commit message is mislabeled.

## Disposition

The evidence stands as committed. This correction records the
lineage so the mislabeled commit message cannot be mistaken for
the H-EXP6 result commit. This is the same broad-staging
governance pattern previously recorded by other workers; it is
recorded here, not hidden.
