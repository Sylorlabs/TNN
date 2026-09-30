# NAMECHECK: ACT Builder (resumed with amended specs)

Date: 2026-09-30. Worker: ACT Builder (resumed lane).
Status: Step 0, written before any implementation work.

## Step 0: Toolchain guard (mandatory)

Guard check executed 2026-09-30 before any work:
- `which python3 python` returned `/usr/bin/python3`.
- The system interpreter cannot be removed from PATH (system
  binary, no permission to alter). Documenting non-use instead:
  this worker will not invoke python3, python, or any other
  forbidden interpreter at any step.
- Allowed toolchain: Zag (via pinned
  `src/tools/toolchain/znc_linux_x86_64_abed8aa1`), shell for
  orchestration only (invoke znc, run binaries, git ops,
  move/copy files).
- If a forbidden executable is invoked, this wave is
  PROCESS-FAIL per the governance ruling.

Guard check recorded. No Python invoked at Step 0.

## Standing rules honored

- Pure Zag for all computational research logic.
- Shell only for orchestration.
- No em dashes in loop documentation (verified by byte check
  at commit time).
- Contaminated paper
  `docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md`
  verified zero-diff before and after.
- Commits local only, explicit pathspecs, owned path only.
- Do not access sealed FW1-FW9 world files.

## Frozen specs governing this build

- ACT prereg: `learner_act/PREREG_ACT.md` (51a818141).
- Integration amendments A1-A12: `integration_coord/INTEGRATION_SPEC.md`
  (62e5ebb9f), APPROVED. ACT-relevant: A3 (evidence-bid
  selection), A4 (POLICY_ROOT register + context ring),
  A8 (utility remap to evidence edges), A11 (signed bid),
  A12 (reserved node addresses 0/1, WRITE to set).
- ISA boundary ruling: `architecture_rulings/ISA_BOUNDARY_RULING.md`
  (0525377f3). {EQ, ADD} approved as ISA primitives. No
  regularity detectors in core. Finite-difference OUT.

## Prior lane state

A prior builder started this lane and was paused before any
commit landed in act_build/. The directory was empty at
resume. This worker starts clean.
