# R27 Accepted Brain State — White-Box Schema Map

**Agent:** A (Brain Cartographer) · **Date:** 2026-09-19
**Source branch:** `tnn-native-lab` @ `30fb66c4e68a` (same as main at map time)

## 1. Artifact provenance

| File | Repo path | Git blob SHA | Bytes |
|---|---|---|---|
| `parent-r27-accepted-state.pkl` | `docs/generations/R33/runs/R33_PARENT_RECOVERED_V1/` | `ceda86509a9e22db8783567f65e377ab860f13da` | 15,871,908 |
| `parent-r27-accepted-policy.json` | same dir | `3941fe06c68a590458f69d1a1d9e4c5ba6acdb7c` | 712 |

Canonical invariants (verified from the artifact itself):
- `format = 'TNN_PRE_V1_R27_GENERAL_LEARNING'`
- `development_step = 60423`, `newborn_restarts = 0`
- `r26_sha256 = 'df3acde273aa682642d13763a24208ff1dbb42968313cbe2a4256f7ccbc1f839'`

The policy JSON is a promotion/rollback ledger (`format: TNN_PRE_V1_R27_POLICY`):
active promotion `STRONGER_MASTER_GENERAL_SPECIFIC_BRIDGE`; retained
`R26_VIDEO_IDENTITY`, `R25_GENERIC_VAD`, `R23_R25_SEMANTIC_GENERATOR`;
rolled back `CATEGORY_METRIC`, `AFFORDANCE_GENERALIZATION`,
`VISUAL_DEBATE_EXTRA_VIEW`, `PROTECTED_GENERALISTS`… (5 entries);
`shadow_partial` (2); `locked_gates` incl. `TEENAGER_ENGLISH`, `ADULT_ENGLISH`,
`NATURAL_VIDEO_AUDIO`, `HUMAN_SUPER…`.

## 2. The one documented Python exception

**Why Python was used here:** the artifact is a Python pickle; there is no
other way to inspect its contents. This is the single sanctioned exception to
the Zag-first rule. Everything downstream — the schema, the negative tests,
any future reader/loader — must be Zag-native. Nothing in this directory is
load-bearing for future work except this document; the inspection scripts are
kept for audit (`restricted_load.py`, `analyze2.py`, `analyze3.py`).

## 3. How it was mapped (method)

1. `pickletools.genops` disassembly first — opcode census, no execution.
2. Custom `RestrictedUnpickler`: `find_class` maps **every** `(module, name)`
   to a generated stub class that records construction args but executes zero
   domain code. Stubs also implement `__setstate__` (records raw build
   state), plus `append`/`extend`/`__setitem__` shims because the pickle uses
   iterator-form REDUCE (APPEND/APPENDS/SETITEM opcodes, e.g. for
   `collections.deque`).
3. Recursive graph walk: 121,094 nodes, max depth 43.

**Namespace warning:** the pickle's class modules (`r27_experiments`,
`r15_master_training`, `r17_experiments`, …) do **not** exist in the repo's
current layout. Do not try to import them — that is exactly why stubs were
used. (An early naive scan misattributed one class as `1.8.0.RoleBindingLearner`;
the true reference is `r20_experiments.RoleBindingLearner`. There is no module
literally named `1.8.0`.)

## 4. The headline: a lineage chain, not a weight matrix

The brain is **five nested accepted states** — each generation embeds the
previous generation's full accepted state ("continuing brain" made literal):

| Level | Class | Format tag | Dev step | Restarts | Prior SHA key |
|---|---|---|---|---|---|
| L0 | `r27_experiments.R27State` | `TNN_PRE_V1_R27_GENERAL_LEARNING` | 60423 | 0 | `r26_sha256` |
| L1 | `r26_experiments.R26State` | `TNN_PRE_V1_R26_VIDEO_ARCHITECTURE` | 60249 | 0 | `r25_sha256` |
| L2 | `r25_release.R25AcceptedState` | `TNN_PRE_V1_R25_ADAPTIVE_NATURAL_ENGLISH_V1` | 57285 | 0 | `r24_sha256` |
| L3 | `r25_release.R24AcceptedState` | `TNN_PRE_V1_R24_ADAPTIVE_MASTER_CLOSURE_V1` | 41144 | 0 | `r23_sha256` |
| L4 | `r23_experiments.R23State` | `TNN_PRE_V1_R23_SEMANTIC_ENGLISH_V2` | 29344 | 0 | `r22_lineage_sha256` |

Every level carries `architecture`, `evidence`, and `self_revision_history`
dicts. R27 added only 174 steps on top of R26's 60249 — development is
cumulative across the lineage.

