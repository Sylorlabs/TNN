# N12 independent final-source engineering review

Date: 2026-09-06.

**Disposition: BLOCKING CHANGES REQUIRED BEFORE PREREGISTRATION for the exact revision identified below.**

The implementation corrections address F01–F05 within the explicitly trusted, live, immutable-map boundary. The remaining blockers are two specific evaluator/oracle gaps, B01 and B02. They are not observed runtime failures or claims that the corrected implementation currently computes an incorrect result. Both can be addressed inside the existing numeric-view engineering scope; neither requires allocator fault injection, a new security boundary, historical behavior reconstruction, or changes to frozen N10/N11.

## Review scope and evidence

Read the native-only execution contract first. Read all 220 lines of `views.zag`, all 449 lines of `driver.zag`, all 211 lines of `DESIGN.md`, and all 51 lines of `CONFIG.json`. All four actual SHA256 values match the requested review identities. Inspected the inherited binding/map/scanner, allocation, hash, and process-supervision sources, and the relevant inert NumPy reduction/frombuffer routines. The initial draft remains a separate historical review, not an approval of this revision.

This review performed only source/reference reads, directory/process inspection, and artifact hashing, plus creation of this review file. No tests, fixture/primary runs, Python, reducers, compilation, compiler probes, or registry/source/canonical changes were performed. Source-level descriptions of controls below mean that assertions are present, not that they passed.

Existing build directories were visible, and a compiler-named process was still present during a process-list inspection. That observation does not establish which task owned the compiler. I did not inspect the potentially active build logs or execute/hash the build executables. This is a source/evaluator review, not an attestation of settled build success, deterministic binaries, or runtime behavior. Compiler/target/platform and settled build-artifact pinning remain part of the already-declared later freeze.

All relative paths in this report are under `/Users/Shared/micah/Documents/TNN/TNN/`. Unless otherwise stated, `views.zag`, `driver.zag`, `DESIGN.md`, and `CONFIG.json` refer to `Research/R33_NATIVE_N12_NUMERIC_VIEWS/`.

## Exact reviewed identities

### Requested final-source package

| File | SHA256 |
| --- | --- |
| `Research/R33_NATIVE_N12_NUMERIC_VIEWS/views.zag` | `1c2717f5fbde4f8308125127cb73fe2de19cf0805bc3eee754b03395dd04a6a6` |
| `Research/R33_NATIVE_N12_NUMERIC_VIEWS/driver.zag` | `351daf8304fdffde75a7c9465939324ec1541bd5056b3acb27b4bf1d79ff09bb` |
| `Research/R33_NATIVE_N12_NUMERIC_VIEWS/DESIGN.md` | `c4811a7fa84f086b3c26197ebefee5094b2fe3b62350e76b019b90cacd015089` |
| `Research/R33_NATIVE_N12_NUMERIC_VIEWS/CONFIG.json` | `58d98ab879695592dedc84e8473300233fd146ad69bd560cd908d1fc33b4c63e` |

### Inherited source closure and reference identities

