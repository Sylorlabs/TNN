# DEBATE: wave-20260927-1121pdt (advocate / skeptic / judge transcript)

Panel: ADVOCATE (argues FOR each adoption or confirmation), SKEPTIC
(argues AGAINST: gaming, confounds, weak bars, cost), JUDGE (renders
reasoned rulings with numbers cited). Working copy ~/workspace/tnn-rsi,
branch tnn-native-lab. Panel convened at local HEAD 759fd30b5
("wave-20260927-1121pdt: red-team review of EXP1c freeze plus verdict
slate"). Pure Zag only in every lane under judgment; this transcript was
authored as plain text with zero Python (no interpreter invoked, no
Python written or run). No em dashes in this document. Nothing pushed.
docs/lab/continual_learning/ untouched (verified: git diff clean on that
path). The six governance rulings, all sealed blind pairs, and DP-1 are
[VOID] to this debate: not decided, not relitigated, not re-presented.

Read before debating: FORK_RESULTS_1121.md, CANDIDATE_LANE_1121.md,
REDTEAM_1121.md, PREREG_EXP1c_FROZEN.md (all under
docs/lab/rsi/runs/wave-20260927-1121pdt/).

## ROUND 0: the standing provenance probe

SKEPTIC (mandatory probe, verbatim): "What is the provenance of the
artifacts under judgment, and what exactly is new versus inherited?"

ADVOCATE (answers per item, with commit ids, first wave, lineage, and
new knowledge claim):

Item 1, fork battery: evidence commit ab577d0e6
("wave-20260927-1121pdt: fork battery results plus frozen enumeration
manifest"). FIRST_RENDERED_WAVE for the battery design:
wave-20260923-2321pdt (frozen harness fork_battery.zag, extracted sha256
f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738) with
the 0821pdt orchestration layer; fresh re-execution this wave
(wave-20260927-1121pdt), fresh scratch /tmp/fb1121, harness rebuilt and
sha verified against the pins. COMPONENT_LINEAGE: 2321pdt frozen
driver plus 0821pdt orchestration; 51 named entries, 42 unique commits,
3 live, 48 fixtures. NEW_KNOWLEDGE_CLAIM: none. The battery certifies
toolchain and extraction stability only, per its scope stamp; it makes
no claim about the contents of the tested commits.

Item 2, EXP1c prereg: design draft 59b9df4b0 (wave-20260927-0821pdt
lane 3); gate evidence commit 463b115b6 (wave-20260927-0221pdt,
the six EXP1b red-team corrections plus WAVE_NOTES_EXP1B.md);
training-mass extension 5a043af3c; freeze commit 8b456736b.
COMPONENT_LINEAGE: EXP1 original 19f97c6cb, then the 2321pdt
reimplementation 74565859f (where the bounce identity-reflection bug
was introduced, now corrected in the record), then the EXP1b retune
(wave-20260927-0221pdt, invention claim DEAD, K4/K6 KILL), then this
design. NEW_KNOWLEDGE_CLAIM: none yet. The prereg proposes the first
design in which the compositional-choice question is non-null (shrunk
399-plan space, 1200-tick horizon, decaying novelty bonus, new K7
choice-reality guard). New this wave: the freeze package (mass plus
frozen prereg). Inherited: the draft text, the six corrections cited
as 463b115b6, the EXP1b mass inherited verbatim with exactly three
documented deltas.

Item 3, queued drafts EXP2-K4 / B1-P9 / COMP2-P11: all three drafts are
inherited from 59b9df4b0 (wave-20260927-0821pdt lane 3). First wave:
0821pdt. COMPONENT_LINEAGE: B1-P9 inherits the B1 BOUNCE DISCARD
(never re-scored); COMP2-P11 inherits the CV-1 adoption plus the
ruling 6 gate (OPEN; LOOP_STATE lines 2791-2792 list "CV-P adoption
still doubly gated (ruling 6 pending)"); EXP2-K4 inherits the 0221pdt
EXP2 follow-up's S2/S3 holdout finding (fidelity evidence only, judge
ruled). NEW_KNOWLEDGE_CLAIM: none. The gate-check findings this wave
(the corpus does not exist; no new B1-class mechanism; ruling 6 still
open) are the wave's new factual findings about gates, not new
mechanisms.

Item 4, his continual_learning flagship: prereg commit 8c22ffb9b,
BUILD+RUN commit 36342eb51 (line verdict GO), in-repo red-team report
commit 899757bc2 (records NO-GO). Author of 899757bc2: micahcooley,
dated 2026-09-27 11:23:07 -0700, after his own GO at 36342eb51.
These are his artifacts, not loop artifacts. FIRST_RENDERED_WAVE for
the loop's knowledge of them: this wave (the run-start merge brought
them in). NEW_KNOWLEDGE_CLAIM by the loop: none, and the loop must
make none; the proposed LOOP_STATE entry is citation only, CLOSED.

Item 5, rh-pull-1-head and rh-pull-2-head: commits 5802fec84 and
4b76bb59f (refs/remotes/rh-pull-N-head carried over from 0821pdt,
tips confirmed identical via ls-remote). Non-TNN research-doc repos;
no src/ directory; pinned toolchain path absent. Ten consecutive
waves of extraction failure with the identical cause. These entries
are inherited fixtures of the battery population, not TNN candidates.

JUDGE: the probe is satisfied. The record is now clean enough to
argue on. Proceeding to the contested calls.

## ROUND 1: fork battery CONFIRM and the perpetual UNTESTABLEs
(the most contested call on the slate)

ADVOCATE: The CONFIRM is earned, not ceremonial. Evidence commit
ab577d0e6 records a fresh enumeration at run start (28 local
branches, 6 remote-tracking refs, 14 worktrees, all SHAs re-verified),
fresh extraction per entry, a harness rebuild verified against the
frozen pins (harness source sha256
f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738,
znc pin 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef),
and exit 0 with VERDICT=PASS on 49 of 49 tested entries. Uniform
evidence, grepped not sampled: B1 byte-identical FORKBATTERY-OK 42
(run sha 5dfe3c161096819c8c0dd6057c4df9944ddd884f57b9a513b47e7655d53c6066),
B2 bin sha 75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2
on all 49, B3 strict check exit 0 on all 49, NEG1 failing with E0002
on all 49, NEG2 differing at char 1 on all 49, tree probe
R32_ZNC_PROBE_OK on all 49. The two UNTESTABLEs were not faked as
passes: git show exit 128, 0-byte redirects deleted, RESULT.txt plus
extract.err archived honestly. The dry run entry (arch-20260923-2321pdt)
has a RESULT.txt byte-identical to the 0821pdt evidence. Against the
recommendation to reclassify: the per-wave extraction attempt is the
only instrument that will ever notice these two trees becoming
testable. Permanently labeling them OUT OF SCOPE trades an honest
known unknown for a blind spot.

SKEPTIC: Ten waves of identical UNTESTABLE with an unchanged cause
is not a sentinel, it is wallpaper. The panel keeps citing "the only
instrument that will notice them becoming testable" as if anyone
checks what nobody reads. The headline 51 named entries with 49 PASS
inflates the denominator and reads like coverage growth when nothing
grew. Two better options exist and the red team named both: formally
reclassify rh-pull-1/2 as OUT OF SCOPE with the recorded reason, and
report the battery as 49/49 on the scoped population; or actually
cover them by vendoring the pinned toolchain into the pull-head
extraction. Perpetuating UNTESTABLE counts is the third option, the
worst one, because it normalizes not-testing as a verdict category.
Also, "toolchain and extraction stability only" is doing a lot of
work in the scope stamp: if the certification is this narrow, what
does 49 PASS actually tell the parent that the pin shas alone did not?

JUDGE: Both positions have force, and the evidence decides between
them. Numbers first: 51 named entries, 49 PASS, 2 UNTESTABLE, 0 FAIL,
0 CONFIRM; 42 unique commits; 3 live entries, 48 fixtures; evidence
commit ab577d0e6. On the skeptic's "what does 49 PASS tell the
parent" challenge: it tells him that the pinned toolchain still
extracts byte-identical and behaves identically across every
toolchain-bearing fork, including the live origin tip 899757bc2 that
carried his own flagship commits in at run start. That is the battery's
contract, and it held on all 49 tested entries with uniform grepped
evidence. CONFIRM stands.

On the reclassification recommendation: I rule against adopting it,
with cited evidence. The UNTESTABLE cause is content-dependent (the
trees lack the pinned toolchain path), not permanent; the loop has
seen trees change content before (origin/tnn-native-lab moved this
very wave from 7aad68fad to 899757bc2). A permanent OUT OF SCOPE
label would remove the only automated check that fires when those
trees change. The red team's second option (vendor the pinned
toolchain into the pull-head extraction) manufactures testability in
two research-doc repos the loop does not own; that is coverage
theater, not coverage. The first option (permanent OUT OF SCOPE) is
honest but trades away detection. Keeping the per-wave UNTESTABLE
with the identical cause recorded is the least bad option, provided
the headline never stands without the scope caveat. Ruling: the
recommendation stays recorded as dissent for the parent; it is NOT
adopted into the verdict. Coordinator verdict 1 is CONFIRMED with
the numbers above, and every future headline for this battery must
carry the scope stamp ("toolchain and extraction stability only;
the two pull-head entries are non-TNN research-doc trees with an
unchanged extraction failure, ten waves running").

## ROUND 2: the EXP1c freeze (was freezing in-wave the right move?)

ADVOCATE: Freezing was the right move, and delaying would have been
process theater. Gate (a) was satisfiable: the six EXP1b corrections
plus WAVE_NOTES_EXP1B.md are all committed in 463b115b6, and the red
team content-verified five of the six by independent git show plus
the deliverable by cat-file (no hollow corrections found). The freeze
ordering is valid by topology: 59b9df4b0 (design) strictly precedes
5a043af3c (mass), which strictly precedes 8b456736b (freeze). No
implementation commit exists anywhere in the ancestry between freeze
and local HEAD 759fd30b5. K1-K7 are byte-identical to the draft
(diff reports zero differences). The mass commit is 89 insertions, 0
deletions, 0 modifications to existing files: pure knowledge text, no
runner code, no scoring, no recipe table. Pre-run assertion is
recorded: pre-run, no scores seen. The two redraft fixes were
drafting errors that had to die before the seal: the draft's M4(c)
said "taught H5" while kb.txt already defines H5 as the EAT rule
(H1-H8 all taken), so a literal H5 void-safety would have made the
mass self-contradictory and poisoned the K4 novelty audit; the
"src/world.zag" path does not exist, the real template is
docs/lab/invention/survival/src/world.zag (bounce-fixed by
938d188cb). Both fixes are documented in the frozen prereg's section
0, both happened before the freeze, and neither moves a bar. This
design is the first in the invention line with a non-null
compositional-choice question (399-plan space, 1200-tick horizon,
decaying B0, K7 choice-reality guard), directly answering the 0221pdt
judge's forward requirement and the EXP1b finding that "composition
is the broken link." The cost budget is fixed compute: 12 variants x
5 arms x 1200 ticks x 2 determinism runs = 144,000 agent-ticks, pure
Zag, pinned toolchain. Nothing was pending that one more wave of
draft status would have resolved.

SKEPTIC: Three objections. First, the freeze happened in the same
wave that authored the mass extension: the lane that wrote 5a043af3c
also sealed 8b456736b. There is no cooling between authorship and
freeze, and the two drafting errors (H5 versus H9, the world.zag
path) prove the draft was still being edited at seal time. If the
draft had stayed a draft, those errors would have been caught by
ordinary review instead of by the freezing wave under its own time
pressure. Second, cost: 144,000 agent-ticks is the largest compute
commitment in the invention line this week, and it is now locked
behind frozen bars that include a brand new bar (K7) that has never
been exercised against any implementation. Freezing an untested bar
is a bet, not a procedure. Third, the implementer is the same loop:
the commit-order self-check is the only guard between freeze and
implementation, and it is recorded by the implementing wave itself.

JUDGE: The skeptic's objections are serious and I take them in
order. On cooling: the objection has a real premise (errors were
found at seal time) but the wrong conclusion. The H5/H9 and path
errors were found and fixed before the freeze, documented in section
0, and both fixes are auditable against the committed files. Keeping
the prereg a draft for another wave would not have added any review
surface that the red team lane did not already provide: the red
team independently re-verified the gate evidence, the bar identity,
and the mass content at 759fd30b5. A draft held for cooling would
have waited on nothing; gate (a) was satisfied and no governance
ruling gates this design. On the cost: 144,000 agent-ticks is
compute, and the pure-Zag requirement is pinned; but the skeptic is
right that K7 is an unexercised bar. The correct reading of K7 is
that it is a validity gate, not a kill: if it fails, the run is
VOID as a test of H1/H2 (the design failed, not the agent), and the
implementing wave must reproduce the section 7 enumeration bound in
evidence. An untested validity gate that voids rather than kills is
the safe direction to err in. On the self-check: it is recorded by
the implementing wave, but the evidence is git topology, which is
not the wave's to forge; the freeze commit 8b456736b is already
sealed, and any implementation commit must strictly follow it.
Ruling: the in-wave freeze was the right move. Coordinator verdict
2 is CONFIRMED: EXP1c FROZEN [NEW] at 8b456736b, queued for future
implementation under the frozen bars. The skeptic's K7 caution is
recorded as a watch item for the implementing wave, not a veto.

## ROUND 3: the queued drafts and the honest null hunt

ADVOCATE: The lane reported the gates honestly and did not
manufacture a candidate, which is exactly what the loop's rules
demand. EXP2-K4: the gate needs 12 real deliberation failure traces
with spec-blind curation, recorded expected outcomes, and commit-order
qualifying selection. The repo holds 27 run-output files in
onebrain3/traces/ from round-3 measurement, committed under
51b7de35d: no expected outcomes, no curator attestation, no
qualifying rule. The S2/S3 holdouts are construction-guaranteed
synthetic probes, which the judge already ruled are fidelity
evidence only. Building the corpus is a new data-collection exercise
(frozen single-deliberation machinery over a problem set, find real
wrong-verdict traces, spec-blind curator, first 12 by commit order).
EXP1c froze on gate (a) precisely because the gate was satisfiable;
EXP2-K4's gate is not, so it stays QUEUED. B1-P9: no new B1-class
(post-pass recolor) mechanism exists since the DISCARD; the only
recent image_upscale commits are the LIGHT-FIELD workstream (KILLED
clean: BAR1 FAIL sealed minus 1.853 dB, BAR2 FAIL checkerboard about
3x worse) and the round-3 honest all-arm kill 7aa40ac0d. The P9 bar
set is a re-freeze template; per its own section 9, bars do not
invent mechanisms. COMP2-P11: gate zero blocks while ruling 6 is
OPEN (LOOP_STATE lines 2791-2792). The null hunt is the honest
verdict: gate (a) froze one draft, so the lane order authorized no
further hunting, and nothing was ready for adopt or discard.

SKEPTIC: An honest null is still a null, and the loop exists to hunt.
Three counters. First, EXP2-K4: if the corpus is a "new
data-collection exercise," why did the lane not start it this wave
so a future wave can freeze? Reporting the gate state without
advancing the corpus is bookkeeping, not hunting. Second, B1-P9:
"bars do not invent mechanisms" is true but convenient; the sensory
line has been KILLED clean repeatedly, and the loop keeps the draft
QUEUED instead of asking whether the whole post-pass recolor family
is exhausted. Third, the null hunt itself: one freeze and three
queues means the candidate pipeline is stalled on gates the loop
itself defined. Gates that never fire are decorations.

JUDGE: The skeptic confuses motion with hunting. On EXP2-K4: the
lane's task was gate checks, not corpus construction; building the
corpus means running the frozen single-deliberation machinery over
a problem set and curating failure traces, which is implementation
work that would itself need a prereg freeze before it. Doing it
inside the gate-check lane would have collapsed the freeze order
the loop just tightened after the red-team audits (prereg commit
order self-check, no pre-authorized Python). The correct sequence
is: a wave freezes a corpus-collection prereg, collects the corpus,
then a later wave freezes EXP2-K4 after the corpus commit. That is
work for the parent to schedule, not a failure of this lane. On
B1-P9: the DISCARD stands and is never re-scored; asking whether
the family is exhausted is a governance-level question about the
sensory line, and the sensory stand-downs (G1 sunshafts, D-VID-1,
ST-1 dead) are unchanged this wave. The lane correctly refused to
re-freeze bars as a substitute for a mechanism. On the pipeline:
one freeze and three queues is exactly what satisfiable gates
produce; gates that fire only when satisfiable are not decorations,
they are the difference between this loop and the one that got
caught presenting old renders as new on 2026-09-23. Ruling:
coordinator verdict 3 is CONFIRMED. EXP2-K4, B1-P9, COMP2-P11 remain
QUEUED ([STACK] x3); the gate-check findings are this wave's new
factual findings ([NEW] as findings); sensory stand-downs unchanged
([RE-CERT]); no adoption or discard verdicts this wave. The honest
null stands.

## ROUND 4: commit order, the void items, interactive TNN

ADVOCATE: Commit-order self-check: vacuous for adoption (no candidate
implementation commits exist; post-freeze commits are ab577d0e6 fork
results, 97ab9ad18 candidate lane docs, 759fd30b5 red-team review,
all lane documentation, no machinery). Freeze ordering valid:
59b9df4b0 strictly precedes 5a043af3c strictly precedes 8b456736b,
by topology. On item 6: the six governance rulings, all sealed blind
pairs, and DP-1 are untouched by every lane this wave; the red team
explicitly scoped them out, the candidate lane neither decided nor
relitigated them, and the fork battery never touched them. They stay
[VOID]. On item 7: the merge survey over 80c40a7af..36342eb51 found
zero new chat/REPL/interactive entry points (the six new .zag files
are all under his continual_learning dir; the two batch fn main
drivers in battery.zag and scorer.zag are batch, not interactive)
and zero stdin-read hits in the new sources; the tnn_chat pins were
re-verified through the fork battery itself (B1 byte-identical,
B2 bin sha 75b85d3c 49/49). No runnable interactive TNN exists
beyond the frozen probe instruments.

SKEPTIC: Conceding the commit order is vacuous only because nothing
was implemented, which is the null hunt again. On the void items I
have no attack: the debate's task explicitly bars relitigating them,
and the lanes observed the bar. On interactive TNN: the survey range
ends at 36342eb51, his BUILD+RUN commit. The six new .zag files are
his, closed to the loop, so the survey's "zero new entry points"
finding is really "zero new loop entry points," which is what the
verdict says. No attack on the finding itself, but the loop should
not be surprised later that his dir contains batch drivers with fn
main: those are his, not loop adoption targets. The citation rules
in slate item 5 cover this.

JUDGE: Ruling: coordinator verdicts 4, 6, and 7 are CONFIRMED.
Commit-order self-check vacuous for adoption, freeze ordering valid
([NEW] line recording this wave's check). The six governance
rulings, all sealed blind pairs, and DP-1 remain [VOID]; this debate
did not review them and renders no opinion on their merits. The
interactive TNN finding is confirmed with the skeptic's precision
kept: zero new loop chat/REPL/interactive entry points in
80c40a7af..36342eb51, zero stdin reads in the new sources, tnn_chat
pins re-verified via the battery ([RE-CERT]).

## ROUND 5: his continual_learning flagship (slate item 5)

ADVOCATE: The slate proposes a his-frontier standing entry in
LOOP_STATE.md plus five citation/boundary rules. All five constrain
the loop and never him: (a) a descriptive citation entry (paths,
prereg 8c22ffb9b, build+run 36342eb51 with his GO, red-team report
899757bc2 with NO-GO marked not-relitigated), CLOSED to the loop;
(b) a loop-internal import ban on his directory, verified true today;
(c) future loop probes cite his MANIFEST SHAs as canonical for
continual-learning claims and do not copy his D1 psm.zag deviation
into loop PSM copies; (d) his fixtures are a closed teaching corpus,
cite-as-prior-work; (e) his Python build tools are his own
authority, the loop's pure-Zag rule does not reach into his dir and
the loop must not run his tooling. His files were not touched (git
diff clean). The directory is CLOSED to the loop.

SKEPTIC: I agree the directory is CLOSED and the five rules are
correctly loop-constraining. My attack is on the slate's framing,
not its rules. The slate says "parent decides whether to surface
the discrepancy to Micah." The red team found the load-bearing
fact: 899757bc2 is authored by micahcooley himself, 2026-09-27
11:23:07 -0700, after his own GO at 36342eb51. The GO/NO-GO
discrepancy is his own later judgment on his own work, not a loop
finding awaiting his attention. "Parent decides whether to surface"
presupposes there is something to surface that he has not seen.
There is nothing. Any mention of the discrepancy must carry the
authorship fact, full stop. The slate's framing is wrong and the
judge should correct it.

JUDGE: The skeptic is right and the correction is material. Verified
independently: git log shows 899757bc2 authored by micahcooley,
2026-09-27 11:23:07 -0700, with the message "Red team report:
continual-learning flagship benchmark -> NO-GO", after his GO at
36342eb51. Ruling: the five citation/boundary rules are CONFIRMED as
loop-constraining only ([NEW] as proposed rules); the his-frontier
standing entry is CONFIRMED as citation-only and CLOSED ([NEW]).
But the slate's "parent decides whether to surface the discrepancy"
framing is OVERTURNED. Corrected framing: there is nothing for the
parent to surface to Micah that he did not write himself; any loop
mention of the GO/NO-GO pair must carry the authorship fact (his own
report, after his own GO). The red team flagged this; this debate
adopts the correction as a verdict.

## JUDGE: final rulings with numbers

Slate item 1: CONFIRMED. Fork battery CONFIRM [RE-CERT]: 51 named
entries, 49 PASS, 2 UNTESTABLE (rh-pull-1/2, ten waves, pinned
toolchain path absent, unchanged cause), 0 FAIL, 0 CONFIRM. Evidence
commit ab577d0e6. The red-team reclassification recommendation is
NOT adopted: permanent OUT OF SCOPE would remove the only automated
check that fires if those trees change content; vendoring the
toolchain into non-loop repos would manufacture testability. The
recommendation stays recorded as dissent. The scope caveat is
mandatory on every headline.

Slate item 2: CONFIRMED. EXP1c FROZEN [NEW] at 8b456736b, upgraded
from the 0821pdt draft. Gate (a) satisfiable: six corrections plus
deliverable content-verified in 463b115b6. Ordering valid:
59b9df4b0 < 5a043af3c < 8b456736b. K1-K7 byte-identical to the draft.
Pre-run, no scores seen. No implementation exists; no adoption this
wave. Queued for future implementation under the frozen bars; the
K7 caution is a watch item, not a veto.

Slate item 3: CONFIRMED. EXP2-K4, B1-P9, COMP2-P11 remain QUEUED
([STACK] x3). Gate findings (no failure-trace corpus; no new
B1-class mechanism; ruling 6 still OPEN) are this wave's new factual
findings. Sensory stand-downs (G1, D-VID-1, ST-1 dead) unchanged
([RE-CERT]). No candidates implemented: honest null stands.

Slate item 4: CONFIRMED. Commit-order self-check vacuous for
adoption; freeze ordering valid ([NEW] line).

Slate item 5: CONFIRMED with the framing correction. His flagship
CLOSED to the loop, untouched ([RE-CERT] as closed corpus). The five
citation/boundary rules confirmed as loop-constraining ([NEW]). The
"parent decides whether to surface" framing is OVERTURNED: nothing
to surface that he did not write himself (899757bc2 authored by
micahcooley, 2026-09-27 11:23:07 -0700, after his GO at 36342eb51);
any mention carries the authorship fact.

Slate item 6: CONFIRMED. Six governance rulings, all sealed blind
pairs, DP-1: UNTOUCHED [VOID]. This debate rendered no opinion on
their merits.

Slate item 7: CONFIRMED. Interactive TNN: tnn_chat pins re-verified
via the fork battery (B1 byte-identical, B2 bin sha 75b85d3c 49/49);
merge survey over 80c40a7af..36342eb51 shows zero new loop
chat/REPL/interactive entry points and zero stdin-read hits
([RE-CERT]). No runnable interactive TNN beyond the frozen probe
instruments.

Coordinator verdicts overturned: two, both with cited evidence.
(1) The item 1 reclassification recommendation is rejected: ten
waves of identical cause (git show exit 128, pinned toolchain path
absent), cause content-dependent not permanent, per-wave extraction
attempt is the detection mechanism, vendoring manufactures
testability in repos the loop does not own. (2) The item 5 surfacing
framing is corrected: 899757bc2 author micahcooley, 2026-09-27
11:23:07 -0700, after 36342eb51.

## Judge's verdict tags for the LOOP_STATE lines

- Fork battery CONFIRM (49/51): [RE-CERT]
- EXP1c freeze package (mass 5a043af3c, prereg 8b456736b): [NEW]
- EXP1c gate (a) evidence verification (463b115b6 six corrections): [RE-CERT]
- EXP2-K4 QUEUED: [STACK]
- B1-P9 QUEUED: [STACK]
- COMP2-P11 QUEUED: [STACK]
- Gate-check findings (corpus absent, no new mechanism, ruling 6 open): [NEW]
- Sensory stand-downs (G1, D-VID-1, ST-1): [RE-CERT]
- Null candidate hunt (no implementation this wave): [NEW]
- Commit-order self-check this wave: [NEW]
- His-frontier standing entry (CLOSED): [NEW]
- Five citation/boundary rules: [NEW]
- Six governance rulings: [VOID]
- Sealed blind pairs: [VOID]
- DP-1: [VOID]
- UNTESTABLE reclassification proposal: [VOID] as a verdict change
  (recorded as dissent, not adopted)
- rh-pull-1/2 UNTESTABLE entries: [RE-CERT]
- Interactive TNN finding (tnn_chat pins, zero new entry points): [RE-CERT]

## Attestation

Zero Python in this debate's production. The transcript was authored
as text and committed with the git CLI only. No Python interpreter
was invoked; no Python was written or run. No pushes. No
modifications to docs/lab/continual_learning/. No em dashes in this
document. The six governance rulings and all sealed blind pairs were
not decided, relitigated, or re-presented.
