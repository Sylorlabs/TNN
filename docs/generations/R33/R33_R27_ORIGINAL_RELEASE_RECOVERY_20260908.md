# R33 original R27 release recovery — 2026-09-08

Status: **EXACT ORIGINAL RELEASE RECOVERED; STATIC CUSTODY VERIFIED; LEGACY CODE NOT EXECUTED; NATIVE MIGRATION/CONTINUITY STILL PENDING**.

This supersedes the earlier conclusion that the original `tnn-pre-v1-r27-general-learning` archive was unavailable. The earlier filesystem, reachable-Git and nested-backup searches were valid for their stated scopes. A timestamp-scoped ChatGPT Library metadata listing subsequently exposed the two original model-generated release archives.

This recovery is read-only provenance work, not a scientific experiment. No archived Python module, verifier, pickle, reducer, learner or historical runtime was executed. Inspection used archive listing, byte streaming, text inspection and hashing only. Canonical R27 was not mutated.

## Recovered Library artifacts

- `tnn-pre-v1-r27-general-learning.zip`
  - Library file id: `file_00000000c22c81fd8fe5078b89177907`
  - size: 56,777,645 bytes
  - Library creation time: `2026-08-20T21:43:59.098586Z`
  - observed whole-archive SHA256: `7042ff849743c9509586840df865f34423a92f9afc09ef2c7cf937b35b68b65e`
  - observed hash exactly matches the historical checksum record.
- `tnn-pre-v1-r27-general-learning.tar.gz`
  - Library file id: `file_00000000b60482309e96b03da442c8c7`
  - size: 56,544,266 bytes
  - Library creation time: `2026-08-20T21:44:01.163837Z`
  - not required for the present static source recovery after the ZIP matched its expected whole-archive identity.

The same Library creation window also contains the historical checksum and cleanroom records plus a standalone `r27-accepted-state.pkl`, R27 status/results/handoff documents and the historical category-holdout video.

## Archive identity and contents

The recovered ZIP contains 782 archive members under `tnn-pre-v1-r27-general-learning/`.

It includes the previously missing source chain:

- `src/r27_experiments.py`
- `src/r26_experiments.py`
- `src/r25_release.py`
- `src/r25_experiments.py`
- `src/r23_experiments.py`
- `src/r22_experiments.py`
- `src/r21_experiments.py`
- `src/r20_experiments.py`
- `src/r19_experiments.py`
- `src/r18_experiments.py`
- `src/r17_experiments.py`
- `src/r15_master_training.py`

It also includes the original verification closure:

- `scripts/verify_r27.py`
- `scripts/verify_r26.py`
- `scripts/verify_r25_lineage.py`
- `scripts/verify.py`
- `verification/r27-root-verification.json`
- `verification/r26-root-verification.json`
- `verification/VERIFICATION_SUMMARY.json`
- `verification/root_verify.log`
- `MANIFEST.sha256`
- `VERSION`

and original accepted-state lineage files including R27, R26, R25, R24 and R23 state artifacts.

## Canonical accepted-state identity

Streaming `state/r27-accepted-state.pkl` directly from the recovered ZIP produced SHA256:

`31e670fcd2a2fefc02a1d032b8016bd93c28844df8ea40889593d030a2096e5a`

That is the exact canonical R27 parent raw-byte SHA256 already carried by R33 custody records. The recovered source bundle therefore contains the same accepted parent bytes, not a similarly named reconstruction.

## Original semantic digest and verifier contract

The recovered `results/r27_summary.json` records:

- format: `R27_ASSEMBLY`
- semantic digest: `562aaaedb5b9ceec2f50482f631992c247cbe50e9f6d2321b811e311ecf73b04`
- development step: 60,423
- newborn restarts: 0
- retained R26 digest: `44d36746ffb9e8d46080376a6e26bb824772d9d4b5e429add404195d02888649`

The original `scripts/verify_r27.py` has 33 effective checks. Statically inspected checks include:

1. exact `R27State` type and release-format identity;
2. zero newborn restarts;
3. development step 60,423;
4. `R27State.digest()` equality to the recorded summary digest;
5. exact R26 accepted-state SHA linkage;
6. retained R26 digest equality;
7. specific-to-general and general-to-specific abstraction thresholds;
8. anonymous abstraction identifiers;
9. known partial/negative R27 proposals remain unpromoted;
10. eight policy gates remain locked;
11. exactly one active promotion, `STRONGER_MASTER_GENERAL_SPECIFIC_BRIDGE`;
12. release-manifest integrity when present; and
13. complete R26 lineage verifier success.

The bundled historical `verification/r27-root-verification.json` records a 33/33 PASS with:

- digest `562aaaedb5b9ceec2f50482f631992c247cbe50e9f6d2321b811e311ecf73b04`
- development step 60,423
- specific-to-general 0.9722222222222222
- general-to-specific 0.9444444444444444
- category best clean 0.7666666666666667
- no-VAD speech 0.7111111111111111
- VAD speech 0.7402777777777779