| File | SHA256 | Scope |
| --- | --- | --- |
| `Research/R33_NATIVE_ONLY_EXECUTION_CONTRACT.md` | `76ed5e73146c1c72322e70d9cc6807ee0bc625005680dcedc2e33fcd189e071e` | Complete contract. |
| `Research/R33_NATIVE_N11_PARENT_CUSTODY/binding.zag` | `769585237b77b4f811df60875f38a0e4889eda46659ff29cc8cca1d87d495626` | Complete source; fixed identity and load admission. |
| `Research/R33_NATIVE_N10_PARENT_MAP/mapio.zag` | `8b6d2395f4e41b0800c9a4bc4c66a00be7ef924550077ab7cd3728767931623c` | Complete source; range-checked wire fields, load validation, read/write/close behavior. |
| `Research/R33_NATIVE_N10_PARENT_MAP/inert.zag` | `f6b1a0ad43016b0c99f545139e6de402d40f78e7b4ffa4e68f655c9ad5aae0e6` | Complete source, with focused reinspection of scanner, integer decoding and chain validation. |
| `Research/R33_NATIVE_IO_V1.zag` | `b9160ff94caf1565360c99ac1144b514836dc34227f97e2a152c541ec6280d2e` | Complete source; allocation, exclusive/read-only file access, limits and check output. |
| `Research/R33_NATIVE_SHA256_V2.zag` | `9824f6db66a943917dbc7cd5e6862ab0967b7ea83161cfc357bb7d17ca683bcf` | Complete source; inherited digest behavior and bounds, not a new cryptographic qualification. |
| `Research/R33_NATIVE_PROCESS_V3.zag` | `04c5bc6c3c7222786ab5c6d9af384935c9dd533a6a89046860da0c67ffcb2f89` | Complete source; direct-child admission, execution, capture, timer and reap handling. |
| `Research/R33_NATIVE_N12_NUMERIC_VIEWS/REFERENCES/numpy_v2_3_5_numeric.py.txt` | `fc3727bd7bbaa1a1d74a2f50f8157dc86cdfc7bb5cf620b1ebdafd3272439b98` | Inert text, especially lines 1957–1961; not imported or executed. |
| `Research/R33_NATIVE_N12_NUMERIC_VIEWS/REFERENCES/numpy_v2_3_5_descriptor.c.txt` | `a362cbc09924b4b019706e0a7b766fbb37b3e1cd6b85a1c3ef27d0038f2fa5f9` | Inert text, especially lines 2690–2816; not compiled or executed. |
| `Research/R33_NATIVE_N12_NUMERIC_VIEWS/INDEPENDENT_REVIEW_DRAFT.md` | `5d15536dabf05569d26c4e3ce0da7bc92754225c0090cb6fed275f458f9dea4b` | Preserved initial review and finding/control checklist. |

The inspected source-level import closure is `driver -> views -> binding -> mapio -> inert -> SHA256 -> IO`, together with `driver -> PROCESS_V3 -> IO`. These are reviewed source identities, not a claim that every eventual build copy, compiler invocation or executable has been independently verified by this review.

## Initial findings: resolved and remaining dispositions

| Finding | Final-source disposition | Evidence and qualification |
| --- | --- | --- |
| F01: map/view association | **Resolved within the declared lifetime boundary.** | `views.zag:157` records raw pointer/length and node/edge allocation identities. `nv_bound` at line 160 checks those identities and revalidates reducer, dtype, carrier, extent, order, shape and strides. All three public read/export operations call it. `driver.zag:264` exercises safe handle mutations and line 271 uses a distinct live map. This is not allocator-generation protection or approval of shallow-copied owning maps. |
| F02: closed-map row access | **Resolved at source level; refusal controls present.** | `nv_row` at `views.zag:205` validates before allocation or slicing. `nv_ready` rejects the cleared/failed map before accessing its former tables. `driver.zag:275` clears a synthetic map before requesting bound reads; lines 165–166 check row refusal after view close. The control uses valid cleared structures, not arbitrary dangling pointers. |
| F03: incomplete tuple chains | **Resolved for the N12 tuple boundary.** | `views.zag:48` traverses to exactly zero with bounded count, increasing valid links, item-only edges, zero second operands, valid members and matching tail. `driver.zag:239` onward includes cycle, negative successor/head, count, tail and operand controls. The negative-successor witness explicitly expects inherited `pm_validate` to accept and N12 to refuse. Arbitrary-map unique edge ownership remains unqualified, as explicitly disclosed in `DESIGN.md:49`. |
| F04: invalid LONG span becoming zero | **Implementation fix resolved; positive qualification remains blocked by B01.** | `views.zag:79` rejects invalid LONG spans before calling the inherited decoder. `driver.zag:249` checks the helper's failure and the enclosing shape refusal. However, no successful native fixture establishes that a valid LONG, including a genuinely empty encoding of zero, is still admitted. |
| F05: zero-axis position changes acceptance | **Resolved at source level under the new documented convention.** | `views.zag:134` validates every axis before product construction. Any zero selects zero elements and pre-zeroed logical strides. Nonempty products and strides are bounded before multiplication. `driver.zag:316` exercises every rank-eight zero position with maximum legal surrounding axes in both orders. Verification of the exported empty/high-rank row is still incomplete under B02. |

The previously known **output-alias defect is removed structurally**: `nv_row` no longer takes a caller-selected writable destination. It returns a separate owning allocation. The disjointness checks, deliberate row overwrite, subsequent `nv_bound`, and raw-plus-seven-table fingerprints at `driver.zag:133` through 167 match this API. Old short-output, partial-overlap and caller-suffix tests no longer apply; their omission is not a blocker.

