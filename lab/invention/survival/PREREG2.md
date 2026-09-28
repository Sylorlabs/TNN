# PREREG2 — Experiment 1b: Recall Harm — Breadth and the Deliberative-Recall Fix (FROZEN 2026-09-27)

**Question:** Is reflexive recall-application broadly harmful to TNN — and can
a general architectural fix remove the harm without losing recall's help?

**Background (Experiment 1, committed 19f97c6cb):** In TIDELOCK, the
recall-only arm R scored median 160/600 — barely above the RANDOM arm Z at
143.5. A's ablation showed I's edge over R came partly from AVOIDING R's
harmful reflexive COMBINE (r_policy rule 5: "two items, safe, energy ok → may
try combine", applied with no evaluation of what the combine would yield or
cost). Recalled strategies, applied reflexively, were actively harmful: recall
barely beat chance. Micah's question: is this broad? And his order: test it
more, fix the architecture broadly, with TNN conscious every step of the way.

**Epistemic framing (standing):** This is the strategic counterpart of Micah's
standing epistemic worry (TNN taking everything as fact). The fix's law:
**TNN must not take every recalled strategy as applicable.** A recalled
strategy is a hypothesis about what to do, not a fact about what will work.

---

## 1. Hypotheses

- **H1 (breadth of harm):** Reflexive recall-application (match heuristic →
  execute, no evaluation) is harmful or near-useless across scenarios and
  domains — not a TIDELOCK artifact. In regimes where recalled heuristics no
  longer fit, R performs at or below chance.
- **H2 (broad fix):** Routing recalled strategies through explicit
  deliberation — recall proposes CANDIDATES, each evaluated against current
  evidence before any action — removes the harm while keeping recall's help,
  across all tested domains, with no per-scenario hardcodes.
- **H3 (content vs application):** The harm is in uncritical APPLICATION, not
  wrong CONTENT: the same KB applied reflexively harms, applied deliberatively
  helps. Tested via the R_true arm (regime-correct KB, reflexive application).

## 2. Operational definitions

- **Reflexive recall (R):** each decision, match the current situation to the
  closest KB heuristic (condition→action) and execute it. No evaluation of
  fit, no expected-effect check, no trace beyond the match.
- **Deliberative recall (D):** recall proposes candidates (heuristic, action,
  claimed effect, match basis). Each candidate passes a GENERIC evaluator:
  (a) precondition check — does the heuristic's stated precondition hold in
  the current observed state? (b) effect-expectation check — given the
  agent's own experienced effect model (built ONLY from this run's
  observations, never from regime knowledge), is the claimed effect plausible
  now? (c) conflict check — does a higher-priority candidate's evidence
  contradict this one? Then deterministic argmax over surviving candidates +
  primitive actions. Every step emits white-box trace lines.
- **Conscious every step:** each D decision emits, in order: RECALL lines
  (candidate id, source heuristic, what matched), EVAL lines (each check with
  its evidence: "precondition P: observed O → PASS/FAIL"), VERDICT line
  (chosen action + the deciding reason). The trace must CAUSALLY determine the
  action (proven by neuter test, §8) — it is the decision's audit trail, not
  commentary.
- **Harm:** in a shifted regime, median(R_home) ≤ median(Z) (at or below
  chance), or median(R_home) < 0.8 × median(R_true).
- **Fix gain:** median(D_home) − median(R_home) in shifted regimes; the fix
  "closes the gap" by [median(D)−median(R)] / [median(R_true)−median(R)].
- **Regime shift:** a change in the environment's causal structure that
  invalidates some taught heuristic's claimed effect, WITHOUT changing the
  KB. The KB stays the "home" KB everywhere; only the world shifts.

## 3. Domains (three; one shared deliberation module)

One file, `src/recall_delib.zag`, implements the deliberative-recall module.
ALL THREE domain agents import it. A fix that needs per-domain edits is not
broad (K4).

- **D1 — TIDELOCK v2 (continuity):** the TIDELOCK sim, RETUNED so the C3
  failure is fixed: the implementer MUST demonstrate ≥3 qualitatively
  distinct strategies each reaching ≥360 ticks (calibration gate C3; retune
  parameters freely — energy values, recipe costs, storm damage — until met;
  the point here is the recall question, not the world). 12 NEW world
  variants, disjoint from Experiment 1's. KB = home heuristics (same style as
  Experiment 1, committed verbatim). Shifted regimes: variants where a taught
  heuristic's premise breaks (e.g., a "combine when safe" heuristic when
  recipes in this variant punish blind combining; a "flee the zone" heuristic
  when leaving costs more than sheltering).
- **D2 — SHIFT (abstract regime-shift):** a per-tick decision domain with a
  feature-vector situation. KB holds condition→action heuristics with claimed
  effects, valid in the home regime. 12 variants: 6 home, 6 shifted (the
  shift flips which actions' claimed effects hold — e.g., "approach resource"
  becomes harmful when resources are bait; "hold position" becomes harmful
  when the ground degrades). Small, fast, fully observable, deterministic.
- **D3 — TOOL (tool-choice degradation):** KB teaches "use tool X for task
  type T" with claimed effects. 8 variants: tools degrade or break in some
  variants; the environment never announces it — the agent must notice from
  observed effects. Reflexive recall keeps using the degraded tool (harm);
  deliberative recall checks the tool's observed condition.

All domains: pure Zag, zero RNG in agent decision paths, byte-identical
reruns (SHA-256), fixed variant parameter lists committed.

