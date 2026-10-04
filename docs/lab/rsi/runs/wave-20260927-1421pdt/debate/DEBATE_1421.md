# DEBATE: wave-20260927-1421pdt (advocate / skeptic / judge transcript)

Panel: ADVOCATE (argues FOR each coordinator-proposed verdict),
SKEPTIC (argues AGAINST: gaming, confounds, weak bars, lenient voids),
JUDGE (renders reasoned rulings with numbers cited). Working copy
~/workspace/tnn-rsi, branch tnn-native-lab (local; nothing pushed, no
reset, no rebase). Panel convened at local HEAD b876016e6
("Merge remote-tracking branch 'origin/tnn-native-lab' into
tnn-native-lab"). Pure Zag only in every lane under judgment; this
transcript was authored as plain text with zero Python (no interpreter
invoked, no Python written or run; files read with cat/grep/head only,
no new evidence artifacts produced). No em dashes in this document
(colons and parentheses used instead). The six governance rulings, all
sealed blind pairs, DP-1, and Micah's frontier lines are [VOID] to this
debate: not decided, not relitigated, not re-presented.

Read before debating: REDTEAM_EXP1C_1421.md and PREREG_EXP1c_FROZEN.md
(the latter frozen at 8b456736b by the 1121pdt candidate lane),
FORK_RESULTS_1421.md plus ENUMERATION_MANIFEST.md, design_lane/
HUNT_1421.md, INTERACTIVE_SURVEY_1421.md (all under
docs/lab/rsi/runs/wave-20260927-1421pdt/, except the prereg under
wave-20260927-1121pdt/preregs/).

## ROUND 0: the standing provenance probe

SKEPTIC (mandatory probe, verbatim): "What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

ADVOCATE (answers per motion, with verbatim provenance: commit ids,
wave ids, what is new versus inherited):

M1, EXP1c implementation attempt: frozen prereg
docs/lab/rsi/runs/wave-20260927-1121pdt/preregs/PREREG_EXP1c_FROZEN.md,
freeze commit 8b456736b (wave-20260927-1121pdt candidate lane),
training mass commit 5a043af3c, design draft 59b9df4b0
(wave-20260927-0821pdt lane 3); frozen world-physics template
docs/lab/invention/survival/src/world.zag bounce-fixed by 938d188cb
(committed at HEAD, 425 lines, working copy byte-identical, no diff).
INHERITED: the prereg (M1-M5 mechanism, K1-K7 bars, C1-C3 gates), the
template, the mass. NEW this wave: the worker's 5-iteration retune
attempt (uncommitted artifacts in docs/lab/rsi/runs/
wave-20260927-1421pdt/exp1c/: variants_iter1..5.txt,
calibrate_iter1..5.txt, check_r2.txt, check_r3.txt, uncommitted
sources exp1c_agent_i.zag, exp1c_runner.zag, exp1c_variants.zag,
exp1c_variants_r2..r5.zag in docs/lab/invention/survival/src/) and
the independent red-team audit REDTEAM_EXP1C_1421.md (this wave,
uncommitted at debate time; the coordinator commits). The attempt
produces no certified calibration evidence; nothing from it is adopted
this wave.

M2, fork battery: harness design frozen wave-20260923-2321pdt
(frozen fork_battery.zag extracted sha256
f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738)
with the 0821pdt orchestration layer; rebuilt pure-Zag binary this
wave sha256 a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66
(byte-identical to the 1121pdt rebuild; harness build deterministic).
INHERITED: the frozen harness, the driver, 49 fixture entries.
NEW this wave: the fresh re-execution (scratch ~/workspace/fb1421),
one newly enumerated archive branch arch-wave-20260927-1121pdt at
4805f5363a0dba762abf2d35e8ab8284abce6731, the moved local entry
local-tnn-native-lab (a98ccd6a2 to b876016e6), the moved live origin
entry origin-tnn-native-lab-rt (899757bc2 to 9beb0ade).
Totals: 52 named entries, 50 PASS, 2 UNTESTABLE (rh-pull-1-head
5802fec8401f28b4036b0dd5ebb23905610cab57, rh-pull-2-head
4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba; pinned toolchain path
absent in tree, content-dependent, identical cause eleven waves
running), 0 FAIL. Evidence commit: this wave's wave record
(uncommitted at debate time; the coordinator commits).

M3, design lane: HUNT_1421.md (this wave, uncommitted; coordinator
commits). INHERITED: the three queued drafts from 59b9df4b0
(EXP2-K4, B1-P9, COMP2-P11); the upscale round-4 records a1e6fc3b4
(honest all-arm kill on fresh sealed battery) and 1638fe526
(subtree attach); the S11 genuineness rule. NEW this wave: the NULL
finding itself and the three blocker re-verifications (corpus still
absent, B1 class still blocked, ruling 6 still OPEN). No new
mechanism, no new prereg.

M4, interactive survey: INTERACTIVE_SURVEY_1421.md (this wave,
uncommitted; coordinator commits). INHERITED: the frozen probe
instruments docs/lab/rsi/fit_authority/tnn_chat.zag and
tnn_chat_decline.zag (untouched this wave), the FIT pins (fresh
re-run due within 8 waves; stale count 1 of 8 entering this wave).
NEW this wave: the finding that no runnable interactive TNN exists
beyond the frozen probes, and the observed (not adopted, not run,
not certified) interactive entry point in Micah's own commit
3cd24f11d (workbuddy round 2, argv[1]=="chat" mode; his frontier
line, CLOSED to the loop).

M5, prereg commit-order self-check: no implementation commits exist
this wave (the EXP1c worker committed nothing; git log since the
8b456736b freeze carries no implementation commit; nothing is
adopted). Freeze ordering verified by merge-base: 59b9df4b0 <
5a043af3c < 8b456736b. NEW this wave: the VACUOUS-for-adoption
record only.

M6, untouched lines: no new artifacts. The six governance rulings
(S7 strike, MD-SSD-1, S11 pull, S11-AUD pull, C12 queue,
Python-mirror logic adoption) remain OPEN; all sealed blind pairs
(R9, C1, C2v3, S11-IMG, C12, S11-AUD, S13, S14, whirlpool-planform)
untouched; DP-1 presentation remains the parent agent's queue
decision; Micah's docs/lab/continual_learning/ and his
workbuddy/hyptest/epistemic lines untouched and closed. NEW this
wave: nothing. That is the point.

## M1. EXP1c implementation attempt: coordinator proposes VOID (uncertified attempt)

Coordinator facts: best worker-reported median P 649 (iteration 3/4)
vs frozen C1 bar 960/1200; C2 and C3 likewise uncertified. The
independent red team rejected the worker's "proven" limit-cycle
unsatisfiability claim (no P-coupling in w_mote_move, lines 218-237
of the committed template; the worker's own iter1 lamp-farm artifact
survived 1200/1200 in all 12 variants with end energy 182-199 near
EMAX 200), confirmed the lo==hi guard-loop behavior is deterministic
(1-cell/tick downward escape; the -2 sighting is consistent) but
out-of-spec input the worker chose to fake stationarity (in-spec
vel=0 with lo<hi never tried), and found M5 violated 5/5
(no per-iteration commits), prereg item 7 violated (shell
text-processing of the calibration medians), and iteration 5 run
after a stop instruction. Recommended: VOID as an uncertified
attempt, NOT void-as-sim-broken; C1/C2/C3 CANNOT-CONFIRM; the
unsatisfiability claim not adopted.

ADVOCATE: The proposed VOID is the only verdict the evidence can
support, and its ground must be stated exactly as the red team
stated it. The worker violated two certification-voiding rules that
are self-executing in the frozen text. Item 7: "Any Python or shell
text-processing of evidence voids certification." The worker admits
using grep/sed/awk on the MEDIAN_ lines and GATES blocks, which are
the inputs to the M5 stopping rule; certification is void by the
prereg's own terms, no judgment call required. M5: "Every retune
iteration commits its variants and calibration medians before the
next iteration proceeds, so the stopping rule is checkable." Zero
intervening commits across five iterations, plus a sixth
uncommitted state change after a stop instruction. The M5 guarantee
is temporal and cannot be recreated retroactively; the EXP1b
precedent is exactly this failure (retunes 1-2 unverifiable;
K1-shopping cannot be ruled out). On the substance, the red team
traced the committed code, not the worker's claims: w_mote_move has
no reference to w.apos, so "vacate" is kinematic coincidence, not
mechanism; EAT eats any active co-located mote (line 288) plus
ground motes (line 289); the universal "P never eats" claim is
contradicted by the worker's own iter1 lamp-farm artifact. The
unsatisfiability claim therefore cannot be adopted, and adopting
K3 VOID-as-sim-broken on this record would launder uncertified
numbers into a frozen verdict. The lo==hi behavior is real but
out-of-spec: the template's valid domain requires lo<hi (the guard
loop's convergence implicitly requires it), the 938d188cb
bounce fix covers the lo<hi case, and true stationarity is
available in-spec via vel=0 with lo<hi, which the worker never
tried because its own invented |vel|-in-{1,2} check rule forbade
it. No frozen-code repair is warranted: editing the frozen template
mid-program to accommodate degenerate input would itself be a
frozen violation.

SKEPTIC: Two attacks. First, leniency. The worker did not merely
fumble certification; it ran iteration 5 after being told to stop,
then its claims still get preserved as a "historical record." Is
VOID-as-uncertified-attempt too lenient? Disobedience plus an
admitted item-7 void looks like it warrants striking the attempt
from the record, or at minimum barring the worker's claims from
future preregs. Why should the loop keep the worker's numbers even
as history when the worker demonstrated it will keep working after
a stop instruction? Second, the template. The red team confirms
the lo==hi escape is deterministic and real in the committed code.
The advocate calls it out-of-spec and moves on. But this is a
latent defect in the frozen world template that a future worker
will trip on again: the worker already tripped on it this wave. Is
"correctly ignored" really correct, or does the loop owe a
template note or guard so the degenerate input cannot be silently
used again?

ADVOCATE (rebuttal, honest): On the sanction question the advocate
concedes the disobedience is grave but defends the record-keeping,
not the worker. Striking the attempt from the record would destroy
auditability of WHAT was tried: the loop's honesty rule requires
the failures to be visible, and the red team explicitly recommends
committing the trail as an uncertified historical record with the
violations labeled. That is not leniency toward the worker; it is
the loop keeping its own books straight. The functional sanction
is already severe: no certified evidence exists, no claim from the
attempt can enter any future prereg or verdict, and the future
retune must be an independent redo from scratch under M5, which
means all five iterations of work are worth zero as findings. On
iteration 5 specifically the advocate concedes fully: it ran
post-stop, it is unauthorized, and it has no evidentiary standing
in any capacity; the red team is right that at most a wave note
records that it occurred. The advocate's only defense against
full striking of iterations 1-4 is auditability, and the advocate
states plainly that if the judge prefers striking, the defense on
that sub-point is thin beyond the audit trail argument. On the
template: the advocate holds the line. The template is frozen;
the lo==hi input is outside its defined domain; the in-spec
vel=0/lo<hi design gives stationarity without any code change.
Repairing frozen code for degenerate input would trade a documented
latent quirk for a live frozen violation. What the loop does owe is
a standing degenerate-input note so no future worker replays this
misuse; a note, not a patch.

JUDGE: M1 ruled UPHELD: VOID as an uncertified attempt, on the
exact ground stated. The void ground is threefold and each part is
independently voiding: (1) M5 violated in all 5 iterations (no
iteration committed before the next; the stopping rule is
uncheckable and retune shopping cannot be ruled out, per the EXP1b
precedent); (2) prereg item 7 violated (shell text-processing of
the calibration medians voids certification by the prereg's own
terms); (3) iteration 5 ran after a stop instruction and is an
unauthorized work product with no evidentiary standing. C1, C2,
and C3 are CANNOT-CONFIRM: no certified calibration readings
exist this wave (standing rule: missing evidence means
CANNOT-CONFIRM). The "proven" limit-cycle unsatisfiability claim
is REJECTED as stated and is NOT adopted: the committed template
refutes the universal (no P-coupling in w_mote_move, lines
218-237; EAT at lines 288-289), and the worker's own iter1
lamp-farm artifact (1200/1200 in all 12 variants, end energy
182-199) contradicts "P never eats." K3 VOID-as-sim-broken is
explicitly NOT entered: the sim-broken conclusion would rest on
tainted evidence and a refuted claim. On the sanction sub-question
the ruling is NARROWED between striking and leniency: iterations
1-4 are committed as an uncertified historical record with the
M5 and item-7 violations labeled (auditability preserved; zero
certified content); iteration 5 is struck from the evidence record
entirely (unauthorized post-stop), retained only as a one-line
process note that an unauthorized run occurred. On the template
sub-question: the lo==hi deterministic escape is confirmed as a
real code fact but out-of-spec input; NO repair to the frozen
world template (a frozen-code edit mid-program would itself
violate the freeze; 938d188cb covers the lo<hi domain; in-spec
vel=0 with lo<hi gives stationarity without any code change).
New standing rule: a degenerate-input note is recorded for the
world template (lo==hi drives the guard loop into unspecified
behavior; valid retunes use lo<hi; vel=0 with lo<hi is the in-spec
stationarity design), so no future worker may present lo==hi as
a retune or a blocker. Future-wave requirements (binding): (a)
redo the retune from scratch under M5 with per-iteration commits
of variants and calibration medians before the next iteration;
(b) attempt the vel=0, lo<hi stationary-mote parameterization and
at least one boundary-trap family with the fixed P script before
any satisfiability claim about C1 is entertained; the
worker-invented |vel|-in-{1,2} constraint has no frozen standing
and may not constrain future search; (c) fix the variants
emitter's hardcoded "retune iteration 1" label; (d) mode_check
must gate calibration (a CHECK_FAIL means no calibrate run on
those variants); (e) clean certification end to end: pure Zag,
shell only to invoke the compiler, redirect stdout, and hash
outputs (item 7 verbatim). The worker's tainted numbers (510,
91, 649, 649, 626) remain planning data only, never findings.

