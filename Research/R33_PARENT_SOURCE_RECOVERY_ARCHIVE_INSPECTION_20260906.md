# R33 parent-source recovery — nested archive inspection

> **Superseded for source-availability status on 2026-09-08.** A timestamp-scoped ChatGPT Library listing recovered the exact original `tnn-pre-v1-r27-general-learning.zip`; its SHA256 `7042ff849743c9509586840df865f34423a92f9afc09ef2c7cf937b35b68b65e` matches the historical checksum and its embedded accepted-state SHA256 matches canonical R27. The original source chain, semantic-digest implementation and 33-check verifier source are now recovered as inert historical evidence. See `Research/R33_R27_ORIGINAL_RELEASE_RECOVERY_20260908.md`. The negative findings below remain valid for the filesystem/nested-archive scope inspected on 2026-09-06.

Date: 2026-09-06. Status: **PARTIAL HISTORICAL PROVENANCE RECOVERED; ORIGINAL
R27 SOURCE/DIGEST/VERIFIER IMPLEMENTATION STILL NOT RECOVERED.**

This is read-only recovery work, not an experiment. Historical archive members
were listed or streamed as inert bytes/text. No recovered Python, Zag, pickle,
reducer, verifier, training code, or historical runtime was executed. Canonical
R27 state was not changed.

## Search scope

The previously identified full backup
`/Users/Shared/micah/Downloads/TNN_COMPLETE_R1_R32_FULL_BACKUP.tar.gz`
(SHA256 `f966c0c7f1649feb1e83436b21d7c51a41442e8a9f3f4f41c33f08affbb3d748`)
was inspected recursively by archive listing/streaming. This closes the earlier
recorded gap that archive contents had not yet been searched.

Nested archives inspected include:

| Nested archive | Exact nested-byte SHA256 |
| --- | --- |
| `TNN/Research/tnn-r27-native-master-shadow.tar.gz` | `5db800a6cc7c05ca052d1d32c51348229ad1b3cd2587402f715df7703d42797b` |
| `TNN/Research/tnn-pre-v1-r28-aeif-no-graph-shadow.tar.gz` | `060e44f8d9aeb1cf395744d13076e7e72044cf7533ab0a3158dad2cae56a412c` |
| `TNN/Research/tnn-r30-big-boom-shadow.tar.gz` | `fd890e453a42c665a42a1d55747e47bd4175d8209863900714c868c762087ffe` |
| `TNN/Research/tnn-r31-endogenous-chunking-shadow.tar.gz` | `dc350b4ff908bc725d8365dc35862465f20e9155786e665b4f99a3009ea0c7b1` |
| `TNN/Research/tnn-v1-current-execution.tar.gz` | `ed14c92315327b0388eb5d4820bf458f22ed2e5bd3813ed3f21b2c51d10ee362` |

The full backup also contains `.zip` companions and other historical bundles.
After the initial targeted R27-through-current inspection, every nested `.tar.gz`
and every nested `.zip` in the full backup was streamed/listed and searched for
the original R27 release name plus the complete known module-chain filenames.
That exhaustive nested-archive target-name pass returned no match for the original
`r27_experiments.py` dependency chain or `tnn-pre-v1-r27-general-learning`.

## Exact historical derivative evidence recovered

The R27 native-master shadow bundle is a later historical derivative package,
not the original accepted R27 Python source release. It nevertheless preserves
useful exact custody/provenance evidence:

- `verification/parent-r27-verifier.log`, SHA256
  `67a74e11090f57aa0084924735f096d6bdc55e7f7514da4ce078e01aff8be349`,
  reports PASS 33/33, digest
  `562aaaedb5b9ceec2f50482f631992c247cbe50e9f6d2321b811e311ecf73b04`,
  development step 60,423, and the same five recorded parent metrics.
- `state/state_bridge_manifest.json`, SHA256
  `d3deec13ee1cf921d32d7d7cc6cdfff04f67ae60af1d2caed0d4651024b899fb`,
  binds accepted parent raw SHA256
  `31e670fcd2a2fefc02a1d032b8016bd93c28844df8ea40889593d030a2096e5a`,
  step 60,423, zero newborn restarts, and expected accepted-state digest
  `562aaaed...3b04`.
