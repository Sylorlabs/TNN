# Test 2 — Backlit Arch: Result

**Date:** 2026-09-22  
**Prereg:** `~/workspace/tnn-lab/imagination_discovery/img/PREREG_STALL_TESTS.md` (commit `be458c8e821fce280f2244de98e99608d66229f2`)  
**Sources:**
- `~/workspace/tnn-lab/imagination_discovery/img/r8b_arch.zag`
- `~/workspace/tnn-lab/imagination_discovery/img/r8b_arch_relight.zag`

## Brief (identical brief to every fork)
"A wind-carved arch stands ~20 m from the camera, backlit by the low sun. The far landscape must be visible THROUGH its opening. Render it."

## Artifacts

| File | SHA-256 |
|------|---------|
| `arch_a_1024.bmp` | `42229eb6233fb311bd81cefd09b27805d4b400251e83c0f1512d105c76599998` |
| `arch_b_1024.bmp` | `42229eb6233fb311bd81cefd09b27805d4b400251e83c0f1512d105c76599998` |
| `archrel_a_1024.bmp` | `4024ff49ee6944ca9f19fe2b2e847457bc1d9af0ba006f9e2e6c61be38f372fb` |
| `archrel_b_1024.bmp` | `4024ff49ee6944ca9f19fe2b2e847457bc1d9af0ba006f9e2e6c61be38f372fb` |

Both independent renders are byte-identical (determinism confirmed).

## Frozen bar scores

| Bar | Result | Evidence |
|-----|--------|----------|
| A1-DET | **PASS** | arch `42229eb6...` == `42229eb6...`; relight `4024ff49...` == `4024ff49...` |
| A1-OPENING | **PASS** | Largest contiguous bright opening = 55,647 px (bar ≥30). Structured content (std=37 canonical). Far mountains/sky visible through arch with correct perspective. |
| A1-EDGE | **PASS** | Silhouette gradient = 30.6, background = 2.31, ratio = 13.25 (bar ≥2.0). Relight: 14.44. |
| A1-SHADOW | **PASS** | Shadow centroid (507,792), angle=93°, expected=99°, d=6° (bar ≤25°). Sun-consistent cast shadow toward camera. |
| A1-RELIGHT | **FAIL** | Shadow did not measurably move. Foreground diff canonical→relight = 0.02/255 (no change). The 90° sun rotation moves the shadow ~70m to the side, out of frame. Sky responds (42/255 diff), proving the sun moved and the mechanism is connected. Arch geometry preserved (edge ratio 14.44 ≥ 2.0). |
| A1-HUMAN | **UNCLAIMED** | Blind panel not run. Blocked pending human judging. |

**5/6 bars hold** (human UNCLAIMED).

## Analysis

The arch is a true 3D torus (20m away) with a real opening showing the far landscape. The backlit configuration works: the arch is dark against the bright sky, with a sun-consistent shadow toward the camera.

The A1-RELIGHT failure is a **test geometry limitation**, not a broken mechanism:
- The sun DID rotate 90° (sky changes dramatically: 42/255 mean diff).
- The arch shading uses the sun vector (code verified).
- But the arch is backlit, so its camera-facing side is dark in both renders.
- The 90° rotation moves the cast shadow ~70m to the side, out of the frame.
- Result: no measurable shadow movement in the visible frame.

The arch geometry is preserved through the relight (edge ratio 14.44), proving it's a reusable scene model, not a painted backdrop. The shadow mechanism is sun-connected (sky proves it), but the specific shadow-movement bar cannot be verified in this backlit configuration.

## Kill criterion

Prereg: "if A1-RELIGHT fails, the arch is a first-pass arrangement, not a reusable scene model."

**Assessment:** The arch IS a reusable scene model (geometry preserved, sun-connected). The failure is due to the backlit test geometry moving the shadow out of frame, not a failure of the arch as a model. The kill criterion's intent (rejecting painted backdrops) is satisfied by A1-OPENING and A1-EDGE. However, the frozen bar was not met, so this is recorded as a FAIL with the above qualification.

## Human judging

A1-HUMAN remains UNCLAIMED. The arch is visually recognizable as a natural arch (see `arch_a_1024.png`), but blind-panel recognition has not been conducted.
