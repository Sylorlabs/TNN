# R33 accepted-parent source and migration dependencies

Reviewer: GPT-6 Pro. Date: 2026-09-05.

Status: **PARENT BYTES PREVIOUSLY LOCATED; ORIGINAL CLASS, SEMANTIC-DIGEST AND RUNTIME DEPENDENCIES NOT CLOSED.**

Repository: `/Users/Shared/micah/Documents/TNN/TNN`.

This is a new, bounded, read-only source/dependency audit. Its only write is this report. No legacy object was imported, deserialized, instantiated or migrated; no pickle reducer, learner, historical generator, verification program or C03 program was executed. Archive members were streamed to text/hash tools without extraction to disk. No prior report, archive, registry, current-state record or C03 file was modified.

## 1. Result and evidence separation

The original `r27_experiments.py` / `R27State` implementation, the function producing the accepted semantic digest, and the eleven referenced custom-module implementations were **not located in the completed search scope below**. This is not a claim that these sources are absent from every possible backup.

The accepted parent remains available at the archive-member locators in [the frozen parent-payload audit](/Users/Shared/micah/Documents/TNN/TNN/Research/R33_PARENT_PAYLOAD_AUDIT.md). That report's SHA-256 was checked in this task: `17a13c4c922ac55d20faf1f0b3c88923184317607e2072676e1901f081e84383`.

Inherited evidence, not a repeated payload inspection in this task:

| Identity | Established by the earlier accepted audit |
| --- | --- |
| Parent member | `tnn-pre-v1-r28-aeif-no-graph-shadow/state/parent-r27-accepted-state.pkl` in the full R28 ZIP and TAR.GZ |
| Raw parent-file SHA-256 | `31e670fcd2a2fefc02a1d032b8016bd93c28844df8ea40889593d030a2096e5a` |
| Serialized root | `r27_experiments.R27State`, step `60423`, newborn restarts `0` |
| Historically reported accepted semantic digest | `562aaaedb5b9ceec2f50482f631992c247cbe50e9f6d2321b811e311ecf73b04` |

The raw-file hash and semantic digest are different identities. This task neither recomputed the latter nor repeated the historical 33-check verification. The actual source found explains why the bridge and R28 integrity checks do not do that either.

## 2. Actual source found: exact locators and hashes

`archive::member` below denotes a member inside a local archive, not an extracted filesystem path. Source line numbers refer to the member's own text. Actual streamed SHA-256 values matched the stated manifest entries.

### A. R27 bridge builder: dependency reference, not the missing class source

Archive: `/Users/Shared/micah/Documents/TNN/TNN/Research/tnn-r27-native-master-shadow.zip`

Member: `tnn-r27-native-master/verification/build_state_bridge.py`

SHA-256: `9f840343b07c6efb4beb53c636c026f7b1275e5c7d30729ec03e0c960e72f18c`.

Manifest: `tnn-r27-native-master/MANIFEST.sha256`, line 30.

Read lines 1–29. Lines 5–12 reference an external parent and the historical source directory `/mnt/data/r27_extract/tnn-pre-v1-r27-general-learning/src`, with a fallback to its parent directory. Both import branches request `r27_experiments`. These are historical dependency hints, not located source files in this repository.

Line 13 would perform an actual legacy load if executed; it was only read. Lines 17–19 compute a raw-file hash and inspect two counters. Line 20 inserts the accepted semantic digest as a **literal expected string**. The file does not define `R27State` or its semantic digest algorithm, and its metadata output is not a full-state serializer.

### B. R28 packaging code: copies state/policy, not the original runtime bundle

Archive: `/Users/Shared/micah/Documents/TNN/TNN/Research/tnn-pre-v1-r28-aeif-no-graph-shadow.zip`

Member: `tnn-pre-v1-r28-aeif-no-graph-shadow/scripts_build_release.py`

SHA-256: `a864d846b82c9e2f35b4aa9f4f05b54dbaa5adfb665dd90de1ee9896de33fee5`.

Manifest: `tnn-pre-v1-r28-aeif-no-graph-shadow/MANIFEST.sha256`, line 606.

