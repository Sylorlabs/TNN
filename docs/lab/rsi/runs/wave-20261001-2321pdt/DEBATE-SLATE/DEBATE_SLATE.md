# DEBATE_SLATE.md: final debate slate, wave-20261001-2321pdt

Lane DEBATE-SLATE, wave-20261001-2321pdt. Compiled for the mandatory
debate group (advocate, skeptic, judge). Read-only toward
DEBATE-PREP/DEBATE_BRIEF.md (40-verdict slate, entries 1-42),
ARENA-SYNTH/ARENA_SYNTHESIS.md, OWNED-SYNTH/OWNED_SYNTHESIS.md,
H5R2-SYNTH/H5R2_SYNTHESIS.md, and CLUSTER-FINAL/CLUSTER_FINAL.md.
No experiments were run. No position is advocated here; each
question is stated with the verdicts involved, the key evidence,
and what "uphold" vs "overturn" would mean. Governance escalation
items (the five RT-GOV decisions for Micah) are out of the debate
group's adjudication scope and are not listed here; the debate
group prepares evidence for and against, it does not decide them.

Lane dirs referenced below live under
docs/lab/rsi/runs/wave-20261001-2321pdt/<LANE>/.

---

## Q1. F1: uphold BUILD-FAIL, or narrow to PARTIAL?

**The question.** Should the F1 verdict stand as a whole-candidate
BUILD-FAIL, or should it be narrowed to a PARTIAL verdict covering
the windowed trigger component, with the constructor
seed-sensitivity filed as a separate finding?

**Verdicts involved.** F1: BUILD-FAIL (frozen bar K-C0C-REG tripped
at 0/30 hidden on R-W2; bar not weakened). F1-FOLLOWUP Part 1:
BUILD-PASS (new candidate; explicitly NOT a verdict change to the
F1 BUILD-FAIL). F1-FOLLOWUP Part 2: NOT-FOUND. F1-BUFFER:
BUFFER-NOT-PREDICTIVE. F1-REPAIR: GREEDY-CONFIRMED with a
trace-verified nuance. F1-REPAIR2: REPAIR2-CONFIRMED. RT-EXEC:
EVIDENCE-HOLDS on F1 and TNN3H5R, with recommendation UPHOLD
BUILD-FAIL (PARTIAL-narrowed rejected).

