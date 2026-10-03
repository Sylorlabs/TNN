# R33-N17 independent review V4 — after manifest repair

Review date: 2026-09-09

Disposition: **REQUEST_CHANGES**.

This is an independent, read-only review of the N17 packet after the V3
manifest-repair work. It covers `DESIGN_PACKET.sha256`, V3, the populated
partial parent inventory, the 33-row verifier matrix, the R25 lineage record,
known-answer and negative fixture specifications, the evidence register,
runtime boundary, status, source index and the authoring/correction manifests.

No binary, Zag source, Python, pickle, N16 artifact or historical verifier was
executed. No canonical state, registry, global state or experiment state was
modified.

## Decision

The packet is not preregistration-ready and is not native R27 continuity
qualified. The V3 whole-packet manifest finding is resolved: every entry
listed in `DESIGN_PACKET.sha256` passes when checked from the repository root,
including the Work Package A artifacts. All packet JSON files also parse.
That repair does not close the substantive continuity gates below.

## Findings

### F1 — R25 lineage is still absent and terminal

`R25_LINEAGE_RECORD.json` remains
`STATIC_MEMBER_HASH_LEADS_ONLY_DEFERRED_BLOCKER`. All four required artifacts
are still `MISSING`, with null member paths, sizes and SHA-256 values:

- accepted R25 state;
- R25 release manifest;
- accepted R25 policy; and
- R25 root receipt.

The exact `r26_r25_sha256` map selector is still pending, and the record says
the available historical R25 source members are not available in N17. The
R26 raw-link, R26 digest-link, R25 receipt and R27-to-R26 lineage rows cannot
therefore be recomputed natively.

### F2 — Parent inventory is populated only partially

`PARENT_TYPE_INVENTORY.json` contains 14 entries, but its status remains
`PARTIAL_ROOT_AND_SOURCE_INVENTORY_NUMERIC_AND_R25_LAYOUTS_BLOCKED`. The
entries still lack complete, individually hashed closure for the exact map
selectors, container/type layouts, key and source ordering, numeric dtype,
shape, byte order and spans, null-versus-absent branches, and digest role.
The unresolved areas include R27 category/system, affordance/speech,
abstraction/policy, semantic generator, architecture/evidence, R26 numeric
objects, state dictionaries, graph and name-memory/string records, optional
speech state, and R25 lineage.

This is not sufficient to define a trustworthy native digest preimage or
native verifier input boundary.

### F3 — The 33-row matrix is not native qualification evidence

`VERIFIER_CHECK_MATRIX_V2.json` has 33 historical effective rows but
`native_count` is null and the status is
`EXPANDED_EFFECTIVE-SCOPE_MATRIX_NOT_QUALIFICATION`. Three rows are
`EXPECTED_VALUE_ONLY`; the remaining 30 are blocked or pending, including:

- 8 `BLOCKED_RUNTIME` rows;
- 5 selector blockers;
- 9 policy-input hash-pending rows;
- 2 R26-digest blockers;
- 1 null-branch blocker;
- 1 manifest-input hash blocker; and
- 3 source-line-accounting rows.

The historical 33/33 receipt is expressly excluded from native evidence.
Exact native or reviewed native-equivalent implementation and fixture-backed
accounting remain unresolved.

### F4 — Fixtures remain specifications, not frozen evidence

`KNOWN_ANSWER_FIXTURE_SPEC.json` contains 13 specified fixtures and remains
`SPECIFIED_NOT_FROZEN_NOT_EXECUTED`. Its entries still depend on pending
selectors, actual parent layouts, runtime behavior or historical witnesses.

`NEGATIVE_FIXTURE_SPEC.json` contains 20 specified fixtures and remains
`SPECIFIED_NOT_FROZEN_NOT_EXECUTED`. Mutation selectors/offsets, baseline and
mutated hashes, exact refusal codes and canaries are not frozen for the
blocked parent fields, policy inputs, promotion controls and R25 inputs.

These specifications establish intended safeguards but cannot establish
continuity or authorize preregistration.

### F5 — Native runtime and semantic equivalence remain unqualified

`EVIDENCE_REGISTER.json` marks `native-r27-runtime` as `UNQUALIFIED` and
`exact-verifier-accounting` as `DRAFT_ONLY`. `PARENT_RUNTIME_BOUNDARY.md`
does not establish a qualified native reader/evaluator for the actual parent.
Native canonical JSON/string/float32 behavior, tensor/state-dict traversal,
explicit refusal behavior, resource bounds, and known-answer execution on the
actual R27/R26/R25 inputs are still absent.

`IMPLEMENTATION_DECISION.md` correctly concludes that no digest/verifier
implementation is justified while the exact preimage, lineage inputs and
native canonicalization semantics remain unresolved.

### F6 — Supporting correction manifest is inconsistent

The repaired `DESIGN_PACKET.sha256` passes all of its listed hashes. However,
`CORRECTION_ARTIFACTS.sha256` still reports two failures:

- `SOURCE_REFERENCE_INDEX.json`; and
- `STATUS.json`.

This does not invalidate the read-only findings above, but the correction
manifest itself is not an integrity-clean, final packet manifest and must be
regenerated after the packet state is finalized. This review file is also new
and is not included in the pre-review design manifest.

### F7 — Status correctly forbids progression

`STATUS.json` remains consistent with a non-executed authoring candidate:

- registered, preregistered, reserved, frozen, admitted and executed: false;
- authoring build compiled: true; authoring build executed: false;
- scientific exposure: 0;
- Python, pickle and reducer execution: false;
- canonical mutation: false;
- learner authority and promotion: false; and
- digest/verifier implementation: not justified.

This status is correct and provides no basis for preregistration, admission,
execution or a continuity claim.

## Checks performed

- `DESIGN_PACKET.sha256`: all listed entries passed from the repository root.
- `AUTHORING_ARTIFACTS.sha256`: passed.
- `CORRECTION_ARTIFACTS.sha256`: failed only for `SOURCE_REFERENCE_INDEX.json`
  and `STATUS.json`.
- All JSON files in the N17 directory parsed successfully with `jq empty`.
- No binary, Zag, Python, pickle, N16 or historical verifier execution.
- No canonical, registry, global or experiment-state mutation.

## Required changes before another review

1. Supply and individually hash the four R25 artifacts, then bind the exact
   native map selectors and linkage fields.
2. Complete every required parent inventory entry, including exact layouts,
   ordering, null/absent branches, digest roles and input hashes.
3. Close every verifier row with native or reviewed native-equivalent
   semantics; do not count historical witness values as native passes.
4. Freeze and bind all known-answer and negative fixtures, including exact
   refusal codes, mutation selectors, canaries and actual parent inputs.
5. Qualify the native parent reader/evaluator and its canonicalization,
   refusal and resource-bound behavior.
6. Regenerate and independently review the correction/final packet manifests,
   including this review, before any preregistration decision.

Until those changes are independently reviewed, the narrowest valid status is
authoring-only, not preregistration-ready, and not continuity-qualified.

