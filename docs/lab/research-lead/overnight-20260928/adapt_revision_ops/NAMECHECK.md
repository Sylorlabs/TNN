# NAMECHECK.md -- ADAPT-REVISION-OPS worker

## Step 0: toolchain guard (mandatory)

- Ran the safebin setup at startup: `$HOME/safebin` contains the
  allowed tools (git, znc, coreutils). `export PATH="$HOME/safebin"`.
- `which python3 python` returns nothing under the safebin PATH.
  Verified 2026-10-02 (guard-check-done).
- All research logic is pure Zag (znc). Shell used only to invoke
  znc, run binaries, and do git/file operations.
- No forbidden executable was invoked during this wave.
- Step 0: PASS.

## Commit-order self-check

- PREREG.md committed ALONE first: commit `17b4161f1`,
  2026-10-02. No implementation in that commit.
- PREREG_AMENDMENT1.md committed ALONE: commit `c77301b86`,
  2026-10-02, pre-implementation.
- PREREG_AMENDMENT2.md committed ALONE: commit `599427055`,
  2026-10-02, pre-implementation.
- PREREG_AMENDMENT3.md committed ALONE: commit `84d7852a8`,
  2026-10-02, pre-implementation.
- Implementation (ts_patch.zag, ts_driver.zag, build.sh,
  ts_full.zag, ts_bin, run outputs, NAMECHECK.md, REPORT.md,
  frozen source copies) committed only after the prereg and all
  amendments, with explicit pathspecs.
- Nothing pushed to GitHub (local commits on `tnn-native-lab`
  only).
- Commit-order: PASS.

## Frozen vs unfrozen

- Unfrozen (this experiment only):
  `docs/lab/research-lead/overnight-20260928/adapt_revision_ops/`.
- Frozen, read-only (sha256-verified copies, not modified):
  - `composition_C/cc_base.zag`
  - `composition_adapt/un_patch.zag`
  - `composition_adapt/adapt_patch.zag`
  - `adapt_revision/revise_patch.zag`
- Paper untouched. Zero em/en dashes in all deliverables
  (byte-verified with grep; build.sh enforces).

## Build records

- Build: `build.sh` concatenates cc_base.zag + un_patch.zag +
  adapt_patch.zag + revise_patch.zag + ts_patch.zag +
  ts_driver.zag into ts_full.zag, compiles with pinned znc to
  ts_bin, runs 3x.
- ts_full.zag sha256:
  `63a8ec76f06b8b1bd8ac35c874e333c7fa9a3d4bb04a8f60ae4723e8dc0e000b`
- ts_bin sha256:
  `7fe5ec29d2c17a22e93dd7282b80f51511292645ca5df5e6e9d800e31554ee3f`
- run1.txt / run2.txt / run3.txt sha256:
  `4ec8a13327db894824dacc2202b4266b585df9ad686be3c52f4d43d18e23fe37`
  (all three identical).
- Determinism: 3/3 byte-identical (cmp pairwise, sha256 equal).
- Frozen-source integrity (K-H2): all four copies byte-identical
  to originals (sha256 verified in build.sh output).
- 0 modes/bridges/handlers, 0 new opcodes, 0 new MAP/edge types.
  Type-16 adapted-from edge reused for revision links; retirement
  is the existing field-36 kill idiom. Adaptation kind is
  recorded in MAP field 12 (2=TRUNCATE, 3=SPECIALIZE) per
  Amendment 1.

## Verdict

ADAPT-REVISION-OPS-COMPLETE. See REPORT.md for results.