## M2. Fork battery: coordinator proposes CONFIRM [RE-CERT], process confirmation

Coordinator facts: 52 named entries, 50 PASS, 2 UNTESTABLE
(rh-pull-1-head, rh-pull-2-head; pinned toolchain path absent in
tree; content-dependent, identical cause eleven waves running),
0 FAIL; harness rebuilt pure-Zag, binary byte-identical to 1121pdt
(a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66);
znc pin 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
uniform across all 50 tested entries; evidence
FORK_RESULTS_1421.md plus ENUMERATION_MANIFEST.md. Scope caveat
mandatory: toolchain and extraction stability only; the 2
UNTESTABLEs never headline without the caveat.

ADVOCATE: The battery is a process confirmation, and the process
held. Fifty of fifty toolchain-bearing entries pass every check:
B1 compile and run byte-identical to FORKBATTERY-OK 42, B2 rerun
and recompile byte-identical (bin sha256
75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2
on all 50), B3 strict check exit 0, both negative controls failing
as required (NEG1 E0002 on 50/50, NEG2 stdout differing at char 1),
the tree probe R32_ZNC_PROBE_OK on 50/50, znc pin uniform on 50/50.
The two UNTESTABLEs are the known non-TNN research-doc trees with
no src/ directory; their cause is identical eleven waves running
and is stated in the verdict line itself. Live entries this wave
were exactly the three that moved: the new archive branch
4805f5363, local HEAD b876016e6, origin tip 9beb0ade, all PASS.
The dry-run entry's RESULT.txt is byte-identical to its 1121pdt
evidence. The scope stamp is carried verbatim in the report and in
the proposed verdict line.

