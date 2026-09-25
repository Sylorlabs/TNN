# SKEPTIC BRIEF: wave-20260924-1721pdt

Role: skeptic. Method: read every verdict, prereg, evidence, seal, red-team
document cold, then independently re-ran the load-bearing checks (commit
ancestry, sha pins, Python scans, contamination greps, merge diffs) with my
own commands. What follows attacks the worker's verdicts on all three
motions. Where the worker's ground is solid I say so; the judge should
know exactly which attacks bite and which do not.

## MANDATORY SKEPTIC'S PROVENANCE PROBE

"What is the provenance of the artifacts under judgment, and what exactly
is new versus inherited?"

CV-1 decline-citation fix: the implementation (impl/cv1c.zag, gate_op.zag,
both R33 imports, kb.txt, gaz.txt, inkb17.txt, adv30.txt) is inherited
byte-identical from the 1421pdt committed sources (commit 5c53da6ba); I
re-verified the cv1c.zag sha (6d8fb9f013ef3efa1bb44881f98cbeafcabd7110ae4fb7396a3e5721b34d7137)
matches at 1421pdt and at HEAD, so the diff is empty by construction.
Inherited further back: the answer-path "morphology crew" section of
cv1c.zag (the birth-year resolution logic) dates to the 2026-09-23
cmp_scale work, whose own commit (b0441c692) contains a committed Python
file (docs/lab/dialogue/cmp_scale/engine/splice.py) and Python run logs
(runs_p/); the source comment at line 1396 documents the Jaccard
resolution as "(proven: 1/12 < 2/12 in the Python mirror)". So the adopted
source carries a documented Python mirror in its development lineage.
What is genuinely new this wave: the prereg (amended F9), the sealed
30-probe set and key, the scoring transcripts, and the verdict. Every
substantive artifact behind the ADOPT (probes, key, scoring) was authored
inside a single worker session playing author, implementer, and scorer
roles. No renders involved (dialogue text only).

G1 SUNSHAFTS v3: the mechanism (g1/g1_sunshafts_v3.zag) is new this wave,
frozen by prereg acf7cedce plus the sign-correction addendum 1da140387,
implemented in 39707e077. Inherited byte-identical: the r8c baseline
source, the V1-V6 validator, the vendored R33_NATIVE_IO_V1.zag, the pinned
toolchain. The D(x,y) field, sun position, and S14 baseline hash are
inherited. New renders (base.bmp, var_v3_*.bmp) exist but are evidence
only; nothing enters the judge queue. What is new is the mechanism and
its measured behavior; what killed it is the interaction between the
frozen sector-agnostic predicate and the frozen upward-only WEDGE
detector.

## M1: AGAINST the CV-1 ADOPT

The numbers are honest (I spot-checked the scoring transcripts against the
key; the per-probe outputs match; determinism shas are as claimed). My
attacks are on what the numbers license, not on the arithmetic.

### 1. CVC-B8: byte-inheritance does not moot separation, and self-attestation sets a precedent

The bar text (frozen) demands "author/implementer separation attested".
The worker's position: the implementation is a byte-copy, so the
implementer role is vacuous and separation is moot; the seal record then
says "probe author and implementer are separate roles in this worker's
workflow", i.e. one session attesting separation from itself. This is the
precedent-setting weakening the motion warned about. Consider what it
licenses going forward: any future wave can inherit an implementation
byte-identical, author its own probes and key in-session, score them
in-session, and satisfy CVC-B8 with a paragraph of self-attestation. The
separation requirement then evaporates exactly in the case where it is
most load-bearing: an ADOPT verdict resting on zero new implementation
evidence, where every substantive artifact (probes, key, scoring,
verdict) was produced by the same mind. The commit-order discipline
(which I verified: dad5ef955 -> b1951de11 -> 91b7ee160 -> de8616b5f,
strict linear ancestry, each committed alone) proves the seal was not
opened early. It proves nothing about the probe author's independence,
because the seal only guards the implementer-from-probes direction. The
author-to-key-to-scorer direction is unguarded by design, and here all
three are the same session. ADOPT on this basis should at minimum be
recorded as ADOPT-ON-SELF-ATTESTED-SEPARATION so the precedent is visible.

### 2. The 30/30 is a consistency check between the author's model and the implementation, not an independent test

