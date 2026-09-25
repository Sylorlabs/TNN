# LEAKFIX — WS2-L ARM B battery leak repairs (frozen prereg → validated batteries)

Authority: `docs/lab/cognition_ws/ws2l/PREREG_WS2L.md` (frozen).
Every rephrase below was required by the §6 gate: the initial extraction produced
ARM B scores deviating from prediction (phase-1 exact-overlap leaks), and each
change was applied, re-run through the real `tocb` binary, and recorded here.

Mechanism note (discovered during validation, 2026-09-25): `init` sorts items by
ID ascending (byte-lexicographic, `bytes_lt`); retrieval score is
`cell_score*1000 + own_score`; ties break to the lexicographically smaller item
ID. The Python mirror used for leak-hunting was corrected to match (verified:
26/26 queries identical to the binary).

## Applied rephrasings (10)

### 1. query QFR06
- old: `the lengthy voyage lasted three weeks by boat`
- new: `the lengthy voyage lasted a month by boat`
- why: query shared "three"+"week" exactly with FR06 item (phase-1 leak; B would
  score FRESH 1/6). "week" also hits v1.1 PP02 ("for weeks"). Rephrased duration
  to "a month" (zero corpus overlap); listed pairs unchanged.

### 2. query QD1
- old: `the airplane soared above the clouds`
- new: `the airplane glided across the sky`
- why: shared "above"+"cloud" with FR04 (phase-1 leak). Rephrased with zero
  corpus overlap.

### 3. item DS6
- old: `the neighbor lent him a ladder yesterday`
- new: `the neighbor loaned him a ladder yesterday`
- why: QD6/QAN3 must test lend|borrow non-bridging, but any lend-lexeme query
  phase-1 hits DS6's "lent" exactly (stem identity), making B-abstain impossible.
  "loaned" keeps DS6 a near-synonym distractor while removing the exact identity.

### 4. query QD6
- old: `she lent the reaper to her friend`
- new: `the farmer lent the reaper to a friend`
- why: shared "she"+"her" with BOR1 (phase-1 leak → B retrieved BOR1). Removed
  pronoun overlap; keeps lend-lexeme so the lend|borrow veto test is intact.

### 5. query QAN3
- old: `she lent the reaper to her friend`
- new: `the farmer lent the reaper to a friend`
- why: same text as QD6; same BOR1 leak. Same fix.

### 6. query QMH2
- old: `the gathering will commence at midday sharp`
- new: `the gathering must commence at midday precisely`
- why: shared unlisted "will"+"sharp" with MH2 (phase-1 leak; B would score
  MULTI-HOP). Kept listed pairs (meeting|gathering, begin|commence chain) intact.
- note: an intermediate attempt with "shall" leaked to v1.1 PX01; reverted.

### 7. query QMH3
- old: `the joyful kid frolicked all day`
- new: `the joyful kid frolicked till dusk`
- why: shared unlisted "day" with MH3 (phase-1 leak).

### 8. query QMO1
- old: `they went to the bazaar every dawn`
- new: `he went to the bazaar at daybreak`
- why: shared "dawn" with DS2 (wrong-item retrieval) and "they" with MO1. Keeps
  tested pair go|went + helper market|bazaar; zero corpus overlap.
- note: an intermediate attempt with "we" leaked to v1.1 PX01; reverted.

### 9. query QMO3
- old: `the children frolicked outdoors every day`
- new: `the children frolicked outdoors nightly`
- why: shared unlisted "day" with MH3 (wrong-item retrieval). Keeps
  child|children + played|frolicked.

### 10. query QMO4
- old: `the teeth throbbed through darkness`
- new: `the teeth throbbed in darkness`
- why: shared unlisted "through" with DOG1/MO4 (wrong-item retrieval). Keeps
  tooth|teeth + helpers ached|throbbed, night|darkness.

## Reverted attempts (2, not in final batteries)
- QMH2 with "shall" instead of "must": leaked to v1.1 PX01. Reverted to "must".
- QMO1 with "we" instead of "he": leaked to v1.1 PX01. Reverted to "he".

## Structural non-fix: QD3 (DIST) vs QAN1 (ADV-NEAR)
QD3 and QAN1 are byte-identical queries (`the canine watched the flock in
darkness`, gold DOG1). The frozen synonym table contains none of
dog|canine, guarded|watched, sheep|flock, night|darkness, so ARM B abstains on
both. §6 predicts DIST 6/6 (QD3 must pass "via canine|dog") and ADV-NEAR 4/6
(QAN1 must MISS because the pair is absent) — mutually inconsistent for a
deterministic mechanism on identical inputs. Making QD3 pass would require
deliberately adding phase-1 exact overlap, violating the battery's zero-overlap
purpose. NOT fixed; recorded as a frozen-prereg contradiction in B_BASELINE.md.
Attained: DIST 5/6.

## Official-51 interference note (observation, not a battery change)
On the combined corpus (v1.1 + 25 new), frozen official query QP04
(`routine arranging numbers ascending via neighbor exchanges`, gold PP04) ties
at tot=1001 with new items BOR1 and DS6 (shared stem "neighbor") and loses the
ID tie-break (BOR1 < DS6 < PP04) → QP04 retrieves BOR1 (50/51). OFFICIAL-51 is
defined on the frozen v1.1 corpus as-is (51/51 replicated, byte-identical);
the combined-corpus interference is documented for the ARM L worker's awareness.
No new-battery text was changed for this.
