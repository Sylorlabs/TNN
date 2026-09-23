# Consistency Gate — pre-delivery audio battery

**Standing rule (Micah, 2026-09-23):** before ANY audio clip reaches him, agents
must analyze the waveform and verify it is a consistent sound. Agents cannot
listen, but they can measure consistency. This gate is **necessary but not
sufficient**: passing earns a clip the right to reach his ears; his ears judge.

**Goodhart guard:** every bar below is calibrated against REAL field recordings,
not invented. Anchors (documented in `calibration/MANIFEST.md` — URL,
metadata, SHA-256, and gate measurements; the audio files themselves are NOT
committed, per the NoDerivatives / ShareAlike licenses):
- `aporee_kids_play_area.wav` — radio aporee 43393/49431, Wu Tsan-cheng,
  Pingtung Park kids play area, 134 s, stereo→mono 44.1 kHz
  (source: https://archive.org/details/aporee_43393_49431, CC BY-NC-ND 3.0)
- `garry_point_park.wav` — radio aporee 54343/62164, Thomas Evdokimoff,
  Garry Point Park BC, first ~200 s, stereo→mono 44.1 kHz
  (source: https://archive.org/details/aporee_54343_62164, CC BY-NC-SA 3.0)

Bars were set from the gate binary's own measurements on the anchors
(§4), at roughly 1.3–1.6× the max anchor value — margin, not tuned to fail
any particular render. The bars were adjusted during calibration while
measuring the anchors and v6, then FROZEN before any v7 rendering; v7 was
iterated against the frozen gate (mechanism fixes only, never bar changes).
Cross-checked: both anchors pass as 30 s excerpts; aporee also passes as
the full 134 s file. Garry Point full-length (~200 s) has NOT been run —
open calibration item, see below.

## 1. FAIL bars (any failure blocks delivery)

Gate-native values (binary: `src/gate.zag`):

| id | metric | bar | aporee 30s | garry 30s | aporee 134s | v6 bed-only | v6 full mix |
|----|--------|-----|-----------|-----------|-------------|-------------|-------------|
| G-PER | max env autocorr, lags 0.5–25 s | ≤ 0.35 | 0.261 | 0.104 | pass | **0.674 FAIL** | **0.373 FAIL** |
| G-STA | std of 1 s log-RMS | ≤ 3.0 dB | 1.93 | 0.73 | pass | 1.68 | **5.59 FAIL** |
| G-LURCH | std of 50 ms log-RMS | ≤ 5.0 dB | 3.65 | 2.03 | pass | 2.55 | **8.04 FAIL** |
| G-DRIFT | std of 1 s spectral centroid | ≤ 800 Hz | 418 | 522 | pass | 129 | 287 |
| G-FLUXm | max 1 s→1 s spectral flux (×1000) | ≤ 350 | 148 | 220 | pass | 183 | 239 |
| G-SIL1 | fraction of 50 ms windows < −60 dBFS | ≤ 0.02 | 0.000 | 0.000 | pass | 0.000 | 0.000 |
| G-SIL2 | longest < −60 dBFS run | ≤ 0.5 s | 0 | 0 | pass | 0 | 0 |
| G-CLIP | peak sample | ≤ 0.95 FS | 0.084 | 0.133 | pass | 0.041 | 0.351 |
| G-CREST | crest factor | ≤ 14 | 4.98 | 4.19 | pass | 7.13 | 10.45 |

Notes:
- G-PER is the decisive v6 failure: short-loop repetition (env autocorr 0.674
  at 1.60 s on the pure bed) is ~2.5–6.5× any real ambience. Real places do
  not pulse. The bar (0.35) sits 1.34× above the hottest anchor (0.261).
- G-STA/G-LURCH catch v6's event-heavy dynamic lurch (5.59/8.04 dB vs real
  0.73–1.93 / 2.03–3.65 dB). Anchors pass with ≥1.37× margin.
- G-DRIFT/G-FLUXm are guardrails, and they are HONEST: v6's timbre drift
  (287) and flux (239) sit *inside* the real-anchor envelope (418–522,
  148–220) — the independent FFT calibration agreed (v6 319 vs anchors
  328–397). A gate that failed v6 here would be Goodharting against reality.
  They catch only pathological spectral jumps.
- During development a 32-band log-spaced energy-centroid variant compressed
  real timbre drift ~30× and *inverted* the anchor/v6 order (anchor 12–16,
  v6 276). That metric was discarded, not barred around — see §4.
- THD-by-construction stays a design attestation: mastering must be
  limiter-only (no always-on waveshaper), recorded in the render's notes.

## 2. WARN (reported, never blocks)

| id | metric | note when |
|----|--------|-----------|
| W-ENDS | first-2 s / last-2 s mean vs clip mean | > 12 dB dip (possible dead head/tail) |
| W-DENSE | max onsets per 2 s (>6 dB jumps) | > 6 (unusually dense scoring) |
| W-DYN | 1 s RMS range | > 14 dB (wider dynamics than any anchor) |

## 3. What the gate caught (validation record)

- v6 full mix (`clips/b_alpha_kids_1e_f_v6opus.wav`): FAILS G-PER/G-STA/G-LURCH
  — the gate catches the exact defect Micah's ears caught ("inconsistent").
- v6 pure bed (forensic control): FAILS only G-PER — isolates the defect to
  the 1.6–1.75 s bed-loop repetition.
- Both real anchors as 30 s excerpts, and aporee as the full 134 s file:
  PASS everything. No false positives on reality. (Garry Point full-length
  not yet run.)
- v7 full mix (`clips/b_alpha_kids_1e_g_v7.wav`, 2026-09-23): PASSES all bars
  (G-PER 0.265, G-STA 2.82 dB, G-LURCH 4.10 dB) — two byte-identical renders
  (SHA-256 `8fb3501e5d28afd6a3cfd445ca8ebbcec1eaac615911a012ec6c94eab114eb98`),
  gate run on both with identical output. The v7 bed alone also passes
  (G-PER 0.156, G-STA 0.84 dB).

## 4. Open calibration items (not blockers for the frozen gate)

- Third reusable/CC0 playground anchor not yet obtained
  (candidate: freesound.org markystar 96348, described as CC0).
- Multiple independent 30 s windows per anchor not yet measured.
- Garry Point full-length WAV not yet gate-verified.
- Calibration audio must stay OUT of the repo (NoDerivatives/ShareAlike);
  only URLs, metadata, hashes, and measurements are committed.

## 5. Method (frozen with the binary)

- Envelope: 50 ms non-overlapping RMS windows, integer milli-dB
  (log2 fixed-point ×1024, then ×3010/1024), floor −120 dB.
- 1 s stats: non-overlapping 1 s RMS windows, same log domain.
- Spectrum: per 1 s window, 64-band linear Goertzel bank 0–11.025 kHz
  (centers (k+0.5)·172.27 Hz), magnitude-weighted centroid
  (Σf·√E/Σ√E); flux = RMS of consecutive per-band normalized-magnitude
  differences (×1000 for display).
- env autocorr: 20 Hz milli-dB envelope, mean-removed, normalized; max over
  lags 0.5–25 s.
- Onsets: > 6 dB rise between consecutive 50 ms windows; max per 2 s bin.
- Gaps: 50 ms windows < −60 dBFS; fraction and longest run.
- Applies to the delivered full-mix clip (16-bit PCM mono 44.1 kHz,
  ≥ 10 s; windows floor-divide).

## 6. Implementation

`src/gate.zag` — pure Zag, compiled with the pinned znc
(`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`) from the
`aud/b_alpha/` directory (imports resolve relative to cwd). Reads the WAV
path from argv[1], prints one line per bar
(`G-PER 0.373 bar 0.350 FAIL`), warns, then `GATE: PASS` / `GATE: FAIL (n
bars)`, exit code 0/1. Deterministic: integer log domain, closed-form
Goertzel, no RNG; two runs on the same file print byte-identical text
(verified 2026-09-23: two byte-identical v7 renders, identical gate output;
single-syscall line buffering; note common_v5's print_i64 emits a stray
newline on this znc build, so the gate formats lines itself).

## 7. Process

1. Render candidate → 2. run gate → 3. FAIL: fix the mechanism, never the
   bar → 4. PASS: attach the gate log when presenting to Micah. A bar change
   requires re-measurement on the anchors and a note here explaining why.
