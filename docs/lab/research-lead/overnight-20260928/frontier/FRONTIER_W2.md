# Frontier Generation Wave 2 (N2)

Date: 2026-09-30. Worker: Frontier Generator (N2).
Status: generation only. No implementation. No Python at any stage.
Zero em/en dash bytes in this file (shell byte-verified before commit).

## 1. What changed since N1

N1 seeded the backlog at `a3bf86ad3` with 18 scored questions. Since then:

- Q4 explanatory-variable discovery is now the closest line to full C0:
  C0-C PASS and C0-D PASS on the independent adversary family F-PARCOND
  (`5f56cc491`), reproduction 3/3 byte-identical (`121b6d5aa`), baseline
  comparison done (`757442c40`). Ordered blockers: (1) researcher-authored
  beam driver, (2) closed operator alphabet, (3) single adversary data point,
  (4) promotion pipeline incomplete. Ref: `5891940d6`.
- OP-RECRUIT v1 proved the C0-A substrate (recruited opcode semantics in
  learner bytes, one generic dispatch). OP-RECRUIT v2 design complete
  (`c6ef7ffcf`); implementation in progress.
- C0 integration design complete (`9aa1fb0b5`): v2-recruited operators feed
  the Q4 discovery beam. Three-phase ordering. Honest ceiling: stronger
  bounded L2, not L3. Called "the only current architecture that can put
  all four C0 directions in one trace."
- L3 bridge design complete (`e4f8642fc`): removes Form Inventor's dedicated
  diagnosis-to-construction recipes, replaces with generic operators plus
  greedy MDL search. Frozen C0-A audit M1-M4. Implementation in progress.
- Discovery hypotheses A and C falsified (myopic repair cannot cross
  valleys). B and D pending. C2 designed (lookahead L=3, net-progress,
  backtracking BMAX=6, `e658766bd`); implementation in progress.
- F3 Phase 1 tested (`720bb095e`); Phase 2 (per-rule refutation, T-DISJ)
  building.
- Goal subsystem complete: navigate, revise, unlearn (wall removal
  BUILD-PASS, `ed3d7e212`); unified architecture documented (`3f00d4226`).
- DEVANG-H4 failed (`5c2f64857`): 14/20 vs 16/20 baseline, bootstrap
  problem in candidate generation. H1 building.
- Memory infrastructure: S9 eviction scale-tested (`83b78a781`), S10 string
  GC design complete (`fa9579074`) and implemented (`54851fd3f`).
- Continuing learner: transfer tested, extended. Lifetime arena wave
  blocked: 63/63 TNN score recorded but verdict ARENA-BLOCKED pending
  Micah's void vs re-freeze decision. LLM baseline still PENDING.
- Active verification BUILD-PASS with 2-hop cross-check; unified
  verification architecture documented.

Standing mandate (Micah): "Make TNN create cognitive structure its
programmers did not supply, integrate it into one continuing learner, and
demonstrate capability/cost advantages against serious LLM baselines."
Controlling question: "What prevents TNN from being a genuinely general,
continuously learning architecture that we would choose instead of an LLM?"

## 2. Standing questions (updated)

1. Why would a rational user still choose an LLM instead of TNN today?
2. What important cognitive structure is still authored by researchers
   rather than TNN?
3. After the C0 integration and L3 bridge both land, what researcher
   residue remains, and is any of it irreducible?

## 3. Scoring rubric

Each question scored 1 to 5 on seven dimensions. Total out of 35.

- IMP: importance to general intelligence
- INF: expected information gain
- NOV: novelty relative to existing experiments
- FAL: ability to falsify a central TNN hypothesis
- L3P: potential for L3 evidence
- CMP: competitive relevance against LLMs
- INT: integration leverage toward one continuing learner

## 4. The 18 questions

### FQ1: Learner-authored search (attack C0-A blocker 1 head on)

