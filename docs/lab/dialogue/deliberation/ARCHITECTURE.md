# Deliberation v1 — Architecture

**Implementation:** `deliberate.zag` (frozen: `deliberate_frozen.zag`)  
**SHA-256:** `d433bd06a102df5842b09318b86caa4e0d4e0ae075e3516bae8c9f85f5403c64`  
**Date:** 2026-09-27

## Overview

Deliberation v1 replaces the round-4 cascade with genuine deliberation machinery.
The decision lives in a ledger; the trace is the ledger rendered during deliberation.

## Ledger Layout

- **25 rows** × 552 bytes: 10 reading hypotheses (hid 0-9), 3 fact candidates
  (hid 10-12), 12 action bids (hid 13-24).
- **Turn fields** at 13804-13820: close-call flag, fact-winner, etc.

## Phase Ordering (G2 Compliant)

1. **GEN:** All candidates generated — readings (0-9), facts (10-12), actions (13-24).
   - Per-GEN idempotence flags ensure exactly-once execution (K1 safety).
2. **ELIM:** Single elimination loop over actions (13-24).
   - PRE_FAIL: precondition false.
   - GATE: withhold/eliminator gate.
   - OUTSCORED: marked BEFORE any ELIM trace (repair #2).
3. **ARGMAX:** Winner = max score among survivors; tie → lowest hid.
   - Margin <5 → close_call flag set, CLOSE + 2×CONTENDER + flag-gated REVIEW.

**G2 Compliance:** No separate fact ELIM/ARGMAX phase. The clarify/withhold/default
GENs select the best gated fact via `best_gated_fact()` (scans hid 10-12), ensuring
all candidates are generated before any elimination.

## The 12 Action Bids

| HID | Action | Base | Fires When |
|-----|--------|------|------------|
| 13 | joke | 240 | joke intent |
| 14 | memory | 237 | memory query |
| 15 | forget | 234 | forget request |
| 16 | correction | 231 | "no," + prior entity |
| 17 | resume | 228 | resume intent |
| 18 | compose | 225 | compose intent |
| 19 | challenge | 222 | challenge intent |
| 20 | provenance | 219 | provenance query |
| 21 | assertion | 216 | assertion |
| 22 | clarify | 213 | predicate mismatch + named entity |
| 23 | withhold | 210 | no fact or gate failure |
| 24 | default | 207 | "did ..." + entity |

**Base scores** compressed from 20-point gaps to 3-point gaps (repair #10) to allow
close-call margins <5. Priority order preserved; bonuses (0-3) reflect evidence.

## Content Tracing (BUILD_SPEC §4)

Every KB-derived value flowing into answer bytes appears in the trace:
- `FACT hid=` lines for fact candidates (even when missing).
- `CONTENT hid=... fact="..."` with full fact text.
- `shaped=` indicates correction entity-swap.
- `ARGMAX`, `CLOSE`, `REVIEW` all cite `hid=`.

## Side-Effect Partition

ACT reads the winner (status 2) and applies side effects:
- Novelty from ledger offset 448 (not 432).
- Return fid from offset 452 (not 436).
- Prior-query state updated ONLY when the winner is not withhold/clarify
  (prevents R4-03 turn 4 regression).

## Close-Call Mechanism

When winner margin <5 over runner-up:
1. `close_call()` sets flag at 13812.
2. `CLOSE hid=` emitted with winner hid.
3. Two `CONTENDER hid=` lines for winner and runner-up.
4. `REVIEW` gated on reading flag 13812 (not a local variable).

**Note:** Natural close calls are rare due to bid precondition exclusivity.
The mechanism is verified by code inspection and the scoring allows <5 margins.
