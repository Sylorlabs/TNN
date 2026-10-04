# JUDGE RULING: wave-20260924-1721pdt debate group

Role: JUDGE. Method: read the advocate brief, the skeptic brief, both
verdicts, both frozen preregs, the G1 addendum, the novelty argument, and
the red-team G1 review cold; independently re-ran the load-bearing checks
(Python-mirror comment at impl/cv1c.zag:1396 and impl/gate_op.zag:1396,
the cmp_scale commit ancestry, evidence wording, and the frozen texts
quoted below). Commits were not altered. Nothing was pushed. The five
governance rulings awaiting Micah and the nine sealed judge pairs are
untouched by every ruling here.

Loop documentation carries no em-dashes per the standing style rule.

## The skeptic's provenance probe (verbatim, as required)

"What is the provenance of the artifacts under judgment, and what exactly
is new versus inherited?"

## EXECUTIVE SUMMARY OF RULINGS

- M1 (CV-1 decline-citation re-test): UPHOLD ADOPT [RE-CERT]. The frozen
  mapping admits exactly one outcome on an 8/8 sweep (ADOPT iff CVC-B1
  through CVC-B8 all PASS; no other outcome exists), and the measured
  sweep is 8/8 PASS with no bar weakened. The skeptic's attacks identify
  real record defects, and I rule on each: (i) the Python-mirror comment
  is documented, grandfathered lineage contact from 2026-09-23, disclosed
  in the record below, and not a void; the verdict's "No Python was
  invoked anywhere in this task" is true as wave-scoped, and the lineage
  disclosure is now required; whether Python-mirror-developed logic may
  be adopted going forward is a red-line question reserved to Micah; (ii)
  CVC-B8 PASS stands by its frozen text, but the self-attested
  single-session separation is recorded as a visible precedent caveat;
  (iii) no material "fresh" versus "reused" contradiction: both the
  prereg and the evidence use "fresh" to mean unsealed training inputs,
  and both disclose byte-inheritance; B5 stands as a rebuild sanity
  check, recorded as carrying no discriminating weight this wave; (iv)
  the traveling caveats must be written into the verdict record by
  addendum (ordered below); (v) the 1421pdt DISCARD is retracted and the
  rule is adopted on this record, but integration into the frozen
  baseline is held until the fallback and fail-closed paths are
  exercised on sealed probes and Micah rules on the Python-mirror
  question.
- M2 (G1 SUNSHAFTS v3): UPHOLD DISCARD [NEW]. Both briefs agree on the
  outcome; the numbers (KB2 1.0000 vs >=1.12, KB3 0.00 vs >=60.0, dL = 0
  at all 39 wedge points) leave no other outcome under the frozen
  mapping. I RECLASSIFY the ruling: the "mechanism miss" label does not
  survive literal reading of the frozen text. The recorded
  classification is "detector mismatch / unfrozen correspondence;
  upward-fan hypothesis refuted for this D field; mechanism performed
  as frozen." The directional-contrast idea is PAUSED pending a
  sector-prior prereg, not terminal-dead. The red team's three locks are
  each rejected on the frozen text (reasons below). The sign-correction
  addendum stands as a legitimate pre-implementation freeze-defect
  repair.
- M3 (wave process): SOUND. The FIT carry-over precondition is codified
  as a standing rule (enumerated frozen chain, verified empty diff,
  determinism already established). Fork battery recorded at 24/24
  effective. Staffing judgments and technical claims are kept separate.
- M4 (standing rules and record corrections): ordered follow-ups below,
  including the LOOP_STATE head DIVERGENCE NOTE correction.

## M1: CV-1 decline-citation re-test, ADOPT [RE-CERT] UPHELD

The numbers are not in dispute: both briefs agree the scoring is honest
(CVC-B1 30/30 with 0 confabulations; B2 20/20; B3 0 violations,
machine-checked 97/97; B4 10/10; B5 17/17 parity plus 30/30 ADV;
B6 1.73x; B7 3/3 identical; B8 seal integrity). Commit order is strictly
prereg dad5ef955 before seal b1951de11 before impl 91b7ee160 before
scoring de8616b5f, and the implementation is sha256-identical to the
1421pdt committed blobs (commit 5c53da6ba). The frozen verdict mapping
(PREREG_CV1_CITE_1721.md, section 4) states: "ADOPT iff CVC-B1 through
CVC-B8 all PASS. Any FAIL means DISCARD with killing evidence...
No other outcome exists." On an 8/8 sweep there is exactly one lawful
outcome. No bar was weakened, narrowed, or re-interpreted. ADOPT stands.

I rule on the five specified sub-questions:

### (i) Python-mirror lineage under the literal pure-Zag standard

