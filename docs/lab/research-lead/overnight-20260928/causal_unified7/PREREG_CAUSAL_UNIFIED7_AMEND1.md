# PREREG H-CAUSAL-UNIFIED7 AMENDMENT 1 (FROZEN)

**Date:** 2026-09-29
**Amends:** `PREREG_CAUSAL_UNIFIED7.md` (commit `db6981b27`)
**Status:** FROZEN. Committed before any harness build, fixture
execution, or result observation under this prereg. No
implementation output has been executed; only the mechanism
source edit exists (unexecuted). Both corrections below are to
the researcher's own pre-execution predictions, derived by
hand-tracing `learn_episode`/`predict` on the frozen fixture.

## Correction 1: K-CU7-1(b), entry 3 episode count

Prereg stated: "the phase-B/C carve is entry 3 and
`en_neps(W,3)==6`".

Corrected: entry 3's episode list is
`[21,22,23,24,25,26,28]`, so `en_neps(W,3)==7`.

Rationale: the phase-C carve (triggered by idx 27) moves the
six winners idx 21..26 into entry 3. The next phase-C episode
idx 28 (`2,0,0,2>0,0,0`) finds entry 3 ACTIVE via `find_entry`,
contradicts it, and `learn_episode` runs `entry_add_ep` BEFORE
the contest-capacity check, so idx 28 is appended to entry 3's
list and then entry 3 goes ST_CONFL (contest cap exhausted).
Frozen bar (b) is therefore:

(b) entry 3's episode list is exactly
`[21,22,23,24,25,26,28]` (`en_neps(W,3)==7`); the first six are
all `EP_COUNTED`; the seventh (idx 28) is `EP_ACT`. KILL on
any deviation.

## Correction 2: K-CU7-1(e), withhold path

Prereg stated: final query returns "r=0 (WITHHOLD
live-contradiction)".

Corrected: final query returns r=0 via the no-entry path
("WITHHOLD (no-entry)"), because every entry covering (2,0,0)
is ST_CONFL at that point and `predict` returns before
reaching the `live_contra_at` guard. The r=0 assertion stands;
only the reason string was mispredicted. Frozen bar (e) is
therefore:

(e) final `fu_predict(W,2,0,0,2,out)` returns r=0, and the
independent white-box helper `adv_live_contra(W,2,2,0,0)==1`,
proving the contradiction is genuinely live (counted winners
vs fresh evidence) rather than silently forgotten. KILL if
r!=0 or the helper !=1.

## Unchanged

All other bars (K-CU7-1(a),(c),(d), K-CU7-2..K-CU7-6), the
verdict rule, the repair R1..R5, and dispositions D1..D2 stand
exactly as frozen. This amendment weakens no bar: (b) is
tightened to the exact predicted list, (e) keeps the r=0
criterion and names the correct mechanism path.

## Governance

- Pure Zag; no Python.
- This document contains no em dashes.
