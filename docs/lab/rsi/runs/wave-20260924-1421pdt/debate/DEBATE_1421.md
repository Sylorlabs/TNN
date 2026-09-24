# DEBATE: wave-20260924-1421pdt

Convenor record. Four motions were debated. The advocate argued the most
favorable reading of each motion; the skeptic argued against. No final
rulings appear here; an independent judge rules from this transcript.
Each motion closes with AWAITING INDEPENDENT JUDGE.

Note on punctuation: this document follows the loop's no-em-dash style.

---

## M1: CV-1 decline-citation fix (cv1_cite)

Skeptic's provenance probe: "What is the provenance of the artifacts
under judgment, and what exactly is new versus inherited?"

Answer: no renders exist for this motion; the evidence is dialogue text
only. The 3 rule edits to the decline-construction rule are new this wave,
built on the adopted 1121pdt cv1.zag (diff: 78 changed lines, 3-word cap
removed, anyhit coverage flags added, best-fact selection removed, full
uncovered list cited, fail-closed and empty-uncovered fallback texts).
The KB (38 facts, sha 3ef27296), the frozen fixtures, the frozen
sentence template, and the answer path are inherited and byte-untouched.
The sealed 30 probes and key are new this wave: fresh content confirmed,
sealed shas 1ea86906d404861144264fca4fabcb14ec31a45b5a8fca47b3ad2beb32af61bb
and 8b4b6a89d99c262ad9af1d8b79c2b2011d4480fd38d7ab26e96c1cbfd15de115,
versus the 1121pdt sealed shas cf2f3293f0dd8fa23cbdaf07a5df95290f692af22c4dc1506636ce953b55db06
and 371cd2823f73ca64aaa8e0de8a12bf3834855a4eae03ccae1db4a12ee8f2992e.
No re-certified probe set; the mechanism is general, with no per-probe
branches and zero sealed probe words in the source diff.

### ADVOCATE (for the narrowest discard framing, most favorable to the candidate)

The killing numbers, CVC-B1 20/30 against >=24/30, CVC-B2 16/20 against
100 percent, CVC-B4 4/10 paraphrases answered, are all driven by the same
10 probes: P01, P03, P04, P05, P09, P10, A04, A06, G05, G09. Every one of
those 10 was intercepted by the frozen path-4 assertion handler and
returned NOTED., byte-identical to the frozen baseline's outputs on the
same probes (md5 e6478a2671d9f178e8c9e8402ebc3e22 for the 10 NOTED
lines; ce6198484b4429389d661fc0a525d684 across candidate, baseline, and
the 1121pdt binary on the two-probe NOTED test). They never reached the
decline-citation mechanism under test. That makes them untested inputs
under the frozen protocol, not evidence that the citation rule is wrong.
The verdict mapping says DISCARD on any FAIL, and the advocate does not
ask any bar to be moved; the point is only that the failure is located
in the probe set, not in the candidate, and the recommendation should
carry that location: discard the wave's verdict, keep the implementation
unchanged, re-author with an amended F9.

On the 20 probes that did reach path 5, the mechanism scored a perfect
20/20: 16/16 declines each name every key-listed payload word, 0 covered
words named (independent machine check: 92 unique quoted words, 0 found
in kb.txt case-insensitive whole-word), 4/4 paraphrase answers are the
cited facts verbatim, 0 confabulations, 0 false coverage claims, no
blanket refusals, the A02/martian class absent on all tested probes.
The ordered defects D1 and D2 are repaired where the mechanism ran.
CVC-B3 passes machine-checked; CVC-B5 passes 17/17 INKB byte-identical
(db6b707550865331666a2cf52d3c930a359c1d114ddf41f11a84656dbef4e7d5 for
both transcripts) plus 30/30 ADV-30 specific declines; CVC-B6 passes at
1.60x inside the 10x budget; CVC-B7 passes 3/3 byte-identical sealed
runs (md5 0c6fc375bfeb60a6f023c3384cd6005f) with zero RNG in any
decision path; CVC-B8 passes on substance with sealed shas matching
their pins and a clean B8-scope contamination grep. The causal root is a
probe-form defect traceable to an F9 spec gap: F9 never specified
interrogative form (PROBES.md contains zero "?" characters, confirmed by
grep), and the prereg's confound list never considered path-4
interception, its F9 guarantee having addressed the wrong failure mode
(the empty-uncovered fallback). The red-team itself reframes this as a
prereg-spec gap realized through literal F9 compliance, which means the
candidate is not implicated at all: the mechanism is general (78-line
diff, no sealed words, no per-probe branches) and the answer path is
byte-untouched.

