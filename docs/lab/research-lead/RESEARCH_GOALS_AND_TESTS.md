# TNN goals, hypotheses, and decisive tests

Date: 2026-10-06. Status: RESEARCH PLAN, not established capability.
Evidence snapshot: origin lane/ownership 91b2acc29731135a143adf27c00400174550eaf1.
Author role: fast adversarial research assistant; no independent human replication.
Working branch: fast/method-identifiability. Not merged into ownership.

## 1. Goals and operational definitions

TNN aims toward one persistent adaptive substrate, not a manager of permanently
specialized cognitive modules. Generic machine primitives are permitted.

**User goal clarification (2026-10-06): prediction is a tool, not TNN's core.**
The aspirational target is the breadth of human intelligent competence: acquiring
knowledge and practical know-how, language use, reasoning, invention, choosing and
carrying out actions, and adapting how it learns/thinks without task-specific human
rescue. This does not assert present human-level ability or require literal biological
brain equivalence. Predictions, answers, and benchmark scores are evidence probes,
not substitutes for that goal. A known fact, fluent practiced skill, uncertain guess,
and newly constructed method are distinct functional cases; terminology alone does
not establish which mechanism supplies them.

Useful operational names: **procedural knowledge / knowing-how** for acquired skill;
**declarative knowledge / knowing-that** for facts; **self-directed adaptation** for
experience-driven changes to learning/action policy. Uncertainty-aware inference
remains useful, but competence must also be tested through consequential action,
communication, transfer, revision, and self-chosen information acquisition.

- G1 Experience-owned competence: new task competence comes from experience,
  not a task-specific source edit, router, named mode, or supplied final method.
- G2 Method ownership: persistent learned structure causes behavior on inputs
  whose answers are not stored. Facts retained / method erased loses the benefit.
- G3 Useful form creation: useful compositions are acquired beyond an explicit
  researcher-enumerated menu of complete solutions. Finite primitives alone are
  not disqualifying; disclose syntax, maximum lengths, and search budgets.
- G4 Transfer and revision: methods help on new depth/composition/representation,
  survive irrelevant experience, and change when wrong without wholesale resets.
- G5 Less handholding: count task-specific human interventions, labels, fixture
  knowledge, demonstrations, resets, and source changes. Generic objectives and
  authorized hard constraints are not the same as supplying a solution.
- G6 Reliable control: authorized limits constrain actual effects through every
  execution path; inspection, revocation, rollback, and resource bounds work.
- G7 Architecture compression: apparent cognition shares machinery; extra graphs,
  modules, or policies must earn their complexity against simpler alternatives.
- G8 Honest science: correctly executed arms, qualified scorers, reproducible pure
  Zag, independent expected answers, and explicit limitations.

Autonomy and control are separate axes. A fixed machine can be controllable but
not adaptive; a successful learner can be adaptive but hard to control. Learned
applicability contracts are not automatically immutable human safety boundaries.
No percentage toward AGI; no transformer superiority without matched comparison.
L3 is a project criterion, not an AGI certificate.

## 1a. Nested adaptive workspace clarification (2026-10-07)

The user proposes nested, overlapping organizations with porous boundaries: a
persistent computational world, not intelligence trapped in a fixed graph traversal
or cognitive module pipeline. This is a hypothesis to test, not a required ontology.
See [scope and claim gates](NESTED_WORKSPACE_SCOPE.md): representability, causal use,
experience acquisition, generative leverage, lifetime revision and human control.
Hand-built folders and retained-state engineering do not count as learned cognition.
Complete-form menus must be distinguished from small generic computational syntax;
fixed primitives alone neither prove nor disprove invention. No TNN/LLM parity or
inability claim without matched evidence. The first direct baseline is
[region assay](overnight-20260928/fast_core_20261006/REGION_REPORT.md); existing
GROUP/MEM nesting is inert to tested proposal construction, not a hypothesis refutation.

## 2. Current evidence and uncertainty

