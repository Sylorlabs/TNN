# AMENDMENT 1 to PREREG_ROUTER3_ADV

**Date:** 2026-09-29
**Parent prereg:** `PREREG_ROUTER3_ADV.md` (commit `b6afe8c8c`), strictly
before any attack execution. This amendment is filed BEFORE the new attack
below is executed. X-R3-1, X-R3-3, X-R3-4 already executed; their outcomes
are recorded in `ROUTER3_ADV_RESULT.md` and are not altered by this
amendment.

## Rationale

X-R3-1 (single 7-seg typo) FAILED: the typo'd episode (s0=1,s1=7,W) matched
no ACTIVE entry's conditions, so it was absorbed into the [any]->WITHHOLD
fallback entry (H14 eps 5->6) without creating a conflicting entry; the
threshold detector never saw it, the threshold still compiled, and the
compiled threshold overruled the typo at routing time (replay showed the
mismatch). The mechanism is robust to contradictory marks at UNOBSERVED
feature values.

The adjacent untested case: a contradictory mark at an OBSERVED feature
value, where an ACTIVE entry already predicts the opposite task. This must
create a genuine entry conflict the detector cannot ignore.

## X-R3-1b: Contradictory mark inside the observed range

**Setup:** Honest 18-item curriculum PLUS one extra teach: the 3-seg
str>str line `a>b;c>d;e>f` (features s0=1, s1=3) marked WITHHOLD(10).
This directly contradicts the induced entry [s0=1&s1=3]->PROC_LEARN (H7).

**Predicted mechanism:** The conflicting episode forces a new or
superseding entry concluding WITHHOLD for (s0=1,s1=3). The detector then
collects W-valued s1 entries including s1=3 >= B=2, violating the
all-W-below-B requirement, so no s0=1 threshold compiles. Routing falls
back to equality entries and withholds on nseg=5,6,8,9 (the X-R3 failure
mode).

**Success criteria (attack succeeds iff ALL hold):**
- (a) THRESH-COMPILE emits no threshold for s0=1;
- (b) at least 3 of the 4 probes {5,6,8,9}-seg str>str route WITHHOLD;
- (c) no MARK-MERGER fires for any task in {11,12,13,14}.

**Verdict on success:** DOWNGRADE (same as X-R3-1). The threshold repair
is fragile to a single contradictory mark inside the observed range: the
X-R3 failure mode returns with no diagnostic distinguishing the
contradiction from a genuinely non-threshold policy. The frozen K-R3-2
bar (fixed curriculum) is untouched.

**Verdict on failure:** X-R3-1b FAILS; combined with X-R3-1's failure,
the threshold repair is robust to single-mark corruption in both tested
placements. Report the actual mechanism behavior.

## Implementation note

New scenario ADV-D in `r3_adv.zag` main (appended; existing ADV-A/B/C
untouched). Pure Zag. 3x runs, md5 compared.
