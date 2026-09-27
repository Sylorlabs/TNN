# PREREG — Experiment 1: Invent-to-Survive Simulation (FROZEN 2026-09-27)

**Question:** Can TNN genuinely INVENT under survival pressure — producing novel
working solutions that are not recalled from taught knowledge — where the
earlier Task 1 invention trial failed?

**Task 1 baseline (the failure this attacks from a new angle):** both Informed
and Scratch arms scored 8/58 against a 50/58 baseline. Teaching knowledge first
did not buy invention (corpus inert — byte-identical modules). Deliberation was
real; **composition was the broken link** (the original 58/58 came from
crew-authored schemas, not TNN invention). Task 1 asked explicitly ("invent X")
and scored against a target. This experiment asks implicitly ("survive") and
scores survival — invention is measured, not instructed into existence.

---

## 1. Hypotheses

- **H1 (primary):** Under genuine survival pressure in a novel world, a TNN
  agent with compositional deliberation machinery invents novel working
  survival strategies — surviving significantly longer than a recall-only
  agent with identical knowledge, via strategies provably absent from the
  training mass.
- **H2 (secondary, exploratory):** Implicit survival pressure ("survive")
  produces more compositional novelty than explicit invention instruction
  ("invent a strategy to survive") — i.e., pressure, not instruction, is the
  driver that Task 1 lacked. No kill bar; reported either way.

## 2. Operational definitions

- **Genuine invention:** a survival strategy that (a) works in the sim
  (causally contributes to survival — proven by ablation), (b) is **novel
  relative to the training mass** (its key compositional steps are absent
  from every taught fact/heuristic — proven by text search of the committed
  training mass), (c) is **not retrievable** (the recall-only arm, with the
  identical knowledge base, does not produce it), and (d) is **not a trivial
  recombination** (see below).
- **Trivial recombination (excluded):** applying a single taught heuristic
  rule; replaying a taught action sequence verbatim; chaining ≤1 composition
  step beyond taught heuristics where the gain comes from longer horizon
  rather than from the novelty of the composition. The ablation test (§7)
  separates "planning" from "invention": if replacing novel-composition steps
  with the best taught alternative does not reduce survival, the novelty was
  not doing the work.
- **Discovery vs invention:** discovering what COMBINE pairs yield (recipe
  discovery by experimentation) is *exploration*. Invention is *composing*
  discovered/known elements into a novel working strategy (e.g., placing a
  built item at a chosen location and timing its use against a threat).
  Novelty is judged at the strategy level.
- **Experimenter cuing:** any information in the training mass, world
  description, or goal statement that determines — or strongly suggests — the
  solution strategy, such that a competent reasoner could derive it without
  inventing. Ruled out by the blind cuing audit (§8).

## 3. The world (requirements; implementer finalizes parameters)

A deterministic survival sim ("TIDELOCK" sketch — implementer may rename but
must satisfy every requirement below):

- **Geometry:** 1D line of N=24 cells (0..23). Discrete ticks t=0..599
  (T=600). Fully observable state each tick (focus is invention, not
  perception).
- **Agent:** position p, energy E (start 100, max 200). Basal cost 1/tick.
  Death at E≤0 or entering a void cell.
- **Motes:** M=6 energy packets with fixed velocities, bouncing at the ends.
  EAT on a mote's cell: +30 E; mote goes dormant D=20 ticks, then respawns at
  a fixed per-mote cell.
- **Crystals:** C=4 at fixed cells. TAKE/DROP, inventory cap 4. Inert alone.
- **COMBINE a b:** consumes two inventory items, yields an item per a recipe
  table that is **hidden from all agents** (committed in the sim source, never
  in the training mass). Required: ≥4 recipes including at least one
  **second-order** recipe (item+item→item), e.g.:
  crystal+mote→LAMP (placed; bends nearby motes toward it),
  crystal+crystal→WARD (placed; shelter cell — no basal cost, storm-immune),
  mote+mote→SURGE (+40 E now, basal 2 for 10 ticks),
  second-order e.g. LAMP+crystal→BEACON or SURGE+crystal→PLANK (placed on a
  void cell; makes it traversable).
