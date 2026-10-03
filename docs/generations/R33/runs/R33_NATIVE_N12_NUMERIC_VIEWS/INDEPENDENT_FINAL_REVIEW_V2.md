# N12 independent final-source review V2 — focused B01/B02 closeout

Date: 2026-09-06.

**Disposition: APPROVE_FOR_PREREGISTRATION for the exact source/evaluator/design/configuration package below, within the declared bounded R33-N12 engineering scope.**

**B01 and B02 are resolved at the source/evaluator-review level. No remaining blocking change was identified in this focused re-review.** This approves preparation of the preregistration; it is not a statement that controls passed, an execution grant, a build attestation, or approval of training or promotion. The existing source/build/platform freeze and execution-admission requirements remain in force.

## Scope and evidence

Read the native-only execution contract and the preserved [INDEPENDENT_FINAL_REVIEW.md](/Users/Shared/micah/Documents/TNN/TNN/Research/R33_NATIVE_N12_NUMERIC_VIEWS/INDEPENDENT_FINAL_REVIEW.md). Compared the current four-file package against `PREREVIEW_V1`, whose source and review hashes match the previous review. Read the entire revised evaluator (546 lines), design (238 lines), and configuration (55 lines). Rechecked the unchanged implementation hash and relevant integer, dtype, shape, binding, and export routines; rechecked the frozen scanner's LONG handling and integer decoding. Rehashed the inherited source closure and inert references against the previous review's identities.

The delta is confined to explicit LONG fixture construction and assertions, the authored u1 row oracle and its call sites, and corresponding design/configuration additions. `views.zag` has no diff. The old fixture entry point delegates to the extended builder with LONG substitution disabled, preserving the existing fixture variants. Inventory, replay, supervision, and the five-child schedule have no implementation diff.

Only source/document inspection, comparison, and hashing were used, followed by creation of this new review. No tests, fixtures, primary, Python, reducers, compiler probes, or compilation were executed by this reviewer. BUILD_03/04 logs and executables were not used as evidence. Earlier reviews, source, registry, canonical files, and build artifacts were not edited. The initial draft and V1 review remain historical records; this file supplies the disposition for the revised package rather than rewriting their verdicts.

## Exact identities

All paths below are relative to `/Users/Shared/micah/Documents/TNN/TNN/`. For discussion and line citations, `driver.zag`, `views.zag`, `DESIGN.md`, and `CONFIG.json` denote files in `Research/R33_NATIVE_N12_NUMERIC_VIEWS/`.

### Package approved for preregistration

| File | SHA256 |
| --- | --- |
| `Research/R33_NATIVE_N12_NUMERIC_VIEWS/views.zag` | `1c2717f5fbde4f8308125127cb73fe2de19cf0805bc3eee754b03395dd04a6a6` |
| `Research/R33_NATIVE_N12_NUMERIC_VIEWS/driver.zag` | `badf9c5af229ee9f203f0f5599e5a31733e01d446804426c4cf9ece62baa9919` |
| `Research/R33_NATIVE_N12_NUMERIC_VIEWS/DESIGN.md` | `11e49bc31be4b087bee38d9db8897b7f72f58afe76119cb5e6f56cabcc4d2a2e` |
| `Research/R33_NATIVE_N12_NUMERIC_VIEWS/CONFIG.json` | `ae2c262196d5630660dbacd43f4fad4fd4307098725c470fd701e8ad7d1fd474` |

### Preserved comparison and review records

