# TNN-1 F-INT4 Disposition

Date: 2026-09-30. Worker: TNN-1 F-INT4 Disposition.
Status: FINT4-DISPOSITION-COMPLETE (disposition only; no implementation).

## Source material

- Integration prereg F-INT4 and K5: commit `7fc7148ac`,
  `docs/lab/research-lead/overnight-20260928/integration_prereg/PREREG_INTEGRATION.md`
- TNN-1 build, `t_xcap` test: commit `0323b97d5`,
  `docs/lab/research-lead/overnight-20260928/tnn1_build/tnn1.zag` (lines 1024-1046)
- TNN-1 red team, Vector 1: commit `cbde38737`,
  `docs/lab/research-lead/overnight-20260928/tnn1_redteam/TNN1_REDTEAM_REPORT.md`

All three were read in full. The build was inspected read-only. No code was
modified.

## 1. What the prereg requires

F-INT4 (falsifier, prereg lines 362-371) requires the integrated system to
pass a cross-capability test with four linked properties:

1. A plan constructed for a query miss (COMP-1 path),
2. promoted as a MAP node (CAM-1 path),
3. later selected by ACT as an action guide through the same edges,
4. with a contradiction against the MAP node demoting both its query
   standing and its action candidacy.

If the mechanisms coexist but do not interact through shared state, "the
integration is four systems in a trench coat and the One-System claim fails."

K5 (positive bar, prereg lines 444-448) requires: "a query-miss plan becomes
an action guide through shared edges, and contradiction demotes both
candidacies. The mechanisms interact through shared state, not merely
coexist."

## 2. What the test actually does

`t_xcap` (tnn1.zag lines 1024-1046) has two disconnected parts:

Part 1 (lines 1026-1030): runs `ev_teach` x4 and `ev_query(W,101,40,201,0)`,
verifying the plan/MAP path returns 201. This exercises the query-miss to
plan to MAP-promotion path. The MAP node created by `promote_map` inside
`mp_run` is discarded; its node id is not captured and `mp_run` does not
return it.

Part 2 (lines 1031-1045): creates a synthetic guide node via `alloc_node`
with manually set fields mimicking a MAP node shape (type 20, relation 505,
promotion clock set to now, a USE self-loop to give it positive bid). The
code comment reads "create a guide node (simulating a MAP that guides
action)". Then `contradict_map` is applied and the test verifies
`map_standing < 0` and `bid < b0`.

The test never calls `ev_act`. It never shows the query's MAP being selected
as an action guide. The synthetic node is not the query's MAP node.

## 3. The exact gap

What the test proves: `map_standing` (the CAM-1 query-path metric) and `bid`
(the ACT action-path metric) are computed over shared edge state on a single
node, and a CONTRADICTS edge demotes both. This is metric co-location
through shared edges. It is real and it is cross-capability.

What the test does not prove: that a query-miss plan becomes an action
guide. Properties 1 and 2 of F-INT4 are exercised (in Part 1) but their
artifact is discarded. Property 3 (ACT selection of the MAP as a guide) is
never attempted. Property 4 (contradiction demoting both candidacies) is
demonstrated only on the synthetic node, not on the query's MAP.

The two parts of the test do not connect. Part 1 shows the plan path works.
Part 2 shows contradiction demotes two metrics on one node. Neither part
shows the plan's MAP flowing into action selection.

## 4. Can the existing binary support a stronger test?

Two levels of strengthening were considered.

Level 1 (supported by the existing binary): replace the synthetic node with
the real MAP node from `ev_query`. A test could run `ev_query` on a miss,
scan the workspace for the most recently created T_MAP node (type 20),
apply `contradict_map` to it, and verify both `map_standing` and `bid`
demote. This closes the "synthetic node" gap. The binary supports it because
`promote_map` creates a real node in the shared workspace and a test has
full access to internal state. No binary modification is needed.

Level 2 (not supported by the existing binary): the full "plan becomes
guide" claim. This would require the MAP node to be selected by `ev_act`.
Inspection of `ev_act` (tnn1.zag lines 691-733) shows candidates must be
connected to the POLICY_ROOT node (`pr = ng(W,0,20)`) and match the action
context. `promote_map` (lines 565-574) does not link the MAP node to the
policy root. `pol_set` (line 747) is called only in test scaffolding (lines
822, 831, 842, 874, 884, 889, 894, 902), never by any system function. There
is no MAP-to-guide registration mechanism anywhere in TNN-1.

