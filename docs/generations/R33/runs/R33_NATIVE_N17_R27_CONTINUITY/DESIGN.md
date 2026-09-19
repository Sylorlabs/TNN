# R33-N17 — native R27 continuity qualifier design

Status: **DESIGN COMPLETE; INDEPENDENT REVIEW PENDING; NOT PREREGISTERED; NOT RESERVED; NO EXECUTION AUTHORIZED**.

## Question

Can native Zag reproduce the accepted R27 semantic identity and the required source-defined continuity invariants directly from the already-custodied canonical serialized parent, without executing Python, pickle globals/reducers/classes, historical evaluators or a learner?

This is a continuity/migration qualification, not a training campaign and not an N16 continuation. It allocates no scientific population, mutates no canonical state and cannot promote a checkpoint.

## Immutable inputs

- canonical R27 bytes: 15,871,908 bytes, SHA256 `31e670fcd2a2fefc02a1d032b8016bd93c28844df8ea40889593d030a2096e5a`;
- N10 inert parent-map manifest SHA256 `b7c083364e98d9e5cd674a47b0136de157fedd538b06c743f0c672652984327f`;
- exact original R27 release ZIP SHA256 `7042ff849743c9509586840df865f34423a92f9afc09ef2c7cf937b35b68b65e`;
- recovered source/member hashes in `SOURCE_REFERENCE_INDEX.json` and `SELECTED_ORIGINAL_MANIFEST.sha256`;
- expected semantic witness only: R27 digest `562aaaedb5b9ceec2f50482f631992c247cbe50e9f6d2321b811e311ecf73b04`, retained R26 digest `44d36746ffb9e8d46080376a6e26bb824772d9d4b5e429add404195d02888649`.

The expected digests are comparison witnesses. They may not replace recomputation.

## Existing native substrate to reuse by pin/copy

- N10 inert pickle descriptor/map reader: complete-stream parse with globals, REDUCE, NEWOBJ and BUILD recorded as data only;
- N12 strict numeric views: exact declared serialized numeric-array byte interpretation and fresh replay;
- N13A legacy Torch storage/tensor/parameter views: exact supported raw storage/tensor mapping and fresh replay;
- native SHA-256 and existing supervisor/IO components.

Consumed source roots remain immutable. N17 must pin/copy required code into a new candidate build rather than modify N10/N12/N13A in place.

## Stage A — Python-compatible canonicalization controls

Before real-parent semantic-digest work, native code must implement only the serialization/string rules actually required by the recovered digest sources. The review must pin exact supported input types from the parent/source inventory.

For `json.dumps(..., sort_keys=True[, default=str])`, controls must cover at minimum sorted keys, default separators `, ` and `: `, ASCII escaping behavior, quotes/backslashes/control characters, booleans, null, integers, nested lists/dicts and every float spelling present in the actual digest fields. Unsupported key/value types must fail closed rather than silently approximate Python.

R27 specialist material additionally requires source-equivalent `str(sorted(...))` formatting if a serialized `specialists` attribute is actually present. R26 requires source-equivalent decimal `str(...)` for identifiers/counts/merge threshold and exact `np.float32(...).tobytes()` semantics for the fields identified below.

No host Python oracle is allowed in execution. Known-answer fixtures must be frozen from independently inspected historical specification data before admission.

## Stage B — canonical parent identity and direct invariants

Using the N10 map, rederive and require:

- source raw SHA and map-manifest identity;
- root descriptor `r27_experiments.R27State`;
- exact format `TNN_PRE_V1_R27_GENERAL_LEARNING`;
- development step 60423 and newborn restarts 0;
- exact `r26_sha256` field and R26 nested state identity;
- explicit null `affordance_model` and `speech_motif_decoder`;
- exact accepted-policy locked gates and sole active promotion from separately pinned immutable policy bytes;
- source-defined identity/decision fields selected by the reviewed verifier mapping.

All observations are read-only. A failed identity check terminates with no semantic-continuity gate.

