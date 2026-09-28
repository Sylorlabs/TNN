# R23 LESSONS — What the Python-era teaching experiments say about taught vocabulary

**Crew:** 7 (non-binding exploratory track), TNN Representation Program, Track B
**Date:** 2026-09-21
**Status:** INSIGHTS ONLY. The Track B prereg is FROZEN (Micah signed 2026-09-21).
Nothing here changes any frozen bar, metric, kill criterion, or the §P / TST-1 / §C
specs. Candidate protocol insights are labeled **PROPOSED-FUTURE-AMENDMENT** and would
need Micah's re-approval per RULE-9. No code was written; all sources read read-only.

## Sources (read-only)

- `/tmp/drive_seg/r23_experiments.py` — 63,069 bytes; the exact R23 source recovered
  2026-09-17 (SHA-256 `517eb325096d5ae71ebb3bf659da77eac4266129136b888b469a99e366d4b642`
  per the recovery record). Four byte-identical copies exist under `/tmp/r23rec/`.
  Read as inert historical source, not a dependency.
- `~/workspace/tnn-lab/units/ARCHAEOLOGY_R31.md` — the archaeology note flagging the
  R23 teaching experiments as "a direct ancestor of the taught-vocabulary arm."

**Honesty caveat, stated up front:** the *quantitative* outcomes of these experiments
(which teacher policy won, the dose curves, the master-vs-TNN advantage number) were
computed into `lineage/r23_summary.json`, which is quarantined in the recovered
archive and **not locally readable** (the local `final-summary.json` is 0 bytes).
What follows is therefore **protocol-level archaeology**: what was varied, what was
measured, what the built-in negative controls were, and what teaching moves the code
embodies. No numeric claim about R23 outcomes is made here — the numbers stay
quarantined until someone with archive access reads them. Per ARCHAEOLOGY_R31.md,
all of it is substrate-remote anyway (Python-era, synthetic 72-dim event streams, not
byte streams) — mechanism inspiration, never transferred evidence.

The one Google Doc flagged by the archaeology note (`ghost#1`, matched "vocabulary")
was not read — it needs the Docs skill, flagged, not blocking.

## The experiments (what the code actually does)

### E1 — `strengthened_master_experiment` / `_teacher_train` (seed 23001, budget 1400 steps)

Four teacher policies teach the same anonymous learner on the same concept set
(FOUNDATION, ~55 English concepts, each with a SURF paraphrase list), evaluated at
steps 100 / 300 / 600 / 1000 / 1400 on single-word and compositional probes:

- **STRONG_DIAGNOSTIC_MASTER.** Steps 0–180: pure *coverage* — always teach the
  least-taught concept. After 180: *diagnose* — probe every concept, pick the one
  with the lowest top1−top2 margin (exposure-penalized), teach that. Surface choice
  rotates paraphrases deterministically and *emphasizes contrast after confusion*
  (when the learner confuses A for B, the confusion pair is recorded and contrast
  is taught). Every 2nd step: a compositional example built around the current
  weakest concept. Every lesson is two updates: teacher evidence at weight .75
  (`'MASTER'`), then the world's own grounding at weight 1.0 (`'DIRECT_WORLD'`).
- **R22_STYLE_MASTER.** Simple random curriculum, first 3 surfaces only — the "dumb
  master" baseline from the previous generation.
- **MASS_MASTER.** Massed practice: 20-step blocks per concept — a deliberate
  overconcentration negative control.
- **SYMBOLIC.** Rejection-only teaching (`symbolic_reject`: a tiny negative nudge,
  lr×.012): pure "no, not that," never a positive example — a negative control for
  correction-without-grounding. The experiment reports `symbolic_gap` = winner minus
  SYMBOLIC, i.e., the value of positive grounded teaching over pure correction is
  an explicit measured quantity.

### E2 — `english_apprenticeship_inversion_experiment` (seed 23601, n=500)

The direct ancestor of Track B's peer-teacher arm: a **master-taught child vs a
TNN-taught child**, both anonymous mutable learners starting from the same blank
state, evaluated identically. The master teacher runs a fixed-then-random
curriculum. The TNN teacher (a mature TNN, not the master) does three things the
master doesn't:

1. **Diagnoses the child's uncertainty** — each step, probes all concepts and
   teaches the one with the lowest top1−top2 margin (the concept the child is
   closest to getting wrong);
