# INDEPENDENT JUDGMENT: wave-20260924-1421pdt

Role: independent judge. I implemented nothing, red-teamed nothing, and
debated nothing this wave. Each motion was decided from the frozen
prereg, the worker verdict, the red-team review, and the advocate/skeptic
transcript. A debate overturns a worker verdict only on cited evidence,
never on rhetoric. No frozen bar was weakened to force a pass.

Note on punctuation: this document follows the loop's no-em-dash style.

---

## M1: CV-1 decline-citation fix (cv1_cite)

### Ruling: CONFIRM DISCARD

Numbers: CVC-B1 20/30 against bar >= 24/30 FAIL; CVC-B2 16/20 against
bar 100 percent FAIL; CVC-B3 PASS; CVC-B4 4/10 paraphrases answered,
FAIL; CVC-B5 PASS; CVC-B6 1.6046x against 10x PASS; CVC-B7 3/3
byte-identical PASS; CVC-B8 PASS on substance. The frozen verdict mapping
is unambiguous: ADOPT iff CVC-B1 through CVC-B8 all PASS; any FAIL means
DISCARD. Three bars fail. The advocate concedes the mapping fires. The
verdict stands as recorded.

(a) Verdict: DISCARD confirmed. The 10 misses (P01, P03, P04, P05, P09,
P10, A04, A06, G05, G09) are real misses under the frozen grading rules:
each is a sealed probe whose key expects a decline or an answer, and the
candidate returned NOTED. The red-team is right that the "unevaluable"
frame is wrong: it would imply the mapping should not fire, and it does
and it did. DISCARD is the only verdict the frozen mapping permits.

(b) Framing: BOTH probe-form defect AND prereg-spec gap, with the weight
on the spec gap, as the red-team's amendment (a) states. F9 never
specified interrogative form (PROBES.md contains zero "?" characters,
confirmed by grep), and the prereg's confound list (items 1 through 8)
never considered path-4 interception; its F9 guarantee addressed the
empty-uncovered fallback, the wrong failure mode. The misses are a
prereg-spec gap realized through the probe author's literal F9
compliance. The refined routing cause is frozen extract_assert pattern
matching plus gazetteer entity matching, not mere "?"-absence: the
noted2 runs show two interrogative-form probes with assertion fragments
still routing to NOTED, and A01 (" was written by " with "bradbury" not
a gazetteer entity) reached path 5 and passed. The verdict is unchanged
by the framing; the framing governs only the next-wave recommendation.

(c) The conditional 20/20: must stay STRICTLY CONDITIONAL. The 20 probes
that reached path 5 are exactly the non-assertion-pattern probes: a
non-random subset defined by the frozen router that produced the misses.
"Mechanism vindicated" is accurate only in that conditional sense. The
numbers are real and useful (16/16 declines name every key-listed payload
word; independent machine check: 92 unique quoted words, 0 found in
kb.txt case-insensitive whole-word; 4/4 paraphrase answers are the cited
facts verbatim; 0 confabulations; 0 false coverage claims), but they may
not be promoted to a bar pass or cited as vindication. Their proper use:
they support re-running this unchanged implementation against a fresh,
properly authored sealed set as a new evaluation, not a continuation.

(d) The F9 fix: requiring "?" is necessary but NOT sufficient, per the
noted2 finding. The next wave's F9 must require interrogative forms AND
exclude frozen assertion-pattern fragments with gazetteer entities. On
the skeptic's leak objection: it is sustained. The probe author must be
told which frozen patterns and which gazetteer entities to avoid, which
is knowledge of the implementation's frozen routing internals flowing
into probe authoring, a leakage-shaped coupling even if frozen-to-frozen.
The next prereg must state explicitly what routing knowledge the probe
author may use, or the author/implementer separation is cosmetic. It
must also pin gazetteer membership as a probe-reachability condition,
since the bars' evaluability depends on it (A01's path-5 reach was an
undocumented coupling the frozen protocol never pinned).