That is historical original-release evidence, not newly rerun evidence.

## Recovered `R27State.digest()` definition

The semantic-digest algorithm is no longer unknown. The recovered source constructs SHA256 over the following ordered material:

1. `format` bytes;
2. `r26_sha256` bytes;
3. decimal `development_step` bytes;
4. `base_state.digest()` bytes;
5. sorted state-dictionary key names plus raw tensor bytes for any active category head, entity head and affordance model;
6. sorted semantic-specialist identifiers when specialists exist;
7. `json.dumps(architecture, sort_keys=True, default=str)` bytes; and
8. `json.dumps(evidence, sort_keys=True, default=str)` bytes.

The verifier additionally binds the retained R26 digest and exact R26 state SHA linkage. Deeper lineage digest implementations are present in the recovered source chain and can now be mapped prospectively into a native continuity specification.

## Selected exact original-manifest hashes

| File | SHA256 |
| --- | --- |
| `src/r27_experiments.py` | `121b4684f24b19701c4badbea330f927088a8314c2bccc37894d87d0b6bed80a` |
| `scripts/verify_r27.py` | `496be360d4bfa40b5badf3414b73b617f55d0dfd88bed97817c27bab61965baa` |
| `src/r26_experiments.py` | `1e87721a93666155aabc67016ccd9416684c00f1e3c02da57f2c712083fc444d` |
| `src/r25_experiments.py` | `c8c40fbdeba5c9e8067bf83499f7c6c581c8c2234988c875a41f25e69b30b880` |
| `src/r25_release.py` | `41f32d0fd2c94c8dec28d516bd2caeecdda8a868f76e8c08558a5e04d5473a57` |
| `src/r23_experiments.py` | `517eb325096d5ae71ebb3bf659da77eac4266129136b888b469a99e366d4b642` |
| `src/r22_experiments.py` | `6353c131e37d7bc07924cb5c765f1aa09ae31b03ef20e8cb79647ab25fc2013a` |
| `src/r21_experiments.py` | `70c26d694fefbb86f9901f7a17704f86ff35cd1747617f778e05352d75d4027a` |
| `src/r20_experiments.py` | `7ac585ef9f9fde034cc624a16252b57550944dcaf0f7e10caa0f66ee3f4630b3` |
| `src/r19_experiments.py` | `6f0524b5a9e9d519f013123fe8a670daff0f542c2c4625a89f653568b66023be` |
| `src/r18_experiments.py` | `d359ef1dfae7d9e8531d6e25264faaef2c18a51ddd0dc33877e0d5c617e9dd9a` |
| `src/r17_experiments.py` | `0ae7e084e2b63848259802ac7ded5f260de4bde7c48ea7d6fce28d7f264bd1ab` |
| `src/r15_master_training.py` | `15b6af6abd2264159f5f8006c7efffb7b7c605211f7d8a3b42c66caabe36defe` |
| `results/r27_summary.json` | `2c55d6665f8641298f5bfd93b723dbde467252c95b6b41599dbe62d4b2decfe2` |
| `state/r27-accepted-policy.json` | `983db6a9c771f4952392d288459d65dfb04c33a7cbca37ac9f10a4365c7887a8` |
| `state/r27-accepted-state.pkl` | `31e670fcd2a2fefc02a1d032b8016bd93c28844df8ea40889593d030a2096e5a` |

## Runtime-closure status

The source archive contains CPython 3.13 bytecode-cache names, and recovered source contains historical `/opt/pyvenv/lib64/python3.13/site-packages/...` sample-data paths. The R27 source imports libraries including `cv2`, `numpy`, `torch` and `skimage`. No standalone exact requirements/lock/environment artifact was identified in the static archive listing.

Therefore the original **source, accepted parent bytes, source lineage, digest algorithm, verifier source, verifier receipt and manifest are recovered**, while exact external package/runtime provenance is not yet independently reconstructed.

R33's native-only contract also means the historical Python verifier cannot simply be rerun as a new scientific evaluator. It remains immutable historical evidence.

## Consequence for R33

The old blocker statement “original R27 source/digest/verifier unavailable” is obsolete.

The remaining parent-continuity work is narrower:

1. preserve this recovered release identity as immutable historical evidence;
2. independently review and map the recovered digest and 33-check verifier semantics;
3. implement a distinct native-Zag R27 continuity reader/verifier against the already-custodied canonical parent bytes without executing legacy Python;
4. demonstrate native reproduction of the canonical R27 step/restart/digest and required verifier invariants under a frozen, independently reviewed continuity protocol; and
5. only after that native continuity gate passes, create an R27-continuous experimental descendant and test the already-qualified N16 support-routing mechanism under a new identity and fresh evidence.

Until native continuity qualification passes, canonical R27 remains step 60,423 with zero newborn restarts, canonical mutation=false, learner authority=false and promotion=false.

The dominant blocker has changed from **missing original source/digest/verifier** to **native migration/behavioral-continuity qualification**, with exact historical runtime/dependency reconstruction remaining a secondary provenance gap.
