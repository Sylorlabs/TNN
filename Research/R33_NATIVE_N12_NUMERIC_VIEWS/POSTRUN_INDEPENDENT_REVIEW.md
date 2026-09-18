# R33-N12 independent postrun evidence review

Date: 2026-09-06.

**Terminal disposition: CONFIRM_BOUNDED_ENGINEERING_PASS for the recorded R33-N12 sole primary, identity `r33-native-n12-strict-numeric-views-v1`.**

The inspected frozen package, native assertions, process records, captured outputs, inventory manifest/pages and postrun integrity evidence support the bounded engineering pass. No contradicting check, capture discrepancy, resource excess, changed pinned input, or unresolved B01/B02 evidence gap was identified. This is not a full R33 completion, training, promotion, historical-behavior, unique-physical-storage or security-certification verdict.

## Scope and method

Read the native-only execution contract first, then frozen PREREGISTRATION, FREEZE, ADMISSION and reservation records; consulted the pinned design/configuration, independent review V2, and selected BUILD_03 evaluator/implementation/supervisor source relevant to interpreting the evidence. Inspected the complete launch output, host timing/stderr, all five child stdout/stderr files, native result, and binary inventory manifest. Scanned every recorded CHECK for field structure and exact actual/expected text agreement, tallied records and selected control keys, inspected the signed-64 boundary output directly, and compared artifact sizes and SHA256 identities. These were read-only inspections of existing evidence, not a new scientific or numeric-view evaluator.

Reverified the existing checksum manifests against their files and compared the final build binaries as bytes. Inspected all eighteen inventory page hashes against their stored manifest entries. No N12 executable, test, fixture, experiment, Python, reducer, compiler or compiler probe was run. Individual parent views were not reconstructed or re-evaluated during this review. The historical primary was not repeated.

The only reviewer-authored file is this report. Earlier reviews, sources, build artifacts, registry and canonical files were not changed. Live main-agent result/state/journal reconciliation documents were not reviewed. Paths abbreviated below are rooted at `/Users/Shared/micah/Documents/TNN/TNN/`; `N12/` denotes `Research/R33_NATIVE_N12_NUMERIC_VIEWS/`, and `RUN/` denotes `Research/R33_NATIVE_N12_RUN_PRIMARY_V1/`.

## Freeze, admission and unchanged inputs

The [preregistration](/Users/Shared/micah/Documents/TNN/TNN/Research/R33_NATIVE_N12_NUMERIC_VIEWS/PREREGISTRATION.md:20), [freeze](/Users/Shared/micah/Documents/TNN/TNN/Research/R33_NATIVE_N12_NUMERIC_VIEWS/FREEZE.json:5) and [admission](/Users/Shared/micah/Documents/TNN/TNN/Research/R33_NATIVE_N12_NUMERIC_VIEWS/ADMISSION.json:7) consistently bind the V2-approved four-file package, final BUILD_03 selection, BUILD_04 comparison, five-child schedule and fixed parent/map identities. Admission records preflight at `2026-09-06T20:32:37Z`. The review approval remains preregistration-only; the separate admission is the recorded primary authorization.

| Existing checksum set | Independently reverified entries | Discrepancies |
| --- | ---: | ---: |
| `Research/R33_NATIVE_N12_PINS.sha256` | 103 | 0 |
| `Research/R33_NATIVE_N10_ARTIFACTS.sha256` | 198 | 0 |
| `Research/R33_NATIVE_N11_ARTIFACTS.sha256` | 217 | 0 |
| `Research/R33_NATIVE_N12_ADMISSION_PINS.sha256` | 2 | 0 |

The retained N12 preflight and dispatch verification logs each contain 103 OK records. The retained postrun logs contain respectively 103, 198, 217 and 2 OK records, with no other/failure lines. The independent hash checks above agree with those records; this report does not merely adopt their assertions. These are entries in separate sets, not a claim of that many distinct files across overlapping manifests.

