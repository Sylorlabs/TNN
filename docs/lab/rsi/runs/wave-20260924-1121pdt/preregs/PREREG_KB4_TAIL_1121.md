# NO-GO MEMO: KB4 adversarial-FIR tail scout

Wave: wave-20260924-1121pdt. Worker: KB4 adversarial-FIR tail scout.
Phase: prereg only. No implementation, no code, no runs, no commits,
no pushes. This file is the complete output of the scout phase.

## Machine-checkable provenance header

- RENDER_SHA: n/a (no render in this phase; prereg-only, no implementation)
- FIRST_RENDERED_WAVE: wave-20260924-1121pdt
- COMPONENT_LINEAGE: KB4V2 T4 epistemic boundary correction (ADOPTED
  narrowed to T4, 1421pdt, JUDGED); MD-SSD-1 T6 motiondir SSD estimator
  (ADOPT, 2021pdt, JUDGED); second-path part C T4/T5 independent veto
  (DISCARD, 0521pdt, JUDGED; design lineage VOID on Python contact per
  M4 R1); FS-F2C colorconst formation improvement (FINAL ALIVE at 98.58
  percent, 2026-09-24, JUDGED; Micah's work; colorconst front CLOSED);
  T2-targeted veto (narrow M4 R2 reopen, QUEUED-UNJUDGED, owned by another
  worker); this KB4-tail scout memo (NEW, NO-GO).
- NEW_KNOWLEDGE_CLAIM: The KB4 adversarial FIR tail is 7 false installs,
  all in T2 colorconst, so no mechanism outside the closed colorconst
  front and the worker-owned T2 veto reopen can move the pinned 7/38
  baseline.

## Pinned baseline

7 false / 38 installs = 18.42 percent (1842 bp) adversarial FIR, pinned
from the 2021pdt committed decisions log (MD-SSD-1 verdict, commit
3683b8f2c) and re-verified as the frozen SP-B1 bar at 0521pdt
(VERDICT_SECONDPATH_PARTE_C.md, JUDGE_RULING_0521.md M4 R2).

## Falses distribution (independent recount of committed evidence)

I recounted the committed 2021pdt decisions log
(decisions_md_run1.log, 925 DECISION lines, commit 3683b8f2c):

- Adversarial candidate installs by task: colorconst 17, motiondir 2,
  pitchdisc 14, timbredisc 5. Total 38.
- Adversarial candidate falses by task: colorconst 7, motiondir 0,
  pitchdisc 0, timbredisc 0. Total 7.
- Colordisc and shapetrans: 0 adversarial installs (the KB4
  collapse-abstention rule withholds all; firing set {colordisc,
  shapetrans}, unchanged).
- The 7 falses: task=colorconst, fixtures p000 p002 p006 p008 p010
  p016 p018, all truth SAME_SURFACE judged DIFFERENT.
- T4 pitchdisc adversarial falses: 0 (the kb4v2 correction is intact;
  PA-B1 holds). T6 motiondir adversarial falses: 0 (MD-SSD-1 holds).

This matches the MD-SSD-1 verdict verbatim: "the 7 remaining
adversarial false installs are exactly the untouched colorconst
cluster." One hundred percent of the residual tail sits in T2
colorconst. No other task carries a residual false.

## Mechanisms ruled out

1. Colorconst-front entries. The 2021pdt DIAGNOSIS.md queued design
   notes (linear cone-space LMS/Bradford second path for T2; T2 contest
   graduation on the MD-SSD-1 pattern; any T2 judgment replacement) are
   colorconst-front entries. CLOSED: FS-F2C is FINAL ALIVE at 98.58
   percent (1183/1200 on a fresh deterministic draw, byte-identical
   reruns) and closed the colorconst front. Owner direction is to stand
   down there. Any loop candidate in this lane collides with Micah's
   shipped rule.

2. T2-targeted veto. Withholding the 7 colorconst falses on
   disagreement is the one narrow M4 R2 reopen ("residual falses exist
   inside the vetoed tasks"). OWNED BY ANOTHER WORKER. Not duplicated
   here.

3. Veto over zero-false tasks. Any veto-only mechanism over tasks with
   zero residual falses (the T4/T5 part C class, or any analog on other
   tasks). CLOSED under M4 R2: SP-B1 "strictly below 7/38" is
   unsatisfiable for this class. Proven at 0521pdt: with 0 false T4/T5
   installs, the veto could only withhold a true install, moving FIR
   from 7/38 (1842 bp) to 7/37 (1891 bp); any k true-install vetoes give
   7/(38-k), which only grows. Part C was JUDGED DISCARD on this
   arithmetic, and the "revisit the SP-B1 bar definition" line was
   struck per M1 (weakening a frozen kill bar is an owner-red-line
   violation).

4. Vote-aggregation or fixed-point combination of judgment paths.
   Excluded under M4/S4 per the lane definition. The frozen part C
   arbitration rule is veto-only ("Path B never votes, never selects,
   never ranks, never aggregates"), and graduation of a second path to
   primary requires a separate frozen contest; for T2 that contest is a
   colorconst-front entry (closed, see item 1).

5. Tainted Goertzel lineage. The b4_dft_energy Goertzel bank from part C
   may not be cited as independently validated, and no future wave may
   adopt it without clean-room re-derivation under a fresh prereg
   (0521pdt governance deviation 1, M4 R1; Python touched the scratch
   source it is byte-identical to). Regardless, it targets T4, which
   carries 0 falses, so it cannot move the baseline.

6. Denominator expansion. Installing currently-withheld true
   adversarial judgments to dilute the FIR (for example by overriding
   the KB4 collapse-abstention rule or the contradiction machinery that
   withholds 16 true T4 adversarial judgments). Not a free lunch: it
   weakens frozen epistemic-humility machinery to game the rate, which
   is dumber (installing judgments the system has principled reasons to
   withhold), not an intelligence gain. No prereg is written on this
   basis.

## Why no mechanism remains

Every mechanism that can move the pinned 7/38 baseline must touch T2
colorconst, because T2 holds 100 percent of the residual falses and
every other task holds 0. Touching T2 is either a colorconst-front
entry (closed by FS-F2C, item 1) or the T2-targeted veto (owned by
another worker, item 2). There is no third lane: the veto-over-zero
class is arithmetically dead (item 3), aggregation is excluded (item
4), the Goertzel lineage is tainted and off-target (item 5), and
denominator gaming is not a free lunch (item 6).

## Decision

STAND-DOWN. No fresh prereg is filed. No implementation follows from
this scout in wave-20260924-1121pdt. A clean stand-down is a successful
outcome: the tail is fully characterized, every lane is accounted for
as closed, colliding, or owned elsewhere, and the pinned 7/38 baseline
stands until the T2 veto worker or Micah's colorconst line moves it.