Problem: Q4's ordered blocker 1 is the researcher-authored beam driver.
Every discovery result so far searches inside researcher-written search.
Hypothesis: the search operators themselves can be recruited. The learner
observes which expansion classes historically pay off on which residual
signatures and recruits search policies as persistent state, replacing
the frozen beam loop.
Why existing TNN fails: OP-RECRUIT recruits domain operators; nothing
recruits the machinery that deploys them.
Falsification: freeze the beam as control; if recruited search policies
never beat it on equal compute across T0-T5 plus F-PARCOND, search
authorship adds no leverage and the beam is irreducible scaffolding.
Scores: IMP 5, INF 5, NOV 5, FAL 4, L3P 5, CMP 2, INT 3. Total 29.

### FQ2: Learner-authored evaluation criteria (the deepest residue)

Problem: the C0 integration's honest ceiling lists the detection
criterion family, beam scoring, and intervention policy as
researcher-authored. v2's DETECT uses researcher MDL-style gain.
Hypothesis: the learner can invent what counts as worth keeping. Run a
meta-experiment: the learner tries several retention criteria across
world families and keeps the criterion that predicts later reuse,
treating criteria as hypotheses with track records.
Why existing TNN fails: every retention rule (keep margins, novelty
thresholds, MDL constants) is a frozen literal.
Falsification: if no learned criterion beats the frozen MDL gain on
held-out families, the criterion is irreducible researcher input and
the L3 ceiling is real.
Scores: IMP 5, INF 5, NOV 5, FAL 5, L3P 5, CMP 2, INT 2. Total 29.

### FQ3: Second independent adversary family for Q4 (C0-C data point 2)

Problem: C0-C demands multiple unforeseen forms; Q4 has exactly one
adversary data point (F-PARCOND). One success may be luck or family
fit.
Hypothesis: commission a second independent adversary post-freeze with
a materially different family (recursive or repeated structure, which
F-PARCOND did not exercise). The learner must solve without redesign.
Why this matters: the criterion is conjunctive across forms; a second
family is the cheapest way to test generality of the discovery
machinery.
Falsification: if the learner fails the second family while passing
the first, C0-C does not generalize and the mechanism is family-bound.
Scores: IMP 4, INF 5, NOV 3, FAL 5, L3P 4, CMP 2, INT 2. Total 25.

### FQ4: T6 program discovery (fragment composition in a new context)

Problem: T6 is gated on all of A-D frozen in ancestry. B and D are
pending; C2 is implementing. T6 asks whether fragments learned in
T0-T5 compose to solve a novel task, which is the compositionality
claim behind the whole discovery lane.
Hypothesis: a learner with a fragment library solves T6 with strictly
less search than a learner without it, and the solution reuses at
least one learned fragment structurally (not just its I/O behavior).
Why existing TNN fails: no experiment has measured cross-task fragment
reuse on the VM; reuse claims are single-task.
Falsification: if T6 needs fresh search with no fragment benefit, the
library is decoration and composition is not real.
Scores: IMP 4, INF 4, NOV 3, FAL 4, L3P 3, CMP 2, INT 3. Total 23.

### FQ5: Cross-substrate reuse (stronger C0-D)

Problem: every C0-D claim so far is single-domain (Q4 reuses trees for
trees; goal subsystem reuses maps for maps). The mandate's reuse
criterion lists transfer across prediction, procedure learning, causal
inference, memory, planning.
Hypothesis: take a structure invented by Q4 (for example the 7-op
F-PARCOND tree) and deploy it as a component in a different cognitive
domain (causal effect prediction, or goal-plan cost estimation). Measure
sample-efficiency gain versus a domain-native baseline.
Why existing TNN fails: synergy phases showed researcher-authored
utility transfer, never learner-invented structure crossing domains.
Falsification: if cross-domain deployment never beats the native
baseline, invented structures are domain-bound and C0-D stays narrow.
Scores: IMP 4, INF 4, NOV 4, FAL 4, L3P 4, CMP 3, INT 5. Total 28.

