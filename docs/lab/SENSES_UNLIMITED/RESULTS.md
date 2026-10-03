# SENSES_UNLIMITED — results (2026-09-22)

## Limits found → removed

| # | Human-range assumption (old) | Status |
|---|---|---|
| 1 | 24×24 RGB 0–255 field (`field.zag`) | REPLACED by u4f: unbounded W×H, 10 i64 channels/cell, values >1e6 legal |
| 2 | Silent `f3_clamp255` saturation | REPLACED: checked arithmetic saturates at i64 boundary AND sets SATFLAG bit |
| 3 | 48 semitone bins from 110 Hz; out-of-range dropped | REPLACED by ufreq: sparse atoms, any i64 Hz, nothing dropped |
| 4 | Frames clamped to 48, harmonics capped at 8 | GONE in ufreq (no frame/harmonic concept in atoms) |
| 5 | Fixed 8 kHz / 44.1 kHz emission rates | GONE in representation (atoms have no sample rate); 44.1 kHz exists only in declared human WAV rendering |
| 6 | Fundamental estimator 50–2000 Hz | GONE (no estimator in ufreq; atoms carry exact Hz) |
| 7 | Sample-rate floor 8 kHz rejection | GONE (no sample rate in atoms) |
| 8 | AVI 24-bit RGB only | Unchanged — AVI/BMP/WAV remain HUMAN RENDERINGS only, never the representation |

## Format status

- **u4f**: implemented, tested. 10 channels (R/G/B/UV/NIR/XRAY/DEPTH/ALPHA/ROUGH/SATFLAG),
  i64 per channel, checked arithmetic, SATFLAG on boundary. False-color emissions:
  HUMAN (RGB), BEE (UV→B, NIR→R, G→G), XRAY (grayscale). Render clipping counted
  in sidecar; field keeps true values.
- **ufreq**: implemented, tested. 40-byte atoms (Hz/amp/phase/t0_us/t1_us), i64 Hz
  (0..9.2e18 documented boundary), no Nyquist, 2.4 GHz as native data.
- **Remaining ceilings** (NOT called unlimited — reported as open):
  - `u4_alloc` caps W,H at 512 (engineering; needs chunked/dynamic storage)
  - `ufreq` arena caps at 1024 atoms (needs chunked/dynamic storage)
  - Frequency is i64 (max ≈9.22e18 Hz ≈ 38 MeV gamma; beyond is unrepresentable)
  - Time is i64 µs (±292,000 years)
  - Visual channels fixed at 10 (needs N-channel schema)
  - Emission oscillator is the fixed sine LUT (declared; waveform replacement is a separate track)

## Probes and measured fidelity

| Probe | Output | Result |
|---|---|---|
| P1 city-radio (14 atoms: AM/FM/GPS/WiFi/2.4G/5G) | 3 band WAVs + sidecar | Band A (AM, k=7): fidelity 0 pm. Band B (FM/GPS, k=17): 0 pm. Band C (GHz, k=19): 0 pm. All < 10 pm bar. |
| P2 bee-vision (64×64 u4f) | bee.bmp + human.bmp + sidecar | M1 UV nectar contrast = 1153 pm (115% — strong). M2 human-blue nectar contrast = -109 pm (≈0 — invisible to RGB). Proves UV structure hidden from RGB. Bee render clipped 2816 px (declared, counted); human clipped 113 px. |
| P3 2.4 GHz band (20 atoms) | WAV + sidecar | k=17, fidelity 0 pm, 0 lost pairs. 2.4 GHz survives exactly in atoms. |
| rt battery (5 checks) | stdout | ALL PASS: u4f roundtrip, ufreq roundtrip, satflag, arena-full, fidelity-bar. |

**Full-spectrum failure (preserved, not rewritten):** the first single-shift P1
(one k for AM..5 GHz) FAILED the fidelity bar — low bands collapsed while k was
chosen for the highest band. Repair: declared 3-band partition with per-band k
and rounding shift. Multi-band passes at 0 pm on all bands.

**WAV sanity:** all emissions mono 44100 Hz, fully bipolar (~50% negative),
thousands of zero-crossings, DC ≈ 0, peak 24000. No rectification (the old
`f3_get32` unsigned-reader bug is not present; peak is sign-correct i64).

## Determinism

Two complete clean runs: 9/9 output files byte-identical (WAVs, BMPs, sidecars).
Pure Zag, no RNG, no external tools. Binary: 120,298 bytes (main), built by
`toolchain/bin/znc_linux_x86_64_abed8aa1`.

## Bug found and fixed (mine, not the compiler's)

`u_write_named` opened files with `O_CREAT|O_EXCL` (flags 657602) — existing
files silently failed to open, so reruns never updated outputs. This masqueraded
as a "znc silently drops statements" compiler bug for ~30 minutes of debugging
(including a minimal reproducer that worked, deepening the confusion). Fixed:
flags 657986 (`O_CREAT|O_TRUNC`, no `O_EXCL`). Lesson: when output doesn't change,
check the file writer before blaming the compiler. The stale-file confusion is
documented here so it isn't repeated.

## Provider fallbacks (Grok-first, per Micah's directive)

| Attempt | Result |
|---|---|
| ExperientialLabs grok-4.7 (design prompts) | Timed out on long prompts; then HTTP 429 `insufficient_credits` (balance -$0.02) |
| UnoRouter gpt-5.6-sol (design) | Null choices / timeouts on long prompts |
| UnoRouter grok-4.6 (design) | Timeouts on long prompts |
| UnoRouter step-3.7-flash:free | 1 req/min free-tier limit |

No Grok-4.7 worker was usable for this track's design/red-team work. Implementation
proceeded natively after the required Grok-first attempts failed. No new
Muse-native workers were spawned.

## Red-team notes (native)

- Pitch-shift preserves RATIOS, destroys absolute pitch: two spectra 2× apart
  render identically. Declared casualty, not a bug — but the mapping is not injective.
- BEE false-color is one arbitrary convention among infinite; the claim is only
  that the mapping is linear and declared, not that bees "see blue".
- XRAY/DEPTH/ALPHA channels are implemented but unprobed (no X-ray scene yet).
- Render clip is impossible by construction (|v| ≤ 24000 < 32767); the atoms never
  clip. The "no silent clipping" law holds at both layers.
- k selection uses truncation while render uses rounding; edge case (rounded
  maxf hitting exactly 20000) is inaudible and documented.

## Files

- Source: `senses_unlimited/src/uspec.zag`
- Docs: `docs/lab/SENSES_UNLIMITED/AUDIT.md`, `SPEC.md`, `RESULTS.md` (this file)
- Deliverables for Micah: `~/workspace/your_files/senses_unlimited/` (4 WAVs, 2 BMPs, sidecars)
- Binary `uspec_bin` and `.zag-cache/` are NOT committed.
