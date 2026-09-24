# PREREG AMENDMENT 4 — F5 skeleton extension + variant clarifications

**Dated:** 2026-09-23. Committed BEFORE final evidence runs.

## A4.1 F5 skeleton: capital confusables added

The frozen skeleton (§3.5) included Cyrillic/Greek small letters but not
capitals. V5b uses U+0405 (CYRILLIC CAPITAL LETTER DZE, looks like Latin S).
Added to skel_fold: U+0405→s, plus 10 Cyrillic capitals (АВЕКМНОРСТХ→abekmhopctx)
and 14 Greek capitals (ΑΒΕΖΗΙΚΜΝΟΡΤΥΧ→abezhikmnoprtyx) that are visual
confusables for Latin. The "bounded skeleton" design is unchanged; the
table is extended within the frozen approach.

## A4.2 F1-V1c clarification

V1c (table entry swapped to wrong K) yields EMPTY (marked KNOWN via the
table), not NOVEL. This is correct per the fork design: the fork trusts
the translation table unconditionally. Table correctness is a curation
requirement (§3.1, Amendment 2 polysemy note). The variant demonstrates
that a corrupted table causes false-known; the safeguard is curation, not
mechanism. Prereg expectation amended: V1c → EMPTY (fork follows table).

## A4.3 F3-V3b clarification

V3b (cross-page halves) yields WITHHELD (SINGLE_SOURCE), not NOVEL+install.
The halves on p1/p2 appear on only one page each, so the base mechanism
withholds them per SINGLE_SOURCE. On p3 (both halves together) they
reassemble to KNOWN. This is correct: the fork does not reassemble across
pages (§3.3), and the base withhold rule applies. Prereg expectation
amended: V3b → WITHHELD (2 withholds, p3 halves KNOWN).