(e) The Python contact: NO evidence void. One accidental `python3 -c`
computing the cost ratio from two literal numbers typed on the command
line. It touched no wave artifact, read no file, wrote no file, and its
output was not used as evidence. The ratio stands on the committed op
streams: 1338.07 / 833.90 = 1.6046, independently recomputed by the
red-team. Under the 0521pdt prospective rule the operative condition is
contact with an artifact; there was none. The 1121pdt M5 precedent
(accidental python3 -c, no artifact touched, disclosure recorded, memo
stood) applies squarely. The disclosure is adequate; the cost number is
independently reproducible from committed artifacts. Nit carried: the
EVIDENCE does not record the awk command that produced 1338.07 and
833.90; the committed op streams are sufficient, but next wave should
record the derivation command in the primary record.

(f) Evidence-quality findings: verdict-changing? NO. But three record
corrections are REQUIRED:

1. The false-as-written EVIDENCE section 5 sentence ("grep over impl/
   for 16 sealed-distinctive words ... 0 hits"). Hits exist in
   runs/adv30.txt, runs/cand_adv30.txt, runs/qmark.txt,
   runs/named_words.txt, and EVIDENCE_CV1_CITE.md itself. These are
   training inputs and scoring transcripts, not mechanism artifacts.
   CVC-B8's frozen scope (cv1c.zag, gate_op.zag, R33_NATIVE_IO_V1.zag,
   R33_NATIVE_SHA256_V2.zag, runs/kb.txt, runs/gaz.txt) is independently
   clean, so CVC-B8 stands on its frozen terms. The sentence must be
   corrected to the B8 scope, with the training/transcript hits stated
   plainly. The training/sealed topical overlap ("mona lisa"/"da vinci"
   adv30.txt line 3 vs sealed A05/G07; "cipher" line 33 vs sealed A07/G05)
   is topical overlap, not leakage; CVC-B5 is a no-regression battery
   and its result stands; the independence narrative is slightly
   weakened and must be recorded as such.
2. The undocumented diagnostics runs/qmark.txt and runs/noted2.txt must
   be documented in the record as post-build diagnostics with their
   timestamps (21:57 to 21:58, after the 21:55 binary build and the 21:52
   seal) and the exonerating facts: the clean source diff (78 changed
   lines, zero sealed probe words, no per-probe branches) plus the
   red-team's use of these very files to confirm the root-cause story.
   Sealed verbatims in an undocumented file is the pattern a breach
   would resemble; the timestamps plus the clean diff are what
   exonerate, and both must be in the primary record.
3. The blank seal-open log in SEAL.md (still reading "to be filled at
   scoring time" when CVC-B8 asks for the seal-open to be logged by
   commit hash) is a process defect. Fill it retroactively by commit
   hash if the scoring commit is attestable; otherwise record it as a
   process defect with a requirement that the next wave fill the log at
   scoring time and document every diagnostic input and output, so the
   author/implementer separation attestation is demonstrated, not
   asserted.

---

## M2: G1 sunshafts re-freeze (g1_v2)

### Ruling: CONFIRM DISCARD

Numbers: KB2 shaft ratio 1.0000 against bar >= 1.12 FAIL; KB3 shaft
variance 0.00 against bar >= 60.0 FAIL; all other bars PASS (KB1 3/3
byte-identical 8076028d9031618544c6986dc6c4ddd12408add53afdf82dac7801c14b8c3bea;
KB4 0.00; KB5 0.00; KB6 1.0000; KB7 0; KB8 2.04x against 3x).
Baseline rebuilt byte-identical to the S14 record
(e4f6555700ad6983e323177573ea66cb0a16c5d121a7b32a34fff5735afecb0d), so no
substrate substitution. Validator V1 through V6 all PASS (sun margin 76
against 40 required; keep counts 39/48/64/24 against asserts
36/36/56/16), independently re-derived by the red-team in awk (39 kept,
drop accounting exactly as the prereg stated). T-gate recalibration ran
per the frozen procedure: mean_T=569, std_T=92, gate=707
(569 + 92 + 46 = 707); wash down from 97.14 percent to about 1.1 percent
(3651 of 325786 sky pixels lifted). Commit order clean: prereg commit
1d8d40013 strictly first and an ancestor of implementation commit
782dbb228; exactly one commit touches the g1_v2 path. The frozen
mapping (validator pass AND KB1..KB8 all pass, else DISCARD) fires.
DISCARD confirmed.

