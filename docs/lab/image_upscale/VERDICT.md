# HONEST UPSCALE — verdict

**Question:** TNN reproduces the fixture byte-for-byte; can it upscale it —
construct pixels it was never given, from its own understanding?

**Answer: not yet — bicubic beats it by 3.9 dB, and the loss is honest and
diagnosed.** TNN 21.96 dB / SSIM 0.7039 vs bicubic 25.89 dB / SSIM 0.8157,
full-frame vs held ground truth. On the constructed (odd) pixels alone:
TNN 21.12 dB vs bicubic 25.87 dB.

## Where TNN wins

16 of 32 tiles, by +0.2 to +2.2 dB — the left side (brick building, bridge
arches) and top-right (sky, far buildings). White-box cause: where TNN's
SHAPES atoms self-match, its construction is BIT-EXACT. Regions 0, 1, 3
reproduce their observed pixels with RMSE 0.00 — the exemplar IS the
texture, so the 2x blocks carry true structure while bicubic merely
smooths. This is the imagination working as intended: TNN's vocabulary
contains the texture, so it constructs it exactly.

## Where TNN loses (and fabricates)

15 of 32 tiles, by -0.2 down to -17.5 dB. The catastrophic losses are the
center band (tiles (4,0),(5,0),(4,1),(5,1),(4,2),(5,2)) and the bottom row.
White-box cause: SHAPES-ZOOM forces each top-level 64x64 block to TAKE an
atom ("assign @64: 8 fixed blocks (take 8)" — no reject option). Region 2
(native (128,0)) took an atom that fits with RMSE 44.15. At native
resolution the residual channel hides this misfit; at 2x there is no
residual for constructed pixels, so the raw model error shows as a visible
checkerboard (even vs odd pixels differ ~18.6 levels on average). TNN
fabricates with confidence where its vocabulary has no matching texture.

**The architectural finding:** the forced-take means TNN commits to models
that don't fit, and the residual hides it. Imagination exposes it. This is
not a bug in the upscale — it is TNN's deliberation working as designed,
and the upscale makes the misfit visible. Fixing it means giving the top
level a reject/split option when no atom fits, or carrying a residual-like
honesty signal into construction.

## Other deliberation notes

- On the 256x92 observation TNN chose order SHAPES -> LINES -> SMOOTH and
  REVERTED SMOOTH (0.18/value vs the 9 bar). After SHAPES+LINES explained
  the downscaled image, planar leaves added nothing. The construction
  follows this deliberation (no SMOOTH render).
- INVENTED pixels: zero. SHAPES+LINES cover the whole frame; the fallback
  (nearest observed) never fired.

## Outpaint (phase 2, imagination)

64px on the right, built from the 3 committed border SHAPES regions' edge
columns (SMOOTH was reverted — recorded, not worked around; LINES not
extended by recorded decision). All 11,776 strip pixels labeled
CONSTRUCTED-SHAPES-EXTRAP — never presented as observed. The strip
continues the edge texture honestly; where the region fit is perfect the
seam is invisible, where it isn't the seam shows. Deterministic:
byte-identical across runs.

## Bottom line

TNN's understanding CAN construct pixels — bit-exactly where its
vocabulary matches. But where the vocabulary doesn't match, the forced-take
design fabricates, and a generic interpolator wins. The honest-upscale
test did its job: it showed exactly where TNN's imagination is real and
where it is bluffing, with the mechanism named. The next step is not a
better interpolator — it is a top level that can say "no atom fits" and a
construction path that stays honest when it does.
