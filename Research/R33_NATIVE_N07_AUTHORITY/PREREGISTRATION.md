# R33-N07 — native authenticated control ledger, bounded engineering

Identity: `r33-native-n07-authenticated-control-ledger-v1`. One sole primary,
37 top-level supervised children and one explicitly nested lock contender:
38 child processes total. No scientific data, learner, real human grant,
accepted-parent use, canonical mutation, training, or promotion.

## Hypothesis, changes and evidence identity

A native supervisor-core candidate can authenticate exact request/candidate
bytes, bind the instance and current state/policy, serialize cooperating writers,
retain consumed nonces/resource charges across process death and synthetic learner
rollback, and reject corrupt or missing control evidence. This is a bounded
engineering hypothesis, not the full protected-runtime contract.

New source: `hmac.zag`, `authority.zag`, `driver.zag`. Frozen imports unchanged:
IO_V1, SHA256_V2 and PROCESS_V3. No old experimental primary runs. Known crash,
corruption, capacity and alias control shapes are disclosed engineering reuse.
RFC4231's public HMAC test vectors are conformance oracles, not fresh science.
The same source author can see the fixtures, keys and expected results.

Trainer-input ledger: no human instruction is converted into a grant. The test
driver alone generates publicly disclosed synthetic actor101/instance7001/
scope9001 tokens under deterministic fixture keys. They authenticate only the
fixture protocol. No real key is generated, enrolled, stored or exposed. Human
identity/provenance and key provisioning remain unimplemented trust boundaries.
Automated test signing is an attributed aid, not a human trainer or consent.

Hardcoding ledger: format magic, byte offsets, cryptographic constants, resource
limits and fixture values are protocol/evaluator substrate. They encode no
learned competence or cognitive answer. Opaque payloads have no semantic parser,
tokenization, graph, supplied linguistic boundaries or learner initialization.

## Formats, authority and serialized transaction

The pinned external policy is128 bytes and binds format/version, actor, instance,
scope, immutable milestone ceiling, initial allowance, initial state version,
dependency digest and initial opaque-state SHA256. Root bytes carry a full
control-key HMAC. Runtime caller supplies the exact policy and separate32-byte
trainer/control keys; keys never enter persistent records.

A request is224 canonical body bytes plus a full32-byte trainer HMAC. It binds
operation, actor, instance, scope, requested milestone, policy epoch, strictly
increasing signed-positive31-bit nonce, state version, non-refundable charge,
logical validity interval, exact candidate length/hash, dependency hash, current
state hash and pinned policy hash. Unknown formats/reserved fields refuse.
No caller-supplied success/verifier flag is accepted. No truncated tag is allowed.
The logical validity clock is the next attempt ordinal, NOT wall-clock expiry.
Module/dependency identities are checked opaque digests, NOT verified executable
loading or native full-state equivalence.

Operation1 replaces a bounded opaque synthetic payload (0..4096bytes) under the
exact current state/version and consumes a positive charge. Operation2 is a
separately authenticated restriction: epoch increases by exactly1, allowance
can only stay equal or decrease, cost0, milestone0. Restriction can reduce the
allowance below already-spent resources without refund and can run when the
operation allowance is exhausted, subject to audit capacity. No widening API.

One nonblocking exclusive advisory lock spans recovery/admission, reservation,
second authorization and publication. Revocation uses that same lock. Staged
request and candidate copies are revalidated before durable reservation and
immediately before hard-link publication; caller buffers are not reread.
The authenticated attempt record binds prior control counters and previous tag,
the complete signed request and exact candidate. One root admits at most32
attempt files, each at most4464bytes. The33rd path is checked during recovery.

A complete authenticated intent always consumes its nonce, allowance charge and
attempt slot, even without a commit marker. An uncommitted state candidate is
not exposed as operational state. A complete authenticated restriction is
effective upon durable intent even if its acknowledgement link was interrupted;
this cannot revive a revoked epoch. A new append uses the next ordinal.
Empty/partial/unauthenticated intents fail recovery closed: no usable state or
keys/handles are returned, and all artifact bytes remain for investigation.
No repair/refund is automatically invented for a partially written grant.

## Exact prospective execution schedule

