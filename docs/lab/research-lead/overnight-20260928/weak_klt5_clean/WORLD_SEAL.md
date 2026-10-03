# Weak K-LT-5 Clean World Seal

Date sealed: 2026-10-01.
Generator: `world_gen.zag` (pure Zag, pinned znc).
Sealed file: `world_sealed.txt`.

## Seal

SHA-256: `0971e9469a7deda9ae5fa7347064d46e89006b252fe1f22dd2454daa6b23f3a6`

This hash was recorded BEFORE any evaluation binary was built or run against
the world. The world file is frozen as of the seal commit. Any modification
invalidates the seal.

## Structural verification (R1-R5, no contents reproduced)

- Line count: 109 (7 header, 1 SETUP, 80 TEACH, 20 PROBE, 1 END).
- R1 (bias): All TEACH chain values are in 6005-6084 (verified: minimum chain
  value 6005 > 4). No chain value equals the expected answer 4, so families
  0,1,2,3,5 cannot verify successfully. Family 4 (count) assembles 4 increments
  from the 5-node chain and verifies 4 = expected.
- R2 (distinct subjects): 20 PROBE subjects are 3001-3020, all distinct.
  Verified by counting unique subject ids: 20.
- R3 (same relation): All 20 PROBE lines use relation 50. Verified.
- R4 (no direct answers): All 80 TEACH lines use relation 51. Zero TEACH lines
  use relation 50. Verified by grep: 0 lines match `^TEACH [0-9]+ 50 `.
- R5 (verifiability): Expected answer 4 on all 20 PROBE lines, flags 0.
  The count family produces exactly 4 (4 chain links).

## Phase assignment

- Phase A: probes 1-10 (subjects 3001-3010).
- Phase B: probes 11-20 (subjects 3011-3020).

## Independence note

This world was designed by the evaluator (this worker) to the fresh prereg's
functional requirements. It uses fresh subject and chain id ranges
(3001-3020, 6005-6084) with no overlap with the VOID world's ranges.
The sealed contents are not reproduced in any report; only this hash and the
structural R1-R5 verification above.