Decisive source read: lines 1–20 and 65–74. Lines 13–18 name and copy the original `state/r27-accepted-state.pkl` and `state/r27-accepted-policy.json` from the historical R27 release. Line 9 defines `sha(p)` as SHA-256 of file bytes; line 19 applies it to the parent. Lines 71–73 embed the step, restart count, semantic-digest literal and historical PASS descriptions in release metadata. They do not compute the accepted semantic digest from state fields.

No copy of the eleven original custom modules appears in the completed R28 archive pathname inventory. Thus this archive preserves the parent payload without closing its executable source dependencies.

### C. R28 shadow verifier source: metadata/file checks only for the parent

Same R28 archive as B.

Member: `tnn-pre-v1-r28-aeif-no-graph-shadow/verification/verify_r28_shadow.py`

SHA-256: `0d2b0d5609ca3b7db06a3feeb1c26adc2e895e0583cab3c7cc52112545c797a6`.

Manifest: `tnn-pre-v1-r28-aeif-no-graph-shadow/MANIFEST.sha256`, line 817.

Read lines 1–24 and 43–50. Lines 13–15 compare JSON metadata with expected literals. Lines 16–18 test parent-file/policy presence and raw-file SHA-256. Lines 19–21 search existing logs for historical PASS markers. Line 49 would write a report; this verifier was **not run**. Its parent checks do not recompute semantic state or establish successful legacy loading.

### D. Runtime pins found, but belonging to earlier releases

| Archive absolute path | Member | Actual member SHA-256 | Manifest line |
| --- | --- | --- | ---: |
| `/Users/Shared/micah/Documents/TNN/TNN/Research/tnn-pre-v1-r5-goldilocks.zip` | `tnn-pre-v1-r5-goldilocks/requirements.txt` | `c756d49c3b631396572e75d301ff6a7ada08732fbd7d229d16cc1e79d69186d3` | 29 |
| `/Users/Shared/micah/Documents/TNN/TNN/Research/tnn-pre-v1-r6-rsi.zip` | `tnn-pre-v1-r6-rsi/requirements.txt` | `c756d49c3b631396572e75d301ff6a7ada08732fbd7d229d16cc1e79d69186d3` | 56 |

Each entire requirements file, lines 1–3, says `numpy==2.3.5`, `opencv-python==4.13.0.0`, `scipy==1.17.0`. These are **not an R27 lockfile**. They do not pin the R27 custom sources, Python build, Torch or scikit-learn dependency versions. No package installation, runtime compatibility test or import was attempted.

### E. A Git-history digest hit that is not the R27 digest

File: `/Users/Shared/micah/Documents/TNN/TNN/Research/R32_E51AI_ANALYSIS/verify_archive.py`.

SHA-256: `4464d395f84905aed8cf93553da56ac4a9452f3114410d0aeacc013c88abdc92`.

Lines 30–31 define `digest(data)` as `hashlib.sha256(data).hexdigest()`. Surrounding lines 20–42 place it in E51AI source/artifact checking. Git identifies its addition in commit `36cab59430c2b108411bad5c09da09767fdffbe4`. It is a byte-hash helper, not evidence of R27 semantic canonicalization.

## 3. Original semantic-digest algorithm: not found

The inspected code establishes only raw-byte SHA-256 and literal/metadata comparisons. It does **not** establish which state fields produced `562aaa…73b04`, how nested ancestry and shared references were treated, the ordering/canonical encoding, numerical normalization, excluded fields, or whether external data participated.

Do not infer an algorithm from the digest's length, substitute SHA-256 of newly encoded state or invent `json.dumps(sort_keys=True)` canonicalization. A new migration digest can identify a new representation, but cannot retroactively certify the original accepted digest. Recover the original digest implementation and its dependencies before claiming reproduction.

## 4. Custom and library dependency inventory

The custom-module identities below come from the earlier accepted payload inventory, specifically its lines 115–119; this task did not reparse the pickle. All eleven filenames were checked against local working paths, relevant archive member paths and all-ref Git path history. None was located. Selected core class definitions were additionally searched in ZIP Python sources and Python Git history to check for renamed files.

