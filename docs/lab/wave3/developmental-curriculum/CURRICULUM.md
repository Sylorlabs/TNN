# Developmental Curriculum — design document

**Investigator:** Wave-3, slug `developmental-curriculum` · **Date:** 2026-09-19
**Branch:** `tnn-native-lab` (no push) · **Apparatus:** this Linux VM, Zag-native (`znc`)
**Mission direction (Micah):** intelligence should NATURALLY EMERGE like humans do —
long developmental horizons, not short training runs. The toy era is over.

## 0. What this document is

A staged capability-growth curriculum in which intelligence emerges
developmentally: each stage adds one capability that builds on prior
mechanisms, inside ONE continuing lineage (no newborn restarts — R27's
60,423 steps, zero restarts, is the shape). Stages are not A/B episode
blocks; they are developmental phases with entry conditions, environment
requirements, and falsifiable exit gates. A rigorous, falsifiable design
is the deliverable; only Stage 1 gets a native pilot here.

### Global laws (bind every stage)

1. **One lineage.** No newborn restarts to hide interference
   (DO_NOT_REPEAT §8.1). A stage's accepted floor becomes the next
   stage's regression constraint.
2. **Evaluator discipline (H-07).** Fresh seeds per stage; determinism
   check (two same-config runs byte-identical); matched controls;
   consumed probes never reused as fresh validation; measurement is
   read-only and never feeds the learner's records.
3. **Endpoint retention, never aggregate-only (E51 law).** Every stage
   reports per-regime / per-cohort / per-replica endpoint retention.
   Aggregate gains never cancel pointwise damage.
4. **Determinism (program law, 2026-09-19).** No RNG anywhere in the
   SYSTEM's decision paths: no random exploration, no random tie-breaks,
   no stochastic policies. Educated guesses, logic, hypotheses,
   verification. Deterministic given state. The WORLD may be
   unpredictable — that is the test — but adversity is expressed as
   DESIGNED curricula, not RNG. Seeded harness RNG is tolerated only as
   scaffolding; this curriculum prefers explicit adversarial sequences.
   Every verdict must distinguish "the system is deterministic" from
   "the test was adversarial."
5. **No table-learning, by construction.** Score tables, N×N table
   scale-ups, RL reward-shaping as the learning paradigm, and random
   exploration as the mechanism are banned as progress (DO_NOT_REPEAT
   §8, HT1). Every gate contains a **table-killer clause**: a property a
   score table structurally cannot exhibit (creation of new rows,
   audited refusals, ledger replay, compositional verification records,
   diagnosis–proposal–measurement records). Outcomes alone never pass a
   gate; the mechanism's artifacts must be present in the ledger.
6. **Scaling is allowed — of real mechanisms.** "Bigger table" is dead;
   every stage carries an explicit **scale dimension** (10×/100× in
   traces, partitions, memory, horizon) with a scaling argument and a
   named next scale test. Small-scale pilots must state the argument,
   not just the hope.

### Memorization vs. development (how gates tell them apart)

Memorizing is producing the right outputs on seen inputs. Development is
acquiring mechanisms that handle the unseen. Each gate therefore pairs
an outcome measure with a **memorization-signature check**: the specific
pattern that would appear if the system were memorizing (switch-storm on
noise, collapse on novel regime, perfect training / failed novel
composite, decision records missing). A stage passes only if outcomes
hold AND the memorization signature is absent AND the mechanism
artifacts (ledger entries, refusals, verifications) are present.

---

## Stage DC-0 — Deliberate Memory (foundation)

**Status:** PROVEN — MA1, 58/58 checks, native Zag, 2026-09-19
(`wave2/memoryagency/TRIAL_RESULTS_MA1.md`).

**Emerging capability.** The system performs memory operations (ADD,
RECORD, KILL, PIN/UNPIN, DEMOTE, ROLLBACK) only as deliberate, audited
operations gated by staged autonomy: at stage NONE, ADD is refused; at
ADD, KILL/PIN are refused (`REFUSED_STAGE`). CORE is structurally
unkillable (`REFUSED_CORE`). Refusals never mutate state
(`audit_clean_refusals`). The ledger is the state: replay from genesis
reconstructs exact live state (`ledger_replay`). Rollback restores
pre-op state from the audit entry's before-snapshot, and the rollback
itself is audited.

