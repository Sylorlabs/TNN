# PREREG: Red Team Attacks on H-GENBIAS (H-GENBIAS-ADV)

**Date:** 2026-09-29
**Status:** FROZEN (committed before any attack execution)
**Role:** Independent adversary. Assume H-GENBIAS is false.
**Target claim:** H-GENBIAS SURVIVES (4/4), commit 0763c13d8: "N-first
two-pass search order fixes the uniform-length overfitting" with "no
regression" on other tasks. The result file itself admits the honest
boundary: "A pathological N-using fitter that does not generalize could
still be selected first; none was observed in testing."

## Background analyzed (not executed)

- Program space: 1055 syntactically enumerated affine programs
  f(k) = a*k + b*n + c over terminals {K, N, C0, C1, C2}, ops {ADD, SUB}.
- `prog_uses_n` is SYNTACTIC: true if any node has type 1 (N), regardless
  of whether N cancels semantically (e.g. n-n=0 counts as N-using).
- Pass 1 returns the first fitter in enumeration order among
  syntactically-N-using programs. It cannot be wrong on training
  (only fitters are considered), so the only failure mode is
  generalization: selecting an N-using fitter that does not generalize.
- With >= 2 distinct training lengths, the affine constraint forces any
  fitter's b to match the truth's b, so no semantically-N-using
  coincidental fitter can beat a non-N truth. The danger zone is
  UNIFORM-length training, where b is underdetermined: a*k + n0*b + c
  is fixed by training but b can be nonzero with c adjusted.

## Attacks (frozen)

### G-A1: Exhaustive fitter audit (overfit swap)

For each task in {reverse, broadcast-last, broadcast-first,
broadcast-middle-const2, broadcast-const1, identity} x training regime
{uniform n=4, mixed lengths}, run the NEW (N-first) discovery, record the
pass-1 winner's bytes, and test generalization on held-out lengths
(L=2..7, restricted to L > c for constant-c tasks where the truth is
only defined for L > c).

- KILL criterion: on ANY task x regime, the N-first winner FAILS to
  generalize (misses >= 1 held-out length) while SOME fitter in the
  1055-program space generalizes. The bias then actively prefers a
  worse program: it swaps one overfit family for another.
- DOWNGRADE criterion: the N-first winner generalizes everywhere but the
  audit shows the safety rests on enumeration-order luck rather than a
  principled generality guarantee (documented with the runner-up
  analysis).
- PASS: N-first winner generalizes on all 10 task x regime combos.

Predicted vulnerable cases (to be verified empirically, not trusted):
uniform-length constant-2 ("abcd>cccc") where n-2 = SUB(N,C2) is an
N-using fitter that fails for L != 4, and uniform-length constant-1
("abcd>bbbb") where n-3 is an N-using fitter. The old single-pass code
finds constant 2 / constant 1 (generalizing); N-first may prefer the
N-using overfits.

### G-A2: Transfer head-to-head (help / hurt / neutral)

For the same matrix, run the OLD (single-pass) discovery and compare
generalization counts old-vs-new per cell.

- KILL/DOWNGRADE: any cell where old generalizes fully and new does
  not (strict regression introduced by the bias). This is scored under
  G-A1's kill criterion; G-A2 reports the full help/hurt/neutral table.
- PASS: new generalizes everywhere old does (no strict regressions),
  with strict improvement on uniform reverse.

### G-A3: Pathological N construction

Adversarially chosen training where the TRUE general program does NOT
use N but a coincidental N-using program fits: uniform n=4 constant
broadcasts ("abcd>cccc;efgh>gggg" truth constant 2; "abcd>bbbb;efgh>ffff"
truth constant 1). These are members of the same constant-broadcast
family as the K-G2 broadcast-last/broadcast-first tasks.

- KILL criterion: N-first selects the N-using coincidental fitter
  (n-2 / n-3) and it fails held-out lengths, while the old code selects
  the generalizing constant. This is the concrete "overfit swap."
- PASS: N-first selects a generalizing program.

### G-A4: Source audit

Grep the discovery source (pdiscover_direct, try_discover_pass,
prog_uses_n, enumeration) for test literals ("abcd", "hello", "dcba",
etc.) and test-specific branches.

- KILL criterion: any test literal or test-conditional branch in the
  discovery path (would indicate the "fix" is hardcoded to the tests).
- PASS: test literals appear only in the harness main; the bias is a
  pure search-order change.

## Verdict rules

- The frozen H-GENBIAS SURVIVES (4/4) verdict on bars K-G1..K-G4 is NOT
  reopened: those bars were frozen before execution and all passed.
  Per governance, verdicts name their frozen bars; new attacks cannot
  retroactively unpass them.
- What this red team CAN do: KILL or DOWNGRADE the BROADER claim that
  N-first is a safe generality bias.
  - KILL (as a general bias): G-A1/G-A2/G-A3 kill criterion met. The
    bias is then reclassified: not a generality bias, but a
    task-specific search-order patch with a demonstrated regression
    mode. Recommendation: do not port to further discovery copies
    until repaired; the honest repair is varied-length evidence or a
    post-discovery validation step, not syntactic N-preference.
  - DOWNGRADE: attacks find only cosmetic differences or
    enumeration-luck safety. The claim is bounded: "safe on tested
    tasks; not a principled generality guarantee."
  - SURVIVES: all four attacks pass. The bias stands as a safe
    generality heuristic for the tested space.

## Method

- Pure Zag. No Python. No exceptions.
- New harness `genbias_redteam.zag`: copies the enumeration,
  prog_uses_n, pfits/peval, proc store, stage_pair, check_apply from
  genbias_test.zag (commit 0763c13d8); adds the audit matrix.
- 3 consecutive runs, md5-verified byte-identical (determinism check).
- Binaries to /tmp only. Commit: prereg (this file), harness source,
  raw outputs (3 runs), adversary report.

## Commit order

This prereg is committed before any attack implementation or execution.
