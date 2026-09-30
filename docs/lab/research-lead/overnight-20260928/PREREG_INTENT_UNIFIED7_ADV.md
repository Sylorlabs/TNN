# PREREG: H-INTENT-UNIFIED7 Independent Red Team (FROZEN)

## Adversary

H-INTENT-UNIFIED7 red team. Date: 2026-09-29. Branch `tnn-native-lab`.

## Target claim under test

H-INTENT-UNIFIED7 SURVIVES (8/8). Result `IU7_RESULT.md`. Builder
prereg `7bc85499d`. R9: all-pairs verbatim-vs-truncated guard in
`intent_winner`, after the R8 block, before the gap==0 tie check.
For each unordered pair (a,b), a<b, with em==1 on exactly one side
and the em==0 side truncated (true npairs > 16): kind-dispatched
answers over qlen bytes; any disagreement emits
`INTENT TRUNCATED-CONFLICT-POSSIBLE: verbatim candidate meets
truncated record with different answer beyond top two; WITHHOLD
AMBIGUOUS` and returns kind=-2.

Stated scope of the surviving claim (from IU7_RESULT.md, "What the
verdict means"): verbatim-vs-truncated conflict detection now covers
genuine contradictions among ALL candidates regardless of rank, for
pairs with em=1 on exactly one side and a truncated em=0 record on
the other.

Disclosed boundaries (not covered by the claim):
- B1: both-verbatim (em=1 on both sides) disagreement beyond the top
  two. The IU3 verbatim guard is top-two-only.
- B2: em=1 vs em=0 non-truncated pair (same as R4/R5).
- B3: precision cost of the POSSIBLE diagnostic (not a bug).

Score model (frozen, from source): qscore = em*40000 + cf*20000 +
lm*10000. Proc candidates: cf=0. Bridge candidates: cf in {0,1}.

## Attacks (frozen)

### X-IU7-1: both-verbatim disagreement beyond the top two

Purpose: verify disclosed boundary B1 is real and genuinely
exploitable, not merely asserted.

Fixture (fresh W, learn order as listed, query `xab`, qlen=3):
- V1 = proc `xab>xxx;xbc>xxx;xde>xxx`
  (proven shape from K-IU7-1: em=1, lm=1, score 50000, answer `xxx`)
- V2 = proc `xbcd>xxx;xdef>xxx;xfgh>xxx;xijk>xxx;xlmn>xxx;xab>xxx`
  (proven shape from X-IU6-2/IU6-ADV: em=1, lm=0 mixed, score 40000,
  answer `xxx`)
- V3 = proc `xbcd>yyy;xdef>yyy;xfgh>yyy;xijk>yyy;xlmn>yyy;xab>yyy`
  (same shape as V2 with constant `yyy` output; expected: proc,
  em=1 on `xab` (6th recorded pair, within cap), lm=0 mixed, score
  40000, recorded answer `yyy`)

Expected arrangement: top=V1 (50000), second=V2 (40000; learned
before V3, strict-greater selection keeps it second on the 40000
tie), V3 (40000) outside the top two. The IU3 verbatim guard
compares top and second: both em=1, both answer `xxx`, agreement,
falls through. R8 skips every pair (em=1 involved). R9 skips every
pair (no em=0 candidate). gap=10000, no tie. Expected outcome:
kind=0, answer `xxx`, no CONFLICT diagnostic. The genuine recorded
contradiction (V3 taught `xab>yyy`, V1 taught `xab>xxx`) is silently
resolved.

SUCCESS (boundary CONFIRMED) iff ALL hold:
1. V1, V2, V3 all learned as procs (t_learn rc in [0,1000)).
2. Candidate record check: V1 em=1 answer `xxx`; V2 em=1 answer
   `xxx`; V3 em=1 answer `yyy` (answers via direct proc_apply on
   `xab`; em via intent_exact_match on the candidate record).
3. t_decide on `xab` returns kind=0 (decisive proc) with answer
   `xxx`.
4. No line containing `CONFLICT` appears in the X-IU7-1 section.

Consequence of SUCCESS: boundary B1 CONFIRMED as stated. The claim
never covered both-verbatim pairs, so per loop precedent (X-IU6-2 on
H-INTENT-UNIFIED6) the verdict is UNCHANGED (SURVIVES).

SETUP-FAIL (no conclusion): condition 1 or 2 fails (V3 does not
learn as a verbatim proc). The fixture is invalid; report and do not
count.

REFUTED (record, no verdict change): kind=-2 on this fixture. The
mechanism over-performs its disclosed boundary; record as
over-performance.

### X-IU7-2: em=1 vs em=0 non-truncated pair beyond the top two

Purpose: verify disclosed boundary B2 is real.

Fixture (fresh W, learn order as listed, query `xab`):
- V1 = proc `xab>xxx;xbc>xxx;xde>xxx` (50000, em=1, `xxx`)
- V2 = proc `xbcd>xxx;xdef>xxx;xfgh>xxx;xijk>xxx;xlmn>xxx;xab>xxx`
  (40000, em=1, `xxx`)
- T4 = proc `abc>cba;def>fed;ghi>ihg` (3 reverse pairs; expected:
  proc via discovery, em=0 on `xab` (not taught), npairs=3, not
  truncated, reverse program applied to `xab` gives `bax`, score
  10000 = em=0 + lm=1)

Expected arrangement: top=V1 (50000), second=V2 (40000). Verbatim
guard: agreement, falls through. Top-two truncated guard: em=1 on
both sides, no branch fires. R8: only T4 has em=0, no pair. R9:
pairs (V1,T4) and (V2,T4) have em=1 on one side, but T4 is not
truncated (3 <= 16), so both are skipped. gap=10000. Expected
outcome: kind=0, answer `xxx`, no CONFLICT diagnostic. T4's
generalized `bax` is silently resolved.

SUCCESS (boundary CONFIRMED) iff ALL hold:
1. V1, V2 procs em=1 answers `xxx`; T4 proc em=0, npairs<=16,
   applied answer differs from `xxx` (expected `bax`).
2. t_decide on `xab` returns kind>=0 with answer `xxx`.
3. No line containing `CONFLICT` in the X-IU7-2 section.

Consequence of SUCCESS: boundary B2 CONFIRMED. Verdict UNCHANGED.
Caveat (disclosed with the result): T4's contradiction is a
generalization, not recorded evidence; the top-two guard would have
caught this pair had T4 ranked in the top two. The boundary is about
rank-hiding of non-truncated em=0 pairs.

SETUP-FAIL / REFUTED: as in X-IU7-1.

### X-IU7-3: rank-4 verbatim-vs-truncated dissenter

Purpose: test the headline R9 claim ("covers genuine contradictions
among ALL candidates regardless of rank") at rank 4. R9 is
all-pairs, so this SHOULD be caught. A miss falsifies the claim.

Fixture (fresh W, learn order as listed, query `xab`):
- V1 = proc `xab>xxx;xbc>xxx;xde>xxx` (50000, em=1, `xxx`)
- V2 = proc `xbcd>xxx;xdef>xxx;xfgh>xxx;xijk>xxx;xlmn>xxx;xab>xxx`
  (40000, em=1, `xxx`)
- V3 = proc `xab>xxx;xbcd>xxx;xdef>xxx;xfgh>xxx` (4 pairs constant
  `xxx`, mixed lengths; expected: proc, em=1, lm=0, score 40000,
  answer `xxx`)
- T4 = proc `abc>cba;def>fed;ghi>ihg;jkl>lkj;mno>onm;pqr>rqp;stu>uts;vwx>xwv;yza>azy;bcd>dcb;efg>gfe;hij>jih;klm>mlk;nop>pon;qrs>srq;tuv>vut;xab>bax`
  (exact K-IU7-1 T3 string, proven: em=0 on `xab`, true npairs=17
  truncated, reverse program, answer `bax`, score 10000)

Expected arrangement: top=V1 (50000), second=V2 (40000). Guards 1-3
fall through (verbatim agreement; em=1/1 top two; R8 has only one
em=0 candidate). R9 must fire on pair (V1,T4): kind=-2 with the NEW
R9 diagnostic `verbatim candidate meets truncated record with
different answer beyond top two`.

MECHANISM-HOLDS iff ALL hold:
1. V1, V2, V3 procs em=1 answers `xxx`; T4 proc em=0, npairs=17,
   answer `bax`.
2. t_decide on `xab` returns kind=-2.
3. The R9 diagnostic text appears exactly once in the X-IU7-3
   section.

DOWNGRADE TRIGGER iff condition 1 holds and (2 or 3) fails: the
headline "ALL candidates regardless of rank" claim is falsified for
rank 4. Verdict becomes DOWNGRADED with the narrowed claim
("verbatim-vs-truncated coverage holds for ranks 1-3 only" or as
the evidence dictates). Not a KILL: the mechanism still catches the
rank-3 case.

SETUP-FAIL: condition 1 fails. No conclusion.

### X-IU7-4: regression (no silent behavior change)

Purpose: independently verify the 8/8 builder claim and the suite
hashes from committed sources.

1. Rebuild `unified_learn.zag` from `git show HEAD:...` (committed
   blob), compile once to /tmp, run main 3 times. Require: 20/20
   each run, stdout md5 ==
   `904de9f83a2873c7a8862b71804a9065` (frozen IU4 hash), 3/3
   byte-identical.
2. Rebuild `intent_learn.zag` from `git show HEAD:...`, run main 3
   times. Require: 10/10, md5 ==
   `98315faec8faea24e75533892c0b240d`, 3/3 byte-identical.
3. Rebuild `iu7_verify.zag` from `git show HEAD:...`, run 3 times,
   cmp each against committed `IU7_VERIFY_RAW.txt`. Require 3/3
   byte-identical.

KILL TRIGGER: any md5 differs, any suite count differs, or any
iu7_verify rebuild output differs from the committed raw. A silent
behavior change invalidates the 8/8 claim.

## Frozen methodology

1. This prereg is committed ALONE before any adversary harness
   build, compile, or run. Commit order verified by
   `git merge-base --is-ancestor`.
2. Adversary harness `iu7_adv.zag` = mechanism region of the
   COMMITTED `unified_learn.zag` (lines 1-1529, everything before
   `fn main`), extracted via `git show HEAD:...`, cmp-verified
   byte-identical against the extraction; helpers t_learn, t_decide,
   iu4_init carried from `iu7_verify.zag`; new adv_show helper
   (prints kind/slot/em/npairs/applied answer for a learned
   candidate); new X-IU7-1..3 attack main. Built in /tmp only;
   binary never committed. Harness source committed as
   `iu7_adv.zag` for provenance.
3. Evidence method: compile once to /tmp with pinned znc
   2026.07.0-dev (edition 2026), execute the binary directly 3
   times for clean raws (avoids `--run` compile-time analyzer
   warnings on stderr, same method as IU6/IU7).
4. Raw evidence: `IU7_ADV_RAW.txt` (md5 recorded, 3/3 cmp).
5. Pure Zag throughout: prereg, harness, builds, runs, greps, md5,
   cmp. No Python at any stage.
6. Only adversary-owned paths staged:
   `PREREG_INTENT_UNIFIED7_ADV.md`, `iu7_adv.zag`,
   `IU7_ADV_RAW.txt`, `IU7_ADV_RESULT.md`. Concurrent workers'
   files untouched (pathspec-restricted staging).
7. No em dashes in loop documentation (byte-verified: 0 in raw).
8. No test-answer literals in mechanism regions; all fixture
   strings live in the harness main().

## Falsification summary

- X-IU7-1 SUCCESS -> B1 CONFIRMED, verdict UNCHANGED.
- X-IU7-2 SUCCESS -> B2 CONFIRMED, verdict UNCHANGED.
- X-IU7-3 DOWNGRADE TRIGGER -> H-INTENT-UNIFIED7 DOWNGRADED.
- X-IU7-4 KILL TRIGGER -> H-INTENT-UNIFIED7 KILLED.
- Any SETUP-FAIL -> that attack yields no conclusion; report the
  setup evidence verbatim.