**L0 `R27State` top-level keys** (14):
`format`, `r26_sha256`, `base_state` (→L1), `category_system`,
`affordance_model`, `speech_motif_decoder`, `abstraction_policy`,
`semantic_generator`, `visual_debate_policy`, `architecture`, `evidence`,
`self_revision_history` (58 entries), `development_step`, `newborn_restarts`.

Notable per-level subsystems: L1 video (`video_encoder`, `video_entity_policy`,
`speech_segmenter`, `speech_index`); L2 language (`foundational_learner`,
`composition_system`, `relational_language`, `speech_core_pam`,
`speech_noise_pam`, `learning_action_policy`); L4 (`mastery_student`,
`foundational_language`, `speech_pam`, `noncore_pams`, `situation_memory`,
`question_interpreter`, `invented_macros`).

`architecture` is a dict of **named subsystems, not layers**:
`discourse, speech, semantics, siblings, procedures, repository,
self_revision, compute, generative_discourse, speech_semantics`.
`architecture['compute']` is a prose policy: *"capability-first; late-noise
fine-tune promoted because aggregate capability improved without regression;
expensive weak candidates rejected"*.
`evidence` is keyed by capability gate: `category_initial, category_dose,
category_large15, category_large21, category_metric, affordance,
visual_debate, speech, abstraction, semantic_generation`.

## 5. The learning atom: Trace (×435)

`r15_master_training.Trace` — 435 instances. Fields of a representative:
- `cue`: 512-dim float32 vector (numpy buffer)
- `ops`: `(('FILTER_GT', 'PARAM'), ('MAP_MUL', 2))` — **symbolic opcodes** over the cue
- `support`: 1.0 (float), `sources`: `{200054}` (source-id set)
- `verified`: 1, `failures`: 0, `age`: 480
- `provenance`: `'SELF_VERIFIED'`, `anchors`: `(b'than 3, then',)`

A trace is a verified symbolic operation-sequence applied to a cue vector,
with provenance and age. **This is the white-box learning atom: operations,
not gradients.** Related: `r17_experiments.EpisodicConcept` (×10):
`cue, answer, support, sources`.

## 6. The developmental log: self_revision_history (58 entries)

The brain's "training log" — 58 structural revision decisions, e.g.:
```
diagnosis: 'late visual noise reduces cheap central identity stability'
proposal:  'recruit learned recurrent PAM only when noisy/ambiguous'
base_accuracy: 0.6771 → candidate_accuracy: 0.9271
compute_multiplier: 2.95, decision: 'PROMOTE', authorship: <recorded>
```
Schema: `diagnosis, proposal, base_accuracy, candidate_accuracy,
compute_multiplier, decision, authorship` (the final entry uses
`owner, diagnosis, proposal, decision, evidence`). Learning = measured
structural revisions with accuracy deltas and compute costs — **not gradient
steps**.

## 7. The student and the memories

`r15_master_training.MutableStudent` (×1) keys: `seed, rng, lineage_hash,
skills, entities, fibers, provenance, parent_history, teacher_dependence,
self_revision, arch, visual_pam, audio_pam, grounded_concepts, program_motifs,
r18_attention, r18_relational_semantics`. (`teacher_dependence` is the H-09
training-first hook.)

Memory systems — all structural, all inspectable:
| Component | Keys |
|---|---|
| `ProtectedSkillMemory` | `fast, slow, step, history, gram_counts` (two-speed!) |
| `GroundedConceptMemory` | `rows` |
| `MotifProgramMemory` | `programs, motifs, centroids` |
| `HybridRelationalMemory` | `dim=768, reg, W` (numpy), `prototypes` |
| `AnonymousRelationalStore` | `dim=1024, W` (numpy), `targets` |
| `VideoNameMemory` | `nmin, nmax, docs, df` (TF-IDF style) |
| `MultiViewEntityGraph` | `max_views, merge_threshold, nodes` |
| `EntityEventGraph` | `nodes, alias, next_id, merge_history` |

Determinism: `random.Random` + numpy `Generator(PCG64)` with pinned
`SeedSequence(65708578)`.

## 8. The tensor question — precise answer

There **are** torch tensors, confined to perceptual components. The exact
accounting:

- **76 torch Parameters** (`_rebuild_parameter` ×76): 32 `Conv1d`, 32
  `Linear`, 8 `GRU`, 2 `Embedding`, 2 `LayerNorm` — inside `ConvWordNet` (×4),
  `EntityHeadNet`, `RawConvSpeechPAM` (×2), speech/video PAMs.
