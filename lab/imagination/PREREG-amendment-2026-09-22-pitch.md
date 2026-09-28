# PROPOSED prereg amendment — human audio pitch-handle wording

Date: 2026-09-22. Status: **APPLIED 2026-09-22.** Approved under Micah's
standing test-governance rule (tests and their documentation fixes do not
require his approval); verifier-confirmed wording gap, behavior already
correct. Applied to `PREREG.md` §Q1 with a dated CORRECTION note. No
mechanism, bar, metric, question, or score changed; all recorded Q1/Q2/Q3
results stand as-is.

## The gap

`PREREG.md` §Q1 says the HUMAN audio vocabulary includes "pitch-bin
handle 4000–4047". The implementation (`src/imagine.zag`,
`ig_enc_pitch`) stores the ORDERED BIN INDEX (0–47), so in practice
human-mode Q1 scenes use values like 19/20 and Q2 designs use 19/20,
26/27.

## Behavior is correct — wording is not

- The stored values are disjoint from machine-mode Hz values
  (machine Q1: 210–540; machine Q2: 260/280, 420/430) in every scene,
  so GEN-2's mode-disjointness holds.
- Pitch order is preserved: the bin index increases monotonically
  with frequency, matching b_percept's pitch ordering, so rising /
  falling / arch contour queries answer identically whether the stored
  value is the handle or the index (all contour logic is ordinal).
- GEN-2 independently scored 12/12: every attribute word is in the
  mode's vocabulary as used.

The independent verifier (subagent, 2026-09-22) confirmed the same gap
and the same behavioral conclusion.

## Proposed change (wording only, no code, no rescore)

In `PREREG.md` §Q1, replace:

> pitch-bin handle 4000–4047

with:

> pitch-bin handle 4000–4047 (stored as the ordered bin index 0–47;
> monotone in frequency, disjoint from machine Hz values)

No mechanism, bar, metric, question, or score changes. All recorded
Q1/Q2/Q3 results stand as-is.

## Approval requested

Micah: approve / reject. On approval, rename to
`PREREG-amendment-2026-09-22-pitch.md` and commit.
