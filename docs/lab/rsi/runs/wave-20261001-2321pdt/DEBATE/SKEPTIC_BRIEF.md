# SKEPTIC BRIEF, wave wave-20261001-2321pdt

Role: skeptic. Mandate: argue why each verdict should be OVERTURNED or
further narrowed. Ruthless but fair; the weakest points are attacked,
the evidence is cited, and the asks are concrete.

## The provenance probe

"What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

This brief answers it per question, because the provenance is where
most of these verdicts are weakest. The pattern across the wave: new
labels on inherited machinery, new claims on accommodated worlds,
and new verdict classes invented or refused at the moment they would
be inconvenient.

### Provenance audit, per question

- Q1 (F1): the windowed trigger is new code; the constructor is
  inherited from the prior wave byte-identically. The killing
  evidence proves the failure lives in the inherited component.
  The bar that tripped (K-C0C-REG) was calibrated by its own author
  on an unvalidated fresh seed and measured constructor
  seed-robustness, a property no F1 trigger bar ever required.
- Q2 (H-PI-REV2): the mechanism is frozen from step-7; nothing new
  was built. The five worlds are new but were designed, by disclosed
  pre-freeze admission, to accommodate the rank-biased diagnosis.
  The claim was never tested against a conflict the rank bias does
  not select until the red team did it post-freeze, and then it
  broke.
- Q3 (ARENA2 vs ARENA3): both mechanisms are new code on inherited
  bases (v6, INQ). The underlying principle is the same inherited
  one: exposure-learned templates plus a permutation parsed from
  the question at runtime. ARENA2 additionally inherits the C9
  negative finding, which is genuinely its own.
- Q4 (E3 mandate): the artifact under test is the frozen TNN-2
  binary and its inherited verifier (t2_try_verify with the
  QUERY-carried expected value). The oracle dependence is inherited
  machinery, not a new discovery about a new mechanism; what is new
  is the realization that every prior construction observation sat
  on it.
- Q5 (H5R2): the 9-line t2_prov_ok helper is new; everything else,
  including the forward node-id enumeration order that produces the
  oldest-first tie-break, is inherited. The tie-breaking artifact
  is inherited implementation detail, not a provenance principle.
- Q6 (ARENA5): DEFRECALL is new code on the inherited v6 base, using
  the inherited roster design from ARENA4. The "general default
  action" claim is new language; the measured behavior is a
  content-blind structural trigger.
- Q7 (CONTLEARN): the frozen core is inherited; the trial/promotion/
  P-INV machinery is inherited researcher-written machinery. The
  "demonstrated" integration is that machinery running, not a new
  learner capability.
- Q8 (CONSEQ): nothing new was built; this wave re-executed a frozen
  prereg. The consequence record (a researcher-written 3-revelation
  counter) is inherited. What is new is only the reproduction.

---

## Q1. F1: PARTIAL-narrowed should be allowed; BUILD-FAIL as recorded is too harsh

**Verdict challenged:** F1 BUILD-FAIL, and RT-EXEC's recommendation
to UPHOLD it while rejecting PARTIAL-narrowed as bar-weakening.

**Skeptic case for overturn.** RT-EXEC proved the skeptic's own
point and then drew the wrong conclusion from it. The reviewer's
evidence is that the trigger cannot be implicated: the prior wave's
frozen binary and the new binary produce byte-identical train states
on sealed rW2, the same 4-construct all-ADD overfit, TRIGGER at
episode 1, the identical [4 4 4 2] structure. Every trigger bar
passes: fires on all 4 interleaved patterns where the old trigger
fired 0 times, 0 false positives on 3 clean worlds, 30/30 learning
on interleaved streams, ablations 57pp/57pp. F1-FOLLOWUP Part 1 then
passed all frozen bars on validated fixtures with zero trigger
regression (byte-identical normalized CONSTRUCT sequence). So the
record contains a component that passes everything and a verdict
that says the candidate failed. The verdict, cited by label, will
be read as "the windowed trigger failed." That reading is false,
and the record knows it is false.

