# N13A POSTRUN Independent Review

Date: 2026-09-06  
Candidate: `R33-N13A / r33-native-n13a-fingerprint-scratch-v1`

## Terminal Disposition

**CONFIRM_BOUNDED_ENGINEERING_PASS**

This disposition is supported by an evidence-only review of the supplied immutable receipts.

This review is **not based on direct filesystem access, fresh hashing, source inspection,
compilation, execution, or rerun activity**. It relies on the owner-supplied immutable
evidence bundle and explicitly preserves the distinction between independently reviewed
evidence claims supplied in receipts, claims that would require direct artifact access or
execution, and claims that remain prohibited.

No experiment, child process, candidate mode, old N13 run, replay, compilation, registry
modification, or source modification was performed by the reviewer.

## Scope and Identity

- Candidate: `R33-N13A`
- Kind: bounded native nonlearning engineering correction
- Primary count: one admitted primary, already consumed
- Frozen input manifest: 335 files, SHA256
  `5ada7db208d347912aaf711cdee732e8915fc2ff80c1ed8327de049e65895cd4`
- Freeze SHA256: `86cc88ca9fa379b723bb6dfb5d43db9641089dcbbac02cae1f162e30ca62ce36`
- Selected `BUILD_03/n13a` SHA256:
  `df5e8bfa67d75c068346f4cc6b636109ccdb3161ac272523359920f0df90d00a`
- `BUILD_04` is reported byte-identical.

Prior source review disposition remains
`APPROVE_FOR_PREREGISTRATION_NO_EXECUTION_AUTHORIZATION`. That approval was not
execution authorization.

## Execution Receipt Review

Supplied launch receipt:

- Session: `85571`
- Interval: `2026-09-06T23:43:00Z–23:43:50Z`
- Exit: `0`
- Terminal marker: `R33_N13A_BOUNDED_TORCH_VIEW_ENGINEERING_PASS`
- Planned children: 6
- Started/reaped children: 6
- Accepted child checks: 24,601
- Final parent CHECK rows: 62
- Parent failures: 0
- Parent checks before result write: 60

Supplied artifact hashes:

- Native result: `b00512373915b52b8ebaf2296d96e2a1389ce1232161216515a147c774a75210`
- Result summary: `701def67c211dc0d4897668e36919aada5be6aa8491241e1be383c8c7db899a7`
- Resource report: `a42febc05474c69dacc868e3481dfc54ddc73641d6e1ba1c5cc47fb58ec6b6ec`
- Launch result: `ba132b7aef273e0189f0ba38991ae967a5ba6c973da919ee08a62cc7adc33a0d`

## Child Results

| Mode | Cases | Checks | Exit | Peak RSS |
| --- | ---: | ---: | ---: | ---: |
| invalid | 0 | 0 | 2 | 1,441,792 |
| hash-controls | 15 | 1,011 | 0 | 37,584,896 |
| matrix | 102 | 8,166 | 0 | 201,736,192 |
| refusals | 123 | 1,059 | 0 | 21,217,280 |
| inventory-write | 1 | 7,168 | 0 | 313,180,160 |
| inventory-replay | 1 | 7,197 | 0 | 316,833,792 |

Reported child properties are started successfully, reaped successfully, no signals,
no timeouts, complete captures, and empty native child stderr. The supplied evidence
distinguishes native child stderr from outer host timing output; `/usr/bin/time -lp`
accounting is not child stderr.

## Resource Review

Frozen RSS ceiling is `402,653,184` bytes. Observed maximum is `316,833,792` bytes,
leaving `85,819,392` bytes of margin. The run therefore remained below the unchanged
resource gate.

Largest reported main-work counters also remained below their frozen limits:

| Counter | Value | Limit |
| --- | ---: | ---: |
| opens | 7,773 | 65,536 |
| records | 4,560 | 327,680 |
| probes | 456 | 16,384 |
| rows | 228 | 8,192 |
| logical_hash_bytes | 131,682,668 | 268,435,456 |
| shape_allocation_attempts | 1,824 | 131,072 |

## N13 Comparison

The consumed N13 failure occurred at the same inventory-write stage at
`409,862,144` bytes. N13A inventory-write observed `313,180,160` bytes. The exact
difference is `96,681,984` bytes.

This supports a bounded regression comparison only. It does not establish exact allocator
attribution, complete causal decomposition, universal memory improvement, or performance
guarantees.

## Inventory and Replay

Reported inventory is 7,089 rows: 228 supported, 0 refused, and 6,861 other reducers.
Supported descriptors comprise 76 storage, 76 tensor, and 76 parameter descriptors, with
76 unique storage nodes, 152 shared references, 456 first/last raw-bit probes, and 0 empty
views. Descriptor totals are 9,738,528 bytes and 2,434,632 elements; unique storage bytes
are 3,246,176.

The output contains 28 pages. Pages 1–27 are 65,536 bytes each and page 28 is 45,312
bytes, giving `27 * 65536 + 45312 = 1,814,784` bytes. The 1,600-byte manifest SHA256 is
`3f56153b9d9e1d6b9c8f3f9af05f8d2f47a88d83bad5d7b91b577c00d0888c33`.

According to the retained native receipts, fresh-process replay regenerated the inventory
and compared every page and the manifest byte-exactly. Operational comparison against the
retained N13 inventory also found N13A pages and manifest equal to N13's unaccepted
inventory. That is regression compatibility only and does not retroactively qualify N13.

## Custody and Verification Receipts

Supplied postrun verification reports:

- 335 frozen source/input pins: OK
- 2 admission pins: OK
- inherited N13: 299 artifacts, 384 source pins, 11 historical closeout entries
- inherited N12: 138 artifacts, 17 historical closeout entries
- total reported postrun verification entries: 1,233
- run + launch manifest: 47 files, SHA256
  `ca92e77953a1966339d235f73087a05048220078b9da01ba697c0e72bfeeb9f8`

These are reviewed as supplied owner receipts, not independently regenerated hashes in
this review.

## Claim Boundaries

R27 remains canonical at step `60423` with zero newborn restarts. R33 training runs remain
zero. This review does not claim learner authority, promotion, semantic-digest
recomputation, original R27 behavior recovery, full parent migration, fresh scientific
evidence, original-method equivalence, allocator fault-injection coverage, hostile-host
security, hard memory isolation, descendant/process-group containment, or training
capability.

N13 remains `FAIL_CONSUMED`. N13A must not be rerun.

## Final Disposition

**CONFIRM_BOUNDED_ENGINEERING_PASS**

Confirmed within the stated evidence boundaries: the admitted N13A primary completed
successfully, all six children completed, frozen resource limits passed, inventory-write
and replay completed, replay matched generated artifacts, the known N13 failure remains
preserved, and no prohibited claim is inferred.

This is a bounded engineering validation outcome, not a promotion, scientific
certification, migration proof, or generalized capability claim.