The original parent still hashes to `31e670fcd2a2fefc02a1d032b8016bd93c28844df8ea40889593d030a2096e5a`; the N10 map manifest still hashes to `b7c083364e98d9e5cd674a47b0136de157fedd538b06c743f0c672652984327f`. Both are the frozen identities. BUILD_03/n12 and BUILD_04/n12 have the frozen SHA256 `139a94483b84717e40c12cc85358e3522f7ebcb23733185b9eca340533f32b32` and compare byte-identically. That confirms retained artifact identity, not runtime correctness by itself.

## Process, CHECK, capture and terminal reconciliation

The five PROCESSV3 records in [launch stdout](/Users/Shared/micah/Documents/TNN/TNN/Research/R33_NATIVE_N12_LAUNCH.stdout:1) occur in the registered order. Each records supervision status 0, started/reaped 1, timer registered 1, timeout/timer-fired 0, signal 0 and valid observed-wall measurement 1. Exits are the registered 2/0/0/0/0.

| Child | Recorded exit | Actual CHECK records | Stdout bytes | CPU microseconds | Observed wall microseconds | Peak RSS bytes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| invalid | 2 | 0 | 0 | 1,047 | 5,817 | 1,409,024 |
| matrix | 0 | 7,211 | 243,497 | 1,349,588 | 1,369,684 | 20,873,216 |
| refusals | 0 | 2,383 | 88,995 | 1,226,087 | 1,269,239 | 19,480,576 |
| inventory-write | 0 | 55 | 2,088 | 22,215,980 | 22,658,629 | 274,989,056 |
| inventory-replay | 0 | 74 | 3,101 | 22,941,580 | 23,426,594 | 277,348,352 |

All **9,723 child CHECK records** have exactly matching recorded actual and expected fields. Signed integer fields, including extrema, were compared as exact text, not converted to floating-point numbers for equality. No malformed or unexpected child-output line was found in the inspected record grammar. Each of the four working children has exactly one zero-failure `N12_CHILD_COUNTS` record matching its actual CHECK tally, followed by exactly one `N12_CHILD_PASS` on the final line. The invalid child is correctly silent; its zero checks and missing pass marker are the registered control, not missing evidence.

Every child stderr is zero bytes. Actual stdout file sizes agree with both PROCESSV3 and the parent's `complete_child_capture` assertions. The largest capture, 243,497 bytes, is below the 1,048,576-byte limit. All observed child durations are within the respective 5/20/20/60/60-second deadlines; no timeout is reported.

The native resource totals recompute from the five records as **47,734,282 CPU microseconds**, **48,729,963 observed-wall microseconds**, and **277,348,352 maximum child RSS bytes**. These match `NATIVE_RESULT.json`. Peak RSS is 264.5 MiB, below the declared 384 MiB observed ceiling; it is the maximum child observation, not a sum or a hard memory-sandbox guarantee. The wall field is the frozen supervisor's nonmonotonic post-hoc measurement, not the clock used for deadline enforcement.

The 31-byte [host stderr](/Users/Shared/micah/Documents/TNN/TNN/Research/R33_NATIVE_N12_LAUNCH.host.stderr:1) contains only `real 48.97`, `user 47.33`, and `sys 0.49`. This is the preregistered host timing output, not a child diagnostic failure. Its rounded whole-launch measurements need not equal the native direct-child sums. The approximately 49-second launch is also below the 180-second parent guard.

**Parent accounting is 50 before result publication and 52 after close, not 50 total.** The launch contains 52 matching parent CHECK records: 49 child-supervision/capture assertions, one all-five-children assertion, then successful exclusive result write and output-root close. The JSON deliberately captures `parent_checks_before_result_write: 50` and zero failures at that point. [Launch lines 56 and 75](/Users/Shared/micah/Documents/TNN/TNN/Research/R33_NATIVE_N12_LAUNCH.stdout:56) supply the two subsequent checks; line 76 is the exact final `R33_N12_BOUNDED_NUMERIC_VIEW_ENGINEERING_PASS` marker.

