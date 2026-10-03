# REPORT: INTEGRATION-HOOK (plan-invalidation hook on binding revision)

Date: 2026-10-03. Worker: INTEGRATION-HOOK.
Lane: `docs/lab/research-lead/overnight-20260928/integration_hook/`
Prereg: commit 557ca6a48 (PREREG.md + NAMECHECK.md, committed alone
before any implementation file existed). Implementation commit
cc01d55ad; artifacts commit 3cd56ea36; this report follows.
Follows up on INTEGRATION-STRESS (C461) follow-up 2.

## Verdict: HOOK WORKS (K1-K6 PASS)

The general plan-version check subsumes IS-D's manual `clear_plans`.
On the replicated IS-D tag-shape collision, the hook fired exactly once,
automatically, on the first query after binding revision, and the plan
rebuilt correctly with the revised family. No `clear_plans` call exists
in the driver. Healthy plans keep loading; the hook never fires
spuriously.

## What was built

- `ih_base.zag`, `ih_world.zag`, `ih_module.zag`: byte-copies of C461's
  `is_base.zag`, `is_world.zag`, `is_module.zag` (cmp-verified).
  `u_revise` untouched.
- `ih_learn.zag`: byte-copy of `is_learn.zag` plus the hook (diff
  audited: hook functions plus the compose edit only):
  - `plan_stale_need(L,S,pi)`: returns p+1 for the first plan need whose
    cached fam differs from the live `bind_fam(L,S,tag)`; 0 if fresh.
    Pure: `u_check` has no side effects. Zero numeric identifiers.
  - `plan_invalidate(L,S,pi,sp)`: zeroes that plan row's goal tag
    (targeted invalidation), records [goal tag, cached fam, current fam]
    at L+13292/13296/13300, bumps the stale counter at L+13288.
  - `compose`: after `plan_find` hits, run the check; on stale,
    invalidate and fall through to the existing build path.
- `ih_main.zag`: reduced driver. IH-SETUP (world A, 4 ret + 4 vfy + 4 cnt
  episodes with specializes, E0 build, E0 re-query) then IH-COLLISION
  (faithful port of C461's demo_collision with the manual `clear_plans`
  removed).
- `ih_build.sh`, `ih_full.zag` (exactly one `fn main`), `ih_bin`,
  `ih_compile.txt`, `ih_run1/2/3.txt` (sha256
  2100138a81b6675654e7ebc4b90aff3d5c5f344d79f7dfb93d8d72ac7ce37723)
  + `.err` (empty).

## Evidence (from ih_run1.txt; runs 2/3 byte-identical)

IH-SETUP anchor: E0
`st=2 vers=2,3,3,5 ans=7:1,611,0,1,611,1,2 agree=1 cs=96 cg=336`
byte-identical to C461's E0. E0 re-query: `st=1 agree=1`,
`IHH-NOFIRE stale=0` (healthy plan loads; hook silent).

IH-COLLISION:
- QD0 `st=2 vers=0 ans=1:0 agree=0 cs=56 cg=56`: stale binding misroutes
  end-to-end. The hook correctly does NOT fire here: the plan was built
  under the live binding (cached fam 0 == live fam 0); the binding is
  stale relative to reality, not relative to the contract.
- ISD-REV `tag=801 probes=3 dc=2 active=0 req=1 olderr=2 revcount=1
  nclause=(1,0,1,1) route1=1 route0=0 route2=0 tr0=0 tr1=1 tr2=0`:
  identical to C461.
- QD1 (no clear_plans): `st=2 vers=3 ans=2:1,1 agree=1 cs=16 cg=56`,
  identical to C461's post-clear_plans recovery line.
- `IHH-INV goal=818 cached=0 cur=1 stale=1`: the hook fired exactly
  once, invalidating goal 818's plan (cached fam 0 vs revised fam 1).
- QD1 re-query: `st=1 agree=1`; stale counter unchanged at 1 (no
  spurious fire). Final `dump_plans` shows goal 818 rebuilt as
  `[0:801:1]`.

## Kill bar assessment (observed vs frozen)

