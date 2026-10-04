# PREREG: COGOPS-PLEN-GRANULARITY

Frozen 2026-10-03. This prereg strictly precedes implementation
(commit-order self-check applies). Non-ledger task (claim minting
paused). Lane:
`docs/lab/research-lead/overnight-20260928/cogops_plen_granularity/`,
branch `tnn-native-lab`.

## Question

COGOPS-ADAPTIVEPLEN-RNG (commit 6daff87c5, verdict INCOMPLETE
negative) found the plen coefficient behaviorally inert: plen=1 vs
plen=3 produced byte-identical revise-search trajectories in 8/8
matched-RNG pairs. Mechanism: plen reaches behavior only through the
composite-fitness ordering `fit = raw - plen*len`; with quantized
replay tiers ({0,100,150,400,1000} per snapshot, averaged over at
most 8 snapshots), raw differences dominated the length penalty
(max swing (3-1)*15 = 30), so zero selection decisions flipped.
Its report explicitly proposed the follow-up tested here: "finer
replay granularity ... so the plen coefficient can actually flip
selections."

This lane tests: (1) whether finer replay granularity makes the
plen coefficient behaviorally relevant (flips selection decisions,
diverges trajectories); (2) what granularity is needed for flips;
(3) whether that rescues the adaptive-PLEN concept or shows plen
is the wrong pressure mechanism at any granularity.

## Design

`gran.zag` reuses the matched-RNG revise driver of
`cogops_adaptiveplen_rng/rng.zag` (same 8 pair seeds, same seed
body, same 40-episode setup, same RNG record/match protocol, same
30-generation revise, same adopt rule `best > cur+150`, same 850
raw passer bar) with three additions:

1. `replay_mode` in learner cell 2402: a researcher-owned
   experimental factor (not a cognitive mode), set by the driver
   before setup. Values 0, 1, 2 select the replay scorer.
2. Counterfactual flip diagnostic in `pop_is_better` and
   `off_beats_pop` (pmode>0 branches only): each selection
   comparison additionally computes the boolean outcome under
   explicit plen=1 and explicit plen=3 (replicating the age
   tiebreak), counting disagreements in cell 2403 and total
   comparisons in cell 2404. Pure reads plus writes to fresh
   cells: reporting only, zero behavioral effect.
3. Adaptive arm (plenmode 4): pmode 3 with cell 2370 = 0, so the
   learner-owned `plen_adapt` thermostat is live during revise
   (the true adaptive revise state, not the plen=1 proxy).

### The three scorers (per snapshot, integer, generic: no etype,
### wiring, or answer named)

Let `a` = 1 if any register holds the true answer value and that
value is not among the body's own SET immediates (else 0);
`n` = count of registers (0..8) holding valid node ids not among
the body's own SET immediates; `st==2` = body yielded.

- g=0 (quantized, CONTROL, byte-exact copy of rng.zag
  `graded_replay`): exact (st==2 and ans==tru) -> 1000;
  else a -> 400; else n>0 -> 150; else st==2 -> 100; else 0.
  Per-snapshot resolution 50; averaged over <=8 snapshots
  approximately 6-point (plus integer-division irregularity,
  already present in the RNG lane).
- g=1 (medium): exact -> 1000; else a -> 400+25*n (400..600);
  else n>0 -> 150+25*(n-1) (150..325); else st==2 -> 100;
  else 0. Per-snapshot step 25, i.e. a strict refinement of
  g=0: no strict g=0 ordering is ever reversed (min a-case 400
  > max n-case 325 > 100 > 0; ties at 400/150 split by n).
- g=2 (fine): g=1 plus near-miss credit
  `near = max(0, 24 - min_r |v_r - tru|)`, 1-point resolution
  (i32-safe saturating abs, no i64 casts), total capped at 999
  so exact 1000 stays unique. Since near <= 24 < 25 (the g=1
  step), g=2 strictly refines g=1: no strict g=1 ordering is
  ever reversed. Per-snapshot 1-point resolution; averaged
  approximately 0.125-point.

Ordering chain: g=0 < g=1 < g=2 are successive strict
refinements. g=2 additionally introduces near-miss partial
credit (a shaping change, not pure granularity); the
dose-response bar GF3 discriminates granularity-driven from
shaping-driven biting. Absolute replay values shift across
g (expected); every comparison is within-granularity.

### Flip arithmetic (plen=1 vs plen=3)

For members x,y with Dlen = len_x - len_y > 0 and
Draw = raw_x - raw_y: P1 prefers x iff Draw > Dlen; P3 prefers
x iff Draw > 3*Dlen. The orderings disagree iff
Dlen < Draw < 3*Dlen (symmetric for Dlen < 0). Approximate
minimum averaged-resolution needed: g=0 needs Dlen >= 3
(Draw = 6.25 in (3,9)); g=1 needs Dlen >= 2 (3.125 in (2,6));
g=2 needs Dlen >= 1. Arithmetic possibility is necessary, not
sufficient: the empirical flip counts decide.

