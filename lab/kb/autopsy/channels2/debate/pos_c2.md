# DEBATER C2 — the transform-consistency probe is the program's pivot experiment

Position: **C2 should run first, now, on the frozen bytes — not because it will
deploy as a standalone channel (my prediction: it won't, on bits), but because
it is the cheapest experiment with the highest decision density on the table.
Its product is the F2 answer plus the per-task consistency map, and every
branch of its prereg decides what gets built next — including constraining C1's
design.** The other debaters and I agree on the run; we disagree on what the
numbers will mean. This paper fixes my meanings before the run, so none of
them can drift afterward.

## 1. Steelman: why C2 should work, and what it taps that the shootout couldn't

**The one move the data-processing inequality allows.** The shootout channels
were functions of the judgment stream J (plus perturbation-class metadata) —
re-summaries of the same adversarially generated judgment process. DPI says no
function of J recovers I(q;Y|J), the sub-boundary residual. C2 is not a
function of J(stim). It re-runs the frozen sense binary on transformed bytes
and reads J(T(stim)): a genuinely new measurement of the same underlying q,
carrying a fresh noise realization the judgment stream never contained. That
is the information the shootout channels couldn't tap — not a better summary,
a second reading.

**Parameter-free, against an adversary that never modeled T.** No fitted
thresholds, no calibration knobs for the adversary to have shaped. The law L
is a semantic fact of each task (flip the image, the comparison is unchanged;
reverse time, the glide flips), frozen before any adversarial fixture is
touched. The frozen adversary optimized J(stim) only. To falsely INSTALL, it
must be wrong twice, consistently, under a transform outside its model — a
strictly harder target than fooling one judgment.

**The adversary selects for fragility; C2 tests exactly fragility.** The
boundary band (δ ≲ σ) enriches the fooled population in marginal measurements
— judgments that crossed the boundary on a noise excursion. Those are
precisely the judgments a consistency probe catches: a second draw usually
lands on the other side. The adversary's construction is C2's mechanism, not
its obstacle.

**The upside the central case misses.** Native characterized the adversary
from gen.py as a pure boundary sampler — but the RENDERER that turns sampled
q into bytes may introduce T-asymmetric artifacts (onset transients in PCM,
spatial gradients in images) that the sense's boundary errors correlate with.
The shootout's (c) channel (two senses, same bytes) could never break those;
C2's transform scrambles them. If the fooling has any T-asymmetric component,
fooled judgments break under T far more often than independence predicts, and
C2's bits jump past the bar. This is a real, pre-registered upside case — the
run measures exactly how much of the fooling lives in T-asymmetric features.

**Cheapest pivot on the table.** Frozen bytes exist (2020 manifest entries,
SHAs spot-checked). The transforms are trivial byte manipulations. The sense
binary is already frozen. Pure Zag, zero RNG, byte-identical reruns. C2 runs
this week; C1 is a multi-week per-task build. Sequencing C1 before C2 reports
is paying the most expensive move before the cheapest measurement lands.

## 2. Prediction: which bar fires, with numbers

| Bar | My prediction | Number | Confidence |
|---|---|---|---|
| F3 calibration gate | PASSES, both senses | ≥95% on the 93 primaries | ~85% — the (T,L) pairs are task-covariant by construction; primaries are clean |
| F2 systematic-error | does NOT fire on the aggregate | P(consistent\|Y=0) ≈ 0.50–0.65 vs the 0.70 bar | ~60% — central estimate sits near the bar; see the confound below |
| F1 bits | FIRES | I(verdict;Y) ≈ 0.03–0.09 bits pooled vs the 0.15 bar | ~70% |
| F4 false-install | FIRES (moot after F1) | P(Y=0\|INSTALL) ≈ 0.20–0.30 | ~60% — an operating-point problem, not an information problem |

Reasons:

- **F1 fires because C2 is an agreement channel, and agreement channels on
  this adversary deliver ~0.08 bits.** Empirical anchor: shootout (c),
  multi-source agreement, measured 0.0797. C2's structure (same sense, two
  byte-versions) harvests the same two sources — band-tail robustness and the
  independent-draw dividend — which substantially overlap what (a)+(c)
  already drank. On band-center fixtures the two draws are near-coin-flips
  whose agreement is ~uninformative about Y; the bits live in the band-tail,
  which the champion already captured. Dead legs dilute the pooled statistic
  further (t5's single steady tone is nearly time-reversal-invariant; color
  tasks may be flip-invariant if the sense uses global color statistics).