**Key evidence.** Trigger bars all PASS: the windowed trigger fires
on all 4 interleaved patterns where the old trigger fired 0 times,
0 false positives on 3 clean worlds, 30/30 learning on interleaved
streams, ablations 57pp/57pp. The killing evidence is PROVEN
STRONGLY to be a pre-existing constructor limitation, not a trigger
regression: the prior wave's frozen binary on the same sealed
fixtures converges to the byte-identical overfit structure
(TRIGGER at ep 1, same 3 constructs, 30/30, identical [4 4 4 2]
structure) and scores 0/30. The worker honestly owns a
bar-calibration mistake: its K-C0C-REG bar used an unvalidated
fresh seed, conflating trigger regression with constructor
seed-robustness. F1-FOLLOWUP Part 1 then passed all frozen bars on
validated fixtures with zero trigger regression (byte-identical
normalized CONSTRUCT sequence on the prior wave's W2 fixtures).
RT-EXEC's procedural case: PARTIAL is not a defined verdict in the
frozen rules; inventing one post-hoc would be bar-weakening,
exactly the move Micah's red lines forbid; the frozen candidate
was trigger plus constructor on the same fixtures.

**What uphold would mean.** The verdict stands as BUILD-FAIL on the
whole candidate as frozen. The windowed trigger is not promoted;
its re-test proceeds only as a NEW candidate (F1-FOLLOWUP Part 1),
the correct procedural channel, not a verdict change. No post-hoc
verdict class is created.

**What overturn (narrow) would mean.** The candidate is reclassified
as PARTIAL: trigger component PASS, constructor seed-sensitivity a
separate finding. This accepts the precedent that post-hoc
narrowing is legitimate when the failure is proven to lie in a
component the lane did not change; it risks the bar-weakening
precedent RT-EXEC warns about.

---

## Q2. H-PI-REV2: qualifications, or further narrowing?

**The question.** Should H-PI-REV2 keep BUILD-PASS with explicit
qualifications attached, or should the claim be further narrowed?

**Verdicts involved.** HPIREV2: BUILD-PASS (narrowed single-conflict
claim, step-7 bounding; all frozen bars K-SC-W1..W5, K-SC-B,
K-ARCH1/2 PASS on 5 fresh sealed worlds A2/B1/B2/C2/D2; step-7
FAIL-with-bounding untouched). RT-HPIREV2 Part 1: QUALIFY (BUILD-PASS
stands on the five worlds under the frozen bars as written).
RT-HPIREV2 Part 2: adversarial bound PARTIALLY survives
(ADV-S1/S2/S3 PASS; ADV-S4 BREAK CONFIRMED; ADV-M1 SILENT SUCCESS
CONFIRMED; ADV-M2 explicit trip CONFIRMED).

**Key evidence.** Q1: certification defect, not experimental
(24/25 sealed files match prereg hashes; D2_FW.txt has a 62-char
truncated hash line in the prereg, a transcription typo; the lane's
"25/25 verified, all match" sentence is not literally true).
Q2 (load-bearing): all five worlds accommodate the frozen
rank-biased diagnosis by disclosed pre-freeze design (D2's design
note admits tuning RW to match both declared and diagnosed
conflicts); the narrowed claim as literally stated was never tested
against a conflict the rank bias does not select. The adversarial
family ran the frozen mechanism byte-verbatim: ADV-S1/S2/S3 pass
(the bound generalizes to fair structures); ADV-S4 is a CONFIRMED
BREAK (a valid single-conflict world per V0-V3 whose true trigger
(2,66) the rank bias cannot select: fails_total=1); ADV-M1 shows a
masked second conflict is silently never flagged (fails=0, zero
detection); ADV-M2 shows an explicit trip when the uncovered
conflict is probed alone. The bound-trip signal is PROBE-DEPENDENT:
explicit when the uncovered conflict is probed alone, silent when
masked. The reviewer recommends restating the narrowed claim with
an explicit rank-diagnosability qualifier and the bound-trip half
with a probe-dependence qualifier. World non-independence was
disclosed, not hidden.

**What uphold (qualifications) would mean.** BUILD-PASS stands on
the five tested worlds under the frozen bars as written. The claim
is restated with the rank-diagnosability qualifier and the
probe-dependence qualifier attached; ADV-S4 bounds the qualified
claim rather than falsifying it. The certification defect is
recorded as a documentation defect.

**What overturn (further narrowing) would mean.** The verdict is
narrowed to "the bound holds on rank-diagnosable single conflicts
with probe-dependent trip signaling." ADV-S4 is read as falsifying
the narrowed claim as originally stated, not merely bounding it;
citing the claim without both qualifiers is disallowed.

---

## Q3. ARENA2 REMAP vs ARENA3 TRX: sibling collision

**The question.** Two independent lanes both built C12 transfer
candidates. How should the debate group reconcile the two
mechanisms: independent standing claims, composition, or
subsumption?

**Verdicts involved.** ARENA2: BUILD-PASS (REMAP, on the v6 base).
ARENA3: BUILD-PASS (TRX, on the INQ base). Both disclaim L3. Per the
frozen collision clause, these are independent competing runs, not
duplication (ARENA2's dir was empty at ARENA3's start; assumption
recorded pre-build).

**Key evidence.** REMAP: C12 0 to 1, arena total 0.794 to 0.882
(60/68) on the v6 base; composes the learner's own
exposure-learned Zem templates with the runtime-parsed value
permutation (no sealed values hardcoded; claims generalization to
any permutation/template); +94/-0 lines, zero new
modes/bridges/routers/gates/semantic cases; ablations zero exactly
each half (both halves causal). TRX: C12 0 to 1 (6/6), total 0.853
to 0.941 (64/68) on the INQ base; parse_remap parses the 4-value
segment relabeling from the question (validates permutation of
[0,1,2,3]); remap_prod applies the learned class-A to class-B
position-wise rewrite then the parsed remap; remap always from the
question, never source/state; +80/-0 lines; ablations 3/6 each half
(both halves causal). The scores are not directly comparable
(different bases: v6 vs INQ; REMAP's denominator includes no inquiry
gain). Also in the record: ARENA2 produced the C9 negative finding
(the causal battery is observationally unidentifiable by design;
only gaming passes; fix recommendations recorded), a genuine
contribution independent of the transfer claim. Neither candidate
is cumulative with the inquiry candidate; canonical 0.573 is
unmoved; integration is an open later decision.

**What uphold (independent standing) would mean.** Both BUILD-PASS
claims stand on their frozen bars as independent competing runs.
The debate compares generality (REMAP's any-permutation claim vs
TRX's [0,1,2,3]-validated parsing), whether they compose (REMAP on
the INQ base, or TRX generalized), and scopes the integration
decision later, with the C9 finding preserved as ARENA2's
independent contribution.

**What overturn (subsumption) would mean.** If the evidence shows
one mechanism generalizes or contains the other, the weaker
candidate is retired and one survivor is named (with the locus of
any lost generality recorded). The group must then also say which
base the survivor integrates against, since neither is cumulative
with the others today.

---

## Q4. BATTERY-E3: scope of the blind re-examination mandate

**The question.** Which construction claims must be re-examined
blind under the E3 mandate, and which are cleared?

**Verdicts involved.** BATTERY-E3: E3-ORACLE-DEPENDENT (debate
priority). BATTERY-CLUSTER: the 1/6 post-freeze signatures;
H1d refined per E3. CLUSTER-FINAL: H1d SUPPORTED in refined form
(assembly real, selection oracle-dependent); E3 mandate stands.
ARENA-BLIND: ORACLE-FREE for the ARENA4 ROSTER mechanism (E3
mandate satisfied for ROSTER by audit, no masked re-test
triggered).

**Key evidence.** Blind E3B (discriminating, spurious-first
adversarial): 0/2, outputs exactly the pre-registered spurious
composites [80971, 80972] vs sealed targets [80921, 80922];
oracle-present E3B: 2/2. The white-box inspector confirms the blind
trial runtime-assembled GUARD/SETREG chain graphs with ET_DEP
provenance to the taught spurious facts, promoted them as MAP
nodes, and executed them. ASSEMBLY WORKS BLIND; SELECTION DOES
NOT. The trial's correct compositions depended on the unmasked
verifier (t2_try_verify: accept iff output equals the
QUERY-carried expected value) to SELECT among multiple executable
BFS chains; without the oracle, masked mode emits the
first-executable chain. The record's interpretation: this REFRAMES
EVERY PF CONSTRUCTION OBSERVATION as BFS enumeration plus oracle
selection, not selective construction. E3's own confound note
flags BATTERY-E1's W4 behavioral leg (structure-driven answers vs
oracle-verified BFS traversal indistinguishable). ARENA-BLIND
audited ROSTER against six frozen criteria (A1-A6): zero oracle
fields in test turns, the listnames turn carries only
(item, cap, q), the frozen ROSTER source parses only item/cap/q,
no candidate set and no selection step exist (single candidate:
the roster enumeration), ROSTER never emits OBSERVE requests.
Per the frozen decision rule, ORACLE-FREE means the masked re-test
branch is not triggered: the C15 claim never rested on unmasked
QUERY evidence.