### FQ6: The continuing-learner integration experiment

Problem: the mandate's endgame is one learner experiencing vocabulary,
concepts, procedures, conflicting evidence, inquiry, causal learning,
memory pressure, interference, corrections, and delayed reuse with no
resets and no task labels. Every subsystem is tested in isolation.
Nobody has attempted the integration.
Hypothesis: a single persistent process can run a sequenced experience
battery with preregistered per-capability retention bounds, and
later capabilities reuse earlier invented structure (C0-D at the system
level).
Why existing TNN fails: integration is always "future work"; the
failure modes of shared state (interference, capacity exhaustion,
stale beliefs) are unmeasured.
Falsification: preregister retention floors per capability; if the
integrated learner breaches floors that isolated learners hold, the
substrate cannot yet carry a continuing life.
Scores: IMP 5, INF 5, NOV 4, FAL 5, L3P 4, CMP 4, INT 5. Total 32.

### FQ7: Doubt into planning (the goal architecture's open seam)

Problem: the goal architecture document (`3f00d4226`) names its open
seam: wiring calibrated doubt (verification SUSPECT flags, F3 doubt
scores) into the goal planner. Sensors are currently assumed truthful.
Hypothesis: doubt-weighted planning (prefer routes through
high-confidence cells, probe low-confidence cells before committing)
reaches goals in fewer wasted actions under unreliable sensors than
the frozen planner.
Why existing TNN fails: verification and planning are separate lanes;
doubt never steers action.
Falsification: if doubt-weighted planning never beats the frozen
planner on sensor-noise worlds, the seam is cosmetic and the lanes
should stay separate.
Scores: IMP 3, INF 4, NOV 3, FAL 3, L3P 2, CMP 2, INT 5. Total 22.

### FQ8: Segmentation bootstrap, post-H4 (failure-driven candidates)

Problem: H4 failed on the bootstrap problem: candidate generation is
the bottleneck. Merge needs clean grounding; grounding needs the
merge. Fragment strengths are deeply negative and cannot distinguish
the true word from noise.
Hypothesis: generate candidates from prediction failures, not from
grounding statistics. Wherever the current segmentation mispredicts an
outcome, propose a boundary at the surprise locus. Surprise is
available before grounding is clean.
Why existing TNN fails: every segmentation attempt so far is
bottom-up statistics over impoverished signal.
Falsification: if failure-driven candidates still never surface "grn"
on T1, the signal is too impoverished for any candidate generator and
segmentation needs a different substrate (for example, H1's
consequence grounding must come first).
Scores: IMP 4, INF 4, NOV 4, FAL 4, L3P 3, CMP 2, INT 2. Total 23.

### FQ9: Multi-hop active verification (does A2 scale?)

Problem: active verification passed with 2-hop compositional
cross-check. Real inference chains are deeper. Cost may explode with
chain length.
Hypothesis: extend A2 to n-hop chains with a frozen per-hop budget and
a halting rule (stop when marginal doubt reduction falls below a
frozen epsilon). Contradiction in a derived belief triggers
re-observation along the derivation chain, cheapest hop first.
Why existing TNN fails: verification depth was never stress-tested;
the 2-hop result may not survive contact with depth.
Falsification: if observation cost grows superlinearly with chain
length despite the halting rule, active verification does not scale
to deep inference and must be redesigned.
Scores: IMP 3, INF 4, NOV 3, FAL 4, L3P 2, CMP 2, INT 3. Total 21.

### FQ10: F3 negation, conjunction, and silent causes

Problem: F3 Phase 2 targets T-DISJ. The battery also holds T-NEG,
T-CONJ, and silent-cause worlds. Negation (a rule that must NOT fire)
and silent causes (no observable antecedent) stress the DNF
vocabulary differently than disjunction does.
Hypothesis: DNF with per-rule refutation handles all three without
researcher-added operators; silent causes are learnable as rules with
empty antecedents gated on context literals.
Why existing TNN fails: F2's vocabulary was single-cause; F3 has not
yet met its hard cases.
Falsification: if negation requires a researcher-added NOT-rule
operator, or silent causes are systematically missed, the DNF
vocabulary is insufficient and the representation needs another
review.
Scores: IMP 4, INF 4, NOV 3, FAL 4, L3P 3, CMP 2, INT 3. Total 23.

