# Protocol v2 DRAFT: QA Report

**Verdict: PROTOCOL-QA-COMPLETE.** 3 minor documentation issues. 0 blocking
issues. 0 contradictions. 0 broken cross-references. 0 missing sections.

**Method:** full sequential read of `LIFETIME_PROTOCOL_V2.md` (1207
lines, sections 0 through 19), then grep verification of every
`Section X` cross-reference, every end-state term, every CORRUPTION
event field order, and all section headers. External jargon (P4, H1)
traced to its defining documents.

## What passed

**Cross-references: all resolve.** Every unique `Section X` reference
in the document (4, 4.1, 5, 6, 6.1, 6.2, 7.7, 7.8, 8, 9, 12, 15, 16,
17, 19) points to a section that exists with the expected content.
Spot checks:

- Section 0 item 10 "Affects: Sections 5 (step 4a), 6 (new 6.2), 7.7,
  18" — step 4a exists in Section 5, Section 6.2 exists, Section 7.7
  references the detector, Section 18 has the CORRUPTION EVENTS
  bullet pointing to 6.2. All correct.
- Section 5 step 4a references "Section 6.2" and "Section 6.1" —
  both correct.
- Section 6.1 CORRUPTION references "(detection algorithm:
  Section 6.2)" — correct.
- Section 6.2 item 13 references "the Section 7.7 end-states" —
  correct.
- Section 7.7 references "the detector (Section 6.2)" — correct.
- Section 12 control 8 references "Section 4.1 and Section 9" —
  both correct.
- Section 16 item 8 references "Section 4.1", "Sections 9, 11",
  "Section 6" — all correct.
- Section 19 D4 references "(Section 16, item 6)" — correct.

**Terminology: ZOMBIE / FOSSIL / CORRUPTION / DELETED consistent.**
Three independent definitions agree:

- Section 6.1 (ZOMBIE-STATE): LIVE = root valid; FOSSIL = root cells
  evicted, MAP inert but occupying budget; ZOMBIE = root field
  points to wrong-typed node; DELETED = evicted cleanly.
- Section 6.2 item 13 (retention-sweep mapping): LIVE -> LIVE;
  ZOMBIE, Z_SHARED, Z_HIJACKED -> ZOMBIE; FOSSIL -> FOSSIL;
  evicted MAP -> DELETED.
- Section 7.7 (four end-states): same four with matching glosses,
  plus the explicit rule that Z_SHARED and Z_HIJACKED classify as
  ZOMBIE at the sweep.

**Event field orders match.** `CORRUPTION(world, map, field,
expected_type, actual_type)` is identical in Section 6.1, Section
6.2 item 7, the worked examples (`CORRUPTION C 45 20
graph-cell(101|102|103|104) tag-902`), and the extension emission
in item 10(a). Fixed field order discipline holds.

**No contradictions between normative sections.** Checked pairs:
K-LT-2 budget-fraction bar (Sec 11) vs degradation reporting
(Sec 7.7); DECLINE zero-expectation (Sec 6.1) vs capability
assessment (Sec 13); GOAL_* NOT-APPLICABLE (Sec 6.1) vs
spontaneity caveat (Sec 8.1) vs assessment (Sec 13); R ratio
definition identical in Sec 7.4, 7.8, and 11; trial-must-run
VOID rule (>2/10 fact_hit) identical in Sec 9 and Sec 12
control 8; V2-hole trap reporting consistent across Sec 4,
7.6, and 11.

**Section numbering: clean.** Headers 0 through 19 present, no
gaps, no duplicates. Subsections 3.1-3.4, 4.1, 6.1, 6.2, 7.1-7.8,
8.1 all present.

**Dashes:** zero em dashes, zero en dashes in the protocol file
(byte-verified).

## Issues found (minor, non-blocking)

**QA-1 (stale changelog entry): Section 0 item 7 vs Section 7.7.**
Item 7 says the interference measure "distinguishes four
end-states: live, retired (future), deleted, fossil (accidental)."
Section 7.7 actually defines the four as LIVE, DELETED, FOSSIL,
ZOMBIE; "retired" is described there as a potential *fifth*
end-state for future builds, not one of the four. The entry
predates the corruption-detector integration (item 10), which is
what introduced ZOMBIE into the taxonomy. The changelog as a whole
remains accurate because item 10 covers the ZOMBIE addition, but
item 7's list is outdated as written. Fix (not applied): update
item 7 to name ZOMBIE instead of "retired (future)", or annotate
it as superseded by item 10.

**QA-2 (undefined in-document term): "P4 profile" (Section 11,
K-LT-2).** The text reads "catastrophic answer loss (per the P4
profile and the eviction-corruption refinement)." P4 is a
prediction label from `q4_baseline/PREREG_Q4BASELINE.md`, defined
in the broader research program but not in the protocol. A reader
holding only the frozen protocol cannot resolve the term. Fix
(not applied): add a parenthetical gloss or a source citation.

**QA-3 (undefined in-document term): "H1 widening" (Section 17).**
The text reads "H2 runs standalone per Micah's ordering (H2 before
H1 widening)." H1 widening is defined in
`tnn3_roadmap/TNN3_ROADMAP.md` (the open-constructor phase) but not
in the protocol. Same reader-isolation concern as QA-2. Fix (not
applied): add a parenthetical gloss or source citation.

## Explicit non-findings

- The Section 6.2 item 12 phrase "require the extensions" carries
  no section number and refers unambiguously to item 10 directly
  above it. Not an error.
- The WORLD A/B/C/D/A' subsections under Section 4 are titled
  `### WORLD X`, not numbered 4.2-4.6. No numbered subsection is
  referenced, so nothing dangles.
- "Section 6." with trailing period (one occurrence) is sentence
  punctuation, not a distinct reference.

## Standing metrics (this QA)

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 0 (read-only audit).
- All other fields: 0.
- Files: 2 (NAMECHECK.md, PROTOCOL_QA.md). No source touched.
