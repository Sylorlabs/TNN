# R33-N09 — supervisor-head-bound checkpoints and confined-worker integration

Identity `r33-native-n09-supervisor-anchored-checkpoint-v1`. One sole primary,
15 top-level native children plus one nested kernel-confined native worker.
No learner, scientific world, accepted-parent object, training, canonical change,
newborn restart, real human grant or promotion. All new logic is native Zag.

## Hypothesis and changed-variable ledger

A worker-visible checkpoint can remain an authenticated cache, not an authority
root: admission must require exact agreement with the independently held current
supervisor journal. A genuine older receipt, wrong-branch receipt with identical
numeric counters, or torn receipt must not rewind the supervisor or cause stale
state delivery. Missing/torn caches can be regenerated from the authoritative
journal after process death. Corrupt authority must not fall back to a valid
cached receipt. The worker cannot read, mutate, unlink or inherit descriptors
for the actual authority journal under the integrated kernel policy.

New files: checkpoint.zag, isolation.zag, worker.zag and driver.zag. Reuse frozen
N07 authority.zag/hmac.zag, IO_V1, SHA256_V2 and PROCESS_V3 unchanged. The OS
adapter is parameterized from N08B's passing native implementation with explicit
absolute-path character validation; all supplied paths belong to the trusted
controller. The frozen Apple dyld-support.sb is unchanged. No old primary runs.
Crash, rollback, tamper, alias and confinement control shapes are disclosed
known engineering reuse; this batch does not claim independent fresh science.

Forbidden changes: modifying frozen imports/old outcomes; replacing original
R27; accepting caller-selected authority roots; bypassing grant/state checks;
allowing worker access to keys/control; changing failed oracles after exposure;
activating graph/BPE/VAD cognition; executing Python or other replacement logic.

## Exact cache format and trust boundary

The cache contains a192-byte canonical header,0..4096 opaque payload bytes and a
full32-byte HMAC under the supervisor control key. Fields: magic R33CP001;
format1; current intent sequence, epoch, state version, maximum consumed nonce,
cumulative spend, current allowance, payload length, published count, orphan
count, state-commit count, instance/scope/actor IDs, pinned policy hash, exact
state hash and current authenticated journal head;32 reserved bytes are zero.
The cache is224..4320bytes, never a runnable grant or arbitrary object graph.

Export stages bytes and tag before writing to caller memory; short output or
internal aliases refuse. Restore verifies the cache MAC and canonical format,
then exact header and payload agreement with a currently open, locked supervisor
store before delivery. Header mismatch returns-8604, payload mismatch-8603,
bad MAC-8602, malformed/short buffer-8601, unusable authority-8610 and internal
alias-8611. Every refusal leaves output unchanged. Successful packet/output
overlap uses a staged copy. No cached version or policy overrides current state.

The N07 journal is the one durable authoritative control history; a separately
updated high-water file would introduce another transaction boundary. N09 does
not invent such a file or claim a two-store atomic commit. Complete durable
uncommitted intents still consume nonce/spend/sequence and change cache identity
even when operational learner payload stays unchanged. Authenticated restrictions
change epoch/allowance and invalidate prior caches without rewriting payload.

This protects cache replay relative to the trusted, fixed supervisor journal
and the tested worker boundary. It does NOT resist a host administrator or
trusted controller replacing all authoritative history with an older authentic
prefix. N07's negative witness remains valid outside this threat model. No remote
or hardware monotonic anchor, genuine key enrollment, production human identity,
asymmetric signature, executable swap verification, full learner serialization,
or whole-runtime security qualification is implied. There is no real grant.

## Sole prospective schedule and falsifiers

1. Invalid mode exits2 without output.
2–3. Normal writer and fresh replay: save initial32-byte receipt, commit4096-byte
   payload at nonce1/cost3/version12, save current receipt. Deliver every byte of
   current payload and reject the authentic older receipt. Fresh replay then
   performs an authenticated synthetic restoration of initial bytes: version13,
   nonce2, spend5; the former current receipt must now fail. New receipt succeeds.
