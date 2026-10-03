# JUDGE_RULING.md: adjudication of the 8 debate questions, wave-20261001-2321pdt

Wave: wave-20261001-2321pdt. Role: JUDGE. Date: 2026-10-02 PDT.
Working copy: ~/workspace/tnn-rsi, branch tnn-native-lab.

Standing rule applied throughout: a verdict can be overturned ONLY with
cited evidence. Frozen-bar discipline: a verdict names the exact bars
that governed it; later results do not retroactively move those bars;
judging a verdict by a bar it never froze is itself a governance
violation.

Sources judged from (no experiments were run by this role):
docs/lab/rsi/runs/wave-20261001-2321pdt/WAVE_RECORD.md,
DEBATE-SLATE/DEBATE_SLATE.md, DEBATE-PREP/DEBATE_BRIEF.md,
ARENA-SYNTH/ARENA_SYNTHESIS.md, OWNED-SYNTH/OWNED_SYNTHESIS.md,
H5R2-SYNTH/H5R2_SYNTHESIS.md, CLUSTER-FINAL/CLUSTER_FINAL.md,
CLUSTER-SYNTHESIS/CLUSTER_SYNTHESIS.md.

## Process caveat (transcript incomplete)

The verbatim provenance probe could not be verified as asked. There is
no DEBATE.md transcript anywhere in the wave record dir (find returned
nothing), DEBATE/ contains only SKEPTIC_NAMECHECK.md (role declared
2026-10-02 ~00:44 PDT, minutes before this ruling), and
DEBATE/ADVOCATE_BRIEF.md and DEBATE/SKEPTIC_BRIEF.md do not exist.
LOOPSTATE-DRAFT/LOOPSTATE_DRAFT.md (line 54) records "Debate outcomes:
PENDING. The debate group has not convened; DEBATE.md is not yet
written." So the debate transcript is incomplete: the skeptic has not
yet asked the verbatim provenance probe in any recorded transcript, and
no advocate or skeptic briefs existed for this judge to read. This
ruling is made from the slate and syntheses per the task instructions.
If the debate group later convenes, the probe must still be asked
verbatim and recorded in DEBATE.md.

---

## Q1. F1: UPHOLD BUILD-FAIL or allow PARTIAL?

**Ruling: UPHOLD BUILD-FAIL.**

The frozen candidate tripped the frozen bar K-C0C-REG (0/30 hidden on
R-W2); the bar was not weakened. RT-EXEC's attribution is PROVEN
STRONGLY: the prior wave's frozen binary on the same sealed fixtures
converges to the byte-identical overfit structure (same 3 constructs,
30/30, identical [4 4 4 2] structure) and scores 0/30, so the trip is a
pre-existing constructor limitation, not a trigger regression. The
trigger component's own bars all pass (fires on all 4 interleaved
patterns where the old trigger fired 0 times; 0 false positives on 3
clean worlds; 30/30 learning on interleaved streams; ablations 57pp/57pp).
The worker owns a bar-calibration mistake (K-C0C-REG used an unvalidated
fresh seed, conflating trigger regression with constructor
seed-robustness).

