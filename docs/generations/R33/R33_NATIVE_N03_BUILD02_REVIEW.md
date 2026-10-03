# R33-N03 BUILD02 independent native journal review

Review date: 2026-09-05 (America/Los_Angeles).

Scope: bounded independent static source/API/falsifier review only. I did not execute or
compile N03, did not run Python, and did not edit journal/driver/boundary sources,
registries, freezes, results, accepted state, or any prior review. The preserved N01B
BUILD02 result is treated only as external executed dependency evidence for the exercised
PROCESS_V3 direct-child lane; it is not N03 evidence.

## Exact reviewed identities

- `Research/R33_NATIVE_JOURNAL_V1.zag` — SHA-256
  `a97f80ad9b4e40de9da25c209469d95b083eff55430018e1729edaa56f8b94ef`
- `Research/R33_NATIVE_N03_DRIVER.zag` — SHA-256
  `660d38066c4834667dee4993749dc94178a334f51c5b90de64da7e62c76af8c0`
- `Research/R33_NATIVE_N03_BOUNDARIES.zag` — SHA-256
  `f0d3da7cc44285f6dcd26d0aef733c738c963021e253164d67f14c7a85aa1a36`

Context identities inspected:

- `Research/R33_NATIVE_PROCESS_V3.zag` —
  `04c5bc6c3c7222786ab5c6d9af384935c9dd533a6a89046860da0c67ffcb2f89`
- frozen `Research/R33_NATIVE_IO_V1.zag` —
  `b9160ff94caf1565360c99ac1144b514836dc34227f97e2a152c541ec6280d2e`
- corrected `Research/R33_NATIVE_SHA256_V2.zag` —
  `9824f6db66a943917dbc7cd5e6862ab0967b7ea83161cfc357bb7d17ca683bcf`
- preserved prior review `Research/R33_NATIVE_N03_REVIEW.md` —
  `52ca9764dd08396a4b2594422a7e3a62b8d6718d6d8bc19f75615ae498a76fa6`
- executed dependency report `Research/R33_NATIVE_N01B_RESULT.md` —
  `445f135ec068192e7a7df4b503c70b11c7ccab66b97d55c659a9cec5555ba8b9`

## Verdict

**BUILD02 is substantially better aligned with the frozen N03 review, but I would not
freeze a broad “all recovery integrity failures are explicitly and correctly classified”
claim on this source yet.** The publication/recovery design remains coherent by source
inspection and the 58-child schedule is now a strong engineering regression set for the
stated trusted-operator/process-death scope. The main remaining source defect is error
attribution inside event validation; the main test confound is that the retained-attempt
byte oracle reuses journal helpers under test.

No N03 runtime result exists from this review. A clean compile is not execution evidence.

## Strongest criticism — event validation still conflates primitive failure with corruption

`nj_validate_record` fails closed, but lines 101-103 collapse two different conditions
into the same integrity statuses:

- `ns_sha256(j.state, hash) != 0` is reported as `-8004`, the same as a before-state
  digest mismatch;
- `ns_sha256(payload, hash) != 0` is reported as `-8003`, the same as an after-state
  digest mismatch;
- `nj_record_digest(record, hash) != 0` is also reported as `-8003`, the same as a
  record-digest mismatch.

Therefore the new root-head diagnostic seam closes the exact prior R1 defect narrowly,
but it does **not** establish general fail-explicit cause attribution for all recovery
hash/digest operations. An allocation/SHA execution failure during event replay can be
misreported as journal corruption. State is still withheld, so this is not a fail-open
integrity bug; it is a semantic/API classification defect.

There is a related narrower case before the new seam: `nj_root_record(initial)` performs
its own SHA operation and returns an empty slice on hash failure; recovery then maps an
empty expected root to `-8002`. Thus the explicit `fault=1` seam tests the subsequent
root-head hash (`ns_sha256(expected, j.head)`), not every SHA failure reachable during
root reconstruction.

### Recommended architecture change

Separate primitive execution status from digest comparison everywhere:

1. call SHA/digest helper;
2. if the helper returns nonzero, return the operational failure class (`-8008` or a
   dedicated hash-operation status);
3. only after a successful helper call compare bytes and return `-8003/-8004` for an
   actual integrity mismatch.

Keep diagnostic seams failure-only. Add bounded native fault seams for root-record SHA,
before-state SHA, after-state SHA, and record-digest execution so each proves no state,
head, transactions, root, or lock escape on failure.

