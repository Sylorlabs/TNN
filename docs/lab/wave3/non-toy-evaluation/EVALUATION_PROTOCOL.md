# Non-Toy Evaluation Protocol (Wave-3)

**Investigator:** Wave-3 investigator, subagent session 2026-09-19
**Slug:** `non-toy-evaluation`
**Status:** METHODOLOGY — protocol specified, not yet executed.
**Branch discipline:** all runs on this Linux VM; no git pushes.

This protocol extends the lab's existing evaluator discipline — it invents
no new foundations. Its job: say what counts as *evidence of general
capability growth* in a TNN whose paradigm is **deliberate memory agency +
verified switching + structural revision + trace composition**, and make that
evidence falsifiable. Benchmark scores are banned as targets; score tables,
RL reward-shaping, and stochastic decision paths are banned as mechanisms.
Honest negatives are first-class: a protocol that cannot fail a system is not
a protocol.

## 0. Program law incorporated (Micah, 2026-09-19 — effective immediately)

1. **Scaling is allowed.** The ban was on scaling *toy mechanisms*
   (N×N score tables, LH-6), never on scaling. "Bigger table" is dead.
   §9 adds an explicit scale dimension: every claim states its scaling
   argument and its next scale test. Scaling a claim beyond tested scale
   without evidence is banned.
2. **No RNG in the AI, period.** No random exploration, no random
   tie-breaks, no stochastic policies, no seeded RNG inside the learner.
   Real AI = educated guesses, logic, hypotheses, verification —
   deterministic given state. Entry gate G0 (§3) rejects any system with
   RNG in its decision paths before any capability claim is heard.
   The toy-era LCG (`rng % 5` exploration, `rng % 2` tie-breaks) is
   retired, not grandfathered: tie-breaking must be deliberate
   (arbitration by hypothesis strength, provenance priority, or
   verification outcome) and recorded in the revision ledger.
3. **The world may be unpredictable — that is the test.** Test adversity
   is expressed as **designed curricula**: explicitly authored sequences
   (regime switches, corruptions, novel families at named points), sealed
   before the run. Seeded RNG in the harness is tolerated only as
   legacy scaffolding, documented with its seed, never part of the system.
   Every verdict must distinguish *"the system is deterministic"*
   (byte-identical trajectory on re-run of the same curriculum) from
   *"the test was adversarial"* (curriculum authored independently,
   difficulty preregistered).

## 1. What the lab already settled (inherited, not re-argued)

| Law | Source | What it binds here |
|---|---|---|
| Evaluator leakage is the default suspect behind any good number | DO_NOT_REPEAT §4 (H-07) | truth-by-time trajectories; frozen, hashed evaluation harness; nonzero oracle-positive prevalence gates; evaluator-blind helpers (no mode/truth/seed/target args); sealed partitions; matched controls; **consumed probes are never reused as fresh validation** |
| E51 law: cumulative disruption ≠ endpoint recovery | DO_NOT_REPEAT §2 (H-08) | retention reported **pointwise per capability and per development step, never aggregate-only**; a new capability never cancels a pointwise loss |
| Learning vs noise (toy-era operationalization) | wave2/longhorizon/PREREG.md | learning = new capability + deterministic reproduction + matched-control separation; noise = within control band, non-reproducible, collapses on return — generalized in §5–§7 |
| Native design language | wave2/ruleslab/RULES_SURVEY.md | additive/delta integer updates, delayed credit via explicit pending slots, determinism by construction; the R27 semantics (structural PROMOTE/rollback over symbolic traces) is the *target*, implemented natively as it matures |
| Target semantics | brain/STATE_SCHEMA.md | learning atom = Trace (verified symbolic op-sequence, provenance-bearing); developmental log = self_revision_history schema (diagnosis → proposal → base/candidate measured delta → decision → authorship); negative-test specs N1–N10 |
| Reference-only law | DO_NOT_REPEAT §6 | shadow-runtime numbers never promote; only native, on-this-VM evidence counts |
| Banned practices | DO_NOT_REPEAT §8 | no newborn restarts; no hardcoded answers; no crediting teacher/evaluator knowledge to the learner; no confidence-threshold abstention; training-first diagnosis before architecture churn; no aggregate-only reporting |

## 2. What counts as evidence of general capability growth

A **capability claim** is a named, dated bundle with four inseparable parts.
If any part is missing, there is no claim — only an anecdote:

1. **Behavioral trajectory.** The system's behavior on a sealed task
   family (never directly trained on), recorded as a truth-by-time
   trajectory: observations, deliberate memory ops, switches, compositions,
   and actions, timestamped against an independent ground-truth timeline
   the system never sees (H-07 discipline at scale).