4. Tamper all256 positions of the initial receipt independently: each alteration
   must refuse without changing64-byte sentinel output. Test short packet,
   private packet/output/export aliases, short export/delivery, valid control,
   successful caller packet/output overlap and no admitted mutation. Quoted or
   newline-containing trusted-profile path candidates must refuse before launch.
5. Separate synthetic branches with identical policy, keys, version12, nonce1
   and spend3 but different state/head: authentic other-branch receipt refuses
   against the first branch; exact own receipt succeeds. Workers cannot choose
   either controller root through the restore API.
6. Commit state, then authenticated restriction epoch1/budget2 with spend3:
   old receipt refuses despite unchanged payload/version12. Current receipt
   succeeds, with current restriction and no refund.
7–8. Exit73 after durable authority commit but before worker cache creation:
   fresh supervisor rejects old receipt, retains nonce1/spend3/version12 and
   reconstructs the exact current cache from authority.
9–10. Exit74 after writing and syncing half the new worker cache: fresh recovery
   rejects torn cache-8601 and old cache-8604, retains current committed control
   state and reconstructs exact new cache. Partial artifact remains.
11–12. N07 fault3 exits73 after complete durable intent before state publication:
   recovery retains nonce1/spend3/seq1/orphan1 but original payload/version11.
   Pre-intent authentic receipt still refuses; reconstructed current receipt
   delivers the original payload without promoting the uncommitted candidate.
13–14. Save authentic cache, preserve exact preimage, then corrupt the actual
   synthetic control intent MAC. Fresh authority open refuses-8408; cache restore
   refuses-8610, output unchanged, root closed and keys empty. No cache fallback.
15. Integrated sandbox: controller commits4096 bytes, exports the current cache,
   publishes it read-only to the worker and holds the real authority lock. A
   deliberate duplicate of the actual intent descriptor40 is passed toward the
   relay; the relay must close it. The nested native worker's10 assertions test
   exact input availability/hash, cache write denial, actual authority read/write/
   unlink denial, socket/fork denial and all nonstdio descriptors absent. The
   controller compares worker-reported input SHA with exact current packet,
   verifies capture and successful counters, then closes/reopens the authority
   and verifies intact current payload/version12/spend3. Actual worker has no
   authority module, keys or test signer linked into its executable.

Each non-crash child must exit0 with exact terminal and unambiguous native
counter records. Intentional exits73/74 require the declared boundary marker.
All15 top-level and one nested child must be reaped, no unexpected stderr or
signal, no incomplete capture. Any unexpected result stops later cases and
fails this sole primary. Preserve failures and touched fixtures. Full check
totals are measured by the native implementation, not guessed here.

## Resources, provenance, review and artifacts

Parent60seconds; each child15seconds; output262144bytes per child; parent1MiB
per file; core0, descriptor ceiling64, observed childRSS positive and<=256MiB.
Top-level CPU/wall/RSS totals are labeled; the nested worker resource row is
retained separately, not silently double-counted. No hard RSS or all-descendant
resource theorem is claimed. Bounded workloads do not prove lifetime arena
reclamation or exhaustive wiping of every cryptographic intermediate.

Trainer-input ledger: deterministic PUBLIC synthetic keys and signed fixture
messages originate only in the native controller, with actor101/instance9009/
scope7009. No human instruction is converted into a grant. All values, sizes,
field layouts, paths and hash constants are protocol/test hardcoding, not learned
competence or cognitive answers. The worker hashes its actually received bytes;
that is an engineering observation, not an intelligence or understanding claim.

Main-agent source/security-boundary engineering review only, not independent
scientific/security certification. Freeze sources, imports, protocol/config/
review/reservation, compiler, two build pairs, platform/profile pins before one
admission. Retain raw captures, caches/preimages/control history, native result,
resources, full analysis with limitations, artifacts manifest, consumed record,
current state, journal and handoff. Continue parent/causal/runtime integration
afterward; a pass is not completion of R33 or authority to train.