## Main confound — exact attempt oracle is not fully independent

The new attempt-length/prefix checks materially improve the old partial-write fixture.
They now verify phase-1 length 0, phase-2/checked-partial length 88, and full-record length
176 against retained attempt bytes.

However `n03_attempt_bytes` calls both `nj_root_record(initial)` and
`nj_record_digest(expected, ...)`, i.e. two helpers from the journal implementation being
tested. Header fields and payload bytes are assembled explicitly, and SHA256_V2 is a
separately qualified dependency, but a shared defect in root-record construction or
record-digest coverage can self-confirm in producer and oracle.

For a stronger “exact bytes” claim, construct the 80-byte root record and the digest input
independently in the driver from literal field offsets, then call only the separately
qualified SHA primitive. Alternatively preregister literal expected digests for the fixed
16-byte fixture. Until then, call this a strong implementation-regression oracle rather
than an independent wire-format oracle.

## Duplicate-path limitation

The prior duplicate-I/O classification defect is substantially corrected:

- failed event open defaults to `-8008`;
- short/extended read becomes `-8001` through exact-size I/O;
- payload/record integrity mismatch becomes `-8003`;
- only a semantically different but readable valid duplicate remains `-8007`.

Boundary modes 20-22 directly exercise corrupt payload, invalid root/open failure, and
truncation. That is adequate for the stated regression claim.

One stronger claim remains unqualified: `nj_duplicate_status` validates payload digest
and whole-record digest, but does not compare the stored prior-head field or before-state
digest to an independently known historical chain state. A same-user actor that mutates
those fields and reseals the unkeyed record digest after the live handle has recovered can
still reach idempotent status if the payload/transaction/parent/kind match. This is within
the design's explicitly excluded resealing/same-user-adversary domain, so it need not block
the trusted-operator N03 lane. If broader duplicate integrity is desired, add a resealed
prior-head/before-state mutation falsifier on an already-open handle and either replay the
historical chain before returning idempotent or make the immutability assumption explicit
in the API contract.

## Disposition of the frozen review findings

### Prior capacity/file-size mismatch — prospectively addressed

The driver now applies a 128 KiB regular-file ceiling and PROCESS_V3 is called with a
128 KiB child output/file limit. A 65,536-byte state produces a 65,600-byte root and
65,696-byte transaction record, both below that ceiling. Boundary 2 checks exact file
sizes and same-process reload, and `max-reload` adds a fresh-process recovery of that
maximum fixture. This is a correct falsifier shape; it becomes evidence only after the
frozen N03 primary executes.

### Prior root-head unchecked SHA — narrowly addressed

Recovery now checks the root-head SHA return and exposes no operational handle on failure.
Boundary 5 uses an explicit failure-only diagnostic seam and then verifies ordinary
recovery still succeeds. The broader event-hash classification issue above remains.

### Prior partial-write ambiguity — addressed for the injected seam

Crash/partial mode now checks both the exact write count and sync result. Deliberate
checked abandonment returns `-8011` only after the intended partial prefix was written and
synced; real I/O failure returns `-8008`. The driver independently reads the retained
attempt and checks the expected length/prefix, then requires recovery before retrying the
original transaction ID. This closes the prior “reservation existed but partial bytes may
not have been written” confound for the exercised fixture.

### Prior alias ambiguity — addressed

`nj_commit` rejects overlap between caller `next` and journal state/head/transaction
storage with `-8010`. `nj_copy` permits exact in-place identity but refuses partial
overlap. Boundary 17-19 exercise state/head/transaction aliasing, partial-overlap refusal,
no mutation, exact in-place copy, and disjoint copy.

### Prior rollback wording — corrected

The driver now names the kind-2 case as an append of initial bytes that is **not an
authorized rollback**. Source still treats `kind=2` as a trusted label, which is consistent
with the generic opaque-snapshot scope.

### Prior failed-attempt provenance limitation — still intentionally present

Recovery still treats unpublished attempts as persistent reservations and validates only
presence/regular-file/size envelope, not content hashes or transaction binding. Selected
crash/partial fixtures now check actual retained bytes, but that does not convert the
generic attempt namespace into cryptographically verified provenance. Keep the original
claim boundary.

## Falsifier adequacy