The probe author knew: the full citation rule (spelled out in prereg
section 3), the frozen KB, the gazetteer, and, crucially, the router's
exact firing condition. F9.4 claims the author "must NOT know the frozen
router internals beyond" the public reachability condition, but F9.5 then
hands the author the negative form of the firing condition verbatim
("the assertion handler fires only on pattern plus gazetteer match with
no '?' present"). That IS the router internals, relabeled "public". The
knowledge pin is theater: the author demonstrably received the firing
condition and used it to pre-scrub every probe (F9.9 mechanical checks)
so that all 30 probes reach the mechanism. The key's uncovered lists
were "computed mechanically (awk) over the frozen KB and hand-verified"
by the same session that then scored the implementation against that
key. The tie-break traps are real stress, but their difficulty ceiling
was set by a mind holding a complete model of the rule. 30/30 under
these conditions shows the implementation matches the author's awk
computation of the rule. It does not show what an independent probe
author would find. The verdict's "NEW_KNOWLEDGE_CLAIM" (the 1421pdt
DISCARD was a measurement artifact) is therefore proven only against a
battery the same session designed to be reachable.

### 3. CVC-B5 is tautological this wave, and the prereg misdescribes its inputs

CVC-B5's first leg (17/17 INKB byte-identical) and second leg (30/30
ADV-30 declines) run byte-identical inputs through a byte-identical
binary. Given determinism (CVC-B7, independently established), the
outputs are guaranteed; the bar cannot fail by construction. A kill bar
that cannot fail is not a kill bar; it is a rebuild sanity check wearing
a bar's uniform. Worse, the prereg's F4 describes these as "fresh
INKB-17 and ADV-30 input files (authored pre-implementation)", while the
evidence (section 3) says they are "the 1421pdt unsealed training inputs,
reused byte-identical". "Fresh" versus "reused byte-identical" is a
direct contradiction between the frozen fixture description and the
evidence. The verdict even notes the INKB sha (db6b7075) matches the
1421pdt record, which is exactly what a tautology looks like. The judge
should strike or discount the B5 leg, leaving the ADOPT resting on
B1-B4, B6, B7: all scored on the same-session battery.

### 4. The battery is narrow and the adopted code has untested paths

The verdict adopts the whole decline-citation implementation, but the
sealed battery never exercises two of its paths. The empty-uncovered
fallback ("F9 keeps it off the sealed set; firing during scoring counts
as a miss", prereg section 8 item 8) fires on no sealed probe and on no
ADV-30 probe (all 30 were declines, and the fallback emits non-decline
text). The atomic-verification fail-closed path is likewise unexercised
in the sealed evidence. These paths are adopted sight unseen. On the
paraphrase side, P01-P10 are surface reorderings with full content-word
overlap (e.g. P02 "which jane austen novel: pride and prejudice?"), which
any overlap matcher answers; the zero-confabulation leg of CVC-B1 is
therefore stressed only on trivially answerable probes. And every probe
was pre-scrubbed to dodge the frozen router's assertion, composition,
resume, and correction paths, so the ADOPT certifies the rule only
inside a sanitized input corridor. Real turns are not pre-scrubbed; the
frozen router still swallows "?"-less assertions into NOTED. The verdict
does not claim otherwise, but the ADOPT will be read as "the
decline-citation fix works", and the traveling caveats (narrow battery,
untested fallback, sanitized corridor) do not appear in the verdict's
own text. They should be written into the verdict before adoption.

### 5. Undisclosed Python-mirror lineage in the adopted source

