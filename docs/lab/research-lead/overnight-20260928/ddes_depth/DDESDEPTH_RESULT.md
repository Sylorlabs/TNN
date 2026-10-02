# DDES Sealed Depth Test Result (L>=8)

## Prereg

Commit `9489e17c0` (file `ddes_depth/PREREG_DDESDEPTH.md`). Committed
alone; implementation is a strict descendant (verified via
git merge-base --is-ancestor before this report).

Target: repaired DDES (ddesr.zag, REPAIR-PASS 17c97a2cd).
This test executes remaining work item 1 from the DDES Promotion
Assessment (b75886067): sealed L>=8 depth run on the repaired binary
(deferred K-NX3 sub-bar from PREREG_DDES.md).

## Sealed World G

H0 = [(X,Z,9),(Z,Y,0)]. H1 = [(X,Y,8)].
Delays 9 and 8 appear in no frozen DDES source file (verified by grep
over ddes/ and ddes_repair/ before implementation).

Analytic expectation (frozen in prereg):
H0 arrivals Y=9; H1 arrivals Y=8. Frontier (Y, t*=8).
Plan [S + 8xW + OY], length 10, L=10 >= 8.

## Method

New file `ddes_depth/ddes_depth.zag`: lines 1-498 are byte-verbatim
from the frozen ddesr.zag (all driver functions:
compute_arrivals, compute_frontier, eff_waits, synthesize_plan,
emit_plan, predict, world_step, ddes_world, w_* helpers,
load_world_A through load_world_F). Appended: load_world_G and a
main() running World G on both truth configs. No logic changes.
This mirrors the adversary precedent (killer.zag).

Compiled with znc (pure Zag). Binary: `ddes_depth/ddes_depth_bin`.

## Test results (3/3 byte-identical, md5 04530a32187f46797c7cfda2ed2492fc)

Exit 0 on all runs. 0 bytes stderr on all runs.

WORLD G
TARGET V*=2 t*=8 schema=1
PLAN [S,W,W,W,W,W,W,W,W,OY] candidates_built=1
EXEC real=0
PRED h0=0 h1=1
SURVIVE h0
ELIM h1
CONVERGE-OK
WORLD G
TARGET V*=2 t*=8 schema=1
PLAN [S,W,W,W,W,W,W,W,W,OY] candidates_built=2
EXEC real=1
PRED h0=0 h1=1
ELIM h0
SURVIVE h1
CONVERGE-OK
SUMMARY ok=2/2 plans_built=2

cfg0 (truth=H0): plan length 10, 1 plan assembled, 1 real execution,
true hypothesis survives. Matches frozen expectation exactly.

cfg1 (truth=H1): plan length 10, 1 plan assembled, 1 real execution,
true hypothesis survives. Matches frozen expectation exactly.

## Kill bar verdicts

- K1 (sealed): PASS. Prereg 9489e17c0 committed alone before any test
  code existed. Delays 9 and 8 verified absent from ddes/ddes.zag and
  ddes_repair/ddesr.zag. Commit order verified: prereg is a strict
  ancestor of the implementation commit.
- K2 (depth convergence): PASS. Both configs CONVERGE-OK. Plan length
  exactly 10 actions (>= 8). Exactly 1 plan assembled per config
  (plans_built=1 then 2). Exactly 1 real execution per config. The
  surviving hypothesis matches truth on both configs.
- K3 (purity): PASS. Pure Zag. No Python used at any stage (source,
  build, execution, analysis). Zero em-dash bytes in all committed
  files (byte-checked). 3/3 byte-identical runs, exit 0, zero stderr.

## Classification

Unchanged: strong L2 (guided generation), NOT L3. This test exercises
the deferred K-NX3 sub-bar on the repaired binary; it does not alter
authorship.

## DEPTH-TESTED

The deferred sealed-depth sub-bar is now executed on the repaired
binary: DDES derives a length-10 discriminating plan in one shot, with
no enumeration, no bound, and no filter, and converges correctly on
both truth configs at depth L=10.
