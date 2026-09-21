# Z3 — Budgeted Chunks: ARM Specification (FROZEN)

**Status:** FROZEN 2026-09-21. No mechanism parameter may change after this
commit without coordinator re-approval. Implementation/compiler bug fixes only.

**Identity (byte-verified against `units/arms/briefs/Z3.json` and the
coordinator's second correction, 2026-09-21):**

- **Z3 — Budgeted chunks**
- **Family:** ECON
- **Mechanism:** "One scarce currency prices storage + access per epoch (B per
  epoch); granularity is economic; fixed prices + hard budget."
- **Binding kill criterion:** "Total cost not ≥20% below the best
  fixed-granularity arm at equal recall accuracy — the machinery buys nothing;
  OR halving B causes >15% accuracy drop for a 50% budget cut (pricing model
  wrong — cliff, not graceful degradation). **The prereg must state explicitly
  why fixed prices + hard budget ≠ reward signal (A-53).**"

**Classification:** Provisional ID arm (`PROVISIONAL-PENDING-FREEZE` per
`ARM_INTERFACE.md §9` / `AMBIGUITIES.md A15`; Micah's freeze outstanding).
`recall(id)` resolves through the persistent arm-maintained ID→storage mapping
(the slot table). The mandatory provisional A15 M1 probe (N=64 deterministic
remappings; recall must return remapped content; restore afterward) is
implemented and labeled provisional.

## 1. Economic parameters (frozen)

| Symbol | Value | Meaning |
|---|---|---|
| `B` | 4,000,000 | Budget per epoch (the scarce currency) |
| `c_create` | 100 | Price: ingest one unit (storage) |
| `c_recall` | 10 | Price: recall one unit (access) |
| `c_revise` | 50 | Price: revise one unit |
| `c_kill` | 5 | Price: kill one unit |
| `c_pin` | 2 | Price: pin (mark valuable) one unit |
| `c_weaken` | 5 | Price: weaken one unit |
| `c_read` | 1 | Price: per 64 bytes read during recall |
| `c_store` | 1 | Price: per live unit per epoch (storage rent, drained at epoch close; never refuses) |
| `S_fine` | 64 bytes | Finest span |
| `S_max` | 65,536 bytes | Coarsest span |

**Epoch:** A ledger-delimited budget period. `b_epoch_open` resets
`budget_left = B / bdiv` and the per-epoch budget ledger; `b_epoch_close`
drains storage rent (`nlive × c_store`, never refuses) and logs the close.
Every priced operation debits via `b_debit`; if `budget_left` is insufficient
the operation is **refused loudly** (returns -1 / logs `OP_REFUSE` /
`BOP_REFUSE`; recall misses are loud, not silent). Refusals are counted
(`epoch_refused`) and reported per mode.

**No learned prices.** All prices are fixed constants. There is no price
adaptation, no bidding, no market, no optimization over prices.

## 2. Why fixed prices + hard budget ≠ reward signal (A-53)

A reward signal is a learned scalar that shapes behavior through optimization
pressure: the system adjusts its policy to maximize it, and the signal's
meaning is whatever the optimizer makes of it. Z3 has none of that:

1. **Prices are fixed, not learned.** `c_create=100` does not change because
   recalls succeeded or failed. Nothing updates a price.
2. **The allocation rule is fixed.** Span selection is a deterministic
   function of `(corpus_bytes, B)` (§3). Consolidation is a fixed predicate
   (§4). Neither is tuned by outcomes.
3. **The budget is a hard constraint, not an objective.** The arm does not
   maximize "budget saved" or minimize spend; it spends what the fixed rule
   dictates and refuses loudly when the budget is exhausted. There is no
   gradient, no policy update, no credit assignment from spend to behavior.
4. **Everything is audited and human-readable.** Every debit lands in the
   per-epoch budget ledger (32-byte entries: op, unit id, debit, balance,
   price id). A human can read exactly what was spent, where, and why.

Fixed prices plus a hard budget are therefore **accounting**, not learning:
a deliberate, audited, human-readable allocation rule with no optimization
pressure toward any behavior. That is why it is not a reward signal.

## 3. Granularity selection (frozen)

`z3_select_span(len, B)` returns the **smallest** power-of-two span
`S ∈ {64, 128, 256, 512, …, 65536}` such that the estimated epoch cost fits:

```
n = ceil(len / S)
unit_cost(S) = c_create + c_recall + (S/64)*c_read + c_store
est = n * unit_cost(S)
select smallest S with est <= B; if none, return -1 (loud failure)
```

Granularity is economic: small corpora can afford fine spans; large corpora
are forced coarse by the fixed budget. The rule is deterministic in
`(len, B)` — identical inputs always select the same span.

Resulting spans for the frozen corpora (r1, B=4,000,000):

| Corpus | Bytes | Span | Spans |
|---|---|---|---|
| prose.bin | 5,422,721 | 256 | 21,183 |
| code.bin | 9,536,657 | 512 | 18,623 |
| t1_prose.bin | 542,273 | 64 | 8,473 |
| t1_code.bin | 542,273 | 64 | 8,473 |
| t2_prose.bin | 4,427,776 | 128 | 34,592 |
| t2_code.bin | 225,280 | 64 | 3,520 |
| t3.bin | 1,048,576 | 64 | 16,384 |
| churn_fresh.bin | 448,000 | 64 | 7,000 |

## 4. Consolidation (frozen)

After ingest, `refine_worth_it(acc, span)` fires only if `span > 64` and
`acc × 100 > span` — i.e., a coarse span is re-cut into 64-byte fine chunks
only when its recall frequency provably amortizes the re-creation cost
(`nf × c_create` vs. recall savings). Fine-chunk IDs are deterministic:
`(corpus<<24) | 0x800000 | (coarse_ordinal×(span/64) + fine_index)`,
so re-ingest revives instead of duplicating. Consolidation never fired in
the 1× battery (recall frequencies never crossed the threshold); the
predicate and its accounting are frozen regardless.

## 5. Epoch boundaries per mode (frozen)

- **m1-1x-***: one epoch (ingest at economic span + full probe + 64 A15 swap probes).
- **m2-***: one epoch per episode (ingest + probe); reference criterion:
  3 consecutive episodes with recall ≥99.5% and boundary ≥95%; censor at 50.
- **m3-1x**: one epoch (1000 V pins + 3000 fresh ingests + 3000 kills +
  50 weakens + 4000 phase-3 ingests with eviction).
- **m4-1x-***: one epoch (ingest + 200 defects + revise/verify episodes).
- **m5-1x**: one epoch (ingest + 500 fresh + 500 kills + full recall).
- **m5-baseline**: no epochs (empty store, touch, spin).
- **m6-***: one epoch per phase (train episodes; in-domain revision;
  transfer ingest+probe; transfer revision).
- **m7-1x**: one epoch (round 0/1/2 ingests + 5000 lookups).
- **m8-1x**: three epochs (M1-prose; M1-code; M3 sequence). Phase boundaries
  are deterministic; the budget ledger is per-epoch.

## 6. Total-cost formula (frozen, for the kill criterion)

```
total_cost = slot_table_bytes
           + normal_ledger_bytes   (64 B/entry)
           + economic_ledger_bytes (32 B/entry, per-epoch; summed over epochs)
           + corpus_buffer_bytes
```

where `slot_table_bytes = cap×24 + ins_cap×4` (six 4-byte slot arrays: ids,
offs, lens, corps, flags, accs; plus the insertion-order queue). The corpus
buffer is counted because Z3 serves recalls from it (the reference B-64 does
likewise). RSS delta is measured by the harness and added by the scorecard
assembly for the memory/source bar; it is not part of `total_cost`.

**Equal-M1 comparison procedure:** Z3's M1 (recall/boundary at its economic
span) must match the best fixed-granularity arm's M1 within the harness's
equality tolerance on **both** corpora (prose and code). Only then is
`total_cost` compared: Z3 survives iff
`total_cost_Z3 ≤ 0.80 × total_cost_best_fixed`.

