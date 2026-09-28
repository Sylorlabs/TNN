# Manifest — H1d rerender-loop repair (2026-09-26 ~21:10 UTC)

Branch: tnn-native-lab. H1: KILLED.

## Source
- `forkb.zag` — patched: op 8 REMOVE_GRAFT (subtractive render path), defect
  bit 6 STICKER, perfected `h1d_judge` wired into the teach loop as the pass
  condition, repair battery + fixed-series writer in `teach()`.
  Built with the pinned toolchain
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

## Docs
- `H1D_VERDICT_RERENDER_REPAIR.md` — white-box mechanism, repair, evidence, verdict.
- `H1D_VERDICT.md` — appended 2026-09-26 update pointer (history preserved).
- `H1D_RERENDER_REPAIR_GALLERY.html` — NEW-badged, self-contained (data URIs,
  zero external loads); before/after frames + computed critic measurements.

## Evidence (every number computed live by the binary)
- `h1d_teach_r3_trace.txt` — the closed-loop trace: R1 STICKER, R2 deliberates
  and applies REMOVE_GRAFT, R3 ONE_ANIMAL → PASS, repair battery 24/24.
- `h1d_fixed_battery.txt` — external `h1d` battery on the fixed series:
  0/24 STICKER (24/24 ONE_ANIMAL); control 24/24 ONE_ANIMAL.
- `h1d_teach_negative_control.txt` — clean bunny input: R1 ONE_ANIMAL,
  immediate PASS, REMOVE_GRAFT never proposed.

## Checks
- Determinism: two full teach runs byte-identical (diff -r clean).
- Selftest: 7/7.
- Baseline (unpatched source) rerun: MAX_ROUNDS, defects remaining — the wall
  reproduced before the repair.

## Not committed (regenerable per repo standard)
- Build binaries, `.zag-cache`, rendered frames (re-render from `forkb.zag` +
  sealed fixtures `frames/{donor,recip,step6}` in forkB-scratch).
