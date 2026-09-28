# Video Fusion Step 6, Workstream 2: CROSS-VIEW — Verdict

## The wall (from step 5)
Side-view pig donor -> front-view bunny recipient is unfixable in a 2D
warp. Step 5's honest negative: the render is a sticker (black blob on the
bunny's face), because (1) cross-view unfixable in 2D, (2) not attached at
the neck, (3) renders as blob, (4) bunny's face remains. This workstream
attacked cause (1) via two honest paths.

## PATH A: view-matched donor footage — NEGATIVE
Searched the full 26 s source video (1 fps scan + full-res verification +
8 fps transition windows) and the web (Commons, Pexels, stock sites). The
pig's head is down in every available frame; no freely-licensed real
front-facing pig footage exists; capture is impossible on this VM.
Full report: `docs/PATH_A_REPORT.md`.

## PATH B: pose-normalized part model — FAKE (honest negative)
A 3D-ish head model that the warp could ROTATE into the recipient's view
cannot be earned from the observations: monocular 2D, one pose family
(head-down grazing), zero depth constraints, and the needed face
appearance is OCCLUDED in all 24 donor frames (the snout points at the
ground; eyes/snout-front/mouth never visible). Any depth assignment or
novel-view appearance is a programmer's sculpture, not an observation.
The only honest pose normalization available is 2D in-plane — which is
exactly what step 5's warp already does, and which demonstrably cannot
bridge a ~90° out-of-plane pitch gap with occluded anatomy.
Full white-box: `docs/PATH_B_WHITEBOX.md`.

## The render question
Neither path is real, so no new fusion render was produced. Rendering
either path would have required faking: mirroring the donor, sculpting a
3D model from a single view, or AI-generating a pig — all explicitly
banned by the brief. The honest output of this workstream is the two
negatives and the surviving wall, not a demo.

## Verdict against Micah's bar
**No head swap delivered.** The bar (ONE animal with the pig's head —
snout, ears, eyes recognizable, attached at the neck, posed and lit as one
creature) is unmet by this workstream, because the cross-view wall stands:

**THE SURVIVING WALL:** the donor's face is never observed. The pig's head
is pitched ~80° down (grazing) in every available frame while the
recipient's head is upright and front-facing. The ~90° out-of-plane gap
carries OCCLUDED anatomy (eyes, snout-front, mouth) that no 2D warp can
invent and no honest 3D model can earn from monocular single-pose
observations. Until view-matched footage exists (new capture) or a
genuinely multi-view observation set exists, the cross-view merge of this
pair is not achievable — in 2D or in honest 3D.

## What this workstream proved (the value)
1. The program can STOP looking for front-facing pig footage of this pair
   in existing sources — the search was exhaustive and the negative is
   definitive.
2. Nobody should build a "3D head rotator" for this donor — the white-box
   shows the required knowledge is not in the data. Any such demo would be
   a sculpture, and this document is the receipt.
3. The unblock is named precisely: new capture (pig head-up facing camera,
   3+ s continuous), or a different donor with front-facing footage.

## Determinism / reproducibility
- All analyses are deterministic (frame extraction via ffmpeg with fixed
  parameters; measurements via numpy, no RNG).
- Toolchain: pinned `znc_linux_x86_64_abed8aa1` (verified runnable;
  no rebuild needed — no code changed).
- Source base: byte-identical copy of step-5 `src/` (commit 9d4d83119);
  the fusion binary `fusion4_bin` (step-5 build) was smoke-tested
  (`selftest` rc=0) and NOT re-run: re-running the cross-view fusion
  would reproduce step 5's sticker, adding nothing.

## Files
- `docs/PATH_A_REPORT.md` — the footage search (local + web + capture)
- `docs/PATH_B_WHITEBOX.md` — why the rotation model can't be earned
- `docs/VERDICT_STEP6.md` — this file
- `evidence/` — scan sheets, transition windows, donor full-res frames,
  measurement tables
- `src/` — byte-identical step-5 source base (the code this workstream
  verified against; unchanged)
