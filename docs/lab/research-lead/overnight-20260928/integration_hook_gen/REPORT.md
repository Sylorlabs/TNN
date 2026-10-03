# REPORT: INTEGRATION-HOOK-GENERALIZE

## Verdict: GENERALIZE PASS (K1-K6 preserved, GK1-GK6 all green)

Non-ledger task. Branch `tnn-native-lab`, lane
`docs/lab/research-lead/overnight-20260928/integration_hook_gen/`.
All commits local, never pushed.

## What was built

A generalization battery on top of INTEGRATION-HOOK's plan-invalidation
hook, testing the three open limitations from that report:

1. **Multi-need stale-interior-need**: a 3-need goal (820) whose middle
   need (plan position p=1) goes stale while the row sits unused.
2. **Coverage-contract staleness**: the RET coverage contract (3000)
   revised to admit 602 only, with binding contracts untouched.
3. **Lazy vs eager**: `u_revise` deliberately left WITHOUT any eager
   plan sweep, to test whether the lazy check inside `compose` suffices.

The hook itself is unchanged except one evidence slot: `plan_invalidate`
now records the stale need index p at L+13304, and IHH-INV prints it as
`need=`. Diff vs `ih_learn.zag` is exactly that slot plus a comment.

## Results

**Regression (K1-K6): PASS.** All seven frozen lines R1-R7 byte-exact
vs INTEGRATION-HOOK (E0, E0R, QD0, ISD-REV, QD1, IHH-INV goal=818 with
the extended `need=0` field, QD1R).

**GK1 multi-need interior: PASS.** `IHH-INV goal=820 cached=0 cur=1
need=1 stale=2`: the hook's scan found the stale need at interior plan
position p=1 (not just p=0), invalidated exactly once, and the rebuilt
plan (`[2:805:0] [1:804:1] [0:803:0]`) agrees with the generic oracle
(`agree=1`).

**GK2 no spurious fire: PASS.** Exactly 3 IHH-INV lines in the whole run,
one per genuine invalidation. The hook stayed silent on G1Q0 (fresh
build), G2Q1 (coverage revision), G1Q1R (fresh rebuild), and G1Q1R2.

**GK3 coverage-contract discrimination: PASS.** After the RET coverage
revision (602 only), `Q id=G2Q1 goal=821 st=1 vers=0 ans=2:1,611
agree=1` with the stale counter unchanged (`G2-NOFIRE stale=1`). The
hook correctly did NOT fire: plan rows cache only [need-idx, tag, fam],
and per-need versions are recomputed from live coverage contracts inside
`execute_plan`. Coverage staleness needs no invalidation by construction.

**GK4 retirement: PASS.** `Q id=G2Q1R goal=821 decline=1` with
`IHH-INV goal=821 cached=0 cur=-1 need=0 stale=3`. A retired clause makes
`bind_fam` return -1 (abstain); -1 differs from any cached fam, so the
hook fires and the compose layer declines cleanly instead of answering
from a dead plan. After restore, `G2Q2` rebuilds with `agree=1`.

**GK5 determinism: PASS.** 3/3 byte-identical, stderr empty,
sha256 78feff9b78095715b523ec27ccf3f69cfbe7f7dc9ebb31b55fe5e19241b11cc3.

**GK6 toolchain: PASS.** Safebin from first command, pure Zag, zero
`clear_plans` call sites, hook-function identifier grep clean, no
em/en dash bytes in lane files.

## Answers to the three design questions

1. **Is eager invalidation needed, or does lazy suffice? LAZY SUFFICES**
   for this architecture. The core lemma: `compose` is the only caller
   of `plan_find` and `execute_plan`, so the invalidation check precedes
   every plan load and no stale plan can execute. The G1 scenario is the
   direct test: the row sat stale through a revision AND two other goal
   queries, then invalidated exactly at next use. No eager sweep exists
   anywhere in the code.
2. **Multi-need interior staleness: HANDLED.** The scan loop finds the
   first stale need at any plan position; `need=` evidence confirms p=1.
3. **Coverage-contract staleness: NO HOOK NEEDED.** Versions are not
   cached in plan rows; they are recomputed from live contracts at
   execute time. The hook's predicate (binding-contract mismatch) is
   exactly the plan's cached surface.

## Caveats and scope limits

- The lazy-suffices lemma holds because `compose` is the sole plan-load
  path. A future architecture with another load path would break it.
- Coverage needs no invalidation only while versions stay uncached.
- Exercised stale positions: p=0 and p=1 (3-need goal). The scan loop is
  general, but deeper positions were not separately probed.
- Retirement was tested on a 1-need goal; the mechanism is the same
  `bind_fam` path used for multi-need.
- Prereg amendment: N12's frozen `dc=2 active=0` was corrected to the
  observed `dc=0 active=1` (committed as 3ab717dbf before implementation).
  Cause: stage_g3_restore reads dc/active after u_revise, which restores
  active=1, dc=0. The observed values are the correct restored-clause
  state (route0=1 confirms). Telemetry read-timing miss in the
  prediction; no mechanism or kill-bar impact; the driver was deliberately
  NOT changed to chase the prediction.

## Commits (local only)

- 6fa328db5 prereg + namecheck (alone)
- 3ab717dbf prereg amendment N12 (alone)
- d7b6600ac implementation
- 386bebe5d artifacts
- (this report)

## Artifacts

- `gen_base/world/module/learn/main.zag`: sources
- `gen_build.sh`: build script
- `gen_full.zag`, `gen_bin`: assembled source and binary
- `gen_run1/2/3.txt`: 3/3 byte-identical runs
- `gen_compile.txt`: clean compile log