**Builds on:** nothing — this is the substrate. (MA1 values were
protocol-fixed; judgment quality is MA3/Phase-4, not re-proven here.)

**Environment must provide:** a bounded slot store; a stage-advancement
protocol the learner does not control unilaterally (stages advance via
audited `SETSTAGE`); capacity pressure (full store → `REFUSED_FULL`);
an audit-capacity limit with fail-closed refusal (`REFUSED_AUDITFULL`).

**Exit gate (passed):** full op-semantics battery 58/58; every refusal
leaves state byte-identical; ledger replay == live state exactly;
staged-autonomy refusals at the right stages.

**Table-killer.** A score table has no operations, no refusal paths, no
ledger. It cannot produce a before==after refusal record or a
replay-equals-live invariant, because there is nothing to replay.

**Scale dimension.** Slots 8 → 80 → 800; ledger 64 → 640 → 6400
entries. Every op is O(1); replay is O(ledger). Next scale test:
DC-0-S10 (80 slots, 640-entry ledger, 10× op volume) — assert op
semantics and replay invariant hold, audit-full refusal still
fail-closed.

---

## Stage DC-1 — Situated Belief (contexts as deliberately-managed partitions)

**Status:** PILOT in this investigation (see `PREREG.md`, `PILOT_RESULTS.md`).

**Emerging capability.** The system maintains *declared* beliefs about
which regime it is in (partitions: label + recorded probe evidence),
and changes belief only through the deliberate, verified, refusable
`SWITCH` operation: commit iff the target partition shows recorded
majority-positive evidence AND the active partition shows recorded
majority-negative evidence (HT1's corroboration rule — structural, in
the op implementation, like `REFUSED_CORE`). New capability beyond
HT1: **novelty → creation**. When the world stops matching everything
known (active measured failing, no live partition verifies, sustained
over a patience window), the system PROPOSEs a new partition declaring
the smallest unused label — it creates knowledge rather than
best-matching old knowledge. Single misleading samples can corrupt
neither corroboration condition (majorities over probe batches, not
samples). Doubt has a mechanism: `REFUSED_UNVERIFIED`, audited, state
untouched.

**Builds on:** DC-0 (deliberate audited ops; ledger replay; refusals
never mutate) + HT1 (corroboration rule; partitions as memory slots).

**Environment must provide:**
- A multi-regime world with a DESIGNED regime sequence: long stable
  stretches, single flips, a rapid-alternation burst (LH-7 pattern),
  and at least one NEVER-BEFORE-SEEN regime injected late.
- Designed adversarial probe batches: isolated misleading batches on
  the active partition during stable stretches, and one misleading
  batch inside a verify round — explicit episode lists, no RNG.
- Read-only measurement blocks (uncorrupted, never fed to RECORD).
- Per-regime endpoint settle phases (return-retention probes).

**Exit gate (preregistered in `PREREG.md`):**
- P1 mechanism unit battery on a scratch store (refusals, clean
  refusals, replay, verified-scan) — all pass.
- P2 novelty→creation: ledger shows PROPOSE of the novel label after
  novelty onset and before any switch to it; no committed switch to a
  wrong-label partition during the novel phase; first post-novelty
  switch targets the novel partition.
- P3 corroboration: every committed SWITCH in the live ledger passes
  the verified-scan (target majority-positive AND old-active
  majority-negative from recorded evidence); committed switches ≤
  true flips + 2 (no switch-storm — the LH-5/HT1 toy signature).
- P4 no collapse: zero measurement blocks ≤ 4/16; per-regime endpoint
  settle ≥ 14/16 for every regime seen.
- P5 determinism: two full runs byte-identical.
- P6 conscious accounting on the live ledger: refusals clean, replay
  exact, audit entries < audit capacity (no silent ledger drop).
- P7 scale leg: same gates at 4× partitions / 4× horizon.

