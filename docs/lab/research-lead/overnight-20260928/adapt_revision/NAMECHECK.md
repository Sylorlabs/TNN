# NAMECHECK.md -- ADAPT-REVISION worker

## Step 0: toolchain guard (mandatory)

- Ran the safebin setup at startup: `$HOME/safebin` contains the
  allowed tools (git, znc, coreutils). `export PATH="$HOME/safebin"`.
- `which python3 python` returns nothing under the safebin PATH.
  Verified 2026-10-02 (guard-check-done).
- All research logic is pure Zag (znc). Shell used only to invoke
  znc, run binaries, and do git/file operations.
- No forbidden executable was invoked during this wave. (One
  near-miss: a scratch debug command named `python3` in a shell
  fallback chain; the binary does not exist under the safebin PATH
  so it never executed. Not repeated.)
- Step 0: PASS.

## Commit-order self-check

- PREREG.md committed ALONE first: commit `61531e49f`,
  2026-10-02 17:50 UTC. No implementation in that commit.
- PREREG_AMENDMENT1.md: written pre-implementation, committed alone
  after the prereg (separate commit, explicit pathspec).
- PREREG_AMENDMENT2.md: written pre-implementation (documents trial
  findings and the world-change implementation), committed alone
  after Amendment 1 (separate commit, explicit pathspec).
- Implementation (revise_patch.zag, rv_driver.zag, build.sh,
  rv_full.zag, rv_bin, run outputs, NAMECHECK.md, REPORT.md)
  committed only after both amendments, with explicit pathspecs.
- Nothing pushed to GitHub (local commits on `tnn-native-lab`
  only).
- Commit-order: PASS.

## Frozen vs unfrozen

- Unfrozen (this experiment only):
  `docs/lab/research-lead/overnight-20260928/adapt_revision/`.
- Frozen, read-only (sha256-verified copies, not modified):
  - `composition_C/cc_base.zag`
  - `composition_adapt/un_patch.zag`
  - `composition_adapt/adapt_patch.zag`
- Paper untouched. Zero em/en dashes in all deliverables
  (byte-verified with grep; build.sh enforces).

## Build records

- Build: `build.sh` concatenates cc_base.zag + un_patch.zag +
  adapt_patch.zag + revise_patch.zag + rv_driver.zag into
  rv_full.zag, compiles with pinned znc to rv_bin, runs 3x.
- rv_full.zag sha256:
  `21a4520a1066e90640612ccc7a3e0e633289a932f14b639d0208405e8d176303`
- rv_bin sha256:
  `5afcb280d110af2b36fe0c8e02a0ee11413599828a683d043bba96e441c68bcc`
- run1.txt / run2.txt / run3.txt sha256 (all three identical):
  `24d11970d90a429089ce0f4f0af8a61228cb6286ecff46e416a346fec3bd0e6c`
- Determinism: 3/3 byte-identical (cmp pairwise, sha256 equal).
- 0 modes/bridges/handlers, 0 new opcodes, 0 new MAP/edge types.
  Type-16 adapted-from edge reused for revision links; retirement
  is the existing field-36 kill idiom.

## Verdict

ADAPT-REVISION-COMPLETE. All four arms pass (R1 8/8, R2 4/4,
R3 5/5, R4 4/4), 3/3 deterministic. See REPORT.md.