On the Python contact: one accidental python3 -c computing the cost
ratio from two literal numbers typed on the command line. It touched no
wave artifact, read no file, wrote no file, and its output was not used
as evidence. The ratio stands on the committed op streams: 1338.07 /
833.90 = 1.6046, independently recomputed by the red-team. Under the
0521pdt prospective rule the operative condition is contact with an
artifact; there was none. The 1121pdt M5 precedent (accidental
python3 -c, no artifact touched, disclosure recorded, memo stood)
applies squarely. Ruling: no evidence void, disclosure adequate. The
cost number is independently reproducible from committed artifacts.

On the B8 sentence correction: the EVIDENCE section 5 sentence "grep
over impl/ for 16 sealed-distinctive words ... 0 hits" is false as
written (hits exist in runs/adv30.txt, runs/cand_adv30.txt,
runs/qmark.txt, runs/named_words.txt, and EVIDENCE_CV1_CITE.md itself).
But those are training inputs and scoring transcripts, not mechanism
artifacts, and CVC-B8's frozen scope (cv1c.zag, gate_op.zag,
R33_NATIVE_IO_V1.zag, R33_NATIVE_SHA256_V2.zag, runs/kb.txt,
runs/gaz.txt) returns 0 hits on the same 16-word list. So B8 stands on
its frozen terms; what needs correction is one evidence sentence,
narrowed to the B8 scope. That is an evidence-accuracy defect, not a
seal breach, and the correction is a documentation edit, not a verdict
change.

### SKEPTIC (against)

Start with the mapping, because the advocate's "untested inputs"
framing is exactly the move the frozen mapping was built to forbid.
ADOPT iff CVC-B1 through CVC-B8 all PASS; any FAIL means DISCARD. The
grading rules define precisely what a miss is, and a NOTED. on a sealed
paraphrase probe that the key expects answered is a miss, full stop.
Calling the 10 misses "untestable" is a post-hoc re-framing that no
frozen bar authorizes. The red-team itself says the "unevaluable" frame
is wrong: it would imply the mapping should not fire, but it does and
it did. The 10 probes are real misses, and DISCARD is the only
verdict the mapping permits. The advocate concedes this; the only
honest debate is about attribution and the next-wave recommendation,
and there the skeptic has four objections.

First, the 20/20 conditional number is selection-biased and must not be
promoted. The 20 probes that reached path 5 are exactly the
non-assertion-pattern probes: a non-random subset defined by the same
frozen routing rule that produced the misses. "Mechanism vindicated" is
accurate only in that conditional sense, as the red-team states. The
advocate's gloss, "the mechanism repairs both ordered defects where it
ran," is true and also nearly vacuous: where it ran is where the frozen
router let it run. The next wave's fresh set, if properly authored to
reach path 5, tests a claim this wave cannot establish.

Second, the F9 fix debate. The worker recommended amending F9 to require
interrogative ("?") forms. The red-team demonstrated this is
insufficient: runs/noted2.txt contains two interrogative-form probes
with assertion-pattern fragments plus gazetteer entities, and both still
route to NOTED. Interrogative form is necessary but not sufficient.
Routing is frozen extract_assert pattern matching plus gazetteer entity
matching: A01 has " was written by " but reached path 5 because
"bradbury" is not a gazetteer entity. So the F9 amendment must require
interrogative forms AND exclude frozen assertion-pattern fragments with
gazetteer entities. The skeptic goes further: the probe author must then
be told which frozen patterns and which gazetteer entities to avoid,
which is knowledge of the implementation's frozen routing internals
flowing into probe authoring, a leakage-shaped coupling even if it is
frozen-to-frozen. The prereg's confound list (items 1 through 8) never
considered this, so the next prereg must state explicitly what routing
knowledge the author may use, or the "separation" is cosmetic. Note also
that A01 reaching path 5 on the strength of "bradbury" not being a
gazetteer entity is an undocumented coupling the frozen protocol never
pinned; the bars' evaluability depends on a gazetteer whose membership
was never frozen as a probe-reachability condition.