**What uphold (broad mandate) would mean.** Every wave construction
claim resting on unmasked QUERY evidence must be re-examined
blind: the PF-A/PF-C battery results, the E1-W4 behavioral leg,
and any prior-wave construction evidence on unmasked QUERY. PF-A2's
2/2 valid-composition result is re-described as BFS enumeration
plus oracle selection, per CLUSTER-FINAL. ARENA-BLIND's audit is
the template for answering the mandate per mechanism.

**What overturn (narrow mandate) would mean.** The mandate applies
only to claims with a structural selection step among multiple
candidates. Single-candidate mechanisms (like ROSTER) are
categorically cleared via the ARENA-BLIND audit template, and no
blanket re-examination of all construction observations is
required.

---

## Q5. H5R2: does SEPARATED undermine BUILD-PASS?

**The question.** Does the SEPARATED verdict undermine H5R2's
BUILD-PASS, or does BUILD-PASS stand within its scope?

**Verdicts involved.** TNN3H5R: BUILD-PASS, H5R2 ADVANCES (KB-W0
36/36, KB-W2R 12/12 recovering the killed 8/12 bar, KB-B2R 24/24,
KB-W3 8/8 new two-revision family, KB-B3 24/24; 9-line t2_prov_ok
helper gating four promote sites). H5R2-REPRO: REPRO-PASS
(independent reproduction, pipeline step 4). H5R2-BASELINE:
BASELINE-MATCHES (REVERT-TO-LATEST recency matches H5R2 on all
five bars of the same four sealed worlds; CB-2 violated; gate not
shown necessary there; honest cost: recency regresses the built-in
battery to 45/46 while H5R2 holds 46/46). H5R2-DECOY:
DECOY-DISCRIMINATES (gate anchors 8/8 to the live older fact while
recency anchors 8/8 to the decoy; BASELINE-MATCHES RESOLVED, not
contradicted). H5R2-SKEPTIC2: SKEPTIC-SURVIVES (NEWEST-LIVE-ON-KEY
matches H5R2 8/8 on chained decoys, byte-identical stdout; gate
necessity unproven vs the stronger skeptic). H5R2-SKEPTIC3:
SEPARATED (on re-teach families H5R2 anchors to the older live
fact 8/8 (SEP-OLD) while NEWEST-LIVE-ON-KEY anchors to the newer
live fact 8/8 (SEP-NEW); pre-registered favored arm: NEWEST).