| Goal | Evidence status | Principal gap |
|---|---|---|
| G1/G2 | bounded adaptation reported; caching and fixed-space alternatives remain | uncacheable heldout plus causal method ablation |
| G3 | no demonstrated L3 in inspected ownership evidence | learner-created useful form, not complete-form menu selection |
| G4 | narrow contract revision reported; general depth/representation transfer absent | unseen-depth, drift, and interference together |
| G5 | task-specific researcher scaffolding remains extensive | intervention ledger and frozen learner across tasks |
| G6 | explicit contracts and memory policies reported | path coverage, revocation, growth, cross-contract isolation |
| G7 | limited unification reported | simpler matched representations and actual core integration |
| G8 | fresh matcher audit confirmed order-dependent false negatives | qualify evaluators before interpreting learning |

The ownership queue explicitly says `measure-tnn` has not run the canonical
learner. Harness/reproduction evidence must not be silently promoted to integrated
TNN evidence. Reports are evidence leads, not fresh replication.

## 3. Common experiment contract (binding for future preregs)

For each test write QUESTION, COMPETING HYPOTHESES, MINIMUM WORLD, CONTROLS,
EXPECTED DISCRIMINATOR, RUN, RESULT, WHAT IT KILLS, WHAT IT DOES NOT KILL,
NEXT QUESTION. Freeze concrete fixtures, seeds, horizons, thresholds, and artifact
paths BEFORE implementation. A plan row is not permission to choose bars after data.

Required whenever relevant:
- fresh, facts-only, facts-retained/method-erased, frozen-method, shuffled-state,
  stronger simple heuristic, and equal-search-budget random/enumerative controls;
- paired identical experience; explicit differences in what each arm may retain;
- both operation/entity relabeling and alternative/order permutation;
- heldout queries whose answers were never observed or leaked via target labels;
- state fingerprints and write/read tracing proving intervention reaches behavior;
- explicit answerability/identifiability gate; do not penalize a learner for missing
  information which no allowed observer could obtain;
- independent oracle or exact hand derivation not generated by the tested scorer;
- separate correctness, coverage, abstention, effect violations, compute, and memory;
- compile success gates execution; nonempty outputs; runtime exit checked; repeat
  deterministic fixtures three times; stochastic tests need preregistered paired
  seeds and uncertainty, not repetition of a single seed;
- science in pure Zag, shell only orchestration; record source/compiler hashes;
- exact artifact schema: case, arm, seed, phase, query, state fingerprint, expected,
  predicted, actual effect, accepted, violation count, work units, memory bytes.
  If an interface cannot expose a field, record unavailable, not a fabricated zero.

No speedup claim without paired representative correctness and measured work/time.
Do not treat a facts-only oracle with privileged answers as a fair learning baseline.
Exhaustive search is a legitimate rival, not proof learning is impossible. Audit
whether retained experience changes future search, structure, or only answer lookup.

## 4. Prioritized hypothesis matrix

T00 is executed in the earlier audit. T01..T03 are now executed: see
[three-probe results](overnight-20260928/fast_goals_20261006/REPORT.md).
All other rows are PLANNED, not implemented capability claims.
Priority is information gain / cost, not probability of a positive result.

### P0 - qualify instruments and control semantics

| ID / goal | Question and competing hypotheses | Minimum world / controls | Discriminator and kill scope |
|---|---|---|---|
| T00 / G8 | Is production membership exact or greedy? | A0->A1 4; A1->3 or 34; all 340 strings; swap alternatives and rename terminals | Exact root accepts 2 and any-NT accepts 3 in both orders. CONFIRMED greedy defect: see fast_membership_order/REPORT.md. Kills current general matcher, not production representations. |
| T01 / G6 | Does contract growth preserve historical rejects, or widen through them? | Learn accepts {2,4}, reject {6}; observe success 8; unchanged u_grow vs frozen and fresh reinduction | Compare admission of 6 before/after; fresh reinduction proves representability. A regression kills growth-as-reject-preserving-control, not learned prediction contracts. |
| T02 / G6/G4 | Are failure/revision records local or shared across contracts? | Two independent contract bases in one arena; three A failures, query B; isolated-state control | B state/revision request must not change from A-only evidence if local semantics claimed. Shared global counters are not proof actual core cross-talk occurs. |
| T03 / G7/G1 | Do refined singleton kinds add behavior beyond flat observed-output membership? | Existing LCONT worlds; compare candidate sets and chosen outer IDs with flat probe_has; coarse/refined/facts retained | Identical choices kill necessity of kinds for this fixture, not kind learning broadly. Erasing kinds alone is weaker than a matched facts-only selector. |
| T04 / G8 | Do arms execute distinct intended state? | Fresh/trained/erased fingerprints, cold build; mutation defects; one behavior-changing state bit | Fail closed if labels mismatch fingerprints or interventions do not reach read sites. Qualify arm instrumentation before learner metrics. |