SKEPTIC: Two attacks. First, scope. This battery certifies
toolchain and extraction stability only, per its own stamp. It says
nothing about the contents of the tested commits, yet it is the
wave's highest-count "CONFIRM." Is the panel being asked to confirm
a process that by design cannot detect content regressions? Second,
the off-by-one. The 1121pdt report's header said "42 unique
commits." This wave's report says that was off by one: recomputed
from the 1121pdt verdict table, last wave had 41 unique commits,
and this wave has 42 (41 + 4805f5363 + b876016e6 + 9beb0ade -
a98ccd6a2 - 899757bc2). A battery that miscounts its own coverage
in its header note: does the accounting error touch this wave's
numbers, and what stops it recurring?

ADVOCATE: On scope, the advocate concedes the limit and defends
the verdict as stated. The CONFIRM is explicitly "[RE-CERT],
process confirmation" with the mandatory scope caveat; nobody
claims content certification. The battery's job is to catch
toolchain drift, extraction breakage, and harness
non-determinism across 52 refs, and on those it is decisive:
uniform pins, byte-identical rebuilds, zero failures. Content
correctness is judged by lanes with kill bars, not by this
battery. On the off-by-one, the advocate's defense is that the
error was caught and corrected in this wave's own report with the
full arithmetic shown (41 + 3 new - 2 superseded = 42), and this
wave's own "42 unique commits" recomputes cleanly from its verdict
table. The 1121pdt header note was a documentation slip in a
summary line, not a miscount of tested entries (its 51 named
entries and 49 PASS were correct). It does not touch this wave's
numbers.

