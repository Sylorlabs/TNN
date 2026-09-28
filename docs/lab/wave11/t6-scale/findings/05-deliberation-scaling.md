# Track 6, Slice 05 — Deliberation Scaling to 1000x

## 1. Slice
Deliberation at 1000x: does eliminative logic hold as |H| grows past the |H|≤6
enumerability bound (t1-state-variation/findings/06-path-selection.md), does the
B=4|H|² step-budget formula hold at 100x/1000x, and how often does the index-0
timeout fallback fire at scale — and is frequent fallback a failure?

## 2. Falsifiable claim
**Claim:** Deliberation quality is constant across scale legs at fixed |H|=6, and
for growing |H| the B=4|H|² budget buys a graceful, predictable degradation curve
rather than a collapse. Precisely: on legs 1x/10x/100x/1000x (12/120/1200/12000
episodes, slice 02), at fixed |H|=6, the per-window standards-compliance rate and
fallback fire rate are leg-independent within measurement noise; the |H|≤6 bound
is an implementation limit (worst-case partition cost), not a fundamental one,
because eliminative logic with the B=4|H|² budget remains verdict-correct at
|H|=12, 24, 48 with fallback rate fitting fallback(|H|) ≤ k·|H|³ (predictable
graceful curve), not a cliff.

## 3. Design
**Two-arm study, both native Zag, deterministic, zero RNG.**

**Arm A — leg constancy at fixed |H|=6.** The existing eliminator (hypotheses die
by evidence, never by vote; B=4|H|² elimination attempts per path) runs the
developmental curriculum + deliberative-standards battery (wave5/6 instruments,
137/137 baseline) at each leg. Windowed (W=100 episodes, slice 02) per-leg series
for: (a) standards-compliance rate, (b) mean verification steps per verdict,
(c) index-0 fallback fire rate, (d) verdict-correct rate on the trapped battery.
Constancy = all four metrics' leg means within the 99% CI of the 100x-leg mean
once W≥10 windows exist (10x leg contributes 1–2 windows; it is a sanity anchor,
not the comparator — 100x is the baseline comparator).

**Arm B — growing |H| sweep.** At the 100x leg (cost control: one leg, 1200
episodes), sweep |H| ∈ {6, 12, 24, 48} with a preregistered eliminative-demand
ladder (each |H| gets traps requiring genuine multi-hypothesis elimination, not
padded dummies — padded hypotheses would fake the curve). Measure: budget
consumption vs B=4|H|² (does the quadratic formula hold empirically, or does real
consumption grow faster?), fallback fire rate per |H|, verdict-correct rate per
|H|. One confirmatory 1000x run at the largest |H| whose 100x verdict-correct rate
stayed ≥99.0% (if any; otherwise the sweep itself is the finding and 1000x runs
at |H|=6). Budget consumption is logged per episode in the 16-word audit ledger
(stage field flags fallback episodes; d1=attempts used, d2=budget), so the whole
curve is extractable by the pure analysis pass of slice 02 — no new probes.

```zag
// Prereg constants
const B_PER_H2: i64 = 4;          // budget formula under test: B = 4*|H|^2
const FALLBACK_IDX: i64 = 0;      // index-0 fallback: valid linear extension by construction

fn eliminate(hs: []Hyp, budget: i64, ledger: *Ledger, ep: i64) -> Verdict {
    let used: i64 = 0;
    while used < budget && !partition_complete(hs) {
        elim_step(hs);             // one evidence-driven elimination; deterministic order
        used += 1;
    }
    ledger_fallback(ledger, ep, used, budget, used >= budget);
    if used >= budget { return verdict_from(hs[FALLBACK_IDX]); } // logged, cannot recurse
    return verdict_from(winner(hs));
}
```
**Fallback semantics under test:** fallback firing is *not* verdict failure — it
is the bounded, logged, deterministic terminator (index 0 provably terminates).
The study measures whether fallback rate rises gracefully (predictable curve) or
explodes (budget formula broken → cliff). Frequent fallback is a *degradation
signal*, not an integrity violation: K-bars distinguish the two.

## 4. Kill bar
Preregistered; any one fires → the scaling claim is dead (narrowed kill recorded):
- **K1 (leg non-constancy):** at fixed |H|=6, any leg's standards-compliance or
  verdict-correct rate falls outside the 100x-leg 99% CI (W≥10 windows) → KILL
  constancy claim; the breaking leg is named.
- **K2 (budget-formula break):** median budget consumption at any swept |H|
  exceeds 2× the 4|H|² prediction (i.e. consumption grows super-quadratically)
  → KILL the formula as a scaling law; it is a small-|H| fit, not a bound.
- **K3 (cliff, not curve):** fallback fire rate across |H|∈{6,12,24,48} fails a
  ≤k·|H|³ fit (chi-square rejects at 99%, and the |H|=24→48 step shows a
  discontinuity: rate jump ≥5× with no fit through it) → KILL graceful-degradation
  claim; the bound is effectively fundamental at the cliff point.
- **K4 (verdict collapse):** verdict-correct rate <99.0% at any swept |H| at 100x
  → no 1000x run at that |H|; if it fails already at |H|=12 → KILL the
  "implementation limit, not fundamental" claim.
- **K5 (replay break):** any episode's fallback episode fails byte-identical
  replay from logged full state → KILL the study run (void), not the claim —
  rerun after infra fix per slice 02 checkpoint rules.
- **K6 (honest negative):** if fallback fire rate at 1000x/|H|=6 exceeds 1% of
  episodes → frequent fallback is *flagged as a wear signal* and the bound is
  re-characterized; it does not kill integrity (fallback is logged and
  verdict-preserving by K4's complement: verdict-correct must still hold ≥99.5%).

## 5. Honesty notes
- **Weakest point: the demand ladder.** If the |H|=24/48 traps don't genuinely
  need more elimination work, the curve is fake — I will look efficient at scale
  for free. The ladder must be validated *before* the sweep (pilot: experts verify
  each trap's minimal elimination count) or Arm B proves nothing.
- The |H|³ fit in K3 is a guess dressed as a criterion: a genuine graceful curve
  could be exponential-with-small-base. The honest test is *predictability*
  (fit holds across the four |H| points), not the specific exponent — the prereg
  should fix the family (polynomial degree ≤3 OR exponential) before building, not
  after seeing data.
- **I am NOT claiming** deliberation *quality* improves at scale — only that it
  does not degrade at fixed |H| and degrades predictably for growing |H|.
  I am NOT claiming fallback-heavy verdicts are as trustworthy as clean ones;
  they are verdict-correct per the battery, which is a weaker statement.
- Sensor-spoofing (the accepted hole) is out of scope here: the curve is measured
  on unspoofed evidence; spoofed runs would confound elimination cost with
  evidence volume.
- 12000 episodes at |H|=48 is the wall-clock risk of the wave; Arm B's 100x sweep
  gates the single 1000x confirmatory run — no 1000x at |H|=48 without passing
  K4 at 100x first.

## 6. Next build step
Build the ledger-side fallback/cost extractor (stage flag + d1/d2 fields per
§3) and run it over an existing 100x ledger (RC3/wave5-6 artifacts, branch
tnn-native-lab) to get the |H|=6 baseline curve *before* writing the sweep —
if the extractor can't reproduce the known 137/137 / zero-fallback expectations
on committed data, the measurement pipeline is broken and the scale legs must
not start.