### FQ11: Sleep and consolidation (offline restructuring)

Problem: the memory lane has eviction (S9) and GC (S10), both online
policies. Nothing reorganizes persistent state offline. Biological
learners consolidate; TNN never sleeps.
Hypothesis: an offline phase (reorder slots by co-access, merge
duplicate content, rebuild indices, re-derive summary statistics)
improves next-episode learning speed at fixed capacity versus a
no-sleep control.
Why existing TNN fails: all memory work is reactive (evict under
pressure); none is proactive restructuring.
Falsification: if consolidated state never beats unconsolidated state
on next-task sample efficiency, consolidation is unnecessary ceremony
and online policies suffice.
Scores: IMP 3, INF 4, NOV 4, FAL 3, L3P 2, CMP 3, INT 4. Total 23.

### FQ12: The learner as its own red team (hypothesis-guided scientist)

Problem: priority 4 of the mandate (hypothesis-guided autonomous
scientist) has no active experiment. F3's disagreement-driven
experiments target action-effect rules only.
Hypothesis: a general belief-level scientist: the learner ranks its
own beliefs by (confidence times falsifiability), generates the
experiment that would most reduce uncertainty per unit cost, and runs
it. Measure belief calibration improvement versus a random-experiment
baseline.
Why existing TNN fails: experiment design is always mechanism-local;
no lane asks "what should I test next" about beliefs in general.
Falsification: if self-generated experiments never falsify a belief
that the random baseline would not also catch, the scientist is
decorative and experiment design stays mechanism-local.
Scores: IMP 5, INF 5, NOV 4, FAL 4, L3P 4, CMP 3, INT 4. Total 29.

### FQ13: Developmental curriculum built from own inventions

Problem: staged development is untested. The learner's promoted
structures could become the training environment for its next stage,
but every lane trains flat.
Hypothesis: two-stage curriculum: stage 1 discovers structures; stage
2 presents tasks whose solutions require composing stage-1 inventions
(the terminals of stage 2 include stage-1 kept variables). Staged
learners reach deeper solutions than flat learners on equal experience.
Why existing TNN fails: curricula are researcher-sequenced task lists,
never learner-product-sequenced.
Falsification: if solution depth never exceeds the flat baseline, self
curriculum adds nothing and staging is a researcher convenience, not
a cognitive lever.
Scores: IMP 4, INF 4, NOV 4, FAL 3, L3P 4, CMP 2, INT 4. Total 25.

### FQ14: The valley-crossing meta-study (B vs D vs C2)

Problem: A and C died of myopia; C1 died of valley-crossing; B
(fragments), D (MAP-Elites), C2 (lookahead plus backtrack) are three
different non-myopic mechanisms with different researcher-set budgets.
Nobody has characterized what each one can actually cross.
Hypothesis: on a parameterized valley-depth battery (valleys of depth
1..k constructed deliberately), each mechanism has a characteristic
maximum crossable depth, and the depth scales with its budget parameter
in a predictable way.
Why this matters: it turns three competing mechanisms into one
measured tradeoff surface, and tells us whether valley-crossing is
solved or merely postponed by budgets.
Falsification: if no mechanism crosses valleys deeper than a small
constant without its budget scaling with k, then non-myopic search is
not solved; all three are budget-shaped, and the real gap is a
mechanism whose reach does not depend on a researcher-set depth.
Scores: IMP 4, INF 5, NOV 4, FAL 5, L3P 3, CMP 2, INT 2. Total 25.

### FQ15: Clean re-freeze of the lifetime arena (governance-gated)

