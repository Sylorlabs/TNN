# ARM_SPEC.md — F-S: Markov-surprise cuts (CUT family)

**Frozen:** 2026-09-21, prereg commit `b0b9140c0eda`, branch `tnn-native-lab`

## 1. Mechanism (frozen)

F-S segments a corpus at points of **Markov surprise** using an order-2 byte
Markov predictor.

### 1.1 Model training
- Count table: order-2 contexts (previous 2 bytes) → next-byte counts.
- 64 MiB total, three shards (21,846 + 21,845 + 21,845 contexts) to respect
  the 2^25 indexed-slice limit.
- Counts are saturating `u32` (cap at 4,294,967,295).
- Training: single pass over corpus, `count[ctx][byte]++` for each position
  i ≥ 2, where ctx = (buf[i-2] << 8) | buf[i-1].

### 1.2 Freeze
- For each of 65,536 contexts, compute `pred[ctx]` = argmax over 256 bytes
  of `count[ctx][byte]`.
- **Tie-breaking (frozen):** lowest byte value wins (deterministic).
- Also store `conf[ctx]` = count[ctx][pred[ctx]] (confidence).

### 1.3 Cut proposal
For each position i (2 ≤ i < n):
- Predicted byte: `p = pred[ctx]`, where ctx = (buf[i-2] << 8) | buf[i-1].
- Actual byte: `a = buf[i]`.
- **Confident miss:** if `p != a` AND `conf[ctx] >= CONF_BAR`, record
  candidate cut at i with confidence `conf[ctx]`.

### 1.4 Cut filtering
- **Local maximum:** candidate at offset o fires only if its confidence is
  strictly greater than all candidates in [o-W, o+W], o ≠ o'. Ties favor
  lower offset (first-seen wins in left-to-right scan).
- **Minimum gap:** fired cuts must be ≥ MIN_GAP apart. Greedy left-to-right:
  keep a cut if it's ≥ MIN_GAP from the last kept cut.

### 1.5 Recurrence gate (AMB-FS-007)
A fired cut **commits** (becomes a chunk boundary) only if the resulting
chunk recurs in the corpus:
- Let `prev` = previous fired cut offset (or 0 for first).
- Let `c` = current fired cut offset.
- Span = buf[prev:c]. If span occurs ≥ 2 times in the corpus (rep ≥ 2),
  commit the cut; else refuse it.
- **Reading:** "previous fired cut" (not "previous committed cut").
  A refused cut advances the proposal span start but is not installed as
  a committed boundary.

### 1.6 Chunks
- Chunks are spans between committed cuts: [0, c1), [c1, c2), ..., [ck, n).
- "Just code 4": chunks are coded as (offset, length) pairs; no further
  transformation.

## 2. Parameters (PROVISIONAL, not frozen)

| Param | Value | Status |
|-------|-------|--------|
| CONF_BAR | 16 | PROVISIONAL — not frozen; competing values untested |
| W | 8 | PROVISIONAL — not frozen; competing values untested |
| MIN_GAP | 32 | PROVISIONAL — not frozen; competing values untested |

**Note:** Micah's standing rule: "when in doubt or guessing at all with
recommendations, just test both." Parameter sensitivity tests were not
completed due to time constraints. The values 16/8/32 are educated guesses
based on Python diagnostics, not frozen.

## 3. Store and ID layer

F-S is an **ID arm**: chunks are assigned persistent monotonic IDs from
`s.next_id` (starting at 1) during chunking. The store provides:
- Slot table: ID → (offset, length, corpus, flags)
- Persistent ID→storage mapping (recall by ID)
- Tombstones, kill, pin, weaken, revision
- Audit ledger with F-S opcodes:
  - CUT_PROPOSE=20, CUT_COMMIT=21, CUT_REFUSE=22
  - TRAINER_SWAP_PROBE=19 (for M1 A15)

## 4. Ambiguities (from AMBIGUITIES.md)

- **AMB-FS-007:** Recurrence gate reading. Chosen: judge each fired cut on
  span since previous *fired* (not committed) cut. A refused cut advances
  the span start but does not install a boundary. This prevents the
  degenerate case where a non-recurring prefix blocks all future commits.

## 5. Battery modes implemented

- `diag-chunk`: diagnostic chunking, prints stats
- `m1-1x-prose`, `m1-1x-code`: M1 recall (implemented, passing)

**Not implemented:** M2, M3, M4, M5, M6, M7, M8, M9. The full battery was
not completed due to time constraints. See BUILD_LOG.md and VERDICT.md.

## 6. Kill criteria (frozen)

F-S is killed if ANY of:
1. Shakespeare boundary F1-agreement with C-W is within ±0.05 (of 1.0)
   AND crew-local reuse M3 ≤ C-W's.
2. Code cut count > 5× C-W's.
3. F-S loses to D on crew-local reuse M3 on both corpora.

**Evaluation:** See VERDICT.md. None fire based on available evidence.
