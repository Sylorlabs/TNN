# PAR_DIVE §6 — Final Verdict Matrix

Frozen prereg: `docs/lab/bytegen/par_dive/PREREG_PAR_DIVE.md` (commit `9b5aefae`).
All evidence on branch `tnn-native-lab`. Rule: a tie keeps the native incumbent.

## Per-contender verdicts (audio)

| Target | Battery | Red team | §6 verdict |
|---|---|---|---|
| NATIVE (hybrid v2) | incumbent baseline | A1b sub-band corruption ATTACK_WORKS; A1c +0.05 FS DC shift ATTACK_WORKS (2.9M bytes, 0/1292 detected); A1d 512-sample zeroing ATTACK_WORKS; parser fail-open (14/14 malformed plans rc=0); 30 Hz cue → false 79 Hz ZCR → octave latch 880→110 Hz wrong | INCUMBENT — but wounded |
| A (pure-PAR end-to-end) | PARTIAL WIN: RT-LONG 440.00 Hz +0.00¢ vs native 453.75 Hz +53.27¢; RT-CASCADE 0 vs 5791 post-fault diffs; coherence 1.000000 vs 0.736557; 9/9 gates; 5-min drift byte-identical. **COST −46% single-threaded** (6.40s vs 4.38s; architectural — integer-division phase recompute vs carried add) | survives §5; parser fail-open | **NO OVERTHROW** (COST regression under §6 "no regression elsewhere") |
| B (PAR render, plan-seeded region state) | **OVERTHROW**: RT-LONG octave latch 880→440 at 0¢ (spectrally verified), near-miss/sub-octave/polyphone correct; COST 8.54s vs PAR 9.03s wall, same 20.1MB RSS; 9/9 gates (G-PER 0.336 < bar 0.350); coherence 1.000000; RT-CASCADE 0 post-cut propagation | determinism scare RESOLVED (redteam compared S1 vs S2 binaries — provenance artifact, 124/124 runs byte-identical); 10/10 region-leakage PASS; parser fail-open | **OVERTHROW — stands** |
| C (bounded-feedback AR / Grok H3) | overthrow on the letter: RT-LONG 440.02 Hz (+0.1¢) vs PAR 880.04 Hz (+1200.1¢); 9/9 gates; coherence 1.000000/0.999999; RT-CASCADE 0 post-cut; COST tie | inherits parser fail-open + 30 Hz trap; 1292-block sustained corruption 1295/1295 vetoed, gain trajectory bit-identical to clean | **OVERTHROW-WITH-CAVEAT**: CHOP-3 shows 41 vs 29 flux spikes (all explained — servo gain-step transients); servo not sonically transparent at flux level; whether that is a "regression" is a judgment call |
| D1 (MR-BIDI) | TIE: bit-identical to PAR on the frozen battery; 9/9 gates; 15s window-cut extension is a documented bonus outside the battery | A-equivalent | **TIE — incumbent keeps** |
| D2 (PLANREF) | overthrow-with-caveat on the audio response task: near-miss RT-LONG latches exact 440 Hz — **0¢ honest error by construction** (re-render-verifies the cue window, then latches the plan's declared f0, no sensor in the loop) vs hybrid v2 abstain-to-nominal (76.7¢) vs PAR render-the-lie (1200¢) | immune to sensor attacks; adversarial plans abstain-or-correct; sustained corruption clean ABSTAIN | **OVERTHROW-WITH-CAVEAT**: no native binary existed, so NATIVE's RT-LONG was never re-measured — overthrow-vs-reference-behaviors, not overthrow-vs-measured-native; safety is plan-provenance all the way down |

## Per-path verdicts

| Path | Verdict |
|---|---|
| Audio | B wins the crown (region-seeded state + plan-derived RESPOND). A is the robustness champion but loses on throughput. |
| Image | PAR holds across images; current raster keeps local draw-order state; formation dominates end-to-end (19:1) — parallel formation is the ~5.5× prize, proven byte-identical. |
| Video (generative) | PAR holds (frame-parallel; frame f's plan never touches f−1). |
| Video (predictive) | state demanded. |
| Dialogue | **state demanded — pure-PAR loses**: genuine circularity (plan must precede rendering; dialogue history is produced by rendering). Formation is mixed parallel-dominant, but carried conversational state is required. |

## Cross-cutting findings (all targets)

1. **Parser fail-open is a family trait**: all six targets accept 1e9 amplitudes (signed rail), 1e18 Hz, negatives/non-numerics coerced, 200 events silently capped at 64. Loud rejection or documented bounds needed everywhere.
2. **v2 exception detector blind to content anomalies** (double-witnessed: redteam A1b/A1c/A1d + forensics): the [0.35×, 2.5×] RMS band detects energy anomalies, not content anomalies. D2's re-render-verification pattern is a candidate fix shape.
3. **30 Hz harmonic trap**: NATIVE and C (same ZCR sensor); B immune via 40–4000 Hz range gate (candidate fix for NATIVE/C).
4. **Genuine AR win on dense sums**: N=16 chord — AR servo self-limits (RMS 0.54 FS) while PAR's plan-exact sum clips at i16 from N=2 up. PAR renders the plan faithfully even when the plan asks for the impossible.
5. **"Repeat means identical bytes" is structural to event-relative phase**, not to carried-state rendering (global bin-oscillator phase-shifts repeats by frac(f·280) after 280 s).
6. **Formation is parallel, render is where the money is**: Micah's "left to right but it first plans parallelly" confirmed in audio/image/video; byte-identical shard reduction proven.

## For Micah's ears (all labeled NEW, all committed or in workspace)

- A: `excerpts/01_rtlong_compare.wav`, `02_motif_coherence.wav`, `03_polyphony.wav` (workspace)
- B: `contender_b/results/excerpts/NEW_B_motif_2s-5p4s.wav`, `REF_PAR_motif_2s-5p4s.wav`
- C: `contender_c/listen/` NEW_C_motif / NEW_PAR_motif / NEW_C_rtlong_resp / NEW_PAR_rtlong_resp
- D: `contender_d/excerpts/d1_boundary_fade.wav` + `d1_boundary_nofade.wav` (A/B pair), `d2_planref.wav`

## Open items (not for the dive — for Micah's decision)

1. Three stray `main` commits: `7e78a52b` (contender D), `fe245937` (contender C), `f9439784` (V2-C). Revert or keep?
2. B's inverted release envelope (`x=(rem*1024)/rel` runs the fade backwards) — deterministic, verdict-unaffecting, fix separately.
3. v2 detector redesign (DC/sub-band blindness) — candidate: D2's re-render-verification pattern.
4. 30 Hz sensor fix for NATIVE/C — candidate: B's 40–4000 Hz range gate.
5. Parser fail-open hardening for all six targets.
6. PAR's multi-core dividend unmeasured (single-threaded Zag binaries); A's COST regression is single-threaded.