Problem: the lifetime arena wave is ARENA-BLOCKED: TNN scored 63/63
but the verdict is void-or-refreeze pending Micah's decision, and the
LLM baseline is PENDING with no credentials or spend authorized.
Hypothesis: a clean re-freeze (binary hash recorded before world
generation, contestant frozen before generation, pure-Zag toolchain
throughout) reproduces the 63/63 and unblocks the competitive lane.
Why this matters: without it, every "TNN vs serious baseline" claim
rests on a voided wave.
Falsification: governance-gated, not research-gated. If Micah voids
the wave, the information is that the wave's cost was tuition; the
re-freeze design is already specified.
Note: do not run the LLM baseline without his explicit approval; no
spend is authorized.
Scores: IMP 4, INF 3, NOV 2, FAL 3, L3P 1, CMP 5, INT 3. Total 21.

### FQ16: Interference and retention under continuing load

Problem: the mandate requires "unrelated interference" as a lived
experience; the continuing learner has transfer tested but retention
under interference is unmeasured. S9 eviction may be the culprit or
the cure.
Hypothesis: interleave task B training inside task A retention
windows with preregistered retention floors for A. A continuing
learner with pinning plus scored eviction holds the floors; an
append-only control does not.
Why existing TNN fails: retention was measured at rest, never under
interference load.
Falsification: if retention floors breach even with pinning, the
substrate needs a protection mechanism it does not have, and S9's
policy must be revised before any integration claim.
Scores: IMP 4, INF 4, NOV 3, FAL 4, L3P 2, CMP 3, INT 5. Total 25.

### FQ17: The recruitment trap (does RETIRE save the learner?)

Problem: v2 recruits operators from observed subsequence frequency.
The greedy first recruitment may be a local optimum: a common but
shallow pattern that blocks discovery of a rarer, deeper operator.
Hypothesis: construct trap worlds where the frequent pattern is
useless and the useful operator is rare. The learner must recruit the
trap, suffer, RETIRE it, and recruit the rare one. Measure recovery.
Why existing TNN fails: recruitment has never been adversarially
tested; DETECT assumes frequency correlates with utility.
Falsification: if the learner locks onto the trap operator and never
recovers within budget, recruitment needs a revision mechanism it
does not have, and v2's RETIRE path is insufficient.
Scores: IMP 4, INF 5, NOV 4, FAL 5, L3P 4, CMP 2, INT 2. Total 26.

### FQ18: End-to-end cost curves for invented cognition

Problem: the mandate demands capability/cost advantages against
serious baselines, but TNN has no published cost curve for a full
cognitive episode. Fragmentary numbers exist (procedure amortization:
Zag 12 to 40x slower than C; hypothesis population 228k updates/sec;
arena persistent state 1,659 bytes, RSS 14.5 MB).
Hypothesis: instrument one full episode (perceive, learn, invent,
reuse) end to end in wall-clock and bytes, across task difficulties,
and publish the curve. Even before the LLM baseline exists, the curve
makes the eventual comparison well-posed.
Why existing TNN fails: cost is measured per mechanism, never per
cognition; nobody can say what thinking costs.
Falsification: if cost scales superlinearly with task difficulty while
capability scales sublinearly, the architecture has a cost disease
that no baseline comparison can hide, and efficiency becomes the top
priority.
Scores: IMP 4, INF 4, NOV 3, FAL 3, L3P 1, CMP 5, INT 2. Total 22.

## 5. Scoreboard