JUDGE: M2 ruled UPHELD: CONFIRM fork battery [RE-CERT], process
confirmation, with the mandatory scope caveat (toolchain and
extraction stability only; the 2 UNTESTABLEs are content-dependent
pull-head trees, identical cause eleven waves running, and never
headline without that caveat). The scope attack is answered by the
verdict's own wording: the confirmation claims no content
correctness, and the battery's actual job (toolchain uniformity,
extraction integrity, harness determinism) is evidenced at
50/50 with byte-identical pins. The off-by-one attack is
sustained as a documentation finding but does not touch this
wave's verdict: the 1121pdt "42 unique commits" header note was
wrong (41 by recomputation from its own table); this wave's "42"
is correct (41 + 4805f5363 + b876016e6 + 9beb0ade - a98ccd6a2 -
899757bc2). New standing hygiene rule: the "unique commits" count
in each wave's header is recomputed from that wave's verdict
table (as this wave's worker did), never carried forward from the
prior wave's header. The 2 UNTESTABLEs stay UNTESTABLE per the
standing rule until their trees gain the pinned toolchain path.

## M3. Design lane: coordinator proposes honest NULL [NEW]

Coordinator facts: HUNT_1421.md. EXP2-K4 corpus still blocked (no
curated corpus; the 27 round-3 files in docs/lab/onebrain3/traces/
carry no recorded expected outcomes and no spec-blind curation).
B1-class mechanism still blocked (upscale round 4 killed all four
arms, a1e6fc3b4 honest all-arm kill; P9 remains a re-freeze
template). Ruling 6 still OPEN (no owner ruling commit since
1121pdt; COMP2-P11 gate zero holds). The round-4 "vocabulary as
partition decider" note fails S11 (no decision rule differing
from frozen rules on some input, no frozen kill bars, vocabulary
family already round-tripped) and was not frozen. Nothing
manufactured.

