# Memory survey — every memory structure in TNN, and what's missing for conscious agency

Agent G (memory agency), 2026-09-19. Sources: `docs/lab/wave1/brain/STATE_SCHEMA.md`
(R27 accepted state), `RULES_SURVEY.md` (rules lab), `DO_NOT_REPEAT.md`.

Micah's paradigm (law): **conscious memory agency** — the system deliberately
manages its own memory (add, kill, pin, promote/demote, short/long term) at
any time it chooses, consciously, never subconsciously. No LLM context window.
No transformer-style RL reward shaping of memory (that framing is documented
secondary work, not the paradigm). The agency capability itself must be
**trained** so the system doesn't self-destruct its knowledge.

---

## 1. What exists today

### 1a. R27 canonical brain (historical, Python — target semantics, not executable)

| Structure | Keys / shape | Who controls it today | Agency status |
|---|---|---|---|
| `ProtectedSkillMemory` | `fast`, `slow`, `step`, `history`, `gram_counts` — **two-speed** | Written by the training harness during development; read by skills | **Subconscious.** Fast/slow consolidation happens *to* the system; it never decides. No PIN, no KILL API. |
| `GroundedConceptMemory` | `rows` | Harness-populated | Subconscious. No deliberate add/forget. |
| `MotifProgramMemory` | `programs`, `motifs`, `centroids` | Harness-populated | Subconscious. |
| `HybridRelationalMemory` | `dim=768`, `reg`, `W` (numpy), `prototypes` | Harness-populated | Subconscious. |
| `AnonymousRelationalStore` | `dim=1024`, `W`, `targets` | Harness-populated | Subconscious. |
| `VideoNameMemory` | `nmin`, `nmax`, `docs`, `df` (TF-IDF) | Harness-populated | Subconscious. |
| `MultiViewEntityGraph` | `max_views`, `merge_threshold`, `nodes` | Harness-populated; merges by threshold | **Closest to agency:** merge decisions are structural and inspectable, but the threshold is set externally, not by the system. |
| `EntityEventGraph` | `nodes`, `alias`, `next_id`, `merge_history` | Harness-populated | Subconscious. `merge_history` is an audit trail the system didn't choose to keep. |
| `Trace` (×435) | `cue` (512-dim f32), `ops` (symbolic opcodes), `support`, `sources`, `age`, `provenance='SELF_VERIFIED'`, `anchors` | Self-verified during development | **Proto-agency.** `provenance='SELF_VERIFIED'` means the system checked its own traces — the only structure where the system is the author of its own memory metadata. But: no deliberate deletion, no pinning, no tiering. Age accrues passively. |
| `self_revision_history` (58) | `diagnosis → proposal → base/candidate accuracy → compute_multiplier → PROMOTE/rollback` | The developmental process | **Proto-agency at the policy level.** The system (via the harness) *decides* structural changes with measured outcomes. This is the decision-loop shape that memory agency should copy: propose → measure → promote/rollback, with an audit trail. |
| `MutableStudent.teacher_dependence` | scalar | Measured externally | Relevant: H-09 hook. A memory-agency regime needs the same withdrawal-style measurement — can the system manage memory *without* a teacher telling it what's important? |

**Summary of 1a:** the brain has rich, white-box, structural memory — but
every write path is owned by the training harness, not by the brain. The
system is the *subject* of memory management, never the *agent*. The two
exceptions that point forward: `Trace.provenance='SELF_VERIFIED'` (self-
authored metadata) and `self_revision_history` (decide → measure →
promote/rollback with audit).

### 1b. Native substrates (Zag — executable, but never wired into a learner)