PARTIAL is not a defined verdict in the frozen rules. Creating it
post-hoc to salvage the trigger component would be bar-weakening,
exactly the move Micah's red lines forbid (RT-EXEC review commit
76b9ee229, recommendation recorded in the wave record). The correct
procedural channel already exists and has been used: F1-FOLLOWUP Part 1
is the NEW candidate with corrected bars, and it BUILD-PASSes (zero
trigger regression, byte-identical normalized CONSTRUCT sequence on the
prior wave's W2 fixtures). The trigger evidence is therefore preserved
in the record without inventing a verdict class.

Commit-order self-check passes both lanes (F1 50de69403 < ba5ebbf8b;
FOLLOWUP chain 001fcfaca < 6dee24671 < 34960a9bc < 63922a500 <
27116eb12 < 728e114f2).

---

## Q2. H-PI-REV2: qualifications, or further narrowing?

**Ruling: OVERTURN (further narrowing).**

The BUILD-PASS measurement stands on the five tested worlds: all frozen
bars K-SC-W1..W5, K-SC-B, K-ARCH1/2 pass; commit order holds (prereg
00b31af53 alone, implementation ec52cf1ca); 3/3 byte-identical; bars
verbatim, none weakened (RT-HPIREV2 Part 1, review commit 5f53f1c7a).

But the claim as stated does not survive. The cited evidence:

- RT-HPIREV2 Part 1, Q2 (load-bearing): all five lane worlds accommodate
  the frozen rank-biased diagnosis by disclosed pre-freeze design (D2's
  design note admits tuning RW to match both declared and diagnosed
  conflicts). The narrowed claim as literally stated was never tested
  against a conflict the rank bias does not select.
- RT-HPIREV2 Part 2 (frozen mechanism run byte-verbatim, seal 8b86b27d2
  committed alone pre-execution, cognition delta 0): ADV-S4 BREAK
  CONFIRMED, a valid single-conflict world per V0-V3 whose true trigger
  (2,66) the rank bias cannot select (fails_total=1). ADV-M1 SILENT
  SUCCESS CONFIRMED (masked second conflict: fails=0, zero detection).
  ADV-M2 explicit trip CONFIRMED (probed second conflict:
  COUNTEREXAMPLE_DETECTED at W3). The bound-trip signal is
  PROBE-DEPENDENT.

ADV-S4 is inside the stated scope of the narrowed claim (a valid
single-conflict world per V0-V3) and the bound fails there. The
unqualified statement "single-conflict bound" is therefore falsified as
stated; what survives is the bound on rank-diagnosable single conflicts
with probe-dependent trip signaling. This is narrowing, not mere
qualification: the five worlds never tested beyond rank-diagnosability
(Q2), so the qualifier is new content required by the adversarial
evidence.

The narrowed surviving claim: "The step-7 bound holds on
rank-diagnosable single conflicts; the bound-trip signal is
probe-dependent (explicit when the uncovered conflict is probed alone,
silent when masked)." ADV-S4 and ADV-M1 attach as the known failure
envelope. Citing the claim without both qualifiers is disallowed. ADV-S1/
S2/S3 PASS (bound generalizes to fair structures) remains the evidence
for the narrowed domain. Q1 (certification defect: 24/25 sealed files
match; D2_FW.txt truncated hash line in the prereg; the lane's "25/25
verified" sentence not literally true) is recorded as a documentation
defect with no experimental weight.

---

## Q3. ARENA2 REMAP vs ARENA3 TRX: sibling collision

**Ruling: UPHOLD independent standing. No subsumption.**

Both lanes are BUILD-PASS on their frozen bars (all bars pass; REMAP:
C12 0 to 1, arena 0.794 to 0.882 on the v6 base; TRX: C12 0 to 1 at 6/6,
arena 0.853 to 0.941 on the INQ base; both 3/3 byte-identical; zero
regressions; zero new modes/bridges/routers/gates/semantic cases; L3
disclaimed by both). Per the frozen collision clause these are
independent competing runs, not duplication: ARENA2's dir was empty at
ARENA3's start, so ARENA3 defaulted to C12 per instructions and recorded
the assumption pre-build.

No evidence in the record shows one mechanism generalizes or contains
the other: REMAP composes the learner's own exposure-learned Zem
templates with a runtime-parsed value permutation (claims any
permutation/template generality); TRX parses the 4-value segment
relabeling from the question (validates permutation of [0,1,2,3]) and
applies the learned class-A to class-B rewrite then the parsed remap.
The scores are not directly comparable (different bases: v6 vs INQ).
Subsumption would require cited evidence the weaker candidate's
generality is contained in the stronger; there is none, so subsumption
would be a claim without evidence.

Preserved: ARENA2's C9 negative finding is an independent contribution
(causal battery observationally unidentifiable by design; only gaming
passes; generator fix recommendations recorded). Open, not decided:
the composition question (REMAP on the INQ base, or TRX generalized
beyond [0,1,2,3]) is a later comparative experiment. Neither candidate
is cumulative with the inquiry candidate today; canonical 0.573 unmoved;
integration is a later decision.

---

## Q4. BATTERY-E3: scope of the blind re-examination mandate

**Ruling: OVERTURN (narrow mandate).**

The E3 finding is real and its mechanism is precisely understood:
blind E3B 0/2 (outputs exactly the pre-registered spurious composites
[80971, 80972] vs sealed targets [80921, 80922]); oracle-present E3B
2/2; the white-box inspector confirms the blind trial runtime-assembled
GUARD/SETREG chain graphs with ET_DEP provenance, promoted them as MAP
nodes, and executed them. ASSEMBLY WORKS BLIND; SELECTION DOES NOT. The
trial's correct compositions depended on the unmasked verifier
(t2_try_verify: accept iff output equals the QUERY-carried expected
value) to SELECT among multiple executable BFS chains; masked mode emits
the first-executable chain in deterministic BFS order. PF-A2's 2/2
valid-composition result is re-described as BFS enumeration plus oracle
selection (CLUSTER-FINAL, section 4). Criterion 0 not met; no L3
language anywhere.

The E3 mechanism can only confound claims that have a structural
selection step among multiple candidates. Where no candidate set and no
selection step exist, there is no oracle pathway for a blind re-test to
remove; a masked re-test there discriminates nothing. ARENA-BLIND
audited ROSTER against six frozen criteria (A1-A6): zero oracle fields
in test turns; the listnames turn carries only (item, cap, q); the
frozen ROSTER source parses only item/cap/q; no candidate set and no
selection step exist (single candidate: the roster enumeration); ROSTER
never emits OBSERVE requests. Per the frozen decision rule, ORACLE-FREE
means the masked re-test branch is not triggered. This audit template
is the correct instrument for single-candidate mechanisms: categorical
clearance via audit, audit performed and committed, not assumed.

So the mandate is: every construction claim whose evidence could rest
on an unmasked QUERY-carried expected value playing a selection role
must be answered, either by blind re-test (selection-step claims) or by
the A1-A6-style audit (single-candidate mechanisms, audited per
mechanism). No blanket masked re-examination of everything is required.

Named applications: (a) PF-A/PF-C battery results re-described per
CLUSTER-FINAL; (b) E1-W4's behavioral leg cannot be cited as
construction evidence (its confound is flagged in both E1 and E3
records: structure-driven answers vs oracle-verified BFS traversal
indistinguishable), while E1's structural leg (licensed derived
structures in persistent state) stands and kills H1c; (c) any
prior-wave construction observation on unmasked QUERY evidence takes the
same fork: blind re-test or A1-A6 audit before citation.

---

## Q5. H5R2: does SEPARATED undermine BUILD-PASS?

**Ruling: UPHOLD (scope-standing), with a mandatory scope boundary.**

BUILD-PASS was awarded against the frozen KB-W2R/KB-W3 families (KB-W0
36/36, KB-W2R 12/12 recovering the killed 8/12 bar, KB-B2R 24/24, KB-W3
8/8, KB-B3 24/24; 9-line t2_prov_ok helper gating four promote sites;
prereg dc7df4aba < implementation 9db334bd4). REPRO-PASS (pipeline step
4, commit 8b30769de) confirmed every number: sources extracted via git
show match lane hashes, 3x independent rebuild byte-identical, all four
sealed world hashes match, 12 re-runs byte-identical. A verdict names
the exact bars that governed it; SEPARATED does not retroactively move
the H5R2 bars. On every frozen family the gate's promoted candidate
coincides with NEWEST-LIVE-ON-KEY's; the re-teach separator family lies
outside the frozen battery's event sequences (the battery never leaves
two live facts on one key). TNN3H5R's own scope statement reads:
"revision-provenance hypothesis on the frozen battery only; no broad
generality or L3 claim."

