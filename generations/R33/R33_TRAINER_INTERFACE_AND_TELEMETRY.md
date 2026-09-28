# R33 human-trainer interface and telemetry

Status: specification and machine-readable event schema, not a working dashboard.
Schema: [R33_TELEMETRY_SCHEMA.json](R33_TELEMETRY_SCHEMA.json).
Trainer means human/person/group; automated teacher help remains separately
identified. Canonical R27 unchanged.

## Trainer workflow

The trainer declares a competency, desired behavior, permitted experiences and
actions, policy/resource constraints, acceptable risk and retention horizon.
Demonstrations, corrections, prompts, permission changes and withdrawals become
immutable attributed input events. The trainer teaches goals and consequences,
not hidden internal answers or hand-set parameter values.

For each lesson the dashboard offers: overview of learning; fresh versus
replayed exposure; transfer/retention curves; confusion and failure examples;
help dependence; retrieved evidence; an internal-change diff; and resource use.
Every point opens the underlying events, checkpoint and metric definition.
Unmeasured panels show `NOT_MEASURED` with a reason, never a guessed zero.

## Required measurements

| Trainer question | Metric / operational definition | Evidence and exclusions |
|---|---|---|
| Is it learning, how quickly? | Success versus unique experience, total presentations and measured compute; time/exposure to preregistered competence | Separate physical executions from branch-lineage presentations and replay; show every fixed checkpoint |
| Does it generalize? | Fresh-example performance on unseen payloads/contexts; transfer to altered nuisance or causal structure | Record overlap checks and source groups; a new rendering of the same example is not automatically an independent sample |
| What is memorized? | Exact-repeat reproduction, near-neighbor interpolation, held-out composition and changed-context tests reported separately | Memory-dependent success is valid capability but not evidence of abstraction; labels are operational, not claims about inner understanding |
| What is retained or forgotten? | Prior-success bitset, newly lost/rescued, ever-lost, worst simultaneous loss, delayed final retention and interference matrix | Follow the same anchors over time; regained final success never erases earlier failures |
| Where is it confused? | Known/unresolved cases, hypothesis competition, empirical calibration and errors by cause/condition | Separate failed UNKNOWN from correct UNKNOWN; heuristic confidence is not a probability |
| Does it need help? | Unassisted versus assisted success, help requests, refused/accepted help, interventions and assistance dose | Any intervention during a qualification episode marks it assisted; teacher competence never becomes learner competence |
| Is memory working? | Retrieval attempted/found/useful, latency and bytes; exact versus approximate reconstruction | Denominators include misses; random/FIFO/LRU controls remain separately labeled |
| What changed internally? | Parameter/memory/route/structure before-after digests, affected coordinates/ranges, update rule, evidence ancestry | Association with a lesson is not proven causal improvement; stronger attribution requires a frozen-control or ablation contrast |
| What did it cost? | CPU/wall time, peak/resident memory, logical bytes, active/stored parameters and connections, operations, I/O, teacher effort | Mark estimates and measurement method; record routing, replay, search, logging and verifier overhead |

The competency snapshot includes examples seen, unique/replayed counts, curve
points, fresh performance, delayed retention, uncertainty/hypotheses, known and
unresolved counts, error taxonomy, operational memorization/transfer indicators,
help dependence, retrieval success, forgetting, interference, lesson deltas,
interventions and resource measurements. Incomplete fields are explicit nulls
with coverage reasons. No summary may silently drop a required hard slice.

## Event contract

Each event binds experiment, branch/brain, episode/experience, competency, monotonic
event ordinal, parent event IDs, source payload digest, policy/grant version,
checkpoint before/after, causal references, action and outcome references,
mutation record, help attribution, resource record, and observation coverage.
Evaluator truth and assessment-only metric records are stored in a separate
access domain. Training targets are admitted only at their declared consequence
time and cannot reveal future or withheld assessment truth.

Content hashes identify exact payloads; episode IDs distinguish repeated
presentations. Group IDs expose shared speaker/object/world provenance to the
evaluator, not as hidden learner features. A lesson can span multiple competencies;
use explicit allocation rather than double-counting total compute.

## Views and trustworthy explanations

The brain view shows the active modules and state that actually exist. The
decision microscope follows evidence to hypotheses, values, action, outcome
and update. The training diff shows changed state with evidence provenance.
The lineage view distinguishes accepted parent, diagnostic forks and proposed
modules. The intervention view shows all human and automated aid. The failure
view separates sensory loss, support gaps, retrieval, routing, objective,
optimization, interference and resource failures, marking untested diagnoses
as hypotheses. The resource view separates capacity from active work.

Generated prose may paraphrase cited records, but cannot invent a rationale.
When the causal chain is incomplete, display the missing link. Version all
aggregation formulas and expose numerators, denominators, uncertainty and sample
units. Validate telemetry with synthetic negative fixtures before training.

Preservation-rule lessons additionally expose proposals, accepted and rejected
updates, visited states, the fixed original preservation-reference digest,
cumulative constraint deltas and useful-learning progress. Rejected optimizer,
RNG, recurrent, parameter and memory changes must be attributable, including
their restoration. Presentation count is not update count. Charge the failed
proposal and verifier overhead even when operational learner state rolls back.
Use the learning-curve, lesson-delta, exposure and resource categories in the
schema; the scientific batch must bind their detailed metric definitions before
claiming those quantities are measured.

## Withdrawal and permissions

Competency-level help progresses only through the gates in
[withdrawal plan](R33_HAND_HOLDING_WITHDRAWAL_PLAN.md). Human permission for a tool
and scientific qualification to operate independently are distinct. A trainer
may keep assistance or authority more restricted even when a component qualifies.
Policy changes require a trainer-authored input event and cannot be synthesized
from learner text that merely claims permission.
