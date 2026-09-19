# R33 parent-payload audit

Reviewer: GPT-6 Pro, independent parent-payload reviewer. Date: 2026-09-05.

Status: **EXACT HISTORICAL PARENT BYTES LOCATED; FULL-STATE MIGRATION AND EXECUTABLE DEPENDENCY CLOSURE NOT ESTABLISHED.**

This is a bounded static inventory and byte-hash audit. No learner, generator, historical verifier, training process, migration, experiment, job dispatch, or registry update was executed. The only authorized output is this report. Archive members were streamed/read in memory, not extracted to disk. Pickle contents were inspected as inert opcode data without importing their classes, calling reducers, or invoking `pickle.load`/`loads`.

## 1. Outcome and exact recovery locators

The actual accepted parent is present in **both full R28 archives**, not in the R27 native-shadow policy/bridge records. These are archive-member locators, not already extracted filesystem paths.

| Container | Absolute filesystem path | Container bytes | Actual SHA-256 |
| --- | --- | ---: | --- |
| R28 ZIP | `/Users/Shared/micah/Documents/TNN/TNN/Research/tnn-pre-v1-r28-aeif-no-graph-shadow.zip` | 45,673,638 | `b155570237d1560b82dcf5fd9ea7771772899ec06c19bef5b74438c517fac5b6` |
| R28 TAR.GZ | `/Users/Shared/micah/Documents/TNN/TNN/Research/tnn-pre-v1-r28-aeif-no-graph-shadow.tar.gz` | 45,252,977 | `060e44f8d9aeb1cf395744d13076e7e72044cf7533ab0a3158dad2cae56a412c` |

Identical member path in both containers:

`tnn-pre-v1-r28-aeif-no-graph-shadow/state/parent-r27-accepted-state.pkl`

Actual member size: **15,871,908 bytes**. Independently streamed SHA-256 from each container:

`31e670fcd2a2fefc02a1d032b8016bd93c28844df8ea40889593d030a2096e5a`

This exactly matches the requested historical parent-file SHA-256 and the R28 ZIP's `MANIFEST.sha256`, line 611. The full ZIP contains 880 entries including directories and 71,594,799 uncompressed bytes according to its directory inventory. Those totals are not measures of learner state.

The 192,512-byte sibling download file is **not the same container**:

`/Users/Shared/micah/Documents/TNN/TNN/Research/tnn-pre-v1-r28-aeif-no-graph-shadow.tar.gz.openai-download-f8c1d75cb0a94756ab59e59117420575`

Its SHA-256 is `a0d0b51a5a2a705a1170825e29d7492e86f1f077218567b0b45231c32d2e08c7`. Its completeness was not established. Use the complete, hash-identified containers above, not this differently sized download companion.

## 2. Identity: what was directly checked versus historically reported

Static parsing of the matched pickle established a root descriptor for `r27_experiments.R27State` with 14 fields, including:

| Root field | Serialized value |
| --- | --- |
| `format` | `TNN_PRE_V1_R27_GENERAL_LEARNING` |
| `development_step` | **60423** |
| `newborn_restarts` | **0** |
| `r26_sha256` | `df3acde273aa682642d13763a24208ff1dbb42968313cbe2a4256f7ccbc1f839` |

The stream declares pickle protocol 5. Its final STOP is at byte offset 15,871,907, with no trailing bytes. The inert inventory consumed the complete outer opcode stream: 175,954 memo entries, 585 NEWOBJ descriptors, and 64 referenced global symbols. These are serialization counts, not neuron, parameter, or competence counts. Encapsulated tensor/storage byte payloads were not executed or decoded into live tensors.

The accepted-state digest is recorded as:

`562aaaedb5b9ceec2f50482f631992c247cbe50e9f6d2321b811e311ecf73b04`

It appears in the archived `state/LINEAGE.txt`, line 3, and `verification/r27_parent_rerun.log`, line 6. The latter records the historical 33/33 PASS and step 60423. **This audit verified the raw-file hash and statically read the counters; it did not independently recompute the semantic accepted-state digest or rerun those 33 checks.** Do not equate the two different hashes.

Companion members in the R28 ZIP were actually hashed:

| Member, relative to `tnn-pre-v1-r28-aeif-no-graph-shadow/` | Actual SHA-256 |
| --- | --- |
| `MANIFEST.sha256` | `599861a0fb86238b140dfb43c3f7274f38e6b192ff091a236ea2720fb59e77a8` |
| `state/parent-r27-accepted-policy.json` | `983db6a9c771f4952392d288459d65dfb04c33a7cbca37ac9f10a4365c7887a8` |
| `state/LINEAGE.txt` | `43553e7315a1105657240d31f503cf8c385670254a9fbf3f579d8f0c3a3a2a92` |
| `verification/r27_parent_rerun.log` | `67a74e11090f57aa0084924735f096d6bdc55e7f7514da4ce078e01aff8be349` |

