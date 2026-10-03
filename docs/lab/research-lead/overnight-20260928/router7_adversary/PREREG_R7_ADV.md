# PREREG_R7_ADV: H-ROUTER7 Independent Red Team

**Date:** 2026-09-29
**Status:** FROZEN (before any attack code, build, or run)
**Target:** H-ROUTER7 SURVIVES (frozen prereg `34347580c`; R1 total-table
fallback + R2 s1>=1 family-audit scope; builder result in
`981459ee3`)
**Stance:** assume the H-ROUTER7 claims are false.

## Claims under test

C1 (R1): "The compiled routing table is total by design: every feature
triple routes to a declared task code; route3 never silently returns
-1." Mechanism: `build_table_rest` appends an explicit terminal
`[any]->WITHHOLD` fallback iff no all-ANY rule was compiled.

C2 (R2): single-segment (s1==1) learn marks are now family-checked like
multi-segment ones. The `s1>=2` scope restriction is removed from the
learn-mark predicates of `audit_single_family` and `audit_task_family`.

C3: no regressions vs H-ROUTER6 (K-R7-3) and deterministic (K-R7-4).

## Code facts established by read-only source review (no execution)

F1. `RT` is `z_alloc(192)`; rules are 8 bytes each: at most 24 compiled
rules. `rt_add` emits `TABLE OVERFLOW` and returns `nrt` unchanged when
`nrt>=24`. The R1 fallback append goes through `rt_add`.

F2. `build_table_rest` compiles ACTIVE equality entries with
`FX_SET` on var0, capped at 64 entries (`nn<64`), each via `rt_add`
(capped at 24). `compile_thresholds` runs first and can add up to 4
rules (two s0 values, GE/LT pair each).

F3. `route_features` sets `s1=nseg`, where `nseg>=1` for every non-empty
line and `nseg` is capped at 9. For the empty line, `s0=pk=0`. Hence a
learn mark with `s0` in {1,2} always has `s1>=1`: the `s1>=1` lower bound
excludes no reachable learn mark of a checked content type.

F4. Query anchors require `s0==0 && s1==1`; `qk` (s2) is only computed
for single-segment lines without `>`. Multi-segment lines always have
s2=0.

F5. In the builder's F-FB section, the out-of-scope attack mark
("ab>1,0"->CL, features (3,1,0)) replays as WITHHOLD via the explicit
fallback: `REPLAY-MISMATCH #19 mark CAUS_LEARN routed WITHHOLD`,
`REPLAY 18/19`.

## Attacks

### X-R7-1 (capacity: TABLE OVERFLOW defeats the total-table invariant)

Fixture OF: fresh world (nep/nent/nct zeroed, root
`new_entry(W,ACT_ROUTE(),0,-1,0)` exactly as `run_induction` starts).
Teach 36 lines as TC_PL (PROC_LEARN), seq 1..36, no conflicts, no query
marks, no WITHHOLD marks:

- v=1..9: v copies of `aa>bb` joined by `;` (features (1,v,0))
- v=1..9: v copies of `1,0,0>1,0` joined by `;` (features (2,v,0))
- v=1..9: v copies of `aab` joined by `;` (features (0,v,0), v>=2;
  (0,1,1) for v=1)
- v=1..9: v copies of `ab>1,0` joined by `;` (features (3,v,0))

Then `compile_thresholds`, `build_table_rest`; emit TABLE-SIZE; scan
the compiled table for an all-ANY rule (emit HASANY01); probe
`route3(RT,nrt,0,10,0)` and emit the raw integer (s1=10 is unreachable
via teach, so no rule can cover it except an all-ANY rule).

Hand-derived expectation: the 36 distinct triples induce at least 24
ACTIVE FX_SET equality entries (no threshold compilation fires: every
s0=1/s0=2 group is single-task, so the {W,M} pair never forms); the
25th `rt_add` emits TABLE OVERFLOW; the root [any] entry stays
FX_UNRES (no WITHHOLD marks), so `hasany==0` and the fallback append is
attempted at nrt=24 and silently dropped by the overflow guard; the
probe returns -1.

Kill criterion (all four must hold): (a) `TABLE OVERFLOW` appears in the
adversary output; (b) no `explicit fallback` TABLE-RULE line appears;
(c) HASANY01=0; (d) the (0,10,0) probe returns -1.

Verdict on success: H-ROUTER7 DOWNGRADED (not killed). The K-R7-1 F-FB
fixture still passes; the mechanism implements the design exactly. What
fails is the categorical C1 headline as stated. Narrowed claim: the
table is total iff fewer than 24 rules are compiled before the fallback
append; at capacity the overflow guard drops the fallback and route3
can return -1. The compile-time TABLE OVERFLOW emit does not change the
per-probe return path.

If (a) does not occur (24 rules unreachable through teach), X-R7-1
FAILS and C1 holds within the teachable envelope.

### X-R7-2 (single-segment evasion attempts)

Fixture S1E: `run_induction(W,0)` (honest anchors: qk=1 PROC n=2, qk=2
CAUS n=2), then:

