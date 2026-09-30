# COMP-1 Builder: NAMECHECK (Step 0)

Date: 2026-09-30. Worker: COMP-1 Builder.
Task: Implement COMP-1 compositional machinery per frozen prereg 4f6f0c5c8.
Verdict label target: COMP1-BUILD-COMPLETE or COMP1-BUILD-FAIL.

## Step 0: Toolchain guard check (before any work)

- Ran `which python3 python`: `/usr/bin/python3` exists (system binary,
  cannot remove /usr/bin from PATH without breaking git/sh).
- Mitigation: created `~/workspace/comp1_safebin/` with `python3` and
  `python` stubs that print a BLOCKED message and exit 127.
  Prepended to PATH for all work in this wave.
- Verified: `which python3` resolves to the stub; invoking it exits 127
  with "BLOCKED: python3 is forbidden by the toolchain guard (COMP-1 wave)".
- Commitment: Zag only for all computational research operations.
  Shell only: invoke znc, run binaries, git ops, move/copy files.
- If a forbidden executable is invoked, this wave is PROCESS-FAIL.

## K1 ordering check

- Prereg commit 4f6f0c5c8 verified as ancestor of HEAD before any
  implementation work (git merge-base --is-ancestor). K1 HOLDS.

## Frozen inputs

- COMP-1 prereg: docs/lab/research-lead/overnight-20260928/composition_prereg/PREREG_COMP1.md (4f6f0c5c8)
- ISA boundary ruling: docs/lab/research-lead/overnight-20260928/architecture_rulings/ISA_BOUNDARY_RULING.md (0525377f3)
- Workspace format targeted: CLA-2 40-byte node layout (type_tag, ref[4], payload[4], valid)

## Owned path

- docs/lab/research-lead/overnight-20260928/comp1_build/
- Commit only this path with explicit pathspecs. Local only, no push.

## Constraints acknowledged

- No em dashes in any file (shell byte grep before commit).
- Contaminated paper TNN_RESEARCH_PAPER_20260929.md: zero-diff verified before and after.
- No sealed FW1-FW9 files accessed at any step.
- No new core execution ops (F7). Template set exactly 3 (F5).
- Candidates only from subject-incident relations (F6).
- E-ruling: expected is post-hoc feedback only; e-ablation mandatory (F2).
- Bootstrap miss-policy source bound: 150 lines.
