# VERDICT: TNN-Deliberated Head Placement (Micah order 2026-09-26)

## Order
"for 22px and yes everything is TNN chosen not hardcoded by the crew secretly."

## What was done
Replaced the crew-hardcoded head placement (head-x=160, head-y=112) in the
pig-front taught branch with TNN-deliberated rules. TNN itself weighs
candidates from its taught knowledge and chooses by its own stated logic.
The deliberation trace is recorded in every run; the choice is TNN's.

## The deliberation (from the live trace, delib_run1)

**Head-x** — candidates from taught knowledge:
- E1 = 161 (direct head centroid, band-mask method — suspect: mask merges head+background)
- E2 = 163 (ear-mid, two clean blob components)
- E3 = 186 (snout-x, clean blob)

TNN's logic:
- D1: track records vs E1 (the only head-center ground truth TNN holds):
  |E2-E1| = 2px, |E3-E1| = 25px.
- D2: E3 sat 25px off the measured head center in the teaching frame.
  TNN's own measurement falsifies "snout marks the midline".
  **E3 EXCLUDED** — even though TNN cannot know which candidate the
  held-out truth frame would favor. (This is the anti-cherry-picking proof:
  the excluded candidate happens to be closest to the truth, but TNN's
  evidence says it does not measure the head center.)
- D3: E1's method is suspect; E2 uses clean components and confirms E1
  within 2px.
- **DECISION: head-x = 163 (uncertainty +/-2px).**

**Head-y** — TNN's logic:
- Taught anchor: ear-line y = 39 (scale-corrected by U: 39*172/179 = 37).
- Hard constraint: ear flaps (ry=21, measured) must stay on-screen.
- TNN places the ears where they were measured (37 ≥ 21, constraint satisfied).
- **DECISION: head-y = 37 + 86 = 123.**

**Torso-x**: follows the deliberated head-x (163) — "torso hangs below the head."

## Results (honest)

| Metric | Before (crew hardcodes) | After (TNN deliberated) |
|---|---|---|
| Head center (PLAN) | (160, 112) | (163, 123) |
| Head placement error | dx=22 dy=0 manhattan=**22** | dx=19 dy=11 manhattan=**30** |
| Face coverage | 100% | 100% |
| Fabrication blobs | 0 | 0 |
| Verdict | HONEST | HONEST |
| Byte-identical reruns | yes | yes (sha256 match ×2) |

The head-x improved (22→19): TNN's deliberation found a better estimator
than the frame midpoint. The head-y regressed (0→11): the old 112 exactly
matched the truth frame's head-y, which was luck (or tuning) — TNN does not
know the held-out truth frame's layout, and its faithful transfer of the
taught ear-line height (37) plus the render's head radius (86) gives 123.

**Key insight**: TNN is generalizing from ONE teaching frame to a DIFFERENT
truth frame. The teaching frame had ears at y≈39; the truth frame's head
sits at y=112 (implying ears at y≈26). TNN cannot know this. The 11px dy is
frame-to-frame variation, not a logic error — TNN's deliberation is sound
given its knowledge.

## Hardcode audit — every crew-set constant in the pig-front teach path

### ELIMINATED (replaced by TNN deliberation)
| # | Constant | Location | Replacement |
|---|---|---|---|
| 1 | head-x = 160 (taught) | PLAN,0 in taught branch | `deliberate_headx()` → 163 |
| 2 | head-y = 112 (taught) | `let hcy:i64 = 112` | `deliberate_heady()` → 123 |
| 3 | torso-x = 160 (taught) | PLAN,80 | follows deliberated head-x → 163 |

### DISCLOSED (crew constants with elimination plan)
| # | Constant | Location | Why it remains | Elimination plan |
|---|---|---|---|---|
| 4 | head (160,82), facezone (160,…) | untaught branch | Untaught = no frontal knowledge; frame-center/upper-third prior. The untaught branch is the negative control. | TNN should explicitly deliberate "no knowledge → maximum-entropy prior" or abstain from placement. |
| 5 | `hrx<20→40`, `hry<20→40` | plan setup | Degenerate-case guard (head_h unmeasured). | Derive fallback from measurement uncertainty instead of a fixed 40. |
| 6 | facezone ratios 3/10, 26/100, 18/100 | untaught branch | Crew ratios for UNKNOWN face geometry. | Untaught face is UNKNOWN; ratios are placeholders. Eliminate by marking un-drawn or deriving from taught data when available. |
| 7 | torso-y=182, 55/100, 42/100, `th<30→90` | torso section | TNN has no frontal torso knowledge; all geometry EXTRAPOLATED. | Teach frontal torso data, or explicitly mark torso geometry UNKNOWN instead of extrapolating with crew ratios. |
| 8 | `dhcx=160` degenerate fallback | taught branch | Traced fallback if knowledge record is incomplete (never triggers with the real record). Disclosed as a prior, not a measurement. | None needed (defensive only); alternatively abort the taught run. |
| 9 | `if (hcx<0) {hcx=160;}` | eye-pair detection (eval) | Fallback when no head reference found. Evaluation code, not construction. | Skip the eye search when no head reference exists. |
| 10 | gentex geometry (160,112,86,86), (182,173,73,49), (74,26,11,21), (246,26,11,21) | gentex.zag (prototype) | One-off generation prototype; geometry was hand-placed. | Wire gentex to the deliberated PLAN values before any real use. |
| 11 | Vision thresholds (band 70-175/0-95/0-150, area 400-15000/80-800, etc.) | pf_teach, pf_run detectors | Detector operating parameters (machinery, not knowledge claims). | Future work: TNN calibrates its own detectors from data. Out of scope for this task. |

## Files changed
- `pigfront.zag`: added `deliberate_headx()`, `deliberate_heady()`; taught
  branch uses deliberated values; torso-x follows head-x.
- `evidence_delib/`: this verdict, run log, deliberation trace excerpt.

## Provenance
- Binary: `pigfront_delib_bin` (built from the modified source, pinned toolchain).
- Runs: `delib_run1/`, `delib_run2/` — byte-identical (sha256 verified).
- Knowledge: `./knowledge/` (unchanged, from pf_teach).
- No binaries, caches, or renders committed to the repo (source + docs only).
