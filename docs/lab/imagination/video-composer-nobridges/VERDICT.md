# No-bridges composer — VERDICT.md (2026-09-26)

## Headline: the no-bridges merge is worse than step-3 — and the trace shows exactly why.

## Side-by-side

| | no-bridges (invented segmentation) | step-3 (framed segmentation) |
|---|---|---|
| Bunny's way of seeing | Invented: **GRAY/MEDIAN@184** — won a 4-formula debate (F3 boundary-led, margin 5532, above-median on P/B/H) | Handed: motion>85th pct, gray<20th, gray>80th pct |
| Pig's way of seeing | Invented: **GRAY/VALLEY@96** — found the natural valley between the pig's dark/light histogram peaks itself (depth 3897 ≥ bar 663) | Handed: same three percentile recipes |
| "The subject" (own rule) | **"The part that moves most"** → bunny head *fragment*, 979 px (mean motion 1351 vs body 710) | motion-concentration × compactness → whole dark head+shoulders |
| Slot | Degenerate: fragment split 449/530 px; "body" won → 46×18 px slot | head-sized slot |
| Graft | 46×64 px pig-skin patch (donor scaled 0.27×) | head-sized pig-head graft |
| Seam (raw → adapted) | 129 → **64** gray levels | 158 → 72 gray levels |

## What eyes see (full frames, full duration — judged directly)

Step-3 reads as "a pig's head pasted over the bunny's face" — clearly
composited, but recognizably an attempt at the merge. No-bridges reads as "a
bunny with a dark smudge on its cheek" — a 46×64 px blemish that does not read
as a merge at all. **Worse as a merge.**

## Why it happened (the mechanism's own words, from the trace)

The subject principle — "the thing the video is about moves; the backdrop
does not" — is honestly applied and picks the highest-motion *piece*, which is
the bunny's head fragment, not the bunny. The fusion organ's slot machinery was
built for whole-body subjects; fed a 979-px fragment it produced a 46×18 slot,
and the donor got shrunk to a postage stamp. The invention (segmentation
method) is cleaner and better-evidenced than step-3's percentile recipes; the
failure is the **subject principle × slot interaction**, and the trace records
every step including the "unusual" slot pick.

## Exact remaining visual boundary

A 46×64 px dark pig-skin rectangle with an 8-px feathered edge on the bunny's
left cheek/neck; ~64 gray levels of luminance step after adaptation; pig-mud
texture visible inside, cream fur outside; no anatomical integration — it sits
*on* the cheek, and the bunny's ears remain untouched above it.

## Determinism (zero RNG in any decision path)

- trace sha256: `7b25d3892323f623c735d4c005d0e5dd45df83410d011ac2f163671ae1cd4fa2`
- frame_12 sha256: `b023b466dd00d2e5d1fd707999f6f4279d3b8f1d199b69bba91080d59a4afd6f`
- frame_00 sha256: `a4730771ffecfb4273569121d64c89181acff0079944064f73b9941ac8fc5545`
- frame_23 sha256: `97871c310e01e770996e23115902a84040b08702eb6fddb4a8c53e78883c6c41`
- Three independent runs (A, B, C): trace byte-identical, all 24 frames
  byte-identical (`cmp` verified).

## Candidacy for "better than step-3"

Rejected. The no-bridges composer invented a genuinely better *segmentation
method* than step-3's framed recipes — but its own subject principle then
undermined the fusion. A future round should keep the invention organ and
revisit the subject principle (piece vs animal) and the slot machinery's
assumptions about subject scale.