A test could manually link the MAP node to the policy root and set the
context, then call `ev_act`. But that would be the test author performing
the integration, not the system demonstrating it. It would prove the test
harness can wire two subsystems together, which is exactly the "trench coat"
pattern F-INT4 is meant to rule out.

Conclusion: Level 1 strengthening is achievable with the existing binary.
Level 2 requires a design change (a registration mechanism by which promoted
MAP nodes become ACT candidates), which would need a new prereg, not a test
tweak.

## 5. Assessment against the frozen bars

F-INT4 (falsifier): does not trigger. The falsifier asks whether the
mechanisms interact through shared state or merely coexist. The test
demonstrates genuine shared-state interaction: one CONTRADICTS edge demotes
both the query-path standing metric and the action-path bid metric. The
workspace is genuinely shared (red team Vector 1 ATTACK-PASS on this point).
There is no trench coat at the state level.

K5 (positive bar): partially satisfied. The "contradiction demotes both
candidacies through shared edges" half holds. The "query-miss plan becomes
an action guide" half is not demonstrated. A literal reading of K5 is not
met by the current test.

## 6. Recommendation

Recommend option (b): narrow the claim, with Level 1 strengthening as a
supporting improvement.

Rationale:

- The prereg's F-INT4, read literally through K5, requires the system to
  perform plan-to-guide conversion. The current binary contains no mechanism
  for this. No test rewrite can demonstrate what the system does not do.
- The narrowed claim, "contradiction demotes both query standing and action
  bid through shared edges on a MAP node," is honestly supported by the test
  and remains a meaningful cross-capability property. It verifies that the
  CAM-1 contradiction mechanism and the ACT bid function operate on the
  same edge state, which is the "shared edges" half of the prereg's
  requirement.
- The "plan becomes guide" half should be explicitly marked as not
  demonstrated, not implied by the XCAP label.
- Level 1 strengthening (use the real MAP node from `ev_query` instead of
  the synthetic node) should be done regardless. It removes the
  "simulating" admission and tests the actual artifact of the query-miss
  path. The existing binary supports it without modification.
- If the full conversion is wanted, it requires: (1) a design for
  MAP-to-guide registration, (2) a new prereg, (3) implementation, (4) a
  genuine test. This is a capability addition under the One-System Rule, not
  a test adjustment. It should be proposed as new work, not smuggled into a
  test revision.

Note on the red team's suggested stronger test ("run ev_query (miss, plan,
promote), then ev_act in the same workspace, and verify the promoted MAP is
selected as the action guide"): this is the right test for the full claim,
but it cannot pass on the current binary without the test manually wiring
the MAP to the policy root. Manual wiring would invalidate the test's
discriminating power. The suggestion should be held for the registration
mechanism, if that work is approved.

## 7. Suggested claim language

Current (overstates): "F-INT4: cross-capability test (contradiction demotes
both standing and bid)" as evidence that "a query-miss plan becomes an
action guide through shared edges."

Narrowed (honest): "XCAP verifies shared-metric integration: a CONTRADICTS
edge against a MAP node demotes both its query-path standing
(`map_standing`) and its action-path candidacy (`bid`), demonstrating that
the CAM-1 and ACT subsystems read and write the same edge state on the same
node. Plan-to-guide conversion (ACT selecting a query-built MAP as a guide)
is not demonstrated in this build; no MAP-to-guide registration mechanism
exists."

## 8. Open items for the parent

- Whether to approve the Level 1 test strengthening (real MAP node) as a
  follow-up task. It needs no prereg change since it stays within the
  narrowed claim.
- Whether the MAP-to-guide registration mechanism is wanted as new
  capability work. If so, it needs a fresh prereg under the One-System
  Rule accounting (new learner-state structures, zero new modes/bridges).
- Whether K5 should be formally amended to the narrowed language, or held
  as partially satisfied pending the registration mechanism.

## Governance

- Zero Python invocations. Analysis and documentation only.
- No em dashes in this file (byte-verified before commit).
- Contaminated paper `TNN_RESEARCH_PAPER_20260929.md` zero-diff verified
  before and after.
- No sealed FW1-FW9 files accessed.
- TNN-1 build inspected read-only; not modified.
- Disposition only. No test implemented. No binary changed.