The four-lane arc is honest and coherent: BASELINE-MATCHES
(REVERT-TO-LATEST matches H5R2 on all five bars of the four sealed
worlds; CB-2 violated; gate not shown necessary there) was RESOLVED, not
contradicted, by DECOY-DISCRIMINATES (gate anchors 8/8 to the live older
fact while recency anchors 8/8 to the decoy). SKEPTIC-SURVIVES
(NEWEST-LIVE-ON-KEY matches H5R2 8/8 on chained decoys, byte-identical
stdout) was then discriminated by SEPARATED (on re-teach families H5R2
anchors to the older live fact 8/8 (SEP-OLD) while NEWEST-LIVE-ON-KEY
anchors to the newer 8/8 (SEP-NEW); pre-registered favored arm: NEWEST).

Mandatory boundary attached to this ruling: H5R2 owns only the frozen
battery's scope. What t2_prov_ok demonstrably is: a stale-superseded
anchoring filter (licenses only candidates whose licensing facts are
live tag-1 non-superseded), which beats recency, no-gate, and chance
and holds 46/46 on the built-in battery where pure recency regresses to
45/46. What it is not: a general provenance policy. Its oldest-first
tie-breaking among live facts is a creation-order artifact of forward
node-id enumeration with no independent justification in the lanes'
evidence; on a re-teach the gate re-derives from stale knowledge. The
re-teach gap is a named open gap. Citation of H5R2 as "provenance policy
correct" or "stale provenance is fixed" without naming the re-teach gap
is disallowed. Any next gate must pass the union of the frozen families
and the separator family, or the scope must be narrowed publicly (the
H5R2-SYNTHESIS next hypothesis: newest-live tie-breaking among all live
licensing facts).

---

## Q6. ARENA5: does NARROW undermine BUILD-PASS?

**Ruling: UPHOLD (bounded scope).**

