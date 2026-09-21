# Y2 — Adversarial chunking: proposed §3-format row

**PROPOSED-PENDING-FREEZE — NOT FROZEN — requires Micah's sign-off before Y2 is built.**

- **What this is:** the missing 53rd-arm row for PREREG_FREEZE.md §3. The frozen
  prereg (b0b9140c0eda, §3) claims 53 arms but defines 52 rows; Y2 —
  adversarial chunking — is catalogued in `ALPHABET_Y-Z.md` and referenced by
  sign-off item **A-46**, but has no §3 row. This file proposes the row text
  only. It makes **no prereg claim** and changes nothing frozen.
- **Sources:** mechanism description verbatim from `ALPHABET_Y-Z.md` §Y2;
  binding kill criterion from A-46 + the catalog's falsification criterion;
  held-out-grammar provenance rule from A-46
  ("held-out-grammar protocol — different crew writes it post-sign-off").
- **Proposed placement in §3:** Cut-signal arms, directly after the Y1 row.

## Proposed row (verbatim, §3 table format)

| Arm | Family | Mechanism (one line) | Kill criterion (binding, PROPOSED) |
|-----|--------|----------------------|-------------------------------------|
| Y2 — Adversarial chunking (red-team segmentation, robustness objective) | CUT | Deterministic read-only red-team proposes worst-case segmentations (pathological cuts: byte-by-byte, mid-word, maximal spans, permuted ID assignments) from a fixed preregistered adversary grammar; the recall organ answers probes from the corrupted-but-legal segmentation; failures are negative evidence against the current scheme, revisable by organ 5 via propose/commit/rollback. | Two binding kill rules: (i) a scheme passes the full adversary grammar yet loses byte-exact recall on the **held-out** adversary grammar — the certification claim dies; (ii) red-teaming cost per cut exceeds 100× the cut cost at 10× scale — Y2 dies as an online mechanism (survives only as offline certification). **Held-out-grammar provenance rule (binding):** the held-out grammar is authored by a separate crew after sign-off — separate from the corpus-C authors — and preregistered BEFORE Y2's battery runs (see `HELDOUT_GRAMMAR_NOTE.md`). |

## Why the row text is this and not that

- Mechanism one-liner is compressed from the catalog's TNN-native mechanism
  text (no new content introduced).
- Kill rule (i) is the catalog's "certification is worthless" falsification
  criterion; kill rule (ii) is the catalog's 100× cost falsification criterion
  crossed with A-46's "cost bar 100×/cut at 10×".
- A-46's ordering constraint ("adversary grammar preregistered FIRST — it is
  the entire claim") is binding on the build sequence, not on the row; the
  held-out-grammar provenance rule is binding on validity of any Y2 verdict.

## Flag for the coordinator (§3 count check)

§3's "Count check" line (48 rows; B counts as 3, C counts as 2 → 53 arms)
reads as already complete without this row. If this row is frozen, the
verifier's row accounting (B as 3, C as 2) should be rechecked so the claimed
53 matches an actual 53 rows — as it stands the arithmetic overcounts by one
even after adding Y2 (48 + 3 = 51, not 53). Do not "fix" silently; resolve at
freeze per RULE-9 amendment procedure.