### P1 - establish learner ownership without task-specific help

| ID / goal | Question and competing hypotheses | Minimum world / controls | Discriminator and kill scope |
|---|---|---|---|
| T05 / G2 | Is the acquired object a method or answer cache? | holdout-uncacheable/program-lossy-style world; disjoint inputs; compact rule oracle; facts retained/method erased | Intact beats facts-only and method erasure at equal budget on unseen queries. No improvement kills tested method claim. Audit source candidate forms and all feedback. |
| T06 / G1 | Can experience disambiguate methods rather than source bias pick one? | join-underdet: two training-consistent rules disagree on heldout; one distinguishing observation available | Before witness, uncertainty is correct; after witness, behavior follows evidence under label swaps. Without witness cannot claim unique acquisition. |
| T07 / G5 | Is competence frozen-source, or researcher rescued? | Frozen learner checksum across three sealed task laws; same interface; explicit intervention ledger | Experience-only improvement with zero task-specific edits/resets/labels. Count interaction and compute costs; zero manual edits alone is not enough. |
| T08 / G3 | Does learner create useful composition rather than select whole-form menu? | Missing bridge world; primitive operations available but no complete bridge stored; novel lengths/combinations held out | Persist new executable structure, causal erase loss, transfer and revision. Compare matched enumeration. Finite DSL success alone is not L3; finite syntax alone is not a disproof. |

### P2 - transfer, revision, and active information acquisition

| ID / goal | Question and competing hypotheses | Minimum world / controls | Discriminator and kill scope |
|---|---|---|---|
| T09 / G4 | Does structure generalize depth or memorize finite expansions? | Genuine recursive grammar, train depths 1..3, test 4..8; qualified bounded parser, recursive oracle, flat facts | Exact heldout positives AND negatives; distinguish parser depth cap from learner failure; avoid any-NT union masking root errors. |
| T10 / G4/G7 | Does one structure transfer representations without source switch? | rep-dual: same relation encoded as sequence and relation table; generic encoding, no task label to learner | Freeze state learned in A, evaluate B; compare representation-switched source oracle and flat baseline. Adapter complexity disclosed, not treated as free. |
| T11 / G4 | Can methods revise and retain unrelated competence? | A->B->changed A->A+B, facts erased controls; misleading episode then corrective evidence | Revised heldout A improves; B remains correct; traces identify changed method. Predefine recovery exposure and tolerated interference. |
| T12 / G1 | Does inquiry learn information acquisition or follow a supplied heuristic? | Disambiguating action costs in join-underdet; random/fixed/uncertainty/greedy-info/oracle budgets matched | Learned policy lowers total evidence+compute cost on heldout laws versus strong greedy-info; more queries alone is not gain. |
| T13 / G2/G4 | Is causal intervention choice learner-owned? | Two observationally equivalent worlds separated by allowed intervention; intervention costs; observations-only and random controls | After intervention evidence, predictions transfer to new interventions; no hidden causal labels/answer menu. Without available distinguishing action, world is unidentifiable. |
| T14 / G1/G4 | Is meta-learning more than caching or erased priors? | Unseen rule parameters, partial observation; prior carrier traced through acquisition; relevant/irrelevant/misleading/fresh | Paired acquisition cost improves on new parameters without retained answers; exact measurement and anti-saturation gate. Carrier surviving is necessary, not evidence of benefit. |

### P3 - reliable control and one persistent substrate

