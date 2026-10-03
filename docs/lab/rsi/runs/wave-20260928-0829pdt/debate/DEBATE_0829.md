# DEBATE TRANSCRIPT: wave-20260928-0829pdt

Date: 2026-09-28. Format: advocate argues FOR each motion, skeptic
argues AGAINST (gaming, confounds, weak bars, cost), judge renders a
reasoned ruling with numbers cited. A debate can overturn a verdict
only with cited evidence, never rhetoric. Every motion below carries
the skeptic's verbatim provenance probe: "What is the provenance of
the artifacts under judgment, and what exactly is new versus
inherited?"

Verdict slate under debate (all record-type motions; no candidate
adoptions this wave):
- M1: Fork battery 56 PASS, 0 FAIL, 2 UNTESTABLE at pin 9f3827356
- M2: Design lane NULL/HELD verdicts with nothing-manufactured statement
- M3: EXP1c attempt 5 stand-down recorded (no retune, no re-run)
- M4: Interactive survey NONE
- M5: tnn_chat FIT staleness 2 of 8, not due, not re-run
- M6: Prereg commit-order self-check VALID, VACUOUS for adoption
- M7: 0521pdt carried fork evidence discharged as evidence only

## M1: Fork battery verdict

ADVOCATE: The battery ran fresh this wave at the run-start pin
9f3827356, not carried. 58 named entries, 56 PASS, 0 FAIL, 2
UNTESTABLE, 47 unique commits. The znc pin 498abcb5 verified uniform
on all 56 tested entries; the pure-Zag harness rebuilt byte-identical
to the frozen instrument a2e6284c; negative controls discriminate on
all 56 (neg1_ok 56/56, neg2_ok 56/56); probe R32_ZNC_PROBE_OK on all
56. The two UNTESTABLEs are the standing pull-head pair with the
documented content cause. This is a CONFIRM verdict with full
evidence: adopt the record.

