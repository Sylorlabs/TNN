# NAMECHECK: Revision Substrate Experimenter

## Step 0: Toolchain Guard (mandatory, recorded)

- Safebin activated: `$HOME/safebin` prepended to PATH.
- `which python3 python` returns nothing (verified 2026-10-01).
- Zero forbidden executables invoked. All computation in Zag via pinned `znc`.
- Shell used only for: invoking znc, running binaries, git operations, moving/copying files.

## Scope

- **UNFROZEN VARIANT ONLY.** This worker creates and modifies
  `docs/lab/research-lead/overnight-20260928/revision_substrate/tnn2_revision_variant.zag`.
- Frozen artifacts untouched: `tnn2.zag`, `tnn2_bin`, build `f4de7ff46`,
  `tnn2_reuse_variant.zag` (read as reference only, not modified).
- The frozen revision-corruption bug (`8b58c4104`) is NOT repaired in TNN-2.

## Input provenance

- Bug report: commit `8b58c4104` (`bug_report/REVISION_BUG.md`).
- Revision advice: commit `5a009ff87` (`revision_advice/REVISION_ADVICE.md`).
- Base variant: `reuse_experiment/tnn2_reuse_variant.zag` (commit `ea8fc0ac1`).
  Copied, then modified. SHA-256 of base recorded before modification.
- Boundary map: commit `8d763d766` (probe pE E1/E4 reference).

## Mission

Test copy-and-commit + MAP retargeting as a correctness architecture
experiment, per Micah's 2026-10-01 approval. No in-place mutation/revert.
Candidate repairs built in fresh cells, verified, then atomically committed.
This makes revision safe; it does NOT make repair form learner-authored.

## Constraints

- Do NOT claim SUF, L3, or learner-authored repair.
- This is correctness infrastructure, not a capability gain.
- Zero em dashes in all documents (byte-verified before commit).
- Paper untouched. Nothing pushed. Local commits only.
- Explicit pathspecs on all git operations. Owned path only.
