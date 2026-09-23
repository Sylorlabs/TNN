# W2 BEFORE / AFTER record — dirty3_uninit

**Question:** does heap pre-dirtying defeat the zeroed-page hiding of
uninitialized reads (v3 amendment item 6)?

## BEFORE — literal item-6 recipe (reproduces W2)

- Build: `replay_driver_zeroing.zag` + the **real** zeroing substrate
  (`R33_NATIVE_IO_V1.zag`, sha256
  `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8`)
  + naive pre-dirty phase (64 × 4 KiB `nio_alloc`, garbage-filled, half
  freed) before the trial runs.
- Result: **8/8 runs byte-identical**
  (`33391cfc6dba0f46a24ef63f7ef0ed3d5fda17caae2f9837648eb718c053fb55`).
  Full per-run hashes in `dirty3_uninit.evidence.txt` (`before_run_0..7`).
- **Conclusion:** the literal "allocate-and-fill garbage before the trial
  binary runs" recipe does NOT defeat the hiding, because the trial's own
  `nio_alloc` unconditionally re-zeroes (substrate lines 19–25). K1-style
  replay "passes" for the wrong reason — exactly the W2 failure.

## AFTER — adversarial-fill substrate (the implemented W2 fix)

- Build: `replay_driver.zag` + adversarial substrate copies
  (`adv_substrate_r0..r7.zag`, template sha256
  `eb801d7ed210095844bbb4895069a173873fe2bcf2bb16c4a323d762d7e8333d`;
  per-copy hashes in `evidence/build.log`) — `nio_alloc` fills with the
  deterministic per-run-tag pattern instead of zeroing — + §3 raw-malloc
  pre-dirty phase.
- Result: **8/8 runs pairwise divergent**; first differing pair (0,1),
  first differing byte offset 1 (the hex of the uninit-read byte `s[3]`).
  Determinism control matches (the tag-baked binary is deterministic per
  se — the divergence comes from the tag-varying fill, not flakiness).
  Full per-run hashes in `dirty3_uninit.evidence.txt` (`run_0..7`).
- **Conclusion:** the zeroed-page hiding is defeated. A program that never
  reads uninitialized memory cannot observe the fill (clean module proves
  it: `variation.evidence.txt`, PASS byte-identical across all 8 runs with
  adversarial conditions active).

## Note on the deviation

The v3 amendment's item 6 assumed an allocator whose pages could be left
dirty. The vendored allocator zeroes unconditionally, so the *intent*
(expose uninit reads to replay) is implemented via the adversarial-fill
substrate variant rather than the letter (pre-run allocate-and-fill).
Proposed as Item C.3 of `AMENDMENT_2026-09-20_REPLAY_BAR.md` for Micah's
re-approval; the clean-module PASS is the empirical proof the substitution
is semantics-preserving for programs without uninit reads.
