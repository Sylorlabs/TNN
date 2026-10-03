# Slice 11 — Arbitrariness Detector (Track 1: state-dependent deterministic variation)

## 1. Slice
Design the detector for ARBITRARY variation: the failure mode where a Track 1
mechanism's expression varies across episodes but tracks nothing in its internal
state — RNG-in-disguise, unlogged noise, or a bug. Mirror of the adaptivity metric.

## 2. Falsifiable claim
A mechanism claiming output = f(input, full internal state) exhibits arbitrary
variation iff, with input fixed and replay-determinism holding, no preregistered
compressible mapping from the enumerated full state predicts its expression
choices above the best-constant baseline. If the detector fires, the mechanism is
killed — its variation is noise, not state-dependence.

## 3. Design
Three gates, run in order, all deterministic, zero RNG. Per Track 1 rules the
state variables are preregistered and enumerated; full state is logged per episode.

**Expression codebook (preregistered BEFORE the run):** each episode's output is
reduced to a categorical expression code E over the MAY-vary surface only —
phrasing-template id, path-branch id, ordering signature, elaboration level.
MUST-NOT-vary fields (verdicts, memory kill/pin/promote, integrity refusals,
ledger contents) are excluded by construction; any run that varies them is
rejected before the detector runs. The codebook is frozen pre-run so the builder
cannot inflate classes after the fact.

**Gate 0 — replay determinism (logical).** For each of N episodes, replay
(input, logged full state) and require byte-identical output, expression
included. Any mismatch on any episode → unlogged influence (clock, hidden
counter, thread race) → declare ARBITRARY, kill immediately.

**Gate 1 — variation existence (logical).** With input fixed: require ≥4 distinct
expression codes, each ≥5% of episodes. Fewer → INCONCLUSIVE (no variation to
judge; not a pass, builder must widen the expression surface).

**Gate 2 — state-dependence (statistical).** Deterministic even/odd episode
split (fit/eval). Preregistered predictor family H, all deterministic:
(a) best-constant (majority class on fit set) — the chance baseline;
(b) per-variable bucketed rules (each enumerated state variable, ≤8 buckets);
(c) k-NN, k=15, on the normalized enumerated state vector;
(d) decision lists, depth ≤3, over enumerated state variables.
The mechanism's builder may nominate ONE additional deterministic predictor into
H before the trial (frozen at prereg). Select by fit-set accuracy (ties broken
toward simpler). Evaluate the winner on the eval split.

**Controls (both required for a valid detector run):** positive — a mechanism
with a known simple state→expression law (e.g. expression tracks the
deliberation-depth counter) must pass all gates; negative — a fenced arm whose
expression is a hash of state (deterministic, replay-clean, incompressible) must
trip Gate 2. If either control misbehaves, the detector run is invalid, not the
mechanism.

Zag-flavored pseudocode:
```
fn detect(episodes: []Episode, H: []Predictor) -> Verdict {
    for e in episodes { if replay(e.input, e.state) != e.output { return ARBITRARY; } } // G0
    let codes = codebook(e.output for e in episodes);                                   // G1
    if distinct(codes) < 4 or any class < 5% { return INCONCLUSIVE; }
    let (fit, eval) = even_odd_split(episodes);
    let best = argmax_fit_accuracy(H, fit);                                             // G2
    let acc = accuracy(best, eval); let p0 = best_constant_rate(fit);
    if binom_pval(acc, n_eval, p0) < 0.01 and (acc - p0) >= 0.10 { return LAWFUL; }
    return ARBITRARY;
}
```

**Sample size:** N=600 episodes per fixed input (300 fit / 300 eval), 3 distinct
fixed inputs → 1800 episodes per mechanism. At p0=0.25 (4 balanced classes) the
bar resolves to ≈35% eval accuracy vs 25% baseline (p<0.01 one-sided, lift ≥10pp).

## 4. Kill bar
The mechanism under test is killed iff ANY of: (i) Gate 0 fires on ≥1 of 1800
episodes (replay divergence); (ii) Gate 1 passes and Gate 2's winning predictor
fails to beat best-constant by ≥10pp at p<0.01 on the eval split, on ≥2 of the 3
fixed inputs. Single-input failure is flagged for re-test, not a kill. Both
controls must behave or the run is void.

## 5. Honesty notes
- This detector tests *dependence on state*, not *meaningfulness* of dependence.
  A degenerate law (expression = logged-counter mod K) passes Gate 2 — it IS a
  function of state. Vacuous-but-state-dependent laws are the adaptivity metric's
  jurisdiction (mirror slice), not this detector's. The boundary is deliberate.
- H is preregistered and finite: a lawful mapping too exotic for H (high-order
  interaction k-NN and depth-3 lists miss) false-positives as arbitrary. The
  builder-nominated predictor slot is the mitigation; residual risk is real and
  must be reported with any kill.
- The codebook is a judgment call made before the run. A hostile codebook can
  hide variation (over-coarse) or manufacture it (over-fine). Codebook and its
  builder-independence rationale are part of the prereg.
- Gate 0 catches unlogged variables only if they move output between record and
  replay. A deterministic unlogged constant (same at record and replay) is
  invisible — the enumerated-state completeness assumption is load-bearing.
- p<0.01 with a 10pp lift requirement (not p-value alone) guards against
  declaring trivially small effects "lawful"; conversely a truly adaptive but
  weakly-expressed dependence may die here — that is the intended strictness.

## 6. Next build step
Build the detector harness itself in native Zag FIRST, against a synthetic pair:
(a) positive-control mechanism with a known planted state→expression law, and
(b) negative-control hash-of-state arm. Ship the detector only after it passes
(a) through all gates and kills (b) at Gate 2 — calibrate the instrument before
aiming it at any real Track 1 mechanism.