(a) Verdict: DISCARD, and the bars were never weakened, narrowed, or
re-interpreted: KB2 >= 1.12, KB3 >= 60.0, and all other thresholds match
the prereg freeze exactly. No Python contact anywhere; toolchain and
vendored IO shas match their frozen pins; the 1413 above-gate pixels
that quantize to L=0 under integer math are real disclosed behavior,
not a hidden wash.

(b) Attribution: MECHANISM MISS, not a freeze defect and not
unpassable-by-construction. Both 1121pdt defects were repaired and the
repairs held; the bars were fully evaluable this wave. Not unpassable
by construction: the wedge fan radiates from the sun along six rays,
all 39 kept points verified in sky; a mechanism that actually lifted
fan-shaped shafts would register on those points. The red-team's
independent recompute from the BMP bytes is decisive: 0/39 wedge points
with nonzero dL, dL = 0 at the sun point (110,300) itself, and the lift
sits in one small blob (2238 px with nonzero dL, max +9 luma, bbox
x 888..1023 y 254..305, centroid 984.5,278.3, about 870px from the sun)
that intersects no wedge ray (the shallowest wedge ray, slope -1/4,
passes through y ~ 72..106 at the blob's x-range while the blob sits at
y 254..305). The worker's mechanism reading is consistent with the
artifacts: the march-mean transmittance rewards long line-of-sight
alignments through low-density corridors far from the sun, not
fan-shaped shafts radiating from it. The frozen shaft detector correctly
reported nothing.

(c) The skeptic's "genuinely at risk" objection: partially sustained as
an attribution caveat, not as a verdict-changer. The bars were genuinely
evaluable this wave, which is what the kill needs; the mechanism's
structural anti-correlation with the fan is independently established,
so the kill does not rest on the gate choice alone. But the skeptic is
right that the frozen gate multiple was an unvalidated modeling
assumption: the 1.5-sigma rationale assumed approximate normality the T
field lacks, the upper tail is thin (march-means regress hard), the
realized lift is 1.1 percent rather than the ~7 percent the rationale
promised, and max lift +9 made KB2 >= 1.12 very hard under the realized
field. The prereg froze two coupled unknowns (gate multiple and
mechanism geometry) and the wave killed both at once, which is fine for
the verdict but weak for attribution: a stronger gate would have lifted
more far-field alignments, not the sun fan, per the red-team's note.
This wave's information value is real (it proved the march-mean
formulation cannot produce fan shafts), and the kill is decisive, but
the next prereg, if any shaft wave is authorized, must measure the
actual T field distribution before freezing a sigma multiple, and must
decouple gate choice from mechanism geometry. The red-team's fan-design
observation is also carried: all six wedge rays have dy = -1 (upward
fan only, 135 degrees up-left through 14 degrees above horizontal-right);
a frozen design choice, not a defect, but the next prereg should make
direction coverage an explicit design decision, not an inherited
accident.

(d) The queued-next min-D line-of-sight note: APPROPRIATE. It was not
implemented, not tested, and not used to adjust any constant, bar, or
verdict this wave. Nothing was smuggled. Any future shaft work must go
under a fresh prereg with its own frozen bars and its own geometric
validation. As a queued-next hypothesis for the coordinator it is
legitimate.

---

## M3: Fork battery

### Ruling: CONFIRM PASS