- `verification/native-toolchain-status.json`, SHA256
  `852036779e5043d813664e1e9ff067a36c6626706c3137d40bd3db6fb2bd30bc`,
  records later Zag-native shadow toolchain provenance: `Sylorlabs/zag`
  release `v2026.06.0`, archive SHA256
  `addf6e99dd50fb2a69e5ab323bae0ec21195800bf38fc1d1bbce381debb2bc94`,
  later Zag-v2 commit `4b19a9c159bed58a45d18c15f36a78dd82870c57`, and
  `znc` blob `611b7f0c215385b7d3073bbebbf6078224c70b4c`.
- `verification/source_contract.py`, SHA256
  `f641633296b739dcc798d424dc27be36b3955d4fcfc1dad942f9a30a4b3df51f`,
  is a later static checker for the Zag shadow source. It is **not** the original
  R27 semantic-digest implementation or the original 33-check parent verifier.
- `src/tnn_r27_native_master.zag`, SHA256
  `79b19f3856d7505ba09286c237fb3afb1ec016283d78678f76a3382e2d7b0bd7`,
  is a later native shadow architecture source. Its own historical STATUS says it
  had not been natively compiled/executed in that package because the compiler
  was unavailable. It is not accepted R27 behavioral source.

The R28 shadow bundle independently preserves a byte-identical copy of the same
R27 parent-verifier output (`67a74e...e349`) and an accepted-policy record,
SHA256 `983db6a9c771f4952392d288459d65dfb04c33a7cbca37ac9f10a4365c7887a8`.
The policy records the active promotion
`STRONGER_MASTER_GENERAL_SPECIFIC_BRIDGE`, retained R26/R25/R23 mechanisms,
rolled-back proposals, shadow partials, and locked gates. This is policy/history
metadata, not executable continuity proof.

The R30 shadow bundle again preserves the same byte-identical 33/33 R27 verifier
output (`67a74e...e349`). Thus the accepted digest/output record is stable across
at least the recovered R27-native-shadow, R28-shadow and R30-shadow bundles.

## Classification

### Exact recovered

- Accepted parent raw-byte SHA256, step and restart invariants already held by R33.
- Historical expected semantic digest value `562aaaed...3b04`.
- Byte-identical 33/33 verifier **output** in three recovered derivative bundles.
- R27 accepted-policy metadata from the R28 shadow.
- Later native-shadow source and later Zag toolchain provenance.

### Reconstructed

None. No semantic-digest algorithm, field order, canonicalization rule, verifier
logic, or original dependency closure was reconstructed from output values.

### Inferred

The repeated byte-identical verifier log strengthens confidence that the recorded
accepted digest and five metric values were stable historical parent identifiers.
It does not establish how those values were computed.

### Still unresolved

- original `r27_experiments.R27State` implementation;
- original semantic-digest implementation and exact field/canonicalization contract;
- original 33-check accepted-parent verifier source and invocation contract;
- original Python/runtime/dependency provenance for the accepted R27 execution;
- source-derived transitive custom-module closure, including
  `r26_experiments.py`, `r25_release.py`, `r25_experiments.py`,
  `r23_experiments.py`, `r22_experiments.py`, `r21_experiments.py`,
  `r20_experiments.py`, `r18_experiments.py`, `r17_experiments.py`, and
  `r15_master_training.py`;
- behavioral equivalence of any native reconstruction.

## Consequence

The parent continuity gate remains blocked. The newly recovered derivative
archives strengthen custody/provenance and give exact historical output targets,
but they do not authorize semantic-digest recomputation, behavioral-continuity
claims, training, parent migration, learner authority, or promotion.

The next valid continuity action remains acquisition of the original
`tnn-pre-v1-r27-general-learning` ZIP/TAR.GZ (expected SHA256 respectively
`7042ff849743c9509586840df865f34423a92f9afc09ef2c7cf937b35b68b65e` and
`770cafe6f51faecd0212f22fee663684537b6a6ce06b2919fcf9c34c5d6614b7`)
or an authoritative complete original source export. Any recovered legacy code
remains inert until separately inspected and mapped into the native continuity
qualification path.

Canonical R27 remains step 60,423 with zero newborn restarts. R33 training runs
remain zero and promotion remains disallowed.
