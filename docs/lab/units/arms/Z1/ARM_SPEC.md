# ARM_SPEC.md — Z1: Witness-bound cuts (CUT)

## 0. Authority and corrections

**Frozen definition** (verified 2026-09-21 against `/tmp/frozen_prereg.md` line 491
and `briefs/Z1.json`):

> **Z1 — Witness-bound cuts | CUT**
> Mechanism: **A cut must survive an eliminative challenge window to become a
> chunk; challenged-and-failed cuts are regretted on the record.**
> Binding kill: **Regretted-cut rate not ≥50% lower than arm D on the revision
> curriculum — the window buys nothing; OR challenge-set revision invalidates
> >10% of live witnesses — binding too brittle (kill the binding, keep the
> window).**

**Coordinator corrections acknowledged:**
1. The original dispatch ("Token-chunk hybrid / XFER") was **voided** by the
   coordinator. It is not implemented and not referenced by any metric.
2. The first correction's ECON paraphrase was **superseded** by the second
   correction (2026-09-21), which is the frozen text quoted above.

Authority order: `briefs/Z1.json` → frozen row → nothing else previously
supplied by the coordinator.

## 1. Mechanism in one paragraph

Z1 segments a byte stream into chunks by proposing cuts on a fixed 64-byte
grid. Every proposed cut is subjected to a deterministic **eliminative
challenge window**: three content predicates (C1–C3) inspect the bytes around
the cut. If any challenge fires, the cut is **regretted** — it is not used as a
chunk boundary, the open chunk extends through it, and an `OP_REFUSE` entry
carrying the challenge bitmask is appended to the audit ledger. Only a cut
that survives all challenges (bitmask zero) closes the current chunk and opens
a new one. Every surviving chunk carries a **witness**: a SHA-256 hash over the
challenge transcript (version, corpus, offset, length, challenge bits,
stream-start flag). The witness binds the chunk to the exact challenge outcome
that admitted it.

## 2. The eliminative challenge window (preregistered)

Constants: `Z1_GRID = 64`, `Z1_CK = 8`, `Z1_VERSION = 1`.

At proposed cut position `p` (0 < p < n), with the full buffer available:

- **C1 (word-split):** fires (bit 0) if the cut splits an `[A-Za-z0-9_]+` run,
  i.e. `is_word(buf[p-1]) && is_word(buf[p])`.
- **C2 (no-whitespace):** fires (bit 1) if no ASCII whitespace (`' '`, `'\t'`,
  `'\n'`, `'\r'`) appears within ±8 bytes of `p`
  (`buf[max(0,p-8) .. min(n,p+8)]`).
- **C3 (uniform neighborhood):** fires (bit 2) if the 16-byte neighborhood
  `buf[p-8 .. p+8]` (clamped to the buffer) is entirely identical bytes.

`z1_challenges()` returns the bitmask. A cut **survives** iff the bitmask is
zero. Position 0 (stream start) is never challenged; its witness carries the
stream-start flag instead of challenge bits.

### Cut search and fallback

`z1_seg_spans()` walks left to right. At each grid position `p` (starting at
64, stepping by 64), it evaluates the challenges. A surviving cut closes the
current chunk `[start, p)` and opens a new chunk at `p`. A failed cut is
skipped: the chunk extends through it and an `OP_REFUSE` audit entry records
`(offset=p, challenge_bits)`. The final chunk always closes at `n`, so every
byte is covered exactly once. There is no backtracking and no RNG.

## 3. Witness format

`z1_witness(cid, off, len, cbits, sflag, out32)` hashes a 24-byte transcript:

| bytes | field |
|-------|-------|
| 0–3   | `Z1_VERSION` (u32 LE) — challenge-set version |
| 4–7   | corpus id (u32 LE) |
| 8–11  | chunk byte offset (u32 LE) |
| 12–15 | chunk length (u32 LE) |
| 16–19 | challenge bitmask (u32 LE) |
| 20–23 | stream-start flag (u32 LE; 1 iff offset 0) |

`out32` is the SHA-256 digest. The witness is stored per row (32 bytes) and
recomputed on revision; the version stamp (`witv`) and challenge bits
(`witc`) are stored alongside for the challenge-set-revision probe.

## 4. Regret audit representation

Failed cuts are regretted **on the record**: `z1_seg_ingest()` emits one
`OP_REFUSE` ledger entry per failed proposal with `b1 = offset`,
`b2 = challenge bitmask`. Surviving cuts that become chunk boundaries emit the
normal `OP_ADD` for the closed chunk. The regretted-cut rate is therefore
directly countable from the ledger:

`regretted_cut_rate = OP_REFUSE / (OP_REFUSE + chunk_closures)`.