All 8 frozen kill bars hold and were independently reproduced
(RT-ARENA5: byte-identical binary hash, 3/3 stripped streams and traces,
surgical ablations, commit order b63f80289 < f3320caf8 < 2320c3454 <
6582398e9). K1: C15 0.947 >= 0.900 on the fresh sealed 68-item battery.
K2: zero regressions (54.947/68). K6: ablation causal (roster off ->
C15 0.000). K7: 174 lines added, 0 removed/changed; zero goal-string
branches (zero "listnames" hits in the mechanism source; fires on
content-free bare prompts like "x"); zero modes/bridges/routers/gates/
semantic cases. K8: L3 explicitly disclaimed. CANDIDATE only; canonical
0.573 unmoved.

The NARROW (ARENA-GEN, verified by ARENA-GEN-VERIFY: AG-1 PASS
reproducing 0.947; AG-2 FAIL at 5/7; AG-3/4/5 PASS) establishes that
DEFRECALL fires for every bare prompt with dispatch miss and non-empty
roster, including "whattime" and bare "invent" where enumeration is
inappropriate. RT-ARENA5 had already bounded the generality evidence:
on the sealed battery the default action is extensionally equivalent to
a listnames handler (exactly one bare prompt of 68); the generality
evidence is intensional (source audit) plus dev probes, and the dev-probe
demonstration was one-sided.

The decisive point: discriminating generality was never preregistered
as a kill bar. ARENA5's prereg K7 demanded only no goal handlers, and
that bar is clean. Judging BUILD-PASS by a bar the lane never froze
would itself be a governance violation. The NARROW bounds the
interpretation; it does not falsify any measurement and does not refute
the intensional claim (zero goal-string branches still holds).

The supported bounded claim: DEFRECALL is a content-blind structural
trigger (dispatch miss AND bare prompt AND non-empty roster) that
volunteers experience-built persistent knowledge, causally tied to the
roster (K6), honest about absence (empty roster yields UNKNOWN, no
hallucination), zero regressions, L2 goal infrastructure, CANDIDATE
only. The words "general default action" in the cognitive sense are
untenable without the discrimination result in ARENA-SYNTHESIS section
4 (enumerate on listnames/recall/who while abstaining on
whattime/invent with adversary-supplied negatives, via general machinery
or learner-created discrimination, preserving K2/K6/K7 quality).

---

## Q7. CONTLEARN: does MACHINERY-DEPENDENT overturn BUILD-PASS?

**Ruling: UPHOLD (bounded). Binding citation discipline.**

CONTLEARN's BUILD-PASS stands on its frozen K0-K6 bars, all met: K4a
unsupervised store 13/13 across 7 family-B + 6 family-C MAPs with zero
answer keys; K4b unsupervised masked reuse 20/20 across 3 task families;
K4c in-arena deletion ablation drops original-value reuse to 0/20 while
successor retrieval stays 20/20; K4d nostore control 20/20 true misses;
K3 2021pdt cl_driver re-run 3/3, REUSE_COUNT 30/30 retained; K5 UNCERT
count 0; K6 3/3 byte-identical per mode; prereg frozen alone (408ffdcdc),
implementation strict descendant (dfcd3caf1), frozen core untouched,
cognition-source delta 0/0/0, no new modes/bridges/handlers. RT-INT:
EVIDENCE-HOLDS with carried qualifications.

The verdict document stated its scope explicitly: the workspace is
owned in the weak H10 sense (resident in the learner's arena,
manipulated only through the frozen event interface); the strong sense
was not claimed. CONTLEARN-OWNED and CONTLEARN-OWNED2 (doubly confirmed,
3/3 byte-identical, independent replication with amended prereg) measured
MACHINERY-DEPENDENT on the identical disclosed battery: 0/6 with the
event-triggered trial/promotion/P-INV machinery disabled vs 6/6 with it;
standing retrieval intact in TREAT (6/6), proving a capability gap, not
breakage; zero MAPs ever constructed (DEPC == GUIDEC at 6/12/18; only
guide-to-UNCERTAINTY edges ever written). LEARNER-MECH / MECH-VERIFY
(CONFIRMED x3 against the frozen bytes) root-caused it: initiation is
event-only; control parameters bypass learner state; the miss path
hardcodes escalation.

Per CONTLEARN-OWNED's verdict: "the strong sense (the learner decides
or authors) is now measured absent, not merely unclaimed." The
discrimination therefore falsifies only the strong reading, which
CONTLEARN never claimed. Retiring or renaming a verdict whose bars were
met and whose scope was honestly stated would rewrite history; the
honest instrument is citation discipline, binding from this ruling:

