# Fork B — T13/T13b Oracle Fix Report: the moon reads as a moon, the ridges resolve

Date: 2026-09-22. Branch: `tnn-native-lab`. Pure Zag, zero RNG.

## The two oracle verdicts

1. **Micah's eyes** (on `r8b_alien_1024.png`): the image reads human-made —
   watercolor, a PASS on the not-AI smell — BUT the moon "is a random black
   dot". "If it's a moon I guess it makes sense, if it's a sun it doesn't,
   or a star — stars should have light." T12's "legible crescent" was
   pixel-measurable yet eye-invisible at display size: the trace overclaimed,
   and the methodological failure is that depiction judged deliberation in
   pixel statistics, not at the size a human sees.
2. **Other humans' eyes** (shown the image by Micah): AI — "because the
   mountains cut off weirdly". The massif's west flank and the right hills
   hit the frame edges as truncated ridge silhouettes. This overturns the
   earlier solo human-made read; their eyes are the binding signal here.

## What changed (moon only + composition only; style untouched)

**T13 — moon reconception** (`b_moonx/y/z`, `b_moonhit`, `b_moonshade`):
- Elongation ~44° → ~52° (bold crescent, ~19% lit instead of ~14%)
- Disc radius 55 → 80 (~122px at 1024, ~30px at phone-screen size)
- Planetshine strengthened ~2.2x (0.16/0.14/0.15 → 0.34/0.32/0.33), so the
  dark side reads as a world, not a hole in the sky
- `mlen` now computed from the direction accessors (the old hardcoded
  squared components would have silently desynced)
- Phase still computed from the T1 sun, never painted; earthshine remains
  the only secondary light

**T13b — edge taper** (new block in `b_hfull`):
- Past the near ground (depth gate 220 — foreground rubble untouched),
  relief eases toward smooth lowland (−15) as the view ray nears the
  lateral frame edge (smoothstep on edge fraction × depth ramp)
- View axis derived from the T9 camera (eye → look target), never placed
- Landforms resolve into hazy low ground before the border instead of
  being sliced mid-stroke

## Display-size acceptance evidence

`moonfix_accept_256.png` — the final 1024 render downsampled to 256px
wide (phone-screen scale):
- Moon: bright amber lit limb on the sunward (left) side, full dark disc
  with subtle maria variation readable against the violet sky —
  unambiguously a crescent moon, not a dot
- Left edge: massif slope descends into hazy low ground before the
  border; right edge: hills ease to smooth plain — no ridge line is cut
  mid-stroke at either edge
- Center composition (massif, peaks, rift, foreground) untouched;
  watercolor read preserved

## Mechanical bars (re-verified, exact)

| Bar | Result | Evidence |
|---|---|---|
| D-RES | PASS | 1024×1024 BMP, 3,145,782 bytes |
| D-SHARP | PASS | grad(O)=2.414, grad(B)=0.875, ratio=2.759 ≥ 1.20 |
| D-COMP | PASS | zero banned primitive tokens in `r8b_alien.zag` code (grep hits are comment prose only: the bar-documentation line, "mid-stroke", "dusk fill", "sky fill"; the shared verifier's FAIL flag is `var1_terminus.zag`, another crew's file) |
| D-DET | PASS | two independent clean 1024² renders byte-identical: SHA-256 `3829e21610cd9f3d35defe77fad3fae8aaecdc132a42b8291a66550237ffaefc` |

Build: pinned znc `znc_linux_x86_64_abed8aa1`, `--no-zagd --no-analyze`,
native binary 75,441 bytes, 0 external build tools. Compiled binary,
`.zagd` and cache files NOT committed.

## Deliverables (this commit)

- `imagination_discovery/img/r8b_alien.zag` — unified trace with T13/T13b
- `imagination_discovery/img/r8b_alien_1024.bmp` — canonical output
- `imagination_discovery/img/r8b_alien_1024.png` — preview
- `imagination_discovery/img/UNIFIED_TRACE.md` — trace with T13/T13b
- `imagination_discovery/img/FORKB_UNIFIED_REPORT.md` — report with T13/T13b
- `imagination_discovery/img/MOONFIX_T13_REPORT.md` — this file
- `imagination_discovery/img/moonfix_accept_256.png` — display-size evidence
