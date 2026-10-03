# FRONTIER AUDIT: 2026-10-03 ~16:00 UTC

Worker: FRONTIER-AUDIT subagent (depth 2/2). Task type: NON-LEDGER
(claim minting paused). Audit and proposals only; no implementation.

Scope: Micah's 10 overnight priorities (2026-10-03) audited against
the lane directories under
`docs/lab/research-lead/overnight-20260928/` in tnn-rsi-gpi3
(222 lanes), the scaling lanes in tnn-rsi-10k, and the main-repo
operand-encoding fix. Method: lane directory mtimes, REPORT.md /
ANALYSIS.md / PREREG.md verdicts, and the tnn-native-lab git log for
2026-10-03. Branch: tnn-native-lab. Commits local only, never pushed.

## 1. Active-worker map (as of 2026-10-03 ~15:52 UTC, verified by lane mtime and git log)

| Worker | Lane(s) | Priority | Status at audit time |
|---|---|---|---|
| SCALING-10000-RETRY | tnn-rsi-10k .../scaling_10000b | #7 | Active. REPORT.md has verdict placeholders PENDING 3/3; K3_AUDIT.md FAILS (4 global scans on happy path) |
| COGOPS-TRANSITION-PREDICT | cogops_transition_predict | #5 | Active. Prereg frozen (c21 battery, K1-K8); probe validated on c20 |
| COMPOSE-SEALED-EVAL | compose_sealed_eval | #1 | Active. EVAL_EXEC.md written; executing the frozen compose_adversary protocol (A/B/C on 14 sealed world families) |
| L2-METAREUSE-COMPOSE-2 | l2_metareuse_compose2 | #2 | Listed active at 15:52; reached L2-METAREUSE-COMPOSE-2-PASS at 15:55 UTC during this audit (build D + control + 7 sealed regressions, 3/3 byte-identical, 0 falsifiers) |
| IVWC-ORACLE-FREE | ivwc_oracle_free | #4 | Listed active at 15:52; reached BUILD-PASS K1-K8 just before (oracle-free internal-model verification, 3/3 byte-identical) |
| FORMAL-COMPOSE-DAG3 | formal_compose_dag3 | #1 | Active. Prereg frozen (DAG1-DAG6); diamond + fan-in/fan-out + deep chain on the frozen rerank mechanism, no implementation yet |
| L2-ESS-CURRICULUM | l2_ess_hypothesis | #9/#10 | Active. H-OP-ESS hypothesis written (H1 vs H0); curriculum implementation of operator epistemic standing underway |

## 2. Audit table: the 10 priorities

Legend: (a) active workers, (b) completed on 2026-10-03, (c) gaps
(no active worker, no recent completion covering the sub-area).

### Priority 1: General DAG / fan-out / fan-in composition

(a) Active: COMPOSE-SEALED-EVAL (sealed evaluation of the three
composition hypotheses A/B/C on the adversary's 14 world families,
including X-FANOUT5, X-FANIN5, X-DAG10, X-PARTIAL); FORMAL-COMPOSE-DAG3
(prereg frozen; tests the promotion mechanism on a 3-structure DAG:
diamond + fan-out + fan-in + 10-link deep chain).

(b) Completed 2026-10-03: FORMAL-COMPOSE-RERANK BUILD-PASS (RR1-RR6;
promotion-based re-ranking resolves the B1 boundary; cycles
structurally impossible, no refusal branch); COMPOSE-ADVERSARY sealed
worlds + witness 16/16 PASS + eval templates; FORMAL-COMPOSE-E2E
BUILD-PASS (EK1-EK7); COMPOSE-LEARNCOMPOSE-1 BUILD-PASS (hypothesis C,
the only mechanism with a learning curve and cross-shape transfer);
GEN-COGOPS-UNIFY ANALYSIS FEASIBLE (U3 fan-out/fan-in demo across
cognitive + domain MAPs); COGOPS-DIAMOND (DIAMOND COMPOSITION
DEMONSTRATED, K1-K6; per-goal 4-step plans over fan-out/fan-in links,
persisted and re-derived).

(c) Gaps:
- G1a: The subsumption question is unanswered. The 2026-10-02
  composition direction requires determining whether one mechanism
  subsumes the others or their principles collapse into ONE general
  composition operation. COMPOSE-SEALED-EVAL will score A/B/C, but no
  worker is tasked with the comparative/subsumption test after the
  scores land.
- G1b: Cyclic pressure on fan-out/fan-in growth is untested. RERANK
  proved cycles structurally impossible on 2-structure chains; DAG3
  tests acyclic diamond/fan-in/fan-out. No sealed battery interleaves
  adversarial cycle-closing attaches with legitimate fan-out/fan-in
  growth.
- G1c: Longer chains (3+ structures) beyond the one discriminating
  [6,5] pair. COMPOSE-2 (now PASS) does operator composition across
  queries with exactly one composition step per query (T3); within-query
  chaining is explicitly out of scope.

### Priority 2: L2 adaptive reuse across heterogeneous structures

(a) Active: none (L2-METAREUSE-COMPOSE-2 reached PASS during this audit).

(b) Completed 2026-10-03: L2-METAREUSE-COMPOSE-2-PASS (operator output
as operator input across queries; the [6,5] CONCRETIZE-then-ABSTRACT
discriminating pair; QD2 op=5 tries=11 via=5; QD3 bounded termination
tries=18; frozen-learner control fails QD2 proving necessity);
L2-METAREUSE-ADVERSARY-PASS (6 operators on 7 sealed builds);
L2-ADAPTIVE-REUSE L2-METAREUSE-PASS (learner-selected reuse operator:
COMBINE/SUBSTITUTE/TRUNCATE, verification decides, ablation proves
necessity); L2-ESS-HYPOTHESIS written (H-OP-ESS: operator epistemic
standing); earlier matrix lanes (l2_extend/specialize/substitute/
truncate/invert/iface_xdomain), xdomain_causal_adapt, grammar_program_gpi3.

(c) Gaps:
- G2a: Sealed-adversary generality of the whole metareuse arc is open
  future work (stated as non-claim in l2_adaptive_reuse/REPORT.md).
  The adversary lane tested the 6 operators, but COMPOSE-2's build D
  world is worker-designed.
- G2b: Within-query operator chaining. COMPOSE-2 PREREG section 10
  non-claims: phase 2 runs only across queries; T2 forbids intra-query
  feedback; depth is exactly one step per query.
- G2c: Operator pairs beyond [6,5]. The prereg documents that [4,5]
  cannot discriminate in this harness; no lane tests other pairs or
  3-operator sequences.

### Priority 3: L3 / SUF learner-originated intermediate structures

(a) Active: none. (The L3-SUF-2 decision is pending with the parent;
two competing hypotheses H-CTXPAIR-1 and H-CTXPAIR-2 are frozen as
inputs.)

(b) Completed 2026-10-03: L3-SUF-1-REDTEAM REDTEAM-SURVIVES (bounded);
R-SUF-1 confirmed as a genuine safe-direction defect (rule (ii)
discards TEST-ACCEPTs; fix direction F6 verified: gate rule (ii) on
absence of ACCEPTs, correct on all 8 patterns, verdict-neutral);
L3-SUF-1-SCALING battery complete (SC-K2 PASS at nent=40; SC-K3 FAIL
at S3 decomposed as honest abstention, Case B; sharp structural
ceiling at nent=41: the frozen usedp buffer); BELIEF-SUF-COMPRESSION
ANALYSIS NON-DUP (belief layer and SUF records do not duplicate or
subsume each other; the SUF record's L3 test status must not be
absorbed into machinery); H-CTXPAIR-1 / H-CTXPAIR-2 preregs frozen
(competing hypotheses for the ctx-blind used-pair completeness
limitation found in scaling).