## Stage C — native R26 digest recomputation

The recovered R27 digest calls `base_state.digest()`. The embedded base state is R26, and the recovered R26 digest does not recursively call its own `base_state.digest()`. Therefore semantic-digest closure requires an exact native implementation of the R26 digest source, not an invented recursive lineage digest.

Native R26 recomputation must consume exactly the source-defined material, in source order:

1. `format` bytes;
2. `r25_sha256` bytes;
3. decimal `development_step` bytes;
4. Python-compatible canonical JSON bytes for R26 `architecture` with sorted keys;
5. video encoder base `basis` and `mean` as C-order float32 bytes when present;
6. entity-head state-dict entries sorted by key, key bytes then each tensor converted to float32 bytes as the source does;
7. graph `merge_threshold` decimal-string bytes and every node/view converted to float32 bytes in serialized order;
8. name-memory docs sorted by identity, then motifs sorted by raw motif key, with source-equivalent identity/count strings;
9. abstraction models sorted by tag, centroids sorted by identity, motif weights sorted by motif, weights as exact float32 bytes;
10. speech-segmenter state dict if present. The parent is expected to encode the segmenter as null, but N17 must derive that rather than assume it.

Terminal Stage-C success requires the independently computed digest to equal `44d36746ffb9e8d46080376a6e26bb824772d9d4b5e429add404195d02888649` and all required view/layout operations to be in the reviewed supported subset. A literal insertion of the expected R26 digest is a hard failure.

## Stage D — native R27 digest recomputation

Using the independently recomputed Stage-C digest, consume the R27 source material in exact order:

1. `format` bytes;
2. `r26_sha256` bytes;
3. decimal `development_step` bytes;
4. recomputed R26 digest ASCII bytes;
5. for category head, entity head and affordance model: if `.net` exists, state-dict entries sorted by key with key bytes followed by raw source-equivalent tensor bytes (`detach().cpu().numpy().tobytes()` semantics); null/absent paths contribute no bytes;
6. source-equivalent sorted semantic-specialist identifier string if `specialists` exists;
7. Python-compatible sorted-key/default-str JSON bytes for `architecture`;
8. Python-compatible sorted-key/default-str JSON bytes for `evidence`.

Terminal digest success requires exact equality to `562aaaedb5b9ceec2f50482f631992c247cbe50e9f6d2321b811e311ecf73b04`. The expected digest may be read only after the preimage has been fully constructed/finalized, or equivalent frozen comparison separation must be demonstrated in review, so the implementation cannot silently substitute the witness.

## Stage E — verifier-semantic coverage matrix

`VERIFY_CONTRACT.md` is the source-derived inventory. Before preregistration, independent review must convert it into an exact machine-readable check matrix with each item labeled `DIRECT_NATIVE_RECOMPUTATION`, `NATIVE_EQUIVALENT_REQUIRES_REVIEW`, `HISTORICAL_WITNESS_ONLY` or `DEFERRED_BLOCKER`.

No `FULL_NATIVE_R27_CONTINUITY_QUALIFIED` outcome may exist while a reviewer-designated required item is `DEFERRED_BLOCKER`, while a native-equivalent justification remains unresolved, or merely because the historical 33/33 receipt is present.

Digest equality alone may support a narrower `R27_SEMANTIC_DIGEST_REPRODUCED_NATIVE` result, but never automatic behavioral-continuity or promotion claims.

## Negative controls required before any admission

The exact preregistration must freeze independently authored negative fixtures that exercise at least:

- one changed canonical-parent/raw-map identity byte;
- changed R27 format, development step and newborn-restart count separately;
- changed R26 raw SHA linkage;
- one changed R26 digest preimage subcomponent;
- JSON key-order, separator, escaping and actual-parent float-format perturbations;
- one state-dict key-order or tensor-byte perturbation for each active head family actually present;
- specialist-list ordering/string perturbation if specialists are present;
- removal/change of a required locked gate;
- change/addition/removal of the sole active promotion;
- semantic-generator identity/retention perturbation if that invariant is admitted as directly representable;
- N10 map-manifest/page tamper;
- replacement of the recomputed R26 digest with the historical witness literal, which must be detectable as an invalid code/config path rather than accepted continuity.

