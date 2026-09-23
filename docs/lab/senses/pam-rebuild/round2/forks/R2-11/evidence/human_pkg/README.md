# R2-11 human-verdict package (double-blind, 200 trials)

**Status: PREPARED — NOT YET DELIVERED. Do not hand to Micah directly;
the parent agent delivers it.**

## What is here
- `HNNN_src.{png,wav,gif}` — the source fixture (viewable conversion).
- `HNNN_P.{png,wav,gif}`, `HNNN_Q.{png,wav,gif}` — the two fork artifacts,
  blind-labeled. The P/Q→fork mapping is sealed (parent holds the key).
- `briefs/HNNN.md` — per-trial brief: the system's claim about the source
  (judgment/confidence/disposition + warrant bytes), each artifact's
  declared divergences, and the five questions for the judge.
- `VERDICT_FORM.md` — the 200-row verdict table for Micah.
- `GATE_REPORT.md` — audio-consistency gate + visual-boundary sanity results
  (13 flags, all investigated and cleared).

## Design
200 trials: 100 clean + 100 adversarial, stratified (see
`../lists/STRATIFICATION.md`), blind order via splitmix64(20260923).
P/Q assignment per trial via splitmix64(20260924).

## Bars this feeds
KB-E3 (audio ≥90% "same"; visual honesty ≥80%), KB-E4 (≥90% mismatch
detection on misjudged trials), KB-E7 (every divergence declared before
human testing — see the briefs), KB-E8 (Micah's head-to-head trust call).