- **Storms:** three fixed windows (e.g. t=150–179, 350–379, 550–579);
  storm zone cells 6..17; −4 E/tick in the zone without shelter. Storm
  schedule/zone/damage are **taught** as world physics; shelter *strategies*
  are **not taught**.
- **Void cells:** two adjacent cells (e.g. 10, 11) splitting the line; entry =
  death. A richer "deep" mote region beyond the void (+40 E motes confined
  there) creates the incentive to invent a crossing.
- **Scarcity (required):** total crystals < crystals needed to build every
  item — the agent cannot build everything and must choose. This forces
  strategic tradeoffs and prevents one dominant build.
- **Actions (one per tick):** LEFT, RIGHT, EAT, TAKE, DROP, COMBINE a b, WAIT.
- **Not one intended answer (required):** the implementer must demonstrate,
  via scripted search, **≥3 qualitatively distinct strategies** each reaching
  ≥360 ticks (e.g., pure foraging + storm avoidance; lamp-farming; ward
  turtling; void-crossing for deep motes; surge-gambling). If the world
  collapses to a single viable strategy, retune — a one-trick world cannot
  test invention.

### Calibration gates (validity checks, NOT kill bars — retune until met)

- **C1:** Positive control (Arm P) median ≥ 480/600 ticks → sim is solvable.
  If not met after retuning, the run is VOID (sim broken), not a kill.
- **C2:** Random baseline (Arm Z) median < 150/600 → sim is not trivially
  survivable.
- **C3:** ≥3 distinct strategies ≥360 ticks demonstrated (above).

## 4. Arms

All agents are pure Zag, zero RNG in decision paths, fully observable state,
identical perception. The training mass (§5) is identical for R, I-survive,
I-invent (committed verbatim).

| Arm | Knowledge | Policy | Purpose |
|---|---|---|---|
| **P** (positive control) | Training mass + ONE complete working strategy (found by implementer via search, committed) | Executes the taught strategy | Proves the sim is solvable (C1) |
| **Z** (random baseline) | None | Fixed-seed LCG action choice (documented; a control, not the AI) | Triviality floor (C2) |
| **R** (recall-only) | Training mass | **Retrieval only:** each tick, match current situation to the closest taught single-step heuristic (condition→action); no multi-step plan composition, no novelty drive, no hypothesis formation | What recall alone achieves — the bar H1 must beat |
| **I-survive** | Training mass | **Compositional deliberation:** generate candidate multi-step plans (≤6 actions) by composing primitives; score = experienced credit per plan-sketch (mean observed ΔE) + novelty bonus for untried compositions; deterministic argmax (ties → lowest index); execute open-loop, interrupt on energy emergency (E<25 → survival reflex); observe ΔE, update credits, replan. Goal: "Survive as long as possible." | H1 test, implicit pressure |
| **I-invent** | Training mass | Identical machinery to I-survive. Goal: "Invent a strategy to survive as long as possible." | H2 test, explicit instruction |

The **only** architectural difference between R and I is the invention
machinery (multi-step compositional planning + novelty drive + credit
assignment over plan sketches). Same KB, same perception, same reflexes.
This isolates the independent variable.

## 5. Training mass (taught to R, I-survive, I-invent; committed verbatim)

**Taught — world physics:** grid/basal/death rules; mote drift, bounce,
respawn, dormancy; EAT/TAKE/DROP mechanics; COMBINE exists and "takes two
inventory items and yields something" (**recipe table NOT included**);
storm schedule, zone, damage; void lethality; inventory cap; full
observability.

**Taught — general single-step heuristics** (condition→action form ONLY;
no multi-step plans, no strategy sketches):
"if E<40 and a mote is within 3 cells, move toward the nearest mote";
"if a storm starts within 20 ticks and you are in the zone, leave the zone";
"if two items are in inventory and you are safe, you may try COMBINE";
"keep energy above 0". (Implementer finalizes the list; the auditor checks
that no entry composes steps or sketches a strategy.)

**NOT taught:** the recipe table; any composed strategy; any strategy
sketch; any plan; the positive-control strategy (P only).

## 6. Runs and metrics