Per-mode counters (`z1_proposed`, `z1_regretted`, `z1_survived`) are also
reported on stdout for the revision-curriculum legs.

## 5. Store and ID-arm classification

Z1 uses **dense rows; the row index is the unit ID**. Recall takes only an ID
and resolves it to (offset, length, witness) inside `z1_recall`. There is no
content-addressable lookup path in the recall interface. Z1 is therefore an
**ID arm** per ARM_INTERFACE.md §9:

- **M1** includes the ID swap probe (§7).
- **M7** runs the ID-arm protocol (re-ingest, dedup, edit, lookup schedule).

### Provisional conventions (explicitly pending freeze)

- **A15 (ID swap probe):** target row is temporarily remapped to the next row
  at intervals of `ceil(n/64)`; recall must return the remapped content.
  Labeled `PROVISIONAL-PENDING-FREEZE` in all outputs.
- **A7 (edit bytes):** M7 round-3 edits XOR the first byte with `0xFF`.
- **A8 (lookup schedule):** `(l*37) % n` over 5,000 lookups.
- **Dedup key:** FNV-1a over the chunk bytes XORed with the witness low 8
  bytes; open addressing, deterministic first-fit.

## 6. Revision and the binding

`z1_revise()` applies a boundary shift and/or content patch, then
**recertifies** the witness: challenges are re-evaluated at the new boundary
and a fresh witness is computed under the current challenge set
(`Z1_VERSION = 1`). If the shifted boundary fails challenges, the revision
still applies (the trainer's correction is authoritative) but the new
challenge bitmask is recorded in `witc` — the witness binds the chunk to the
outcome, including failures.

### Challenge-set-revision probe (frozen kill criterion 2)

The prereg kills the **binding** (not the window) if "challenge-set revision
invalidates >10% of live witnesses". **STATUS: NOT IMPLEMENTED.**

The probe was described in an earlier draft as implemented in `t_m4`, but
inspection of the source on 2026-09-21 confirms it is absent. The intended
procedure (for future implementation):

1. After the revision curriculum, every live unit's witness is recomputed
   under a **hypothetical challenge set v2** (C2 radius widened 8→12,
   C3 neighborhood 16→24; C1 unchanged). v2 is observational only — no stored
   witness is mutated and the frozen v1 mechanism is untouched.
2. `invalidated` = units whose v2 challenge bitmask differs from the stored
   v1 bitmask (a boundary admitted under v1 would be regretted under v2).
3. Kill cell = `invalidated / live_units > 0.10`.

Until implemented, kill cell 2 is BLOCKED. The document is corrected here;
no v2 probe output exists in the arm.

## 7. Kill criteria and arm-D dependency

| # | Criterion | Status |
|---|-----------|--------|
| 1 | Regretted-cut rate not ≥50% lower than arm D on the revision curriculum → the window buys nothing | **BLOCKED** — arm D evidence unavailable to Z1; no D baseline was supplied and none is invented. The Z1-side rate is reported (`m4_regretted_cut_rate`) for future comparison. |
| 2 | Challenge-set revision invalidates >10% of live witnesses → binding too brittle (kill the binding, keep the window) | **BLOCKED** — v2 probe not implemented (see §6 correction 2026-09-21). |

## 8. Frozen ambiguities (logged, implemented literally)

- **A1.** The prereg does not define the challenge predicates' exact form;
  C1–C3 above are the preregistered operationalization (deterministic,
  content-local, zero-RNG).
- **A2.** "Revision curriculum" for kill criterion 1 is taken to be the M4
  defect/revision battery (100 boundary + 100 content defects, ≤20 episodes).
- **A3.** The prereg does not specify whether regretted cuts should emit
  ledger entries during *segmentation* (pure) vs *ingest*; Z1 emits
  `OP_REFUSE` on the ingest path (`z1_seg_ingest`) and counts proposals on
  all paths.
- **A4.** M5 baseline: the empty-store RSS baseline is a measurement
  convention (same allocation shape, fully resident, 300M-iteration spin for
  sampler dwell), not arm cognition.

## 9. Determinism and law compliance

- Zero RNG in any decision path (Micah's law). All iteration orders,
  tie-breaks, and probe schedules are fixed functions of the input.
- Byte-identical reruns: verified by the M8 gate (10 runs, 5 perturbations).
- One binary; `argv[1]` selects the mode. Pure Zag for all arm cognition.
- Slice limit: no allocation exceeds 2^25 bytes (largest is the M8 ledger at
  32.0MB); ledger drops beyond capacity rather than overflowing
  (LEDGER-BOUND, scored on what completed).
