# Architecture Compression Tracker

Date established: 2026-09-30.
Worker: Architecture Compression Tracker.
Status: COMPRESSION-TRACKING-ESTABLISHED.
Method: MEASUREMENT_PROCEDURE.md (cognition lines, per BASELINE_TABLE.md and
REMEASURE_REPORT.md). This document tracks capability per researcher-authored
line over time. It is a living document: append rows, never edit historical
rows.

## The metric (Micah's priority 6)

"How much general capability does each researcher-authored line buy?"

Not "smallest source wins". Capability density is the goal. The desired
trajectory:

```text
capability up
specialized mechanisms down
duplicated code down
learner-created state up
```

## Ratios defined

- **R_test** (provisional): builder self-tests passed / cognition lines.
  Not canonical, because test batteries differ in difficulty and scope.
  Useful only for watching direction of travel within one lineage.
- **R_world** (canonical): freeze worlds passed / cognition lines.
  Comparable across generations because the world suite is fixed.
  Only defined for systems actually run on the frozen worlds.
- **R_fw** (future canonical): sealed FW1-FW9 worlds passed / cognition
  lines. This is the number the integration build must report.

## Current snapshot (2026-09-30)

| Generation | Cognition lines | Self-tests | Freeze worlds | Learned structures | State bytes | Modes | Bridges | Handlers | Sem cases | R_test (per 100 lines) | R_world |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Frozen core (87ac95d08) | 586 | n/a (run 97b28e6a6) | 1/9 | 0 | 32768 | 0 | 0 | 0 | 0 | n/a | 1/586 = 0.17/100 |
| contlearn2 (179b4a950) | 136 | n/a (LEARNER-EXTENDED) | not run | 0 | 1024 | 0 | 0 | 0 | 0 | n/a | not run |
| CLA-2 (e639904f2) | 685 | 15/15 | not run | 3 (GROUP, MAP, edge-standing) | 16384 | 0 | 0 | 0 | 0 | 2.19 | pending |
| CAM-1 (371d20743) | 408 | 6/6 | not run | 1 (MAP nodes) | 344080 | 0 | 0 | 0 | 0 | 1.47 | pending |
| ACT (f7d87938f) | 162 | 24/24 | not run | 2 (POLICY_ROOT, ACTION-GUIDEs) | 33816 | 0 | 0 | 0 | 0 | 14.81 | pending |
| COMP-1 (170e39424) | ~300 (estimated, unmeasured) | 10/10 | not run | 5+ (plan nodes, step nodes, SEQ edges, query records, SUPPORTS/USE edges) | CLA-2 workspace | 0 | 0 | 0 | 0 | ~3.33 (est) | pending |
| DEVINT-CLA2 (35f9500b2) | unmeasured (1212 total lines) | 11/11 stages | not run | extends CLA-2 workspace | CLA-2 workspace | 0 | 0 | 0 | 0 | unmeasured | pending |

Notes:
- COMP-1 cognition lines are an estimate from the integration scout
  (INTEGRATION_SCOUT.md), not a formal re-measurement. The 879 figure in
  BUILD_REPORT.md is total source lines including driver and harness.
  A formal re-measurement of comp1.zag is an open item below.
- DEVINT-CLA2 is a developmental experiment on the CLA-2 workspace, not
  part of the four-system integration path. Listed for completeness.
- CAM-1 posture is bounded L2 per the red team (menu selection, not
  composition). Its integration plan deletes the P-DEP menu; only verify,
  promote, and contradict port forward.

## A correction to the parent task's arithmetic

The parent task stated 685 + 408 + 162 + 879 = 2134 across four builds.
That mixes cognition lines (685, 408, 162) with COMP-1's total source
lines (879). The honest cognition-line total is 1255 measured plus
~300 estimated for COMP-1, or **~1555 total**. The re-measurement report
already records this: "Starting point: 1255 cognition lines; COMP-1 not
yet measured but ~300 estimated cognition lines, for ~1555 total across
four." This tracker uses 1555 as the pre-integration total.

## Duplication inventory (from integration scout)

~475 lines of workspace machinery written 4 times: byte accessors,
node/edge accessors (4 spellings of the same operations), allocators,
linkers, teach/query paths, activation (2 versions), evidence bid
(3 versions, one with the ACT directionality divergence since fixed),
and 4 test harnesses. Integration recovers roughly this much.

## Integration target row (to be filled when the build lands)

| Field | Target / expectation | Actual (pending) |
|---|---|---|
| Cognition lines | ~1100 projected (scout); hard ceiling 1200 (integration prereg shape, K-INT) | pending |
| One binary | CLA-2 workspace format wins (40-byte nodes, 16-byte edges, 12 edge types) | pending |
| Test suites | CLA-2 15 + ACT 24 + COMP-1 10 must all pass on the one binary; CAM-1 verify/promote/contradict ported, menu deleted | pending |
| Modes / bridges / handlers / semantic cases | 0 / 0 / 0 / 0 | pending |
| Sealed FW1-FW9 | run the full suite, report worlds passed | pending |
| R_fw | worlds passed / cognition lines | pending |
| CAM-1 menu ban | source scan confirms eval_body 4-way dispatch does not reappear | pending |

## Trajectory reading (2026-09-30)

1. **Lines:** negative so far. 1555 (four separate builds) > 586 (frozen
   core). Each builder wrote a full stack. The projection awaits the
   integrated build.
2. **One-System metrics:** holding at zero across all six rows.
   Modes 0, bridges 0, handlers 0, semantic cases 0. No subsystem
   proliferation has occurred.
3. **Learner-created structure:** positive. 0 -> 3 + 1 + 2 + 5+.
   The learner now creates GROUP nodes, MAP nodes, edge-derived
   standing, POLICY_ROOT conventions, ACTION-GUIDEs, plan/step nodes,
   SEQ edges, and query records, where the frozen core created nothing.
4. **Capability:** builders pass their own suites (15, 6, 24, 10, 11).
   Cross-comparable capability (freeze worlds, then FW1-FW9) is pending
   for every builder system. This is the largest evidence gap in the
   program.

## Open measurement items

1. Formal re-measurement of COMP-1 cognition lines (per
   MEASUREMENT_PROCEDURE.md) to replace the ~300 estimate.
2. Formal re-measurement of DEVINT-CLA2 cognition lines (informational;
   not in the integration path).
3. Integrated build measurement: cognition lines, all four test suites,
   zero-count verification for modes/bridges/handlers/semantic cases.
4. Sealed FW1-FW9 run on the integrated build: worlds passed, R_fw.
5. Fresh freeze-challenge rerun on the integrated build (Micah's
   priority 5): does 1/9 improve without source edits?

## Update protocol

- Append a new snapshot row after every builder landing, integration
  milestone, or sealed-world run.
- Fill the integration target row when the integrated build lands;
  move it to a dated snapshot row.
- Never edit a historical row. Corrections go in a dated note, as the
  correction above does.
- Commit this file with the owned path only, explicit pathspecs,
  contaminated-paper zero-diff verified.
