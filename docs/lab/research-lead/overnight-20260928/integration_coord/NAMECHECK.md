# Architecture Integration Coordinator: Step 0 Name-Check

Date: 2026-09-30. Worker: Architecture Integration Coordinator.
Status: starting integration compatibility verification.

## Standing rules identified before any work

From LOOP_STATE.md and the coordinator template (519e6d5d1):

1. **Pure Zag rule:** everything in pure Zag. No Python, C, or other languages
   allowed. Shell may sequence processes and perform approved checks. Any
   Python invocation is a process failure.
2. **Contaminated paper:** `docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md`
   must never be edited, staged, committed, cited as canonical evidence, or
   treated as canonical. Zero diff before and after this work.
3. **No em dashes** in loop documentation.
4. **Frozen bars:** preregistration precedes implementation; never move or
   reinterpret a frozen bar after seeing results.
5. **Commit only owned paths** with explicit pathspecs.
6. **Micah's latest direction:** CLA-1/CLA-2 is the primary architecture
   direction. LORG ideas fold into the generic learner-owned workspace, not a
   separate memory engine. ACT is a hypothesis: generic operation consulting
   learner-created state, no planner/curiosity subsystem. CAM-1 must live
   inside the CLA event loop and workspace. Compose-ops must be minimal
   general structural operations, not one giant oracle.
7. **Coordination/verification only.** This lane writes no implementation code.
   Read-only monitoring of builder commits.
8. **Do not access sealed FW1-FW9 files** (evaluator/adversary assets, not
   design hints).

## Sealed files I will not open

`docs/lab/research-lead/overnight-20260928/freeze_worlds_v2/` beyond the
already-reviewed design metadata. No FW1-FW9 world files will be opened.

## Interface sources to read

- CLA-2 prereg: `continuing_learner/PREREG_CLA2.md` (commit 24351fd31)
- CAM-1 prereg: `construct_apply/PREREG_CAM1.md` (commit 68a41be8a)
- ACT prereg: `learner_act/PREREG_ACT.md` (commit 51a818141)
- Compose-ops spec: `compose_ops/COMPOSE_OPS_SPEC.md` (commit 881b17638)

## Verdict label

INTEGRATION-SPEC-COMPLETE on delivery of integration specification,
compatibility report, and commit.