My own grep found what the wave's "Python-cleanliness" verification did
not surface: impl/cv1c.zag line 1396 (and the identical line in
gate_op.zag) reads "(proven: 1/12 < 2/12 in the Python mirror)". I traced
it: the comment is inherited byte-identical from 1421pdt (sha-verified),
first introduced in the 2026-09-23 cmp_scale commits, whose tree
contains docs/lab/dialogue/cmp_scale/engine/splice.py and Python run
logs (runs_p/). So the adopted candidate's answer-path logic was
developed and verified against a Python mirror, and the mirror is
committed in the repo history. The verdict's process disclosure ("No
Python was invoked anywhere in this task") is true only because "this
task" is scoped to exclude lineage. The prereg's void condition covers
"any Python contact with a wave artifact"; the comment sits inside the
wave's adopted implementation artifact. The Python-anywhere rule
(0521pdt) and the 09-24 governance tightening ("pure-Zag rule restored
literally", "void-on-sight for any prereg that pre-authorizes Python
tooling") postdate the mirror, so this is grandfathered contact, not a
void. But the verdict adopts the code without disclosing it, and the
finish-up coordinator's "Python-cleanliness" attestation apparently
missed or silently grandfathered a documented Python mirror in the
adopted source. The judge should decide whether "pure Zag, literally"
permits adopting Python-mirror-developed logic, and the disclosure
should be in the verdict either way. Note the comment is in the
answer-path morphology section, not the decline-citation rule under
test, so it does not taint the B1-B4 evidence directly; it taints the
"no Python anywhere" cleanliness claim attached to the ADOPT.

### 6. What the reversal licenses

The 1421pdt DISCARD is reversed to ADOPT with zero implementation
change. The worker's framing ("measurement artifact, not mechanism
miss") is supported by the evidence. But note the asymmetry this
creates: a DISCARD can be overturned by re-authoring probes in-session
until the implementation passes, with the implementation frozen
throughout. The only thing that changed between DISCARD and ADOPT is
probe authorship quality, and the author is the party most motivated to
see the re-test pass. The seal discipline prevents the crudest form of
this (tuning the implementation to the probes), but nothing prevents
tuning the probes to the implementation, because the author knows the
implementation's rule exactly and the "reachability" pre-screening (F9.9)
is precisely probe-to-implementation tuning by another name. The prereg
freezes the tuning procedure rather than forbidding it. The judge
should weigh whether ADOPT-via-reauthored-probes, with no
implementation delta and no independent author, meets the bar for
integrating the rule into the frozen baseline, or whether it meets the
bar only for "the 1421pdt DISCARD is retracted".

## M2: AGAINST the G1 "mechanism miss, not freeze defect" ruling (not against DISCARD)

I agree with DISCARD as the outcome: KB2 = 1.0000 and KB3 = 0.00 are
honest measurements, the numbers trace to committed evidence (I
re-verified the probe output, verifier INFO lines, and the
quantization reconciliation 2805 - 2609 = 196 with delta < 12 giving
L = 0), and the frozen verdict mapping leaves no other outcome. My
attack is on the classification and on the red-team's three locks,
because the classification sets precedent for how the loop learns.

### Lock (a): the "no re-interpretation" clause is misread, and it cuts against the verdict itself

The frozen clause reads: "No bar may be weakened, narrowed, or
re-interpreted to force a pass." Its text bars re-interpretation to
force a PASS. VOID is not a pass, and in any case the G1 frozen mapping
has only two outcomes (READY-FOR-JUDGE or DISCARD; "any bar unevaluable
maps to DISCARD"), so a freeze-defect reclassification could not force
a pass under any reading. The red team applies the clause to block a
classification change the clause does not address: that application is
itself a re-interpretation of the clause beyond its text. Worse, the
clause cuts against the verdict's own ruling. The frozen fan-direction
decision states the fan "has no fixed global opening direction". The
verdict rules the mechanism "missed" the upward fan. A miss requires
aim; the frozen text explicitly disclaims aim. Reading an aimless
predicate as having missed its target is a post-hoc re-interpretation
of the frozen fan language to force a narrative. The verdict's own
mechanism description admits the tension: the predicate "selects
angular local minima wherever the D field puts them, with no reason to
produce the upward fan the detector and the visual concept require".
"No reason to produce" and "missed" cannot both be true. The honest
description is: the mechanism worked exactly as frozen (sun-anchored
lift confirmed: 2805 delta passers, 77 percent within 200 px of the
sun, max dL 35 versus v2's 9, clarity gate at 87.9 per mille as
designed); the frozen detector measured a sector the frozen mechanism
never aimed at.

### Lock (b): the novelty caveat is a risk disclosure, not a pre-registered verdict mapping

The red team treats the novelty argument's caveat as binding
pre-registration of the failure mode. Read it literally: "v3 can still
fail KB2/KB3: if no wedge sightline is a strict angular local minimum,
or if the D field near the sun has no gap structure at the frozen fan
scale, the wedge points get zero lift and v3 discards exactly like v2."
The realized failure satisfies the letter of the first disjunct (no
wedge sightline was a minimum), but not its evidentiary basis: the
caveat's failure mode is field-sparsity (no gap structure), while the
realization is field-richness-in-the-wrong-sector (2805 passers, 2609
lifted pixels, just below the sun). A caveat whose letter covers
sparsity, sector-mismatch, and nearly any KB2/KB3 failure is not a
pre-registered mapping from a specific failure mode to a verdict; it is
a blanket risk disclosure of the form "the bars are at risk". You
cannot pre-register "the bars might fail" and then claim the specific
way they failed was pre-registered. The lock therefore begs the
question: it uses a tautologically broad caveat to launder a
classification decision the caveat never made.

### Lock (c): cherry-picked binding statements

The red team binds the prereg's authorial claim that the WEDGE set
"measures exactly the fan the mechanism targets" while discounting the
equally frozen, equally authorial fan-direction decision ("no fixed
global opening direction"). When two frozen statements conflict, the
red team selected the one that sustains "mechanism miss". But the
conflict itself is the freeze defect: the prereg froze a
sector-agnostic mechanism, a sector-specific detector, and an
unfalsified-at-freeze correspondence claim between them, with nothing
in the mechanism to enforce the correspondence. The D-field belief
("the minima will be sunward/upward") was the author's prediction, and
it was refuted by the D field. A refuted prediction about the field is
not a mechanism malfunction. The correct lesson, which the verdict's
own structural observation already states, is that the predicate
needs a sector prior: that is a design-stage omission, knowable at
freeze time (the author chose sector-agnosticism explicitly), not a
mechanism miss discovered at runtime.

### The "terminal state" framing overclaims

The verdict and red team call this "the honest terminal state for this
line". But the evidence shows the mechanism idea (sun-anchored
directional-contrast selection) worked as frozen; what failed was the
unfrozen correspondence between its output sector and the detector's
sector. The next step (a sector prior) is already specified in the
verdict's own structural observation, so the line is not terminal for
lack of ideas; it is paused pending a re-aimed prereg. Recording
"mechanism miss" teaches the loop that directional-contrast selection
failed, when the evidence says the selection worked and the aim was
never frozen. The classification should read: mechanism performed as
frozen; upward-fan hypothesis for this D field refuted; detector
mismatch; re-aim under a new prereg with a sector prior. The outcome
(DISCARD, no judge queue) is unchanged; the lesson is not.

## M3: wave process

### FIT carry-over: sound, but the wording matters

I independently verified the carry-over argument and it holds: the
in-tree FIT chain inputs (pinned znc blob 498abcb5, the R33 SHA256
source, kb.txt, gaz.txt) are byte-identical across 53616213e,
63156682c, and ead33399e; the .zag sources are extracted read-only
from the archive branch, not from the merged tree, so the merges
(10,048 files in the first, cognition_ws source changes in the
second) cannot touch them. Byte-identical inputs through a
byte-identical deterministic binary is indeed a tautology, not
missing evidence, and the 9/9 rerun identity on the certified run
closes the determinism leg. The advocate brief's "empty diff on all
frozen paths" is accurate as written (it says "on all frozen paths",
not "empty diff" unqualified). My residual: the precedent should be
recorded precisely as "carry-over is valid only when the frozen chain
is fully enumerated and its diff across the merge is verified empty",
because the merges here were enormous and a future "docs-only" merge
characterization done sloppily would silently void the argument.

### Fork battery and merges

23/23 worker PASS plus the new origin tip in finish-up (24/24
effective) is as reported; I did not re-run the battery (that would
be redundant), but the recorded shas, harness agreement, and negative
controls are internally consistent. The two origin merges had zero
conflicts, no reset, no rebase; all eight verdict-relevant commits
are ancestors of HEAD (verified). No issue.

### One staffing note the verdict buries

Three waves on G1 internals is correctly flagged, but the verdict's
"terminal state" language (see M2) converts a staffing judgment into
a technical one. Keep them separate: the staffing call (pause G1,
frontier is PAMs v2 and b_alpha v9) is sound; the technical claim
(the mechanism idea is dead) is not established by this evidence.

## Independent grep summary (Python and provenance)

- No .py files, no python invocations, no python tokens in any authored
  .zag source or runner script anywhere in the wave directory this
  wave. The only matches are the runners' own self-check grep patterns
  and "No Python" disclosure comments. Scoring used shell coreutils
  and the pinned Zag binaries only.
- Contamination grep (CVC-B8): zero occurrences of any sealed probe
  payload word (sphinx, galleon, dagger, prism, onyx, quartz, raven,
  xenon, saber, willow, titan, lantern, nomad) in impl/cv1c.zag,
  impl/gate_op.zag, or the KB fixtures. The static separation check
  holds.
- The "Python mirror" comment (impl/cv1c.zag:1396, impl/gate_op.zag:1396)
  is inherited byte-identical from 1421pdt (sha-verified) and originates
  in the 2026-09-23 cmp_scale commits, whose tree contains a committed
  splice.py and Python run logs. Documented Python-mirror development
  of adopted logic; undisclosed in the verdict.

## Recommended rulings for the judge

1. CV-1: do not ADOPT on this record as a clean adoption. At most
   record ADOPT-SCOPED: the 1421pdt DISCARD is retracted as a
   measurement artifact, and the citation rule passes B1-B4/B6/B7 on
   a same-session battery. Require before baseline integration: (a)
   the fallback and fail-closed paths exercised on sealed probes;
   (b) the Python-mirror lineage disclosed and ruled on under the
   literal pure-Zag standard; (c) the CVC-B5 tautology and the
   "fresh" versus "reused" fixture contradiction corrected in the
   record; (d) the traveling caveats (narrow paraphrase battery,
   sanitized input corridor, self-attested separation) written into
   the verdict.
2. G1: DISCARD stands; reclassify the ruling from "mechanism miss" to
   "detector mismatch / unfrozen correspondence; upward-fan hypothesis
   refuted; mechanism performed as frozen". Do not record the
   directional-contrast idea as dead; record the sector prior as the
   specified next step for any future prereg. The red team's three
   locks do not survive literal reading, and the "terminal state"
   framing should be downgraded to a staffing pause.
3. Process: the FIT carry-over and fork battery stand; codify the
   carry-over precondition (enumerated frozen chain, verified empty
   diff) so it does not become a blanket license to skip re-certs.