LEARNOWN-DEMONSTRATED may be cited only in the bounded form
"LEARNOWN-DEMONSTRATED (machinery-enabled scope; strong sense measured
absent, CONTLEARN-OWNED/OWNED2)". It evidences learner-owned
responsiveness and storage within the frozen interface (the weak H10
sense), not learner-authored integration. Any citation of the label
without the bounded form is disallowed, given the label hazard carried
by RT-INT. The K3 result (REUSE_COUNT 30/30 retained) is cited
unconditionally. The TNN-3 open question (initiation-from-state,
control-from-state, trigger-from-state, white-box initiation) is the
genuine next work; no further machinery-disabled replications are
needed (OWNED-SYNTHESIS section 9).

---

## Q8. CONSEQ and CONTLEARN qualifications: qualified citation or stripped?

**Ruling: UPHOLD qualified citation, with binding citation forms.**

CONSEQ VALIDATION-PASS: independent re-execution of the frozen Node2-v2
K-H3 prereg (4b05c8011); 5/5 kill bars PASS; 3/3 byte-identical; hashes
match committed records bit for bit; causal ablations on Link 1
(consequence record disabled: default reverts to fixed 30) and Link 3
(production read disabled: guide stays 30) both NECESSARY. RT-INT:
EVIDENCE-HOLDS, no dissent.

Stripping advancement entirely would treat a successful independent
reproduction with causal ablations as zero information, which the
evidence does not support: the ablations show the consequence record
is causally necessary for the behavior, which is exactly what the
shared-consequence-substrate hypothesis predicts. The carried
qualifications define the citation boundary: (a) this wave confirms
reproduction fidelity, not adversarial validation; the
independent-adversary clause was never met (builder-sealed worlds), and
it defines the next experiment; (b) the consequence record is a
researcher-written 3-revelation counter, inside the frozen claim bounds
but still researcher-authored; (c) scope honestly held: it validates
the consequence re-entry template, not the shared tag-61 substrate
itself; (d) C174 is validated separately, in dev-harness scope only
(bar (c) = shared-code fallback per RT-C174; bar (d) = K-H3-world
compat; thresholds/weights are researcher scaffolding; broader worlds
untested).

Binding citation form for CONSEQ: "reproduction-fidelity evidence with
causal ablations for the consequence re-entry template; adversary
clause open; builder-sealed worlds." Citation as validation of the
shared tag-61 substrate itself is disallowed until C174's broader-world
validation exists.

CONTLEARN's qualifications are governed by the Q7 ruling: the
LEARNOWN-DEMONSTRATED label survives only in the bounded citation form,
with the weak/strong distinction attached (masked queries remain
researcher scaffolding, per RT-INT). The K3 result is cited
unconditionally.

Under these binding forms, citing either result as advancing its parent
hypothesis is allowed; citing either beyond the stated boundary is
disallowed.

---

## Summary of rulings

| Q | Question | Ruling |
|---|---|---|
| 1 | F1: BUILD-FAIL or PARTIAL | UPHOLD BUILD-FAIL (trigger preserved via F1-FOLLOWUP Part 1, the correct channel) |
| 2 | H-PI-REV2: qualifications or narrowing | OVERTURN (further narrowing): bound on rank-diagnosable single conflicts, probe-dependent trip; ADV-S4/M1 the known envelope |
| 3 | ARENA2 vs ARENA3 | UPHOLD independent standing; no subsumption; C9 finding preserved; composition a later experiment |
| 4 | E3 mandate scope | OVERTURN (narrow mandate): blind re-test for selection-step claims; A1-A6 audit (performed, not assumed) clears single-candidate mechanisms |
| 5 | H5R2 vs SEPARATED | UPHOLD (scope-standing) with mandatory scope boundary: superseded-anchoring fix only; re-teach gap named; no general provenance-policy citation |
| 6 | ARENA5 vs NARROW | UPHOLD (bounded scope): bars met, no bar moved; "general default action" untenable without discrimination result |
| 7 | CONTLEARN vs MACHINERY-DEPENDENT | UPHOLD (bounded): binding citation form "LEARNOWN-DEMONSTRATED (machinery-enabled scope; strong sense measured absent)" |
| 8 | CONSEQ/CONTLEARN citation | UPHOLD qualified citation with binding citation forms; adversary clause (CONSEQ) and weak/strong distinction (CONTLEARN) mandatory |

## Escalation note for the parent

Nothing in these rulings changes the protected-core boundary or creates
an irreversible architecture commitment, so no governance escalation is
triggered by the judging itself. The Q2 narrowing and Q5 scope boundary
are the two rulings most likely to affect what future lanes may cite;
both are recorded with their citation forms above.
