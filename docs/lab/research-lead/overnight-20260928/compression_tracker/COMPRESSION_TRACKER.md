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

## Snapshot update: TNN-1 and MUL-1 (2026-09-30)

Appended 2026-09-30 by the Compression Tracker Updater. Historical rows
above are untouched.

| Generation | Lines (note) | Self-tests | Freeze worlds | Learned structures | Modes | Bridges | Handlers | Sem cases | R_test (per 100 lines) | R_world |
|---|---|---|---|---|---|---|---|---|---|---|---|
| TNN-1 (0323b97d5) | 1088 total source (cognition classification pending) | 35/35 (15 CLA-2 + 6 ACT compact + 10 COMP-1 + 2 CAM-1 + 1 DEVINT compact + 1 XCAP) | not run | inherits CLA-2/COMP-1/ACT structures; plan-to-guide cross-capability edge in XCAP | 0 | 0 | 0 | 0 | 3.22 | pending |
| MUL-1 (fbf14f73a) | 563 total source (cognition classification pending) | 5/5 P-MUL | not run | 4-cell MUL PROC (learner-constructed via 4297 rejected trials) | 0 | 0 | 0 | 0 | 0.89 | pending |

Notes:
- TNN-1 line count is 1088 measured via wc on tnn1.zag. The build
  report states 1090; both are under the 1200-line F-INT1 ceiling.
  Cognition-line classification per MEASUREMENT_PROCEDURE.md is an open
  item (see below). R_test uses total source lines until classified.
- TNN-1 carries a compact 6-test ACT battery (A1-A6, directional bid),
  not the standalone ACT 24/24 suite. The integration prereg target row
  above specified "ACT 24"; the builder delivered 6 compact tests. This
  deviation is recorded, not hidden. The 35-test total is 15+6+10+2+1+1.
- MUL-1 line count is 563 measured via wc on mul1.zag. The 5 P-MUL
  tests are construction tests (learner builds MUL from ADD/EQ/branch),
  not capability checks, so R_test is not comparable to capability
  batteries. Listed for completeness.
- Inquiry build (396ecafa4, 936-line inquiry.zag, 115 cognition lines
  claimed) is PROCESS-FAIL per the Worker Toolchain Guard: the builder
  self-disclosed one python3 invocation (text-patching a /tmp scratch
  copy, deleted without execution). No scientific standing until a clean
  re-freeze lands. Not counted in any ratio.

## Trajectory reading update (2026-09-30, post-integration)

1. **Lines:** first genuine compression. Pre-integration total ~1555
   cognition lines (1255 measured + ~300 COMP-1 estimate) across four
   separate builds. TNN-1 is 1088 total source lines in one binary,
   roughly 30 percent smaller, while passing 35 tests spanning five
   formerly separate capability families plus one cross-capability
   interaction test. Cognition-line classification is still pending, so
   this is a source-line comparison, not yet a cognition-line one.
2. **One-System metrics:** still zero. TNN-1 reports 0 modes, 0 bridges,
   0 handlers, 0 semantic cases. The CAM-1 eval_body menu is deleted,
   not ported. MUL-1 adds no arithmetic op to the core. The red teams
   (TNN-1, MUL-1, COMP-1) are in flight to verify these zeros
   independently.
3. **Learner-created structure:** positive and deepening. TNN-1 inherits
   the CLA-2/COMP-1/ACT structure inventory and adds a demonstrated
   cross-capability edge (query-miss plan becomes action guide through
   shared edges). MUL-1 adds a learner-constructed 4-cell executable
   procedure that beat the prereg's 6-cell sketch by discovering
   zero-init made INITs unnecessary. The learner is now building
   executable structure the researcher sketched less efficiently.
4. **Capability:** TNN-1 passes 35/35 in one process, byte-identical 3x.
   MUL-1 passes 5/5 P-MUL with oracle audit (correct not first, 72
   genuine rejections, shuffled rerun re-promotes). Cross-comparable
   capability (freeze worlds, then FW1-FW9) remains pending for every
   system including TNN-1. This is still the largest evidence gap.
   Micah's priority 5 (freeze rerun on the consolidated core) is the
   next canonical measurement.

## Open measurement items (updated 2026-09-30)

Prior items 1-5 remain open. Additions:

6. Formal cognition-line classification of tnn1.zag (1088 lines) per
   MEASUREMENT_PROCEDURE.md, to make the 1555-to-TNN-1 comparison a
   cognition-line comparison.
7. Formal cognition-line classification of mul1.zag (563 lines).
8. R_test recomputation for TNN-1 after item 6.
9. Sealed FW1-FW9 run on TNN-1: worlds passed, R_fw (the canonical
   number the integration was built to report).
10. Inquiry clean re-freeze: if it lands, add its row (115 claimed
    cognition lines, 300-line budget) and note the PROCESS-FAIL
    predecessor.

## Update protocol

- Append a new snapshot row after every builder landing, integration
  milestone, or sealed-world run.
- Fill the integration target row when the integrated build lands;
  move it to a dated snapshot row.
- Never edit a historical row. Corrections go in a dated note, as the
  correction above does.
- Commit this file with the owned path only, explicit pathspecs,
  contaminated-paper zero-diff verified.

## Snapshot update: cognition-line basis (2026-09-30, round 2)

Appended 2026-09-30 by the Compression Tracker Updater (round 2).
Historical rows above are untouched.