- All 76 Parameters have `requires_grad=True`; underlying tensor payloads
  rebuild with `requires_grad=False` (standard torch pickle artifact).
- All 76 have **empty** `backward_hooks` (OrderedDicts with zero items).
- **Zero gradient payloads. Zero optimizer state.** A full key sweep of all
  121,094 nodes found no `optimizer/momentum/lr_scheduler/weight_decay/
  grad_fn` keys; the only "grad" string in 15.8 MB is `scale_grad_by_freq`
  (an `nn.Embedding` constructor kwarg, ×4 — not gradient state).
- Tensor storage ≈ **3.26 MB of 15.87 MB (~20%)**. 26 distinct shapes; most
  common `(48,)`, `(128,)`, `(16,1,31)`, `(32,16,15)`.
- The other ~80%: 5,765 numpy arrays via `_frombuffer` (mostly 2048-byte
  float32 = 512-dim vectors: trace cues, relational `W` matrices), 1,054
  OrderedDicts, 7,347 raw byte blobs (13.1 MB total).
- **17 sklearn `LogisticRegression`**: 11 in `RoleBindingLearner`, 5 in
  `QuestionLearner`, 1 in `SurfaceOperationLearner` — linear probes, not
  brain-level training.

Honest caveat for the negative tests: `requires_grad=True` means torch
*autograd could* flow through the perceptual components if someone called
`.backward()`. The architectural claim is narrower and checkable: no
optimizer ever attaches, no gradients are ever stored, and all brain-level
learning is trace/memory/policy operations (Sections 5–6).

## 9. "What TNN is NOT" — negative-test specs

Specs only; implementation is a later workstream. Each MUST hold for the
accepted state and for any future native state artifact:

- **N1 — No optimizer state.** Artifact contains zero keys matching
  `optimizer|momentum|lr_scheduler|weight_decay`; zero `grad_fn` payloads.
- **N2 — No gradient payloads.** Zero stored `.grad` tensors; all
  Parameter `backward_hooks` are empty.
- **N3 — Learning is structural.** Every `self_revision_history` entry
  matches `(diagnosis, proposal, base_accuracy, candidate_accuracy,
  compute_multiplier, decision, authorship)`; no gradient-step records exist.
- **N4 — Trace ops are symbolic.** Every `Trace.ops` is a tuple of symbolic
  opcodes (e.g. `FILTER_GT`, `MAP_MUL`) over cue vectors — never a weight
  delta.
- **N5 — Lineage nesting invariant.** `R27State.base_state` is `R26State` →
  … → `R23State`; each level carries the prior level's sha256;
  `development_step` is monotonic non-decreasing across levels;
  `newborn_restarts == 0` at every level.
- **N6 — Canonical invariants.** `format ==
  'TNN_PRE_V1_R27_GENERAL_LEARNING'`, `development_step == 60423`,
  `newborn_restarts == 0`.
- **N7 — Tensor containment.** torch Parameters exist ONLY inside named
  perceptual components (`Conv1d/Linear/GRU/Embedding/LayerNorm` under
  speech/entity/video PAMs); none at brain level; total tensor storage <
  25% of artifact bytes.
- **N8 — White-box memory.** Memory components expose structural keys
  (`fast/slow/history/gram_counts`, `rows`, `programs/motifs/centroids`,
  `nodes/merge_history`); no opaque blobs except torch storages and
  dtype+shape-recorded numpy buffers.
- **N9 — Determinism.** Seeded RNG present and pinned (`random.Random`,
  numpy `PCG64`/`SeedSequence`); seeds recorded, never `None`.
- **N10 — Ledger consistency.** `parent-r27-accepted-policy.json`
  `active_promotions`/`rolled_back` entries each correspond to a
  `self_revision_history` decision.

## 10. Open questions / blockers for future agents

1. **No Zag-native reader exists yet.** The class modules in the pickle
   (`r27_experiments`, …) are not in the repo; a native loader must be
   written from this schema (Agent B/C territory).
2. **How the 76 perceptual params were learned** is undocumented — no
   optimizer state, no training script. They arrived learned; the process
   didn't.
3. **R27 added only 174 steps** over R26 (60249 → 60423). What those steps
   were is in `self_revision_history` — worth mining for the developmental
   curriculum pattern.
4. `MutableStudent.teacher_dependence` — unexamined; likely the H-09
   teacher-withdrawal measurement point.
5. The final `self_revision_history` entry uses a different schema
   (`owner,…`) — possibly a newer record format; confirm before writing N3
   tests.
6. `sources: {200054}` on traces — source-id registry unresolved; find what
   issues source ids.
