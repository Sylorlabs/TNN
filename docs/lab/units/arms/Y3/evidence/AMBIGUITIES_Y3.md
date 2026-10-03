# AMBIGUITIES_Y3.md — Y3 (Temporal/versioned IDs) literal-reading adoptions

Per the ambiguity rule: every gap between the frozen brief/harness and what the
code had to decide is implemented literally and logged here, never silently
reinterpreted. Shared harness ambiguities (A1–A17) live in the harness's
AMBIGUITIES.md; this file records Y3-specific adoptions. Frozen §3 row:

> Y3 — Temporal/versioned IDs | IDENT | Mechanism: Identity = serial + birth
> epoch + revision lineage; tombstoned IDs never reused; never dangles. |
> Binding kill criterion: Mean lineage depth > 50 on the standard revision
> curriculum (fragmentation, not versioning); OR any recall resolving to a
> tombstoned span (dangling reference observed) — kill and fix before any
> further claim.

## A-Y3-1: the "standard revision curriculum"
The brief's "standard revision curriculum" is the M4 trial every arm runs:
plant 200 defects (100 boundary-shift / 100 content-patch) on a full-corpus
store, then deliberate-repair episodes until all verify or 20 episodes pass.
No arm-specific curriculum was invented. Boundaries use the same 12-cycle
delta schedule as the reference arms so M4 is cross-arm comparable.

## A-Y3-2: "mean lineage depth"
Defined literally: for each of the 200 revised units, depth = 1 (the live
version) + the number of tombstoned versions for that serial in the version
log; mean over the 200 units. Emitted as the `LINEAGE,<corpus>,<mean>,max=<max>`
TAG line by m4-1x (both corpora). Kill if mean > 50.

## A-Y3-3: "fragmentation, not versioning"
The parenthetical is read as the kill row's own gloss: the kill criterion
fires on mean DEPTH (fragmentation) exceeding 50, not on the mere existence
of versions. No separate "versioning" metric was invented; the criterion is
the numeric bar, nothing more.

## A-Y3-4: "any recall resolving to a tombstoned span (dangling reference observed)"
Literal reading: a recall is "resolving to a tombstoned span" when a live
recall path returns bytes belonging to a version that was tombstoned —
i.e. the recall dangles. This is NOT the same as explicit time-travel recall
(recall(serial, epoch)), which deliberately requests a tombstoned version
and is required to return exactly that version's recorded bytes (verified by
the `TIMETRAVEL` self-test). Implemented as the `DANGLE` check in m3-1x and
m8-1x: recall of each of the 3000 killed serials must return -1 (loud
failure). Any non -1 = dangling reference observed = kill and fix.

## A-Y3-5: the A15-provisional swap probe
ARM_INTERFACE.md §9 requires a persistent ID layer to implement the §15
provisional schedule. Implemented in y3_m1_run: N=64 deterministic
ID→content remappings after every ceil(n/64) recalls, logged with the frozen
opcode 0x13 TRAINER_SWAP_PROBE (d1=probe_idx, d2=remapped_slot), probed
recalls excluded from the recall/boundary denominators, side-channel
(original-bytes-despite-remap) → M1 cell scored 0. The probe and the
m1_id_probe cell are marked PROVISIONAL-PENDING-FREEZE in stdout TAG,
fragment, and scorecard until §15 freezes. See A15 in harness AMBIGUITIES.md.

## A-Y3-6: M7 for an ID arm
§9's M7 fallback (no bars, N/A) is conditioned on "no ID layer". Y3 carries a
persistent serial→slot mapping, so M7 runs with bars. The prereg does not
freeze the C' construction or lookup schedule; adopted literally from the
only concrete construction available: C' = first-byte XOR 0xFF on every
100th unit (as a recorded content patch, audited as a trainer op), lookup
schedule serials (l*37)%n split 1666/1667/1667. Logged by the `M7LITERAL` TAG.

## A-Y3-7: birth epoch
The brief's "birth epoch" contains no wall-clock-able quantity (wall clock is
forbidden by the interface). Implemented as the ledger sequence number of
the entry that issued the version — the ADD entry's own index for birth,
the REVISE entry's own index for a new version. Deterministic, replayable,
and checkable against the ledger bytes.

## A-Y3-8: the slot region (M5 / M8)
The arm's persistent arrays: 11 slot arrays (serials, epochs, roots, offs,
lens, corps, flags, shifts, pidx, skeys, svals at cap×4 B), the
insertion-order queue (ins_cap×4), and the version log (vlog_cap×20). M5's
slot_table_bytes = cap×44 + ins_cap×4 + vlog_cap×20. M8's store image covers
the same region plus next_serial (4 B); the patch staging area is excluded,
matching the reference arm's precedent (it is arm-scratch, never state that
affects recall except through audited flags).

## A-Y3-9: SLOT_REUSE logging
The frozen opcode namespace includes 0x0A SLOT_REUSE (slot=new slot).
Y3 logs it whenever a tombstoned slot is re-occupied by a new serial.
Tombstoned SERIALS are never reused (the kill row's requirement); tombstoned
SLOTS are storage and may be re-occupied — the opcode exists precisely to
make that visible in the ledger.

## A-Y3-10: lineage root
Every serial founds its own lineage, so root = serial at issue. The roots
array is carried for schema completeness (the §3 mechanism names "revision
lineage" as part of identity); it is written by slot insertion and hashed
in the M8 store image.

## A-Y3-11: dedup vs new version
Re-ingesting an identical span of a LIVE serial resolves to the same serial
(no new version). Re-ingesting the span of a DEAD serial mints a FRESH
serial — the tombstoned serial is never resurrected, per "tombstoned IDs
never reused". Dedup hits are checked for liveness so a killed span's index
entry goes stale rather than resurrecting.

## A-Y3-12: epoch fixup vs SLOT_REUSE log order
birth_epoch is defined as the ADD entry's own ledger index. When slot
insertion re-occupies a tombstoned slot it logs SLOT_REUSE first, so the
epoch is captured after insertion, right before the ADD append. The -1
provisional epoch in the slot record is overwritten in the same call; no
path reads it in between (single-threaded, sequential).

## A-Y3-13: M2 sustained-3 criterion vs single-probe ETC
The M2 criterion requires content ≥ 99.5% AND boundary ≥ 95% "sustained 3
consecutive probes", ETC = index of the first probe in the first sustained-3
run. The Y3 M2 loop probes once per episode and stops at the first passing
probe (ETC=1). This is exact, not an approximation: the arm's deliberate
ingest is single-pass complete and deterministic, and no state changes
between consecutive probes, so probes 2 and 3 are provably 100.0/100.0 and
the sustained-3 run provably starts at probe 1. A literal 3-probe loop would
return the same ETC with 3× the compute.
birth_epoch is defined as the ADD entry's own ledger index. When slot
insertion re-occupies a tombstoned slot it logs SLOT_REUSE first, so the
epoch is captured after insertion, right before the ADD append. The -1
provisional epoch in the slot record is overwritten in the same call; no
path reads it in between (single-threaded, sequential).