SKEPTIC: What is the provenance of the artifacts under judgment, and
what exactly is new versus inherited? The driver is inherited
(byte-identical to 0521pdt's run_one.sh, diff exit 0), the harness
source is inherited (f38d9154 extracted from the 2321pdt archive),
the znc is inherited (pin unchanged since before the battery
existed), 57 of 58 entries are fixtures with unchanged SHAs. The only
new thing is one live entry at the new pin, and the pin's delta is
two LOOP_STATE-only doc commits. The verdict is honest but thin: it
re-proves what the 0521pdt wave already proved at f03aa6fc8, and the
scope stamp admits the battery certifies toolchain stability only,
not commit contents. Could the CONFIRM label overstate a no-change
wave? And the duplicate count: 58 named entries but only 47 unique
commits, with 8 duplicate groups; the headline must carry both
numbers or it games the coverage claim.

JUDGE: CONFIRM, with the numbers stated plainly. The skeptic's
provenance probe is answered correctly and the advocate's claim
survives it: new this wave is a fresh execution at the new pin
9f3827356 (1 live entry), inherited is the driver, harness source,
znc pin, and 57 fixture SHAs. The verdict is not overstated because
the record states 56 PASS of 58 named entries over 47 unique commits,
live 1, fixture 57, and the scope stamp is explicit. Ruling: M1
CONFIRMED as a CONFIRM record. The 1721pdt probe-loss FAIL stays
closed (repair 37d1d3cab confirmed ancestor of the pin; probe
R32_ZNC_PROBE_OK on 56/56).

## M2: Design lane NULL/HELD

ADVOCATE: The hunt surveyed f03aa6fc8..9f3827356: 3 commits, 0
invention-dir changes, 0 mechanism hits, EXP2-K4 HELD (explicit
expiry question already on Micah's queue, not repeated), COMP2-P11
HELD (ruling 6 still OPEN, no new ruling text), intelligence trades
HELD, sensory NULL under standing stand-downs, and the 1721pdt
nothing-manufactured statement. This is exactly what the forward bar
requires: an honest NULL/HELD report. Adopt.

SKEPTIC: What is the provenance of the artifacts under judgment, and
what exactly is new versus inherited? Everything in this motion is
inherited status from the 0221pdt hunt: the same HELDs, the same
NULLs, the same open questions. New is only the merge-range
re-survey. The risk is status-quo laundering: recording HELD every
wave without movement can read as diligence while nothing advances.
Is there any evidence the lane is doing real survey work and not just
re-stamping? And on EXP2-K4: the recommendation is now several waves
old with his question unanswered; does HELD-with-no-expiry drift
toward indefinite deferral, and is the lane self-auditing that drift?

JUDGE: CONFIRMED. The survey evidence is real this wave: the range
was enumerated (3 commits listed with ids), the invention dir was
swept (0 changes), the counts are given. Re-stamping unchanged
statuses after a real survey is diligence, not laundering, provided
the record says nothing moved, which it does. On the drift concern:
the 0221pdt binding record already prohibits lane retirement on his
silence, so indefinite HELD is the mandated holding pattern, not a
drift; the question stays banked on his queue and is not repeated.
The nothing-manufactured statement is present and correct. M2
CONFIRMED as an honest NULL/HELD record.

## M3: EXP1c attempt 5 stand-down

ADVOCATE: The judge banked two explicit questions to Micah (Q1
exploration/exploitation redesign as a new design direction, Q2
K7-bar attainability or re-specification) and ruled no attempt-5
retune until he rules. Recording the stand-down this wave is the
correct motion: it prevents a retune that would violate a binding
judge ruling. Adopt the stand-down record.

SKEPTIC: What is the provenance of the artifacts under judgment, and
what exactly is new versus inherited? The stand-down is inherited
from the 0221pdt judge verdict; new this wave is only the
re-recording. Is there any temptation evidence the loop re-ran or
retuned EXP1c this wave anyway? A silent re-run would be the gaming
mode to watch for: progress theater behind a recorded stand-down.

JUDGE: CONFIRMED, with the skeptic's check answered by the commit
record: no EXP1c commits exist in f03aa6fc8..9f3827356, no
experiment dirs were added under the 0829pdt run dir, and the wave
evidence contains zero EXP1c artifacts. The stand-down held. M3
CONFIRMED as a stand-down record. The two questions stay banked on
Micah's queue; nothing is re-asked.

## M4: Interactive survey NONE

ADVOCATE: The range was swept read-only: 0 added files outside prior
records, 0 added .zag files, tree-wide ls-tree at the pin shows only
the pre-existing frozen batch probe instruments. The verdict NONE is
evidence-backed. Adopt.

SKEPTIC: What is the provenance of the artifacts under judgment, and
what exactly is new versus inherited? The NONE verdict is inherited
from every prior survey; the instruments cited are pre-existing.
Could the sweep have missed an interactive entry point added inside
the 0521pdt records (1,246 changed files)? The survey excluded the
prior-wave records from the "new entry points" grep; is that
exclusion justified, or does it assume what it should check?

JUDGE: CONFIRMED. The exclusion is justified: the 0521pdt records
were themselves wave-0521pdt loop artifacts (manifest, battery doc,
evidence dirs, scripts), already swept by the 0521pdt lane and by
this wave's fork battery; none contain interactive entry points, and
the battery's per-entry extraction confirms they are inert record
trees. The sweep method (added-file grep outside prior records plus
tree-wide ls-tree for tnn_chat/interactive names) is adequate for a
read-only survey. M4 CONFIRMED as NONE.

## M5: tnn_chat FIT staleness 2 of 8, not due

ADVOCATE: The last fresh re-run was at 2021pdt where staleness reset
to 0 of 8; this wave it is 2 of 8, not due. Not re-running is the
rule-following motion: re-running early would burn znc build cycles
for no verdict value. Record the staleness visibly and move on.

SKEPTIC: What is the provenance of the artifacts under judgment, and
what exactly is new versus inherited? The staleness count is carried
arithmetic, and the "not due" conclusion is inherited cadence. The
concern: is the 8-wave cadence itself still the right bar, or is the
loop coasting on a cadence nobody re-examined? Also, does staleness
2 of 8 mean the FIT instrument itself is two waves stale and could
miss a regression introduced in the two LOOP_STATE commits? That
would be a confound: claiming coverage the FIT no longer provides.

JUDGE: CONFIRMED with a note. The FIT instrument tests the frozen
batch probe, and the two intervening commits are LOOP_STATE docs
only (verified: 9f3827356 touches LOOP_STATE.md alone; 3e76c0fde
likewise per its record message), so no regression path exists for
the FIT to miss. The 8-wave cadence is a standing rule the loop may
not unilaterally change; questioning it is banked as an open note,
not a verdict. Staleness recorded as 2 of 8, visibly, not re-run.
M5 CONFIRMED.

## M6: Prereg commit-order self-check VALID, VACUOUS for adoption

ADVOCATE: This wave's commits will be record-only (manifest,
battery doc, hunt, survey, debate, LOOP_STATE). No prereg exists
because no candidate is adopted. The self-check is VALID over the
empty adoption set and VACUOUS: nothing needed a prereg, nothing
got adopted. Record it honestly.

SKEPTIC: What is the provenance of the artifacts under judgment, and
what exactly is new versus inherited? A VACUOUS check is a check
that checked nothing. Is "VALID, VACUOUS" an honest finding or a
way to skip the check? The gaming mode: waves with no candidates
always passing the check by construction makes the check a ritual.
Should the check instead be recorded as NOT APPLICABLE?

JUDGE: CONFIRMED as VALID, VACUOUS. The distinction matters and is
kept: VALID means the check was actually run (the wave's commit set
was enumerated and contains zero candidate adoptions, hence zero
prereg requirements); VACUOUS means the adoption set is empty. NOT
APPLICABLE would imply the rule does not cover this wave, which is
false: the rule covers every wave, and this wave it fired on an
empty set. The skeptic's ritual concern is noted as a standing
calibration point, not a verdict change. M6 CONFIRMED.

## M7: 0521pdt carried fork evidence discharged

ADVOCATE: The failed 0521pdt wave committed fork-lane evidence
ef418824b (56 PASS, 0 FAIL, 2 UNTESTABLE at pin f03aa6fc8), carried
as evidence only through the 0821pdt INCOMPLETE record. This wave
re-ran the full battery fresh at the new pin 9f3827356 with matching
results (56 PASS, 0 FAIL, 2 UNTESTABLE). The carried evidence is now
discharged: it agrees with a fresh execution and it never became a
debated verdict. Record the discharge.

SKEPTIC: What is the provenance of the artifacts under judgment, and
what exactly is new versus inherited? The carried evidence is
inherited (0521pdt's execution); the fresh re-run is this wave's.
The risk being checked: could the fresh run have been influenced to
match the carried evidence (confirmation pressure), and is the
discharge real or is the loop quietly upgrading carried evidence to
verdict status? Also, the fresh pin differs from the carried pin by
two LOOP_STATE commits; the results matching exactly is expected,
not informative.

JUDGE: CONFIRMED. The fresh run used the frozen driver byte-identical
to the carried run's driver and the same pins; matching results
under identical procedure at a docs-only-delta pin is the expected
outcome and is stated as such, not as new information. The carried
evidence is discharged as evidence only: it was never debated and is
not now promoted to a verdict. The honest treatment question in the
wave agenda is answered: full re-run plus verified carry-forward,
per precedent. M7 CONFIRMED.

## Judge's summary

Seven motions, seven CONFIRMs, zero overturns. The slate is
record-only: no candidate adoptions, no new judge-queue items, no
ruling changes, no sealed pairs touched. Numbers cited throughout:
58 named entries, 56 PASS, 0 FAIL, 2 UNTESTABLE, 47 unique commits,
znc pin uniform 56/56, harness a2e6284c byte-identical, negative
controls 56/56. The wave's honest-treatment question is closed by
M7. Commit-order check stands VALID, VACUOUS. Nothing in this
transcript weakens a frozen kill bar, adopts a candidate, or touches
a governance ruling.