The procedural defense, that PARTIAL is not a defined verdict class
and inventing one post-hoc is bar-weakening, is formalism protecting
a mislabeled verdict. Two points. First, the bar itself was
admitted miscalibrated by its own author: K-C0C-REG used an
unvalidated fresh seed and conflated trigger regression with
constructor seed-robustness. "Never weaken a frozen kill bar"
forbids the builder from moving the bar after seeing results; it
does not forbid the debate group from recognizing that the bar
measured a property the lane never set out to test and no prior
wave ever required. The real bar-move is on the uphold side:
imposing constructor seed-robustness retroactively on a trigger
lane. Second, refusing PARTIAL does not avoid precedent-setting; it
sets the precedent that a proven component isolation, byte-identical
reproduction, and an honest bar-calibration admission still cannot
narrow a verdict. That precedent punishes exactly the honesty the
loop wants.

**Ask:** record the verdict as PARTIAL (trigger component PASS on
all trigger bars; constructor seed-sensitivity a separate finding,
already filed as F1-FOLLOWUP Part 2 NOT-FOUND and the F1-BUFFER /
REPAIR / REPAIR2 line). Constrain the precedent: narrowing is
allowed only when the failure is proven to lie in a component the
lane did not change, proven by byte-identical reproduction on the
prior wave's fixtures. That is a high bar, not a loose one, and it
is met here.

---

## Q2. H-PI-REV2: the ADV-S4 break is fatal; narrow further

**Verdict challenged:** H-PI-REV2 BUILD-PASS, even with the
RT-HPIREV2 qualifications attached.

**Skeptic case for further narrowing.** The red team did the
experiment the lane never did: it ran the frozen mechanism
byte-verbatim against a valid single-conflict world per V0-V3
whose true trigger (2,66) the rank bias cannot select. The bound
broke: fails_total=1. That world is inside the narrowed claim's
stated scope. A bound that fails on a valid in-scope world is not
a bound with a qualification; it is a falsified claim. Calling
ADV-S4 a "bound on the qualified claim" is rewording a
counterexample.

The load-bearing finding (Q2) is worse than a caveat: all five lane
worlds accommodated the frozen rank-biased diagnosis by disclosed
pre-freeze design, with D2's design note admitting tuning to match
both declared and diagnosed conflicts. The narrowed claim as
literally stated was never tested against a conflict the rank bias
does not select. Five worlds, all shaped to fit the mechanism, then
a PASS. That is the shape of a self-fulfilling evaluation, honestly
disclosed but self-fulfilling all the same.

ADV-M1 compounds it: a masked second conflict is silently never
flagged (fails=0, zero detection). The bound-trip signal is
probe-dependent, explicit when the uncovered conflict is probed
alone, silent when masked. A single-conflict bound whose trip
signal goes silent under masking cannot detect the scenario it was
built to bound.