Third, the Python ruling is correct on precedent but the skeptic
dissents on the margin of comfort. The EVIDENCE does not record the awk
command that produced 1338.07 and 833.90; the red-team calls the
committed op streams "sufficient," and they are, but sufficiency of the
streams is exactly what the missing command should have established in
the primary record rather than in review. More importantly, the
undocumented diagnostics runs/qmark.txt and runs/noted2.txt were
committed in the implementation commit, never mentioned in EVIDENCE or
VERDICT, and qmark.txt contains sealed probe verbatims (P01, A01).
Post-build timestamps (21:57 to 21:58, after the 21:55 binary build and
the 21:52 seal) plus the clean source diff exonerate pre-implementation
contamination, and the red-team used these very files to confirm the
root-cause story. But combine them with the blank SEAL.md seal-open log
(still reading "to be filled at scoring time" when CVC-B8 asks for the
seal-open to be logged by commit hash) and you get a record that is not
fully auditable: sealed verbatims in an undocumented file plus a blank
seal log is precisely the pattern a breach would resemble if the
timestamps were ever disputed. Next wave must fill the seal-open log at
scoring time and document every diagnostic input and output, or the
author/implementer separation attestation stays partially asserted
rather than demonstrated.

Fourth, the B8 sentence correction understates the damage. The false
sentence is in the evidence document's contamination section, the one
place a reader looks for the seal story. The training/sealed topical
overlap ("mona lisa"/"da vinci" in adv30.txt line 3 vs sealed A05/G07;
"cipher" in adv30.txt line 33 vs sealed A07/G05) is topical overlap, not
leakage, and CVC-B5 is a no-regression battery so its result stands; but
it weakens the training-battery independence narrative, and the false
"0 hits" sentence sat on top of that. The correction must be committed,
not noted: narrow the sentence to the B8 scope and state the hits in
training inputs and transcripts plainly. Evidence-quality defects that
survive into the record become the next wave's assumptions.

On the contested framing question, probe-defect versus prereg-gap: the
skeptic says the distinction is verdict-irrelevant and
recommendation-critical. It is verdict-irrelevant because the mapping
fired on real misses. It is recommendation-critical because "the author
slipped" recommends retraining the author while "the spec never
specified interrogative form and never considered path-4 interception"
recommends amending the spec; the red-team's amendment (a) says it is
both, a spec gap realized through literal compliance. The skeptic
accepts that composite but insists the spec-gap half carries the weight:
F9 was written to defeat the old first-3 cap and the tie-break traps,
and it succeeded at that while being blind to the router. The bars
frozen on top of that blindness were testing the probe set's form as
much as the candidate's mechanism.

AWAITING INDEPENDENT JUDGE

---

## M2: G1 sunshafts re-freeze (g1_v2)

Skeptic's provenance probe: "What is the provenance of the artifacts
under judgment, and what exactly is new versus inherited?"

