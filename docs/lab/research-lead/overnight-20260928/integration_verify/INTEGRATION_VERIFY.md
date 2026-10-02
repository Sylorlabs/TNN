# Guard Integration Verification

**Verdict: INTEGRATION-VERIFY-COMPLETE.**
**Status: verify only; no edits made.**

This document verifies the six insertion points specified in the guard
integration spec (commit `abe3d32e5`) against the actual content of the
TNN-3 preregistration structure (commit `206499c03`). All six insertion
points are structurally valid. No renumbering is required. Two minor
issues are flagged for the preregistration author (one mixed reference
frame, one capability-count error in draft text). Neither blocks
integration.

## Reference frame

The integration spec mixes two reference frames, and both resolve
unambiguously once named:

- **Frame 1 (outline):** the proposed preregistration document outline
  defined in prereg-structure Section 6 ("Structure: proposed
  preregistration document outline"). Insertions A, B, D, E, F target
  this frame.
- **Frame 2 (synthesis):** the prereg structure synthesis document's own
  sections (1. Inventory, 2. Dependencies, 3. Order, ...). Insertion C
  targets this frame.

## Point-by-point verification

### A. Section 1, new subsection 1.5 (reference)

- Outline Section 1 ("Identity and precedence") contains exactly
  1.1, 1.2, 1.3, 1.4. Subsection 1.4 is "What this preregistration
  covers". Subsection 1.5 does not exist.
- The synthesis document's own Section 1 ("Inventory") uses subsections
  1a-1g, so "1.4" and "1.5" unambiguously resolve to the outline frame.
- **Result: VALID. No conflict, no renumbering.**

### B. Section 2, end-of-section note after 2.8 (note)

- Outline Section 2 ("Frozen kill bar text") contains exactly
  2.1-2.8. Subsection 2.8 is "For each bar: the specific TNN-2 failure
  mode it targets". The synthesis document's own Section 2 uses
  subsections 2a-2d, so "2.8" unambiguously resolves to the outline
  frame.
- The insertion is an unnumbered end-of-section note, not a new
  numbered subsection, so it cannot collide with future numbering.
- **Result: VALID. No conflict, no renumbering.**

### C. Section 3, Step 4 row note (note)

- The outline's Section 3 ("Structural signature function", 3.1-3.4)
  has no order summary table and no Step 4. This insertion therefore
  targets the synthesis document's own Section 3 ("Order: in what order
  should they be attempted"), which contains a "Step 4: H1 widening
  (open constructor), ONLY after Step 1" subsection and an "Order
  summary table" whose Step 4 row exists with a Prerequisites cell
  ("Step 1, Step 2").
- The Step 4 narrative carries the constraint text ("This step must not
  precede Step 1, per the treadmill warning"), so the insertion's
  premise is satisfied. The integration doc's quoted phrase is a close
  paraphrase of the actual constraint wording, not verbatim, but the
  target cell exists and appending a citation to it is structurally
  sound.
- **Clarity issue (minor):** this is the only insertion in the
  synthesis-document frame; A, B, D, E, F are in the outline frame.
  The integration spec should state the frame explicitly ("prereg
  structure Section 3", not just "Section 3") so the preregistration
  author does not look for an order summary table in the outline's
  Section 3. Flagged, not blocking.
- **Result: VALID with a clarity flag. No conflict, no renumbering.**

### D. Section 6, new subsection 6.9 (insertion)

- Outline Section 6 ("Architecture accounting") contains exactly
  6.1-6.8. Subsection 6.8 is "ISA freeze attestation (no new opcodes;
  protected core unchanged)". Subsection 6.9 does not exist.
- **Result: VALID. No conflict, no renumbering.**

### E. Section 8, new subsection 8.6 (insertion)

- Outline Section 8 ("Verification procedures") contains exactly
  8.1-8.5. Subsection 8.5 is "No weakening after results (amendment
  requires transparent re-freeze and full re-run)". Subsection 8.6
  does not exist.
- **Result: VALID. No conflict, no renumbering.**

### F. Section 10, new subsection 10.4 (insertion)

- Outline Section 10 ("Governance and audit") contains exactly
  10.1-10.3. Subsection 10.3 is "Contamination checks (builder never
  sees sealed worlds before freeze)". Subsection 10.4 does not exist.
  (The synthesis document itself has no Section 10, so the outline
  frame is unambiguous.)
- **Result: VALID. No conflict, no renumbering.**

## Referenced-commit checks

All commits cited in the insertion draft text exist in the repository:

- `1646b9732` (treadmill guard) - exists
- `64eec921f` (SUF definition) - exists
- `f383dd11c` (floor spec) - exists
- `ed2357141` (re-clustering) - exists
- `22197da2c` (H3-lite design) - exists

## Content issue flagged (minor, not structural)

Insertion B's draft text says: "Each of the seven floor capabilities
(F1/F2/F3/G1/G2/G3, floor spec commit `f383dd11c`)". The floor spec
defines exactly six capabilities (F1, F2, F3, G1, G2, G3); it names six
and lists six. The word "seven" is a count error (also present in the
floor spec's own commit message, "7 capabilities (F1-F3 freeze, G1-G3
GW)", where 3+3=6). The preregistration author should correct "seven"
to "six" when applying insertion B. This does not affect the validity
of the insertion point.

## Summary

| # | Location | Target frame | Target exists | New number free | Verdict |
|---|---|---|---|---|---|
| A | 1.5 | outline Sec 1 | 1.1-1.4 present | 1.5 free | VALID |
| B | note after 2.8 | outline Sec 2 | 2.1-2.8 present | n/a (note) | VALID |
| C | Step 4 row | synthesis Sec 3 | table + row present | n/a (cell append) | VALID, clarity flag |
| D | 6.9 | outline Sec 6 | 6.1-6.8 present | 6.9 free | VALID |
| E | 8.6 | outline Sec 8 | 8.1-8.5 present | 8.6 free | VALID |
| F | 10.4 | outline Sec 10 | 10.1-10.3 present | 10.4 free | VALID |

No renumbering is required anywhere. The guard remains a discipline,
not a bar, under all six insertions, consistent with the integration
spec's consistency notes. The two flagged items (mixed reference frame
in C; "seven" vs six capabilities in B's draft text) are author-facing
corrections, not blockers.