| Generation | Cognition lines | Self-tests | Freeze worlds | Learned structures | Modes | Bridges | Handlers | Sem cases | R_test (per 100 cognition lines) | R_world |
|---|---|---|---|---|---|---|---|---|---|---|---|
| TNN-1 (0323b97d5, remeasured 6c40f4238) | 641 (53 functions) | 35/35 (ACT portion is 6-test compact, not full 24) | not run | GROUP, MAP, PLAN, STEP, COMB, COEFF node types as learner-authored structures | 0 | 0 | 0 | 0 | 5.46 | pending |
| Inquiry-1 clean re-freeze (18ed3331c) | 149 | 12 bars pass (P-INQ1..P-INQ5a/b/c, A1, A2, C1-C3) | not run | UNCERTAINTY and GUIDE nodes created by learner-side pieces (161/162 traces) | 0 | 0 | 0 | 0 | n/a (construction battery, not unit tests) | pending |

Notes:
- TNN-1 cognition breakdown per MEASUREMENT_PROCEDURE.md: 99 generic
  substrate (workspace primitives + EXECUTE ISA) + 102 retention/eviction
  + 144 teach/query/act path + 284 plan synthesis/composition + 12 init
  = 641. Excluded: INFRA 23, ACCESSOR 55, DRIVER 331 (35 tests + runner),
  38 non-function lines. 641 + 23 + 55 + 331 + 38 = 1088 total source.
- The cognition figure replaces the source-line R_test (3.22/100) with
  5.46/100. Open items 6-8 from the prior list are resolved by this
  remeasurement.
- **Process note on the remeasurement wave:** the remeasurement worker
  invoked python3 once for arithmetic sums (11th Python incident to
  date). All sums were re-verified via awk-only computation and the
  committed numbers are the awk-verified ones. Per the literal Worker
  Toolchain Guard the wave is PROCESS-FAIL. Micah decides whether the
  awk-verified measurement stands or a fully clean re-do is required.
  The figures above carry that caveat.
- Inquiry-1 clean re-freeze (935-line inquire.zag, 149 cognition lines
  under the 300-line bound) passes all frozen bars with 3/3 byte-identical
  runs and zero Python (restricted safebin PATH). It supersedes the
  PROCESS-FAIL predecessor (396ecafa4); both remain on record. Inquiry
  is a separate binary, not yet integrated into TNN-1.

## Trajectory reading update (2026-09-30, cognition-line basis)

1. **Lines: the compression story strengthens.** On the source-line
   basis the prior reading said 1555 -> 1088 (about 30% smaller). On
   the cognition-line basis: the measured separate sum 1255 (CLA-2 685
   + CAM-1 408 + ACT 162) -> 641 is a 49% reduction; with the COMP-1
   ~300 estimate included (1555 -> 641) it is about 59%. Against the
   frozen core: 586 -> 641, a 55-line (+9.4%) increase. Those 55 lines
   buy: the unified structural workspace (CLA-2 port), the ACT
   action-selection path, COMP-1 plan synthesis and composition, the
   CAM-1 verify/contradict port, and the DEVINT curriculum driver.
   Five capability families for 9.4% more cognition lines than the
   frozen core.
2. **R_test on cognition basis.** TNN-1: 5.46/100. For reference on the
   same basis: ACT standalone 14.81/100 (24 tests / 162 lines), CLA-2
   2.19, CAM-1 1.47. ACT carries no workspace substrate of its own (it
   borrows the learner workspace), so its density is not directly
   comparable. TNN-1 carries the full substrate plus four capability
   ports. R_test remains provisional; test batteries differ.
3. **XCAP claim correction.** The F-INT4 disposition (86518edc4) narrowed
   the cross-capability claim: no MAP-to-guide registration mechanism
   exists in TNN-1. The honest claim is "contradiction demotes both
   query standing and action bid through shared edges on a MAP node";
   the prior reading's "query-miss plan becomes action guide" is
   corrected to this. F-INT4 the falsifier does not trigger (shared
   workspace is genuine); K5 is partially satisfied. Level 1
   strengthening (use the real MAP node, supported by the binary) is
   in flight.
4. **ACT coverage gap.** The coverage scout (4b36f0c1e) found TNN-1's
   6-test ACT battery covers only 3 of 16 standalone checks; 11 are
   uncovered (state-varying emission, decoy no-bleed, no-hallucination,
   retention negative half). The integration prereg required 24/24 with
   no test changes, so K4's P-INT2 is not literally satisfied. A
   remediation prereg is in flight. This does not change the
   cognition-line count (tests are driver lines, excluded from
   cognition), but it qualifies the 35/35 claim: the ACT portion is a
   6-test compact.
5. **Inquiry standing restored.** The clean re-freeze gives inquiry
   scientific standing after the PROCESS-FAIL predecessor. Uncertainty
   reification and guide construction both originate from learner state
   (Pieces A/B, process ids 161/162), with zero researcher-authored
   curiosity subsystem and zero domain/content branches (K-INQ2
   triple-verified).
6. **Largest evidence gap unchanged.** No freeze worlds and no sealed
   FW1-FW9 have run on TNN-1. R_world and R_fw are still pending for
   every system. Micah's priority 5 (freeze rerun on the consolidated
   core) remains the next canonical measurement; it is blocked on the
   five governance flags presented for Micah's rulings.

## Open measurement items (updated 2026-09-30, round 2)

- Items 6-8: resolved by 6c40f4238, subject to Micah's decision on the
  awk-verified numbers given the wave's PROCESS-FAIL.
- Item 10: inquiry re-freeze row added above (149 cognition lines).
- Still open: item 1 (COMP-1 cognition remeasurement to replace the
  ~300 estimate), item 7 (mul1.zag classification), item 9 (sealed
  FW1-FW9 on TNN-1, blocked on freeze governance), item 5 (fresh freeze
  rerun, blocked on Micah's five flags).

