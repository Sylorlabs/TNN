# R33-N13 consumed failure: inventory memory ceiling

Status: FAILED_RESOURCE_GATE; sole primary consumed and independently confirmed.
Postrun artifact custody is indexed separately in R33_NATIVE_N13_ARTIFACT_INDEX.json.
No retry, standalone replay or frozen-source change is allowed.

The approved BUILD_05 binary executed once after preregistration, unique
reservation,384 verified input pins and separate launch admission. The original
native command session72555 settled exit1/chunk3e3256. Retained UTC interval:
2026-09-06T22:27:14Z through22:27:45Z. Outer elapsed31.67s.

## Actual acceptance and failure

| Child | Exit | Cases | Reported checks/failures | Observed RSS bytes | Disposition |
|---|---:|---:|---:|---:|---|
| invalid | 2 | 0 | none | 1392640 | Accepted silent invalid mode |
| matrix | 0 | 102 | 8166/0 | 218349568 | Accepted |
| refusals | 0 | 123 | 1059/0 | 29868032 | Accepted |
| inventory-write | 0 | 1 | 7168/0 | 409862144 | Rejected by frozen RSS ceiling |
| inventory-replay | not launched | not executed | none | unmeasured | Withheld after failure |

The inventory process exceeded402653184bytes (384MiB) by7208960bytes
(6.875MiB). Its zero exit and child PASS do not override that resource failure.
All four launched children were started/reaped, with zero signals and empty
stderr. Native capture sizes were0/255462/38637/208868bytes, all below1MiB.
The supervisor retained only9225 accepted child checks; the rejected inventory's
7168 checks are not credited. Of42 parent check rows, two mismatch: RSS bound
and completion of all five children. Native result publication and root close
succeeded, but no terminal parent PASS was emitted. The sole primary failed.

## Retained inventory observations, not qualified replay

The rejected inventory child wrote28 pages and a1600-byte manifest. It reported
7089 REDUCE rows:228 candidates,228 supported,0 refused,6861 other reducers;
76 storage/76 tensor/76 parameter views,76 unique serialized storage nodes and
152 shared references. Descriptor-wise payload9738528bytes/2434632elements;
unique-storage-node payload3246176bytes;456 first/last probes;0 empty views.
Manifest SHA2563f56153b9d9e1d6b9c8f3f9af05f8d2f47a88d83bad5d7b91b577c00d0888c33.
These are retained observations of the failed attempt, not a passed inventory,
fresh-process replay, original-method oracle or complete parameter census.

Main nonreset work counters (opens/records/probes/rows/logical-hash-bytes/shape
allocation attempts): matrix1207/6040/930/88/15260294/2386;
refusals76/315/1/1/7959872/32;
inventory7773/4560/456/228/131682668/1824. These are bounded API counters,
not total-process work or all allocations; isolated budget controls are separate.

## Preservation and next dependency

After settlement,384 input pins,2 admission pins and673 inherited entries all
verified:1059 lines with empty corresponding stderr. The encompassing shell
command subsequently exited1 only because an unrelated source-read path
evaluator.zag did not exist in N12; no hash check failed and no test was rerun.
The actual N12 source listing was then inspected. Historical source/oracle/result
bytes, canonical parent and immutable closeout snapshots remain unchanged.

R27 remains canonical at60423/restarts0. Diagnostic count25, training0;
no learner authority, promotion, original behavior or scientific qualification.
Keep the frozen384-entry manifest and admission pins unchanged. Euler's terminal
postrun review confirms FAIL_CONSUMED -- INVENTORY_WRITE_RSS_LIMIT_EXCEEDED.
Report SHA256f5ffe72118bcacae5d21f1b4db810d952db7c9c51c8e8b108e59a837ebb19dfa.
It confirms the accepted counts, unlaunched replay, retained inventory integrity
and failure containment. No experiment was rerun by the reviewer.

The pinned compiler's actual commit source lowers _zag_free to a no-op and uses
non-reclaiming bump arenas. Repeated header-map and whole-message SHA allocations
therefore accumulate until process exit. The review identifies140083200bytes of
requested header tables and131682668 logical bytes copied by evaluator hashes,
including110333672bytes across two parent fingerprints. These are source-level
allocation extents, not a byte-exact RSS decomposition or measured savings.
See R33_N13_POSTRUN_MEMORY_DIAGNOSIS/DIAGNOSIS.md. A corrective N13A must preserve
the SAME384MiB ceiling, independent byte oracles and known-evidence regression
attribution, and undergo independent exact-source review before registration.

Original class/method/digest/verifier/dependency recovery, source-grounded native
behavioral continuity, full sensory/telemetry/authority and later scientific
work remain open. N13 failure is not evidence that the whole R series is done.
