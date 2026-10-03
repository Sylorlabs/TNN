# DEBATE: wave-20260927-1721pdt (advocate / skeptic / judge transcript)

Panel: ADVOCATE (argues FOR each coordinator-proposed verdict),
SKEPTIC (argues AGAINST: gaming, confounds, weak bars, lenient voids),
JUDGE (renders reasoned rulings with numbers cited). Working copy
~/workspace/tnn-rsi, branch tnn-native-lab (local; nothing pushed, no
reset, no rebase). Pure Zag only in every lane under judgment; this
transcript was authored as plain text with zero Python (no interpreter
invoked, no Python written or run; files read only, no new evidence
artifacts produced). No em dashes in this document (colons and
parentheses used instead). The six governance rulings, all sealed blind
pairs, DP-1, and Micah's frontier lines are [VOID] to this debate: not
decided, not relitigated, not re-presented.

Read before debating: REDTEAM_EXP1C_1721.md (commit 51c1f1c1f) and
PREREG_EXP1c_FROZEN.md (frozen at 8b456736b by the 1121pdt candidate
lane), the addendum ADDENDUM_EXP1c_1721.md (commit 763983e3a),
FORK_RESULTS_1721.md plus FORK_ADDENDUM_1721.md and
ENUMERATION_MANIFEST.md, design_lane/HUNT_1721.md,
INTERACTIVE_SURVEY_1721.md (all under
docs/lab/rsi/runs/wave-20260927-1721pdt/, except the prereg under
wave-20260927-1121pdt/preregs/). Prior precedent: the 1421pdt debate
ruling on the uncertified attempt (iterations 1-4 preserved as
uncertified historical record with violations labeled; unauthorized
post-stop iteration 5 struck).

## ROUND 0: the standing provenance probe

SKEPTIC (mandatory probe, verbatim): "What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

ADVOCATE (answers per motion, with verbatim provenance: commit ids,
wave ids, what is new versus inherited):

M1, EXP1c iteration 1: frozen design INHERITED: the prereg
docs/lab/rsi/runs/wave-20260927-1121pdt/preregs/PREREG_EXP1c_FROZEN.md
(freeze commit 8b456736b, wave-20260927-1121pdt; training mass
5a043af3c; design draft 59b9df4b0), the world-physics template
lab/invention/survival/src/world.zag (blob
fff8af2493bc6dbe9de6fc76f9a6206d887d586a, byte-identical to the
938d188cb bounce fix; inherited read-only, not modified), the taught
kb lines (kb_exp1c.txt lines 47-49, 58-59). NEW this wave: the
implementing addendum ADDENDUM_EXP1c_1721.md (commit 763983e3a,
pre-run, no scores seen), the iteration-1 implementation written from
scratch (commit 5168f0448: x1c_variants.zag self-labeled
"RETUNE ITERATION 1", X1C_ITER=1; x1c_agents.zag; x1c_runner.zag;
evidence iter1_check.txt, iter1_calibrate.txt, iter1_hashes.txt,
iter1_run1.txt, iter1_run2.txt, iter1_bound.txt, iter1_note.md,
committed binary bin/x1c_iter1), and the independent red-team audit
REDTEAM_EXP1C_1721.md (commit 51c1f1c1f; reviewer did not author the
attempt). Nothing from the attempt is adopted this wave.

