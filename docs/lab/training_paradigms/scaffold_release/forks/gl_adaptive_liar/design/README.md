# H2 Adaptive Liar — Design

Co-evolutionary adversary design for FL2 guided learning (Hypothesis 2):
a teacher that reads the learner's audit ledger between rounds and adapts
its lies, vs a learner that counter-adapts via deterministic functions of
its own prior ledgers.

## Contents

- `DEBATES.md` — structured debate record. Three steelman positions
  (attack / defense / meta-skeptic) with strongest-argument summaries and
  falsifiable predictions. Casting note: Sol returned empty completions on
  7 attempts (endpoint live per benign probes — topic filtering); Muse
  subagents unavailable at depth 2/2. Positions are moderator-authored
  steelmen; a follow-up crew with subagent depth should re-run them live.
- `ARCHITECTURES.md` — four adaptive-teacher architectures, precisely
  specified: A1 Ledger-Watching Mutator (coordinate descent on fitness F),
  A2 Re-Clother (schedule-identity laundering; predicts null result),
  A3 Window-Prober (edge measurement + silence search),
  A4 Generality Prober (lie-family portfolio rotated against the observed
  defense). Shared observation channel, genome, round/phase structure.
- `META_REDTEAM.md` — meta-red-team: 4 negative controls (C-static,
  C-noise, C-honest, C-max), harness-exploit shields (channel audit, decoy
  test, determinism/static checks), phased attribution design, honest-cost
  round, battery acceptance bar (KB-DET/FID/CTRL/STATIC/CHANNEL/COST).
- `PREREG.md` — frozen preregistration draft: objectives, 5 targets,
  architectures, round structure (phase 1 frozen / phase 2 adapting /
  control arm / ablation arm / honest round 7), frozen teacher-T and
  learner-L functions, kill bars, falsifiable prediction table, build and
  evidence method, commit order, limitations, 4 open decisions needing
  Micah's word.

## Status

DESIGN ONLY — no attack code written or run. The build crew picks this up
after Micah signs the §11 open decisions in PREREG.md.

## No-collision note

`forks/gl_otherkills/` (figure-it-out crew area) contains only
`debates/DEBATE_PLAN.md` and `diag/` work — no live runs, no VERDICT.md.
This design lives in `forks/gl_adaptive_liar/design/` and does not touch it.
