# NO-GO MEMO: M4 R2 T2-targeted veto reopen

Wave: wave-20260924-1121pdt. Worker: M4 R2 reopen investigator.
Phase: prereg only. No implementation, no code, no runs beyond the
deterministic recount probe described below, no commits, no pushes.
This file is the complete output of the investigator phase.

## Machine-checkable provenance header

- RENDER_SHA: n/a (no render in this phase; prereg-only, no implementation)
- FIRST_RENDERED_WAVE: wave-20260924-1121pdt
- COMPONENT_LINEAGE: KB4V2 T4 epistemic boundary correction (ADOPTED
  narrowed to T4, 1421pdt, JUDGED); MD-SSD-1 T6 motiondir SSD estimator
  (ADOPT, 2021pdt, JUDGED); second-path part C T4/T5 independent veto
  (DISCARD, 0521pdt, JUDGED; T4 Goertzel/T5 centroid design lineage VOID
  on Python contact per M4 R1, may not be cited as independently
  validated); FS-F2C colorconst formation improvement (FINAL ALIVE at
  98.58 percent, 2026-09-24, JUDGED; Micah's work; colorconst front
  CLOSED and RETIRED for the loop); KB4 adversarial-FIR tail scout
  (NO-GO memo, 1121pdt, NEW); this M4 R2 T2-veto reopen memo (NEW, NO-GO).
- NEW_KNOWLEDGE_CLAIM: The 7 residual false adversarial installs are
  all in the senses-rebuild T2 colorconst, which is Micah's closed
  colorconst front (FS-F2C FINAL ALIVE subsumed and retired it), so the
  one permitted M4 R2 reopen path (a T2-targeted veto) is blocked by
  collision and the pinned 7/38 baseline stands.

## The M4 R2 closure and the one permitted reopen path

M4 R2 closed the veto-only mechanism class at 0521pdt: "a veto-only
mechanism over tasks with zero residual falses cannot improve
adversarial FIR; SP-B1 'strictly below' is unsatisfiable for the
class." The verdict (VERDICT_SECONDPATH_PARTE_C.md) and the M1/M4
debate rulings (JUDGE_RULING_0521.md) permit exactly one reopen: a
T2-targeted veto candidate under a fresh prereg, IF residual falses
exist inside the vetoed tasks, stated in frozen testable form. The
verdict records that all 7 false adversarial installs (pinned baseline
7/38 = 1842 bp) sit in T2 colorconst, outside the T4/T5 path-B
coverage. Vote-aggregation and fixed-point operator families are closed
under M4/S4 and are not touched here.

## False-install distribution (frozen testable form)