Each negative is a fixed engineering/control case, not a tunable search. Failures are retained; no threshold relaxation or control deletion after exposure.

## Execution/custody protocol if review eventually approves preregistration

1. Independent review first. Allowed dispositions are `REQUEST_CHANGES` or `APPROVE_FOR_PREREGISTRATION_ONLY_NO_EXECUTION_AUTHORIZATION`.
2. Only after approval: create exact preregistration, reservation and fresh candidate source/build identities. No scientific populations are required because this is a deterministic parent-continuity qualification, but invocation consumption still applies.
3. Freeze exact source/config/design/review/reference/compiler/binary and N10/N12/N13A input pins.
4. Create a separate admission for exactly one primary continuity invocation. First actual invocation consumes it regardless of outcome.
5. Execute once under the native supervisor; preserve complete stdout/stderr/timestamps/exit/resource receipts and immutable artifact hashes.
6. No retry, retune, code repair, expected-value change or negative-fixture change after the admitted invocation. A failed consumed candidate requires a new identity.
7. Independent postrun review before final disposition.

## Forbidden claims and actions

- no Python execution, `pickle.load`, reducer/global/class invocation, `torch.load` or hidden foreign evaluator;
- no historical `verify_r27.py`/`verify_r26.py` rerun;
- no N16 rerun or population reuse;
- no learner update, canonical R27 mutation, authority grant or promotion;
- no substitution of historical digest/receipt literals for recomputation;
- no activation of serialized graph/BPE/VAD mechanisms merely because their historical objects are retained in the parent;
- no claim of complete mutable-state migration, behavioral equivalence, consciousness, production readiness or R27 superiority from a narrower digest result.

## Success ladder

The protocol must report the narrowest achieved level:

1. `R27_NATIVE_IDENTITY_RECONFIRMED`
2. `R26_SEMANTIC_DIGEST_REPRODUCED_NATIVE`
3. `R27_SEMANTIC_DIGEST_REPRODUCED_NATIVE`
4. `R27_REQUIRED_VERIFIER_INVARIANTS_REPRODUCED_NATIVE`
5. `FULL_NATIVE_R27_CONTINUITY_QUALIFIED`

Higher levels require every lower level plus the independently reviewed requirements for that level. None is achieved by this design document itself.

## Review-correction artifacts

Following independent review V1, N17 now carries
`PARENT_TYPE_INVENTORY_SCHEMA.json`, `VERIFIER_CHECK_MATRIX.json` and
`R25_LINEAGE_REQUIREMENTS.md`. These are deliberately marked unpopulated or
draft. They prevent the identity-only authoring binary, historical 33/33
receipt, or retained digest witnesses from being mistaken for a complete native
continuity implementation. The actual type inventory, exact check expansion,
R25 input hashes, known-answer fixtures, negative controls and native runtime
closure must be completed and independently reviewed before preregistration.

## 2026-09-09 authoring closure artifacts

This package now carries a partial evidence register and explicit implementation
decision, a root/source type-layout inventory, an expanded 33-slot effective-scope
matrix, a static R25 lineage record, the proposed native runtime ABI, and separate
known-answer and negative-fixture specifications. These artifacts advance the
authoring boundary without claiming that the missing selectors, numeric layouts,
R25 bytes, or native-equivalent behavioral checks exist. `AUTHORING_ARTIFACTS.sha256`
verifies the new fixture, inventory and lineage artifacts.

The digest/verifier implementation remains deliberately absent. The exact reason
is recorded in `IMPLEMENTATION_DECISION.md`: a guessed preimage or a literal
historical witness would be invalid continuity evidence. No file in this package
changes that execution or claim boundary.
