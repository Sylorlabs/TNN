# DEBATE_MATERIALS.md: materials package for the mandatory debate group

Lane: DEBATE-PREP2 (replacement materials worker), wave-20261001-2321pdt.
Working copy: ~/workspace/tnn-rsi, branch tnn-native-lab. All commits
local only, never pushed.

Purpose: this is the single package the debate group (advocate,
skeptic, judge) works from. It lists the 8 adjudication questions
from DEBATE-SLATE/DEBATE_SLATE.md, and for each question gives the
verdicts involved, the key evidence files, and the synthesis
documents to read. It also carries the skeptic's verbatim provenance
probe, the 5 RT-GOV governance decisions (which are EXCLUDED from
debate and go to Micah), the mandatory reading list, and role
checklists.

Compiling lane: DEBATE-SLATE. Source slate:
docs/lab/rsi/runs/wave-20261001-2321pdt/DEBATE-SLATE/DEBATE_SLATE.md.
This package adds no experiments, no new verdicts, and advocates no
position. Lane dirs referenced live under
docs/lab/rsi/runs/wave-20261001-2321pdt/<LANE>/.

---

## PART 1: THE 8 ADJUDICATION QUESTIONS

### Q1. F1: uphold BUILD-FAIL, or narrow to PARTIAL?

**The question.** Should the F1 verdict stand as a whole-candidate
BUILD-FAIL, or should it be narrowed to a PARTIAL verdict covering
the windowed trigger component, with the constructor seed-sensitivity
filed as a separate finding?

**Verdicts involved.**
- F1: BUILD-FAIL (frozen bar K-C0C-REG tripped at 0/30 hidden on
  R-W2; bar not weakened). Commits: prereg 50de69403, implementation
  ba5ebbf8b (binary 6f2b155b...), sealed eval 3b159b401, judge-brief
  14fdf441d.
- F1-FOLLOWUP Part 1: BUILD-PASS (new candidate; explicitly NOT a
  verdict change to the F1 BUILD-FAIL). Commits: 001fcfaca (Part 1
  prereg) -> 6dee24671 (Part 2 prereg) -> 34960a9bc -> 63922a500 ->
  27116eb12 -> 728e114f2; commit-order holds.
- F1-FOLLOWUP Part 2: NOT-FOUND (no whole-fixture property separates
  overfit from correct seeds).
- F1-BUFFER: BUFFER-NOT-PREDICTIVE (commit 451823613).
- F1-REPAIR: GREEDY-CONFIRMED with a trace-verified nuance. Commits:
  b4afb6236 (prereg alone) -> fadaee3fb -> cbded055d -> 5935c5169 ->
  4c253fb36.
- F1-REPAIR2: REPAIR2-CONFIRMED (prereg b4dfa3f32; S-prime 27/27
  across three series).
- RT-EXEC: EVIDENCE-HOLDS on F1 and TNN3H5R; recommendation UPHOLD
  BUILD-FAIL, PARTIAL-narrowed rejected. Review commit 76b9ee229.