| Required original custom module | Mapping area indicated by the prior descriptor inventory | Source result in searched scope |
| --- | --- | --- |
| `r27_experiments.py` | Root R27 state, category/abstraction/debate policy, inherited-state ownership | Not located; bridge import reference found |
| `r26_experiments.py` | Embedded R26, video representation, entity/name state, legacy multiview graph | Not located |
| `r25_release.py` | Embedded R25/R24 accepted-state wrappers and relational storage | Not located |
| `r25_experiments.py` | Adaptive concept and promoted-composition learner state | Not located |
| `r23_experiments.py` | Embedded R23, grounded/speech mechanisms, semantic generation, ByteBPE | Not located |
| `r22_experiments.py` | Temporal reinspection mechanism | Not located |
| `r21_experiments.py` | Historical convolutional speech modules | Not located |
| `r20_experiments.py` | Question, role-binding and surface-operation mechanisms | Not located |
| `r18_experiments.py` | Relational memory and temporal attention | Not located |
| `r17_experiments.py` | Grounded/motif memory and sensory PAMs | Not located |
| `r15_master_training.py` | Nested student, protected skill memory, traces, fibers and entity/event graph | Not located |

These are serialized dependency names, not a complete transitive import graph. Without the original files, additional imports, class initialization/state hooks, helper functions, resource lookup and semantic-digest calls remain **unresolved/unsearched from source**, rather than a known exhaustive list of missing modules. Historical `Master` identifiers do not confer human trainer authority on software.

The previous inventory also identifies NumPy internal buffer/dtype and RNG constructors, `random.Random`, scikit-learn LogisticRegression state, Torch network/parameter/tensor rebuild helpers, and `torch.storage._load_from_bytes`. Required version/build/ABI and device behavior remain unqualified. In particular, opaque Torch storage bytes are not made safe or fully interpreted merely by inventorying the outer pickle's symbols. Neither storage reducers nor nested storage payloads were executed here.

## 5. Field-mapping blockers

| State family | Required mapping or evidence before a full-continuity claim |
| --- | --- |
| Root identity and embedded ancestors | Preserve root step60423/restarts0, nested accepted-state fields and aliases. Ancestor counters are historical nested state, not a license to restart at an earlier step. Resolve source-defined ownership, state hooks and semantic-digest coverage. |
| Learned numeric state | Preserve tensor/array values, shape, dtype, layout/byte order and shared storage. Establish original inference/update semantics from source; field names and serialized weights alone do not supply those semantics. |
| Memory, provenance and raw evidence | Map stored episodes, policies, codebooks, expansions, retrieval/replay state and external references. Account for required blobs and causal parents; serialized trace descriptors do not establish a complete raw archive or durable journal. |
| Null or empty accepted fields | The previous audit records R27 `affordance_model` and `speech_motif_decoder` as null, R26 `speech_segmenter` as null, and `speech_index` as empty. Preserve these values; supplying newly initialized implementations is a change, not recovery. |
| RNG, optimizer, pending work and resources | Determine the authoritative reachable-state inventory and persistence semantics. Some saved RNG/replay state does not establish coverage of all global streams, optimizer accumulators, pending actions or supervisor accounting. |
| Legacy graphs | Keep historical `EntityEventGraph` / `MultiViewEntityGraph` data inert and recoverable. Do not activate graph-based cognition in active TNN/Foundry, and do not discard their learned contents to make the new state appear graph-free. A lossless permitted representation and behavioral-continuity evidence remain to be designed and qualified. |
| Legacy ByteBPE and boundaries | Preserve the original byte/token tables, merges and associations as inert legacy data. Do not run ByteBPE, use its tokenization as active learner input, or silently replace it and claim equivalent learned behavior. Storage preservation is not qualified transfer into an allowed raw-evidence representation. |
| Historical VAD policy | The accepted-policy companion retains `R25_GENERIC_VAD`; that metadata does not locate the responsible source or prove how it executes. Preserve it as historical policy, not permission to insert VAD or supplied token boundaries into active R33 sensing. |
| Authority and rollback | Map historical configuration separately from current human grants and protected supervisor state. Restored old policy must not restore revoked authority, refund cumulative resources or erase audit history. |

