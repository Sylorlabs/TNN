# AMENDMENT 1 to PREREG: F3 REVISE Simple-Baseline Comparison

Status: FROZEN. Committed alone before any baseline implementation file,
build script, binary, or run exists.

Parent: PREREG_REVISE_BASELINE.md (4786633c5).

## Correction

Section 2 of the parent prereg recorded an incorrect sha256 for the
S-CONJ2 world file. The hash 8668e4a9... was the sealed evaluator's
`sealed_gen.zag` build script hash, not the world file hash. The correct
hashes, verified against commit 1df8addec (the sealed-evaluation commit):

- S-CONJ2: revise_sealed/world_sconj2.zag
  sha256 64ba1097cb601a060c67e5857914d00ba8791623ea31ea20222e894b4327534c
- S-NEG2: revise_sealed/world_sneg2.zag
  sha256 545118a1fe9d30186930d16539c305bdf5197ee804c13f4c948ae4cecfb7735f

The world files themselves are unchanged and are the sealed-evaluation
files from 1df8addec. Only the recorded hashes are corrected.

## Governance note

This amendment was written before any baseline .zag file was (re)created,
before any build, and before any run. The incorrect-hash prereg (4786633c5)
never governed an execution: no build or run occurred under it. The K1
commit-order check for step 5 uses this amendment commit: it strictly
precedes every baseline implementation file, build script, binary, and
run. The error is disclosed here rather than silently fixed.