The main agent reports the outer process settled with exit 0. The retained terminal sequence and the pinned [return-zero path](/Users/Shared/micah/Documents/TNN/TNN/Research/R33_NATIVE_N12_NUMERIC_VIEWS/BUILD_03/driver.zag:533) corroborate that report. The scoped launch/timing files do not themselves contain a separate shell exit-status receipt, so this review does not claim to have independently recovered such a receipt. Direct-child exit statuses are explicitly recorded. This provenance qualification does not reveal a contradictory outcome or require repeating the primary.

## B01/B02 and fixed-oracle evidence

### B01: positive LONG and signed-64 boundaries

The refusals log contains all 16 successful standalone LONG decodes and all 10 end-to-end LONG integer checks, with eight successful views and the two intended negative-shape refusals. The pinned order is eight standalone cases plus five view cases for LONG1, followed by the same for LONG4; no new expected values were substituted during this review.

For each opcode, the eight actual/expected values are `0`, `128`, `-128`, `-1`, `1`, `-1`, `9223372036854775807`, and `-9223372036854775808`, corresponding to the literal bodies in the frozen evaluator. In particular:

| Boundary | LONG1 log line | LONG4 log line | Actual and expected text |
| --- | ---: | ---: | --- |
| Maximum signed i64 | 55 | 348 | `9223372036854775807` |
| Minimum signed i64 | 63 | 356 | `-9223372036854775808` |

See [refusals.stdout:55](/Users/Shared/micah/Documents/TNN/TNN/Research/R33_NATIVE_N12_RUN_PRIMARY_V1/refusals.stdout:55) and [refusals.stdout:348](/Users/Shared/micah/Documents/TNN/TNN/Research/R33_NATIVE_N12_RUN_PRIMARY_V1/refusals.stdout:348). The extrema are printed correctly in both actual and expected fields; the native failure count is zero. The `80 00` positive-128 and `80` negative-128 distinction, empty-LONG zero, and eight-byte positive/negative sign extensions likewise match their literal expectations.

The valid empty LONG view refuses scalar access as intended; nonempty dimension-128 and dimension-one views succeed; -128 refuses as a shape with -9003; -1 succeeds in the allowed dtype sentinel case. The invalid-span witness still reports helper failure -1 at [refusals.stdout:2261](/Users/Shared/micah/Documents/TNN/TNN/Research/R33_NATIVE_N12_RUN_PRIMARY_V1/refusals.stdout:2261). Thus the prior raw-span failure/valid-zero distinction now has passing recorded positive and negative evidence within the frozen controls.

### B02: complete scalar/empty/high-rank row expectations

The refusals log contains 20 successful scalar/rank-eight/empty shape controls and 28 successful full shape-row checks: those 20 plus the eight accepted LONG-backed views. It records **224 authored-dimension checks and 224 independent-stride checks**, together with 28 row-length, reserved-success-field and original-payload-digest assertions. All match. The frozen oracle checks all sixteen header fields, eight dimensions, eight strides, the full payload digest and the declared allocation-disjointness conditions; it does not obtain expected shape/stride values from the exported row.

The 16 maximum-axis empty shape cases refuse element access and preserve the declared zero-logical-stride export convention. The actual-parent inventory has no supported empty view, so this empty-layout evidence is synthetic-control evidence, not an observation of an empty parent array.

The matrix additionally records 93 supported matrix fixtures and seven supplemental bit fixtures, 558 independent C/F coordinate assertions and 558 low/high limb assertions each, all matching. Its resident-i64 stride assertion is 8/8. The supplemental output explicitly retains subnormal low=1/high=0, Boolean byte 2, and asymmetric 64-bit low=84,281,096/high=16,909,060 in both byte orders. The raw-plus-seven-table unchanged assertions occur 100 times in matrix and 96 times in refusals, all 1/1; the deliberately inherited negative-terminator acceptance witness remains 0/0 followed by N12 refusal controls.