No global mutable-state coverage fraction, complete lossless map, runtime compatibility or graph/BPE/VAD-free historical-parent claim is established. Inert archival preservation can coexist with a graph/BPE/VAD-free active design, but does not by itself prove that the active replacement retains accepted capabilities.

## 6. Completed bounded searches

Working-tree filename search included hidden/ignored files inside this repository, excluding `.git` internals and Python caches. Targeted text searches covered source, documentation and metadata. Git searches used local objects only; there was no fetch or remote access.

Repository HEAD at inspection: `04a7268ac5c08ce3b3f1f3a35f48a2425fdceec8`. The repository reports non-shallow history. `git rev-list --all --count` returned 313 commits; including reflogs also returned 313. All-ref path history showed no filename for any of the eleven modules. All-ref Python-history searches for the R27/module/digest symbols produced only the unrelated E51AI digest helper described above; additional core-class-definition searches found no original accepted-state definitions. Targeted documentation/metadata history searches for `r27_experiments`, `R27State`, `r25_release` and `r15_master_training` completed without matches.

R27/R28 archives were introduced in commit `16c318c` (2026-08-28). Current archive bytes have Git blob identities `a4f889a3faefc7fc285e042caf0974e3285f57d2` for R27 ZIP, `c98c320b92c01bd139ef2acfd66cb145f5f17405` for R28 ZIP, and `6725a2852b13e427b805d43a577b343c3626cb0c` for R28 TAR.GZ, matching the all-ref object inventory. There is no different version of these three archives in that reachable-object listing. Git blob identifiers are not SHA-256 file hashes.

The following **137 top-level `.py` member occurrences across 14 archives** were streamed through targeted module/R27/digest searches. A search is not a full semantic code review. Paths in this table are relative to the absolute repository path above; SHA-256 values were actually measured in this task.

| Archive path | Python members scanned | Container SHA-256 |
| --- | ---: | --- |
| `Research/tnn-r27-native-master-shadow.zip` | 11 | `bfd755a76bff995bd8373fa88ed5922716a21c8926d7703199dc62ffe03e55ce` |
| `Research/tnn-pre-v1-r28-aeif-no-graph-shadow.zip` | 52 | `b155570237d1560b82dcf5fd9ea7771772899ec06c19bef5b74438c517fac5b6` |
| `Research/tnn-pre-v1-r5-goldilocks.zip` | 15 | `be943522196e2d13aaa254aed8c4245a3dc99afee567b42d99dca6308d9df06f` |
| `Research/tnn-pre-v1-r6-rsi.zip` | 25 | `b33f52d11f475662241298b78d3dafd5770a318fa29b6573a8cbefb0a1df5258` |
| `Research/tnn-v1-current-execution.zip` | 10 | `d81b63e8c923e652a779791f78e4b75eec2582576a0653209b2f03aee3dec4a2` |
| `Research/tnn-v1-evidence-fibers-senses-search.zip` | 3 | `86a2c5275a9e2ec90d337c485b9a96842a5843faec5335db0856e7c76ad584cf` |
| `Research/tnn-r30-big-boom-shadow.zip` | 1 | `c0f349edf713bb6796d8ed617465bacc8699f09c2c4401810206a82cbba88623` |
| `Research/tnn-r31-endogenous-chunking-shadow.zip` | 7 | `27821ee9f49f52c67b4c39f2bd5c33c56448fc2007b8e2c4374fa23eec337bbd` |
| `Research/R32_MIDCAMPAIGN_SNAPSHOT.tar.gz` | 8 | `a53db71ab7f18ffb7c962f9f37468ad3821e8452f4882625e03619e6655b748d` |
| `Research/R32_RUNTIME_SNAPSHOT.tar.gz` | 1 | `9ddcde817a87aed8c47c30ca65368a1d60749162489cc33decdc975f530271f1` |
| `Research/R32_V38_AUTOCONTINUE_BUNDLE.tar.gz` | 0 | `f61d29ba15886eae3dc0561362f36f659acee892b9855e1aa00ed664a5c8841d` |
| `Research/R32_V39_BUNDLE.tar.gz` | 1 | `fd7877146395c92702ad40d65495b205b89c4eed2fe5ec0a333edddce9edd6ef` |
| `Research/R32_V40_BUNDLE.tar.gz` | 1 | `46bcecb466df39321708e9c33b7871e95be05c42cd4ce88ac53dd470fa1ea09a` |
| `Research/checkpoints/R32_E45_PREIMPLEMENT_2026-08-23.tar.gz` | 2 | `ee14ade52c89699e8c0864c85c0dac919d88289cf52625f72cb8331163c8def7` |

