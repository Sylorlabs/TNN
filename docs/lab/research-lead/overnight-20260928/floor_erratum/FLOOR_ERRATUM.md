# Erratum to the Frozen TNN-3 Floor Specification

**Status: ERRATUM, not an amendment.** This document does not modify the frozen
floor specification. It transparently records an internal count error found in
it, per Micah's ruling of 2026-10-01: add a transparent erratum, do not alter
frozen history silently.

**Frozen document:** `docs/lab/research-lead/overnight-20260928/floor_preserve/FLOOR_SPEC.md`,
committed as `f383dd11c` ("FLOOR-SPEC-COMPLETE: TNN-3 preservation spec").
The frozen file is untouched by this erratum.

---

## 1. The error

The frozen spec says "seven capabilities" in three places:

- Line 12: "The seven capabilities below are the floor."
- Line 168: "The floor is seven capabilities; everything else is either a target or out of scope."
- Line 234: "Seven capabilities, four from the freeze pass set, three from the GW positives."

But the spec enumerates exactly **six** capability sections:

- F1. Associative recall (FW1, FW2)
- F2. Law change and revert (FW4)
- F3. Targeted update without collateral damage (FW5)
- G1. Construction over learner-taught facts (GW3 phase 2)
- G2. Single-level value revision through the query path (GW7 probe 5)
- G3. Inquiry discrimination and re-fire (GW6 primary, GW7)

3 freeze capabilities plus 3 GW capabilities equals 6, not 7.

Line 234 compounds the error with "four from the freeze pass set, three from
the GW positives." The "four" confuses the four freeze worlds in the 4/9 pass
set (FW1, FW2, FW4, FW5) with the three freeze capabilities: F1 covers two
worlds (FW1 and FW2), so 4 worlds map to 3 capabilities. The correct split is
three from the freeze pass set and three from the GW positives.

## 2. What is correct

**6 capabilities:** F1, F2, F3 (freeze) + G1, G2, G3 (GW).

**7 verification tests** (the floor battery, spec section 4, lines 176-182):

1. FW1 probe set (associative recall, retention)
2. FW2 probe set (associative recall)
3. FW4 sequence (law change/revert)
4. FW5 probe sets (targeted update, no collateral)
5. GW3 phases 1-2 (construction over taught facts)
6. GW7 through probe 5 (single-level revision, no dependents)
7. GW6 primary 7 probes (inquiry discrimination and re-fire)

F1 covers two tests (FW1 + FW2); every other capability maps to one test.
Hence 6 capabilities produce 7 tests.

**Rule for readers:** "seven floor **tests**" is CORRECT. "Seven floor
**capabilities**" is INCORRECT. "Six floor **capabilities**" is CORRECT.

The spec's own "seven verification tests" phrasing (lines 175, 187, 211) is
correct and unaffected by this erratum.

## 3. What this erratum does not do

- It does not edit, amend, or supersede the frozen spec `f383dd11c`.
- It does not change any capability definition, threshold, or NOT-floor listing.
- It does not change the anti-gaming clause or any breaking criterion.
- It is a transparent record of the count error so downstream documents can
  cite the correct numbers without silently rewriting frozen history.

## 4. Downstream documents carrying the error

The doc audit (`doc_audit/DOC_AUDIT.md`) identified 9 live occurrences of
"seven capabilities" / "7 capabilities" that should read "six" / "6". They are
listed here so they can be fixed in their own documents; this erratum does not
fix them.

| # | File | Line | Text |
|---|---|---|---|
| 1 | treadmill_guard/TREADMILL_GUARD.md | 154 | "For each of the seven floor capabilities" |
| 2 | treadmill_guard/NAMECHECK.md | 23 | "the 7 capabilities F1-F3, G1-G3" (names 6, says 7) |
| 3 | design_synthesis/TNN3_DESIGN_SYNTHESIS.md | 11 | "the floor (7 capabilities)" |
| 4 | design_synthesis/TNN3_DESIGN_SYNTHESIS.md | 62 | "all seven floor capabilities" |
| 5 | final_tally/FINAL_TALLY.md | 27 | "7 capabilities TNN-3 must preserve" |
| 6 | prereg_check/NAMECHECK.md | 48 | "7 capabilities" |
| 7 | prereg_check/PREREG_READINESS.md | 77 | "7 capabilities" |
| 8 | synthesis_review/SYNTHESIS_REVIEW.md | 9 | "7 capabilities" |
| 9 | synthesis_review/SYNTHESIS_REVIEW.md | 31 | "the floor spec has 7: F1/F2/F3 + G1/G2/G3" (arithmetic error: 3+3=6) |

Note: the guard-integration NAMECHECK count error was already fixed in
`9e6c457cc`. The "seven floor tests" occurrences (8 across the tree) are
correct and need no action.

---

**Verdict: FLOOR-ERRATUM-COMPLETE.** Erratum authored as a separate document.
Frozen spec untouched. No em dashes. Paper untouched. Nothing pushed.