| File | SHA256 |
| --- | --- |
| `Research/R33_NATIVE_N12_NUMERIC_VIEWS/INDEPENDENT_REVIEW_DRAFT.md` | `5d15536dabf05569d26c4e3ce0da7bc92754225c0090cb6fed275f458f9dea4b` |
| `Research/R33_NATIVE_N12_NUMERIC_VIEWS/INDEPENDENT_FINAL_REVIEW.md` and its `PREREVIEW_V1` copy | `af8839e2eb9ed7e3b7eb39ebd9860261af9fc68e6e8f94d5f174cc3f07001249` |
| `Research/R33_NATIVE_N12_NUMERIC_VIEWS/PREREVIEW_V1/views.zag` | `1c2717f5fbde4f8308125127cb73fe2de19cf0805bc3eee754b03395dd04a6a6` |
| `Research/R33_NATIVE_N12_NUMERIC_VIEWS/PREREVIEW_V1/driver.zag` | `351daf8304fdffde75a7c9465939324ec1541bd5056b3acb27b4bf1d79ff09bb` |
| `Research/R33_NATIVE_N12_NUMERIC_VIEWS/PREREVIEW_V1/DESIGN.md` | `c4811a7fa84f086b3c26197ebefee5094b2fe3b62350e76b019b90cacd015089` |
| `Research/R33_NATIVE_N12_NUMERIC_VIEWS/PREREVIEW_V1/CONFIG.json` | `58d98ab879695592dedc84e8473300233fd146ad69bd560cd908d1fc33b4c63e` |

### Unchanged inherited identities

| File | SHA256 |
| --- | --- |
| `Research/R33_NATIVE_ONLY_EXECUTION_CONTRACT.md` | `76ed5e73146c1c72322e70d9cc6807ee0bc625005680dcedc2e33fcd189e071e` |
| `Research/R33_NATIVE_N11_PARENT_CUSTODY/binding.zag` | `769585237b77b4f811df60875f38a0e4889eda46659ff29cc8cca1d87d495626` |
| `Research/R33_NATIVE_N10_PARENT_MAP/inert.zag` | `f6b1a0ad43016b0c99f545139e6de402d40f78e7b4ffa4e68f655c9ad5aae0e6` |
| `Research/R33_NATIVE_N10_PARENT_MAP/mapio.zag` | `8b6d2395f4e41b0800c9a4bc4c66a00be7ef924550077ab7cd3728767931623c` |
| `Research/R33_NATIVE_IO_V1.zag` | `b9160ff94caf1565360c99ac1144b514836dc34227f97e2a152c541ec6280d2e` |
| `Research/R33_NATIVE_SHA256_V2.zag` | `9824f6db66a943917dbc7cd5e6862ab0967b7ea83161cfc357bb7d17ca683bcf` |
| `Research/R33_NATIVE_PROCESS_V3.zag` | `04c5bc6c3c7222786ab5c6d9af384935c9dd533a6a89046860da0c67ffcb2f89` |
| `Research/R33_NATIVE_N12_NUMERIC_VIEWS/REFERENCES/numpy_v2_3_5_numeric.py.txt` | `fc3727bd7bbaa1a1d74a2f50f8157dc86cdfc7bb5cf620b1ebdafd3272439b98` |
| `Research/R33_NATIVE_N12_NUMERIC_VIEWS/REFERENCES/numpy_v2_3_5_descriptor.c.txt` | `a362cbc09924b4b019706e0a7b766fbb37b3e1cd6b85a1c3ef27d0038f2fa5f9` |

This table re-establishes unchanged identities, not a new full audit of each dependency or authentication of the references' upstream release provenance. The source closure remains `driver -> views -> binding -> mapio -> inert -> SHA256 -> IO`, with `driver -> PROCESS_V3 -> IO`.

## B01 — resolved: valid LONG decoding and end-to-end acceptance

The [literal LONG emitter](/Users/Shared/micah/Documents/TNN/TNN/Research/R33_NATIVE_N12_NUMERIC_VIEWS/driver.zag:36) explicitly selects opcode 138 or 139, emits a one-byte or four-byte length header respectively, and copies a separately authored body. It does not derive that body from `nv_integer` or route these controls through the default BININT encoder. The frozen scanner at `inert.zag:158` maps both forms to kind 4.

The [standalone controls](/Users/Shared/micah/Documents/TNN/TNN/Research/R33_NATIVE_N12_NUMERIC_VIEWS/driver.zag:274) pass each stream through `pm_scan` and `pm_validate`, assert kind 4 and body extent, and assert both `NvInt.status == 0` and an independent literal value. The [schedule](/Users/Shared/micah/Documents/TNN/TNN/Research/R33_NATIVE_N12_NUMERIC_VIEWS/driver.zag:311) supplies the following eight bodies for **each** opcode:

