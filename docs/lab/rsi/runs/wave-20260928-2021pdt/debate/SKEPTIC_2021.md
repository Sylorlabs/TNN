# SKEPTIC: wave-20260928-2021pdt debate

Wave: wave-20260928-2021pdt. I argue AGAINST each adoption, attacking
gaming, confounds, weak bars, and cost. My provenance probe appears
verbatim in every motion: "What is the provenance of the artifacts
under judgment, and what exactly is new versus inherited?" The advocate
must answer it; a motion whose provenance story fails is void.

## M1: against the fork battery CONFIRM

The battery's scope is narrow by design: it certifies toolchain and
extraction stability, not the contents of the tested commits. A CONFIRM
here can be read as a stronger claim than the evidence supports. The
fixture set is heavy: 58 of 60 entries are frozen SHAs, so most of the
battery re-verifies old pins rather than testing anything new this
wave; only the two LIVE entries (both at the same SHA) exercise the
current tip. batch_2021.log is empty (0 lines), so no driver execution
trace survives; every verdict rests on RESULT.txt files, which I cannot
independently tie to a live execution beyond their timestamps and the
deterministic structure of the driver. The two UNTESTABLE entries keep
repeating for the same cause; the battery has never actually tested a
fork that lacks the pinned toolchain. And the harness binary is reused
from fb1421 rather than rebuilt from source this wave: I verified its
sha256 matches the frozen instrument (a2e6284c), but a byte-identical
binary is not a fresh build, and the "fresh execution" claim leans on
that reuse. Probe: "What is the provenance of the artifacts under
judgment, and what exactly is new versus inherited?" The execution is
new; the driver, harness, and 58 fixtures are inherited. My attack: the
adoption must stay scoped to process confirmation and must not be cited
later as evidence that the tip's contents are good.

## M2: against the design lane NULL/HELD

An empty survey range makes NULLs cheap: "nothing new in an empty
range" is true but nearly content-free, and the nothing-manufactured
statement is doing more rhetorical work than evidentiary work. The
EXP2-K4 HELD rests on an unanswered question that has now sat on
Micah's queue for four waves; HELD is not a verdict, it is a pause, and
repeated waves of HELD risk normalizing indefinite deferral. The
COMP2-P11 grep is a string search, not a semantic audit: "no new
ruling-6 text" only means nobody wrote the literal words, not that no
new Python-mirror-derived logic entered. Probe: "What is the provenance
of the artifacts under judgment, and what exactly is new versus
inherited?" The NULLs are new (empty-range survey); all HELD statuses
are inherited. My attack: accept the NULLs as range-scoped facts, but
do not let HELD read as progress.

## M3: against the interactive survey NONE

Same cheapness objection: an empty range yields NONE for free. The
survey did not run any binary, so "no runnable interactive TNN" remains
a code-text claim, never an execution claim. The frozen batch probes
have never been shown to exercise a live loop, and the FIT instrument
only tests batch behavior. Probe: "What is the provenance of the
artifacts under judgment, and what exactly is new versus inherited?"
The NONE is new (empty-range survey); the probe inventory is inherited.
My attack: the NONE must not be cited as evidence that interactive TNN
is impossible, only that no new entry point appeared in an empty range.

## M4: against the EXP1c stand-down re-verification

Re-verifying a stand-down by noting an empty EXP1c footprint is a
self-congratulation loop: the footprint is empty because the wave
attempted nothing, and attempting nothing is what the stand-down
requires. The two banked questions (Q1, Q2) are now four waves old
with no answer; the stand-down is correct procedure but the queue is
stagnating, and this wave does nothing to unblock it. Probe: "What is
the provenance of the artifacts under judgment, and what exactly is new
versus inherited?" The empty footprint is new; the ruling and questions
are inherited. My attack: keep the stand-down, but flag the stagnation
in the wave record rather than treating compliance as achievement.

## M5: against the commit-order self-check

The check fired on an empty set, which proves nothing about the
discipline that matters: the lane files are being committed by this
wave AFTER their evidence was produced, and their own "commit order" is
fine only because nothing is an adoption. The deeper caveat (commit
order evidences commit order only, never run order and never content
identity) means even a VALID verdict on a real candidate would not
establish the ordering that matters. Probe: "What is the provenance of
the artifacts under judgment, and what exactly is new versus inherited?"
Nothing is under judgment; the check result is vacuous. My attack: the
caveat must ride with every future citation of this check, and no
adoption may ever be described as "commit-order verified" without the
caveat attached.

## M6: against the FIT staleness accounting

Staleness arithmetic is only as good as the verdict-bearing-wave count
behind it, and this wave's verdicts are mostly confirmations of prior
records. If confirmations count as verdict-bearing, the staleness
denominator inflates; if they do not, this wave may not advance the
count at all. Either way the 4-of-8 number is bookkeeping, not evidence.
The FIT has not been re-run for four waves, and "the range is empty"
is a weak comfort: the last four waves were record-heavy, and a
regression hidden in a record is exactly what the FIT is meant to
catch. Probe: "What is the provenance of the artifacts under judgment,
and what exactly is new versus inherited?" The 4-of-8 arithmetic is new;
the 8-wave cadence rule is inherited. My attack: keep the count at 4
of 8 only if this wave's debated verdicts qualify as verdict-bearing;
if a stricter reading is intended, the loop should say so.

## M7: against VOID

VOID is the safest verdict and also the laziest: seven governance items
have now waited multiple waves with zero movement. Documenting them as
UNTOUCHED each wave is correct per the mandate, but the record should
not pretend that non-movement is neutral: the C12 stack remains in the
judge queue under a confounded stack, and the Python-mirror logic
question (ruling 6) still gates all mirror-developed logic. Probe: "What
is the provenance of the artifacts under judgment, and what exactly is
new versus inherited?" The VOID labels are new this wave; every
governance item is inherited and untouched. My attack: VOID is correct,
but the queue-fragmentation cost must stay visible in LOOP_STATE.md.

## M8: against the adoption motion

A wave whose verdicts are all confirmations, NULLs, stand-downs, and
VOIDs is indistinguishable in the record from a wave that ran nothing,
unless the evidence counts carry it. The fork battery's 60 evidence
dirs are the only hard new evidence; everything else is paperwork.
Probe: "What is the provenance of the artifacts under judgment, and
what exactly is new versus inherited?" The battery execution is new;
the rest is inherited. My attack: adopt the slate only if the verdict
lines distinguish [NEW] evidence from [VOID] placeholders, so no
future wave mistakes paperwork for progress.
