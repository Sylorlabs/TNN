# TNN autonomy position

## Core position

TNN should become more autonomous in deciding **how to learn**, not in
silently deciding what it is allowed to do.

The trainer should provide goals, values, boundaries, experiences, resources
and real-world permissions. Within those constraints, TNN should increasingly
own the decisions that determine whether learning is effective:

- what deserves attention;
- what should be repeated, replayed or rehearsed;
- what should be remembered exactly versus compressed;
- which competing hypothesis needs more evidence;
- which observation or action would be most informative;
- when to answer, investigate, defer or say UNKNOWN;
- which representation or reversible chunk is worth forming;
- which failure deserves a new mechanism;
- when to ask the trainer, teacher or sibling for help; and
- when not to change itself.

This is different from giving TNN unrestricted autonomy. The learner must not
grant itself authority, rewrite its protected verifier, erase provenance,
restore expired permissions, bypass rollback, or redefine the trainer's values.

## What autonomy should mean in practice

Autonomy should be measured by decision ownership, not by human-like language
or by the number of components in the system. A more autonomous TNN should be
able to start with the same broad learning loop and independently choose:

```text
observe
→ identify uncertainty or opportunity
→ select memory, practice, inquiry or action
→ predict the consequence
→ observe what happened
→ update its model and learning policy
→ decide what to do next
```

The trainer may define the destination and forbidden regions. TNN should learn
the route, pacing, representations, memory strategy and evidence-seeking policy.

## Autonomy levels

| Level | TNN owns | Still externally protected |
|---|---|---|
| A0 — passive learner | Parameter updates from supplied examples | Data order, repetition and evaluation procedure |
| A1 — active learner | Replay, rehearsal, retrieval and practice selection | Goals, values, resource ceiling and allowed actions |
| A2 — inquisitive learner | Hypothesis alternatives and evidence-seeking actions | Safety boundaries and external permissions |
| A3 — representational learner | Chunks, abstractions, memory placement and local specialization | Raw-evidence retention floor and rollback |
| A4 — constructive learner | Shadow proposals for new non-core modules or wiring motifs | Promotion gate, canary, provenance and resource limits |
| A5 — developmental learner | Learning strategy, architecture-search policy and when not to modify itself | Protected verifier, trainer policy, authority and irreversible actions |

Higher autonomy must be earned through evidence. It is not unlocked because the
system produces convincing explanations, passes a language benchmark, or asks
for permission in natural language.

## What would make TNN genuinely autonomous

The decisive demonstrations should show that TNN can:

1. choose useful replay and practice without a fixed hand-authored schedule;
2. notice when its current representation is inadequate;
3. select an observation that separates live hypotheses;
4. improve from consequences rather than hidden answer labels;
5. preserve old capabilities while learning new ones;
6. discover reusable representations across more than one task or modality;
7. request assistance when it predicts that assistance has positive value;
8. withdraw assistance and retain the competence it genuinely learned;
9. propose a structural change, test it in shadow, and reject it when it fails;
10. explain decisions through causal traces that match its actual state; and
11. voluntarily choose restraint when additional learning or action is not worth
    its cost or risk.

## Anti-facade tests

Autonomy claims should fail if any of the following is true:

- the trainer secretly chooses the examples, replay schedule or answer path;
- a fixed probe count or confidence threshold replaces inquiry;
- evaluator labels influence learner routing or memory selection;
- a teacher's answer is recorded as learner discovery;
- each new task receives a bespoke module and bespoke objective;
- the system cannot state what evidence would change its decision;
- the learner's explanation cannot be reconstructed from durable state; or
- a capability disappears when prompting, retrieval, demonstrations or teacher
  support are withdrawn.

## Relationship to transformers

Transformers can display impressive intelligence-like behavior through next-token
prediction because language is rich training data. TNN should not claim superiority
merely because it uses a different objective. Its autonomy claim becomes stronger
only if the learner itself controls more of the learning process: what to retain,
what to practice, what to investigate, how to represent experience and whether a
change is worth making.

The most important future comparison is therefore not just benchmark accuracy.
It is matched learning opportunity under teacher withdrawal, delayed testing,
new sensory conditions, interference, active inquiry and resource pressure.

## Current status

This is a design position, not a claim that current TNN has achieved these levels.
The current R33 work has qualified bounded native engineering and synthetic
learning mechanisms, but not a complete autonomous continuing learner. R27 remains
canonical, and learner authority and promotion remain unqualified.