| Little-endian body (hex) | Expected signed value |
| --- | --- |
| Empty body | 0 |
| `8000` | 128 |
| `80` | -128 |
| `ff` | -1 |
| `0100000000000000` | 1 |
| `ffffffffffffffff` | -1 |
| `ffffffffffffff7f` | 9223372036854775807 |
| `0000000000000080` | -9223372036854775808 |

The sign boundary and extensions are consistent with the inspected decoder. The minimum expected value is expressed as `-9223372036854775807-1`, avoiding an out-of-range positive signed literal. This is a source-level consistency check; neither native arithmetic nor output formatting was executed here.

The [view controls](/Users/Shared/micah/Documents/TNN/TNN/Research/R33_NATIVE_N12_NUMERIC_VIEWS/driver.zag:285) add five cases per opcode: accepted empty LONG dimension zero; accepted dimension 128; decoded -128 with exact shape refusal -9003; accepted eight-byte dimension one; and accepted eight-byte -1 in both dtype size/alignment sentinel positions. The builder substitutes both state fields at lines 64 and 66; the unchanged dtype validator requires both to equal -1. The sentinel case keeps a positive shape of one, so it does not confuse an allowed dtype sentinel with an allowed negative axis.

Successful views assert rank/dimension/count, coordinate behavior, scalar or empty behavior, and the complete row oracle. The 128-element fixture's byte carrier has exactly 128 authored `ab` bytes, and its first/last scalar expectations are 171. Negative-shape cases use the existing exact-refusal helper, including empty owning outputs and no successful scalar payload. All fixtures retain before/after raw-plus-seven-table fingerprints.

The prior invalid-LONG-span witness remains at [driver.zag:344](/Users/Shared/micah/Documents/TNN/TNN/Research/R33_NATIVE_N12_NUMERIC_VIEWS/driver.zag:344); the over-eight-byte refusal remains at line 401 with its existing nine-byte fixture branch. A genuine empty LONG now has an explicit successful oracle, independently of those refusals. Hypothetically rejecting all kind-4 nodes would fail the new standalone status checks and successful-view checks. The V1 B01 counterexample is therefore closed without inventing expected parent inventory counts.

## B02 — resolved: complete authored shape-row oracle

The new [p12_u1_shape_row](/Users/Shared/micah/Documents/TNN/TNN/Research/R33_NATIVE_N12_NUMERIC_VIEWS/driver.zag:224) asserts successful ownership and exactly 160 bytes before inspecting the record. It checks all sixteen four-byte header fields, all eight dimensions, all eight strides, and the 32-byte original-payload digest. Unused dimension/stride slots and the success/reserved word at offset 60 are explicitly checked as zero where required.

Layout expectations come from the caller's authored shape, order, payload length, and the fixed u1/one-byte/`|`/bytes-carrier grammar. They are not copied from `v.dims`, `v.strides`, or another exported row. Provenance IDs and offsets are checked against the parsed fixture descriptors, rather than copied from the view. The expected digest hashes the separately authored payload using the already-frozen SHA helper; this is independent selection of expected bytes, not an independent cryptographic implementation or new SHA qualification.

The simple stride oracle sets active strides to one only for nonempty fixtures and to zero otherwise. That is correct for **every current call site**: scalar shape has no active axes; nonempty rank-eight fixtures have all dimensions one; positive LONG-backed views have rank one; and every remaining shape is empty under the declared zero-stride convention. The helper is deliberately not a general multidimensional-stride oracle. Nontrivial rank-two C/F layouts retain their independent matrix oracle.

Both call sites are present: [existing shape controls](/Users/Shared/micah/Documents/TNN/TNN/Research/R33_NATIVE_N12_NUMERIC_VIEWS/driver.zag:271) and [successful LONG-backed views](/Users/Shared/micah/Documents/TNN/TNN/Research/R33_NATIVE_N12_NUMERIC_VIEWS/driver.zag:306). Thus scalar unused fields, all rank-eight fields, and every maximum-axis empty shape are checked on export, not just in live view storage. An exporter zeroing slots 2–7 would now fail the rank-eight authored-dimension/stride expectations, closing the specific B02 counterexample even if replay repeated the same wrong bytes.