2. **Mechanism attribution.** Which deliberate structures produced the
   behavior: which traces composed (op-sequences + provenance), which
   memory ops fired (kill/pin/promote), which verified switches occurred,
   which revision-ledger entries cover it. White-box or it didn't happen.
3. **Control deltas.** The same task family run under the control battery
   (§6). The claim is *the delta between the full system and the
   mechanism-disabled controls* — not a raw score.
4. **Retention row.** The capability's entry in the per-capability
   retention matrix (§7): every previously accepted capability re-probed
   at this development step, reported individually.

**Evidence of growth = an increase in the set of accepted capabilities
where each new capability** (a) solves a task family the system was never
directly trained on (§5, novelty L2 or L3), (b) is attributed to deliberate
mechanisms with inspectable provenance, (c) survives the full control
battery (degrades or disappears when the attributed mechanism is disabled),
and (d) coincides with zero pointwise retention losses on previously
accepted capabilities.

**Not evidence:** benchmark score improvements on trained families;
single-number aggregates; shadow-runtime numbers; anything the
disabled-agency control also does; anything reproducible by content
memorization (survives scrambled-provenance); anything the harness
produces with a null system (evaluator artifact).

Scores may appear as *measured observations inside a preregistered
protocol*. Optimizing against a benchmark, or promoting on a score table,
is banned — promotions happen on mechanism-attributed capability claims
plus clean retention, decided by a recorded agent of record following the
self_revision_history schema (diagnosis, proposal, base-vs-candidate
measured delta, decision, authorship).

## 3. Entry gates (run before any capability claim is heard)

| Gate | Test | Fail verdict |
|---|---|---|
| **G0 — No RNG in the system** | Inspect the system artifact and decision code: zero RNG/PRNG state, zero `rand`/`random`/`LCG` calls in any decision path (extends STATE_SCHEMA N1/N2 to stochasticity). All tie-breaking is deliberate logic, recorded. | NEGATIVE (entry-gate failure); amend design, do not rerun silently |
| **G1 — Lineage continuity** | One developmental lineage; `newborn_restarts == 0`; accepted floors are regression constraints (DO_NOT_REPEAT §8.1) | NEGATIVE |
| **G2 — Determinism by construction** | Identical state + identical designed curriculum → byte-identical trajectory (exact-equality check, no seeds involved — the system has none) | NEGATIVE |
| **G3 — Sealed harness** | Evaluation task-family logic frozen and hashed *before* the system runs against it; helper code takes no truth/target/seed arguments (H-07); ground-truth timeline generated and sealed independently of the system | BLOCKED (protocol cannot run) |
| **G4 — Trace machinery sound** | B001 gate on the trace helper (DO_NOT_REPEAT §5: the prototype silently dropped an event at saturation) — no claim may rest on unfixed trace machinery | BLOCKED |
| **G5 — Novelty floor** | The task family is classified on the novelty ladder (§5) and is at least L2 | claim inadmissible as growth evidence (may still be reported as L0/L1 sanity) |

## 4. The protocol phases

1. **Preregister.** Capability name, novelty-ladder classification, the
   task family (sealed, hashed), the designed adversarial curriculum,
   the attributed mechanism, the control battery to be run, and — most
   importantly — the **kill criteria** (§8): exact conditions under which
   the claim dies. Recorded by an agent of record.
2. **Seal.** Freeze the harness, generate the ground-truth timelines,
   author the adversarial curriculum (explicit sequences, §9), hash
   everything. The system author does not author the probe families;
   probe authors are recorded (independence requirement).
3. **Run.** Full system on the curriculum; record the behavioral
   trajectory with full mechanism attribution (trace compositions,
   memory ops, switches, ledger entries).
4. **Control.** Run the identical curriculum under each control in the
   battery (§6) — same episodes, same order, same harness.
5. **Retention audit.** Re-probe every previously accepted capability
   at endpoint; fill the retention matrix pointwise (§7).
6. **Verdict.** Apply the kill criteria. Record POSITIVE / NEGATIVE /
   MIXED / BLOCKED with the evidence bundle (commands, stdouts, exits,
   SHA256SUMS, RECEIPT.txt — mirroring the R34 evidence pattern).
   Negative verdicts name the cause; the system is amended, not rerun
   silently.

## 5. Novelty requirements (what "never directly trained on" means)

The **novelty ladder**:

- **L0 — Trained family, held-out episodes.** Memorization is possible.
  Not evidence of growth. Used only as a sanity gate (the system should
  not fail what it was taught).
