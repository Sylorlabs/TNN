# REDTEAM_SELF - SA1 (knowledge vs architecture)

Wave: wave-20261002-0521pdt. Lane: SENSORY (audio).
Self red-team of the SA1 BUILD-FAIL verdict. Every anomaly below was
investigated, not dropped.

## R1 harmonic-leakage hypothesis

Status: NOT TRIGGERED (NEVT = 0, nothing to leak). The deeper finding
is worse than leakage: the harmonic prediction itself is near-zero.
Checker-measured harmonic RMS: child 84.82, speech 171.26 (vs signal
RMS 1928.28 / 3125.98). The phase-locked mean washed out because no
single period fits 5 s of drifting pitch. Had the gates been looser,
any "events" would have been raw signal peaks, i.e. the exact failure
mode the prereg's anti-leakage gates were built to prevent. The gates
worked; the model did not. KNOWLEDGE: a global period is not a valid
harmonic model for 5 s of natural speech. ARCHITECTURE: the frozen SA1
design bakes in global stationarity.

## R2 old-failure signature (~170x)

Status: VACUOUS (no events). The signature is absent because nothing
was emitted. Note for SA1b: the max-attenuation discipline (events
bounded by source peak P) is retained as a hard gate.

## R3 hash ablation (top-32)

Status: NOT RUN (nothing to ablate). The B3 child failure
(H(var)/H(src) = 0.305 < 0.5) is baseline-inherited: the variant
rendered zero events, so its H equals the baseline's H exactly. The
baseline child render is spectrally duller than the source (texture at
the extractor's 0.15 mix; harmonic stack normalized by measured
mean). This is a property of the committed renderer, not an SA1
regression. It is reported as a B3 FAIL per the frozen bar text, with
this attribution. No rescue attempted; R3 does not apply.

## R4 dropout / weirdness

1. Meter f0 on src_speech = 121823 mHz (lag 362) vs the atom's
   commanded 466296 mHz (T0 94.575). INVESTIGATED: the atom's T0 came
   from a 1 s extraction window; the 5 s source's global autocorr
   peaks at 362 (~122 Hz). Per-chunk T0s (448, 185, 459, 358, 353)
   confirm the source is nonstationary; 362 is the energy-weighted
   compromise, not a meter bug. The render (driven at commanded f0)
   meters at 464211 mHz, within B4. KNOWLEDGE: global f0 estimates on
   5 s speech are window/method-dependent; the atom and the source
   honestly disagree.
2. Isolator T0 on child = 116 vs atom T0 112.16. Same cause, same
   conclusion. Not a bug.
3. Variant == baseline byte-identical on all 6 renders. EXPECTED
   (0 events applied; the event loop is a no-op). The render path is
   otherwise the committed baseline path; determinism (B6) holds.
4. No NaN, no DC jump, no onset explosion, no clipping in any render.
   The meter's onset detector behaves monotonically (source > render
   on both atoms, as expected for onset-poor renders).

## Knowledge vs architecture: the verdict on the verdict

ARCHITECTURE (design flaw, frozen): SA1 as specified assumes a
signal that is globally periodic up to a single period. Natural 5 s
speech violates this; the residual is the signal; the contrast gate
fires on nothing. A short-time harmonic model (per-chunk T0, overlap
blend, or pitch-tracked phase lock) is a DIFFERENT mechanism with its
own prereg (SA1b), not a parameter change: it changes what the
isolator computes, the event semantics, and the cost model.

KNOWLEDGE (gained): (a) quantified nonstationarity of the two battery
sources (per-chunk T0 ranges, global-rrms sweep flat at signal rms);
(b) the 6x contrast gate is correctly calibrated against harmonic
residue (it rejected everything rather than leaking); (c) the
baseline render's HF deficit on child (B3) is pre-existing and bounds
what any transient channel can claim on H.

## Toolchain incidents (process, not science)

Two pinned-znc defects were found and worked around during this wave,
recorded in ~/AGENTS.md: (1) a name/layout-dependent _zag_print
miscompile for dynamic content (byte-identical body named print_i64
failed, named f passed; 10+ repros); all SA1 stdout now goes through
single-buffer cursor emits plus one raw write, and every binary's
output bytes were verified. (2) `as []f64` does not rescale .len
(stays byte count); benign here (indexed 0..n-1 only). (3) 4-byte
reads for 2-byte WAV samples run past EOF on the last sample
(panic); fixed with d_get16. None of these affect the verdict: the
0-candidate result comes from the frozen gate arithmetic on f64
state, verified through two independent programs (isolator and
checker agree: NEVT = 0).

No Python was invoked in this lane. Safebin guard held for the full
wave.
