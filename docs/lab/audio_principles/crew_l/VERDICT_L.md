# VERDICT L — Audio Principles, Closed-Loop Crew

**Battery verdict: L-PASS** (all three prereg §2.3 criteria met on all 3 runs;
LOOP-UNSTABLE not triggered; all protocol gates green).

- Date: 2026-09-25. Frozen prereg commit `f9748042bfbbbef3ee2a9b3f2d8d91f394efe79e`.
- Seal commit (design+sources+manifests, pre-test): `0b2c5d0bdbea`
- Amendment D1 seal (L01 90→133 Hz): `8960c44a2598`
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`, pure Zag.
- This verdict **informs** the four structural calls (§10); it does not decide them.

## Plain-language verdict

TNN can close the loop on its own audio. Given a pitch+envelope intent, its
native input organ ingested its own rendered WAV, measured a deviation from
the intent, and re-rendered — driving pitch error from ~1–2.6% down to
~0.0001% in three iterations, on all 20 held-out cases, three times
byte-identically. A second native loop did the same for a spectral target,
crushing an 8–16 kHz excess by 285–2308× to the measurement floor. This is
not open-loop generation: the correction decisions were computed in Zag from
the organ's own measurements of the previous render, with no Python in the
loop. What it is not: deliberative audio reasoning. The correction law is a
fixed deadbeat servo — it corrects, it does not contemplate. The
"conscious of audio" question stays with the perception prong; what L kills
is the claim that TNN *cannot* close a sensorimotor loop on audio at all.

## Battery results (prereg §2.3, 20 cases × 3 runs, frozen scorer)

| criterion | bar | run1 | run2 | run3 |
|---|---|---|---|---|
| (a) mean ERR(3)/ERR(0) | ≤ 0.80 | 0.000059 | 0.000059 | 0.000059 |
| (b) Wilcoxon one-sided ERR(3)<ERR(0) | p < 0.01 | 9.54e-07 | 9.54e-07 | 9.54e-07 |
| (c) strictly improved | ≥ 16/20 | 20/20 | 20/20 | 20/20 |
| (c) SHA(iter3) ≠ SHA(iter0) | all | 20/20 | 20/20 | 20/20 |
| (c) sign agreement (|dev|>1%) | ≥ 80% | 18/18 | 18/18 | 18/18 |

Wilcoxon: exact enumeration over 2^20 sign assignments, W+ = 210 (max), m = 20,
no ties, no zero-differences. p = 2^-20.

Per-iteration mean ERR (L-R1), all runs: **0.018845 → 0.000024 → 0.000001 →
0.000001** — monotone decreasing, converged by iter2, no sawtoothing;
LOOP-UNSTABLE not flagged. Per-case ERR(0) ranged 0.0096–0.0260 (the designed
1–2.9% quantization residual); ERR(3) ≤ 0.000003 everywhere.

Determinism (§2.4): 3 full protocol reruns — 240/240 render WAV SHAs and
60/60 loop logs byte-identical across runs. Zero RNG in the loop path
(source-audited: no rand/time/getrandom/rdtsc).

Dither check (§5.3): deterministic ×1.001 gain on all 20 run-1 iter0 renders →
native organ re-measurement stable 20/20 (same env class, |ΔF0|/F0 ≤ 0.5%;
bar was ≥19/20).

Organ self-check (§3.5): 10 frozen reference WAVs (pure, vibrato, two-tone,
−20 dB noise, tremolo, edge F0s) — organ-vs-scorer agreement 10/10 F0
(within 2%; actual agreement ≤0.01%) and 10/10 envelope class. The organ
faithfully replicates the frozen analyzer, *including its failure mode*
(see sensor characterization).

## HF-reduction diagnostic (native 8–16 kHz servo)

5 cases (HF tone 9/10/12/15 kHz at 3 starting gains + 440 Hz bed), pure-Zag
measure-and-attenuate loop, 3 iterations:

| case | b3r iter0 | b3r iter3 | reduction |
|---|---|---|---|
| H1 (9 kHz) | 198118e-6 | 206e-6 | ×962 |
| H2 (12 kHz) | 199504e-6 | 207e-6 | ×964 |
| H3 (15 kHz) | 199597e-6 | 207e-6 | ×964 |
| H4 (12 kHz, 2× gain) | 498536e-6 | 216e-6 | ×2308 |
| H5 (10 kHz, ½ gain) | 58963e-6 | 207e-6 | ×285 |

Gain converged to ~4–5‰ in all cases — the floor where the HF tone's residual
matches the pure-440 bed's own 8–16 kHz sidelobe leakage (b3r=190e-6). No
oscillation. The native band organ is a usable closed-loop error signal for a
spectral-balance target.

## Sensor characterization (divergence-as-data)

The self-check verified a **blind spot shared by the organ and the frozen
scorer**: the normalized-autocorrelation peak over lags 36..551 cannot resolve
F0 below ~125 Hz. Both implementations report the lag-36 edge (1225 Hz) for
true 82/110/115/117/120 Hz tones; 125 Hz resolves. This is a property of the
frozen measurement definition (triangular-window decay lets the lag-36
sidelobe beat the true-period peak), not a TNN implementation bug — organ and
scorer agree to the digit. Consequence: a closed loop has no error gradient
below ~125 Hz (it would diverge), so the battery's operating range is
[133, 1175] Hz. Any gate or metric anchored to this F0 definition inherits
the blind spot.

## Anti-gaming audit (§5)

- §5.1: 58 distinct test-render SHAs (240 files; duplicates are converged
  iter2=iter3 repeats, expected); test∩dev = ∅, test∩ref = ∅; no dev/ref SHA
  or prefix in any loop log or the argv log.
- §5.2: argv log (60 lines) — every invocation is exactly
  `[loop, case_id, pitch:<hz>, env:<class>, outdir]`; no measured value ever
  crossed into native argv/stdin.
- §5.4: Zag sources contain no scorer linkage (no `.py` references, no scorer
  file reads — file I/O is raw syscalls on WAV paths only); shared constants
  (2048/Hann/lags/0.40/thirds) are the public measurement definitions.
- §5.6: no `as []i32/u32/u16` (comment-only mention), no slice > 2^25 B,
  no RNG/time sources. Correction law is fixed arithmetic, identical for all
  cases — no per-case tuning possible.

## Deviations (documented, not silent)

- **D1** (sealed `8960c44a2598`, before any test render): L01 90 Hz → 133 Hz.
  Cause: the sensor blind spot above — 90 Hz is unmeasurable by the shared
  definition, so including it would test the sensor (already characterized),
  not the loop. Same selection rule, env cycle preserved (7/7/6); original
  manifest preserved in history.
- **D2** (chronology vs §5.3): the local loop source/binaries were built
  before the intent manifest was sealed — §5.3 wants targets sealed before
  the control path is built. Substance: the loop was built and frozen against
  a single dev render (440 Hz); the 20 targets were then selected by a
  mechanical rule (integer Hz, qerr∈[1%,2.9%]) the loop cannot see; the
  correction law is target-agnostic (dev = target − measured) with no
  per-case parameters, so no tuning-to-targets was possible; uniform
  deadbeat convergence on all 20 unseen cases is consistent with a general
  loop, not a fitted one. Recorded honestly; the seal-before-render barrier
  (§5.5) held end to end.

## Kill-table bearing

- Killed: "TNN cannot ingest its own render, detect deviation from intent,
  and correct it" — natively, in pure Zag, 20/20 × 3.
- Not killed: "audio is a shitty open-loop generator" in the strong sense —
  the loop corrects pitch/envelope/spectral-balance on synthetic tones via a
  fixed servo; deliberative audio reasoning (the consciousness question) was
  not tested here and stays with the perception/control prongs.
- New load-bearing fact: the F0 sensor's sub-125 Hz blind spot (shared
  definition property).

## Structural calls (informed, not decided)

1. **G4c source-relative reading (B-F3 → ears) vs re-anchor vs hold.** The HF
   loop is direct evidence that a source-relative spectral measurement (the
   organ's own 8–16 kHz band ratio) can serve as a closed-loop error signal
   natively and converge to the measurement floor. Feasibility of a
   source-relative G4c reading is supported by mechanism, not just by
   argument. Whether it should go to ears in that form is for the perception
   prong and Micah.
2. **Gate re-anchor amendment.** Concrete input: any gate anchored to the
   frozen autocorr F0 is blind below ~125 Hz — verified in both the native
   organ and the frozen scorer. If the gate's operating range includes low
   F0, it needs re-anchoring (different estimator or a range restriction);
   otherwise the blind spot stands as a documented limitation.
3. **B-F2 reuse-penalized DP re-test vs kill stands.** No bearing — L tested
   correction of fresh renders, not reuse-penalized DP. Stating this
   explicitly rather than stretching.
4. **B-F1 prosody-taming redesign.** Limited but real bearing: the envelope
   dimension (rise/decay/flat) was natively measured with 100% classification
   agreement and 20/20 dither stability, and the correction path never needed
   the envelope boost (boost=0 in all 60 iterations) because classification
   never failed. Envelope targets are a tractable native control dimension;
   prosody is far richer than three envelope classes, so this does not
   validate a prosody design — it only removes "envelope is unmeasurable"
   as an objection.

## Limitations

- Pure-tone stimuli; single-parameter (pitch) servo + 3-class envelope.
- The correction law is fixed arithmetic, not deliberation — L shows
  closed-loop control, not audio reasoning.
- F0 operating range [133, 1175] Hz (sensor blind spot below ~125 Hz).
- No ear claims made or makeable (agents cannot hear; waveform/analyzer
  evidence only).

## Evidence tree

- `docs/lab/audio_principles/crew_l/DESIGN_L.md` — frozen design
- `docs/lab/audio_principles/crew_l/BUILD_LOG.md` — build log + deviations D1/D2
- `docs/lab/audio_principles/crew_l/src/` — pure-Zag sources (core + 4 mains)
- `docs/lab/audio_principles/crew_l/frozen/scorer_l.py` — frozen scorer
- `docs/lab/audio_principles/crew_l/h/` — deterministic harness (genref/intent/run/score/dither/hf)
- `docs/lab/audio_principles/crew_l/manifests/` — intent (sealed, amended),
  ref, dev manifests
- `docs/lab/audio_principles/crew_l/ref_wavs/` — 10 frozen reference WAVs
- `evidence/` (this commit): `run1..3/{L01..L20}/{loop.log,loop.rc,*_iter{0..3}.wav}`,
  `runN/sha_table.json`, `runN/score.json`, `scores_summary.json`,
  `argv_log.jsonl`, `selfcheck.json`, `dither.json`, `dither/*_x1001.wav`,
  `hf.json`, `hf/{H1..H5}/hfloop.log`

Commits: seal `0b2c5d0bdbea` → amendment `8960c44a2598` → this verdict (3/3).
No binaries, no `.zagd`/cache files committed.