- **L1 — Interpolation.** Same family, parameter variations within the
  training distribution. Weak evidence at best; never sufficient alone.
- **L2 — Recombination.** Novel arrangement of known primitives: the
  task family requires composing previously learned traces/primitives in
  a configuration never seen in training. **Counts as growth** when
  mechanism-attributed and control-separated.
- **L3 — True zero-shot.** The family requires a genuinely new primitive
  or a novel composition *pattern* the system invents deliberately
  (hypothesis → verification → PROMOTE). Strongest evidence.

Requirements for L2/L3 families:

- **Sealed partitions at family level**, not just episode level: no
  episode, cue pattern, or ground-truth trajectory from the probe family
  may appear in training, in any transform (cue vectors included —
  the worked example in §10 shows why).
- **Independent authorship:** probe families are authored by an agent
  other than the system/training author; authorship is recorded.
- **Nonzero oracle-positive prevalence:** every probe family contains
  cases where the ground truth is non-trivial (H-07 gate at scale) —
  a family where "do nothing" or "repeat the cue" is always right is
  rejected as a probe.
- **Designed adversarial content** (§9): the curriculum places
  regime switches, corruptions, and novel-family insertions at authored
  points, recorded in advance.
- **Consumed probes are never reused as fresh validation.** A family
  that has served as a probe is burned; future claims need fresh families
  (R33 N13A/N14/N16 gates are consumed — do not rerun).

## 6. Control conditions (the real-scale battery)

Each control runs the *identical* curriculum as the full system — same
episodes, same order, same sealed harness (the toy era's matched-controls
discipline). The claim is the delta between the full system and the
mechanism-disabled controls.

| Control | Toy-era ancestor | What it disables / scrambles | What survival of the capability under this control means |
|---|---|---|---|
| **C1 — Disabled-agency** | disabled-update control | All deliberate memory ops (kill/pin/promote) and deliberate switching frozen; memory becomes passive storage, switching locked to the pre-run policy | Capability is **not** caused by memory agency → kill the agency attribution (memorization or fixed-policy artifact) |
| **C2 — Disabled-composition** | (new — paradigm-specific) | Trace composition op blocked; base traces and memory intact | Capability persists → it was latent in base memory, not composed → kill the composition claim |
| **C3 — Scrambled-provenance** | scrambled-reward control | Provenance metadata permuted (source IDs, verification flags shuffled); content untouched | Capability persists → the system memorizes *content*, not verified *attributions* → memorization verdict |
| **C4 — Scrambled-structure** | (new — paradigm-specific) | Composition order / op-sequence order permuted | Order-invariance → composition is an illusion; the ops don't do the work |
| **C5 — Memory-lesion** | (new) | Accepted-partition only (candidate memory disabled); then the reverse: candidate-only, killed-traces-only | Attributes the capability to a specific memory structure; killed-traces-only succeeding is a leakage alarm |
| **C6 — Null-system harness check** | E45's broken evaluator (the default suspect) | A trivial system (replay-last, do-nothing) runs the harness | Nonzero "capability" from the null system → the evaluator leaks; fix the harness, void all claims on this battery |
| **C7 — Teacher-withdrawal** | H-06/H-09 (specified, not run) | For systems trained with teachers: teacher removed, dependence measured | Capability collapses → teacher dependence, not learner capability; crediting teacher knowledge to the learner is banned (DO_NOT_REPEAT §8.3) |

Kill-criterion template (preregistered per claim): *"If capability under
C1 or C2 is within ±1 probe of the full system, the attributed mechanism
is not the cause — claim killed. If C3 preserves the capability, verdict
is MEMORIZATION, not composition. If C6 is nonzero, the battery is void."*

## 7. Retention requirements (the E51 law, generalized)

- **Per-capability retention matrix.** Rows: every accepted capability
  (named, with its sealed probe family and its original acceptance
  evidence). Columns: development steps / revisions. Cells: endpoint
  probe outcome at that step. Reported **pointwise — never aggregate-only**.
- **Endpoint, not cumulative.** After each structural revision
  (PROMOTE candidate), every accepted capability is re-probed at
  endpoint. A new capability gained does not cancel any pointwise loss:
  **any single lost capability is a retention failure** — the revision
  is rejected (rollback) and recorded as a negative, not averaged away.
- **No newborn restarts.** The lineage continues; accepted floors are
  regression constraints (DO_NOT_REPEAT §8.1).
- **Revision ledger.** Every promotion decision follows the
  self_revision_history schema: diagnosis, proposal, base-vs-candidate
  measured delta, compute cost, decision, authorship. The ledger is the
  audit trail of the retention matrix.

## 8. Falsifiability — what a NEGATIVE looks like