| ID | Question | Total |
|----|----------|-------|
| FQ6 | Continuing-learner integration experiment | 32 |
| FQ1 | Learner-authored search | 29 |
| FQ2 | Learner-authored evaluation criteria | 29 |
| FQ12 | Learner as its own red team | 29 |
| FQ5 | Cross-substrate reuse | 28 |
| FQ17 | The recruitment trap | 26 |
| FQ3 | Second adversary family for Q4 | 25 |
| FQ13 | Developmental curriculum from own inventions | 25 |
| FQ14 | Valley-crossing meta-study | 25 |
| FQ16 | Interference and retention | 25 |
| FQ4 | T6 fragment composition | 23 |
| FQ8 | Segmentation bootstrap post-H4 | 23 |
| FQ10 | F3 negation, conjunction, silent causes | 23 |
| FQ11 | Sleep and consolidation | 23 |
| FQ7 | Doubt into planning | 22 |
| FQ18 | End-to-end cost curves | 22 |
| FQ9 | Multi-hop active verification | 21 |
| FQ15 | Clean arena re-freeze (governance-gated) | 21 |

## 6. New hypotheses (6, two unconventional)

### H-NEW-1: C0INTEG Phase A build (conventional)

Build Phase A of the C0 integration design (`9aa1fb0b5`): menu
extension plus generic dispatch for opcodes 32..63, with I1 (substrate
regression: v2 R-V1 plus Q4 F-PARCOND) and I3 (no-fire control), gated
by F-BREAK (byte-identical kept-variable outputs after rewrite) and
F-LEAK (validation inputs from learner-observed samples only; harness
truth table never touched; violation voids the run). Dependency: needs
the OP-RECRUIT v2 implementation to land first. This directly attacks
ordered blockers 1 and 2 of the Q4 line: the beam composes recruited
operators, so the menu grows at runtime from learner experience.
Falsifiers frozen in the design transfer unchanged.

### H-NEW-2: Q4 second adversary family (conventional)

Commission independent adversary number two after the current freeze,
with a materially different family from F-PARCOND: recursive or
repeated structure (for example, iterated application, or a
computation selected by a computed index rather than a direct
conditional). The learner faces it with no redesign. Second C0-C data
point; FQ3 is the question, this is the preregistrable experiment.

### H-NEW-3: Continuing-learner integration pilot (conventional)

A bounded pilot of FQ6: one process, no reset, five sequenced
experiences (vocabulary episode, concept learning, procedure
invention, conflicting evidence with active verification, delayed
reuse probe), with preregistered per-capability retention floors and
a no-interference control arm. If the pilot holds its floors, scale to
the full battery (causal learning, memory pressure, unrelated
interference, corrections). This is the mandate's clause 2 made
concrete.

### H-NEW-4: The learner writes its own preregistrations (UNCONVENTIONAL)

Give the learner the preregistration format and require it to freeze
its own falsifiable predictions before each experiment, with a
researcher audit scoring whether the predictions were actually
falsifiable (not vacuous). Rationale: preregistration is a model of
one's own uncertainty made public. A learner that can preregister
honestly has metacognition; a learner whose preregs are vacuous
("I predict I will learn something") has no self-model, and that is
itself a precise, measurable gap. Falsification of the hypothesis:
the audit finds zero non-vacuous preregs across three experiment
types, killing the claim that the learner models its own ignorance.
This tests the mandate's "traceable beliefs" clause from the inside.

### H-NEW-5: Deliberate amnesia probe (UNCONVENTIONAL)

Mid-life, wipe a random subset of persistent learner state (a
frozen fraction, preregistered) and measure recovery time on held-out
probes versus fresh learning from scratch. Rationale: the mandate
distinguishes integrating knowledge from storing facts. Genuinely
integrated knowledge degrades gracefully under partial amnesia and
recovers faster than relearning, because surviving structure
re-scaffolds the lost parts. If recovery time equals fresh-learning
time, the "integration" is just storage with extra steps, and the
continuing-learner claim is weaker than believed. Frozen controls:
wipe size, probe set, and the fresh-learning baseline are all
preregistered; the wipe mechanism is researcher-operated (it is a
measurement instrument, not a cognitive claim).

### H-NEW-6: Valley-depth characterization battery (conventional)