The accepted policy is 712 bytes and is distinct from both the actual pickle and the R28 shadow policy. Target-member hashes were compared with the relevant manifest lines; an exhaustive rehash of every archive-manifest entry was not completed.

## 3. Mutable-state coverage actually observed

The complete historical pickle is substantially more than a policy stub. Inert descriptors preserve nested R27 → R26 → R25 → R24 → R23 state, along with shared references. An embedded ancestor is not missing merely because its original standalone file is unavailable.

| State family | Observed serialization evidence | Remaining boundary |
| --- | --- | --- |
| Developmental identity and ancestry | R27 step60423/restarts0; embedded R26 step60249, R25 step57285, R24 step41144, each restarts0; nested `r23_state` descriptor | Not a native migration or independent validation of every ancestor digest |
| R27-specific state | `category_system` dictionary with 4 entries; `abstraction_policy` with 2; `visual_debate_policy` with 6; `semantic_generator`; `architecture` with 58; `evidence` with 12; `self_revision_history` with 58 entries | Dictionary sizes/history counts are not evidence of causal completeness or accepted competence |
| Learned numerical mechanisms | NumPy buffer/dtype descriptors; Torch network/parameter/storage descriptors; 17 serialized LogisticRegression objects with coefficients/intercepts; learned `W`, bases and prototypes in custom objects | Exact historical class/runtime closure and executable tensor interpretation not established |
| Memory, replay, provenance | `ProtectedSkillMemory` fields `fast`, `slow`, `gram_counts`, `history`, `step`; 435 `Trace` descriptors with cue/ops/anchors/support/sources/provenance; grounded-concept rows; learner buffer/replay fields | Not a demonstrated complete raw-evidence archive, durable causal transaction log, or exhaustive referenced-blob closure |
| Policies and revision history | R27/R26/R25/R24 revision lists of 58/52/47/34 entries; sibling, learning-action, abstraction and architecture dictionaries; accepted-policy companion | Human-granted R33 authority, revocation state and non-rewindable supervisor accounting are not thereby qualified |
| RNG | `random.Random` and NumPy generator/PCG64/SeedSequence descriptors; custom learner `rng` fields | Presence of some RNG state does not establish complete Python/NumPy/Torch/global stream coverage |
| Historical sensory and language mechanisms | R25 `speech_core_pam` and `speech_noise_pam`; R26 video encoder; semantic generators, relational stores, graph objects and ByteBPE descriptors | Historical objects must not be silently activated as compliant graph-free, BPE-free, boundary-free R33 cognition |
| Mid-update and external state | Some learner learning-rate, replay, steps, routing/module and memory fields are serialized | Full optimizer accumulators, pending actions, external raw blobs, grants, resource counters and durable trace cursor/append ancestry remain unaccounted against an authoritative runtime inventory |

Explicit nulls are not missing files: R27 `affordance_model` and `speech_motif_decoder` are serialized as null. R26 `speech_segmenter` is null and `speech_index` is an empty dictionary. Filling these from a new initializer would change the accepted state rather than recover it.

No defensible global mutable-state coverage percentage or `dark_state_count=0` can be reported: the runtime denominator and transitive external-state inventory have not been established. This follows the accounting requirements in `R33_WHITE_BOX_OBSERVABILITY_CONTRACT.md`, lines 16–35, and `TNN_R27_TRACEABILITY.md`, lines 22–43.

### Legacy architecture is genuinely present

The inert object inventory contains `r15_master_training.EntityEventGraph`, `r26_experiments.MultiViewEntityGraph`, and two `r23_experiments.ByteBPE` descriptors. The latter contain `max_vocab`, `merges`, and `token_bytes`; `SemanticRoundTripGenerator` includes a `bpe` field. This is stronger evidence than merely finding those words in documentation.

The accepted-policy companion, lines 6–10, explicitly retains `R26_VIDEO_IDENTITY`, `R25_GENERIC_VAD`, and `R23_R25_SEMANTIC_GENERATOR`. Thus an archive named "no-graph-shadow" can correctly retain a graph/BPE-bearing historical parent without proving that parent is a graph-free active system. Preserve the historical bytes; classify and isolate their contents before any separately authorized migration. Historical "Master" names do not make a program the human trainer.