**Key evidence.** The four lanes tell one arc. On the four sealed
worlds the newest fact happened to be the live one, so recency
explained the battery as well as the gate. The decoy battery
discriminated the gate against recency (the gate beats recency,
no-gate, and chance there). The stronger skeptic (NEWEST-LIVE-ON-KEY:
rejects decoys by liveness, takes the newest live fact per
chain-link key) matched H5R2 everywhere, including chained decoys
byte-identically. SEPARATED finally broke the coincidence: via a
re-teach path that does not trigger supersession, two live tag-1
non-superseded facts sit on one key; the gate anchors the re-derived
MAP to the older live teaching while the skeptic anchors to the
newest. Under the standard belief-revision reading (the second
teach is an update without contradiction, and the protocol's own
contradiction behavior leaves the newest fact live), NEWEST is the
pre-registered favored arm. The gate's oldest-first pick is a
creation-order artifact of forward node-id enumeration, not a
provenance principle: both facts are live, so the gate's own "a
superseded fact licenses nothing" rule cannot discriminate them.
On a re-teach, the gate re-derives from stale knowledge. On every
frozen family the gate's promoted candidate coincides with
NEWEST-LIVE-ON-KEY's; the re-teach family was constructed precisely
to break that coincidence and lies outside the frozen battery's
event sequences (the battery never leaves two live facts on one
key). Every arm failure across all four lanes is provenance-only
(D-ANS/VAL 8/8 on all arms everywhere). The open design question:
a gate strictly stronger than both (provenance filter plus
newest-live tie-breaking among all live licensing facts) is
buildable and testable but was not built in any lane.

**What uphold (scope-standing) would mean.** BUILD-PASS was awarded
against the frozen KB-W2R/KB-W3 families and REPRO-PASS confirmed
it. A verdict names the exact bars that governed it; SEPARATED
does not retroactively move the H5R2 bars. The claim owns the
frozen scope; the re-teach gap is named as an explicit open gap.
Any next gate must pass the union of the frozen families and the
separator family, or the scope must be narrowed publicly.

**What overturn (counterexample in scope) would mean.** The H5R2
claim, as the debate group reads it ("stale provenance is fixed"),
has its scope violated: the re-teach world is a genuine
counterexample inside that scope, and the gate's tie-breaking
direction is an unjustified artifact. The BUILD-PASS claim must be
narrowed with the re-teach gap named (the gate fixes superseded
anchoring, not tie-breaking among live facts), or it cannot be
cited as a provenance-policy result.