The protocol fails a system in any of these ways (each preregistered as a
kill criterion before the run):

1. **Mechanism kill:** capability survives the mechanism-disabled
   control (C1/C2) within the preregistered band → the attributed
   mechanism is not the cause. Named cause: memorization, fixed-policy
   artifact, or latent base memory.
2. **Memorization verdict:** capability survives scrambled-provenance
   (C3) → the system memorized content, not verified attributions.
3. **Leakage void:** null-system harness check (C6) is nonzero, or
   post-hoc analysis finds probe content in training (cue vectors,
   trajectories, transforms) → the battery is void; the evaluator is the
   suspect (DO_NOT_REPEAT §4 — the default).
4. **Retention rejection:** any pointwise loss in the retention matrix
   → the revision is rolled back; the loss is recorded as a negative
   against the revision, never averaged away.
5. **Novelty failure:** the probe family is found to overlap training
   (L2/L3 claim collapses to L0/L1) → claim inadmissible as growth.
6. **Determinism failure:** G2 exact-equality fails, or G0 finds RNG in
   a decision path → entry-gate NEGATIVE; the system is amended, not
   silently rerun.
7. **Teacher dependence:** capability collapses under teacher withdrawal
   (C7) → not learner capability.

Verdict vocabulary:

- **POSITIVE** — all entry gates pass; novelty L2+; claim survives every
  control (degrades/disappears exactly where the attribution predicts);
  zero pointwise retention losses; verdict recorded in the revision ledger.
- **NEGATIVE** — any kill criterion fires. The verdict names the cause
  and the preregistered next step. This is a first-class result.
- **MIXED** — passes controls but with recorded anomalies (e.g. partial
  attribution: degrades under C2 but not to the control floor; or passes
  on the designed curriculum but fails on the independently authored
  family). MIXED never promotes; it preregisters the follow-up.
- **BLOCKED** — the protocol cannot run (G3/G4: harness unsealed, trace
  machinery unfixed, no native implementation of the claimed mechanism).

## 9. Designed adversarial curricula (program law §0.3)

Test adversity is authored, not sampled. A curriculum is an explicit
sequence document: named phases, regime switches at named points, novel
family insertions, corruption episodes — written and sealed *before* the
run, with its difficulty rationale recorded. Examples of authored
adversity: a switch-storm phase followed by silence (the HT1 shape);
a corruption burst at a named step (the LH-5 shape, authored not ramped
by RNG); a probe family inserted at the moment of maximum memory load.

Seeded RNG in the harness is tolerated only as scaffolding (documented,
seed recorded) and must be replaced by designed sequences wherever the
adversity is load-bearing. The verdict text must always separate:

- *"The system is deterministic"*: byte-identical trajectory on re-run
  of the same curriculum (G2) — a property of the system.
- *"The test was adversarial"*: the curriculum was authored
  independently, sealed before the run, difficulty preregistered — a
  property of the test. A system that is deterministic but unchallenged
  has passed nothing.

## 10. Scale dimension (program law §0.1)

Every claim states: (a) the scale it was tested at (trace count,
partition count, memory size, horizon steps, curriculum breadth,
lineage depth); (b) the **scaling argument** — why the mechanism should
survive 10×/100× on each axis; (c) the **next scale test**, named and
preregistered.

The protocol is scale-invariant by construction: every gate is a
*comparison* (full system vs control, before vs after, L2/L3 vs L0) —
none depends on absolute scale. Cost grows linearly in
(capabilities × controls × curricula); the retention matrix is
O(capabilities × steps) and stays pointwise at any scale — tooling
(the ledger + matrix) carries it, aggregation never replaces it.

Scaling a claim beyond tested scale without evidence is banned. "Bigger
table" is dead; bigger *memory with the same deliberate mechanisms* is
exactly what §9's next-scale tests are for.

## 11. Worked example — hypothetical HT2 trace-composition claim (NEGATIVE)

*Hypothetical. No code was run; this exercises the protocol end to end so
a real result can be dropped into the same shape. Names are illustrative.*

**The claim.** The HT2 trace-composition engine, trained on family A
(temporal-ordering tasks, 400 episodes) and family B (causal-attribution
tasks, 400 episodes), exhibits **L2 novelty**: on sealed probe family C
(diagnostic tasks requiring a *temporal trace* `t_A` composed with a
*causal trace* `t_B` via the composition op `COMPOSE(t_A, t_B)`), it
solves 15/16 probe episodes. Attributed mechanism: deliberate composition
— the ledger shows `COMPOSE` firing with provenance `SELF_VERIFIED` on
14 of 15 solved episodes. Scale tested: 2 families, ~40 traces, horizon
~800 episodes. Scaling argument (preregistered): composition is
structural (op-sequences over traces, not table size), so 10× traces
should not change the mechanism; next scale test: 10× trace memory with
the same families.