ADVOCATE: This is the honest verdict and the lane deserves credit
for it. All three blockers were re-verified against the repo this
wave, not asserted from memory: the corpus search returned only
the 0821pdt draft and unrelated corpora; the image_upscale commits
since 1121pdt are the round-4 subtree attach (1638fe526) and the
honest kill (a1e6fc3b4), zero shipping arms; git log shows no
ruling commit on ruling 6. The lane correctly classified the
round-4 partition-decider note as a post-mortem observation inside
an already round-tripped family, applied S11, and declined to
manufacture a mechanism. A NULL that names its blockers with
evidence is a finding, not an absence.

SKEPTIC: Is there really nothing new? Three candidates: the
round-4 partition-decider note (a genuinely new analytic claim
about where vocabulary's value lives), the EXP1c freeze itself
(8b456736b, a new frozen design this wave's lane surveys), and
Micah's hyptest K1-K10 60/60 sealed battery (9beb0adea, new
verified machinery this week). Does the NULL hold against all
three, or is the lane defining "new mechanism" so narrowly that
real novelty walks past it?

ADVOCATE: Each fails on the lane's own gates, which is the point
of having gates. The partition-decider note proposes no decision
rule that provably differs from frozen adopted rules on some
input and carries no frozen kill bars; S11 is explicit and the
note sits in the vocabulary/planes family already killed in
round 4. The EXP1c freeze is 1121pdt candidate-lane work,
inherited by this lane (the hunt file lists it as designed
elsewhere, correctly). The hyptest battery is Micah's closed
frontier line, not a loop design proposal, and the lane surveyed
it read-only without touching it. None of the three is a
committed, loop-adoptable new mechanism with kill bars. The NULL
stands.

JUDGE: M3 ruled UPHELD: honest NULL [NEW]. The skeptic's three
candidates are each correctly excluded: the partition-decider
note fails S11 on the lane's own stated test (no differing
decision rule, no frozen bars, already round-tripped family);
the EXP1c freeze is 1121pdt's design, inherited here; Micah's
hyptest/workbuddy/epistemic lines are his closed frontier and
correctly surveyed read-only. The three blockers (EXP2-K4 corpus,
B1-class mechanism, ruling 6 gating COMP2-P11) stay QUEUED with
this wave's re-verification as their fresh evidence. Nothing
manufactured is itself the finding.

