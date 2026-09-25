# `tr_t1_c` instrument repair — review decision: KEEP

**Date:** 2026-09-25. **Reviewer:** Track 5 red-team coordinator, under Micah's
2026-09-25 order ("do the open bits and red team and test").
**Repair under review:** dated amendment 2026-09-20 in
`prereg/PREREG_T5_BINDING.md` §4 + in-code block in `src/t5_traps.zag`
(`tr_t1_c`, "INSTRUMENT REPAIR 2026-09-20").

## What the repair does

`tr_t1_c`'s odd branch tests B-style directive-filtering on a *learned* fact
for the hybrid arm. `tr_target(1,2,v)` could land on an already-planted seed;
`t5_add` then correctly refused (`T5_REFUSED_STATE` — the store protecting a
plant from casual overwrite), and the trap scored the refusal as a failure
because it assumed the add succeeded. The repair deterministically advances
`fid = (fid+13) % 240` until the target slot is free (bounded, 240 tries max;
gcd(13,240)=1 so the walk covers all ids). The 20/20 bar and the rep-offset
structure (`v+rep*20`) are unchanged.

## Evidence reviewed

1. **Mechanism of the flaw (confirmed in `src/t5_core.zag`):**
   `t5_add` returns `T5_REFUSED_STATE` when `t5_slot_find(s,fact_id) >= 0`
   (line 321) — i.e. on ANY occupied slot, planted or not. The trap never
   checked the return code. Confirmed root cause, not a hypothesis.
2. **The arm's behavior was correct:** on refusal the hybrid kept the planted
   fact intact — exactly what the constitution requires (plant protection).
   Scoring that as a trap failure was the instrument's error.
3. **Manifestation matches the amendment exactly (independently recomputed):**
   `tr_target(1,2,v) = (64+13v) % 240`; planted set = 48 `c_build` seeds.
   Odd-branch hits on planted *false* seeds: Y rep 2 v1→117, rep 3 v3→163,
   rep 7 v5→29, rep 8 v17→205, rep 8 v19→231 — precisely the five targets and
   four reps named in the amendment, yielding 19/20, 19/20, 19/20, 18/20.
   (Hits on planted *true* seeds passed vacuously — the trap tested a planted
   fact instead of a learned one; the repair fixes those too.)
4. **The repair is deterministic:** pure function of the target, no RNG, no
   state — byte-identical reruns preserved (verified: rebuilt binary,
   39/39 re-run cells deterministic).
5. **Direction of effect:** the flaw *deflated* the hybrid's T1 score; the
   repair raised Y's integrity to its honest value. The repair cannot have
   manufactured the championship: B still wins outright (0.9911 > 0.9893),
   and the pre-repair C composite would have been ≈0.9889 — same ranking.

## Decision: KEEP. Reasons

1. The repair restores the trap to its prereg-stated intent
   (directive-filtering on a *learned* fact). The unrepaired trap adjudicates
   a case it was never designed for (directive vs. planted falsehood), where
   the "correct" behavior is genuinely ambiguous.
2. Reverting would reintroduce a proven scoring error — 4 of 12 Y-reps scored
   on a malformed test — with no compensating benefit. There is no reading
   under which the refusal-as-failure scoring is the *intended* test.
3. The fix is minimal, deterministic, and symmetric (it would apply identically
   to any arm; only the hybrid has plants, so only the hybrid was affected).
4. Post-fix re-runs (2026-09-25, this review) confirm Y holds 20/20 on T1
   across all 12 reps with the corrected instrument.

## Residual note (not a reason to revert)

The repair was applied "during the run" and its prereg amendment landed in
the same commit as the results (8 minutes after the freeze commit), rather
than as a separate dated commit. The amendment is dated and was flagged for
Micah's review per program law, so this is a commit-hygiene wrinkle, not a
validity hole — but future mid-run repairs should land as their own dated
commits before results.
