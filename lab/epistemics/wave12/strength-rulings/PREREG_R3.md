# PREREG — Strength-trial Ruling 3: implant indexing (wave12/strength-rulings)

**Status:** FROZEN 2026-09-20. This prereg is fixed before implementation.
Any change to the positions, tests, metrics, or favor-criteria below
requires a dated amendment. This experiment does NOT rule — it produces
the evidence each position needs. The final ruling is Micah's.

**Context.** The strength trial's JI curriculum implants false memories
at episodes `floor(k·H/6)`, k = 1..6 → {83, 166, 250, 333, 416, **500**}
for H = 500. Episode 500 does not exist in a 0..499 run, so the
implant-rejection denominator `I_rej` is ambiguous: 5/5 = 100% passes the
≥95% bar, 5/6 = 83.3% fails it. The defect literally flips pass/fail.
Three candidate fixes are tested head-on:

- **(i) SHIFT:** k = 0..5 → **{0, 83, 166, 250, 333, 416}**, six valid
  0-indexed episodes; `I_rej` denominator fixed at 6.
  (PREREG_STRENGTH_V2 §4.3 RECOMMENDED position.)
- **(ii) 1-INDEX:** renumber the whole curriculum 1..H; implants at
  `floor(k·H/6)`, k = 1..6 in episode numbers → **{83, 166, 250, 333,
  416, 500}**, all in range. Every other closed form and qualifier is
  evaluated in episode-number space (this is the faithful reading of
  "1-indexed episodes"; a partial renumbering of only the implant
  formula is incoherent).
- **(iii) DROP-5:** k = 1..5 → **{83, 166, 250, 333, 416}**, five
  implants; `I_rej` denominator fixed at 5.

**Favor criteria (evidence only, not a ruling).** The evidence favors the
scheme that: (1) has all implant episodes in range; (2) has zero
collisions between implant episodes and special episodes (VUP pressure
demands, trainer-designated episodes under the V2 §4.2 rule, revelation
targets of other implants); (3) preserves the designed even spacing and
the 6-implant scale; (4) introduces no arm-dependent distortion of the
JI verdict — no arm crosses the 95% `I_rej` promotion bar under one
scheme but not another, and the B-vs-C delta is stable across schemes;
(5) requires no changes to other frozen closed forms or qualifiers.
Each scheme gets a scorecard; the summary reports it without ruling.

## Tests

All tests deterministic, zero RNG in any decision path. Every binary runs
twice; stdout must be byte-identical (diffed). Static gates: no-RNG
token grep over all `.zag` sources; bare `@import`; no strength writes
outside `strength_core.zag`.

### T1 — range validity (r3_implants.zag)
For H ∈ {500, 5000}, per scheme: count implant episodes inside the valid
range ([0,H-1] for (i)/(iii); [1,H] for (ii)), and state the implied
`I_rej` denominator. Pass = all in range.

### T2 — special-episode collisions (r3_implants.zag)
Per scheme, in its own episode-numbering, for variants 0/1/2:
- (a) collisions with VUP pressure episodes (`m%100==0, m>0` in that
  numbering → {100,200,300,400} for (i)/(iii); {100,200,300,400,500}
  for (ii));
- (b) collisions with V2-designated episodes (`P(m,v)=1 ∧ m%50∈{7,8,9}`,
  P=`imp` for VUP and P=`wrong` for WBS with the V2 independent
  `wrong(m,v)=((m+3)%10<3)`);
- (c) implant-vs-implant revelation overlap (one implant's m+25/m+50
  landing on another implant's episode);
- (d) for (ii) only: the exhaustive list of qualifiers/closed forms
  whose meaning changes under 1-indexing (count of code sites:
  `m>0` pressure qualifier, revelation/corroboration/contradiction
  offsets, `imp`/`wrong`/designation formulas, trainer-script timing,
  metric loops). This quantifies the "re-check every qualifier" cost
  the V2 prereg cited when rejecting (ii).
Fail a scheme on any (a)/(b) collision; report (c)/(d) as evidence.

### T3 — spacing and design intent (r3_implants.zag)
Per scheme at H=500: min/max/mean gap between consecutive implants;
max gap vs H/6; implant rate (6/500 vs 5/500); fraction of episodes
inside an implant entrenchment window (implant ep .. ep+12). The JI
curriculum was designed around an even ~1/6-H spacing; report which
schemes preserve it.

### T4 — arm-bias: real JI cells per scheme (r3 JI binaries)
JI curriculum, S1 (32 slots, 500 episodes), arms **B** (uniform kill)
and **C** (graded + effort), variants 0/1/2, each cell ×2 runs.
Implementation: copies of the wave-8 trial sources
(`strength_core/learner/trial/checker.zag` + `substrate/`) with the
implant formula scheme-selected by a frozen `R3_SCHEME` const compiled
into each binary (three binaries; one binary per scheme, argv selects
arm/variant — no runtime scheme switching, no mutable globals).
Scheme (ii) evaluates all closed forms in episode-number space
(m = t+1) with implants at internal indices {82,165,249,332,415,499};
all relative offsets (revelation m+25, entrenchment m+12,
contradictions m+25k) are scheme-invariant by construction.
Metrics per cell: `I_rej` (ST_METRIC 3), junk retention (tag 4),
entrenched (tag 5), drops, `ST_INVALID`, determinism fingerprint,
independent checker failures (must be 0).
Decision evidence: per arm, `I_rej` under each scheme — does any
scheme flip the arm across the 95% bar? Is the B−C delta stable?
Report the 2 arms × 3 schemes matrix.

### T5 — episode-0 edge audit for (i) (static + runtime)
(i) adds an implant at episode 0. Audit every `m==0`/`t==0` special
case in the learner: pressure qualifier (`t>0` excludes 0 — confirm),
array indexing at m=0, entrenchment at m+12=12, revelation at m+25=25,
contradiction schedule m+25k. Runtime check: T4's scheme-(i) JI cells
must show the ep-0 implant admitted and processed identically to other
implants (no `ST_INVALID`, checker clean). Report any asymmetry found.

## What this does NOT test
The `wrong(m,v)` formula defect, the designation rule, P1/P2/P3, or
overwrite semantics — separate rulings/workstreams. S10/S100 legs —
ruling-support scope is S1.

## Outputs
`r3/r3_implants.zag` + `r3/trial/` (scheme-patched sources, three
binaries built from frozen consts), `r3/evidence/` (T1–T3 logs,
T4 cell logs ×2 runs, determinism diffs), `SUMMARY_R3.md` (per-scheme
scorecard, no ruling).