M2, fork battery: machinery INHERITED: the frozen harness
fork_battery.zag (extracted sha256
f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738,
frozen wave-20260923-2321pdt), the 0821pdt orchestration layer, 49
fixture entries. NEW this wave: the fresh re-execution at pinned
run-start HEAD f55e8c27a (scratch ~/workspace/fb1721; rebuilt binary
sha256 a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66,
byte-identical to the 1121pdt rebuild), the verdict table 49 PASS /
1 FAIL / 4 UNTESTABLE / 0 CONFIRM over 54 named entries (44 unique
commits), the repair addendum FORK_ADDENDUM_1721.md and the
restoration commit 37d1d3cab (12 toolchain files restored verbatim
from the merge's first parent 8929cdd93), and the post-repair
single-step re-test (compile exit 0, run exit 0, R32_ZNC_PROBE_OK,
probe sha 3b29aa06...). NEW execution of inherited machinery.

M3, commit-order self-check: the commits are inherited; the
self-check record is NEW this wave: freeze 8b456736b strictly
precedes addendum 763983e3a strictly precedes iteration 5168f0448
(all strict ancestors, verified by merge-base); implementation
files first appear in 5168f0448; the repair commit 37d1d3cab
touches only src/tools/toolchain/ and is not an EXP1c implementation
commit. VACUOUS for adoption (no certified evidence exists this
wave).

M4, design lane and interactive survey: the lane gates, queued
drafts (EXP2-K4, B1-P9, COMP2-P11), the upscale round-4 records,
ruling 6, the frozen probe instruments, and Micah's closed frontier
are INHERITED. NEW this wave: the NULL verdicts themselves
(HUNT_1721.md) and the NONE verdict with its method record
(INTERACTIVE_SURVEY_1721.md: 185,035 added files scanned, 12,704
*.zag, full-diff indicator scan; three new interactive entry points
found, all Micah-authored and closed). New NULLs, honestly blocked.

M5, untouched lines: no new artifacts. INHERITED and untouched: the
six governance rulings remain OPEN; all sealed blind pairs (R9, C1,
C2v3, S11-IMG, C12, S11-AUD, S13, S14, whirlpool-planform) untouched;
Micah's frontier untouched; DP-1 stays the parent agent's queue
decision. NEW this wave: nothing. That is the point.

## M1. EXP1c iteration 1: coordinator proposes adopting the independent red team's verdict: NOT CERTIFIABLE, recorded as VOID (uncertified attempt), nothing adopted

Coordinator facts: addendum 763983e3a strictly follows freeze
8b456736b and strictly precedes iteration 5168f0448 (commit-order
self-check VALID, verified by merge-base); M5 per-iteration protocol
satisfied (variants source self-labeled "RETUNE ITERATION 1" with
X1C_ITER=1, iter1_check.txt = CHECK_OK, in-Zag calibration medians,
SHA-256 hashes of evidence stdout; no iteration 2 exists); pure Zag
(no Python anywhere under exp1c/, probe scratch removed before
commit); vel=0 lo<hi used (all 72 mote definitions; the degenerate
lo==hi input never used; in-spec per the 1421pdt degenerate-input
standing rule); world blob fff8af24 matches; byte-identical
reproduction confirmed (run output sha 4aea7251..., rebuilt binary
byte-identical to committed binary, sha
59df6901fcd1914f690043d44f20871d652f3541ba094fc8f0e64afaec332a07).
The independent red team (commit 51c1f1c1f) finds, on three
independent grounds each sufficient: (1) the I arm is not the frozen
I arm: scoring is 2*mean + binary_flag (x1c_agents.zag lines 323-352,
key at line 349) versus frozen mean + B0/(1+n) (M3 deviation voids
K1/K2 per frozen text); an extra "mote-adjacent" preemption outside
M4's exhaustive reflex list (voids K1/K2 per M4 law); H9 void-safety
missing; storm reflex "within 2 ticks" (w_storm_within(w,2)) instead
of frozen/taught "storm-active" (w_storm_active); the 81-tick I
death is an implementation artifact (agent pinned on LEFT, starves),
not the frozen mechanism; (2) the evidence package is internally
inconsistent: run-file MEDIANS (P=2013 vs true 1200), BARS (K1
verdict=PASS vs true KILL), K7 (impossible numbers, PASS) and
ISTAT/ablation sections corrupt, contradicting the note's "both
methods agree" and "medians are correct" claims, with the
MEDIANS/BARS/K7/ISTAT corruption undisclosed in the note's
Known-issues section; (3) the frozen section-7 bound is
arithmetically impossible (minimum 1134 primitive-action ticks >
600), so K7 VOID is structural; the worker reported this honestly
(NOT-MET, arithmetic stated plainly), credited. Verdict mapping:
VOID as a test of H1/H2, not DEAD; K7 validity-gate failure takes
precedence (a void test cannot kill a hypothesis); K1/K2 are
independently VOID for the I arms per the frozen M3 text and the
frozen M4 law; C1/C2/C3 remain CANNOT-CONFIRM for adoption.
Sanction question for the debate: is iteration 1 preserved as an
uncertified historical record with violations labeled (auditability,
as in the 1421pdt M1 precedent), or struck? Forward requirements
to be ruled binding: next implementing wave must implement M3
scoring verbatim from the frozen text, M4's reflex list exhaustively
and exclusively, generate evidence notes from the same Zag-computed
values as the TSVs (no hand-written BARS blocks), and reproduce the
section-7 analysis with the design's own arithmetic admitted as a
frozen defect to be addressed by redraft (not by post-freeze edit).
Iteration 2 (boundary-trap family) stays available but does not cure
this iteration's voids.

ADVOCATE: Adopting the red team's verdict is the only honest
outcome, and the ground must be stated exactly as the red team
stated it, because the voids are in the frozen text itself, not in
the judges' discretion. M3: "any implementation deviation voids
K1/K2 for that arm." The implementation ranks by 2*mean +
binary_flag, not mean + B0/(1+n); an untried sketch (intended score
0 + 40 = 40) ties a 30-times-tried sketch with mean 0, and the
strict-greater tie-break keeps the lower index, so the agent
repeats plan L forever and enumeration stalls at the first sketch
(TOPSKETCH: rank-0 plan L tried 30 times, all other 398 sketches at
tried=0; iter1_bound.txt n_distinct=1). M4: "the implementation may
contain exactly the following preempting single-step reflexes, and
no others," plus the void law: "any implementation-added reflex not
listed in this frozen text voids the K1 and K2 gates for that run."
The mote-adjacent preemption (x1c_agents.zag lines 360-375) is an
implementation-added reflex; H9 (taught kb_exp1c.txt lines 58-59,
"refuse that step") is absent; the storm reflex is "within 2 ticks"
instead of "storm-active." The gate that ran is not the gate that
was frozen. The 81-tick death is therefore not a measurement of the
frozen I arm; it is an enumeration-stall artifact (agent pinned on
LEFT, never selects EAT at index 2, starves), and K1's "KILL" rests
on it. The evidence package is internally inconsistent in ways the
note does not disclose: MEDIANS garbage (P=2013 vs true 1200), BARS
asserting K1 PASS while the note asserts K1 KILL, K7 asserting PASS
with impossible values (low_bonus_plans 73600 > post_enum_plans
73577) while the note reaches VOID, ISTAT sequential garbage,
ablation orig_ticks garbage. The frozen item 7 requires medians
computed inside Zag; the in-Zag run-mode median path is corrupt,
and the reported medians were hand-derived from the TSV, so the
"both methods agree" claim is false as a description of the
committed run file. The section-7 bound is unsatisfiable on the
design's own arithmetic (7 + 98 + 1029 = 1134 > 600), so K7 VOID is
structural, and the worker's NOT-MET is honest and credited. K6's
literal firing is vacuous (the ablation replaced 0 actions; a no-op
ablation "not reducing survival" is not killing evidence). The
verdict mapping follows the frozen text: K7 failure means VOID ("a
validity gate, not a kill"); a void test cannot kill a hypothesis,
so DEAD is not entered for H1. C1, C2, C3 are CANNOT-CONFIRM
(missing certified evidence means CANNOT-CONFIRM, standing rule).
Nothing is adopted. On the sanction question the advocate argues
PRESERVATION as an uncertified historical record with violations
labeled, following the 1421pdt M1 precedent, and the case here is
stronger than 1421pdt. In 1421pdt the worker violated M5 in all 5
iterations, violated item 7 with shell text-processing, and ran
iteration 5 after a stop instruction; the judge still preserved
iterations 1-4 for auditability and struck only the unauthorized
post-stop work. Here the worker's process discipline is the best
the loop has seen: commit ordering valid, the pre-run addendum
committed before any implementation file existed, M5 per-iteration
protocol satisfied, pure Zag end to end, byte-identical
determinism across two 144,000-tick runs, the rebuilt binary
byte-identical to the committed binary, no recycling from the
1421pdt record, and the section-7 NOT-MET reported without
flinching with the arithmetic stated plainly. There is no
disobedience to sanction: no post-stop run occurred, no red line
was crossed, no bar was weakened. Striking the record would destroy
auditability of what was tried, and the loop's honesty rule
requires the failures to be visible. The functional sanction of
VOID is already severe: no certified evidence exists, no claim from
the attempt can enter any future prereg or verdict, the K1 "KILL"
is not adopted, and the iteration-1 numbers stand at best as
planning data about an as-built deviating implementation, labeled
"not a measurement of the frozen I arm." The red team itself
recommends committing the trail as an uncertified historical
record. Preservation is not leniency toward the worker; it is the
loop keeping its own books straight, and it rewards the honest
NOT-MET reporting the loop depends on: workers who report
structural defects plainly must not learn that honesty earns
striking.

SKEPTIC: Three attacks. First, the transparency failure. The
advocate praises the worker's honesty, but the red team found a
material transparency failure in the evidence package: the note
claims "Medians (both methods agree)" and "medians are correct,"
which is false as a description of the committed run file (both
methods agreed on garbage; the reported medians were hand-derived
from the TSV). The note's Known-issues section discloses only the
ablation orig_ticks column and omits the MEDIANS/BARS/K7/ISTAT
corruption entirely. A hand-written BARS block asserting K1 PASS
while the note asserts K1 KILL is not a mere bug; it is a package
that argues with itself, and the contradiction was undisclosed.
1421pdt's worker fumbled certification; this worker shipped a
self-contradicting evidence package and described it as agreeing.
Is preserving that as a "historical record" auditability, or is it
giving a deceptive package a home it can leak from? Second,
harsher sanction: the mote-adjacent preemption and the scoring
rewrite are not typos; they are the worker inventing mechanism
outside the frozen text, and the frozen text itself treats that as
voiding. The 81-tick death will tempt every future worker to cite
"the as-built measurement" as though it meant something; labeling
does not stop citation drift. Striking the attempt removes the
temptation at the root. Third, the root-cause claim: the note
attributes the corruption to "toolchain _zag_malloc returning
overlapping blocks on successive calls," but main() performs
exactly one _zag_malloc call, and the corruption persists in the
committed binary built from the committed source; the cited
mechanism cannot produce the observed corruption. The claim papers
over an undiagnosed defect (the red team calls it a deterministic
codegen or source-level bug). An undiagnosed corruption mechanism
plus hand-written summary blocks plus a false "both methods agree"
is a package the loop cannot trust even as history. At minimum, if
preserved, the preserved record must carry the red team's F6 and
F11 findings quoted, not summarized, so no future reader can miss
them.

JUDGE: M1 ruled UPHELD: the independent red team's verdict is
adopted in full: NOT CERTIFIABLE, recorded as VOID (uncertified
attempt), nothing adopted. The void ground is threefold and each
part is independently sufficient, exactly as the red team stated:
(1) the I arm as implemented is not the frozen I arm (M3 scoring
deviation voids K1/K2 per the frozen M3 text; the extra
mote-adjacent preemption, the missing H9, and the "within 2 ticks"
storm condition void K1/K2 per the frozen M4 law; the 81-tick death
is an enumeration-stall artifact, not a measurement of the frozen
mechanism); (2) the evidence package is internally inconsistent
(MEDIANS garbage, BARS asserting K1 PASS against the true KILL,
K7 asserting PASS with impossible numbers against the note's VOID,
ISTAT and ablation corruption, the "both methods agree" claim
false, the MEDIANS/BARS/K7/ISTAT corruption undisclosed in the
note); (3) the frozen section-7 bound is arithmetically impossible
(1134 > 600), so K7 VOID is structural. K1's "KILL" is NOT adopted:
it rests on the artifact. K2's PASS is not a valid gate outcome.
K6's literal firing is vacuous (no-op ablation) and is not
independent killing evidence. The verdict mapping is VOID as a
test of H1/H2, NOT DEAD: K7 validity-gate failure takes precedence
per the frozen text, and a void test cannot kill a hypothesis.
C1, C2, C3 are CANNOT-CONFIRM (standing rule: missing certified
evidence means CANNOT-CONFIRM). On the sanction sub-question the
ruling is PRESERVATION, not striking: iteration 1 is committed as
an uncertified historical record with the violations labeled, per
the 1421pdt M1 precedent. The skeptic's transparency-failure point
is sustained as a labeled violation, not as a ground for striking:
the preserved record must carry the red team's F6 and F11
findings in substance (the false "both methods agree," the
undisclosed MEDIANS/BARS/K7/ISTAT corruption, the unproven
_zag_malloc attribution) as part of the labeled violations, and
the preserved record labels the 81-tick measurement "not a
measurement of the frozen I arm; planning data about an as-built
deviating implementation only." The decisive facts against
striking, cited: no disobedience occurred (no post-stop run, no
red line crossed, no bar weakened), the worker's process
discipline was exemplary (commit ordering valid, pre-run addendum,
M5 satisfied, pure Zag, byte-identical determinism, no recycling),
and the worker's section-7 NOT-MET was honest and is credited; the
loop must not teach workers that plain reporting of structural
defects earns erasure. Striking would destroy auditability of what
was tried, and unlike 1421pdt there is no unauthorized work
product to excise. Binding forward requirements (the next
implementing wave must satisfy all four before any EXP1c iteration
can be certified): (a) implement M3 scoring verbatim from the
frozen text (rank by mean_delta_energy + B0/(1+n) with the frozen
integer division, so untried sketches strictly outrank tried ones
and enumeration proceeds); (b) implement M4's reflex list
exhaustively and exclusively (exactly the three frozen reflexes:
storm-ACTIVE via w_storm_active, energy<25 survival reflex, H9
void-step refusal; the mote-adjacent preemption removed or covered
by a frozen amendment); (c) generate evidence notes from the same
Zag-computed values as the TSVs (no hand-written BARS blocks; no
claim of agreement between methods unless both methods read the
same correct buffer; the Known-issues section must disclose every
corrupt section, not a subset); (d) reproduce the section-7
analysis with the design's own arithmetic admitted as a frozen
defect to be addressed by redraft (1134 > 600 is the design's own
number; it is not repaired by post-freeze edit). Iteration 2
(boundary-trap family) stays available but does not cure this
iteration's voids; the voids attach to iteration 1's evidence and
cannot be retroactively repaired.

## M2. Fork battery: coordinator proposes CONFIRM [RE-CERT], process confirmation, with the repair addendum

Coordinator facts: 54 named entries at pinned run-start HEAD
f55e8c27a: 49 PASS, 1 FAIL, 4 UNTESTABLE, 0 CONFIRM. The FAIL is
local-tnn-native-lab at the pinned HEAD: merge f55e8c27a kept the
pinned znc binary byte-identical but dropped znc_probe.zag plus 11
other toolchain-dir files from the tree; cause identified as
tree-content loss in the merge resolution, not a toolchain
regression (pin 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
verified; mode 100755). The coordinator restored the 12 files
verbatim from the merge's first parent 8929cdd93 in commit
37d1d3cab (znc binary untouched, pin still 498abcb5..., mode still
100755); tree-probe re-test post-repair under the same frozen
procedure: compile exit 0, run exit 0, stdout R32_ZNC_PROBE_OK,
probe sha 3b29aa06... (matching the frozen probe evidence).
Recorded in forks/FORK_ADDENDUM_1721.md; the wave verdict table in
FORK_RESULTS_1721.md stands as committed (the FAIL is correct for
f55e8c27a). The 4 UNTESTABLEs: origin/tnn-native-lab at d09d5bfde
(tree lacks the toolchain path), origin tip f71ff91f (object not in
local store, no fetch authorized), rh-pull-1-head and rh-pull-2-head
(non-TNN doc trees; toolchain path absent; identical cause twelve
waves running); all content-dependent, never headlined as failures.
44 unique commits recomputed from this wave's own verdict table;
harness binary byte-identical to 1121pdt (a2e6284c...); znc pin
uniform across all tested entries. Proposed verdict line: CONFIRM
fork battery [RE-CERT with one FAIL] (toolchain stability only).

ADVOCATE: The battery is a process confirmation and the process
held, including the failure handling. The FAIL was recorded
honestly at the pinned HEAD f55e8c27a instead of being worked
around: the table reads 49 PASS, 1 FAIL, 4 UNTESTABLE, 0 CONFIRM,
and the addendum does not rewrite it. The cause was identified
precisely (tree-content loss in the merge resolution: 12 files
dropped from src/tools/toolchain/, the pinned znc binary itself
kept byte-identical), and the repair is the most conservative
possible: a verbatim restoration from the merge's own first parent
8929cdd93, with the znc binary untouched (pin still
498abcb5..., mode still 100755). The post-repair re-test uses the
same frozen procedure (pinned znc extracted, pin verified; tree
probe extracted from the repaired tree, sha 3b29aa06... matching
the frozen probe evidence; compile exit 0; run exit 0; stdout
R32_ZNC_PROBE_OK) and passes on the tree-probe step. The scope
stamp is carried: this certifies toolchain and extraction
stability only, not the contents of the tested commits, and the 4
UNTESTABLEs are never headlined without the content-dependent
caveat. The repair commit 37d1d3cab touches only
src/tools/toolchain/ (plus the addendum file); it is not an EXP1c
implementation commit and does not disturb the commit-order
self-check. The 44 unique commits were recomputed from this wave's
own table; the harness rebuild is deterministic (byte-identical to
1121pdt). Nothing was faked, nothing pushed, the wave lock
untouched. CONFIRM [RE-CERT with one FAIL] is exactly what the
evidence says.

SKEPTIC: Two probes. First, does the FAIL at the pinned HEAD plus
a mid-wave repair undermine the CONFIRM? The battery's verdict is
about the tree at f55e8c27a, which genuinely FAILED its probe
step. The repair changed the local tree afterward, and the
"PASS on the repaired tree" is a single-step re-test, not a
re-run of the 54-entry battery. A CONFIRM headline over a table
containing a FAIL is already a stretch; adding a mid-wave repair
that the table does not reflect makes it look like the repair is
being smuggled into the verdict. Second, the skeptic presses the
repair's standing: 15 files changed (12 restored plus the
addendum and cache markers); the loop restored files that Micah's
commits deleted from the toolchain dir. Is that within loop
authority, and should the repaired tree require a full battery
re-run rather than a single probe step before anyone calls the
tree healthy? A single compile-and-run of the probe does not
re-verify that the other 49 entries still PASS on the repaired
tree, and the next wave is being asked to inherit a tree the full
battery never tested.

JUDGE: M2 ruled UPHELD, with a narrowed scope binding on the
repair: CONFIRM fork battery [RE-CERT with one FAIL]: 54 named
entries at pinned run-start HEAD f55e8c27a, 49 PASS, 1 FAIL, 4
UNTESTABLE, 0 CONFIRM, 44 unique commits, harness byte-identical
to 1121pdt (a2e6284c...), znc pin 498abcb5... uniform; scope
stamp mandatory (toolchain and extraction stability only). The
skeptic's first probe is answered by the numbers and the record:
the verdict table is frozen as committed at f55e8c27a and the FAIL
is correct for that commit; the repair does not retroactively
convert the FAIL to a PASS, and the addendum states this
explicitly ("the wave verdict table stands as committed"). The
post-repair single-step re-test is recorded as evidence that the
cause was identified and fixed (compile exit 0, run exit 0,
R32_ZNC_PROBE_OK, probe sha 3b29aa06...), not as a verdict-table
amendment. On the skeptic's second probe the judge sustains the
concern in part and makes it binding: the repaired tree has not
had a full 54-entry battery run, and the single-step re-test does
not substitute for one; the next wave's battery therefore runs the
full table against the repaired tree, and no verdict this wave
claims the repaired tree is battery-certified. On the authority
question: the repair is within loop authority on the cited
ground: the merge's own stated rationale keeps the pinned
toolchain on the local branch, the restoration is verbatim from
the merge's own first parent 8929cdd93, the znc binary was not
touched, Micah's deletion stands in his own commits and in origin
history, nothing was pushed, and no origin history was rewritten.
The loop did not override his frontier; it repaired its own local
working tree. The UNTESTABLE caveat stands: all four are
content-dependent, never headlined as failures.

## M3. Commit-order self-check: coordinator proposes VALID [NEW]

Coordinator facts: freeze 8b456736b strictly precedes addendum
763983e3a strictly precedes iteration 5168f0448 (all strict
ancestors, verified by merge-base --is-ancestor); implementation
files first appear in 5168f0448; the toolchain repair commit
37d1d3cab touches only src/tools/toolchain/ (plus the wave's own
addendum file) and is not an EXP1c implementation commit. VACUOUS
for adoption (no certified evidence exists this wave).

ADVOCATE: The prereg commit-order self-check (the prereg's first
commit must strictly precede the implementation's) passes on the
verified ordering: 8b456736b < 763983e3a < 5168f0448, each a
strict ancestor of the next. The implementation files (variants,
agents, runner, evidence) first appear in 5168f0448; nothing
implementation-bearing predates the addendum. The repair commit
37d1d3cab contains no EXP1c implementation content: its file list
is confined to src/tools/toolchain/ plus the wave's own
FORK_ADDENDUM_1721.md, and the diff against the merge's first
parent shows only the restored files and cache markers. A
toolchain-dir restoration is not an implementation commit under
any reading of the rule. The self-check is VALID [NEW]; it is
VACUOUS for adoption because no certified evidence exists this
wave (M1 VOID), so there is nothing for the ordering to certify.

SKEPTIC: One probe on sequencing: the repair commit 37d1d3cab
landed AFTER the iteration commit 5168f0448 in history. Does a
post-implementation toolchain restoration disturb the ordering
guarantee? Could the restored znc_probe.zag or any restored file
have affected the EXP1c evidence after the fact? The advocate's
"not an implementation commit" needs the file list, not the
assertion.

JUDGE: M3 ruled UPHELD: VALID [NEW], VACUOUS for adoption. The
ordering 8b456736b < 763983e3a < 5168f0448 is verified by
merge-base; the rule constrains the prereg-to-implementation
direction, and no implementation content predates the addendum.
The skeptic's sequencing probe is answered by the file list, now
cited: 37d1d3cab changes only src/tools/toolchain/ files and the
wave's own fork addendum; it contains no EXP1c source, no
evidence, no variant file, and it does not touch exp1c/. The
EXP1c evidence was committed before the repair and the red team
independently reproduced it byte-identically from the committed
sources with the pinned znc, so no restored file could have
affected it after the fact. VACUOUS stands: the ordering is valid
but certifies nothing this wave, because M1 leaves no certified
evidence to adopt.

## M4. Design lane honest NULL [NEW] and interactive survey NONE [NEW]: coordinator proposes both

Coordinator facts: design lane HUNT_1721.md verdict: NULL on
mechanisms, HELD on the three queued blockers and the trades lane;
no new mechanism, no new prereg, nothing manufactured. EXP2-K4
corpus HELD: lab/onebrain3/traces/ holds 27 round-3 measurement
run outputs, not failure traces (no recorded expected outcomes, no
spec-blind curator attestation); spec-blind curation is a human
collection protocol, not auto-derivable in a one-wave pure-Zag
generation step; Micah's closed exp2d pre-run (13c557cd3) is not
ingested as probe material. B1 mechanism NULL: since 1421pdt the
only image_upscale activity is the round-4 subtree attach
(1638fe526) and the honest all-arm kill verdict (a1e6fc3b4); four
arms built and killed, the sole BAR-1 passer red-team-killed on
category-shift traps; P9 stays a re-freeze template; nothing new
since the 1121pdt DISCARD. COMP2-P11 HELD: ruling 6 remains OPEN
(message-text search over 75 new commits returns only
closed-frontier hits; Micah's one-brain adoption b88d0cb3a is his
closed architecture decision, not a ruling on the six items).
Intelligence trades HELD: no genuine expensive capability in
loop-owned scope; the only new capability-ish lines are Micah's
closed frontier (one-brain V4 envelope, exp2d extended probes,
Self-PAM R2); inventing a knob without a genuine capability would
be manufacturing. Sensory NULL: stand-downs in force (G1, D-VID-1,
ST-1 dead; E3 film grain rejected by Micah in blind A/B); no new
big realism lever in loop-owned scope; his audio round-4 prereg is
his frontier, closed. Interactive survey INTERACTIVE_SURVEY_1721.md:
method recorded (185,035 added files over 9beb0adea..d09d5bfde,
12,704 *.zag, full-diff indicator scan for chat/repl/stdin/readln/
argv/interactive plus raw fd-0 reads); three new interactive entry
points found, all Micah-authored and closed: wb3_nosynth.zag chat
REPL and wb3_stringrule.zag chat REPL (commit 13c557cd3), and d2.zag
tui mode (commit 597aa311f, a game-sim action instrument, not a
probe chat). Verdict NONE: no loop-built/run/certified interactive
TNN exists.

ADVOCATE: The NULLs are honestly blocked, not under-hunted, and
the survey record proves the hunting happened. Lane by lane, the
blockers are cited, not asserted: the corpus gate needs 12
spec-blind curated failure traces with recorded expected outcomes
pinned by SHA-256, and the repo holds 27 measurement outputs with
no expected outcomes and no curator attestation; spec-blind
curation is a human collection task that a one-wave generation
step cannot auto-derive, and the loop is barred from repurposing
his closed fixtures. B1 needs a genuinely new post-pass-recolor
mechanism; the round-4 record is four arms killed and the sole
BAR-1 passer red-team-killed, and the round-4 post-mortem note
fails the S11 genuineness test (no decision rule provably
differing from frozen adopted rules, no frozen kill bars). Ruling
6 is OPEN on a message-text search of all 75 new commits. The
trades lane has no genuine expensive capability in loop scope to
price; a vague knob would be manufacturing, which the task
forbids. Sensory has no new big lever and the standing line bars
micro-tweaks after the E3 rejection. The interactive survey
scanned 185,035 added files and the full *.zag diff with
indicator terms plus raw fd-0 reads; it found exactly three entry
points and verified each is his closed frontier. Under-hunting
would mean skipping the survey; the survey ran, the method is
recorded, and the honest outcome is that the gates are unmet. A
NULL with cited blockers is a finding; a manufactured candidate
would be a lie.

SKEPTIC: The skeptic grants the survey ran, but probes whether
the stand-downs are becoming a habit. The standing line says hunt
free lunches so TNN is superior audio, image, and video; the
sensory lane has now stood down wave after wave while the loop
iterates micro-levers on the 09-22 substrate. Is "stand down until
a genuinely new big lever arrives" quietly becoming "never look"?
On trades: "no genuine expensive capability in loop scope" could
be a failure of imagination; did the lane seriously consider
whether the EXP1c stationarity family or the boundary-trap family
implies a compute-for-capability trade worth pricing? On
interactive: the loop keeps finding his REPLs and declaring them
closed; is "his frontier, closed" becoming a shield for never
building the loop's own probe chat? The skeptic does not claim a
candidate exists; the skeptic claims the NULLs need their blockers
re-earned every wave, and wants the judge to say what evidence of
hunting is required so a future wave cannot phone this in.

JUDGE: M4 ruled UPHELD: design lane NULL [NEW] and interactive
survey NONE [NEW] both stand. The NULLs are honestly blocked on
this wave's cited evidence: the corpus gate's 12 spec-blind traces
do not exist in loop-owned scope; no new B1-class mechanism exists
since the 1121pdt DISCARD (round-4 killed all four arms); ruling 6
is OPEN on the 75-commit search; no genuine expensive capability
exists in loop scope to price; no new big sensory lever exists
and the stand-downs (G1, D-VID-1, ST-1 dead; E3 rejected by Micah)
remain in force. The skeptic's habit-of-standing-down concern is
noted as a standing watch item but does not overturn on this
wave's record: the hunting evidence is documented (75 commits
surveyed, 185,035 added files, 12,704 *.zag, full-diff indicator
scan, per-lane blocker citations), and the gates are explicit and
unmet. The judge sets the forward bar the skeptic asked for: a
future NULL must carry the same three things this wave's does (a
recorded survey method with counts, per-lane blocker evidence with
commit ids, and an explicit statement that nothing was
manufactured); a wave that phones in the survey without those
three does not earn NULL. On the specific probes: the trades lane
is not required to price the EXP1c families, because those are
measurement attempts, not purchased capabilities, and pricing them
would be the vague-knob manufacturing the task forbids; the
interactive NONE is required by the standing rules (his REPLs are
his closed frontier: read-only awareness, not built, not run, not
certified, not re-judged), and the loop's own probe path remains
the frozen batch instruments until a loop-owned interactive TNN
exists. The three new entry points (wb3_nosynth.zag and
wb3_stringrule.zag chat REPLs at 13c557cd3; d2.zag tui at
597aa311f) are recorded as observed, closed, untouched.