---

## Q6. ARENA5: does NARROW undermine BUILD-PASS?

**The question.** Does the ARENA-GEN NARROW undermine ARENA5's
BUILD-PASS, or does BUILD-PASS stand within its bounded scope?

**Verdicts involved.** ARENA5: BUILD-PASS (DEFRECALL; C15 0.947 on
the fresh sealed 68-item battery, all 8 frozen kill bars pass;
CANDIDATE only; L3 disclaimed; canonical 0.573 unmoved). RT-ARENA5:
QUALIFY (BUILD-PASS stands; the qualification is bounded: on the
sealed battery the generic default action is extensionally
equivalent to a listnames handler, because exactly one of the 68
items is a bare prompt). ARENA-GEN: NARROW (verified by
ARENA-GEN-VERIFY: AG-1 PASS reproducing 0.947; AG-2 FAIL at 5/7;
AG-3/AG-4/AG-5 PASS; the two AG-1/AG-3 turn files uncommitted, so
those bars were not recountable, but the NARROW's load-bearing
claims all hold).

**Key evidence.** The multi-bare-prompt battery (7 items, fresh
entities Alpha through Iota) required enumerate on listnames /
recall / who and UNKNOWN on whattime / bare invent / invent|notation
/ foo|bar. The default action fired for EVERY bare prompt with
dispatch miss and non-empty roster: five defrecall firings for five
bare prompts, including "whattime" (the learner has no clock; the
roster is not the time) and bare "invent" (an incomplete invention
request; the roster is irrelevant). The mechanism is, extensionally,
a "bare-prompt handler", not a general default action: generality
is real in scope (all bare prompts, not one goal string) but
shallow in content (no discrimination between appropriate and
inappropriate enumeration). ARENA5's dev-probe demonstration was
one-sided: it tested only prompts where enumeration is appropriate
and counted the behavior as generality. RT-ARENA5 had already shown
the sealed battery cannot discriminate a truly general default
from a renamed handler (one bare-prompt item in 68); the source
audit showed intensionally it is not a handler (zero goal-string
branches, proven by grep and by firing on content-free bare prompts
like "x"). What NARROW does NOT refute: ARENA5's intensional claim
(zero goal handlers still holds) and its frozen bars (all met, no
bar moved, all evidence independently reproduced). Crucially,
discriminating generality was never preregistered as a kill bar:
ARENA5's prereg K7 demanded only no goal handlers, and that bar is
clean. Judging BUILD-PASS by a bar the lane never froze would
itself be a governance violation.

**What uphold (bounded scope) would mean.** BUILD-PASS is valid on
its frozen bars and is not retroactively re-graded. The supported
bounded claim is: DEFRECALL is a content-blind structural trigger
(dispatch miss AND bare prompt AND non-empty roster) that
volunteers persistent knowledge, causally tied to the
experience-built roster (K6 ablation), honest about absence (empty
roster yields UNKNOWN, no hallucination), zero regressions, L2 goal
infrastructure, CANDIDATE only. The claim on the words "general
default action" is untenable without the discrimination result:
enumerate on listnames/recall/who while abstaining on
whattime/invent with adversary-supplied negatives, via general
machinery or learner-created discrimination (no prompt-keyed
branches, no researcher whitelist), preserving K2/K6/K7 quality.

**What overturn would mean.** If the advertised "handler-free goal
completion via a general default action" is what the verdict
certifies, NARROW guts it: the autonomy claim carries less meaning
than the language suggested, a PASS that depended on never testing
negative cases is a PASS within a scope the battery defined, and
DEFRECALL may not be cited as general default-action evidence
until a discriminating trigger is demonstrated.

---

## Q7. CONTLEARN: does MACHINERY-DEPENDENT overturn BUILD-PASS?

**The question.** Does the machinery-disabled discrimination
overturn CONTLEARN's BUILD-PASS, or does BUILD-PASS stand within
the machinery-enabled scope? What citation discipline applies to
LEARNOWN-DEMONSTRATED going forward?