Numbers: 19/19 forks PASS on both the frozen shell battery and the
pure-Zag harness, which agree everywhere. Every fork's znc is
byte-identical to the pinned sha
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef;
znc_probe.zag is the identical sha
3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919 on every
fork. The battery is genuinely discriminating: NEG1 (unterminated
string) fails compile and check with exit 1 on all 19; NEG2
(wrong-output program) compiles but fails the byte-compare on all 19;
zero CANNOT-CONFIRM anywhere. The harness build is deterministic:
rebuilt from the 2321pdt archive source (f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738),
byte-identical to last wave's harness (a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66).
Method was read-only throughout (fetch only; five non-tracking remote
heads extracted via git show from FETCH_HEAD; no checkout, no merge, no
reset, no push; seven forktest/* worktrees tested read-only). No Python
invoked anywhere; scratch under ~/workspace, never /tmp. This is a
solid toolchain-identity confirmation at this wave's commits.

On the skeptic's objections:

1. The remote tip moved twice mid-wave (e1f78ba35 to ad7919c25 to
   9d4f484bfe). The battery tested the final tip 9d4f484bfe read-only.
   For a toolchain-identity battery this is not a defect: byte-identical
   is byte-identical, and the observation is pinned to the tested
   commits, which the evidence doc states explicitly. The moving tip is
   a concurrency discipline concern for the coordinator, not a
   verdict-changer.
2. Local HEAD moved under the battery: the brief pinned 28088d207 while
   the working copy tested at ef6801b3 (28088d207 an ancestor). The
   working-copy entry therefore attaches to ef6801b3, not the brief's
   pin. The evidence doc records this explicitly. Byte-identity of the
   tested znc is unaffected, so the PASS stands; but the result is
   scoped to the observed HEAD, and the coordinator should re-verify at
   the brief-pinned HEAD if the brief's pin is required to attach.
3. Coverage hole: the three extra detached worktrees at
   ~/workspace/tnn-rsi-wave3/ (probe, senses, trades, all at bd3097874)
   were not in the brief and were not tested. They are the same SHA as
   the tested forktest/tnn-native-lab worktree (bd3097874, PASS), which
   mitigates the practical risk for toolchain identity, but their znc
   files were never hashed. The battery's defined scope is the
   enumerated fork set, and within that scope 19/19 is confirmed; the
   three worktrees are queued-next coverage for the coordinator.
4. Scope reminder, carried: the battery tests toolchain identity, not
   wave artifacts. 19/19 PASS says every enumerated fork carries the
   pinned znc; it says nothing about the cv1_cite or g1_v2 evidence,
   and must not be read as a blanket wave-health number.
5. The znc mode drift (754 worktree vs 100755 in the index) is mode-only
   with zero byte drift, benign this wave, but it is the second wave in
   a row with mode drift on the znc binary. The coordinator should
   normalize the mode and record the convention.

---

## M4: tnn_chat FIT

### Ruling: CONFIRM FIT

Numbers: decline binary rebuild byte-identical to the 1121pdt record
(20273a99215680b5e3e42bbdbbfed105c7109d15ba189c903cf0d88db54418e7);
baseline rebuild byte-identical to the 1121pdt record
(1ada2fae63ddd63d37f06705459c0d8b1d9c8dffc859af25949221bf5895749c).
Probe results on merged HEAD 28088d207 (a merge of origin/tnn-native-lab
e1f78ba35, about 2992 files and 470300 insertions of V-NOLIMIT teach
sources and evidence): KB1 30/30 specific declines, 0 blanket refusals
(3 runs; run 1 output sha a2ca4dd7dd64018e2ce9fd1ca78111928f73e818b9ec6b6738cd6be04ee85308,
byte-identical to the prior wave's recorded output); KB2 17/17 in-KB
turns answered, 0 declines, decline output sha
e05fb4ece4624249be8b4b35c073aa216a359ea08853c0621a6fadcc4e57c264
byte-identical to the rebuilt baseline on all 3 runs each; KB5 10/10
in-KB answers, 0 declines, output sha
4f1603aa2a798a97679e91f54c0614d0de8465856a982a61debc54bc4670e88d
byte-identical to baseline on all 3 runs each; rerun determinism 9/9
run-pairs byte-identical by cmp. All four probe source shas verified
against the prior wave's recorded values before building (c0776ad6,
a87011fe, e6379ddb, 9824f6db); fixtures at HEAD canonical shas (kb.txt
3ef27296, gaz.txt b75fd113); pinned toolchain sha unchanged. No Python
anywhere in the work; nothing pushed to GitHub. This is a clean
re-verification that the large merge introduced no observable change to
the FIT instrument chain.

Scope is carried literally, as both the advocate and the skeptic agree:
the instrument is a 38-fact closed-book probe, not a general
interactive TNN, and no live interactive TNN exists on this branch.
FIT passing means the instrument chain is unchanged on merged HEAD
28088d207; it is NOT merge review of 470300 insertions, and the
coordinator must not let the FIT green light stand in for broader merge
review. The FIT statement is tied to merge commit 28088d207 explicitly;
the wave's later local commits are outside its scope.

---

## Standing rule question

Do any of this wave's findings require a new standing rule? NO. The
issues this wave surfaced are all handled by existing rules (the 0521pdt
Python-anywhere rule plus the 1121pdt M5 precedent; the frozen-bar rule;
commit-order self-check; seal discipline) plus prereg-level fixes. What
is needed is not a new rule but tighter next-wave preregs, listed below.
The five pending governance rulings are Micah's and stay untouched by
this judgment.

## Required record corrections

1. EVIDENCE_CV1_CITE.md section 5: correct the false "0 hits over impl/"
   contamination sentence to the CVC-B8 frozen scope, and state the
   training-input and scoring-transcript hits plainly.
2. CV-1 record: document runs/qmark.txt and runs/noted2.txt as post-build
   diagnostics with their timestamps (21:57 to 21:58, after the 21:55
   binary build and the 21:52 seal) and the exonerating facts (clean 78-line
   source diff, zero sealed probe words, no per-probe branches).
3. CV-1 SEAL.md: fill the seal-open log retroactively by commit hash if
   attestable; otherwise record the blank log as a process defect with a
   standing requirement that the next wave fill the seal-open log at
   scoring time and document every diagnostic input and output.
4. Fork battery record: explicitly pin the tested HEADs (working copy at
   ef6801b3, brief pin 28088d207 as its ancestor; origin/tnn-native-lab
   tip tested at 9d4f484bfe), so the scope of the 19/19 observation is
   unambiguous.

## Queued-next items (coordinator owns these; the judge recommends)

1. Next CV-1 wave: amend F9 to require interrogative forms AND exclude
   frozen assertion-pattern fragments with gazetteer entities; pin what
   routing knowledge the probe author may use; pin gazetteer membership
   as a probe-reachability condition; record the awk derivation of the
   cost ratio in the primary record; re-run the unchanged
   implementation against a fresh sealed set as a new evaluation.
2. G1: if another shaft wave is authorized, it is a mechanism redesign,
   not a re-freeze: measure the actual T field distribution before
   freezing any sigma multiple; do not freeze coupled unknowns (gate
   multiple and mechanism geometry) without a decoupling plan; make the
   wedge fan's direction coverage an explicit design decision; the min-D
   line-of-sight formulation goes under a fresh prereg only.
3. Fork battery: add the three ~/workspace/tnn-rsi-wave3/ worktrees to
   enumeration coverage; pin tested HEADs explicitly in the record;
   normalize the znc file mode drift and record the convention.
4. Standing mandate check for the coordinator: two waves have now been
   spent on the internals of the G1 march-mean mechanism while the
   loop's standing line is big levers on realism and Micah's actual
   frontier is the PAMs v2 deep dive and the b_alpha v9 rebuild. This
   is a coordinator staffing consideration, not a ruling.

## Summary of rulings

- M1 (CV-1 decline-citation): CONFIRM DISCARD. Killing evidence:
  CVC-B1 20/30, CVC-B2 16/20, CVC-B4 4/10; 10 probes intercepted by the
  frozen path-4 assertion handler from a prereg-spec gap (F9 never
  specified interrogative form; confound list never considered path-4
  interception) refined to assertion-pattern plus gazetteer matching.
  The 20/20 conditional stays strictly conditional. The Python contact
  voids nothing under the 0521pdt rule and the 1121pdt M5 precedent.
- M2 (G1 sunshafts re-freeze): CONFIRM DISCARD. Killing evidence:
  KB2 1.0000, KB3 0.00, both recomputed from the BMP bytes; genuine
  mechanism miss (lift lands ~870px from the sun, max +9 luma, 0/39
  wedge points moved). The gate's normality assumption is a valid
  attribution caveat for the next prereg, not a verdict-changer.
- M3 (fork battery): CONFIRM PASS. 19/19 PASS with discriminating
  negative controls, znc 498abcb5 everywhere, scoped to the tested
  commits; three untested worktrees and the mode drift are queued-next
  items.
- M4 (tnn_chat FIT): CONFIRM FIT. Binaries byte-identical to the 1121pdt
  records (20273a99, 1ada2fae), 30/30 declines, 17/17 in-KB parity,
  10/10 KB5, 9/9 rerun pairs byte-identical; scope is the 38-fact
  closed-book probe chain on merged HEAD 28088d207 only.

No new standing rule is required. No bar was weakened. Nothing was
pushed to GitHub. Nothing was written to LOOP_STATE.md.