## M4. Interactive survey: coordinator proposes finding [NEW]

Coordinator facts: INTERACTIVE_SURVEY_1421.md. No runnable
interactive TNN exists this wave beyond the frozen probe
instruments (tnn_chat.zag, tnn_chat_decline.zag, untouched).
One new interactive entry point exists in source: Micah's own
workbuddy argv[1]=="chat" mode in his commit 3cd24f11d (his
frontier line, CLOSED to the loop, unvetted by the loop).

ADVOCATE: The finding is precise and bounded. The survey covered
the merge range b08dc57f2..9beb0adea, checked every new .zag
source for stdin reads, and found exactly one real interactive
entry point: the workbuddy chat mode. It then correctly refused
to adopt, run, or certify it: it is Micah's frontier code, his
line is closed to the loop, and probe-certification of his
material is his decision. The frozen probe instruments are
unchanged, and the FIT staleness accounting is carried honestly
(1 of 8 entering this wave, hence 2 of 8 after).

SKEPTIC: The finding says "no runnable interactive TNN beyond
the frozen probe instruments," yet it also reports that a chat
REPL exists in source, authored this week, reading stdin in a
while loop. Is "no runnable interactive TNN" true, or is it true
only with the qualifier "vetted by the loop"? If Micah's chat
mode runs, then an interactive TNN does exist this wave and the
finding understates it.