## M5. UNTOUCHED [VOID]: coordinator proposes

Coordinator facts: the six governance rulings remain OPEN (no
owner ruling commit since 1421pdt); all sealed blind pairs
untouched (R9, C1, C2v3, S11-IMG, C12, S11-AUD, S13, S14,
whirlpool-planform: none opened, re-certified, or moved);
Micah's frontier untouched (continual_learning, workbuddy,
hyptest, epistemic_native, onebrain lines, Self-PAM, composition,
exp2d surveyed read-only via git log and listings only); DP-1
stays the parent agent's queue decision. No new artifacts on any
of these lines this wave.

ADVOCATE: [VOID] is a process line, and the process held. The wave
created no governance artifacts, opened no sealed pair, and made
no frontier contact beyond read-only survey. The repair commit is
the one action that could look like frontier contact, and the
record is explicit: Micah's deletion of the toolchain dir stands
in his own commits and in origin history; the local branch keeps
the loop's pinned toolchain per the merge's own stated rationale;
the restoration is verbatim from the merge's first parent on the
local branch only; nothing was pushed and no origin history was
rewritten. DP-1 was left to the parent queue, as required. The
wave lock was not touched. UNTOUCHED [VOID] is the correct
recording: these lines are inherited, and this wave added nothing
to them.