(c) Gaps:
- G3a: L3-SUF-2 has no builder. The R-SUF-1 fix is verified but NOT
  implemented (code frozen); the ctx-pair hypotheses are hypothesis
  only.
- G3b: Transfer / reuse / revision / retirement of SUF forms is
  explicitly out of scope of the scaling lane. No lane tests L3
  criterion C0-D (cognitive reuse: the structure must improve
  transfer, prediction, procedure learning, causal inference, memory,
  planning, or sample efficiency).
- G3c: Cognitive reuse of the invented intermediate across a changed
  surface representation (C0-C transfer requirement) is untested.

### Priority 4: Internal verification without expected-answer oracle

(a) Active: none (IVWC-ORACLE-FREE reached BUILD-PASS K1-K8 just
before the audit snapshot: verification with zero consequence
observations; learner never executes any plan on any true world
before verdicting).

(b) Completed 2026-10-03: IVWC-EXPAND3 BUILD-PASS (K1-K9; consequence-
trained verifier, commit-before-signal, content ablation now genuine
3/12 < 9/12, revision replicates bit-exactly, law-change dial shows
edge degrading +2 -> -1); IVWC-VETO BUILD-PASS (K1-K8); INTERNAL-VERIFY
BUILD-PASS (K1-K6); IVWC-ORACLE-FREE BUILD-PASS (K1-K8).

(c) Gaps:
- G4a: The verifier's CONTENT is never learned. Expand3's honest
  caveat: "The verifier is a fixed bucket table." Oracle-free proved
  verification can run on beliefs alone, but the verifier itself is
  researcher machinery.
- G4b: Self-verdict on composed structures (X+Y->Z composites from
  the compose lanes) is untested. All IVWC lanes verify plans, not
  compositions.
