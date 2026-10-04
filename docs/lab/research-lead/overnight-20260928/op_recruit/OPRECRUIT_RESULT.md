# OP_RECRUIT Result: Runtime Operator Recruitment

## Verdict: RECRUITMENT-TESTED (MIXED)

The ALLOCATE_OP mechanism is implemented correctly and the C0-A claim
is validated. The C0-D test yields a weak positive signal on T4 but
not the predicted full solution; T5 shows no benefit. The primary
blocker is beam-search pruning, not the recruitment mechanism.

## Commits

- Prereg: `9d9c78cbd` (frozen before implementation)
- Amendment A1: `fcb666900` (beam width 500->100, transparent,
  pre-implementation; matches GENEXEC2 code)
- Implementation + result: (this commit)

Prereg strictly precedes implementation (verified via
`git merge-base --is-ancestor` before reporting).

## What was built

`op_recruit.zag` (pure Zag): GENEXEC2 VM extended with opcode range
32..63 for recruited ops. ONE generic dispatch case
(`op>=32 && op<64`); no per-op semantic case. `recruit_op` copies a
solved program's bytes into learner state (`rec_buf`) and assigns the
next opcode. Execution is a unary stack function: pop a, run bytes
with in0=a on a fresh stack (recursive `vm_run`, depth guard 8), push
result.

## Results (3/3 byte-identical runs)

| Check | Result |
|-------|--------|
| RECRUIT opcode | 32, nrec=1, RECRUIT_OK 1 |
| SANITY_OP32 ([IN0, OP32] on T1) | 17/17 |
| BASELINE_T4 (P1, no recruit) | 6/13, prog=[IN0 PUSH:2 MOD] |
| BASELINE_T5 (P1, no recruit) | 3/13, prog=[PUSH:2] |
| P1R_T4 (beam + OP32) | 7/13, uses_op32=1, prog=[IN0 PUSH:2 SUB OP32] |
| P1R_T5 (beam + OP32) | 3/13, uses_op32=0, prog=[PUSH:2] |

md5: `6904203264e2008bdf2b0c3fab7a9bad` (run1.txt, run2.txt, run3.txt identical)

## Kill bar verdicts

- K1 (design): PASS. ALLOCATE_OP designed, protocol specified, C0-A
  argument and CALL-difference claim documented in prereg.
- K2 (implementation): PASS. Pure Zag; exactly one generic VM case for
  32..63 (audit: ABS/STEP/DOUBLE/COUPLED/COND appear only in
  descriptive comments, never as dispatch cases); zero Python; zero em
  dash bytes; 3/3 byte-identical; exit 0.
- K3 (C0-D test): PASS (procedure executed; verdict follows evidence).
  Verdict is MIXED, see below.

## C0-A: VALIDATED

SANITY_OP32 17/17 proves the mechanism: OP32's semantics (absolute
value) resides entirely in the learner-recruited bytes. The source
contains no absolute-value case. If a different fragment were
recruited, OP32 would mean something else. The CALL-difference claim
holds: CALL cannot compose as a stack function (it uses global in0);
the recruited op's pop/bind/push wrapper makes it composable, which is
why P1R_T4's program uses OP32 as the final |.|.

## C0-D: MIXED (weak positive, confounded by search)

Prediction (4.4) was "unsolvable to solvable" with the 5-op T4 program
[IN0, OP32, PUSH 2, SUB, OP32]. Not met: P1R_T4 reached 7/13, not
13/13, and P1R_T5 did not use OP32.

Falsification (4.5) required 0/13 with no improvement. Not met: P1R_T4
improved 6/13 -> 7/13 and uses OP32.

Diagnosis (per 4.5(a)): the beam prunes the crucial [IN0, OP32] prefix.
[IN0, OP32] outputs |x|; on T4 it scores only 2/13 (matches when
|x|=1), so it is pruned before the full 5-op solution is reached. The
beam instead found [IN0 PUSH:2 SUB OP32] (|x-2|, 7/13), which applies
OP32 last. The recruited op IS useful and IS used, but the sparse-
reward beam cannot retain the deep composition prefix. This is the
same search bottleneck identified in F1 and the P1 Redesign direction,
not a defect in the recruitment mechanism.

T5: the 7-op solution needs OP32 twice with ADD; the beam never
retained an OP32 prefix (uses_op32=0). Consistent with the search
diagnosis.

## Baseline discrepancy (honest report)

The prereg cited GENEXEC2's T4 baseline as 0/13. My P1 re-run (same
width 100, max_len 12, same episodes) scores 6/13 with
[IN0 PUSH:2 MOD]. Manual verification: x mod 2 (nonneg) equals
||x|-2| at x in {-3,-2,-1,1,2,3}, i.e., 6/13. The GENEXEC2 report's
0/13 appears to be an error (or measured differently); the program
[IN0 PUSH:2 MOD] is listed in that report and scores 6/13 under the
frozen episode construction. The comparison in this report uses my
re-run baseline (6/13), which is the fair same-implementation control.

## Classification

C0-A mechanism: sound. This is the first GENEXEC2-lineage mechanism
where a learner-recruited opcode has correct composable semantics
defined entirely by learner bytes. L2 structural (the recruitment is
learner-invoked but the wrapper and protocol are researcher-designed);
not L3 (no open-ended invention of the operator concept itself).

## Recommendation

The P1 Redesign worker's success is a precondition for a clean C0-D
retest. With a search that retains [IN0, OP32], the 5-op T4 solution
should be found, which would convert this MIXED result into C0-D
SUPPORTED. The ALLOCATE_OP substrate is ready for that test.

## Files

- PREREG_OPRECRUIT.md (prereg + Amendment A1)
- op_recruit.zag (implementation)
- OPRECRUIT_RESULT.md (this file)
- run1.txt, run2.txt, run3.txt (raw outputs)