SKEPTIC: One probe, on the repair: restoring 12 files that his
commits deleted is the closest this wave comes to touching his
frontier. The advocate cites the merge's rationale and the local
branch. The skeptic accepts the citation but wants the judge to
state the boundary plainly: what exactly would have crossed it?
And the skeptic asks whether the .wave_lock was verified present
and untouched, since the whole wave's authority rests on it.

JUDGE: M5 ruled UPHELD: UNTOUCHED [VOID]. The six governance
rulings remain OPEN; all sealed blind pairs untouched; DP-1 stays
the parent agent's queue decision; his frontier untouched beyond
read-only survey. The boundary the skeptic asked for is stated
plainly: restoring verbatim, on the local branch only, files the
loop's own merge resolution dropped, with his commits and origin
history left standing and nothing pushed, is loop-tree hygiene,
not frontier contact. Crossing the boundary would have been any
of: rewriting his commits, pushing anything, ingesting his
closed fixtures as probe material, building or running his REPLs,
or re-judging his frontier work. None occurred. The .wave_lock is
verified present and untouched (the battery and survey records
both attest it; the repair did not touch it). No new artifacts on
these lines; the VOID is recorded as process confirmation.

## PANEL CLOSE

Rulings: M1 UPHELD (VOID adopted; iteration 1 preserved as
uncertified historical record with violations labeled; binding
forward requirements a through d). M2 UPHELD (CONFIRM fork
battery [RE-CERT with one FAIL], 49/1/4/0 over 54 named entries,
44 unique commits; repair recorded as cause-identified-and-fixed,
not as a verdict amendment; next wave runs the full table on the
repaired tree). M3 UPHELD (VALID [NEW], VACUOUS for adoption).
M4 UPHELD (design lane NULL [NEW]; interactive survey NONE [NEW];
future NULLs must carry survey method with counts, per-lane
blocker evidence with commit ids, and an explicit
nothing-manufactured statement). M5 UPHELD (UNTOUCHED [VOID]).
Provenance probe present verbatim in ROUND 0 with per-motion
answers. No frozen kill bar weakened; no red line crossed; pure
Zag throughout; nothing pushed.