The facts: impl/cv1c.zag line 1396 and impl/gate_op.zag line 1396 read
"(proven: 1/12 < 2/12 in the Python mirror)" inside the answer-path
morphology section. I confirmed the comment is inherited byte-identical
from 1421pdt and originates in the 2026-09-23 cmp_scale work, whose
commit b0441c692 (dated 2026-09-23 10:14:53 -0700) contains
docs/lab/dialogue/cmp_scale/engine/splice.py and Python run logs.

Ruling: disclose-and-grandfather, not a violation, on this record.

- The prereg's void condition is "any Python contact with a wave
  artifact" (0521pdt Python-anywhere rule). The contact was on
  2026-09-23, before the 0521pdt tightening and before the 09-24 literal
  restoration of the pure-Zag rule, and it touched the cmp_scale
  artifacts, not any artifact authored this wave. This wave's work
  (prereg, probes, key, scoring, verdict) had no Python contact; both
  briefs and my own grep confirm the scans are clean.
- The verdict's disclosure "No Python was invoked anywhere in this
  task" is true as wave-scoped, but the lineage was undisclosed and the
  comment sits inside the adopted implementation artifact. That gap is
  now closed by this ruling and by the ordered addendum.
- The comment is in the answer-path morphology section, not the
  decline-citation rule under test, so it does not taint the B1-B4
  evidence directly; it taints only the breadth of the cleanliness
  claim, which the addendum corrects.
- Whether Python-mirror-developed logic may be adopted under the
  literal pure-Zag standard going forward is a red-line question. Only
  Micah can change or clarify a red line. I record it as awaiting him
  (M4 follow-up 2). Until he rules, the loop may not adopt newly
  Python-mirror-developed logic; this wave's case is grandfathered
  contact, not a void, and is not a precedent for future adoption.

### (ii) CVC-B8 self-attestation

The frozen bar text demands "author/implementer separation attested."
An attestation exists in the seal record, the commit order discipline
held, and static grep confirms zero sealed probe bytes in the candidate
artifacts. The implementation predates the sealed set, so the
implementer-from-probes direction the seal guards could not be violated.
On the bar's frozen text, CVC-B8 PASSES, and re-reading it now to
require cross-worker authorship would be a post-hoc narrowing of a
frozen bar, which is forbidden.

But the skeptic's precedent warning is correct and is hereby recorded:
every substantive artifact behind this ADOPT (probes, key, scoring,
verdict) was authored inside a single worker session, and the
separation is self-attested. This ADOPT is therefore on the record as
ADOPT-ON-SELF-ATTESTED-SEPARATION under a single-session re-test of
byte-inherited implementation. Future RE-CERT re-tests should rotate
the probe author across workers, and any prospective amendment to CVC-B8
must go through the prereg and Micah, never retroactively.

### (iii) The CVC-B5 "fresh" versus "reused" wording

There is no material contradiction. The prereg's F4 reads "fresh
INKB-17 and ADV-30 input files (authored pre-implementation as unsealed
training inputs, committed with the implementation evidence)," and the
evidence (section 3, line 41) reads "reused byte-identical (unsealed
training artifacts, not sealed probes)" while calling the same probes
"30 fresh adversarial training probes" at line 69. Both documents use
"fresh" to mean unsealed training inputs (never part of a sealed set),
and both disclose byte-inheritance from 1421pdt; the verdict reports
the matching INKB sha db6b7075 openly. The wording is ambiguous and
should say "unsealed" in future preregs (record correction below), but
no bar text was contradicted and no measurement changes.

On the tautology claim: CVC-B5's legs (byte-identical inputs through a
byte-identical binary) cannot fail by construction given determinism,
and both briefs effectively agree. I rule the B5 PASS stands (striking
a passing bar would itself be a narrowing), and the record now states
that B5 carried no discriminating weight this wave: it is a rebuild
sanity check, not evidence for the NEW_KNOWLEDGE_CLAIM. The ADOPT rests
on B1-B4, B6, and B7.

### (iv) Traveling caveats written into the verdict

The skeptic's caveats are factual and must be in the record, not merely
in a debate brief. The coordinator is ordered to append an addendum to
VERDICT_CV1_CITE_1721.md carrying: (a) the Python-mirror lineage
disclosure from (i); (b) the B5 rebuild-sanity note from (iii); (c) the
single-session authorship and self-attested B8 separation note from
(ii); (d) the narrow paraphrase battery (surface reorderings, full
content-word overlap), the sanitized input corridor (every probe
pre-screened past the frozen router's assertion, composition, resume,
and correction paths; real turns are not pre-scrubbed), and the
untested fallback and fail-closed paths (adopted sight unseen; the
empty-uncovered fallback fired on no sealed or ADV probe).