**Memorization signature ruled out:** switch-storm under the burst
(table: 357 switches for 10 flips in HT1); failure to create a novel
partition (a table cannot add a row); collapsed blocks.

**Table-killer.** Three clauses, any one of which a table fails
structurally: (a) P2 — `argmax` over existing cells cannot PROPOSE a
new row; (b) P3's verified-scan — a table's decision step is a single
reflexive function evaluation with no corroboration requirement and no
refusal path (HT1 §1a); (c) P6 — a table has no ledger to replay.

**Scale dimension.** Partitions 4 → 16 → 64; regimes 3 → 8 → 32;
episodes 64 → 256 → 1024. Per-episode cost: O(1) normal, O(cap) in
verify mode (slot-order scan, deterministic tie-break by lowest slot —
no random tie-breaks); PROPOSE label scan O(cap); ledger append O(1).
Next scale test: DC-1-S16 (cap 64, 32 regimes incl. 4 novel, 1024
episodes) — assert P2–P6 hold and wall-time scales ~linearly in
episodes × cap.

---

## Stage DC-2 — Trace Composition

**Status:** DESIGNED (not yet piloted).

**Emerging capability.** R27's learning atom — the Trace (verified
symbolic op-sequence over a cue, with provenance) — becomes
*composable* by deliberate operation. Given verified traces T1, T2
that solve sub-tasks, the system can COMPOSE them (T1∘T2), VERIFY the
composite deliberately on held-out probes (measure, not reflex), and
COMMIT it only if verified — otherwise audited ROLLBACK. Components
stay intact: endpoint retention of component traces is measured
separately (E51 law), so composition can never silently destroy what
it builds on. Composition depth grows developmentally (2, then 3,
then n).

**Builds on:** DC-0 (deliberate ops, rollback) + DC-1 (verify-before-
commit discipline) + R27 trace schema (symbolic opcodes, provenance,
`verified` flag).

**Environment must provide:**
- Sub-task curricula that train component traces to the DC-1 gate
  level, then COMPOSITE tasks built from those components that are
  NEVER shown during component training (novelty by construction).
- A frozen verifier (H-07: evaluator-blind, no truth/seed/target
  arguments to helpers) and held-out probe sets per composite.
- Anchor probes for every component trace (retention suite).

**Exit gate (falsifiable):**
- On a preregistered set of novel composites (≥ 12, documented
  before the run): ≥ 75% solved, where "solved" means the composite
  trace was composed, verified on held-out probes, and committed.
- Every committed composite has a verification record in the ledger
  (compose → verify → commit entries, with probe evidence).
- Component endpoint retention: every component trace scores ≥ its
  pre-composition baseline on anchor probes (any regression is a
  failure per the E51 law, not averaged away).
- Negative control: at least 2 composites designed to be
  UNverifiable must be rolled back, with audited rollback entries
  (the rollback path must fire, not just the happy path).
- Determinism: two runs byte-identical.

**Memorization signature ruled out:** high training scores on
components + chance-level novel composites = memorizing, not
composing. The gate measures ONLY novel composites.

**Table-killer.** A composite never observed in training has no cell
in any (context, object) table; `argmax` cannot combine two cells
into a new behavior. Composition is a structural operation the table
lacks — and the gate additionally requires the verification RECORD,
which a table cannot produce.

**Scale dimension.** Traces 4 → 40 → 400 (R27 carried 435 — the
mechanism is designed for that order); composition depth 2 → 3 → 4;
cue dimensionality fixed by the perceptual substrate. Compose is
O(depth); verify is O(probes). Next scale test: DC-2-S10 (40 traces,
depth-3 composites) after the small pilot passes.

---

## Stage DC-3 — Structural Revision (the R27 miniature)

**Status:** DESIGNED (not yet piloted).

**Emerging capability.** The system's own 58-revision decision
procedure, miniaturized: DIAGNOSE (from ledger evidence — cite the
entries) → PROPOSE a structural change (new partition, revised trace,
recruited mechanism) → MEASURE candidate vs. base on held-out probes
with a frozen evaluator → PROMOTE only on measured improvement with
ZERO anchor regression, else audited ROLLBACK. This is R27's
`self_revision_history` schema
(diagnosis, proposal, base→candidate accuracy, compute cost, decision,
authorship) made into a native, running loop rather than a historical
record.

