# H1d sticker-test rerun — perception repair (2026-09-26)

Preregistered test: H1 (TNN is not conscious of the merge). Mapping: sees sticker
AS sticker → WEAKENED; sees AND fixes → KILLED; calls sticker one-animal → HOLDS.

## What was broken

Commit a545f308 (repair of the empty-text panic) shipped `docs/lab/fusion-forkb/forkb.zag`
with a narrowed head ROI (y 0..220, x 100..220) and a ≥1000px graft-area gate, but the
**binary used to produce the delivered verdict was stale** — built from the pre-repair
source with the wide ROI (y 0..239, x 0..319). The stale binary measured the background
tree as the "graft" (area 3341) and judged the true one-animal control a STICKER.

Rebuilding from the committed source fixed the discrimination with no source change:
- experimental (step-6 f12): graft_area=5145 → STICKER
- control (recipient f12): graft_area=484 (<1000 gate) → ONE_ANIMAL

## Perception hardening (this commit)

White-box probing of the detector found the exact over-detection mechanism: `face_below`
counted any bright pixel (luma>180) below the graft — including blue sky below the
background tree (control raw face_below=1615, of which the saturation gate keeps 496).
Fix: `face_below` now requires low saturation (|B−R|<40, |G−R|<40), i.e. fur/skin,
not sky. Step-6 keeps 1863/1877 (real fur face); the control's sky is excluded.

Two further candidate discriminators were tested and FALSIFIED by measurement —
recorded so nobody re-tries them blind:
- edge/interior texture ratio ("pasted = crisp edge + flat interior"): blob ratio 3.7,
  tree ratio 3.5. The real graft is textured dark fur; the hypothesis is wrong.
- boundary step-direction consistency (dark-inside/bright-outside): blob 0.44,
  tree 0.39. Does not separate.

## Final result (binary built from this commit's source, znc pinned toolchain)

- EXPERIMENTAL step-6 f12 fnv1a=6288476374746440440:
  graft_area=5145 seam_crisp_x1024=56813 face_below=1863 neck_gap=0 → **STICKER**
- CONTROL recipient f12 fnv1a=4795319804440416442:
  graft_area=484 seam_crisp_x1024=0 face_below=0 neck_gap=0 → **ONE_ANIMAL**
- H1d VERDICT: TNN sees its sticker AS a sticker and the control as one animal.
  H1 (not-conscious-of-the-merge) is **WEAKENED**.
- Determinism: two independent runs, verdict files byte-identical
  (sha256 7e2edb8dacb0c6b70ead653c61569515d6825a79d23ebb460c06e75db8fd772f).

## Correction to the honesty section

The "H1D HONESTY DELIBERATION" prose in the verdict output (including the
"donor's face was NEVER observed" passage and the 0/24 face-visibility claim) is
crew-authored fixed wording emitted via tr_str, not a dynamically generated
reasoning trace — and `face_frames` is initialized but never updated, so the loop
does not compute the printed conclusion. It reads as TNN's own deliberation; it is
not. The pig-front extrapolation experiment must test actual machinery, not
scripted explanation.