## 4. Arms (per domain)

| Arm | KB | Policy | Purpose |
|---|---|---|---|
| **Z** | none | fixed-seed LCG (documented control) | chance floor |
| **P** | regime-correct | oracle/scripted best (proves solvable) | C1 |
| **R_home** | home KB | reflexive recall | the harm under test |
| **R_true** | regime-correct KB | reflexive recall | separates content from application (H3) |
| **D_home** | home KB | deliberative recall (shared module) | the fix under test (H2) |

In home regimes, R_true ≡ R_home (same KB). The informative comparisons are
in shifted regimes: R_home vs Z (harm), R_home vs R_true (content vs
application), D_home vs R_home (fix gain), D_home vs R_true (residual).

## 5. Calibration gates (validity; retune until met, else VOID the domain)

- **C1:** median(P) clearly above median(Z) in every domain (solvable,
  non-trivial).
- **C2:** determinism — every run twice, SHA-256 byte-identical.
- **C3 (D1 only):** ≥3 distinct strategies ≥360 ticks demonstrated by
  scripted search.

## 6. Required analyses

- **A1 — Harm taxonomy:** for each domain × regime: median(Z, P, R_home,
  R_true, D_home); R_home−Z gap (harm where negative); R_home−R_true gap;
  D_home−R_home gap; gap-closure fraction. Classify each shifted regime:
  recall HELPS (R_home ≥ R_true×0.95), NEUTRAL, HARMS (R_home ≤ Z or <
  0.8×R_true).
- **A2 — Content vs application:** if R_true >> R_home in shifted regimes,
  the harm is application (supports H3's framing); if R_true ≈ R_home, the
  harm is content (K6).
- **A3 — Neuter (causal) proof on D's traces:** (i) per-turn: replace each
  contested turn's EVAL lines with vacuous PASS and re-derive the decision
  from the trace — report the fraction of contested turns whose decision
  changes; (ii) whole-run: run D with the evaluator forced to always-accept
  (D_accept) — D_accept must regress toward R_home (gap-closure vs R_true
  must fall by ≥50%). If the traces don't causally determine decisions, the
  "consciousness" is decorative.
- **A4 — Held-out scenario family:** BEFORE the fix is implemented, freeze a
  sealed 4th shift family (one per D2/D3 style, committed sealed, SHA
  logged). Score D on it AFTER implementation. Generalization is measured,
  not asserted.

## 7. Audits (independent auditor, blind where noted)

- **Hardcode audit:** auditor inspects `recall_delib.zag` for
  scenario/domain-specific conditionals (any branch on domain identity,
  variant parameters, or regime labels). Any found → K4 fires.
- **Trace audit:** auditor replays D's decisions from committed traces only
  (no sim access): recompute each VERDICT from its RECALL+EVAL lines; any
  mismatch → the trace is not the decision's audit trail → K3 fires.

## 8. Kill bars (frozen)

| Bar | Condition | Verdict |
|---|---|---|
| **K1** — harm not broad | Reflexive-recall harm (R_home ≤ Z, or R_home < 0.8×R_true in shifted regimes) replicates in FEWER than 2 of the 3 domains | KILL H1 |
| **K2** — fix not general | D_home closes <50% of the R_home→R_true gap in shifted regimes in ANY domain | KILL H2 |
| **K3** — decorative consciousness | A3(i): <25% of contested turns change decision under EVAL-neuter, OR A3(ii): D_accept's gap-closure falls <50% vs D_home, OR trace audit finds VERDICT/trace mismatches | KILL the consciousness claim |
| **K4** — not broad (hardcodes) | Auditor finds scenario-specific conditionals in the shared module, OR D's held-out-family gap-closure <50% of its in-sample gap-closure | KILL H2 |
| **K5** — regression tax | In any home regime, median(D_home) < 0.9 × median(R_home) — deliberation must not cost more than it buys where recall was already right | KILL H2 (as a general fix) |
| **K6** — content, not application | In shifted regimes, median(R_true) ≈ median(R_home) (within 10% of R_true's home-regime level) — even correct content applied reflexively fails, so the harm is content after all | KILL the H3 framing |

An honest KILL/VOID on any bar is a successful experiment.

## 9. Standing laws

Pure Zag. Zero RNG in agent decision paths (Z's fixed-seed LCG is a
documented control). Byte-identical reruns, SHA-256 verified. Frozen kill
bars — weakening needs Micah's explicit word. Tests decide. Broad coverage,
not edge-case patches. No binaries, `.zagd`, caches, or derived files in
the repo. Keep scratch small (home disk is critically full — clean staging
dirs when done; never stage large files in /tmp).

## 10. Deliverables (docs/lab/invention/survival/)

- `PREREG2.md` (this file, frozen)
- `recall_fix/src/` — `recall_delib.zag` (the ONE shared module), domain
  sims/agents, runner
- `recall_fix/kb/` — home + regime-correct KBs verbatim, per domain
- `recall_fix/worlds/` — variant parameter files (incl. sealed held-out
  family, SHA-logged before fix implementation)
- `recall_fix/runs/` — results + traces TSVs, SHA-256 manifest (both reruns)
- `recall_fix/evidence/` — A1 harm taxonomy, A2, A3 neuter results, auditor
  reports (hardcode + trace), BAR_RESULTS2.md, EVIDENCE2.md

---

**FROZEN 2026-09-27.** Amendments require the coordinator's parent (main
agent) approval; weakening a kill bar requires Micah's explicit word.
