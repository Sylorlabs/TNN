# DEBATE TRANSCRIPT: wave-20260927-2021pdt

Roles: ADVOCATE argues FOR each proposed verdict (certify as much as the
evidence supports). SKEPTIC argues AGAINST certification (withhold as much
as the evidence requires). The judge is a separate agent and is not bound
by either brief. No em-dashes are used in this document.

Wave record under debate:
- EXP1c addendum d9e96ad91, iteration 1 milestone 2 9625c211a, full
  experiment milestone 3 f26d510f3, evidence note milestone 4 4750f1a19,
  independent red team bb60f27f5 (report
  docs/lab/rsi/runs/wave-20260927-2021pdt/exp1c/REDTEAM_EXP1C_2021.md)
- Fork battery dbe397973 (report
  docs/lab/rsi/runs/wave-20260927-2021pdt/forks/FORK_RESULTS_2021.md)
- tnn_chat FIT 927b3f3f7, evidence 78a8037fd (report
  docs/lab/rsi/runs/wave-20260927-2021pdt/tnn_chat/FIT_RESULTS_2021.md)
- Design lane and interactive survey 6062b4a94 (reports
  docs/lab/rsi/runs/wave-20260927-2021pdt/design_lane/HUNT_2021.md and
  docs/lab/rsi/runs/wave-20260927-2021pdt/INTERACTIVE_SURVEY_2021.md)

Frozen prereg: docs/lab/rsi/runs/wave-20260927-1121pdt/preregs/PREREG_EXP1c_FROZEN.md
(freeze 8b456736b). Pinned toolchain: src/tools/toolchain/znc_linux_x86_64_abed8aa1,
SHA-256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef.
World template: docs/lab/invention/survival/src/world.zag, blob
fff8af2493bc6dbe9de6fc76f9a6206d887d586a. Training mass:
docs/lab/invention/survival/kb/kb_exp1c.txt and kb_p_exp1c.txt (5a043af3c).

---

# ADVOCATE BRIEF

## M1. EXP1c wave 2: VOID (uncertified attempt) as a test of H1/H2 [VOID], nothing adopted; K7-void takes precedence over K1/K6; K1/K6 numbers recorded as measurements from a voided run, not adopted kills; iteration preserved as an uncertified historical record with violations labeled.

The proposed verdict is the maximum the evidence supports, and it is
fully supported. The independent red team (bb60f27f5) verified every
material element of the attempt except the one blocker, finding R1:

1. M3 is implemented verbatim. e1c_agents.zag lines 303-309 score each
sketch as mean experienced delta-energy plus B0/(1+n) with integer
division, and lines 316-331 run a deterministic argmax with
strict-greater tie-break, so enumeration proceeds in M1 lex order; the
IDIAG n_distinct reaches 399 for I-invent in 6 variants, confirming
enumeration actually proceeds and the 1721pdt F1 stall is fixed.
e1c_run.zag lines 69-70 set B0=40 for arms 3 and 5 and B0=120 for arms
4 and 6, matching the frozen schedule. A grep finds no bonus constants
beyond the two frozen B0 values. This is the exact fidelity the 1721pdt
red team demanded.

2. M4 contains exactly the three frozen reflexes and no others.
e1c_agents.zag lines 408-412 implement the verbatim storm-active
condition (the 1721pdt F4 "within 2 ticks" drift is gone); lines
414-418 implement the verbatim energy-below-25 survival reflex; lines
334-348 (xi_h9) gate every step about to be taken against the taught
H9 void-step refusal (the 1721pdt F3 absence is fixed). The 1721pdt F2
mote-adjacent preemption is gone. The plank carve-out mirrors the
frozen world's own void-fall rule (world.zag lines 274-275) and its
boundary clamp (lines 264-280), so it is fidelity to frozen physics,
not condition drift.

3. The evidence note is genuinely Zag-generated and byte-identical to
fresh e1c_evidence.zag stdout. The red team hand-recomputed all seven
medians from run1.tsv (P=1200, R=1200, Z=24, I-survive=918,
I-invent=920, I-survive-abl=1082, I-invent-abl=1200) and every number
matches the note. No 1721pdt F6-style corruptions exist.

4. Determinism is independently reproduced end to end: the red team
rebuilt from committed sources with the pinned znc and reproduced
run1.tsv byte-identically twice (SHA-256
0e82ba093953da59e0d4d1de25cf75501b5108992857ae281607c9519281c288,
matching evidence/HASHES.txt); run1.tsv and run2.tsv are byte-identical;
84 RUN rows plus 48 IDIAG rows.