| ID / goal | Question and competing hypotheses | Minimum world / controls | Discriminator and kill scope |
|---|---|---|---|
| T15 / G6 | Are authorized hard limits enforced at effects or only proposals? | Allowed goal with forbidden side effect; direct, composite, nested and replay paths; drift/growth | Every path logs effects; zero forbidden effects on exhaustive finite fixture, useful allowed goals still solved. Abstain-always is safe but not capable. Hard-policy authority immutable to learner updates. |
| T16 / G6 | Do revocation/rollback survive aliases and cached composites? | Create method+alias+composite, revoke one operation, resume/reload/checkpoint | Revoked effects never execute; unrelated capabilities preserved; no stale replay bypass. Version/provenance audit plus direct runtime effects. |
| T17 / G6/G4 | Are learned constraints robust to noisy feedback? | One deceptive success or mislabeled outcome, corrected later; genuine safe cases and actual forbidden effect oracle | Predictive confidence may adapt; hard limits cannot widen. Report false admission and false denial separately, not just accuracy. |
| T18 / G7 | Is graph topology causally useful or equivalent storage? | graph-vs-flat with equal facts, query access, search budget and memory; topology erase/rewire and rename | Intact topology improves heldout behavior beyond flat table; ablation loss not explained by destroyed facts or unfair lookup costs. No result generalizes to all graphs. |
| T19 / G4/G6 | Can one learner persist under interference and memory pressure? | A->B->C->changed A->A+B->misleading->pressure->reuse; same instance; pin/unpin/eviction controls | No source task router; measure retention, recovery, capacity, dropped inputs and policy violations. Memory retention alone is not method ownership. |
| T20 / G7/G8 | Do harness results occur in the actual TNN interface? | Minimal winning fixture ported to canonical learner with same evidence protocol | Direct end-to-end behavior, no reproduction substitute. First deliverable is an interface/adapter audit if canonical interface absent. |
| T21 / G5/G6 | Does TNN beat a transformer on these goals? | Same feedback, tools, effect guards, task exposure and heldout laws; report training differences | Human intervention, success, compute and violations all measured. Not scheduled in this short pure-Zag wave: no matched transformer runner qualified here. No blanket superiority claim. |

## 5. Recommended order and stop rules

1. Execute T00..T03 as cheap instrument/representation checks (this fast lane).
2. Main builder qualifies membership and contract semantics; do not add specialist
   layers merely to protect a scorer which is wrong.
3. Run T05/T06 first ownership gate, paired with T15 minimal authority test.
4. Only survivors proceed to T09/T11 and T20 actual-interface replication.
5. Add inquiry/causality/meta-learning when their information and carrier gates pass.
6. Graph expansion or large scaling comes after a causal advantage, not before it.

If a test fails, stop the associated claim, not the whole architecture. A repaired
implementation needs a new prereg or clearly declared repair protocol and full
rerun. Unexpected findings do not license silently changing bars. Preserve failures.

## 6. General competence probes beyond answer prediction

- **Act rather than guess:** acquire and execute methods on uncached world states;
  record real intermediate/final effects, not only predicted outcomes. Separate
  evaluator knowledge of desired effects from learner access to sealed answers.
- **Communicate rather than complete text:** learn a small compositional signaling
  protocol from interactions; a listener must accomplish unseen referent goals.
  Rename symbols, swap speakers/listeners, withhold novel combinations, measure
  pragmatic success versus phrase lookup. A synthetic language is not human fluency.
- **Reason rather than repeat:** reuse acquired relations to derive unseen consequences,
  with underdetermination/abstention controls. Test counterexamples and method erasure.
- **Think for itself rather than follow source curriculum:** learner chooses which
  observation/action to take under budget; compare strong information/cost heuristics.
  Researcher-authored exploration algorithms are generic bias, not earned meta-policy.
- **Know when to revise:** preserve useful practice but challenge it under contradictory
  effects; neither reflexive guessing nor immutable lookup meets the full goal.
- **Human breadth is an aspiration:** passing one toy action/language fixture does not
  imply human-like cognition, consciousness, or biological brain equivalence.

These complement T05..T20, not permanent specialist modules. They require concrete
preregistrations and qualified worlds before execution.

## 7. Doc-reading and handoff rules

- Historical REPORT/PREREG files remain unchanged. Corrections to their current
  interpretation live in CURRENT_EVIDENCE_NOTES.md, linked from FRONTIER_QUEUE.
- HYPOTHESIS files describe proposals; words such as PASS by construction are
  design assertions, not observed bars. No scheduler/epistemics terminology decides
  whether retained state adds useful behavior; rival schedulers can also retire and
  retry operators.
- Existing-world names in this plan are target specifications from the brief, not
  promises that exact drivers exist on this branch. Search/port before implementation.
- Run-specific prereg and results: overnight-20260928/fast_goals_20261006/.
- First falsifier evidence: overnight-20260928/fast_membership_order/REPORT.md.
