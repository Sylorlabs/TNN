# TNN continuing learner architecture assessment

Date: 2026-09-12  
Scope: R33 current evidence and the native continuing-life engineering workstream

This assessment answers the operational question for this phase: can the same
learner become more capable through experience, preserve earlier capability,
adapt to changed conditions, and need less help? The current evidence does not
yet support that claim. The main reason is structural: the repository contains
several qualified or partially qualified mechanisms, but no native, behaviorally
continuous R27 learner wired through the full observation, memory, hypothesis,
action, consequence, and update loop.

## What is actually connected

The new native workstream connects an observation contract to a deterministic
world, records actions and delayed consequences in the world state, and commits
complete world-plus-ingress checkpoint sections through descriptor-rooted
storage. A fresh process reconstructs the checkpoint and produces the same next
world states and consequences. The `learn` entry point still refuses to launch
while the reviewed R27 behavioral runtime is pending.

The current path is therefore:

```text
encoded observation -> stream validation -> world action -> consequence
                                      \-> complete checkpoint/reload
```

The missing path is:

```text
experience -> learner-owned memory/hypothesis change -> selected action
           -> attributed consequence -> native learner update -> preserved reload
```

The missing path is the decisive limitation. The new world and checkpoint
fixtures are deliberately not presented as a TNN brain or as a learning result.

## Evidence map

| Area | Working evidence | Current boundary |
|---|---|---|
| Native digest identity | N17 exactly recomputes the historical R26 and R27 semantic digests | Full verifier behavior, R25 lineage, policy and runtime rows remain open; digest equality is not behavioral continuation |
| Runtime and telemetry | N19 BUILD_06 has a narrow append and separate-process recovery pass | Review V2 still leaves root custody, errno mapping, crash durability, resource enforcement, and execution-level telemetry qualification open |
| Synthetic adaptation | N16 is a consumed synthetic support-routing qualification | It used researcher-selected projection/preservation controls and a synthetic parent; no R27 continuity or general continuing-life claim follows |
| Encoded sensory transport | N14 is a consumed bounded PCM16LE/RGB8 information-preservation pass | Physical microphone/camera transport, timing qualification, semantic perception, and changed-condition learning remain open |
| Current workstream | `common.zag`, `observation.zag`, `world.zag`, `checkpoint.zag`, `storage.zag`, and `driver.zag` pass CL-ENGINEERING-01 | Engineering fixtures contain no learner update and use no scientific population |

The dated handoff is retained under `HISTORY_BEFORE/`. It is not the current
status source: the local N17 and N19 status records are newer and explicitly
keep the continuity and runtime gates open. R27 remains the accepted parent at
step 60,423 with zero newborn restarts; no file in this workstream mutates it.

## Ownership of decisions

| Decision | Current owner | Evidence or implication |
|---|---|---|
| Observation bytes, provenance, source/clock metadata | Native interface, with the researcher defining the wire contract | The new observation module retains raw bytes and rejects malformed or out-of-order records |
| World dynamics, action meanings, delayed consequence timing | Researcher-designed fixture | `world.zag` is a controlled environment for later experiments; these choices are not learned by TNN |
| Checkpoint section layout and custody policy | Researcher-designed protected substrate | The contract provides complete state transport, not a learned memory policy |
| Action selection and hypothesis formation in the integrated learner | Not currently implemented in this workstream | `learn` remains refused pending the R27 behavioral runtime |
| N16 routing/preservation mechanism | Candidate mechanism selected and bounded by the researcher | It needs matched controls and mechanism-removal tests inside a fresh continuing-life campaign |
| Goals, values, permissions, curriculum, rollback, and evaluator separation | Trainer/protected supervisor by architecture policy | The new fixtures do not silently inject hidden answers into learner inputs |
| Pass/fail checks, hidden-state comparison, and resource accounting | Evaluator/supervisor | These checks are evidence about the system, not cognition supplied to it |

## Retain, revise, missing, unsupported

### Retain

- R27 as the accepted immutable parent and all consumed experiments as historical evidence.
- Native Zag as the forward execution language and white-box inspection boundary.
- Raw sensory evidence beside any future learned abstraction.
- Descriptor-rooted persistence, predecessor digests, explicit provenance, and fail-closed recovery.
- A separate world-owned evaluator view so hidden regime, object identity, and future consequence are not learner observations.
- N16 as a candidate mechanism to test, not as an assumed explanation of improvement.

### Revise

- Use this workstream as the current entry point rather than the stale J091
  handoff. The handoff remains historical evidence.
- Treat “native digest match” and “runtime recovery pass” as component claims
  with their stated scopes. Neither should be summarized as a continuing learner.
- Make every future checkpoint include all learner-owned mutable state, causal
  trace attribution, world state, and sensory ingress state in one admission and
  reload operation.
- Separate engineering witnesses from scientific exposure. The current run is
  an engineering result and does not open a training or validation gate.

### Missing

- Exact native verifier-equivalent R27 continuation, including all unresolved
  source-line, policy, manifest, runtime, and lineage rows.
- A native learner state that receives observations, owns memory/hypotheses,
  selects actions, attributes delayed consequences, and updates itself.
- Durable serialization of that complete learner state and causal trace,
  followed by behavioral comparison before and after a fresh-process reload.
- Qualified real audio/visual device transport and timing, followed by changed
  condition perception tests using raw evidence only.
- A preregistered continuing-life population with fresh evidence partitions,
  matched controls, mechanism-removal arms, resource accounting, and help
  withdrawal.

### Unsupported claims

The repository does not currently support claims of integrated learning,
retention plus new acquisition, transfer to unfamiliar combinations, reduced
assistance, physical sensory perception, R27 behavioral continuity, or learner-
owned structural self-modification. More checkpoints, longer execution, or a
larger test count would not close those gaps.

## Decision for the next phase

Keep the two tracks parallel. Finish N17's verifier-equivalent continuity rows
and N19's runtime boundary, while qualifying real transport independently. Then
wire the same accepted parent and complete learner state into the world and
sensory ingress interfaces. Only after that should a fresh scientific campaign
test acquisition, retention, transfer, changed conditions, reload continuation,
and withdrawal of assistance under the frozen gate in
`SCIENTIFIC_CAMPAIGN_GATE.md`.