- **F2 doesn't fire because the error is noise-driven** — native's own
  accounting (δ ≲ σ band, band-tail leakage, A/B dividend) says the adversary
  exploits measurement noise, not systematic bias. A noise-driven fool can't
  be wrong twice consistently under an unmodeled transform at 0.70 rates.
- **But the aggregate F2 is confounded, and this is my most important
  pre-registered caveat:** identity-L tasks (t1/t2/t3/t5) where the sense's
  features are T-invariant give P(consistent|Y=0) ≈ 1.0 *vacuously* — the
  probe can't move the judgment — which inflates the aggregate toward the
  0.70 bar on a technicality. (F3 catches vacuous+non-identity-L, since
  calibration would fail; vacuous+identity-L passes F3 silently — the hole
  Debater J independently identified.) My central 0.50–0.65 already bakes in
  partial vacuity; if t1–t3 are fully flip-invariant the aggregate can touch
  0.70 without the error being "systematic" in any sense that warrants
  retiring the family. Hence amendment A2 below — it must be frozen before
  the run, or F2's reading will be argued afterward instead of measured now.
- **Net: C2 does not deploy standalone.** Its value was never the standalone
  bits — it's the pivot measurement plus the per-task map.

## 3. What would falsify my position

I concede — specifically, in these terms:

1. **F2 fires cleanly on non-vacuous tasks** (per-task P(C) well below 1.0,
   P(consistent|Y=0) ≥ 0.70 on the aggregate over non-vacuous tasks): the
   error is systematic relative to every probe we can construct. I sign the
   family's retirement myself — including the "second reading" strategy
   (C3 dead on arrival) — and C1-class work becomes the only direction.
2. **F1 fires AND the combination analysis (amendment A1) shows C2 adds
   <0.03 incremental bits over the (a)+(c) champion:** the transform axis is
   redundant — C2 taps nothing the champion didn't already have. The run's
   only product is the F2 answer.
3. **F3 voids a sense:** the (T,L) table was mis-specified for that sense.
   Instrument failure, not theory failure; that sense's results are void as
   the prereg says.
4. **P(C) ≈ 1.0 overall, all tasks:** the transforms were vacuous — this run
   tested nothing. Kills the instance, not the idea.

What does **not** falsify me: F1 firing alone (predicted — the standalone bar
was never C2's value proposition); F4 firing alone (operating point,
retunable); an F2 aggregate ≥0.70 driven by vacuous tasks (instrument
artifact — amendment A2 exists precisely to separate this from the real
signal).

## 4. Attacks

### On C1 (stimulus-analytic verification) — its weakest points

- **"In principle" is doing all the work.** "A direct analytic measurement
  has the full bit in principle" assumes the hand-built analytic beats the
  frozen sense binary's measurement noise σ on the same δ-band. A
  hastily-built pitchdisc analytic with worse σ' than the frozen sense LOSES
  to the sense. C1 hasn't shown its six analytics beat the binaries they
  replace — it assumes direct = better. A second reading from the same
  binary (C2/C3) has KNOWN σ. The burden of σ'-vs-σ proof is on C1, and it
  is currently unmet.
- **The independence guarantee is asserted, not constructed.** An analytic
  you write is another deterministic function of the same bytes, by the same
  authors, from the same physics. Against the frozen boundary-sampler it
  wins — but so does C2's T, which the adversary equally never modeled.
  C1's advantage over C2 here is not principled; it's just a different
  unmodeled axis that costs six research projects instead of six byte
  transforms. Against the adaptive adversary, C1's fixed human-authored
  computation is the SOFTER target — inspectable, modelable, correlatable.
- **C1 needs C2's answer before it can be designed right.** If F2 fires
  (systematic), C1's analytic must use a *different measurement principle*
  than the sense, not a cleaner implementation of the same one. If F2 stays
  quiet (noise-driven), C1 is overkill for noise — you don't need a new
  instrument, you need a second reading. Either way C2 is upstream of C1.
  Building C1 before C2 reports is sequencing malpractice: the most
  expensive move on the table, justified by investigator agreement rather
  than measurement.
