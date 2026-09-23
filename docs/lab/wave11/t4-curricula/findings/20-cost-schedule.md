# Slice 20 — Curriculum cost and schedule (Track 4: teaching curricula)

## 1. Slice
Track 4, slice 20: program-management slice — episode budgets per curriculum per stage with
justification, audit/compute cost model (bytes per episode at 1x, projected at 10x/100x),
wall-clock schedule for the 10x integration trial, staffing (all agent-run), cost kill bars,
and the cut-order tradeoff under budget halving.

## 2. Falsifiable claim
The three curricula's 1x pilots establish the cost model (audit entries/episode, wall-clock
seconds/episode), and the full 10x program completes within the budgets in §3 with audit
growth per episode ≤4 KiB at 10x and zero replay divergence. If any curriculum's 10x leg
exceeds its audit byte budget by >2× or its wall-clock budget by >2×, that leg's design —
not the learner — is killed or re-preregistered smaller, and the English E5–E6 arm is the
first cut under a 50% budget reduction without degrading the full-system composite margin
by more than 1 control-sigma.

## 3. Design

**Episode budgets (per stage, with justification).**
- *Code* (slice 01 commits 3,950 at 1x; stage counts C1 100 … C12 300, ~350 adversarial):
  justified by the 95% byte-identical trace bar — each concept needs enough generator-unseen
  programs for overgeneralization to meet refutation; adversarial 350 is the minimum for
  K3 (≤1 of 10 variant kills per stage). 10x = 39,500; 100x = 395,000.
- *English* (proposed; slice 02 gives stages, not counts): E1 lexicon 800 (each binding needs
  deliberate add + disambiguating evidence; ≤1x exposures leave gavagai unresolved), E2 grammar
  600 (novel word-order parses), E3 pragmatics 400 (adversarial traps need volume to beat
  attractive misreadings), E4 canonical production 500 (50/50 round-trip bar needs 500 held
  meanings), E5 varied production 800 (100/100 zero-drift check over a palette), E6 composition
  300 (structural checks, the weakest bar, kept small deliberately). Total 3,400 at 1x; 34,000
  at 10x. E6 is the smallest because its metric is the least falsifiable.
- *Messy reality* (slice 03): 5 mess classes × 3 stages × 300 episodes = 4,500 curriculum +
  4,500 machinery-only control (the 15-point control gap is the whole falsification; the
  control costs exactly as much as the curriculum). Justification for 300: distinguishing a
  95% hold rate from 90% at 1% significance needs ~300 trials. 1x = 9,000; 10x = 90,000.
- *10x integration trial* (slice 19): 1x pilot 60 × 8 systems = 480 episode-runs; 10x full
  600 × 8 = 4,800 episode-runs (F + seven controls A–G). 10x program total ≈ 168,300 runs.