**Key evidence.** Trigger bars all PASS (fires on all 4 interleaved
patterns where the old trigger fired 0 times; 0 false positives on 3
clean worlds; 30/30 learning on interleaved streams; ablations
57pp/57pp). The killing evidence is PROVEN STRONGLY to be a
pre-existing constructor limitation, not a trigger regression: the
prior wave's frozen binary on the same sealed fixtures converges to
the byte-identical overfit structure (TRIGGER at ep 1, same 3
constructs, 30/30, identical [4 4 4 2] structure) and scores 0/30.
The worker honestly owns a bar-calibration mistake: its K-C0C-REG bar
used an unvalidated fresh seed, conflating trigger regression with
constructor seed-robustness. F1-FOLLOWUP Part 1 then passed all frozen
bars on validated fixtures with zero trigger regression (byte-identical
normalized CONSTRUCT sequence on the prior wave's W2 fixtures).
RT-EXEC's procedural case: PARTIAL is not a defined verdict in the
frozen rules; inventing one post-hoc would be bar-weakening, exactly
the move Micah's red lines forbid; the frozen candidate was trigger
plus constructor on the same fixtures.

**Synthesis documents to read.** DEBATE-SLATE/DEBATE_SLATE.md Q1
section (uphold vs overturn meanings fully stated there). Key lane
files: F1/ judge brief, F1-FOLLOWUP/ verdict docs, RT-EXEC/ review.

**What the group must decide.** Uphold whole-candidate BUILD-FAIL
(the windowed trigger is not promoted; re-test proceeds only as a NEW
candidate), or narrow to PARTIAL (trigger component PASS, constructor
seed-sensitivity a separate finding). Note the precedent question:
is post-hoc narrowing legitimate when the failure is proven to lie
in a component the lane did not change?

### Q2. H-PI-REV2: qualifications, or further narrowing?

**The question.** Should H-PI-REV2 keep BUILD-PASS with explicit
qualifications attached, or should the claim be further narrowed?

**Verdicts involved.**
- HPIREV2: BUILD-PASS (narrowed single-conflict claim, step-7
  bounding; all frozen bars K-SC-W1..W5, K-SC-B, K-ARCH1/2 PASS on 5
  fresh sealed worlds A2/B1/B2/C2/D2; step-7 FAIL-with-bounding
  untouched). Commits: prereg 00b31af53 (alone), implementation
  ec52cf1ca.
- RT-HPIREV2 Part 1: QUALIFY (BUILD-PASS stands on the five worlds
  under the frozen bars as written). Commits: seal 8b86b27d2,
  erratum 1c40232af, review 5f53f1c7a.
- RT-HPIREV2 Part 2: adversarial bound PARTIALLY survives (ADV-S1/S2/S3
  PASS; ADV-S4 BREAK CONFIRMED; ADV-M1 SILENT SUCCESS CONFIRMED;
  ADV-M2 explicit trip CONFIRMED).

**Key evidence.** Q1: certification defect, not experimental (24/25
sealed files match prereg hashes; D2_FW.txt has a 62-char truncated
hash line in the prereg, a transcription typo; the lane's "25/25
verified, all match" sentence is not literally true). Q2
(load-bearing): all five worlds accommodate the frozen rank-biased
diagnosis by disclosed pre-freeze design (D2's design note admits
tuning RW to match both declared and diagnosed conflicts); the
narrowed claim as literally stated was never tested against a
conflict the rank bias does not select. The adversarial family ran
the frozen mechanism byte-verbatim: ADV-S1/S2/S3 pass (the bound
generalizes to fair structures); ADV-S4 is a CONFIRMED BREAK (a valid
single-conflict world per V0-V3 whose true trigger (2,66) the rank
bias cannot select: fails_total=1); ADV-M1 shows a masked second
conflict is silently never flagged (fails=0, zero detection); ADV-M2
shows an explicit trip when the uncovered conflict is probed alone.
The bound-trip signal is PROBE-DEPENDENT: explicit when the
uncovered conflict is probed alone, silent when masked. The reviewer
recommends restating the narrowed claim with an explicit
rank-diagnosability qualifier and the bound-trip half with a
probe-dependence qualifier. World non-independence was disclosed, not
hidden.

**Synthesis documents to read.** DEBATE-SLATE/DEBATE_SLATE.md Q2
section. Key lane files: HPIREV2/ sealed eval, RT-HPIREV2/ review
and adversarial family.

**What the group must decide.** BUILD-PASS-with-qualifications (claim
restated with rank-diagnosability and probe-dependence qualifiers;
ADV-S4 bounds the qualified claim rather than falsifying it), or
further narrowing to "the bound holds on rank-diagnosable single
conflicts with probe-dependent trip signaling" (ADV-S4 read as
falsifying the narrowed claim as originally stated; citing the claim
without both qualifiers disallowed).

### Q3. ARENA2 REMAP vs ARENA3 TRX: sibling collision

**The question.** Two independent lanes both built C12 transfer
candidates. How should the debate group reconcile the two mechanisms:
independent standing claims, composition, or subsumption?

**Verdicts involved.**
- ARENA2: BUILD-PASS (REMAP, on the v6 base). Commits: prereg
  5a055b575 (alone), implementation+eval 18309290c.
- ARENA3: BUILD-PASS (TRX, on the INQ base). Commits: prereg
  829208f99 (alone), implementation 9191e71de, eval records in
  d51d8ef5b.
- Both disclaim L3. Per the frozen collision clause, these are
  independent competing runs, not duplication (ARENA2's dir was empty
  at ARENA3's start; assumption recorded pre-build).

**Key evidence.** REMAP: C12 0 to 1, arena total 0.794 to 0.882
(60/68) on the v6 base; composes the learner's own exposure-learned
Zem templates with the runtime-parsed value permutation (no sealed
values hardcoded; claims generalization to any permutation/template);
+94/-0 lines, zero new modes/bridges/routers/gates/semantic cases;
ablations zero exactly each half (both halves causal). TRX: C12 0 to 1
(6/6), total 0.853 to 0.941 (64/68) on the INQ base; parse_remap parses
the 4-value segment relabeling from the question (validates permutation
of [0,1,2,3]); remap_prod applies the learned class-A to class-B
position-wise rewrite then the parsed remap; remap always from the
question, never source/state; +80/-0 lines; ablations 3/6 each half
(both halves causal). The scores are not directly comparable
(different bases: v6 vs INQ; REMAP's denominator includes no inquiry
gain). Also in the record: ARENA2 produced the C9 negative finding
(the causal battery is observationally unidentifiable by design; only
gaming passes; fix recommendations recorded), a genuine contribution
independent of the transfer claim. Neither candidate is cumulative with
the inquiry candidate; canonical 0.573 is unmoved; integration is an
open later decision.

**Synthesis documents to read.** DEBATE-SLATE/DEBATE_SLATE.md Q3
section. Key lane files: ARENA2/ and ARENA3/ lane dirs (judge briefs,
sealed evals).

**What the group must decide.** Independent standing (compare
generality: REMAP's any-permutation claim vs TRX's [0,1,2,3]-validated
parsing; consider composition, e.g. REMAP on the INQ base; preserve
the C9 finding as ARENA2's independent contribution), or subsumption
(one mechanism generalizes or contains the other; name the survivor,
record the locus of any lost generality, and say which base the
survivor integrates against).

### Q4. BATTERY-E3: scope of the blind re-examination mandate

**The question.** Which construction claims must be re-examined blind
under the E3 mandate, and which are cleared?

**Verdicts involved.**
- BATTERY-E3: E3-ORACLE-DEPENDENT (debate priority). Commits:
  a17a276c8 (prereg alone) -> ce46b327a (implementation) ->
  4f49f8b66 (12 sealed runs + judge brief).
- BATTERY-CLUSTER: COMPLETE; the 1/6 post-freeze signatures; H1d
  refined per E3.
- CLUSTER-FINAL: H1d SUPPORTED in refined form (assembly real,
  selection oracle-dependent); E3 mandate stands.
- ARENA-BLIND: ORACLE-FREE for the ARENA4 ROSTER mechanism (E3 mandate
  satisfied for ROSTER by audit, no masked re-test triggered).
  Commits: 0b95a6601 (prereg) -> c2eb08c2a (audit + verdict).

**Key evidence.** Blind E3B (discriminating, spurious-first
adversarial): 0/2, outputs exactly the pre-registered spurious
composites [80971, 80972] vs sealed targets [80921, 80922];
oracle-present E3B: 2/2. The white-box inspector confirms the blind
trial runtime-assembled GUARD/SETREG chain graphs with ET_DEP
provenance to the taught spurious facts, promoted them as MAP nodes,
and executed them. ASSEMBLY WORKS BLIND; SELECTION DOES NOT. The
trial's correct compositions depended on the unmasked verifier
(t2_try_verify: accept iff output equals the QUERY-carried expected
value) to SELECT among multiple executable BFS chains; without the
oracle, masked mode emits the first-executable chain. This REFRAMES
EVERY PF CONSTRUCTION OBSERVATION as BFS enumeration plus oracle
selection, not selective construction. E3's own confound note flags
BATTERY-E1's W4 behavioral leg (structure-driven answers vs
oracle-verified BFS traversal indistinguishable). ARENA-BLIND audited
ROSTER against six frozen criteria (A1-A6): zero oracle fields in
test turns; the listnames turn carries only (item, cap, q); the frozen
ROSTER source parses only item/cap/q; no candidate set and no
selection step exist (single candidate: the roster enumeration);
ROSTER never emits OBSERVE requests. Per the frozen decision rule,
ORACLE-FREE means the masked re-test branch is not triggered: the C15
claim never rested on unmasked QUERY evidence.

**Synthesis documents to read (mandatory).**
- CLUSTER-FINAL/CLUSTER_FINAL.md (Cluster 1 and 2 final
  discrimination program, E1-E6 plus E8; DERIVATION SUBORDINATION
  and GUIDE CONTENT DECOUPLING as decided measured properties).
- CLUSTER-FINAL/JUDGE_BRIEF.md.
- DEBATE-SLATE/DEBATE_SLATE.md Q4 section.
- Evidence paths: BATTERY-CLUSTER/CLUSTER_ANALYSIS.md,
  BATTERY-E1/E1_RUN.md through BATTERY-E8/E8_RUN.md and their
  JUDGE_BRIEF.md files, BATTERY-E3/E3_RUN.md.

**What the group must decide.** Broad mandate (every wave construction
claim resting on unmasked QUERY evidence must be re-examined blind:
the PF-A/PF-C battery results, the E1-W4 behavioral leg, and any
prior-wave construction evidence on unmasked QUERY; PF-A2's 2/2
valid-composition result re-described as BFS enumeration plus oracle
selection), or narrow mandate (applies only to claims with a
structural selection step among multiple candidates; single-candidate
mechanisms like ROSTER are categorically cleared via the ARENA-BLIND
audit template; no blanket re-examination required).

### Q5. H5R2: does SEPARATED undermine BUILD-PASS?

**The question.** Does the SEPARATED verdict undermine H5R2's
BUILD-PASS, or does BUILD-PASS stand within its scope?

**Verdicts involved.**
- TNN3H5R: BUILD-PASS, H5R2 ADVANCES (KB-W0 36/36, KB-W2R 12/12
  recovering the killed 8/12 bar, KB-B2R 24/24, KB-W3 8/8 new
  two-revision family, KB-B3 24/24; 9-line t2_prov_ok helper gating
  four promote sites). Commits: prereg dc7df4aba, implementation
  9db334bd4 (binary 19dcf2e4...), sealed eval e20ba5402.
- H5R2-REPRO: REPRO-PASS (independent reproduction, pipeline step 4).
  Commit 8b30769de.
- H5R2-BASELINE: BASELINE-MATCHES (REVERT-TO-LATEST recency matches
  H5R2 on all five bars of the same four sealed worlds; CB-2
  violated; gate not shown necessary there; honest cost: recency
  regresses the built-in battery to 45/46 while H5R2 holds 46/46).
- H5R2-DECOY: DECOY-DISCRIMINATES (gate anchors 8/8 to the live older
  fact while recency anchors 8/8 to the decoy; BASELINE-MATCHES
  RESOLVED, not contradicted).
- H5R2-SKEPTIC2: SKEPTIC-SURVIVES (NEWEST-LIVE-ON-KEY matches H5R2
  8/8 on chained decoys, byte-identical stdout; gate necessity
  unproven vs the stronger skeptic).
- H5R2-SKEPTIC3: SEPARATED (on re-teach families H5R2 anchors to the
  older live fact 8/8 (SEP-OLD) while NEWEST-LIVE-ON-KEY anchors to
  the newer live fact 8/8 (SEP-NEW); pre-registered favored arm:
  NEWEST).
- RT-EXEC: EVIDENCE-HOLDS on TNN3H5R (review commit 76b9ee229).

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
newest. Under the standard belief-revision reading (the second teach
is an update without contradiction, and the protocol's own
contradiction behavior leaves the newest fact live), NEWEST is the
pre-registered favored arm. The gate's oldest-first pick is a
creation-order artifact of forward node-id enumeration, not a
provenance principle: both facts are live, so the gate's own "a
superseded fact licenses nothing" rule cannot discriminate them. On
a re-teach, the gate re-derives from stale knowledge. On every frozen
family the gate's promoted candidate coincides with
NEWEST-LIVE-ON-KEY's; the re-teach family was constructed precisely
to break that coincidence and lies outside the frozen battery's event
sequences (the battery never leaves two live facts on one key).
Every arm failure across all four lanes is provenance-only (D-ANS/VAL
8/8 on all arms everywhere). The open design question: a gate
strictly stronger than both (provenance filter plus newest-live
tie-breaking among all live licensing facts) is buildable and
testable but was not built in any lane.

**Synthesis documents to read (mandatory).**
- H5R2-SYNTH/H5R2_SYNTHESIS.md (the four-gate-verdict arc; what
  t2_prov_ok IS and IS NOT; the precise open question on the
  strictly-stronger gate).
- DEBATE-SLATE/DEBATE_SLATE.md Q5 section.
- Key lane files: TNN3H5R/, H5R2-REPRO/, H5R2-BASELINE/,
  H5R2-DECOY/, H5R2-SKEPTIC2/, H5R2-SKEPTIC3/ (EVAL files; all report
  3/3 byte-identical runs with recorded SHA-256 hashes).

**What the group must decide.** Scope-standing (BUILD-PASS was
awarded against the frozen KB-W2R/KB-W3 families; SEPARATED does not
retroactively move the H5R2 bars; the re-teach gap is named as an
explicit open gap; any next gate must pass the union of the frozen
families and the separator family, or the scope is narrowed
publicly), or counterexample-in-scope (the claim "stale provenance is
fixed" is violated by the re-teach world; the BUILD-PASS claim must
be narrowed with the re-teach gap named, or it cannot be cited as a
provenance-policy result).

### Q6. ARENA5: does NARROW undermine BUILD-PASS?

**The question.** Does the ARENA-GEN NARROW undermine ARENA5's
BUILD-PASS, or does BUILD-PASS stand within its bounded scope?

**Verdicts involved.**
- ARENA5: BUILD-PASS (DEFRECALL; C15 0.947 on the fresh sealed
  68-item battery, all 8 frozen kill bars pass; CANDIDATE only; L3
  disclaimed; canonical 0.573 unmoved). Commits: b63f80289 (prereg)
  -> f3320caf8 (Amendment 1: seed validity rule) -> 2320c3454
  (implementation, defrecall_contestant.zag) -> 6582398e9 (sealed
  eval + judge brief).
- RT-ARENA5: QUALIFY (BUILD-PASS stands; the qualification is
  bounded: on the sealed battery the generic default action is
  extensionally equivalent to a listnames handler, because exactly
  one of the 68 items is a bare prompt). Commit-order self-check:
  b63f80289 < f3320caf8 < 2320c3454 < 6582398e9.
- ARENA-GEN: NARROW (verified by ARENA-GEN-VERIFY: AG-1 PASS
  reproducing 0.947; AG-2 FAIL at 5/7; AG-3/AG-4/AG-5 PASS; the two
  AG-1/AG-3 turn files uncommitted, so those bars were not
  recountable, but the NARROW's load-bearing claims all hold).

**Key evidence.** The multi-bare-prompt battery (7 items, fresh
entities Alpha through Iota) required enumerate on listnames / recall
/ who and UNKNOWN on whattime / bare invent / invent|notation /
foo|bar. The default action fired for EVERY bare prompt with dispatch
miss and non-empty roster: five defrecall firings for five bare
prompts, including "whattime" (the learner has no clock; the roster is
not the time) and bare "invent" (an incomplete invention request; the
roster is irrelevant). The mechanism is, extensionally, a
"bare-prompt handler", not a general default action: generality is
real in scope (all bare prompts, not one goal string) but shallow in
content (no discrimination between appropriate and inappropriate
enumeration). ARENA5's dev-probe demonstration was one-sided: it
tested only prompts where enumeration is appropriate and counted the
behavior as generality. RT-ARENA5 had already shown the sealed battery
cannot discriminate a truly general default from a renamed handler
(one bare-prompt item in 68); the source audit showed intensionally it
is not a handler (zero goal-string branches, proven by grep and by
firing on content-free bare prompts like "x"). What NARROW does NOT
refute: ARENA5's intensional claim (zero goal handlers still holds)
and its frozen bars (all met, no bar moved, all evidence independently
reproduced). Crucially, discriminating generality was never
preregistered as a kill bar: ARENA5's prereg K7 demanded only no goal
handlers, and that bar is clean. Judging BUILD-PASS by a bar the lane
never froze would itself be a governance violation.

**Synthesis documents to read (mandatory).**
- ARENA-SYNTH/ARENA_SYNTHESIS.md (the PASS -> QUALIFY -> NARROW
  progression; the precise bounded DEFRECALL claim in section 3;
  what lifting the NARROW would require in section 4).
- DEBATE-SLATE/DEBATE_SLATE.md Q6 section.
- Key lane files: ARENA5/, ARENA-GEN/, ARENA-GEN-VERIFY/ (lane dirs
  with the sealed battery, per-prompt traces, and the binary hash
  matching ARENA5's sealed build).

**What the group must decide.** Bounded scope (BUILD-PASS is valid
on its frozen bars and is not retroactively re-graded; the supported
bounded claim is DEFRECALL as a content-blind structural trigger that
volunteers persistent knowledge, causally tied to the
experience-built roster; the words "general default action" are
untenable without the discrimination result), or overturn (the
autonomy claim carries less meaning than the language suggested; a
PASS that depended on never testing negative cases is a PASS within
a scope the battery defined; DEFRECALL may not be cited as general
default-action evidence until a discriminating trigger is
demonstrated).

### Q7. CONTLEARN: does MACHINERY-DEPENDENT overturn BUILD-PASS?

**The question.** Does the machinery-disabled discrimination overturn
CONTLEARN's BUILD-PASS, or does BUILD-PASS stand within the
machinery-enabled scope? What citation discipline applies to
LEARNOWN-DEMONSTRATED going forward?

**Verdicts involved.**
- CONTLEARN: BUILD-PASS, LEARNOWN-DEMONSTRATED (frozen K0-K6 all
  PASS: K4a unsupervised store 13/13 across 7 family-B + 6 family-C
  MAPs with zero answer keys; K4b unsupervised masked reuse 20/20
  across 3 task families; K4c in-arena deletion ablation drops
  original-value reuse to 0/20 while successor retrieval stays
  20/20; K4d nostore control 20/20 true misses; K3 2021pdt cl_driver
  3/3 re-run, REUSE_COUNT 30/30 retained; K5 UNCERT count 0; K6 3/3
  byte-identical; K0-K2 prereg frozen alone, frozen core untouched,
  pure Zag, cognition delta 0/0/0, no new modes/bridges/handlers).
  Commits: prereg 408ffdcdc, implementation dfcd3caf1.
- CONTLEARN-OWNED: MACHINERY-DEPENDENT (0/6 vs 6/6 on a fixed
  disclosed battery of fresh 2-hop chains; STORE_OK 0/6 vs 6/6,
  REUSE 6/12 vs 12/12, DELAYED 6/12 vs 12/12; zero MAP nodes at every
  phase).
- CONTLEARN-OWNED2: MACHINERY-DEPENDENT, independently replicated
  (discarded pilot, amended prereg).
- LEARNER-MECH: root-cause analysis (frozen core blob hash pinned).
  Key file: LEARNER-MECH/LEARNER_MECH_ANALYSIS.md. (MECH-VERIFY
  notes a transcription error: the printed SHA-256 is 79 characters;
  the correct value is
  a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd;
  the git blob hash is correct and pins the exact bytes analyzed, so
  no claim is affected.)
- MECH-VERIFY: CONFIRMED x3 (initiation event-only, control bypasses
  learner state, miss path hardcodes escalation). Key file:
  MECH-VERIFY/MECH_VERIFY_REPORT.md.
- RT-INT: EVIDENCE-HOLDS on CONTLEARN with carried qualifications
  (label hazard; keep the weak/strong distinction attached when
  cited). Review commits f70c676f4, 6c8485fdc.

**Key evidence.** On the identical disclosed battery, the continuing
learner integrates 0/6 with the event-triggered trial/promotion/P-INV
machinery disabled and 6/6 with it. Standing retrieval of taught
1-hop facts is intact in TREAT (6/6), proving a capability gap, not
breakage. The learner's own mechanisms demonstrably respond to new
experience (6/12/18 UNCERTAINTY+guide pairs accumulate), but that
response never recurses into integration: no mechanism reads the
guides to build anything, and zero MAPs are ever constructed (DEPC
equals GUIDEC at 6/12/18: the only learner-side edges ever written
were guide-to-UNCERTAINTY links). LEARNER-MECH, verified against the
frozen bytes: (a) initiation is event-only (mp_run, t2_trial,
t2_try_verify, promote_graph, bootstrap_miss reachable only from the
four researcher-invoked event handlers or self-tests; learner state is
read as DATA, never as CONTROL; nothing in state can gate, enable,
defer, retry, or redirect the trial loop); (b) control parameters
bypass learner state entirely (mp_run derives control bits and accept
oracle from event flags/expected; the "learner-set miss policy"
comment is inaccurate as control-flow description; mp_run never reads
the mp slot); (c) the miss path hardcodes escalation (ev_query runs
trial -> bootstrap -> inquire on miss with no branch keyed on learner
state). CONTLEARN's own verdict document stated the scope explicitly:
the workspace is owned in the weak H10 sense, and the strong sense
was not claimed. The machinery-disabled lanes upgrade that scope
statement: per CONTLEARN-OWNED, "the strong sense (the learner
decides or authors) is now measured absent, not merely unclaimed."
RT-INT: removing answer keys kills the key-matching confound but does
not escape scaffolding (masked queries remain researcher
scaffolding).

**Synthesis documents to read (mandatory).**
- OWNED-SYNTH/OWNED_SYNTHESIS.md (the five-verdict synthesis; the
  supersession that bounds LEARNOWN-DEMONSTRATED; the mechanism gap;
  the constitution's learner-authority reading; the TNN-3 open
  question on learner-initiated construction).
- DEBATE-SLATE/DEBATE_SLATE.md Q7 section.
- Key lane files: CONTLEARN/ (VERDICT_LEARNOWN.md,
  PREREG_LEARNOWN.md), CONTLEARN-OWNED/ (VERDICT_OWNED.md,
  PREREG_OWNED.md), CONTLEARN-OWNED2/ (VERDICT_OWNED2.md,
  PREREG_OWNED2.md plus erratum), LEARNER-MECH/
  (LEARNER_MECH_ANALYSIS.md), MECH-VERIFY/ (MECH_VERIFY_REPORT.md).

**What the group must decide.** Bounded (the measurements in
CONTLEARN are true of the machinery-enabled core, and the
discrimination falsifies only the strong reading, which CONTLEARN
never claimed; BUILD-PASS stands within the machinery-enabled scope;
citation discipline going forward: LEARNOWN-DEMONSTRATED is cited only
in the bounded form "LEARNOWN-DEMONSTRATED (machinery-enabled scope;
strong sense measured absent, CONTLEARN-OWNED/OWNED2)"; it evidences
learner-owned responsiveness and storage within the frozen interface
(weak H10), not learner-authored integration), or overturn (the
LEARNOWN-DEMONSTRATED label, now measured to require researcher
machinery for integration, no longer names any learner-owned
capability distinct from the machinery; the verdict is retired or
renamed so it cannot be misread as learner-authored integration).

### Q8. CONSEQ and CONTLEARN qualifications

**The question.** How do the carried qualifications bind citation of
the CONSEQ and CONTLEARN results? Do they stand as qualified
evidence, or must their advancement claims be stripped?

**Verdicts involved.**
- CONSEQ: VALIDATION-PASS (independent re-execution of frozen
  Node2-v2 K-H3 prereg: 5/5 kill bars PASS, 3/3 byte-identical,
  hashes match bit for bit; causal ablations on Link 1 (consequence
  record disabled: default reverts to fixed 30) and Link 3
  (production read disabled: guide stays 30) both NECESSARY). Commits:
  prereg 4b05c8011, eval commits e068ac9a4.
- C174: VALIDATION-PASS (shared tag-61 consequence store graduates
  from EMERGES to validated-on-frozen-bars as infrastructure;
  dev-harness scope). Commits: prereg 134af1cb2 -> implementation
  b5e0274f7 -> seal 0096b30ca -> eval 3028240e4.
- RT-INT: EVIDENCE-HOLDS on CONSEQ and CONTLEARN, no dissent, with
  carried qualifications. Review commits f70c676f4, 6c8485fdc.
- RT-C174: EVIDENCE-HOLDS, no dissent, with carried qualifications
  (bar (c) = shared-code fallback; bar (d) = K-H3-world compat).
  Review commit 89b27a9ce.

**Key evidence.** CONSEQ: this wave confirms reproduction fidelity,
not adversarial validation; the independent-adversary clause was
never met (builder-sealed worlds). The consequence record is a
researcher-written 3-revelation counter, inside the frozen claim
bounds but still researcher-authored. Scope honestly held: it
validates the consequence re-entry template, not the shared tag-61
substrate itself (C174 validated separately, in dev-harness scope
only; broader worlds untested; thresholds/weights are researcher
scaffolding; migration boundary documented). CONTLEARN: masked queries
remain researcher scaffolding, honestly disclosed; the
"LEARNOWN-DEMONSTRATED" label is a hazard; the weak/strong distinction
must stay attached when cited (weak H10 sense: the workspace is the
single frozen arena; no learner-agency claim; no procedure execution
at query time; reuse is exact-hit retrieval via activate). The K3
regression check (REUSE_COUNT 30/30 retained) is solid under either
reading.

**Synthesis documents to read.** DEBATE-SLATE/DEBATE_SLATE.md Q8
section. Red-team reviews RT-INT/ and RT-C174/ (carried
qualifications verbatim). Key lane files: CONSEQ/ (K-H3 eval), C174/
(EVAL_RESULTS.md).

**What the group must decide.** Qualified citation (both results
stand with their qualifications attached as the red teams carried
them: CONSEQ cited as reproduction-fidelity evidence advancing the
shared-consequence-substrate hypothesis toward, not through, the
adversary clause; the adversary clause defines the next experiment;
CONTLEARN cited as learner-owned responsiveness and storage in the
weak H10 sense, with the machinery-enabled scope from Q7; the K3
result cited unconditionally), or stripped advancement (the verdicts
stand as measurements but may not be cited as advancing their parent
hypotheses: CONSEQ does not advance the shared-consequence-substrate
hypothesis until the adversary clause is met; CONTLEARN's
"learner-owned" framing is retired as a citation hazard).

---

## PART 2: THE SKEPTIC'S VERBATIM PROVENANCE PROBE

This probe MUST be asked of every artifact under judgment, by the
skeptic, before any verdict is upheld:

**"What is the provenance of the artifacts under judgment, and what
exactly is new versus inherited?"**

"Inherited" means taken from prior waves, the frozen base, or shared
instruments; "new" means created and evidenced this wave. The prepared
answers below come from DEBATE-PREP/DEBATE_BRIEF.md section 3; the
skeptic must verify each against the committed lane evidence, not take
the answers at face value.

**HPIREV2.** New: the narrowed step-7 single-conflict bound as a
frozen claim; 5 fresh sealed worlds; the bound-trip 3/3 evidence; the
certification (minus the Q1 transcription defect); zero cognition
source delta on this lane. Inherited: the frozen TNN-2 base; the
rank-biased diagnosis machinery and the step-5/6 results from the
prior wave; the step-7 FAIL-with-bounding frame itself. Not claimed:
L3, generality, SURVIVES status.

**CONTLEARN.** New: the learner-owned push evidence (unsupervised
store 13/13, masked reuse 20/20, in-arena deletion ablation, nostore
control), the 2021pdt cl_driver 3/3 re-run with REUSE_COUNT 30/30
retained. Inherited: the frozen arena and core; the prior wave's
INTEGRATION-DEMONSTRATED result (which the prior red team qualified
as machinery integration under per-query supervision); the weak-H10
framing. Researcher scaffolding remains disclosed.

**TNN3H5R (H5R2).** New: the 9-line t2_prov_ok helper and 4 gated
promote sites; the KB-W2R 12/12 recovery (was the 8/12 kill); the new
KB-W3 two-revision family 8/8; the net +9 architecture delta.
Inherited: the frozen battery worlds; the TNN-2 base (cumulative diff
net -4); the H5R kill it repairs. Seal note disclosed: single worker
as coordinator/builder/evaluator with pre-frozen mitigations.

**ARENA2 (REMAP).** New: the REMAP mechanism (exposure-learned Zem
templates composed with runtime-parsed permutation); C12 0 to 1;
60/68. Inherited: the v6 base and the exposure templates it composes.
Bonus new this wave: the C9 negative finding with killing evidence
and generator fix recommendations (a genuine contribution independent
of the transfer claim).

**ARENA3 (TRX).** New: the TRX mechanism (question-parsed 4-value
relabeling applied to learned A/B templates); C12 6/6; 64/68 on the
INQ base. Inherited: the INQ base and A/B exposure templates; the C12
target itself (born of the sibling collision, assumption recorded).
L3 disclaimed; canonical 0.573 unmoved.

**ARENA5 (DEFRECALL).** New: the generic default action replacing
ARENA4's dedicated listnames handler (174 lines; zero goal-string
references; roster-on/action-off ablation proves the default action is
the goal-completion path). Inherited: ARENA4's roster verbatim; the
v6 base; the battery (seed 71503461337032). Caveat disclosed: on this
battery the default action is extensionally equivalent to a listnames
handler; generality rests on intension.

**F1-FOLLOWUP Part 1.** New: the corrected-bar re-test (trigger
reproduces old binary byte-exactly on validated fixtures; zero trigger
regression). Inherited: the F1 windowed trigger; the prior wave's W2
fixtures. Explicitly NOT a verdict change to the F1 BUILD-FAIL; filed
as a new candidate.

---

## PART 3: THE 5 RT-GOV GOVERNANCE DECISIONS (EXCLUDED FROM DEBATE; FOR MICAH)

The debate group does NOT adjudicate these. Per the slate, the group
prepares evidence for and against each, but the decisions are Micah's
alone. Source: RT-GOV/RT-GOV_REVIEW.md, ESCALATION section
(verbatim-ready, review commit 7a1ebe002).

**Decision 1 (Adoption).** "Adopt the 197-line TNN3-SUBSTRATE package
(PKG-BEGIN to PKG-END, sha256
be4e5867ac305ba8ebe190922f7741f6a4c053729f99064354606c146affdff8)
into the TNN-2 lineage's cognition layer, with the specified adoption
diff (lb_run at ev_observe's three returns; ls_bump +1/-1 and lt_fire
hooks; lbid at the four selector sites 145, 259, 872, 884), as the
substrate for the H2R/H4R/H6R/H7R re-attempts? No protected-core
change is requested."

**Decision 2 (Baseline).** "Accept that this changes the frozen
baseline six lanes verified against (frozen tnn2.zag
a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd),
with the pre-package baseline preserved in git history for the sealed
SUBSTRATE-ABSENT findings? Note: once re-attempts freeze their kill
bars against the adopted build, reversing the adoption invalidates
those bars."

**Decision 3 (Standing composition).** "Accept lbid's
record-wins-else-bid composition as the substrate default, with H6R
allowed to propose full replacement semantics under its own bars, or
direct a different composition rule now?"

**Decision 4 (Polarities).** "Accept the +1/-1 confirm/contradict
polarities as fixed machinery (analogous to the existing ET_CFM/ET_CON
self-edges), or require learner ownership of polarity magnitudes
before H6R freezes its bars?"

**Decision 5 (Amendment discipline).** "Accept Amendments 1-2 as
committed inside the prototype commit (evidence is internally
consistent; one-line deletion, bars unchanged), or require future
prereg amendments to re-freeze alone before implementation?"

For each decision the group prepares: the evidence for, the evidence
against, and what changes in the research program if Micah says yes
vs no. Relevant context the group must surface: the H6R BUILD-FAIL
standing-record eviction gap (records never protection-pinned, lbid
0, always evicted before fact nodes) is a crisp substrate design gap
that adoption would inherit; the group should say whether that gap is
a reason to delay adoption or the first repair target after adoption.
The EXECUTE placement ruling (amendments A-C) remains pending and
still gates H4R's B4; the substrate package does not ask for it. Also
note RT-GOV's requested documentation fix: "904 ticket nodes" should
read "type-904 ticket nodes" in ADOPTION_RECOMMENDATION.md section 2.

---

## PART 4: MANDATORY READING LIST

Before debate opens, all three roles read:

1. DEBATE-SLATE/DEBATE_SLATE.md (this package's source; the 8
   questions with verdicts, evidence, and uphold/overturn meanings).
2. DEBATE-PREP/DEBATE_BRIEF.md (the 40-verdict slate, entries 1-42;
   the 7 debates; the provenance answers in section 3; evidence
   paths in the appendix).
3. DEBATE-PREP/JUDGE_BRIEF.md (verdict counts, flags for the group,
   open questions).
4. WAVE_RECORD.md (docs/lab/rsi/runs/wave-20261001-2321pdt/
   WAVE_RECORD.md): the wave's 40 verdict bullets as committed.

Per-question mandatory reads:

- Q1: F1/, F1-FOLLOWUP/, F1-BUFFER/, F1-REPAIR/, F1-REPAIR2/,
  RT-EXEC/ lane dirs.
- Q2: HPIREV2/, RT-HPIREV2/ lane dirs.
- Q3: ARENA2/, ARENA3/ lane dirs.
- Q4: CLUSTER-FINAL/CLUSTER_FINAL.md, CLUSTER-FINAL/JUDGE_BRIEF.md,
  BATTERY-E3/ lane dir.
- Q5: H5R2-SYNTH/H5R2_SYNTHESIS.md, TNN3H5R/, H5R2-REPRO/,
  H5R2-BASELINE/, H5R2-DECOY/, H5R2-SKEPTIC2/, H5R2-SKEPTIC3/ lane
  dirs.
- Q6: ARENA-SYNTH/ARENA_SYNTHESIS.md, ARENA5/, ARENA-GEN/,
  ARENA-GEN-VERIFY/ lane dirs.
- Q7: OWNED-SYNTH/OWNED_SYNTHESIS.md, CONTLEARN/,
  CONTLEARN-OWNED/, CONTLEARN-OWNED2/, LEARNER-MECH/, MECH-VERIFY/,
  RT-INT/ lane dirs.
- Q8: CONSEQ/, C174/, RT-INT/, RT-C174/ lane dirs.

Still-running lanes that may move verdicts: SENSORY (needs red-team
coverage when it lands), LANE-AUDIT, QUAL-SUMMARY (the qualifications
synthesis). The debate records which verdicts it read as of which
commits.

---

## PART 5: ROLE CHECKLISTS

### Advocate checklist

- [ ] For each question assigned, state the exact frozen bars the
  verdict was awarded against (bar names and numbers, not
  paraphrases).
- [ ] Answer the skeptic's provenance probe for every artifact
  BEFORE being asked: what is new, what is inherited, what is not
  claimed.
- [ ] Present the bounded claim the evidence actually supports,
  including the honest caveats already on record (certification
  defects, one-sided dev probes, disclosed seal notes).
- [ ] Cite byte-identity and independent reproduction where it
  exists (H5R2-REPRO, CONSEQ 3/3, ARENA5 3/3, ARENA-GEN-VERIFY).
- [ ] Never reach beyond the frozen bars: if the verdict was earned
  on bars X, do not claim it also proves Y.
- [ ] For Q1: show the corrected-bar evidence (F1-FOLLOWUP Part 1)
  went through the correct procedural channel as a new candidate.
- [ ] For Q5: show the exact frozen scope of the KB-W2R/KB-W3 bars
  and that REPRO-PASS confirmed them.
- [ ] For Q6: show K7 (no goal handlers) is the only generality-adjacent
  bar the lane ever froze, and it is clean.
- [ ] For Q7: show the measurements are true of the
  machinery-enabled core and the strong reading was never claimed.
- [ ] For Q8: show the qualifications were carried by the red teams
  with no dissent, and name the next experiments the qualifications
  define (adversary clause; discriminating trigger).

### Skeptic checklist

- [ ] Ask the verbatim provenance probe for EVERY artifact under
  judgment: "What is the provenance of the artifacts under judgment,
  and what exactly is new versus inherited?" Verify the answers
  against committed evidence; do not accept the prepared answers at
  face value.
- [ ] For each BUILD-PASS, name the strongest alternative
  explanation and check whether the record attacks it: recency
  (Q5), oracle selection (Q4), handler equivalence (Q6),
  researcher-scaffolded integration (Q7), rank-bias accommodation
  (Q2).
- [ ] Check citation discipline: does every citation of a qualified
  verdict carry its qualification in the bounded form (Q2's two
  qualifiers; Q6's intension-only generality; Q7's
  "LEARNOWN-DEMONSTRATED (machinery-enabled scope; strong sense
  measured absent, CONTLEARN-OWNED/OWNED2)"; Q8's carried
  qualifications)?
