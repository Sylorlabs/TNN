# ARM_SPEC.md — L1: Absolute Position IDs

Arm: **L1** · Class: **IDENT** · Round: r1 · Scale: 1x (+10x conditional)

> COORDINATOR CORRECTION (2026-09-21, acknowledged): the mechanism/kill text
> quoted in the original dispatch task message was a coordinator dispatch error
> (spec text from a different taxonomy whose arm IDs overlapped). The true
> frozen §3 row for L1 — verified byte-identical between the frozen commit
> `b0b9140c0edaf6fc678edea9e9fd4bf9cf485aca` and the workspace copy — is the
> one built here. The voided text is not reproduced anywhere in this arm's
> sources, docs, or evidence.

## 1. Mechanism (frozen §3 row, verbatim)

- **Arm:** L1 — Absolute position IDs
- **Class:** IDENT
- **Mechanism:** ID = (stream, segment, offset); identity is WHERE, not what.
- **Binding kill criteria** (any one kills):
  1. store cost > 3x K1 on corpus A with no recall-accuracy advantage — dies
     as primary (may survive as secondary index, cf. K3);
  2. any revision batch changes an existing position ID — its one promise
     broken, dies outright;
  3. mean segments-touched per sequential recall > 4 on corpus C.

Per-arm brief: `units/arms/briefs/L1.json` (matches the frozen row).

## 2. Design decisions (all inside the frozen row)

- **Unit of knowledge:** fixed 64-byte chunks of the corpus byte stream
  (segmentation is a fixed, content-blind framing — identity stays WHERE,
  never what). One unit = one position ID; one position ID = one unit.
- **Position ID:** `pid = (stream << 40) | (segment << 20) | local_offset`,
  with `SEG_SHIFT = 20` (1 MiB segments), `SEG_MASK = 2^20 − 1`. stream is the
  corpus (prose/code/fresh). Positions are pure functions of (stream, index):
  no content hashing anywhere in the ID path.
- **Eternity of identity:** a position ID, once assigned, is never mutated.
  `l_revise` repairs content *around* the ID — it never rewrites the slot
  record's (stream, segment, offset). Kill criterion (ii) is checked explicitly
  in M4 (pid snapshot before/after the 20-episode revision batch; any change
  → the arm dies outright).
- **Byte store:** append-only arena of 1 MiB segments. A segment holds many
  64-byte units (16,384 per segment). Units of one stream occupy contiguous
  segments; offsets inside a segment never move after write.
- **Revision model:** the persistent slot table maps each position ID to its
  storage record; an append-only revision map holds old→new (seg, offset)
  entries. A content revision appends the repaired 64 bytes to the stream's
  open segment and records the mapping — the position ID is untouched.
  Segments are immutable once sealed; only the open segment accepts appends.
- **Slot placement:** deterministic, ID-derived (golden-ratio hash of the
  position ID) with linear probing — no RNG, no content dependence. The
  insertion queue gives FIFO eviction order for the M3 phase-3 pressure leg.
- **Defects:** boundary defects are recorded shifts (the ID stays ground
  truth; revision drops the shift). Content defects are recorded patches that
  the recall path applies until revised. All trainer ops are logged.
- **A15 swap probe (PROVISIONAL-PENDING-FREEZE):** the M1 probe implements the
  harness's proposed 64-point ID→content remapping schedule literally: after
  every ⌈n/64⌉ recalls the persistent revision map is patched so the next
  recall target resolves to the *following* unit's position, a
  `TRAINER_SWAP_PROBE` ledger entry is written, and the arm must return the
  **remapped** content — returning the original bytes is a side-channel FAIL
  (M1 cell scored 0). The temporary mapping is restored immediately after the
  probe recall. The schedule and remap function are provisional per
  `units/arms/harness/AMBIGUITIES.md` A15 and are NOT part of the frozen bar.

## 3. Metric semantics (L1-specific, schema metrics-v1)

- **M1** `m1_recall_tenths` (bar ≥ 950), `m1_boundary_tenths` (≥ 950),
  `m1_id_probe` ∈ {PASS, FAIL (side channel)}. Units: 64-byte chunks.
  Boundary = slot record's (seg, offset) equals the assigned position and no
  unresolved shift. Reported per corpus (prose / code).
- **M2** episodes-to-criterion: recall ≥ 995 AND boundary ≥ 950 for 3
  consecutive episodes; 50-episode ceiling, censored=1 if never reached.
  Tiers: t1 (10-ep block repeats), t2 (no immediate repeats), t3 (code).
  Episode-0 probe on the empty store is the leak check. M9 piggybacks on t3.
- **M3** survival = % of 1,000 valuable units (spread over both corpora)
  recallable through the ID layer after 7,000 fresh ingests, 3,000 kills and
  4,000 capacity-pressure ingests; weaken ops (50) are processed as audited
  annotations, never ignored; freeze tripwires per the interface.
- **M4** boundary-revision and content-revision rates over 20 episodes on 200
  defect units (100 boundary shifts, 100 content renames/XORs), kill rate,
  kill-substitution flag; plus the kill-criterion-(ii) eternity assertion
  (any position-ID change → outright death) and an informational
  fragmentation probe (distinct segments touched by a sequential recall pass;
  the battery has no corpus C, so criterion (iii) is measured on A/B only —
  see VERDICT.md).
- **M5** spent = units stored vs budget = total units + 2% headroom; over iff
  spent > budget, any store failure, or recall probe < 495/500.
  `m5_slot_table_bytes` = the arm's M8 slot region per A16 (8 slot arrays +
  insertion queue + segment table + revision map, fixed capacity).
  Baseline (`m5-baseline`) touches the same fully resident empty store.
- **M6** 200 kill probes (recall blocked, removed-from-live, leak metric),
  phase-A/B recall, 200 pin-then-kill probes.
- **M7** ID-arm protocol (provisional C′ edit + lookup schedule): hit rate over
  5,000 deterministic lookups, reuse = ID references / distinct live IDs
  (2 decimals), dedup over rounds 1–2 (2 decimals). C′ round-2 revision goes
  through the content-defect → deliberate-revise path. All provisional.
- **M8** full-trace determinism: M1(with probe)+M3+M4+M5 phases run twice per
  perturbation × 5 perturbations; artifacts compared byte-for-byte:
  `store_hashes.txt` (per-2^20-chunk SHA-256 + chain), `ledger.bin`,
  `ledger_chain.txt`, `alloc_trace.txt`, stdout/stderr identical.

## 4. Kill-bar evaluation plan

- (i) store cost: from M5 (`m5_slot_table_bytes` vs corpus A bytes), compared
  against K1 by the coordinator; needs "no recall-accuracy advantage" —
  evaluated jointly with the M1 recall row.
- (ii) eternity: from M4 (`eternal=` TAG field + unit_verified pid checks);
  any change = outright death.
- (iii) fragmentation: from the M4 fragmentation probe; corpus C is absent
  from the battery, so the cell is measured on A/B and reported as
  provisional (see VERDICT.md).

## 5. Known harness gaps (not arm defects)

- `scorecard_assemble.py` is B-64-specific (hardcodes `"arm": "b64"`, M1 ID
  probe N/A, M7 always N/A). The frozen harness was not modified; L1 ships an
  evidence-side assembly step instead (see BUILD_LOG.md).
- The battery has no corpus C; kill criterion (iii) cannot be evaluated as
  frozen and is reported with that caveat.