**B01 and B02 are supported by the recorded native controls, not just their prior source-level closure.** This remains the registered finite engineering coverage, not exhaustive parser, arithmetic, allocation or historical-method qualification.

## Inventory, source binding and fresh replay

The write and replay logs report identical inventories and successful accounting assertions. Their totals also agree with the retained binary manifest header inspected against the frozen wire format.

| Recorded inventory measure | Value |
| --- | ---: |
| All REDUCE descriptors / rows | 7,089 |
| Recognized frombuffer candidates | 5,765 |
| Supported views | 5,763 |
| Refused candidates | 2 |
| Other reducers | 1,324 |
| Descriptor-wise payload bytes | 9,823,452 |
| Descriptor-wise elements | 2,375,934 |
| First/last scalar probes | 11,494 |
| Supported empty views | 0 |
| Inventory pages | 18 |

The partitions reconcile: `5,765 + 1,324 = 7,089` and `5,763 + 2 = 5,765`. The two refused candidates are retained subset refusals, not failed test assertions or an implicit claim that their storage was interpreted. The preregistration intentionally did not require a guessed support count. Other reducers are not additional supported arrays.

The manifest is exactly 1,024 bytes: a 160-byte header plus eighteen 48-byte entries. Its source and map hashes at byte offsets 64 and 96 match the frozen parent and N10 map-manifest hashes. All eighteen stored page hashes match independently computed SHA256 values of the saved pages. Entries 1–17 describe 400 rows / 64,000 bytes each; entry 18 describes 289 rows / 46,240 bytes. This accounts for `17*400 + 289 = 7,089` rows and **1,134,240 total row bytes**. Header/entry reserved bytes inspected in the manifest are zero.

The [replay log](/Users/Shared/micah/Documents/TNN/TNN/Research/R33_NATIVE_N12_RUN_PRIMARY_V1/inventory-replay.stdout:7) contains eighteen successful full-page byte comparisons, correct recorded page extents including the final 46,240 bytes, and a successful full 1,024-byte manifest comparison at lines 69–70. The 74 versus 55 check-count difference is consistent with eighteen additional per-page replay assertions and one additional manifest assertion. It is not missing or duplicated fixture accounting.

Both inventory modes record successful pinned-map loading, accepted-parent identity, full before/after raw-plus-seven-table memory fingerprints, post-inspection identity, and exact -8904 training-admission refusal. These are native-run observations; the independent postrun parent/N10/N11 hash checks corroborate unchanged retained inputs. The frozen accepted identity remains step 60423 and zero newborn restarts; no new state was initialized.

Whole-payload hashing and first/last scalar probes are different evidence. The native run hashes every supported payload, but it does not individually decode every parent element. This reviewer verified inventory page hashes and recorded replay evidence, not every payload by a new decoder. Descriptor totals may double-count shared storage and are not unique physical storage, tensor completeness, parameter counts or semantic-digest equivalence. Replay shows repeatability of this implementation over known material; the independent synthetic oracles provide the separate finite correctness checks.

## Exact package and key evidence identities