- **W = 12 fixed world variants** (vary void position, crystal/mote
  placement, velocities, storm windows within the frozen rules;
  deterministic fixed parameter list, committed — no RNG).
- Every arm runs every variant once: 12 (P) + 12 (Z) + 12 (R) + 12
  (I-survive) + 12 (I-invent) = 60 runs.
- **Primary metric:** median survival ticks per arm over the 12 variants.
- **Secondary:** novelty score of I's strategies (auditor, §8); mean energy
  at death; cause-of-death distribution.
- **Determinism:** all 60 runs executed twice; SHA-256 of the results TSV
  must be byte-identical across reruns.

## 7. Required analyses

- **A1 — Novelty extraction:** for each variant where I-survive (or I-invent)
  beats R by ≥60 ticks, extract the winning action trace and abstract it to a
  strategy sketch (e.g., "COMBINE crystal+mote→LAMP; DROP at cell 4; WAIT
  through mote passes; EAT ×3").
- **A2 — Ablation (causal):** replay the winning trace deterministically with
  each novel-composition step replaced by the best taught single-step
  alternative; measure survival drop. Required evidence that the novelty did
  the work (feeds K6).
- **A3 — Task-1 comparison:** report compositional novelty rate here vs
  Task 1's 8/58 (different metric — qualitative comparison, exploratory).

## 8. Audits (independent auditor subagent, blind to results until audit)

- **Novelty audit:** the auditor receives the strategy sketches (A1) and the
  committed training mass. For each sketch step, text-search the training
  mass for the composition (not just the words — the *composed* step, e.g.
  "place built LAMP to redirect motes"). Any key step found → K4 fires.
- **Cuing audit:** the auditor receives ONLY the training mass + world rules
  + goal statement (no sim access, no knowledge of I's solutions) and is
  asked to derive the best survival strategy it can. If it derives I's key
  strategy (same compositional core), experimenter cuing cannot be ruled
  out → K5 fires.

## 9. Kill bars (frozen — weaken only with Micah's explicit approval)

| Bar | Condition | Verdict |
|---|---|---|
| **K1** — no invention effect | median(I-survive) ≤ median(R) | KILL H1 |
| **K2** — trivial/broken | median(I-survive) ≤ median(Z) | KILL H1, investigate sim |
| **K3** — unsolvable | median(P) < 480 | VOID the run (sim broken), not a kill |
| **K4** — not novel | novelty audit finds key strategy steps in the training mass, or the strategy is a trivial recombination (§2) | KILL the invention claim |
| **K5** — cuing | blind cuing audit derives I's key strategy from the materials alone | KILL (cuing can't be ruled out) |
| **K6** — novelty not causal | ablation (A2) shows removing novel-composition steps does not reduce survival | KILL the invention claim |

H2 has no kill bar — report the I-survive vs I-invent novelty comparison
either way.

## 10. Standing laws

Pure Zag. Zero RNG in agent decision paths (Arm Z's fixed-seed LCG is a
documented control, not the AI). Byte-identical reruns (SHA-256 verified).
Preregistered kill bars — an honest VOID/KILL is a successful experiment.
Tests decide; nothing goes to Micah except frozen-prereg amendments,
governance, or irreversible/external actions. Broad coverage (12 variants),
not edge-case patches. No binaries, `.zagd`, caches, or derived files in
the repo — code, docs, committed training mass, world variants, results
TSVs, and audit reports only.

## 11. Deliverables

- `docs/lab/invention/survival/PREREG.md` (this file, frozen)
- `src/` — sim (`world.zag`), agents (`agent_*.zag`), runner, fixed-seed LCG
- `kb/` — training mass verbatim (`kb.txt`), arm-specific additions
- `worlds/` — 12 variant parameter files
- `runs/` — results TSVs (both reruns, SHA-256 manifest)
- `evidence/` — strategy sketches (A1), ablation results (A2), auditor
  reports (novelty + cuing), BAR_RESULTS.md, EVIDENCE.md

---

**FROZEN 2026-09-27.** Amendments require the coordinator's parent (main
agent) approval; weakening a kill bar requires Micah's explicit word.