### (v) Integration versus retraction

The record supports: the 1421pdt DISCARD is retracted as a measurement
artifact (10 assertion-routed probes never reached the mechanism), and
the decline-citation rule is adopted on fresh sealed evidence.
Integration of the rule into the frozen baseline is NOT authorized on
this record alone: it is held until (a) the fallback and fail-closed
paths are exercised on sealed probes and (b) Micah rules on the
Python-mirror question from (i). The verdict's own "Queued next"
section already defers integration to the coordinator; this ruling makes
the conditions explicit.

On the reversal asymmetry (attack 6): the 1421pdt verdict itself
recommended this exact remedy ("re-author a fresh sealed set amending
F9... re-run against this unchanged implementation"), the 1721pdt prereg
froze the remedy with its amended F9 and NEW_KNOWLEDGE_CLAIM before any
probe existed, and the seal preceded scoring. Probe re-authoring here
was a preregistered procedure, not ad hoc tuning. The residual risk
(motivated author, F9.9 reachability pre-screening as probe-to-rule
tuning) is real and is recorded in the caveats; it is the reason the
adoption is scoped and baseline integration is held, not a reason to
discard an 8/8 sweep.

## M2: G1 SUNSHAFTS v3, DISCARD [NEW] UPHELD, CLASSIFICATION CHANGED

The outcome is undisputed: KB2 = 1.0000 vs bar >=1.12 FAIL; KB3 = 0.00
vs bar >=60.0 FAIL; dL = 0 at all 39 validated wedge points. The frozen
mapping ("any gate, validator check, or bar failed... maps to DISCARD")
admits no other outcome. DISCARD stands; nothing enters the judge
queue.

On the classification, I side with the skeptic. The frozen text, quoted
literally:

- Verdict mapping: "No bar may be weakened, narrowed, or re-interpreted
  to force a pass." This clause bars re-interpretation that forces a
  PASS. A classification change cannot force a pass: the G1 mapping has
  only READY-FOR-JUDGE or DISCARD, and KB2/KB3 remain failed under every
  classification. The red team's lock (a) applies the clause to a ruling
  the clause does not address, which is itself a re-interpretation
  beyond its text. Lock (a) is rejected.
- Fan-direction decision (frozen): "The fan has no fixed global opening
  direction; it is anchored per-pixel to the sunward ray." A
  mechanism-miss ruling requires aim; the frozen text explicitly
  disclaims fixed aim. The verdict's own mechanism description admits
  the predicate "selects angular local minima wherever the D field puts
  them, with no reason to produce the upward fan the detector and the
  visual concept require." "No reason to produce" and "missed" cannot
  both stand. The honest description is that the mechanism performed
  exactly as frozen: sun-anchored lift confirmed (2805 delta passers,
  2609 pixels with nonzero dL, max |dL| 35 vs v2's 9, 2003 of 2609
  = 76.8 percent within 200 px of the sun, clarity gate 28476/323997
  = 87.9 per mille inside the frozen 50..150 band), and the minima
  simply lay below the sun (lift band bbox x 125..1023, y 308..458)
  while the frozen detector measured the upward fan (every wedge point
  y < 300).
- The novelty argument's caveat ("v3 can still fail KB2/KB3: if no wedge
  sightline is a strict angular local minimum, or if the D field near
  the sun has no gap structure at the frozen fan scale, the wedge points
  get zero lift and v3 discards exactly like v2") pre-registered the
  outcome mapping (DISCARD on this failure), not the failure-mode
  classification. The realized failure satisfied the letter of the
  first disjunct but its evidentiary basis was field-sparsity, while
  the realization was field-richness-in-the-wrong-sector. A blanket
  risk disclosure ("the bars are at risk") cannot launder a
  classification the caveat never made. Lock (b) supports the DISCARD
  outcome; it does not support "mechanism miss."
- Lock (c): the prereg freezes both "the WEDGE point set ... measures
  exactly the fan the mechanism targets" (authorial belief) and "no
  fixed global opening direction" (design decision). Binding the first
  while discounting the second is selective. The conflict itself is the
  freeze defect: a sector-agnostic mechanism, a sector-specific
  detector, and an unfalsified-at-freeze correspondence claim between
  them. The D-field belief (minima will be sunward/upward) was the
  author's prediction, and it was refuted by the D field.

Recorded classification: detector mismatch / unfrozen correspondence;
upward-fan hypothesis for this D field refuted; mechanism performed as
frozen. This changes no outcome and weakens no bar.

On "terminal state": the verdict's own red-team note 3 already
specifies the next step (a sector prior, or D-field correspondence with
the visible cloud). The directional-contrast idea is therefore not dead
for lack of ideas; it is PAUSED pending a re-aimed prereg with a sector
prior. The staffing call (pause G1 internals, frontier is PAMs v2 and
b_alpha v9) stands as a staffing judgment, separated from the
technical claim. The "terminal state" framing is downgraded
accordingly.

The sign-correction addendum stands: it was committed pre-implementation
(ancestry prereg acf7cedce, addendum 1da140387, impl 39707e077; the
addendum commit contains only the addendum file), it repairs a real
internal contradiction (frozen formula selects the densest decile,
frozen prose selects the clearest: disjoint sets), SGATE = 1152 is the
flipped score's own measured 90th percentile (not a blind negation),
no kill bar was touched, and the tripwire measured 87.9 per mille,
confirming the corrected gate behaves as designed. This is a legitimate
S10 internal-consistency repair, not post-hoc tuning.

## M3: WAVE PROCESS SOUND

- Merges: two origin merges (53616213e by the worker; 63156682c and
  ead33399e in finish-up), zero conflicts, no reset, no rebase; origin
  fully merged at 14c883855; all verdict-relevant commits are ancestors
  of HEAD. Sound.
- FIT carry-over: sound on this record, and I codify it as a standing
  rule: carry-over of a frozen FIT chain across a merge is valid ONLY
  when (1) the frozen chain is fully enumerated (pinned toolchain blob
  sha 498abcb5, the R33 SHA256 source, kb.txt, gaz.txt), (2) those
  inputs are extracted read-only from the archive branch rather than
  the merged tree, so merge file volume (10,048 files in the first
  merge; cognition_ws source changes in the second) cannot touch them,
  (3) the diff of the enumerated chain across the merge is verified
  empty, and (4) determinism is already established (9/9 rerun identity
  on the certified run). Without all four, a fresh re-run is required.
  This must not become a blanket license to skip re-certs.
- Fork battery: 23/23 worker PASS plus the new origin tip tested in
  finish-up: 24/24 effective, recorded.
- Python scans: clean across the wave's own work (CV-1 and G1),
  consistent with (i) above.

## M4: STANDING RULES AND RECORD CORRECTIONS (ordered follow-ups)

1. Coordinator: append the traveling-caveat addendum to
   VERDICT_CV1_CITE_1721.md per M1(iv), quoting this ruling's (i)
   through (iii) disclosures. Do not alter the verdict's bars,
   numbers, or outcome.
2. Awaiting Micah (red-line question, not decided here): whether
   Python-mirror-developed logic may be adopted under the literal
   pure-Zag standard going forward. Until he rules, the loop may not
   adopt newly Python-mirror-developed logic; the 1721pdt case is
   grandfathered contact and is not a precedent for future adoption.
3. Coordinator: record the G1 v3 classification change (detector
   mismatch / unfrozen correspondence; upward-fan hypothesis refuted;
   mechanism performed as frozen; idea PAUSED pending a sector-prior
   prereg) in the wave record, and ensure no summary carries the
   superseded "mechanism miss" label without the correction.
4. Coordinator: correct the LOOP_STATE head DIVERGENCE NOTE, which
   still carries the disproven "deleted loop records" claim; the
   correction lives in the 0521pdt section. The head note must not
   carry a disproven claim: strike it there or annotate it as disproven
   with a pointer to the 0521pdt correction.
5. Standing: the FIT carry-over precondition from M3 is now a standing
   rule for all future waves.
6. Standing: future RE-CERT re-tests should rotate the probe author
   across worker sessions; ADOPT-ON-SELF-ATTESTED-SEPARATION is now a
   named, visible precedent, not a silent one.
7. Standing: preregs must describe unsealed training inputs as
   "unsealed" rather than "fresh" to avoid the B5 wording ambiguity.
8. Unchanged by this ruling: the five loop-governance rulings awaiting
   Micah, the nine sealed judge pairs, the frozen baseline, and
   Micah's frontier work (PAMs v2, b_alpha v9).

## Disposition

- M1: UPHOLD ADOPT [RE-CERT] with recorded caveats and held baseline
  integration.
- M2: UPHOLD DISCARD [NEW]; classification changed to detector
  mismatch / unfrozen correspondence; idea paused, not terminal.
- M3: SOUND; FIT carry-over codified as a standing rule; fork battery
  24/24 recorded.
- M4: follow-ups 1 through 8 above; follow-up 2 awaits Micah.

Nothing was committed and nothing was pushed by the judge. The ruling
file lives at
docs/lab/rsi/runs/wave-20260924-1721pdt/debate/JUDGE_RULING_1721.md.