**Preregistered kill criteria.**
- K1: if disabled-composition (C2) solves within ±1 probe of the full
  system, composition is not the cause — claim killed.
- K2: if scrambled-provenance (C3) preserves the capability,
  verdict is MEMORIZATION.
- K3: null-system harness check (C6) must be 0/16, else the battery is void.
- K4: zero pointwise retention losses on the 6 previously accepted
  capabilities (retention matrix, §7).

**Designed adversarial curriculum (sealed before the run, hashed).**
Authored — not seeded: phase 1, family A with a switch-storm of 5
adversarial regime flips at episodes 60/61/63/68/75 (the HT1 shape);
phase 2, silence (no flips, 100 episodes); phase 3, family B with a
corruption burst at episodes 210–215 (authored, LH-5 shape); phase 4,
probe family C inserted at maximum memory load (episode 400), 16 probes.
Difficulty rationale recorded: the storm tests whether composition
survives unpredictability without a switch-storm collapse; the burst
tests provenance verification under corruption.

**Entry gates.** G0: inspection finds no RNG in decision paths —
tie-breaking is deliberate arbitration by provenance priority, recorded
in the ledger (toy-era LCG tie-break retired per program law §0.2).
G2: two runs of the identical curriculum produce byte-identical
trajectories — *"the system is deterministic."* G3: harness frozen and
hashed before the run; helpers take no truth/target arguments. G4:
trace helper carries the B001 fix. G5: family C classified L2
(recombination of A-primitives and B-primitives in a novel diagnostic
configuration), authored independently by Agent X (not the system author).

**Results.**

| Condition | Solved / 16 | Notes |
|---|---|---|
| Full system | 15/16 | `COMPOSE` fired, provenance `SELF_VERIFIED`, 14/15 solved |
| C1 disabled-agency | 13/16 | agency contributes little — first anomaly, recorded |
| **C2 disabled-composition** | **14/16** | **within ±1 of full system — K1 FIRES** |
| C3 scrambled-provenance | 9/16 | degrades; provenance matters somewhat |
| C6 null-system | 0/16 | harness clean |
| Retention matrix | 6/6 held | no pointwise losses |

**Diagnosis (the protocol doing its job).** K1 fires: blocking the
composition op barely moves the outcome (15→14). The capability was
latent in base memory — it was not composed. Post-hoc provenance audit
finds the cause: family C's author unknowingly reused cue-vector
patterns from family A's training episodes (a cosine-similarity audit
shows 11/16 probe cues within the training cue neighborhood). The
"recombination" was L0 memorization wearing an L2 label — evaluator
leakage, the default suspect (DO_NOT_REPEAT §4). The `COMPOSE` ledger
entries were real operations on already-sufficient traces: the
attribution was honest, the *novelty* was not.

**Verdict: NEGATIVE.** Claim killed by K1 with named cause:
provenance leakage in probe-family authorship (novelty failure, §8.5;
mechanism kill, §8.1). First-class result — recorded, not rerun.
**Preregistered next step:** re-seal family C with disjoint cue
generation (generation procedure audited for cue-neighborhood overlap
before sealing), then rerun the identical protocol. The retention
matrix stays clean and the system stays deterministic — the failure is
precise: attribution held, novelty didn't. A protocol that couldn't
produce exactly this verdict would be decoration.

## 12. Evidence bundle (per run)

Mirror the R34 evidence pattern: commands, stdouts, exit codes,
SHA256SUMS, RECEIPT.txt, the sealed curriculum hash, the revision-ledger
entry, the retention matrix (pointwise), and the verdict with its kill
criterion citations. Nothing pushes to git. Consumed probe families are
marked burned and never reused.

## 13. Open questions

1. The C7 teacher-withdrawal measurement is still specified-not-run
   (H-06/H-09) — the protocol needs it the moment a teacher-trained
   system makes a claim.
2. The nonzero-UNKNOWN abstention geometry (DO_NOT_REPEAT §1, §3) needs
   world/harness support before "deliberate abstention on probe family
   D" can become a claim — currently deferred.
3. Authoring genuinely disjoint L2/L3 families at scale is the hardest
   human part of this protocol; the cue-neighborhood audit in §11
   should become a standard pre-sealing check.
4. The 10× trace-memory scale test (§10) is preregistered but unrun —
   it is the first thing that would graduate an §11-style claim from
   small-scale to a scaling argument with evidence.