| Substrate | Mechanism | Agency status |
|---|---|---|
| `r34_memory_lifecycle_v1.zag` | Bounded-linear future-use estimator `pred=clamp01(0.5+0.25·(bias+w·x))`; delayed delta credit `w += lr·error·g·x`; when full, evict lowest predicted future-use (ties → oldest); incoming must strictly beat worst to displace | **Best raw material.** Already separates *protected substrate* (capacity, integrity, provenance) from *learner-owned value judgment* (the weights). But: eviction is automatic policy, not a deliberate learner action; uses f32/f64 + `@noalloc` — **never compiled with the pinned znc** (playbook-proven subset is integer; compile-test before use). |
| `r34_curiosity_progress_v1.zag` | Two-speed prediction-error EMA; curiosity = `\|slow−fast\| + novelty` | Never wired in. Relevance: a *candidate value signal* the learner could consult before a deliberate MEM_PIN — but the score must advise, not decide. |
| `r34_hypothesis_state_v1.zag` | Pairwise contrastive credit | Never wired in. Not memory agency. |
| `r34_self_model_v1.zag` | Per-strategy delta heads + error EMA | Never wired in. Relevance: self-model of *own memory-operation outcomes* is exactly what a trained agency regime needs (did my last KILL hurt?). |
| R34 v3 checkpoint (`checkpoint.zag`/`storage.zag`) | Byte-exact save/reload, corruption/torn refusal | **Infrastructure agency already exists** at the storage layer: the system refuses to load corrupt inner state (2005) rather than confabulating. Memory agency must inherit this: never silently absorb a damaged memory. |

### 1c. What the native learners do today

R34 v1/v2/v3 and P2/P3: the "memory" is a 2×2 score table (+ contexts).
Updates are additive/delta on scores. There is **no memory object** — nothing
to add, kill, or pin. The learner cannot even *name* a memory, let alone
manage one. This is the gap the operation set closes.

---

## 2. What's missing for conscious agency (the gap list)

1. **Memory as addressable objects.** No native structure today has a slot
   the learner can point at and say "that one." (R27 traces have identity
   via `sources`/anchors but no operation API.)
2. **Deliberate mutation verbs.** No MEM_ADD / MEM_KILL / MEM_PIN /
   PROMOTE / DEMOTE exists anywhere. The closest verb is the lifecycle
   substrate's automatic eviction — policy, not agency.
3. **Explicit value judgment by the learner.** Value today is either
   harness-assigned (R27) or reward-driven (R34 scores). Conscious agency
   needs the learner to *declare* "this memory is worth V" as its own
   judgment, auditable and revisable — not as a reward gradient.
4. **Protection domains.** Nothing distinguishes "my core knowledge —
   never touch" from "working memory — manage freely." Micah's
   self-destruction concern lives exactly here.
5. **Staged autonomy.** H-06 names staged autonomy as PLAN_NOT_EXECUTED.
   Memory ops must unlock in stages, earned by demonstrated safe operation.
6. **Audit + rollback of memory mutations.** R27 has `merge_history` and
   `self_revision_history` as *records*; agency needs them as *mechanisms*:
   every mutation logged with before/after, every mutation reversible.
7. **Core/user separation.** No region concept exists. (Sketch in
   MEMORY_OPS.md §5; serving is explicitly later work.)
8. **Training the agency itself.** No curriculum exists for *learning to
   manage memory*. This is the wave-3 research program: memory-pressure
   curricula where the learner is scored on endpoint retention of what it
   chose to protect — not on reward.

---

## 3. Design constraints inherited from the negative record

- **No reward shaping of memory** (Micah's law; also H-09 training-first:
  diagnose training before architecture). Value signals advise; the
  learner's declared judgment decides. The trial in this workstream assigns
  values explicitly at MEM_ADD — no reward enters the memory path.
- **Aggregate gains never cancel pointwise damage** (E51AJ law): memory
  experiments report **per-slot endpoint retention**, never aggregate
  "memory health."
- **Never silently absorb damage** (R33-B000 defect 3; v3 refusal codes):
  a failed/corrupt memory op is a *refusal with a code*, never a quiet
  no-op. The op set returns result codes for every path.
- **No confidence-threshold anything** (banned practice 4): PIN is a
  deliberate action with an audit entry, not a threshold crossing.
- **Evaluator separation** (H-07): the trial's value assignments are
  fixed by the protocol, not by the learner grading its own homework —
  the learner's *decisions* (which slot to kill, what to pin) are what's
  under test, against pre-registered expectations.
