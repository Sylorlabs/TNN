# F1-COMPARE — verdict

Date: 2026-09-23. Plain-language report on the comparison repair.

## What was wrong

The machine could compare two things, but only when the question was worded
exactly like one of two frozen templates ("was the author of…before…",
"which is taller…"). Any other wording — "was he born before the eiffel
tower was built?", "who was born first, darwin or melville?", "which of
those two was built first?" — skipped the comparison machinery entirely and
fell back to single-fact retrieval, which just repeated one date instead of
answering. "Those two" was never resolved to the pair being discussed.

## What was built

A general comparison step that runs before retrieval on every turn:

1. It looks for comparison *words* anywhere in the question (before, first,
   taller, older, later…) — not exact phrasings.
2. It finds the two things being compared: names in the question, pronouns
   resolved through the existing salience stack ("he" → Andy Weir), "the
   author of X" resolved to the actual author, bare surnames ("darwin")
   matched to full names, and "those two" resolved to the pair from the
   last comparison.
3. It pulls each side's number from the knowledge base using the existing
   year/height helpers — the marker it searches for (born, built,
   published, completed, dedicated, opened, tall) is picked by what the
   knowledge base actually contains for that entity, not by the question's
   wording.
4. It answers: "yes."/"no." for yes-no questions, or names the winner
   ("charles darwin was born first.", "the eiffel tower was built first.").
   If a number is missing for either side, it declines the comparison
   instead of inventing one.

The two frozen templates were deleted and replaced by this engine; the
unrelated yes/no ("did X write Y") and "birth year" branches are untouched.

## Verdict per kill bar

1. **Acquisition — PASS.** All three failed turns now answer correctly:
   turn 3 → `no.`, turn 4 → `charles darwin was born first.`,
   turn 7 → `the eiffel tower was built first.` (turn 7 works even with
   turn 6 in between — the compared pair survives unrelated turns).
2. **Release (anti-hardcode) — PASS, 7/7** (bar was ≥6/7). Seven frozen
   held-out phrasings, never used during development, all correct —
   including unseen comparison words (earlier, later, older), unseen value
   markers (dedicated, completed, opened), and an honest decline when Big
   Ben has no year to compare. The source contains no per-phrasing
   branches (verified by inspection).
3. **No regressions — PASS.** The 5 good round-2 turns still produce their
   recorded outputs; the full round-1 battery is 370/370 with every
   section score identical to the pre-repair baseline (no section dropped).
4. **Determinism — PASS.** Two full runs of every battery byte-identical
   (`cmp` clean, matching sha256); the program contains no randomness
   machinery at all.
5. **No gaming — PASS.** No branch keys on a multi-word phrasing, no
   per-entity special cases, no probe-tuned constants. The general
   machinery is: a single-word comparison-word list, an entity-type-agnostic
   marker list, and an auxiliary-verb question-shape test.

## What didn't work / known limits

- A latent length typo (17 vs 18) in the pre-existing "the"-prefix name
  list meant "montparnasse tower" could never get its "the". Fixed as a
  data correction; no passing output changed.
- A question mixing intents ("did the author of moby dick write pride and
  prejudice before 1900?") is read as a comparison first — single-intent
  dispatch is a known boundary of this machine, out of F1's scope.
- The engine only compares two entities and only on time/height values
  present in the KB. Anything else falls through to retrieval, as before.

## Commits (branch `tnn-native-lab`)

- `1d826c7` — PREREG_F1.md frozen before implementation.
- `390d17c25614bfb86ccf337c48078c7f64ca0ec1` — repaired fork + HELDOUT.md + build notes + run logs + this verdict.
