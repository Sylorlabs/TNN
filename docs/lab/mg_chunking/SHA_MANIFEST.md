# SHA_MANIFEST.md — MG chunking promotion + learned policy (2026-09-26)

Fork origin: `1de59c334aea10907cdc34545c7a3e97a868c6d2` (short `1de59c334aea1`),
`mg_chunk.zag` byte-identical to the GitHub file at that commit.

## Frozen fork baseline

48fd1f4f60e1e92d44d8a6158cd52838ad3631b9a6105ec95d6eb16644d6bbb7  mg_chunk.zag
e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8  R33_NATIVE_IO_V1.zag
55e4e44daf243cd50e94a305de18acd1f8c58c3b514b082065476eeca7b89149  build.sh
de7d9c8a5c4ffac7c284e6496985d462eec41ee58ffd41e72fad45b16d7d2951  VERDICT.md
94fba9e3578d84402eeebf0ab3d09c814630a2b9635fd8ed1fcebd70bfe9c74f  evidence/RUN_R1.out
94fba9e3578d84402eeebf0ab3d09c814630a2b9635fd8ed1fcebd70bfe9c74f  evidence/RUN_R2.out

## Phase 1 — promotion (D live, C/W/S retired to negative controls)

86a2d38890793dd083fb97c199dc0ca06066c86936da6e34cf9fae0e3da7adaa  intake.zag
7dc0c567c22a3c6159f0135239ea9b837d440fa0a2448fee0fccf5b4dfbcd37b  controls.zag
2291e3a7cb191bb8405f7adcc998974e65d6f6faf9eacf6d576696d41420e8f4  build_promotion.sh
045be875fd8b57141af0ca6407af11b426cd9bcee7de15145df0f72767bbdb95  PROMOTION_VERDICT.md
25563035cdf8b1d9de0dd571445533edb7a3e1645d5a09ec54e94b4bf044d69e  evidence_promotion/RUN_P1.out
25563035cdf8b1d9de0dd571445533edb7a3e1645d5a09ec54e94b4bf044d69e  evidence_promotion/RUN_P2.out
5c9eea118441e93cf28bcadda101734c9fa36813acbabb9ab98a854652b1d23f  evidence_promotion/RUN_C1.out
5c9eea118441e93cf28bcadda101734c9fa36813acbabb9ab98a854652b1d23f  evidence_promotion/RUN_C2.out

Promotion: 24/24 correct, 24/24 native, 0 fallbacks, byte-identical reruns (PASS).
Controls reproduce the frozen baseline: C 23/24, W 24/24 (6 native), S 23/24 (2 native).

## Phase 2 — learned chunking policy (pure Zag, zero RNG)

ecd9175f69e39494a37c35156e00c5f4a13f065e8800ba905c29a7169e1967eb  learned_chunk.zag
4cc124687f12cb98dc14b11ba6b24f96e7ed9cb17bf566cd76569e186e34687b  LEARNED_VERDICT.md
47f1b1a2caa16c89b914ec2052432d3bee552904712329dcde3dde871c307587  evidence_learned/RUN_L1.out
47f1b1a2caa16c89b914ec2052432d3bee552904712329dcde3dde871c307587  evidence_learned/RUN_L2.out

Learned: 36/36 correct (24 old + 12 new traps), 36/36 native, 0 fallbacks,
byte-identical reruns (PASS). Toolchain: znc_linux_x86_64_abed8aa1.