Answer: the variant BMPs are new renders this wave (sha
8076028d9031618544c6986dc6c4ddd12408add53afdf82dac7801c14b8c3bea,
3/3 byte-identical), rendered by the new g1_sunshafts_v2.zag pass
compiled with the pinned znc (498abcb5). The r8c substrate
(r8c_alien.zag, Fork C mind's-eye elaboration) is inherited, and the
baseline was rebuilt byte-identical to the S14 record
(e4f6555700ad6983e323177573ea66cb0a16c5d121a7b32a34fff5735afecb0d),
so no substrate substitution. The march/transmittance machinery is
inherited unchanged from 1121pdt; the new mechanism content this wave
is the recalibrated T-gate procedure (measured mean_T=569, std_T=92,
gate=707) and the sun position S=(110,300) with the runtime geometric
validator. The point sets are the frozen re-freeze sets, not the 1121pdt
defective ones. No sealed pair was prepared, and no JUDGE_BRIEF.md
exists; nothing enters the judge queue. Prior judge-queue items R9,
C1, C2v3, S11-IMG, C12, S11-AUD, S13, S14, and whirlpool-planform are
untouched and listed QUEUED-UNJUDGED.

### ADVOCATE (for the narrowest discard framing, most favorable to the candidate)

Both 1121pdt defects were repaired and the repairs held. The geometric
validator passes every frozen check: V1 sun 76px above the horizon
(margin >= 40 required), V2 sun tier_at == 0, V3/V4/V5 every kept
WEDGE/OFFWEDGE/RADCUT point tier_at == 0, V6 keep counts 39/48/64/24
against asserts 36/36/56/16, with the runner diffing validator and
verifier *_KEPT lines and requiring them identical, which they were.
The red-team independently re-derived the wedge set in awk from the
frozen formula and got 39 kept with exactly the prereg's drop accounting
(5 out of frame left, 2 out of frame right, 2 inside the giant disc),
so the validator is not certifying itself. The T-gate recalibration ran
per the frozen procedure on the rebuilt baseline: mean_T=569,
std_T=92, gate=707, and the arithmetic checks (569 + 92 + 46 = 707).
The broad sky wash is gone: 3651 of 325786 sky pixels lifted, about
1.1 percent, versus 97.14 percent at the hardcoded gate 400 in 1121pdt,
and full-frame off-wedge mean|dL| is 0.00. KB1 passes (3/3
byte-identical 8076028d); KB4/KB5/KB6/KB7 pass; KB8 passes at 2.04x
against a 3x budget (1948ms avg vs 957ms baseline, budget 2871ms).
Commit order is clean: prereg commit 1d8d40013 strictly first,
implementation commit 782dbb228 second, with 1d8d40013 an ancestor, and
git log on the g1_v2 path shows exactly one commit. No Python contact
anywhere; static checks pass; toolchain and vendored IO shas match
their frozen pins.

The killing evidence, KB2 = 1.0000 against >= 1.12 and KB3 = 0.00
against >= 60.0, is a genuine mechanism miss, not a freeze defect and
not unpassable-by-construction. Not a freeze defect: both 1121pdt
defects were repaired, the repairs held, and the bars were fully
evaluable this wave. Not unpassable-by-construction: the wedge fan
radiates from the sun along six rays with all kept points verified in
sky; a mechanism that actually lifted fan-shaped shafts would register
on those points, so the bars were genuinely at risk. The red-team
recomputed the killing evidence from the BMP bytes: 0/39 wedge points
have nonzero dL, the sun point itself has dL = 0, and the lifted pixels
form one small blob (2238 px with nonzero dL, max dL 9, bbox x 888..1023
y 254..305, centroid 984.5,278.3) that intersects no wedge ray: the
shallowest wedge ray (slope -1/4) passes through y ~ 72..106 at the
blob's x-range while the blob sits at y 254..305. The frozen shaft
detector correctly reported nothing. The worker's mechanism reading is
consistent with the artifacts: the march-mean transmittance rewards
long line-of-sight alignments through low-density corridors far from
the sun, not fan-shaped shafts radiating from it. The 1413 above-gate
pixels that quantize to L=0 under integer math are real disclosed
behavior, not a hidden wash; every nonzero-dL pixel sits inside the
reported blob bbox, so KB4/KB5 hold at 0.00 honestly.

This is what a re-freeze is supposed to produce when the mechanism is
wrong: clean evaluability, a decisive kill, and new knowledge. The
wave's information value is high: it proved the march-mean
transmittance formulation cannot produce fan shafts (its signal lands
~870px from the sun, anti-correlated with the target), and it produced
the structural hypothesis queued next, a minimum-D line-of-sight
formulation that would concentrate the signal near the sun. The
red-team ruled that note appropriate as a queued-next hypothesis: not
implemented, not tested, not used to adjust any constant, bar, or
verdict this wave, and any future shaft work must go under a fresh
prereg. Nothing was smuggled. DISCARD with the candidate blameless on
process is the right verdict, and the bars were never weakened,
narrowed, or re-interpreted to force a pass.

### SKEPTIC (against)

The advocate's "genuinely at risk" claim needs pressure, because the
numbers describe a near-total miss with an uncomfortable confound. KB2
is exactly 1.0000 and KB3 exactly 0.00: not a single one of 39 wedge
points moved, and the sun point itself has dL = 0 (L=95 both). The lift
that exists is a faint blob at the frame edge, max +9 luma, ~870px from
the sun. The skeptic's charge: the march-mean formulation is not a
shaft mechanism that fell short; it is anti-correlated with shafts by
construction, since T = mean(1024-D) over the full pixel-to-sun segment
makes far pixels' T an average over long paths, so high-T pixels sit
far from the sun where paths align with corridors. The advocate calls
this "new knowledge," and it is, but it is knowledge the 1121pdt
evidence already foreshadowed: the 1121pdt INFO values (KB2 info 1.2644,
KB3 info 197.15 over the broken point sets) measured the same
march-mean machinery, and the wash finding (97.14 percent lifted) showed
the field mean behavior. Two waves have now been spent on the internals
of this mechanism while the loop's standing mandate is big levers on
realism, and while Micah's actual frontier is the PAMs v2 deep dive and
the b_alpha v9 rebuild. The "queued next" min-D hypothesis is a third
wave's worth of mechanism iteration on the same played-out substrate
unless the coordinator deliberately decides otherwise.

On the gate confound: the frozen rationale said mean + 1.5 sigma lifts
"about 7 percent of sky pixels" under approximate normality. The field
is not normal: the T distribution's upper tail is thin (march-means
regress hard), so the gate catches only 1.1 percent and even the max
lift is +9 luma. The advocate treats the gate as validated because the
wash is gone; the skeptic treats it as an unvalidated modeling
assumption frozen into the prereg. The skeptic's sharper point: with
max lift +9 across 2238 of 325786 pixels, KB2 >= 1.12 on wedge means
was near-impossible regardless of where the lift landed, so was the bar
"at risk" in any meaningful sense, or did the gate choice nearly
vacuous the kill bars while the mechanism miss finished the job? The
red-team notes a lower multiple would lift more, but nothing in the
frozen evidence suggests the lift would then fall on the sun fan rather
than on far-field alignments; the skeptic agrees with that and adds
that the prereg therefore froze two coupled unknowns (gate multiple and
mechanism geometry) and the wave killed both at once, which is fine for
a verdict but weak for attribution. The worker's red-team note 2
concedes the overshoot; the next prereg, if there is one, should
measure the field's actual T distribution before freezing a sigma
multiple.

