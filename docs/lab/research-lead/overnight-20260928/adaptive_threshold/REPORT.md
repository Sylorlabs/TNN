# Adaptive Threshold: Report

## Verdict: ADAPTIVE-THRESHOLD-COMPLETE

The evidence threshold is now a learner-state value written by experience.
It adapts to experienced noise: T=2 in stable, T=5 in noisy, T=3 (transient)
in changing environments. 3/3 byte-identical per arm.

## Mechanism

One evidence node (tag 40, subtype 3) holds learner-owned evidence state:

- V: current run value, R: current run length
- E: error score (+3 on revelation mismatch, -1 on match, floor 0)
- T: threshold = 2 + E/3, clamped to [2,5]
- writes, mismatches, maxT: diagnostics

Write rule: when R >= T and V differs from the default action, write V to
the policy default (field 20, the same production path as Node2-v2).
The uncertainty preamble, the write path, and the guide read path are
unchanged: Links 1, 3, 4 of the ablated causal chain are intact. Only the
record-to-write condition changed.

Variant core differs from the tested Node2-v2 core by exactly one line:
the call inside `ev_observe_aw` is redirected from `resolve_uncertainty_v2`
to `resolve_uncertainty_adaptive`. See BUILD.md.

## Results

Adaptive arm (SHA-256 `ea5d31fcd2cd9a62d5db0d482f3292557b4904499001eebb8ac5213d2ca1ba2b`):

| Environment | default | T | E | writes | mm | maxT | guide |
|-------------|---------|---|---|--------|----|------|-------|
| stable | 45 | 2 | 2 | 1 | 0 | 3 | 45 |
| noisy phase 1 | 30 | 5 | 12 | 0 | 4 | 5 | - |
| noisy phase 2 | 45 | 5 | 10 | 1 | 4 | 5 | - |
| changing mid | 45 | 2 | 2 | 1 | 0 | 3 | - |
| changing end | 60 | 3 | 3 | 2 | 1 | 3 | - |

Fixed arm (SHA-256 `06b2022d04f933bcf2f8fbc154eb657cbfa102579d6ac2b90395c45aade3d949`):

| Environment | default | history after |
|-------------|---------|---------------|
| stable | 45 | reset (wrote at 3) |
| noisy phase 1 | 45 | reset (wrote on 3-tail) |
| noisy phase 2 | 45 | (45,45,45), no write |
| changing mid | 45 | reset |
| changing end | 60 | reset |

## Per-environment analysis

**Stable (45,45,45).** Adaptive commits after 2 revelations: T falls 3 to 2
as consistency accumulates. Faster than the fixed 3. The later miss builds
a guide carrying 45, confirming the adaptive write propagates through the
production read path.

**Noisy (45,46,45,45,47,45,45,45).** Two noise spikes drive E to 12 and T to
5. The 3-tail of 45s is not enough: R=3 < T=5, default stays 30, zero
writes. The fixed arm commits on the same 3-tail despite 4 prior mismatches.
This is the core behavioral contrast: the adaptive learner demands more
evidence precisely when its recent experience has been noisy.

**Noisy phase 2 (three more 45s).** After 5 consecutive 45s, R=5 >= T=5:
the learner commits. Caution is not paralysis; sustained stability
overcomes the noise penalty.

**Changing (45,45,45 then 60,60,60).** Adopts 45 quickly (T=2), then the
first 60 registers a mismatch (mm=1, E rises, T goes 2 to 3), and after 3
consistent 60s revises the default to 60. Revision works with an adaptive
delay proportional to the detected change.

## Learner-ownership analysis (honest)

RESEARCHER-OWNED: the update rule itself. E moves +3 on mismatch and -1 on
match; T = 2 + E/3 clamped to [2,5]; initial E=3; the run-length record
structure; the form of the write condition (R >= T). None of these were
learned.

LEARNER-OWNED: the values. T=2 vs T=5 vs T=3, E=2 vs E=12, the write
decisions and their timing. No researcher-set parameter determines that the
noisy environment gets T=5; that value is computed from the learner's own
mismatch history. The threshold is not "another tunable researcher field":
there is no field to tune, only experience to accumulate.

This matches the standing of Node2-v2's policy value (learner-owned value,
researcher-owned rule). What it is not: the rule itself being learned. A
stronger result would have the learner select or revise the adaptation rule
from prediction errors. That remains open.

## Answer to Micah's question

"Can TNN learn WHEN enough evidence has accumulated?" Partial yes. The
mechanism demonstrates a threshold value that tracks experienced noise
across environments (2/5/3), written by experience through the same
consequence chain the ablation validated. The mapping from noise to
threshold is researcher-authored. The "when" adapts; the "how to adapt"
does not.

## Limitations

- Three synthetic environments, one policy node, builder-run worlds.
- The +3/-1/E/3/clamp constants are researcher-chosen; only their
  consequences (the T values) are experience-driven.
- E has no forgetting beyond the -1 decay; a very old noisy past keeps T
  elevated until enough consistent revelations arrive (phase 2 shows this
  resolves, but slowly).
- Independent-adversary replication not run.

## Standing metrics

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 6 (evidence node layout, E update
  rule, T formula, clamp bounds, initial E=3, write condition form)
- LEARNER-OWNED STRUCTURAL DECISIONS: 1 (the threshold value T over time,
  plus write timing)
- SOURCE-ENUMERABLE FORMS: 0
- SUF DECISIONS: 0
- LEARNER-INTERNAL CRITERIA: 0
- REUSE EVENTS: 0
- REVISION EVENTS: 1 (changing env, 45 to 60, adaptive delay)
- COGNITION LINES: ~80 new (evidence node, adaptive resolve)
- MODES: 0, BRIDGES: 0, HANDLERS: 0, SEMANTIC CASES: 0