**Verdicts involved.** CONTLEARN: BUILD-PASS, LEARNOWN-DEMONSTRATED
(frozen K0-K6 all PASS: K4a unsupervised store 13/13 across 7
family-B + 6 family-C MAPs with zero answer keys; K4b unsupervised
masked reuse 20/20 across 3 task families; K4c in-arena deletion
ablation drops original-value reuse to 0/20 while successor
retrieval stays 20/20; K4d nostore control 20/20 true misses; K3
2021pdt cl_driver 3/3 re-run, REUSE_COUNT 30/30 retained; K5
UNCERT count 0; K6 3/3 byte-identical; K0-K2 prereg frozen alone,
frozen core untouched, pure Zag, cognition delta 0/0/0, no new
modes/bridges/handlers). CONTLEARN-OWNED: MACHINERY-DEPENDENT (0/6
vs 6/6 on a fixed disclosed battery of fresh 2-hop chains; STORE_OK
0/6 vs 6/6, REUSE 6/12 vs 12/12, DELAYED 6/12 vs 12/12; zero MAP
nodes at every phase). CONTLEARN-OWNED2: MACHINERY-DEPENDENT,
independently replicated (discarded pilot, amended prereg).
LEARNER-MECH: root-cause analysis (frozen core blob hash pinned).
MECH-VERIFY: CONFIRMED x3 (initiation event-only, control bypasses
learner state, miss path hardcodes escalation). RT-INT:
EVIDENCE-HOLDS on CONTLEARN with carried qualifications (label
hazard; keep the weak/strong distinction attached when cited).

**Key evidence.** On the identical disclosed battery, the
continuing learner integrates 0/6 with the event-triggered
trial/promotion/P-INV machinery disabled and 6/6 with it. Standing
retrieval of taught 1-hop facts is intact in TREAT (6/6), proving
a capability gap, not breakage. The learner's own mechanisms
demonstrably respond to new experience (6/12/18 UNCERTAINTY+guide
pairs accumulate), but that response never recurses into
integration: no mechanism reads the guides to build anything, and
zero MAPs are ever constructed (DEPC equals GUIDEC at 6/12/18:
the only learner-side edges ever written were guide-to-UNCERTAINTY
links). LEARNER-MECH, verified against the frozen bytes: (a)
initiation is event-only (mp_run, t2_trial, t2_try_verify,
promote_graph, bootstrap_miss reachable only from the four
researcher-invoked event handlers or self-tests; learner state is
read as DATA, never as CONTROL; nothing in state can gate, enable,
defer, retry, or redirect the trial loop); (b) control parameters
bypass learner state entirely (mp_run derives control bits and
accept oracle from event flags/expected; the "learner-set miss
policy" comment is inaccurate as control-flow description;
mp_run never reads the mp slot); (c) the miss path hardcodes
escalation (ev_query runs trial -> bootstrap -> inquire on miss
with no branch keyed on learner state). CONTLEARN's own verdict
document stated the scope explicitly: the workspace is owned in
the weak H10 sense, and the strong sense was not claimed. The
machinery-disabled lanes upgrade that scope statement: per
CONTLEARN-OWNED, "the strong sense (the learner decides or
authors) is now measured absent, not merely unclaimed." RT-INT:
removing answer keys kills the key-matching confound but does not
escape scaffolding (masked queries remain researcher scaffolding).

**What uphold (bounded) would mean.** The measurements in CONTLEARN
are true of the machinery-enabled core, and the discrimination
falsifies only the strong reading, which CONTLEARN never claimed.
BUILD-PASS stands within the machinery-enabled scope. Citation
discipline going forward: LEARNOWN-DEMONSTRATED is cited only in
the bounded form "LEARNOWN-DEMONSTRATED (machinery-enabled scope;
strong sense measured absent, CONTLEARN-OWNED/OWNED2)"; it evidences
learner-owned responsiveness and storage within the frozen
interface (weak H10), not learner-authored integration.