On the fan design: the red-team's observation that all six wedge rays
have dy = -1, sampling only upward-going rays from the sun (135 degrees
up-left through 14 degrees above horizontal-right), with no ray sampling
near-horizontal rightward or downward directions, is a design choice
under the frozen prereg, not a defect. The skeptic notes it anyway
because it constrains what any future mechanism must satisfy: the
"genuinely at risk" claim is scoped to the upward fan, and a mechanism
that produced correct downward shafts would still read 1.0000 here.
That is the prereg's choice and it was frozen, but it should be an
explicit design decision in the next prereg, not an inherited accident.

On cost and safety: KB8 at 2.04x wall-clock passes, but it is wall
clock, not the op-count discipline used on the dialogue side; and the
safety numbers (KB4/KB5 0.00, KB6 1.0000, no dropouts, E3 honored) are
real but they are the consolation of a mechanism that moved almost
nothing. A mechanism that cannot lift the fan cannot break the terrain
either; the passes are evidence of a near-null, not of restraint.

AWAITING INDEPENDENT JUDGE

---

## M3: Fork battery (19/19 PASS)

Skeptic's provenance probe: "What is the provenance of the artifacts
under judgment, and what exactly is new versus inherited?"

Answer: a process confirmation, not a candidate. No new candidate
artifacts are under judgment. The battery tests the pinned znc binary
(sha 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef)
as carried by each enumerated fork, plus the frozen shell driver and
the pure-Zag harness rebuilt from the 2321pdt archive source
(f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738;
rebuilt binary byte-identical to last wave's a2e6284c...). Everything
under test is inherited: the toolchain, the harness, the probe
(znc_probe.zag sha 3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919
identical on every fork). What is new this wave is the observation
itself: 19/19 forks tested at their current commits, including the
moved origin/tnn-native-lab tip 9d4f484bfe, tested read-only.

### ADVOCATE (for the confirmation being solid)

19/19 forks PASS on both the shell battery and the pure-Zag harness,
which agree everywhere. Every fork's znc is byte-identical to the
pinned 498abcb5 sha; znc_probe.zag is the identical sha on every fork.
The battery is genuinely discriminating: NEG1 (unterminated string)
fails compile and check with exit 1 on all 19; NEG2 (wrong-output
program) compiles but fails the byte-compare on all 19; zero
CANNOT-CONFIRM anywhere. The method is clean and read-only: `git fetch
origin` observed the remote tip; the five non-tracking remote heads
were fetched into FETCH_HEAD only and extracted via `git show
FETCH_HEAD:<path>`; nothing was checked out, no local ref created or
updated, no merge, no reset, no push. The seven forktest/* detached
worktrees were tested read-only from scratch copies and all passed on
both drivers, which is better than 1121pdt, where the worker marked
them ABSENT and the coordinator had to test them after. The harness
build is deterministic: rebuilt from the archive source, byte-identical
to last wave's harness binary (a2e6284c...). The one anomaly found, the
working-copy znc mode 754 versus 100755 recorded in the index, is
mode-only drift with zero byte drift. No Python was invoked at any
point; scratch lived under ~/workspace, never /tmp. This is a solid,
discriminating, read-only confirmation that the pinned toolchain is
uniform across the whole fork tree at this wave's commits.

### SKEPTIC (against)

The 19/19 number is real but the wave's ground moved under the
battery. origin/tnn-native-lab moved twice mid-wave: the pre-wave
remote-tracking ref was e1f78ba35, the first fetch brought ad7919c25
("PAM RT-X: build sources for battery B-3034-X..."), and a follow-up
fetch minutes later brought 9d4f484bfe ("CRITIC 4: fix doubled
path ..."), which was stable across re-checks. The battery tested
9d4f484bfe, the final tip, read-only. But local HEAD also moved by
concurrent worker commits during the run: the brief pinned 28088d207
while the working copy tested at ef6801b3, with 28088d207 an ancestor.
So the battery's "working copy" result attaches to a HEAD that no
longer exists, and the local branch is behind the remote tip with the
merge explicitly left to the coordinator. A toolchain-identity battery
is robust to most of this, byte-identical is byte-identical, but the
skeptic's point is that the wave's concurrency discipline is loose:
two moving tips and a moved HEAD in one wave, and the evidence doc
itself flags the ordering rather than resolving it.

Coverage has a real hole: three extra detached worktrees exist at
~/workspace/tnn-rsi-wave3/ (probe, senses, trades, all at bd3097874),
not in the brief, not tested. The runner flagged them for the
coordinator, which is honest, but they are exactly the kind of place an
untested znc could hide, and "flagged for the coordinator" is not
coverage. The skeptic also notes what the battery does not test: it
tests toolchain identity, not wave artifacts. A 19/19 PASS says every
fork carries the pinned znc; it says nothing about the cv1_cite or
g1_v2 evidence, which is correct scoping but should not be read as a
blanket wave-health number. The mode drift (754 worktree vs 100755
index) is benign this wave, but it is the second wave in a row with
mode drift on the znc binary (last wave: 100755 worktree vs 100644
committed), which suggests the file's handling is sloppy even if its
bytes are stable.

AWAITING INDEPENDENT JUDGE

---

## M4: tnn_chat FIT (FIT)

Skeptic's provenance probe: "What is the provenance of the artifacts
under judgment, and what exactly is new versus inherited?"

Answer: a process confirmation, not a candidate. No new candidate
artifacts are under judgment. The binaries under test are rebuilds of
inherited sources pulled read-only from the wave archive: baseline
tnn_chat.zag (c0776ad6..., from the 0834pdt run) and decline
tnn_chat_decline.zag (a87011fe..., from the 1121pdt run), with the
vendored R33_NATIVE_IO_V1.zag (e6379ddb...) and
R33_NATIVE_SHA256_V2.zag (9824f6db...); all four source shas verified
against the prior wave's recorded values before building. The fixtures
are the canonical HEAD kb.txt (3ef27296) and gaz.txt (b75fd113), and
the frozen probe fixtures from the 1121pdt archive. What is new this
wave is the observation on merged HEAD 28088d207 (a merge of
origin/tnn-native-lab e1f78ba35, roughly 2992 files and 470300
insertions of V-NOLIMIT teach sources and evidence): the rebuilt
binaries are byte-identical to the 1121pdt records, so the merge
introduced no FIT-relevant change.

### ADVOCATE (for the confirmation being solid)

FIT on the merged HEAD 28088d207 with zero deviation. Binary
reproducibility 2/2: the decline binary rebuilds to
20273a99215680b5e3e42bbdbbfed105c7109d15ba189c903cf0d88db54418e7 and
the baseline to 1ada2fae63ddd63d37f06705459c0d8b1d9c8dffc859af25949221bf5895749c,
both byte-identical to the 1121pdt records, so the e1f78ba35 merge,
roughly 2992 files and 470300 insertions, introduced no FIT-relevant
change. The merge did not touch the FIT instrument chain: pinned
toolchain sha unchanged, all four probe source shas verified against
the prior wave's recorded values before building, fixture shas
unchanged. Probe results: KB1 30/30 specific declines on each of 3
runs (26 "My knowledge base contains nothing about ..." turns plus 4
"No knowledge-base fact connects/covers ..." turns, 0 blanket
refusals), run 1 output sha a2ca4dd7dd64018e2ce9fd1ca78111928f73e818b9ec6b6738cd6be04ee85308
byte-identical to the prior wave's recorded kb1_out30_r1.txt; KB2
17/17 in-KB turns answered with 0 declines, byte-identical baseline
parity across 3 runs each; KB5 10/10 in-KB answers, 0 declines,
byte-identical baseline parity across 3 runs each; rerun determinism
9/9 run-pairs byte-identical by cmp. No Python anywhere in the work;
nothing pushed to GitHub. The traveling caveats are stated plainly:
the instrument is a 38-fact closed-book probe, not a general
interactive TNN, and no live interactive TNN exists on this branch.
This is a clean re-verification that a large merge left the dialogue
instrument chain untouched.

### SKEPTIC (against)

The numbers are all real and the skeptic does not dispute a single
sha; the dispute is about what FIT can and cannot see. The instrument
is a 38-fact closed-book probe with frozen fixtures: it re-verifies
that the decline gate still declines the same 30 adversarial turns and
answers the same 17 in-KB turns. A 2992-file, 470300-insertion merge
of V-NOLIMIT teach sources and evidence could touch a great deal that
this instrument cannot observe; FIT passing means the instrument chain
is unchanged, not that the merge is safe in any broader sense. The
advocate's "the merge did not touch the FIT instrument chain" is the
correct, narrow claim; anything broader is promotion. The skeptic also
notes the merge under test is pinned to 28088d207 while the wave's
local HEAD kept moving under concurrent worker commits (the fork
battery tested at ef6801b3); the FIT statement is tied to a specific
merge commit, and any later local commit is outside its scope. The
caveats are carried honestly (closed-book instrument, no live
interactive TNN), and the skeptic's only addition is that the FIT
verdict's scope should be read literally: it re-certifies the probe
instrument, nothing more, and the coordinator should not let a FIT
green light stand in for merge review of 470300 insertions.

AWAITING INDEPENDENT JUDGE

---

Convenor close: four motions debated, provenance probe answered in
each, no rulings rendered. Transcript committed under
docs/lab/rsi/runs/wave-20260924-1421pdt/debate/DEBATE_1421.md.
AWAITING INDEPENDENT JUDGE.