**Compute/ledger cost model.** Audit entry = 16 words = 64 bytes (entry layout: op@0 …
d2@60, committed convention). Per-episode logged ops at 1x (model, to be calibrated by the
pilots): ~1 deliberate memory op + 1 deliberation record + 1–3 post-change verifications +
0–5 trust-tier ops (MRC) + checkpoints = 8–24 entries → **nominal 1 KiB/episode, cap 4
KiB/episode** (matches slice 19's K6: >4× median audit growth is runaway logging). 1x program
≈ 16,350 episodes ≈ 16 MB audit. 10x: ≈168k × 1 KiB ≈ 170 MB nominal, 675 MB at the 4 KiB
cap. 100x code leg: 395,000 × 1 KiB ≈ 395 MB (≤2^25 slice limit per chunk — chunked replay
already validated). All numbers are model, not measured: the 1x pilot's first deliverable
is the measured entries/episode histogram, and the 10x budgets scale from the measured
median, not from this page. Storage is trivial; the load-bearing cost is replay-verification
CPU, which is linear in audit bytes.

**Wall-clock schedule (10x integration trial).** Precedent: wave5 ran 2,595 temptations at
10x and 100x inside one wave session; RC3 passed at 100x. Native Zag episodes are seconds,
not minutes — the binding constraint is agent build/compile/debug cycles, not CPU.
- 1x pilot (480 episode-runs + 16,350 pilot episodes): **1 agent-run session** (~24h,
  mostly harness build + first measured cost calibration).
- 10x integration trial (4,800 episode-runs): **1–2 sessions** (checkpoint harness from
  slice 19 must be green first; serial dependency).
- 10x curriculum legs (168k episode-runs): **2–4 sessions**, parallelizable across three
  curriculum-builder agents; the code 100x leg (395k) is gated until 10x kill bars clear.
- Full 10x program: **≈1–2 weeks wall clock, zero human-blocked time.**

**Staffing (Micah's autonomy default: "TNN does all").** 0 human FTE by design. One
coordinator agent + three curriculum-builder agents + one red-team agent (curriculum
integrity, slice 18). Humans appear only at the points Micah reserved: prereg approval,
phase-transition ratification (0→1 pure trainer gate; combination gates thereafter), and
force-pin — all audited. No staffing is proposed for episode running, grading, or replay
verification; those are mechanical and agent-run.

**Cost kill bar (when an arm becomes not worth it).** An arm is cut or re-preregistered if
ANY fires: (C1) audit bytes/episode at 10x > 2× its measured 1x median sustained over a
full leg — the model is wrong, shrink the arm; (C2) wall-clock > 2× the schedule budget
with kill bars still unevaluated — agent-loop thrash, fix the harness not the episodes;
(C3) an arm consumes >50% of the 10x episode budget while trailing its control margin
below the preregistered gap — paying for evidence you are not getting; (C4) any projected
100x/1000x leg exceeds 10 GB audit before its 10x kill bars are evaluated — scale is
evidence, not the goal.

**Tradeoff: the halving order.** Budget halves → cut English E5–E6 FIRST (saves ~11k
episodes at 10x, 32% of the English arm). Why: E5's varied production is Track 1's
jurisdiction wearing a Track 4 costume — expression variation belongs to state-variation,
not to teaching; E6's structural scoring is the weakest bar in the entire program (slice
02's own honesty note); E1–E4 already buy comprehension + canonical production, the load-
bearing linguistic goals. Second cut: MRC adversarial class 3 (fabrication consistent
with all observations) stage-3 — slice 03's honesty note concedes the accepted honest
limit (no architecture spots a perfect lie without records), so it is the lowest
information-per-dollar spend in the program. Keep at all costs: the full code curriculum
(cheapest per-check, byte-identical bars, exercises the substrate directly, load-bearing
for C11) and MRC contradiction/adversarial-stages-1–2 vs the machinery-only control (the
falsifiable gap lives there, per slice 03). 100x code leg is trimmed before any whole
curriculum dies — scale legs are expendable, curricula are not.

## 4. Kill bar
This slice's claim dies if: (K1) measured audit bytes/episode at 1x exceed 4 KiB for any
curriculum (the model above is falsified at the pilot); (K2) the 10x integration trial
fails to complete in 2 sessions with zero replay divergence (schedule model wrong);
(K3) after halving, cutting E5–E6 degrades the full-system composite margin by >1
control-sigma (the cut-order claim is wrong — E5–E6 was load-bearing after all);
(K4) any curriculum's 10x leg cost is dominated (>70%) by agent build/debug rather than
episode running — then the cost problem is a harness problem and the budgets are void.

## 5. Honesty notes
- The 1 KiB/episode nominal is a model from entry layout, not a measurement — no wave has
  published bytes-per-episode. The honest move is pilot-calibration, not defending this
  number; §3 says so explicitly.
- Wall-clock is dominated by agent loops, which I cannot predict from native binary speed;
  "1–2 weeks" is anchored on wave5/RC3 session throughput, not on a timing study.
- Cut-order rests on a judgment: English E5–E6 overlaps Track 1. If Track 1's slice 05
  (phrasing function) shows expression teaching is load-bearing for variation correctness,
  the cut order flips and MRC class-3 goes first.
- Not claiming these budgets are minimal — they are the maximum spend that still keeps the
  10x program inside one coherent wave; cheaper is fine if kill bars still resolve.

## 6. Next build step
Instrument the audit ledger to emit a per-episode entry/byte histogram FIRST, before any
curriculum 1x pilot runs: one native Zag counter module wired into the existing append-
only audit path, outputting (entries, bytes, op-class mix) per episode over 200 dry-run
episodes of each curriculum's harness. This is the most informative step because every
budget, schedule, and kill bar in this slice is downstream of one measured number —
without it the entire §3 is an educated guess, and with it the 10x budgets become
calibrated facts.