| Top-level modes | Expected evidence |
| --- | --- |
| `invalid` | exit2, no output |
| `hmac` | All seven RFC4231 SHA256 vector cases (case5 checks the published128-bit prefix but authentication still requires256bits); first/last tag-byte and truncated-tag rejection, output tails/alias and size/wire bounds |
| `normal-write`, `normal-replay` | Maximum4096-byte snapshot, empty snapshot, then authorized restoration of the original synthetic bytes;3 attempts,3 commits, version14, nonce3, spent6 survive fresh replay |
| `refusals` | All256 single-byte token modifications reject-8402; re-signed wrong actor/instance/scope/ceiling/epoch/version/nonce/interval/length/digests/reserved fields reject with the source-pinned codes; candidate swap and private aliases refuse; no rejected admission changes counters/state |
| `quota-write`, `quota-replay` | Two state commits spend6; restriction to budget0/epoch1 remains with version13 and3 attempts; no refund on reload |
| `revocation-write`, `revocation-replay` | Signed old epoch refuses; two restrictions and one state commit retain epoch2, budget1, spent2, version12,3 attempts; even an authenticated allowance increase refuses |
| `nonce-write`, `nonce-replay` | Nonce2147483647 round-trips exactly; reuse refuses, no wrap or extra admission |
| `capacity-write`, `capacity-replay` |32 commits/charges, version43; default expired logical interval refuses first, extended authenticated interval still refuses capacity; no33rd artifact |
| `lock-owner` | One nested fresh `lock-contender` refuses-8409 with no usable state/handles; owner can commit and reopen after release; nested child must be reaped |
| `crash1-write` / replay | exit71 after empty reservation; replay refuses-8408, closed/empty state |
| `crash2-write` / replay | exit72 after half record; replay refuses-8408, closed/empty state |
| `crash3-write` / replay | exit73 after complete intent sync, before link; nonce1 and charge3 survive, state version11, one orphan; nonce reuse refuses; continued append spends5 total |
| `crash4-write` / replay | exit74 after link but before directory sync; in this process-death experiment fresh replay sees committed version12/charge3; continued append spends5 |
| `crash5-write` / replay | exit75 after complete publication sync but before in-memory update; fresh replay sees committed version12/charge3; continued append spends5 |
| `crash6-write` / replay | Simulated returned commit failure after intent sync: operation returns-8407, invalidates handles; fresh replay retains charge/nonce, not candidate state; continued append spends5 |
| `revoke-crash-write` / replay | exit73 after restriction intent; replay retains epoch1/budget1/version11/one orphan; old epoch and restored allowance are refused |
| `corrupt1..4-write` / replay | Preserve preimages/retained names before native fixture mutations: tampered attempt MAC, missing first intent, tampered root MAC, valid but wrong commit link; all fresh replays refuse-8408 and return empty/closed state |
| `prefix-limit` | Required negative boundary witness: a new fixture root containing an authentic older signed prefix opens at version12 while its source reached13. This demonstrates the missing externally protected high-water anchor, NOT a protected-runtime pass |

All modes are single-admission engineering controls in the registered order.
Any unexpected check, exit, signal, capture loss, count mismatch or limit failure
stops subsequent children and fails the primary. Preserve every completed and
partial result. Expected intentional exits71..75 have an armed-boundary marker;
other successful children need native counters and their terminal pass marker.
The parent must account for37 top-level and1 nested reaped child.

## Resources, review and qualification boundary

Parent60s, child15s, child per-file output262144bytes, parent per-file1MiB, core0,
fd64; observed per-child RSS must be positive and <=256MiB. CPU/wall/RSS are
native process measurements; top-level totals are labeled as such to avoid
unsupported descendant aggregation. The nested child's own counters/resource
row is retained. No hard RSS or hostile descendant containment is claimed.

Native arena allocations are bounded by this process schedule, not proven
incrementally reclaimable. Clearing known key buffers is not a guarantee that
all cryptographic intermediate arena copies are erased or absent from dumps.
MAC comparison has a fixed-length source accumulator, not an established
compiler/microarchitecture constant-time proof.

Main-agent engineering review only. This does not discharge independent science
or protected-authority review. No production admission follows these tests.
Hostile same-user access, sandbox/process isolation, real identity enrollment,
private-key custody, asymmetric signatures, externally anchored rollback
prevention, wall-clock expiry, full learner serialization/causal trace integration,
external irreversible actions and power-cut durability remain out of scope.
Advisory cooperating-writer serialization is not an OS security boundary.

Preserve source/config/review/reservation/compiler/build freezes before exposure,
one admission, native results/logs/preimages/resources, analysis including the
expected negative witness, checksums, registries/state/journal/handoff. A pass
advances the bounded authenticated-control component only. R27 stays canonical
at60423/restarts0; original-source/semantic continuity remains a training gate.

Normative construction: RFC2104 section2. Public conformance vectors: RFC4231
section4. No claim that those RFCs certify this implementation or its deployment.