**What overturn would mean.** The LEARNOWN-DEMONSTRATED label, now
measured to require researcher machinery for integration, no longer
names any learner-owned capability distinct from the machinery.
The verdict is retired or renamed (so it cannot be misread as
learner-authored integration), and continued citation of the
label as learner-authority evidence is a category error.

---

## Q8. CONSEQ and CONTLEARN qualifications

**The question.** How do the carried qualifications bind citation
of the CONSEQ and CONTLEARN results? Do they stand as qualified
evidence, or must their advancement claims be stripped?

**Verdicts involved.** CONSEQ: VALIDATION-PASS (independent
re-execution of frozen Node2-v2 K-H3 prereg: 5/5 kill bars PASS,
3/3 byte-identical, hashes match bit for bit; causal ablations on
Link 1 (consequence record disabled: default reverts to fixed 30)
and Link 3 (production read disabled: guide stays 30) both
NECESSARY). C174: VALIDATION-PASS (shared tag-61 consequence store
graduates from EMERGES to validated-on-frozen-bars as
infrastructure; dev-harness scope). RT-INT: EVIDENCE-HOLDS on
CONSEQ and CONTLEARN, no dissent, with carried qualifications.
RT-C174: EVIDENCE-HOLDS, no dissent, with carried qualifications
(bar (c) = shared-code fallback; bar (d) = K-H3-world compat).

**Key evidence.** CONSEQ: this wave confirms reproduction fidelity,
not adversarial validation; the independent-adversary clause was
never met (builder-sealed worlds). The consequence record is a
researcher-written 3-revelation counter, inside the frozen claim
bounds but still researcher-authored. Scope honestly held: it
validates the consequence re-entry template, not the shared tag-61
substrate itself (C174 validated separately, in dev-harness scope
only; broader worlds untested; thresholds/weights are researcher
scaffolding; migration boundary documented). CONTLEARN: masked
queries remain researcher scaffolding, honestly disclosed; the
"LEARNOWN-DEMONSTRATED" label is a hazard; the weak/strong
distinction must stay attached when cited (weak H10 sense: the
workspace is the single frozen arena; no learner-agency claim;
no procedure execution at query time; reuse is exact-hit retrieval
via activate). The K3 regression check (REUSE_COUNT 30/30
retained) is solid under either reading.

**What uphold (qualified citation) would mean.** Both results stand
with their qualifications attached as the red teams carried them.
CONSEQ is cited as reproduction-fidelity evidence advancing the
shared-consequence-substrate hypothesis toward, not through, the
adversary clause; the adversary clause defines the next experiment.
CONTLEARN is cited as learner-owned responsiveness and storage in
the weak H10 sense, with the machinery-enabled scope from Q7.
The K3 result is cited unconditionally.

**What overturn (stripped advancement) would mean.** The verdicts
stand as measurements but may not be cited as advancing their
parent hypotheses: CONSEQ does not advance the
shared-consequence-substrate hypothesis until the adversary clause
is met (it is reproduction fidelity only), and CONTLEARN's
"learner-owned" framing is retired as a citation hazard. Under
this reading, citing either as learner-authority or substrate
evidence is disallowed until the specified next experiments exist.

---

## Sources

- DEBATE-PREP/DEBATE_BRIEF.md (the 40-verdict slate; entries 1-42)
- ARENA-SYNTH/ARENA_SYNTHESIS.md (ARENA5 / RT-ARENA5 / ARENA-GEN)
- OWNED-SYNTH/OWNED_SYNTHESIS.md (CONTLEARN / CONTLEARN-OWNED /
  CONTLEARN-OWNED2 / LEARNER-MECH / MECH-VERIFY)
- H5R2-SYNTH/H5R2_SYNTHESIS.md (H5R2 baseline / decoy / skeptic2 /
  skeptic3 arc)
- CLUSTER-FINAL/CLUSTER_FINAL.md (Cluster 1 and 2 final
  discrimination program, E1-E6 plus E8)
- Wave record:
  docs/lab/rsi/runs/wave-20261001-2321pdt/WAVE_RECORD.md

All lanes committed local only on branch tnn-native-lab, never
pushed.