### Arms

Per granularity g in {0,1,2}, per pair k in 0..7 (same
`pair_env_seed`/`pair_learn_seed` as the RNG lane):
- P1 (plenmode 1): pmode 3, cell 2370 = 1; records RNG state.
- P3 (plenmode 3): pmode 2 (fixed plen 3); RNG-match checked.
- PADAPT (plenmode 4): pmode 3, cell 2370 = 0 (plen_adapt
  live); RNG-match checked.
72 revise searches per binary run. Expected RNG-MATCH: 48/48
(P3 + PADAPT x 8 pairs x 3 g); graded_replay consumes no RNG,
so replay_mode cannot break the match.

### Reporting (per arm)

`REVISE-RESULT` (trials, best, adopted), per-generation `GEN`
(sumlen, bestraw, fixcount; `g=` stays the generation index,
granularity is the new `rg=` field), `FLIP` (flips, comps,
plenend), `PLEN-ADJ` lines when the thermostat fires,
`SEEDCUR` (cur, ns). Trajectory divergence is assessed by
shell diff of GEN sequences (analysis only, same as the RNG
lane); flip counts are computed in-Zag.

## Frozen kill bars

- GF1 REPLICATION (control): at g=0, P1 vs P3 GEN-trajectories
  byte-identical in >=7/8 pairs AND flips = 0 in >=7/8 pairs
  AND the g=0 GEN sequences byte-match the RNG lane's
  published GEN sequences (commit 6daff87c5 rng_run1.txt) in
  16/16 arms (P1+P3 x 8 pairs). Validates the port changed
  nothing behaviorally.
- GF2 BITES: at g=2, flip count > 0 in >=6/8 pairs (P1 or P3
  arm). Primary test of "pressure bites".
- GF3 DOSE-RESPONSE: per-pair total flips monotone
  f(g=0) <= f(g=1) <= f(g=2) in >=6/8 pairs, with strict
  f(g=2) > f(g=0) in >=4/8 pairs. Answers "what granularity
  is needed".
- GF4 ADAPTIVE EFFECT: at g=2, PADAPT vs P3 GEN-trajectories
  byte-differ in >=4/8 pairs. Informative (not bar-driving):
  PLEN-ADJ fire count, and mean revise-cost ratio
  cost(PADAPT)/cost(P3) at g=2.
- GF5 DETERMINISM: 3/3 byte-identical runs (sha256 recorded,
  cmp-checked).
- GF6 GUARDS: build.sh enforces safebin-only PATH,
  python3/python do not resolve, no `python` token, no
  `as *i32`, no `_MODE`, opcode dispatch exactly 1..8, no
  `while.*!(`, exactly one `fn main(`.

## Predictions (not bars)

GF1 PASS 8/8 (port is verbatim machinery). GF2 PASS (flips
appear at g=2 in most pairs). GF3 PASS (monotone). GF4
uncertain, lean PASS (0->1 vs 3 is a larger coefficient gap
than 1 vs 3). Revise-cost effect of adaptive under fine
replay: no directional prediction; reported honestly.

## Verdict mapping (frozen)

- GF1 FAIL -> INCOMPLETE (driver/port broken; no inference
  licensed).
- GF1 PASS, GF2 FAIL -> INCOMPLETE (negative): plen is inert
  even at 1-point replay resolution. The "make pressure bite
  via granularity" hypothesis is retired; plen is the wrong
  pressure mechanism regardless of replay granularity.
- GF1+GF2 PASS, GF3 FAIL -> INCOMPLETE (partial): pressure
  bites only at g=2, implicating the near-miss shaping rather
  than granularity per se; granularity alone does not rescue
  plen.
- GF1+GF2+GF3 PASS, GF4 FAIL -> INCOMPLETE (negative for the
  adaptive concept): the plen coefficient is behaviorally
  live under fine replay, but the learner-owned ramp shows no
  treatment effect in revise; adaptive PLEN not rescued.
- ALL PASS -> COMPLETE (mechanism confirmed): finer
  granularity makes plen pressure bite and the adaptive ramp
  shows a treatment effect. "Rescue as optimizer" is then
  decided by the informative cost ratio: rescued iff
  mean cost(PADAPT) <= mean cost(P3) at g=2, reported either
  way with no bar moved.

## Honesty notes (preregistered)

- g=2 adds near-miss partial credit; it is not a pure
  granularity manipulation. GF3 exists to separate the two
  explanations.
- Absolute replay values (cur, bestraw) shift across g; all
  treatment comparisons are within-granularity.
- The flip diagnostic counts counterfactual disagreements;
  flips without trajectory divergence are possible and will
  be reported as such (biting at the decision level vs the
  trajectory level).
- If adaptive never fires PLEN-ADJ in revise, the PADAPT arm
  is effectively plen-0-fixed; that outcome is reported as a
  finding about the thermostat's revise-phase dormancy, not
  silently reinterpreted.
