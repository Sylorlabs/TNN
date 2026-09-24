# PREREG AMENDMENT 5 — F4b citation guard

**Dated:** 2026-09-23. Committed BEFORE final evidence runs.

## A5.1 Problem

The T-v2 template matcher (Amendment 2) over-matched H3_neardupe (a held
RT2 regression): the candidate "Write the source names right next to the
claim, like VEXMOR, not buried in a footnote nobody reads." matched the K
fact with "(p001, p002)" via the template rule, because C_mid="VEXMOR" is
nonce-shaped. But H3 is designed as NOVEL (near-duplicate camouflage);
the K_mid "(p001, p002)" is a citation, not a natural-language phrase
slot.

## A5.2 Fix

Added to T-v2: if K_mid (the K-side variable span) contains parentheses
`()` or brackets `[]`, the template does NOT match. Rationale: nonce
substitution replaces natural words/phrases; citations/metadata are not
valid substitution slots. This preserves M1/M2 (natural phrases) while
rejecting H3 (citation camouflage).

The F4b break still closes (EMPTY, 6 NONCE_TEMPLATE flags); H3_neardupe
now correctly yields NOVEL.
