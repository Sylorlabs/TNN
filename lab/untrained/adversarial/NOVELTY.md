# Novelty Audit: Adversarial Fixtures

Date: 2026-09-26
Method: Git blob IDs via `git hash-object`; repository-object lookup via
`git cat-file -e` against origin/tnn-native-lab (fetched 2026-09-26,
commit f67e989339a67b882f72378b39fad342a1aa6d9e).

Every fixture blob was checked. All 17 return "absent" (object not found
in the repository). The fixtures are novel: they were generated
2026-09-26 by fixtures/gen_adv.py (deterministic, zero-RNG) and have
never existed in the repository.

## Blob IDs (from SEAL_BLOBS.txt) and lookup results

| Fixture | Blob ID | In repo? |
|---|---|---|
| A1_faint_clicks.wav | f95673dc43ddcba3112b4b4c4c2c2238c92e9508 | absent |
| A2_wobble_am.wav | 35bbeadcd26d750fb4cd6824e9579bb933c938b3 | absent |
| A3_two_rhythms.wav | 51675f9e5d7fb05d5a8ae35207bd1ca26636db03 | absent |
| A4_inharmonic.wav | a9fd14ad5e31d963a06f097b4fce4c02f030c08f | absent |
| A5_slow_drift.wav | 0cd8db4763e718b3521ea26e94476718b746f06a | absent |
| I6_mid_texture.ppm | da6e55910ef294ee0e7546076b7a0e20e10cd36d | absent |
| I7_s_ridge.ppm | f9bff80ff0b8a4085bde40736e49520dfa4c6a84 | absent |
| I8_isotropic.ppm | 0e4e0d127d5b7914368b0158daa5fa2079fdddb5 | absent |
| I9_near_blank.ppm | df7257e105de9828d559e0e3d1694bec449de801 | absent |
| V10_conflict_f_001.ppm | 95dfe05715ccbf496c6e3076ae54989bf5336e46 | absent |
| V10_conflict_f_002.ppm | 4619554bd7e4831103f09ed7744b19ea92a5c831 | absent |
| V10_conflict_f_003.ppm | 030b15dad1bc93945c6be6d7dcc77ecd86898b57 | absent |
| V10_conflict_f_004.ppm | 4619554bd7e4831103f09ed7744b19ea92a5c831 | absent |
| V10_conflict_f_005.ppm | 95dfe05715ccbf496c6e3076ae54989bf5336e46 | absent |
| V10_conflict_f_006.ppm | 94338f7372453a224adedccf74b02a7d8c367517 | absent |
| V10_conflict_f_007.ppm | 3bd8d7a053be32eb463b999751d6a719e5467ea6 | absent |
| V10_conflict_f_008.ppm | 94338f7372453a224adedccf74b02a7d8c367517 | absent |

Note: V10 frames 1&5, 2&4, 6&8 are byte-identical by construction (the
triangle-wave pan revisits positions). This is expected and documented
in the generator.

## Conclusion
All fixtures are novel to the repository. The SHA-256 seal
(SEAL_SHA256.txt) commits the exact bytes; anyone can regenerate the
fixtures via fixtures/gen_adv.py and verify the hashes.
