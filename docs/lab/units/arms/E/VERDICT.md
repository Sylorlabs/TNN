# Arm E — VERDICT (Track A, Round 1)

Date: 2026-09-21. Author: Arm E crew.

## VERDICT: KILLED

Binding kill criterion (frozen prereg §3, arm E row, quoted verbatim):

> "Stored-bytes-per-recall ≥ 2× B-64's at equal M1 on either corpus at 10x
> (copies-only strictly dominated by the dumbest persistent segmentation)."

## Evidence

**Equal M1 at 10x** (each leg ×2, byte-identical stdout, final binaries):

| corpus | E recall/boundary | B-64 recall/boundary | units |
|---|---|---|---|
| prose 10x | 100.0 / 100.0 | 100.0 / 100.0 | 847,301 |
| code 10x | 100.0 / 100.0 | 100.0 / 100.0 | 1,486,773 |

**Stored bytes** (M5 `m5_slot_table_bytes`, the arm store region per A16 —
slot table + owned copies for E; slot table + insertion queue for B-64;
audit ledger excluded per prereg §5 M5, which reports audit bytes as a
separate cost column):

| arm | stored bytes (10x prose) | per source byte | per recall |
|---|---|---|---|
| E | 91,679,710 | 1.69 B/B | 108.2 B |
| B-64 | 33,167,612 | 0.61 B/B | 39.1 B |

**Ratio: 91,679,710 / 33,167,612 = 2.764× ≥ 2×. The criterion fires.**

Corroboration: E also exceeds the M5 bar (per-byte memory ≤ 1.5× source
bytes): 1.69× > 1.5×, while B-64 passes at 0.61×.

## Death certificate

> "references matter, transient segmentation does not."

E segmented perfectly well — 100% recall, 100% boundary fidelity at both
scales on both corpora, a clean M8 determinism gate, and a green 1x row
(M1–M9). It died on the one thing its mechanism could not escape: every
unit persisted as an owned byte copy, so its store costs ~2.76× the
reference-holding B-64 for identical recall. Ephemeral segmentation bought
nothing over the dumbest persistent segmentation; the copy is the cost.

## 1x M1–M9 row (final binary, 18/18 battery, M8GATE PASS)

- M1: prose 100.0/100.0 (84,731 u); code 100.0/100.0 (148,678 u)
- M2: T1/T2/T3 all reach criterion (T3 synthetic 100.0); no leak signal
- M3: survival 100.0, fresh recall 100.0, 8,050 mgmt entries, freeze CLEAR
- M4: 100.0% boundary-defect revision, 100.0% content-defect revision
- M5: 84,731 units learned; 9,322,125 slot-table bytes; 85,731 ledger entries
- M6: p2c/c2p 100.0/100.0, revision 100.0, tax 0.0; validity gate PASS
- M7: N/A (no ID layer — non-ID arm, not a penalty)
- M8: PASS (5 perturbations, byte-identical)
- M9: "fast-then-flat" (takeoff ep 1, steepness 100.0, late gain 0.0)

Scorecard: `scorecard_r1_1x.json` (this directory).

## Ambiguities / caveats

1. **Metric reading:** "stored bytes" = M5 memory-store bytes per prereg §5
   (A16 store region); the audit ledger is a separate cost column and is
   excluded. Including it would change the ratio to 1.67× — the verdict
   depends on this reading, which follows the prereg's own M5 definition.
2. **Corpus scope:** the M5 cost leg is prose-defined per §5 ("Full prose
   ingest"); the criterion's "either corpus" is satisfied on prose. Code
   M1 equality is shown for completeness.
3. **B-64 10x** used a measurement-only B-64 variant (same reference/
   re-read semantics, large-file support added; uncommitted evidence
   tooling in `work/b64_10x/`), since B-64 itself is a 1x arm.
4. **Same-key re-ingest** revives the existing entry (documented
   same-provenance behavior, not dedup); 10x tiles use distinct keys.
5. The 1x M8 gate passes on the final binary; the M8 ledger-hash loop was
   re-verified during the 4-shard ledger patch.

## What survives

E's 1x row is fully green — as a pure recall/retention/revision substrate it
works. What died is the thesis that transient segmentation plus owned copies
can compete with persistent references on cost. Any future STORE-family arm
must either deduplicate (becoming D-like, forbidden for E) or show the copy
cost buys something references cannot.

## Commits

- Evidence commit: `4ce17ac3d3a576df5a5cd7e95eefa1326eeb5d52` (tnn-native-lab;
  superseded path layout, kept for history)
- Path-fix commit: `33dcc60b12a8d34189039cbe3ab74e3374a4d583` (tnn-native-lab;
  canonical layout under `docs/lab/units/arms/E/`)
