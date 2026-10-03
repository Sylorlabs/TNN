# NAMECHECK: Weak K-LT-5 Adversary

## Step 0: Toolchain Guard

Date: 2026-10-01.
Scope: **ADVERSARY ONLY.** Design and seal the weak K-LT-5 world. No implementation, no test execution, no frozen source modification.

Toolchain verification performed at task start:
- Created `$HOME/safebin` with symlinks to allowed tools (git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat, grep, sed, awk, wc, cmp, sha256sum, etc.).
- Exported `PATH="$HOME/safebin"`.
- Ran `which python3 python`: returned nothing (no output before "guard-check-done").
- Result: **PASS.** No forbidden executables in PATH. Zero Python invocations.

This worker performs adversary world design and sealing only. The world generator is pure Zag via the pinned znc. Shell use is limited to: invoking znc, running binaries, git operations, moving/copying files.

## Independence Declaration

This worker did NOT build H3-lite Node 1. The Node 1 implementation (`45c55ed83`) was built by a separate worker. This worker's role is strictly adversarial: design a world that discriminates (satisfies prereg R1-R5) without biasing toward pass or fail.

The world is designed from the frozen prereg requirements and the frozen source mechanics, not from knowledge of the Node 1 implementation's internals beyond the public prereg specification.

## Input Provenance

Read-only inputs:
- `weak_klt5/WEAK_KLT5_PREREG.md` (FROZEN): R1-R5 sealed world requirements, E-ratio definition, predicted trajectories.
- `weak_klt5/NAMECHECK.md`: Design worker's toolchain record.
- `h3lite_node1/H3LITE_NODE1.md`: Family ids, initial order, mechanism description (public).
- `h3lite_node1/h3n1_base.zag` (frozen copy): Assembler mechanics, verification logic, gating (read-only).
- `h3lite_node1/h3n1_funcs.zag`: Dispatch order, family attempt structure (read-only).

No sealed worlds opened (this IS the sealed world being created). Frozen source not modified. The test is NOT run by this worker.

## Constraints Honored

- Adversary ONLY. No test execution.
- Frozen prereg not modified.
- Zero em dashes (byte-verified before commit).
- Paper untouched.
- Nothing pushed (local commit only).
- Sealed world hashed; design doc does not reveal the full fact list.

## Deliverables

- `NAMECHECK.md` (this file)
- `WORLD_DESIGN.md` (design rationale, sealing method, hashes; NO sealed fact list)
- `world_gen.zag` (pure Zag generator)
- `world_sealed.txt` (sealed world data, SHA-256 committed)
- `world_bin` (compiled generator, for reproducibility)

## Verdict

**ADVERSARY-COMPLETE** (pending parent acknowledgment of commit).