Implement FQ14 as a battery: construct valleys of parameterized depth
1..k on the GENEXEC2 VM, run B (fragment induction), D (MAP-Elites),
and C2 (lookahead plus backtrack) on each, and record maximum
crossable depth per mechanism against its budget parameter. Output is
a tradeoff surface, not a winner: it tells the program-discovery lane
exactly what each mechanism buys and where the budget-shaped ceiling
is. If all three plateau at small constant depth, the lane learns
that non-myopic search is unsolved and stops tuning budgets.

## 7. Highest-information proposal

**H-NEW-1 (C0INTEG Phase A build)** is the highest-information next
experiment.

Reasons:

1. It is the consensus convergence point. The C0 status matrix
   (`5891940d6`) identifies Q4 as closest to full C0 with two ordered
   blockers; the C0 integration design (`9aa1fb0b5`) is the only
   architecture that puts all four C0 directions in one trace. Building
   Phase A tests the integration's load-bearing assumption (recruited
   operators compose inside the discovery beam) with frozen falsifiers.
2. Both outcomes are informative. PASS advances C0-A and C0-B
   simultaneously and unblocks Phase B (consolidation plus grown-menu
   discovery). FAIL localizes exactly which integration assumption
   breaks: substrate compatibility (v1 already de-risks this),
   tree-fragment DETECT adaptation (the design's stated medium risk),
   or the validation information barrier (the stated compile-time
   separation risk). Each failure mode prescribes its own next design.
3. It is buildable now. Dependencies are landing: OP-RECRUIT v2
   implementation is active, Q4 is proven and reproduced, and the
   design freezes the gates (F-BREAK, F-LEAK) and the battery (I1, I3).
   No new science is needed to start; the science is in the result.
4. It dominates the alternatives on information per unit work. FQ2
   (learner-authored criteria) is deeper but premature: you cannot
   test whether the learner can author criteria before the substrate
   in which criteria operate exists. FQ6 (full integration) is larger
   but should follow the pilot H-NEW-3, and the pilot itself benefits
   from knowing whether recruited operators compose. H-NEW-4 and
   H-NEW-5 are high-novelty probes but test properties of a learner
   whose core invention loop is still being built.

Sequencing recommendation: H-NEW-1 first (needs v2 implementation to
land); H-NEW-2 in parallel (independent adversary, no dependency);
H-NEW-3 pilot after H-NEW-1 Phase A passes (so the pilot's procedure
invention stage can use grown menus); H-NEW-6 alongside the B/D/C2
completions (it consumes their results); H-NEW-4 and H-NEW-5 once a
continuing learner exists to probe (they are measurements of the
integrated system, not precursors to it).

## 8. Treadmill watch (added this wave)

- Program discovery: A, C, C1 falsified on myopia/valley-crossing; B,
  D, C2 are three more non-myopic attempts. If H-NEW-6 shows all three
  plateau at budget-shaped depths, stop the lineage and open the
  architecture review the standing rules require ("is the current
  representation itself wrong?").
- Segmentation: H4 failed on bootstrap; H1 is the fallback. If H1
  also fails on T1, the lane has two failed hypotheses on the same
  task family and owes an architecture review, not a third hypothesis.
- Verification: 2-hop passed; do not extend to n-hop by researcher
  increments without FQ9's cost-scaling measurement, or the lane
  becomes hop-count tuning.
- The paper remains a contaminated internal log. No wave may cite it
  as evidence. Canonical claims reconstruct from preregs, ancestry,
  raw results, reproductions, adversaries, and audits only.

## 9. Governance notes

- This document is generation only: questions, scores, hypotheses,
  sequencing. It makes no empirical claims and freezes no bars.
- FQ15 is governance-gated: the arena re-freeze needs Micah's
  void-or-refreeze ruling, and the LLM baseline needs his explicit
  spend/credential approval. Nothing here authorizes either.
- The Python audit is active elsewhere; this wave's generation used
  no Python at any stage.
- Backlog discipline: this file supersedes N1's backlog as the live
  queue. N1's file remains in history (`frontier_gen/BACKLOG.md`) and
  is not edited.
