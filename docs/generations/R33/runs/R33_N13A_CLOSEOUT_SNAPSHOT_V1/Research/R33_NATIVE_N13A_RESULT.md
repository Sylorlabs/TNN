# N13A fingerprint-memory corrective regression result

Status: **NATIVE BOUNDED ENGINEERING PASS; INDEPENDENT POSTRUN REVIEW PENDING.**
Identity: r33-native-n13a-fingerprint-scratch-v1. Exactly one primary executed.
This is known-evidence storage/fingerprint engineering, not fresh science,
original behavioral continuity, full parent migration, training or R33 completion.

## Execution, acceptance and counts

Selected approved BUILD_03/n13a supervise ran once,2026-09-06T23:43:00Z to
23:43:50Z. Original session85571, initial chunk90c120, terminal chunke29673,
exit0. Outer elapsed50.37seconds. Its result publication and root close passed,
followed by R33_N13A_BOUNDED_TORCH_VIEW_ENGINEERING_PASS.

| Child | Cases | Accepted checks | Exit | Observed peak RSS bytes |
|---|---:|---:|---:|---:|
| invalid | 0 | 0 | 2 | 1441792 |
| hash-controls | 15 | 1011 | 0 | 37584896 |
| matrix | 102 | 8166 | 0 | 201736192 |
| refusals | 123 | 1059 | 0 | 21217280 |
| inventory-write | 1 | 7168 | 0 | 313180160 |
| inventory-replay | 1 | 7197 | 0 | 316833792 |

All6children started/reaped with supervisor status0, no timeout/signal/native
stderr and complete captured output. Each satisfied the unchanged402653184-byte
observed RSS ceiling and fixed deadline/capture/finite-case checks. The invalid
child was silent as expected. Five work children reported zero failed checks and
their terminal markers. Counts are24601accepted child checks/242grouped cases,
plus62parent CHECK rows with zero mismatches. Native JSON reports60checks BEFORE
result-write/close; the final62includes those two. No rejected child is credited.
The new hash child's1011checks match independent pre-execution source arithmetic.

Retained native result SHA256:
b00512373915b52b8ebaf2296d96e2a1389ce1232161216515a147c774a75210.
Full original-command receipts and output are in R33_NATIVE_N13A_LAUNCH_PRIMARY_V1;
child outputs, complete inventory and native result are in
R33_NATIVE_N13A_RUN_PRIMARY_V1. R33_NATIVE_N13A_LAUNCH_RESULT.json records the
actual settled tool evidence; it is an owner receipt, not a signed OS attestation.

## Exact inventory and fresh-process replay

Both inventory processes reported7089REDUCE rows:228supported candidates,
0refused candidates and6861other reducers. Supported descriptors comprise
76storage,76tensor and76parameter views, with76unique serialized storage-node
identities and152shared references. Descriptor-wise totals are9738528bytes and
2434632elements; unique storage-node bytes3246176. There were456first/last raw-bit
probes and0empty views. These describe the declared format subset, not every
runtime parameter or original inference/update behavior.

The28pages contain27*65536+45312=1814784bytes,7089*256exact row bytes.
The1600-byte R33TS001 manifest SHA256 is
3f56153b9d9e1d6b9c8f3f9af05f8d2f47a88d83bad5d7b91b577c00d0888c33.
A separately launched fresh replay process rederived and compared every page
and manifest byte. Complete input/seven-table fingerprints matched before/after,
parent identity remained valid, and training admission returned-8904 in both.

Operational postrun byte comparisons also found all28pages and the entire
manifest identical to N13's preserved UNACCEPTED inventory. That is disclosed
known-evidence regression compatibility, not retroactive qualification of N13.
The228count was not selected as a new success oracle after its earlier exposure.

## Memory and resource result

Inventory-write observed313180160bytes (298.671875MiB), versus409862144bytes
(390.875MiB) in N13's failed same stage:96681984bytes/92.203125MiB lower in this
single comparison. The maximum across all new children was316833792bytes
(302.15625MiB), leaving85819392bytes/81.84375MiB below the unchanged384MiB cap.
This is measured per-process RSS, not a per-allocation trace, replicated speed/
memory study or proof that all other accumulation has been eliminated.

Source accounting predicted2944bytes of new output/scratch requests for two
fingerprints instead of copying110333672logical input bytes. That prediction
is not substituted for measured RSS. The same pinned compiler still retains
bump allocations. Reader/header, row/page/loader hashes and their cumulative
allocation mechanisms remain unchanged. No cap increase, cache, global allocator
reset, new free implementation or hidden foreign hash was used.

Native aggregate child CPU48818521microseconds; optional summed child wall
50004878microseconds. See R33_NATIVE_N13A_RESOURCE_REPORT.json for per-child
timing/captures and six main work counters. Every logged main account is within
its fixed limit; low-budget control accounts and inherited loader work retain
their declared separate scopes. Comparing total50.37seconds with failed N13's
shorter schedule would not be a matched speed comparison.

## Custody, failures and remaining closeout

POSTRUN/source-pins verifies335frozen files and admission-pins verifies2.
Additional checks verified N13's299artifacts/384source pins/11historical closeout
entries and N12's138artifacts/17historical closeout entries. The47retained native
run/outer-launch files were hashed and reverified. Total1233postrun verification
entries, all corresponding stderr empty. Run/launch manifest SHA256:
ca92e77953a1966339d235f73087a05048220078b9da01ba697c0e72bfeeb9f8.
The original parent and all153map files are included in the335frozen inputs.

No native test failed in this primary. Historical N13 failure, rejected N13/N13A
builds, reviewer initialization/coordination issues and the68-byte erroneous
N12-closeout path lookup remain retained; the corrected lookup did not overwrite
its error. N13A is now consumed and may not rerun. Independent postrun review,
complete artifact index/manifest and final historical closeout remain pending.

Canonical R27 is unchanged at60423/restarts0. Diagnostics26, R33training0,
no learner authority or promotion. Original source/digest/verifier dependencies,
complete behavioral/mutable-state migration, end-to-end sensory/telemetry/
protected authority and subsequent scientific stages remain open. Finite trusted
slice/owner scope only; no actual OOM injection or hostile-host security claim.
