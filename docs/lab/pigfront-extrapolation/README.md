# Pig-Front Extrapolation Experiment

**Date:** 2026-09-26  
**Order:** Micah ~12:52 PDT — "lets try an experiment — what does it think the front looks like based off the pig's side view and its limited view."  
**Hypothesis tested:** "All that's needed is learning" — the architecture is fine; missing learned knowledge is the gap.

## Question

What does TNN construct for the pig's unseen FRONT, given:
- 24 side/back donor frames (head down, eating; face never visible), and
- only knowledge legitimately held in TNN's committed store?

## Method

Pure Zag, zero RNG. Single binary (`pigfront.zag`), three phases:

1. **Phase 1 — Observe & Construct:** TNN observes all 24 donor frames with its own
   vision (luma masks, connected components, color measurement). It inventories
   its held pig-anatomy knowledge (P1..P6 propositions, verified NOT HELD via
   stimulus-tape grep and curriculum inventory). It deliberates region-by-region
   (head, face zone, ears, torso, legs, background), marking each OBSERVED /
   EXTRAPOLATED / UNKNOWN. It renders a constructed front view and an epistemic map.

2. **Phase 2 — Self-Critique:** TNN inspects its own construction with its Zag
   perception: M1 (unknown-zone marker check), M2 (head-color grounding),
   M3 (fabrication scan for sneaked dark blobs), M4 (eye-pair detector on
   construction), M5 (ear-flap detector). Verdict: HONEST or FABRICATED.

3. **Phase 3 — Truth Comparison:** Compare against Fork A's real frontal pig frame
   (different pig). Measure head placement error, face-zone coverage, and classify
   each miss as knowledge (absent proposition) vs machinery (failed where
   knowledge existed).

**Determinism:** Two runs, byte-identical outputs, SHA-256 verified.

## Preregistered Verdict Mapping

- **SUPPORTED:** Machinery correct where knowledge existed, every miss maps to
  absent knowledge, no fabrication.
- **WEAKENED:** Machinery failed where knowledge existed, or an unmapped miss.
- **KILLED:** Fabrication, or machinery failure where knowledge existed.

## Results

| Metric | Value |
|---|---|
| Frames observed | 24/24 |
| Head-down frames | 12/24 |
| Ear-flap frames | 17/24 |
| Eye-pair detector firings | 17/24 (side-view spots, NOT frontal faces) |
| Frontal faces observed | 0/24 |
| Head color (measured) | rgb(37,33,35) |
| Torso color (measured) | rgb(170,152,137) |
| Self-critique | HONEST |
| Head placement error vs truth | 52px manhattan |
| Face-zone coverage of true face | 10% |
| Hypothesis verdict | **WEAKENED** (ear detector sensitivity; all misses map to absent knowledge) |

## Key Findings

1. **TNN refused to fabricate a face.** With zero pig-anatomy propositions held
   and zero frontal views, it marked the face UNKNOWN (magenta stripes) rather
   than inventing eyes and a snout.

2. **The eye-pair detector is not a valid frontal-face test.** It fired 17/24 on
   side-view spot pairs (eye + light fur patches on the dark head), but found NO
   pair in the real frontal truth frame. The honest conclusion: 0/24 frontal
   faces observed, based on all frames being side/back views — not on the
   detector output.

3. **C3 (ears) failed on detector sensitivity, not construction.** The ears were
   observed (17/24) and rendered (visible in the construction), but the M5
   critique detector didn't find them. This is a detector limitation.

4. **Every miss maps to absent knowledge** (P1/P2/P4/P6 not held), not machinery
   failure. The machinery worked: colors grounded, head placed, ears inferred,
   honesty held.

## Conclusion

The missing piece is learned knowledge, not new architecture. Teach TNN pig
anatomy through its own intake, re-run, and the face should fill in.

## Files

- `pigfront.zag` — complete experiment source (pure Zag, zero RNG)
- `metrics.txt` — key measurements
- `trace_pigfront.txt` — full deliberation trace (5.4KB)
- `RUNLOG.md` — run log with SHAs

**Dependency:** `@import("R33_NATIVE_IO_V1.zag")` (standard TNN native IO, already in repo).

**NOT committed:** binaries, `.zagd` cache, run output PPMs (regenerable from source).
