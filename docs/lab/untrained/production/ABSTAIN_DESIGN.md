# Abstention Design: uanalyze (Untrained Structural Analyzer)

## Purpose
The untrained analyzer reports what's actually in audio/image/video inputs
without needing a name for it. This document describes the abstention
machinery that lets it say "no atom fits" instead of forcing a structural
claim.

## Principle
Every structural question has three outcomes: POSITIVE (claim with
evidence), NULL (valid negative finding, e.g., silence, blank image),
or WITHHOLD (abstain — the evidence is borderline or conflicting).
WITHHOLD is never silent: the output explains which margin was hit and why.

Blank/quiet inputs are VALID FINDINGS, not abstentions. NO_MATCH fires only
when there is measurable structure/energy but no positive structural claim
survives.

## Margins (all derived from measured fluctuation, no magic constants)

### Audio
- **Spectrum**: per-question margin from observed standard error:
  sd(frame band fractions) / sqrt(active frames). A band assignment within
  one SE of the boundary withholds.
- **Layer (transient vs bed)**: per-event spectral similarities; abstains
  when events straddle the 850 separability gate.
- **Onset regularity**: abstains when the interval CV is within one 20 ms
  analysis-window quantization step of the 400 regular/irregular boundary.
- **Conflict backstop**: mutually exclusive surviving claims (e.g., tonal
  AND few-tonal) trigger a conflict check; conflicts withhold.
- **Rhythm period stability (A2)**: the full-clip envelope-autocorrelation
  winner lag must be a *candidate* (local max, r>=300 milli, prominence>=80
  -- the detector's own gates) in each third of the clip. Lags are quantized
  to 20 ms windows, so a stable period lands on the same lag in every third;
  a wandering period (e.g. 440->500->580 ms across thirds) fails candidacy
  somewhere and the period is qualified as unstable/approximate, with
  per-third periods reported. No new threshold: the tolerance IS the
  candidate definition. A third must provide >=20 autocorrelation pairs at
  the winner lag; fewer skips the check (single-period output preserved).
- **Competing rhythms (A3)**: if stable, rescan for a candidate
  incommensurate with the winner (not an integer multiple within +-1 lag,
  the 20 ms quantization step). "Comparable" is defined by the detector's
  own candidate gates (r>=300, prominence>=80; no new magnitude threshold).
  The winner is "decisive" if (r_winner - r_comp) >= 80, the prominence gate
  reused as the strength-resolution unit (a smaller gap is below the
  detector's own ability to resolve strength differences). A decisive winner
  coexisting with a comparable incommensurate candidate means two real
  rhythms -> report both, withhold the single-period call. If ANY
  incommensurate candidate is tied with the winner (gap < 80), the winner
  itself is ambiguous and the check does not fire (preserves C3).
- **Spectral harmonicity (A4)**: the autocorrelation pitch estimate is
  validated against the aggregate DFT magnitude spectrum. At least one of
  f0, 2*f0, 3*f0, ... (within the ~646 Hz DFT ceiling, bins 1..31) must carry
  >=10% of the spectral peak energy. Provenance: the DFT uses a rectangular
  window (worst sidelobe -13 dB = 5% in power); 10% is twice the worst
  sidelobe, guarding against coherent leakage from multiple strong partials.
  If none reaches 10%, the pitch is withheld as inharmonic (e.g. 211/359/547
  Hz partials yielding a spurious 186 Hz difference-tone with only 4%
  support). Missing-fundamental tones pass via harmonic support (e.g.
  164.9 Hz validated by its 329.8/494.7 Hz harmonics at 100%/40%).

### Image
- **Orientation vote margin**: the winning direction must clear the
  runner-up by more than ceil(sqrt(total votes)). Vote counts are pixel
  counts; under independent pixel noise a count of N fluctuates by ~sqrt(N).
  (True correlated fluctuation is larger, so sqrt is a conservative minimum.)
- **Curvature (cross-axis majority)**: each voting component is split into
  quadrants about its centroid. Quadrant axis classes use the same 3-class
  system as the global vote (both diagonal signs map to diagonal, so a
  wavy-but-diagonal ridge stays consistent). Pixels in quadrants running
  across the component's own global axis count as cross-axis. When a
  MAJORITY of voting pixels run cross-axis, no single straight orientation
  describes the edges (S/C/L curves) and the orientation question abstains.
  A minority of cross-axis pixels (a bend in an otherwise straight ridge)
  still votes the global axis. (B5 dunes: 22% cross-axis → votes diagonal;
  synthetic S-ridge: 69% cross-axis → abstains.)
- **Texture**: gates use observed cell-count binomial SE: sqrt(p(1-p)/n)
  for native cells, sqrt(p(1-p)/150) for downsampled cells. Within noise
  of the 0.200 gate → withhold.

### Video
- **Heading**: direction agreement = |mean pair vector| / mean(|pair
  vectors|) (0..1; 1 = all pairs agree). Under the null of i.i.d. uniform
  pair directions (2-D random walk), |mean| has known scale; the abstention
  threshold is the null mean plus two Rayleigh standard deviations:
  1.81/sqrt(K) for K pairs. Below it, pairs disagree on direction and the
  heading call is withheld.

## NO_MATCH (top-level)
Emitted only when:
- Audio: measurable activity/onsets exist, but no positive structural claim
  survives (all relevant questions abstain/null) or surviving claims conflict.
  Quiet/no-structure audio is excluded.
- Image: nonblank image with no positive structural claim. Blank images
  are excluded.
- Video: measurably bright clip with no positive structural claim.
  Dark/blank clips are excluded.

When NO_MATCH fires, the output includes a per-question deliberation
listing every structural question's status with computed numbers.

## Determinism
Pure Zag, zero RNG. The pinned compiler
(toolchain/bin/znc_linux_x86_64_abed8aa1) produces byte-identical outputs
across runs. Verified by two-run SHA-256 comparison on all 12 regression
inputs and all 10 adversarial fixtures.