## 4. Other locations checked

| Location | Actual finding |
| --- | --- |
| `/Users/Shared/micah/Documents/TNN/TNN/Research/tnn-r27-native-master-shadow.zip` | 83,397 bytes; SHA-256 `bfd755a76bff995bd8373fa88ed5922716a21c8926d7703199dc62ffe03e55ce`. Its state directory contains only the bridge manifest and shadow policy, not accepted parent bytes. |
| `/Users/Shared/micah/Documents/TNN/TNN/Research/tnn-v1-current-execution.tar.gz` | 42,615 bytes; SHA-256 `ed14c92315327b0388eb5d4820bf458f22ed2e5bd3813ed3f21b2c51d10ee362`. Full member listing showed sources/evaluators/results and empty directories, not the accepted R27 pickle. Its manifest is an inventory of those files, not the missing parent. |
| `/Users/Shared/micah/Documents/TNN/TNN-R1` | Two files: gate status and failure report; no checkpoint payload. |
| `/Users/Shared/micah/Documents/TNN/TNN-R1-Audit` | Six files including download companions: gate status, failure report and final summary; no checkpoint payload. |
| Historical `/mnt/data/tnn-r27-full-work/state/r27-accepted-state.pkl` | Not present in this local environment. It is the old input path in the archived bridge builder, not the recovery locator to use now. |

The R27 shadow ZIP's actual member hashes are:

| Member, relative to `tnn-r27-native-master/` | SHA-256 |
| --- | --- |
| `state/state_bridge_manifest.json` | `d3deec13ee1cf921d32d7d7cc6cdfff04f67ae60af1d2caed0d4651024b899fb` |
| `state/shadow-policy.json` | `019aa097a32f9747cba3a9a41bd38dd8019ddf8077e3092ceadc33d741a56a8f` |
| `verification/build_state_bridge.py` | `9f840343b07c6efb4beb53c636c026f7b1275e5c7d30729ec03e0c960e72f18c` |

Static reading of `build_state_bridge.py`, lines 5–24, explains the distinction: it loads a historical external pickle and emits selected metadata, not a full copy or native state migration. It was not executed here.

Loose R31 reference-only pickles were hashed and are not this parent: the 50K file is 5,648,276 bytes, SHA-256 `fbda09cf4eee5915c671239702e487f713a687b7ee4c955a022fdb06f55a4b5b`; the 120K file is 10,250,192 bytes, SHA-256 `3178448b4db5cf8b00980049046f16af08fd6a66712ec052d0f24eccc4a9bf8d`. Both are under `/Users/Shared/micah/Documents/TNN/TNN/Research/`, named `R31_INTEGRATED_LIFE_50K_STATE_REFERENCE_ONLY.pkl` and `R31_INTEGRATED_LIFE_120K_STATE_REFERENCE_ONLY.pkl`. Neither was deserialized.

## 5. Genuinely unresolved recovery dependencies

**Not missing:** the exact historical accepted pickle and its accepted-policy companion. Do not regenerate a parent or start a newborn to solve a file-availability problem that has now been resolved.

**Not located/closed by this bounded audit:** the original R27 class/digest implementation and its complete source/runtime dependency bundle. The payload names `r27_experiments.R27State`; the checked loose-source search found no definition, and the relevant R28 archive listing did not supply the original R27 loader module. The original `/mnt/data/r27_extract/tnn-pre-v1-r27-general-learning` path is absent locally. No globally exhaustive filesystem/Git-history/remote search is claimed.

The pickle's custom module references are `r15_master_training`, `r17_experiments`, `r18_experiments`, `r20_experiments`, `r21_experiments`, `r22_experiments`, `r23_experiments`, `r25_experiments`, `r25_release`, `r26_experiments`, and `r27_experiments`. Library references include NumPy internals, sklearn and Torch storage/network rebuild symbols. This is a dependency inventory, not a claim that every listed module is absent everywhere or that whatever versions are installed now are compatible. Torch storage byte reducers also require review before any real deserialization.

**Still unestablished:** the accepted semantic-digest algorithm and its scope; complete external raw-blob/state references; reproducible whole-state native encoding; field ownership/authority mapping; a migration acceptance witness. These are evidence gaps, not proof that every corresponding historical store was omitted from the pickle.

The R28 archive's `verification/verify_r28_shadow.py`, lines 13–21, checks summary metadata, the parent-file hash, and text in pre-existing historical logs. That code does not freshly load the R27 parent or recompute its semantic digest. A shadow-integrity PASS is therefore insufficient evidence of runnable full-state recovery.

