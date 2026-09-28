# SENSES REMATCH — Preregistration amendment 2026-09-21/22

Amends `docs/lab/senses/rebuild/PREREG.md` (KB1–KB5 unchanged, recomputed per
budget). Micah's directive: approach B (human-style qualitative percepts) lost
round 1 (54.0% vs 72.6%, killed by KB1). Rematch at LONG HORIZON: does B
overtake A with 10–100× more training? His hypothesis: qualitative sensing
learns slower but deepens better with extended training, while raw values
plateau. Second hypothesis: B's robustness advantage (smallest adversarial
degradation in round 1: 8.3pp vs 20.9pp) GROWS with training.

## What "training" means (operationalization)

Both senses are fixed-algorithm binaries with hand-set decision thresholds
(documented design bets). "Training amount" = labeled primary-style fixtures
used to FIT those thresholds via the deterministic protocol below. No
architecture change, no vocabulary change (a data-grown vocabulary would be
B2 — explicitly out of scope; if B plateaus on resolution limits, that
belongs to B2, not this rematch).

## Budget ladder (per-task primary counts × multiplier)

Round-1 primary counts: t1 60, t2 40, t3 90, t4 60, t5 60, t6 60 (= 370).

| Budget | Multiplier | Training fixtures | Status |
|---|---|---|---|
| T0 | 0 | 0 (round-1 hand-tuned values, no fitting) | baseline = published 72.6 / 54.0 |
| T1 | 1× | 370 | required |
| T2 | 10× | 3,700 | required |
| T3 | 50× | 18,500 | required |
| T4 | 100× | 37,000 | best-effort |

Feasibility clause: the verdict is valid if T3 completes. Crossover is
adjudicated at the highest completed budget ≥ T3. If only ≤ T2 completes,
the rematch is INCONCLUSIVE (neither a B win nor a B kill) and must be rerun.

## Data discipline (seeds frozen here)

- TRAIN: new fixtures, MASTER_SEED = 20260922, same generator code, same
  per-task counts × multiplier, primary-style only. Photo pool: the FIXED
  170 cached photos reused (new seeds drive new crops/transforms).
- TEST-FRESH: 370 primary-style fixtures, MASTER_SEED = 20260923. NEVER
  touched during fitting. PRIMARY test set for KB6 and KB1–KB3.
- TEST-R1: round-1 primary fixtures (seed 20260921). Secondary only —
  designers saw these during round 1 (contaminated).
- ADV-R1: round-1 adversarial fixtures (185). Frozen robustness probe at
  every budget. NEVER in training.
- Noise/adversarial variants are NEVER training data.

## Fitting protocol (identical for both approaches, deterministic)

