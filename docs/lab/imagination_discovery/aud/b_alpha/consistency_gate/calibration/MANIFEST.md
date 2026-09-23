# Calibration manifest

Real field recordings the consistency gate's bars are calibrated against.
The anchors are CALIBRATION, not source material. Only this manifest —
URLs, metadata, SHA-256 hashes, and gate measurements — is committed.
The audio files themselves are NOT in the repo (NoDerivatives/ShareAlike
licenses); they live in the local calibration directory for measurement
only and must be excluded from every commit.

## Anchor 1 — children/playground

- File: `aporee_kids_play_area.mp3` (5,363,904 bytes) → decoded
  `aporee_kids_play_area.wav` (11,818,542 bytes), `aporee_kids_play_area_30s.wav`
- SHA256: mp3 `1bdf00548f532f143ff085a2c5f02f483ac8d15d0c7fc619718083f7fc7e0f67`
  / wav `24981f77ff52acb701f3e6957ece9c5b5ab8d53857887d7bc69bc0d717c79b77`
  / 30s `6adafbf0143df1c1721377cd8eaa7f25aa6305fb4be6d12c6268d28281738960`
- Source: https://archive.org/details/aporee_43393_49431 (radio aporee
  43393/49431), recorded by Wu Tsan-cheng, Pingtung Park kids' play area,
  2019-03-26. 134 s, stereo, 48 kHz MP3; decoded to mono 44.1 kHz 16-bit WAV.
- License per archive.org metadata: **CC BY-NC-ND 3.0**. NoDerivatives: do NOT
  use as render source material; do not redistribute as a derivative without
  resolving licensing. Measurements and hashes committed instead.

## Anchor 2 — park ambience

- File: `garry_point_park.mp3` (9,000,001 bytes, partial download) → decoded
  `garry_point_park.wav` (17,640,470 bytes), `garry_point_park_30s.wav`
- SHA256: mp3 `35b7e499f514e54921e0f4e7ef0f3ce33c60d7aac8cae9f04749c6d444d49f63`
  / wav `e286e604ab0bcdb6fd944d48005fc7e57952ae0cab30fcda9d44cd4993100ba1`
  / 30s `61063e66d6b9d1789bdfa21c2235cae0683732f48fbf6c3279267694c3cfa866`
- Source: https://archive.org/details/aporee_54343_62164 (radio aporee
  54343/62164), recorded by Thomas Evdokimoff, Garry Point Park / Scotch Pond
  BC, 2021-08-27. Decoded to mono 44.1 kHz 16-bit WAV.
- License per archive.org metadata: **CC BY-NC-SA 3.0**. Calibration use only.

## Gate-native measurements (frozen 2026-09-23, binary `src/gate.zag`)

Full-length runs: aporee 134 s PASS (all bars). Garry Point full-length
(~200 s) NOT yet run — open item; the 30 s excerpt passes.

| id | aporee 30s | garry 30s | aporee 134s | bar | bar/anchor |
|----|-----------|-----------|-------------|-----|------------|
| G-PER | 0.261 | 0.104 | pass | 0.35 | 1.34× |
| G-STA | 1.93 dB | 0.73 dB | pass | 3.0 dB | 1.56× |
| G-LURCH | 3.65 dB | 2.03 dB | pass | 5.0 dB | 1.37× |
| G-DRIFT | 418 Hz | 522 Hz | pass | 800 Hz | 1.53× |
| G-FLUXm | 148 | 220 | pass | 350 | 1.59× |
| G-SIL1 | 0.000 | 0.000 | pass | 0.02 | — |
| G-SIL2 | 0 s | 0 s | pass | 0.5 s | — |
| G-CLIP | 0.084 | 0.133 | pass | 0.95 | — |
| G-CREST | 4.98 | 4.19 | pass | 14 | — |

Independent Python cross-check (FFT-based, `/tmp/calibrate.py`): anchors
G-PER 0.106–0.201, G-STA 0.73–1.93 dB, G-LURCH 2.03–3.65 dB, centroid std
328–397 Hz, flux ≤ 0.00026 — same rank order as the gate on every bar.
