# PREREG_ROUTER7: H-ROUTER7 Total-Table + Single-Segment Family Audit

**Date:** 2026-09-29
**Status:** FROZEN (before any implementation)
**Parent:** H-ROUTER6 SURVIVES; red team SURVIVES all 4 attacks with two
suggested follow-ups.

## Background

The H-ROUTER6 red team (R6-ADV, SURVIVES) left two suggested follow-ups,
neither a finding:

1. **Latent table-shape observation (X-R6-3d):** an out-of-scope mark
   (`ab>1,0`->CL, features (3,1,0)) drives the induced `[any]` entry to
   CONFLICTED. `build_table_rest` compiles only ST_ACTIVE entries, so the
   compiled table loses its `[any]->WITHHOLD` fallback rule. `route3`
   then returns -1 (NO-MATCH) for unmatched inputs instead of 10
   (WITHHOLD). Behaviorally identical today (project semantics normalize
   -1 to WITHHOLD in `check_route3`/`tc_name`), but the table is no
   longer total: a silent -1 replaces a declared rule. If NO-MATCH and
   WITHHOLD ever diverge semantically, this becomes observable.

2. **Carried scope boundary:** the task-family and single-family
   diagnostics scope learn-mark checks to `s1>=2` (multi-seg range).
   Single-segment learn marks (s1==1, e.g. `ab>cd`->CL at features
   (1,1,0)) are unchecked. The s1>=2 restriction has no principled
   basis for learn marks: the WITHHOLD boundary marks that motivated
   caution are excluded by the `t!=TC_W()` / `t in {PL,CL}` predicates
   already.

## Repair (H-ROUTER7)

**R1: Total routing table (explicit fallback preservation).**

In `build_table_rest`, after compiling ACTIVE equality entries, scan the
compiled rules for an all-ANY rule (k0==CK_ANY && k1==CK_ANY &&
k2==CK_ANY). If none exists, append an explicit terminal
`[any]->WITHHOLD` fallback rule via `rt_add` with a loud emit:

`TABLE-RULE [any]->WITHHOLD (explicit fallback: no induced [any] rule; total-table invariant)`

This guarantees the compiled routing table is total by design: every
feature triple routes to a declared task code; `route3` never silently
returns -1. This is a default-deny safety invariant, not an induced
rule: when the learned decline is lost to a CONFLICTED entry, the
decline semantics are preserved explicitly rather than degrading to an
implicit -1.

What is NOT changed: rule ordering (fallback is terminal, after all
ACTIVE entries in descending specificity); first-match semantics;
`compile_thresholds`; induction; all audits. The explicit fallback is
appended ONLY when no all-ANY rule was compiled; when the induced
`[any]` entry is ACTIVE, output is unchanged.

**R2: Family audit scope extended to s1>=1 learn marks.**

Change `s1>=2` to `s1>=1` in the learn-mark predicates of
`audit_single_family` and `audit_task_family` (both the inconsistency
checks and the has1/has2 summary logic). Update the `audit_single_family`
emit label from `learn-marks s1>=2:` to `learn-marks s1>=1:` for honesty.
A single-segment learn mark of a content type is now family-checked like
a multi-segment one. The s0 in {1,2} content-type scoping is unchanged;
s0=3 (mixed) marks remain out of scope (no content-type mapping exists).

## Frozen kill bars

**K-R7-1 (fallback preserved):** F-FB fixture: honest curriculum
(`run_induction` gamed=0) + `teach(W,"ab>1,0",TC_CL(),19,...)` (exact
X-R6-3d CAND1 attack; pilot-verified: features (3,1,0), drives the [any]
entry to CONFLICTED, R6 table has zero all-ANY rules, route3(3,1,0)
returns -1). PASS iff: (a) the [any] entry is CONFLICTED (the test
exercises the intended path; verified by grep for "CONFLICTED action 7
[any]"); (b) the compiled table contains a terminal `[any]->WITHHOLD`
rule with the explicit-fallback emit; (c) `route3(RT,nrt,3,1,0)` returns
10 (WITHHOLD), not -1.

**K-R7-2 (single-segment family check):** F-S1 fixture: honest
curriculum + `teach(W,"ab>cd",TC_CL(),19,...)` (pilot-verified: features
(1,1,0), a single-segment string-pair learn mark with swapped family;
R6 diagnostic emits `no-task-family-inconsistency`, tfam=0). PASS iff:
`TASK-FAMILY-INCONSISTENCY` is emitted for the s0=1 mark and
`(tfam & 1)==1`. (The causal contest machinery may independently open a
LAW-CHANGE contest on this mark; that is separate machinery and does not
affect this bar.)

**K-R7-3 (no regressions):** All of the following hold with the modified
mechanism: K-R6-1 (`(tfam5 & 12)==12 && (tfam5 & 3)==0 &&
(tfam5 & 64)!=0`), K-R6-2 (`(tfam6 & 4)!=0 && (tfam6 & 3)==0 &&
(tfam6 & 64)!=0`), K-R5-1 (`(tfam4 & 3)==3`), K-R5-2a (`tfam1==0`),
K-R5-2b (`(tfam2 & 1)==1` and CL merger intact), K-R5-2c
(`(tfam3 & 1)==1` and sfanom3==1), K-R4-1 through K-R4-5. PASS iff all
hold. Additionally: the six frozen sections (honest, X-R1 gamed,
confined, SWAP, F-P1 pollution-swap, F-P2 single-side) produce output
byte-identical to the committed `ROUTER6_RAW_OUTPUT.txt` EXCEPT for the
`audit_single_family` label change (`learn-marks s1>=2:` ->
`learn-marks s1>=1:`, counts unchanged); verified by diff showing no
other differences.

**K-R7-4 (determinism):** 3 consecutive runs of `router7_learn`
byte-identical (cmp). PASS iff identical.

If any bar fails, H-ROUTER7 is KILLED (do not adjust bars).

## Test plan

1. Copy `router6_learn.zag` to `router7_learn.zag` verbatim; verify with
   cmp before editing. `router6_learn.zag` must remain unmodified
   (verified by git status / diff at the end).
2. Apply exactly: (a) explicit-fallback logic in `build_table_rest`;
   (b) s1>=1 scope in `audit_single_family` + `audit_task_family` and
   the label update; (c) F-FB and F-S1 curriculum sections + main()
   verdict lines for K-R7-1/K-R7-2; (d) extended final gate. No other
   changes.
3. Build with the pinned toolchain (`znc 2026.07.0-dev (edition 2026)`),
   run, verify K-R7-1, K-R7-2 bars in-program, diff the six frozen
   sections against committed `ROUTER6_RAW_OUTPUT.txt` (expecting only
   the label change).
4. Run 3x, compare with cmp: verify K-R7-4.
5. Pilot note: F-FB and F-S1 dynamics were verified against the
   UNMODIFIED router6 mechanism before this prereg was frozen
   (exploration only; no mechanism code was written before this
   freeze).

## Classification expectation

Bounded L2+ structural learning with provenance diagnostics (unchanged).
The total-table invariant is a safety property; the s1>=1 extension is a
diagnostic scope repair. NOT L3.

## Governance

Pure Zag. No Python at any stage. Prereg frozen before implementation.
Commit order: this prereg strictly precedes the implementation commit
(verify with `git merge-base --is-ancestor`). Only owned files staged.
No em dashes in loop docs.