The full R28 TAR.GZ was additionally hashed (`060e44f8d9aeb1cf395744d13076e7e72044cf7533ab0a3158dad2cae56a412c`), and its sorted member pathname inventory matched the R28 ZIP exactly. This is pathname parity, not independent revalidation of every TAR member's contents. The nested R5 ZIP at `tnn-pre-v1-r6-rsi/lineage/tnn-pre-v1-r5-goldilocks.zip` was streamed and hashed to `be943522196e2d13aaa254aed8c4245a3dc99afee567b42d99dca6308d9df06f`, identical to the separately searched R5 ZIP.

## 7. Missing within scope versus unsearched

**Not missing:** the exact accepted parent and its accepted-policy companion, as established by the frozen payload audit. Existing nested ancestors are not missing simply because their original standalone releases are unavailable.

**Not located in completed searches:** the eleven custom-module source files; original R27 accepted-state digest implementation and field-selection contract; original R27 dependency lock/runtime provenance; original R27 full verifier source. The bridge and packaging helpers above are located source, but are not substitutes.

**Unsearched or not closed:** transitive imports of those unavailable modules; archived bytecode, opaque tensor/storage content and runtime hooks; arbitrary alternate encodings or source embedded in non-Python members beyond the targeted metadata reads; unreachable/dangling Git objects; remote repositories/releases and external backups; files outside this repository; full historical manifests and external raw-evidence closure. Current installed package versions were not inspected or treated as historical pins.

Nested `tnn-pre-v1-r4-final.zip` members in R5/R6 were identified but not opened; their manifest entry is not a source-content check. Secondary TAR/download companions and the E51 run-artifact ZIPs in `.scratch` were not recursively searched for original R27 source in this task. The R5 member inside R6 is covered by its byte identity to the searched standalone R5 archive, as noted above. These boundaries prevent turning a bounded negative search into a globally exhaustive absence claim.

Two combined Python-based archive scans were blocked before execution and contribute **no completed checks**. A shell scan initially used unsupported `rg --label`; its archive-content portion did not establish results. The tool help was inspected and the successful, explicitly scoped text scans used `awk` instead. Only their successful results count above. The last Git-history search session settled with exit zero. No blocked prior task attempt has been recounted as new evidence.

## 8. Recommended next change and claim limits

Keep parent availability and executable dependency closure as separate gates. The next recovery work item should acquire the **original hash-identified R27 source release**, its eleven known custom modules plus source-derived transitive imports, the original digest/verifier implementation, and original runtime provenance. If an authoritative source bundle cannot be recovered, any reimplementation must be labeled a new, unqualified compatibility implementation rather than the recovered original.

Then author a field-by-field, ownership-aware mapping specification that preserves aliases, nulls, numerical state and historical evidence while isolating legacy graph/BPE/VAD mechanisms. Review object hooks and nested storage formats before authorizing any deserialization. No source reconstruction, package installation, load, extraction or migration is authorized or performed by this report.

This dependency gap blocks a claim of original executable reconstruction, full accepted-parent migration or continuing-brain qualification. It does **not** prevent separately scoped C03 journal/native-replay component work and is not a judgment on C03's result.

Do not claim: original class/runtime closure; freshly recomputed accepted semantic digest; reproduced historical 33/33 checks; complete mutable-state coverage; lossless native continuation; a graph/BPE/VAD-free historical parent; preservation of capabilities merely from retaining inert bytes; new learner authority; consciousness; or promotion. R27 remains the accepted canonical parent, and R32/E51AJ remains a completed non-promoted experimental frontier.
