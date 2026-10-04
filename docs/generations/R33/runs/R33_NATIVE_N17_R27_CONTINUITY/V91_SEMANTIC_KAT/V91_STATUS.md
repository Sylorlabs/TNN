# V91 native historical generator recovery — 2026-09-17

V91 historical evaluation generator reconstruction is now closed for the two
paths exercised by the recovered R23 experiment: naive n=1 generation and
semantic roundtrip n=128 generation/reranking. Qualification remains
fail-closed for broader N17 continuity and authority.

## Exact historical inputs recovered

Read-only recovery directory:

`recovery_exact_20260917/`

- `r23_experiments.py`
  - 63,069 bytes
  - SHA-256 `517eb325096d5ae71ebb3bf659da77eac4266129136b888b469a99e366d4b642`
- historical R23 accepted state
  - 7,028,883 bytes
  - SHA-256 `fc24881f104052c09a4cb6e596b01ae5c107d9ae0356c8799ec97eff3edf440b`
- historical R23 summary
  - 29,242 bytes
  - SHA-256 `74cdb944e1037e92100d0dee2eca6ffaebcabe53346bb114c4bd09b035e3a495`

Historical Python is treated only as inert source specification. It is never
executed in qualification.

## Dataset/order recovery

The earlier split mismatch was caused by Zag `u64` arithmetic behavior:
high-bit right shift and modulo were signed. Explicit logical-shift and
unsigned-modulo handling corrected the historical personalized BLAKE2 path.

Qualified reconstruction:

- raw train rows: 3,626
- raw test rows: 622
- intended historical rows matched: 16/16
- failures: 0
- condition frame SHA-256:
  `d427ce14e1a1ccd12b7f5e09f2d385a557b37ffd425539e68473e6ecc4be6db2`

Frozen evidence:

`evidence/RECOVERY_EXACT_DATASET_20260918T043836Z`

## Naive n=1 generator parity

Pure-Zag reconstruction covers retained tensor loading, BPE decode,
42-dimensional condition projection, float32-equivalent rounding points, GRU,
top-k=7, softmax, Torch seeded multinomial behavior, BOS/EOS handling and
historical max length.

All 16 historical naive outputs match exactly:

- `V91_NATIVE_ORACLE_MATCHES,16`
- `V91_NATIVE_ORACLE_FAILURES,0`

Generated frame SHA-256:

`c7d58028a88613ba5274b776653cc03d7c2976c03be7270994226b0bc9d132f3`

Frozen evidence:

`evidence/RECOVERY_EXACT_NATIVE_GENERATOR_20260918T045549Z`

The inference closure has no oracle/custody import. Oracle comparison occurs
only after the generated artifact exists.

## Semantic roundtrip n=128 parity

The remaining historical path has now been reconstructed in pure Zag:

1. generate 128 candidates with seed `33101 + row_index`
2. reproduce batched seeded top-k multinomial sampling
3. retain cumulative model log probability
4. decode BPE candidate strings
5. reproduce `raw_hash(text, 768)` using personalized BLAKE2b-64
6. apply retained `interpreter.W` (768 x 42)
7. reproduce semantic MSE, length penalty and historical combined score
8. select the best candidate
9. create the inference artifact before opening historical roundtrip custody

Frozen qualification:

`evidence/RECOVERY_EXACT_ROUNDTRIP_20260918T051756Z`

Results:

- actual native roundtrip outputs: 16
- exact historical oracle matches: 16/16
- oracle failures: 0
- deterministic repeat: byte-identical
- roundtrip parity: true
- historical evaluation generator parity: true
- inference oracle import: false
- historical Python executed: false
- foreign ML runtime used: false

Artifact identities:

- generated roundtrip frame:
  `3a2f4075ad758f9481bdc6f6f5cff75dc044b0a69e3ee14e6280c3f309d253f5`
- post-inference roundtrip oracle frame:
  `fba38cd8fc63a63d6167ce4e39263d458582ec4164da2d7ca927adfc91733f82`
- condition frame:
  `d427ce14e1a1ccd12b7f5e09f2d385a557b37ffd425539e68473e6ecc4be6db2`

The evidence directory includes source projections, compiler/build records,
per-row worker artifacts, repeat inference, command journal, canonical
before/after hashes, SHA256SUMS and a complete verification pass.

## Retained model custody

The retained model/BPE/interpreter inputs remain byte-bound to the historical
R23 material.

- BPE frame SHA-256:
  `f83d2f7c63b2f40f386c37b96fc5d17ea120f715e503f58b62a6ca428cd21f6c`
- interpreter W:
  - shape 768 x 42
  - 129,024 float32 bytes
  - SHA-256 `3f5c806cfa243f9fc5de398101d93a9fc59b8ea1d4cb55cbe08165d940e3e5c3`

All 11 retained model tensor files, BPE frame and interpreter bytes were
previously shown byte-equal between nested historical R23 and retained R27
custody.

## Canonical and authority boundary

Canonical R27 is unchanged before and after roundtrip qualification:

- state SHA-256:
  `31e670fcd2a2fefc02a1d032b8016bd93c28844df8ea40889593d030a2096e5a`
- policy SHA-256:
  `983db6a9c771f4952392d288459d65dfb04c33a7cbca37ac9f10a4365c7887a8`

No learning authority, successor promotion, canonical mutation or foreign ML
runtime is admitted. The V91 historical reconstruction is closed, while the
overall N17/full-continuity gate remains closed pending the remaining historical
R25/R26 work and later independent review.

## Next frontier

The next ordered workstream is exact R25/R26 member/hash recovery:

- exact R25 accepted state, policy, manifest and required source members
- exact R26 accepted state, policy, source and release/video/smoke dependencies
- native mapping only after exact bytes and source semantics are admitted

Do not substitute shadow/similarly named artifacts for exact historical release
members.