The previously known **empty-axis stride overflow is removed** by zero detection before multiplication and the all-zero empty convention. For nonempty views, positive dimensions, the element/product ceiling and the payload-width check bound strides and coordinate arithmetic. `nv_bits` validates the flat index before narrowing/multiplication, so its start/extent are bounded by the validated raw span. Both 32-bit wire representation and 64-bit intermediate arithmetic fit under these invariants. These are source-level arguments, not compiler/runtime measurements.

`nv_close` now sets status -9008 and clears ownership fields. Single ownership, map-outlives-view, immutability and no shallow copies are explicit. No generation-safe or concurrent hostile-writer guarantee is implied by resolving F01/F02.

## Blocking changes

### B01 — P2: The evaluator can reject every valid LONG and still satisfy its synthetic expectations

Evidence: [fixture integer encoder](/Users/Shared/micah/Documents/TNN/TNN/Research/R33_NATIVE_N12_NUMERIC_VIEWS/driver.zag:27), [overlong fixture branch](/Users/Shared/micah/Documents/TNN/TNN/Research/R33_NATIVE_N12_NUMERIC_VIEWS/driver.zag:64), [invalid-span witness](/Users/Shared/micah/Documents/TNN/TNN/Research/R33_NATIVE_N12_NUMERIC_VIEWS/driver.zag:249), and [integer/shape controls](/Users/Shared/micah/Documents/TNN/TNN/Research/R33_NATIVE_N12_NUMERIC_VIEWS/driver.zag:304).

`f12_integer` emits BININT for every value in signed-32 range. All allowed shape dimensions, all successful dtype integer fields, and every positive shape fixture are in that range. Its eight-byte LONG branch is used for an out-of-range dimension such as maximum i64. The other explicit LONG cases are a nine-byte encoding and an invalid raw span, both expected to refuse.

Consequently, a hypothetical change making `nv_integer` reject every kind-4 node would still satisfy these synthetic LONG expectations. This is a static counterexample to the evaluator's coverage, not an experiment performed here. The inventory's intentionally unfixed supported/refused counts cannot supply the missing positive oracle: a refusal can simply be reported as an unsupported descriptor. No parent counts should be guessed to compensate.

The initial review specifically required distinguishing a valid empty LONG zero from raw-span failure and positive signed-LONG boundary controls. `DESIGN.md:55` retains valid, in-bounds LONG encodings up to eight bytes in the supported subset. That is an existing scope requirement, not a request to support new integer types or arbitrary precision.

**Required before preregistration:** add a small explicit native integer-control group through the frozen scanner/validator, with fixed expectations independent of `nv_integer`. It must include a valid empty LONG encoding of zero, a nonempty LONG-backed dimension that produces a successful view, and signed/sign-extension boundaries. In particular, distinguish little-endian body `80 00` (128) from body `80` (-128), and cover an eight-byte legal sign extension. Verify `NvInt.status` and value, successful view shape/count and scalar or empty behavior, and the appropriate row. Retain the existing invalid-span and over-eight-byte refusals. A decoded negative dimension must refuse as a shape, whereas -1 used in an allowed dtype-state sentinel has its separate expected meaning.

Cover each LONG opcode explicitly claimed by the final fixture specification, or state its encoding coverage accurately; no requalification campaign for all frozen parser opcodes is requested. Update only the affected evaluator/design/configuration accounting in the implementation task, retain the existing scope and five-child schedule where practical, and submit new hashes for re-review. This review itself does not make those edits or run the controls.

### B02 — P2: Scalar, rank-eight and empty rows lack an independent layout oracle

Evidence: [shape control](/Users/Shared/micah/Documents/TNN/TNN/Research/R33_NATIVE_N12_NUMERIC_VIEWS/driver.zag:213), [row assertion in that control](/Users/Shared/micah/Documents/TNN/TNN/Research/R33_NATIVE_N12_NUMERIC_VIEWS/driver.zag:225), and [fresh-page comparison](/Users/Shared/micah/Documents/TNN/TNN/Research/R33_NATIVE_N12_NUMERIC_VIEWS/driver.zag:324).

The 93 matrix fixtures check the complete nonempty rank-two row layout. The twenty additional shape fixtures check the live view's dimensions/strides and scalar or empty access. But after exporting their row, they assert only row status and the byte-extent field at offset 40. They do not assert its length, rank/elements, all eight serialized dimensions/strides, unused fields, or payload digest.