"BUILD-PASS with qualifications" will not survive contact with
citation. The qualifiers (rank-diagnosability, probe-dependence)
are not decorations on a passing claim; they ARE the claim's
actual content, and the original language never contained them. A
PASS stamp with footnotes becomes a PASS stamp without footnotes
within two citations. The certification defect (24/25 sealed files
match prereg hashes, not 25/25 as the lane's sentence claimed) is
small, but it shows the lane's evidentiary hygiene was imperfect
exactly where the load-bearing design accommodation sits.

**Ask:** narrow the verdict to the restated claim, "the bound holds
on rank-diagnosable single conflicts with probe-dependent trip
signaling," and rule that citing the claim without both qualifiers
is disallowed. ADV-S4 is recorded as falsifying the claim as
originally stated, not bounding it.

---

## Q3. ARENA2 vs ARENA3: one must yield (sibling collision)

**Verdicts challenged:** ARENA2 BUILD-PASS (REMAP) and ARENA3
BUILD-PASS (TRX) as independent standing claims.

**Skeptic case for subsumption.** The frozen collision clause calls
these "independent competing runs, not duplication." They are
duplication. Both mechanisms are the same principle: compose the
learner's exposure-learned templates with a value permutation parsed
from the question at runtime, with no sealed values hardcoded.
REMAP composes Zem templates with the runtime-parsed permutation;
TRX parses the 4-value relabeling and applies the class-A to class-B
rewrite. The differences are parameterizations, not principles.

The claimed differentiator does not exist in evidence. REMAP's
"generalizes to any permutation/template" was never tested beyond
the frozen battery; it is an asserted generality, not a measured
one. TRX's [0,1,2,3]-validated parsing is narrower on its face but
at least demonstrated. The scores are not comparable (different
bases: v6 at 0.882 vs INQ at 0.941), the ablations are not
comparable (exact-zero halves vs 3/6 halves), and neither has been
run on the other's base, so the one discriminating test the
collision demands, composition (REMAP on the INQ base, or TRX
generalized), was never run. Two non-comparable PASSes on two
bases for one principle is double-counting toward "transfer
demonstrated," and it violates the one-system rule in spirit: two
separate transfer mechanisms where one principle would do. Micah's
2026-10-02 composition ruling is explicit that separate composition
engines must be comparatively tested toward one general operation;
the same logic applies here.

Preserve what is genuinely ARENA2's own: the C9 negative finding
(the causal battery is observationally unidentifiable by design;
only gaming passes) is a real independent contribution and stays
regardless.

**Ask:** name one survivor for the C12 transfer claim. The honest
candidate is REMAP, conditional on actually testing its
any-permutation claim; until that test exists, REMAP's generality
is withdrawn and both stay CANDIDATE. TRX yields as the narrower
parameterization, its record preserved but retired as a separate
standing claim. The locus of lost generality, if any, is recorded:
TRX's explicit parse-and-validate of [0,1,2,3] vs REMAP's
untested any-permutation assertion.

---

## Q4. BATTERY-E3: the mandate is too broad as written and too narrow as executed

**Verdict challenged:** the E3 mandate's scope ("every wave
construction claim resting on unmasked QUERY evidence must be
re-examined blind").

**Skeptic case.** As written, the mandate is unexecutable: it names
no closed list of claims, no method beyond the audit template, and
no sunset. As executed, it is security theater. The one mechanism
it cleared, ROSTER via ARENA-BLIND, is the one mechanism that never
needed clearing: single candidate, no selection step, no verifier
with expected anywhere in its path. The audit template is trivially
satisfiable for any mechanism that never had a selection step,
which means the broad reading generates paperwork, not evidence.

Meanwhile the genuinely implicated claims go unexamined. E3's own
confound note flags BATTERY-E1's W4 behavioral leg:
structure-driven answers vs oracle-verified BFS traversal are
indistinguishable there, and no blind re-run of E1-W4 has happened.
And the biggest unexamined suspect is CONTLEARN: its 6/6
machinery-enabled integration runs the same t2_try_verify
machinery with the QUERY-carried expected value doing selection.
The machinery-disabled discrimination (0/6) tested machinery
presence, not oracle dependence. If the constructions the learner
later "reuses" were oracle-selected, then CONTLEARN's reuse
evidence is reuse of oracle-selected structures, and the E3 reframe
("BFS enumeration plus oracle selection, not selective
construction") applies directly. The mandate, read honestly,
requires a blind re-examination of CONTLEARN's construction phase.
That has not happened.

**Ask:** replace the blanket mandate with a named-claims mandate:
(1) a closed list of implicated claims (PF-A2's 2/2 already
re-described; E1-W4 behavioral leg; CONTLEARN construction phase;
H7R re-derivation construction; ARENA2/ARENA3 transfer
construction); (2) blind re-runs of E1-W4 and CONTLEARN's
construction phase specifically; (3) a sunset rule: any claim not
re-examined blind within two waves is marked ORACLE-UNEXAMINED and
may not be cited as construction evidence. Single-candidate
mechanisms are cleared by the audit template, but the template is
recorded as the trivial case, not the program.

---

## Q5. H5R2: SEPARATED undermines BUILD-PASS

**Verdict challenged:** TNN3H5R BUILD-PASS ("H5R2 ADVANCES") as a
provenance-policy result.

**Skeptic case for overturn.** The scope-standing defense is
bar-legalism. Yes, a verdict names the exact bars that governed it,
and yes, the re-teach family lies outside the frozen battery's
event sequences. But the claim's public meaning, the thing
"H5R2 ADVANCES" will be cited for, is "stale provenance is fixed."
SEPARATED shows that on a constructible event sequence, the gate
re-derives from stale knowledge: two live tag-1 non-superseded
facts on one key, and the gate anchors the re-derived MAP's DEP
edges to the older one. That is stale-provenance anchoring, the
exact failure mode the gate was built to fix, produced by the gate
itself.

The gate's oldest-first pick has no provenance justification
anywhere in the record. It is a creation-order artifact of forward
node-id enumeration. Both facts are live, so the gate's own rule
("a superseded fact licenses nothing") cannot discriminate them.
Under the protocol's own revision semantics, contradiction leaves
the newest fact live, and the pre-registered rationale favored
NEWEST-LIVE-ON-KEY. So the measured fact is: the gate's
tie-breaking direction is arbitrary, it coincides with
newest-live on every frozen family (which is why it passed), and
on the one family that breaks the coincidence it picks the
unjustified side. The H5R2-SYNTHESIS admits no lane shows a world
where picking the older live fact over the newer is the correct
policy.

The honest caveat in the SKEPTIC3 record cuts both ways: "under
strict monotonic teach reading, neither answer is privileged."
If neither is privileged, then the gate is not "the correct
provenance policy" anywhere; it is better than recency, no-gate,
and chance (shown), and unseparated from newest-live-on-key except
where its pick is unjustified (shown). "H5R2 ADVANCES" overclaims
exactly the policy-correctness that was never demonstrated. The
stronger gate (provenance filter plus newest-live tie-breaking
among all live licensing facts) was named, is buildable, and was
not built in any lane.

**Ask:** narrow the verdict: the gate fixes superseded anchoring
on the frozen families; it is not established as the correct
provenance policy. The re-teach gap is named as a known open gap,
and the verdict may not be cited as a provenance-policy result
until the stronger gate passes the union of the frozen families
and the separator family.

---

## Q6. ARENA5: NARROW undermines BUILD-PASS

**Verdict challenged:** ARENA5 BUILD-PASS as "autonomous C15 goal
completion via a general default action."

**Skeptic case for overturn.** The NARROW did not qualify the
advertised claim; it falsified it. The advertised claim was
"handler-free goal completion via a general default action."
ARENA-GEN measured the mechanism on a diverse bare-prompt battery:
it enumerates the roster on "whattime" (the learner has no clock;
the roster is not the time) and on bare "invent" (an incomplete
invention request; the roster is irrelevant). That is not goal
completion. It is a bare-prompt reflex: dispatch miss plus bare
prompt plus non-empty roster always yields enumeration,
appropriate or not. The ARENA-SYNTHESIS itself concedes the words
"general default action" are "untenable without the discrimination
result." The discrimination result is in, and it is negative.

The generality case was never real. RT-ARENA5 showed the sealed
battery contained exactly one bare-prompt item, making the default
action extensionally equivalent to a listnames handler there; the
generality evidence rested on intension plus the lane's dev probes.
ARENA-GEN showed those dev probes were one-sided by design: only
prompts where enumeration is appropriate were tested and counted as
generality. A generality demonstration constructed to succeed is
not evidence of generality. And the surviving intensional claim
(zero goal-string branches) is now irrelevant to the point at
issue: content-blindness is precisely what makes the mechanism fail
discrimination. The trigger's blindness is the defect, not a
virtue.

The governance defense ("judging BUILD-PASS by a bar the lane
never froze would itself be a governance violation") confuses
re-grading bars with fixing a claim. Nobody proposes failing the
frozen bars; all 8 hold. What changed is the verdict's citation
meaning. A verdict is not just a bar checklist; it is a claim that
enters the record and gets cited. Keeping BUILD-PASS un-narrowed
lets "general default action" propagate with a PASS stamp after
being measured false on a diverse battery. The record already
proves qualifiers get dropped in citation.

**Ask:** the verdict stands on its frozen bars but its claim is
renamed: BUILD-PASS (DEFRECALL, content-blind bare-prompt trigger
that volunteers persistent knowledge; the "general default action"
generality claim is withdrawn). DEFRECALL may not be cited as
general default-action evidence until a discriminating trigger is
demonstrated per the synthesis section 4 criteria.

---

## Q7. CONTLEARN: MACHINERY-DEPENDENT overturns BUILD-PASS as labeled

**Verdict challenged:** CONTLEARN BUILD-PASS with the label
LEARNOWN-DEMONSTRATED.

**Skeptic case for overturn.** The measurements are true; the label
is false. On the identical disclosed battery, integration is 0/6
with the machinery disabled and 6/6 with it, doubly confirmed
(CONTLEARN-OWNED, CONTLEARN-OWNED2). Zero MAPs are ever constructed
learner-side. LEARNER-MECH, verified x3 against the frozen bytes,
shows no learner-state path can initiate construction, control
parameters bypass learner state entirely, and the miss path
hardcodes escalation. The "demonstrated" integration is
researcher-machinery integration running on researcher-fired
events. The strong sense (the learner decides or authors) is not
merely unclaimed; it is measured absent.

The proposed remedy, citation discipline ("LEARNOWN-DEMONSTRATED
(machinery-enabled scope; strong sense measured absent,
CONTLEARN-OWNED/OWNED2)"), does not work. Labels get shortened and
qualifiers get dropped; the record proves it (the "25/25 verified"
sentence survived its own 24/25 defect; ARENA2's "ordering-fragile"
survived until ARENA4 refuted it). A label that needs a paragraph
of hedging to be truthful is a bad label, and this one asserts the
strong reading in plain English: "demonstrated" plus
"learner-owned" IS the strong reading. You cannot keep the words
and disclaim their meaning.

Even the weak-H10 reading is thinner than it sounds. The "reuse"
is exact-hit retrieval via activate of machinery-taught facts;
masked queries remain researcher scaffolding (RT-INT); the
learner's own response to experience (UNCERTAINTY+guide pairs)
never recurses into integration. What the learner "owns" is
storage and retrieval inside a researcher-driven pipeline.

**Ask:** retire or rename the label (e.g.,
MACHINERY-ENABLED-INTEGRATION-DEMONSTRATED), keep the measurements
(13/13, 20/20, ablations, determinism) as true of the
machinery-enabled core, and rule that continued citation of
LEARNOWN-DEMONSTRATED as learner-authority evidence is a category
error.

---

## Q8. CONSEQ and CONTLEARN: the qualifications are insufficient; strip the advancement claims

**Verdicts challenged:** CONSEQ VALIDATION-PASS and CONTLEARN
BUILD-PASS as citable advances of their parent hypotheses.

**Skeptic case.** A qualification that is not in the verdict label
is not a qualification; it is a footnote, and footnotes get
dropped. CONSEQ's carried qualifications live in the RT-INT review:
the independent-adversary clause was never met (builder-sealed
worlds), and this wave confirms reproduction fidelity, not
adversarial validation. The verdict label says VALIDATION-PASS. The
parent hypothesis is the shared consequence substrate, but the
scope honestly held is only the consequence re-entry template, the
consequence record is a researcher-written 3-revelation counter,
and C174 validated the store only in dev-harness scope with
researcher-scaffolded thresholds and weights. So what "advanced"?
A reproduction of a builder-sealed template. Citing CONSEQ as
advancing the shared-substrate hypothesis is exactly the overclaim
the qualifications were supposed to prevent, and the label will be
what gets cited.

CONTLEARN is the same structure with the Q7 label hazard: the
weak/strong distinction lives in the review, the label lives in
the verdict list, and the label wins every citation.

The general principle the debate should adopt: advancement is a
claim about a hypothesis, and it must be earned by the experiment
the hypothesis requires. CONSEQ's hypothesis requires the
adversary clause; until it is met, the verdict is
REPRODUCTION-CONFIRMED, a measurement, not an advance. CONTLEARN's
"learner-owned" framing requires the strong sense; it is measured
absent, so the framing is retired per Q7.

**Ask:** both verdicts stand as measurements with renamed,
non-advancing labels. Neither may be cited as advancing its parent
hypothesis (shared consequence substrate; learner-owned
integration) until the specified next experiments exist: the
independent-adversary clause for CONSEQ, and a learner-initiated
construction run (initiation-from-state with white-box evidence)
for CONTLEARN. The K3 regression check (REUSE_COUNT 30/30) may be
cited unconditionally, as the slate notes.

---

## Closing

The wave's evidence is strong; its labels are not. In every
question above, the measurements survive and the advertising does
not. The debate should do the unglamorous work the evidence
already did: rename the verdicts to say what was actually shown.
A PASS stamp on a false claim is worse than a FAIL, because a FAIL
gets reworked and a PASS gets cited.
