# SLICE 07 — Variation at scale: Track 1's variation machinery at 1000x
Date: 2026-09-20. Track 6 (scale/duration to 1000x), slice 07. Investigator: wave11 swarm.
Depends on: TRACK1_SYNTHESIS.md (K1–K9, calibration bands, four projections, firewalls).

## 1. Slice
Track 1's variation machinery at 1000x: does state-dependent deterministic variation remain
adaptive (not degenerate, not arbitrary) at scale, with firewalls intact and replay byte-identical?

## 2. Falsifiable claim
Arm C calibrated at 1x — variation function, four projections, firewalls, and selector form
frozen; only calibration constants re-fittable per dated amendment — clears the Track 1
adaptivity gates at **every** scale leg (1x, 10x, 100x, 1000x): direction rate ≥0.60
(99.5% CI >0.50, ≥400 sampled pairs/leg), NMI ≥ max(0.30, 5×null) on held-out novel states,
diversity D strictly in (0.15, 0.6·D_cross), Spearman ρ ≥ 0.4 between variant distance and
state distance, replay byte-identical at every leg, per-episode audit ≤1.10× null bytes.
If any leg fails, the study must classify the failure as kill-Arm-C or re-parameterize —
no silent leg-skipping.

## 3. Design
Per-leg protocol (legs S1/S10/S100/S1000 episodes; Arm C vs null vs fenced Arm B at each leg):
(a) **Stratified adaptivity sample.** Exhaustive pair analysis is impossible at 1000x. Per leg,
sample ≥400 state pairs stratified: early/mid/late within-block, cross-block, and held-out
novel states never seen during 1x calibration. Run adaptivity harness (T1-10) and
arbitrariness detector (T1-11) on the sample only. Direction rate, NMI, D, ρ computed per leg.
(b) **State-entropy probe (the anti-explosion instrument).** The variation selector reads only
the four projections P(M), salience, budget, load (T1-01–04). Per leg, measure the effective
distinguishing entropy H of the selector input vector across episodes. Lawful prediction: H
grows sublinearly, never collapses. Known saturation risk: salience weights are capped in
[16,1000] from logical clocks (T1-02/04) — at 1000x most memories may pin at 1000, starving
the selector of distinguishing input. If H collapses, variation degenerates to cosmetic jitter
regardless of calibration. This probe runs BEFORE judging D: D-drift with intact H is
calibration; D-drift with collapsed H is structural starvation.
(c) **Calibration bands per leg.** D and D_cross are both measured per leg (D_cross must be
re-measured at 1000x — the RNG-equivalence upper bound may itself drift with scale; bands
computed against a stale D_cross are meaningless). Constants may be re-fit per leg only via
dated amendment; the selector form and projections stay frozen. One repair per failure total.
(d) **Replay at 1000x (the performance bar).** Full-state logging per episode is O(state×
episodes) and will break K8-cost and the 2^25-byte slice limit. Use checkpoint + append-only
delta state logging (consistent with MA1's append-only audit, committed on branch). Replay =
inputs + checkpoints + deltas, outputs byte-compared. Bar: zero mismatches; replay wall time
≤1.5× forward run; per-episode audit bytes ≤1.10× null arm. On mismatch, differential test:
replay a 100x subsegment — mismatch there too → implementation bug (repair); mismatch only at
full leg and localized to VARIATION_CHOICE entries → K1 fires on the concept.
(e) **NULL-fallback rate monitor.** Per T1-22, corrupted state degrades to deterministic NULL
variation. Corruption probability compounds over 1000x; track NULL-fallback rate per leg. A
rising NULL rate mimics degeneracy (boring phrasing) but is a harness problem, not a
variation failure — disambiguate before judging D.
(f) **K7 head-to-head at 1000x.** Fenced Arm B vs Arm C at the top leg, same as lower legs;
the scale study inherits K7 unchanged.

## 4. Kill bar
**Kills Arm C outright (concept dead, no repair):**
- Any firewall violation at 1000x absent at lower legs: ledger-byte divergence across variants,
  verdict divergence, or memory-op divergence under expression perturbation (K2/K3/K4 scaled) —
  variation is not quarantinable at scale.
- K1 replay mismatch at 1000x that the differential test localizes to the variation selector
  logic (not the checkpoint implementation).
- Adaptivity collapse at 1000x that survives one dated re-parameterization AND then also fails
  the gates at 10x/100x on retest — structural, not a calibration artifact.
**Sends back for re-parameterization (dated amendment, one repair, re-benchmark per
no-free-lunch):** D band drift with firewalls intact and H healthy; adaptivity dip at 1000x
only (passes ≤100x) with H collapsed → re-parameterize selector inputs (rank-normalized or
block-relative deltas instead of absolute capped weights) and rerun; replay cost overrun with
zero mismatches → implementation-level repair (checkpoint granularity), concept untouched.
If a re-parameterized build then fails at a lower leg it previously passed, the re-parameterization
itself is the defect — revert it, do not compound repairs.

## 5. Honesty notes
Sampling at 1000x means rare state configurations are missed; held-out novel states are sampled,
not enumerated, so a "passes at 1000x" verdict is a statistical claim with the stated CIs, not
a proof. D_cross drifting with scale makes the upper band (0.6·D_cross) partly self-referential —
both numerator and denominator move. The salience-cap saturation is the single most likely
degeneracy mechanism and was a judgment call in T1-04/21, not a derived constant. NULL-fallback
disambiguation assumes the corruption model is scale-invariant, which is untested. This study
does not cover deliberation-path variation beyond |H| ≤ 6 (T1-06 scope bound) — large
deliberation is still excluded from variation, at all legs.

## 6. Next build step
Build the scale harness (stratified sampler + state-entropy probe + NULL-fallback monitor) and
rehearse it at 100x against the existing RC3 corpus — the 100x leg is already proven ground, so
any harness bug shows up cheaply before anyone commits to the 1000x run. Do not start the 1000x
leg until the harness reproduces the known 100x Track 1 adaptivity results within the prereg CIs.
