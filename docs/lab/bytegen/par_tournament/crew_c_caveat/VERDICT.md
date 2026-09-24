# CREW C-CAVEAT — verdict: contender C's CHOP-3 caveat (41 vs 29)

Date: 2026-09-24. Question (Micah): settle contender C's open caveat BY
EXPERIMENT — its servo adds flux-level spikes (41 vs 29 on CHOP-3).
Regression or not?

## Verdict: NOT-A-REGRESSION

The 12 "extra" flux spikes are not new transients the servo creates. They
are vibrato-extremum flux peaks that exist in PAR at 92–101% of C's
magnitude, counted only because CHOP-3's per-file adaptive threshold sits
11.6% lower on C's render (0.003533) than on PAR's (0.003995). At a common
fixed threshold the phenomenon inverts: C shows 13 spikes vs PAR's 29, and
no C variant's tallest flux peak exceeds PAR's own maximum (0.004701,
identical). The servo never puts energy anywhere PAR's natural transients
don't already reach.

## Experimental basis (each claim → the run that proves it)

1. **Reproduction (not vibes).** Rebuilt stock C from the frozen source
   (SHA-256 `0640f28f…a26c6d3db` verified) with the pinned znc; byte-identical
   reruns proven by `cmp`. With `~/workspace/aud_v10/chop.py` and an
   independently generated complete 296-event list: stock C = 41 total /
   0 unexplained, PAR = 29 / 0 unexplained. Both anchor counts reproduced
   exactly. (The dive's 271-event list was not found anywhere; the 296-list
   reproduces both anchors, validating the instrument for this experiment.)

2. **Causality — the servo is necessary for the count delta, but not via
   new transients.** Three forks, all byte-identical across reruns:
   - C-servo-unity (g ≡ 1, servo deleted): **29 spikes = PAR exactly**,
     byte-identical to PAR's own WAV. The extras require the servo.
   - C-servo-off (frozen at the plan-derived target g*=T/S, no dynamics):
     **53 spikes — worse than stock — and G-PER FAILS** (0.362 > 0.350).
     Removing the servo's *dynamics* (deadband + contraction) while keeping
     gain ≠ 1 increases stepping. The dynamics are load-bearing; the
     residual extras come from the gain *level* shifting the flux floor,
     not from adapt steps.
   - C-servo-smooth (512-sample linear ramp at adapt-block steps, full
     servo dynamics preserved: 146 adapts vs 137, gain envelope
     mean 1.0116 [0.877, 1.212] ≈ stock): **36 spikes, 9/9 gates PASS,
     RT-LONG honest-cents win preserved** (440.00 Hz, +0.0¢ vs PAR's
     1760/+2400¢), byte-identical reruns. The ramp kills 2 of the 9 C-only
     spikes (the 4.3654/26.3546 pair nearest the +6.2%/+8.7% adapt steps),
     adds zero new spikes, and shaves max flux 0.004701 → 0.004475.
     It cannot reach 29 because the remaining 7 are threshold artifacts,
     not step transients — no ramp can fix a threshold.

3. **Audibility (analyzers, not ears).**
   - Every C-only spike's flux peak exists in PAR at 92–101% magnitude;
     all 9 sit below PAR's smallest counted spike (0.0040).
   - At PAR's fixed threshold: stock 13 / off 8 / smooth 5 / unity 29 /
     PAR 29. No variant exceeds PAR's transient envelope.
   - The C−PAR difference signal at the extra-spike windows is harmonic
     (<2 kHz: 80–83%), not broadband: it is the servo's intended level
     correction, −34 to −42 dBFS, not a transient.
   - Quantitative conclusion: there is no transient energy in C that
     isn't in PAR. Nothing here is a candidate for an audible artifact
     beyond what PAR itself produces at those instants.

4. **Red team — faults injected AT the adapt boundary (t=4.7864 s,
   dg=−9.5%).**
   - 64-sample burst: veto fired, gain trajectory **bit-identical** to
     clean (0/1295 blocks diverged). The servo cannot be made to spike
     by a burst.
   - +0.1 FS DC for 2 s: veto correctly did not fire (inside the RMS
     band); servo tracked it as a level (gain −33.6% max, bounded),
     re-settled to ±3 LSBs within 0.8 s after the attack; CHOP-3 38,
     0 unexplained. An adversary can force a temporary bounded level
     duck, not spikes.

## What the caveat really is (correction to the honest disclosure)

The dive's disclosure said "the rest are servo-amplified vibrato extrema."
Measured: C's flux at those instants is 0.92–1.01× PAR's — **not
amplified**. The accurate statement: the servo lowers the whole-file flux
floor slightly (median 0.000789 vs 0.000879), which lowers CHOP-3's
adaptive threshold, which promotes 9–12 borderline vibrato-extremum peaks
over the line. The count delta is a measurement-threshold interaction, not
a sonic difference. (The "6 of 14 within 12 ms of an adapt boundary" claim
did not reproduce under the validated instrument: 0 of 9 C-only spikes
within 12 ms; nearest-step distances 25–218 ms.)

## Secondary findings

- Freezing the gain at the plan-derived target (the task's literal
  ablation) is strictly worse than the live servo: 53 spikes + a G-PER
  gate failure. The servo's deadband/contraction dynamics earn their keep.
  Do not ship the frozen variant.
- C-servo-smooth (512-sample ramp) is the new champion configuration
  **if** the tournament values minimizing the adaptive count: 36 spikes
  (fewest of any servo-carrying variant), 9/9 gates, RT-LONG win kept,
  servo dynamics and determinism intact. It does not reach 29 — nothing
  with gain ≠ 1 can, because the residual is a threshold artifact.
- Recommendation: keep the caveat disclosed but reword it per the
  correction above; adopt C-servo-smooth as the tournament candidate; do
  not treat the 41-vs-29 count as a regression signal in §6 — the frozen
  bar (0 unexplained) is the binding one and it passes with margin.

## Artifacts (all in `bytegen/par_tournament/crew_c_caveat/`)
- `src/render_c{,_off,_unity,_smooth,_cav}.zag` + pinned-znc binaries
  (binaries NOT committed); fork SHAs in RUNLOG.
- `results/chop3_{c,par,smooth}.txt`, `work/` (traces, logs, analysis
  scripts), `excerpts/` — 4 WITHHELD-NOT-FOR-REVIEW motif WAVs
  (servo-on / servo-off / servo-smooth / PAR). Committed; never presented.
- Method note: all WAVs via each renderer's own `seq` path; mixes at
  `seqmix`/`seq+mix`; determinism by `cmp` on every binary.
