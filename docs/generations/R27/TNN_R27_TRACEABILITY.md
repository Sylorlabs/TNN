# Causal Traceability Contract

Each consequential mutable decision is represented as a parent-linked trace event with: development step, subsystem stage, generic reason code, internal subject/candidate ID, evidence strength, confidence/uncertainty, and parent event ID.

Stages cover sensor, PAM, routing, entity, memory, world model, language, social learning, architecture revision, and action/observation decisions.

Failure reasons are generic: evidence gain, uncertainty, contradiction, plateau, memory miss, route miss, representation loss, resource pressure, regression, verified gain, source conflict, delayed regret. They do not encode evaluator answers or task labels.

The intent is to reconstruct a causal chain such as:

`raw evidence -> core signature -> PAM route -> entity hypothesis -> memory retrieval -> world/language binding -> decision -> error -> failure diagnosis -> PAM/memory revision`

Trace infrastructure is protected core observability. TNN may learn from its traces but cannot rewrite the immutable root verifier.

## 2026-09-05 white-box extension

The project now treats causal traceability as a promotion gate for all future
mutable cognition, not only action decisions. The target is that TNN remains a
white-box architecture even as memory, routing, Foundry structures, and large
connection systems become learner-owned.

Every consequential mutation must additionally record:

- parent checkpoint / mechanism version;
- exact trainer/teacher/direct-evidence provenance that contributed to the update;
- parameter, memory, route, or architecture fields changed;
- affected resource allocation;
- proposed reason / expected gain;
- pre-change capability-regression fingerprint where applicable;
- shadow/canary result for structural changes;
- promotion or rollback decision;
- authority level that permitted the mutation.

All promotion-eligible mutable stores must participate in deterministic
serialization, integrity hashing, provenance, and inspection. The target
`dark_state_count` is zero: a mutable store that can affect cognition but cannot
be reconstructed or attributed is an architecture defect, not an acceptable
black-box exception.

Trainer state and evaluator state remain separate. Trainer goals, curriculum,
values/policies, demonstrations, and permissions receive explicit trainer
provenance. Hidden evaluator truth/membership may score behavior but cannot enter
learner traces as an inference input.

Human-facing inspection should be able to reconstruct:

1. why an action was chosen;
2. which alternatives were live;
3. what memory and modules were used;
4. what changed during training;
5. the earliest causal change associated with a regression;
6. what information came from the trainer versus direct evidence;
7. which structural candidate was promoted or rolled back and why.

Natural-language explanations may summarize these records but are not themselves
proof of causal traceability. See `TNN_ARCHITECTURE_ROLES_AND_CONNECTIONS.md` and
`TNN_MEGA_PLAN_WHITE_BOX_DEVELOPMENTAL_ARCHITECTURE.md` for the authority and
milestone contracts.