For example, an exporter that persistently zeroed dimension/stride slots 2–7 while correctly handling slots 0–1 could pass the rank-two row assertions and all current live-view rank-eight assertions. Replaying the same exporter would reproduce the same incorrect bytes. This is an evaluator blind spot, not a claim that the reviewed `nv_row` loop currently does that: the inspected loop writes all eight slots.

**Required before preregistration:** strengthen the existing twenty shape fixtures, without adding a new experiment family. Assert an owned 160-byte row and the declared record fields against the fixture specification: rank, elements, byte extent, all eight dimensions and logical strides, unused/reserved fields, provenance fields and original-payload digest. Rank-zero unused axes must be zero; rank-eight all-ones has eight dimensions/strides of one; each empty fixture retains all eight requested dimensions and has eight zero strides. Derive expectations from the authored shape and the documented convention, not by copying `v.dims`, `v.strides`, or another `nv_row` result.

This closes the export side of the existing F05/stride correction and row contract. Whole-page replay remains useful for reproducibility, but cannot substitute for these independent layout expectations.

## Other controls and evaluator behavior reviewed

| Area | What the current source establishes prospectively |
| --- | --- |
| Positive scalar matrix | The loops at `driver.zag:174` describe 88 combinations of eleven dtypes, two explicit endians, two C/F orders and two carrier kinds, plus five alternate-symbol/one-byte-endian cases. The seven supplemental fixtures give 100 positive bit fixtures in total. These counts agree with the design/configuration; they are planned counts, not observed results. |
| Bit-pattern oracle | Literal low/high expectations cover all-ones, high-bit and alternating integers; f4/f8 signed zero, infinities and quiet/signaling NaN payloads. Supplemental cases add minimum subnormal bit patterns, Boolean byte 2 and asymmetric 64-bit bytes with low `0x05060708`, high `0x01020304` in both byte orders. No floating evaluation, Boolean normalization or signed-i64 scalar oracle is used. |
| Coordinates and grammar refusals | Asymmetric `(2,3)` fixtures use independent formulas `i*3+j` / `i+j*2` for C/F coordinates. Negative, one-past, wrong-rank and maximum-i64 flat-index checks are present. Envelope/dtype/state/order/arity, integer-for-Boolean flags, external/readonly-external/text carriers, shape kind/rank, byte length, and dimension/product refusals assert declared statuses rather than exit alone. This is representative scoped coverage, not exhaustive malformed-pickle conformance. |
| Failure payload and restoration | `p12_expect_refusal` checks empty ownership, no source pointer, empty row, exact row/scalar error and zero scalar limbs. Synthetic table mutations are restored, validated and fingerprinted. The actual parent is never the mutation fixture. Handle refusals check bound rejection and empty row/scalar error; source control flow also routes coordinate reads through the same bound validator. |
| Memory non-mutation | `p12_fingerprint` covers raw input plus nodes, edges, memo, stack, marks, globals and histogram. Positive row overwrite is followed by view validation and fingerprints. This is an engineering invariant in the trusted process, not kernel isolation or arbitrary-memory-writer resistance. |
| Schedule and terminal handling | Five `p12_run` calls use deadlines 5/20/20/60/60 seconds and expected exits 2/0/0/0/0. A failed parent check prevents the next child launch. The parent checks supervision status, started/reaped flags, exit, signal, stderr, observed RSS, capture length, one line-started completed-count record with zero failures, and presence of the child pass marker. Child `main` emits that marker only after handled work with zero recorded failures. The fixed producer is trusted; this is not a general hostile-log parser qualification. |

The old initial checklist's allocator fault injection, arbitrary forged pointers, generation reuse and concurrent writer controls are **not renewed as requirements** here. The design and configuration expressly exclude them. Representative positive and negative LONG acceptance, and correctness of the already-produced row fields, are not among those exclusions and are the only blocking control changes requested.

## Nonlearning inventory, binding and replay

The path at `driver.zag:341` loads the actual map using the unchanged `pb_load` and checks accepted identity. The inherited loader verifies the fixed binding, map manifest and pages, raw hash, and map validation before returning success. The descriptor's historical semantic digest is not recomputed or used as a new authority grant.

