# PREREG_R6_ADV: H-ROUTER6 Red Team (frozen)

**Date:** 2026-09-29
**Status:** FROZEN (before any attack code, build, or run)
**Target:** H-ROUTER6 SURVIVES (`ROUTER6_RESULT.md`): R1 contested anchors
are loud findings (ANCHOR-CONTESTED, bits 2/3); R2 honest summary
(all-clear `no-task-family-inconsistency` only when every learn-bearing
content type has a known, uncontested anchor and all checks pass; else
`task-family-check-partial` bit6 or `task-family-anchor-missing` bit5).
**Assumption:** the repair claim is false. Every attack below is a genuine
attempt to break it.
**Method:** `r6_adv.zag` = `router6_learn.zag` lines 1-1785 byte-verbatim
(verified by cmp; everything before `fn main`) + adversary main only.
Pure Zag. No Python at any stage. Builds in /tmp only, never committed.
Determinism: 3/3 runs byte-identical required for evidence to count.

## X-R6-1 (Hybrid: contested-anchor + coherent-relabel)

Coherent re-labeling alone is the disclosed boundary (honest boundary #3):
a fully coherent wrong anchor is internally consistent and undetectable by
any within-curriculum check. Contested anchors alone are now loud
tripwires. The hybrid asks whether COMBINING them re-opens silence: a
contested type whose learn marks go unchecked, PLUS a coherently
re-labeled type whose wrong anchor makes swapped learns look consistent.

Fixture H1 (custom induction mirroring run_induction_swap, but qk=2
queries taught as PQ from the start so no CQ mark ever exists for qk=2):
- learns: s0=1 multi-seg str>str -> CL (SWAP), s0=2 multi-seg iii>ii -> PL
  (SWAP), single-seg and W marks as in run_induction_swap
- queries: "hello"->PQ, "world"->PQ (qk=1 honest), "zzz"->CQ (qk=1
  dissent: contest), "1,0,0"->PQ, "0,0,0"->PQ (qk=2 coherent re-label,
  wrong family, zero dissent)
- corruption probes: "zz>yy;xx>ww" and "3,3,3>3,2;4,4,4>4,3" via
  learned_route3 (honest policy: PROC_LEARN and CAUS_LEARN)

Expected honest behavior: qk=1 contested (bits: ANCHOR-CONTESTED qk=1);
qk=2 anchor PROC (wrong but coherent); s0=2 swapped learns consistent with
the wrong anchor (no fire); s0=1 learns unchecked; summary
`task-family-check-partial`; NO `no-task-family-inconsistency`.

KILL/DOWNGRADE criterion: `no-task-family-inconsistency` appears anywhere
in the H1 diagnostic block, OR tfam carries neither contested nor partial
bits ((tfam & 76)==0), while the corruption probes confirm genuinely
swapped routing (str-pair -> CAUS_LEARN, tripletrans -> PROC_LEARN).
Either outcome is a NEW silence vector combining the two evasions and
DOWNGRADEST the repair claim. If the output is loud (contested + partial,
no all-clear), X-R6-1 FAILS (the hybrid is handled honestly).

## X-R6-2 (Partial: contested type + genuine inconsistency on the known type)

When one anchor is contested and the other type carries a genuine
learn/query inconsistency, the per-mark check fires (fired!=0), which
SKIPS the summary block entirely. The question: does the contested path
hide or dilute the real inconsistency?

Fixture H2: run_induction_swap (full SWAP learns) + honest queries +
"zzz"->CQ (contest qk=1 only).
- qk=1: PQ,PQ,CQ -> contested. qk=2: CQ,CQ -> CAUS (known).
- s0=2 swapped learns (PL, family PROC) vs CAUS anchor -> must fire bit1
  with per-mark TASK-FAMILY-INCONSISTENCY lines.

KILL/DOWNGRADE criterion: the s0=2 TASK-FAMILY-INCONSISTENCY lines are
ABSENT from the H2 diagnostic block, OR `no-task-family-inconsistency`
appears in it. Either hides a genuine inconsistency behind the contested
path and DOWNGRADEST/KILLS the claim. Expected honest behavior (attack
fails): ANCHOR-CONTESTED (qk=1) AND TASK-FAMILY-INCONSISTENCY (s0=2
marks) both present, bit1 set, no all-clear line.

## X-R6-3 (Edge: partial-summary edge cases)

H3a (contested anchor, zero learn marks): teach "hello"->PQ,
"world"->PQ, "zzz"->CQ only. No PL/CL marks anywhere. Expected:
ANCHOR-CONTESTED + `task-family-check-partial`, no all-clear.
KILL criterion: `no-task-family-inconsistency` appears -> the summary
overstates on a degenerate curriculum.

H3b (anchor missing for a type with NO learn marks): honest s0=1 learns
(PL) + "hello"->PQ, "world"->PQ; no qk=2 queries at all; no s0=2 learns.
Expected: `no-task-family-inconsistency` (nothing is unchecked; the
missing type carries no learn marks) and no partial bit. This is an
honesty calibration: the all-clear must still be emittable when vacuous.
KILL criterion: `task-family-check-partial` appears here -> the repair
over-flags and the summary semantics are broken.

H3c (anchor missing for a type WITH learn marks): qk=2 queries
"1,0,0"->CQ, "0,0,0"->CQ (CAUS known); s0=2 learns honest (CL);
s0=1 learns swapped (CL); NO qk=1 queries at all. Expected:
`task-family-check-partial: anchor missing for a content type with learn
marks` (bit6), no all-clear. This exercises the new R2 missing-anchor
branch (the X-R5-2c sibling). KILL criterion: `no-task-family-inconsistency`
appears -> the R2 branch is broken and the summary overstates.

H3d (scope probe: corrupting mark outside the s1>=2 scope): the family
diagnostic only examines learn marks with s1>=2 (inherited scope, probed
in X-R5-2d where the attack mark was defeated by an honest mark at
identical features). Here the attack uses NOVEL single-segment items with
no honest counterpart at the same features, taught as CL, then probes
routing of the same shape against an honest baseline.
- Baseline B: run_induction(gamed=0); probe novel inputs N1..N3, record
  routes.
- Attack A: run_induction(gamed=0) + teach(candidate, TC_CL()); probe the
  same inputs.
- Candidates are chosen in-harness by printing route_features and
  selecting s1==1 items whose features do not collide with any honest
  curriculum item.
KILL/DOWNGRADE criterion: some candidate produces (probe route in A)
!= (probe route in B) — real routing corruption — while the A diagnostic
block shows tfam==0 with `no-task-family-inconsistency` emitted and
mergers_mask==0 and sfanom==0 (full silence). That breaks the "honest
summary" claim and DOWNGRADEST the repair. If no candidate corrupts
(induction defeats them, as in X-R5-2d), the boundary is confirmed and
X-R6-3d FAILS.

## X-R6-4 (Regression and source audit)

- Rebuild `router6_learn.zag` from the committed source
  (`git show HEAD:docs/lab/research-lead/overnight-20260928/router6_learn.zag`),
  run 3x in /tmp, cmp against committed `ROUTER6_RAW_OUTPUT.txt`.
  PASS iff byte-identical and sha256 equals
  `4ce8a69eff2dec1fa09fd072f056670fcea7c630cc2caf98332511524eb0abf4`.
- Grep the rebuilt output: every K-*-PASS line present —
  K-R5-1, K-R5-2a, K-R5-2b, K-R5-2c, K-R4-1..K-R4-5, K-R6-1, K-R6-2 — and
  the line `H-ROUTER6 AUTOMATED BARS PASS`.
- Source audit: diff `router5_learn.zag` vs `router6_learn.zag`; confirm
  the delta is confined to `audit_task_family` (R1/R2), the F-P1/F-P2
  fixture sections, and the K-R6 verdict lines. Confirm the literals
  "zzz" and "9,9,9" appear ONLY in fixture/teach sections, never inside
  `audit_task_family` or any other mechanism function.
- KILL criterion: any byte difference, any bar not PASS, or fixture
  literals inside mechanism code -> KILL (regression) or DOWNGRADE per
  the nature of the deviation.

## Verdict rules

- If any X-R6-1/2/3 kill criterion fires while all frozen K-R6 bars still
  pass, H-ROUTER6 is DOWNGRADED (claim narrows; mechanism stands).
- If any frozen K-R6 bar breaks, H-ROUTER6 is KILLED.
- X-R6-4 failure is KILL (regression) or DOWNGRADE per deviation nature.
- If all four attacks fail, H-ROUTER6 SURVIVES this red team.

## Governance

Pure Zag, no Python at any stage (implementation, fixtures, builds,
greps, hashes, diffs). Only adversary-owned files staged
(`router6_adversary/`). No binaries committed. No em dashes in loop docs.
Prereg committed alone before any attack code; ordering verified with
`git merge-base --is-ancestor`.