The helper checks row nonoverlap with input and view dimensions/strides and frees the returned allocation. The unchanged matrix retains node/edge nonoverlap checks, deliberate row overwrite, subsequent view validation, and map fingerprints. Ownership remains the declared trusted-allocator/single-owner contract; no arbitrary-pointer or allocator-failure qualification is implied.

## Control accounting and integration

| Planned control group | Static count and disposition |
| --- | --- |
| Existing scalar-bit matrix | 93 fixtures, unchanged. |
| Supplemental scalar-bit fixtures | 7 fixtures, unchanged. |
| Existing scalar/rank-eight/empty shape fixtures | 20: scalar C/F, rank-eight all-ones C/F, and each of eight zero positions in C/F. All now invoke the complete row oracle. |
| Explicit LONG scalar decodes | 8 per opcode, 16 total; each expects successful decoding. |
| Explicit LONG view cases | 5 per opcode, 10 total: 8 expected successful views and 2 expected negative-shape refusals. These are not ten successful views. |
| Calls to the new full shape-row oracle on the planned success path | 20 existing shape fixtures plus 8 accepted LONG view cases, 28 total. |

These are counts derived from source, not observed execution or check totals. `CONFIG.json:14` through 20 and `DESIGN.md:153` through 176 agree with the loops and call sites. The 26 new LONG cases run at the start of the existing refusals child; failure returns before the rest of that child's work, and the unchanged supervisor will not launch subsequent children after a failed parent check.

The five modes and expected exits remain invalid/2, matrix/0, refusals/0, inventory-write/0, inventory-replay/0. Deadlines remain 5/20/20/60/60 seconds under the 180-second parent guard, with unchanged capture/file and observed-RSS bounds. This review does not measure whether execution will fit those bounds. No timeout, output limit, or failed check may be waived on the basis of this approval.

The source-bound nonlearning inventory and complete-page/manifest replay are unchanged. They still classify all REDUCE descriptors, report unsupported forms without guessing counts, hash each supported payload, and probe only its first/last scalars. The new independent synthetic expectations close the two review gaps without turning known-parent replay into a scientific or historical-behavior oracle.

## Final finding dispositions and approval boundary

| Item | Disposition for the reviewed package |
| --- | --- |
| B01, successful LONG qualification controls | Resolved for preregistration by explicit literal decode and end-to-end controls for LONG1 and LONG4. |
| B02, complete scalar/empty/high-rank row expectations | Resolved for preregistration by the authored full-record oracle at all relevant call sites. |
| F01–F05 implementation corrections, output aliasing, and empty-axis overflow | Prior source-level dispositions retained; implementation and inherited source hashes are unchanged. B01/B02's associated evaluator gaps are now closed. |
| Remaining blocking changes in this focused bounded review | None identified. |

The previously accepted limitations remain: live immutable validated maps; uniquely owned view and row allocations; no shallow-copy lifetime, generation-reuse, arbitrary forged-pointer, concurrent-writer, or arbitrary-map ownership guarantee; no allocator fault-injection qualification; and no new security or cryptographic certification. Element strides and all-zero empty strides are the declared N12 convention, not historical NumPy object-layout recovery. Reference provenance and the parent's actual historical NumPy version remain as qualified in the preserved review.

The exact package above may proceed to preregistration with this review included. Compiler/import/target/platform, fixture design, allowed effects, resource bounds, and the settled selected build pair must still be pinned through the already-required freeze/admission workflow before any execution. Those are existing downstream requirements, not an additional unresolved B01/B02 blocker. Material changes to the reviewed package require review of the changed identities; a compiler success or deterministic binary pair is not evidence that these controls passed.

**Terminal verdict: APPROVE_FOR_PREREGISTRATION — bounded engineering scope only.** No tests were run by this review, and no original-method recovery, tensor/storage completeness, semantic-digest equivalence, training readiness, real authority grant, security certification, scientific promotion, or R33 completion is claimed.
