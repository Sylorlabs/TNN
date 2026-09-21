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
| CONF_BAR | 16 | PROVISIONAL — sweep-tested (see below) |
| W | 8 | PROVISIONAL — sweep-tested (see below) |
| MIN_GAP | 32 | PROVISIONAL — sweep-tested (see below) |

**Parameter sweep (2026-09-21, per Micah's "test both" rule):**
Seven configurations tested on M1-prose recall and M3 churn:
(16,8,32), (8,8,32), (32,8,32), (16,4,32), (16,16,32), (16,8,16), (16,8,64).
Results: [pending sweep completion — see BUILD_LOG.md].

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

All modes implemented and passing (2026-09-21, 1x):

- `diag-chunk`: diagnostic chunking, prints stats
- `m1-1x-prose`, `m1-1x-code`: M1 recall (prose: 211u 100/100; code: 17156u 100/100)
- `m2-t1-prose`, `m2-t1-code`: M2 tier-1 (ETC=1, 100/100)
- `m2-t2-prose`, `m2-t2-code`: M2 tier-2 (ETC=1, 100/100)
- `m2-t3-1x`: M2 tier-3 (ETC=1, 100/100)
- `m3-1x`: M3 churn (survival 100%, fresh 100%, weaken 50/50, freeze 0)
- `m4-1x-prose`, `m4-1x-code`: M4 repair (1 episode, 100/100 both)
- `m5-1x`, `m5-baseline`: M5 cost (PROVISIONAL — see §7)
- `m6-p2c-1x`, `m6-c2p-1x`: M6 transfer (tax 0.0 both directions)
- `m7-1x`: M7 (lookup 100%, reuse 2.0; A7/A8 PROVISIONAL — see §7)
- `m8-1x`: M8 perturbations (clean/frag/aslr/starve/freelist; see §7)
- `sweep`: parameter sensitivity (CONF_BAR × W × MIN_GAP; see §2)

All modes: two runs, byte-identical stdout (determinism verified).

## 7. Provisional components (not frozen)

The following are crew-local provisional designs, NOT part of the frozen
mechanism. They are marked provisional in all outputs:

- **M5 (cost):** Structural byte accounting (slot table, ledger, corpus
  buffer) vs a fixed-work baseline spin. The baseline does not replicate
  the harness's RSS methodology; treat M5 as structural cost only.
- **M7 A7/A8 (edits/schedule):** Edit = first-byte XOR (harness-equivalent
  for F-S's offset/length coding); schedule = deterministic lookup
  (l*37)%nunits; unit split 1666/1667/1667 over three 5000-unit regimes.
  The frozen harness edit/schedule was not available; this is a
  crew-local stand-in.
- **M8 perturbations:** `frag` (interleaved alloc/free), `aslr`
  (4,096-byte ASLR pad), `starve`/`freelist` (accepted as no-op flags;
  the harness runner defines their exact semantics). All perturbations
  produce byte-identical M1/M3 results to clean.
- **A15 (trainer swap probe):** After each ceil(nunits/64) recalls, remap
  next ID to (slot+1)%nslots, log TRAINER_SWAP_PROBE, recall, restore.
  Implemented in M1; verified via audit log.

## 6. Kill criteria (frozen)

F-S is killed if ANY of:
1. Shakespeare boundary F1-agreement with C-W is within ±0.05 (of 1.0)
   AND crew-local reuse M3 ≤ C-W's.
2. Code cut count > 5× C-W's.
3. F-S loses to D on crew-local reuse M3 on both corpora.

**Evaluation:** See VERDICT.md. None fire based on available evidence.