1. Run each binary ONCE per training fixture; collect (score-vector, truth).
   A scores come from existing `debug_vec` (no binary change). B color/pitch/
   shape scores come from emitted percept handles + the FROZEN relation tables
   reimplemented in Python (tables are compile-time constants documented in
   `b_percept/PERCEPT_DESIGN.md`; the Python copy is verified against the
   binary's own judgments at hand-tuned values before any fitting).
2. INSTRUMENTATION (B only, judgment path untouched): emit the three timbre
   per-mille features (crest, brightness, form factor) and the motion triple
   (changed-pixel count, dx, dy) as extra output lines. VALIDATION GATE: the
   instrumented B binary must reproduce round-1 judgments byte-identically
   on all 925 round-1 fixtures before any fitting. If not identical: fix, do
   not proceed.
3. Per (approach, task, budget): sweep the preregistered grid below on the
   training set; objective = training accuracy. Tie-break (deterministic):
   grid point closest to the round-1 hand-tuned value (absolute difference;
   multi-param: lexicographic on per-param distance in sweep order); residual
   tie → smallest grid index. Multi-param tasks: single coordinate sweep in
   the listed order, starting from hand-tuned values, no iteration.
4. Confidence rules are NOT fitted (they don't affect judgments; KB1–KB3 use
   judgments only). They stay frozen.

### Grids (hand-tuned value in parens; crew verifies against source and
### records any correction in CALIBRATION.md BEFORE fitting — no data peeking)

APPROACH A:
- colordisc: score dist (RGB units); grid {10,20,30,(40),50,60,80,100};
  dist ≤ t → SAME.
- colorconst: score dist (per-mille); grid {50,75,100,125,(150),175,200,250,300}.
- shapetrans: NO fittable decision threshold (nearest-prototype on ratio;
  prototypes are geometric truths). Lum mask threshold 382 stays fixed.
  Documented, not fitted.
- pitchdisc: score dppm; grid {5000,10000,15000,(20000),30000,50000};
  d < t → SAME.
- timbredisc: score r (per-mille centroid); coordinate sweep b1 (PURE/DARK)
  ∈ {1020,1040,1060,(1075),1100,1130}, b2 (DARK/RICH) ∈
  {1300,1350,(1400),1450,1500}, b3 (RICH/BRIGHT) ∈ {2600,2800,(3000),3200,3400}.
- motiondir: score mag (px); grid mag < t → STILL, t ∈ {1,2,(3),4,5}.
  Pixel-diff mask threshold 90 stays fixed (documented, not fitted).

APPROACH B:
- colordisc / colorconst: k = pc_color_dist(p1,p2) from frozen tables;
  grid k ∈ {0,(1),2,3,4}; dist ≤ k → SAME.
- pitchdisc: k = |bin1 − bin2|; grid k ∈ {(0),1,2,3}.
- shapetrans: vote rule grid: min axis-matches ∈ {2,3} × tie-break priority
  orders (crew defines the exact set from pc_shape_decide; hand behavior =
  current binary). Recorded in CALIBRATION.md before fitting.
- timbredisc: instrumented features (crest, bright, form); coordinate sweep
  crest ∈ {1000,1075,(1150),1225,1300} → RICH; bright ∈ {40,50,(60),70,80} →
  BRIGHT; form ∈ {1600,1700,(1780),1860,1950} → DARK; else PURE. Order fixed.
- motiondir: instrumented (mcount, dx, dy); still iff mcount < t,
  t ∈ {100,150,(200),250,300}; speed bands fixed.

## KB6 — long-horizon crossover (NEW, frozen decision rule)

Adjudicated on TEST-FRESH at the highest completed budget T* ≥ T3:

- CROSSOVER CONFIRMED iff (B_mean − A_mean) ≥ 2pp AND B_mean ≥ 60%.
  → B revived as a viable sense; KB1 kill lifted.
- Else → B STAYS DEAD. Report it straight, no rescue.

Also report descriptively per budget: means per task, learning curves
(accuracy vs training amount), each approach's plateau point (budget after
which |Δ| < 1pp), and whether curves crossed at any earlier budget.

## Robustness-at-scale (preregistered descriptive criterion, no kill bar)

At each budget: adversarial accuracy on ADV-R1; degradation
D = primary(TEST-FRESH) − adversarial(ADV-R1), per approach.
"B's robustness advantage grows" is SUPPORTED iff at T*:
D_B < D_A AND (D_A − D_B)(T*) > (D_A − D_B)(T0). Else NOT SUPPORTED.

## KB1–KB5 per budget

Recomputed at every budget on TEST-FRESH (KB1 viability, KB2 head-to-head
with the 2pp/2× tie rule, KB3 fragility on ADV-R1) and via the shared
memory rule from round-1 `score.py` (KB4 false-install ≤ 10%, fitted
judgment streams, all variants in fixed order). KB5: 3 reruns of the full
fitted pipeline byte-identical. Pure Zag binaries, zero RNG, deterministic
Python sweep.

## Deliverables

`docs/lab/senses/rematch/`: this amendment, CALIBRATION.md (grids as
recorded before fitting), instrumented B sources + rebuild log, training /
TEST-FRESH manifests (SHA256), per-budget run logs, learning-curve tables +
plots data, VERDICT.md (KB1–KB6, crossover decision, robustness verdict,
plateau report). Log to `~/workspace/NIGHT_RUN_2026-09-21.md`.
