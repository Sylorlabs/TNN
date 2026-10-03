# STAGE 0 STATE REGION DECLARATION

Date: 2026-09-30. Governs: world_learn.zag / world_learn_bin (Stage 0 readiness build).
Protocol: FREEZE_PROTOCOL.md sections 2.2 and 3.2.

## Persistent learner state: W, one 32768-byte array

The binary allocates exactly one 32768-byte region W per process. W is the declared persistent learner state. Its content is loaded from the state file at startup (or initialized fresh) and written back to the state file after the event stream. No other byte crosses a process boundary.

Byte ranges (all offsets decimal):

- W[0..4): global tick counter. Incremented by newtick() on every learn() and query() call.
- W[4..8): unused, zero.
- W[8..12): foundation-evict flag. Set to 1 when a foundation slot (subj 1..6) is evicted under pressure.
- W[12..64): unused, zero.
- W[64..1648): fact store. Base 64, 36 slots of 44 bytes. Rule record fields (byte offsets within slot): 0 subj, 4 rel, 8 obj, 12 correct, 16 wrong, 20 dependents, 24 contradictions, 28 last_used, 32 taught, 36 superseded, 40 valid.
- W[1648..2000): unused, zero.
- W[2000..2048): collateral sample slots, 12 i32 values (coll_record / coll_changes discipline).
- W[2048..16384): unused, zero.
- W[16384..32768): DDES hypothesis ledger slice L (16384 bytes, entry stride 1152). Entries e0..e6 were used by the legacy P1-P11 driver (e5 = P11 R1 ADAPT, e6 = P11 R1b STATIC). The generic Stage 0 world driver never writes this region: there are no generic causal event verbs yet, and adding them would be cognitive machinery, not plumbing. The region is declared persistent because it is part of W and the legacy driver wrote it; a future stage may drive it generically or rule it out of the persistent set.

## Scratch: per-run, never persisted

- World file bytes: one fresh _zag_read_file allocation per process. Read-only during the event loop, never copied into W, never written to the state file.
- State load buffer sb: transient copy source when loading an existing state file; its content is exactly the state file content, copied into W byte for byte.
- Parser temporaries: integer locals only (line offsets, field bounds, event counts).
- The z_alloc backing of W is fresh per process, but its content is exactly the loaded state file (or the zero initial state); it carries no other information.

## Scratch discipline

The only bytes ever written to the state file are the 32768 bytes of W. Parse buffers, the load buffer, and all temporaries are process-local and die with the process. Therefore any byte outside the declared W that influenced behavior could not have crossed worlds: there is no channel for it. The binary's code region (.text) is immutable across worlds.

## Initial state (null-world state)

32768 zero bytes. sha256: c35020473aed1b4642cd726cad727b63fff2824ad68cedd7ffb73c7cbd890479
Recorded artifact: null_state.bin (this directory), produced by the Stage 0 null-world run.