- teach `ab>cd` as TC_CL, seq 19 (features (1,1,0); builder's F-S1;
  family CAUS vs PROC anchor: swapped)
- teach `9,9,9>9,8` as TC_PL, seq 20 (features (2,1,0); family PROC vs
  CAUS anchor: swapped)

Then the phase 1b/1c/1d pipeline and `audit_task_family`; count
`TASK-FAMILY-INCONSISTENCY` lines and read tfam.

Kill criterion: zero `TASK-FAMILY-INCONSISTENCY` lines, or
`(tfam&3)==0`, with both swapped marks present in the curriculum. Any
evasion of the extended check under a known uncontested anchor breaks
C2.

Expected honest outcome: two INCONSISTENCY lines (s0=1 bit0, s0=2
bit1), `(tfam&3)==3`; X-R7-2 FAILS and C2 holds for the evasion set.
(The causal contest machinery may emit LAW-CHANGE lines for these
marks; that is separate machinery and does not affect this bar.)

Fixture S1C (disclosed-boundary calibration, not a kill): S1E plus
teach `zzz` as TC_CQ, seq 21 (features (0,1,1); contests the qk=1
anchor). Expect the H-ROUTER6 disclosed behavior unchanged by R2:
`ANCHOR-CONTESTED` for qk=1, `task-family-check-partial`, zero
`TASK-FAMILY-INCONSISTENCY` for s0=1. Any deviation from the R6
disclosed behavior is reported.

### X-R7-3 (regression and integrity)

- Rebuild `router7_learn.zag` from the committed git blob with the
  pinned toolchain (`znc 2026.07.0-dev (edition 2026)`); run 3x.
- Byte-compare each run against committed `ROUTER7_RAW_OUTPUT.txt`.
- Diff the six frozen sections (honest, gamed, confined, swap,
  pollution-swap, single-side) against committed
  `ROUTER6_RAW_OUTPUT.txt`: the only permitted differences are the
  `learn-marks s1>=2:` to `learn-marks s1>=1:` label lines.
- Confirm K-R7-1/K-R7-2 PASS lines and all K-R6-1/K-R6-2/K-R5-1/
  K-R5-2a/K-R5-2b/K-R5-2c/K-R4-1..K-R4-5 bars in the rebuilt output.

Kill criterion (any one): rebuilt output differs from the committed
raw; the three runs differ from each other; the six-section diff shows
any difference beyond the label change; any frozen bar reads FAIL.

Verdict on success: H-ROUTER7 KILLED (integrity failure).

Expected honest outcome: X-R7-3 FAILS (everything reproduces).

### X-R7-4 (new boundaries introduced by R1/R2)

4a (no laundering through the fallback): rerun the builder's F-FB
fixture verbatim (honest curriculum + `ab>1,0`->CL). Confirm
`audit_replay` still reports `REPLAY-MISMATCH` for the attack mark:
the explicit fallback must not launder the out-of-scope mark through
the replay audit. Finding iff the mark replays clean.

4b (single-family scope delta): minimal curriculum with anchors
(`hello`,`world` as PQ; `1,0,0`,`0,0,0` as CQ) plus `ab>cd` as PL
(features (1,1,0); s0=1 learns exist ONLY at s1==1) plus
`5,5,5>5,4;6,6,6>6,5` as CL (features (2,2,0)). Run
`audit_single_family`. Under H-ROUTER6's s1>=2 scope this curriculum
fires SINGLE-FAMILY-ANOMALY (s0=1 has no learns at s1>=2); under R2's
s1>=1 scope it must not. Document the delta and classify: false-positive
fix vs diagnostic regression. Finding iff the task-family check also
misses a genuine inconsistency on this curriculum.

Neither 4a nor 4b changes the verdict by itself; results are recorded
as boundaries.

## Verdict rule

- X-R7-1 success: DOWNGRADED (C1 narrowed as above).
- X-R7-2 evasion success: DOWNGRADED at minimum; KILL if it also breaks
  the frozen K-R7-2 fixture.
- X-R7-3 success: KILLED.
- X-R7-4: boundaries only.
- All attacks fail: H-ROUTER7 SURVIVES this red team.

## Method

- Harness `r7_adv.zag` = lines 1..1799 of the committed
  `router7_learn.zag` blob (everything before `fn main`), copied
  verbatim and cmp-verified, plus attack-only `main()`. No mechanism
  edits. Fixture dynamics are driven through the public `teach` /
  `run_induction` / pipeline functions only.
- Pinned toolchain `znc 2026.07.0-dev (edition 2026)`. Every attack run
  3x; byte-identical via cmp required.
- Pure Zag. No Python at any stage (fixtures are hand-written Zag
  string literals; builds, runs, greps, hashes, cmp via shell only).
- X-R7-3 uses `git show` of the committed blob; no worktree source.

## Governance

- This prereg is committed alone before any attack code, build, or run.
  Verify with `git merge-base --is-ancestor`.
- Only `router7_adversary/` paths staged. No binaries committed (builds
  in /tmp/r7adv and /tmp/r7reg only). No em dashes in loop docs.
- No worker-count claims; scheduler state not needed for this task.