2. **Teaches as a peer, at peer weight** — updates carry weight .6 with source
   `'SIBLING'` (below the master's .75);
3. **Varies the surface from its own neighborhood** — every 4th step, an extra
   paraphrase drawn from the teacher's own learned surface neighborhood at weight .5.

Both teachers' lessons are always followed by the world's independent grounding
(1.0, `'DIRECT_WORLD'`). The reported quantity is `advantage` = TNN-taught minus
master-taught. The boundary string is the thesis in one line: *"English-specific
teacher inversion on anonymous mutable learners; both teachers use externally
grounded consequences, no English dictionary installed into child."*

### E3 — the learner both experiments share: `AnonymousGroundedLearner`

- **Source-reliability hierarchy, baked into the update rule:**
  `DIRECT_WORLD 1.0 > MASTER .75 > SIBLING .55`. Teacher evidence is *discounted by
  source*; nothing the teacher says outranks the world's own consequences.
- **Spaced replay with source-deduplication** — the replay buffer dedups by
  (source, content-hash), so five repetitions from one source don't count five times.
- **`symbolic_reject`** exists but is deliberately weak (1.2% of the learning rate)
  — correction is a nudge, never the teaching.

### E4 — `sibling_language_community_experiment` (seed 23501)

Four sibling learners each get a *different quarter* of surfaces and concepts, then
share sourced episodes with provenance. The receiver keeps received evidence
**lower-weight until locally checked**, then verifies by direct consequence. The
misinformation trap: **five repeated false claims from one origin (.12 weight each)
versus one direct observation (1.0)** — the direct observation wins
(`misinformation_recovery`). Same-source repetition is low authority *by
construction*.

### E5 — `cooperative_play_experiment` (seed 23401)

Language is useful because it *reduces action cost* (grounded pointing → 1 try vs
blind guessing). Symbolic rejection-only is again the negative control. A sibling
with 10% noise is usable **because errors are source-checked by action** —
consequence corrects the peer, not the peer's authority.

## Teaching moves that worked (protocol-level)

- **T1 — Coverage, then diagnosis.** Never start diagnostic. The strong master opens
  with 180 steps of pure least-exposed-concept coverage and only then switches to
  margin-driven teaching. Cold start needs breadth; diagnosis needs a baseline to
  diagnose *against*.
- **T2 — Teacher proposes, world confirms, every lesson.** The `.75 MASTER` +
  `1.0 DIRECT_WORLD` double-update is the whole integrity model: the teacher never
  writes directly into the learner, and teacher evidence is always outranked by
  independent grounding. This is the direct ancestor of §B.5's corroboration rule
  and of "confidence is a weight, never a command" — R23 had already learned that
  the teacher must not be the authority of last resort.
- **T3 — Discount by source, dedup by source.** 1.0 / .75 / .55 is a standing
  reliability hierarchy, and replay dedups (source, content) so repetition from one
  mouth doesn't compound. Track B's §B.5 currently treats corroborating sources as
  equivalent ("own observation, a second teacher, or the oracle"); R23 suggests
  they shouldn't be.
- **T4 — The peer teacher diagnoses uncertainty and paraphrases.** The TNN teacher's
  three moves — lowest-margin concept, peer weight, surface variation from its own
  neighborhood — are a spec for what Track B's arm-1 wiring should *do*: teach what
  the learner is closest to getting wrong, in the teacher's own words, not the
  master's script. A peer teacher that just repeats the master curriculum is
  E2's control condition, not its innovation.
- **T5 — Contrast after confusion.** Confusion pairs are recorded
  (`confusions[(c, guess)] += 1`) and the *contrast* is taught, with paraphrase
  surfaces rotated deterministically. Error-driven contrast teaching, not
  error-blind repetition.
- **T6 — Composition around the weakest concept.** Every 2nd step the strong master
  teaches a two-concept composition built around the current weakest concept.
  Vocabulary was never taught as isolated words — always in compositional usage.
  This matches §P's grounding spans as usage examples, and suggests the frozen
  protocol's word-at-a-time framing may under-teach.
- **T7 — Provenance on shared episodes; repetition ≠ grounding.** Sibling evidence
  arrives labeled, is held light until locally verified, and five repeats from one
  origin lose to one direct observation. The ancestor of the appeal bound (max 2 —
  re-asking doesn't make it truer) and of "TEACHER PROPOSES, TNN DISPOSES."
- **T8 — The boundary itself.** "No English dictionary installed into child" —
  teacher/evaluator owns curriculum and grounding; the learner holds only generic
  byte-to-event weights plus replay. This is Micah's 2026-09-21 installed-vs-learned
  ruling in Python-era clothing: taught is a *route* to learned, never a quiet form
  of installed. R23's architecture already refused to let teaching blur into
  installation.

## What failed (the built-in negative controls)

- **F1 — Massed practice (MASS_MASTER).** Twenty-step blocks per concept: the
  overconcentration control. Blocked teaching was built to lose to interleaved,
  diagnostic teaching.
- **F2 — Rejection-only teaching (SYMBOLIC).** Pure correction with no positive
  grounded example: the `symbolic_gap` metric exists to quantify exactly how much
  this loses by. "No, not that" is not teaching.
- **F3 — Unchecked peer noise.** The 10%-noisy sibling is only usable because every
  claim is source-checked by action/consequence. Peer teaching without grounding
  verification is not in the design space — it was excluded by architecture, not
  tested and failed.

## What the dose curves showed (structure, not numbers)

- **D1 — Geometric eval schedule.** `_teacher_train` evaluates at steps
  100/300/600/1000/1400 on a 1400-step budget — roughly geometric spacing. The
  *shape* of the curve matters: the coverage phase (0–180) and the diagnostic phase
  (180+) are expected to show different slopes, and the dose curve is how you'd see
  whether diagnosis actually accelerates over random curriculum or just re-labels
  it. Track B scores mastery and cost but freezes no dose-sampling schedule —
  endpoint-only scoring can't distinguish "fast starter, early plateau" from "slow
  starter, late surge," which is exactly the difference the teacher arms are
  supposed to compete on.
- **D2 — The inversion comparison is teacher-policy, not dose.** n=500 fixed for
  both children; the only variation is *who teaches and how*. That's the right
  ancestor for Track B's arm bake-off: fix the dose, vary the teacher.

## Concrete protocol insights for a FUTURE amendment (all PROPOSED, none in force)

- **PA-R1 — Coverage-then-diagnosis in the arm-1 wiring spec.** The peer teacher's
  wiring spec (§B.2.3) currently demands "selective proposals and expressed
  uncertainty" — R23 suggests adding a *schedule*: a coverage phase over
  underexposed vocabulary before margin-driven teaching begins. Cold-start
  diagnosis has no baseline.
- **PA-R2 — Weighted corroboration sources.** §B.5 treats own observation, second
  teacher, and oracle as equivalent corroboration. R23's 1.0 / .75 / .55 hierarchy
  suggests weighting them (own observation highest), so a teacher+teacher
  corroboration pair counts for less than teacher+world. (Note the resonance with
  ATTACK_CATALOG.md A6: the colluding-teacher shape exploits equivalent-weighted
  corroboration.)
- **PA-R3 — Repetition non-accumulation.** The appeal bound (max 2) already embodies
  "re-asking doesn't make it truer"; R23's source-deduped replay suggests extending
  the principle: repeated identical teacher assertions must not accumulate
  authority by repetition alone, in deliberation weighting as well as in appeals.
- **PA-R4 — Geometric dose checkpoints.** Add preregistered mastery-vs-dose
  sampling (e.g., geometric checkpoints across the curriculum slice) so teacher
  arms compete on learning *curves*, not endpoints. Informs the cost model (§M)
  without changing its frozen per-word definitions.
- **PA-R5 — Confusion-pair contrast as a teacher move.** When the learner's REVISE/
  REJECT reveals a confusion pair, the teacher may teach the contrast — a
  preregistered, auditable teacher move consistent with "teacher proposes,"
  distinct from re-proposing the same span (which counts against appeal bounds).

## What this document does NOT do

- It does not report R23 numeric outcomes (quarantined; not locally available).
- It does not transfer any R23 quantity into the native program (substrate gap —
  synthetic 72-dim event streams vs byte streams — per ARCHAEOLOGY_R31.md).
- It does not amend the frozen prereg. Every PA-R item above is a candidate for a
  future dated amendment cycle, requiring Micah's re-approval per RULE-9.