- G4c: The law-change dial covers one axis (wall density; expand3
  caveat #2). Break behavior under item-law, belief-noise, or
  energy-budget changes is unknown.

### Priority 5: Cognitive-operation bodies becoming increasingly learner-created

(a) Active: COGOPS-TRANSITION-PREDICT (c21 battery; tests whether the
leadership-transition inequality is genuinely predictive, probe
validated on c20 D2-7 and Block B).

(b) Completed 2026-10-03: COGNITIVE-OPS-LEARNER MIGRATION DEMONSTRATED
(K1-K6; researcher VERIFY specialized by the learner into an indexed
procedure with provenance; coverage-based selection with
correctness-preserving fallback; revision tracked with provenance);
COGOPS-DIAMOND (learner-owned RETRIEVE/VERIFY/COUNT composed into
per-goal plans); GEN-COGOPS-UNIFY ANALYSIS FEASIBLE (cognitive
procedures as GEN-composable structures; U10 spec-decline/generic-
fallback); COGOPS-LEADERSHIP-TRANSITION BUILD-FAIL (informative:
1 forced transition D2-7); the cogops_hedge/optimistic/pessimistic/
costaware/alternation strategy family.

(c) Gaps (all four are the cognitive_ops_learner report's own
recommended follow-ups, none started):
- G5a: Composition of two learner-owned procedures (specialized
  VERIFY feeding a learner-owned RETRIEVE).
- G5b: Retirement of the generic fallback (coverage confidence +
  correctness record).
- G5c: Creation from a weaker scaffold (learner invents the index
  form itself, toward L3).
- G5d: Interleaved worlds (A/B episodes mixed; coverage union vs
  revision; interference).

### Priority 6: Formal knowledge automatically constraining behavior

(a) Active: none. (FORMAL-COMPOSE-DAG3 is composition; it exercises a
representational ACYCLIC store but does not build constraint
induction.)

(b) Completed 2026-10-03: FORMAL-KNOWLEDGE REPORT (the design
document: three enforcement strengths REPRESENTATIONAL / ADMISSIONAL /
ADVISORY; binding-constraint channel design; P1-P7 falsifiable
predictions; fk_main.zag prototype TESTED: 200 adversarial inserts,
193 duplicates, REP and GATE arms 0 committed duplicates, META
remove_noevidence=0 / remove_withevidence=1); FORMAL-CONSTRAINTS
COMPLETE (wiring-dependence analysis: content learner-built, channel
researcher-defined; Arm L 6/6, fidelity_L 448/468 exact shortcut);
LEARNED-CONTRACTS LCONT-1-BUILD-PASS (kind refinement from failure:
kind 0 splits into 6 behaviorally-grounded kinds; permutation
control; K0-K6); FORMAL-COMPOSE-RERANK BUILD-PASS (representational
cycle impossibility, no refusal branch).

(c) Gaps (all named as unbuilt follow-ups in the FORMAL-KNOWLEDGE
report, sections 6 and 10):
- G6a: The induction-to-representation migration is designed but
  NOT built (P4 setup: duplicate-failure disconfirmations cause the
  learner to migrate list -> keyed on its own).
- G6b: P6 (ACYCLIC port to the composition edge store) NOT done.
- G6c: P5 (rename battery on the constraint mechanism) and the P1
  sealed 10,000-insert adversarial battery NOT run; multi-predicate
  interaction NOT tested.

### Priority 7: 5k / 10k+ scaling with correctness

(a) Active: SCALING-10000-RETRY (tnn-rsi-10k scaling_10000b; verdicts
PENDING 3/3 runs).

(b) Completed 2026-10-03: operand-encoding fix BUILD-PASS in the main
repo (per Micah's 2026-10-02 ruling: sign-tagged invariant op >= 0 =
NODE id, op < 0 = FRAME slot; all 7 governance steps; K2 100/500/1000
MAPs 39/39 correct byte-identical; K3a 24/24 at 5000; K3b 7007x scan
reduction; K3c determinism; K4 25/25 boundary; K5 red team zero panics;
K6 no semantic regressions); scaling_10000b K3_AUDIT (method: every
while loop on the ev_query happy path classified; verdict K3 FAILS:
four GLOBAL scans: decay, activate, is_superseded, bid nested loops,
t2_gather_lin, execute-step seq_nx scans); L3-SUF-1-SCALING (sharp
ceiling nent=41, structural).

(c) Gaps:
- G7a: The four GLOBAL scans on the happy path have no bounded
  replacement (the audit is diagnosis, not repair; the retry may or
  may not address them).
- G7b: The 2026-10-02 red-team finding (an index cycle crashes the
  indexer: panic, slice out of bounds) has no validation lane; the
  7007x reduction depends on the index.
- G7c: No 10k correctness battery exists yet; no scaling run under
  capacity pressure (eviction path) exists.

### Priority 8: Strong lifetime / meta-learning and negative-transfer control

(a) Active: NONE.

(b) Completed 2026-10-03: LIFETIME-META-2 META-LEARNING DEMONSTRATED
(cluster episodes: B5a 672 >= 350; examples-to-criterion 63 -> 3.3
late-typical mean; B5g negative-transfer signature -86 on atypicals,
sign as predicted); LIFETIME-META-1 NO META-LEARNING net (split
finding: B5b decrease PASS, B5a advantage FAIL -39; diagnosed:
outlier negative transfer underestimated + overshoot coupling +
prereg calibration error); NEGATIVE-TRANSFER PASS (K1-K5: selective
retention EMERGES from entry-local error-driven revision with no
protection mechanism; fragility isolated to ADDRESSING via the ML0
ablation; forward interference bounded at 2 extra passes).

There IS prior work here (base-rate prior learning, retention/
revision dynamics). What is missing is everything beyond the
minimal surrogates.

(c) Gaps:
- G8a: The NT1 preregistered follow-up is unstarted: port the
  winning rule (entry-local evidence revision + dedicated addressing)
  to the shared continuing-learner substrate, rerun A/B/A there,
  test under capacity pressure with rule-structured families. NT1's
  honest boundary: nevict=0 (eviction untested), key-value families
  only, single contradiction magnitude.
- G8b: Meta-learning is prior-MEAN learning only. LM2's honest
  boundary: "empirical-Bayes base-rate learning (L1/L2-ish). Not
  strategy invention, not L3." No lane tests whether the persistent
  learner can learn a STRATEGY across episodes.
- G8c: No interleaved-family lifetime test (no task labels, graded
  contradictions, interference asymmetry). The continuing-learner
  regime is untested.
- G8d: nt_pressure, eviction_policy, reclamation lanes exist but no
  2026-10-03 completion ties them to the NT1 rule.

### Priority 9: Belief reasoning from provenance / evidence

(a) Active: L2-ESS-CURRICULUM (operator epistemic standing; the ESS
pattern applied to L2 operators). Note: this covers operator standing,
not the belief layer itself.

(b) Completed 2026-10-03: BELIEF-PROVENANCE-8 BP-8-PASS (23/23;
multi-channel absorption nets measured: same-fact 90/0/1,
order-sensitive, per-channel saturation; 12-cycle fixpoint; HET ring
converges per type-14 reachability component); BELIEF-SUF-COMPRESSION
NON-DUP (belief layer vs SUF records: complementary, different
subjects/algebras/action vocabularies; no merge); PATTERN-EPISTEMIC-
STATE PATTERN.md (ESS named: 7-mechanism survey; open P3 substrate
question: does the record algebra unify with belief R2/R3/R7 or
contract dc/C_FAIL_RUN); L2-ESS-HYPOTHESIS (H1/H0 with falsifiers
F-A..F-D).

(c) Gaps:
- G9a: Eviction-sync design is undecided and needs the parent's
  ruling (persist vs tombstone vs R4-retire; BP-8 section 5). No
  experiment has compared the three options on preregistered metrics.
- G9b: Per-edge vs per-channel absorption is measured but not judged
  (BP-8 section 5 open question).
- G9c: Belief reasoning has never been connected to composition:
  R7 selection over composites vs first-verifying enumeration is
  untested. Priority #9 has no demonstrated consequence for #1.
- G9d: Per-belief bar adoption and d_self recovery path (BP-8 open
  questions) unstarted.

### Priority 10: Architecture compression (remove duplicated mechanisms)

(a) Active: NONE.

(b) Completed 2026-10-03: BELIEF-SUF-COMPRESSION NON-DUP (a NEGATIVE
result for #10: the pair does not duplicate; the honest partial
overlap P3 is a possible future shared evidence-ingestion substrate,
not recommended now); GEN-COGOPS-UNIFY ANALYSIS FEASIBLE (one GEN
composer for domain + cognitive structures; honest negatives listed:
learned kinds scaffold, plan persistence, order dissociation, pivot
links, >4-MAP tried-table defect found); the 2026-10-01
COMPRESSION_AUDIT (analysis only; ranked candidates Rank 1..8, none
executed); L2-ESS-HYPOTHESIS section 11 (operator standing as the
architectural-compression direction: researcher control lines move
into learner state).

(c) Gaps:
- G10a: No ranked audit candidate has been executed. Rank 1 (trial
  4-phase loop -> generic candidate-source iterator) is the highest-
  ratio candidate and is untouched.
- G10b: GEN-COGOPS-FULL is analysis only. The ANALYSIS recommends a
  full preregistered test per PREREG_DESIGN.md addressing learned
  kinds, plan persistence, order dissociation, pivot links, scaling;
  not started.
- G10c: The R-SUF-1 fix (red-team-verified: gate rule (ii) on absence
  of ACCEPTs, correct on all 8 patterns) is not implemented; a known
  researcher-authored miscalibration remains in frozen code pending
  L3-SUF-2.
- G10d: The A-vs-B-vs-C subsumption test (the #10-relevant outcome
  of the composition arc) has no tasked worker; it is queued behind
  COMPOSE-SEALED-EVAL.

## 3. Prioritized experiment proposals

Every proposal below is scoped as a pure-Zag, preregistered,
kill-bar-driven worker task (safebin toolchain, commit-order
self-check, 3/3 byte-identical determinism bar, local commits only).
Each names its grounding, states the predicted information gain, and
notes non-duplication against active workers. Priorities #8, #9, #10
first, since they have no active workers.

### PRIORITY 8 (lifetime / meta-learning / negative transfer): no active worker

#### E8.1 NT-PORT-PRESSURE: the NT1 rule on the continuing learner under capacity pressure

Grounding: negative_transfer/REPORT.md, "Recommended follow-up
(preregistered, PREREG Section 9): Port the winning rule
(entry-local evidence revision + dedicated addressing) to the shared
continuing-learner substrate, rerun A/B/A there, and test under
capacity pressure with rule-structured families." Honest boundaries
from the same report: nevict=0 in NT1 (eviction implemented but
untested), key-value memorization families only, single
contradiction magnitude, minimal surrogates not the production
substrate.

Design: implement entry-local error-driven evidence revision with
dedicated addressing on the continuing-learner substrate (not the
NT1 surrogate). Curriculum: family A (rule-structured, e.g.
k-hop chains with shared substructure, not bare key-value pairs),
then family B (contradicts a subset of A, agrees elsewhere), then
re-ask A. Capacity cap forces evictions (nevict > 0 required by a
bar). Arms: PORT (the rule), NOADDR (overlapping address map, the
ML0-style fragility control), FRESH (reset between families).

Kill-bar sketch: K1 retention of non-contradicted A after B (>=
preregistered rate, e.g. 11/12); K2 revision of contradicted keys
to B values with zero FORGET of agreed keys; K3 forward
interference bounded (extra passes <= preregistered bound);
K4 eviction audit: evicted entries are lowest-evidence first, and
no live high-evidence structure is evicted (white-box check);
K5 determinism 3/3; K6 no task labels / no freeze flags in learner
(grep audit).

Predicted information gain: HIGH. Decides whether the NT1
principle (the only demonstrated retention/revision mechanism)
survives the two realistic pressures it has never faced: the real
substrate and memory pressure. If retention collapses under
eviction, the eviction policy (not the update rule) is the next
bottleneck, which reorders the #8 backlog.

Non-duplication: no active worker touches lifetime or NT.

#### E8.2 LM-STRATEGY: meta-learning a strategy, not a prior mean

Grounding: lifetime_meta2/REPORT.md honest boundaries: "What was
learned is the prior MEAN over biases: empirical-Bayes base-rate
learning (L1/L2-ish). Not strategy invention, not L3. The estimator
form, w=20, initial m=50 are researcher-supplied mechanism; the
learned quantity is m." LM1 recommendation #4 (widen the gap) is
spent; the next step is strategy.

Design: keep the LM2 episode curriculum (12 episodes, typical +
atypical, independent streams) but let the LEARNER choose the
estimator weight w per episode from its experience (w currently
researcher-fixed at 20), or equivalently learn a stopping/probe
policy. Arms: STRAT (learner-chosen w, updated post-episode from
the revealed bias and the episode's examples-to-criterion),
FIXED-20 (LM2 replication control), FIXED-ORACLE-W (best constant
w chosen post-hoc by the researcher; the bar the learner must beat
or approach without supervision).

Kill-bar sketch: K1 STRAT examples-to-criterion on held-out
episodes < FIXED-20 (strict, preregistered margin); K2 STRAT within
a preregistered band of FIXED-ORACLE-W (shows the choice is
nontrivial, not luck); K3 the chosen w trajectory tracks the
experienced bias dispersion (white-box: w rises when atypicals
appear); K4 determinism; K5 no researcher meta-rule (update inputs
audited).

Predicted information gain: HIGH. First test of L2+/L3-flavored
meta-learning: the learner invents HOW to learn, not just what the
base rate is. A FAIL (learner cannot beat fixed w) is equally
informative: it bounds the lifetime learner at prior-tuning and
forces a representation rethink for #8.

Non-duplication: no active worker touches lifetime or NT.

#### E8.3 NT-GRADED-INTERLEAVE: graded contradictions, interleaved families, no task labels

Grounding: negative_transfer/REPORT.md honest boundaries ("Single
contradiction magnitude; graded contradiction out of scope");
cognitive_ops_learner/REPORT.md recommended follow-up #4
("Interleaved worlds: A/B episodes mixed, testing coverage union vs
revision and interference"); l2_interference / l2_interference2
lanes (earlier interference work).

Design: families A and B interleaved episode-by-episode with NO
task labels and no family markers; contradiction magnitude graded
(full contradiction, partial overlap, agreement). The learner uses
the NT1 rule (entry-local revision + dedicated addressing).
Measure retention curves per magnitude and interference asymmetry
(A->B vs B->A).

Kill-bar sketch: K1 retention of agreed knowledge >= threshold
across the interleave; K2 revision latency monotone in
contradiction magnitude (graded, not binary); K3 interference
asymmetry quantified and bounded (later family does not erase
earlier agreed knowledge beyond the preregistered bound);
K4 determinism; K5 no-label audit (driver never names a family).

Predicted information gain: MEDIUM-HIGH. Moves NT from the
sequential A-then-B lab setup to the continuing-learner regime
Micah's standing question demands (one learner, no task labels,
no resets). Tests whether entry-local revision generalizes to
interference or needs a new mechanism.

Non-duplication: no active worker touches lifetime or NT.

### PRIORITY 9 (belief reasoning from provenance/evidence): no active worker on the belief layer

#### E9.1 BP-COMPOSE-SELECT: R7 belief selection over composites vs first-verifying enumeration

Grounding: belief_provenance_8/REPORT.md (R7 selection: argmax eff
among candidates, abstain -3; beliefs attach to B-COMP composite
nodes); compose_adversary/PREREG.md (A/B/C mechanisms select by
trial enumeration); formal_knowledge/REPORT.md section 2 survey
("belief_provenance_2 ... This is still ADVISORY: a belief guides
selection; it cannot block an action").

Design: take the three frozen composition mechanisms (A: backchain,
B: suspend, C: learncompose) and give each a shared belief layer
over candidate composites (b_sup from corroboration runs and
provenance liveness, BP-2..8 machinery, read-only port). Selection
arm R7-SEL uses R7 (argmax eff, abstain below bar) instead of
first-verifying enumeration; control arm ENUM keeps the frozen
selection. Evaluate on a sealed composition battery (reuse the
compose_adversary world families via the sealed-eval harness once
COMPOSE-SEALED-EVAL completes, or a fresh adversary battery).

Kill-bar sketch: K1 R7-SEL solve rate >= ENUM solve rate (no
capability loss); K2 R7-SEL tries strictly fewer than ENUM (belief
guidance pays); K3 confident-wrong commits: R7-SEL <= ENUM (beliefs
do not add fabrication); K4 abstention arm: on unsolvable worlds
R7-SEL abstains (-3) where ENUM burns tries; K5 determinism;
K6 belief records are learner-written from experience (no
researcher endorsement literals; K7-style audit).

Predicted information gain: HIGH. Priority #9 currently has no
demonstrated consequence for any other priority; beliefs are
advisory records about claims. This is the first test of whether
belief reasoning changes construction behavior. A FAIL (R7 adds
nothing or adds wrong commits) would show the belief layer is
epiphenomenal for composition and redirect #9 toward revision/
eviction-sync instead.

Non-duplication: L2-ESS-CURRICULUM tests operator standing, not
belief-guided composite selection; COMPOSE-SEALED-EVAL scores the
frozen mechanisms without a belief layer.

#### E9.2 BP-ABSORB-ADJUDICATE: per-edge vs per-channel absorption, decided

Grounding: belief_provenance_8/REPORT.md section 5 open questions:
"Whether absorption should be per-edge rather than per-channel
(saturation measured, not judged)." BP-8 measured: same-fact
match+contradict nets 90/0/1, two type-7s saturate to one R2
(conf 2 not 3), absorption order-sensitive.

Design: two absorb variants sharing the frozen BP-7 machinery:
ABS-CH (per-channel, frozen behavior) and ABS-ED (per-edge: each
new edge contributes its own R2/R3). Sealed worlds designed so the
variants DIVERGE (multiple confirming edges on one fact; contradict
then multiple matches). Preregistered desirability criterion: the
winner is the variant that (i) preserves the RK-B kill (no
confident fabrication from tie-break-filled interiors) and
(ii) converges honestly on a 12-cycle with heterogeneous edge
injection (no oscillation, fixpoint idempotent).

Kill-bar sketch: K1 divergence demonstrated (the variants produce
different nets on at least one preregistered world); K2 criterion
(i) and (ii) both met by exactly one variant; K3 determinism;
K4 zero new edge types / machinery (variants differ only in the
absorb counting rule).

Predicted information gain: MEDIUM. Closes a measured-but-unjudged
open question with a decision procedure instead of an opinion.
The loser becomes a compression input (#10): one absorb rule dies.

Non-duplication: no active worker on the belief layer
(L2-ESS-CURRICULUM is operator standing).

#### E9.3 BP-EVICT-SYNC: persist vs tombstone vs R4-retire, compared on frozen metrics

Grounding: belief_provenance_8/REPORT.md section 5: "eviction-sync
design (still needs the parent ruling: persist vs tombstone vs
R4-retire)"; section 6 notes for the parent list it as a suggested
next. NT1 shows retention mechanics; nothing ties beliefs to
eviction.

Design: belief-bearing learner (BP-2..8 machinery) under capacity
pressure forcing eviction of belief-licensed structures. Three
arms: EV-PERSIST (beliefs survive eviction of their structure),
EV-TOMB (eviction writes tombstones; R4-style liveness degrades
dependent beliefs), EV-R4RET (eviction triggers R4 retire of
dependent beliefs). Battery: A/B/A re-ask with eviction between B
and re-ask; measure selection quality (R7 picks the right
survivor), wrong-commit rate, and belief-record honesty
(b_sup reflects post-eviction evidence).

Kill-bar sketch: K1 one arm strictly dominates on the preregistered
primary metric (wrong commits post-eviction); K2 the winner's
b_sup values remain calibrated (no confident beliefs on evicted
structures); K3 determinism; K4 the comparison is mechanism-only
(no new edge types).

Predicted information gain: MEDIUM-HIGH. Produces the evidence the
parent's eviction-sync ruling needs; unblocks the continuing-learner
design that #8 also needs. A three-way loss (no arm dominates)
would itself be informative: it would show eviction-sync needs a
new mechanism, not a choice among three.

Non-duplication: no active worker on the belief layer.

### PRIORITY 10 (architecture compression): no active worker

#### E10.1 TRIAL-UNIFY: execute the audit's Rank-1 candidate

Grounding: compression_audit/COMPRESSION_AUDIT.md section 3,
Rank 1: "Trial 4-phase loop -> generic candidate-source iterator."
The audit notes the `assemble -> t2_try_verify -> promote_graph`
triple repeats 4 times verbatim inside the 81-line t2_trial, and
the search ORDER (chains before sums before counts before
single-hops) is hardcoded researcher-owned control flow.

Design: rewrite t2_trial's four phases as ONE generic
candidate-source iterator (a table of (gather_fn, assemble_fn)
pairs driven by a single loop) on the frozen TNN-2 base. No
behavior change intended: this is a compression test, not a
capability test. Run the FW1-FW9 regression battery (the
regression battery Micah ruled on 2026-10-01: a 9/9 establishes no
generality, but here it is used correctly as a no-regression
check).

Kill-bar sketch: K1 FW1-FW9 9/9 identical verdicts pre/post;
K2 cognition lines strictly reduced (>= 20 percent fewer lines in
the trial/search region); K3 zero new modes/bridges/handlers;
K4 3/3 byte-identical; K5 the hardcoded order becomes data (the
phase table), so reordering phases is a table edit, not a code
edit (white-box check).

Predicted information gain: MEDIUM-HIGH. The compression audit is
currently analysis-only; this is the first EXECUTED compression.
PASS proves the audit's highest-ratio candidate is real and gives
the template for Ranks 2-8. FAIL (behavior changes or lines do not
shrink) falsifies the candidate honestly.

Non-duplication: no active worker on compression.

#### E10.2 GEN-COGOPS-FULL: the full preregistered unification test

Grounding: gen_cogops_unify/ANALYSIS.md verdict FEASIBLE and
"Recommendation: Proceed to a full preregistered test
(PREREG_DESIGN.md). The PoC establishes feasibility; the prereg
must address the honest negatives, especially learned kinds, plan
persistence, order dissociation, pivot links, and scaling." Also
the PoC's finding 9: the frozen GEN's tried tables are hardcoded
for 4 MAPs (any experiment with >4 MAPs on the frozen GEN base is
suspect; the PoC relocates them).

Design: implement PREREG_DESIGN.md as a frozen prereg (prereg
committed alone first). Must include: learned-kind arm (no
researcher-written pkind), plan-persistence arm (GEN persists the
trial sequence and reuses it post-wipe, the cogops K5 property),
order-dissociation arm ([RET,VFY] vs [VFY,RET] from the same
bindings), pivot-link arm (the prereg's kill bar), and a >4-MAP
scaling arm exercising the relocated tried tables.

Kill-bar sketch: per PREREG_DESIGN.md; at minimum: K1 learned
kinds grow from experience (no pkind literals); K2 plan reuse
post-wipe byte-identical; K3 order dissociation demonstrated;
K4 pivot arm passes; K5 6+ MAPs with no tried-table aliasing
(white-box audit); K6 determinism.

Predicted information gain: HIGH. Decides whether ONE composer
(GEN) subsumes domain and cognitive composition: the central #10
question for the composition arc. The honest negatives are exactly
the bars; a FAIL on any of them localizes what unification cannot
cover.

Non-duplication: no active worker on compression; the ANALYSIS is
a PoC, not the full test.

#### E10.3 R-SUF-1-FIX: implement the red-team-verified fix as the L3-SUF-2 seed

Grounding: l3_suf_redteam/REPORT.md F6: "gating rule (ii) on absence
of ACCEPTs (the adversary's proposed fix, mirroring rule (i))
yields the correct mask on ALL 8 evidence patterns, preserving the
P2 hedge and fixing P3/P8. The fix changes no sealed verdict."
Notes for the parent: "The fix ... is NOT implemented (code
frozen); recorded for the next design." H-CTXPAIR-1/H-CTXPAIR-2
are the competing inputs to the L3-SUF-2 decision.

Design: new (unfrozen) learner implementing the gated rule (ii)
plus the winning H-CTXPAIR hypothesis's used-pair handling
(H-CTXPAIR-1 ctx-aware used-pair set vs H-CTXPAIR-2 learned
per-form context-invariance; run both, the shootout in E3.2
decides, or run the fix first with the used-pair set as a
parameter). Re-run the sealed SUF battery (adversary's worlds via
the sealed protocol).

Kill-bar sketch: K1 all previously-passing sealed verdicts
unchanged (verdict-neutral, per F6); K2 P3/P8 patterns now mark
correctly (decoy TEST-ACCEPT + fabrej -> RESOLVED(1); contradictory
ACCEPTs + fabrej -> FALSIFIED-ALL(0)); K3 the P2 hedge preserved
(partial-probe U still marks 3); K4 no new researcher-authored
conditionals beyond the gated rule (A-LIT audit); K5 determinism.

Predicted information gain: MEDIUM-HIGH. Removes a KNOWN
researcher-authored miscalibration (the red team found the
source's own "NO marking rule" audit note inaccurate). It is also
the necessary cleanup before L3-SUF-2: the next design should not
inherit a proven defect. Compression-flavored: one bad conditional
dies, replaced by the symmetric rule.

Non-duplication: no active worker implements the fix; the
H-CTXPAIR lanes are hypothesis-only by their own preregs.

### PRIORITY 1 (composition): active workers cover the core; proposals target the gaps

#### E1.1 COMPOSE-SUBSUMPTION: queued behind the sealed eval

Grounding: 2026-10-02 composition direction: "run comparative/
adversarial experiments (3-5+ structures, different domains,
partial applicability, no expected-answer supervision, revision/
reuse of composites) to determine whether one mechanism subsumes
the others or their principles collapse into ONE general
composition operation." compose_adversary/PREREG.md HARD/SOFT
bars for A (backchain), B (suspend), C (learncompose).

Design (starts only after COMPOSE-SEALED-EVAL reports): take the
sealed-eval winner(s) and test each on the other mechanisms'
home-turf families (A's chains, B's fan-in efficiency, C's
trap/revision and cross-shape transfer), plus novel hybrids
(fan-out + partial applicability, cyclic diamond attempts).
Kill-bar sketch: K1 subsumption bar: one mechanism meets all
three home-turf HARD bar sets; K2 if no mechanism does, the
subsumption hypothesis is KILLED and the report names which
principle each mechanism uniquely owns (feeds #10: no merge);
K3 determinism; K4 no expected-answer supervision in the test
worlds (fresh adversary or witness-checked).

Predicted information gain: HIGH. This is the decision the whole
composition arc exists to produce. Either one mechanism subsumes
the others (compression: two mechanisms retire) or the honest
negative stands (three principles, no merge; also a #10 input).

Non-duplication: COMPOSE-SEALED-EVAL scores A/B/C; no worker is
tasked with the post-score subsumption test.

#### E1.2 CYCLE-FANOUT-BATTERY: representational ACYCLIC under growth pressure

Grounding: formal_compose_rerank/REPORT.md (cycles structurally
impossible by the rank invariant; no refusal branch; B1 cross-rank
attaches now commit via promotion); formal_compose_dag3/PREREG.md
(acyclic diamond + fan-in/fan-out + deep chain; adversarial
cycle-closing attaches at three scales).

Design: the frozen es_rerank.zag store under a growth battery:
legitimate fan-out/fan-in expansion interleaved with adversarial
cycle-closing attaches (2-hop, 3-hop, self-loop, cross-rank), at
larger scale than DAG3 (deeper chains, wider fan-out). Kill-bar
sketch: K1 zero committed cycles across the battery (adversarial
attaches written, all inert); K2 every acyclic attach readable
(no valid assembly refused); K3 rank invariant holds at every
stage (read graph strictly decreasing; diverge=0); K4 determinism.

Predicted information gain: MEDIUM. DAG3 tests the mechanism on
one 3-structure DAG; this tests the GUARANTEE under adversarial
growth pressure. Also serves #6/P6 (formal_knowledge's ACYCLIC
prediction for composition edge stores): a PASS here is the P6
evidence.

Non-duplication: FORMAL-COMPOSE-DAG3 tests one frozen DAG shape;
this is an adversarial growth battery, a different test.

### PRIORITY 2 (L2 reuse): active worker just completed; proposals target the gaps

#### E2.1 METAREUSE-SEALED-GENERALITY: adversary-designed worlds for the 6 operators

Grounding: l2_adaptive_reuse/REPORT.md non-claims: "One world
family. No generality claim beyond the seven arms; the world is
builder-designed, not adversary-designed. Sealed-adversary
generality is open future work." l2_metareuse_adversary/REPORT.md
(PASS on 7 sealed builds for the operator set).

Design: independent adversary (separate worker, no access to
builder worlds) designs sealed worlds exercising the six operators
(COMPOSE/SUBSTITUTE/TRUNCATE/INVERT/ABSTRACT/CONCRETIZE) plus the
phase-2 composition path, with a witness checker. The frozen
extended learner (COMPOSE-2 build) is evaluated blind.

Kill-bar sketch: K1-K5/K8 mirror the COMPOSE-2 bars on the sealed
worlds (operator choice by verification, exact grounding,
provenance hygiene); K2 the discriminating composition pair
fires on at least one sealed world the adversary designed to
require it; K3 determinism; K4 adversary blindness statement.

Predicted information gain: MEDIUM-HIGH. The whole L2 arc rests
on builder-designed worlds; this is the generality test the
reports explicitly leave open. A FAIL localizes which operators
do not generalize.

Non-duplication: L2-METAREUSE-COMPOSE-2 is complete; no active
worker on sealed generality.

#### E2.2 WITHIN-QUERY-CHAIN: operator chaining inside one query

Grounding: l2_metareuse_compose2/PREREG.md section 2b T2 ("A Z MAP
built during phase 2 is recorded for FUTURE queries but is not
added to the current query's list: no intra-query chaining") and
section 10 non-claims ("within-query operator chaining ...
out of scope").

Design: extend the phase-2 design with an intra-query chaining
arm: after phase 2 builds Z_j from Z_i, allow one further
composition step WITHIN the same query (Z_j as source for a third
operator). Preregistered termination: max chain depth 2 per query,
bounded operator calls, no same-query feedback loops beyond depth
2. Worlds: queries solvable only by 2-step chains (neither
single-operator nor cross-query composition suffices; cross-query
needs the intermediate query to exist, which it does not).

Kill-bar sketch: K1 chain queries solve (via/val exact); K2
termination: tries bounded by the preregistered count, zero hangs;
K3 control (frozen COMPOSE-2 learner, cross-query only) fails the
chain queries; K4 determinism; K5 provenance chain Z_k -> Z_j ->
taught source complete (t16 edges).

Predicted information gain: MEDIUM. Tests whether composition
must be staged across queries or can nest within one: the
difference between a pipeline and a genuine composition
operator. Informs whether the T2 restriction is load-bearing or
an artifact.

Non-duplication: COMPOSE-2 explicitly forbids this; no active
worker on it.

### PRIORITY 3 (L3/SUF): no active worker; L3-SUF-2 decision pending

#### E3.1 SUF-REUSE-TRANSFER: the invented form reused across a changed surface

Grounding: l3_suf_scaling/REPORT.md out of scope:
"Transfer/reuse/revision/retirement at scale untested." Micah's
L3 bar C0-D: the structure must improve transfer, prediction,
procedure learning, causal inference, memory, planning, or sample
efficiency. belief_suf_compression/ANALYSIS.md: the SUF record is
the learner-invented intermediate under L3 test.

Design: two world families sharing deep structure but with
changed surface representation (per C0-C: transfer across changed
surface representation). Family 1: the learner invents the SUF
form (sealed protocol as in l3_suf_adversary). Family 2 (sealed,
adversary-designed): same deep structure, permuted surface.
Measure: does the learner REUSE the invented form (not rebuild),
and does reuse improve examples-to-criterion vs a from-scratch
control? Ablation arm: the SUF record wiped between families.

Kill-bar sketch: K1 reuse demonstrated (the family-1 form's
elements referenced on family 2, white-box trace); K2 transfer
gain: examples-to-criterion strictly lower than from-scratch
control; K3 ablation destroys the advantage (the record is
load-bearing); K4 the invented form is not enumerated in source
(C0-A/B audit); K5 determinism.

Predicted information gain: HIGH. No SUF lane has tested C0-D.
This is the difference between "the learner invented a record"
and "the invention does cognitive work." A FAIL (no transfer)
would bound the SUF claim at L2+ and redirect #3.

Non-duplication: no active worker on SUF; H-CTXPAIR lanes are
hypothesis-only.

#### E3.2 H-CTXPAIR-SHOOTOUT: the two competing hypotheses built and compared

Grounding: l3_ctx_pair_hypothesis/PREREG.md (H-CTXPAIR-1:
ctx-aware used-pair set) and l3_ctxpair2_hypothesis/PREREG.md
(H-CTXPAIR-2: learned per-form context-invariance). Both are
frozen INPUTS to the parent's pending L3-SUF-2 decision; both
preregs state no implementation is authorized under them. The
scaling report's actionable item (a): "the ctx-blind used-pair
set in the probe strategy (a completeness limitation worth a
future hypothesis)."

Design: two builder lanes from the two frozen preregs, same
battery (the S3-scale worlds where SC-K3 failed: cross-context
determined pairs un-evidenced). Each builder implements its
hypothesis's probe-strategy fix; both evaluated on the shared
battery plus a fresh sealed set.

Kill-bar sketch: K1 each builder meets its own prereg's bars;
K2 head-to-head: the winner is the hypothesis with strictly
better cross-context determined-pair coverage at equal probe
budget; K3 safety invariants hold for both (0 wrong predictions,
100 percent U-abstention); K4 determinism; K5 the loser is
recorded as killed with the trace evidence (not amended).

Predicted information gain: MEDIUM-HIGH. Resolves the L3-SUF-2
input competition empirically instead of by parent fiat, and
fixes the one actionable completeness limitation the scaling
lane found. Keeps the 20+ hypothesis discipline honest: two live
hypotheses, one survives.

Non-duplication: the H-CTXPAIR lanes forbid implementation under
their preregs; these are new builder lanes.

### PRIORITY 4 (internal verification): oracle-free just completed; gaps are the verifier itself

#### E4.1 LEARNED-VERIFIER: the verifier's content becomes learner-owned

Grounding: ivwc_expand3/REPORT.md honest caveat #3: "The verifier
is a fixed bucket table; the claims concern the self-verdict loop,
the content ablation, and the limits curves." ivwc_oracle_free
(proved verification can run with zero consequence observations,
on beliefs + committed plans).

Design: the verifier table is LEARNED from the learner's own
consequence experience (belief_execute outcomes in the oracle-free
setting), then frozen and sealed-tested. Arms: LEARNED (table from
experience), FIXED (the expand3 bucket table, control), SHUFFLED
(content ablation as in expand3 K6).

Kill-bar sketch: K1 LEARNED beats the trivial baseline on sealed
worlds (acc > maj, preregistered margin); K2 content ablation:
SHUFFLED < LEARNED (strict); K3 the learned table's entries are
traceable to experienced (bucket, eff) pairs (white-box);
K4 determinism; K5 no oracle tokens (A3/A4 audits).

Predicted information gain: MEDIUM-HIGH. Moves #4 from "the
self-verdict loop works" to "the verifier itself is learned":
the remaining researcher-authored piece of the IVWC arc. A FAIL
(the learned table cannot beat trivial) would show verification
needs given structure, bounding #4 at L2.

Non-duplication: IVWC-ORACLE-FREE is complete; no active worker.

#### E4.2 IVWC-COMPOSED: self-verdict on X+Y->Z composites

Grounding: ivwc_expand3/REPORT.md (self-verdict on plans);
compose_adversary (A/B/C compose structures, no self-verification);
Micah's 2026-10-02 composition direction (no expected-answer
supervision).

Design: the IVWC loop (commit + pre-execution PASS/FAIL
self-verdict + revision) applied to COMPOSED structures: the
learner commits to a composite Z of X and Y, verdicts it
pre-execution from consequence-trained (or belief) verification,
and revises on REJECT. Sealed composition worlds (reuse the
compose_adversary families).

Kill-bar sketch: K1 commit-before-signal (world-call counter 0
after commit); K2 self-verdict discriminates good/bad composites
(mean PASS eff > mean FAIL eff, strict); K3 beats trivial
baseline; K4 revision protocol replicates; K5 determinism.

Predicted information gain: MEDIUM. Joins #4 (verification) with
#1 (composition): the first test of whether a learner can judge
its own compositions without an expected-answer oracle. Directly
serves the 2026-10-02 direction's "no expected-answer supervision"
requirement.

Non-duplication: no IVWC lane touches composites; no active worker.

### PRIORITY 5 (cognitive ops): active worker on transition-predict; gaps are the learner-owned procedures

#### E5.1 COGOPS-COMPOSE-PROCS: two learner-owned procedures composed by the learner

Grounding: cognitive_ops_learner/REPORT.md recommended follow-up
#1: "Composition: two learner-owned procedures selecting/
composing (e.g., specialized VERIFY feeding a learner-owned
RETRIEVE)." cogops_diamond/REPORT.md (per-goal plan assembly over
learner-owned procedures, DIAMOND COMPOSITION DEMONSTRATED).
gen_cogops_unify/ANALYSIS.md honest negative #6: "GEN does not
invent cognitive procedure bodies. Unification covers COMPOSITION
only."

Design: the learner owns two specialized procedures (from the
cognitive_ops_learner migration: indexed VERIFY; plus an indexed
RETRIEVE). On diamond goals, the learner composes them itself
(VERIFY's output feeding RETRIEVE, or the reverse per the goal's
dependency links), with no GEN and no researcher-written
pipeline. Provenance tracks which procedure revision served each
need.

Kill-bar sketch: K1 composed plans solve diamond goals the single
procedures cannot; K2 provenance complete (need -> procedure
revision -> episode range); K3 selection follows learned coverage
at execution time (as in cogops_diamond); K4 determinism;
K5 no VERIFY_MODE / RETRIEVE_MODE / pipeline constant (grep audit).

Predicted information gain: MEDIUM-HIGH. The missing step between
"procedures migrate into learner state" (done) and "the learner
composes its own procedures" (the actual #5 target). GEN composes
them externally; this tests learner-driven composition.

Non-duplication: COGOPS-TRANSITION-PREDICT tests the leadership
inequality, not procedure composition.

#### E5.2 COGOPS-RETIRE: the generic fallback becomes learner-governed

Grounding: cognitive_ops_learner/REPORT.md recommended follow-up
#2: "Retirement: conditions under which the learner drops the
generic fallback (retire = coverage confidence + correctness
record)." The report's honest boundary: "retirement of the generic
procedure (it remains the fallback and the oracle)" is not
established.

Design: the migrated learner (specialized VERIFY + generic
fallback) runs an extended curriculum. Retirement protocol
(preregistered): the learner drops the generic fallback for a
coverage region when coverage confidence (episodes) and the
correctness record (agreements with the generic oracle) both
exceed preregistered thresholds; re-instatement when a
post-retirement disagreement occurs.

Kill-bar sketch: K1 retirement fires on the preregistered
schedule (not early, not never); K2 post-retirement correctness
preserved (specialized verdicts still agree with the oracle on
audits); K3 re-instatement fires on an injected failure and
restores correctness; K4 determinism; K5 the thresholds are
learner-adjusted (R7-style), not researcher constants.

Predicted information gain: MEDIUM. Removes the last researcher
crutch in the migration arc: the generic procedure as permanent
fallback/oracle. Tests whether learner-owned standing can govern
its own machinery's lifecycle (ties #5 to #9's ESS pattern).

Non-duplication: no active worker on retirement.

### PRIORITY 6 (formal knowledge): no active worker; the FORMAL-KNOWLEDGE follow-ups are unbuilt

#### E6.1 MIGRATION: duplicate-failure disconfirmations cause list -> keyed migration

Grounding: formal_knowledge/REPORT.md section 10: "Build the
induction-to-representation migration (P4 setup): the experiment
where duplicate-failure disconfirmations cause the learner to
migrate list -> keyed on its own." Section 4.3: the induction path
reuses contract_unify's induct machinery; the migration is "itself
a gated action requiring the disconfirmation evidence that
motivated it." The prototype tested only the mechanism pattern,
not the induction.

Design: learner starts with a list store and the contract_unify
induct machinery. Adversarial duplicate inserts produce
disconfirmation events attributed (by the invalidate machinery)
to the UNIQUENESS clause. When the preregistered evidence bar is
reached, the learner migrates the store list -> keyed (the
migration op flows through the meta-gate, which requires the
latched evidence). Control: no-migration arm (stays list).

Kill-bar sketch: K1 migration fires only after the preregistered
disconfirmation count (META-style: remove_noevidence=0 analogue);
K2 post-migration committed duplicates = 0 across the adversarial
battery; K3 control arm commits > 0 duplicates; K4 the induced
constraint params match the induct output (white-box: the clause
the learner wrote is the clause that binds); K5 determinism.

Predicted information gain: HIGH. This is the load-bearing unbuilt
step of #6: the moment a learned formal fact PROMOTES itself from
advisory belief to representational constraint by learner action.
Everything else in the report is design or prototype.

Non-duplication: no active worker on formal knowledge.

#### E6.2 CONSTRAINT-10K: the P1/P2 sealed battery at scale plus the rename battery

Grounding: formal_knowledge/REPORT.md P1: "sealed adversarial
world, 10,000 insert attempts with 50 percent adversarial
duplicates against a keyed store with ACTIVE UNIQUENESS:
committed duplicate entries = 0 exactly. Control (list store):
> 0." P2 (admissional gate variant; the wiring-dependence test).
P5: "mechanical identifier permutation over world, stores, and
constraint records; refusal pattern and final state byte-identical
after inverse mapping."

Design: sealed adversarial insert battery at 10,000 attempts
against three arms: REP (keyed store, representational
UNIQUENESS), GATE (action-root gate, admissional), LIST (control).
Then the P5 rename battery: mechanically permute every identifier
and re-run; refusal pattern and final state must be byte-identical
after inverse mapping.

Kill-bar sketch: K1 REP committed duplicates = 0 exactly;
K2 GATE committed = 0, refusals = duplicate attempts;
K3 LIST committed > 0 (the battery has teeth); K4 rename battery
byte-identical after inverse mapping; K5 determinism 3/3.

Predicted information gain: MEDIUM. Scales the prototype's
200-attempt existence proof to the preregistered 10k prediction
and runs the domain-blindness battery: the two properties that
would make binding constraints a general mechanism rather than a
demo. Ties #6 to #7 (scaling).

Non-duplication: no active worker on formal knowledge.

### PRIORITY 7 (scaling): active retry; proposals avoid duplicating it

#### E7.1 INDEX-PANIC-VALIDATION: the index-cycle crash, adversarially tested

Grounding: MEMORY.md 2026-10-02: "Same-day red team: an index
cycle crashes the indexer (panic, slice out of bounds), so index
validation is needed before production." The 7007x scan reduction
(K3b, operand-encoding fix) depends on the MAP index; the
scaling_10000b K3_AUDIT covers the query happy path, not the
indexer's cycle handling.

Design: adversarial battery against the frozen indexer: cyclic
index references, malformed bucket chains, duplicate keys,
stale entries. The indexer must handle all inputs without panic;
behavior on malformed input is preregistered (refuse / skip /
repair, not crash).

Kill-bar sketch: K1 zero panics across the battery (any panic =
FAIL); K2 well-formed inputs index correctly (correctness
control); K3 malformed inputs produce the preregistered
non-crash outcome; K4 determinism.

Predicted information gain: MEDIUM-HIGH. Unblocks production use
of the index the 7007x number depends on. A panic anywhere is a
hard FAIL with a stack trace pointing at the exact defect: the
cheapest high-value scaling work available.

Non-duplication: SCALING-10000-RETRY audits the query path; no
worker validates the indexer's cycle handling.

#### E7.2 EVICT-PRESSURE-10K: correctness under capacity pressure

Grounding: negative_transfer/REPORT.md honest boundary: "No
capacity pressure was exercised (nevict=0 both arms); the
eviction rule is implemented but untested." scaling_10000b K3_AUDIT
lists the happy path; the eviction/fallback paths are "audited
separately" (not done). MEMORY.md 2026-10-02 base-capacity lesson:
at-capacity alloc triggers full-arena eviction scans (~0.8s each).

Design: 10k-MAP battery with the arena capped to force evictions
during both teaching and querying. Kill-bar sketch: K1
correctness preserved (query answers match the uncapped control);
K2 eviction audit: evicted entries are lowest-priority first;
no live MAP required by the battery is evicted (white-box);
K3 determinism; K4 per-query latency bound (no eviction-scan
cliff: preregistered cap).

Predicted information gain: MEDIUM. The realistic scaling regime
is capped memory, not infinite arenas. Tests whether the index
and the eviction policy compose. Feeds #8 (lifetime under
pressure) with a production substrate.

Non-duplication: SCALING-10000-RETRY's battery is the happy path;
no worker tests the eviction path at scale.

## 4. Watchdog hypothesis backlog (20+ live hypotheses)

For the watchdog's 20+ hypothesis maintenance. Status key:
LIVE = untested and proposed; FROZEN-H = hypothesis prereg frozen,
builder unstarted; ACTIVE = worker running; DONE-20261003 =
completed 2026-10-03.

1. H-CTXPAIR-1 vs H-CTXPAIR-2 shootout (E3.2). FROZEN-H.
2. L3-SUF-2 design incorporating the R-SUF-1 fix (E10.3). LIVE.
3. SUF transfer/reuse across changed surface representation (E3.1). LIVE.
4. NT rule ported to the continuing learner under pressure (E8.1). LIVE.
5. Learner-chosen estimator strategy across episodes (E8.2). LIVE.
6. Graded-contradiction interleave with no task labels (E8.3). LIVE.
7. R7 belief selection over composites (E9.1). LIVE.
8. Per-edge vs per-channel absorption adjudication (E9.2). LIVE.
9. Eviction-sync three-way comparison (E9.3). LIVE.
10. Trial 4-phase loop -> generic candidate-source iterator (E10.1). LIVE.
11. GEN-COGOPS full unification test (E10.2). LIVE.
12. A-vs-B-vs-C subsumption after sealed eval (E1.1). LIVE (queued).
13. Cycle-fanout adversarial growth battery (E1.2). LIVE.
14. Sealed-adversary generality for the 6 L2 operators (E2.1). LIVE.
15. Within-query operator chaining (E2.2). LIVE.
16. Learned verifier content (E4.1). LIVE.
17. IVWC self-verdict on composites (E4.2). LIVE.
18. Two learner-owned procedures composed by the learner (E5.1). LIVE.
19. Generic-fallback retirement protocol (E5.2). LIVE.
20. List -> keyed migration from disconfirmations (E6.1). LIVE.
21. 10k sealed constraint battery + rename battery (E6.2). LIVE.
22. Index-cycle panic validation (E7.1). LIVE.
23. Eviction-pressure 10k correctness (E7.2). LIVE.
24. Operator epistemic standing curriculum (L2-ESS-CURRICULUM). ACTIVE.
25. COGOPS transition inequality prediction (c21). ACTIVE.
26. FORMAL-COMPOSE-DAG3 diamond/fan-in/fan-out/deep-chain. ACTIVE.
27. COMPOSE-SEALED-EVAL A/B/C scoring. ACTIVE.
28. SCALING-10000-RETRY verdicts. ACTIVE.
29. ESS record algebra unification with belief R2/R3/R7 (PATTERN.md open P3 substrate question). LIVE.
30. Coarser kind emergence under merging pressure (learned_contracts honest boundary: "coarser emergence would need a merging pressure, which is future work"). LIVE.
31. Input-side (in-kind) contract learning (learned_contracts honest boundary: "in-kind stayed universal (0) throughout"). LIVE.
32. The stale-specialist divergence scenario for operator standing (l2_ess_hypothesis section 6). LIVE (feeds #24).

## 5. Notes and caveats for the parent

- Two listed-active workers completed during the audit window:
  L2-METAREUSE-COMPOSE-2 (PASS, 15:55 UTC) and IVWC-ORACLE-FREE
  (BUILD-PASS K1-K8). The watchdog should reassign their capacity
  to #8/#9/#10 gaps.
- Priorities #3 and #6 have no active workers and no 2026-10-03
  completions beyond analysis/hypothesis documents; both have
  frozen, verified, unimplemented next steps (R-SUF-1 fix;
  migration experiment), which is unusual backlog maturity.
- The #8 backlog is the thinnest in mechanism terms: NT1 and LM2
  are minimal surrogates with preregistered follow-ups unstarted.
  E8.1 is the single highest-priority experiment in this audit
  because every other lifetime proposal depends on whether the
  NT1 rule survives the real substrate.
- Nothing in this audit duplicates an active worker's frozen
  battery. E1.1 is explicitly queued behind COMPOSE-SEALED-EVAL;
  E3.2 and the H-CTXPAIR builders respect the hypothesis preregs'
  no-implementation clauses by proposing new builder lanes.
- Style: hyphens only, no em/en dashes. Commits local with
  explicit pathspecs; nothing pushed. Non-ledger task.