## 6. Required review judgments

**Strongest criticism:** metadata continuity, exact-byte availability, and executable developmental continuity have been too easy to conflate. Parent availability is now established, but a hash-matched Python pickle plus historical PASS log is not a native continuing R33 brain. The blocker should be described as dependency/coverage/migration qualification, not "accepted parent payload not found."

**Confound:** the R28 no-graph container name and later graph-free design can mask legacy graph/BPE/VAD-bearing accepted state. Likewise, a bridge's `parent_digest` is an assertion about another artifact, not its bytes. Recovering the correct parent must neither silently activate prohibited old mechanisms nor discard their learned contents and describe the result as lossless continuity.

**Falsifier:** reject parent identity if the candidate member's raw SHA-256, root step, or restart count differs from the requested values; the two located members passed those static identity checks. Reject a later full-continuity claim if any inventoried consequential field or required external reference lacks a preserved mapping, is silently default-initialized, or cannot be traced to the accepted parent. No such migration test was run. The serialized graph and ByteBPE objects already falsify an unqualified claim that the historical payload itself is graph/BPE-free.

**Recommended next change:** in a separately authorized no-learning recovery change, pin the complete container, exact member, raw payload hash and accepted-policy hash; establish an immutable recovery location and original class/digest/runtime closure before actual deserialization. Then create a field-by-field migration/retention inventory separating protected substrate, human trainer configuration, learner state, evaluator-only material and inert legacy preservation. Do not add live graph/BPE/VAD/token-boundary mechanisms to satisfy recovery. Keep C02 file-ingress evidence component-scoped; it does not settle parent migration. No extraction or registry edit is performed by this audit.

**Forbidden claims:** accepted parent bytes are absent; the shadow policy is the full accepted state; the semantic digest or historical 33/33 checks were freshly reproduced here; all mutable state is accounted; the historical parent is graph/BPE-free; runtime compatibility, native full-state migration, deterministic continuing learning, M0–M7 enforcement, zero dark state, new capability, consciousness or promotion has been established. R27 remains canonical; R32/E51AJ remains a completed non-promoted experimental frontier.

## 7. Current-state snapshot and evidence boundary

The inspected `R33_CURRENT_STATE.json` snapshot records C01 component completion, zero R33 training runs, no promoted checkpoint, `full_parent_migration_verified: false`, `runtime_milestone_enforcement_verified: false`, and specification-level rather than integrated-runtime telemetry. The main agent may advance C02 concurrently; this audit does not infer C02's final status or alter any of those fields.

Read local files, with SHA-256 measured during this audit:

| File under `/Users/Shared/micah/Documents/TNN/TNN/Research/` | SHA-256 | Read scope |
| --- | --- | --- |
| `R33_CURRENT_STATE.json` | `dab7a6516765fe56178e884da8339adcea026683f42ed018fe187d379a41b9c4` | Lines 1–48 |
| `R33_AUDIT_SCOPE.json` | `a18f35e9da8c92127255706abf813e37d13c6d5c33e495ee0b37ebe49c9fc2ea` | Lines 1–48 |
| `R33_ARCHITECTURE_CONTRACT.md` | `991418a200a8a151d29144a791a8b7150818295d54548cffec4cd0e5c9a5eb24` | Lifetime identity, lines 40–58 |
| `R33_WHITE_BOX_OBSERVABILITY_CONTRACT.md` | `e814dbc1da911da0741c27795f5b7106e575998e450b8f45684b4ef1fff08e2b` | Lines 1–53 |
| `TNN_R27_TRACEABILITY.md` | `b553941822d70ee571aeca9255f1e8e367e2e6b0dfef0be7a275e372131f759d` | Lines 1–58 |

Also read current handoff/C01 result/C02 configuration, relevant R28 metadata and parent-verification records, the two candidate archive member listings/manifests, relevant R30/R31/R32 archive names, and the sibling-directory inventories. Searches included hidden/ignored working files under `/Users/Shared/micah/Documents/TNN`, excluding `.git` and Python caches where specified. A filename census returned 2,277 entries at that point; this is not a claim that all were hashed or fully audited.

Several broader hash/inventory commands were blocked before execution; no evidence is attributed to them. An initial inert-parser attempt stopped on a reduced container, after which its opcode representation was inspected and the corrected inert inventory completed. No historical object code or reducer was executed in either attempt. Full archive-manifest validation, historical digest recomputation, runtime coverage tests and migration remain outside the completed evidence.