**Builds on:** DC-2 (compose/verify/commit/rollback) + DC-1
(corroboration discipline) + R27 revision schema.

**Environment must provide:**
- A designed capability-breaking shift (a regime change that defeats
  the current best trace/partition — the world must be able to make
  the system wrong, adversarially by design).
- A frozen evaluator and held-out probe suite the learner cannot
  influence; an anchor suite covering all prior stages' floors.
- A candidate sandbox: proposed structures are measured BEFORE they
  can affect live behavior.

**Exit gate (falsifiable):**
- After the breaking shift, the system produces a diagnosis citing
  ≥ 2 ledger entries, proposes a structural change, and measures it.
- PROMOTE happens only if candidate ≥ base on the new task AND no
  anchor regresses (E51 no-tradeoff rule); the promotion record
  matches the R27 schema fields.
- Harmful-proposal control: a preregistered-bad proposal (designed to
  regress an anchor) must be ROLLED BACK, with the rollback audited —
  the gate tests the refusal path, not just promotion.
- Prior stages' floors (DC-0–DC-2 gates) re-run as regression
  constraints on the same lineage — all hold.
- Determinism: two runs byte-identical.

**Memorization signature ruled out:** "revision" that only re-tunes to
the breaking shift while silently dropping an old capability
(caught by the anchor suite); diagnosis that cites nothing (caught by
the citation requirement).

**Table-killer.** The gate is on the DECISION RECORD — diagnosis,
proposal, measurement, promotion/rollback entries — not on final
performance. A table has no diagnosis or proposal machinery; there is
no record it could forge without implementing the mechanism, at which
point it is no longer a table.

**Scale dimension.** Revisions per developmental run 1 → 10 → 100;
anchor suite 10 → 100 → 1000 probes; ledger-indexed diagnosis
O(ledger). Next scale test: DC-3-S10 (10 sequential revisions on one
lineage, full anchor suite each time).

---

## Stage DC-4 — Learner-Driven Inquiry

**Status:** DESIGNED (HT2 territory — the honest boundary of HT1/DC-1).

**Emerging capability.** The policy stops being protocol-fixed in the
harness. The system decides WHEN to probe and WHAT to hypothesize:
educated guesses (smallest-unused-label was the deterministic seed of
this), hypotheses recorded BEFORE measurement (no post-hoc
storytelling), deliberate inquiry under a probe budget. Verification
discipline (DC-1) still binds every commitment.

**Builds on:** DC-1 (policy was harness-fixed there) + DC-3
(hypothesis as a first-class record).

**Environment must provide:**
- A sparse measurement budget per phase (probes cost; the system must
  allocate).
- Novel situations where the right question matters more than the
  right answer (e.g., two candidate labels, budget for one probe
  batch — the hypothesis must pick).
- A hypothesis log the evaluator can check for pre-registration
  (hypothesis timestamped before its measurement).

**Exit gate (falsifiable):**
- Every measurement the system requests is preceded by a recorded
  hypothesis (ledger order: hypothesis entry clock < measurement
  entry clock); post-hoc hypotheses (measurement before hypothesis)
  count as failures.
- Probe budget respected in every phase (hard cap, audited).
- Capability floors (DC-1–DC-3 gates) hold with ≤ the probe count the
  protocol-fixed policy used — learner-driven must do at least as
  well with no more probes (efficiency is the claim).
- Determinism: same state → same inquiry decisions (no RNG in the
  inquiry path).

**Memorization signature ruled out:** hypotheses that merely restate
past measurements; inquiry that probes everything (budget discipline
fails) = no judgment, just coverage.

