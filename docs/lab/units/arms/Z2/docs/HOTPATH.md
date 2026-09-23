# Z2 hot-path characterization — the breach checker under the znc miscompile history

Requirement (frozen §3 row): "Hot-path characterization required (znc
miscompile history)." The breach checker (`z_check` in `cl/arm.zag`) runs on
the recall hot path — every `z_recall` calls it before returning any byte.
The znc history (ZNC-2026-09-19-001: hot-path miscompile) means we do not
trust the checker's presence on authority; we characterize it with evidence.

## What the checker is

A pure function of `(slot contract fields, declared purpose, ledger seq)`:

1. tombstone test: `flags & F_LIVE` → refuse 203
2. restriction test: `restr & purpose` → refuse 202
3. expiry test: `ledger_seq >= exp` → refuse 201
4. else allow

Cost: O(1) per recall — 3 integer compares, ~10 integer ops, 1 branch chain.
No loops, no allocation, no syscalls, no clocks, no addresses, no RNG.
Inputs: every field it reads (`flags`, `restr`, `exp`, `ids`) is written at
`slot_insert` / `z_contract_set` before any recall can observe the slot —
no uninitialized reads by construction.

## Evidence the checker is really on the path (not compiled away)

1. **Call counting** (`z2-hotpath-1x`): `checker_calls` increments once per
   `z_check` entry. Over 20,000 recalls × 2 in-process passes the count is
   exactly 40,000 = 2 × ops. A miscompile that dropped the call would show
   a short count; one that skipped the check would show allows where the
   decision log shows refuses.
2. **Decision-log hashing** (`z2-hotpath-1x`): every recall's allow/refuse
   decision (with reason code) is recorded; the 20,000-byte log is
   sha256-hashed and printed. The battery's double-run rule requires the
   hash byte-identical across two fresh processes.
3. **In-process self-check** (`z2-hotpath-1x`): the identical 20,000-op
   stream re-runs inside the same process; decision logs compared
   byte-for-byte; mismatches reported (must be 0). Catches
   state-dependent misbehavior (e.g. a check reading stale/uninitialized
   state that differs between passes).
4. **Refusal liveness** (`z2-misuse-1x`): 9,000 misuse probes produce 9,000
   loud refusals with REFUSE ledger entries (reasons 201/202/203 all
   exercised). The refuse path is live code — it cannot have been
   compiled into a no-op.
5. **M8 adversarial determinism**: the contract arrays (`restr`, `exp`,
   `vsign`) are part of the M8 store image (`store_hashes.txt`), and every
   ledger byte (including REFUSE entries) is in `ledger.bin`. The
   `frag` perturbation (deterministic heap pre-fragmentation) catches
   uninitialized-memory reads; `aslr` (1.2MB pad) catches address leaks;
   `starve` (entropy/clock starvation) catches clock/RNG dependence;
   `freelist` (reversed free-list init) catches order dependence. All five
   × 2 reruns must be byte-identical — any checker dependence on
   uninitialized memory, addresses, or init order would diverge here.

## Result (r1 1x)

See `scorecard_r1_1x.json` (`z2.hotpath`): 20,000 ops, 40,000 checker
calls, 0 self-check mismatches, decision hash stable across the double
run, M8 gate PASS. The checker is characterized as: deterministic, O(1),
pure function of initialized state, present on every recall, with a live
refuse path. No miscompile signature observed.