5. K7 is computed on the frozen quantity with the instrumentation
inversion fixed: among post-enumeration selections only, counting
10*bonus < score. Data: I-survive 0 post-enumeration selections,
I-invent 89 post and 0 learned. Fraction 0 < 0.50, so K7 VOID is
correct, with the addendum's pre-run zero-denominator handling
(no post-enumeration plans observed means K7 fails).

6. Commit order is strict: 8b456736b < d9e96ad91 < 9625c211a <
f26d510f3 < 4750f1a19, verified by merge-base with no intervening
commits, and the addendum was committed alone before any
implementation file existed. The sources are pure Zag.

The section-7 redraft addendum is legitimate, not a post-freeze bar
move. The 1721pdt debate imposed it as a binding forward requirement:
"treats the section 7 arithmetic as a frozen defect to be fixed by
redraft, never by post-freeze edit." The addendum (d9e96ad91) states
the corrected 1134-tick minimum, withdraws only the arithmetically
impossible claims, and explicitly changes no mechanism, bar, gate,
horizon, bonus number, or decay rule. Its "K7 takes precedence over
any K1 firing" restates the frozen section 6 text ("K3 or K7 failure
means VOID"; "K7 is a validity gate, not a kill"), it does not invent
precedence. Its zero-denominator K7 handling was specified
pre-implementation, so it is pre-hoc, not post-hoc.

The C3 misstatement is severable from the VOID verdict. C3 is a
calibration validity gate on the sim, not a kill bar and not part of
the H1/H2 test machinery. The false premise is prose in ITERATION1.md
("qualitatively distinct") plus an in-Zag gate that counts medians
only; it cannot move K1, K2, K6, or K7 by one tick. The red team's
own finding R1 states: "This finding does not change any kill-bar
verdict." The sim-diversity concern C3 guards is substantially met in
the full run, where the P arm (taught ward strategy, median 1200) and
the R arm (heuristics, median 1200) are behaviorally distinct
surviving strategies. The correct sanction is to strike the
distinctness sentence in the record and leave the run's verdicts
otherwise intact. VOID rests on K7, which is independently verified.

K1 and K6 are recorded as measurements, not adopted kills, exactly as
the proposed verdict states. The numbers are arithmetically correct
(hand-verified from run1.tsv: 918<=1200 fires K1; 1082>=918 and
1200>=920 fire K6). The K6 ablation is a genuine intervention, not a
no-op: it excludes COMBINE-containing sketches from I-arm selection,
medians move, and the M4 reflexes including H9 void safety are
preserved, so there is no EXP1b-style void-reflex dropout confound;
it fires, which is real negative information about this design family
for the next design wave. Labeling preserves data; striking destroys
it. The 1421pdt precedent and the 1721pdt debate sanction are
preservation, not striking, with violations labeled, and auditability
is the reason. The worker's honesty is credited: K7 VOID, K4
CANNOT-CONFIRM, K5 INCOMPLETE, and the section-7 NOT-MET were all
reported without flinching, and no retune shopping occurred (the
worker stopped at iteration 1 under M5 with the per-iteration commit).

