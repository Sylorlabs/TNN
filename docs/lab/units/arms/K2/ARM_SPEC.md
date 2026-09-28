# ARM SPEC — K2: 64-bit FNV-1a Identity

**Arm ID:** K2
**Family:** IDENT
**Track A — Representation Program**
**Spec authority:** `~/workspace/tnn-lab/units/arms/briefs/K2.json` + byte-verified frozen K2 row (ALPHABET_G-L.md §K2)

## 1. Mechanism

K2 is K1 with `ID = FNV-1a-64(content)` — ~15 lines of pure Zag, no native
identity hash. Cheap hash identity with honest, counted collisions; chain
rules for disambiguation.

- **Identity:** 64-bit FNV-1a of the unit's content bytes. Pure Zag; no native import.
- **Dedup table:** Linear probing from `hash mod tcap`, where `tcap = 2 × cap`
  (frozen: table sized at 2× expected unique spans).
- **Collision handling:** Equal hashes require full-byte comparison before
  dedup. True collisions (same ID, different bytes) use insertion-order
  chains. Collisions and maximum chain lengths are counted honestly.
- **Capacity:** Table capacity 2× expected uniques. Resize = deliberate audited
  rebuild (corpora sizes known up front; not exercised in the 1× battery).
- **Synthetic collision vectors:** Required and implemented (`t-collision`
  mode forces distinct contents to share one ID deterministically).
- **Maximum chain length:** 4 (kill bar — see §3).

## 2. Falsifiable Predictions

- *Strength:* ≥ 95% of K1's dedup savings at ~10× lower hash cost per add
  (measured ops).
- *Weakness:* Collision chains engage on corpus B at 10× scale (honest-collision
  path gets real exercise); chain-walk cost becomes measurable.

## 3. Binding Kill Criterion (exact, from brief)

> **Bidirectional:** if K2's dedup savings within 2 pts of K1's AND per-add
> cost lower → **K1 dies on cost grounds** (keep K2). If chain lengths exceed 4
> on any corpus run → K2 dies (64 bits too small for the store's lifetime).

## 4. Audit Ledger (frozen 64-byte layout)

All fields 4 bytes. `op@0, slot@4, rc@8, b1..b5@12..28, a1..a5@32..48,
stage@52, d1@56, d2@60`. IDs recorded in a-fields are truncated to low 32 bits
(the full 64-bit ID lives in the slot table; the ledger records the tag).

## 5. Modes

One binary; `argv[1]` selects the mode:
`m1-1x-prose`, `m1-1x-code`, `m2-t1-prose`, `m2-t1-code`, `m2-t2-prose`,
`m2-t2-code`, `m2-t3-1x`, `m3-1x`, `m4-1x-prose`, `m4-1x-code`, `m5-baseline`,
`m5-1x`, `m6-p2c-1x`, `m6-c2p-1x`, `m7-1x`, `m8-1x`, `t-collision`.

Each mode prints a human-readable `M#,...` line, a `K2CHAIN,...` line
(max chain, collision count), and a `METRIC_JSON {...}` line.

## 6. Determinism

Zero RNG in any decision path. Fixed ingest order. No wall-clock, addresses,
or PIDs in the ledger, store image, allocator trace, or stdout. All M8
artifacts are byte-identical across the 5 perturbation runs.

## 7. Known Limits

- M5: per-byte memory 2.42× (bar 1.5×), audit 16.2/KB (bar 10/KB). The 2×
  hash table + 9 slot arrays are inherent to the design. Scorecard FAILs;
  not a kill criterion.
- K1 comparison pending: K1 has not run M7/M5; the bidirectional criterion's
  K1 direction is undecidable until K1 reports dedup savings and per-add cost.