The 58-child shape is coherent by source inspection: the prior 25 scenario shape is
retained, 32 boundary modes are added, and one separate maximum-size reload is added.

The new boundary schedule covers the most important omissions from the frozen review:

- payload lengths 1, 65,536, 0 refusal, and 65,537 refusal;
- maximum root/event exact file sizes plus fresh-process reload;
- injected root-head hash failure;
- wrong initial oracle, truncated/extended/root-byte corruption;
- partial initialization and repeated initialization refusal;
- event/attempt gaps and event-33/attempt-65 overflow presence;
- state/head/transaction alias refusal and generic overlap behavior;
- duplicate corrupt/read-I/O/truncation classification;
- truncated/extended event, magic, length, kind, reserved field, after-hash, transaction
  zero/high-bit malformed cases;
- duplicate transaction ID in a resealed two-record recovery chain.

The frozen IO helper's `nio_read_exact` first obtains file size and rejects growth beyond
the requested maximum, so the extended-root and extended-event cases are valid exact-size
falsifiers rather than prefix-read false positives.

### Highest-value missing falsifier

Add failure-only injection at each hash/digest execution site in `nj_validate_record` and
require an operational failure status rather than `-8003/-8004`, with the standard
no-state/no-head/no-transactions/no-root/no-lock postcondition. This directly tests the
strongest remaining source defect.

Secondary, only if a stronger live-handle integrity claim is wanted: mutate and reseal a
published duplicate's prior-head or before-state digest after recovery, then verify the
duplicate path does not return idempotent success.

## Literal-oracle / compiler-interface review

I found no imported numeric status constant used as an expected assertion oracle in the
reviewed N03 driver/boundary logic. Expected statuses are literal numeric values or local
`i32` variables initialized from literals. That avoids the pinned imported-top-level-const
failure demonstrated by frozen N01P. This is a source property, not N03 execution evidence.

String constants such as `N03_ROOT` are not part of that numeric-oracle hazard.

## Resource and side-effect scope

The 128 KiB change fixes the earlier per-file envelope mismatch but must not be described
as a general storage quota:

- `RLIMIT_FSIZE`/PROCESS_V3 bounds individual regular files, not aggregate bytes in the
  N03 run tree;
- the parent supervisor deadline applies to the direct child; N01B supports that exercised
  direct-child mechanism, not descendant/process-group containment;
- `peak_rss <= 256 MiB` in the driver is an observed-value assertion, **not a hard RSS
  limit**;
- the outer parent guard and child guards are fail-safes, not proof of hostile-runtime
  containment;
- no chroot/sandbox, network denial, total-disk quota, or same-user mutation protection is
  supplied by these three journal sources;
- boundary mutation helpers operate on the dedicated N03 fixture tree and retain preimage
  files, but that is source-scoped evaluator discipline, not kernel-enforced write
  isolation.

The N03 run should therefore be described as bounded native engineering fixtures over a
fixed reviewed write tree, not as a filesystem/process security certificate.

## What not to claim

Even if the future sole N03 primary passes all 58 children, do not claim:

- all SHA/allocation/I/O failure causes are precisely classified until event-validation
  primitive-failure paths are separated and falsified;
- the attempt-byte oracle is implementation-independent wire-format certification;
- unpublished attempts have generic content integrity, authenticated provenance, or an
  explicit event-to-attempt transaction binding;
- live duplicate handling resists same-user resealing or hostile concurrent mutation;
- power-loss, storage-controller, APFS crash durability, or hardware persistence;
- signed/authenticated authority, tamper resistance, trusted timestamps, operator identity,
  or rollback authorization;
- hard RSS containment, aggregate disk quota, descendant/process-group containment,
  network sandboxing, or whole-runtime security isolation;
- full-brain/checkpoint completeness, sensory S0/S1 lineage, learner cognition, training,
  promotion, grant change, dominance, or R33 completion.

## Precise claim boundary

If the frozen BUILD02 identity later executes all 58 children as preregistered, the
defensible claim is a **native macOS trusted-operator opaque-snapshot journal engineering
regression** covering the exercised exact-size envelope, process-death publication
boundaries, fresh recovery, selected partial-attempt bytes, bounded capacities,
alias/overlap rejection, selected malformed/corrupt records, duplicate transaction
handling, and direct-child supervision. That remains process-crash engineering evidence,
not power-loss durability, adversarial integrity, scientific learning evidence, or a
whole-runtime certificate.