Provenance for M1: new this wave are the section-7 redraft addendum
(d9e96ad91), the fresh implementation sources (e1c_agents.zag,
e1c_calib.zag, e1c_check.zag, e1c_emit.zag at 9625c211a; e1c_run.zag
at f26d510f3; e1c_evidence.zag at 4750f1a19), the fresh calibration
evidence (iterations/iter1/*) and full-run evidence
(evidence/run1.tsv, run2.tsv, note1.md, note2.md, HASHES.txt), the
independent red-team review (bb60f27f5), and this debate. Inherited
are the frozen prereg 8b456736b (M1-M5, K1-K7, C1-C3 verbatim), the
training mass at 5a043af3c, the world template blob
fff8af2493bc6dbe9de6fc76f9a6206d887d586a (bounce fix 938d188cb), the
pinned toolchain 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef,
and the 1421pdt/1721pdt records as planning reference only. Nothing
was recycled as evidence.

## M2. Fork battery: CONFIRM [RE-CERT], 55 named entries, 53 PASS, 0 FAIL, 2 UNTESTABLE.

The 1721pdt debate's binding note required "the next wave runs the
full 54-entry table on the repaired tree." This wave ran a full
55-entry table on the repaired tree: the task-pinned run-start HEAD
fc1a43b8c carries the toolchain repair (37d1d3cab is its ancestor;
git ls-tree confirms znc_probe.zag plus the other 11 dropped files
are present). The local-tnn-native-lab entry now PASSES. The closure
condition is met on its own terms; the 1721pdt single-step re-test
was never meant to amend the verdict table, and the full rerun now
exists, so the FAIL is genuinely closed by content restoration, not
by any harness or driver change (the harness is rebuilt byte-identical
to 1721pdt at
a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66).

Every new or moved ref since 1721pdt is handled in the record. Origin
tnn-native-lab moved a5bba138 to bedf8b4a since 1721pdt close; both
origin named entries were newly testable this wave (the bedf8b4a
object is in the local store) and PASS. The one new branch
(tnn-native-lab-wave-archive-wave-20260927-1721pdt at 4042f15bf) was
enumerated and tested first in the batch, PASS. Read-only ls-remote
at run start and close agree; the tnn-native-lab tip did not move
during the run. The mid-run local HEAD move (fc1a43b8c to 927b3f3f7
by another lane) is inert by pinning: the tested entry is the
task-pinned run-start commit, and the report says so explicitly.

The standing hygiene rule is satisfied and independently checkable:
recomputed from this wave's own verdict table, 55 data rows give 53
PASS and 2 UNTESTABLE with 44 distinct commit SHAs. Uniform battery
evidence holds across all 53 PASS runs: znc pin
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef on
53/53, probe source sha 3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919
on 53/53, B1/B2/B3 pass, and both negative controls fail as required
(NEG1 E0002 on all 53; NEG2 stdout "WRONG OUTPUT" differing at char 1
on all 53). The two UNTESTABLEs are rh-pull-1-head and rh-pull-2-head
with the identical content-dependent cause thirteen waves running
(pinned toolchain path absent in non-TNN research-doc trees); the
counts are never headlined without that caveat, per the report.

Provenance for M2: new this wave is the full 55-entry execution on
the repaired tree (dbe397973), the enumeration manifest, the
build-record files, and the 55 per-entry evidence dirs. Inherited are
the frozen battery procedure, the pure-Zag harness source
(byte-identical rebuild), the pinned znc, the frozen flag order and
expected outputs, and the standing UNTESTABLE cause for the two
pull-head entries. No result was faked; scope stays toolchain and
extraction stability only.

## M3. tnn_chat FIT: [NEW, process confirmation], fresh re-run PASS.

The standing rule (minted wave-20260927-0521pdt) mandated a fresh
re-run this wave: the last fresh re-run was verified at
wave-20260927-1421pdt and the stale count stood at 4 of 8, so the
re-run was DUE. It was done, not skipped. The numbers are clean:
decline and baseline binaries rebuilt with the pinned znc are
byte-identical to the frozen records (decline
20273a99215680b5e3e42bbdbbfed105c7109d15ba189c903cf0d88db54418e7;
baseline
1ada2fae63ddd63d37f06705459c0d8b1d9c8dffc859af25949221bf5895749c),
2/2 PASS; KB1 30/30 specific declines with 0 blanket refusals across
3 runs; KB2 17/17 answered with 0 declines and byte-identical
baseline parity; KB5 10/10 answered with 0 declines and byte-identical
baseline parity; 9/9 required rerun pairs byte-identical (15/15
including baseline pairs); all three output hashes byte-identical to
the prior wave records; all 15 runs exit 0 with empty stderr.

The skeptic's merge-range probe is answered with a precise negative.
The chain-diff over 80c40a7af..fc1a43b8c on the FIT chain paths
(docs/lab/rsi/fit_authority/, the pinned znc,
docs/lab/bytegen/authority_law/dialogue/) shows exactly one change:
an additive record-only file docs/lab/rsi/fit_authority/SHA256SUMS
(34 insertions; every pin in it matches the frozen records). Zero
changes to any instrument source, fixture, kb.txt, gaz.txt, R33
support source, or the znc binary. Zero Python anywhere (shell
coreutils only), so nothing is voided.

This is process confirmation with literal scope: the frozen 38-fact
closed-book probe chain only, on HEAD fc1a43b8c. It is not a
candidate verdict and not merge review of the merged-in work. The
report states the caveats plainly (closed-book instrument, not an
open-domain model; the traveling confabulation caveat; no live
learning), which is exactly the honesty the loop asks for. Evidence
commit 78a8037fd; lane commit 927b3f3f7; nothing pushed.

Provenance for M3: new this wave is the fresh re-run execution and
its report. Inherited are the frozen probe instruments
(tnn_chat.zag, tnn_chat_decline.zag), the R33 support sources, the
canonical kb.txt and gaz.txt, the three probe fixtures, the expected
classes and output hashes, the pinned toolchain, and the frozen
procedure itself.

## M4. Design lane: NULL/HELD [NEW]. Interactive survey: NONE loop-owned [NEW].

The 1721pdt judge set a forward bar: future NULLs must carry survey
method with counts, per-lane blocker evidence with commit ids, and an
explicit nothing-manufactured statement. HUNT_2021 clears that bar on
all three:

1. Survey method with counts: the merge range d09d5bfde..fc1a43b8c
resolves to 30 origin commits plus 10 local first-parent commits;
11,765 files added in the range (2,098 of them .zag);
docs/lab/onebrain3/traces/ listed (27 files, unchanged from the
1721pdt count); a case-insensitive name scan for corpus, failure,
and trace across every added file; the adding commit traced for
each hit; docs/lab/image_upscale/ changes enumerated.

2. Per-lane blocker evidence with commit ids: EXP2-K4 HELD because
the 27 trace files are round-3 measurement run outputs added by
Micah's f71ff91f6 (no expected outcomes, no spec-blind curator
attestation), the one corpus-named addition is his TA-CORPUS v1 seal
(879bbb4cf, SHA-256
c36108728ebce982bc0255cd835f05a65c25952722c3af45a2c6032c0283ce03,
a Self-PAM text-approx corpus, closed to the loop), and the 45
trace-named files resolve to inherited history or his closed video
and imagination traces; B1 NULL because no new round subtree, arm,
or mechanism text exists in loop scope since the 1121pdt DISCARD,
PREREG_B1_P9.md last touched by 09bfaae63 stays a re-freeze template,
and the P9 bar set fails the S11 genuineness test; ruling 6 HELD
because a message-text search over all 30 origin commits for
ruling, governance, Python-mirror, and COMP2-P11 terms returns
exactly one hit, RULING_KHA3_2026-09-27.md inside 57d055bbb, which
records a test-determined ruling on the K-HA-3 spec clause and is
not ruling 6; trades HELD because no genuinely new expensive
capability exists in loop-owned scope (the new capability-ish lines
are all his closed frontier, read-only) and inventing an expensive
knob without a genuine capability would be manufacturing; sensory
NULL under the standing stand-downs (G1, D-VID-1, ST-1 dead; E3
rejected by Micah in blind A/B).

3. An explicit nothing-manufactured statement: "No candidate was
invented, no knob was costumed as a capability, no closed-frontier
artifact was ingested as probe material, and no verdict was padded
to look like progress."

The interactive survey is equally methodical: the full added-file
.zag diff (217,516 lines) scanned for chat, repl, stdin, readln,
readline, argv, interactive, tui plus raw fd-0 reads; all 184 .zag
files added by the 30 origin commits enumerated and grepped; the 16
other fd-0 hits dispositioned as pre-existing with commit ids; the
one tui hit dispositioned as a code comment referencing the existing
d2bin tui instrument. The three new entry points (h1.zag chat REPL
at 9dbd01e26, h2.zag chat REPL plus fuzz driver at 7979a55b1,
h3.zag chat/chat-fixed/chattrace modes at 7f5a8ccdb) are all
Micah-authored in his closed D2 new-learner frontier: surveyed
read-only, never built, run, certified, or re-judged. Verdict NONE
loop-owned is therefore earned, not asserted.

Provenance for M4: new this wave are the hunt report and the survey
report (6062b4a94). Inherited are the standing stand-downs, the
QUEUED drafts (PREREG_EXP2_K4.md, PREREG_B1_P9.md,
PREREG_COMP2_P11.md), the 1121pdt DISCARD, the frozen probe
instruments, and Micah's frontier commits, which enter the record
only as read-only survey citations with closed-frontier status
stated. Nothing was manufactured and nothing of his was ingested.

## M5. Commit-order self-check: VALID, VACUOUS for adoption. UNTOUCHED [VOID]: the six governance rulings, all nine sealed blind pairs, DP-1, Micah's frontier dirs.

The commit order is strict end to end: 8b456736b < d9e96ad91 <
9625c211a < f26d510f3 < 4750f1a19, each verified by merge-base
--is-ancestor with exactly one commit in each interval (no
intervening commits). The addendum (d9e96ad91) contains one file and
was committed alone before any implementation file existed; the
exp1c/src files first appear at 9625c211a. The other lanes' commits
(fork dbe397973, FIT 927b3f3f7 / evidence 78a8037fd, design and
survey 6062b4a94, red team bb60f27f5) are lane-local and carry no
EXP1c implementation content. Nothing is adopted this wave (the EXP1c
attempt is VOID, no candidate, no mechanism, no bar), so the check is
VACUOUS for adoption exactly as stated. The standing caveat is
carried: commit order evidences commit order only, never run order.

UNTOUCHED holds on inspection of the wave record. The six governance
rulings (S7 strike, MD-SSD-1, S11 pull, S11-AUD pull, C12 queue,
Python-mirror logic) appear only as OPEN/untouched statements; the
design lane's ruling-6 search confirms no governance document was
touched in the range. All nine sealed blind pairs (R9, C1, C2v3,
S11-IMG, C12, S11-AUD, S13, S14, whirlpool-planform) appear only in
untouched lists; none was opened, re-certified, or moved. DP-1
appears only as the parent agent's queue decision. Micah's frontier
dirs (continual_learning, workbuddy, hyptest, epistemic_native, and
the surveyed onebrain, Self-PAM, composition, exp2d, D2 new-learner,
combiner_arch, shared-brain, Grow-with-me, NW-1 lines) were touched
only read-only via git log and listings. No wave commit decides,
relitigates, or re-presents any of them. The 1721pdt debate's
[VOID]-to-the-debate treatment of the rulings is repeated verbatim
in spirit and in fact.

Provenance for M5: the ordering evidence is new this wave (fresh
merge-base verification); the ordering rule itself and the six
rulings, nine pairs, DP-1 queue status, and frontier closures are
inherited and untouched.

---

# SKEPTIC REPORT

## M1. AGAINST certifying the EXP1c wave-2 attempt: the C3 defect is not severable, the K1/K6 numbers are uninformative, and the record carries an unverified compiler claim.

> "What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

New this wave: the section-7 redraft addendum (d9e96ad91), the fresh
implementation sources (9625c211a, f26d510f3), the fresh calibration
and full-run evidence (iterations/iter1/*, evidence/*), the
Zag-generated evidence note (4750f1a19), the independent red-team
review (bb60f27f5), and this debate. Inherited: the frozen prereg
8b456736b (M1-M5, K1-K7, C1-C3 verbatim), the training mass at
5a043af3c, the world template blob
fff8af2493bc6dbe9de6fc76f9a6206d887d586a, the pinned toolchain, and
the 1421pdt/1721pdt records as planning reference. Nothing in this
list is disputed. What is disputed is whether the new artifacts, as
committed, can carry the verdict the advocate wants.

First, the C3 misstatement is fatal to the attempt's certification,
not severable from it. The 1721pdt red team issued a binding required
correction: "make C3 check behavioral distinctness, not just median
counts, or field a third genuinely distinct surviving strategy"
(finding F10). This wave did neither. The in-Zag C3 gate still counts
medians only (C3_DISTINCT=3 never tests distinctness), and the
worker's own calibration data refutes the prose: calib1.txt shows f0
(forage) and f2 (homebody) with IDENTICAL (ticks, e_end) in all 12
variants (variant 0: 1200/145 and 1200/145; variant 1: 1200/161 and
1200/161; identical across all twelve). Yet ITERATION1.md asserts the
three strategies are "qualitatively distinct" and the e1c_calib.zag
comment calls them "behaviorally distinct by construction." That
phrase was written after the data existed. The advocate's severability
argument misses the load-bearing point: the M5 stop decision reads
"Retuning stops at iteration 1... C3 PASS (3/3 distinct >=720)." The
stopping rule is M5, and M5 is what makes iteration 1 the attempt at
all. A stop decision resting on a false premise means the retune
protocol's stopping condition was not honestly satisfied as claimed.
You cannot sever the premise of the stop from the legitimacy of the
run that followed the stop. The coordinator's proposed "VOID with
violations labeled" is the right shape, but the C3 claim must be
struck from the record, not footnoted: a frozen gate may not stand
PASS on a false premise in a preserved historical record, or the
preservation itself becomes the certification.

Second, K1 and K6 "measurements from a voided run" are arithmetic
without information, and recording them as verdict lines invites
misreading. The redrafted section 7 proves enumeration costs a
minimum of 1134 primitive-action ticks, leaving at most 66 choice
ticks in a 1200-tick horizon; I-invent's 89 post-enumeration
selections against 399 sketches confirm the choice phase never
materialized. The run was therefore predestined to K7-VOID before
the first tick executed. What does 918 measure? The starvation
dynamics of an I arm that never finishes enumerating, not invention,
not choice. What does the K6 firing measure? That excluding
COMBINE-containing sketches from an agent that never gets to choose
anyway moves medians. These are true computations on real TSVs, and
the TSVs should be preserved, but entering "K1 KILL (measurement)"
and "K6 KILL (measurement)" as verdict lines in the wave record is
ceremony around a predetermined outcome. Future readers will cite
"I-survive median 918 < R 1200" with the void label quietly dropped;
the loop has seen exactly this failure mode before (old renders
re-certified and presented as new on 2026-09-23). The honest record
is: run executed, determinism confirmed, K7-VOID as predicted by the
redrafted bound, all bars uninformative. Numbers live in the TSVs;
no verdict line should exist, not even a parenthesized one.

Third, the znc slice claim in ITERATION1.md is unverified as written
and should not ride along in a preserved record unchallenged. The
worker claims a non-deterministic store smear where a single
pdat[0] = 16 corrupted indices 32, 35, 38, 41, 44. The red team built
three purpose-built probes and could not reproduce that pattern or
any non-determinism; the closest scenario was clean for 64- and
1024-element slices. What the red team did confirm is a different
signature: a deterministic index-32 read-back anomaly after
interleaved _zag_malloc, in the same bug family but not the claimed
one. The workaround (1024-element slices allocated up front) is
validated end to end by byte-identical reproduction, and that is
sufficient for the evidence. But the attributed cause, non-deterministic
smearing at exact indices, is unproven, and the original failing
probe was never committed, so no future worker can verify it. The
loop's own standard is that claims rest on committed evidence. Keep
the workaround; strike or downgrade the causal claim to UNPROVEN in
the preserved record.

Fourth, a content-stability wrinkle the order check does not cover:
milestone 3 (f26d510f3) edits e1c_agents.zag by 23 lines after
milestone 2 (9625c211a) committed it. The commit chain is strict, and
M5's letter (per-iteration commits before the next iteration) holds.
But the full experiment did not run on byte-identical agent sources
to the iteration-1 calibration commit, so "iteration 1" names two
slightly different agent sources: the calibrated one and the run
one. The red team reviewed the final sources and verified M3/M4 on
them, which contains the damage, but the preserved record should
label this explicitly: the calibration agents and the full-run
agents are not the same committed bytes.

The advocate is right that the worker's honesty is exemplary (K7
VOID, K4 CANNOT-CONFIRM, K5 INCOMPLETE, section-7 NOT-MET, no
retune shopping) and that everything except C3 verified. That is
precisely why the right verdict is VOID with the C3 claim struck,
the verdict lines removed, and the compiler claim downgraded: the
honesty deserves a record that is as clean as the worker's conduct,
not one that carries a repeated F10 and an unproven toolchain story
into the archive.

## M2. AGAINST a clean CONFIRM: the repair is asserted more than verified, and the coverage accounting leans on local-store freshness.

> "What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

New this wave: the full 55-entry execution on the repaired tree
(dbe397973), the enumeration manifest, the build-record files, and
the 55 per-entry evidence dirs. Inherited: the frozen battery
procedure, the pure-Zag harness source (byte-identical rebuild
a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66),
the pinned znc, the frozen expected outputs, and the standing
content-dependent UNTESTABLE cause for the two pull-head entries.
The numbers are not disputed: 55 data rows, 53 PASS, 2 UNTESTABLE,
44 distinct commit SHAs recomputed from this wave's own table
(independently verified). What is disputed is whether "the 1721pdt
FAIL is closed" is proven or merely asserted.

The 1721pdt FAIL was tree-content loss in a merge resolution at
f55e8c27a: 12 toolchain-dir files dropped. This wave tests a
different merge, fc1a43b8c, whose ancestor 37d1d3cab restored the
12 files. FORK_RESULTS_2021 verifies presence (git ls-tree shows
the files) and behavior (the tree probe compiles with the fork's
own znc and emits R32_ZNC_PROBE_OK). What it does not cite is a
per-file byte comparison of the 12 restored files against their
copies at 8929cdd93, the commit the repair claims to restore from.
"Restored verbatim" is asserted in the repair commit's prose and
repeated in the battery report; the battery's own evidence
establishes that 12 files exist and the probe works, not that they
are byte-identical to the pre-loss versions. For a battery whose
entire purpose is byte-level toolchain stability, that is the one
comparison that would close the incident with finality, and it is
missing. The judge should require it before entering "closed"
without qualification: the verdict can be CONFIRM on the 55 entries
as executed, with the 1721pdt FAIL marked closed-by-rerun and the
verbatim-restoration claim marked unverified-pending-sha-comparison.

Two further cautions. The mid-run local HEAD move (fc1a43b8c to
927b3f3f7 by another lane during the run) repeats the pattern
banked as an open question at 1721pdt: lane commits racing the
battery. Pinning made this instance inert, and the report discloses
it, but the pattern is structural and the judge should note that
each wave's "inert by pinning" is a per-instance claim, not a fix.
And the two former origin UNTESTABLEs became testable only because
the bedf8b4a object sat in the local store; no fetch is authorized,
so "live" origin coverage each wave depends on local-store
freshness, which the battery does not measure. The UNTESTABLE pair
(rh-pull-1-head, rh-pull-2-head) now stands at thirteen waves with
the identical content-dependent cause; the caveat is carried
correctly, but the effective coverage of the battery narrows each
wave these entries persist, and the headline count should keep
carrying the caveat, as the report does.

The hygiene rule itself is satisfied: 44 unique commits recomputed
from this wave's table, and my independent recomputation agrees.
That is the rule working as designed.

## M3. AGAINST reading FIT as more than process confirmation: the procedure is sound, the scope must stay literal.

> "What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

New this wave: the fresh re-run execution and its report
(927b3f3f7; evidence commit 78a8037fd). Inherited: the frozen probe
instruments, the R33 support sources, the canonical kb.txt and
gaz.txt, the three fixtures, the expected classes and output
hashes, the pinned toolchain, and the frozen procedure. The numbers
are not disputed: 2/2 byte-identical rebuilds, 30/30 specific
declines with 0 blanket refusals, 17/17 in-KB parity, 10/10 KB5
parity, 9/9 required rerun pairs byte-identical, all output hashes
matching prior records, 15/15 runs exit 0 with empty stderr, zero
Python.

The skeptic's case here is narrow because the evidence is strong,
and intellectual honesty requires saying so: the chain-diff over
80c40a7af..fc1a43b8c shows exactly one change (the additive
record-only SHA256SUMS file, pins matching frozen records) and
zero changes to any instrument source, fixture, kb.txt, gaz.txt,
R33 support, or the znc binary. The frozen-procedure reuse is sound
by design; with the chain paths untouched this wave, the reuse is
valid for this wave.

The skeptic's insistence is on the label, not the numbers. The
report's own caveats bound the reading: this certifies the 38-fact
closed-book probe chain only; the decline binary is a supervised
red-team probe instrument, not a general interactive TNN; the
traveling caveat (tnn_chat emits unflagged confabulations on
out-of-KB questions) persists verbatim from the 0521pdt survey.
FIT PASS must never migrate into any candidate claim or be read as
conversational competence. The proposed "[NEW, process confirmation]"
label is correct only if the judge holds it to process: it confirms
the chain still behaves, nothing more. One record-keeping note for
the judge: the FIT record spans two commits (evidence 78a8037fd per
the report, lane commit 927b3f3f7 per the slate); future citations
should use the evidence commit.

## M4. AGAINST taking the NULLs at face value without noting their structural limits.

> "What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

New this wave: the hunt report and the survey report (6062b4a94).
Inherited: the standing stand-downs, the QUEUED drafts, the 1121pdt
DISCARD, the frozen probe instruments, and Micah's frontier commits,
which enter only as read-only survey citations. The method, counts,
commit ids, and the nothing-manufactured statement are all present
as the advocate describes, and the 1721pdt forward bar is met. The
skeptic does not dispute the diligence. The skeptic disputes what
the NULLs can conclude.

On EXP2-K4: blocker reason 3 (the loop is barred from repurposing
Micah's closed fixtures) is governance, not technical feasibility.
Combined with blocker reason 2 (spec-blind curation is a human
collection protocol), the honest reading is that this corpus may
never be loop-collectable at all. HELD is the right entry this wave,
but the judge should note the lane risks becoming a permanent HELD
rather than a queued task; at some point the loop needs a different
design for K4 or a decision to retire the lane, and endless HELDs
should not be mistaken for progress toward collection.

On ruling 6: the dismissal of the one message-text hit is grounded
(RULING_KHA3_2026-09-27.md inside 57d055bbb records a
test-determined ruling on the K-HA-3 spec clause, not the
Python-mirror-adoption governance question), and HELD is correct.
The skeptic asks only that the judge confirm the HELD rests on that
distinction, since a future text search returning a differently
named ruling document could be misread the other way.

On trades: "no honest trade to name" is the right stand-down, and
the alternative (an invented expensive knob) would be
manufacturing, which the task forbids. But the lane's stated
dependency (truthfulness-under-adversarial-pressure measurement
depends on the EXP2-K4 corpus) chains the trades lane to the lane
above, which the skeptic has just argued may never be collectable.
The judge should flag the dependency: two HELDs leaning on each
other are one HELD with extra steps.

On the survey: the three new entry points are correctly fenced as
Micah's closed D2 new-learner frontier (9dbd01e26, 7979a55b1,
7f5a8ccdb), read-only, never built, run, certified, or re-judged.
The skeptic's watch-item is the provenance section's detailed
enumeration of his frontier commits: it is attributed and
read-only, which is within the survey mandate, but the judge should
keep watching the line between surveying his frontier and narrating
it as loop context. This wave stays on the right side.

## M5. AGAINST treating order-validity as content-validity, and FOR an explicit judge ruling on the new interpretive precedent.

> "What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

The ordering evidence is new this wave (fresh merge-base
verification: 8b456736b < d9e96ad91 < 9625c211a < f26d510f3 <
4750f1a19, strict, exactly one commit per interval, first
exp1c/src appearance at 9625c211a, addendum committed alone). The
ordering rule, the six rulings, the nine pairs, the DP-1 queue
status, and the frontier closures are inherited and untouched. The
skeptic does not dispute VALID, and with nothing adopted this wave
the check is indeed VACUOUS for adoption. The standing caveat
(commit order evidences commit order only, never run order) is
carried, which is good, because it is the crack the skeptic widens.

Commit order is not content stability. The milestone-3 edit of
e1c_agents.zag (23 lines changed after milestone 2 committed it)
means the chain's strictness certifies sequence, not that the
iteration-1 calibration and the full experiment ran the same agent
bytes. The red team reviewed the final sources, which contains the
damage for M3/M4 purposes, but the judge should enter explicitly
that VALID here means order-valid only, consistent with the carried
caveat.

The deeper point is precedent. The addendum installs two
interpretive readings that the frozen text does not state in so
many words: "K7 takes precedence over any K1 firing" and K1/K6 as
"measurements from a voided run" rather than kills or non-events.
The advocate's defense (restatement of frozen section 6) is
reasonable, and the skeptic does not claim the readings are wrong.
The skeptic claims they are new: the frozen text says "K3 or K7
failure means VOID" and "K7 is a validity gate, not a kill," from
which precedence follows, but no prior wave has entered the
"measurements from a voided run" category into the record, and
future waves will cite this wave for it. A reading that will be
cited as precedent should be confirmed by the judge explicitly,
with cited evidence, not settled by one wave's debate transcript.
The same applies to the K6 operationalization note (red-team R3):
excluding COMBINE-containing sketches differs narrowly from EXP1b's
A2 token replacement; it is recorded as a reasonable
operationalization, not a deviation, and nothing is adopted, so it
is moot this wave; but any future adoption must freeze the
operationalization first, and the judge should say so now.

On UNTOUCHED the skeptic finds nothing to dispute: the six
governance rulings appear only as OPEN, the nine sealed blind pairs
(R9, C1, C2v3, S11-IMG, C12, S11-AUD, S13, S14, whirlpool-planform)
only in untouched lists, DP-1 only as the parent agent's queue
decision, and the frontier dirs only in read-only survey. No wave
commit decides, relitigates, or re-presents any of them. The
addendum's redraft of frozen section 7 is the one item that even
approaches the governance line, and it was authorized by the
1721pdt debate's binding forward requirement, committed
pre-implementation, and changes no bar, gate, mechanism, horizon, or
bonus number. It stays on the right side, but only just, which is
why the judge's explicit confirmation matters.

---

# NOTES FOR THE JUDGE

Contested hardest, in the skeptic's ranking: (1) whether the C3
false premise is severable from the M5 stop decision or fatal to the
attempt's certification; (2) whether K1/K6 verdict lines may stand
even as "measurements" from a K7-voided, predestined run; (3) whether
the znc slice causal claim stays in the preserved record as stated
or is downgraded to UNPROVEN; (4) whether the "measurements from a
voided run" reading is confirmed as precedent or left as this
wave's gloss. The advocate and skeptic agree on: VOID as a test of
H1/H2, nothing adopted, M3/M4/determinism/pure-Zag verified, fork
battery numbers, FIT numbers, the NULL/HELD lane entries, the survey
verdict, commit-order validity with vacuous adoption, and the
UNTOUCHED lines.