| Bar | Frozen | Observed | Result |
|-----|--------|----------|--------|
| K1 | IHH-INV once on QD1; stale 0->1; QD1 st=2 | exact (`goal=818 cached=0 cur=1 stale=1`) | PASS |
| K2 | QD1 `st=2 vers=3 ans=2:1,1 agree=1` | exact (`cs=16 cg=56`) | PASS |
| K3 | E0R st=1; QD1R st=1; IHH-INV exactly once; stale=0 after E0R | exact | PASS |
| K4 | 3/3 byte-identical, stderr empty | sha256 2100138a x3; .err 0 bytes | PASS |
| K5 | safebin, no python, pure Zag, pinned znc | verified (Step 0 recorded) | PASS |
| K6 | zero identifiers in hook; zero clear_plans call sites; minimal diff | grep/diff verified | PASS |

## Falsification criteria (frozen; none fired)

- F1 (hook fails to fire on QD1): NOT FIRED.
- F2 (spurious fire on E0R/QD0/QD1R): NOT FIRED.
- F3 (QD1 loads stale plan or disagrees): NOT FIRED.
- F4 (any frozen value differs): NOT FIRED.
- F5 (non-determinism / stderr / toolchain): NOT FIRED.

## What this establishes (and does not)

Establishes: the report's follow-up 2 is answered yes. A general
plan-version check inside `compose` subsumes the manual `clear_plans`
for the binding layer, and strictly improves on it: (1) it fires
automatically, so no caller must remember to clear; (2) it is targeted,
invalidating only the plan whose binding changed (E0's plan row was
never touched); (3) it covers any fam-changing transition, including
retirement-without-revision (bind_fam then returns -1), which an
eager revise-time hook would miss. The revision path (`u_revise`) needed
no modification.

Does not establish: eager invalidation. The hook is lazy: a stale plan
row that is never loaded is never invalidated (the final dump shows
goal 813 still caching fam 0 for tag 801 after the revision). This is
safe (the check runs before every load, so a stale plan can never
execute) but a future eager sweep on revision could proactively clean
such rows. Also not tested: multi-need plans with a stale interior need
(the hook records the first stale need; the mechanism is need-indexed
and general, but only single-need staleness was exercised); coverage
contract staleness (IS-A's bucket rebuild), which lives below the fam
cache and is out of scope by design.

## Architecture accounting

- Cognition lines added: ~32 lines (two hook functions + 7-line compose
  edit + comments). New hardcoded semantic cases: 0. Modes/bridges/
  handlers: 0. New opcodes/edge types: 0.
- Researcher-owned: the hook code, the driver, the prereg.
- Learner-owned (in S/L state): the stale counter and invalidation
  evidence slots are learner-state counters; the invalidation itself is
  a learner-state transition driven by the live contract, not a demo
  action. The driver never calls clear_plans or invalidates directly.
- Pinned znc via safebin.

## Toolchain guard

Step 0 executed at startup and recorded in NAMECHECK.md:
PATH=$HOME/safebin as the first command; `which python3` and
`which python` return nothing. Zero Python computation. Git writes via
/usr/bin/git absolute path; explicit pathspecs on every commit; nothing
pushed. K5 PASS with no disclosures.

## Disclosed bounds

- The collision demo is researcher-staged (as in C461); the hook logic,
  the trials, the revision, and the query answers are real.
- Self-triggered revision in the live query path remains open
  (C461 follow-up 1); the hook removes the manual step after revision
  fires but does not trigger revision itself.
- One stress scenario (IS-D), frozen world. No broad generality claim.

## Deliverables

All in `docs/lab/research-lead/overnight-20260928/integration_hook/`:
PREREG.md (frozen, commit 557ca6a48), NAMECHECK.md (Step 0),
ih_base/ih_world/ih_module.zag (byte-copies, cmp-verified),
ih_learn.zag (hook), ih_main.zag (driver), ih_build.sh, ih_full.zag
(exactly one `fn main`), ih_bin, ih_compile.txt,
ih_run1/2/3.txt (+ .err, empty), REPORT.md (this file).
Commits: 557ca6a48 (prereg alone), cc01d55ad (implementation),
3cd56ea36 (artifacts + runs); REPORT commit follows. All local,
never pushed.

## Recommended follow-ups (for the parent, not decided here)

1. Wire the hook's stale evidence into a revision trigger: a plan
   invalidated twice in a row for the same tag is counterevidence the
   binding (not the plan) is wrong, which is C461 follow-up 1 territory.
2. Multi-need stale-interior-need test and a retirement-without-revision
   track to exercise the -1 path the hook already covers in code.
3. Consider an eager sweep variant and measure whether lazy checking
   costs anything at plan-load scale.
