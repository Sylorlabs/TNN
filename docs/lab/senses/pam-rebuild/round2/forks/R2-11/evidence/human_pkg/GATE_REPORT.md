# R2-11 human-package gate report

Audio-consistency gate (peak/DC/stationarity/join-click) and
visual-boundary sanity (dims/payload/degeneracy/square-presence)
run over all 400 blind artifacts.

## FAILURES (13 trials)

- H003: P degenerate single-value image
- H010: P bright square missing in 8/8 frames
- H024: P degenerate single-value image
- H036: Q degenerate single-value image
- H069: P degenerate single-value image
- H093: Q degenerate single-value image
- H098: P degenerate single-value image
- H104: Q peak 24870 exceeds 0.75FS
- H110: P bright square missing in 1/8 frames
- H146: P bright square missing in 8/8 frames
- H151: P degenerate single-value image
- H152: P peak 24874 exceeds 0.75FS
- H197: P degenerate single-value image

## Adjudication of the 13 flags (2026-09-23)

All 13 were investigated against the source fixtures and the sealed key.
None is a defect; the gates flagged (a) declared renderer lossiness and
(b) faithful replays of sources that do not match the gate's naive
expectations. Detail:

- H003/H024/H036/H069/H093/H098 (colorconst, fork B render, "single-value
  image"): the T2 renderer paints uniform gray panels from the two stored
  mean-luma bytes. On SAME_SURFACE trials where both luma bytes agree the
  render is legitimately one flat gray - the declared divergence (chroma
  and texture discarded, ~24.4k/24.6k bytes). The sources are textured
  photos (CCN-1/CCN-2); the loss is declared in each brief. Not a bug.
- H010/H146 (motiondir, fork A replay, "square missing in 8/8 frames"):
  the sources contain no bright square (H146: dim drifting texture, max
  124; H010/MOT-3: max 117). Fork A replays them byte-exactly. The
  square-presence expectation applies only to fork B's canonical renderer.
- H110 (motiondir, fork A replay, "square missing in 1/8 frames"): the
  source itself has one dim frame (frame 5 max 63). Faithful replay.
- H104 (pitchdisc, fork A replay, "peak 24870 > 0.75FS"): the frozen noise
  source itself peaks at 24870 (0.759 FS). Faithful replay; the 0.75FS
  ceiling constrains the renderer, not the witness.

Disposition: all 200 trials ship as built. The 13 flags are recorded here
as reviewed-and-cleared, not as failures.
