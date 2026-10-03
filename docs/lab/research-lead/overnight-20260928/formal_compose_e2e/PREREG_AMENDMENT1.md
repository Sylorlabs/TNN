# PREREG_AMENDMENT1.md -- FORMAL-COMPOSE-E2E

Date: 2026-10-03. Worker: FORMAL-COMPOSE-E2E. Lane:
`docs/lab/research-lead/overnight-20260928/formal_compose_e2e/`.
Status: PRE-VERDICT (no official runs yet; the debug run that
exposed the issue is not an official run).

## Issue

PREREG section 2.4 specified the extend-stack adversarial
battery derives `smid` from `SRC_ID32 = get32(stF,1268)` after
the FULL arm. A debug build showed `get32(stF,1268) = -1` at
that point: `ex_query` resets 1268 to -1 at the start of every
query, and Q2B (which reuses Z via the pipeline without
extending) runs after Q2, so the post-Q2 value is lost. With
smid=-1 the battery issued attaches from item -1 (no-ops on
REP; misrecorded u8 255 rows on LIST), and the E2E-EX lines did
not match the hand derivation (v16=0, a1=0 on LIST).

## Amendment

The driver captures `smid_q2 = get32(stF,1268)` immediately
after the Q2 `ex_query` (before Q2B), and the adversarial
battery uses the captured value. The value is still learner
state (SRC_ID32 written by ex_extend), only the capture timing
changes.

## Effect on frozen predictions and bars

None. The hand-derived predictions in PREREG 3.1 already assume
smid=1 (the correct SRC_ID32 value from Q2); the amendment
makes the implementation actually use it. Kill bars EK1-EK7 are
unchanged. The debug build that exposed the issue is discarded;
official 3/3 runs start after this amendment is committed.