**Table-killer.** A hypothesis about an UNSEEN label ("I believe
regime 7 looks like this; measure it") is unrepresentable in a table
over seen (context, object) pairs. The gate requires the hypothesis
record to precede evidence.

**Scale dimension.** Budget 16 → 160 → 1600 probes/phase; candidate
hypotheses 2 → 20 → 200. Next scale test: DC-4-S10 with 20-way
hypothesis choices under tight budget.

---

## Stage DC-5 — Autonomy under Withdrawal

**Status:** DESIGNED (H-06 anti-facade territory; teacher-withdrawal
was specified, never run — DO_NOT_REPEAT §7).

**Emerging capability.** Scaffolding is withdrawn and development
continues: the system self-initiates deliberate ops (propose, verify,
revise, inquire) without harness prompting, sustains its capability
floors, and respects regression constraints on its own. This is the
stage that answers "was it the teacher?" — with measurement, not
assurance.

**Builds on:** DC-0–DC-4 (the full developmental stack) + R27's
`teacher_dependence` instrumentation hook (`MutableStudent`).

**Environment must provide:**
- Withdrawal phases: harness prompting reduced to zero in steps
  (prompted → hinted → silent), while the world keeps changing by
  design.
- `teacher_dependence` instrumentation: which ops were
  harness-prompted vs. self-initiated (authorship in the ledger —
  R27 recorded authorship per revision).
- The full anchor suite from all prior stages.

**Exit gate (falsifiable):**
- Capability floors from DC-0–DC-4 hold at full withdrawal (every
  prior gate re-run as regression constraint).
- The ledger shows self-initiated deliberate ops during silent phases
  (authorship = learner, not harness) — development continues, not
  just inference.
- No newborn restart: the withdrawing lineage is the same lineage
  (lineage hash chain unbroken, `newborn_restarts == 0` invariant).
- Determinism: same state → same self-initiated decisions.

**Memorization signature ruled out:** floors held by frozen behavior
with zero self-initiated ops = a stopped clock, not autonomy (caught
by the authorship requirement).

**Table-killer.** N/A — by DC-5 there is no table left to kill; this
stage is the anti-facade test for the whole stack.

**Scale dimension.** Withdrawal duration 1× → 10× → 100× episodes;
world-change count during withdrawal 1 → 10 → 100. Next scale test:
DC-5-S10 (10× silent episodes with 10 designed world changes).

---

## What would falsify the curriculum itself

Honest negatives are first-class. The curriculum design is wrong if:
1. Any stage's gate can be passed by a score-table control on the same
   curriculum (the table-killer clauses are then insufficient —
   redesign the gate, not the table).
2. A stage's capability does not transfer as a regression floor to the
   next stage (stages are then blocks, not development).
3. The scale argument fails at the first scale test (mechanism is
   secretly superlinear or RNG-dependent).
4. Determinism breaks (same state, different decisions) — the system
   is not the system we designed.

## Relation to prior art

| Prior work | What this curriculum takes | What it does not repeat |
|---|---|---|
| MA1–MA3 (memory agency) | DC-0 substrate: deliberate audited ops, staged autonomy, ledger replay | Re-proving op semantics |
| HT1/CTX (post-table) | DC-1 mechanism: corroborated switching, partitions as slots | Randomized harness; protocol-fixed policy forever (DC-4 unfixes it) |
| LH-1–5,7 (long horizon) | H-07 discipline, determinism, endpoint retention; long horizons as the norm | A/B episode blocks as the curriculum shape; reward-shaping paradigm |
| R27 lineage | Developmental shape (60,423 steps, zero restarts); trace atom; revision schema | Claiming behavioral continuity (BLOCKED — DO_NOT_REPEAT §7) |
| E51 series | Endpoint retention law; no-aggregate-only reporting | Replay-based preservation (failed — not used) |
| H-06 | DC-5 withdrawal measurement spec | Claiming autonomy without the withdrawal test |

## Deliverables of this investigation

- `CURRICULUM.md` (this file): stages + gates + environment spec.
- `PREREG.md`: preregistration for the Stage-1 (DC-1) native pilot,
  including program-law amendments (determinism, scale, designed
  adversity) — written BEFORE any run.
- `PILOT_RESULTS.md`: pilot results, if run.
- `pilot/`: native Zag sources + runner + evidence.
