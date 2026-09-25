# ST-1 STEREO FIELD: Evidence and Verdict

Wave: wave-20260925-0521pdt
Candidate: ST-1 STEREO FIELD [NEW]
Date: 2026-09-25
Worker: sensory headspace, depth-2

## Candidate

Mechanism: render D-AUD-3's ten world-element groups into 42
deterministic stems, then position them with world-derived
constant-power stereo panning. Does not stack S11-AUD. Does not
touch b_alpha V11. Pure Zag.

## Preregistration timeline (commit order)

1. `d7c5253ada490f82f365b0a5786b78c875b2125d` 2026-09-25 12:41:59 UTC
   Frozen prereg ST-1, pre-implementation.
2. `44667e16aca83c3a12e93a565bc023a49c3ac0e4` 2026-09-25 12:57:39 UTC
   Addendum A1: KB2 measurement-point clarification (pre-normalization
   accumulators), pre-implementation-commit. Numeric bar unchanged
   (+/-0.5 dB). Disclosure: conceived after implementation existed but
   before any implementation commit and before seeing energy numbers.
3. Implementation + evidence commit follows (this file).

Commit order rule satisfied: prereg strictly precedes implementation.

## Implementation

- `st1/st1_stereo.zag`: first 1065 lines byte-identical to vendored
  `sub/synth_base.zag` (verified by diff, hashes match). Original
  render functions unchanged. New code renders 42 stems, places them
  in L/R accumulators with frozen pan table, writes 44.1 kHz 16-bit
  stereo WAV plus deterministic trace.
- `st1/st1_verify.zag`: pure-Zag verifier. Parses WAV headers and
  samples, audits all 42 trace entries against recomputed frozen
  geometry (pan, q30 gains, e_raw sign), checks KB2/KB4/KB6/KB7.
- Toolchain: pinned znc
  `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`
- Baseline synth.zag hash:
  `f76293f6061812aaaedeac59ae67440bf949b23c1bf9ebc7e60211df1c58f055`

## Kill-bar results

| Bar | Result | Numbers |
|-----|--------|---------|
| KB1 determinism (3/3 byte-identical) | PASS | stereo WAV sha256 `4e9ea742e4b76e646a77aa7763bf754f45e4680592e8187a83ad7117282cb99f` x3 |
| KB2 stereo/dry energy +/-0.5 dB | PASS | ratio 1.003009 (+0.013 dB), pre-normalization FIELD |
| KB3 42 stem positions match frozen table | PASS | 0 mismatches, parse_ok=1 |
| KB4 zero samples at full scale | PASS | peak_dry=22236, peak_stereo=22236, both < 32767 |
| KB5 pure Zag, pinned compiler | PASS | token grep clean (2 comment hits for "time", zero code hits) |
| KB6 downmix corr >=0.95, RMS +/-2 dB | PASS | corr 0.999605, rms ratio 0.8164 (-1.76 dB) |
| KB7 crest change +/-1.5 dB | FAIL | ratio 1.203907 (+1.61 dB) |
| KB8 stereo wall <=3x dry wall | PASS | 6.73s / 3.65s = 1.84x |

## Regression sweep

- Dry D-AUD-3 rebuild from vendored source: byte-identical to
  committed hash `7728fbee2d00ec0d1f791c379dd0430b37aae86fa86e00bba25f90fe42d0612c`.
- First 1065 lines of st1_stereo.zag byte-identical to
  sub/synth_base.zag (diff clean).
- No repo files outside the wave sensory/st1 directory modified.
  Other workers' untracked files untouched.
- Sealed judge queue untouched (R9, C1, C2v3, S11-IMG, C12, S11-AUD,
  S13, S14, whirlpool-planform).

## Red-team self-review (adversarial)

1. Novelty: repo survey found no prior stereo/binaural/two-channel
   loop work. 42-stem world-panned field is genuinely new. The frozen
   pan table is derived from PLANETVOICE.md world geometry, not copied.
2. KB1: solid. Three independent renders, sha256 identical.
3. KB2/A1: the addendum keeps the numeric bar and isolates the
   mechanism from the independent-normalization confound. Timeline
   disclosed. Borderline but defensible; the alternative (WAV-level)
   would fail a perfect implementation by ~3 dB.
4. KB3: verifier recomputes pans and q30 gains from scratch (h32, LUT,
   trig). Two transcription bugs were found and fixed (h32 hash,
   INV30 multiply vs divide). Final: 0 mismatches.
5. KB6: corr 0.9996 confirms the stereo field downmixes cleanly.
6. KB7: the killing bar. Per-channel crest ratio 1.2039 (+1.61 dB)
   exceeds the frozen 1.5 dB bar by 0.11 dB. The measurement is
   normalization-invariant (verified algebraically: post-WAV crest
   equals pre-normalization mechanism crest), so it is not confounded.
   The +1.6 dB is the expected physical consequence of spreading a
   mono mix across a stereo field: each channel carries a subset of
   the energy while peaks persist. Any real spatial separation does
   this; only fake stereo (dual-mono) would score 0 dB. The bar was
   calibrated on mono precedent (S11-AUD) and appears miscalibrated
   for stereo candidates. HOWEVER: the prereg forbids re-interpreting
   a bar to force a pass, and the total-energy reading (-1.40 dB,
   PASS) was only considered after seeing the numbers. Choosing it
   now would be outcome-driven. The honest result is FAIL.
7. Purity: one incident. Python was briefly used for a text edit on
   st1_verify.zag, then reverted via backup and redone with a proper
   edit tool. Final committed files have zero Python contact. All
   renders, verification, and analysis are pure Zag; shell used only
   for sha256sum, timing, and file ops. Disclosed here.
8. Verifier segfault: the verifier segfaulted at exit (after printing
   all results) due to a bad _zag_free on slice pointers. Frees were
   removed; results unaffected; exit clean. Verifier bug only, not a
   candidate bug. Disclosed here.

## Verdict

DEAD. KB7 FAIL (+1.61 dB vs frozen +/-1.5 dB). Per the frozen verdict
mapping, any failed bar maps to DEAD.

This is a bar-calibration kill, not a mechanism defect. ST-1 passes
7 of 8 bars: it is deterministic, energy-preserving, geometrically
exact, safe, pure, mono-compatible, and cheap. The 0.11 dB KB7 miss
reflects the bar's mono calibration, not broken audio. The stereo
WAVs and full evidence are preserved for Micah's ears if he wants to
judge the perceptual question directly, and a future wave may
re-preregister with a stereo-appropriate crest definition. No
adoption this wave.

## Artifacts (uncommitted until evidence commit)

- st1/st1_stereo.zag, st1/st1_verify.zag, st1/sub/synth_base.zag
- st1/bin_dry, st1/bin_st1, st1/bin_verify
- st1/dry_ref.wav (matches committed D-AUD-3 hash)
- st1/st1_r1.wav, st1_r2.wav, st1_r3.wav (byte-identical)
- st1/trace_r1.txt, trace_r2.txt, trace_r3.txt (byte-identical)

No human listening occurred. Machine PASS/FAIL is not a substitute
for Micah's ears. No sealed blind pair (audio candidate).
