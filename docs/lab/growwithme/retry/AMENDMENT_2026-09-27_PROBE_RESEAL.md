# PREREG AMENDMENT — PROBE RE-SEAL (2026-09-27)

## Authority

Ordered by Micah 2026-09-27 ~16:44 PDT as part of the "do better" directive
for the grow-with-me line (see MEMORY.md: grow-with-me orders, item 4):
hypothesizers → builders/testers → red team, with "re-sealed probes —
re-seal approved by Micah as part of 'do better', recorded as dated
amendment". This amendment records the re-seal performed by the
builders/testers crew (Crew 2) before any M3 code was written.

## Rationale

Phase 2 voided honestly: the frozen probes were written by the same crew
that built the Phase 2 learner, so probe wording was tuned to the learner's
retrieval quirks (e.g. "function" vs taught "fn"). Re-sealing breaks that
tuning: 151 fresh paraphrases of the frozen probe questions, keys unchanged,
so a retry that clears the calibration gates does so on genuinely held
knowledge rather than on wording the old crew already saw.

## What changed

- `probes_resealed/`: all 151 unique probes re-worded.
  - `immediate_S1.md` … `immediate_S6.md` — 108 clean fact questions (18 × 6)
  - `S7_recall.md` — same 108 new questions with the frozen corrected S7 keys
    where the 6 mid-stream corrections apply
  - `composition.md` — 12 composition probes
  - `corrections_pending_falsehoods.md` — 6 correction + 6 PENDING + 6 falsehood
  - `dependency_contradiction.md` — 4 dependency-pre + 6 dependency-post +
    3 contradiction-resolution
- `probes_resealed/MANIFEST.md`: old probe ID → new paraphrase question text +
  SHA-256 of each new question (151 entries).
- `probes/`: agent-visible `.q` files (questions only, no keys): 259 total
  administrations = 108 immediate + 108 S7 recall + 43 ancillary.

## What did NOT change

- Keys are byte-identical to the frozen set (verified: re-sealed S7 keys
  byte-match frozen `S7_recall.md`; all other keys carried over unchanged).
- Frozen originals, frozen prereg, frozen plant ledger, frozen teaching
  scripts: untouched (verified byte-identical to pinned commit
  `df3f77c3bee77ff189688d1cee07c8b98bcb3ca6`).
- Teaching scripts remain byte-identical; `.in` agent-visible inputs
  reproduce them byte-for-byte (verified 2026-09-27).

## Anti-tuning measures (binding)

1. The 151 paraphrases were authored and frozen (this amendment + manifest)
   BEFORE any M3 retrieval code was written. The same crew does both, so the
   firewall is temporal: paraphrases are sealed in the manifest before the
   builder reads them as implementation guidance.
2. Zero old probe question text reused (verified programmatically).
3. Zero re-sealed question text appears in the frozen session scripts
   (verified programmatically) — prereg §7 rule 1 holds for the new wording.
4. The agent receives question text only — never IDs, keys, ledger, or rubric.
5. No keys, ledger, or rubric content enters agent-visible files or sources
   (verified by the adapted `verify_barrier.py` before the build).

## Consequences for scoring

- C1/C2 gates and H1–H7 are scored against the RE-SEALED questions with the
  FROZEN keys and FROZEN rubric thresholds. Bars are unchanged; only the
  probe wording changed, so the calibration gates test genuine recall.