| Artifact | SHA256 |
| --- | --- |
| `N12/views.zag` | `1c2717f5fbde4f8308125127cb73fe2de19cf0805bc3eee754b03395dd04a6a6` |
| `N12/driver.zag` | `badf9c5af229ee9f203f0f5599e5a31733e01d446804426c4cf9ece62baa9919` |
| `N12/DESIGN.md` | `11e49bc31be4b087bee38d9db8897b7f72f58afe76119cb5e6f56cabcc4d2a2e` |
| `N12/CONFIG.json` | `ae2c262196d5630660dbacd43f4fad4fd4307098725c470fd701e8ad7d1fd474` |
| `N12/INDEPENDENT_FINAL_REVIEW_V2.md` | `239507a0afe46f815360dc0a4018673583eb40dcc4117a34adbd4107fc4f29bb` |
| `N12/PREREGISTRATION.md` | `142985f42b401836df842893f995558ca5abf5584336e8f910aab46c5050c246` |
| `N12/FREEZE.json` | `100080dee13aa4d1ec18dbd30b005c749c5858d2034bd0a059513d1cb8125621` |
| `N12/ADMISSION.json` | `636bc91f67df5d88db63cb473eba407ad64fd24d2153e0d1de9f8808131b565d` |
| `Research/R33_NATIVE_N12_PINS.sha256` | `6e603e573a1176301db135bea907ca451d1d3916fdc1d3fa59233fc118bf5323` |
| `Research/R33_NATIVE_N12_ADMISSION_PINS.sha256` | `7d452e21687682ab9ef8e72d8355406c8c1771e852ec221ccee94f4e7ae829a1` |
| `RUN/NATIVE_RESULT.json` | `7b14a6ce0699907a80ea8b61586aaa59d6aa469c1b4b556ae2c348841e6d49c9` |
| `RUN/numeric-manifest.bin` | `5e36edf7b13005ed02189f710321c1729f898549da1f21a7a10339859749b595` |
| `Research/R33_NATIVE_N12_LAUNCH.stdout` | `b3414bc7e031aa191bdc5d51d85915fad9c4481ff527a43f961e83fe68848e6c` |
| `Research/R33_NATIVE_N12_LAUNCH.host.stderr` | `5ff4a37a8edca0641f3630afee5e630bd82790741452b5321d2ae31028fbeba1` |
| `RUN/matrix.stdout` | `16b9d7d92cd77fb1a083a3b296c9b744594524c58725b5568ffd3461f884eac4` |
| `RUN/refusals.stdout` | `7d8d2be171536e859e522c827dca02d8f9739463207b8ea6479aa1b0d3b3952d` |
| `RUN/inventory-write.stdout` | `33a91183e607ea4cdf50fdd9379195a2e6dcbc1b1a329a2691a8bf845b2dc32f` |
| `RUN/inventory-replay.stdout` | `24e84aa429798d6b65173b76082d6ba354f6ea3d29f3ea4c29fc186d14c3a478` |

The empty invalid stdout and all five empty child stderrs have SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. The retained postrun verification records are also identified: PINS `5f8fe7390fba58d0659086b2ba4541fba691c896f3e9648b81148d06305f0e91`; N10 `091118302fec9f6167afe263aec19ab790fd3963864600ba0ebf9137853d043a`; N11 `6b750818d304a15bdb023ddb6b70412cfeabc8ffb07df75011957c4b05ae8586`; ADMISSION_PINS `f5ad31aea86937e25c64c9bacfa40e7ba555077901f939a5c7a36fa8602c058b`, all under `Research/R33_NATIVE_N12_POSTRUN_*.txt`.

## Limits and final disposition

The approved trust boundary is unchanged: a live immutable validated map and uniquely owned view/row allocations, with no arbitrary forged-pointer, shallow-copy lifetime, allocator-generation, concurrent-writer or arbitrary-map unique-edge-ownership guarantee. Allocator fault injection and exhaustive failure/leak qualification were excluded. Direct-child supervision and observed RSS are not process-tree containment or production security certification. Current artifact integrity does not independently prove a hostile host could never rewrite its history.

Element strides and all-zero empty strides are N12 conventions, not recovered historical NumPy object layouts. The parent's historical NumPy version and complete original class/method/digest closure remain unresolved. Neither the -8904 refusal nor this engineering pass grants learner authority. Known-parent inventory/replay is not fresh scientific/generalization evidence.

**Confirmed: the recorded, frozen N12 primary supports its bounded numeric-view engineering pass. No contradictory evidence or additional blocking change was identified in this postrun check.** This report does not authorize a rerun, modify the preregistered oracle, approve live registry reconciliation not inspected here, or claim original-method recovery, full tensor/storage migration, training readiness, scientific promotion or R33 completion.
