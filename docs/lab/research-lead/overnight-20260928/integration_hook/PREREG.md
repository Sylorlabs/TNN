# PREREG: INTEGRATION-HOOK (plan-invalidation hook on binding revision)

Date: 2026-10-03. Worker: INTEGRATION-HOOK. Lane:
`docs/lab/research-lead/overnight-20260928/integration_hook/`
Follows up on INTEGRATION-STRESS (C461) follow-up 2.

## Background

C461 froze two integration findings: (a) plans cache the bound fam at
build time, so binding revision requires a plan rebuild to take effect
(IS-D); (b) two consecutive spurious failures retire a clause before the
3-fail revision latch (IS-C). In IS-D the worker called `clear_plans`
manually after `u_revise` to make the revised binding take effect. The
report recommended testing whether a general plan-version check subsumes
the manual clear_plans. This experiment builds and tests that hook.

## Hypothesis

A general plan-version check inside `compose` subsumes IS-D's manual
`clear_plans`: before loading a cached plan, re-check every cached
(tag, fam) pair against the live binding contract via `bind_fam`. On any
mismatch, invalidate only that plan row and fall through to rebuild.
This fires automatically on binding revision (no caller action),
invalidates only affected plans (targeted, not a full clear), covers any
fam-changing transition (revision, retirement), and never fires when
bindings are unchanged.

## Design (frozen before implementation)

Build on C461's integrated composer, not a redesign:

- `ih_base.zag`, `ih_world.zag`, `ih_module.zag`: byte-copies of
  C461's `is_base.zag`, `is_world.zag`, `is_module.zag` (cmp-verified).
  `u_revise` is NOT modified.
- `ih_learn.zag`: byte-copy of `is_learn.zag` plus two hook functions:
  - `plan_stale_need(L,S,pi)`: returns p+1 for the first need whose
    cached fam differs from the live `bind_fam(L,S,tag)`; 0 if all fresh.
    Pure (u_check has no side effects). No identifiers: tags, fams, goal
    tags all read from the plan row at runtime.
  - `plan_invalidate(L,S,pi,sp)`: zeroes the plan row's goal tag
    (targeted invalidation, same cell `clear_plans` zeroes), records
    [goal tag, cached fam, current fam] at L+13292/13296/13300 and bumps
    the stale counter at L+13288.
  - `compose`: after `plan_find` hits, run the check; on stale,
    invalidate and fall through to the existing build path. No other
    changes to plan_new / execute_plan / learn_bindings.
- `ih_main.zag`: reduced driver. IH-SETUP (world A, 4 ret + 4 vfy + 4 cnt
  episodes with specializes, E0 build, E0 re-query) then IH-COLLISION
  (byte-faithful port of C461's demo_collision: QD0, real trials, 3x
  u_invalidate, judgment table, u_revise, QD1, QD1 re-query, dump_plans).
  **No `clear_plans` call anywhere in the driver** (grep-verified).
  The driver prints `IHH-INV goal=<gt> cached=<f> cur=<f> stale=<n>`
  from the evidence slots.

Why lazy (query-time) rather than an eager hook inside u_revise: the
check fires exactly when a stale plan would otherwise execute, needs no
caller discipline, and covers retirement-without-revision (bind_fam then
returns -1) which an eager revise-hook would miss.

## Test scenario

The IS-D tag-shape collision, replicated: tag bound to RETRIEVE (fam 0)
is reused by a VERIFY-shaped goal (nf=4). QD0 builds the plan under the
stale binding (hook must NOT fire: cached fam 0 == live fam 0) and
misroutes visibly. Real trials contradict; 3x u_invalidate latches
revision; u_revise flips the binding to fam 1. QD1 must hit the hook.

## Frozen predictions

P1 (setup anchor): E0 line identical to C461:
`Q id=E0 goal=813 st=2 vers=2,3,3,5 ans=7:1,611,0,1,611,1,2 agree=1 cs=96 cg=336`
P2 (healthy plan loads): E0 re-query `st=1 agree=1`; `IHH-NOFIRE stale=0`.
P3 (stale misroute, hook correctly silent): QD0
`Q id=QD0 goal=818 st=2 vers=0 ans=1:0 agree=0 cs=56 cg=56`.
P4 (revision): ISD-REV
`tag=801 probes=3 dc=2 active=0 req=1 olderr=2 revcount=1 nclause=(1,0,1,1) route1=1 route0=0 route2=0 tr0=0 tr1=1 tr2=0`.
P5 (hook fires): `IHH-INV goal=818 cached=0 cur=1 stale=1` printed once.
P6 (rebuild correct): QD1
`Q id=QD1 goal=818 st=2 vers=3 ans=2:1,1 agree=1 cs=16 cg=56`
with NO clear_plans call in the driver.
P7 (targeted, healthy plan survives): QD1 re-query `st=1 agree=1`,
stale counter unchanged at 1.

## Kill bars

- K1 (hook fires on revision): P5 observed exactly; stale counter 0->1
  across QD1; QD1 st=2 (rebuilt, not loaded). FAIL otherwise.
- K2 (plans rebuild correctly): P6 observed exactly (agree=1 with the
  revised fam). FAIL otherwise.
- K3 (no spurious invalidation): P2 and P7 observed; IHH-INV appears
  exactly once in the full output. FAIL otherwise.
- K4 (determinism): 3/3 byte-identical runs (sha256 recorded), stderr
  empty on all runs. PROCESS-FAIL otherwise.
- K5 (toolchain): safebin from first command, pinned znc, pure Zag, no
  python. PROCESS-FAIL on any violation.
- K6 (generality/no identifiers): the hook functions contain zero
  numeric identifiers (grep audit: no tag/rel/fam/goal literals);
  `clear_plans` has zero call sites; the diff vs is_learn.zag is the hook
  plus the compose edit only. FAIL otherwise.

## Falsification criteria

- F1: IHH-INV fires zero times on QD1 (hook failed to fire).
- F2: IHH-INV fires on E0R, QD0, or QD1R (spurious invalidation).
- F3: QD1 shows st=1 (stale plan loaded) or agree=0.
- F4: any frozen P1-P7 value differs.
- F5: runs not byte-identical, stderr non-empty, or toolchain violation.

## Deliverables and commit order

1. This PREREG.md + NAMECHECK.md (Step 0), committed ALONE.
2. Implementation: ih_base/ih_world/ih_module/ih_learn/ih_main.zag,
   ih_build.sh, ih_full.zag.
3. Artifacts: ih_bin, ih_compile.txt, ih_run1/2/3.txt (+ .err), sha256.
4. REPORT.md with verdict.

No em/en dashes in any lane file (byte audit). No domain language in
code or docs: fams/tags/rels are opaque integers throughout.