- **C1's own falsifier #3 admits the thesis might fail on the frozen bytes.**
  If an independent analytic can't beat 0.15 bits on bytes the generator
  built FROM q, then "the information is sitting in the bytes" is weaker
  than claimed — extractability-by-procedure is exactly what's at issue,
  and the task-built sense already fails at it near the boundary.

### On J (judgment-side family) — its weakest points

- **J's two predictions are in tension.** "F2 doesn't fire BECAUSE
  noise-driven" + "F1 doesn't fire BECAUSE fresh axis" can't both hold:
  under the noise-driven model, band-center consistency is agreement between
  two near-coin-flip draws — ~zero bits about Y. The bits live in the
  band-tail, which (a)+(c) already drank. A fresh question is not fresh
  information. J's deploy prediction needs the noise story for F2 and needs
  to forget it for F1.
- **"The cap is the adversary's, not the family's" is true and irrelevant.**
  We face THIS adversary; the bar is ~1 bit against it. A family whose
  ceiling is set by the adversary's δ parameter is a weather vane, not a
  repair program. (And if a looser band raised the cap, the SUSPECT gate
  wouldn't be failing at 41.3% in the first place.)
- **J concedes the substance while disputing the procedure.** F2-clean plus
  C3-failed equals family dead — J signs that. Our disagreement is
  governance (how much evidence before law), not substance. I grant J half
  the governance point: automatic permanent retirement on one aggregate
  number IS too strong — which is why amendment A2 (per-task, vacuous-task
  exclusion) exists. The issue isn't sample size needing replication; it's
  the vacuous-task confound needing a pre-registered rule. J should support
  A2 rather than demand a second battery.
- **J's "C2's weakest points" section helps my case more than his.** J shows
  a T-invariant systematic fool passes F3 and defeats C2 silently — then
  bets it won't materialize, on the noise-driven accounting. That bet is
  exactly what the run settles. We agree on the experiment; we disagree on
  the number; the prereg decides between us.

### On Sol (new-data-first) — brief

- **The premise was checked and wrong:** 2020 manifest-verified fixture
  bytes on this VM; "no raw signal" applied to the input tables, not the
  machine. Human verifiers and second sensors are the fallback AFTER
  frozen-byte channels fail — not the first move. Sequencing new data
  collection before C2/C3/C1 run on frozen bytes is paying the highest
  cost first.
- **Humans can't do byte-identical reruns.** A human-verifier channel is
  non-deterministic by construction — it violates the program's own
  discipline (frozen inputs, 2× reruns) that both investigators demanded.
  Keep Sol's candidates as the adaptive-adversary defense, where new,
  unmodelable measurement principles are genuinely required.

## 5. Two prereg amendments to freeze before the run

The outline is not yet frozen; these close the two holes the debate exposed:

- **A1 — score the stacking question.** Add I(champion_verdict, C2_verdict;
  Y) on TEST: does C2 add incremental bits over (a)+(c)? My prediction:
  +0.02–0.06 (largely overlapping sources). If it stacks past ~0.20
  combined, C2's value proposition changes from "diagnostic" to
  "complementary channel" even with F1 fired.
- **A2 — per-task F2 with a vacuous-task exclusion rule.** Report per-task
  P(C), P(C|Y=0), P(C|Y=1). Frozen interpretive rule: a task with P(C) ≥
  0.98 is declared VACUOUS (the probe cannot move the judgment); vacuous
  tasks are excluded from the aggregate F2. Rationale: including vacuous
  identity-L tasks biases F2 toward firing on a technicality; the
  permanent-retirement consequence must rest on the non-vacuous reading.

## Bottom line

Run C2 — not as the deployable, but as the pivot. It taps the one thing DPI
permits (a second measurement, not a better summary), it costs almost
nothing, and its branches decide the program: F2-clean → retire
judgment-side, build C1 with a design constraint; F1-without-F2 → agreement
channels exhausted, C3 next, C1 still owes its σ' proof; deploy (upside
case) → scale the methodology. No other proposed experiment compresses this
much decision into one frozen-binary rerun. The kill bars stay as written,
plus A1/A2 — and whatever they say, the reading rules are fixed now, not
after.
