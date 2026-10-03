# AMENDMENT 1 to PREREG_REVISE5_ADV.md (transparent correction)

**Date:** 2026-09-29
**Amends:** PREREG_REVISE5_ADV.md (9f534872b), X-RV5-1 held-out
expectations. Frozen before any verdict is drawn.

## Error found

The prereg stated the hidden-truth (H) expectations as:
"zbq" -> H says "bbb"; "zaq" -> H says "qqq"; "zqw" -> H says "www".

This is wrong for "zbq". H is: IF input[2]=='y' THEN broadcast-first
ELSE broadcast-last. "zbq" = ['z','b','q']; input[2]='q' (113), not
'y', so H prescribes broadcast-last = "qqq", not "bbb". The last
byte of "zbq" is 'q'; broadcast-last repeats the LAST byte.

The first harness run exposed this: CHECK A0 (control) failed
because P0 correctly predicted "qqq" for "zbq" while the harness
expected "bbb". The mechanism was correct; the red-team fixture
constant was miscalculated.

## Correction

Corrected H expectations: "zbq" -> "qqq", "zaq" -> "qqq",
"zqw" -> "www".

## Why this is not a weakening

The kill criterion's logical content is unchanged: HARM = at least
one held-out mispredicted post-append while P0 predicted all three
correctly pre-append. Only the miscalculated byte constant is fixed
to what H actually prescribes. The observed mechanism behavior in
the first run already showed post-append predictions of "zzz" on
all three held-outs ([122,122,122] bytes); with corrected constants
all three are mispredictions vs H ("qqq","qqq","www").

## Lineage

- Prereg: 9f534872b (this amendment committed before the rerun).
- First (void) harness run: fixture error caught by the A0
  control; no verdict drawn from it.
- Rerun uses corrected constants; raw output will show the
  corrected CHECKs.