## 7. Half-B diagnostic (frozen)

Modes `m1h-1x-prose` / `m1h-1x-code` rerun M1 with `bdiv=2`
(`budget_left = B/2` per epoch; span selection uses `B/2`). Kill iff
recall accuracy drops by more than 15% relative to full-B M1 on either
corpus (a cliff, not graceful degradation).

## 8. ID-arm mapping and provisional procedures

- **Persistent mapping:** the slot table (`id → (offset, length, corpus,
  flags)`). `slot_find` is open-addressed hashing on the unit ID; placement
  is a pure function of the ID (perturbation-independent).
- **A15 swap probe (PROVISIONAL-PENDING-FREEZE):** N=64 deterministic
  probes. Each probe patches the target slot's mapping to resolve to another
  live slot, logs `OP_SWAP`, recalls by the original ID, expects the
  remapped bytes, then restores. Returning original content would be a side
  channel and scores M1 as zero. Result: `m1_id_probe: PASS (64/64)`.
- **M7 (PROVISIONAL-PENDING-FREEZE):** uses the harness validator's
  unfrozen A7/A8 placeholders — C′ as first-byte XOR `0xFF` on every 100th
  span (an audited content defect, `OP_TDC`); lookups `(l×37)%nunits` split
  1666/1667/1667 across rounds 0/1/2. Repeated units resolve to the **same**
  IDs (revive path); C′ edits are in-place patches on the same IDs
  (declared, audited), never fresh unrelated IDs. Metric readings:
  `hit_rate` = served lookups / 5000; `reuse` = ID references (ingests +
  defects + lookups, all rounds) / distinct live IDs;
  `dedup` = 1 − distinct stored / total ingested over rounds 1–2.

## 9. Audit ledgers

- **Normal ledger** (`ledger.bin`, M5/M8): 64-byte entries
  `(op, slot, rc, b1..b5, a1..a5, stage, d1, d2)` for every state change.
  Recalls do not log op entries (they are accesses, not state changes);
  every priced access is in the budget ledger.
- **Economic ledger** (`budget_ledger.bin`, per-epoch; M8 artifact):
  32-byte entries `(bop, unit_id, debit, balance, price_id, op)` for every
  debit, epoch open/close, and refusal. The M8 stdout prints its sha256
  (perturbation-independent by construction).

## 10. Determinism

Pure Zag. No randomness in any decision path. Slot placement is a pure
function of unit ID. The M8 battery (5 perturbations × 2 reruns) must be
byte-identical on all required artifacts; `freelist-rev` and `starve` are
documented no-ops for Z3 (no freelist; no clock/entropy use).