- [ ] Check that no verdict is cited beyond its frozen scope:
  SEPARATED's re-teach gap, ADV-S4's confirmed break, AG-2's 5/7,
  the decoy lane's limits.
- [ ] Verify prereg-first commit order and seal integrity for every
  verdict you attack; if you find a process defect (truncated hash
  lines, uncommitted turn files, swept commits), name it and say
  whether it is experimental or certification-only.
- [ ] For Q4: demand the per-mechanism audit backlog be named
  explicitly (which claims rest on unmasked QUERY evidence and are
  still unaudited).
- [ ] For Q3: demand the reconciliation answer the mechanism
  question, not just the scores (composition? subsumption?
  independent standing?).

### Judge checklist

- [ ] For each question, record the verdict under judgment, the
  exact frozen bars that governed it, and the commit ids of the
  evidence read.
- [ ] Verify prereg-first commit order (the prereg's first commit
  strictly precedes the implementation's) before treating any
  verdict as eligible.
- [ ] Confirm no bar was weakened to force a pass, and no
  post-hoc verdict class was invented (Q1: PARTIAL is not a defined
  verdict in the frozen rules; inventing one is bar-weakening).
- [ ] Confirm the verdict is not being judged by a bar the lane
  never froze (Q6: judging BUILD-PASS by discriminating generality
  would be a governance violation).
- [ ] Decide per question: uphold, narrow (with the exact narrowed
  claim and citation form recorded), or overturn (with the verdict
  retired or renamed as specified).
- [ ] For each ruling, record: the citation form going forward, the
  known open gaps named, and the next experiment the ruling defines.
- [ ] For the 5 RT-GOV decisions: prepare evidence for and against
  each, and what changes if Micah says yes vs no. DO NOT decide
  them; they are Micah's alone.
- [ ] Resolve or record the H7R/H6R flag: the H7R record states
  "Substrate halves now 3/3 passing (H2R, H6R, H7R)" while this
  wave's H6R lane verdict is BUILD-FAIL; establish whether this is
  a naming collision or a contradiction before it enters any
  citation.

### Shared rules for all three roles

- A verdict names the exact frozen bars that governed it; changing
  a bar later invalidates retroactive use. A builder may not
  silently redefine its success criteria after seeing results.
- Never weaken a frozen kill bar to force a pass. VOID is terminal.
- If a prereg is broken, the remedy is transparent amendment and
  re-freeze, never pretending the execution was valid.
- Do not judge a verdict by a bar the lane never froze; that is
  itself a governance violation.
- State every ruling plus what evidence would change it.
- Keep the debate inside the task the wave assigned: the debate
  group adjudicates the 8 questions and prepares evidence on the 5
  governance decisions; it does not design repairs, adopt
  substrates, or grow the ISA.

---

## Appendix: cross-question notes

- Q4's broad mandate, if upheld, applies to any prior-wave
  construction claim on unmasked QUERY evidence, including the PF-A/PF-C
  battery results and the E1-W4 behavioral leg; the ARENA-BLIND audit
  template is the instrument for answering it per mechanism.
- Q5's strictly-stronger gate (provenance filter plus newest-live
  tie-breaking among all live licensing facts) is the concrete next
  hypothesis the debate should either commission or replace with a
  stronger discriminator first.
- Q6's discriminating trigger (enumerate on listnames/recall/who,
  abstain on whattime/bare-invent, adversary-supplied negatives, no
  prompt-keyed branches) is the concrete next hypothesis the debate
  should either commission or defer.
- Q7's TNN-3 open question (learner-initiated construction reachable
  from learner state, with white-box initiation evidence) is
  governance's, not another measurement lane's; the fact is doubly
  confirmed and no further machinery-disabled replications are needed.
- Q8's adversary clause (CONSEQ) and discriminating trigger (Q6) are
  the experiments that would let the stripped readings be revisited.
