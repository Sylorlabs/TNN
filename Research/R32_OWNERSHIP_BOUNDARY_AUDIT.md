# R32 — Cognitive Ownership Boundary Audit

Date: 2026-08-30  
Status: `ACTIVE ARCHITECTURE AUDIT — NOT A PROMOTION CLAIM`  
Canonical: R27 step 60,423

## Ownership principle

TNN should own **modifiable cognition**, not **the laws that certify cognition**.

The target is a machine intelligence whose non-protected cognitive state is first-class, inspectable, causally attributable, and writable by the learner itself. TNN should be able to discover that an internal influence exists, trace what it affects, estimate whether it helps or harms delayed grounded utility, and strengthen, weaken, gate, reroute, split, merge, create, archive, restore, or replace it when evidence justifies the change.

That does **not** imply that TNN should own evaluator truth, provenance integrity, the immutable raw-evidence record, hardware/resource hard limits, compiler correctness, or the external verifier. Those are part of the protected shell / world boundary rather than cognition.

## Current ownership classes

- `OWNED`: the learner already updates/selects the state from grounded experience in the relevant implementation.
- `PARTIAL`: learner-owned state exists, but its vocabulary, search grammar, schedule, or scope is still researcher supplied.
- `EXTERNAL`: cognition-relevant choice is still selected by researcher/runtime rather than TNN.
- `PROTECTED`: intentionally outside learner write authority.

## Audit

| Domain | Current class | Current boundary | Intended direction |
|---|---|---|---|
| source trust | OWNED | updated from later grounded outcomes | keep learner-owned |
| source dependence | PARTIAL | mutable penalty exists, update form remains authored | let TNN learn richer dependence models |
| consequence associations | OWNED/PARTIAL | learned values inside fixed hypothesis/action vocabulary | expand to learner-created entities/actions/consequences |
| temporal hazard state | PARTIAL | values learn, horizon vocabulary and update law are fixed | learner-select temporal abstractions and forecasting structure |
| terminal action values | PARTIAL | learned weights; E52A learner selected eight pair interactions | TNN should own representation growth and replacement more generally |
| continuation value | PARTIAL | learned but E52B unstable; E53 changes update substrate | stabilize and then make meta-control learner-owned |
| average reward / resource shadow price | PARTIAL | E53 has mutable learner state, but full discriminator is not yet executed | integrate into continuing cognition |
| replay mixture | EXTERNAL/PARTIAL | E53 core accepts current/replay masses supplied by caller | TNN chooses retention/replay mixture from delayed utility |
| update rate / trust region | EXTERNAL/PARTIAL | rate, residual clip, value clip are caller inputs | TNN selects/adapts its own safe update geometry |
| feature / representation coordinates | EXTERNAL/PARTIAL | most current 32 coordinates are authored; Foundry can add bounded pair products | TNN creates, composes, retires, and replaces useful coordinates |
| Foundry search grammar | PARTIAL | learner chooses within researcher-defined bounded pair-product grammar | learner expands its own non-core mechanism grammar under verification |
| hypothesis ontology and cardinality | EXTERNAL/PARTIAL | current native discriminator is principally A/B/UNKNOWN | TNN creates, splits, merges, and retires arbitrary grounded hypotheses |
| action vocabulary | EXTERNAL/PARTIAL | KEEP/CURRENT/RESTORE/UNKNOWN/CONTINUE supplied | TNN creates reusable options, skills, probes, subgoals, and action abstractions |
| investigation target | EXTERNAL/PARTIAL | frontier mostly learns whether to continue; evidence stream/action family is supplied | TNN chooses what observation/action/viewpoint would best discriminate hypotheses |
| memory policy | PARTIAL | authority target is TNN, but current state still records `PRIVILEGED_GENERIC_HEURISTIC` defaults | TNN owns exact/compressed/archive/retrieval/consolidation decisions end-to-end |
| self-created chunks | PARTIAL | strong R31/reference evidence; native integrated reproduction still pending | native reversible learner-owned abstraction hierarchy |
| sensory PAM choice | EXTERNAL/PARTIAL | researcher currently compares temporal raw, segmented recurrent, etc. | TNN selects/constructs sensory mechanisms from experience |
| internal routing/connectivity | EXTERNAL/PARTIAL | individual weights/interactions are mutable, but no complete self-description/write surface for all non-core causal influences exists | first-class connection/influence registry with learner read/write authority |
| module/PAM creation | PARTIAL | bounded Foundry evidence exists; broad autonomous mechanism invention is not demonstrated | learner creates and shadow-tests non-core PAMs |
| compute/cognitive scheduling | EXTERNAL | runtime/researcher decides most execution allocation | TNN allocates compute, parallelism, rehearsal, consolidation, and investigation effort |
| curriculum / experience selection | EXTERNAL/PARTIAL | researcher supplies experimental worlds; active observation is bounded | learner increasingly chooses useful experiences while world truth stays external |
| social inquiry protocol | PARTIAL | Master/sibling framework is designed externally | TNN owns when/who/what/how to ask, verify, teach, and discount; teacher remains external |
| goal/subgoal hierarchy | EXTERNAL/PARTIAL | root grounded utility geometry is supplied | retain protected root constraints; let TNN create instrumental goals and priorities |
| full online self-modification | PARTIAL | E53 has conservative update/rollback primitives | extend to every non-core cognitive mechanism with causal trace and rollback |

## Protected shell — intentionally not TNN-owned

The following remain externally authoritative even in a mature TNN:

- environment/world truth and real consequences;
- hidden evaluator labels, benchmark modes, and answer keys;
- immutable provenance roots and causal-trace integrity;
- immutable/raw evidence record needed to detect reinterpretation or falsification;
- verifier logic and scientific promotion criteria;
- compiler/runtime correctness and hardware safety limits;
- human permissions and hard safety boundaries;
- canonical release/promotion decision.

TNN may model these boundaries and reason about them, but it must not silently rewrite the evidence or verifier that judges its own changes.

## Highest-priority ownership transfers

1. **Meta-learning control** — TNN selects replay mixture, update rate, and trust-region magnitude from delayed grounded utility instead of receiving a caller schedule.
2. **Hypothesis creation** — move beyond fixed A/B state toward learner-created competing world hypotheses with split/merge/retirement.
3. **Investigation selection** — own *what to inspect/do next*, not only CONTINUE versus terminate.
4. **Connection/influence introspection** — expose every non-core causal influence through a self-describing learner-readable/writeable registry.
5. **Representation/PAM invention** — expand beyond researcher-authored coordinates and bounded pair products.
6. **Memory/compute scheduling** — learner controls storage, retrieval, consolidation, rehearsal, parallelism, and compute allocation.

The next native pressure test targets item 1 because E52B's oscillation makes it immediately causal to the current frontier. It does not claim the other ownership gaps are solved.