The inventory loop visits every kind-16 REDUCE in node order. Recognized frombuffer candidates are counted separately; ordinary unsupported statuses -9001 through -9004 receive zero-initialized refusal rows with node, opcode offset and status. Allocation/row-generation or other unexpected failures are not credited as unsupported success. The final accounting compares records with the map's reduction count and reconciles candidate/supported/refused/other counts without imposing guessed numeric counts.

Successful rows hash the complete original payload. Their first and last scalar reads are re-encoded and compared to the retained bytes; one-element views have one probe and empty views have none. The totals are descriptor-wise, so shared storage can be counted repeatedly. These probes are not exhaustive decoding of every parent element, and the byte hashes are not semantic or behavior equivalence evidence.

The 160-byte manifest header carries the original-file and map-manifest hashes from the successfully validated binding. The remaining fields bind declared counts, descriptor totals and probe counts. Each 48-byte page entry contains ordinal/count/length and a page hash. Page and manifest capacities in source agree with the configuration: 400 rows per 64000-byte page, at most 1311 pages and 63088 manifest bytes. The maximum descriptor-wise byte/element sum under the stated node/payload caps fits a positive i64.

The replay mode independently reloads the pinned map in the next child, rederives rows and manifest, and compares saved lengths and every page/manifest byte. It reads rather than replaces the inventory. Before/after memory fingerprints and accepted-identity checks accompany both modes. This is an appropriate repeatability check over known engineering material, subject to B01/B02's independent-oracle limitations, not fresh scientific evidence or a historical method rerun.

`pb_training_admission` remains an always-refusing custody-only operation; the -8904 assertion does not establish complete runtime authority enforcement. No promotion follows from a future N12 pass.

## Accepted boundaries and nonblocking qualifications

**Admission and ownership.** Numeric APIs require a live immutable validated map and uniquely owned view allocations. Pointer/length/table-identity binding plus metadata rechecks is adequate for the stated wrong-live-map and safely corrupted-handle cases. It is not a content signature on every read, unique-edge-ownership proof for arbitrary tables, defense against wide forged fields, allocator-generation tracking, or lifetime protection for shallow copies. These exclusions are explicit and acceptable for this bounded review.

**Representation and reference semantics.** Element strides and zero logical strides for empty arrays are declared N12 conventions. The inert NumPy source supports the selected four-argument C/F frombuffer and plain version-3 dtype reduction grammar; its broader optional axis-order/K branch is not silently accepted. Explicit endian handling and raw unsigned limbs are consistent with the declared byte interpretation. `readonly` is a serialized-carrier flag, not a write grant. The reference hashes identify inspected text, not independently authenticated upstream release provenance or the parent's actual historical NumPy version.

**Resources and failures.** The code declares the 180-second parent guard, the 165-second sum of child deadlines, exclusive new output root, 1 MiB file/capture ceilings, zero core allowance, 64 descriptors and the observed 384 MiB child RSS ceiling. The latter is not a hard memory sandbox; the frozen supervisor contains only the direct child. Output publication and reads are limited by the selected source paths, not a newly qualified hostile-process filesystem sandbox. Time/RSS feasibility is unmeasured by this review.

The generic map/page envelope is not proof of successful processing of every map up to those limits. For example, full-table fingerprinting uses the inherited one-shot hash size limit; overly large table fingerprints fail the run rather than establishing general maximum-capacity support. No additional stress campaign is requested for this fixed-parent scope.

**Allocation status detail.** Top-level view/row allocation failures use -9007, while a digest-helper failure during row creation is freed and translated to -9006 at `views.zag:217`. The design's short status glossary should therefore not be read as a complete allocation-cause taxonomy. Both are terminal inventory failures rather than supported/unsupported data results. Allocator fault injection and comprehensive OOM/leak qualification remain excluded; this detail is not an additional blocker.

## Required handoff and approval boundary

Resolve **B01** with positive LONG and sign-boundary controls, and **B02** by extending the existing shape controls' row oracles. Preserve the initial draft, this reviewed revision's identities, the failed authoring artifacts and frozen imports. Supply the revised evaluator and any changed design/configuration hashes for a focused independent re-review. Do not treat a source edit, successful compilation or byte-identical build pair as evidence that the new controls have passed.

This report does **not** approve preregistration for the four hashes above. It does not grant execution or authorize registry changes. It does not request a broader project scope. No original-method recovery, tensor/storage completeness, training readiness, real grant, security certification, scientific promotion, or R33 completion is claimed.
