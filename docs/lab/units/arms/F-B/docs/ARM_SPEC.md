# F-B ARM_SPEC — Branching-continuation cuts

**Status:** INCOMPLETE — core mechanism implemented and verified; full M1–M9 not completed.

## Frozen mechanism (from ALPHABET_A-F.md, PREREG_FREEZE.md, briefs/F-B.json)

**"Surprise via continuation-branching (not Markov): cut where the set of possible continuations spikes. Cheaper sibling of F-S."**

Literal rule:
- Consider repeated prefixes/spans of lengths `2..LMAX`.
- Cut before `i` if the longest repeated span ending at `i-1` has `contdiv >= BR_BAR`.
- D-style rolling-hash candidate tracking.
- `BR_BAR=3`, justification code `5`.
- Shared D parameters: `W=256`, `LMAX=64`, `MIN_LEN=3`, 4096 candidates.
- Candidate eviction: exact lowest `rep`, then oldest/lower `seq`.

## Provisional choices (not frozen)

- **`REP_BAR=2`**: The frozen documents do not specify a numeric REP_BAR for F-B.
  Provisional choice: 2 (minimum literal meaning of "repeated"). D-R's
  independent choice of 3 is not F-B authority. Marked PROVISIONAL-PENDING-FREEZE.
- **Online interpretation**: Candidates are queried after observing spans ending
  at the current position (online), not two-pass. Documented as provisional.
- **`W=256` semantics**: Window parameter from D family; F-B implementation does
  not currently enforce a sliding window (uses full history). Provisional.

## Implementation

File: `cl/arm.zag` (559 lines, pure Zag)

Core components:
- `FB` struct: candidate table (4096 slots, 64-byte entries), hash buckets,
  binary min-heap for exact `(rep,seq)` eviction, direct-mapped first-seen table,
  256-bit continuation bitsets per candidate.
- `fb_segment()`: Online literal segmentation. For each position `i`, observes
  spans of lengths 2..64 ending at `i-1`, updates candidate rep/contdiv, then
  queries the longest repeated span ending at `i-1`. Cuts before `i` if its
  contdiv >= 3.
- Content verification: NOT YET IMPLEMENTED (hash-only lookup). Required for
  correctness; flagged as gap.
- Chunk store / ID infrastructure: NOT YET IMPLEMENTED.
- M1–M9 modes: NOT YET IMPLEMENTED (only `segtest` diagnostic mode exists).

## Kill criterion (binding)

From PREREG_FREEZE.md:
**"M3 < C-W's both corpora; OR within noise of F-S on all metrics both corpora —
redundant arm, keep F-S, retire F-B."**

Note: P-FB1 wording says "below C-W on either corpus" which conflicts with the
binding both-corpora rule. The binding rule governs.

**Status:** Cannot be adjudicated — no C-W or F-S scorecards located as of
2026-09-21. Do not invent comparison results.