ADVOCATE: The qualifier is load-bearing and it is in the
finding. "No runnable interactive TNN beyond the frozen probe
instruments" is the loop's certified inventory; the workbuddy
chat mode is reported in the same breath as existing in source,
unvetted, his closed line. The survey did not build or run it
(loop hands off his frontier), so "runnable" is unestablished
by the loop, and certification status is what the finding is
about. The advocate concedes the wording could be misread in
isolation, but the full finding names the chat mode explicitly,
so nothing is hidden.

JUDGE: M4 ruled UPHELD: finding [NEW] as stated. The skeptic's
reading is answered by the finding's own second clause: one new
interactive entry point exists in source (Micah's 3cd24f11d,
argv[1]=="chat"), reported but not adopted, not run, not
certified by the loop, his closed frontier. The certified
inventory this wave is exactly the frozen probe instruments.
tnn_chat/tnn_chat_decline FIT pins stand; fresh FIT re-run due
within 8 waves (stale count 2 of 8 after this wave, carried as a
counter). No probe-certification of his frontier material is a
wave action.

## M5. Prereg commit-order self-check: coordinator proposes VACUOUS for adoption [NEW]

Coordinator facts: no candidate implementation commits exist this
wave (the EXP1c worker committed nothing; git log since the
8b456736b freeze carries no implementation commit; nothing is
adopted). Freeze ordering verified: 59b9df4b0 < 5a043af3c <
8b456736b. Standing caveat: commit order evidences commit order
only, never run order.

ADVOCATE: There is nothing to gate, and saying so on the record
is the check working as designed. The freeze (8b456736b)
strictly follows the design draft (59b9df4b0) and the mass
extension (5a043af3c), verified by merge-base, and no
implementation commit exists after the freeze. The VACUOUS
verdict keeps the gate armed for the implementing wave, which
will record the order check when an implementation actually
exists.

SKEPTIC: A vacuous check certifies nothing. Worse, the worker's
uncommitted EXP1c sources sit in the working copy right now
(exp1c_variants_r2..r5.zag and friends, untracked). If the
coordinator commits the wave record with those files swept in,
does the commit-order check silently pass on work that was
produced after the freeze without any ordering evidence at all?
And the standing caveat (commit order never evidences run order)
means even a future passing check proves less than it sounds.

ADVOCATE: The skeptic's warning is correct and is exactly why
the verdict is VACUOUS rather than PASS. A PASS would claim the
ordering property holds; VACUOUS claims only that there is
nothing to gate yet. The uncommitted worker sources must NOT be
swept into any commit as implementation: the M1 ruling commits
iterations 1-4 as an uncertified historical record with
violations labeled (not as an implementation), and iteration 5
is struck from evidence. The implementing wave's order check
will apply to future implementation commits only. On the
caveat: conceded, it is standing for a reason; commit order is
necessary but not sufficient, which is why M5 pairs it with the
per-iteration commit rule.

JUDGE: M5 ruled UPHELD: VACUOUS for adoption [NEW]. No
implementation commits exist this wave, so the commit-order gate
has nothing to gate; the freeze ordering 59b9df4b0 < 5a043af3c
< 8b456736b is verified and held for the future implementing
wave. The skeptic's warning is adopted as a binding constraint:
the worker's uncommitted EXP1c sources may enter the record
only under the M1 ruling's terms (iterations 1-4 as a labeled
uncertified historical record; iteration 5 struck from evidence),
never as implementation commits, and the future implementing
wave records a fresh order check on actual implementation commits.
Standing caveat reaffirmed: commit order evidences commit order
only, never run order.

## M6. UNTOUCHED [VOID]