I verified the distribution two ways. First, committed evidence:
VERDICT_SECONDPATH_PARTE_C.md ("The 7 false adversarial installs are
all in T2 colorconst... There are 0 false T4/T5 adversarial installs"),
summary_run2.txt (cand_adv_false=7, cand_adv_installs=37,
cand_adv_fir_bp=1891), DEBATE_TRANSCRIPT.md ("all 7 falses sitting in
T2 colorconst"), REDTEAM_WAVE_0521.md (consistent with the frozen
2021pdt record and 0 false T4/T5).

Second, a deterministic Zag recount probe on HEAD (pure Zag, no
Python): I compiled the committed driver4.zag and judge4.zag with the
pinned Linux znc toolchain, using the byte-identical Linux
R33_NATIVE_IO_V1.zag (sha256
e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8,
the exact copy the 0521pdt wave vendored, recovered from
docs/lab/senses/pam-rebuild/round2/forks/FS-F2C/src/), and ran it over
the frozen fixture root
docs/lab/senses/rebuild/harness/fixtures. The regenerated decisions
log is sha256-identical to the committed 0521pdt record
(5081b621c939706f820bf20fba53d16cd6ee019c4e8b78d1566dad3c463a7ce5),
confirming the recount reproduces the original run exactly.

Frozen distribution, candidate arm, adversarial variant:

- Total false installs: 7. Total installs: 37. FIR 7/37 = 1891 bp.
- Falses by task: T2 colorconst 7; T1 colordisc 0; T3 shapetrans 0;
  T4 pitchdisc 0; T5 timbredisc 0; T6 motiondir 0.
- Installs by task: T2 colorconst 17; T4 pitchdisc 13; T5 timbredisc 5;
  T6 motiondir 2; T1 colordisc 0; T3 shapetrans 0 (the KB4
  collapse-abstention rule withholds all T1/T3 adversarial installs;
  firing set {colordisc, shapetrans}, unchanged).
- The 7 falses: fixtures p000 p002 p006 p008 p010 p016 p018, all
  task=colorconst, all truth SAME_SURFACE judged DIFFERENT. This
  matches the independent 2021pdt recount in PREREG_KB4_TAIL_1121.md
  verbatim (same 7 fixtures).

Testable form: "7 false adversarial installs total; 7 in T2
colorconst; 0 in T1; 0 in T3; 0 in T4; 0 in T5; 0 in T6." Residual
falses exist inside T2, the task a T2-targeted veto would cover. The
arithmetic precondition for the reopen is satisfied.

## The block: collision with Micah's closed colorconst front

The arithmetic precondition is satisfied, but the reopen is blocked by
closure collision. The evidence:

1. Micah's FS-F2C colorconst is FINAL ALIVE at 98.58 percent
   (1183/1200 on a fresh deterministic draw, byte-identical reruns,
   zero regression), documented in
   docs/lab/senses/pam-rebuild/round2/forks/FS-F2C/VERDICT_FS-F2C.md.
   It earned FS-E2 install scope and CLOSED the colorconst front.

2. The loop's own standing record retired the front:
   memory/2026-09-24.md records "Prereg decisions: colorconst RETIRED
   (Micah's FS-F2C FINAL ALIVE subsumed it)."

3. The 7 residual falses live in the senses-rebuild T2 colorconst:
   fixture root docs/lab/senses/rebuild/harness/fixtures,
   task=colorconst, confirmed by the deterministic recount above.
   This is Micah's closed colorconst front.

4. A T2-targeted veto is loop work on the colorconst task. The
   1121pdt tail scout (PREREG_KB4_TAIL_1121.md) already found that
   any loop candidate in this lane collides with Micah's shipped
   rule. The reopen requires, as a conjunct, that "a T2 veto there
   does not collide with his closed work." It does collide: the
   falses sit in his closed front, and the loop retired colorconst.

No clean-room mechanism avoids this. The tainted T4 Goertzel/T5
centroid lineage is in any case off-target (T4/T5 carry 0 falses) and
void for independent-validity claims per M4 R1. Any T2 veto would be
built around the residual falses of the old KB4-era j_colorconst
(65 percent adversarial, 87.5 percent primary) on a front where Micah
has already shipped 98.58 percent. That is iterating a played-out
substrate where he has won, not a free lunch. The standing direction
is to stand down there.

Micah's overnight work (FS-E4b, PAM round-4, H2 run-2, LI-HARDEN,
one-brain variant-B repairs, i32 OFFSET RULE, hell-hole V4, fable
work) was not re-litigated; no hole was found and none is claimed.

## Decision

STAND-DOWN. No T2-targeted veto prereg is filed. The one permitted M4
R2 reopen path is closed by collision with Micah's closed colorconst
front: the 7 residual falses belong to the senses-rebuild T2
colorconst, which his FS-F2C FINAL ALIVE subsumed and the loop
retired. The pinned 7/38 (1842 bp) adversarial FIR baseline stands.
A clean stand-down is a successful outcome: the distribution is now
verified by an independent deterministic recount, every reopen lane
is accounted for as closed or colliding, and nothing is forced.

## Verdict line

STAND-DOWN (M4 R2 T2-veto reopen blocked: residual falses are in
Micah's closed colorconst front).
