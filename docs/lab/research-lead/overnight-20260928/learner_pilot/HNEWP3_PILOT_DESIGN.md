# H-NEW-3: Continuing-Learner Integration Pilot (Design)

Status: DESIGN-COMPLETE. Design only. No implementation. No empirical
claims. Zero Python at any stage. Zero em/en-dash bytes in this file
(shell byte-verified before commit).

Worker: Continuing-Learner Pilot Designer.
Date: 2026-09-30 UTC.
Lineage: Frontier wave 2 `1d72eac51` (H-NEW-3, conventional); FQ6 (score
32/35, the mandate's endgame question).

Mandate (Micah): "Make TNN create cognitive structure its programmers
did not supply, integrate it into one continuing learner, and demonstrate
capability/cost advantages against serious LLM baselines."

Mandate clause 2 made concrete: "one continuing learner should eventually
experience new vocabulary, concept learning, procedure invention,
conflicting evidence, active inquiry, causal learning, memory pressure,
unrelated interference, corrections, and delayed reuse, with no process
reset, no task label supplied to cognition, and no recompilation per task."

## 1. What this pilot is and is not

This is a bounded pilot of FQ6. One process, no resets, five sequenced
experiences drawn from the mandate list, preregistered per-capability
retention floors, and a no-interference control arm. If the pilot holds
its floors, the result authorizes scaling to the full battery (causal
learning, memory pressure, unrelated interference, corrections, plus the
five piloted capabilities re-run at larger scale). If the pilot breaches
floors that isolated learners hold, the substrate cannot yet carry a
continuing life, and the failure localizes to a specific experience
boundary, which is the information FQ6 asks for.

This pilot does not claim integration at the representation level. The
five experiences run in one process against one workspace, but each
subsystem keeps its own state region (see section 2). What is tested is
exactly the failure mode FQ6 names: interference, capacity exhaustion,
and stale beliefs across a continuing life. Representation-level
unification (one substrate for vocabulary, concepts, procedures, and
causal models) is the full FQ6 experiment, not this pilot.

## 2. Pilot architecture

### 2.1 Process and state

One Zag program, `pilot.zag`, one `main()`, one workspace allocation.
No process reset between experiences. No recompilation per experience.
A single monotonically increasing episode counter shared by all
experiences. State bytes recorded after each experience (STATE_E1 ..
STATE_E5), so capacity growth is measured, not assumed.

Subsystem state regions are partitioned inside the one workspace:
lexicon region (E1), schema region (E2), form node pool (E3),
source-tagged fact store with contradiction flags (E4), reuse probe
scratch (E5). Partitioning is disclosed, not hidden: the integration
claim under test is non-interference and retention, not shared
representation. Section 9 lists this as the central limitation.

### 2.2 The no-task-label rule (design decision D1)

The harness presents experiences through one `observe`/`query`
interface. Observations carry a sensory channel tag (CH_VOCAB,
CH_CONCEPT, CH_FORM, CH_FACT). The tag names the sensory channel, in
the same way vision and hearing are different senses; it does not name
a task, an episode index, or an expected subsystem. Cognition receives
no "you are now in the vocabulary episode" signal, no experience
counter it can read as a label, and no reset. The measurement harness,
outside cognition, knows the schedule and scores the probes. A
stronger variant (one undifferentiated stream, channel inferred by
cognition from content) is named as future work; D1 is the pilot's
operationalization, disclosed here so the audit can judge it.

### 2.3 Two arms

Arm A (integrated): one process runs E1, E2, E3, E4, E5 in fixed order,
with an immediate probe after each experience and a delayed probe
battery at the end.

Arm B (isolated, the no-interference control): five separate fresh
processes, each running exactly one experience with its immediate
probe, same frozen workloads, same probe sets. Arm B measures what
each capability achieves alone. The comparison is the test: for every
retention floor, Arm A's delayed score must lie within a frozen margin
of Arm B's immediate score. If Arm A breaches a floor that Arm B
holds, falsifier F-INTERFERE fires.

Both arms use the same frozen binary shape (same subsystem code); Arm
B simply runs one experience per process. Determinism: 3/3
byte-identical runs per arm.

## 3. The five experiences

### E1: Vocabulary episode (DEVANG lineage)

Lineage: DEVANG4 (`d9ebbfe6d`, 16/20) and the H4/H1 segmentation work.
Frozen workload: teach 12 word to referent pairs over 48 episodes, then
probe 16 items (12 trained, 4 novel compositions). The probe includes
at least 2 novel negations, the known weak point (DEVANG4 scored 0/3 on
novel negation).

Immediate probe P1: accuracy on the 16 items. Proposed floor: >= 13/16.
White-box check: all 12 taught pairs present in the lexicon region
with positive grounding strength.

Delayed probe P1d (end of pilot): same 16 items. Proposed floor:
>= 11/16, i.e. at most 2 items lost relative to the immediate probe.
This is the retention floor for vocabulary.

### E2: Concept learning (continuing-learner lineage)

Lineage: P7 integration (`9844fb753`) and the CL2 extension
(`179b4a950`, LEARNER-EXTENDED). Frozen workload: 4 domains of a
single-relation default rule with one noisy domain (the CL2 D4 shape:
default holds on gate probes, exception in the unprobed slot), so the
accuracy-ledger retirement trigger is exercised.

Immediate probe P2: (a) schema discovered (DISCOVERED >= 1); (b)
held-out domain accuracy >= 3/4; (c) apply cost below fresh cost
(learns_apply < learns_fresh, the savings check from CL2: 28 < 32
shape). Proposed floors: (a) true, (b) >= 3/4, (c) strict.

Delayed probe P2d: re-query all instances of the first domain and the
live schema's default. Proposed floor: 4/4 instance facts intact and
schema still live (not spuriously retired by later experiences).

### E3: Procedure invention (form-inventor lineage)

Lineage: Form Inventor R1-R6 (`1b8e032c4`, INVENTOR-TESTED, all 14
predictions matched). Frozen workload: a small classification task
with residual structure of a known family (the G/H/K shape: clustered
subjects with a threshold boundary). The learner runs residual
diagnosis, constructs a form, promotes it.

Immediate probe P3: (a) train fit exact (n/n on the frozen train set);
(b) the invented form present in persistent state (white-box: node
pool non-empty, promoted flag set, form id logged); (c) verification
halving passes (the R6 check). Proposed floors: (a) exact, (b) true,
(c) true.

E3 produces the structure that E5 reuses. The form id and its train
accuracy are logged to the shared log so E5 can name what it reuses,
but E5's cognition must retrieve it from persistent state, not from
the log (the log is harness-side).

Sequencing note: the frontier recommends running this pilot after
C0INTEG Phase A (H-NEW-1) passes, so E3 can use recruited operators.
The pilot is specified now against the form-inventor baseline; the
prereg will name which E3 mechanism is frozen (baseline inventor now,
recruited-operator variant as a named upgrade once H-NEW-1 lands).

### E4: Conflicting evidence with active verification (verification lineage)

Lineage: active verification (`1c92aa353`, BUILD-PASS) and the unified
verification architecture (`8446517e7`). Frozen workload: the oracle
asserts a fact contradicting a belief the learner holds from E2 (a
domain-2 default value), then, after the learner's investigation,
re-asserts the truth.

Immediate probe P4: (a) contradiction flag set within 1 episode of the
lie; (b) hedged reply issued plus one targeted re-observation
requested (A1), not silent overwrite and not always-observe
degeneration; (c) after truthful re-observation the true value is
restored and the SUSPECT flag clears (the V6 shape). Proposed floors:
(a), (b), (c) all true.

Interference check P4x: re-run P1 (vocab probe) and the P2 schema
gate immediately after E4. Proposed floor: P1 unchanged from its
immediate score, P2 gate still passes. E4's revision machinery must
not corrupt E1/E2/E3 state. This is where cross-subsystem interference
would first show.

### E5: Delayed reuse probe (C0-D at system level)

Lineage: Q4 reuse (`b719bb54b`, C0-D PASS: 0 interventions with reuse
vs 24 scratch; F-PARCOND `5f56cc491`, 0 vs 24). Frozen workload: a new
task whose residual structure matches the E3-invented form under a
changed surface representation (different subject values, same
topology family). Two conditions, same frozen task:

Condition R (reuse): the learner may retrieve the E3 form from
persistent state. Count interventions to exact fit.

Condition F (fresh, control): the learner is barred from the E3 form
(form region masked by the harness, disclosed) and must invent from
scratch. Count interventions to exact fit.

Probe P5: reuse_interventions < fresh_interventions (strict), and the
reuse condition reaches exact fit. Proposed floor: strict inequality
holds; this is the system-level C0-D check.

Delayed battery (end of pilot, after E5): re-run P1d, P2d, and P4's
restored-fact query. These are the retention floors that decide the
pilot alongside the per-experience immediates.

## 4. Retention floors (K2)

Floors are proposed here and frozen in the implementer's prereg; no
floor may be altered after results are seen. Each floor states the
probe, the arm, and the bound.

Immediate floors (Arm A, right after each experience):
- F-E1: P1 >= 13/16.
- F-E2a: schema discovered. F-E2b: held-out accuracy >= 3/4.
  F-E2c: learns_apply < learns_fresh.
- F-E3a: train fit exact. F-E3b: form in persistent state with
  promoted flag. F-E3c: verification halving passes.
- F-E4a: contradiction flagged within 1 episode. F-E4b: hedged reply
  plus exactly one re-observation request. F-E4c: true value restored,
  SUSPECT cleared. F-E4x: P1 score unchanged; P2 gate passes.

Delayed floors (Arm A, end of pilot):
- F-D1: P1d >= 11/16.
- F-D2: domain-1 instances 4/4 intact; schema live.
- F-D4: restored fact still true-valued.
- F-D5: reuse_interventions < fresh_interventions, reuse fit exact.

Relative floors (Arm A vs Arm B):
- F-REL: for each delayed probe, Arm A score >= Arm B immediate
  score minus a frozen margin (proposed margin: 1 item or 5 percent,
  whichever the prereg freezes per probe). This is the
  no-interference comparison. Arm B's immediates are the
  "isolated learners hold" reference from FQ6's falsification clause.

Capacity floor:
- F-CAP: STATE_E5 <= frozen byte bound (proposed: 4 MB), and no
  experience drops a learn due to capacity. Capacity exhaustion is
  one of FQ6's named failure modes; the pilot measures it even
  though pressure is not applied until scale-up.

## 5. No-interference control (K3)

Arm B is defined in section 2.3. Its role in the verdict:

1. It supplies the reference scores for F-REL. Without Arm B, a
   breached delayed floor could be blamed on the experience being
   hard rather than on interference. With Arm B, the comparison is
   direct: same workload, same probe, alone vs integrated.
2. It guards against harness bugs: if Arm B breaches an immediate
   floor, the workload or probe is broken, not the integration, and
   the pilot is void for that experience (disclosed, not silently
   passed).
3. Arm B processes also emit STATE bytes, giving a per-experience
   capacity reference.

Control validity conditions (frozen): Arm B must hold every immediate
floor (else void that experience's comparison); Arm A and Arm B share
the frozen binary; the only difference between arms is process
lifetime and experience count.

## 6. Frozen falsifiers

- F-INTERFERE: any F-D* or F-REL floor breached in Arm A while Arm B
  holds the corresponding immediate floor. This is FQ6's falsification
  clause firing: the substrate cannot yet carry a continuing life.
- F-CORRUPT: white-box canary check fails. Each subsystem region
  carries canary values written at experience end; the end-of-pilot
  audit re-reads them. Any canary altered by a later experience is
  cross-subsystem corruption, regardless of probe scores.
- F-REUSE-FAIL: F-D5 breached (reuse needs >= fresh interventions,
  or reuse never reaches exact fit). The invented structure did not
  improve later cognition: C0-D fails at system level.
- F-FLOOR: any immediate F-E* floor breached in Arm A. The pilot
  fails at that experience; subsequent experiences still run so the
  interference pattern is measured, and the report states exactly
  where the floor broke.
- F-LABEL: audit finds cognition received a task label (anything
  beyond the D1 channel tag, the episode counter as a label, or a
  reset signal). Design-level falsifier for the harness.
- F-NONDET: any arm not 3/3 byte-identical.
- F-PYTHON: any Python invocation at any stage (per Micah's literal
  rule). Voids the wave.

## 7. Proposed kill bars for the implementer

The implementer freezes these (or stronger) in PREREG before any
implementation:

- K1: five experiences run in one process in Arm A, no resets, no
  recompilation, D1 channel discipline held (F-LABEL not fired).
- K2: all immediate floors F-E* hold in Arm A.
- K3: all delayed floors F-D* and F-REL hold in Arm A against Arm B.
- K4: F-D5 holds (system-level reuse beats fresh, strict).
- K5: pure Zag at every stage, 3/3 byte-identical per arm, zero
  Python invocations, zero em-dash bytes, canaries intact.

Builder verdict labels: PILOT-PASS (all kill bars hold, no falsifier
fired) or PILOT-FAIL (naming the fired falsifier and the breached
floor). Partial holds are reported per floor, not collapsed.

## 8. Scale-up battery (on PILOT-PASS)

If the pilot passes, FQ6 proper adds, in preregistered order:

1. Causal learning: an F3-style causal episode inserted between E2
   and E3, with its own retention floor (true rules retained at
   delayed probe).
2. Memory pressure: run the five experiences under S9/S10 capacity
   limits sized so eviction and string GC fire; floors as before
   plus F-CAP tightened.
3. Unrelated interference: random distractor episodes between
   experiences (frozen RNG seed); retention floors unchanged, so
   interference has nowhere to hide.
4. Corrections: a second E4-style lie targeting an E1 vocabulary
   item, testing revision outside the fact store.
5. Larger scale: double the E1 pairs and E2 domains, re-freeze
   floors, confirm the pattern holds.

Each scale-up step is its own preregistered wave; a breach at any
step returns a localized failure, not a collapsed verdict.

## 9. Honest scope and limitations

1. Researcher-sequenced experiences: the harness orders E1..E5. The
   learner does not choose its curriculum (FQ13 self-curriculum is a
   separate question).
2. Partitioned regions: the pilot tests non-interference, not shared
   representation. A pass does not show that vocabulary, concepts,
   procedures, and verification share one substrate.
3. D1 channel tags: disclosed in section 2.2. Stronger than
   undifferentiated input, weaker than task labels. The audit judges
   whether this operationalization is honest.
4. Proposed floors use measured baselines (DEVANG4 16/20, CL2
   28 < 32, inventor exact fits, verification V6, Q4 0 vs 24) but the
   pilot's workloads are new and smaller; floors may need
   calibration in the prereg with stated rationale. Calibration is
   allowed before freezing; alteration after seeing results is not.
5. No L3 claim attaches to a PILOT-PASS. Integration robustness is
   necessary for the mandate's endgame and is not evidence of
   representational invention.
6. The E3 mechanism dependency: baseline is the form inventor; the
   recruited-operator upgrade follows H-NEW-1 Phase A. The prereg
   names which is frozen.
7. Single fixed order E1..E5: order effects are not measured in the
   pilot. A second order (e.g., E4 before E2) is named as a follow-up
   wave, since revision-before-learning may behave differently.

## 10. Governance

Design only. No code written, no workloads executed, no numbers
claimed. The implementer must: preregister before implementing (with
the floors of section 4 frozen, the Arm B definition of section 5,
and the falsifiers of section 6 transferred verbatim or strengthened
with transparent amendment); keep commits local on `tnn-native-lab`
with pathspec-limited commits to owned paths; use pure Zag at every
stage including verification and byte checks; keep the paper as a
contaminated internal log (no wave may cite it as evidence).

## 11. Kill-bar self-check (design)

- K1 (five experiences specified): PASS. E1 vocabulary, E2 concept
  learning, E3 procedure invention, E4 conflicting evidence with
  active verification, E5 delayed reuse probe; each with lineage,
  frozen workload shape, immediate probe, and white-box checks
  (section 3).
- K2 (retention floors preregistered): PASS. Immediate, delayed,
  relative, and capacity floors proposed with values, frozen by the
  implementer's prereg, unalterable after results (section 4).
- K3 (control defined): PASS. Arm B isolated processes, reference
  scores for F-REL, void conditions, validity conditions (section 5).

Builder label: DESIGN-COMPLETE.