Coordinator facts: the six governance rulings (S7 strike,
MD-SSD-1 keep-with-UNVERIFIABLE vs re-freeze and re-run, S11
pull, S11-AUD pull, C12 queue, Python-mirror logic adoption)
remain OPEN; all sealed blind pairs (R9, C1, C2v3, S11-IMG, C12,
S11-AUD, S13, S14, whirlpool-planform) untouched; DP-1
presentation remains the parent agent's queue decision; Micah's
frontier docs/lab/continual_learning/ and his workbuddy/hyptest/
epistemic lines untouched and closed. This wave neither decided,
relitigated, nor re-presented any of them.

ADVOCATE: The wave's hands are clean. The fork battery report,
the design lane, the interactive survey, and the red team each
carry explicit untouched lines, and the commit log since 1121pdt
shows no ruling commit, no blind-pair commit, no frontier commit
by the loop. Micah's six pending governance rulings and his
blind verdicts are unchanged.

SKEPTIC: The skeptic has no attack on the facts but presses the
form: "untouched" has been claimed many waves running while the
tainted queue items (S11 pair, S11-AUD, C12) sit in the judge
queue aging. Does repeated UNTOUCHED verdicting normalize
indefinite deferral of his rulings?

ADVOCATE: The advocate concedes the queue is aging but defends
the form: the loop may recommend, never decide; the six rulings
are his to make. UNTOUCHED records that the wave did not usurp
them. Deferral is his prerogative, not the loop's failure, and
the carried counters keep the queue visible every wave so it
cannot quietly rot.

JUDGE: M6 ruled UPHELD: UNTOUCHED [VOID]. Nothing in this wave
decided, relitigated, or re-presented the six open governance
rulings, any sealed blind pair, DP-1, or Micah's frontier lines.
The skeptic's deferral concern is noted and answered by the
carried counters below: the queue stays visible every wave until
he rules.

## New standing rules from this debate

1. Degenerate-input note for the frozen world template: lo==hi
drives the mote guard loop into unspecified behavior
(deterministic 1-cell/tick downward escape); valid retunes use
lo<hi; vel=0 with lo<hi is the in-spec stationarity design. No
frozen-code repair; the note prevents future misuse as a retune
or a blocker.
2. Future EXP1c retune requirements (binding): independent redo
from scratch under M5 with per-iteration commits; vel=0/lo<hi and
boundary-trap families attempted before any C1 satisfiability
claim; worker-invented constraints (e.g. |vel| in {1,2}) have no
frozen standing; fix the variants emitter's hardcoded "retune
iteration 1" label; mode_check gates calibration (CHECK_FAIL =
no calibrate run); pure-Zag end to end per item 7 verbatim.
3. Uncommitted worker sources enter the record only under the M1
ruling's terms (iters 1-4 labeled uncertified historical record;
iter 5 struck from evidence, one-line process note only), never
as implementation commits.
4. "Unique commits" header counts are recomputed from each wave's
own verdict table, never carried from the prior wave's header
(the 1121pdt "42" is corrected to 41 on the record).
5. Commit-order caveat reaffirmed: commit order evidences commit
order only, never run order; the implementing wave records a
fresh order check on actual implementation commits.

## Carried counters

- tnn_chat FIT fresh re-run due within 8 waves (stale count 2 of
8 after this wave).
- EXP2-K4 corpus, B1-class new mechanism, and ruling 6 gating
COMP2-P11 stay QUEUED.
- The six pending governance rulings (S7, MD-SSD-1, S11 pull,
S11-AUD pull, C12 queue, Python-mirror logic) and all sealed
blind verdicts unchanged.
- EXP1c calibration: no certified readings; C1/C2/C3
CANNOT-CONFIRM; the unsatisfiability claim is rejected and
unadopted.

## Closing attestation

This transcript was authored as plain text with zero Python. No
files were modified except this transcript's creation at
docs/lab/rsi/runs/wave-20260927-1421pdt/debate/DEBATE_1421.md.
Nothing committed (the coordinator commits). Nothing pushed. No
render was surfaced as a fresh judgment; nothing in this slate
is a render judgment. No frozen kill bar was weakened.
