# EVIDENCE DP-1 DOPPLER FLYBY - wave-20260925-1721pdt

Candidate: DP-1 DOPPLER FLYBY [NEW]
Date: 2026-09-25. Worker: sensory headspace, depth-2.
Prereg: docs/lab/rsi/runs/wave-20260925-1721pdt/sensory/dp1/PREREG_DP1_1721.md
Prereg commit: 18ad30fe3 (frozen pre-implementation, committed alone).

## Provenance header (machine-checkable)

RENDER_SHA: 994f9402f387889dfe331afa51d0dab866b00ee873a5dfa3cd5a52123bd3c771
FIRST_RENDERED_WAVE: wave-20260925-1721pdt
COMPONENT_LINEAGE: D-AUD-3-substrate(synth.zag f76293f6061812aaaedeac59ae67440bf949b23c1bf9ebc7e60211df1c58f055, vendored byte-identical as sub/synth_base.zag); R9:QUEUED-UNJUDGED; C1:QUEUED-UNJUDGED; C2v3:QUEUED-UNJUDGED; S11-IMG:QUEUED-UNJUDGED; S11-AUD:QUEUED-UNJUDGED; S12:DEAD; S12b:DEAD; S13:QUEUED-UNJUDGED; S14:QUEUED-UNJUDGED; whirlpool-planform:QUEUED-UNJUDGED; B1:DEAD; DF-1:DEAD; C-D19:DEAD; G1:STOOD-DOWN; ST-1:DEAD; D-VID-1:STOOD-DOWN
NEW_KNOWLEDGE_CLAIM: A frozen constant-velocity flyby rendered through a time-varying propagation delay adds motion-based realism to the D-AUD-3 bed via doppler pitch fall, inverse-distance loudness swell, and lateral pan at linear resampling cost.
Tag: [NEW].

## Implementation

- sub/synth_base.zag: vendored D-AUD-3 substrate, sha256
  f76293f6061812aaaedeac59ae67440bf949b23c1bf9ebc7e60211df1c58f055,
  byte-identical to docs/lab/imagination_discovery/aud/synth.zag.
- dp1_flyby.zag: first 1065 lines byte-identical to sub/synth_base.zag
  (sha256 dc90784e8df016116283fd5e43622492170bb85d4f85feee3e4a3cd1cd8ea1b4
  both sides, verified). Appended DP-1 block (dp1_newcode.zagfrag) plus new
  main are the only differences. All render_* and score_aud3 byte-identical.
- dp1_verify.zag: standalone pure-Zag verifier (KB2/KB3/KB4/KB5/KB8).
- Toolchain: pinned znc
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef,
  flags --no-zagd --no-analyze --no-foreground-cache.
- Modes: bin_dp1 base | variant | probe.

Frozen mechanism params (per prereg): C=319, V=30, DMIN=15, T_CA=10.5,
D_REF=25, PREROLL=1.0, engine f0=48 NP=6 B=0.0008, throb 0.4 Hz depth 0.25,
DP_SCALE=0.09, TARGET_FLYBY_PEAK=8000.
Engine calibration (disclosed): src_q24_peak=644791348 measured at render,
CAL=8000/(0.09*1.6666667*(src_peak/512)), cal_x1e9=42349616, identical all runs.

## Kill-bar results (all frozen, none moved)

| Bar | Result | Numbers |
|-----|--------|---------|
| KB1 determinism 3/3 | PASS | variant WAV sha256 994f9402... x3; trace sha256 eb375fd6... x3 |
| KB2 no clipping | PASS | base_peak=21713, var_peak=21739, both < 32767, 0 clips |
| KB3 doppler ratio +/-3% | PASS | f_approach=52.500, f_recession=43.500, ratio_meas=1.207, ratio_exp=1.207 |
| KB4 crest +/-1.5 dB | PASS | crest_ratio=0.994 (bounds 0.84140..1.18850) |
| KB5 energy +/-2 dB | PASS | rms_ratio=1.007 (bounds 0.79433..1.25893) |
| KB6 pure Zag, pinned compiler | PASS | token grep zero hits in DP-1-authored code; znc 498abcb5 |
| KB7 cost <=2.0x baseline | PASS | variant 6.726 s / baseline 3.603 s = 1.867x |
| KB8 trace audit 210/210 | PASS | 0 mismatches at 1e-9 scale |

Verifier output (bin_verify, pure Zag): header_ok=1, fails=0.
Full output in dp1_verifier_out.txt.

## Artifacts (all local, never pushed)

- dp1_baseline.wav: D-AUD-3 bed, stereo dual-mono, fixed scale.
  sha256 a32ff18e8a359963152a090aa96ee16a32461dbf9632b9510e6bba4bdd224f7c
- dp1_variant_r1.wav (r2, r3 byte-identical): bed plus doppler flyby.
  sha256 994f9402f387889dfe331afa51d0dab866b00ee873a5dfa3cd5a52123bd3c771
- dp1_probe.wav: isolated flyby stem, mono (KB3 measurement).
  sha256 e20dbae75e266db301e4936415352c289b9f9e266611219f8db2d689e83b6f94
- dp1_trace.txt: 210 trajectory checkpoints, sha256
  eb375fd64aa9325d1f7cb8957ad38335c2e6ee0362231bc5c3aaaf37244e6712
- LISTENING_DP1.md: listening instruction for his ears.

## Regression sweep

- No repo files outside docs/lab/rsi/runs/wave-20260925-1721pdt/sensory/dp1/
  created or modified. Other workers' untracked files untouched.
- Sealed judge queue untouched (R9, C1, C2v3, S11-IMG, C12, S11-AUD,
  S13, S14, whirlpool-planform). DP-1 is NOT queued; his verdict decides.
- b_alpha, audio_principles, and all his frontier files untouched.

## Disclosures

1. Pre-prereg baseline characterization (disclosed in prereg): rendered the
   dry D-AUD-3 bed with a throwaway binary to measure bed_q24_peak=
   123529294 and bed_rms_q24=13791633.770, which set the frozen DP_SCALE=
   0.09 and TARGET_FLYBY_PEAK=8000. Characterization artifacts deleted.
2. Python contact (one instance): used `python3 -c` once to count dash
   characters in my own draft fragment (read-only, no modification, no
   analysis, no wave artifact written). All subsequent checks used grep.
3. KB3 measurement detail: the verifier lowpasses the probe with 2
   cascaded one-poles (k=0.0071, fc about 50 Hz) before zero crossings,
   because the 6-partial engine overcounts raw crossings. Documented in
   the verifier source.
4. Post-render comment edit: changed "time-varying" to "varying-delay" in
   one DP-1 comment to meet the strict KB6 zero-comment-hit bar;
   recompiled, re-rendered, all SHAs unchanged (comment-only).

## Verdict

READY-FOR-JUDGE. All 8 frozen bars pass. WAVs ready for his ears per
LISTENING_DP1.md. Not adopted, not queued; his verdict decides.
